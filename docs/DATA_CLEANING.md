# Data cleaning and validation rules

1. The supplied `data/raw/sector_indices.zip` is treated as an immutable source. It contains daily snapshot CSVs; all source index names are retained in the master panel.
2. The snapshot filename `ind_close_all_DDMMYYYY.csv` is the canonical date because three files have internal `Index Date` labels that disagree with their filenames. Both fields are preserved and mismatches are flagged in the audit.
3. Required index fields are `Index Name`, `Index Date`, OHLC fields, and closing value. Missing optional valuation/activity data are preserved as missing rather than filled in the raw master panel.
4. Duplicate records are checked using `(filename date, IndexName)`. Conflicting OHLC duplicates cause the script to fail; exact duplicates can be deduplicated and counted in the audit.
5. Rows with missing, nonnumeric or nonpositive close values are not treated as usable price observations. OHLC checks verify positive prices and that High/Low bounds are consistent with Open, Close and one another when values are present.
6. Weekend records are not automatically removed. NSE may have special sessions, and the archive's missing-date log is not an authoritative exchange calendar. Official session completeness remains unverified.
7. The primary inference universe is defined in `config/sector_universe.json`: 16 long-history sector/industry indices. The full 180-index archive stays in the master panel and size-audit matrix, but is not mixed indiscriminately into the primary EDA or macro regressions.
8. Returns and rolling features are computed after sorting each index by date. Returns are set missing across observed gaps longer than seven calendar days; no return is manufactured across those gaps.
9. Categorical index names and index groups are one-hot encoded for the dataset-size audit. Numeric feature missing values are median-imputed within index with a global median fallback. Imputation counts are recorded in the encoded feature metadata. Macro regressions use the cleaned outcome series and source predictors, not the imputed size-audit matrix.
10. CPI is filtered to the All-India Combined General Index. Derived YoY inflation is `100 * (CPI_t / CPI_(t-12) - 1)` and compared with the workbook's reported value.
11. FX, reserves, repo, GVA, IIP and S&P series are cleaned at their native frequencies. No fictional daily values are added via forward fill. Reference dates are not assumed to be public release timestamps.
12. For S&P alignment, same-date US closes are disallowed for Indian returns because the US close follows the Indian session on a shared calendar date.
13. JSONL exports serialize missing values as JSON `null` and include row/column/missing-value metadata in a manifest.
