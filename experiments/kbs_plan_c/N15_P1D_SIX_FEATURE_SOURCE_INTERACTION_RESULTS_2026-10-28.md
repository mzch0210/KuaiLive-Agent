# N15 P1-D — Six-feature exact-quota source-interaction results

**Date:** 2026-10-28  
**Workflow:** [GitHub Actions run #40633996865](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40633996865)  
**Executed commit:** `d2c79c1a13b806b5c159f1375bedfe4eedbd575c`  
**Script blob SHA:** `f50c29aafcfb19e69411ae3f3e4c74df99b7fa82`  
**Artifact:** `n15-p1d-six-feature-source-interaction-dev-aggregate`, artifact ID `12792727846`; ZIP SHA-256 `4ebcd8f1b7791573ecfe2f19c5a662b490eefb2b47480cb95b46ee25b8a5a418`.  
**Status:** **EXECUTION PASS; EXPLORATORY DEV EVIDENCE ONLY.** Public compile/synthetic preflight and restricted self-hosted run both succeeded. B1/B2 provenance, roster and source parity passed. The workflow explicitly recorded no TEST access.

## 1. Frozen protocol and scope

- Population: 50,049 reused DEV events / 12,628 users.
- Five outer user-disjoint folds; same fixed HGB capacity as the prior P1 protocol.
- Only quota: q=0.30; exact per-fold batch top-k selection; 15,014 calls per policy and source.
- Sources: Full Memory and Long-only Memory only.
- Six-feature panel: candidate count plus five Base-score descriptors. This removes the six direct history/relationship descriptors from the earlier 12-feature panel, but it is **not** a literal no-history panel because Base scores may encode user history.
- F- and original uncorrected S-supervised policies are evaluated against the same full-F incumbent-relative increment. S labels remain target-retained retrospective labels.
- 2,000 user-cluster bootstrap repetitions; intervals are descriptive and condition on the fitted outer-fold policies.
- Aggregate-only output; no TEST/G5/B4-A outcome was opened, no Base/Memory model was retrained, and no row-level output was uploaded.

## 2. Results at q=0.30

All values are unweighted original-DEV metrics. (D_s) is the full-F NDCG@10 difference between F-supervised and S-supervised allocation policies for source (s). (I=D_{Full}-D_{LongOnly}).

| Base family | (D_{Full}) | (D_{LongOnly}) | Interaction (I) | Descriptive 95% user-cluster interval | Calls per policy/source |
|---|---:|---:|---:|---:|---:|
| SASRec | +0.001908042 | +0.000231566 | **+0.001676476** | [+0.000152109, +0.003104834] | 15,014 |
| GRU4Rec | +0.000899030 | +0.001377618 | **−0.000478588** | [−0.001899109, +0.000884844] | 15,014 |

Execution invariants passed: 50,049 events, 12,628 users, B1/B2 source parity PASS, zero TEST-label access, exact equal calls within each F/S pair, allocation-value identity error below (10^{-12}), and interaction identity error below (10^{-12}).

## 3. Direct comparison with P1-B's 12-feature panel

At the same q=0.30 quota and same DEV cohort, P1-B under the 12-feature panel reported:
- SASRec: (D_{Full}=+0.006133), (D_{LongOnly}=+0.011180), (I=-0.005047), descriptive interval [−0.007022, −0.003235].
- GRU4Rec: (D_{Full}=+0.005398), (D_{LongOnly}=+0.010291), (I=-0.004893), descriptive interval [−0.006725, −0.003070].

The six-feature diagnostic changes this pattern materially:
- **SASRec:** the interaction reverses sign: negative under 12 features, positive under six features; each panel's own descriptive interval is away from zero in its respective direction.
- **GRU4Rec:** the interaction magnitude is much smaller under six features and its descriptive interval crosses zero.

These separate intervals are not a formal test of the difference between panels. Do not infer a statistically tested panel-by-source interaction from comparing the intervals, and do not claim that a particular removed feature causally explains the shift. The same DEV cohort was reused, and feature-panel selection is post hoc.

## 4. Scientific adjudication

**P1-D answers the narrow diagnostic question and confirms that the P1-B source interaction is feature-panel dependent in this reused-DEV, offline exact-quota setting.** It does not support an invariant or universal knowledge-source mechanism.

The correct interpretation is:
1. The 12-feature panel produced a negative Full-minus-Long supervision-gap interaction for both model families.
2. With the six-feature panel, the SASRec interaction reverses sign and the GRU4Rec interaction is descriptively near zero/uncertain.
3. The six-feature panel excludes direct history/relationship descriptors but retains Base-score features that may encode user history. Therefore the contrast is about the **available feature panel**, not a clean treatment that removes all user-history information.
4. This is exploratory, within-cohort evidence. It is neither independent replication nor causal identification.

## 5. Consequences and stop rule

- Mark the feature-panel dependence risk **OBSERVED / MATERIAL** rather than merely hypothetical.
- Do not run another quota, feature panel, source combination or corrected-S variant on this DEV cohort to seek a preferred sign.
- Do not replace the original N14 H1/H2 results or revise the original three-member Holm family.
- Do not promote the P1-B negative interaction to a headline mechanism claim. If later manuscript changes are considered, frame the source interaction as conditional exploratory evidence and make feature dependence explicit.
- Keep KBS submission and P3 independent confirmation on HOLD. The result improves the honesty and specificity of the evidence boundary but does not resolve method-level originality, the corrected-S competitor, external validity, data-rights publication checks, or production value.

## 6. Reproducibility references

- P1-D workflow: https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40633996865
- P1-B comparison: https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n15-scientific-strengthening-20261027/experiments/kbs_plan_c/N15_P1B_SOURCE_INTERACTION_RESULTS_2026-10-28.md
- P1-C prior estimand reconciliation: https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n15-scientific-strengthening-20261027/manuscript/kbs_latex/N15_P1C_ESTIMAND_RECONCILIATION_AND_FEATURE_PANEL_DECISION_2026-10-28.md
