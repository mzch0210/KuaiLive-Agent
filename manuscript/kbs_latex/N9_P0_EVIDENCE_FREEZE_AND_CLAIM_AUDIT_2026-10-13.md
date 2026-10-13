# N9-P0 | B1/B2 public-source evidence freeze and manuscript claim audit
Date: 2026-10-13. **Status: PUBLIC-SOURCE CLAIM REGISTER PASS; private row-level independent rehash PENDING**. No new scientific experiment and no frozen-TEST access.

## 1. Source freeze and inferential layers
| Evidence layer | Task/unit/cohort | Original authority | Editorial ownership |
| --- | --- | --- | --- |
| Prior prospective decision evidence | Twitch/LiveRec streamer, 44,221 held-out TEST events | `main.tex` (unchanged blob `40be249de52c0ae423b793c0dd4c55f2fdd69f46`) | §§6.1–6.2 |
| Prior prospective decision evidence | M3 author, 47,575 TEST events / 12,533 shared users, six Base fits | `experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md` | §§6.1–6.2, 6.5 |
| Already examined paired diagnostic | original KuaiLive room, 10,222 paired room TEST events | `main.tex` + original regime audit | §6.3; not M3 author replication |
| New exploratory mechanism | **M3 DEV author**, same 50,049 events / 12,628 users, single 20261012 Base seed per SASRec and GRU4Rec | B1 report, B2 report, B2 public JSON | §§5, 6.3–6.4 plus new supplemental evidence, never independent TEST |

Detailed claim–source–candidate–cohort–section register (38 entries):
`N9_P0_B1B2_CLAIM_SOURCE_COHORT_REGISTER_2026-10-13.csv`.
Each row records source Git blob, model, source arm, candidate regime, metric, interval where present, naturally realized calls and interpretation boundary.

## 2. B1 decision-support result ready for P1 drafting
Full-active F held-out nested DEV quality: SASRec S→F 0.296499 (14,988 Memory calls), F→F 0.302658 (15,016), adapted→F 0.301847 (14,954); GRU4Rec S→F 0.298123 (15,001), F→F 0.303093 (14,762), adapted→F 0.303000 (14,989). The F-aligned minus S-trained contrasts are +0.006159, 95% paired user CI [0.004835,0.007543] for SASRec and +0.004970 [0.003550,0.006369] for GRU4Rec. F-vs-S calls are **not exactly equal**. Adapted uses F-label supervision on outer-training DEV users and does not beat direct F→F. Five outer × four inner user-disjoint folds; 2,000 user-cluster bootstrap draws; DEV-only, post-G5 exploratory.

Scientific function: **candidate regime of knowledge-value supervision → quality of downstream fixed-source use on the same F author ranking events**. Do not describe sampled S as a prospective target-retained online generator or make a generic sampling-theory originality claim.

## 3. B2 source mechanism result ready for P1 drafting
Raw DEV NDCG@10 under F/S target-retained offline protocols: Full 0.343509/0.668498; Long-only 0.333231/0.773602; Short-only 0.273839/0.407506; popularity-only 0.022215/0.197796; history-placement placebo 0.007576/0.189571. Full versus Long order changes between F and S.

B2 12-feature nested decision transfer loss, F→F minus S→F: Full SASRec +0.006159 / GRU4Rec +0.004970, Long +0.010605 / +0.010262; Short +0.020694 / +0.020291 BUT this last contrast coincides with ~150–170 S-supervised calls versus ~14,800 F-supervised calls and **is not an equal-budget effect**. Popularity and weak placebo have near-zero calls and likely decision floor. In 6-feature candidate+Base-only panel, Full losses decrease to +0.001814/+0.001607; varying predictor information prevents an isolated causal attribution to relation descriptors. Original 12 feature set and six descriptor panel share cohort, not independent replications.

## 4. Claims eligible for journal prose
1. Fixed explicit relationship memory has **incumbent- and candidate-specific incremental ranking value**, tested in existing frozen results.
2. On a *post-G5 exploratory matched M3 DEV* study, F-aligned versus S-derived knowledge-value supervision leads to distinct held-out F choice quality with paired user intervals.
3. Knowledge-source composition changes ranking comparisons across candidate regimes, and relation-related pretarget features are implicated but not causally isolated.
4. Specified invocation-constrained decision support does not establish lower deployed cost. On original M3 TEST Always Memory still has higher NDCG, and separate warmed DEV replay is faster.

## 5. P0 rejection checks and open work
- **PASS on public-source reconciliation:** B1 and B2 source report Git blobs, cohort, candidate definitions, 5×4 GroupKFold, realized calls, intervals, and public machine aggregate have been read; B2 public per-arm full-memory values match B1 report to rounding.
- **PENDING private independent rehash:** private event CSVs, checkpoint files, complete model scores and row-level CI arrays are on a self-host research cache rather than exposed through the public GitHub connection; run A0 privacy-safe rehash when authorized self-host access is available, never infer hashes from a public summary.
- **NO new confirmatory family:** do not fold B1/B2 bootstrap intervals into G5 Holm corrections; the two studies use the **same** cohort.
- **SOURCE caveats:** full-versus-sampled changes candidate number *and* identities; retrospective target retention is for offline label calculation; history-placement placebo does not preserve full global user-author marginals; 6 features are **not** history-free in the Base representation.
- **Manuscript is still untouched:** these records authorize drafting, not claims that main TEX or S1–S9 has been updated.

## 6. P1 preparation contract
One main B1 downstream-decision table with all three arms, natural calls and user-paired contrasts, plus one compact B2 source-regime table with the Full/Long reversal; put full source × gate × feature panels, folds, limitations and source provenance in a coherent new supplemental section. Retain original frozen-test hierarchy and M3 Always Memory quality/cost counterevidence. All journal sentences must be about the *decision-support scientific question*, never a new selector algorithm.

Sources:
- https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md
- https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md
- https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/B2_NESTED_DEV_SOURCE_SPECIFICITY_AGGREGATE_2026-10-13.json
