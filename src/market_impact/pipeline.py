from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

from .json_store import JsonDatasetStore


@dataclass(frozen=True)
class ProjectPaths:
    """Centralized project paths; avoid scattered hard-coded paths."""
    root: Path

    @property
    def raw(self) -> Path: return self.root / "data" / "raw"
    @property
    def processed(self) -> Path: return self.root / "data" / "processed"
    @property
    def json_processed(self) -> Path: return self.root / "data" / "processed_json"
    @property
    def reports(self) -> Path: return self.root / "reports"
    @property
    def figures(self) -> Path: return self.reports / "figures"


class LegacyAnalysisAdapter:
    """Compatibility adapter while existing tested statistical routines are migrated.

    It isolates the current analysis implementation behind a small interface.
    New code should use the OOP orchestration here rather than importing legacy
    scripts directly throughout the codebase.
    """
    def __init__(self, project: ProjectPaths):
        self.project = project

    def run_cleaning_and_h1_h3(self) -> None:
        script = self.project.root / "src" / "legacy_pipeline.py"
        subprocess.run([sys.executable, str(script)], cwd=self.project.root, check=True)

    def run_h4_h7(self) -> None:
        script = self.project.root / "src" / "legacy_h4_h7.py"
        subprocess.run([sys.executable, str(script)], cwd=self.project.root, check=True)


class JsonExportStage:
    """Convert every processed tabular CSV into JSONL and create a manifest."""
    def __init__(self, project: ProjectPaths):
        self.project = project

    def run(self) -> dict:
        store = JsonDatasetStore(self.project.json_processed, self.project.reports / "json_dataset_manifest.json")
        exported = []
        for csv_path in sorted(self.project.processed.glob("*.csv")):
            frame = pd.read_csv(csv_path)
            name = csv_path.stem
            json_path = store.write_frame(name, frame, source_file=f"data/processed/{csv_path.name}")
            exported.append({"dataset": name, "rows": len(frame), "columns": len(frame.columns), "jsonl": str(json_path.relative_to(self.project.root))})
        manifest_path = store.write_manifest()
        return {"exported_datasets": exported, "count": len(exported), "manifest": str(manifest_path.relative_to(self.project.root))}


class ResearchPipeline:
    """Application service coordinating cleaning, hypotheses, JSON export and QA."""
    def __init__(self, project_root: Path | None = None):
        root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
        self.paths = ProjectPaths(root)
        self.analysis = LegacyAnalysisAdapter(self.paths)
        self.json_export = JsonExportStage(self.paths)

    def run(self, run_h4_h7: bool = True) -> dict:
        self.analysis.run_cleaning_and_h1_h3()
        if run_h4_h7:
            self.analysis.run_h4_h7()
        json_summary = self.json_export.run()
        summary = {
            "project": "NIFTY 50 Market Impact Lab",
            "pipeline_version": "2.0.0",
            "status": "completed",
            "steps": ["clean_and_analyze_h1_h3", "analyze_h4_h7" if run_h4_h7 else "skip_h4_h7", "export_processed_datasets_to_jsonl"],
            "json_export": json_summary,
            "notes": [
                "JSONL files are the human-readable processed-data interchange format.",
                "CSV files are retained for compatibility and spreadsheet inspection.",
                "JSON export preserves nulls; it does not impute missing values.",
                "Existing analysis routines are isolated behind LegacyAnalysisAdapter for a safe migration path.",
            ],
        }
        (self.paths.reports / "pipeline_run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return summary
