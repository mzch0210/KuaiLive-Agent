# N15 P1-C — Estimand reconciliation, feature-panel dependence, and revised decision gates

**Date:** 2026-10-28  
**Branch:** kbs-n15-scientific-strengthening-20261027; Draft PR #9  
**Historical status at initial P1-C decision (2026-10-28; superseded by the P1-D result addendum below):** P1-A and P1-B computation PASS as exploratory DEV evidence. P1-C existing-evidence reconciliation COMPLETE. A single six-feature exact-quota diagnostic was then CONDITIONAL / NOT AUTHORIZED TO EXECUTE YET.

**Current status (verified 2026-10-28):** P1-D has since completed successfully as an aggregate-only exploratory DEV diagnostic on [Actions #40633996865](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40633996865); see [the result report](../../experiments/kbs_plan_c/N15_P1D_SIX_FEATURE_SOURCE_INTERACTION_RESULTS_2026-10-28.md). The result makes feature-panel dependence OBSERVED / MATERIAL for this reused-DEV offline batch protocol. No further same-DEV feature/quota/source search is authorized. N14 remains unchanged; independent P3 and KBS submission remain HOLD.

## Executive decision

N15 is revised, not abandoned. Keep the N14 single research question and every frozen original result unchanged. The primary empirical question remains whether candidate-regime-aligned supervision of a fixed historical relationship Memory changes the allocation and full-candidate ranking quality of a frozen use policy.

The P1-A result shows that the F-supervision advantage does not disappear under a newly defined, exact-call offline batch allocation on the reused DEV cohort. P1-B shows a negative Full-versus-Long-only source-by-supervision interaction under the 12-feature panel. Neither result is an independent confirmation, a pure label-only causal effect, a deployable online policy, or proof of production savings.

The key newly elevated risk is **feature-panel dependence of the source interaction**. Earlier B2 threshold-policy results using six descriptors (candidate count plus five Base-score descriptors) showed that the Full-minus-Long transfer-regret contrast can weaken or change direction relative to the 12-feature panel. Because B2 used a different threshold-policy estimand, it does not directly refute P1-B; it does mean the source interaction must not be described as an invariant knowledge-source mechanism.

**Original revised sequence at the time of P1-C decision (historical; superseded by the P1-D result addendum below):** (1) complete and record this source-level estimand reconciliation; (2) decide whether source specificity is essential to the proposed KBS contribution; (3) only if it is essential, rights and source gates pass, and the result could change the manuscript decision, consider one q=0.30 six-feature exact-quota diagnostic; (4) independently assess novelty and future-data eligibility before any confirmatory work. Do not expand the reused-DEV search.

**Current disposition:** P1-D is complete and is not authorization for further same-DEV exploration. The next legitimate step is reuse of existing independent-review materials and resolution of author-owned publication/data-rights gates; P3 and KBS submission remain HOLD.

## 1. Evidence reconciliation: do not pool unlike estimands

| Evidence | Population and policy | Main result | What it supports | What it does not support |
|---|---|---|---|---|
| N14 B4-A H1 | 30,000 additional author targets; frozen threshold policies; 20-cell population weights; naturally realized call rates differ | Weighted F−S: SASRec +0.005391; GRU4Rec +0.003585 | Original frozen primary comparison | Equal-call causal effect, future-period replication, or revised Holm inference |
| N15 P1-A | 50,049 reused DEV events / 12,628 users; five outer user-disjoint folds; exact per-fold q=0.30 batch top-k; 12 pretarget features; unweighted full-F NDCG | SASRec +0.006133; GRU4Rec +0.005398; 15,014 calls per arm and architecture | The F-versus-original-S difference persists for this offline equal-call allocation estimand | A reinterpretation of B4-A, online feasibility, independent confirmation, or production cost savings |
| N15 P1-B, Full source | Same reused DEV; exact quotas; 12-feature panel | D_Full(0.30): SASRec +0.006133; GRU4Rec +0.005398 | F-supervised policy quality advantage within this panel and protocol | A label-only intervention |
| N15 P1-B, Long-only source | Same reused DEV; exact quotas; 12-feature panel | D_Long(0.30): SASRec +0.011180; GRU4Rec +0.010291 | Larger F-versus-S gap for Long-only under the 12-feature protocol | A universal ranking of knowledge sources or causal source effect |
| N15 P1-B interaction | I = D_Full − D_Long | SASRec −0.005047, descriptive user-cluster 95% interval [−0.007022, −0.003235]; GRU4Rec −0.004893, interval [−0.006725, −0.003070] | A stable descriptive interaction over the four prespecified quotas in this reused cohort and feature panel | Confirmatory inference, policy-refitting uncertainty, or transfer beyond this cohort |
| Earlier B2, 12-feature threshold policies | Same DEV cohort; different naturally realized threshold-policy estimand | Full-minus-Long transfer-regret contrast: SASRec −0.004445; GRU4Rec −0.005292 | Qualitative corroboration under a different policy protocol | An exact-quota estimate or independent replication |
| Earlier B2, six-feature threshold policies | Same DEV; candidate count plus five Base-score descriptors; not a literal no-history representation | Full regret: 0.001814 / 0.001607; Long-only regret: −0.000210 / 0.001452 for SASRec / GRU4Rec | Feature information may materially change the observed transfer-regret pattern | Direct numerical comparison with P1-B or proof that direct relation features causally produce the interaction |

All N15 P1-A/B intervals are descriptive uncertainty conditional on fitted policies; they do not account for the complete model-selection/refitting process. The original N14 three-member Holm family and its values remain frozen.

## 2. P1-C adjudication completed from existing sources

1. **Resource-matching objection:** partially addressed for the P1-A offline batch estimand only. Exact call counts remove a simple call-volume imbalance explanation within that estimand. They do not transform the original B4-A threshold-policy comparison into an equal-call experiment.
2. **Source-specificity objection:** partially addressed. P1-B provides a consistent negative Full-minus-Long interaction under the 12-feature panel, but it is conditional on the panel, labels, fitted selector and offline batch policy.
3. **Feature-panel concern:** remains open and is now a named risk. B2's six-feature threshold analysis is not the same estimand, but its change in pattern makes a general source-mechanism claim unsafe without a direct, narrowly defined comparison.
4. **Corrected-S competitor:** remains open. NI1g's NO-GO applies to previously explored candidates and is not a theorem that all valid sampled-only corrections fail. Do not rerun stopped candidates or claim universal impossibility.
5. **Practical value:** unresolved. Always Memory retains the best unconstrained full-F ranking result, and the older timed Utility path was slower than Always Memory. Invocation count is not a measured cost or latency benefit.
6. **External validity:** unresolved. P1-A/B and B2 reuse the heavily analyzed DEV period. They are not new confirmatory evidence.

## 3. Revised primary narrative and contribution boundary

Keep one paper-level question: **Does aligning the supervision regime for the incumbent-relative value of fixed historical relationship Memory with the full active candidate regime change frozen use-policy decisions and full-candidate ranking quality?**

Treat source specificity as a secondary, conditional mechanism question—not a separate headline contribution—until its feature dependence is resolved.

Permitted wording, with the appropriate exploratory qualification:
- Candidate-regime supervision changes the fitted policy's full-candidate allocation value in the tested offline batch setting.
- The F-versus-S policy-quality gap differs between Full and Long-only under the tested 12-feature panel.
- Earlier B2 results motivate a feature-information boundary rather than an invariant source effect.

Forbidden wording:
- A new sampled-ranking correction, new learning-to-defer algorithm, theorem or universal optimal router.
- A pure causal effect of labels or source identity.
- A proven production efficiency, latency, or cost saving.
- An independent replication or a new confirmatory TEST.
- A claim that every valid corrected-S method has failed.

## 4. Conditional one-shot diagnostic: exact-quota six-feature source interaction

**Decision: HOLD unless all admission conditions below are explicitly met. This document authorizes no private execution.**

The diagnostic is justified only if the authors choose source specificity as essential to the KBS contribution and the answer could change the manuscript's claim. Otherwise, stop after P1-C and retain P1-B as a bounded exploratory sensitivity result.

If admitted, freeze the following before any private data read:
- **Single primary quota:** q=0.30 only. Do not rerun q=0.10, 0.20 or 0.40.
- **Population and split:** the existing 50,049-event / 12,628-user DEV source, exact certified B1/B2 roster and the same five outer user-disjoint folds. No TEST, B4-A or G5 outcome access.
- **Source arms:** Full Memory and Long-only only; no expansion to the five-source panel.
- **Feature panel:** exactly the six existing B2 descriptors: candidate count and the five frozen Base-score descriptors. Exclude direct relationship-history descriptors. Do not call this a no-history panel, because Base scores may encode user history.
- **Supervision and outcomes:** retain the existing F and original uncorrected target-retained S labels; score both policies on the same full-F candidates and the same F utility scale. No corrected-S retraining.
- **Allocation:** the same exact per-fold label-blind top-k rule and tie-breaking as P1-A/B; each F/S pair must receive identical calls within each fold. Expected aggregate q=0.30 allocation is 15,014 calls per arm when the same original roster and fold sizes are preserved.
- **Primary descriptive estimand:** D_s(0.30) = full-F NDCG of F-supervised policy minus full-F NDCG of S-supervised policy for source s; I(0.30) = D_Full(0.30) − D_LongOnly(0.30).
- **Uncertainty:** paired user-cluster bootstrap intervals, labeled descriptive only. No new confirmatory p-value, no post-hoc multiplicity claim and no claim of independent replication.
- **Outputs:** aggregate-only summary and provenance hashes on an isolated immutable path. Never export private rows, event/user identifiers, per-request scores, model weights or joblib artifacts.

### Admission gates

All must pass before implementation or execution:
1. Written decision that source specificity is necessary to the intended scientific contribution, not merely an interesting extra analysis.
2. Confirmed authorization and lawful access to the exact restricted B1/B2 artifacts and self-hosted compute; prior workflow presence is not authorization.
3. Source SHA, roster, label parity, feature definitions, fold parity and output path verified before fitting.
4. Public synthetic tests cover exact calls, no label leakage, feature selection, deterministic ties, source-interaction identity and aggregate-only output.
5. Code and analysis are frozen before the private run; no test outcome is opened.

If any gate fails, mark P1-D NO-GO and do not substitute another DEV search. A result with negative I and descriptive intervals away from zero would be **consistent with** a source interaction under this six-feature panel, not causal proof. If I weakens, crosses zero descriptively, or reverses, narrow the claim to feature-conditional evidence and do not keep searching feature panels.

## 5. Updated novelty and stop/GO rule

Relevant prior art further narrows the defensible novelty:
- Krichene & Rendle, KDD 2020, show sampled ranking metrics may fail to preserve full-ranking comparisons and discuss corrections: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Subbiah, Rendle & Aggarwal, CIKM 2024, study corrected rank estimation under negative sampling: https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/
- Mao, Mohri & Zhong, ICML 2025, establish learning-to-defer surrogate and consistency results for multiple experts: https://proceedings.mlr.press/v267/mao25c.html
- DeSalvo et al., Budgeted Multiple-Expert Deferral, 2025 preprint, study explicit budget-constrained expert querying: https://arxiv.org/abs/2510.26706
- Montreuil et al., ICLR 2026, formulate Top-k and adaptive Top-k learning-to-defer: https://proceedings.iclr.cc/paper_files/paper/2026/hash/6dc129f0383f9fa270347bb09f0030d4-Abstract-Conference.html

These works do not automatically subsume the fixed historical relationship-memory setting, but they mean exact-quota allocation and general expert routing cannot be presented as method novelty. The only defensible prospective contribution is a carefully bounded empirical/decision-design insight about candidate-regime-indexed incremental value for a fixed, explicit knowledge source, supported by valid evidence.

**Stop / GO criteria**
- **GO to limited P1-D implementation:** only if source specificity is indispensable, rights/source gates pass, and the result can change the paper's claim.
- **NO-GO to P1-D:** if source specificity is not essential, any gate fails, or the only objective is to obtain another favorable same-DEV number.
- **P3 independent confirmation:** HOLD until truly unseen, lawful, eligible targets and full candidate/history reconstruction are verified and the new hypothesis family is frozen before outcomes.
- **KBS submission:** HOLD. Reassess after the evidence boundary and prior-art matrix are updated; a green CI or favorable DEV interval is not a submission GO.

## 6. Audit trail and protected artifacts

P1-C is a desk-based reconciliation of existing aggregate files; it does not read private rows, fit a model, create a new empirical estimate or access TEST. It uses:
- N14 P6/P7 novelty and submission audit.
- N15 P1-A strict equal-call DEV result.
- N15 P1-B Full-versus-Long interaction result.
- B2 complete DEV source-selector analysis, including both 12-feature and six-feature threshold-policy panels.
- N15 P0 no-repeat contract and corrected-S method gate.

No change is authorized to N14 main.tex, the original N13 research archive, original H1/H2 values, the original three-test Holm family, or previously revealed TEST outcomes.


## P1-D result addendum (2026-10-28)

P1-D has now executed successfully; see [N15 P1-D result report](../../experiments/kbs_plan_c/N15_P1D_SIX_FEATURE_SOURCE_INTERACTION_RESULTS_2026-10-28.md) and [Actions run #40633996865](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40633996865). Under the six-feature panel at q=.30, SASRec interaction I=+0.001676476 (descriptive user-cluster 95% interval [+0.000152109,+0.003104834]), reversing P1-B's 12-feature sign. GRU4Rec I=−0.000478588 (interval [−0.001899109,+0.000884844]), attenuated and crossing zero. This confirms a material feature-panel dependence concern for the tested reused-DEV offline batch protocol, not a formal panel-by-source interaction test or causal explanation. No further same-DEV feature/quota/source search is authorized.
