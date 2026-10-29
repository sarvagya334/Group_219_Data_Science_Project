# Unified Sector-Index Macroeconomic Hypothesis Testing Report

**Indices:** Nifty Auto, Nifty Bank, Nifty Commodities, Nifty Energy, Nifty FMCG, Nifty Financial Services, Nifty Infrastructure, Nifty IT, Nifty Media, Nifty Metal, Nifty Pharma, Nifty Private Bank, Nifty PSU Bank, Nifty PSE, Nifty Realty, Nifty Services Sector.
**Index sample:** 2016-01-05 to 2026-09-30.
**Macro hypothesis families generated:** H1, H2, H3, H4, H5, H6, H7.

## Executive summary

This is one integrated multi-index study. The same source macroeconomic variables are aligned to all selected sector-index return series; each hypothesis reports per-sector-index fits and direct pairwise tests of whether macro sensitivity differs. The pairwise slope tests regress the paired index return difference (A minus B) on the same macro predictor(s), which tests the coefficient difference directly rather than comparing separate p-values.

**These are observational associations, not identified causal effects.** No investor information set can be certified where the workbook provides reference dates but not actual publication timestamps. H5 GVA has a short effective sample and is exploratory.

## Data overview

- Common index closes: 2650.
- Daily index return rows: 2649.
- USD/INR observations: 6812.
- CPI observations: 156; derived YoY inflation observations: 144.
- Weekly reserve observations: 1336.
- RBI repo effective-date rows: 58.
- Quarterly GVA observations: 17 (short history; 2022-23 constant-price base series only).
- Monthly IIP observations: 104.
- S&P 500 observations: 2513.

### CPI inflation derivation

The primary inflation predictor is newly calculated from the Combined CPI General Index rather than copied from the reported inflation cell:

`inflation_yoy_derived_pct = 100 × (CPI_index[t] / CPI_index[t−12] − 1)`

The supplied reported YoY series and the derived series have 144 overlapping non-missing months; their correlation is 0.9999986217439643 and mean absolute difference is 0.0024572867348339775 percentage points. See `data/clean/macro/cpi_inflation_derived_clean.csv` for both columns.

## Hypotheses and methods

### H1 — USD/INR and daily index returns

Outcome: daily close-to-close return in percent. Predictor: same-date percentage change in USD/INR. Per-index OLS with Newey–West/HAC standard errors. Pairwise tests regress the difference in two index returns on USD/INR change to test whether the FX slope differs. Same-date FX observation timing is unverified.

### H2 — CPI-derived inflation and monthly index returns

Outcome: month-end-to-month-end index return in percent. Predictor: inflation derived from the CPI index. The report includes the same-reference-month association and a one-reference-month lag sensitivity. CPI publication timestamps and consensus expectations are absent, so neither should be treated as a clean surprise/event study; same-month association is not predictive.

### H3 — Weekly foreign-exchange reserves and weekly index returns

Outcome: Friday-ending weekly index return. Predictors: weekly reserve percentage change plus weekly USD/INR percentage change. A future-reserves lead diagnostic is also reported per index. A significant lead is a warning for timing/common-shock problems, not a causal result. The reserve workbook's public release timestamp is absent.

### H4 — RBI repo-rate effective-date event study

Map each supplied effective date to the first supplied index session on or after it. Expected daily return is estimated over sessions [t−120, t−21], requiring at least 80 observations. The CAR is sum of returns over [t−1, t, t+1] minus three times the estimated mean. The primary test is a two-sided one-sample t-test of mean CAR = 0; all paired event-CAR differences among the selected sector indices are tested and Holm-corrected. This is an exploratory proxy because public announcement timestamps and a complete official MPC decision archive have not been verified.

### H5 — Real GVA growth and quarterly index returns

GVA measure: GVA at Basic Prices, constant prices, 2022-23 base-year workbook. YoY growth is calculated from the same base-year series and the primary predictor is lagged one quarter. Same-quarter results are secondary only. The effective sample is small, so p-values are low-power exploratory evidence. No older base-year GVA series is spliced into the sample.

### H6 — IIP growth and monthly index returns

IIP YoY growth is derived from the supplied Monthly sheet in the 50 Macroeconomic Indicators workbook. The primary association uses a one-reference-month lag; same-month results are secondary. Exact release dates and vintage/revision history are not supplied.

### H7 — Prior US-session S&P 500 returns and Indian index returns

For each Indian date, the predictor is the most recent S&P 500 daily return strictly before that date (`merge_asof` backward, exact matches disabled). Per-index regressions control for that index's own previous daily return. Pairwise slope-difference tests control for the difference in the two indices' own-lag returns. This is association/predictive sensitivity, not causality or a profitability test.

## Results by hypothesis

### H1 — USD/INR changes and daily index returns

**Null:** USD/INR percentage change has zero linear association with same-date index daily return; for pairwise tests, its slope is equal across indices.

| Index | n | Focus coefficient | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |
|---|---:|---:|---|---:|---:|---|
| Nifty Auto | 2590 | -1.17972 | [-1.46073, -0.898704] | 1.901e-16 | 9.506e-16 | Reject H0 |
| Nifty Bank | 2590 | -1.37389 | [-1.66591, -1.08188] | 2.934e-20 | 2.934e-19 | Reject H0 |
| Nifty Commodities | 2590 | -1.21406 | [-1.45307, -0.975053] | 2.378e-23 | 3.329e-22 | Reject H0 |
| Nifty Energy | 2590 | -1.03049 | [-1.25232, -0.808666] | 8.624e-20 | 7.38e-19 | Reject H0 |
| Nifty FMCG | 2590 | -0.688309 | [-0.878301, -0.498317] | 1.242e-12 | 3.726e-12 | Reject H0 |
| Nifty Financial Services | 2590 | -1.40146 | [-1.67268, -1.13023] | 4.17e-24 | 6.255e-23 | Reject H0 |
| Nifty Infrastructure | 2590 | -1.13238 | [-1.36034, -0.904426] | 2.114e-22 | 2.748e-21 | Reject H0 |
| Nifty IT | 2590 | -0.534249 | [-0.784219, -0.284279] | 2.803e-05 | 2.803e-05 | Reject H0 |
| Nifty Media | 2590 | -0.957794 | [-1.20298, -0.71261] | 1.911e-14 | 7.644e-14 | Reject H0 |
| Nifty Metal | 2590 | -1.44362 | [-1.74492, -1.14231] | 5.969e-21 | 6.565e-20 | Reject H0 |
| Nifty Pharma | 2590 | -0.432954 | [-0.623935, -0.241973] | 8.862e-06 | 1.772e-05 | Reject H0 |
| Nifty Private Bank | 2590 | -1.3733 | [-1.6911, -1.0555] | 2.464e-17 | 1.479e-16 | Reject H0 |
| Nifty PSU Bank | 2590 | -1.55541 | [-1.87561, -1.23521] | 1.719e-21 | 2.063e-20 | Reject H0 |
| Nifty PSE | 2590 | -1.06001 | [-1.30109, -0.81893] | 6.824e-18 | 4.777e-17 | Reject H0 |
| Nifty Realty | 2590 | -1.6107 | [-1.90955, -1.31186] | 4.382e-26 | 7.011e-25 | Reject H0 |
| Nifty Services Sector | 2590 | -1.11715 | [-1.35749, -0.876817] | 8.2e-20 | 7.38e-19 | Reject H0 |

**Pairwise Slope Tests**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | 0.194176 | 0.02621 | 0.9436 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty Commodities | 0.0343443 | 0.6404 | 1 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty Energy | -0.149224 | 0.1151 | 1 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty FMCG | -0.491406 | 3.431e-08 | 2.985e-06 | Reject H0 | 2590 |
| Nifty Auto − Nifty Financial Services | 0.221741 | 0.004361 | 0.205 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty Infrastructure | -0.0473309 | 0.5147 | 1 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty IT | -0.645466 | 3.698e-07 | 3.07e-05 | Reject H0 | 2590 |
| Nifty Auto − Nifty Media | -0.221921 | 0.03531 | 1 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty Metal | 0.263903 | 0.0106 | 0.4345 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty Pharma | -0.746761 | 8.074e-10 | 7.832e-08 | Reject H0 | 2590 |
| Nifty Auto − Nifty Private Bank | 0.193581 | 0.03949 | 1 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty PSU Bank | 0.375697 | 0.00546 | 0.2512 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty PSE | -0.119705 | 0.2178 | 1 | Do not reject H0 | 2590 |
| Nifty Auto − Nifty Realty | 0.43099 | 2.297e-06 | 0.0001837 | Reject H0 | 2590 |
| Nifty Auto − Nifty Services Sector | -0.0625621 | 0.4181 | 1 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty Commodities | -0.159831 | 0.07204 | 1 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty Energy | -0.343399 | 0.001354 | 0.0731 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty FMCG | -0.685582 | 3.456e-12 | 3.733e-10 | Reject H0 | 2590 |
| Nifty Bank − Nifty Financial Services | 0.0275651 | 0.3795 | 1 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty Infrastructure | -0.241507 | 0.002765 | 0.1438 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty IT | -0.839642 | 8.4e-12 | 8.904e-10 | Reject H0 | 2590 |
| Nifty Bank − Nifty Media | -0.416097 | 0.0001334 | 0.009071 | Reject H0 | 2590 |
| Nifty Bank − Nifty Metal | 0.0697272 | 0.55 | 1 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty Pharma | -0.940937 | 1.651e-12 | 1.799e-10 | Reject H0 | 2590 |
| Nifty Bank − Nifty Private Bank | -0.000594509 | 0.9783 | 1 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty PSU Bank | 0.181521 | 0.1106 | 1 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty PSE | -0.313881 | 0.003475 | 0.1737 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty Realty | 0.236814 | 0.01216 | 0.4863 | Do not reject H0 | 2590 |
| Nifty Bank − Nifty Services Sector | -0.256738 | 1.888e-08 | 1.681e-06 | Reject H0 | 2590 |
| Nifty Commodities − Nifty Energy | -0.183568 | 0.0003722 | 0.0227 | Reject H0 | 2590 |
| Nifty Commodities − Nifty FMCG | -0.52575 | 2.679e-10 | 2.706e-08 | Reject H0 | 2590 |
| Nifty Commodities − Nifty Financial Services | 0.187396 | 0.02011 | 0.746 | Do not reject H0 | 2590 |
| Nifty Commodities − Nifty Infrastructure | -0.0816752 | 0.0701 | 1 | Do not reject H0 | 2590 |
| Nifty Commodities − Nifty IT | -0.67981 | 2.561e-09 | 2.356e-07 | Reject H0 | 2590 |
| Nifty Commodities − Nifty Media | -0.256266 | 0.003401 | 0.1735 | Do not reject H0 | 2590 |
| Nifty Commodities − Nifty Metal | 0.229559 | 0.0004393 | 0.02636 | Reject H0 | 2590 |
| Nifty Commodities − Nifty Pharma | -0.781105 | 7.702e-15 | 8.781e-13 | Reject H0 | 2590 |
| Nifty Commodities − Nifty Private Bank | 0.159237 | 0.1113 | 1 | Do not reject H0 | 2590 |
| Nifty Commodities − Nifty PSU Bank | 0.341352 | 0.003663 | 0.1795 | Do not reject H0 | 2590 |
| Nifty Commodities − Nifty PSE | -0.154049 | 0.001157 | 0.06365 | Do not reject H0 | 2590 |
| Nifty Commodities − Nifty Realty | 0.396645 | 2.147e-05 | 0.00161 | Reject H0 | 2590 |
| Nifty Commodities − Nifty Services Sector | -0.0969064 | 0.1755 | 1 | Do not reject H0 | 2590 |
| Nifty Energy − Nifty FMCG | -0.342182 | 0.0001567 | 0.0105 | Reject H0 | 2590 |
| Nifty Energy − Nifty Financial Services | 0.370964 | 0.0001964 | 0.01277 | Reject H0 | 2590 |
| Nifty Energy − Nifty Infrastructure | 0.101893 | 0.08236 | 1 | Do not reject H0 | 2590 |
| Nifty Energy − Nifty IT | -0.496242 | 5.392e-05 | 0.003721 | Reject H0 | 2590 |
| Nifty Energy − Nifty Media | -0.0726976 | 0.4441 | 1 | Do not reject H0 | 2590 |
| Nifty Energy − Nifty Metal | 0.413127 | 3.226e-05 | 0.002322 | Reject H0 | 2590 |
| Nifty Energy − Nifty Pharma | -0.597537 | 6.254e-10 | 6.129e-08 | Reject H0 | 2590 |
| Nifty Energy − Nifty Private Bank | 0.342805 | 0.004195 | 0.2013 | Do not reject H0 | 2590 |
| Nifty Energy − Nifty PSU Bank | 0.52492 | 2.009e-05 | 0.001527 | Reject H0 | 2590 |
| Nifty Energy − Nifty PSE | 0.0295188 | 0.5838 | 1 | Do not reject H0 | 2590 |
| Nifty Energy − Nifty Realty | 0.580213 | 4.618e-08 | 3.971e-06 | Reject H0 | 2590 |
| Nifty Energy − Nifty Services Sector | 0.0866617 | 0.3315 | 1 | Do not reject H0 | 2590 |
| Nifty FMCG − Nifty Financial Services | 0.713147 | 1.248e-15 | 1.447e-13 | Reject H0 | 2590 |
| Nifty FMCG − Nifty Infrastructure | 0.444075 | 1.357e-09 | 1.275e-07 | Reject H0 | 2590 |
| Nifty FMCG − Nifty IT | -0.15406 | 0.1747 | 1 | Do not reject H0 | 2590 |
| Nifty FMCG − Nifty Media | 0.269485 | 0.007959 | 0.3502 | Do not reject H0 | 2590 |
| Nifty FMCG − Nifty Metal | 0.755309 | 1.2e-09 | 1.14e-07 | Reject H0 | 2590 |
| Nifty FMCG − Nifty Pharma | -0.255355 | 0.006856 | 0.3085 | Do not reject H0 | 2590 |
| Nifty FMCG − Nifty Private Bank | 0.684987 | 2.653e-10 | 2.706e-08 | Reject H0 | 2590 |
| Nifty FMCG − Nifty PSU Bank | 0.867103 | 4.356e-10 | 4.356e-08 | Reject H0 | 2590 |
| Nifty FMCG − Nifty PSE | 0.371701 | 0.0002779 | 0.01751 | Reject H0 | 2590 |
| Nifty FMCG − Nifty Realty | 0.922396 | 6.375e-18 | 7.522e-16 | Reject H0 | 2590 |
| Nifty FMCG − Nifty Services Sector | 0.428844 | 4.95e-08 | 4.208e-06 | Reject H0 | 2590 |
| Nifty Financial Services − Nifty Infrastructure | -0.269072 | 0.0002124 | 0.01359 | Reject H0 | 2590 |
| Nifty Financial Services − Nifty IT | -0.867207 | 8.126e-14 | 9.02e-12 | Reject H0 | 2590 |
| Nifty Financial Services − Nifty Media | -0.443662 | 2.512e-05 | 0.001859 | Reject H0 | 2590 |
| Nifty Financial Services − Nifty Metal | 0.0421622 | 0.7039 | 1 | Do not reject H0 | 2590 |
| Nifty Financial Services − Nifty Pharma | -0.968502 | 5.969e-15 | 6.864e-13 | Reject H0 | 2590 |
| Nifty Financial Services − Nifty Private Bank | -0.0281596 | 0.5138 | 1 | Do not reject H0 | 2590 |
| Nifty Financial Services − Nifty PSU Bank | 0.153956 | 0.1943 | 1 | Do not reject H0 | 2590 |
| Nifty Financial Services − Nifty PSE | -0.341446 | 0.0006655 | 0.0386 | Reject H0 | 2590 |
| Nifty Financial Services − Nifty Realty | 0.209249 | 0.01963 | 0.746 | Do not reject H0 | 2590 |
| Nifty Financial Services − Nifty Services Sector | -0.284303 | 3.539e-18 | 4.212e-16 | Reject H0 | 2590 |
| Nifty Infrastructure − Nifty IT | -0.598135 | 1.162e-07 | 9.761e-06 | Reject H0 | 2590 |
| Nifty Infrastructure − Nifty Media | -0.17459 | 0.04654 | 1 | Do not reject H0 | 2590 |
| Nifty Infrastructure − Nifty Metal | 0.311234 | 0.000923 | 0.05261 | Do not reject H0 | 2590 |
| Nifty Infrastructure − Nifty Pharma | -0.69943 | 7.716e-13 | 8.488e-11 | Reject H0 | 2590 |
| Nifty Infrastructure − Nifty Private Bank | 0.240912 | 0.008976 | 0.377 | Do not reject H0 | 2590 |
| Nifty Infrastructure − Nifty PSU Bank | 0.423027 | 0.0001645 | 0.01086 | Reject H0 | 2590 |
| Nifty Infrastructure − Nifty PSE | -0.0723741 | 0.2259 | 1 | Do not reject H0 | 2590 |
| Nifty Infrastructure − Nifty Realty | 0.478321 | 1.723e-08 | 1.551e-06 | Reject H0 | 2590 |
| Nifty Infrastructure − Nifty Services Sector | -0.0152312 | 0.8114 | 1 | Do not reject H0 | 2590 |
| Nifty IT − Nifty Media | 0.423545 | 0.0009388 | 0.05261 | Do not reject H0 | 2590 |
| Nifty IT − Nifty Metal | 0.909369 | 3.615e-12 | 3.868e-10 | Reject H0 | 2590 |
| Nifty IT − Nifty Pharma | -0.101295 | 0.4209 | 1 | Do not reject H0 | 2590 |
| Nifty IT − Nifty Private Bank | 0.839047 | 9.697e-11 | 9.988e-09 | Reject H0 | 2590 |
| Nifty IT − Nifty PSU Bank | 1.02116 | 5.522e-10 | 5.466e-08 | Reject H0 | 2590 |
| Nifty IT − Nifty PSE | 0.525761 | 3.481e-05 | 0.002471 | Reject H0 | 2590 |
| Nifty IT − Nifty Realty | 1.07646 | 1.058e-15 | 1.237e-13 | Reject H0 | 2590 |
| Nifty IT − Nifty Services Sector | 0.582904 | 2.217e-11 | 2.328e-09 | Reject H0 | 2590 |
| Nifty Media − Nifty Metal | 0.485824 | 2.619e-05 | 0.001912 | Reject H0 | 2590 |
| Nifty Media − Nifty Pharma | -0.52484 | 1.472e-06 | 0.0001192 | Reject H0 | 2590 |
| Nifty Media − Nifty Private Bank | 0.415502 | 0.0005009 | 0.02955 | Reject H0 | 2590 |
| Nifty Media − Nifty PSU Bank | 0.597618 | 2.986e-06 | 0.0002359 | Reject H0 | 2590 |
| Nifty Media − Nifty PSE | 0.102216 | 0.2853 | 1 | Do not reject H0 | 2590 |
| Nifty Media − Nifty Realty | 0.652911 | 1.99e-09 | 1.851e-07 | Reject H0 | 2590 |
| Nifty Media − Nifty Services Sector | 0.159359 | 0.09791 | 1 | Do not reject H0 | 2590 |
| Nifty Metal − Nifty Pharma | -1.01066 | 2.946e-14 | 3.329e-12 | Reject H0 | 2590 |
| Nifty Metal − Nifty Private Bank | -0.0703217 | 0.5756 | 1 | Do not reject H0 | 2590 |
| Nifty Metal − Nifty PSU Bank | 0.111794 | 0.4102 | 1 | Do not reject H0 | 2590 |
| Nifty Metal − Nifty PSE | -0.383608 | 1.319e-05 | 0.001015 | Reject H0 | 2590 |
| Nifty Metal − Nifty Realty | 0.167087 | 0.1596 | 1 | Do not reject H0 | 2590 |
| Nifty Metal − Nifty Services Sector | -0.326465 | 0.001488 | 0.07886 | Do not reject H0 | 2590 |
| Nifty Pharma − Nifty Private Bank | 0.940342 | 7.85e-11 | 8.164e-09 | Reject H0 | 2590 |
| Nifty Pharma − Nifty PSU Bank | 1.12246 | 4.752e-14 | 5.322e-12 | Reject H0 | 2590 |
| Nifty Pharma − Nifty PSE | 0.627056 | 3.778e-09 | 3.438e-07 | Reject H0 | 2590 |
| Nifty Pharma − Nifty Realty | 1.17775 | 5.87e-20 | 7.044e-18 | Reject H0 | 2590 |
| Nifty Pharma − Nifty Services Sector | 0.684199 | 8.124e-10 | 7.832e-08 | Reject H0 | 2590 |
| Nifty Private Bank − Nifty PSU Bank | 0.182115 | 0.1601 | 1 | Do not reject H0 | 2590 |
| Nifty Private Bank − Nifty PSE | -0.313286 | 0.0087 | 0.3741 | Do not reject H0 | 2590 |
| Nifty Private Bank − Nifty Realty | 0.237409 | 0.01863 | 0.7267 | Do not reject H0 | 2590 |
| Nifty Private Bank − Nifty Services Sector | -0.256143 | 5.717e-06 | 0.0004459 | Reject H0 | 2590 |
| Nifty PSU Bank − Nifty PSE | -0.495402 | 3.696e-05 | 0.002587 | Reject H0 | 2590 |
| Nifty PSU Bank − Nifty Realty | 0.0552931 | 0.6693 | 1 | Do not reject H0 | 2590 |
| Nifty PSU Bank − Nifty Services Sector | -0.438259 | 0.0002999 | 0.01859 | Reject H0 | 2590 |
| Nifty PSE − Nifty Realty | 0.550695 | 3.751e-07 | 3.076e-05 | Reject H0 | 2590 |
| Nifty PSE − Nifty Services Sector | 0.0571429 | 0.5297 | 1 | Do not reject H0 | 2590 |
| Nifty Realty − Nifty Services Sector | -0.493552 | 2.484e-08 | 2.186e-06 | Reject H0 | 2590 |

**Caveat:** These are same-date daily observations. The supplied workbook does not establish exact FX observation timestamp relative to the Indian market close; treat results as contemporaneous associations, not predictive or causal effects.

### H2 — CPI-derived inflation and monthly index returns

**Null:** CPI-derived inflation has zero linear association with monthly index returns; paired alternative: inflation slopes are equal across indices.

| Index | n | Focus coefficient | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |
|---|---:|---:|---|---:|---:|---|
| Nifty Auto | 119 | 0.324574 | [-0.329649, 0.978797] | 0.3309 | 1 | Do not reject H0 |
| Nifty Bank | 119 | 0.00821271 | [-0.578507, 0.594933] | 0.9781 | 1 | Do not reject H0 |
| Nifty Commodities | 119 | 0.118033 | [-0.400582, 0.636649] | 0.6555 | 1 | Do not reject H0 |
| Nifty Energy | 119 | -0.0236848 | [-0.573012, 0.525642] | 0.9327 | 1 | Do not reject H0 |
| Nifty FMCG | 119 | 0.100205 | [-0.25143, 0.45184] | 0.5765 | 1 | Do not reject H0 |
| Nifty Financial Services | 119 | -0.0063922 | [-0.541841, 0.529057] | 0.9813 | 1 | Do not reject H0 |
| Nifty Infrastructure | 119 | 0.0469138 | [-0.314808, 0.408635] | 0.7993 | 1 | Do not reject H0 |
| Nifty IT | 119 | 0.224643 | [-0.510006, 0.959292] | 0.549 | 1 | Do not reject H0 |
| Nifty Media | 119 | 0.470273 | [-0.211719, 1.15227] | 0.1765 | 1 | Do not reject H0 |
| Nifty Metal | 119 | 0.271629 | [-0.56298, 1.10624] | 0.5235 | 1 | Do not reject H0 |
| Nifty Pharma | 119 | 0.493708 | [-0.140415, 1.12783] | 0.127 | 1 | Do not reject H0 |
| Nifty Private Bank | 119 | 0.0431615 | [-0.571148, 0.657471] | 0.8905 | 1 | Do not reject H0 |
| Nifty PSU Bank | 119 | -0.00274203 | [-0.904775, 0.89929] | 0.9952 | 1 | Do not reject H0 |
| Nifty PSE | 119 | 0.142511 | [-0.404668, 0.68969] | 0.6097 | 1 | Do not reject H0 |
| Nifty Realty | 119 | 0.110556 | [-0.615407, 0.836519] | 0.7653 | 1 | Do not reject H0 |
| Nifty Services Sector | 119 | 0.0344354 | [-0.428347, 0.497218] | 0.884 | 1 | Do not reject H0 |

**Pairwise Same Reference Month Slope Tests**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | 0.316361 | 0.3407 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Commodities | 0.206541 | 0.3842 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Energy | 0.348259 | 0.2857 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty FMCG | 0.224369 | 0.4722 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Financial Services | 0.330966 | 0.3344 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Infrastructure | 0.27766 | 0.2491 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty IT | 0.0999309 | 0.8136 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Media | -0.145699 | 0.686 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Metal | 0.052945 | 0.8604 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Pharma | -0.169133 | 0.5738 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Private Bank | 0.281413 | 0.4003 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty PSU Bank | 0.327316 | 0.4471 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty PSE | 0.182063 | 0.6006 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Realty | 0.214018 | 0.6399 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Services Sector | 0.290139 | 0.3504 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Commodities | -0.109821 | 0.6268 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Energy | 0.0318975 | 0.9201 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty FMCG | -0.0919924 | 0.7506 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Financial Services | 0.0146049 | 0.8553 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Infrastructure | -0.0387011 | 0.8728 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty IT | -0.216431 | 0.5593 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Media | -0.462061 | 0.2255 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Metal | -0.263417 | 0.4076 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Pharma | -0.485495 | 0.2577 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Private Bank | -0.0349488 | 0.4261 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty PSU Bank | 0.0109547 | 0.9761 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty PSE | -0.134299 | 0.6657 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Realty | -0.102343 | 0.7285 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Services Sector | -0.0262226 | 0.8396 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Energy | 0.141718 | 0.477 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty FMCG | 0.0178284 | 0.9479 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Financial Services | 0.124426 | 0.569 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Infrastructure | 0.0711196 | 0.5564 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty IT | -0.10661 | 0.7322 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Media | -0.35224 | 0.1997 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Metal | -0.153596 | 0.486 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Pharma | -0.375674 | 0.1935 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Private Bank | 0.0748719 | 0.7518 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty PSU Bank | 0.120775 | 0.7526 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty PSE | -0.0244779 | 0.9083 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Realty | 0.00747738 | 0.9809 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Services Sector | 0.0835981 | 0.6226 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty FMCG | -0.12389 | 0.6412 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Financial Services | -0.0172926 | 0.955 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Infrastructure | -0.0705986 | 0.7162 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty IT | -0.248328 | 0.5448 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Media | -0.493958 | 0.0894 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Metal | -0.295314 | 0.4325 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Pharma | -0.517392 | 0.1454 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Private Bank | -0.0668463 | 0.8354 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty PSU Bank | -0.0209427 | 0.9637 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty PSE | -0.166196 | 0.4793 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Realty | -0.134241 | 0.7067 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Services Sector | -0.0581201 | 0.8252 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Financial Services | 0.106597 | 0.6936 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Infrastructure | 0.0532913 | 0.7907 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty IT | -0.124438 | 0.7763 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Media | -0.370068 | 0.3123 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Metal | -0.171424 | 0.6927 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Pharma | -0.393503 | 0.3079 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Private Bank | 0.0570436 | 0.8476 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty PSU Bank | 0.102947 | 0.8173 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty PSE | -0.0423062 | 0.8783 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Realty | -0.010351 | 0.9776 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Services Sector | 0.0657697 | 0.794 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Infrastructure | -0.053306 | 0.8085 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty IT | -0.231036 | 0.4993 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Media | -0.476666 | 0.1948 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Metal | -0.278021 | 0.4035 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Pharma | -0.5001 | 0.2184 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Private Bank | -0.0495537 | 0.5955 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty PSU Bank | -0.00365017 | 0.993 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty PSE | -0.148904 | 0.6325 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Realty | -0.116948 | 0.6443 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Services Sector | -0.0408276 | 0.6345 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty IT | -0.177729 | 0.5804 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Media | -0.42336 | 0.1074 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Metal | -0.224715 | 0.4665 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Pharma | -0.446794 | 0.0833 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Private Bank | 0.00375231 | 0.9881 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty PSU Bank | 0.0496559 | 0.9005 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty PSE | -0.0955975 | 0.639 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Realty | -0.0636422 | 0.8382 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Services Sector | 0.0124785 | 0.941 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Media | -0.24563 | 0.5568 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Metal | -0.0469859 | 0.9069 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Pharma | -0.269064 | 0.4111 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Private Bank | 0.181482 | 0.629 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty PSU Bank | 0.227385 | 0.686 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty PSE | 0.082132 | 0.8482 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Realty | 0.114087 | 0.7688 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Services Sector | 0.190208 | 0.4889 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Metal | 0.198644 | 0.6009 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Pharma | -0.0234342 | 0.9474 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Private Bank | 0.427112 | 0.2671 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty PSU Bank | 0.473015 | 0.3029 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty PSE | 0.327762 | 0.29 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Realty | 0.359717 | 0.2953 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Services Sector | 0.435838 | 0.1833 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty Pharma | -0.222078 | 0.5714 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty Private Bank | 0.228468 | 0.4837 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty PSU Bank | 0.274371 | 0.4909 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty PSE | 0.129118 | 0.7173 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty Realty | 0.161073 | 0.6904 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty Services Sector | 0.237194 | 0.4446 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty Private Bank | 0.450546 | 0.2971 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty PSU Bank | 0.49645 | 0.3662 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty PSE | 0.351196 | 0.3798 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty Realty | 0.383152 | 0.4228 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty Services Sector | 0.459272 | 0.18 | 1 | Do not reject H0 | 119 |
| Nifty Private Bank − Nifty PSU Bank | 0.0459036 | 0.9054 | 1 | Do not reject H0 | 119 |
| Nifty Private Bank − Nifty PSE | -0.0993498 | 0.7632 | 1 | Do not reject H0 | 119 |
| Nifty Private Bank − Nifty Realty | -0.0673945 | 0.8239 | 1 | Do not reject H0 | 119 |
| Nifty Private Bank − Nifty Services Sector | 0.00872619 | 0.9505 | 1 | Do not reject H0 | 119 |
| Nifty PSU Bank − Nifty PSE | -0.145253 | 0.6583 | 1 | Do not reject H0 | 119 |
| Nifty PSU Bank − Nifty Realty | -0.113298 | 0.8244 | 1 | Do not reject H0 | 119 |
| Nifty PSU Bank − Nifty Services Sector | -0.0371774 | 0.9294 | 1 | Do not reject H0 | 119 |
| Nifty PSE − Nifty Realty | 0.0319553 | 0.9309 | 1 | Do not reject H0 | 119 |
| Nifty PSE − Nifty Services Sector | 0.108076 | 0.7054 | 1 | Do not reject H0 | 119 |
| Nifty Realty − Nifty Services Sector | 0.0761207 | 0.7593 | 1 | Do not reject H0 | 119 |

**Pairwise One Reference Month Lag Slope Tests**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | 0.257624 | 0.457 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Commodities | 0.191269 | 0.4971 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Energy | 0.354246 | 0.3174 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty FMCG | -0.0848482 | 0.7948 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Financial Services | 0.250011 | 0.4843 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Infrastructure | 0.163579 | 0.563 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty IT | -0.0330268 | 0.9419 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Media | -0.0725661 | 0.8352 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Metal | 0.0794961 | 0.8239 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Pharma | -0.257147 | 0.4738 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Private Bank | 0.217495 | 0.5383 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty PSU Bank | 0.109814 | 0.8028 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty PSE | 0.0326873 | 0.9236 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Realty | 0.134595 | 0.7844 | 1 | Do not reject H0 | 119 |
| Nifty Auto − Nifty Services Sector | 0.195171 | 0.5568 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Commodities | -0.0663557 | 0.7974 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Energy | 0.0966214 | 0.7766 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty FMCG | -0.342473 | 0.3228 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Financial Services | -0.00761392 | 0.9221 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Infrastructure | -0.0940453 | 0.7405 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty IT | -0.290651 | 0.4572 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Media | -0.330191 | 0.3315 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Metal | -0.178128 | 0.5989 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Pharma | -0.514771 | 0.2505 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Private Bank | -0.0401292 | 0.247 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty PSU Bank | -0.14781 | 0.6929 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty PSE | -0.224937 | 0.4415 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Realty | -0.12303 | 0.6796 | 1 | Do not reject H0 | 119 |
| Nifty Bank − Nifty Services Sector | -0.062454 | 0.6637 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Energy | 0.162977 | 0.4065 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty FMCG | -0.276117 | 0.3145 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Financial Services | 0.0587418 | 0.804 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Infrastructure | -0.0276896 | 0.8309 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty IT | -0.224296 | 0.4371 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Media | -0.263835 | 0.2417 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Metal | -0.111773 | 0.6748 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Pharma | -0.448416 | 0.1129 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Private Bank | 0.0262265 | 0.9226 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty PSU Bank | -0.0814548 | 0.8521 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty PSE | -0.158582 | 0.3945 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Realty | -0.0566738 | 0.8563 | 1 | Do not reject H0 | 119 |
| Nifty Commodities − Nifty Services Sector | 0.00390173 | 0.9822 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty FMCG | -0.439094 | 0.1176 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Financial Services | -0.104235 | 0.7402 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Infrastructure | -0.190667 | 0.3232 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty IT | -0.387273 | 0.3197 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Media | -0.426812 | 0.1004 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Metal | -0.27475 | 0.5125 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Pharma | -0.611393 | 0.08162 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Private Bank | -0.136751 | 0.6943 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty PSU Bank | -0.244432 | 0.6393 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty PSE | -0.321559 | 0.124 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Realty | -0.219651 | 0.5337 | 1 | Do not reject H0 | 119 |
| Nifty Energy − Nifty Services Sector | -0.159075 | 0.5467 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Financial Services | 0.334859 | 0.2841 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Infrastructure | 0.248427 | 0.1951 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty IT | 0.0518214 | 0.8958 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Media | 0.0122821 | 0.9717 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Metal | 0.164344 | 0.7293 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Pharma | -0.172299 | 0.5575 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Private Bank | 0.302343 | 0.3955 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty PSU Bank | 0.194662 | 0.7221 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty PSE | 0.117535 | 0.6894 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Realty | 0.219443 | 0.6163 | 1 | Do not reject H0 | 119 |
| Nifty FMCG − Nifty Services Sector | 0.280019 | 0.2973 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Infrastructure | -0.0864313 | 0.7328 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty IT | -0.283037 | 0.4319 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Media | -0.322577 | 0.3152 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Metal | -0.170514 | 0.6212 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Pharma | -0.507158 | 0.2265 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Private Bank | -0.0325153 | 0.7248 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty PSU Bank | -0.140197 | 0.7417 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty PSE | -0.217323 | 0.4385 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Realty | -0.115416 | 0.6555 | 1 | Do not reject H0 | 119 |
| Nifty Financial Services − Nifty Services Sector | -0.05484 | 0.57 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty IT | -0.196606 | 0.5019 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Media | -0.236145 | 0.3543 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Metal | -0.0840831 | 0.8181 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Pharma | -0.420726 | 0.0836 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Private Bank | 0.0539161 | 0.8568 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty PSU Bank | -0.0537652 | 0.907 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty PSE | -0.130892 | 0.4721 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Realty | -0.0289843 | 0.9339 | 1 | Do not reject H0 | 119 |
| Nifty Infrastructure − Nifty Services Sector | 0.0315913 | 0.8643 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Media | -0.0395392 | 0.9154 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Metal | 0.112523 | 0.7847 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Pharma | -0.22412 | 0.4297 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Private Bank | 0.250522 | 0.5297 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty PSU Bank | 0.142841 | 0.8074 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty PSE | 0.0657141 | 0.8643 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Realty | 0.167622 | 0.6766 | 1 | Do not reject H0 | 119 |
| Nifty IT − Nifty Services Sector | 0.228197 | 0.4121 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Metal | 0.152062 | 0.6842 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Pharma | -0.184581 | 0.6065 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Private Bank | 0.290061 | 0.4 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty PSU Bank | 0.18238 | 0.7138 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty PSE | 0.105253 | 0.7168 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Realty | 0.207161 | 0.5297 | 1 | Do not reject H0 | 119 |
| Nifty Media − Nifty Services Sector | 0.267737 | 0.3287 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty Pharma | -0.336643 | 0.4519 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty Private Bank | 0.137999 | 0.6865 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty PSU Bank | 0.0303179 | 0.9454 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty PSE | -0.0468089 | 0.9025 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty Realty | 0.0550988 | 0.8895 | 1 | Do not reject H0 | 119 |
| Nifty Metal − Nifty Services Sector | 0.115674 | 0.7233 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty Private Bank | 0.474642 | 0.3018 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty PSU Bank | 0.366961 | 0.5393 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty PSE | 0.289834 | 0.428 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty Realty | 0.391742 | 0.4405 | 1 | Do not reject H0 | 119 |
| Nifty Pharma − Nifty Services Sector | 0.452318 | 0.1842 | 1 | Do not reject H0 | 119 |
| Nifty Private Bank − Nifty PSU Bank | -0.107681 | 0.7792 | 1 | Do not reject H0 | 119 |
| Nifty Private Bank − Nifty PSE | -0.184808 | 0.5485 | 1 | Do not reject H0 | 119 |
| Nifty Private Bank − Nifty Realty | -0.0829003 | 0.7844 | 1 | Do not reject H0 | 119 |
| Nifty Private Bank − Nifty Services Sector | -0.0223248 | 0.8857 | 1 | Do not reject H0 | 119 |
| Nifty PSU Bank − Nifty PSE | -0.0771267 | 0.8428 | 1 | Do not reject H0 | 119 |
| Nifty PSU Bank − Nifty Realty | 0.024781 | 0.9631 | 1 | Do not reject H0 | 119 |
| Nifty PSU Bank − Nifty Services Sector | 0.0853565 | 0.8469 | 1 | Do not reject H0 | 119 |
| Nifty PSE − Nifty Realty | 0.101908 | 0.7738 | 1 | Do not reject H0 | 119 |
| Nifty PSE − Nifty Services Sector | 0.162483 | 0.5094 | 1 | Do not reject H0 | 119 |
| Nifty Realty − Nifty Services Sector | 0.0605756 | 0.8115 | 1 | Do not reject H0 | 119 |

**Caveat:** CPI workbook supplies reference months and reported rates but no publication timestamps or expectations. Same-month analysis is contemporaneous and may use information published after some/all of the market-return month. One-reference-month lag is a timing sensitivity, not proof that the exact release was available before each return.

### H3 — Weekly FX reserves and index returns, controlling for USD/INR

**Null:** Reserve-change coefficient is zero; paired alternative: coefficient differs across indices.

| Index | n | Focus coefficient | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |
|---|---:|---:|---|---:|---:|---|
| Nifty Auto | 560 | 0.222845 | [-0.200489, 0.646179] | 0.3022 | 1 | Do not reject H0 |
| Nifty Bank | 560 | 0.350096 | [-0.0902448, 0.790436] | 0.1192 | 1 | Do not reject H0 |
| Nifty Commodities | 560 | 0.428227 | [0.0856761, 0.770777] | 0.01428 | 0.1999 | Do not reject H0 |
| Nifty Energy | 560 | 0.140955 | [-0.187126, 0.469036] | 0.3997 | 1 | Do not reject H0 |
| Nifty FMCG | 560 | 0.0717693 | [-0.2044, 0.347939] | 0.6105 | 1 | Do not reject H0 |
| Nifty Financial Services | 560 | 0.345129 | [-0.080754, 0.771011] | 0.1122 | 1 | Do not reject H0 |
| Nifty Infrastructure | 560 | 0.230423 | [-0.0842565, 0.545103] | 0.1512 | 1 | Do not reject H0 |
| Nifty IT | 560 | 0.603125 | [0.217035, 0.989216] | 0.002201 | 0.03521 | Reject H0 |
| Nifty Media | 560 | 0.210063 | [-0.224544, 0.644671] | 0.3435 | 1 | Do not reject H0 |
| Nifty Metal | 560 | 0.7495 | [0.263794, 1.23521] | 0.002491 | 0.03736 | Reject H0 |
| Nifty Pharma | 560 | 0.219212 | [-0.102968, 0.541392] | 0.1823 | 1 | Do not reject H0 |
| Nifty Private Bank | 560 | 0.3749 | [-0.071659, 0.821459] | 0.09988 | 1 | Do not reject H0 |
| Nifty PSU Bank | 560 | 0.179985 | [-0.316835, 0.676805] | 0.4777 | 1 | Do not reject H0 |
| Nifty PSE | 560 | 0.311561 | [-0.0384675, 0.66159] | 0.08106 | 0.9727 | Do not reject H0 |
| Nifty Realty | 560 | 0.371292 | [-0.091016, 0.833601] | 0.1155 | 1 | Do not reject H0 |
| Nifty Services Sector | 560 | 0.378482 | [0.00463934, 0.752325] | 0.04722 | 0.6139 | Do not reject H0 |

**Pairwise Controlled Reserves Slope Tests**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | -0.12725 | 0.3682 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Commodities | -0.205381 | 0.07718 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Energy | 0.0818901 | 0.5904 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty FMCG | 0.151076 | 0.3089 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Financial Services | -0.122283 | 0.3488 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Infrastructure | -0.0075778 | 0.9443 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty IT | -0.38028 | 0.03071 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Media | 0.0127818 | 0.9362 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Metal | -0.526655 | 0.0004416 | 0.05211 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Pharma | 0.0036334 | 0.9801 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Private Bank | -0.152055 | 0.3135 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty PSU Bank | 0.04286 | 0.84 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty PSE | -0.0887157 | 0.5607 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Realty | -0.148447 | 0.2807 | 1 | Do not reject H0 | 560 |
| Nifty Auto − Nifty Services Sector | -0.155637 | 0.1648 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Commodities | -0.078131 | 0.6042 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Energy | 0.20914 | 0.2089 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty FMCG | 0.278326 | 0.1129 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Financial Services | 0.00496692 | 0.883 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Infrastructure | 0.119673 | 0.3464 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty IT | -0.25303 | 0.1978 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Media | 0.140032 | 0.4517 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Metal | -0.399405 | 0.04531 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Pharma | 0.130884 | 0.485 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Private Bank | -0.0248045 | 0.4219 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty PSU Bank | 0.17011 | 0.3859 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty PSE | 0.0385346 | 0.8145 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Realty | -0.0211968 | 0.8951 | 1 | Do not reject H0 | 560 |
| Nifty Bank − Nifty Services Sector | -0.0283866 | 0.6732 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Energy | 0.287271 | 0.0001897 | 0.02276 | Reject H0 | 560 |
| Nifty Commodities − Nifty FMCG | 0.356457 | 0.003542 | 0.4002 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Financial Services | 0.0830979 | 0.5537 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Infrastructure | 0.197804 | 0.00217 | 0.2495 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty IT | -0.174899 | 0.312 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Media | 0.218163 | 0.122 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Metal | -0.321274 | 0.003683 | 0.4125 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Pharma | 0.209015 | 0.1101 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Private Bank | 0.0533265 | 0.7413 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty PSU Bank | 0.248241 | 0.1658 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty PSE | 0.116666 | 0.1075 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Realty | 0.0569342 | 0.6863 | 1 | Do not reject H0 | 560 |
| Nifty Commodities − Nifty Services Sector | 0.0497444 | 0.6721 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty FMCG | 0.0691859 | 0.6028 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty Financial Services | -0.204174 | 0.1978 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty Infrastructure | -0.0894679 | 0.2664 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty IT | -0.46217 | 0.02283 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty Media | -0.0691083 | 0.6671 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty Metal | -0.608545 | 0.0004338 | 0.05163 | Do not reject H0 | 560 |
| Nifty Energy − Nifty Pharma | -0.0782567 | 0.6153 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty Private Bank | -0.233945 | 0.1782 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty PSU Bank | -0.0390301 | 0.8439 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty PSE | -0.170606 | 0.01415 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty Realty | -0.230337 | 0.1732 | 1 | Do not reject H0 | 560 |
| Nifty Energy − Nifty Services Sector | -0.237527 | 0.09734 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty Financial Services | -0.273359 | 0.09534 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty Infrastructure | -0.158654 | 0.1503 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty IT | -0.531356 | 0.004403 | 0.4844 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty Media | -0.138294 | 0.4506 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty Metal | -0.677731 | 0.0004867 | 0.05694 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty Pharma | -0.147443 | 0.306 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty Private Bank | -0.303131 | 0.09909 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty PSU Bank | -0.108216 | 0.6142 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty PSE | -0.239792 | 0.08727 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty Realty | -0.299523 | 0.105 | 1 | Do not reject H0 | 560 |
| Nifty FMCG − Nifty Services Sector | -0.306713 | 0.02948 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty Infrastructure | 0.114706 | 0.3249 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty IT | -0.257997 | 0.1623 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty Media | 0.135065 | 0.4537 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty Metal | -0.404371 | 0.03428 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty Pharma | 0.125917 | 0.4782 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty Private Bank | -0.0297714 | 0.5526 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty PSU Bank | 0.165143 | 0.4101 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty PSE | 0.0335677 | 0.8302 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty Realty | -0.0261637 | 0.8632 | 1 | Do not reject H0 | 560 |
| Nifty Financial Services − Nifty Services Sector | -0.0333536 | 0.5126 | 1 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty IT | -0.372702 | 0.0239 | 1 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty Media | 0.0203596 | 0.8902 | 1 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty Metal | -0.519077 | 0.0008256 | 0.09577 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty Pharma | 0.0112112 | 0.9256 | 1 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty Private Bank | -0.144477 | 0.2863 | 1 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty PSU Bank | 0.0504378 | 0.7877 | 1 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty PSE | -0.0811379 | 0.3626 | 1 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty Realty | -0.140869 | 0.2753 | 1 | Do not reject H0 | 560 |
| Nifty Infrastructure − Nifty Services Sector | -0.148059 | 0.1129 | 1 | Do not reject H0 | 560 |
| Nifty IT − Nifty Media | 0.393062 | 0.07407 | 1 | Do not reject H0 | 560 |
| Nifty IT − Nifty Metal | -0.146375 | 0.4738 | 1 | Do not reject H0 | 560 |
| Nifty IT − Nifty Pharma | 0.383913 | 0.02044 | 1 | Do not reject H0 | 560 |
| Nifty IT − Nifty Private Bank | 0.228225 | 0.2589 | 1 | Do not reject H0 | 560 |
| Nifty IT − Nifty PSU Bank | 0.42314 | 0.1132 | 1 | Do not reject H0 | 560 |
| Nifty IT − Nifty PSE | 0.291564 | 0.1514 | 1 | Do not reject H0 | 560 |
| Nifty IT − Nifty Realty | 0.231833 | 0.2412 | 1 | Do not reject H0 | 560 |
| Nifty IT − Nifty Services Sector | 0.224643 | 0.1043 | 1 | Do not reject H0 | 560 |
| Nifty Media − Nifty Metal | -0.539437 | 0.002741 | 0.3125 | Do not reject H0 | 560 |
| Nifty Media − Nifty Pharma | -0.00914842 | 0.9599 | 1 | Do not reject H0 | 560 |
| Nifty Media − Nifty Private Bank | -0.164837 | 0.3927 | 1 | Do not reject H0 | 560 |
| Nifty Media − Nifty PSU Bank | 0.0300782 | 0.8806 | 1 | Do not reject H0 | 560 |
| Nifty Media − Nifty PSE | -0.101498 | 0.505 | 1 | Do not reject H0 | 560 |
| Nifty Media − Nifty Realty | -0.161229 | 0.333 | 1 | Do not reject H0 | 560 |
| Nifty Media − Nifty Services Sector | -0.168419 | 0.3157 | 1 | Do not reject H0 | 560 |
| Nifty Metal − Nifty Pharma | 0.530288 | 0.00501 | 0.541 | Do not reject H0 | 560 |
| Nifty Metal − Nifty Private Bank | 0.3746 | 0.07704 | 1 | Do not reject H0 | 560 |
| Nifty Metal − Nifty PSU Bank | 0.569515 | 0.004717 | 0.5142 | Do not reject H0 | 560 |
| Nifty Metal − Nifty PSE | 0.437939 | 0.004128 | 0.4582 | Do not reject H0 | 560 |
| Nifty Metal − Nifty Realty | 0.378208 | 0.0309 | 1 | Do not reject H0 | 560 |
| Nifty Metal − Nifty Services Sector | 0.371018 | 0.03135 | 1 | Do not reject H0 | 560 |
| Nifty Pharma − Nifty Private Bank | -0.155688 | 0.4143 | 1 | Do not reject H0 | 560 |
| Nifty Pharma − Nifty PSU Bank | 0.0392266 | 0.8704 | 1 | Do not reject H0 | 560 |
| Nifty Pharma − Nifty PSE | -0.0923491 | 0.5843 | 1 | Do not reject H0 | 560 |
| Nifty Pharma − Nifty Realty | -0.152081 | 0.3489 | 1 | Do not reject H0 | 560 |
| Nifty Pharma − Nifty Services Sector | -0.15927 | 0.2788 | 1 | Do not reject H0 | 560 |
| Nifty Private Bank − Nifty PSU Bank | 0.194915 | 0.3679 | 1 | Do not reject H0 | 560 |
| Nifty Private Bank − Nifty PSE | 0.0633391 | 0.7174 | 1 | Do not reject H0 | 560 |
| Nifty Private Bank − Nifty Realty | 0.00360768 | 0.9826 | 1 | Do not reject H0 | 560 |
| Nifty Private Bank − Nifty Services Sector | -0.00358214 | 0.9629 | 1 | Do not reject H0 | 560 |
| Nifty PSU Bank − Nifty PSE | -0.131576 | 0.4594 | 1 | Do not reject H0 | 560 |
| Nifty PSU Bank − Nifty Realty | -0.191307 | 0.3956 | 1 | Do not reject H0 | 560 |
| Nifty PSU Bank − Nifty Services Sector | -0.198497 | 0.3278 | 1 | Do not reject H0 | 560 |
| Nifty PSE − Nifty Realty | -0.0597314 | 0.7247 | 1 | Do not reject H0 | 560 |
| Nifty PSE − Nifty Services Sector | -0.0669213 | 0.6393 | 1 | Do not reject H0 | 560 |
| Nifty Realty − Nifty Services Sector | -0.00718982 | 0.9583 | 1 | Do not reject H0 | 560 |

**Caveat:** The workbook provides reserve observation week-end but not first public-release timestamps. Same-week joins are contemporaneous associations. A significant future-reserve lead is a warning for common shocks, dependence or timing issues, not evidence of causality.

### H4 — RBI repo-rate effective-date event study

**Null:** Mean three-session abnormal return (CAR) around supplied repo effective dates equals zero; paired alternative: event CAR differs between indices.

| Index | Eligible events | Mean CAR (%) | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |
|---|---:|---:|---|---:|---:|---|
| Nifty Auto | 32 | 0.323773 | [-0.545823, 1.19337] | 0.4534 | 1 | Do not reject H0 |
| Nifty Bank | 32 | 0.252211 | [-0.335872, 0.840293] | 0.3885 | 1 | Do not reject H0 |
| Nifty Commodities | 32 | 0.30407 | [-0.38286, 0.991001] | 0.3736 | 1 | Do not reject H0 |
| Nifty Energy | 32 | 0.0358511 | [-0.624391, 0.696093] | 0.9125 | 1 | Do not reject H0 |
| Nifty FMCG | 32 | 0.106654 | [-0.622928, 0.836236] | 0.7676 | 1 | Do not reject H0 |
| Nifty Financial Services | 32 | 0.161451 | [-0.461928, 0.784831] | 0.6011 | 1 | Do not reject H0 |
| Nifty Infrastructure | 32 | 0.118328 | [-0.430533, 0.667189] | 0.6632 | 1 | Do not reject H0 |
| Nifty IT | 32 | 0.376494 | [-0.243403, 0.99639] | 0.2248 | 1 | Do not reject H0 |
| Nifty Media | 32 | 0.402301 | [-0.667646, 1.47225] | 0.449 | 1 | Do not reject H0 |
| Nifty Metal | 32 | 0.565345 | [-0.434579, 1.56527] | 0.2577 | 1 | Do not reject H0 |
| Nifty Pharma | 32 | 0.196893 | [-0.54313, 0.936916] | 0.5913 | 1 | Do not reject H0 |
| Nifty Private Bank | 32 | 0.379838 | [-0.267168, 1.02684] | 0.2403 | 1 | Do not reject H0 |
| Nifty PSU Bank | 32 | 0.0640085 | [-0.830262, 0.958279] | 0.8849 | 1 | Do not reject H0 |
| Nifty PSE | 32 | 0.663326 | [0.00737481, 1.31928] | 0.04763 | 0.7621 | Do not reject H0 |
| Nifty Realty | 32 | 0.255471 | [-0.838894, 1.34984] | 0.6373 | 1 | Do not reject H0 |
| Nifty Services Sector | 32 | 0.179653 | [-0.330662, 0.689967] | 0.4781 | 1 | Do not reject H0 |

**Pairwise Tests**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | 0.0715626 | 0.8623 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Commodities | 0.0197027 | 0.9425 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Energy | 0.287922 | 0.3814 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty FMCG | 0.217119 | 0.6466 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Financial Services | 0.162322 | 0.6594 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Infrastructure | 0.205445 | 0.5023 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty IT | -0.0527205 | 0.904 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Media | -0.0785274 | 0.8564 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Metal | -0.241571 | 0.5111 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Pharma | 0.12688 | 0.8028 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Private Bank | -0.0560645 | 0.9009 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty PSU Bank | 0.259765 | 0.5719 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty PSE | -0.339552 | 0.4017 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Realty | 0.0683023 | 0.859 | 1 | Do not reject H0 | 32 |
| Nifty Auto − Nifty Services Sector | 0.144121 | 0.6942 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Commodities | -0.0518599 | 0.8632 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Energy | 0.216359 | 0.5219 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty FMCG | 0.145557 | 0.6574 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Financial Services | 0.0907591 | 0.5438 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Infrastructure | 0.133883 | 0.5557 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty IT | -0.124283 | 0.6594 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Media | -0.15009 | 0.7764 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Metal | -0.313134 | 0.4744 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Pharma | 0.0553175 | 0.8513 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Private Bank | -0.127627 | 0.1486 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty PSU Bank | 0.188202 | 0.5964 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty PSE | -0.411115 | 0.1645 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Realty | -0.0032603 | 0.9942 | 1 | Do not reject H0 | 32 |
| Nifty Bank − Nifty Services Sector | 0.072558 | 0.5301 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Energy | 0.268219 | 0.2349 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty FMCG | 0.197416 | 0.5575 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Financial Services | 0.142619 | 0.6358 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Infrastructure | 0.185742 | 0.2925 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty IT | -0.0724232 | 0.8396 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Media | -0.0982302 | 0.8257 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Metal | -0.261274 | 0.3102 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Pharma | 0.107177 | 0.7485 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Private Bank | -0.0757673 | 0.8196 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty PSU Bank | 0.240062 | 0.5563 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty PSE | -0.359255 | 0.1291 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Realty | 0.0485996 | 0.8931 | 1 | Do not reject H0 | 32 |
| Nifty Commodities − Nifty Services Sector | 0.124418 | 0.6436 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty FMCG | -0.0708029 | 0.8509 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty Financial Services | -0.1256 | 0.7058 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty Infrastructure | -0.0824768 | 0.6675 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty IT | -0.340643 | 0.3788 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty Media | -0.366449 | 0.3984 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty Metal | -0.529493 | 0.2071 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty Pharma | -0.161042 | 0.6664 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty Private Bank | -0.343987 | 0.3545 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty PSU Bank | -0.0281574 | 0.943 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty PSE | -0.627474 | 0.002107 | 0.2528 | Do not reject H0 | 32 |
| Nifty Energy − Nifty Realty | -0.21962 | 0.5382 | 1 | Do not reject H0 | 32 |
| Nifty Energy − Nifty Services Sector | -0.143802 | 0.6247 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty Financial Services | -0.0547975 | 0.8917 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty Infrastructure | -0.011674 | 0.9709 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty IT | -0.26984 | 0.523 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty Media | -0.295647 | 0.5655 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty Metal | -0.458691 | 0.3436 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty Pharma | -0.0902391 | 0.8112 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty Private Bank | -0.273184 | 0.4162 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty PSU Bank | 0.0426454 | 0.9274 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty PSE | -0.556672 | 0.09443 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty Realty | -0.148817 | 0.7728 | 1 | Do not reject H0 | 32 |
| Nifty FMCG − Nifty Services Sector | -0.0729986 | 0.8361 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty Infrastructure | 0.0431235 | 0.8504 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty IT | -0.215042 | 0.4833 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty Media | -0.240849 | 0.6384 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty Metal | -0.403893 | 0.3283 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty Pharma | -0.0354416 | 0.9182 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty Private Bank | -0.218386 | 0.2844 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty PSU Bank | 0.0974429 | 0.7956 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty PSE | -0.501874 | 0.1403 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty Realty | -0.0940194 | 0.8148 | 1 | Do not reject H0 | 32 |
| Nifty Financial Services − Nifty Services Sector | -0.0182011 | 0.858 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty IT | -0.258166 | 0.4369 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty Media | -0.283973 | 0.5289 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty Metal | -0.447017 | 0.226 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty Pharma | -0.0785652 | 0.8019 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty Private Bank | -0.26151 | 0.3219 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty PSU Bank | 0.0543194 | 0.8841 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty PSE | -0.544998 | 0.008812 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty Realty | -0.137143 | 0.7093 | 1 | Do not reject H0 | 32 |
| Nifty Infrastructure − Nifty Services Sector | -0.0613247 | 0.7512 | 1 | Do not reject H0 | 32 |
| Nifty IT − Nifty Media | -0.025807 | 0.9664 | 1 | Do not reject H0 | 32 |
| Nifty IT − Nifty Metal | -0.188851 | 0.6918 | 1 | Do not reject H0 | 32 |
| Nifty IT − Nifty Pharma | 0.179601 | 0.5994 | 1 | Do not reject H0 | 32 |
| Nifty IT − Nifty Private Bank | -0.00334408 | 0.9911 | 1 | Do not reject H0 | 32 |
| Nifty IT − Nifty PSU Bank | 0.312485 | 0.5427 | 1 | Do not reject H0 | 32 |
| Nifty IT − Nifty PSE | -0.286832 | 0.4294 | 1 | Do not reject H0 | 32 |
| Nifty IT − Nifty Realty | 0.121023 | 0.8087 | 1 | Do not reject H0 | 32 |
| Nifty IT − Nifty Services Sector | 0.196841 | 0.3895 | 1 | Do not reject H0 | 32 |
| Nifty Media − Nifty Metal | -0.163044 | 0.7825 | 1 | Do not reject H0 | 32 |
| Nifty Media − Nifty Pharma | 0.205407 | 0.6823 | 1 | Do not reject H0 | 32 |
| Nifty Media − Nifty Private Bank | 0.0224629 | 0.9677 | 1 | Do not reject H0 | 32 |
| Nifty Media − Nifty PSU Bank | 0.338292 | 0.5164 | 1 | Do not reject H0 | 32 |
| Nifty Media − Nifty PSE | -0.261025 | 0.5851 | 1 | Do not reject H0 | 32 |
| Nifty Media − Nifty Realty | 0.14683 | 0.7508 | 1 | Do not reject H0 | 32 |
| Nifty Media − Nifty Services Sector | 0.222648 | 0.6641 | 1 | Do not reject H0 | 32 |
| Nifty Metal − Nifty Pharma | 0.368451 | 0.4665 | 1 | Do not reject H0 | 32 |
| Nifty Metal − Nifty Private Bank | 0.185507 | 0.6874 | 1 | Do not reject H0 | 32 |
| Nifty Metal − Nifty PSU Bank | 0.501336 | 0.3367 | 1 | Do not reject H0 | 32 |
| Nifty Metal − Nifty PSE | -0.097981 | 0.8159 | 1 | Do not reject H0 | 32 |
| Nifty Metal − Nifty Realty | 0.309874 | 0.4965 | 1 | Do not reject H0 | 32 |
| Nifty Metal − Nifty Services Sector | 0.385692 | 0.345 | 1 | Do not reject H0 | 32 |
| Nifty Pharma − Nifty Private Bank | -0.182945 | 0.5478 | 1 | Do not reject H0 | 32 |
| Nifty Pharma − Nifty PSU Bank | 0.132885 | 0.7796 | 1 | Do not reject H0 | 32 |
| Nifty Pharma − Nifty PSE | -0.466432 | 0.1337 | 1 | Do not reject H0 | 32 |
| Nifty Pharma − Nifty Realty | -0.0585778 | 0.8998 | 1 | Do not reject H0 | 32 |
| Nifty Pharma − Nifty Services Sector | 0.0172405 | 0.9539 | 1 | Do not reject H0 | 32 |
| Nifty Private Bank − Nifty PSU Bank | 0.315829 | 0.4463 | 1 | Do not reject H0 | 32 |
| Nifty Private Bank − Nifty PSE | -0.283488 | 0.3518 | 1 | Do not reject H0 | 32 |
| Nifty Private Bank − Nifty Realty | 0.124367 | 0.7914 | 1 | Do not reject H0 | 32 |
| Nifty Private Bank − Nifty Services Sector | 0.200185 | 0.2273 | 1 | Do not reject H0 | 32 |
| Nifty PSU Bank − Nifty PSE | -0.599317 | 0.1737 | 1 | Do not reject H0 | 32 |
| Nifty PSU Bank − Nifty Realty | -0.191462 | 0.7006 | 1 | Do not reject H0 | 32 |
| Nifty PSU Bank − Nifty Services Sector | -0.115644 | 0.7654 | 1 | Do not reject H0 | 32 |
| Nifty PSE − Nifty Realty | 0.407855 | 0.306 | 1 | Do not reject H0 | 32 |
| Nifty PSE − Nifty Services Sector | 0.483673 | 0.08673 | 1 | Do not reject H0 | 32 |
| Nifty Realty − Nifty Services Sector | 0.0758183 | 0.8549 | 1 | Do not reject H0 | 32 |

### H5 — Quarterly real GVA growth and index returns

**Null:** Lagged GVA YoY growth has zero linear association with quarterly index returns; pairwise slopes equal across indices.

| Index | n | Focus coefficient | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |
|---|---:|---:|---|---:|---:|---|
| Nifty Auto | 12 | 1.74983 | [-4.10618, 7.60584] | 0.5581 | 1 | Do not reject H0 |
| Nifty Bank | 12 | 5.14226 | [-0.858586, 11.1431] | 0.09305 | 0.6971 | Do not reject H0 |
| Nifty Commodities | 12 | 4.69426 | [-0.403548, 9.79207] | 0.0711 | 0.6971 | Do not reject H0 |
| Nifty Energy | 12 | 5.53818 | [-0.672329, 11.7487] | 0.0805 | 0.6971 | Do not reject H0 |
| Nifty FMCG | 12 | 3.98787 | [-0.121729, 8.09746] | 0.05718 | 0.6971 | Do not reject H0 |
| Nifty Financial Services | 12 | 4.93459 | [0.520643, 9.34854] | 0.02844 | 0.4266 | Do not reject H0 |
| Nifty Infrastructure | 12 | 3.49961 | [-0.182834, 7.18206] | 0.06251 | 0.6971 | Do not reject H0 |
| Nifty IT | 12 | -1.21622 | [-7.72252, 5.29008] | 0.7141 | 1 | Do not reject H0 |
| Nifty Media | 12 | -1.48725 | [-15.7388, 12.7643] | 0.8379 | 1 | Do not reject H0 |
| Nifty Metal | 12 | 6.12378 | [1.88665, 10.3609] | 0.004616 | 0.07386 | Do not reject H0 |
| Nifty Pharma | 12 | 3.23257 | [-0.0503975, 6.51554] | 0.05362 | 0.6971 | Do not reject H0 |
| Nifty Private Bank | 12 | 6.12774 | [0.23683, 12.0186] | 0.04147 | 0.5806 | Do not reject H0 |
| Nifty PSU Bank | 12 | -2.23796 | [-9.05877, 4.58285] | 0.5202 | 1 | Do not reject H0 |
| Nifty PSE | 12 | 1.81863 | [-4.97984, 8.61711] | 0.6001 | 1 | Do not reject H0 |
| Nifty Realty | 12 | 7.33201 | [-3.3592, 18.0232] | 0.1789 | 1 | Do not reject H0 |
| Nifty Services Sector | 12 | 3.11299 | [-0.106556, 6.33253] | 0.05808 | 0.6971 | Do not reject H0 |

**Pairwise Lagged Growth Slope Tests**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | -3.39243 | 0.1944 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Commodities | -2.94443 | 0.2314 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Energy | -3.78835 | 0.005647 | 0.6777 | Do not reject H0 | 12 |
| Nifty Auto − Nifty FMCG | -2.23804 | 0.04798 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Financial Services | -3.18476 | 0.1035 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Infrastructure | -1.74978 | 0.2957 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty IT | 2.96605 | 0.6119 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Media | 3.23708 | 0.6129 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Metal | -4.37395 | 0.04792 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Pharma | -1.48274 | 0.6385 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Private Bank | -4.37791 | 0.07524 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty PSU Bank | 3.98779 | 0.3743 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty PSE | -0.0688028 | 0.9848 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Realty | -5.58218 | 0.1534 | 1 | Do not reject H0 | 12 |
| Nifty Auto − Nifty Services Sector | -1.36316 | 0.5346 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Commodities | 0.447998 | 0.916 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Energy | -0.395916 | 0.9072 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty FMCG | 1.15439 | 0.6223 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Financial Services | 0.207668 | 0.8449 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Infrastructure | 1.64265 | 0.5117 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty IT | 6.35848 | 0.2192 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Media | 6.62951 | 0.2242 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Metal | -0.981519 | 0.7985 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Pharma | 1.90969 | 0.474 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Private Bank | -0.985475 | 0.02676 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty PSU Bank | 7.38022 | 0.06388 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty PSE | 3.32363 | 0.5333 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Realty | -2.18975 | 0.4531 | 1 | Do not reject H0 | 12 |
| Nifty Bank − Nifty Services Sector | 2.02927 | 0.2297 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Energy | -0.843914 | 0.6548 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty FMCG | 0.706395 | 0.7367 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Financial Services | -0.24033 | 0.9418 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Infrastructure | 1.19465 | 0.5182 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty IT | 5.91048 | 0.22 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Media | 6.18151 | 0.4417 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Metal | -1.42952 | 0.1195 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Pharma | 1.46169 | 0.6724 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Private Bank | -1.43347 | 0.7274 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty PSU Bank | 6.93222 | 0.1426 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty PSE | 2.87563 | 0.03024 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Realty | -2.63775 | 0.6527 | 1 | Do not reject H0 | 12 |
| Nifty Commodities − Nifty Services Sector | 1.58128 | 0.5759 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty FMCG | 1.55031 | 0.3534 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty Financial Services | 0.603584 | 0.8195 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty Infrastructure | 2.03856 | 0.2 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty IT | 6.7544 | 0.2465 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty Media | 7.02543 | 0.2863 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty Metal | -0.585603 | 0.7476 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty Pharma | 2.30561 | 0.4774 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty Private Bank | -0.589559 | 0.8527 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty PSU Bank | 7.77614 | 0.08493 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty PSE | 3.71954 | 0.1693 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty Realty | -1.79384 | 0.6817 | 1 | Do not reject H0 | 12 |
| Nifty Energy − Nifty Services Sector | 2.42519 | 0.356 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty Financial Services | -0.946725 | 0.494 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty Infrastructure | 0.488254 | 0.6574 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty IT | 5.20409 | 0.289 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty Media | 5.47512 | 0.4213 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty Metal | -2.13591 | 0.2698 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty Pharma | 0.755297 | 0.7731 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty Private Bank | -2.13987 | 0.3489 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty PSU Bank | 6.22583 | 0.1499 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty PSE | 2.16923 | 0.5016 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty Realty | -3.34414 | 0.4081 | 1 | Do not reject H0 | 12 |
| Nifty FMCG − Nifty Services Sector | 0.874881 | 0.505 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty Infrastructure | 1.43498 | 0.3871 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty IT | 6.15081 | 0.1955 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty Media | 6.42184 | 0.2916 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty Metal | -1.18919 | 0.6881 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty Pharma | 1.70202 | 0.4514 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty Private Bank | -1.19314 | 0.2726 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty PSU Bank | 7.17255 | 0.07024 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty PSE | 3.11596 | 0.477 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty Realty | -2.39742 | 0.4791 | 1 | Do not reject H0 | 12 |
| Nifty Financial Services − Nifty Services Sector | 1.82161 | 0.0292 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty IT | 4.71584 | 0.2808 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty Media | 4.98687 | 0.4449 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty Metal | -2.62417 | 0.07998 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty Pharma | 0.267044 | 0.9001 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty Private Bank | -2.62812 | 0.2603 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty PSU Bank | 5.73757 | 0.1096 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty PSE | 1.68098 | 0.562 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty Realty | -3.8324 | 0.3856 | 1 | Do not reject H0 | 12 |
| Nifty Infrastructure − Nifty Services Sector | 0.386627 | 0.7605 | 1 | Do not reject H0 | 12 |
| Nifty IT − Nifty Media | 0.271029 | 0.9762 | 1 | Do not reject H0 | 12 |
| Nifty IT − Nifty Metal | -7.34 | 0.1138 | 1 | Do not reject H0 | 12 |
| Nifty IT − Nifty Pharma | -4.44879 | 0.2661 | 1 | Do not reject H0 | 12 |
| Nifty IT − Nifty Private Bank | -7.34396 | 0.1601 | 1 | Do not reject H0 | 12 |
| Nifty IT − Nifty PSU Bank | 1.02174 | 0.8267 | 1 | Do not reject H0 | 12 |
| Nifty IT − Nifty PSE | -3.03485 | 0.5539 | 1 | Do not reject H0 | 12 |
| Nifty IT − Nifty Realty | -8.54823 | 0.2573 | 1 | Do not reject H0 | 12 |
| Nifty IT − Nifty Services Sector | -4.32921 | 0.2783 | 1 | Do not reject H0 | 12 |
| Nifty Media − Nifty Metal | -7.61103 | 0.301 | 1 | Do not reject H0 | 12 |
| Nifty Media − Nifty Pharma | -4.71982 | 0.4117 | 1 | Do not reject H0 | 12 |
| Nifty Media − Nifty Private Bank | -7.61499 | 0.1388 | 1 | Do not reject H0 | 12 |
| Nifty Media − Nifty PSU Bank | 0.750708 | 0.8829 | 1 | Do not reject H0 | 12 |
| Nifty Media − Nifty PSE | -3.30588 | 0.7074 | 1 | Do not reject H0 | 12 |
| Nifty Media − Nifty Realty | -8.81926 | 0.09693 | 1 | Do not reject H0 | 12 |
| Nifty Media − Nifty Services Sector | -4.60024 | 0.4833 | 1 | Do not reject H0 | 12 |
| Nifty Metal − Nifty Pharma | 2.89121 | 0.2973 | 1 | Do not reject H0 | 12 |
| Nifty Metal − Nifty Private Bank | -0.00395616 | 0.9991 | 1 | Do not reject H0 | 12 |
| Nifty Metal − Nifty PSU Bank | 8.36174 | 0.03199 | 1 | Do not reject H0 | 12 |
| Nifty Metal − Nifty PSE | 4.30515 | 0.02983 | 1 | Do not reject H0 | 12 |
| Nifty Metal − Nifty Realty | -1.20823 | 0.8319 | 1 | Do not reject H0 | 12 |
| Nifty Metal − Nifty Services Sector | 3.01079 | 0.2345 | 1 | Do not reject H0 | 12 |
| Nifty Pharma − Nifty Private Bank | -2.89517 | 0.2344 | 1 | Do not reject H0 | 12 |
| Nifty Pharma − Nifty PSU Bank | 5.47053 | 0.01473 | 1 | Do not reject H0 | 12 |
| Nifty Pharma − Nifty PSE | 1.41394 | 0.7402 | 1 | Do not reject H0 | 12 |
| Nifty Pharma − Nifty Realty | -4.09944 | 0.4031 | 1 | Do not reject H0 | 12 |
| Nifty Pharma − Nifty Services Sector | 0.119584 | 0.9525 | 1 | Do not reject H0 | 12 |
| Nifty Private Bank − Nifty PSU Bank | 8.36569 | 0.0226 | 1 | Do not reject H0 | 12 |
| Nifty Private Bank − Nifty PSE | 4.3091 | 0.407 | 1 | Do not reject H0 | 12 |
| Nifty Private Bank − Nifty Realty | -1.20428 | 0.6853 | 1 | Do not reject H0 | 12 |
| Nifty Private Bank − Nifty Services Sector | 3.01475 | 0.07765 | 1 | Do not reject H0 | 12 |
| Nifty PSU Bank − Nifty PSE | -4.05659 | 0.4548 | 1 | Do not reject H0 | 12 |
| Nifty PSU Bank − Nifty Realty | -9.56997 | 0.1175 | 1 | Do not reject H0 | 12 |
| Nifty PSU Bank − Nifty Services Sector | -5.35095 | 0.1555 | 1 | Do not reject H0 | 12 |
| Nifty PSE − Nifty Realty | -5.51338 | 0.4086 | 1 | Do not reject H0 | 12 |
| Nifty PSE − Nifty Services Sector | -1.29435 | 0.7373 | 1 | Do not reject H0 | 12 |
| Nifty Realty − Nifty Services Sector | 4.21903 | 0.2953 | 1 | Do not reject H0 | 12 |

**Pairwise Same Quarter Slope Tests Secondary**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | 1.01045 | 0.81 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Commodities | -1.34964 | 0.7719 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Energy | -3.86432 | 0.4013 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty FMCG | 1.5671 | 0.5498 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Financial Services | 2.38363 | 0.6024 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Infrastructure | 0.923006 | 0.7945 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty IT | 3.81265 | 0.2867 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Media | -5.14967 | 0.4222 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Metal | -3.74648 | 0.3996 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Pharma | -4.19339 | 0.1615 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Private Bank | 1.60898 | 0.7334 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty PSU Bank | -5.08697 | 0.2584 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty PSE | -1.20875 | 0.7174 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Realty | 2.5728 | 0.6199 | 1 | Do not reject H0 | 13 |
| Nifty Auto − Nifty Services Sector | 1.95672 | 0.5899 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Commodities | -2.36009 | 0.2364 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Energy | -4.87476 | 9.632e-05 | 0.01098 | Reject H0 | 13 |
| Nifty Bank − Nifty FMCG | 0.556653 | 0.8542 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Financial Services | 1.37319 | 0.1613 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Infrastructure | -0.0874413 | 0.938 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty IT | 2.80221 | 0.5619 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Media | -6.16012 | 0.08736 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Metal | -4.75693 | 0.01074 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Pharma | -5.20383 | 0.02401 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Private Bank | 0.598529 | 0.3438 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty PSU Bank | -6.09742 | 0.09084 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty PSE | -2.2192 | 0.3129 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Realty | 1.56235 | 0.8254 | 1 | Do not reject H0 | 13 |
| Nifty Bank − Nifty Services Sector | 0.946272 | 0.4571 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty Energy | -2.51467 | 0.08096 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty FMCG | 2.91674 | 0.2797 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty Financial Services | 3.73328 | 0.003828 | 0.4134 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty Infrastructure | 2.27265 | 0.2417 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty IT | 5.1623 | 0.3091 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty Media | -3.80003 | 0.404 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty Metal | -2.39684 | 2.375e-05 | 0.002731 | Reject H0 | 13 |
| Nifty Commodities − Nifty Pharma | -2.84374 | 0.2287 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty Private Bank | 2.95862 | 0.124 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty PSU Bank | -3.73733 | 0.403 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty PSE | 0.140891 | 0.9493 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty Realty | 3.92244 | 0.6449 | 1 | Do not reject H0 | 13 |
| Nifty Commodities − Nifty Services Sector | 3.30636 | 0.03313 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty FMCG | 5.43142 | 0.06859 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty Financial Services | 6.24795 | 1.871e-08 | 2.245e-06 | Reject H0 | 13 |
| Nifty Energy − Nifty Infrastructure | 4.78732 | 0.0004077 | 0.04566 | Reject H0 | 13 |
| Nifty Energy − Nifty IT | 7.67697 | 0.1192 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty Media | -1.28536 | 0.7285 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty Metal | 0.117837 | 0.9397 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty Pharma | -0.329069 | 0.8718 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty Private Bank | 5.47329 | 7.589e-06 | 0.0008955 | Reject H0 | 13 |
| Nifty Energy − Nifty PSU Bank | -1.22266 | 0.767 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty PSE | 2.65556 | 0.196 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty Realty | 6.43712 | 0.4013 | 1 | Do not reject H0 | 13 |
| Nifty Energy − Nifty Services Sector | 5.82104 | 8.907e-06 | 0.001042 | Reject H0 | 13 |
| Nifty FMCG − Nifty Financial Services | 0.816534 | 0.777 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty Infrastructure | -0.644094 | 0.8025 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty IT | 2.24555 | 0.597 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty Media | -6.71677 | 0.2257 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty Metal | -5.31358 | 0.03937 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty Pharma | -5.76049 | 0.0002182 | 0.02465 | Reject H0 | 13 |
| Nifty FMCG − Nifty Private Bank | 0.0418761 | 0.9899 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty PSU Bank | -6.65407 | 0.1762 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty PSE | -2.77585 | 0.2867 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty Realty | 1.0057 | 0.8881 | 1 | Do not reject H0 | 13 |
| Nifty FMCG − Nifty Services Sector | 0.38962 | 0.8588 | 1 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty Infrastructure | -1.46063 | 0.3719 | 1 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty IT | 1.42902 | 0.7881 | 1 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty Media | -7.53331 | 0.06568 | 1 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty Metal | -6.13011 | 7.638e-08 | 9.089e-06 | Reject H0 | 13 |
| Nifty Financial Services − Nifty Pharma | -6.57702 | 0.006767 | 0.7173 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty Private Bank | -0.774657 | 0.2873 | 1 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty PSU Bank | -7.47061 | 0.08287 | 1 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty PSE | -3.59239 | 0.1472 | 1 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty Realty | 0.189167 | 0.9809 | 1 | Do not reject H0 | 13 |
| Nifty Financial Services − Nifty Services Sector | -0.426914 | 0.7648 | 1 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty IT | 2.88965 | 0.4533 | 1 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty Media | -6.07268 | 0.1005 | 1 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty Metal | -4.66949 | 0.01432 | 1 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty Pharma | -5.11639 | 0.001095 | 0.1205 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty Private Bank | 0.68597 | 0.675 | 1 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty PSU Bank | -6.00998 | 0.04778 | 1 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty PSE | -2.13176 | 0.05665 | 1 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty Realty | 1.64979 | 0.8057 | 1 | Do not reject H0 | 13 |
| Nifty Infrastructure − Nifty Services Sector | 1.03371 | 0.1661 | 1 | Do not reject H0 | 13 |
| Nifty IT − Nifty Media | -8.96233 | 0.08376 | 1 | Do not reject H0 | 13 |
| Nifty IT − Nifty Metal | -7.55913 | 0.146 | 1 | Do not reject H0 | 13 |
| Nifty IT − Nifty Pharma | -8.00604 | 0.0284 | 1 | Do not reject H0 | 13 |
| Nifty IT − Nifty Private Bank | -2.20368 | 0.6815 | 1 | Do not reject H0 | 13 |
| Nifty IT − Nifty PSU Bank | -8.89963 | 0.005155 | 0.5516 | Do not reject H0 | 13 |
| Nifty IT − Nifty PSE | -5.02141 | 0.1197 | 1 | Do not reject H0 | 13 |
| Nifty IT − Nifty Realty | -1.23985 | 0.8431 | 1 | Do not reject H0 | 13 |
| Nifty IT − Nifty Services Sector | -1.85593 | 0.6356 | 1 | Do not reject H0 | 13 |
| Nifty Media − Nifty Metal | 1.40319 | 0.7681 | 1 | Do not reject H0 | 13 |
| Nifty Media − Nifty Pharma | 0.956289 | 0.8293 | 1 | Do not reject H0 | 13 |
| Nifty Media − Nifty Private Bank | 6.75865 | 0.06405 | 1 | Do not reject H0 | 13 |
| Nifty Media − Nifty PSU Bank | 0.062702 | 0.9869 | 1 | Do not reject H0 | 13 |
| Nifty Media − Nifty PSE | 3.94092 | 0.3537 | 1 | Do not reject H0 | 13 |
| Nifty Media − Nifty Realty | 7.72247 | 0.3364 | 1 | Do not reject H0 | 13 |
| Nifty Media − Nifty Services Sector | 7.10639 | 0.05972 | 1 | Do not reject H0 | 13 |
| Nifty Metal − Nifty Pharma | -0.446906 | 0.8491 | 1 | Do not reject H0 | 13 |
| Nifty Metal − Nifty Private Bank | 5.35546 | 0.002805 | 0.3058 | Do not reject H0 | 13 |
| Nifty Metal − Nifty PSU Bank | -1.34049 | 0.7649 | 1 | Do not reject H0 | 13 |
| Nifty Metal − Nifty PSE | 2.53773 | 0.2588 | 1 | Do not reject H0 | 13 |
| Nifty Metal − Nifty Realty | 6.31928 | 0.4464 | 1 | Do not reject H0 | 13 |
| Nifty Metal − Nifty Services Sector | 5.7032 | 0.0004139 | 0.04595 | Reject H0 | 13 |
| Nifty Pharma − Nifty Private Bank | 5.80236 | 0.02864 | 1 | Do not reject H0 | 13 |
| Nifty Pharma − Nifty PSU Bank | -0.893587 | 0.8247 | 1 | Do not reject H0 | 13 |
| Nifty Pharma − Nifty PSE | 2.98463 | 0.05836 | 1 | Do not reject H0 | 13 |
| Nifty Pharma − Nifty Realty | 6.76619 | 0.3084 | 1 | Do not reject H0 | 13 |
| Nifty Pharma − Nifty Services Sector | 6.15011 | 1.582e-05 | 0.001835 | Reject H0 | 13 |
| Nifty Private Bank − Nifty PSU Bank | -6.69595 | 0.1005 | 1 | Do not reject H0 | 13 |
| Nifty Private Bank − Nifty PSE | -2.81773 | 0.2865 | 1 | Do not reject H0 | 13 |
| Nifty Private Bank − Nifty Realty | 0.963824 | 0.8988 | 1 | Do not reject H0 | 13 |
| Nifty Private Bank − Nifty Services Sector | 0.347744 | 0.8335 | 1 | Do not reject H0 | 13 |
| Nifty PSU Bank − Nifty PSE | 3.87822 | 0.1849 | 1 | Do not reject H0 | 13 |
| Nifty PSU Bank − Nifty Realty | 7.65977 | 0.2347 | 1 | Do not reject H0 | 13 |
| Nifty PSU Bank − Nifty Services Sector | 7.04369 | 0.04124 | 1 | Do not reject H0 | 13 |
| Nifty PSE − Nifty Realty | 3.78155 | 0.577 | 1 | Do not reject H0 | 13 |
| Nifty PSE − Nifty Services Sector | 3.16547 | 0.02273 | 1 | Do not reject H0 | 13 |
| Nifty Realty − Nifty Services Sector | -0.61608 | 0.9315 | 1 | Do not reject H0 | 13 |

**Caveat:** GVA quarterly release timestamps are not supplied. Lagging by one quarter is only a conservative proxy; the precise information set cannot be established from the provided workbook.

**Caveat:** The supplied 2022-23-base GVA series contains only a short quarterly history, so YoY growth has a very small effective sample. Treat all H5 inference as exploratory and underpowered; do not splice the separate old-base-year workbook without a documented official linking method.

### H6 — Industrial production growth and index returns

**Null:** One-reference-month-lagged IIP YoY growth has zero linear association with monthly index returns; pairwise slopes equal across indices.

| Index | n | Focus coefficient | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |
|---|---:|---:|---|---:|---:|---|
| Nifty Auto | 91 | -0.0151484 | [-0.105611, 0.0753138] | 0.7428 | 1 | Do not reject H0 |
| Nifty Bank | 91 | 0.0359847 | [0.00583746, 0.0661319] | 0.01931 | 0.2897 | Do not reject H0 |
| Nifty Commodities | 91 | 0.00731722 | [-0.0636981, 0.0783326] | 0.84 | 1 | Do not reject H0 |
| Nifty Energy | 91 | 0.00393668 | [-0.0790389, 0.0869123] | 0.9259 | 1 | Do not reject H0 |
| Nifty FMCG | 91 | 0.0112832 | [-0.020427, 0.0429933] | 0.4856 | 1 | Do not reject H0 |
| Nifty Financial Services | 91 | 0.0335549 | [0.00747906, 0.0596307] | 0.01166 | 0.1866 | Do not reject H0 |
| Nifty Infrastructure | 91 | -0.00841658 | [-0.0751368, 0.0583037] | 0.8047 | 1 | Do not reject H0 |
| Nifty IT | 91 | 0.00390033 | [-0.0644838, 0.0722844] | 0.911 | 1 | Do not reject H0 |
| Nifty Media | 91 | 0.0283603 | [-0.092852, 0.149573] | 0.6465 | 1 | Do not reject H0 |
| Nifty Metal | 91 | -0.000621904 | [-0.0773891, 0.0761453] | 0.9873 | 1 | Do not reject H0 |
| Nifty Pharma | 91 | -0.0342951 | [-0.126433, 0.0578425] | 0.4657 | 1 | Do not reject H0 |
| Nifty Private Bank | 91 | 0.0241483 | [-0.00502993, 0.0533265] | 0.1048 | 1 | Do not reject H0 |
| Nifty PSU Bank | 91 | 0.0690641 | [-0.00119588, 0.139324] | 0.05403 | 0.7564 | Do not reject H0 |
| Nifty PSE | 91 | 0.0313025 | [-0.0302381, 0.0928432] | 0.3188 | 1 | Do not reject H0 |
| Nifty Realty | 91 | 0.00382188 | [-0.0724255, 0.0800693] | 0.9217 | 1 | Do not reject H0 |
| Nifty Services Sector | 91 | 0.019411 | [-0.00778334, 0.0466054] | 0.1618 | 1 | Do not reject H0 |

**Pairwise Lagged Growth Slope Tests**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | -0.0511331 | 0.2743 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Commodities | -0.0224656 | 0.1803 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Energy | -0.0190851 | 0.2299 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty FMCG | -0.0264316 | 0.4307 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Financial Services | -0.0487033 | 0.3131 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Infrastructure | -0.00673183 | 0.6917 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty IT | -0.0190487 | 0.4758 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Media | -0.0435087 | 0.07711 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Metal | -0.0145265 | 0.5042 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Pharma | 0.0191467 | 0.1098 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Private Bank | -0.0392967 | 0.4048 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty PSU Bank | -0.0842125 | 0.01708 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty PSE | -0.0464509 | 0.1448 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Realty | -0.0189703 | 0.5747 | 1 | Do not reject H0 | 91 |
| Nifty Auto − Nifty Services Sector | -0.0345594 | 0.3658 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Commodities | 0.0286675 | 0.4282 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Energy | 0.032048 | 0.4286 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty FMCG | 0.0247015 | 0.254 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Financial Services | 0.00242979 | 0.5545 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Infrastructure | 0.0444013 | 0.1959 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty IT | 0.0320843 | 0.3966 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Media | 0.00762435 | 0.9013 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Metal | 0.0366066 | 0.33 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Pharma | 0.0702798 | 0.1353 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Private Bank | 0.0118364 | 6.645e-07 | 7.974e-05 | Reject H0 | 91 |
| Nifty Bank − Nifty PSU Bank | -0.0330794 | 0.2394 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty PSE | 0.00468214 | 0.8712 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Realty | 0.0321628 | 0.3287 | 1 | Do not reject H0 | 91 |
| Nifty Bank − Nifty Services Sector | 0.0165736 | 0.1359 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Energy | 0.00338053 | 0.7411 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty FMCG | -0.00396594 | 0.8766 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Financial Services | -0.0262377 | 0.4864 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Infrastructure | 0.0157338 | 0.0139 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty IT | 0.00341689 | 0.8719 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Media | -0.0210431 | 0.5299 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Metal | 0.00793912 | 0.4792 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Pharma | 0.0416123 | 0.01032 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Private Bank | -0.0168311 | 0.6473 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty PSU Bank | -0.0617469 | 0.01605 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty PSE | -0.0239853 | 0.2079 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Realty | 0.00349534 | 0.8953 | 1 | Do not reject H0 | 91 |
| Nifty Commodities − Nifty Services Sector | -0.0120938 | 0.6599 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty FMCG | -0.00734648 | 0.8116 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty Financial Services | -0.0296182 | 0.4834 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty Infrastructure | 0.0123533 | 0.2289 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty IT | 3.63506e-05 | 0.9989 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty Media | -0.0244236 | 0.4294 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty Metal | 0.00455859 | 0.7939 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty Pharma | 0.0382318 | 0.02147 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty Private Bank | -0.0202116 | 0.6246 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty PSU Bank | -0.0651274 | 0.009677 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty PSE | -0.0273659 | 0.1829 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty Realty | 0.0001148 | 0.9961 | 1 | Do not reject H0 | 91 |
| Nifty Energy − Nifty Services Sector | -0.0154744 | 0.6318 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty Financial Services | -0.0222717 | 0.2859 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty Infrastructure | 0.0196997 | 0.378 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty IT | 0.00738283 | 0.7734 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty Media | -0.0170772 | 0.7261 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty Metal | 0.0119051 | 0.6985 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty Pharma | 0.0455782 | 0.2022 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty Private Bank | -0.0128651 | 0.5483 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty PSU Bank | -0.0577809 | 0.0729 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty PSE | -0.0200194 | 0.4362 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty Realty | 0.00746128 | 0.8074 | 1 | Do not reject H0 | 91 |
| Nifty FMCG − Nifty Services Sector | -0.00812788 | 0.5461 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty Infrastructure | 0.0419715 | 0.2393 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty IT | 0.0296545 | 0.4347 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty Media | 0.00519455 | 0.9341 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty Metal | 0.0341768 | 0.3865 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty Pharma | 0.06785 | 0.1637 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty Private Bank | 0.00940661 | 0.01092 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty PSU Bank | -0.0355092 | 0.2507 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty PSE | 0.00225235 | 0.9415 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty Realty | 0.029733 | 0.3921 | 1 | Do not reject H0 | 91 |
| Nifty Financial Services − Nifty Services Sector | 0.0141438 | 0.2088 | 1 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty IT | -0.0123169 | 0.5711 | 1 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty Media | -0.0367769 | 0.2766 | 1 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty Metal | -0.00779467 | 0.6196 | 1 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty Pharma | 0.0258785 | 0.1447 | 1 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty Private Bank | -0.0325648 | 0.3511 | 1 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty PSU Bank | -0.0774807 | 0.002092 | 0.2489 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty PSE | -0.0397191 | 0.02294 | 1 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty Realty | -0.0122385 | 0.6055 | 1 | Do not reject H0 | 91 |
| Nifty Infrastructure − Nifty Services Sector | -0.0278276 | 0.275 | 1 | Do not reject H0 | 91 |
| Nifty IT − Nifty Media | -0.02446 | 0.517 | 1 | Do not reject H0 | 91 |
| Nifty IT − Nifty Metal | 0.00452224 | 0.8665 | 1 | Do not reject H0 | 91 |
| Nifty IT − Nifty Pharma | 0.0381954 | 0.1608 | 1 | Do not reject H0 | 91 |
| Nifty IT − Nifty Private Bank | -0.0202479 | 0.5935 | 1 | Do not reject H0 | 91 |
| Nifty IT − Nifty PSU Bank | -0.0651638 | 0.06464 | 1 | Do not reject H0 | 91 |
| Nifty IT − Nifty PSE | -0.0274022 | 0.3778 | 1 | Do not reject H0 | 91 |
| Nifty IT − Nifty Realty | 7.84495e-05 | 0.9982 | 1 | Do not reject H0 | 91 |
| Nifty IT − Nifty Services Sector | -0.0155107 | 0.5696 | 1 | Do not reject H0 | 91 |
| Nifty Media − Nifty Metal | 0.0289822 | 0.4194 | 1 | Do not reject H0 | 91 |
| Nifty Media − Nifty Pharma | 0.0626554 | 0.01084 | 1 | Do not reject H0 | 91 |
| Nifty Media − Nifty Private Bank | 0.00421205 | 0.9453 | 1 | Do not reject H0 | 91 |
| Nifty Media − Nifty PSU Bank | -0.0407038 | 0.4165 | 1 | Do not reject H0 | 91 |
| Nifty Media − Nifty PSE | -0.00294221 | 0.9502 | 1 | Do not reject H0 | 91 |
| Nifty Media − Nifty Realty | 0.0245384 | 0.5562 | 1 | Do not reject H0 | 91 |
| Nifty Media − Nifty Services Sector | 0.00894929 | 0.8664 | 1 | Do not reject H0 | 91 |
| Nifty Metal − Nifty Pharma | 0.0336732 | 0.06944 | 1 | Do not reject H0 | 91 |
| Nifty Metal − Nifty Private Bank | -0.0247702 | 0.5153 | 1 | Do not reject H0 | 91 |
| Nifty Metal − Nifty PSU Bank | -0.069686 | 0.009102 | 1 | Do not reject H0 | 91 |
| Nifty Metal − Nifty PSE | -0.0319244 | 0.1511 | 1 | Do not reject H0 | 91 |
| Nifty Metal − Nifty Realty | -0.00444379 | 0.8832 | 1 | Do not reject H0 | 91 |
| Nifty Metal − Nifty Services Sector | -0.0200329 | 0.5112 | 1 | Do not reject H0 | 91 |
| Nifty Pharma − Nifty Private Bank | -0.0584434 | 0.2173 | 1 | Do not reject H0 | 91 |
| Nifty Pharma − Nifty PSU Bank | -0.103359 | 0.004018 | 0.4741 | Do not reject H0 | 91 |
| Nifty Pharma − Nifty PSE | -0.0655976 | 0.03531 | 1 | Do not reject H0 | 91 |
| Nifty Pharma − Nifty Realty | -0.038117 | 0.2523 | 1 | Do not reject H0 | 91 |
| Nifty Pharma − Nifty Services Sector | -0.0537061 | 0.165 | 1 | Do not reject H0 | 91 |
| Nifty Private Bank − Nifty PSU Bank | -0.0449158 | 0.1285 | 1 | Do not reject H0 | 91 |
| Nifty Private Bank − Nifty PSE | -0.00715426 | 0.8111 | 1 | Do not reject H0 | 91 |
| Nifty Private Bank − Nifty Realty | 0.0203264 | 0.5463 | 1 | Do not reject H0 | 91 |
| Nifty Private Bank − Nifty Services Sector | 0.00473723 | 0.6783 | 1 | Do not reject H0 | 91 |
| Nifty PSU Bank − Nifty PSE | 0.0377616 | 0.0246 | 1 | Do not reject H0 | 91 |
| Nifty PSU Bank − Nifty Realty | 0.0652422 | 0.005837 | 0.683 | Do not reject H0 | 91 |
| Nifty PSU Bank − Nifty Services Sector | 0.0496531 | 0.05072 | 1 | Do not reject H0 | 91 |
| Nifty PSE − Nifty Realty | 0.0274807 | 0.2025 | 1 | Do not reject H0 | 91 |
| Nifty PSE − Nifty Services Sector | 0.0118915 | 0.6094 | 1 | Do not reject H0 | 91 |
| Nifty Realty − Nifty Services Sector | -0.0155892 | 0.5783 | 1 | Do not reject H0 | 91 |

**Pairwise Same Month Slope Tests Secondary**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | -0.0643665 | 0.2122 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Commodities | -0.0597962 | 0.002665 | 0.3145 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Energy | -0.0122301 | 0.547 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty FMCG | -0.0793141 | 0.1466 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Financial Services | -0.0696046 | 0.1517 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Infrastructure | -0.0356325 | 0.1331 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty IT | -0.0668993 | 0.06188 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Media | -0.0563429 | 0.04878 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Metal | -0.124072 | 0.002031 | 0.2417 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Pharma | -0.042632 | 0.3302 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Private Bank | -0.0578342 | 0.1831 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty PSU Bank | -0.0550788 | 0.4875 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty PSE | -0.0627299 | 0.09829 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Realty | -0.0142576 | 0.821 | 1 | Do not reject H0 | 92 |
| Nifty Auto − Nifty Services Sector | -0.0664751 | 0.11 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Commodities | 0.00457029 | 0.9237 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Energy | 0.0521364 | 0.2614 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty FMCG | -0.0149476 | 0.3056 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Financial Services | -0.00523808 | 0.2912 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Infrastructure | 0.0287341 | 0.3731 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty IT | -0.00253277 | 0.9151 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Media | 0.00802363 | 0.8312 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Metal | -0.0597056 | 0.4564 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Pharma | 0.0217345 | 0.8133 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Private Bank | 0.00653236 | 0.4658 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty PSU Bank | 0.00928774 | 0.789 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty PSE | 0.00163667 | 0.9557 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Realty | 0.0501089 | 0.06826 | 1 | Do not reject H0 | 92 |
| Nifty Bank − Nifty Services Sector | -0.00210857 | 0.8587 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Energy | 0.0475661 | 1.029e-07 | 1.235e-05 | Reject H0 | 92 |
| Nifty Commodities − Nifty FMCG | -0.0195179 | 0.7121 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Financial Services | -0.00980837 | 0.828 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Infrastructure | 0.0241638 | 0.1933 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty IT | -0.00710307 | 0.8128 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Media | 0.00345334 | 0.896 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Metal | -0.0642759 | 0.06007 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Pharma | 0.0171642 | 0.7205 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Private Bank | 0.00196206 | 0.961 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty PSU Bank | 0.00471745 | 0.9483 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty PSE | -0.00293362 | 0.9203 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Realty | 0.0455387 | 0.4082 | 1 | Do not reject H0 | 92 |
| Nifty Commodities − Nifty Services Sector | -0.00667886 | 0.8587 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty FMCG | -0.067084 | 0.1939 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty Financial Services | -0.0573745 | 0.1934 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty Infrastructure | -0.0234023 | 0.1884 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty IT | -0.0546692 | 0.07247 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty Media | -0.0441128 | 0.1126 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty Metal | -0.111842 | 0.003277 | 0.3834 | Do not reject H0 | 92 |
| Nifty Energy − Nifty Pharma | -0.0304019 | 0.5537 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty Private Bank | -0.0456041 | 0.2462 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty PSU Bank | -0.0428487 | 0.5387 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty PSE | -0.0504997 | 0.04711 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty Realty | -0.00202747 | 0.969 | 1 | Do not reject H0 | 92 |
| Nifty Energy − Nifty Services Sector | -0.054245 | 0.1398 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty Financial Services | 0.00970951 | 0.4835 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty Infrastructure | 0.0436817 | 0.2254 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty IT | 0.0124148 | 0.655 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty Media | 0.0229712 | 0.5949 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty Metal | -0.0447581 | 0.603 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty Pharma | 0.0366821 | 0.7006 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty Private Bank | 0.0214799 | 0.2442 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty PSU Bank | 0.0242353 | 0.5313 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty PSE | 0.0165843 | 0.6301 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty Realty | 0.0650565 | 0.05111 | 1 | Do not reject H0 | 92 |
| Nifty FMCG − Nifty Services Sector | 0.012839 | 0.4757 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty Infrastructure | 0.0339722 | 0.2447 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty IT | 0.00270531 | 0.8979 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty Media | 0.0132617 | 0.711 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty Metal | -0.0544676 | 0.484 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty Pharma | 0.0269726 | 0.7611 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty Private Bank | 0.0117704 | 0.06901 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty PSU Bank | 0.0145258 | 0.7084 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty PSE | 0.00687475 | 0.8103 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty Realty | 0.055347 | 0.06949 | 1 | Do not reject H0 | 92 |
| Nifty Financial Services − Nifty Services Sector | 0.00312951 | 0.7092 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty IT | -0.0312669 | 0.06497 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty Media | -0.0207104 | 0.3843 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty Metal | -0.0884397 | 0.08915 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty Pharma | -0.00699954 | 0.9099 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty Private Bank | -0.0222017 | 0.3735 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty PSU Bank | -0.0194463 | 0.7427 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty PSE | -0.0270974 | 0.1511 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty Realty | 0.0213749 | 0.6224 | 1 | Do not reject H0 | 92 |
| Nifty Infrastructure − Nifty Services Sector | -0.0308426 | 0.1504 | 1 | Do not reject H0 | 92 |
| Nifty IT − Nifty Media | 0.0105564 | 0.668 | 1 | Do not reject H0 | 92 |
| Nifty IT − Nifty Metal | -0.0571729 | 0.3587 | 1 | Do not reject H0 | 92 |
| Nifty IT − Nifty Pharma | 0.0242673 | 0.7413 | 1 | Do not reject H0 | 92 |
| Nifty IT − Nifty Private Bank | 0.00906513 | 0.6181 | 1 | Do not reject H0 | 92 |
| Nifty IT − Nifty PSU Bank | 0.0118205 | 0.8163 | 1 | Do not reject H0 | 92 |
| Nifty IT − Nifty PSE | 0.00416945 | 0.8554 | 1 | Do not reject H0 | 92 |
| Nifty IT − Nifty Realty | 0.0526417 | 0.1517 | 1 | Do not reject H0 | 92 |
| Nifty IT − Nifty Services Sector | 0.000424204 | 0.9749 | 1 | Do not reject H0 | 92 |
| Nifty Media − Nifty Metal | -0.0677293 | 0.1848 | 1 | Do not reject H0 | 92 |
| Nifty Media − Nifty Pharma | 0.0137109 | 0.83 | 1 | Do not reject H0 | 92 |
| Nifty Media − Nifty Private Bank | -0.00149128 | 0.9611 | 1 | Do not reject H0 | 92 |
| Nifty Media − Nifty PSU Bank | 0.00126411 | 0.9839 | 1 | Do not reject H0 | 92 |
| Nifty Media − Nifty PSE | -0.00638696 | 0.8417 | 1 | Do not reject H0 | 92 |
| Nifty Media − Nifty Realty | 0.0420853 | 0.3706 | 1 | Do not reject H0 | 92 |
| Nifty Media − Nifty Services Sector | -0.0101322 | 0.7371 | 1 | Do not reject H0 | 92 |
| Nifty Metal − Nifty Pharma | 0.0814402 | 0.005273 | 0.6117 | Do not reject H0 | 92 |
| Nifty Metal − Nifty Private Bank | 0.066238 | 0.3593 | 1 | Do not reject H0 | 92 |
| Nifty Metal − Nifty PSU Bank | 0.0689934 | 0.5035 | 1 | Do not reject H0 | 92 |
| Nifty Metal − Nifty PSE | 0.0613423 | 0.3137 | 1 | Do not reject H0 | 92 |
| Nifty Metal − Nifty Realty | 0.109815 | 0.194 | 1 | Do not reject H0 | 92 |
| Nifty Metal − Nifty Services Sector | 0.0575971 | 0.4144 | 1 | Do not reject H0 | 92 |
| Nifty Pharma − Nifty Private Bank | -0.0152022 | 0.8555 | 1 | Do not reject H0 | 92 |
| Nifty Pharma − Nifty PSU Bank | -0.0124468 | 0.9168 | 1 | Do not reject H0 | 92 |
| Nifty Pharma − Nifty PSE | -0.0200979 | 0.7881 | 1 | Do not reject H0 | 92 |
| Nifty Pharma − Nifty Realty | 0.0283744 | 0.7794 | 1 | Do not reject H0 | 92 |
| Nifty Pharma − Nifty Services Sector | -0.0238431 | 0.7695 | 1 | Do not reject H0 | 92 |
| Nifty Private Bank − Nifty PSU Bank | 0.00275538 | 0.9481 | 1 | Do not reject H0 | 92 |
| Nifty Private Bank − Nifty PSE | -0.00489568 | 0.8505 | 1 | Do not reject H0 | 92 |
| Nifty Private Bank − Nifty Realty | 0.0435766 | 0.1704 | 1 | Do not reject H0 | 92 |
| Nifty Private Bank − Nifty Services Sector | -0.00864093 | 0.1852 | 1 | Do not reject H0 | 92 |
| Nifty PSU Bank − Nifty PSE | -0.00765107 | 0.8711 | 1 | Do not reject H0 | 92 |
| Nifty PSU Bank − Nifty Realty | 0.0408212 | 0.08151 | 1 | Do not reject H0 | 92 |
| Nifty PSU Bank − Nifty Services Sector | -0.0113963 | 0.7928 | 1 | Do not reject H0 | 92 |
| Nifty PSE − Nifty Realty | 0.0484723 | 0.1104 | 1 | Do not reject H0 | 92 |
| Nifty PSE − Nifty Services Sector | -0.00374524 | 0.8721 | 1 | Do not reject H0 | 92 |
| Nifty Realty − Nifty Services Sector | -0.0522175 | 0.1004 | 1 | Do not reject H0 | 92 |

**Caveat:** IIP source is the supplied macro-indicator workbook. Release timestamps and vintage/revision data are not supplied; lagged reference month is a timing proxy, not a real-time information-set test.

### H7 — Prior US-session S&P 500 returns and Indian index returns

**Null:** Prior S&P 500 return coefficient equals zero per index; paired alternative: sensitivity differs across indices.

| Index | n | Focus coefficient | 95% CI | Raw p | Holm p (sector family) | Decision after Holm |
|---|---:|---:|---|---:|---:|---|
| Nifty Auto | 2450 | 0.274255 | [0.15894, 0.38957] | 3.14e-06 | 3.454e-05 | Reject H0 |
| Nifty Bank | 2450 | 0.264773 | [0.130392, 0.399154] | 0.0001126 | 0.0005629 | Reject H0 |
| Nifty Commodities | 2450 | 0.270449 | [0.163396, 0.377503] | 7.366e-07 | 1.031e-05 | Reject H0 |
| Nifty Energy | 2450 | 0.224989 | [0.116626, 0.333352] | 4.714e-05 | 0.0004242 | Reject H0 |
| Nifty FMCG | 2450 | 0.135183 | [0.050992, 0.219374] | 0.001649 | 0.003298 | Reject H0 |
| Nifty Financial Services | 2450 | 0.27898 | [0.143043, 0.414916] | 5.761e-05 | 0.0004609 | Reject H0 |
| Nifty Infrastructure | 2450 | 0.224355 | [0.113429, 0.335281] | 7.366e-05 | 0.0004609 | Reject H0 |
| Nifty IT | 2450 | 0.354005 | [0.249395, 0.458616] | 3.299e-11 | 4.948e-10 | Reject H0 |
| Nifty Media | 2450 | 0.28216 | [0.210897, 0.353423] | 8.473e-15 | 1.356e-13 | Reject H0 |
| Nifty Metal | 2450 | 0.34668 | [0.204413, 0.488948] | 1.787e-06 | 2.324e-05 | Reject H0 |
| Nifty Pharma | 2450 | 0.156525 | [0.0575068, 0.255544] | 0.001947 | 0.003298 | Reject H0 |
| Nifty Private Bank | 2450 | 0.264424 | [0.126325, 0.402522] | 0.0001748 | 0.0006994 | Reject H0 |
| Nifty PSU Bank | 2450 | 0.217898 | [0.100233, 0.335564] | 0.0002839 | 0.0008518 | Reject H0 |
| Nifty PSE | 2450 | 0.19951 | [0.105643, 0.293378] | 3.103e-05 | 0.0003103 | Reject H0 |
| Nifty Realty | 2450 | 0.259856 | [0.132929, 0.386783] | 6.005e-05 | 0.0004609 | Reject H0 |
| Nifty Services Sector | 2450 | 0.285412 | [0.166367, 0.404457] | 2.614e-06 | 3.137e-05 | Reject H0 |

**Pairwise Slope Tests**

| Pair | Estimate | Raw p | Holm p | Decision | n |
|---|---:|---:|---:|---|---:|
| Nifty Auto − Nifty Bank | 0.0120847 | 0.674 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty Commodities | 0.0131007 | 0.4423 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty Energy | 0.0503535 | 0.02613 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty FMCG | 0.138612 | 3.911e-06 | 0.0004576 | Reject H0 | 2450 |
| Nifty Auto − Nifty Financial Services | 4.64099e-05 | 0.9988 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty Infrastructure | 0.0605566 | 0.000951 | 0.09224 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty IT | -0.0753766 | 0.02518 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty Media | -0.0102526 | 0.8463 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty Metal | -0.0589776 | 0.09099 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty Pharma | 0.114196 | 0.0004427 | 0.04564 | Reject H0 | 2450 |
| Nifty Auto − Nifty Private Bank | 0.00950256 | 0.7455 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty PSU Bank | 0.0585311 | 0.1112 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty PSE | 0.0731632 | 0.004325 | 0.3892 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty Realty | -0.00149951 | 0.9586 | 1 | Do not reject H0 | 2450 |
| Nifty Auto − Nifty Services Sector | 0.000343618 | 0.9883 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Commodities | -0.00109385 | 0.9662 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Energy | 0.0363313 | 0.1912 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty FMCG | 0.124326 | 0.001156 | 0.111 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Financial Services | -0.0114428 | 0.1698 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Infrastructure | 0.0471505 | 0.02814 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty IT | -0.0885162 | 0.04923 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Media | -0.0209104 | 0.7378 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Metal | -0.0715895 | 0.09121 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Pharma | 0.0993311 | 0.02693 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Private Bank | -0.00276633 | 0.5633 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty PSU Bank | 0.0462171 | 0.2511 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty PSE | 0.059696 | 0.09515 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Realty | -0.014555 | 0.6721 | 1 | Do not reject H0 | 2450 |
| Nifty Bank − Nifty Services Sector | -0.0126204 | 0.4157 | 1 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty Energy | 0.0371266 | 0.003561 | 0.324 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty FMCG | 0.126836 | 6.678e-06 | 0.0007746 | Reject H0 | 2450 |
| Nifty Commodities − Nifty Financial Services | -0.0117442 | 0.6684 | 1 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty Infrastructure | 0.0471113 | 0.000195 | 0.02106 | Reject H0 | 2450 |
| Nifty Commodities − Nifty IT | -0.0884889 | 0.005735 | 0.4991 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty Media | -0.0218442 | 0.6561 | 1 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty Metal | -0.0758034 | 0.007278 | 0.6259 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty Pharma | 0.100701 | 0.000905 | 0.08869 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty Private Bank | -0.0012203 | 0.9637 | 1 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty PSU Bank | 0.0447278 | 0.1463 | 1 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty PSE | 0.0603801 | 0.0004123 | 0.0433 | Reject H0 | 2450 |
| Nifty Commodities − Nifty Realty | -0.0144245 | 0.5562 | 1 | Do not reject H0 | 2450 |
| Nifty Commodities − Nifty Services Sector | -0.0126277 | 0.5238 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty FMCG | 0.0862711 | 0.001832 | 0.1722 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty Financial Services | -0.0489346 | 0.09103 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty Infrastructure | 0.0106592 | 0.4513 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty IT | -0.126001 | 0.0001702 | 0.01872 | Reject H0 | 2450 |
| Nifty Energy − Nifty Media | -0.0618372 | 0.2307 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty Metal | -0.113601 | 0.0006609 | 0.06741 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty Pharma | 0.0629137 | 0.03673 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty Private Bank | -0.0384602 | 0.1815 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty PSU Bank | 0.00780199 | 0.8179 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty PSE | 0.0216556 | 0.2007 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty Realty | -0.0521278 | 0.0562 | 1 | Do not reject H0 | 2450 |
| Nifty Energy − Nifty Services Sector | -0.0498465 | 0.01951 | 1 | Do not reject H0 | 2450 |
| Nifty FMCG − Nifty Financial Services | -0.137105 | 0.000859 | 0.08504 | Do not reject H0 | 2450 |
| Nifty FMCG − Nifty Infrastructure | -0.0792292 | 0.004555 | 0.4054 | Do not reject H0 | 2450 |
| Nifty FMCG − Nifty IT | -0.212526 | 2.138e-09 | 2.565e-07 | Reject H0 | 2450 |
| Nifty FMCG − Nifty Media | -0.150917 | 0.0003419 | 0.03658 | Reject H0 | 2450 |
| Nifty FMCG − Nifty Metal | -0.202209 | 5.164e-05 | 0.005836 | Reject H0 | 2450 |
| Nifty FMCG − Nifty Pharma | -0.0247672 | 0.3739 | 1 | Do not reject H0 | 2450 |
| Nifty FMCG − Nifty Private Bank | -0.12515 | 0.001206 | 0.1145 | Do not reject H0 | 2450 |
| Nifty FMCG − Nifty PSU Bank | -0.0813841 | 0.07328 | 1 | Do not reject H0 | 2450 |
| Nifty FMCG − Nifty PSE | -0.0648017 | 0.01985 | 1 | Do not reject H0 | 2450 |
| Nifty FMCG − Nifty Realty | -0.13556 | 0.0003908 | 0.04143 | Reject H0 | 2450 |
| Nifty FMCG − Nifty Services Sector | -0.138086 | 2.515e-05 | 0.002893 | Reject H0 | 2450 |
| Nifty Financial Services − Nifty Infrastructure | 0.059591 | 0.007634 | 0.6489 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty IT | -0.0762155 | 0.08974 | 1 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty Media | -0.00926159 | 0.8872 | 1 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty Metal | -0.0602473 | 0.1543 | 1 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty Pharma | 0.111881 | 0.01814 | 1 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty Private Bank | 0.00837825 | 0.4217 | 1 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty PSU Bank | 0.05772 | 0.154 | 1 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty PSE | 0.0717783 | 0.05175 | 1 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty Realty | -0.00271596 | 0.9363 | 1 | Do not reject H0 | 2450 |
| Nifty Financial Services − Nifty Services Sector | -3.11156e-05 | 0.9983 | 1 | Do not reject H0 | 2450 |
| Nifty Infrastructure − Nifty IT | -0.135627 | 7.641e-05 | 0.008482 | Reject H0 | 2450 |
| Nifty Infrastructure − Nifty Media | -0.0692832 | 0.1798 | 1 | Do not reject H0 | 2450 |
| Nifty Infrastructure − Nifty Metal | -0.122218 | 0.0004388 | 0.04564 | Reject H0 | 2450 |
| Nifty Infrastructure − Nifty Pharma | 0.05364 | 0.1014 | 1 | Do not reject H0 | 2450 |
| Nifty Infrastructure − Nifty Private Bank | -0.0495123 | 0.02916 | 1 | Do not reject H0 | 2450 |
| Nifty Infrastructure − Nifty PSU Bank | -0.00292157 | 0.9302 | 1 | Do not reject H0 | 2450 |
| Nifty Infrastructure − Nifty PSE | 0.0121163 | 0.5764 | 1 | Do not reject H0 | 2450 |
| Nifty Infrastructure − Nifty Realty | -0.0627288 | 0.01461 | 1 | Do not reject H0 | 2450 |
| Nifty Infrastructure − Nifty Services Sector | -0.0599451 | 0.0001871 | 0.02039 | Reject H0 | 2450 |
| Nifty IT − Nifty Media | 0.0646208 | 0.2607 | 1 | Do not reject H0 | 2450 |
| Nifty IT − Nifty Metal | 0.0145305 | 0.7196 | 1 | Do not reject H0 | 2450 |
| Nifty IT − Nifty Pharma | 0.189068 | 7.892e-09 | 9.392e-07 | Reject H0 | 2450 |
| Nifty IT − Nifty Private Bank | 0.0859249 | 0.06113 | 1 | Do not reject H0 | 2450 |
| Nifty IT − Nifty PSU Bank | 0.133977 | 0.000671 | 0.06777 | Do not reject H0 | 2450 |
| Nifty IT − Nifty PSE | 0.147914 | 1.042e-06 | 0.0001229 | Reject H0 | 2450 |
| Nifty IT − Nifty Realty | 0.0750031 | 0.02922 | 1 | Do not reject H0 | 2450 |
| Nifty IT − Nifty Services Sector | 0.075847 | 0.01542 | 1 | Do not reject H0 | 2450 |
| Nifty Media − Nifty Metal | -0.0584734 | 0.388 | 1 | Do not reject H0 | 2450 |
| Nifty Media − Nifty Pharma | 0.124483 | 0.01493 | 1 | Do not reject H0 | 2450 |
| Nifty Media − Nifty Private Bank | 0.0183868 | 0.7709 | 1 | Do not reject H0 | 2450 |
| Nifty Media − Nifty PSU Bank | 0.0639992 | 0.2664 | 1 | Do not reject H0 | 2450 |
| Nifty Media − Nifty PSE | 0.0839982 | 0.06335 | 1 | Do not reject H0 | 2450 |
| Nifty Media − Nifty Realty | 0.00148891 | 0.9788 | 1 | Do not reject H0 | 2450 |
| Nifty Media − Nifty Services Sector | 0.00922402 | 0.8755 | 1 | Do not reject H0 | 2450 |
| Nifty Metal − Nifty Pharma | 0.175614 | 3.708e-05 | 0.004227 | Reject H0 | 2450 |
| Nifty Metal − Nifty Private Bank | 0.0689261 | 0.1126 | 1 | Do not reject H0 | 2450 |
| Nifty Metal − Nifty PSU Bank | 0.118406 | 0.0008277 | 0.08277 | Do not reject H0 | 2450 |
| Nifty Metal − Nifty PSE | 0.140035 | 5.383e-05 | 0.006029 | Reject H0 | 2450 |
| Nifty Metal − Nifty Realty | 0.056583 | 0.08395 | 1 | Do not reject H0 | 2450 |
| Nifty Metal − Nifty Services Sector | 0.0602428 | 0.09028 | 1 | Do not reject H0 | 2450 |
| Nifty Pharma − Nifty Private Bank | -0.101666 | 0.02593 | 1 | Do not reject H0 | 2450 |
| Nifty Pharma − Nifty PSU Bank | -0.0555479 | 0.2131 | 1 | Do not reject H0 | 2450 |
| Nifty Pharma − Nifty PSE | -0.040883 | 0.1746 | 1 | Do not reject H0 | 2450 |
| Nifty Pharma − Nifty Realty | -0.114571 | 0.001963 | 0.1825 | Do not reject H0 | 2450 |
| Nifty Pharma − Nifty Services Sector | -0.112986 | 0.002279 | 0.2097 | Do not reject H0 | 2450 |
| Nifty Private Bank − Nifty PSU Bank | 0.0488604 | 0.2516 | 1 | Do not reject H0 | 2450 |
| Nifty Private Bank − Nifty PSE | 0.0617906 | 0.09357 | 1 | Do not reject H0 | 2450 |
| Nifty Private Bank − Nifty Realty | -0.0121759 | 0.7321 | 1 | Do not reject H0 | 2450 |
| Nifty Private Bank − Nifty Services Sector | -0.0098614 | 0.5603 | 1 | Do not reject H0 | 2450 |
| Nifty PSU Bank − Nifty PSE | 0.0171854 | 0.5491 | 1 | Do not reject H0 | 2450 |
| Nifty PSU Bank − Nifty Realty | -0.0620599 | 0.05066 | 1 | Do not reject H0 | 2450 |
| Nifty PSU Bank − Nifty Services Sector | -0.0577815 | 0.09245 | 1 | Do not reject H0 | 2450 |
| Nifty PSE − Nifty Realty | -0.0757996 | 0.005671 | 0.4991 | Do not reject H0 | 2450 |
| Nifty PSE − Nifty Services Sector | -0.0720206 | 0.008678 | 0.7289 | Do not reject H0 | 2450 |
| Nifty Realty − Nifty Services Sector | 0.00124098 | 0.9628 | 1 | Do not reject H0 | 2450 |

**Caveat:** The supplied S&P source is historical daily data; source/license and timezone conventions should be verified. Association is not causation or proof of a trading strategy.

## Multiple testing and interpretation

Holm family-wise error correction is applied to each set of per-index primary coefficient tests and to the eligible pairwise slope comparisons within each named family. Secondary lag/same-period specifications are corrected within their own per-index/pairwise families but the whole research suite still includes multiple families. P-values are not effect-size measures.

For H5, the small number of quarterly observations makes inference fragile even when the software reports a numerical p-value. This is not evidence that the hypothesis is proven or disproven.

## Reproducibility and output locations

- Clean macro data: `data/clean/macro/`.
- Per-index coefficients and pairwise slope comparisons: `reports/macro_hypotheses/hypothesis_results.json` and `.csv`.
- Per-hypothesis standalone JSON: `reports/macro_hypotheses/individual_hypotheses/`.
- Event CAR table: `reports/macro_hypotheses/h4_repo_event_car_by_index.csv`.
- CPI inflation derivation audit: `reports/macro_hypotheses/data_alignment_audit.json`.
- Macro charts: `reports/macro_hypotheses/figures/`.
- Cross-index EDA: `reports/comparative_eda_and_hypothesis_report.md` and `reports/figures/`.

## Data and research limitations

1. The supplied snapshot archive has a missing-date log, but its listed dates have not been independently reconciled against an official NSE trading-session calendar.
2. The source appears to be a price-return series; do not claim total shareholder returns unless the series definition confirms dividend reinvestment.
3. Sector and thematic indices can share underlying constituents and common market shocks; the paired difference design accounts for matched dates but does not make index universes independent.
4. Macroeconomic series are revised and publication times matter. The supplied workbooks do not provide consistent real-time vintages or release timestamps for CPI, GVA, IIP, reserves or FX.
5. Repo effective dates may differ from the public decision announcement timestamp; H4 is event-window exploration, not causal policy evaluation.
6. No transaction costs, dividends, portfolio weights, slippage or out-of-sample strategy tests are included.
7. This project is a reproducible statistical research workflow, not investment advice.
