# N15 P0 — Scientific baseline, reviewer-risk register and protected evidence

**Established:** 2026-10-27. **Parent:** N14 draft PR #8, branch `kbs-n14-single-question-scope-reset-20261023`, commit `de73da5e62ee58c01337ecca69ec562411af08ee`. **N15 branch:** `kbs-n15-scientific-strengthening-20261027`.

**Historical status snapshot (2026-10-28, before P1-D authorization/execution):** P0 baseline/provenance retained; P1-A and P1-B exploratory DEV computations completed; P1-C desk-based estimand reconciliation completed in [N15_P1C_ESTIMAND_RECONCILIATION_AND_FEATURE_PANEL_DECISION_2026-10-28.md](N15_P1C_ESTIMAND_RECONCILIATION_AND_FEATURE_PANEL_DECISION_2026-10-28.md). P1-D was then **CONDITIONAL HOLD / NOT AUTHORIZED**. This preserves the pre-execution decision and is superseded only as to P1-D execution status by Section 9 below.

**Current status (verified 2026-10-28):** P1-D completed successfully as a narrow, aggregate-only exploratory DEV diagnostic on [Actions #40633996865](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40633996865); see [the result report](../../experiments/kbs_plan_c/N15_P1D_SIX_FEATURE_SOURCE_INTERACTION_RESULTS_2026-10-28.md). The six-feature result makes feature-panel dependence **OBSERVED / MATERIAL**; it does not establish a causal or invariant source mechanism. No further same-DEV quota/feature/source search is authorized. This remains an internally authored audit, not a real independent journal review. N14 and frozen original results remain unchanged; KBS originality remains HIGH-CONTESTABLE and P3/submission remain HOLD.

## 1. Scope and one testable question

Keep N14's **single question**. Candidate-regime supervision of an incumbent-relative historical relationship Memory value changes frozen full-active recommendation decisions and their ranking quality. N15 asks whether the **resource-matched decision consequence** survives and whether it has a **knowledge-source / candidate-competition boundary**. Do not add parallel headline RQs or claim a novel metric, selector, theoretical guarantee or measured production efficiency.

Fixed notation: `B` existing SASRec/GRU4Rec Base, `M` historical Short/Long/Popularity scorer, `Z` pretarget decision features, `C_S` original retrospective target-retained 575-item candidates, `C_F` full-active event-time candidates, `Delta_r=u_10(M; C_r)-u_10(B; C_r)`. `F/S` supervision schemes use different information and different DEV-calibrated thresholds; their existing B4-A comparison is a **complete-policy** contrast, not an isolated label intervention.

### New hypothesis for evaluation, NOT an established discovery

With the same **offline batch call quota** on identical full-F candidate requests, the F-supervised policy may achieve greater population-weighted full-F ranking quality than the originally tested uncorrected S-supervised policy. Under independently specified availability and capability constraints, the decision-loss differential may vary by candidate competition and knowledge-source support. Neither statement follows automatically from existing N14 results. A valid corrected sampled-only alternative remains an open competitor.

## 2. Exact inherited evidence ledger

| ID | Population / source | Frozen known result | Use in N15 | Forbidden extrapolation |
|---|---|---|---|---|
| D1 | Room, 10,222 paired events, original diagnostic | Memory−Base S −0.04120; F +0.04631; shift +0.08751; membership +0.08827, normalization −0.00076 | Context only | Not identical to M3 author-ranking; no isolated candidate-count mechanism |
| G5 | Original Author TEST, 47,575 requests / 12,533 users; six Base fits share cohort | SAS primary Base .258004, Utility .302866, Always Memory .346792; GRU Base .260033, Utility .304004 | Protected history | No independent new-period replication or test-time tuning |
| B1 | Exploratory Author DEV, 50,049 events / 12,628 users | SAS S→F .296499, F→F .302658; GRU .298123/.303093 | Mechanism + feasibility | Not a confirmatory held-out cohort |
| G2 | Same 50,049 DEV events | 10,672 SAS / 11,517 GRU requests switch; F-only 5,350/5,639 and S-only 5,322/5,878 | Prior decomposition, don't repeat | Not proportions of calls; not causal mediation |
| B4-A H1 | 30,000 distinct additional Author target IDs / 10,387 users, dates 2026-03-27..31, 20 stratum weights | SAS F−S +.005391 CI [.003646,.007174] Holm p .000600; GRU +.003585 CI [.001599,.005576] Holm p .000800 | Protected primary N14 result | Same recording period as G5; different user independence not assured |
| B4-A calls | Same 30,000 | SAS F 8704 / S 9105 (29.013% vs 30.350% raw); GRU F 8629 / S 9168 (28.763% vs 30.560% raw). Weighted F/S 29.203%/30.537% SAS, 29.008%/30.809% GRU | motivates new *matched-resource* estimand | Differences 1.337/1.797 raw pp exceed old ~1pp tolerance |
| Adverse | Same B4-A F eval; separate original DEV timed replay | Always Memory .348744 > both F policies .305446/.304530; old Utility 1.76941ms vs Always Memory .69165ms | Preserve in paper | Not positive production efficiency |
| B4-A H2 | 4096 event subset nested in B4-A | Historical true-minus-null +.031145 CI [.027389,.035098] Holm p .000600; original cohort TRAIN-only Popularity nonfloor prerequisite NOT VERIFIED | Retain original third Holm member as archive | No independent H2 validation; no isolated semantic mechanism |
| V2a/NI1g | Synthetic identification, 50,049 exploratory DEV, rank estimators | NO-GO for scientifically valid corrected-S policy with prior two candidates, V2b not run | Continue as open competitor | Never say all corrected-S fail |
| Rev3.1 | KuaiRec Big→Small audit | NO-GO, only 7/1411 optimistic repeated-author historical coverage | Reject this replication path | Not proof all external datasets fail |

The original 3-test Holm family cannot be rewritten after evidence revelation. Separate future N15 hypothesis family must be prospective.

## 3. Reviewer objection → evidentiary status → N15 action

| Risk | Severity | Available evidence | Unresolved alternative | New action | Exit gate |
|---|---|---|---|---|---|
| E1 originality beyond sampled evaluation + deferral | P0 | N14 policy consequence; N14 P6/P7 nearest prior art | unsurprising alignment of supervision and evaluation | Decision-focused, equal-quota allocation estimand; external source-specificity | One paragraph identifying a defensible incremental KBS insight; otherwise HIGH-CONTESTABLE retained |
| M1 unmatched policy calls | P0 | Original F/S B4-A frozen comparisons, N9 B1B DEV fairness audit | effective resource difference explains advantage | P1 exact common quota on new held-out predictions | Pre-locked same-resource rules; no revealed-TEST retune |
| M2 corrected-S comparator | P0 | NI1g NO-GO for explored candidates | mathematically legitimate sampled-only alternative | Method-only eligibility audit before any model training | signed assumptions/info contract; otherwise stop and disclose |
| E2 historical source specificity | P1 | B2 5-source DEV, N9 B1A source interaction, H2 composite null | generic ranker selector with weak/floor sources | Full-vs-Long source×supervision *decision* analysis | Adjust for base source competence and actual calls; no guaranteed monotonicity |
| S1 gate necessity and cost | P0 | Always Memory dominates accuracy; old Utility slower | hypothetical quota may lack practical meaning | resource legitimacy / optional timed F path if external need | Without real constraint, no deployment claim |
| E3 external transfer | P1 | same-period G5/B4-A and failed KuaiRec feasibility | cohort-specific effects | admissible new time/data gate | no replacement TEST without lawful temporal/roster/history reconstruction |
| M3 statistical dependency | P1 | 10,387 B4-A users vs G5 user overlap possible; 4096 nested | false cohort independence | explicit split/time/cluster ledger | prospective independent test family only |
| S3 rights/reproducibility | P0 submission | GitHub scripts/public aggregates; private event and model artifacts | outsider unable to recompute full user CI | versioned availability and rights register | human source-owner attestation required |

## 4. Prior-art boundary (verified 2026-10-27 via original publishers)

- Krichene & Rendle, KDD 2020, sampled metrics can reverse ranking comparisons and correction is known: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Subbiah, Rendle & Aggarwal, CIKM 2024, sampled rank correction for training WARP/LambdaRank: https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/
- Mao, Mohri & Zhong, ICML 2024, regression with multi-expert deferral (two-stage pretrained expert and costs): https://proceedings.mlr.press/v235/mao24d.html
- Zhong et al., KBS 2026, scene-aware memory discrimination, DOI 10.1016/j.knosys.2026.115496: https://www.sciencedirect.com/science/article/pii/S0950705126002388
- Existing project `N10_C1_KBS_NOVELTY_BOUNDARY_MATRIX_2026-10-14.md` additionally audits dynamic/knowledge gating; these are NOT first proposed here.

Novelty admissible only as a **bounded empirical/decision-design insight**, unless new methods and independent evidence justify a broader method contribution. Do not claim a first learned knowledge-use gate or first sampled ranking correction.

## 5. Rules for edits, results and peer review

1. Keep the original N13 archive and N14 core manuscript/target source blobs unchanged throughout P0/P1.
2. Add N15 new files only; no raw event IDs, user IDs, private weights, per-request features/labels exported to public repo.
3. Source all conclusions to exact experiment files. Existing DEV remains exploratory. No B4-A TEST threshold or stratum selection changes.
4. P1 score rank selection can be analyzed on DEV but cannot retroactively change original B4-A policy. Separate new dynamic budget or batch quota formulation from live serving claims.
5. No human peer review is represented as complete. All AI-assisted internal critique is labeled simulation.
6. Preserve source-level audits, same-commit PDF and old H2 third Holm member if a future manuscript is revised.
7. Data/legal publication rights, author declarations and COI remain human owner signoff gates.

## 6. N15 P0 research status at creation

- Baseline N14 head: confirmed `de73da5e62ee58c01337ecca69ec562411af08ee`; PR #8 draft, N14 not merged.
- N14 primary numeric source and NI1g, N9 B1B and G2 audited read-only.
- New N15 branch created from N14 head with NO changes to protected original experiments.
- This document does not assert new equal-budget NDCG or new replication.


## 7. 2026-10-28 decision addendum — after N15 P1-A/P1-B

- P1-A exact-call offline batch allocation: exploratory DEV result PASS; F−S +0.006133 SASRec and +0.005398 GRU4Rec at q=.30, with 15,014 calls per arm. This is a new estimand, not a revision of B4-A H1.
- P1-B Full-vs-Long interaction: exploratory DEV result PASS under the 12-feature panel; I(0.30)=−0.005047 SASRec and −0.004893 GRU4Rec. The feature-panel dependence highlighted by the prior B2 six-feature threshold-policy analysis is now a primary open interpretation risk.
- P1-C reconciliation: completed as desk analysis only. No private rows were read, no models refit, no TEST opened, and no new empirical estimate created.
- Revised next step: first decide whether source specificity is essential to the KBS contribution. Only if yes, and all rights/source/protocol gates pass, consider one q=.30 six-feature exact-quota diagnostic. Otherwise stop further reused-DEV experimentation.
- N14's three-member Holm family, original H1/H2 values, manuscript and archived research sources remain immutable. No corrected-S universal impossibility claim; no production cost/latency claim; no independent replication claim.


## 8. Initial 2026-10-28 P2 novelty reassessment and P1-D admission decision (historical; superseded for P1-D execution only)

See [N15_P2_NOVELTY_REASSESSMENT_AND_P1D_ADMISSION_DECISION_2026-10-28.md](N15_P2_NOVELTY_REASSESSMENT_AND_P1D_ADMISSION_DECISION_2026-10-28.md). At the time of the initial review, source-specificity was judged essential to the intended KBS positioning but unproven, and P1-D was **NO-GO** because explicit source-owner/data-rights authorization was not documented in the project record. That historical gate is retained as decision provenance. A later narrow user confirmation authorized the internal diagnostic only; the run then completed successfully as recorded in Section 9. This does not establish public redistribution permission or general legal clearance. KBS originality remains HIGH-CONTESTABLE and submission remains HOLD.


## 9. 2026-10-28 P1-D result adjudication

P1-D passed on Actions run [#40633996865](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40633996865); aggregate-only result: [N15_P1D_SIX_FEATURE_SOURCE_INTERACTION_RESULTS_2026-10-28.md](../../experiments/kbs_plan_c/N15_P1D_SIX_FEATURE_SOURCE_INTERACTION_RESULTS_2026-10-28.md). At q=.30, SASRec I=+0.001676476 (descriptive user-cluster 95% interval [+0.000152109,+0.003104834]); GRU4Rec I=−0.000478588 (interval [−0.001899109,+0.000884844]). Against P1-B's 12-feature negative interactions, this is evidence that the source interaction is feature-panel conditional in this reused-DEV offline batch setting. It is not a formal panel-by-source test, causal explanation, or independent replication. No additional DEV panel/quota search is authorized; P3 and submission remain HOLD.
