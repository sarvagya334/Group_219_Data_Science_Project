# Comparative EDA and Cross-Index Hypothesis Tests

**Observed sample:** 2016-01-05 to 2026-09-30.
**Common closes:** 2,650; **close-to-close return observations:** 2,649.

## Executive summary

This report compares 16 long-history NSE sector/industry index series on common dates. It describes performance, return distributions, volatility, correlation and drawdowns, then tests paired differences in mean returns, absolute returns and conditional downside returns.

This is index-level descriptive/inferential analysis. It is not a causal analysis of macroeconomic events and does not establish a profitable trading strategy.

## Descriptive statistics

Returns are simple close-to-close percentage changes. Annualized volatility is daily standard deviation multiplied by sqrt(252). Annualized mean return is the arithmetic daily mean multiplied by 252 and is not CAGR.

| Index | Cumulative return (%) | Annualized volatility (%) | Mean daily return (%) | Skew | Excess kurtosis | Max drawdown (%) | Worst 5-session return (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Nifty Auto | 223.64 | 21.90 | 0.0539 | -0.221 | 9.010 | -62.38 | -20.83 |
| Nifty Bank | 230.26 | 21.44 | 0.0543 | -0.721 | 16.001 | -47.86 | -26.77 |
| Nifty Commodities | 280.96 | 19.85 | 0.0584 | -0.896 | 9.236 | -50.27 | -17.22 |
| Nifty Energy | 328.24 | 20.57 | 0.0634 | -0.720 | 8.683 | -41.23 | -19.25 |
| Nifty FMCG | 122.02 | 15.99 | 0.0352 | -0.123 | 11.248 | -32.87 | -14.62 |
| Nifty Financial Services | 257.67 | 20.69 | 0.0567 | -0.831 | 15.309 | -43.54 | -25.40 |
| Nifty Infrastructure | 220.68 | 18.31 | 0.0507 | -0.809 | 11.088 | -43.58 | -16.22 |
| Nifty IT | 151.93 | 21.45 | 0.0440 | -0.204 | 4.986 | -43.97 | -20.51 |
| Nifty Media | -38.96 | 27.42 | -0.0036 | -0.314 | 9.157 | -72.90 | -21.54 |
| Nifty Metal | 585.05 | 27.87 | 0.0881 | -0.423 | 3.595 | -64.33 | -21.86 |
| Nifty Pharma | 125.17 | 18.94 | 0.0378 | 0.091 | 5.185 | -46.11 | -14.15 |
| Nifty Private Bank | 191.42 | 21.78 | 0.0499 | -0.799 | 18.257 | -49.90 | -28.53 |
| Nifty PSU Bank | 189.63 | 32.66 | 0.0611 | 0.918 | 19.424 | -73.28 | -23.86 |
| Nifty PSE | 198.71 | 21.29 | 0.0504 | -1.134 | 12.619 | -54.59 | -18.29 |
| Nifty Realty | 382.68 | 29.15 | 0.0764 | -0.411 | 3.350 | -56.44 | -22.53 |
| Nifty Services Sector | 188.90 | 17.46 | 0.0462 | -1.083 | 16.414 | -40.17 | -21.22 |

## Figures

1. `reports/figures/01_normalized_performance.png`: all selected sector indices rebased to 100 at the first common close.
2. `reports/figures/02_daily_returns.png`: daily returns over time.
3. `reports/figures/03_return_boxplots.png`: return distributions; plotted outliers are hidden for readability but retained in calculations.
4. `reports/figures/04_rolling_volatility_20d.png` and `05_rolling_volatility_60d.png`: rolling annualized volatility.
5. `reports/figures/06_return_correlation_heatmap.png`: Pearson return correlation matrix.
6. `reports/figures/07_drawdowns.png`: drawdown from running peak.

## EDA interpretation guide

- **Normalized performance:** compares growth of 1 unit invested in each price series from a shared start; it does not account for dividends unless the source index itself does.
- **Return distributions:** skewness indicates asymmetry; excess kurtosis indicates heavier/lighter tails than a Gaussian distribution. Extreme observations should be source-checked, not automatically deleted.
- **Rolling volatility:** shows time-varying risk; 20-session estimates react faster and are noisier than 60-session estimates.
- **Correlation:** high positive correlation means daily returns often move together, not that one causes the other. Overlapping constituents naturally raise dependence.
- **Drawdown:** loss from the prior running peak. Recovery time is measured in calendar days after the maximum-drawdown trough, and is null if not recovered by sample end.
- **Stress metrics:** worst 5/20-session returns are descriptive sample extrema and can be sensitive to the chosen period.

## Cross-index hypothesis testing

The test runner uses paired return differences because indices are observed on the same dates and have overlapping constituents. Each pairwise difference series is tested with an intercept-only OLS model using Newey-West/HAC standard errors with up to five lags. Holm correction is applied within each family of 120 pairwise comparisons. Alpha is 0.05.

### H1 — Mean daily return difference

For each pair A and B: H0: E[r_A − r_B] = 0; H1: E[r_A − r_B] ≠ 0. The estimate is in percentage points per day. A statistically significant result does not automatically imply an economically meaningful difference.

### H2 — Absolute-return intensity difference

For each pair: H0: E[|r_A| − |r_B|] = 0. Absolute return is used as a scale/volatility-intensity proxy. It is not the same as testing equality of variance or annualized standard deviation.

### H3 — Conditional downside-return difference

For each pair: compare r_A − r_B on dates when at least one index has a negative return. This asks whether the relative return differs on down days for at least one index. It is not a formal tail-dependence or CVaR test.

### Results

| Family | Pair | Estimate (pp/day) | HAC 95% CI | Raw p-value | Holm p-value | Decision at 5% | n |
|---|---|---:|---|---:|---:|---|---:|
| H1_mean_daily_return_difference | Nifty Auto − Nifty Bank | -0.00041 | [-0.04271, 0.04188] | 0.9847 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Bank | 0.06719 | [0.03026, 0.10411] | 0.0003626 | 0.01269 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Bank | -0.05376 | [-0.11247, 0.00495] | 0.07271 | 1 | Do not reject H0 | 1630 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Commodities | -0.00449 | [-0.04247, 0.03349] | 0.8167 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Commodities | 0.07053 | [0.03683, 0.10424] | 4.101e-05 | 0.001517 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Commodities | -0.08504 | [-0.14181, -0.02827] | 0.003323 | 0.1928 | Do not reject H0 | 1565 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Energy | -0.00949 | [-0.05583, 0.03685] | 0.6883 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Energy | 0.03511 | [-0.00649, 0.07670] | 0.09806 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Energy | -0.05327 | [-0.12189, 0.01534] | 0.1281 | 1 | Do not reject H0 | 1642 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty FMCG | 0.01869 | [-0.02610, 0.06349] | 0.4134 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty FMCG | 0.25196 | [0.21325, 0.29067] | 2.83e-37 | 2.179e-35 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty FMCG | -0.13103 | [-0.18983, -0.07223] | 1.257e-05 | 0.0009176 | Reject H0 | 1712 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Financial Services | -0.00280 | [-0.04324, 0.03765] | 0.8922 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Financial Services | 0.09404 | [0.05890, 0.12918] | 1.563e-07 | 7.034e-06 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Financial Services | -0.07339 | [-0.13059, -0.01619] | 0.01191 | 0.5718 | Do not reject H0 | 1637 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Infrastructure | 0.00319 | [-0.03208, 0.03846] | 0.8593 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Infrastructure | 0.14386 | [0.11004, 0.17768] | 7.594e-17 | 4.405e-15 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Infrastructure | -0.12116 | [-0.17111, -0.07121] | 1.992e-06 | 0.0001534 | Reject H0 | 1570 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty IT | 0.00986 | [-0.04921, 0.06892] | 0.7436 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty IT | 0.00780 | [-0.04046, 0.05605] | 0.7515 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty IT | 0.02004 | [-0.05770, 0.09778] | 0.6134 | 1 | Do not reject H0 | 1787 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Media | 0.05753 | [0.00207, 0.11298] | 0.04202 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Media | -0.24767 | [-0.30079, -0.19456] | 6.285e-20 | 3.834e-18 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Media | 0.19164 | [0.11970, 0.26359] | 1.781e-07 | 1.461e-05 | Reject H0 | 1692 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Metal | -0.03427 | [-0.08958, 0.02105] | 0.2247 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Metal | -0.31548 | [-0.35970, -0.27126] | 1.948e-44 | 1.598e-42 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Metal | 0.14362 | [0.06235, 0.22490] | 0.0005331 | 0.03412 | Reject H0 | 1635 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Pharma | 0.01613 | [-0.03548, 0.06774] | 0.5403 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Pharma | 0.09635 | [0.05069, 0.14201] | 3.532e-05 | 0.001413 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Pharma | -0.02528 | [-0.10019, 0.04964] | 0.5085 | 1 | Do not reject H0 | 1716 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Private Bank | 0.00401 | [-0.03845, 0.04646] | 0.8532 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Private Bank | 0.05940 | [0.02164, 0.09716] | 0.002048 | 0.06347 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Private Bank | -0.03408 | [-0.09318, 0.02502] | 0.2584 | 1 | Do not reject H0 | 1641 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty PSU Bank | -0.00723 | [-0.07463, 0.06016] | 0.8334 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty PSU Bank | -0.47714 | [-0.53748, -0.41680] | 3.52e-54 | 3.098e-52 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty PSU Bank | 0.26608 | [0.18269, 0.34948] | 4.014e-10 | 3.733e-08 | Reject H0 | 1707 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty PSE | 0.00348 | [-0.04217, 0.04913] | 0.8813 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty PSE | 0.01609 | [-0.02798, 0.06016] | 0.4742 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty PSE | -0.03334 | [-0.10183, 0.03515] | 0.3401 | 1 | Do not reject H0 | 1615 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Realty | -0.02250 | [-0.07900, 0.03400] | 0.435 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Realty | -0.38624 | [-0.43416, -0.33832] | 3.249e-56 | 2.942e-54 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Realty | 0.18557 | [0.11294, 0.25821] | 5.512e-07 | 4.299e-05 | Reject H0 | 1634 |
| H1_mean_daily_return_difference | Nifty Auto − Nifty Services Sector | 0.00773 | [-0.03002, 0.04547] | 0.6883 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Auto − Nifty Services Sector | 0.21964 | [0.18706, 0.25222] | 7.538e-40 | 5.955e-38 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Auto − Nifty Services Sector | -0.14470 | [-0.19773, -0.09166] | 8.94e-08 | 7.599e-06 | Reject H0 | 1601 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Commodities | -0.00408 | [-0.04394, 0.03579] | 0.8411 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Commodities | 0.00335 | [-0.03482, 0.04152] | 0.8635 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Commodities | -0.03396 | [-0.09692, 0.02900] | 0.2905 | 1 | Do not reject H0 | 1570 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Energy | -0.00907 | [-0.05502, 0.03688] | 0.6988 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Energy | -0.03208 | [-0.07592, 0.01176] | 0.1516 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Energy | -0.00940 | [-0.07914, 0.06035] | 0.7918 | 1 | Do not reject H0 | 1636 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty FMCG | 0.01911 | [-0.02730, 0.06551] | 0.4196 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty FMCG | 0.18478 | [0.14031, 0.22924] | 3.801e-16 | 2.166e-14 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty FMCG | -0.08718 | [-0.15281, -0.02155] | 0.009229 | 0.4707 | Do not reject H0 | 1719 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Financial Services | -0.00238 | [-0.01460, 0.00984] | 0.7024 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Financial Services | 0.02685 | [0.01408, 0.03962] | 3.779e-05 | 0.001474 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Financial Services | -0.02790 | [-0.04621, -0.00960] | 0.00281 | 0.1658 | Do not reject H0 | 1360 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Infrastructure | 0.00360 | [-0.03182, 0.03903] | 0.8419 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Infrastructure | 0.07668 | [0.04064, 0.11271] | 3.038e-05 | 0.001246 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Infrastructure | -0.05917 | [-0.11336, -0.00498] | 0.03234 | 1 | Do not reject H0 | 1574 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty IT | 0.01027 | [-0.04946, 0.07000] | 0.7361 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty IT | -0.05939 | [-0.11048, -0.00830] | 0.0227 | 0.4767 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty IT | 0.04648 | [-0.03670, 0.12967] | 0.2734 | 1 | Do not reject H0 | 1782 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Media | 0.05794 | [0.00116, 0.11473] | 0.04552 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Media | -0.31486 | [-0.37147, -0.25825] | 1.142e-27 | 8.106e-26 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Media | 0.22523 | [0.14932, 0.30115] | 6.064e-09 | 5.457e-07 | Reject H0 | 1723 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Metal | -0.03385 | [-0.09061, 0.02291] | 0.2425 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Metal | -0.38267 | [-0.42940, -0.33593] | 5.775e-58 | 5.313e-56 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Metal | 0.19405 | [0.11080, 0.27731] | 4.916e-06 | 0.0003687 | Reject H0 | 1638 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Pharma | 0.01654 | [-0.04125, 0.07433] | 0.5748 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Pharma | 0.02916 | [-0.02102, 0.07935] | 0.2547 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Pharma | 0.01379 | [-0.07202, 0.09959] | 0.7528 | 1 | Do not reject H0 | 1747 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Private Bank | 0.00442 | [-0.00375, 0.01259] | 0.2887 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Private Bank | -0.00778 | [-0.01616, 0.00059] | 0.06862 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Private Bank | 0.01562 | [0.00374, 0.02750] | 0.009946 | 0.4874 | Do not reject H0 | 1325 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty PSU Bank | -0.00682 | [-0.06190, 0.04825] | 0.8082 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty PSU Bank | -0.54433 | [-0.59919, -0.48947] | 3.103e-84 | 3.352e-82 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty PSU Bank | 0.39700 | [0.32738, 0.46662] | 5.324e-29 | 6.23e-27 | Reject H0 | 1582 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty PSE | 0.00389 | [-0.04219, 0.04998] | 0.8685 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty PSE | -0.05110 | [-0.09864, -0.00355] | 0.03518 | 0.7037 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty PSE | 0.00383 | [-0.06768, 0.07533] | 0.9165 | 1 | Do not reject H0 | 1628 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Realty | -0.02209 | [-0.07986, 0.03568] | 0.4536 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Realty | -0.45343 | [-0.50434, -0.40252] | 3.095e-68 | 3.064e-66 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Realty | 0.26636 | [0.19119, 0.34153] | 3.792e-12 | 3.716e-10 | Reject H0 | 1605 |
| H1_mean_daily_return_difference | Nifty Bank − Nifty Services Sector | 0.00814 | [-0.01307, 0.02935] | 0.4519 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Bank − Nifty Services Sector | 0.15245 | [0.13152, 0.17339] | 3.158e-46 | 2.621e-44 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Bank − Nifty Services Sector | -0.12690 | [-0.15903, -0.09477] | 9.846e-15 | 1.004e-12 | Reject H0 | 1435 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Energy | -0.00499 | [-0.03103, 0.02104] | 0.707 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Energy | -0.03543 | [-0.05934, -0.01152] | 0.003685 | 0.1106 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Energy | 0.02697 | [-0.01265, 0.06660] | 0.1821 | 1 | Do not reject H0 | 1450 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty FMCG | 0.02319 | [-0.01849, 0.06487] | 0.2756 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty FMCG | 0.18143 | [0.14642, 0.21644] | 3.096e-24 | 2.044e-22 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty FMCG | -0.07633 | [-0.13694, -0.01572] | 0.01358 | 0.6381 | Do not reject H0 | 1682 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Financial Services | 0.00170 | [-0.03637, 0.03976] | 0.9304 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Financial Services | 0.02350 | [-0.01288, 0.05988] | 0.2055 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Financial Services | 0.00709 | [-0.05440, 0.06858] | 0.8212 | 1 | Do not reject H0 | 1572 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Infrastructure | 0.00768 | [-0.01507, 0.03043] | 0.5081 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Infrastructure | 0.07333 | [0.05219, 0.09447] | 1.059e-11 | 5.4e-10 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Infrastructure | -0.05476 | [-0.09012, -0.01939] | 0.002408 | 0.1445 | Do not reject H0 | 1425 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty IT | 0.01435 | [-0.04035, 0.06904] | 0.6071 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty IT | -0.06274 | [-0.10640, -0.01908] | 0.004858 | 0.136 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty IT | 0.06365 | [-0.01104, 0.13834] | 0.09485 | 1 | Do not reject H0 | 1743 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Media | 0.06202 | [0.01102, 0.11302] | 0.01715 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Media | -0.31821 | [-0.36553, -0.27088] | 1.165e-39 | 9.084e-38 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Media | 0.26706 | [0.19937, 0.33475] | 1.052e-14 | 1.063e-12 | Reject H0 | 1651 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Metal | -0.02977 | [-0.06290, 0.00335] | 0.07812 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Metal | -0.38601 | [-0.41491, -0.35712] | 3.721e-151 | 4.465e-149 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Metal | 0.31798 | [0.27379, 0.36217] | 3.586e-45 | 4.303e-43 | Reject H0 | 1419 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Pharma | 0.02062 | [-0.02488, 0.06611] | 0.3744 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Pharma | 0.02581 | [-0.01354, 0.06517] | 0.1986 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Pharma | 0.02305 | [-0.04419, 0.09029] | 0.5017 | 1 | Do not reject H0 | 1679 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Private Bank | 0.00850 | [-0.03241, 0.04941] | 0.6839 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Private Bank | -0.01113 | [-0.05074, 0.02848] | 0.5818 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Private Bank | 0.04722 | [-0.01692, 0.11136] | 0.1491 | 1 | Do not reject H0 | 1579 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty PSU Bank | -0.00274 | [-0.06416, 0.05867] | 0.9303 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty PSU Bank | -0.54768 | [-0.60095, -0.49441] | 2.653e-90 | 2.892e-88 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty PSU Bank | 0.37791 | [0.30580, 0.45003] | 9.542e-25 | 1.097e-22 | Reject H0 | 1639 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty PSE | 0.00797 | [-0.01618, 0.03212] | 0.5178 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty PSE | -0.05444 | [-0.08038, -0.02851] | 3.891e-05 | 0.001479 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty PSE | 0.05539 | [0.01468, 0.09609] | 0.007653 | 0.3979 | Do not reject H0 | 1431 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Realty | -0.01801 | [-0.07218, 0.03616] | 0.5146 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Realty | -0.45678 | [-0.50072, -0.41284] | 2.857e-92 | 3.143e-90 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Realty | 0.29159 | [0.22000, 0.36318] | 1.422e-15 | 1.479e-13 | Reject H0 | 1560 |
| H1_mean_daily_return_difference | Nifty Commodities − Nifty Services Sector | 0.01222 | [-0.02042, 0.04485] | 0.4631 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Commodities − Nifty Services Sector | 0.14911 | [0.11943, 0.17878] | 7.069e-23 | 4.454e-21 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Commodities − Nifty Services Sector | -0.08763 | [-0.13888, -0.03638] | 0.000805 | 0.05071 | Do not reject H0 | 1534 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty FMCG | 0.02818 | [-0.01865, 0.07501] | 0.2382 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty FMCG | 0.21686 | [0.17706, 0.25666] | 1.276e-26 | 8.802e-25 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty FMCG | -0.06832 | [-0.13574, -0.00089] | 0.04705 | 1 | Do not reject H0 | 1727 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty Financial Services | 0.00669 | [-0.03773, 0.05111] | 0.7679 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty Financial Services | 0.05893 | [0.01703, 0.10083] | 0.005842 | 0.1524 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty Financial Services | -0.00585 | [-0.07502, 0.06332] | 0.8684 | 1 | Do not reject H0 | 1638 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty Infrastructure | 0.01268 | [-0.01753, 0.04288] | 0.4108 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty Infrastructure | 0.10876 | [0.08112, 0.13639] | 1.228e-14 | 6.629e-13 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty Infrastructure | -0.06453 | [-0.11019, -0.01887] | 0.005608 | 0.3028 | Do not reject H0 | 1480 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty IT | 0.01934 | [-0.03983, 0.07852] | 0.5218 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty IT | -0.02731 | [-0.07443, 0.01981] | 0.256 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty IT | 0.04697 | [-0.03323, 0.12718] | 0.251 | 1 | Do not reject H0 | 1793 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty Media | 0.06701 | [0.01101, 0.12302] | 0.01902 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty Media | -0.28278 | [-0.33409, -0.23147] | 3.358e-27 | 2.35e-25 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty Media | 0.24778 | [0.17537, 0.32019] | 1.99e-11 | 1.91e-09 | Reject H0 | 1712 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty Metal | -0.02478 | [-0.07518, 0.02562] | 0.3352 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty Metal | -0.35059 | [-0.39225, -0.30892] | 4.252e-61 | 4.039e-59 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty Metal | 0.21476 | [0.14209, 0.28743] | 6.936e-09 | 6.173e-07 | Reject H0 | 1596 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty Pharma | 0.02561 | [-0.02521, 0.07643] | 0.3233 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty Pharma | 0.06124 | [0.01727, 0.10521] | 0.006336 | 0.1584 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty Pharma | 0.00636 | [-0.06373, 0.07646] | 0.8588 | 1 | Do not reject H0 | 1738 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty Private Bank | 0.01349 | [-0.03371, 0.06070] | 0.5753 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty Private Bank | 0.02430 | [-0.02088, 0.06947] | 0.2918 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty Private Bank | 0.01799 | [-0.05275, 0.08872] | 0.6182 | 1 | Do not reject H0 | 1647 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty PSU Bank | 0.00225 | [-0.06329, 0.06779] | 0.9463 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty PSU Bank | -0.51225 | [-0.56875, -0.45575] | 1.193e-70 | 1.229e-68 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty PSU Bank | 0.33146 | [0.25318, 0.40974] | 1.051e-16 | 1.114e-14 | Reject H0 | 1693 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty PSE | 0.01296 | [-0.01498, 0.04091] | 0.3632 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty PSE | -0.01902 | [-0.04550, 0.00747] | 0.1593 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty PSE | 0.04232 | [-0.00171, 0.08635] | 0.05959 | 1 | Do not reject H0 | 1450 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty Realty | -0.01302 | [-0.07323, 0.04719] | 0.6717 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty Realty | -0.42135 | [-0.47200, -0.37070] | 9.038e-60 | 8.405e-58 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty Realty | 0.24168 | [0.15816, 0.32519] | 1.414e-08 | 1.245e-06 | Reject H0 | 1630 |
| H1_mean_daily_return_difference | Nifty Energy − Nifty Services Sector | 0.01721 | [-0.02184, 0.05626] | 0.3877 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Energy − Nifty Services Sector | 0.18453 | [0.14873, 0.22034] | 5.432e-24 | 3.476e-22 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Energy − Nifty Services Sector | -0.09400 | [-0.15294, -0.03505] | 0.001775 | 0.1101 | Do not reject H0 | 1603 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty Financial Services | -0.02149 | [-0.06462, 0.02164] | 0.3288 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty Financial Services | -0.15793 | [-0.19990, -0.11595] | 1.648e-13 | 8.734e-12 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty Financial Services | 0.07315 | [0.00925, 0.13704] | 0.02485 | 1 | Do not reject H0 | 1706 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty Infrastructure | -0.01550 | [-0.05295, 0.02194] | 0.4171 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty Infrastructure | -0.10810 | [-0.13992, -0.07628] | 2.782e-11 | 1.391e-09 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty Infrastructure | 0.04984 | [-0.00271, 0.10238] | 0.06302 | 1 | Do not reject H0 | 1674 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty IT | -0.00884 | [-0.06214, 0.04446] | 0.7452 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty IT | -0.24417 | [-0.28544, -0.20290] | 4.297e-31 | 3.137e-29 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty IT | 0.10894 | [0.03942, 0.17846] | 0.00213 | 0.13 | Do not reject H0 | 1824 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty Media | 0.03883 | [-0.02141, 0.09908] | 0.2064 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty Media | -0.49964 | [-0.55521, -0.44407] | 1.638e-69 | 1.671e-67 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty Media | 0.27004 | [0.19134, 0.34874] | 1.758e-11 | 1.705e-09 | Reject H0 | 1776 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty Metal | -0.05296 | [-0.11521, 0.00929] | 0.09543 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty Metal | -0.56744 | [-0.61649, -0.51840] | 7.502e-114 | 8.403e-112 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty Metal | 0.23008 | [0.14479, 0.31536] | 1.239e-07 | 1.028e-05 | Reject H0 | 1736 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty Pharma | -0.00257 | [-0.04845, 0.04331] | 0.9126 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty Pharma | -0.15561 | [-0.19388, -0.11735] | 1.584e-15 | 8.872e-14 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty Pharma | 0.08798 | [0.02609, 0.14986] | 0.005333 | 0.2933 | Do not reject H0 | 1753 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty Private Bank | -0.01469 | [-0.06162, 0.03224] | 0.5396 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty Private Bank | -0.19256 | [-0.23771, -0.14742] | 6.273e-17 | 3.701e-15 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty Private Bank | 0.09875 | [0.03246, 0.16504] | 0.003504 | 0.1997 | Do not reject H0 | 1728 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty PSU Bank | -0.02593 | [-0.10064, 0.04878] | 0.4964 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty PSU Bank | -0.72911 | [-0.79162, -0.66659] | 1.173e-115 | 1.326e-113 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty PSU Bank | 0.34317 | [0.25331, 0.43304] | 7.155e-14 | 7.155e-12 | Reject H0 | 1796 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty PSE | -0.01522 | [-0.06303, 0.03260] | 0.5328 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty PSE | -0.23587 | [-0.28050, -0.19125] | 3.76e-25 | 2.519e-23 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty PSE | 0.09852 | [0.03109, 0.16595] | 0.004187 | 0.2345 | Do not reject H0 | 1722 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty Realty | -0.04120 | [-0.10689, 0.02449] | 0.219 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty Realty | -0.63821 | [-0.68957, -0.58685] | 5.093e-131 | 5.958e-129 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty Realty | 0.28161 | [0.19587, 0.36735] | 1.214e-10 | 1.141e-08 | Reject H0 | 1718 |
| H1_mean_daily_return_difference | Nifty FMCG − Nifty Services Sector | -0.01097 | [-0.04785, 0.02591] | 0.56 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty FMCG − Nifty Services Sector | -0.03232 | [-0.06686, 0.00221] | 0.06659 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty FMCG − Nifty Services Sector | 0.00468 | [-0.05070, 0.06006] | 0.8685 | 1 | Do not reject H0 | 1682 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty Infrastructure | 0.00599 | [-0.02693, 0.03891] | 0.7215 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty Infrastructure | 0.04983 | [0.01582, 0.08383] | 0.004078 | 0.1183 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty Infrastructure | -0.03768 | [-0.09032, 0.01497] | 0.1607 | 1 | Do not reject H0 | 1574 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty IT | 0.01265 | [-0.04393, 0.06923] | 0.6612 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty IT | -0.08624 | [-0.13500, -0.03748] | 0.0005275 | 0.01794 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty IT | 0.06981 | [-0.00936, 0.14899] | 0.08396 | 1 | Do not reject H0 | 1772 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty Media | 0.06032 | [0.00363, 0.11702] | 0.03703 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty Media | -0.34171 | [-0.39852, -0.28490] | 4.423e-32 | 3.317e-30 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty Media | 0.23322 | [0.15205, 0.31439] | 1.786e-08 | 1.536e-06 | Reject H0 | 1720 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty Metal | -0.03147 | [-0.08778, 0.02485] | 0.2734 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty Metal | -0.40952 | [-0.45594, -0.36309] | 5.758e-67 | 5.586e-65 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty Metal | 0.21608 | [0.13240, 0.29977] | 4.173e-07 | 3.297e-05 | Reject H0 | 1637 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty Pharma | 0.01892 | [-0.03652, 0.07437] | 0.5036 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty Pharma | 0.00231 | [-0.04699, 0.05161] | 0.9268 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty Pharma | 0.02831 | [-0.05544, 0.11207] | 0.5076 | 1 | Do not reject H0 | 1750 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty Private Bank | 0.00680 | [-0.00743, 0.02104] | 0.3488 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty Private Bank | -0.03463 | [-0.04885, -0.02042] | 1.8e-06 | 7.908e-05 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty Private Bank | 0.04534 | [0.02410, 0.06657] | 2.863e-05 | 0.002032 | Reject H0 | 1396 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty PSU Bank | -0.00444 | [-0.06405, 0.05517] | 0.884 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty PSU Bank | -0.57118 | [-0.62921, -0.51315] | 6.458e-83 | 6.91e-81 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty PSU Bank | 0.37816 | [0.30519, 0.45113] | 3.068e-24 | 3.497e-22 | Reject H0 | 1642 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty PSE | 0.00627 | [-0.03897, 0.05152] | 0.7858 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty PSE | -0.07795 | [-0.12428, -0.03162] | 0.0009754 | 0.03219 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty PSE | 0.03007 | [-0.04181, 0.10195] | 0.4123 | 1 | Do not reject H0 | 1631 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty Realty | -0.01971 | [-0.07606, 0.03664] | 0.493 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty Realty | -0.48028 | [-0.53006, -0.43050] | 9.783e-80 | 1.037e-77 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty Realty | 0.27298 | [0.19827, 0.34769] | 7.992e-13 | 7.912e-11 | Reject H0 | 1618 |
| H1_mean_daily_return_difference | Nifty Financial Services − Nifty Services Sector | 0.01052 | [-0.00577, 0.02681] | 0.2055 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Financial Services − Nifty Services Sector | 0.12560 | [0.10900, 0.14221] | 1.019e-49 | 8.657e-48 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Financial Services − Nifty Services Sector | -0.10320 | [-0.12907, -0.07734] | 5.28e-15 | 5.439e-13 | Reject H0 | 1397 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty IT | 0.00667 | [-0.04583, 0.05916] | 0.8035 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty IT | -0.13607 | [-0.17942, -0.09272] | 7.635e-10 | 3.741e-08 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty IT | 0.09121 | [0.01710, 0.16532] | 0.01585 | 0.7293 | Do not reject H0 | 1745 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty Media | 0.05434 | [0.00342, 0.10526] | 0.03649 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty Media | -0.39154 | [-0.44197, -0.34111] | 2.723e-52 | 2.342e-50 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty Media | 0.29330 | [0.22793, 0.35866] | 1.435e-18 | 1.579e-16 | Reject H0 | 1671 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty Metal | -0.03746 | [-0.08459, 0.00968] | 0.1194 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty Metal | -0.45934 | [-0.49910, -0.41959] | 1.504e-113 | 1.669e-111 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty Metal | 0.30635 | [0.24101, 0.37170] | 3.952e-20 | 4.426e-18 | Reject H0 | 1560 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty Pharma | 0.01294 | [-0.03121, 0.05708] | 0.5657 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty Pharma | -0.04751 | [-0.08663, -0.00840] | 0.01727 | 0.3799 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty Pharma | 0.04759 | [-0.01932, 0.11450] | 0.1633 | 1 | Do not reject H0 | 1676 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty Private Bank | 0.00082 | [-0.03589, 0.03753] | 0.9652 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty Private Bank | -0.08446 | [-0.12217, -0.04675] | 1.133e-05 | 0.0004759 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty Private Bank | 0.06459 | [0.00952, 0.11966] | 0.02152 | 0.9685 | Do not reject H0 | 1591 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty PSU Bank | -0.01043 | [-0.06982, 0.04897] | 0.7308 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty PSU Bank | -0.62101 | [-0.67354, -0.56847] | 9.777e-119 | 1.115e-116 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty PSU Bank | 0.43143 | [0.36441, 0.49844] | 1.677e-36 | 1.996e-34 | Reject H0 | 1639 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty PSE | 0.00029 | [-0.02954, 0.03011] | 0.985 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty PSE | -0.12777 | [-0.15981, -0.09574] | 5.38e-15 | 2.959e-13 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty PSE | 0.10507 | [0.05799, 0.15214] | 1.219e-05 | 0.000902 | Reject H0 | 1478 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty Realty | -0.02569 | [-0.07753, 0.02614] | 0.3312 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty Realty | -0.53011 | [-0.57436, -0.48586] | 6.405e-122 | 7.366e-120 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty Realty | 0.35433 | [0.28694, 0.42172] | 6.652e-25 | 7.716e-23 | Reject H0 | 1531 |
| H1_mean_daily_return_difference | Nifty Infrastructure − Nifty Services Sector | 0.00454 | [-0.02249, 0.03156] | 0.7422 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Infrastructure − Nifty Services Sector | 0.07578 | [0.04900, 0.10255] | 2.899e-08 | 1.333e-06 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Infrastructure − Nifty Services Sector | -0.05617 | [-0.09871, -0.01362] | 0.009669 | 0.4834 | Do not reject H0 | 1525 |
| H1_mean_daily_return_difference | Nifty IT − Nifty Media | 0.04767 | [-0.02138, 0.11672] | 0.176 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty IT − Nifty Media | -0.25547 | [-0.31469, -0.19625] | 2.777e-17 | 1.666e-15 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty IT − Nifty Media | 0.17390 | [0.07958, 0.26822] | 0.0003018 | 0.02022 | Reject H0 | 1809 |
| H1_mean_daily_return_difference | Nifty IT − Nifty Metal | -0.04412 | [-0.11268, 0.02444] | 0.2072 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty IT − Nifty Metal | -0.32328 | [-0.37751, -0.26904] | 1.561e-31 | 1.155e-29 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty IT − Nifty Metal | 0.09473 | [0.00315, 0.18632] | 0.04263 | 1 | Do not reject H0 | 1795 |
| H1_mean_daily_return_difference | Nifty IT − Nifty Pharma | 0.00627 | [-0.05140, 0.06394] | 0.8313 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty IT − Nifty Pharma | 0.08855 | [0.04067, 0.13644] | 0.0002893 | 0.01041 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty IT − Nifty Pharma | -0.03182 | [-0.11014, 0.04651] | 0.4259 | 1 | Do not reject H0 | 1810 |
| H1_mean_daily_return_difference | Nifty IT − Nifty Private Bank | -0.00585 | [-0.06554, 0.05384] | 0.8477 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty IT − Nifty Private Bank | 0.05161 | [0.00029, 0.10292] | 0.0487 | 0.9253 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty IT − Nifty Private Bank | -0.03084 | [-0.11374, 0.05207] | 0.466 | 1 | Do not reject H0 | 1791 |
| H1_mean_daily_return_difference | Nifty IT − Nifty PSU Bank | -0.01709 | [-0.10327, 0.06908] | 0.6975 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty IT − Nifty PSU Bank | -0.48494 | [-0.55490, -0.41497] | 4.92e-42 | 3.985e-40 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty IT − Nifty PSU Bank | 0.19490 | [0.08739, 0.30242] | 0.0003807 | 0.02513 | Reject H0 | 1857 |
| H1_mean_daily_return_difference | Nifty IT − Nifty PSE | -0.00638 | [-0.06835, 0.05559] | 0.8401 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty IT − Nifty PSE | 0.00829 | [-0.04369, 0.06028] | 0.7545 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty IT − Nifty PSE | -0.01502 | [-0.09860, 0.06857] | 0.7247 | 1 | Do not reject H0 | 1787 |
| H1_mean_daily_return_difference | Nifty IT − Nifty Realty | -0.03236 | [-0.10863, 0.04391] | 0.4057 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty IT − Nifty Realty | -0.39404 | [-0.45127, -0.33681] | 1.664e-41 | 1.331e-39 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty IT − Nifty Realty | 0.13784 | [0.03835, 0.23733] | 0.00662 | 0.3509 | Do not reject H0 | 1791 |
| H1_mean_daily_return_difference | Nifty IT − Nifty Services Sector | -0.00213 | [-0.04440, 0.04014] | 0.9213 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty IT − Nifty Services Sector | 0.21184 | [0.17377, 0.24992] | 1.099e-27 | 7.911e-26 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty IT − Nifty Services Sector | -0.17932 | [-0.24131, -0.11734] | 1.425e-08 | 1.245e-06 | Reject H0 | 1615 |
| H1_mean_daily_return_difference | Nifty Media − Nifty Metal | -0.09179 | [-0.15467, -0.02892] | 0.004218 | 0.5061 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Media − Nifty Metal | -0.06781 | [-0.12194, -0.01368] | 0.01408 | 0.3239 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Media − Nifty Metal | -0.06659 | [-0.15105, 0.01787] | 0.1223 | 1 | Do not reject H0 | 1688 |
| H1_mean_daily_return_difference | Nifty Media − Nifty Pharma | -0.04140 | [-0.10435, 0.02154] | 0.1973 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Media − Nifty Pharma | 0.34402 | [0.28735, 0.40070] | 1.235e-32 | 9.39e-31 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Media − Nifty Pharma | -0.21508 | [-0.29787, -0.13228] | 3.553e-07 | 2.843e-05 | Reject H0 | 1771 |
| H1_mean_daily_return_difference | Nifty Media − Nifty Private Bank | -0.05352 | [-0.11065, 0.00361] | 0.06635 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Media − Nifty Private Bank | 0.30708 | [0.25005, 0.36411] | 4.899e-26 | 3.331e-24 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Media − Nifty Private Bank | -0.20054 | [-0.27658, -0.12450] | 2.357e-07 | 1.909e-05 | Reject H0 | 1734 |
| H1_mean_daily_return_difference | Nifty Media − Nifty PSU Bank | -0.06476 | [-0.13570, 0.00618] | 0.07356 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Media − Nifty PSU Bank | -0.22947 | [-0.29505, -0.16389] | 6.982e-12 | 3.631e-10 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Media − Nifty PSU Bank | 0.07804 | [-0.01016, 0.16623] | 0.08289 | 1 | Do not reject H0 | 1755 |
| H1_mean_daily_return_difference | Nifty Media − Nifty PSE | -0.05405 | [-0.10859, 0.00049] | 0.05211 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Media − Nifty PSE | 0.26376 | [0.21264, 0.31489] | 4.936e-24 | 3.209e-22 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Media − Nifty PSE | -0.22338 | [-0.29535, -0.15141] | 1.177e-09 | 1.071e-07 | Reject H0 | 1685 |
| H1_mean_daily_return_difference | Nifty Media − Nifty Realty | -0.08003 | [-0.14016, -0.01990] | 0.009089 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Media − Nifty Realty | -0.13857 | [-0.19545, -0.08169] | 1.797e-06 | 7.908e-05 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Media − Nifty Realty | -0.03067 | [-0.11111, 0.04978] | 0.455 | 1 | Do not reject H0 | 1686 |
| H1_mean_daily_return_difference | Nifty Media − Nifty Services Sector | -0.04980 | [-0.10306, 0.00345] | 0.06683 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Media − Nifty Services Sector | 0.46732 | [0.41499, 0.51964] | 1.304e-68 | 1.304e-66 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Media − Nifty Services Sector | -0.32243 | [-0.39472, -0.25013] | 2.3e-18 | 2.484e-16 | Reject H0 | 1694 |
| H1_mean_daily_return_difference | Nifty Metal − Nifty Pharma | 0.05039 | [-0.01064, 0.11142] | 0.1056 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Metal − Nifty Pharma | 0.41183 | [0.36258, 0.46108] | 2.281e-60 | 2.145e-58 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Metal − Nifty Pharma | -0.16887 | [-0.25423, -0.08350] | 0.0001056 | 0.00729 | Reject H0 | 1719 |
| H1_mean_daily_return_difference | Nifty Metal − Nifty Private Bank | 0.03827 | [-0.01915, 0.09569] | 0.1914 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Metal − Nifty Private Bank | 0.37488 | [0.32706, 0.42271] | 2.908e-53 | 2.53e-51 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Metal − Nifty Private Bank | -0.17472 | [-0.25808, -0.09135] | 3.993e-05 | 0.002795 | Reject H0 | 1651 |
| H1_mean_daily_return_difference | Nifty Metal − Nifty PSU Bank | 0.02703 | [-0.04194, 0.09601] | 0.4424 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Metal − Nifty PSU Bank | -0.16166 | [-0.21817, -0.10515] | 2.056e-08 | 9.661e-07 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Metal − Nifty PSU Bank | 0.15604 | [0.06831, 0.24376] | 0.0004898 | 0.03184 | Reject H0 | 1680 |
| H1_mean_daily_return_difference | Nifty Metal − Nifty PSE | 0.03774 | [-0.00612, 0.08161] | 0.09171 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Metal − Nifty PSE | 0.33157 | [0.29040, 0.37274] | 3.923e-56 | 3.492e-54 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Metal − Nifty PSE | -0.21606 | [-0.28085, -0.15127] | 6.334e-11 | 6.018e-09 | Reject H0 | 1550 |
| H1_mean_daily_return_difference | Nifty Metal − Nifty Realty | 0.01176 | [-0.05341, 0.07693] | 0.7236 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Metal − Nifty Realty | -0.07076 | [-0.12217, -0.01935] | 0.006978 | 0.1675 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Metal − Nifty Realty | 0.03989 | [-0.05015, 0.12993] | 0.3853 | 1 | Do not reject H0 | 1616 |
| H1_mean_daily_return_difference | Nifty Metal − Nifty Services Sector | 0.04199 | [-0.01068, 0.09467] | 0.1182 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Metal − Nifty Services Sector | 0.53512 | [0.49242, 0.57782] | 3.33e-133 | 3.929e-131 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Metal − Nifty Services Sector | -0.31659 | [-0.39100, -0.24219] | 7.456e-17 | 7.978e-15 | Reject H0 | 1614 |
| H1_mean_daily_return_difference | Nifty Pharma − Nifty Private Bank | -0.01212 | [-0.07050, 0.04626] | 0.6841 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Pharma − Nifty Private Bank | -0.03695 | [-0.08830, 0.01440] | 0.1585 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Pharma − Nifty Private Bank | -0.00136 | [-0.08705, 0.08432] | 0.9751 | 1 | Do not reject H0 | 1752 |
| H1_mean_daily_return_difference | Nifty Pharma − Nifty PSU Bank | -0.02336 | [-0.10137, 0.05465] | 0.5572 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Pharma − Nifty PSU Bank | -0.57349 | [-0.63500, -0.51198] | 1.356e-74 | 1.424e-72 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Pharma − Nifty PSU Bank | 0.23953 | [0.13992, 0.33915] | 2.442e-06 | 0.0001856 | Reject H0 | 1801 |
| H1_mean_daily_return_difference | Nifty Pharma − Nifty PSE | -0.01265 | [-0.06411, 0.03882] | 0.63 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Pharma − Nifty PSE | -0.08026 | [-0.12804, -0.03248] | 0.0009945 | 0.03219 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Pharma − Nifty PSE | 0.01115 | [-0.06083, 0.08313] | 0.7614 | 1 | Do not reject H0 | 1703 |
| H1_mean_daily_return_difference | Nifty Pharma − Nifty Realty | -0.03863 | [-0.10741, 0.03015] | 0.271 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Pharma − Nifty Realty | -0.48259 | [-0.53641, -0.42878] | 3.728e-69 | 3.765e-67 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Pharma − Nifty Realty | 0.20328 | [0.11134, 0.29522] | 1.467e-05 | 0.001056 | Reject H0 | 1717 |
| H1_mean_daily_return_difference | Nifty Pharma − Nifty Services Sector | -0.00840 | [-0.05659, 0.03979] | 0.7326 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Pharma − Nifty Services Sector | 0.12329 | [0.08059, 0.16600] | 1.527e-08 | 7.327e-07 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Pharma − Nifty Services Sector | -0.08426 | [-0.15714, -0.01137] | 0.02348 | 1 | Do not reject H0 | 1721 |
| H1_mean_daily_return_difference | Nifty Private Bank − Nifty PSU Bank | -0.01124 | [-0.07128, 0.04879] | 0.7136 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Private Bank − Nifty PSU Bank | -0.53654 | [-0.59513, -0.47796] | 4.738e-72 | 4.928e-70 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Private Bank − Nifty PSU Bank | 0.34247 | [0.26571, 0.41923] | 2.246e-18 | 2.449e-16 | Reject H0 | 1639 |
| H1_mean_daily_return_difference | Nifty Private Bank − Nifty PSE | -0.00053 | [-0.04800, 0.04694] | 0.9825 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Private Bank − Nifty PSE | -0.04331 | [-0.09233, 0.00570] | 0.08329 | 1 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty Private Bank − Nifty PSE | -0.00376 | [-0.07674, 0.06922] | 0.9196 | 1 | Do not reject H0 | 1633 |
| H1_mean_daily_return_difference | Nifty Private Bank − Nifty Realty | -0.02651 | [-0.08449, 0.03146] | 0.3701 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Private Bank − Nifty Realty | -0.44565 | [-0.49719, -0.39410] | 2.091e-64 | 2.007e-62 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Private Bank − Nifty Realty | 0.23736 | [0.16192, 0.31280] | 6.969e-10 | 6.412e-08 | Reject H0 | 1616 |
| H1_mean_daily_return_difference | Nifty Private Bank − Nifty Services Sector | 0.00372 | [-0.01843, 0.02587] | 0.7421 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Private Bank − Nifty Services Sector | 0.16024 | [0.13834, 0.18213] | 1.186e-46 | 9.962e-45 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Private Bank − Nifty Services Sector | -0.14038 | [-0.17368, -0.10708] | 1.429e-16 | 1.501e-14 | Reject H0 | 1456 |
| H1_mean_daily_return_difference | Nifty PSU Bank − Nifty PSE | 0.01071 | [-0.04978, 0.07120] | 0.7285 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty PSU Bank − Nifty PSE | 0.49323 | [0.43765, 0.54881] | 9.184e-68 | 9e-66 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty PSU Bank − Nifty PSE | -0.33432 | [-0.40681, -0.26183] | 1.583e-19 | 1.757e-17 | Reject H0 | 1645 |
| H1_mean_daily_return_difference | Nifty PSU Bank − Nifty Realty | -0.01527 | [-0.08822, 0.05769] | 0.6816 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty PSU Bank − Nifty Realty | 0.09090 | [0.02653, 0.15527] | 0.005643 | 0.1524 | Do not reject H0 | 2649 |
| H3_downside_return_difference | Nifty PSU Bank − Nifty Realty | -0.10343 | [-0.19871, -0.00814] | 0.03338 | 1 | Do not reject H0 | 1670 |
| H1_mean_daily_return_difference | Nifty PSU Bank − Nifty Services Sector | 0.01496 | [-0.04716, 0.07708] | 0.6369 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty PSU Bank − Nifty Services Sector | 0.69678 | [0.63996, 0.75360] | 1.214e-127 | 1.409e-125 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty PSU Bank − Nifty Services Sector | -0.44202 | [-0.51734, -0.36670] | 1.289e-30 | 1.52e-28 | Reject H0 | 1651 |
| H1_mean_daily_return_difference | Nifty PSE − Nifty Realty | -0.02598 | [-0.08350, 0.03154] | 0.376 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty PSE − Nifty Realty | -0.40233 | [-0.45225, -0.35242] | 3.233e-56 | 2.942e-54 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty PSE − Nifty Realty | 0.22255 | [0.14066, 0.30443] | 1e-07 | 8.401e-06 | Reject H0 | 1581 |
| H1_mean_daily_return_difference | Nifty PSE − Nifty Services Sector | 0.00425 | [-0.03695, 0.04545] | 0.8398 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty PSE − Nifty Services Sector | 0.20355 | [0.16264, 0.24446] | 1.794e-22 | 1.112e-20 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty PSE − Nifty Services Sector | -0.12428 | [-0.18912, -0.05943] | 0.0001723 | 0.01172 | Reject H0 | 1593 |
| H1_mean_daily_return_difference | Nifty Realty − Nifty Services Sector | 0.03023 | [-0.02604, 0.08650] | 0.2923 | 1 | Do not reject H0 | 2649 |
| H2_absolute_return_difference | Nifty Realty − Nifty Services Sector | 0.60588 | [0.55865, 0.65312] | 1.834e-139 | 2.182e-137 | Reject H0 | 2649 |
| H3_downside_return_difference | Nifty Realty − Nifty Services Sector | -0.35870 | [-0.43245, -0.28495] | 1.532e-21 | 1.731e-19 | Reject H0 | 1598 |

## Correlation summary

| Pair | Pearson r | Spearman rho | n |
|---|---:|---:|---:|
| Nifty Auto — Nifty Bank | 0.6852 | 0.5919 | 2649 |
| Nifty Auto — Nifty Commodities | 0.7320 | 0.6670 | 2649 |
| Nifty Auto — Nifty Energy | 0.6150 | 0.5611 | 2649 |
| Nifty Auto — Nifty FMCG | 0.5455 | 0.4819 | 2649 |
| Nifty Auto — Nifty Financial Services | 0.6939 | 0.6003 | 2649 |
| Nifty Auto — Nifty Infrastructure | 0.7474 | 0.6885 | 2649 |
| Nifty Auto — Nifty IT | 0.3876 | 0.3251 | 2649 |
| Nifty Auto — Nifty Media | 0.5570 | 0.5173 | 2649 |
| Nifty Auto — Nifty Metal | 0.6297 | 0.5772 | 2649 |
| Nifty Auto — Nifty Pharma | 0.4653 | 0.4481 | 2649 |
| Nifty Auto — Nifty Private Bank | 0.6844 | 0.5873 | 2649 |
| Nifty Auto — Nifty PSU Bank | 0.5372 | 0.5204 | 2649 |
| Nifty Auto — Nifty PSE | 0.6138 | 0.5753 | 2649 |
| Nifty Auto — Nifty Realty | 0.6404 | 0.5785 | 2649 |
| Nifty Auto — Nifty Services Sector | 0.7182 | 0.6351 | 2649 |
| Nifty Bank — Nifty Commodities | 0.6973 | 0.6298 | 2649 |
| Nifty Bank — Nifty Energy | 0.5978 | 0.5338 | 2649 |
| Nifty Bank — Nifty FMCG | 0.5101 | 0.4434 | 2649 |
| Nifty Bank — Nifty Financial Services | 0.9672 | 0.9444 | 2649 |
| Nifty Bank — Nifty Infrastructure | 0.7356 | 0.6562 | 2649 |
| Nifty Bank — Nifty IT | 0.3637 | 0.2941 | 2649 |
| Nifty Bank — Nifty Media | 0.4955 | 0.4459 | 2649 |
| Nifty Bank — Nifty Metal | 0.5943 | 0.5381 | 2649 |
| Nifty Bank — Nifty Pharma | 0.3806 | 0.3542 | 2649 |
| Nifty Bank — Nifty Private Bank | 0.9859 | 0.9761 | 2649 |
| Nifty Bank — Nifty PSU Bank | 0.7073 | 0.7143 | 2649 |
| Nifty Bank — Nifty PSE | 0.5866 | 0.5404 | 2649 |
| Nifty Bank — Nifty Realty | 0.6231 | 0.5751 | 2649 |
| Nifty Bank — Nifty Services Sector | 0.9224 | 0.8781 | 2649 |
| Nifty Commodities — Nifty Energy | 0.8666 | 0.8225 | 2649 |
| Nifty Commodities — Nifty FMCG | 0.5381 | 0.4689 | 2649 |
| Nifty Commodities — Nifty Financial Services | 0.7003 | 0.6300 | 2649 |
| Nifty Commodities — Nifty Infrastructure | 0.8791 | 0.8416 | 2649 |
| Nifty Commodities — Nifty IT | 0.4167 | 0.3432 | 2649 |
| Nifty Commodities — Nifty Media | 0.5965 | 0.5501 | 2649 |
| Nifty Commodities — Nifty Metal | 0.8896 | 0.8704 | 2649 |
| Nifty Commodities — Nifty Pharma | 0.5305 | 0.4868 | 2649 |
| Nifty Commodities — Nifty Private Bank | 0.6808 | 0.6134 | 2649 |
| Nifty Commodities — Nifty PSU Bank | 0.6321 | 0.6054 | 2649 |
| Nifty Commodities — Nifty PSE | 0.8756 | 0.8421 | 2649 |
| Nifty Commodities — Nifty Realty | 0.6805 | 0.6377 | 2649 |
| Nifty Commodities — Nifty Services Sector | 0.7467 | 0.6777 | 2649 |
| Nifty Energy — Nifty FMCG | 0.4590 | 0.3981 | 2649 |
| Nifty Energy — Nifty Financial Services | 0.6002 | 0.5284 | 2649 |
| Nifty Energy — Nifty Infrastructure | 0.8117 | 0.7678 | 2649 |
| Nifty Energy — Nifty IT | 0.3450 | 0.2716 | 2649 |
| Nifty Energy — Nifty Media | 0.5139 | 0.4643 | 2649 |
| Nifty Energy — Nifty Metal | 0.6673 | 0.6061 | 2649 |
| Nifty Energy — Nifty Pharma | 0.4448 | 0.4001 | 2649 |
| Nifty Energy — Nifty Private Bank | 0.5798 | 0.5184 | 2649 |
| Nifty Energy — Nifty PSU Bank | 0.5610 | 0.5222 | 2649 |
| Nifty Energy — Nifty PSE | 0.8558 | 0.8139 | 2649 |
| Nifty Energy — Nifty Realty | 0.5720 | 0.5273 | 2649 |
| Nifty Energy — Nifty Services Sector | 0.6486 | 0.5772 | 2649 |
| Nifty FMCG — Nifty Financial Services | 0.5298 | 0.4717 | 2649 |
| Nifty FMCG — Nifty Infrastructure | 0.5710 | 0.5131 | 2649 |
| Nifty FMCG — Nifty IT | 0.3716 | 0.3075 | 2649 |
| Nifty FMCG — Nifty Media | 0.3906 | 0.3565 | 2649 |
| Nifty FMCG — Nifty Metal | 0.4132 | 0.3627 | 2649 |
| Nifty FMCG — Nifty Pharma | 0.4253 | 0.4024 | 2649 |
| Nifty FMCG — Nifty Private Bank | 0.5120 | 0.4395 | 2649 |
| Nifty FMCG — Nifty PSU Bank | 0.3579 | 0.3500 | 2649 |
| Nifty FMCG — Nifty PSE | 0.4338 | 0.3982 | 2649 |
| Nifty FMCG — Nifty Realty | 0.4538 | 0.4134 | 2649 |
| Nifty FMCG — Nifty Services Sector | 0.5726 | 0.5095 | 2649 |
| Nifty Financial Services — Nifty Infrastructure | 0.7431 | 0.6581 | 2649 |
| Nifty Financial Services — Nifty IT | 0.3838 | 0.3195 | 2649 |
| Nifty Financial Services — Nifty Media | 0.4854 | 0.4368 | 2649 |
| Nifty Financial Services — Nifty Metal | 0.5906 | 0.5384 | 2649 |
| Nifty Financial Services — Nifty Pharma | 0.3896 | 0.3679 | 2649 |
| Nifty Financial Services — Nifty Private Bank | 0.9543 | 0.9241 | 2649 |
| Nifty Financial Services — Nifty PSU Bank | 0.6403 | 0.6260 | 2649 |
| Nifty Financial Services — Nifty PSE | 0.5817 | 0.5290 | 2649 |
| Nifty Financial Services — Nifty Realty | 0.6306 | 0.5748 | 2649 |
| Nifty Financial Services — Nifty Services Sector | 0.9474 | 0.9145 | 2649 |
| Nifty Infrastructure — Nifty IT | 0.4322 | 0.3609 | 2649 |
| Nifty Infrastructure — Nifty Media | 0.5791 | 0.5369 | 2649 |
| Nifty Infrastructure — Nifty Metal | 0.7258 | 0.6745 | 2649 |
| Nifty Infrastructure — Nifty Pharma | 0.5161 | 0.4802 | 2649 |
| Nifty Infrastructure — Nifty Private Bank | 0.7188 | 0.6401 | 2649 |
| Nifty Infrastructure — Nifty PSU Bank | 0.6457 | 0.6070 | 2649 |
| Nifty Infrastructure — Nifty PSE | 0.8007 | 0.7589 | 2649 |
| Nifty Infrastructure — Nifty Realty | 0.7057 | 0.6618 | 2649 |
| Nifty Infrastructure — Nifty Services Sector | 0.7957 | 0.7241 | 2649 |
| Nifty IT — Nifty Media | 0.3174 | 0.2711 | 2649 |
| Nifty IT — Nifty Metal | 0.3588 | 0.2855 | 2649 |
| Nifty IT — Nifty Pharma | 0.3402 | 0.2925 | 2649 |
| Nifty IT — Nifty Private Bank | 0.3663 | 0.2917 | 2649 |
| Nifty IT — Nifty PSU Bank | 0.2327 | 0.2077 | 2649 |
| Nifty IT — Nifty PSE | 0.3219 | 0.2657 | 2649 |
| Nifty IT — Nifty Realty | 0.3404 | 0.2946 | 2649 |
| Nifty IT — Nifty Services Sector | 0.6237 | 0.5914 | 2649 |
| Nifty Media — Nifty Metal | 0.5247 | 0.4857 | 2649 |
| Nifty Media — Nifty Pharma | 0.3958 | 0.3935 | 2649 |
| Nifty Media — Nifty Private Bank | 0.4910 | 0.4412 | 2649 |
| Nifty Media — Nifty PSU Bank | 0.4895 | 0.4716 | 2649 |
| Nifty Media — Nifty PSE | 0.5452 | 0.4979 | 2649 |
| Nifty Media — Nifty Realty | 0.5548 | 0.5018 | 2649 |
| Nifty Media — Nifty Services Sector | 0.5256 | 0.4799 | 2649 |
| Nifty Metal — Nifty Pharma | 0.4705 | 0.4330 | 2649 |
| Nifty Metal — Nifty Private Bank | 0.5789 | 0.5252 | 2649 |
| Nifty Metal — Nifty PSU Bank | 0.5609 | 0.5301 | 2649 |
| Nifty Metal — Nifty PSE | 0.7341 | 0.6902 | 2649 |
| Nifty Metal — Nifty Realty | 0.5972 | 0.5589 | 2649 |
| Nifty Metal — Nifty Services Sector | 0.6328 | 0.5726 | 2649 |
| Nifty Pharma — Nifty Private Bank | 0.3762 | 0.3503 | 2649 |
| Nifty Pharma — Nifty PSU Bank | 0.3481 | 0.3504 | 2649 |
| Nifty Pharma — Nifty PSE | 0.4521 | 0.4279 | 2649 |
| Nifty Pharma — Nifty Realty | 0.4346 | 0.4195 | 2649 |
| Nifty Pharma — Nifty Services Sector | 0.4514 | 0.4195 | 2649 |
| Nifty Private Bank — Nifty PSU Bank | 0.6330 | 0.6344 | 2649 |
| Nifty Private Bank — Nifty PSE | 0.5654 | 0.5228 | 2649 |
| Nifty Private Bank — Nifty Realty | 0.6151 | 0.5651 | 2649 |
| Nifty Private Bank — Nifty Services Sector | 0.9138 | 0.8632 | 2649 |
| Nifty PSU Bank — Nifty PSE | 0.6162 | 0.5861 | 2649 |
| Nifty PSU Bank — Nifty Realty | 0.5517 | 0.5381 | 2649 |
| Nifty PSU Bank — Nifty Services Sector | 0.6198 | 0.6000 | 2649 |
| Nifty PSE — Nifty Realty | 0.6056 | 0.5732 | 2649 |
| Nifty PSE — Nifty Services Sector | 0.6213 | 0.5686 | 2649 |
| Nifty Realty — Nifty Services Sector | 0.6471 | 0.5919 | 2649 |

## Important limitations

1. **Calendar completeness:** matching dates across indices does not certify that every official NSE trading session is present.
2. **Index overlap:** Sector index series may share constituents and common market shocks; paired-difference tests should not be interpreted as independent portfolio samples.
3. **Price-return vs total-return:** source index type should be confirmed. Dividend treatment can materially change long-horizon comparisons.
4. **Index reconstitution:** constituents and methodology may change over the sample, so these are historical index-level returns rather than a fixed-company panel.
5. **Multiple comparisons:** Holm adjustment is within each stated family; broader exploratory analysis can still inflate false-positive risk.
6. **Time-series assumptions:** HAC inference is robust to some autocorrelation/heteroskedasticity but not every structural break or model misspecification.
7. **No macroeconomic testing here:** the current multi-index archive contains index OHLC CSVs only. Tests of USD/INR, CPI, RBI rates, reserves or S&P 500 require a separately audited, correctly aligned macro dataset.
8. **No causal or investment claim:** association and historical differences do not establish causal mechanisms or future profitability.

## Reproducibility

Run `make all` for data cleaning and date audit, `make eda` for EDA and tests, `make test` for automated checks, or `make full` for the entire workflow. Outputs are written to `reports/eda/`, `reports/hypothesis_tests/` and `reports/figures/`.
