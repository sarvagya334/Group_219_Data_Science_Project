from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class DatasetMetadata:
    """Machine-readable provenance and shape information for one dataset."""
    dataset_name: str
    source_file: str
    output_file: str
    rows: int
    columns: list[str]
    dtypes: dict[str, str]
    missing_values: dict[str, int]
    null_policy: str = "Missing values are JSON null; no imputation is performed by the exporter."
    format: str = "JSON Lines (one JSON object per record, UTF-8)"


class JsonDatasetStore:
    """Write tabular datasets as readable JSON Lines and maintain a manifest.

    JSONL is used rather than one giant JSON array because it streams well,
    handles large files, and lets each record be inspected independently.
    """

    def __init__(self, output_dir: Path, manifest_path: Path):
        self.output_dir = Path(output_dir)
        self.manifest_path = Path(manifest_path)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._manifest: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _json_value(value: Any) -> Any:
        if value is None or value is pd.NA or value is pd.NaT:
            return None
        if isinstance(value, (pd.Timestamp, datetime, date)):
            return value.isoformat()
        if isinstance(value, np.generic):
            value = value.item()
        if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
            return None
        if isinstance(value, (str, int, float, bool)):
            return value
        try:
            if pd.isna(value):
                return None
        except (TypeError, ValueError):
            pass
        return str(value)

    def write_frame(self, name: str, frame: pd.DataFrame, source_file: str = "derived") -> Path:
        """Persist a DataFrame as newline-delimited JSON, with null-safe values."""
        safe_name = name.replace("/", "_").replace(" ", "_")
        path = self.output_dir / f"{safe_name}.jsonl"
        # pandas emits standards-compliant JSON nulls and ISO date strings.
        records = []
        for record in frame.to_dict(orient="records"):
            records.append({str(k): self._json_value(v) for k, v in record.items()})
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
        metadata = DatasetMetadata(
            dataset_name=name,
            source_file=source_file,
            output_file=str(path.relative_to(self.output_dir.parent)),
            rows=int(len(frame)),
            columns=[str(c) for c in frame.columns],
            dtypes={str(c): str(frame[c].dtype) for c in frame.columns},
            missing_values={str(c): int(frame[c].isna().sum()) for c in frame.columns},
        )
        self._manifest[name] = asdict(metadata)
        return path

    def write_json(self, filename: str, payload: Any) -> Path:
        path = self.output_dir / filename
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
        return path

    def write_manifest(self) -> Path:
        payload = {
            "schema_version": "1.0",
            "encoding": "UTF-8",
            "tabular_format": "JSONL",
            "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "datasets": self._manifest,
        }
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
        return self.manifest_path
