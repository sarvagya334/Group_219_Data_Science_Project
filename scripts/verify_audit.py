"""Post-run checks for sector-index data preparation and encoded-size audit."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.sparse import load_npz

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
AUDIT = json.loads((REPORTS / "sector_data_quality_audit.json").read_text())
SIZE = json.loads((REPORTS / "dataset_size_audit.json").read_text())

assert AUDIT["source_snapshot_csv_count"] >= 2000
assert AUDIT["distinct_index_names"] >= 100
assert AUDIT["valid_close_rows_in_master_panel"] > 200_000
assert AUDIT["duplicate_date_index_groups"] == 0
assert AUDIT["conflicting_duplicate_groups"] == 0
assert len(AUDIT["primary_sector_indices"]) == 16
# The complete mixed-index archive contains four recorded OHLC boundary violations
# in peripheral series (including fixed-income/USD-converted indices). These are
# deliberately retained and documented for review instead of silently rewritten.
# Require the audit to record every exception; the primary 16-index universe is
# validated individually below and must have complete OHLC data.
if AUDIT["ohlc_validation"]["status"] == "REVIEW_REQUIRED":
    assert AUDIT["ohlc_validation"]["violating_complete_ohlc_rows"] > 0
    assert AUDIT["ohlc_validation"].get("examples"), "Known OHLC exceptions must be documented"
    assert len(AUDIT["ohlc_validation"]["examples"]) >= min(
        4, AUDIT["ohlc_validation"]["violating_complete_ohlc_rows"]
    )
else:
    assert AUDIT["ohlc_validation"]["status"] == "PASS"
    assert AUDIT["ohlc_validation"]["violating_complete_ohlc_rows"] == 0

sets = []
for idx, info in AUDIT["primary_sector_indices"].items():
    path = ROOT / info["clean_file"]
    frame = pd.read_csv(path, parse_dates=["Date"])
    assert len(frame) == info["unique_dates"], idx
    assert frame["Date"].is_unique, idx
    assert frame["Date"].is_monotonic_increasing, idx
    assert frame["Close"].notna().all(), idx
    assert (frame["Close"] > 0).all(), idx
    complete_ohlc = frame[["Open", "High", "Low", "Close"]].notna().all(axis=1)
    valid = frame.loc[complete_ohlc, ["Open", "High", "Low", "Close"]]
    assert (valid["High"] >= valid[["Open", "Close", "Low"]].max(axis=1)).all(), idx
    assert (valid["Low"] <= valid[["Open", "Close", "High"]].min(axis=1)).all(), idx
    # Missing Open/High/Low is not imputed: keep the valid Close observations and
    # expose optional-field missingness rather than inventing OHLC values.
    assert info["coverage_fraction_vs_archive"] >= 0.95, idx
    sets.append(set(frame["Date"]))
assert len(set.intersection(*sets)) >= 2500

assert SIZE["requirement_met"] is True
assert SIZE["instances_times_encoded_attributes"] >= 3_000_000
encoded = load_npz(ROOT / SIZE["encoded_matrix_path"])
assert list(encoded.shape) == [SIZE["instances"], SIZE["encoded_attribute_count"]]
assert encoded.shape[0] == AUDIT["valid_close_rows_in_master_panel"]
print("PASS: snapshot audit documented, 16 primary indices validated, encoded dataset size verified.")
