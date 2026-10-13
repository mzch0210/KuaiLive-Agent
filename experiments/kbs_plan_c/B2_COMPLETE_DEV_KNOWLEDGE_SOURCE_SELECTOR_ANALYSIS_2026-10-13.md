# B2 — Relationship-knowledge source ablation, candidate regimes and nested decision quality

**Date:** 2026-10-13. **Decision: B2-1 PASS; B2-2 computation and data identity PASS; B2-3 nested DEV science PASS with carefully scoped interpretations.** Entire exercise is **post-G5, post-B1 exploratory DEV evidence**, not a new independently revealed TEST or a pre-registered G5 inferential family.

## 1. Provenance and execution recovery

- **Scientific design fixed before new source outcomes**: [B2 relationship-knowledge specificity protocol](B2_RELATIONSHIP_KNOWLEDGE_SPECIFICITY_PROTOCOL_2026-10-13.md), 50,049 original matched author-ranking DEV events, 12,628 users, original trained primary-seed SASRec/GRU4Rec and corrected full/all-prior relation Memory.
- **Exact parity pilot**: [#38367455403](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38367455403) PASS, both original Full Memory F rank and B1 S NDCG reproduced without discrepancy on 128 time-spread DEV events.
- **All-event component labels**: [#38367721633](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38367721633), Python computation completed 50,049 rows in **161.97 seconds**, Full-Memory F/S exact mismatches **0/0**; self-host private source persisted and JSON/schema validation passed. The final GitHub `upload-artifact` failed with `ECONNRESET`, which caused the **workflow** to be marked FAILURE but did **not** invalidate or roll back the private research output. [Full-score audit](B2_FULL_DEV_FIVE_SOURCE_ABLATION_RESULTS_AND_PENDING_GATE_2026-10-13.md).
- An artifact-only recovery run failed while resolving GitHub Actions dependencies; to prevent repeated private scoring, the nested source was reattached using [a source-verifying gate](B2_FULL_DEV_LABELS_PASS_GATE_2026-10-13.json) and a [download-/upload-/checkout-free inline scientific workflow #38369503457](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38369503457), which completed **SUCCESS**, rehashed the persisted private input against its manifest **before fitting** and printed only safe aggregate results. Source code is persisted in `.github/workflows/kbs-b2-inline-offline-nested-dev.yml` and `analysis/kbs_plan_c/b2_nested_knowledge_specificity_dev.py`; its inlined threshold/HGB/bootstrap routines reproduce the frozen definitions.
- [Machine-readable public aggregate](B2_NESTED_DEV_SOURCE_SPECIFICITY_AGGREGATE_2026-10-13.json) was reassembled directly from four safely formatted successful job-log summaries; complete private DEV per-event outcomes remain on self-host. Private nested report SHA256: `80aaa58e194a3e39188dc5807f2c3b913e1e5378df7dce254dbe3ca1d65e7d74`.
- **No** original G5 TEST revealed, no Base retrained, no private user IDs, event IDs or per-candidate scores exported; original N8 main article and S1–S9 unchanged.

## 2. Does genuine relationship evidence outperform nonpersonal controls?

All statistics below are averaged over the same 50,049 DEV events. S candidate regime is **575 target-retained sampled authors for retrospective ranking labels only**; it is not a feasible online candidate generator.

| Memory composition | Full-active F NDCG@10 | Sampled S NDCG@10 |
|---|---:|---:|
| Full: 0.10 popularity + 0.45 short + 0.45 long | **0.343509** | 0.668498 |
| Long-only | 0.333231 | **0.773602** |
| Short-only | 0.273839 | 0.407506 |
| TRAIN-only popularity | 0.022215 | 0.197796 |
| History-score placement placebo | 0.007576 | 0.189571 |

Under F, Full Memory is better than Long-only. Under S, Long-only is considerably better than Full. This is a source-level **candidate-regime interaction on ranking utility**: the same historical evidence composition can be evaluated in different orders when the candidate set changes. It reinforces the importance of aligning the ranking-value target to the actual decision environment, but Krichene and Rendle (KDD 2020) already established general sampled metric non-preservation. Thus the result **does not itself invent new sampling theory**.

Long- and Short-only outperform nonpersonal popularity/relationship-placement placebo on absolute ranking metrics; nevertheless the shift placebo is an intentionally broken within-event history-to-author placement, not a globally realistic randomized history model. The fixed 0.45/0.45/0.10 mixture was not retuned. Claims about causal *identity-specific* relational effects must remain bounded.

## 3. Main B2-3 question: does the candidate regime matter for the actual selector, by knowledge type?

For each variant and Base, exactly the original B1 nested logic was applied: **5 outer × 4 inner user-disjoint folds**, HGB regression max_iter 120/depth 3/LR .05/leaf 50, original OOF `score >= threshold` with ≤30% **inner-DEV** Memory calls and 2,000 paired user-cluster bootstrap draws. S→F learned/calibrated only from S labels, F→F from F labels. All strategies are evaluated on identical F outer-user data. No retrospective TEST equal-call threshold adjustment was used.

### Original twelve pretarget decision features

| Memory source | SASRec F→F NDCG | SASRec regret F→F − S→F | GRU4Rec F→F NDCG | GRU4Rec regret |
|---|---:|---:|---:|---:|
| Full Memory | 0.302658 | 0.006159 | 0.303093 | 0.004970 |
| Long-only | 0.298562 | 0.010605 | 0.300374 | 0.010262 |
| Short-only | 0.279424 | 0.020694 | 0.279585 | 0.020291 |
| Popularity-only | 0.258167 | 0.000000 | 0.258971 | 0.000010 |
| Relation-shifted placebo | 0.258167 | 0.000020 | 0.258971 | 0.000014 |

**Paired user intervals and actual calls**:

| Memory source | SASRec calls S→F/F→F | GRU4Rec calls S→F/F→F | SASRec regret 95% CI | GRU4Rec regret 95% CI |
|---|---:|---:|---|---|
| Full Memory | 14988/15016 | 15001/14762 | 0.004835, 0.007543 | 0.003550, 0.006369 |
| Long-only | 14992/14782 | 14913/14944 | 0.008746, 0.012488 | 0.008508, 0.011887 |
| Short-only | 171/14766 | 141/14851 | 0.019189, 0.022249 | 0.018616, 0.021906 |
| Popularity-only | 1/0 | 4/0 | 0.000000, 0.000000 | 0.000000, 0.000030 |
| Relation-shifted placebo | 5/0 | 2/0 | 0.000000, 0.000054 | 0.000000, 0.000042 |

Important caveat: Short-only's extremely large regret primarily coincides with **near-zero Memory calls under S-supervision but approximately 15,000 under F-supervision**; it cannot be interpreted as a same-budget causal effect or evidence that Short-only has the strongest intrinsic knowledge utility. Popularity-only and history-placebo are so weak that reasonable selectors usually return Base with essentially zero calls; their near-zero regret is partly a **floor effect**, not necessarily a strong identification of relation-specific domain adaptation.

**Cross-source matched decision-regret contrasts**: with the twelve-feature policy, Full-minus-Long regret is **-0.004445** SASRec (paired 95% CI [-0.006390, -0.002561]) and **-0.005292** GRU4Rec (CI [-0.007074, -0.003481]); Long-only has **larger** transfer regret than Full under this panel. User-paired contrasts are not independent multi-seed evidence and lack a new pre-registered multiplicity family.

## 4. Feature-information control: candidate count plus Base score descriptions only

To avoid a misleading popularity-only control being secretly rescued by genuine relationship-history features in the gate, all source-arm comparisons were also repeated using only **six pretarget descriptors** (candidate count and five Base score features). The same users, F/S outcomes and original gate capacity/threshold objective were retained.

| Memory source | SASRec regret, 6 features | GRU4Rec regret, 6 features | SASRec calls S/F | GRU4Rec calls S/F |
|---|---:|---:|---:|---:|
| Full Memory | 0.001814 | 0.001607 | 14931/14908 | 14749/15112 |
| Long-only | -0.000210 | 0.001452 | 15054/14842 | 14997/15030 |
| Short-only | 0.018903 | 0.017778 | 58/14981 | 173/15050 |
| Popularity-only | 0.000032 | -0.000003 | 9/30 | 0/20 |
| Relation-shifted placebo | 0.000000 | 0.000000 | 7/9 | 0/2 |

For **Full Memory**, the transfer regret decreases from **0.006159 → 0.001814** (SASRec; a 70.6% reduction) and **0.004970 → 0.001607** (GRU4Rec; a 67.7% reduction). This suggests that the original historical/evidence descriptors help the learner exploit regime-dependent conditional utility; nevertheless the two feature panels also differ in predictor information and potential approximation capacity, so this is **not** an isolated causal mechanism test. The six-feature panel still uses Base representations that encode user history, so it is more accurate to call it **no direct relation-feature panel**, not literally no-history or no-user-information.

Under six features Long-only's S→F penalty is weak or inconsistent between Base families; Short-only remains strongly affected with a major call-rate drift. Thus the B2 observations point to **context and information availability as part of the knowledge-use decision**, not an invariant universal sign reversal associated with all relation knowledge.

## 5. What B2 changes in the KBS scientific-risk assessment

- **R3, scientific importance of the three-part combination: PARTIALLY MITIGATED — stronger than after B1, not closed.** B1 established same-task candidate regime → value target → held-out decision-quality loss. B2 now tests **where expert value comes from**: true long/short historical relation signals yield much higher raw ranking quality than popularity and broken history placement, and their S→F selector responses differ from no-relation controls. This is a concrete controlled joint knowledge-source/decision evaluation, more closely tied to KBS's empirical mechanism precedent (e.g., Yerragunta et al. KBS 2026, 346:116167).
- **R1, generic deferral novelty: still materially OPEN.** None of the source ablations invents a new consistent estimator, new domain-adaptation theorem, or a competitive full Learning-to-Defer/DS-Frame baseline; all are post-hoc evaluations with the established fixed utility target.
- **R2, Always Memory absolute quality/efficiency: still OPEN.** In primary M3 DEV, Full Always Memory 0.343509 is more accurate than the 30%-call selectors; actual service computation cost is not validated. Do not claim Memory routing saves latency/resources.
- **Important limitation**: the null placebo rotates within-event history-score support and does not preserve cross-user/global author marginals; the target-retained sampled regime is an offline metric construction. Observed call-rate drift, target/history feature access and single shared DEV cohort limit external validity and interpretation.

**Editorial decision: B2 source ablation and nested DEV complete, with important evidence for a more integrated knowledge-value study, but not sufficient to declare submission-ready or promote to new confirmatory TEST.**

## 6. Next scientific decision, without automatic new experiments

A follow-on independent outcome cohort could test the precise mechanisms **only if truly unseen, authorized DEV/TEST data are available** and the authors freeze effect definitions, equal-cost/reference curves and sensitivity rules before revealing outcomes. A stricter relationship placebo preserving user and author marginals, plus a cost-matched route evaluation, would improve causal interpretation. Given the remaining substantial R1/R2 editorial risks, the authors should reassess scientific-thesis framing and decide explicitly whether a new independent TEST is necessary for KBS before modifying the N8 submitted manuscript.

## 7. Research integrity

This document is an audit of experimental evidence, not new body text. Original manuscript `main.tex` blob `40be249de52c0ae423b793c0dd4c55f2fdd69f46`, combined S1–S9 blob `f5575d29ac3de222a04f78b48698cae119eac0bf` and frozen original G5 TEST are unchanged. This post-G5 DEV research should enter any revised manuscript as **clearly labeled exploratory mechanistic corroboration**, not one-shot confirmation of originally frozen G5 claims.
