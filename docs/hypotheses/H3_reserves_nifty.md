# H3 — Foreign-exchange reserves and weekly sector-index returns

## Research question

Are weekly FX-reserve changes associated with weekly returns after controlling for USD/INR movement? Do reserve sensitivities differ across the 16 sector/industry indices?

## Variables and method

Outcome: Friday-ending weekly return. Predictors: percentage change in weekly total FX reserves and percentage change in USD/INR. Each model uses OLS with HAC standard errors. Pairwise sensitivity tests model the weekly return difference on the same predictor/control set. A future-reserves lead diagnostic tests for timing/common-shock warnings.

## Hypotheses

Per index, H0: reserve coefficient is zero; H1: nonzero. For each pair, H0: reserve slopes are equal; H1: they differ. The models use two-sided tests and Holm correction within the respective families.

## Interpretation and caveats

A significant future-reserves lead is a warning about common shocks, serial dependence or timing—not evidence that future reserves cause current returns. The reserves workbook does not supply first public-release timestamps, so same-week joins are contemporaneous analysis rather than real-time forecasting.
