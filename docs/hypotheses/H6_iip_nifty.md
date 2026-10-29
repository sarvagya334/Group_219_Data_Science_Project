# H6 — Industrial production growth and monthly sector-index returns

## Research question

Is industrial production growth associated with monthly returns across the 16 primary indices, and do its estimated slopes differ?

## Variable and method

Derive IIP YoY growth as `100 × (IIP_t / IIP_(t-12) - 1)` from the Monthly sheet in `50 Macroeconomic Indicators.xlsx`. The primary predictor is lagged one reference month; same-month models are secondary. OLS with HAC standard errors is used, and pairwise slope comparisons receive Holm correction.

## Hypotheses and caveats

Per index, H0: lagged IIP-growth coefficient equals zero; H1: it is nonzero. Per pair, H0: slopes are equal; H1: unequal. Release timestamps, data vintages and revision histories are not supplied, so the lag is a timing proxy. Results are associations, not a causal claim.
