# Plan C G1 — DEV-only active warm-author feasibility PASS

**Source**: [successful workflow #38204794887](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38204794887), artifact ID `11726458631` (`availability.json`). Both hosted synthetic interval/author-identity unit test and User-host 6.537M-room sweep succeeded. An earlier attempt [#38204702979](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38204702979) failed because the analyzer expected `start_ts/end_ts`, whereas the actual frozen G1 room Parquet schema uses `open_ts/close_ts`; this was corrected before these statistics.

## Scope

- **Only DEV**, using 512 fixed evenly spaced rank-order timestamps chosen from the frozen 50,049-event DEV panel; never accesses a TEST event or ranking metric.
- A candidate is a **distinct author seen in eligible TRAIN** for whom ≥1 room is active at the sampled timestamp under the half-open interval convention.
- In this dataset's sampled DEV windows, the observed active room count happens to equal the active distinct warm-author count at each sampled clock instant; do **not** assume equality elsewhere without validation.
- The script exports only aggregate counts, not author or room IDs.

## Author-level active candidates

| Statistic | Active train-known authors |
|---|---:|
| Evaluated DEV timestamps | **512** |
| Minimum | **14,422** |
| 10th percentile | **23,948** |
| Median | **33,751** |
| 90th percentile | **50,901** |
| Maximum | **53,752** |
| Sampled timestamps with fewer than 575 authors | **0** |

The full eligible-room input contains **6,537,125** room intervals, all scanned. Run time **21.2 seconds** using CPU and an isolated Parquet reader. The warm author universe is **897,025** TRAIN-seen authors.

## Decision

**Full-active, warm-author ranking remains computationally feasible for the pre-registered 50,049 DEV / 47,575 sealed TEST samples.** At approximately 33,751 author candidates per typical event, one full DEV scoring pass corresponds to ~1.7 billion event–author scores; use batched GPU matrix products, shared fixed Memory scores and cache reuse. This is a planning approximation, not an observed training time or a speed benchmark.

A secondary 575-candidate sampled-active regime is structurally feasible on all 512 audited DEV timestamps, but cannot be called an identical distribution to full-active. It must be treated as a candidate-regime sensitivity and scored with the same per-event pair and candidate membership under both Base and Memory.

Next tasks: implement/train Base SASRec/GRU4Rec on **TRAIN only**, produce aligned DEV scores and DEV gate OOF policies, freeze all comparator checkpoints and thresholds, then perform one-shot sealed TEST. E1/E2/E3 TEST performance remains **unobserved**.
