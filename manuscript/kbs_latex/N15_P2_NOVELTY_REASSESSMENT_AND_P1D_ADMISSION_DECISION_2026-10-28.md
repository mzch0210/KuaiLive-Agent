# N15 P2 — KBS novelty reassessment and P1-D admission decision

**Date:** 2026-10-28  
**Branch:** `kbs-n15-scientific-strengthening-20261027`; Draft PR #9  
**Decision:** **Source-specificity is essential to the intended KBS positioning, but P1-D is NO-GO in the current phase because required source-owner/data-rights authorization is not documented.** No private experiment or alternative reused-DEV search is authorized by this record.

## 1. Executive decision

The N14 core paper remains a coherent and tightly scoped empirical study, but its method-level novelty is still HIGH-CONTESTABLE. Its central ingredients are individually established: sampled-ranking evaluation can disagree with full-candidate ranking; learned selective prediction/deferral already chooses between an incumbent and a specialist; and budget-constrained/top-k expert allocation is now an active research area.

P1-A contributes a useful exact-call **offline batch estimand**, not a new selector algorithm or an online policy. P1-B provides the most distinctive knowledge-system signal so far: under the 12-feature panel, the F-versus-S supervision gap differs between Full and Long-only Memory. Yet prior B2 results show that the source-regret pattern depends on the available feature panel under a different threshold-policy estimand. Thus the interaction is a conditional exploratory association, not a universal source effect.

**Adjudication:** source-specificity is needed if the authors want to defend a KBS-specific knowledge-use contribution beyond the familiar combination of sampled-metric sensitivity and standard deferral. It must remain a secondary, tightly bounded mechanism question rather than a headline causal claim. The current evidence is not enough to clear KBS novelty.

## 2. Prior-art update (official publisher/proceedings sources checked 2026-10-28)

| Work | What is already established | Consequence for this project |
|---|---|---|
| Krichene & Rendle, KDD 2020, [On Sampled Metrics for Item Recommendation](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/) | Sampled ranking metrics can fail to preserve full-ranking comparisons. | The sampled/full discrepancy itself is not novel. |
| Subbiah, Rendle & Aggarwal, CIKM 2024, [Improved Estimation of Ranks for Learning Item Recommenders with Negative Sampling](https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/) | Rank-estimation correction under negative sampling is already studied. | The uncorrected S comparator cannot be treated as the strongest possible corrected alternative; NI1g NO-GO only covers its tested candidates. |
| Mao, Mohri & Zhong, ICML 2024, [Regression with Multi-Expert Deferral](https://proceedings.mlr.press/v235/mao24d.html) | Learned expert deferral and consistency frameworks. | Applying a selector to a fixed Memory source is not a new generic deferral method. |
| Montreuil et al., ICLR 2026, [Why Ask One When You Can Ask k? Top-k Learning-to-Defer](https://proceedings.iclr.cc/paper_files/paper/2026/hash/6dc129f0383f9fa270347bb09f0030d4-Abstract-Conference.html) | Top-k and adaptive Top-k expert allocation with consistency guarantees. | Generic budgeted/top-k allocation is not a defensible novelty claim. |
| Cortes, Mao, Mohri & Zhong, ICML 2026, [Optimized Deferral for Imbalanced Settings](https://proceedings.mlr.press/v306/cortes26b.html) | Cost-sensitive deferral methods and guarantees for expert imbalance. | Do not claim new deferral optimization or resource-aware learning theory. |
| Montreuil et al., AISTATS 2026, [Online Learning-to-Defer with Varying Experts](https://proceedings.mlr.press/v300/montreuil26b.html) | Online deferral with dynamically varying expert availability and regret analysis. | No online-feasibility or regret claim is supported by the offline fold-batch experiment. |
| DeSalvo et al., 2025 preprint, [Budgeted Multiple-Expert Deferral](https://arxiv.org/abs/2510.26706) | Explicit budgeted expert querying and associated guarantees. | A fixed call quota alone does not establish methodological novelty. |

These works do not directly evaluate this exact setting—a fixed, transparent historical relationship-memory ranker, incumbent-relative NDCG increment, candidate-regime-specific offline labels, and a common full-active candidate outcome. That difference is potentially relevant, but it is an empirical problem-specific distinction rather than a new general method. This literature review is a focused novelty check, not a systematic review of all 2026 work.

## 3. Project evidence mapped to the novelty decision

### N14 original frozen evidence

- The original 30,000-target B4-A comparison remains a complete-policy comparison with naturally different F/S call rates; the three-member Holm family is immutable.
- The room-ranking result motivates candidate-regime sensitivity but does not isolate candidate count causally.
- Always Memory remains better on unconstrained full-candidate NDCG; the older pointwise Utility path was slower. No production efficiency benefit is established.
- The additional 30,000 targets come from the same recording period and are not an independent future-period replication.
- A valid corrected-S comparator remains unresolved.

### N15 exploratory evidence

- **P1-A:** exact-call offline batch top-k at q=.30 preserves an F-supervision advantage on the reused DEV cohort. This addresses one narrow net-call-volume objection for the new estimand only.
- **P1-B:** under the 12-feature panel, Full-minus-Long interaction is −0.005047 for SASRec and −0.004893 for GRU4Rec at q=.30; the sign is stable across the four explored quotas. All values remain post-G5 exploratory evidence on the same DEV cohort.
- **B2 feature control:** the prior six-feature threshold-policy analysis (candidate count plus five Base-score descriptors) substantially changed the Full/Long pattern. Because this is a different policy estimand, it is not a direct contradiction of P1-B, but it makes an invariant source-mechanism claim untenable.
- **P1-C:** existing evidence reconciliation is complete. No private rows were read, no models were fit, and no TEST was opened.

## 4. P1-D scientific value versus admissibility

**Scientific value:** A single q=.30 exact-quota diagnostic using the six frozen B2 descriptors could determine whether the P1-B source interaction remains descriptively present when direct relation-history descriptors are removed. This result could change how narrowly the paper states its knowledge-specific contribution. It would still be exploratory, not independent confirmation or causal identification.

**Admission decision: NO-GO for the current phase.** The project’s [N12-C7 rights register](N12_C7_CLAIM_SOURCE_REPRODUCIBILITY_AND_RIGHTS_REGISTER_2026-10-19.md) explicitly leaves licensing/authorization and redistribution status **OPEN / NOT CLEARED**. The P1-C admission contract requires documented authorization and lawful access to the exact restricted B1/B2 artifacts and self-hosted compute; existing workflow history does not substitute for that signoff. No signed source-owner/data-rights attestation was found in the project record reviewed for this decision.

Accordingly:
- Do not run P1-D on private B1/B2 sources now.
- Do not create a replacement DEV analysis, expand the feature/budget grid, rerun the B2 sweep, or search for a favorable panel.
- Do not infer permission from prior successful self-hosted Actions runs.
- Reopen P1-D only after the responsible human data/source owner records explicit authorization, lawful-use basis, allowed compute location, permitted aggregate output scope and source-hash provenance in the rights register. A fresh gate review must be recorded before execution.

## 5. Revised claims and manuscript implications

Keep the N14 manuscript source unchanged in this phase. If a later author-approved revision is considered:
- retain the candidate-regime supervision result as a bounded empirical policy comparison;
- describe P1-A only as an exploratory exact-call offline batch sensitivity analysis;
- describe P1-B only as an exploratory 12-feature Full-versus-Long conditional interaction;
- do not call the six-feature B2 control a no-history panel: Base scores may encode user history;
- do not claim a pure causal source or label effect, new sampled-rank correction, novel L2D algorithm, online feasibility, production savings, independent replication, or universal failure of corrected-S methods.

## 6. Stop/GO matrix

| Gate | Decision | Reason |
|---|---|---|
| N14 manuscript preservation | PASS | Core source remains unchanged. |
| P1-C evidence reconciliation | COMPLETE | Existing aggregates and protocol distinctions reconciled. |
| KBS scope | PASS | Recommender/knowledge-use decision is within scope. |
| KBS method-level originality | HOLD / HIGH-CONTESTABLE | Core building blocks are established; no new method/theorem and corrected-S competitor remains unresolved. |
| Source-specificity as a KBS contribution | ESSENTIAL BUT UNPROVEN | Needed to distinguish the knowledge-system insight, but currently only conditional exploratory evidence. |
| P1-D private six-feature diagnostic | **NO-GO in current phase** | Required explicit source-owner/data-rights authorization is not documented. |
| P3 independent confirmation | HOLD | No eligible unseen cohort has been established. |
| KBS submission | HOLD | Novelty, data rights, reproducibility and author-owned declarations remain unresolved. |

## 7. Next legitimate action

The next action is **not another experiment**. The human project/data owner must resolve and record the outstanding rights/authorization status. If the owner cannot establish it, close P1-D without execution and reassess whether the bounded empirical contribution is sufficient for KBS or whether a different venue is more appropriate. If authorization is later established, make a new dated admission decision; do not silently reopen the current NO-GO.
