#!/usr/bin/env python3
"""Build the all-index panel and selected sector-index files from NSE snapshots.

The source archive contains one CSV per snapshot date. Some CSVs have an internal
Index Date label inconsistent with their filename; the filename is retained as
canonical snapshot date and every mismatch is recorded in the audit. No external
calendar is inferred from weekdays alone.
"""
from __future__ import annotations
from pathlib import Path
import json
import re
import csv
import io
import zipfile
import math
import numpy as np
import pandas as pd
from scipy import sparse

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
SELECTED_DIR = CLEAN / "sector_indices"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
SOURCE_ZIP = RAW / "sector_indices.zip"
CONFIG = json.loads((ROOT / "config" / "sector_universe.json").read_text(encoding="utf-8"))
CORE = CONFIG["primary_sector_indices"]

SOURCE_TO_OUTPUT = {
    "Open Index Value": "Open",
    "High Index Value": "High",
    "Low Index Value": "Low",
    "Closing Index Value": "Close",
    "Points Change": "PointsChange",
    "Change(%)": "ChangePct",
    "Volume": "Volume",
    "Turnover (Rs. Cr.)": "TurnoverRsCr",
    "P/E": "PE",
    "P/B": "PB",
    "Div Yield": "DivYield",
}
PRICE_COLS = ["Open", "High", "Low", "Close"]
NUMERIC_FEATURES = [
    "Open", "High", "Low", "Close", "PointsChange", "ChangePct", "Volume",
    "TurnoverRsCr", "PE", "PB", "DivYield", "return_pct", "log_return_pct",
    "momentum_5d_pct", "momentum_20d_pct", "volatility_20d_pct",
    "volatility_60d_pct", "high_low_range_pct", "open_gap_pct",
]


def to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.strip().str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .replace({"-": np.nan, "": np.nan, "nan": np.nan, "None": np.nan, "NA": np.nan}),
        errors="coerce",
    )


def classify_index(name: str) -> str:
    n = name.lower()
    if "vix" in n:
        return "Volatility"
    if "g-sec" in n or "gsec" in n or "bond index" in n or "bharat bond" in n or "1d rate" in n:
        return "Fixed Income / Rate"
    if any(k in n for k in ["inverse", "leverage", "futures", "arbitrage", "equal weight", "low volatility", "momentum", "quality", "alpha", "value", "shariah", "dividend", "liquid", "esg", "multifactor", "growth sectors"]):
        return "Factor / Strategy"
    if any(k in n for k in ["nifty 50", "nifty 100", "nifty 200", "nifty 500", "largemidcap", "midcap 150", "smallcap 250", "midsmallcap", "midcap 50", "smallcap 50", "midcap 100", "smallcap 100", "microcap"]):
        return "Broad / Market-cap"
    sector_terms = [
        "auto", "bank", "commodit", "energy", "fmcg", "financial services", "infrastructure", "nifty it", "media", "metal", "pharma", "realty", "pse", "services sector", "oil & gas", "consumer", "healthcare", "manufactur", "defence", "digital", "mobility", "tourism", "internet", "capital markets", "railways", "cement", "power", "housing", "construction", "capital goods", "hospitals", "nbfc", "insurance", "retail", "telecommunication", "sugar", "microfinance", "transport", "logistics", "chemicals", "industrial", "mnc", "psu", "cpse", "corporate group", "conglomerate", "reits", "invit", "realty"
    ]
    if any(k in n for k in sector_terms):
        return "Sector / Theme"
    return "Other Equity / Composite"


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return s


def main():
    if not SOURCE_ZIP.exists():
        raise FileNotFoundError(f"Missing raw snapshot archive: {SOURCE_ZIP}")
    pattern = re.compile(r"^sector_indices/daily_snapshots/ind_close_all_(\d{8})\.csv$")
    records = []
    invalid_files = []
    mismatch_by_file = {}
    missing_log_dates = []
    source_header = ["Index Name", "Index Date", *SOURCE_TO_OUTPUT.keys()]
    with zipfile.ZipFile(SOURCE_ZIP) as zf:
        members = [n for n in zf.namelist() if pattern.match(n)]
        if not members:
            raise ValueError("No daily snapshot CSVs found in sector_indices.zip")
        for file_i, member in enumerate(members, 1):
            if file_i % 500 == 0:
                print(f"Reading snapshot {file_i}/{len(members)}", flush=True)
            match = pattern.match(member)
            file_date = pd.to_datetime(match.group(1), format="%d%m%Y", errors="coerce")
            if pd.isna(file_date):
                invalid_files.append(member)
                continue
            expected_internal_label = file_date.strftime("%d-%m-%Y")
            mismatch_count = 0
            try:
                with zf.open(member) as stream:
                    reader = csv.reader(io.TextIOWrapper(stream, encoding="utf-8-sig", newline=""))
                    header = next(reader, None)
                    if header is None or any(col not in header for col in source_header):
                        invalid_files.append({"file": member, "missing_columns": [c for c in source_header if not header or c not in header]})
                        continue
                    positions = {col: header.index(col) for col in source_header}
                    for row in reader:
                        if len(row) < len(header):
                            invalid_files.append({"file": member, "malformed_row": True})
                            continue
                        index_name = row[positions["Index Name"]].strip()
                        source_date = row[positions["Index Date"]].strip()
                        mismatch = source_date != expected_internal_label
                        if mismatch:
                            mismatch_count += 1
                        values = [row[positions[col]] for col in SOURCE_TO_OUTPUT]
                        records.append([index_name, file_date, source_date, Path(member).name, bool(mismatch), *values])
            except Exception as exc:
                invalid_files.append({"file": member, "error": str(exc)})
                continue
            if mismatch_count:
                mismatch_by_file[Path(member).name] = {
                    "filename_date": file_date.strftime("%Y-%m-%d"),
                    "source_internal_date_labels": [expected_internal_label],
                    "mismatch_rows": mismatch_count,
                    "handling": "Use the date encoded in the snapshot filename as canonical date; preserve source Index Date label in master data."
                }
        log_path = "sector_indices/daily_snapshots/_missing_dates.log"
        if log_path in zf.namelist():
            missing_log_dates = [x.strip() for x in zf.read(log_path).decode("utf-8", errors="replace").splitlines() if x.strip()]
    if not records:
        raise ValueError("No valid daily snapshot rows could be read")
    columns = ["IndexName", "Date", "SourceIndexDate", "SourceFile", "SourceDateMismatch", *SOURCE_TO_OUTPUT.values()]
    all_rows = pd.DataFrame(records, columns=columns)
    all_rows["Date"] = pd.to_datetime(all_rows["Date"], errors="coerce")
    for col in SOURCE_TO_OUTPUT.values():
        all_rows[col] = to_numeric(all_rows[col])
    all_rows["IndexName"] = all_rows["IndexName"].astype(str).str.strip()
    all_rows = all_rows[all_rows["IndexName"].notna() & all_rows["IndexName"].ne("")].copy()
    all_rows["IndexGroup"] = all_rows["IndexName"].map(classify_index)

    # Key uniqueness should follow snapshot filenames, not inconsistent internal labels.
    duplicate_mask = all_rows.duplicated(["Date", "IndexName"], keep=False)
    duplicate_groups = int(all_rows.loc[duplicate_mask].groupby(["Date", "IndexName"]).ngroups)
    conflicting_groups = 0
    if duplicate_mask.any():
        for _, g in all_rows.loc[duplicate_mask].groupby(["Date", "IndexName"]):
            if len(g[["Open", "High", "Low", "Close"]].drop_duplicates()) > 1:
                conflicting_groups += 1
        if conflicting_groups:
            raise ValueError(f"Conflicting duplicate date/index keys found: {conflicting_groups}")
        all_rows = all_rows.sort_values("SourceFile").drop_duplicates(["Date", "IndexName"], keep="first")

    # Keep rows with valid, positive close values in the main analytical panel.
    raw_row_count = int(len(all_rows))
    invalid_close_mask = all_rows["Close"].isna() | (all_rows["Close"] <= 0)
    invalid_close_rows = all_rows.loc[invalid_close_mask].copy()
    panel = all_rows.loc[~invalid_close_mask].copy()
    panel = panel.sort_values(["IndexName", "Date"]).reset_index(drop=True)
    print(f"Panel built with {len(panel)} rows; computing features", flush=True)
    panel["return_pct"] = panel.groupby("IndexName", sort=False)["Close"].pct_change(fill_method=None) * 100.0
    print("Computed simple returns", flush=True)
    gaps = panel.groupby("IndexName")["Date"].diff().dt.days
    panel.loc[gaps > 7, "return_pct"] = np.nan
    panel["log_return_pct"] = panel.groupby("IndexName", sort=False)["Close"].transform(lambda s: np.log(s / s.shift(1)) * 100.0)
    print("Computed log returns", flush=True)
    panel.loc[gaps > 7, "log_return_pct"] = np.nan
    panel["momentum_5d_pct"] = panel.groupby("IndexName", sort=False)["Close"].transform(lambda s: (s / s.shift(5) - 1) * 100.0)
    print("Computed 5-session momentum", flush=True)
    panel["momentum_20d_pct"] = panel.groupby("IndexName", sort=False)["Close"].transform(lambda s: (s / s.shift(20) - 1) * 100.0)
    print("Computed 20-session momentum", flush=True)
    panel["volatility_20d_pct"] = panel.groupby("IndexName", sort=False)["return_pct"].transform(lambda s: s.rolling(20, min_periods=15).std() * np.sqrt(252))
    print("Computed 20-session volatility", flush=True)
    panel["volatility_60d_pct"] = panel.groupby("IndexName", sort=False)["return_pct"].transform(lambda s: s.rolling(60, min_periods=40).std() * np.sqrt(252))
    print("Computed 60-session volatility", flush=True)
    panel["high_low_range_pct"] = (panel["High"] - panel["Low"]) / panel["Close"] * 100.0
    prev_close = panel.groupby("IndexName")["Close"].shift(1)
    panel["open_gap_pct"] = (panel["Open"] / prev_close - 1) * 100.0
    panel.loc[gaps > 7, "open_gap_pct"] = np.nan

    date_counts = panel.groupby("IndexName")["Date"].nunique().sort_values(ascending=False)
    name_counts = {str(k): int(v) for k, v in date_counts.items()}
    mismatch_details = [{"file": k, **v} for k, v in mismatch_by_file.items()]
    mismatch_rows = int(panel["SourceDateMismatch"].sum())
    unique_dates = sorted(panel["Date"].dropna().unique())
    audit = {
        "generated_by": "scripts/clean_and_validate.py",
        "source_archive": "data/raw/sector_indices.zip",
        "source_snapshot_csv_count": int(len(members)),
        "invalid_or_skipped_source_files": invalid_files,
        "raw_index_rows_after_key_deduplication": raw_row_count,
        "valid_close_rows_in_master_panel": int(len(panel)),
        "rows_excluded_for_missing_or_nonpositive_close": int(len(invalid_close_rows)),
        "distinct_index_names": int(panel["IndexName"].nunique()),
        "unique_snapshot_dates": int(panel["Date"].nunique()),
        "date_range": {"start": pd.Timestamp(min(unique_dates)).strftime("%Y-%m-%d"), "end": pd.Timestamp(max(unique_dates)).strftime("%Y-%m-%d")},
        "index_observation_counts": name_counts,
        "duplicate_date_index_groups": duplicate_groups,
        "conflicting_duplicate_groups": conflicting_groups,
        "source_index_date_mismatch_files": mismatch_details,
        "source_index_date_mismatch_rows_in_all_raw_rows": int(all_rows["SourceDateMismatch"].sum()),
        "source_missing_dates_log_entries": int(len(set(missing_log_dates))),
        "source_missing_dates_log": sorted(set(missing_log_dates)),
        "ohlc_validation": {},
        "primary_sector_indices": {},
        "limitations": [
            "The archive includes 180 index series across sector, thematic, broad-market, factor/strategy, fixed-income and volatility families; it is not purely a sector-only archive.",
            "The source missing-date log lists dates absent from the snapshot collection; dates have not been independently compared with the official NSE session calendar.",
            "Three snapshot files have internal Index Date labels inconsistent with filenames. The filename date is used as the canonical date and the mismatches are retained in this audit.",
            "Index launch dates differ. The primary hypothesis universe uses long-history sector/industry indices; newer index series remain in the all-index panel and size audit but are not used in the primary models.",
            "Index-series values may represent price indices, total-return indices, strategy indices, debt indices or other index types. Their definitions should be checked before comparing performance across families.",
        ],
    }

    # OHLC check for rows that have all four fields. Missing OHLC is common for some index types.
    ohlc_complete = panel[PRICE_COLS].notna().all(axis=1)
    bad_ohlc = ohlc_complete & (
        (panel["Low"] > panel[["Open", "Close", "High"]].min(axis=1)) |
        (panel["High"] < panel[["Open", "Close", "Low"]].max(axis=1)) |
        (panel[PRICE_COLS] <= 0).any(axis=1)
    )
    audit["ohlc_validation"] = {
        "rows_with_complete_ohlc": int(ohlc_complete.sum()),
        "rows_missing_any_ohlc_component": int((~ohlc_complete).sum()),
        "violating_complete_ohlc_rows": int(bad_ohlc.sum()),
        "status": "PASS" if not bad_ohlc.any() else "REVIEW_REQUIRED",
    }
    if bad_ohlc.any():
        audit["ohlc_validation"]["examples"] = panel.loc[bad_ohlc, ["IndexName", "Date", *PRICE_COLS]].head(30).to_dict("records")

    # Full all-index master dataset and a features table, preserving all index names.
    cols = ["IndexName", "IndexGroup", "Date", *SOURCE_TO_OUTPUT.values(), "return_pct", "log_return_pct", "momentum_5d_pct", "momentum_20d_pct", "volatility_20d_pct", "volatility_60d_pct", "high_low_range_pct", "open_gap_pct", "SourceFile", "SourceIndexDate", "SourceDateMismatch"]
    master_path = CLEAN / "sector_index_panel_clean.csv"
    panel[cols].to_csv(master_path, index=False, date_format="%Y-%m-%d", float_format="%.8f")

    # Long-history sector-only primary series: ≥95% of unique snapshot dates, intersected with pre-specified list.
    all_date_count = int(panel["Date"].nunique())
    core_missing = []
    for name in CORE:
        part = panel[panel["IndexName"].eq(name)].sort_values("Date").copy()
        if part.empty:
            core_missing.append(name)
            continue
        count = int(part["Date"].nunique())
        if count < math.ceil(all_date_count * CONFIG["selection_policy"]["threshold_fraction"]):
            core_missing.append(name)
        file = SELECTED_DIR / f"{slugify(name)}_clean.csv"
        clean = part[["IndexName", "Date", *SOURCE_TO_OUTPUT.values(), "return_pct", "log_return_pct", "momentum_5d_pct", "momentum_20d_pct", "volatility_20d_pct", "volatility_60d_pct", "high_low_range_pct", "open_gap_pct"]].copy()
        clean.to_csv(file, index=False, date_format="%Y-%m-%d", float_format="%.8f")
        audit["primary_sector_indices"][name] = {
            "unique_dates": count,
            "first_date": part["Date"].min().strftime("%Y-%m-%d"),
            "last_date": part["Date"].max().strftime("%Y-%m-%d"),
            "clean_file": str(file.relative_to(ROOT)),
            "coverage_fraction_vs_archive": count / all_date_count,
        }
    if core_missing:
        raise ValueError(f"Configured primary sector universe failed data availability policy: {core_missing}")

    audit_path = REPORTS / "sector_data_quality_audit.json"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False, default=str, allow_nan=False) + "\n", encoding="utf-8")
    lines = [
        "# Sector-index source audit", "",
        f"- Snapshot files read: **{audit['source_snapshot_csv_count']:,}**",
        f"- All-index rows with valid positive close: **{len(panel):,}**",
        f"- Distinct index names: **{panel['IndexName'].nunique():,}**",
        f"- Unique snapshot dates: **{panel['Date'].nunique():,}**",
        f"- Date range: **{audit['date_range']['start']} to {audit['date_range']['end']}**",
        f"- Missing-date log entries supplied with the archive: **{audit['source_missing_dates_log_entries']:,}**",
        f"- Snapshot files whose internal date label differs from filename: **{len(mismatch_details)}**",
        f"- Encoded source-date mismatch rows: **{audit['source_index_date_mismatch_rows_in_all_raw_rows']:,}**",
        f"- Complete OHLC rows with invariant violations: **{audit['ohlc_validation']['violating_complete_ohlc_rows']:,}**",
        "", "## Primary sector-index universe", "", "| Index | Observations | First date | Last date | Coverage fraction |", "|---|---:|---|---|---:|"
    ]
    for name, info in audit["primary_sector_indices"].items():
        lines.append(f"| {name} | {info['unique_dates']:,} | {info['first_date']} | {info['last_date']} | {info['coverage_fraction_vs_archive']:.3%} |")
    lines += ["", "## Important interpretation notes", ""] + [f"- {x}" for x in audit["limitations"]]
    (REPORTS / "sector_data_quality_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Writing audit, building encoded matrix", flush=True)
    # Build a sparse one-hot + numeric matrix to document post-encoding dimensions.
    # Missing numeric features are median-imputed within index; global median is fallback.
    feature_df = panel[NUMERIC_FEATURES].copy()
    imputation_counts = {}
    for col in NUMERIC_FEATURES:
        missing_count = int(feature_df[col].isna().sum())
        imputation_counts[col] = missing_count
        by_index_median = panel.groupby("IndexName")[col].transform("median")
        global_median = feature_df[col].median()
        if not np.isfinite(global_median):
            global_median = 0.0
        feature_df[col] = feature_df[col].fillna(by_index_median).fillna(global_median).fillna(0.0)
    numeric_matrix = sparse.csr_matrix(feature_df.to_numpy(dtype=np.float32))
    index_codes, index_categories = pd.factorize(panel["IndexName"], sort=True)
    group_codes, group_categories = pd.factorize(panel["IndexGroup"], sort=True)
    row_positions = np.arange(len(panel), dtype=np.int32)
    index_onehot = sparse.csr_matrix(
        (np.ones(len(panel), dtype=np.float32), (row_positions, index_codes)),
        shape=(len(panel), len(index_categories)),
    )
    group_onehot = sparse.csr_matrix(
        (np.ones(len(panel), dtype=np.float32), (row_positions, group_codes)),
        shape=(len(panel), len(group_categories)),
    )
    encoded = sparse.hstack([numeric_matrix, index_onehot, group_onehot], format="csr", dtype=np.float32)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    sparse.save_npz(PROCESSED / "sector_index_features_encoded.npz", encoded, compressed=True)
    feature_columns = {
        "numeric_features": NUMERIC_FEATURES,
        "index_name_categories": list(index_categories),
        "index_group_categories": list(group_categories),
        "imputation_counts_by_numeric_feature": imputation_counts,
        "encoding": "numeric features (missing values median-imputed within index; global median fallback) + one-hot IndexName + one-hot IndexGroup",
        "warning": "This encoded matrix is for dimensionality/data-preparation documentation and generic modelling. Macro hypothesis regressions use original returns and predictors, not imputed feature values.",
    }
    (PROCESSED / "encoded_feature_columns.json").write_text(json.dumps(feature_columns, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_instances, n_attributes = encoded.shape
    size_audit = {
        "generated_by": "scripts/clean_and_validate.py",
        "instances_definition": "one index-observation row per snapshot date and Index Name with a valid positive close",
        "instances": int(n_instances),
        "numeric_feature_count": len(NUMERIC_FEATURES),
        "one_hot_index_name_columns": int(index_onehot.shape[1]),
        "one_hot_index_group_columns": int(group_onehot.shape[1]),
        "encoded_attribute_count": int(n_attributes),
        "instances_times_encoded_attributes": int(n_instances * n_attributes),
        "required_cells": 3000000,
        "requirement_met": bool(n_instances * n_attributes >= 3000000),
        "encoded_matrix_path": "data/processed/sector_index_features_encoded.npz",
        "feature_definition_path": "data/processed/encoded_feature_columns.json",
        "imputation": "Median by index name, then global median fallback, then 0 only where an entire feature is missing. Counts are in encoded_feature_columns.json.",
    }
    (REPORTS / "dataset_size_audit.json").write_text(json.dumps(size_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not size_audit["requirement_met"]:
        raise ValueError(f"Encoded dataset has only {size_audit['instances_times_encoded_attributes']:,} cells; expected at least 3,000,000")

    print(json.dumps({
        "source_files": len(members), "rows": len(panel), "index_names": int(panel["IndexName"].nunique()),
        "dates": int(panel["Date"].nunique()), "primary_sector_indices": len(audit["primary_sector_indices"]),
        "encoded_shape": list(encoded.shape), "encoded_cells": size_audit["instances_times_encoded_attributes"],
        "audit": str(audit_path), "dataset_size_audit": str(REPORTS / "dataset_size_audit.json")
    }, indent=2))


if __name__ == "__main__":
    main()
