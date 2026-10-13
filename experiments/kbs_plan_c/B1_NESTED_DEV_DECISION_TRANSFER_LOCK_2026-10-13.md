# B1-3 DEV candidate-regime decision transfer: fixed analysis contract

**Date:** 2026-10-13; written while the first successful B1 nested-run was still computing. **Design class:** new **POST-G5 EXPLORATORY DEV ONLY** experiment. Does **not** expand the original G5 TEST registered family.

**Input source:** the first successful 50,049-event/12,628-user B1-2 private paired source `klm3_b1_full_dev_candidate_labels_seed20261012_v1`, original corrected full-active F labels + newly constructed 575-candidate sampled S labels, same pretrained SASRec/GRU4Rec seed 20261012 and corrected fixed relationship Memory. Original full-active event-level 12 features are identical across arms and were available before observing the target. S target-retained candidates define **offline supervision** and do not enter online gate features.

## Frozen arm meanings

1. **S→F pure cross-regime transfer**: fit one hist-gradient-boosted regressor to `Memory_S - Base_S` over inner/outer-train DEV users; inner OOF threshold selection at ≤30% Memory calls uses **only S labels**, never F labels. Freeze its pointwise score threshold; report its naturally realized calls and utility on outer full-active F users.
2. **F→F within-regime reference**: same 12 predictors, same HGB capacity and user splits; fit, calibrate on the F label difference. All fitted/evaluated data are DEV; outer-F labels used only after a rule is frozen on the outer training users.
3. **Candidate-aware/adapted→F**: concatenate matched S and F training examples, label by regime and explicit (sample=575, full event-time roster) candidate log count, and fit HGB to the corresponding regime-specific value. F labels from the **outer training users** are allowed for inner calibration. Therefore this is **regime-adapted training**, not zero-shot candidate transfer, and it should be compared primarily with F→F.

**Estimator:** `sklearn.ensemble.HistGradientBoostingRegressor`, squared loss, `max_iter=120`, learning rate 0.05, max depth 3, `min_samples_leaf=50`, `l2_regularization=1`, early stopping disabled, frozen 20261012 seed; `scikit-learn 1.5` verified offline installation. Five outer GroupKFold and four inner GroupKFold by user (same users across arms; no user across inner train/eval or outer train/eval). The published scikit-learn `GroupKFold` specification guarantees nonoverlapping groups by fold; this is independently asserted in code. (https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html).

**Threshold:** original `frozen_gate.select_threshold`, OOF pointwise selection `score >= threshold` with complete tied score blocks and best mean target gain subject to at most 0.30 inner training calls; not test-label count matching.

**Outer outcomes**: absolute **F NDCG@10**, Memory-call counts and observed call rate, conditional gain vs Always Base and Always Memory; paired (V_F(\pi_F)-V_F(\pi_S)), (V_F(\pi_\mathrm{adapted})-V_F(\pi_S)), and (V_F(\pi_\mathrm{adapted})-V_F(\pi_F)); 2,000 paired user-cluster percentile Bootstrap draws with independent fixed seed 20261013. Cluster confidence intervals are **exploratory descriptive uncertainty** conditional on one shared DEV cohort and two fixed trained Base families, not independently registered TEST significance.

**Critical scientific distinction:** S→F is allowed to experience budget/calibration drift in F; do **not** retrospectively change its threshold to produce equal observed F calls. Report both naturally realized calls and quality; if called for, a separately declared F-inner adaptation/equal-cost frontier may be run later, labeled as adaptation, not pure transfer. `candidate-aware` may use full outer-training labels and cannot be advertised as saving the need for full labels. A modest association of sampled vs full label outcomes is not a demonstrated decision mechanism.

**Acceptance:** complete five outer folds for each Base family, no leakage, fixed source byte hash, publicly archived aggregate only, complete paired user intervals, full-vs-sampled value diagnostic. No experiment outcome is assumed in advance. If (V_F(\pi_F)\approx V_F(\pi_S)), the proposed RQ2→RQ3 decisional effect may be small; do not manufacture a new finding. If F->F better but candidate-adapted not better than F->F, claim only regime-matched supervision, not superior new routing algorithm.

**GPU efficiency:** B1-2 completed 50,049 event label construction in 113.08 s using frozen batches of 512 and cached F outcomes. This B1-3 stage fits light HGB decision models on CPU; high RTX3090 GPU usage during this stage is neither expected nor an optimization target.

Source scripts: `analysis/kbs_plan_c/b1_nested_regime_transfer_dev.py`, `analysis/kbs_plan_c/frozen_gate.py`, [B1 stage1 results](B1_STAGE1_GPU_PARITY_AND_CPU_BOTTLENECK_RESULTS_2026-10-13.md). Original G5 TEST remains unmodified.
