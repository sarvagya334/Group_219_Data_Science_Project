# Sector-index source audit

- Snapshot files read: **2,652**
- All-index rows with valid positive close: **256,577**
- Distinct index names: **180**
- Unique snapshot dates: **2,652**
- Date range: **2016-01-01 to 2026-09-30**
- Missing-date log entries supplied with the archive: **152**
- Snapshot files whose internal date label differs from filename: **3**
- Encoded source-date mismatch rows: **318**
- Complete OHLC rows with invariant violations: **4**

## Primary sector-index universe

| Index | Observations | First date | Last date | Coverage fraction |
|---|---:|---|---|---:|
| Nifty Auto | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Bank | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Commodities | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Energy | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty FMCG | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Financial Services | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Infrastructure | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty IT | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Media | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Metal | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Pharma | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Private Bank | 2,650 | 2016-01-05 | 2026-09-30 | 99.925% |
| Nifty PSU Bank | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty PSE | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Realty | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |
| Nifty Services Sector | 2,652 | 2016-01-01 | 2026-09-30 | 100.000% |

## Important interpretation notes

- The archive includes 180 index series across sector, thematic, broad-market, factor/strategy, fixed-income and volatility families; it is not purely a sector-only archive.
- The source missing-date log lists dates absent from the snapshot collection; dates have not been independently compared with the official NSE session calendar.
- Three snapshot files have internal Index Date labels inconsistent with filenames. The filename date is used as the canonical date and the mismatches are retained in this audit.
- Index launch dates differ. The primary hypothesis universe uses long-history sector/industry indices; newer index series remain in the all-index panel and size audit but are not used in the primary models.
- Index-series values may represent price indices, total-return indices, strategy indices, debt indices or other index types. Their definitions should be checked before comparing performance across families.
