# Methodology — NSE sector-index EDA and macroeconomic hypothesis testing

## Objective and scope

The primary statistical analysis studies 16 sector/industry index series selected in `config/sector_universe.json`, using the broad supplied NSE daily-snapshot archive as the master input. The former four broad-market series are no longer the primary outcome universe. The archive contains 180 index names across sector, broad-market, thematic, strategy/factor, volatility and fixed-income categories. The 16 selected indices are used for comparable long-history analyses.

## Data preparation

Each source file is named `ind_close_all_DDMMYYYY.csv`. The filename date is canonical; the internal `Index Date` label is retained and any mismatch is recorded. The cleaning script builds a long-format panel with the source file and mismatch flag, validates price fields, handles duplicate `(Date, IndexName)` keys, removes unusable closing values from the analytical panel, and preserves missing optional features. Returns, momentum and rolling risk features are calculated within index after sorting by date. Return calculations are not carried across observed gaps longer than seven calendar days.

The feature matrix used for the course dataset-size calculation has one row for each valid index-date row in the master panel. It contains 19 numeric price/activity/valuation/return/risk features plus 180 one-hot index-name attributes and 6 one-hot index-group attributes. Its actual dimensions are written to `reports/dataset_size_audit.json`; it is a size/audit matrix, not the direct input to macro regressions.

## EDA

The EDA focuses on the 16 primary series over their common date window. It calculates normalized price performance, daily return distributions, quantiles, skewness, excess kurtosis, annualized volatility, 20- and 60-session rolling volatility, drawdowns, worst rolling 5/20-session returns, and Pearson/Spearman correlations. Pairwise analysis compares 120 index pairs in each of three families: mean daily return, mean absolute daily return (movement-intensity proxy), and return differences conditional on at least one index returning negatively. Paired differences and Newey-West/HAC standard errors are used; Holm correction is applied within each family.

## Macroeconomic models

Each hypothesis is estimated separately for each of the 16 selected sector/industry indices. Where applicable, the code also tests slope differences directly by regressing the paired outcome difference `r_A,t - r_B,t` on the same predictor and controls. This is preferable to comparing two individual p-values. The hypothesis runner uses OLS with Newey-West/HAC standard errors for continuous-predictor models and Holm correction within named families.

- **H1:** same-date USD/INR percentage change and daily index returns.
- **H2:** CPI-derived YoY inflation and month-end monthly returns, with a one-reference-month lag sensitivity.
- **H3:** weekly FX reserve change plus USD/INR change and Friday-ending weekly returns; includes a future-reserves lead diagnostic.
- **H4:** three-session cumulative abnormal returns around supplied RBI repo-rate effective-date proxies; expected returns estimated from sessions `t-120` through `t-21`.
- **H5:** one-quarter-lagged real GVA YoY growth and quarterly returns; same-quarter sensitivity is secondary.
- **H6:** one-reference-month-lagged IIP YoY growth and monthly returns; same-month sensitivity is secondary.
- **H7:** strictly prior US-session S&P 500 return and Indian index returns, controlling for the sector index's own previous return.

## Interpretation

A p-value tests a specified null and is not a measure of effect size or the probability the null is true. An association is not a causal effect. A significant coefficient in one series and a non-significant coefficient in another does not establish a difference between coefficients; use the direct pairwise tests. Results should be reported with sample sizes, coefficients, confidence intervals, raw/adjusted p-values, and effect-size context.

## Limitations

The source archive's `_missing_dates.log` has 152 entries but has not been reconciled to the official NSE trading calendar. Three source files have internal date-label discrepancies, handled using filename dates and explicit flags. The full archive is not exclusively sector indices; the 16-series primary universe is separately defined. Macroeconomic reference periods do not always equal public release dates, and real-time vintages are absent. H4 uses effective-date proxies rather than a verified, time-stamped complete announcement calendar. H5 has approximately 12 usable quarterly observations per primary model and is exploratory/underpowered. The exact price-return versus total-return definition of every source index is not established. No causal identification, cost-aware trading strategy, or out-of-sample trading profitability is claimed.
