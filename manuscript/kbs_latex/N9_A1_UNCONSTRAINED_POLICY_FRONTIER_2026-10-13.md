# N9-A1 — DEV decision-support quality across invocation constraints

**2026-10-13 | PASS | Post-G5 exploratory DEV only.** Successful [self-host run #38382693869](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38382693869); the inline scientific source was checked against Git blob SHA before execution. The private B1 DEV source was independently rehashed. Frozen G5 TEST and prior manuscript were not read or edited.

## Method

Same **50,049 M3 DEV author events / 12,628 users**, one frozen SASRec and one frozen GRU4Rec primary seed, same twelve pre-outcome descriptors and 5 outer × 4 inner user-disjoint GroupKFold design as B1. HistGradientBoostingRegressor settings match B1; inner OOF thresholds maximize observed incremental F-ranking NDCG under predeclared inner maximum Memory-call rates of 0/10/20/30/50/70/90/100%. The 100% condition is an **unrestricted learned policy**, not Always Memory. No outer-F target is used for threshold/model choice. Realized outer calls are **not** strictly equal to inner limits. Two thousand paired user-bootstrap replicates provide descriptive CI; not an added G5 inferential family.

## Results: all policies evaluated under F full-active candidates

| Calibrated maximum | SASRec calls / observed rate | SASRec NDCG@10 | GRU4Rec calls / observed rate | GRU4Rec NDCG@10 |
|---:|---:|---:|---:|---:|
| 0% | 0 / 0.00% | 0.258167 | 0 / 0.00% | 0.258971 |
| 10% | 5001 / 9.99% | 0.278263 | 5006 / 10.00% | 0.279025 |
| 20% | 9946 / 19.87% | 0.291381 | 9904 / 19.79% | 0.292962 |
| 30% | 15016 / 30.00% | 0.302658 | 14762 / 29.50% | 0.303093 |
| 50% | 25081 / 50.11% | 0.319654 | 25230 / 50.41% | 0.320478 |
| 70% | 34980 / 69.89% | 0.332695 | 34831 / 69.59% | 0.332078 |
| 90% | 44768 / 89.45% | 0.341040 | 45164 / 90.24% | 0.341051 |
| 100% | 50006 / 99.91% | 0.343495 | 49770 / 99.44% | 0.343363 |

Original fixed references: SASRec Always Base 0.258167, GRU4Rec Always Base 0.258971, both Always Memory 0.343509. **The original B1 F→F 30% arm was exactly replicated:** SASRec 0.302658, 15,016 calls; GRU4Rec 0.303093, 14,762 calls (same inner user splits, source, model, threshold logic).

At an unconstrained 100% inner cap the policy calls Memory on 50006 (99.91%) SASRec events and 49770 (99.44%) GRU4Rec events. Its NDCG@10 becomes 0.343495 / 0.343363, both slightly **below Always Memory 0.343509**. Relative to the 30% rule, this unrestricted threshold policy increases NDCG by 0.040837 (SASRec, user CI [0.038750, 0.042806]) and 0.040270 (GRU4Rec, CI [0.038163, 0.042302]). These differences compare policies with very different naturally realized calls, not equal-cost effects.

## Scientific interpretation

**R2 strengthened with a precise condition:** estimated marginal value has measurable value as a *choice signal under an explicit specialist-invocation restriction*. In the M3 author task, removing this restriction causes the learner to select Memory for almost all cases without beating always-on Memory. Therefore any real-world benefit from restricting specialist use requires independent access/cost/permission evidence; a reduction of abstract Memory invocations is **not** a measured production saving. This evidence refines the decision-support contribution rather than elevating an algorithm-novelty claim.

**R1:** A1 does not establish originality beyond existing decision/deferral approaches; retain scoped scientific distinction pending strong alternatives and knowledge-source controls. **R3:** B1/B2 source × candidate × decision mechanisms stand as exploratory, nonindependent same-cohort evidence. Do not promote A1 as fresh independent TEST.

## Source / provenance

- `analysis/kbs_plan_c/n9_a1_decision_support_frontier_dev.py`
- `.github/workflows/kbs-n9-a1-decision-frontier-dev.yml`
- `experiments/kbs_plan_c/N9_A1_DECISION_FRONTIER_PUBLIC_AGGREGATE_2026-10-13.json`
- Private full fold/interval summary remains on the authorized runner at `klm3_n9_a1_frontier_seed20261012_v1/summary.json`; only aggregate results are reproduced here.
