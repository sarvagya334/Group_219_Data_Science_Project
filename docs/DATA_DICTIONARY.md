# Data dictionary — NSE Sector Index Market Impact Lab

## Raw inputs (`data/raw/`)

| Source | Contents | Frequency | Role |
|---|---|---|---|
| `sector_indices.zip` | 2,652 dated snapshot CSVs, 180 distinct index names | Daily snapshot | Master source panel, size audit and primary 16-index analyses |
| `Daily Exchange Rate of the Indian Rupee.xlsx` | USD/INR level | Daily | H1 predictor and H3 control |
| `CPI - Rural, Urban, Combined.xlsx` | Combined CPI level and reported YoY inflation | Monthly reference period | H2; derives YoY inflation from CPI level |
| `RBIB Table No. 33 _ Foreign Exchange Reserves - Weekly.xlsx` | Foreign-exchange reserves | Weekly | H3 predictor |
| `rbi_repo_rate.xlsx` | Repo effective date, repo rate and rate change | Event dates | H4 event study |
| `Quarterly Estimates ... (Base _ 2022-23).xlsx` | GVA at Basic Prices, constant prices | Quarterly | H5 predictor |
| `50 Macroeconomic Indicators.xlsx` | IIP and related indicators | Monthly | H6 predictor |
| `sp500_historical.csv` | S&P 500 historical price series | US session | H7 predictor |

The snapshot archive contains sector/industry indices as well as broad-market, thematic, factor/strategy, volatility and fixed-income indices. `config/sector_universe.json` defines the 16 primary sector/industry indices used for comparable statistical analysis.

## Main clean outputs

| File | Purpose |
|---|---|
| `data/clean/sector_index_panel_clean.csv` | Long-format master panel of cleaned rows from all archive index names, including canonical filename date, original internal date label, source filename, mismatch flag, raw market fields and engineered features |
| `data/clean/sector_indices/*_clean.csv` | Individual clean series for the 16 primary indices |
| `data/clean/sector_index_common_closes.csv` | Common-date closing-value panel for the selected 16 series |
| `data/clean/sector_index_daily_returns_pct.csv` | Common-date daily simple returns in percent |
| `data/clean/macro/cpi_inflation_derived_clean.csv` | Combined CPI level, derived YoY inflation, source-reported rate and comparison fields |
| `data/clean/macro/usd_inr_daily_clean.csv` | USD/INR level and percent change |
| `data/clean/macro/fx_reserves_weekly_clean.csv` | Weekly reserves level and change |
| `data/clean/macro/gva_quarterly_2022_23_base_clean.csv` | Constant-price GVA and derived growth measures |
| `data/clean/macro/iip_monthly_clean.csv` | IIP and derived YoY growth |
| `data/clean/macro/sp500_daily_clean.csv` | S&P 500 daily returns |
| `data/processed/sector_index_features_encoded.npz` | Sparse encoded feature matrix used for dataset-size audit |
| `data/processed/encoded_feature_columns.json` | Encoded column definitions and imputation metadata |

## Feature definitions

- `return_pct`: `100 × (Close_t / Close_(t-1) - 1)` within each index; missing across observed gaps longer than seven calendar days.
- `log_return_pct`: `100 × log(Close_t / Close_(t-1))`.
- `momentum_5d_pct`, `momentum_20d_pct`: close-to-close percentage change over the previous 5 or 20 observed rows.
- `volatility_20d_pct`, `volatility_60d_pct`: rolling return standard deviation multiplied by √252, subject to minimum observations coded in the pipeline.
- `high_low_range_pct`: `100 × (High - Low) / Close`.
- `open_gap_pct`: `100 × (Open / previous Close - 1)`.
- `inflation_yoy_derived_pct`: `100 × (Combined CPI_t / Combined CPI_(t-12) - 1)`.
- `IndexGroup`: a documented heuristic group label (e.g. sector/theme, broad-market, strategy/factor, fixed income/rate, volatility, other); it is useful for audit/encoding, not a claim of official NSE classification.

## Encoded dataset size

The encoded matrix has one row per valid index-date observation in the full archive. The current generated audit reports 256,577 instances × 205 encoded attributes = 52,598,285 cells. The 205 columns are 19 numeric attributes, 180 one-hot index names and 6 one-hot index groups. See `reports/dataset_size_audit.json`; do not hard-code these dimensions in any final report without rerunning the size audit after changes.
