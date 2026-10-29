# NSE Sector Index Market Impact Lab

A single, reproducible research project studying how Indian macroeconomic variables relate to **sector and industry index returns** across a broad NSE index archive. This replaces the former four-broad-index analysis as the primary research universe. The primary inference universe is 16 long-history sector/industry indices; the complete supplied archive (180 distinct index names) is retained for data-quality audit and the encoded dataset-size requirement.

The project includes comparative EDA, seven macroeconomic hypothesis families (H1-H7), pairwise sensitivity tests, CPI-derived YoY inflation, a post-encoding dataset-size audit, machine-readable result files, JSONL exports, tests, and one Makefile. It does not include a submission PDF; the results produced here can be uploaded for the next report-writing step.

## 1. Primary research universe

The 16 primary sector/industry indices are:

- Nifty Auto
- Nifty Bank
- Nifty Commodities
- Nifty Energy
- Nifty FMCG
- Nifty Financial Services
- Nifty Infrastructure
- Nifty IT
- Nifty Media
- Nifty Metal
- Nifty Pharma
- Nifty Private Bank
- Nifty PSU Bank
- Nifty PSE
- Nifty Realty
- Nifty Services Sector

These are specified in `config/sector_universe.json`. They have long overlapping histories in the archive, which supports consistent comparisons. The raw archive contains 180 index series in total, including broad-market indices, newer sector/theme indices, factor/strategy indices, India VIX and fixed-income indices. Those other series remain in the master panel but are not mixed indiscriminately into the primary sector regressions.

The former NIFTY 50, NIFTY Next 50, NIFTY 100 and NIFTY Midcap 100 are **not** the primary outcome series in this version.

## 2. Data source and coverage

### Index data

Input: `data/raw/sector_indices.zip`, supplied as `sector_indices/daily_snapshots/ind_close_all_DDMMYYYY.csv` files. The archive contains 2,652 dated snapshots, with a date span from 2016-01-01 to 2026-09-30. Each snapshot contains all index rows reported in that file, including fields such as:

- Index Name and Index Date
- Open, high, low and closing index values
- Points change and percentage change
- Volume and turnover
- P/E, P/B and dividend yield (where available)

The source archive includes `_missing_dates.log` with 152 date strings that its collector marks as missing. This file has not been independently reconciled against the official NSE session calendar. Three snapshot files also have internal `Index Date` labels that conflict with their filename dates. The data preparation uses the structured filename date as the canonical snapshot date and records the original label and discrepancy in `reports/sector_data_quality_audit.json`.

The archive does not establish a source URL, license, full official calendar, or whether every index series is a price-return or total-return series. Fill in the true acquisition URL and terms in your final report if your instructor expects them.

### Macroeconomic source files

The original project’s raw source workbooks are retained in `data/raw/`:

- `Daily Exchange Rate of the Indian Rupee.xlsx` — daily USD/INR series
- `CPI - Rural, Urban, Combined.xlsx` — Combined CPI index and reported inflation
- `RBIB Table No. 33 _ Foreign Exchange Reserves - Weekly.xlsx` — weekly reserves
- `rbi_repo_rate.xlsx` — repo-rate effective-date data
- `Quarterly Estimates of Gross Value Added At Basic Price (At Constant Prices) New Series (Base _ 2022-23).xlsx` — quarterly real GVA
- `50 Macroeconomic Indicators.xlsx` — monthly IIP and other indicators
- `sp500_historical.csv` — historical S&P 500 prices

These files are supplied inputs; the pipeline does not download data from the web.

## 3. Installation and execution

Python 3.10+ is recommended. On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the complete workflow:

```bash
make full
```

Individual commands:

```bash
make clean-validate  # parse snapshots, build master data, audit source and encode features
make eda             # comparative EDA plus 3 paired index-index test families
make macro           # run H1-H7 for the 16 sector/industry indices
make h1              # USD/INR
make h2              # CPI-derived inflation
make h3              # FX reserves with USD/INR control and lead diagnostic
make h4              # RBI repo-rate event study
make h5              # quarterly real GVA growth
make h6              # industrial production (IIP) growth
make h7              # prior US-session S&P 500 return
make export-jsonl    # JSONL export for selected clean tables
make test            # test suite and artifact checks
make help            # print commands
```

`make full` does not alter files in `data/raw/`. It rebuilds cleaned data, runs EDA, estimates all seven macro hypothesis families, exports JSONL, and runs the checks. A full run typically takes longer than a single hypothesis because data cleaning and feature encoding scan all 2,652 snapshots.

## 4. Main outputs

| Output | Description |
|---|---|
| `data/clean/sector_index_panel_clean.csv` | All 180 index series in long format, cleaned and with engineered features |
| `data/clean/sector_indices/` | Separate clean CSV for each of the 16 primary sector/industry indices |
| `data/clean/sector_index_common_closes.csv` | Common-date close panel for the selected sector universe |
| `data/clean/sector_index_daily_returns_pct.csv` | Daily close-to-close return panel |
| `data/processed/sector_index_features_encoded.npz` | Sparse encoded feature matrix for the post-encoding size audit |
| `data/processed/encoded_feature_columns.json` | Feature names, one-hot categories and imputation counts |
| `reports/sector_data_quality_audit.md` / `.json` | Source file, date, OHLC, missing-date and selected-universe audit |
| `reports/dataset_size_audit.json` | Actual encoded matrix dimensions and `instances × attributes` arithmetic |
| `reports/eda/` | Descriptive statistics, returns, normalized price series, correlations and pairwise EDA tests |
| `reports/figures/` | Seven EDA figures |
| `reports/comparative_eda_and_hypothesis_report.md` | EDA methodology and generated comparisons |
| `reports/macro_hypotheses/unified_multi_index_macro_hypothesis_report.md` | Detailed H1-H7 methods and generated sector-index results |
| `reports/macro_hypotheses/hypothesis_results.json` / `.csv` | Combined machine-readable macro results |
| `reports/macro_hypotheses/individual_hypotheses/` | One JSON file per H1-H7 |
| `reports/macro_hypotheses/h4_repo_event_car_by_index.csv` | Event-level repo CAR calculations by sector index |
| `reports/json_dataset_manifest.json` and `data/processed_json/` | Export manifest and JSONL tables |

## 5. Dataset-size requirement

The course guideline asks for at least 3 million `instances × attributes` after encoding. The pipeline calculates this from the real generated matrix rather than hard-coding a claimed count.

The verified output for the supplied archive is:

- **Instances:** 256,577 index-date rows with a valid positive close.
- **Numeric attributes:** 19 price, valuation, activity and derived return/risk features.
- **One-hot index-name attributes:** 180.
- **One-hot index-group attributes:** 6.
- **Total encoded attributes:** 19 + 180 + 6 = 205.
- **Total cells:** 256,577 × 205 = **52,598,285**, which exceeds 3,000,000.

Missing numeric features are median-imputed within index, using a global median fallback; the per-feature imputation counts are written to `encoded_feature_columns.json`. This encoded matrix is for data preparation/dimensionality documentation and generic modelling. The macroeconomic regressions use actual index returns and original macro predictors, not the imputed values in the size-audit matrix.

## 6. EDA and cross-index tests

The EDA covers the 16 primary sector/industry series over a common sample. It produces normalized performance, daily-return distributions, box plots, 20- and 60-session rolling volatility, return correlations and drawdowns. It also runs three pairwise test families across the 16 indices (120 pairs per family):

1. Mean daily return difference.
2. Mean absolute daily-return difference as a movement-intensity proxy.
3. Conditional downside-return difference on sessions when at least one of the two indices has a negative return.

Paired return differences are used because the indices share dates and can share constituents. HAC standard errors account for some time dependence; Holm adjustment is applied within each of the three test families. The absolute-return statistic is not a formal variance-equality test, and the conditional downside comparison is not a formal expected-shortfall model.

## 7. Macroeconomic hypotheses

Each primary hypothesis is re-estimated for all 16 sector/industry series, with per-index coefficients, confidence intervals, p-values, adjusted p-values, and direct pairwise coefficient-difference tests.

| ID | Hypothesis | Main model |
|---|---|---|
| H1 | USD/INR changes and daily index returns | Daily OLS with Newey-West/HAC standard errors |
| H2 | CPI-derived YoY inflation and monthly returns | Monthly regression; same-reference-month and one-month-lag sensitivity |
| H3 | Weekly FX reserve changes and weekly returns | Reserves change plus USD/INR control; future-reserves lead diagnostic |
| H4 | RBI repo-rate events | Three-session cumulative abnormal returns around supplied effective-date proxies |
| H5 | Real GVA growth and quarterly returns | Lagged one-quarter YoY GVA growth; very short effective sample |
| H6 | IIP growth and monthly returns | Lagged one-reference-month YoY industrial production growth |
| H7 | Prior US-session S&P 500 return and Indian-sector returns | Strictly prior US session with sector index's own lag as control |

### CPI-derived inflation

The primary CPI predictor is recalculated from the Combined CPI General Index:

`inflation_yoy_derived_pct = 100 × (CPI_index[t] / CPI_index[t-12] - 1)`

The workbook's reported YoY series is retained for validation. The data-alignment audit reports the correlation and mean absolute difference between the derived and reported values.

### Statistical interpretation

- Individual per-index tests and pairwise coefficient-difference tests answer different questions. Significant slopes for two sectors do not prove their slopes differ.
- A p-value is not an effect-size measure, and non-significance is not proof of no effect.
- These are observational associations, not identified causal effects or trading-strategy results.

## 8. Limitations that are present in the report

1. The archive's missing-date log has not been independently checked against the official NSE session calendar.
2. Three internal date labels disagree with filename dates; the filename was used as canonical and these rows are flagged.
3. The archive contains multiple index types and is not exclusively sector indices. The primary 16-index universe was pre-specified to use long, overlapping histories.
4. CPI, FX, reserves, GVA and IIP source timestamps/vintages are not consistently supplied. Reference-period dates are not always the date a statistic became available to market participants.
5. H4 uses effective-date proxies, not a verified complete announcement calendar with time-stamped policy surprises.
6. H5 has roughly 12 usable quarterly observations per primary model and is underpowered/exploratory.
7. The source does not document every index's price-return vs total-return definition; dividend treatment must be verified before claiming investor total returns.
8. Holm correction is within named test families; many hypothesis families are still examined overall.
9. No causal or profitability claims, transaction costs, slippage, or out-of-sample trading strategy are evaluated.
