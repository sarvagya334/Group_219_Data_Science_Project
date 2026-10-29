# H5 — Quarterly real GVA growth and sector-index returns

## Research question

Is real GVA growth associated with quarterly returns across the 16 primary indices, and do the lagged-GVA slopes differ across index pairs?

## Measure and method

Use the supplied GVA at Basic Prices, constant-price series on the 2022–23 base. YoY growth is `100 × (GVA_t / GVA_(t-4) - 1)`. The primary predictor is lagged one quarter; same-quarter growth is a secondary sensitivity. OLS with HAC standard errors is used, with Holm-adjusted pairwise slope-difference tests.

## Hypotheses and critical limitation

Per index, H0: coefficient on lagged GVA growth equals zero; H1: it is nonzero. For each pair, H0: slopes are equal; H1: slopes differ. The data yield only about 12 usable quarterly observations per primary model, so estimates are underpowered and highly uncertain. The workbook lacks release timestamps, and the 2022–23 base-year series is not mechanically spliced with older-base data.
