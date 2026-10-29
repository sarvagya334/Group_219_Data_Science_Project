#!/usr/bin/env python3
"""Post-run checks for sector-index EDA artifacts."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
EDA = ROOT / "reports" / "eda"
TESTS = ROOT / "reports" / "hypothesis_tests"
FIG = ROOT / "reports" / "figures"

def main():
    desc = json.loads((EDA / "descriptive_statistics.json").read_text())
    hyp = json.loads((TESTS / "cross_index_hypothesis_tests.json").read_text())
    assert len(desc["indices"]) == 16
    assert desc["common_price_observations"] > 2500
    assert desc["common_return_observations"] == desc["common_price_observations"] - 1
    assert len(hyp["pairwise_tests"]) == 360  # 120 pairs x 3 test families
    assert all(t["n"] > 1000 for t in hyp["pairwise_tests"])
    assert all(t["p_value_holm"] is None or 0 <= t["p_value_holm"] <= 1 for t in hyp["pairwise_tests"])
    assert len(list(FIG.glob("*.png"))) >= 7
    for filename in ["daily_returns_pct.csv", "normalized_prices_base100.csv", "return_correlation_matrix.csv"]:
        assert (EDA / filename).exists(), filename
    assert (ROOT / "reports" / "comparative_eda_and_hypothesis_report.md").exists()
    print("PASS: sector EDA artifacts, 360 pairwise tests, corrected p-values and figures exist.")

if __name__ == "__main__":
    main()
