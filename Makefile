.PHONY: help install clean-validate eda macro hypotheses h1 h2 h3 h4 h5 h6 h7 export-jsonl test full clean
PYTHON ?= python3

help:
	@echo "NSE Sector Index Market Impact Lab"
	@echo "  make install         Install dependencies"
	@echo "  make clean-validate  Build/clean all sector-index snapshots and audit data"
	@echo "  make eda             Run 16-sector comparative EDA and paired tests"
	@echo "  make macro           Run H1-H7 macroeconomic hypotheses across 16 sector indices"
	@echo "  make h1 ... make h7  Run one macro hypothesis across the sector-index universe"
	@echo "  make export-jsonl    Export selected clean tables to JSONL"
	@echo "  make test            Run automated tests and artifact checks"
	@echo "  make full            Run data build, EDA, H1-H7, exports, and tests"
	@echo "  make clean           Remove generated outputs (raw inputs kept)"

install:
	$(PYTHON) -m pip install -r requirements.txt

clean-validate:
	$(PYTHON) scripts/clean_and_validate.py

eda: clean-validate
	$(PYTHON) scripts/run_eda.py

macro: clean-validate
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis all

hypotheses: macro

h1: clean-validate
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis H1
h2: clean-validate
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis H2
h3: clean-validate
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis H3
h4: clean-validate
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis H4
h5: clean-validate
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis H5
h6: clean-validate
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis H6
h7: clean-validate
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis H7

export-jsonl:
	$(PYTHON) scripts/export_jsonl.py

test:
	$(PYTHON) -m pytest -q
	$(PYTHON) scripts/verify_audit.py
	$(PYTHON) scripts/verify_eda.py

full: clean-validate
	$(PYTHON) scripts/run_eda.py
	$(PYTHON) scripts/run_macro_hypotheses.py --hypothesis all
	$(PYTHON) scripts/export_jsonl.py
	$(PYTHON) -m pytest -q
	$(PYTHON) scripts/verify_audit.py
	$(PYTHON) scripts/verify_eda.py

clean:
	rm -f data/clean/*.csv data/clean/macro/*.csv data/clean/sector_indices/*.csv
	rm -f data/processed/sector_index_features_encoded.npz data/processed/encoded_feature_columns.json
	rm -f data/processed_json/*.jsonl
	rm -f reports/*.json reports/*.md reports/eda/*.csv reports/eda/*.json reports/hypothesis_tests/*.csv reports/hypothesis_tests/*.json reports/figures/*.png
	rm -f reports/macro_hypotheses/*.json reports/macro_hypotheses/*.csv reports/macro_hypotheses/*.md reports/macro_hypotheses/figures/*.png reports/macro_hypotheses/individual_hypotheses/*.json reports/json_dataset_manifest.json
