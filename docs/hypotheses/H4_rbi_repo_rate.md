# H4 — RBI repo-rate effective-date event study across sector indices

## Research question

Do sector/industry index returns show nonzero three-session cumulative abnormal returns (CARs) around the supplied RBI repo-rate effective dates, and do paired event CARs differ by index?

## Event design

Map each supplied effective date to the first supplied index session on or after it. Estimate expected daily return from sessions `[t-120, t-21]`, requiring at least 80 observations. CAR is the sum of returns over `[t-1, t, t+1]` minus three times the estimation-window mean. The primary per-index test is a two-sided one-sample t-test of mean CAR equal to zero; paired event-CAR differences are tested across index pairs with Holm correction.

## Hypotheses and limitations

Per index, H0: mean CAR=0; H1: mean CAR is nonzero. Pairwise H0: mean CAR difference is zero; H1: it is nonzero. The effective dates are not verified public announcement timestamps and the source may not be a complete official MPC calendar. The benchmark is a simple pre-event mean, not a market model. This is exploratory event-window analysis, not a causal policy evaluation.
