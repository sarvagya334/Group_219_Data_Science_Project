#!/usr/bin/env python3
"""Unified macroeconomic hypothesis testing for the NSE sector-index universe.

This script evaluates the same macroeconomic hypotheses across a pre-specified
universe of long-history NSE sector/industry indices. It also tests whether exposure slopes
are different across index pairs using the paired return difference as outcome.
No external data is downloaded. Raw files under data/raw are never modified.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import warnings
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.stats as st
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN_INDEX = ROOT / "data" / "clean"
CLEAN_MACRO = ROOT / "data" / "clean" / "macro"
REPORTS = ROOT / "reports" / "macro_hypotheses"
FIGURES = REPORTS / "figures"
INDIVIDUAL = REPORTS / "individual_hypotheses"

INDEX_FILES = {
    'Nifty Auto': 'sector_indices/nifty_auto_clean.csv',
    'Nifty Bank': 'sector_indices/nifty_bank_clean.csv',
    'Nifty Commodities': 'sector_indices/nifty_commodities_clean.csv',
    'Nifty Energy': 'sector_indices/nifty_energy_clean.csv',
    'Nifty FMCG': 'sector_indices/nifty_fmcg_clean.csv',
    'Nifty Financial Services': 'sector_indices/nifty_financial_services_clean.csv',
    'Nifty Infrastructure': 'sector_indices/nifty_infrastructure_clean.csv',
    'Nifty IT': 'sector_indices/nifty_it_clean.csv',
    'Nifty Media': 'sector_indices/nifty_media_clean.csv',
    'Nifty Metal': 'sector_indices/nifty_metal_clean.csv',
    'Nifty Pharma': 'sector_indices/nifty_pharma_clean.csv',
    'Nifty Private Bank': 'sector_indices/nifty_private_bank_clean.csv',
    'Nifty PSU Bank': 'sector_indices/nifty_psu_bank_clean.csv',
    'Nifty PSE': 'sector_indices/nifty_pse_clean.csv',
    'Nifty Realty': 'sector_indices/nifty_realty_clean.csv',
    'Nifty Services Sector': 'sector_indices/nifty_services_sector_clean.csv',
}
HYPOTHESES = ["H1", "H2", "H3", "H4", "H5", "H6", "H7"]


def json_safe(value):
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, (pd.Timestamp, np.datetime64)):
        return pd.Timestamp(value).isoformat()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return float(value) if math.isfinite(float(value)) else None
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if pd.isna(value):
        return None
    return value


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_safe(obj), indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False).str.strip()
        .replace({"-": np.nan, "": np.nan, "nan": np.nan, "None": np.nan}), errors="coerce"
    )


def parse_date(series: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(series):
        return pd.to_datetime(series, errors="coerce")
    # `mixed` explicitly supports source CSV/workbook columns with more than one
    # textual date representation while keeping invalid values as NaT.
    return pd.to_datetime(series, errors="coerce", dayfirst=True, format="mixed")


def load_index_prices() -> tuple[pd.DataFrame, pd.DataFrame]:
    series = {}
    for index_name, filename in INDEX_FILES.items():
        path = CLEAN_INDEX / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing {path}; run `make clean-validate` first")
        df = pd.read_csv(path, parse_dates=["Date"]).sort_values("Date").drop_duplicates("Date")
        if df["Date"].isna().any() or df["Close"].isna().any() or (df["Close"] <= 0).any():
            raise ValueError(f"Invalid dates or close values in {path}")
        series[index_name] = df.set_index("Date")["Close"].astype(float).rename(index_name)
    prices = pd.concat(list(series.values()), axis=1, join="inner").sort_index().dropna()
    if len(prices) < 100:
        raise ValueError(f"Too few common index observations: {len(prices)}")
    returns = prices.pct_change(fill_method=None) * 100.0
    gaps = prices.index.to_series().diff().dt.days
    # Do not calculate one-day returns across an unexpectedly large source gap.
    returns.loc[gaps > 7, :] = np.nan
    returns.iloc[0, :] = np.nan
    prices.to_csv(CLEAN_INDEX / "sector_index_common_closes.csv", date_format="%Y-%m-%d")
    returns.to_csv(CLEAN_INDEX / "sector_index_daily_returns_pct.csv", date_format="%Y-%m-%d", float_format="%.8f")
    return prices, returns


def load_fx() -> pd.DataFrame:
    path = RAW / "Daily Exchange Rate of the Indian Rupee.xlsx"
    raw = pd.read_excel(path, sheet_name="Daily Foreign Exchange Spot Rat", header=5)
    cols = {str(c).strip().lower(): c for c in raw.columns}
    date_col = cols.get("date")
    usd_col = cols.get("us dollar")
    if date_col is None or usd_col is None:
        raise ValueError(f"Unexpected FX workbook columns: {list(raw.columns)}")
    df = pd.DataFrame({"date": parse_date(raw[date_col]), "usd_inr": numeric(raw[usd_col])})
    df = df.dropna(subset=["date", "usd_inr"]).sort_values("date").drop_duplicates("date", keep="last")
    df["usd_inr_change_pct"] = df["usd_inr"].pct_change(fill_method=None) * 100.0
    df.to_csv(CLEAN_MACRO / "usd_inr_daily_clean.csv", index=False, date_format="%Y-%m-%d", float_format="%.8f")
    return df


def load_cpi_and_derive_inflation() -> tuple[pd.DataFrame, dict]:
    path = RAW / "CPI - Rural, Urban, Combined.xlsx"
    xls = pd.ExcelFile(path)
    sheet = next((s for s in xls.sheet_names if "CPI - 2012=100" in s), None)
    if sheet is None:
        raise ValueError(f"Could not locate CPI 2012=100 sheet in {xls.sheet_names}")
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    # Source layout: month col 1, description col 2, status col 3,
    # combined CPI index col 8, published YoY inflation col 9.
    cpi = pd.DataFrame({
        "month_text": raw.iloc[7:, 1].astype(str).str.strip().to_numpy(),
        "commodity": raw.iloc[7:, 2].astype(str).str.strip().to_numpy(),
        "status": raw.iloc[7:, 3].astype(str).str.strip().to_numpy(),
        "combined_cpi_index": numeric(raw.iloc[7:, 8]).to_numpy(),
        "inflation_yoy_reported_pct": numeric(raw.iloc[7:, 9]).to_numpy(),
    })
    cpi = cpi[cpi["commodity"].str.upper().eq("A) GENERAL INDEX")].copy()
    cpi["date"] = pd.to_datetime(cpi["month_text"].str.upper(), format="%b-%Y", errors="coerce") + pd.offsets.MonthEnd(0)
    cpi = cpi.dropna(subset=["date", "combined_cpi_index"]).sort_values("date").drop_duplicates("date", keep="last")
    # Derive annual inflation from the CPI index itself, as requested, rather than
    # blindly adopting the precomputed inflation column supplied in the workbook.
    cpi["inflation_yoy_derived_pct"] = cpi["combined_cpi_index"].pct_change(periods=12, fill_method=None) * 100.0
    cpi["inflation_mom_derived_pct"] = cpi["combined_cpi_index"].pct_change(periods=1, fill_method=None) * 100.0
    cpi["inflation_yoy_lag1_reference_pct"] = cpi["inflation_yoy_derived_pct"].shift(1)
    comparable = cpi[["inflation_yoy_derived_pct", "inflation_yoy_reported_pct"]].dropna()
    audit = {
        "definition": "Derived CPI inflation YoY = 100 * (CPI_index_t / CPI_index_t-12 - 1).",
        "cpi_start_date": cpi["date"].min().strftime("%Y-%m-%d") if len(cpi) else None,
        "cpi_end_date": cpi["date"].max().strftime("%Y-%m-%d") if len(cpi) else None,
        "months": int(len(cpi)),
        "derived_yoy_non_null": int(cpi["inflation_yoy_derived_pct"].notna().sum()),
        "reported_yoy_non_null": int(cpi["inflation_yoy_reported_pct"].notna().sum()),
        "derived_vs_reported_comparison_n": int(len(comparable)),
        "derived_vs_reported_correlation": float(comparable.corr().iloc[0, 1]) if len(comparable) > 2 else None,
        "derived_minus_reported_mae_percentage_points": float((comparable["inflation_yoy_derived_pct"] - comparable["inflation_yoy_reported_pct"]).abs().mean()) if len(comparable) else None,
        "note": "The workbook's month is a reference period; a publication timestamp was not supplied. Same-month models are contemporaneous associations, not release-timed predictive tests. The lagged-reference model is only a timing sensitivity proxy.",
    }
    cpi.to_csv(CLEAN_MACRO / "cpi_inflation_derived_clean.csv", index=False, date_format="%Y-%m-%d", float_format="%.8f")
    return cpi, audit


def load_reserves() -> pd.DataFrame:
    path = RAW / "RBIB Table No. 33 _ Foreign Exchange Reserves - Weekly.xlsx"
    raw = pd.read_excel(path, sheet_name="Report 1", header=None)
    # Workbook columns: column 1 is week-end date; column 3 is Total Reserves USD millions.
    df = pd.DataFrame({"date": parse_date(raw.iloc[5:, 1]), "reserves_usd_mn": numeric(raw.iloc[5:, 3])})
    df = df.dropna(subset=["date", "reserves_usd_mn"]).sort_values("date").drop_duplicates("date", keep="last")
    df["reserves_change_pct"] = df["reserves_usd_mn"].pct_change(fill_method=None) * 100.0
    df["week_end"] = df["date"].dt.to_period("W-FRI").dt.end_time.dt.normalize()
    df.to_csv(CLEAN_MACRO / "fx_reserves_weekly_clean.csv", index=False, date_format="%Y-%m-%d", float_format="%.8f")
    return df


def load_repo_events() -> pd.DataFrame:
    path = RAW / "rbi_repo_rate.xlsx"
    df = pd.read_excel(path)
    required = {"Effective Date", "Repo Rate*", "Change (percentage points)"}
    if not required.issubset(df.columns):
        raise ValueError(f"Unexpected repo workbook columns: {list(df.columns)}")
    out = pd.DataFrame({
        "effective_date": parse_date(df["Effective Date"]),
        # Source represents 5% as 0.05 and 25 bp as 0.0025; convert explicitly.
        "repo_rate_pct": numeric(df["Repo Rate*"]) * 100.0,
        "repo_change_pp": numeric(df["Change (percentage points)"]) * 100.0,
    }).dropna(subset=["effective_date", "repo_rate_pct"]).sort_values("effective_date").drop_duplicates("effective_date", keep="last")
    out["decision"] = np.select([out["repo_change_pp"] > 0.00001, out["repo_change_pp"] < -0.00001], ["hike", "cut"], default="hold")
    out.to_csv(CLEAN_MACRO / "repo_rate_events_clean.csv", index=False, date_format="%Y-%m-%d", float_format="%.8f")
    return out


def load_gva() -> pd.DataFrame:
    path = RAW / "Quarterly Estimates of Gross Value Added At Basic Price (At Constant Prices) New Series (Base _ 2022-23).xlsx"
    xls = pd.ExcelFile(path)
    sheet = next((s for s in xls.sheet_names if "2022-23" in s), None)
    if sheet is None:
        raise ValueError(f"Could not find 2022-23 GVA sheet: {xls.sheet_names}")
    raw = pd.read_excel(path, sheet_name=sheet, header=5)
    raw = raw.loc[:, [c for c in raw.columns if not str(c).startswith("Unnamed")]].copy()
    year_col, q_col = "Industry/ Year", "Quarter"
    total_col = next((c for c in raw.columns if "GVA at Basic Prices" in str(c)), None)
    if year_col not in raw.columns or q_col not in raw.columns or total_col is None:
        raise ValueError(f"Unexpected GVA schema: {list(raw.columns)}")
    raw[year_col] = raw[year_col].ffill()
    raw = raw[raw[q_col].astype(str).str.strip().isin(["Q1", "Q2", "Q3", "Q4"])].copy()
    raw["financial_year"] = raw[year_col].astype(str).str.strip()
    raw["quarter"] = raw[q_col].astype(str).str.strip()
    raw["gva_constant_price_crore"] = numeric(raw[total_col])
    dates = []
    for fy, q in zip(raw["financial_year"], raw["quarter"]):
        m = re.match(r"^(\d{4})-(\d{2,4})$", fy)
        if not m:
            dates.append(pd.NaT); continue
        y = int(m.group(1))
        qn = int(q[-1])
        month = {1: 6, 2: 9, 3: 12, 4: 3}[qn]
        year = y if qn < 4 else y + 1
        dates.append(pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(0))
    raw["date"] = dates
    gva = raw[["date", "financial_year", "quarter", "gva_constant_price_crore"]].dropna(subset=["date", "gva_constant_price_crore"]).sort_values("date").drop_duplicates("date", keep="last")
    # The supplied file is explicitly the 2022-23 base-year series; do not splice in the old base-year workbook.
    gva["gva_yoy_growth_pct"] = gva["gva_constant_price_crore"].pct_change(4, fill_method=None) * 100.0
    gva["gva_yoy_growth_lag1q_pct"] = gva["gva_yoy_growth_pct"].shift(1)
    gva.to_csv(CLEAN_MACRO / "gva_quarterly_2022_23_base_clean.csv", index=False, date_format="%Y-%m-%d", float_format="%.8f")
    return gva


def load_iip() -> pd.DataFrame:
    path = RAW / "50 Macroeconomic Indicators.xlsx"
    raw = pd.read_excel(path, sheet_name="Monthly", header=3)
    raw = raw.loc[:, [c for c in raw.columns if not str(c).startswith("Unnamed")]].copy()
    if "Period" not in raw.columns or "Index of Industrial Production" not in raw.columns:
        raise ValueError(f"Monthly macro indicators missing expected fields: {list(raw.columns)}")
    text = raw["Period"].astype(str).str.strip()
    parsed_text = pd.to_datetime(text.str.upper(), format="%b-%Y", errors="coerce")
    df = pd.DataFrame({"date": (parsed_text + pd.offsets.MonthEnd(0)), "iip_index": numeric(raw["Index of Industrial Production"])})
    df = df.dropna(subset=["date", "iip_index"]).sort_values("date").drop_duplicates("date", keep="last")
    df["iip_yoy_growth_pct"] = df["iip_index"].pct_change(12, fill_method=None) * 100.0
    df["iip_yoy_growth_lag1m_pct"] = df["iip_yoy_growth_pct"].shift(1)
    df.to_csv(CLEAN_MACRO / "iip_monthly_clean.csv", index=False, date_format="%Y-%m-%d", float_format="%.8f")
    return df


def load_sp500() -> pd.DataFrame:
    path = RAW / "sp500_historical.csv"
    raw = pd.read_csv(path)
    raw.columns = [str(c).replace("\ufeff", "").strip() for c in raw.columns]
    if not {"Date", "Price"}.issubset(raw.columns):
        raise ValueError(f"Unexpected S&P 500 CSV columns: {list(raw.columns)}")
    df = pd.DataFrame({"date": parse_date(raw["Date"]), "sp500_close": numeric(raw["Price"])})
    df = df.dropna(subset=["date", "sp500_close"]).sort_values("date").drop_duplicates("date", keep="last")
    df["sp500_return_pct"] = df["sp500_close"].pct_change(fill_method=None) * 100.0
    df.to_csv(CLEAN_MACRO / "sp500_daily_clean.csv", index=False, date_format="%Y-%m-%d", float_format="%.8f")
    return df


def fit_hac(df: pd.DataFrame, target: str, predictors: list[str], focus: str | None = None, min_n: int = 8) -> dict:
    cols = [target] + predictors
    work = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(work) < min_n or work[target].nunique() < 2:
        return {"status": "insufficient_data", "n": int(len(work)), "min_n_required": min_n, "predictors": predictors}
    y = work[target].astype(float)
    X = sm.add_constant(work[predictors].astype(float), has_constant="add")
    maxlags = min(5, max(1, len(work) // 4))
    try:
        fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
        ci = fit.conf_int(alpha=0.05)
        coeff = {str(k): float(v) for k, v in fit.params.items()}
        p_values = {str(k): float(v) for k, v in fit.pvalues.items()}
        ses = {str(k): float(v) for k, v in fit.bse.items()}
        cis = {str(k): [float(ci.loc[k, 0]), float(ci.loc[k, 1])] for k in fit.params.index}
        focus = focus or predictors[0]
        return {
            "status": "tested", "n": int(fit.nobs), "r_squared": float(fit.rsquared),
            "coefficients": coeff, "standard_errors_hac": ses, "p_values": p_values,
            "confidence_intervals_95": cis, "focus_predictor": focus,
            "focus_estimate": coeff.get(focus), "focus_p_value": p_values.get(focus),
            "focus_ci95": cis.get(focus), "method": f"OLS with Newey-West/HAC standard errors (maxlags={maxlags})",
            "small_sample_warning": bool(len(work) < 30), "rows_dropped_for_missing": int(len(df[cols]) - len(work)),
        }
    except Exception as exc:
        return {"status": "model_error", "n": int(len(work)), "error": str(exc), "predictors": predictors}


def fit_one_sample_mean(values: pd.Series) -> dict:
    x = pd.Series(values).dropna().astype(float)
    n = len(x)
    if n < 2:
        return {"status": "insufficient_data", "n": n}
    mean = float(x.mean())
    se = float(st.sem(x))
    res = st.ttest_1samp(x, 0.0, nan_policy="omit")
    crit = float(st.t.ppf(0.975, n - 1))
    return {"status": "tested", "n": n, "mean_car_pct": mean, "sd_car_pct": float(x.std(ddof=1)),
            "se_pct": se, "ci95_pct": [mean - crit * se, mean + crit * se],
            "t_statistic": float(res.statistic), "degrees_freedom": n - 1, "p_value": float(res.pvalue),
            "method": "Two-sided one-sample t-test of event CAR mean = 0; effective dates are proxy event dates"}


def holm_adjust(p_values):
    out = [None] * len(p_values)
    valid = [(i, float(p)) for i, p in enumerate(p_values) if p is not None and np.isfinite(p)]
    valid.sort(key=lambda v: v[1])
    m, running = len(valid), 0.0
    for rank, (i, p) in enumerate(valid):
        running = max(running, min(1.0, (m - rank) * p))
        out[i] = running
    return out


def adjust_index_results(by_index: dict, p_field: str = "focus_p_value") -> dict:
    """Holm-adjust the per-index coefficient tests within the sector-index family."""
    adjusted = holm_adjust([fit.get(p_field) for fit in by_index.values()])
    for fit, p_adj in zip(by_index.values(), adjusted):
        fit["p_value_holm_across_indices"] = p_adj
        fit["reject_h0_after_holm_across_indices"] = bool(p_adj is not None and p_adj < 0.05)
    return by_index


def make_pairwise_slope_tests(panel: pd.DataFrame, outcome_by_index: dict[str, pd.Series], predictors: list[str], family: str, focus: str, min_n: int = 8) -> list[dict]:
    tests = []
    for a, b in combinations(INDEX_FILES.keys(), 2):
        diff = (outcome_by_index[a] - outcome_by_index[b]).rename("return_difference_pct")
        joined = pd.concat([diff, panel[predictors]], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
        fit = fit_hac(joined, "return_difference_pct", predictors, focus=focus, min_n=min_n)
        tests.append({
            "hypothesis_family": family, "index_a": a, "index_b": b,
            "null_hypothesis": f"The {focus} slope is equal for {a} and {b} (coefficient in return difference = 0)",
            "alternative_hypothesis": f"The {focus} slopes differ between {a} and {b}",
            "focus_predictor": focus, "slope_difference_estimate": fit.get("focus_estimate"),
            "p_value": fit.get("focus_p_value"), "ci95": fit.get("focus_ci95"), "n": fit.get("n", len(joined)),
            "status": fit.get("status"), "method": fit.get("method"), "small_sample_warning": fit.get("small_sample_warning", len(joined) < 30),
        })
    adjusted = holm_adjust([t.get("p_value") for t in tests])
    for t, p_adj in zip(tests, adjusted):
        t["p_value_holm_within_family"] = p_adj
        t["alpha"] = 0.05
        t["reject_h0_after_holm"] = bool(p_adj is not None and p_adj < 0.05)
    return tests


def load_monthly_returns(prices: pd.DataFrame) -> pd.DataFrame:
    monthly = prices.resample("ME").last()
    monthly_returns = monthly.pct_change(fill_method=None) * 100.0
    gaps = monthly.index.to_series().diff().dt.days
    monthly_returns.loc[gaps > 40, :] = np.nan
    monthly_returns.index.name = "date"
    return monthly_returns


def load_weekly_returns(prices: pd.DataFrame) -> pd.DataFrame:
    weekly = prices.resample("W-FRI").last()
    weekly_returns = weekly.pct_change(fill_method=None) * 100.0
    gaps = weekly.index.to_series().diff().dt.days
    weekly_returns.loc[gaps > 10, :] = np.nan
    weekly_returns.index.name = "week_end"
    return weekly_returns


def make_repo_event_study(prices: pd.DataFrame, returns: pd.DataFrame, repo: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    rows = []
    sessions = prices.index
    returns_pct = returns.copy()
    for _, event in repo.iterrows():
        effective_date = pd.Timestamp(event["effective_date"]).normalize()
        if effective_date < sessions.min() or effective_date > sessions.max():
            continue
        pos = int(sessions.searchsorted(effective_date, side="left"))
        if pos >= len(sessions):
            continue
        mapped_date = sessions[pos]
        # Estimation window: return observations t-120 through t-21, require >=80.
        est_start, est_stop = max(0, pos - 120), max(0, pos - 20)
        est = returns_pct.iloc[est_start:est_stop]
        # Event window returns at t-1, t, t+1.
        ev = returns_pct.iloc[max(0, pos - 1):min(len(returns_pct), pos + 2)]
        for index_name in INDEX_FILES:
            est_vals = est[index_name].dropna()
            ev_vals = ev[index_name].dropna()
            if len(est_vals) < 80 or len(ev_vals) < 3:
                continue
            exp_daily = float(est_vals.mean())
            car = float((ev_vals - exp_daily).sum())
            rows.append({
                "index": index_name, "effective_date": effective_date, "mapped_index_session": mapped_date,
                "mapping_lag_calendar_days": int((mapped_date - effective_date).days),
                "repo_rate_pct": float(event["repo_rate_pct"]), "repo_change_pp": float(event["repo_change_pp"]),
                "decision": str(event["decision"]), "estimation_n": int(len(est_vals)), "event_n": int(len(ev_vals)),
                "expected_daily_return_pct": exp_daily, "raw_3_session_return_pct": float(ev_vals.sum()),
                "car_minus_expected_return_pct": car,
            })
    event_df = pd.DataFrame(rows)
    if event_df.empty:
        return {"status": "insufficient_events", "eligible_events_per_index": {}}, event_df
    by_index = {}
    for name in INDEX_FILES:
        part = event_df[event_df["index"] == name].sort_values("effective_date")
        mean_test = fit_one_sample_mean(part["car_minus_expected_return_pct"])
        by_index[name] = {
            **mean_test,
            "events_by_decision": {str(k): int(v) for k, v in part["decision"].value_counts().items()},
            "mean_repo_change_pp": float(part["repo_change_pp"].mean()) if len(part) else None,
            "mean_mapping_lag_days": float(part["mapping_lag_calendar_days"].mean()) if len(part) else None,
        }
    pairwise = []
    pivot = event_df.pivot(index="effective_date", columns="index", values="car_minus_expected_return_pct")
    for a, b in combinations(INDEX_FILES.keys(), 2):
        pair = pivot[[a, b]].dropna()
        if len(pair) >= 2:
            res = st.ttest_rel(pair[a], pair[b], nan_policy="omit")
            diff = (pair[a] - pair[b]).astype(float)
            se = float(st.sem(diff)) if len(diff) > 1 else np.nan
            crit = float(st.t.ppf(0.975, len(diff) - 1)) if len(diff) > 1 else np.nan
            estimate = float(diff.mean())
            ci = [estimate - crit * se, estimate + crit * se] if np.isfinite(se) else None
            p_value = float(res.pvalue)
            status = "tested"
        else:
            estimate = p_value = None; ci = None; status = "insufficient_data"
        pairwise.append({"hypothesis_family": "H4_repo_event_car_pairwise_difference", "index_a": a, "index_b": b,
                         "null_hypothesis": "Mean paired difference in event-window CAR equals zero", "alternative_hypothesis": "Mean paired difference in CAR is nonzero",
                         "mean_car_difference_pct": estimate, "ci95": ci, "p_value": p_value, "n_matched_events": int(len(pair)), "status": status,
                         "method": "Paired two-sided t-test across matched repo effective dates; interpret as exploratory because event timestamps are not verified announcements."})
    adjusted = holm_adjust([t["p_value"] for t in pairwise])
    for t, p in zip(pairwise, adjusted):
        t["p_value_holm_within_family"] = p
        t["alpha"] = 0.05
        t["reject_h0_after_holm"] = bool(p is not None and p < 0.05)
    return {"status": "completed", "definition": "Event CAR is sum of daily returns in [t-1,t,t+1] minus 3 times the mean daily return in estimation window [t-120,t-21].", "effective_dates_are_proxy_event_dates": True, "by_index": by_index, "pairwise_tests": pairwise, "eligible_events_per_index": {k: int((event_df['index'] == k).sum()) for k in INDEX_FILES}}, event_df


def align_prior_us_sessions(indian: pd.DataFrame, us: pd.DataFrame) -> pd.DataFrame:
    """Match each Indian session to a US session strictly earlier than its date."""
    return pd.merge_asof(
        indian.sort_values("date"), us.sort_values("sp_date"),
        left_on="date", right_on="sp_date", direction="backward", allow_exact_matches=False,
    )


def build_macro_panels(prices, returns, fx, cpi, reserves, repo, gva, iip, sp500):
    panels = {}
    # H1 daily FX: same-date change is a contemporaneous association, not a release-timed prediction.
    fx_panel = returns.join(fx.set_index("date")["usd_inr_change_pct"].rename("usd_inr_change_pct"), how="inner")
    panels["H1"] = fx_panel

    # H2 month-end returns matched by CPI reference month. Both same-month and one-reference-month lag.
    monthly_returns = load_monthly_returns(prices)
    cpi_ix = cpi.set_index("date")
    h2 = monthly_returns.join(cpi_ix[["inflation_yoy_derived_pct", "inflation_yoy_lag1_reference_pct", "inflation_mom_derived_pct"]], how="inner")
    panels["H2"] = h2

    # H3 weekly index returns and reserves grouped into Friday-ending calendar weeks; include FX control.
    weekly_returns = load_weekly_returns(prices)
    res_week = reserves.groupby("week_end", as_index=True)["reserves_change_pct"].last().rename("reserves_change_pct")
    fx_week = fx.set_index("date")["usd_inr"].resample("W-FRI").last().dropna().to_frame("usd_inr")
    fx_week["usd_inr_change_pct"] = fx_week["usd_inr"].pct_change(fill_method=None) * 100
    h3 = weekly_returns.join(res_week, how="inner").join(fx_week[["usd_inr_change_pct"]], how="left")
    h3["future_reserves_change_pct"] = h3["reserves_change_pct"].shift(-1)
    panels["H3"] = h3

    # H5 GVA: map quarter's total constant-price GVA to its calendar quarter-end.
    qreturns = prices.resample("QE").last().pct_change(fill_method=None) * 100
    qreturns.index.name = "date"
    h5 = qreturns.join(gva.set_index("date")[["gva_constant_price_crore", "gva_yoy_growth_pct", "gva_yoy_growth_lag1q_pct"]], how="inner")
    panels["H5"] = h5

    # H6: industrial production growth as an additional supplied monthly macro indicator.
    h6 = monthly_returns.join(iip.set_index("date")[["iip_yoy_growth_pct", "iip_yoy_growth_lag1m_pct"]], how="inner")
    panels["H6"] = h6

    # H7 S&P500: for each Indian session, use the last US close strictly before it.
    ind = returns.copy().reset_index(names="date").sort_values("date")
    sp = sp500[["date", "sp500_return_pct"]].dropna().rename(columns={"date": "sp_date"}).sort_values("sp_date")
    aligned = align_prior_us_sessions(ind, sp)
    aligned["us_session_lag_days"] = (aligned["date"] - aligned["sp_date"]).dt.days
    aligned = aligned.set_index("date")
    for name in INDEX_FILES:
        aligned[f"{name}_lag1_pct"] = aligned[name].shift(1)
        # If the previous index return is missing, don't create a valid predictor from a gap.
        aligned.loc[aligned[name].isna(), f"{name}_lag1_pct"] = np.nan
    panels["H7"] = aligned
    for name, df in panels.items():
        df.to_csv(CLEAN_MACRO / f"panel_{name.lower()}_multi_index.csv", index_label="date", date_format="%Y-%m-%d", float_format="%.8f")
    return panels


def analyze_h1(panel: pd.DataFrame) -> dict:
    predictor = ["usd_inr_change_pct"]
    by_index = adjust_index_results({name: fit_hac(panel, name, predictor, focus=predictor[0]) for name in INDEX_FILES})
    outcomes = {name: panel[name] for name in INDEX_FILES}
    pairwise = make_pairwise_slope_tests(panel, outcomes, predictor, "H1_usd_inr_slope_difference", predictor[0])
    return {"id": "H1", "title": "USD/INR changes and daily index returns", "null": "USD/INR percentage change has zero linear association with same-date index daily return; for pairwise tests, its slope is equal across indices.", "alternative": "Association/slope is nonzero or differs by index.", "frequency": "daily", "outcome_unit": "percentage points per session", "predictors": predictor, "by_index": by_index, "pairwise_slope_tests": pairwise,
            "timing_caveat": "These are same-date daily observations. The supplied workbook does not establish exact FX observation timestamp relative to the Indian market close; treat results as contemporaneous associations, not predictive or causal effects."}


def analyze_h2(panel: pd.DataFrame) -> dict:
    predictor = "inflation_yoy_derived_pct"
    by_index = adjust_index_results({name: fit_hac(panel, name, [predictor], focus=predictor) for name in INDEX_FILES})
    lag_predictor = "inflation_yoy_lag1_reference_pct"
    by_index_lag = adjust_index_results({name: fit_hac(panel, name, [lag_predictor], focus=lag_predictor) for name in INDEX_FILES})
    pairwise = make_pairwise_slope_tests(panel, {name: panel[name] for name in INDEX_FILES}, [predictor], "H2_cpi_derived_yoy_slope_difference", predictor)
    lag_pairwise = make_pairwise_slope_tests(panel, {name: panel[name] for name in INDEX_FILES}, [lag_predictor], "H2_lagged_cpi_reference_slope_difference", lag_predictor)
    return {"id": "H2", "title": "CPI-derived inflation and monthly index returns", "null": "CPI-derived inflation has zero linear association with monthly index returns; paired alternative: inflation slopes are equal across indices.", "alternative": "Association is nonzero or inflation sensitivity differs between indices.", "frequency": "monthly", "inflation_formula": "100 * (combined CPI index this month / combined CPI index 12 months earlier - 1)", "by_index_same_reference_month": by_index, "pairwise_same_reference_month_slope_tests": pairwise, "by_index_one_reference_month_lag": by_index_lag, "pairwise_one_reference_month_lag_slope_tests": lag_pairwise,
            "timing_caveat": "CPI workbook supplies reference months and reported rates but no publication timestamps or expectations. Same-month analysis is contemporaneous and may use information published after some/all of the market-return month. One-reference-month lag is a timing sensitivity, not proof that the exact release was available before each return."}


def analyze_h3(panel: pd.DataFrame) -> dict:
    predictors = ["reserves_change_pct", "usd_inr_change_pct"]
    by_index = adjust_index_results({name: fit_hac(panel, name, predictors, focus="reserves_change_pct") for name in INDEX_FILES})
    future = adjust_index_results({name: fit_hac(panel, name, ["future_reserves_change_pct"], focus="future_reserves_change_pct") for name in INDEX_FILES})
    outcomes = {name: panel[name] for name in INDEX_FILES}
    pairwise = make_pairwise_slope_tests(panel, outcomes, predictors, "H3_reserves_controlled_slope_difference", "reserves_change_pct")
    lead_results = {name: {**fit, "diagnostic_only": True} for name, fit in future.items()}
    return {"id": "H3", "title": "Weekly FX reserves and index returns, controlling for USD/INR", "null": "Reserve-change coefficient is zero; paired alternative: coefficient differs across indices.", "alternative": "Reserve changes are associated with index returns or sensitivity differs.", "frequency": "weekly, Friday-ending buckets", "by_index_controlled": by_index, "pairwise_controlled_reserves_slope_tests": pairwise, "future_reserves_lead_diagnostic": lead_results,
            "timing_caveat": "The workbook provides reserve observation week-end but not first public-release timestamps. Same-week joins are contemporaneous associations. A significant future-reserve lead is a warning for common shocks, dependence or timing issues, not evidence of causality."}


def analyze_h4(prices, returns, repo) -> dict:
    summary, event_df = make_repo_event_study(prices, returns, repo)
    if "by_index" in summary:
        adjust_index_results(summary["by_index"], p_field="p_value")
    if len(event_df):
        event_df.to_csv(REPORTS / "h4_repo_event_car_by_index.csv", index=False, date_format="%Y-%m-%d", float_format="%.8f")
        # Event CAR distributions by category are shown descriptively; event count is small.
        plt.figure(figsize=(10, 5))
        for idx_name in INDEX_FILES:
            part = event_df.loc[event_df["index"] == idx_name, "car_minus_expected_return_pct"].dropna()
            if len(part): plt.hist(part, bins=12, alpha=0.35, label=idx_name)
        plt.axvline(0, linewidth=0.9)
        plt.title("H4: Three-session abnormal-return proxy around repo effective dates")
        plt.xlabel("CAR (%)"); plt.ylabel("Event count"); plt.legend(); plt.grid(axis="y", alpha=0.2)
        plt.tight_layout(); plt.savefig(FIGURES / "H4_repo_event_car_distributions.png", dpi=160); plt.close()
    return {"id": "H4", "title": "RBI repo-rate effective-date event study", "null": "Mean three-session abnormal return (CAR) around supplied repo effective dates equals zero; paired alternative: event CAR differs between indices.", "alternative": "Mean CAR is nonzero or CAR distributions/sensitivity differ across index segments.", "frequency": "event study", **summary,
            "caveats": ["Effective dates are not verified public announcement timestamps.", "The file may not be a complete official MPC decision calendar; holds and changes reflect supplied workbook only.", "Event CAR uses a simple mean-return benchmark, not a market model; treat results as exploratory.", "Overlapping event windows or macro shocks can induce dependence; paired comparisons are not causal."]}


def analyze_h5(panel: pd.DataFrame) -> dict:
    predictor = "gva_yoy_growth_lag1q_pct"
    same = "gva_yoy_growth_pct"
    by_index = adjust_index_results({name: fit_hac(panel, name, [predictor], focus=predictor, min_n=8) for name in INDEX_FILES})
    by_index_same = adjust_index_results({name: fit_hac(panel, name, [same], focus=same, min_n=8) for name in INDEX_FILES})
    pairwise = make_pairwise_slope_tests(panel, {name: panel[name] for name in INDEX_FILES}, [predictor], "H5_lagged_gva_growth_slope_difference", predictor, min_n=8)
    pairwise_same = make_pairwise_slope_tests(panel, {name: panel[name] for name in INDEX_FILES}, [same], "H5_same_quarter_gva_slope_difference", same, min_n=8)
    return {"id": "H5", "title": "Quarterly real GVA growth and index returns", "null": "Lagged GVA YoY growth has zero linear association with quarterly index returns; pairwise slopes equal across indices.", "alternative": "Association is nonzero or growth sensitivity differs across indices.", "frequency": "quarterly", "gva_measure": "GVA at Basic Prices, constant prices, 2022-23 base series supplied", "by_index_lagged_growth": by_index, "pairwise_lagged_growth_slope_tests": pairwise, "by_index_same_quarter_secondary": by_index_same, "pairwise_same_quarter_slope_tests_secondary": pairwise_same,
            "sample_warning": "The supplied 2022-23-base GVA series contains only a short quarterly history, so YoY growth has a very small effective sample. Treat all H5 inference as exploratory and underpowered; do not splice the separate old-base-year workbook without a documented official linking method.",
            "timing_caveat": "GVA quarterly release timestamps are not supplied. Lagging by one quarter is only a conservative proxy; the precise information set cannot be established from the provided workbook."}


def analyze_h6(panel: pd.DataFrame) -> dict:
    predictor = "iip_yoy_growth_lag1m_pct"
    same = "iip_yoy_growth_pct"
    by_index = adjust_index_results({name: fit_hac(panel, name, [predictor], focus=predictor) for name in INDEX_FILES})
    by_index_same = adjust_index_results({name: fit_hac(panel, name, [same], focus=same) for name in INDEX_FILES})
    pairwise = make_pairwise_slope_tests(panel, {name: panel[name] for name in INDEX_FILES}, [predictor], "H6_lagged_iip_growth_slope_difference", predictor)
    pairwise_same = make_pairwise_slope_tests(panel, {name: panel[name] for name in INDEX_FILES}, [same], "H6_same_month_iip_growth_slope_difference", same)
    return {"id": "H6", "title": "Industrial production growth and index returns", "null": "One-reference-month-lagged IIP YoY growth has zero linear association with monthly index returns; pairwise slopes equal across indices.", "alternative": "Association is nonzero or IIP sensitivity differs across indices.", "frequency": "monthly", "by_index_lagged_growth": by_index, "pairwise_lagged_growth_slope_tests": pairwise, "by_index_same_month_secondary": by_index_same, "pairwise_same_month_slope_tests_secondary": pairwise_same,
            "timing_caveat": "IIP source is the supplied macro-indicator workbook. Release timestamps and vintage/revision data are not supplied; lagged reference month is a timing proxy, not a real-time information-set test."}


def analyze_h7(panel: pd.DataFrame) -> dict:
    predictor = "sp500_return_pct"
    by_index = {}
    for name in INDEX_FILES:
        predictors = [predictor, f"{name}_lag1_pct"]
        by_index[name] = fit_hac(panel, name, predictors, focus=predictor)
    by_index = adjust_index_results(by_index)
    # Pairwise outcome differences are controlled for the difference in previous-session Indian returns.
    outcomes = {name: panel[name] for name in INDEX_FILES}
    pair_tests = []
    for a, b in combinations(INDEX_FILES.keys(), 2):
        diff = (outcomes[a] - outcomes[b]).rename("return_difference_pct")
        lag_diff = (panel[f"{a}_lag1_pct"] - panel[f"{b}_lag1_pct"]).rename("indian_lag_return_difference_pct")
        design = pd.concat([panel[[predictor]], lag_diff], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
        y = diff.reindex(design.index)
        joined = pd.concat([y, design], axis=1).dropna()
        fit = fit_hac(joined, "return_difference_pct", [predictor, "indian_lag_return_difference_pct"], focus=predictor)
        pair_tests.append({"hypothesis_family": "H7_prior_us_return_slope_difference", "index_a": a, "index_b": b,
                           "null_hypothesis": "Prior S&P 500 return slope equal across indices, controlling for differential own-lag return",
                           "alternative_hypothesis": "Prior S&P 500 return slope differs across indices",
                           "focus_predictor": predictor, "slope_difference_estimate": fit.get("focus_estimate"), "p_value": fit.get("focus_p_value"),
                           "ci95": fit.get("focus_ci95"), "n": fit.get("n", len(joined)), "status": fit.get("status"), "method": fit.get("method"),
                           "small_sample_warning": fit.get("small_sample_warning", len(joined) < 30)})
    adjusted = holm_adjust([x.get("p_value") for x in pair_tests])
    for t, p in zip(pair_tests, adjusted):
        t["p_value_holm_within_family"] = p; t["alpha"] = 0.05; t["reject_h0_after_holm"] = bool(p is not None and p < 0.05)
    return {"id": "H7", "title": "Prior US-session S&P 500 returns and Indian index returns", "null": "Prior S&P 500 return coefficient equals zero per index; paired alternative: sensitivity differs across indices.", "alternative": "Prior US market return is associated with index return or sensitivity differs across index segments.", "frequency": "daily", "by_index_controlled_for_own_lag": by_index, "pairwise_slope_tests": pair_tests,
            "alignment_rule": "For each Indian trading date, merge with the latest S&P 500 close strictly before that date (allow_exact_matches=False).", "timing_caveat": "The supplied S&P source is historical daily data; source/license and timezone conventions should be verified. Association is not causation or proof of a trading strategy."}


def make_macro_scatter_plots(panels: dict[str, pd.DataFrame]):
    """Create matched 2x2 descriptive scatter panels for each continuous macro hypothesis."""
    specs = {
        "H1_usd_inr_scatter.png": ("H1", "usd_inr_change_pct", "Daily USD/INR change (%)", "Daily index return (%)", "Same-date daily association"),
        "H2_cpi_inflation_scatter.png": ("H2", "inflation_yoy_derived_pct", "Derived CPI YoY inflation (%)", "Monthly index return (%)", "Same-reference-month association"),
        "H3_reserves_scatter.png": ("H3", "reserves_change_pct", "Weekly FX-reserve change (%)", "Weekly index return (%)", "Unadjusted plot; regression controls for USD/INR"),
        "H5_gva_scatter.png": ("H5", "gva_yoy_growth_lag1q_pct", "Lagged quarterly real GVA YoY growth (%)", "Quarterly index return (%)", "Very small sample; exploratory"),
        "H6_iip_scatter.png": ("H6", "iip_yoy_growth_lag1m_pct", "Prior-reference-month IIP YoY growth (%)", "Monthly index return (%)", "Release-date limitations apply"),
        "H7_sp500_scatter.png": ("H7", "sp500_return_pct", "Prior US-session S&P 500 return (%)", "Indian index daily return (%)", "Strictly prior US session; raw scatter"),
    }
    for filename, (hid, xcol, xlabel, ylabel, note) in specs.items():
        panel = panels[hid]
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        for ax, index_name in zip(axes.flat, INDEX_FILES):
            use_cols = [index_name, xcol]
            if hid == "H7": use_cols.append(f"{index_name}_lag1_pct")
            data = panel[use_cols].replace([np.inf, -np.inf], np.nan).dropna()
            ax.scatter(data[xcol], data[index_name], alpha=0.4, s=12)
            if len(data) >= 3 and data[xcol].nunique() > 1:
                slope, intercept = np.polyfit(data[xcol].astype(float), data[index_name].astype(float), 1)
                x = np.linspace(data[xcol].min(), data[xcol].max(), 100)
                ax.plot(x, intercept + slope*x, linewidth=1.25)
            ax.axhline(0, linewidth=0.6)
            ax.set_title(f"{index_name} (n={len(data)})")
            ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.grid(alpha=0.2)
        fig.suptitle(f"{hid}: {note}", y=1.01, fontsize=13)
        fig.tight_layout()
        fig.savefig(FIGURES / filename, dpi=160, bbox_inches="tight")
        plt.close(fig)


def make_macro_coefficient_plot(results: dict):
    """Plot coefficients/95% CIs in separate axes because predictor units differ by hypothesis."""
    plot_specs = [
        ("H1", "by_index", "usd_inr_change_pct", "USD/INR daily change"),
        ("H2", "by_index_same_reference_month", "inflation_yoy_derived_pct", "CPI-derived YoY inflation"),
        ("H3", "by_index_controlled", "reserves_change_pct", "Weekly reserve change (FX controlled)"),
        ("H5", "by_index_lagged_growth", "gva_yoy_growth_lag1q_pct", "Lagged real GVA growth (small sample)"),
        ("H6", "by_index_lagged_growth", "iip_yoy_growth_lag1m_pct", "Lagged IIP growth"),
        ("H7", "by_index_controlled_for_own_lag", "sp500_return_pct", "Prior US-session S&P 500 return"),
    ]
    fig, axes = plt.subplots(3, 2, figsize=(13, 12))
    for ax, (hid, key, focus, title) in zip(axes.flat, plot_specs):
        result = results.get(hid, {})
        by = result.get(key, {})
        ys, vals, lows, highs, ns = [], [], [], [], []
        for idx in INDEX_FILES:
            fit = by.get(idx, {})
            est = fit.get("focus_estimate")
            ci = fit.get("focus_ci95")
            if est is None or ci is None: continue
            ys.append(idx); vals.append(est); lows.append(max(0.0, est-ci[0])); highs.append(max(0.0, ci[1]-est)); ns.append(fit.get("n", 0))
        if vals:
            yloc = np.arange(len(vals))
            ax.errorbar(vals, yloc, xerr=np.vstack([lows, highs]), fmt="o", capsize=3)
            ax.set_yticks(yloc, [f"{n} (n={nn})" for n, nn in zip(ys, ns)])
            ax.axvline(0, color="black", linewidth=0.8)
        ax.set_title(title)
        ax.set_xlabel("Coefficient estimate (95% HAC CI)")
        ax.grid(axis="x", alpha=0.22)
    fig.suptitle("Macroeconomic sensitivity by index — coefficients have different predictor units", y=1.005, fontsize=14)
    fig.tight_layout()
    fig.savefig(FIGURES / "macro_slope_coefficients_by_index.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def write_hypothesis_markdown(results: dict, data_audit: dict, inflation_audit: dict):
    lines = [
        "# Unified Sector-Index Macroeconomic Hypothesis Testing Report", "",
        f"**Indices:** {', '.join(INDEX_FILES.keys())}.",
        f"**Index sample:** {data_audit.get('index_start')} to {data_audit.get('index_end')}.",
        f"**Macro hypothesis families generated:** {', '.join(results.keys())}.", "",
        "## Executive summary", "",
        "This is one integrated multi-index study. The same source macroeconomic variables are aligned to all selected sector-index return series; each hypothesis reports per-sector-index fits and direct pairwise tests of whether macro sensitivity differs. The pairwise slope tests regress the paired index return difference (A minus B) on the same macro predictor(s), which tests the coefficient difference directly rather than comparing separate p-values.", "",
        "**These are observational associations, not identified causal effects.** No investor information set can be certified where the workbook provides reference dates but not actual publication timestamps. H5 GVA has a short effective sample and is exploratory.", "",
        "## Data overview", "",
        f"- Common index closes: {data_audit.get('common_price_observations')}.",
        f"- Daily index return rows: {data_audit.get('daily_return_observations')}.",
        f"- USD/INR observations: {data_audit.get('fx_rows')}.",
        f"- CPI observations: {inflation_audit.get('months')}; derived YoY inflation observations: {inflation_audit.get('derived_yoy_non_null')}.",
        f"- Weekly reserve observations: {data_audit.get('reserve_rows')}.",
        f"- RBI repo effective-date rows: {data_audit.get('repo_event_rows')}.",
        f"- Quarterly GVA observations: {data_audit.get('gva_quarters')} (short history; 2022-23 constant-price base series only).",
        f"- Monthly IIP observations: {data_audit.get('iip_months')}.",
        f"- S&P 500 observations: {data_audit.get('sp500_rows')}.", "",
        "### CPI inflation derivation", "",
        "The primary inflation predictor is newly calculated from the Combined CPI General Index rather than copied from the reported inflation cell:", "",
        "`inflation_yoy_derived_pct = 100 × (CPI_index[t] / CPI_index[t−12] − 1)`", "",
        f"The supplied reported YoY series and the derived series have {inflation_audit.get('derived_vs_reported_comparison_n')} overlapping non-missing months; their correlation is {inflation_audit.get('derived_vs_reported_correlation')} and mean absolute difference is {inflation_audit.get('derived_minus_reported_mae_percentage_points')} percentage points. See `data/clean/macro/cpi_inflation_derived_clean.csv` for both columns.", "",
        "## Hypotheses and methods", "",
        "### H1 — USD/INR and daily index returns", "",
        "Outcome: daily close-to-close return in percent. Predictor: same-date percentage change in USD/INR. Per-index OLS with Newey–West/HAC standard errors. Pairwise tests regress the difference in two index returns on USD/INR change to test whether the FX slope differs. Same-date FX observation timing is unverified.", "",
        "### H2 — CPI-derived inflation and monthly index returns", "",
        "Outcome: month-end-to-month-end index return in percent. Predictor: inflation derived from the CPI index. The report includes the same-reference-month association and a one-reference-month lag sensitivity. CPI publication timestamps and consensus expectations are absent, so neither should be treated as a clean surprise/event study; same-month association is not predictive.", "",
        "### H3 — Weekly foreign-exchange reserves and weekly index returns", "",
        "Outcome: Friday-ending weekly index return. Predictors: weekly reserve percentage change plus weekly USD/INR percentage change. A future-reserves lead diagnostic is also reported per index. A significant lead is a warning for timing/common-shock problems, not a causal result. The reserve workbook's public release timestamp is absent.", "",
        "### H4 — RBI repo-rate effective-date event study", "",
        "Map each supplied effective date to the first supplied index session on or after it. Expected daily return is estimated over sessions [t−120, t−21], requiring at least 80 observations. The CAR is sum of returns over [t−1, t, t+1] minus three times the estimated mean. The primary test is a two-sided one-sample t-test of mean CAR = 0; all paired event-CAR differences among the selected sector indices are tested and Holm-corrected. This is an exploratory proxy because public announcement timestamps and a complete official MPC decision archive have not been verified.", "",
        "### H5 — Real GVA growth and quarterly index returns", "",
        "GVA measure: GVA at Basic Prices, constant prices, 2022-23 base-year workbook. YoY growth is calculated from the same base-year series and the primary predictor is lagged one quarter. Same-quarter results are secondary only. The effective sample is small, so p-values are low-power exploratory evidence. No older base-year GVA series is spliced into the sample.", "",
        "### H6 — IIP growth and monthly index returns", "",
        "IIP YoY growth is derived from the supplied Monthly sheet in the 50 Macroeconomic Indicators workbook. The primary association uses a one-reference-month lag; same-month results are secondary. Exact release dates and vintage/revision history are not supplied.", "",
        "### H7 — Prior US-session S&P 500 returns and Indian index returns", "",
        "For each Indian date, the predictor is the most recent S&P 500 daily return strictly before that date (`merge_asof` backward, exact matches disabled). Per-index regressions control for that index's own previous daily return. Pairwise slope-difference tests control for the difference in the two indices' own-lag returns. This is association/predictive sensitivity, not causality or a profitability test.", "",
        "## Results by hypothesis", "",
    ]
    for hid, result in results.items():
        lines.append(f"### {hid} — {result.get('title', '')}")
        lines.append("")
        lines.append(f"**Null:** {result.get('null', 'See structured result file.')}")
        lines.append("")
        by = result.get("by_index", result.get("by_index_controlled", result.get("by_index_lagged_growth", result.get("by_index_lagged_growth", result.get("by_index_controlled_for_own_lag", result.get("by_index_same_reference_month", {}))))))
        if by:
            if hid == "H4":
                lines.append("| Index | Eligible events | Mean CAR (%) | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |")
                lines.append("|---|---:|---:|---|---:|---:|---|")
                for name, fit in by.items():
                    est = fit.get("mean_car_pct"); ci = fit.get("ci95_pct"); pv = fit.get("p_value"); p_adj = fit.get("p_value_holm_across_indices")
                    est_s = "—" if est is None else f"{est:.6g}"
                    ci_s = "—" if not ci else f"[{ci[0]:.6g}, {ci[1]:.6g}]"
                    pv_s = "—" if pv is None else f"{pv:.4g}"
                    padj_s = "—" if p_adj is None else f"{p_adj:.4g}"
                    decision = "Reject H0" if fit.get("reject_h0_after_holm_across_indices") else ("Do not reject H0" if pv is not None else "Not tested")
                    lines.append(f"| {name} | {fit.get('n', '—')} | {est_s} | {ci_s} | {pv_s} | {padj_s} | {decision} |")
            else:
                lines.append("| Index | n | Focus coefficient | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |")
                lines.append("|---|---:|---:|---|---:|---:|---|")
                for name, fit in by.items():
                    est = fit.get("focus_estimate")
                    ci = fit.get("focus_ci95")
                    pv = fit.get("focus_p_value")
                    p_adj = fit.get("p_value_holm_across_indices")
                    est_s = "—" if est is None else f"{est:.6g}"
                    ci_s = "—" if not ci else f"[{ci[0]:.6g}, {ci[1]:.6g}]"
                    pv_s = "—" if pv is None else f"{pv:.4g}"
                    padj_s = "—" if p_adj is None else f"{p_adj:.4g}"
                    decision = "Reject H0" if fit.get("reject_h0_after_holm_across_indices") else ("Do not reject H0" if pv is not None else "Not tested")
                    lines.append(f"| {name} | {fit.get('n', '—')} | {est_s} | {ci_s} | {pv_s} | {padj_s} | {decision} |")
            lines.append("")
        pair_keys = [k for k in result if k.startswith("pairwise") and isinstance(result[k], list)]
        for key in pair_keys:
            tests = result[key]
            lines.append(f"**{key.replace('_', ' ').title()}**")
            lines.append("")
            lines.append("| Pair | Estimate | Raw p | Holm p | Decision | n |")
            lines.append("|---|---:|---:|---:|---|---:|")
            for t in tests:
                estimate = t.get("slope_difference_estimate", t.get("mean_car_difference_pct"))
                p = t.get("p_value")
                pa = t.get("p_value_holm_within_family")
                decision = "Reject H0" if t.get("reject_h0_after_holm") else ("Do not reject H0" if pa is not None else "Not tested")
                lines.append(f"| {t.get('index_a')} − {t.get('index_b')} | {'—' if estimate is None else f'{estimate:.6g}'} | {'—' if p is None else f'{p:.4g}'} | {'—' if pa is None else f'{pa:.4g}'} | {decision} | {t.get('n', t.get('n_matched_events', '—'))} |")
            lines.append("")
        for k in ["timing_caveat", "sample_warning"]:
            if result.get(k): lines += [f"**Caveat:** {result[k]}", ""]
    lines += [
        "## Multiple testing and interpretation", "",
        "Holm family-wise error correction is applied to each set of per-index primary coefficient tests and to the eligible pairwise slope comparisons within each named family. Secondary lag/same-period specifications are corrected within their own per-index/pairwise families but the whole research suite still includes multiple families. P-values are not effect-size measures.", "",
        "For H5, the small number of quarterly observations makes inference fragile even when the software reports a numerical p-value. This is not evidence that the hypothesis is proven or disproven.", "",
        "## Reproducibility and output locations", "",
        "- Clean macro data: `data/clean/macro/`.",
        "- Per-index coefficients and pairwise slope comparisons: `reports/macro_hypotheses/hypothesis_results.json` and `.csv`.",
        "- Per-hypothesis standalone JSON: `reports/macro_hypotheses/individual_hypotheses/`.",
        "- Event CAR table: `reports/macro_hypotheses/h4_repo_event_car_by_index.csv`.",
        "- CPI inflation derivation audit: `reports/macro_hypotheses/data_alignment_audit.json`.",
        "- Macro charts: `reports/macro_hypotheses/figures/`.",
        "- Cross-index EDA: `reports/comparative_eda_and_hypothesis_report.md` and `reports/figures/`.", "",
        "## Data and research limitations", "",
        "1. The supplied snapshot archive has a missing-date log, but its listed dates have not been independently reconciled against an official NSE trading-session calendar.",
        "2. The source appears to be a price-return series; do not claim total shareholder returns unless the series definition confirms dividend reinvestment.",
        "3. Sector and thematic indices can share underlying constituents and common market shocks; the paired difference design accounts for matched dates but does not make index universes independent.",
        "4. Macroeconomic series are revised and publication times matter. The supplied workbooks do not provide consistent real-time vintages or release timestamps for CPI, GVA, IIP, reserves or FX.",
        "5. Repo effective dates may differ from the public decision announcement timestamp; H4 is event-window exploration, not causal policy evaluation.",
        "6. No transaction costs, dividends, portfolio weights, slippage or out-of-sample strategy tests are included.",
        "7. This project is a reproducible statistical research workflow, not investment advice.", "",
    ]
    (REPORTS / "unified_multi_index_macro_hypothesis_report.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hypothesis", default="all", choices=["all"] + HYPOTHESES, help="Run all macro hypotheses or a single H1-H7 track")
    args = parser.parse_args()
    for d in [CLEAN_MACRO, REPORTS, FIGURES, INDIVIDUAL]: d.mkdir(parents=True, exist_ok=True)
    prices, returns = load_index_prices()
    fx = load_fx()
    cpi, inflation_audit = load_cpi_and_derive_inflation()
    reserves = load_reserves()
    repo = load_repo_events()
    gva = load_gva()
    iip = load_iip()
    sp500 = load_sp500()
    panels = build_macro_panels(prices, returns, fx, cpi, reserves, repo, gva, iip, sp500)
    data_audit = {
        "index_start": prices.index.min().strftime("%Y-%m-%d"), "index_end": prices.index.max().strftime("%Y-%m-%d"),
        "common_price_observations": int(len(prices)), "daily_return_observations": int(returns.notna().any(axis=1).sum()),
        "fx_rows": int(len(fx)), "reserve_rows": int(len(reserves)), "repo_event_rows": int(len(repo)),
        "gva_quarters": int(len(gva)), "gva_yoy_non_null": int(gva["gva_yoy_growth_pct"].notna().sum()),
        "iip_months": int(len(iip)), "iip_yoy_non_null": int(iip["iip_yoy_growth_pct"].notna().sum()),
        "sp500_rows": int(len(sp500)),
    }
    save_json(REPORTS / "data_alignment_audit.json", {"generated_by": "scripts/run_macro_hypotheses.py", **data_audit, "cpi_inflation_audit": inflation_audit,
        "index_names": list(INDEX_FILES.keys()), "macro_files": [p.name for p in RAW.iterdir() if p.is_file() and (p.suffix.lower() == ".xlsx" or p.name == "sp500_historical.csv")],
        "limitations": ["Same date alignment across indices does not certify official NSE session completeness.", "Macro reference periods do not always equal publication/availability dates.", "GVA uses only the supplied 2022-23 base-year series."]})

    runners = {
        "H1": lambda: analyze_h1(panels["H1"]),
        "H2": lambda: analyze_h2(panels["H2"]),
        "H3": lambda: analyze_h3(panels["H3"]),
        "H4": lambda: analyze_h4(prices, returns, repo),
        "H5": lambda: analyze_h5(panels["H5"]),
        "H6": lambda: analyze_h6(panels["H6"]),
        "H7": lambda: analyze_h7(panels["H7"]),
    }
    selected = HYPOTHESES if args.hypothesis == "all" else [args.hypothesis]
    results = {}
    for hid in selected:
        print(f"Running {hid}...")
        result = runners[hid]()
        results[hid] = result
        save_json(INDIVIDUAL / f"{hid.lower()}_results.json", result)
    if args.hypothesis == "all":
        make_macro_scatter_plots(panels)
        make_macro_coefficient_plot(results)
        save_json(REPORTS / "hypothesis_results.json", {"metadata": data_audit, "results": results})
        flat = []
        for hid, result in results.items():
            for key, value in result.items():
                if not isinstance(value, list): continue
                if not key.startswith("pairwise") or not value: continue
                for row in value:
                    flat.append({"hypothesis": hid, "comparison_family": key, **row})
        pd.DataFrame(flat).to_csv(REPORTS / "hypothesis_results.csv", index=False)
        write_hypothesis_markdown(results, data_audit, inflation_audit)
    print(json.dumps({"selected_hypotheses": selected, "data_audit": data_audit,
                      "results_directory": str(REPORTS), "individual_results": [str(INDIVIDUAL / f"{h.lower()}_results.json") for h in selected]}, indent=2))


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        main()
