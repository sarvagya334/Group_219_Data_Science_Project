# H2 — CPI-derived inflation and monthly sector-index returns

## Research question

Is CPI-derived YoY inflation associated with monthly returns across the 16 primary sector/industry indices, and does estimated sensitivity differ by index?

## Inflation calculation

The primary rate is derived from the All-India Combined CPI General Index: `100 × (CPI_t / CPI_(t-12) - 1)`. The reported workbook rate is retained as a validation comparison. The results and derivation audit are in `reports/macro_hypotheses/`.

## Hypotheses and method

Per index, H0: coefficient on derived YoY inflation equals zero; H1: nonzero. Pairwise H0: two index slopes are equal; H1: slopes differ. Outcome is month-end-to-month-end return. Same-reference-month models are accompanied by a one-reference-month lag sensitivity. OLS/HAC is used; Holm correction is applied within the relevant family.

## Timing limitation

CPI reference-month dates are not release timestamps, and market expectations are unavailable. The same-month model is not a real-time predictive test or CPI-surprise study. The lagged-reference-month model is a sensitivity proxy, not proof of exact availability.
