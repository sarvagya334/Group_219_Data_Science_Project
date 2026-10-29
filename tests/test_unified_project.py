from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
from scipy.sparse import load_npz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_macro_hypotheses as mh


def test_primary_sector_index_files_are_valid_and_cover_long_history():
    assert len(mh.INDEX_FILES) == 16
    date_sets = []
    for index_name, relative_path in mh.INDEX_FILES.items():
        frame = pd.read_csv(ROOT / "data" / "clean" / relative_path, parse_dates=["Date"])
        assert {"Date", "Close", "Open", "High", "Low"}.issubset(frame.columns)
        assert frame["Date"].is_unique
        assert frame["Date"].is_monotonic_increasing
        # The source archive has some early dates with Close but missing Open/High/Low.
        # Those optional OHLC fields remain missing rather than being fabricated.
        assert frame["Close"].notna().all()
        assert (frame["Close"] > 0).all()
        full_ohlc = frame[["Open", "High", "Low", "Close"]].notna().all(axis=1)
        valid = frame.loc[full_ohlc, ["Open", "High", "Low", "Close"]]
        assert (valid["High"] >= valid[["Open", "Close", "Low"]].max(axis=1)).all()
        assert (valid["Low"] <= valid[["Open", "Close", "High"]].min(axis=1)).all()
        assert len(frame) >= 2500, index_name
        date_sets.append(set(frame["Date"]))
    assert len(set.intersection(*date_sets)) >= 2500


def test_cpi_inflation_is_derived_from_index():
    frame = pd.read_csv(ROOT / "data" / "clean" / "macro" / "cpi_inflation_derived_clean.csv", parse_dates=["date"])
    assert frame["date"].is_monotonic_increasing
    valid = frame.dropna(subset=["inflation_yoy_derived_pct"])
    assert len(valid) >= 100
    row = valid.iloc[-1]
    previous_date = row["date"] - pd.DateOffset(months=12)
    previous = frame.loc[frame["date"] == previous_date, "combined_cpi_index"]
    assert len(previous) == 1
    expected = (row["combined_cpi_index"] / previous.iloc[0] - 1) * 100
    assert abs(expected - row["inflation_yoy_derived_pct"]) < 1e-7


def test_prior_us_alignment_never_uses_same_date_close():
    indian = pd.DataFrame({"date": pd.to_datetime(["2024-01-02", "2024-01-03"]), "indian_return": [1.0, 2.0]})
    us = pd.DataFrame({"sp_date": pd.to_datetime(["2024-01-02", "2024-01-03"]), "sp500_return_pct": [10.0, 20.0]})
    aligned = mh.align_prior_us_sessions(indian, us)
    assert pd.isna(aligned.loc[0, "sp_date"])
    assert aligned.loc[1, "sp_date"] == pd.Timestamp("2024-01-02")
    assert aligned.loc[1, "sp500_return_pct"] == 10.0


def test_hac_fit_returns_coefficients_and_uncertainty():
    rng = np.random.default_rng(9)
    x = rng.normal(size=200)
    y = 0.8 * x + rng.normal(scale=0.5, size=200)
    result = mh.fit_hac(pd.DataFrame({"y": y, "x": x}), "y", ["x"], focus="x")
    assert result["status"] == "tested"
    assert result["n"] == 200
    assert result["focus_estimate"] is not None
    assert result["focus_ci95"] is not None
    assert 0 <= result["focus_p_value"] <= 1


def test_full_hypothesis_outputs_cover_the_sector_universe():
    path = ROOT / "reports" / "macro_hypotheses" / "hypothesis_results.json"
    assert path.exists(), "Run `make full` before result-artifact tests"
    data = json.loads(path.read_text())
    assert set(data["results"]) == {"H1", "H2", "H3", "H4", "H5", "H6", "H7"}
    expected = set(mh.INDEX_FILES)
    for hid, result in data["results"].items():
        by_index = (result.get("by_index") or result.get("by_index_controlled") or
                    result.get("by_index_same_reference_month") or result.get("by_index_lagged_growth") or
                    result.get("by_index_controlled_for_own_lag"))
        assert by_index is not None, hid
        assert set(by_index) == expected, hid
        for key, rows in result.items():
            if key.startswith("pairwise") and isinstance(rows, list):
                assert len(rows) == 120, (hid, key)
                for row in rows:
                    p = row.get("p_value_holm_within_family")
                    assert p is None or 0 <= p <= 1
                    assert "reject_h0_after_holm" in row
    audit = json.loads((ROOT / "reports" / "macro_hypotheses" / "data_alignment_audit.json").read_text())
    assert audit["cpi_inflation_audit"]["derived_yoy_non_null"] > 100
    assert audit["repo_event_rows"] > 0


def test_repo_event_cars_include_every_primary_sector_index():
    frame = pd.read_csv(ROOT / "reports" / "macro_hypotheses" / "h4_repo_event_car_by_index.csv")
    assert set(frame["index"].unique()) == set(mh.INDEX_FILES)
    assert frame.groupby("index").size().min() >= 20
    assert frame["car_minus_expected_return_pct"].notna().all()


def test_encoded_dataset_meets_course_cell_requirement():
    audit = json.loads((ROOT / "reports" / "dataset_size_audit.json").read_text())
    assert audit["requirement_met"]
    assert audit["instances_times_encoded_attributes"] >= 3_000_000
    matrix = load_npz(ROOT / audit["encoded_matrix_path"])
    assert list(matrix.shape) == [audit["instances"], audit["encoded_attribute_count"]]


def test_jsonl_manifest_covers_exported_clean_csvs():
    manifest_path = ROOT / "reports" / "json_dataset_manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text())
    candidates = [p for p in (ROOT / "data" / "clean").rglob("*.csv") if p.name != "sector_index_panel_clean.csv"]
    assert len(manifest["datasets"]) == len(candidates)
    assert all(item["rows"] >= 1 for item in manifest["datasets"].values())
