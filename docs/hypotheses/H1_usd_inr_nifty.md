# H1 — USD/INR changes and sector-index daily returns

## Research question

Are same-date USD/INR percentage changes associated with daily returns for the 16 primary sector/industry indices, and do the estimated sensitivities differ across index pairs?

## Variables and method

Outcome: index close-to-close simple return in percent. Predictor: percentage change in the supplied USD/INR series. Each index is fitted using OLS with Newey-West/HAC standard errors. The pairwise coefficient-difference test regresses `r_A - r_B` on the same FX predictor and tests its slope against zero; Holm correction is applied within the 120-pair family.

## Hypotheses

For each index, H0: the FX coefficient equals zero; H1: it is nonzero (two-sided, alpha 0.05). For each pair A/B, H0: their FX slopes are equal; H1: the slopes differ.

## Interpretation and caveats

Under the source quotation convention, a rise in rupees per US dollar indicates rupee depreciation. Same-date timing of the FX observation relative to Indian market close is not verified; this is contemporaneous association, not proven prediction or causation. The source workbook does not establish a real-time investor information set.
