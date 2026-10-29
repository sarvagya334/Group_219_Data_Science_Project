#!/usr/bin/env python3
"""Export selected cleaned analysis tables to standards-compliant JSONL with a manifest. The full all-index master panel remains CSV to avoid duplicating a large dataset."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from market_impact.json_store import JsonDatasetStore


def main():
    csv_files = sorted(p for p in (ROOT / "data" / "clean").rglob("*.csv") if p.name != "sector_index_panel_clean.csv")
    if not csv_files:
        raise SystemExit("No cleaned CSVs exist. Run make full first.")
    out = ROOT / "data" / "processed_json"
    manifest = ROOT / "reports" / "json_dataset_manifest.json"
    store = JsonDatasetStore(out, manifest)
    for path in csv_files:
        rel = path.relative_to(ROOT / "data" / "clean")
        name = str(rel.with_suffix("")).replace("\\", "/")
        df = pd.read_csv(path)
        store.write_frame(name, df, source_file=str(path.relative_to(ROOT)))
    store.write_manifest()
    print(f"Exported {len(csv_files)} cleaned datasets to {out}; manifest: {manifest}")


if __name__ == "__main__":
    main()
