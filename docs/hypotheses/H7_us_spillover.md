# H7 — Prior US-session S&P 500 returns and sector-index returns

## Research question

Are returns in the most recent completed US session associated with each Indian sector-index return, after controlling for its own lagged return, and do the estimated US-return sensitivities differ?

## Alignment and model

Calculate S&P 500 close-to-close percentage returns. For Indian session date `t`, align the latest S&P 500 observation strictly earlier than `t` using backward as-of matching with exact matches disabled. Regress each Indian daily return on this prior US-session return and the same index's own previous return. For paired slope comparisons, use the paired difference in Indian returns and the difference in their own-lag controls.

## Hypotheses and caveats

Per index, H0: coefficient on prior S&P 500 return equals zero; H1: nonzero. Per pair, H0: the two coefficients are equal; H1: they differ. Use OLS/HAC and Holm correction within the family. Confirm S&P source license, timezone and adjusted-close convention. A lagged association is not causality or evidence of a profitable strategy; no transaction costs or out-of-sample strategy tests are included.
