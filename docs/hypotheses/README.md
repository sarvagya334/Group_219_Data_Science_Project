# Hypothesis specifications — sector/industry-index study

Each hypothesis is run across the same 16 primary long-history sector/industry indices in `config/sector_universe.json`, using common index outcome definitions and the supplied macroeconomic source files.

- [H1 — USD/INR and daily index returns](H1_usd_inr_nifty.md)
- [H2 — CPI-derived inflation and monthly returns](H2_cpi_nifty.md)
- [H3 — FX reserves and weekly returns](H3_reserves_nifty.md)
- [H4 — RBI repo-rate event study](H4_rbi_repo_rate.md)
- [H5 — GVA growth and quarterly returns](H5_gva_nifty.md)
- [H6 — IIP growth and monthly returns](H6_iip_nifty.md)
- [H7 — Prior US-session S&P 500 return](H7_us_spillover.md)

## Shared inference conventions

Continuous-predictor models use OLS with Newey-West/HAC standard errors. Direct sensitivity comparisons use paired return differences, not comparisons of separate p-values. Holm correction is applied to the per-index tests and pairwise tests within each named family (up to 120 index pairs in the 16-index universe). Secondary lag/reference-period variants have their own stated tests. The full research suite contains multiple families, so within-family Holm correction does not remove all multiple-testing concerns. Results are observational associations, not causal estimates.
