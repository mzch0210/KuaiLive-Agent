# Supplementary S10 (draft) — Matched DEV candidate-regime supervision and relationship-source decision analysis

**Draft prepared 2026-10-13; not yet assembled into canonical S1–S9 or submitted as independent TEST.** This section is journal-style scientific support for the two proposed main-text N9-P1 tables. Its numerical results come from existing post-G5 exploratory DEV audits; private row-level verification and manuscript integration remain pending.

## S10.1 Experimental cohort, ranking unit and comparison target

Both B1 and B2 use the **same 50,049 KuaiLive-M3 DEV events from 12,628 user clusters**, with author (persistent creator) as the ranking unit. The incumbent rankers are one frozen SASRec primary seed and one frozen GRU4Rec primary seed, each trained before these analyses. The Memory specialist is the fixed corrected all-prior-history Short/Long/Popularity ranker, not a jointly retrained auxiliary neural model. All policies target the ranking of eligible TRAIN-known active authors at event time.

Let F denote the full-active ranking-candidate regime; let S denote a deterministic **575 target-retained sampled** retrospective evaluation regime. A sampled observation retains the subsequently observed author only in the offline calculation of `u_10` labels; target retention is not an observable decision-time feature, not an online generation procedure, and not a justification for assigning realized target information to a gate.

Define `Delta_r(x)=u_10(M,x;r)-u_10(B,x;r)` for r in {S,F}. B1 estimates separate selectors trained from either Delta_S or Delta_F and compares their decisions on held-out F examples. The main exploratory contrast is `V_F(pi_F)-V_F(pi_S)`, conditional on each estimated policy's **naturally realized calls**. Candidate membership changes number, identity and competition jointly; no isolated candidate-count causal effect is claimed.

## S10.2 Nested fitting, frozen selection and statistical scope

Use **5 outer GroupKFold splits by user** and **4 inner GroupKFold splits** on each outer training partition, with no user shared across fit and validation folds. Predictors are fixed twelve pretarget features consisting of seven history/candidate descriptors and five Base-score summaries. Each model is `HistGradientBoostingRegressor`, with 120 iterations, learning rate 0.05, max depth 3, minimum leaf 50, L2 1, no early stopping. Inner out-of-fold predictions determine a single pointwise score threshold under the original at-most-30%-of-inner-DEV invocation target, with indivisible score ties. Outer subjects are only scored after calibration and are not used to pick a retrospective best threshold or match outer call counts.

The pure S→F arm fits to Delta_S and calibrates only with S supervision, then evaluates on outer F. The F→F arm fits and calibrates on F labels from outer-training users. The regime-adapted→F arm includes S and F labels and regime descriptors during outer-training, calibrates on F inner labels, and **has access to F supervision**; it is neither label-free adaptation nor an improvement beyond native F→F.

Use 2,000 paired user-cluster percentile bootstrap draws for descriptive 95% intervals. Five outer folds on this one cohort are not five independent prospective TEST cohorts. All B1/B2 arm choices were devised after original G5 outcome review; these confidence intervals do not enter the frozen G5 registered Holm testing family. Original G5 TEST remains unopened for these analyses.

## S10.3 Candidate supervision, full-ranking policy utility

| Incumbent | S→F NDCG@10; calls | F→F NDCG@10; calls | Adapted→F NDCG@10; calls | F→F − S→F (paired 95% user CI) |
| --- | --- | --- | --- | --- |
| SASRec | 0.296499; 14,988 | 0.302658; 15,016 | 0.301847; 14,954 | 0.006159 [0.004835, 0.007543] |
| GRU4Rec | 0.298123; 15,001 | 0.303093; 14,762 | 0.303000; 14,989 | 0.004970 [0.003550, 0.006369] |

The F-aligned rule improves quality relative to S supervision in both incumbent families under their observed invocation rates. Adapted-to-F does not exceed native F→F; its training includes the full-supervision information that is unavailable to a pure S-trained policy. The absolute reference NDCG@10 for Always Memory on these full-active DEV events is 0.343509, above these selectors; the result supports the decision relevance of candidate-aligned valuation **under a stipulated invocation rule**, not unconditional or latency superiority.

## S10.4 Five knowledge sources and candidate-regime comparisons

The specialist source conditions are: the fixed full 0.45 Short + 0.45 Long + 0.10 popularity mixture, Long-only, Short-only, training-only popularity, and a deliberately broken within-event historical-score placement placebo. The original mixture was not retuned. Under F, Full Memory yields 0.343509 NDCG@10 versus Long-only 0.333231; under S, Full yields 0.668498 versus Long-only 0.773602. The source ordering reverses. Short-only obtains 0.273839 F and 0.407506 S, popularity-only 0.022215 F and 0.197796 S, and placement placebo 0.007576 F and 0.189571 S.

This demonstrates source-dependent evaluation differences on fixed historical score constructions. The placebo is not a globally margin-preserving history randomization. Extremely weak controls cannot isolate the specific contribution of correct viewer--creator identity when selectors almost never choose those experts.

## S10.5 Source-dependent selection transfer and information availability

For original twelve-feature selectors, full-candidate aligned-minus-sampled-trained decision-quality differences were:

| Memory source | SASRec difference | GRU4Rec difference | Interpretation |
| --- | ---: | ---: | --- |
| Full | 0.006159 | 0.004970 | Matched users, similar but nonidentical calls |
| Long-only | 0.010605 | 0.010262 | Larger transfer penalty than Full under this feature panel |
| Short-only | 0.020694 | 0.020291 | Strong call-rate shift confounds same-budget interpretation |
| Popularity-only | 0.000000 | 0.000010 | Near-zero invocation floor |
| Relationship shifted | 0.000020 | 0.000014 | Very weak source; near-zero invocation floor |

In the Short-only condition, SASRec S→F invokes Memory 171 times and F→F 14,766 times; GRU4Rec corresponding calls are 141 and 14,851. These raw contrasts must **not** be described as equal-budget causal decision regret.

To probe whether direct relation-history descriptors affect transfer, the same experiments were repeated with just six pretarget features (candidate-count summary plus five Base-score descriptors), rather than the original twelve. For Full Memory the transferred-policy difference falls to 0.001814 SASRec and 0.001607 GRU4Rec, compared with 0.006159 and 0.004970 under twelve features. The six-feature control is not literally history-free: Base score representations still encode user behavioral history; reducing feature dimension and richness can also affect approximation. The contrast identifies a conditional **information dependence**, not a single isolated causal relationship-history channel.

## S10.6 Reproducibility record and interpretation boundaries

B1 source reports completed runs `38364829652` (paired F/S DEV source) and `38365477972` (nested policy transfer); private paired DEV CSV SHA256 recorded in the B1 report as `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`. B2 identifies run `38369503457` as the completed digest-verified nested source study, with public aggregate `B2_NESTED_DEV_SOURCE_SPECIFICITY_AGGREGATE_2026-10-13.json`. Per-event identifiers and model scores remain private. Public artifacts and report digests aid provenance but do not substitute for independently reviewing local private source data before final submission.

The inferential hierarchy of this manuscript is unchanged: original frozen Twitch/M3 TEST results remain the principal independent decision tests, the original 10,222-room sampled/full comparison is a retrospective diagnostic, and these B1/B2 **same-cohort post-G5 DEV** analyses provide exploratory mechanistic support. No prediction-time target identity, deployed production saving, generic learning-to-defer priority, or six independent TEST repetitions is inferred.

Sources: `experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md`, `experiments/kbs_plan_c/B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md`, `experiments/kbs_plan_c/B2_NESTED_DEV_SOURCE_SPECIFICITY_AGGREGATE_2026-10-13.json`. Existing sampling-metric precedent: Krichene and Rendle, KDD 2020, https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ .
