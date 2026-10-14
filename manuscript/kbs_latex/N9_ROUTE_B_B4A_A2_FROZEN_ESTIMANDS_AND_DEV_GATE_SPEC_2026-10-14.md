# B4-A A2 — frozen estimands and DEV-only gate specification (before B4-A target reveal)

**Freeze timestamp: 2026-10-14.** Source: A1 sealed SHA256 main `be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14`, mechanism subset `40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059`. A0/A1 outcomes were never read. A2 is **DEV-only**; B4-A labels, current target authors, TEST NDCG, G5 old TEST metrics, and new rankings MUST NOT be input.

## Primary population-representation rule

A1 selected **1,500 event IDs** per each of 5 source dates × 4 within-day pretarget-history rank quartiles. The natural eligible-population distribution across dates is very unequal. Consequently the **primary estimand** is the eligible TEST-like request population mean, estimated by post-stratification:
`w_c = N_c / n_c` in each of the 20 design cells. Here `N_c` is the total *pretarget metadata qualified* eligible-residual source pool count in cell `c` (from the frozen A1 SQL's NTILE(4) window), `n_c=1500` for the 30k main sample and `n_c` is the fixed observed sample count per cell in the 4096 nested subset. Weights apply identically to all paired metrics, policies, calls, numerator/denominator, and bootstrap replicates. The 20-cell balanced design mean (equal per cell) is secondary. No outcome-adaptive weight selection or after-reveal exclusion.

Uncertainty: **5,000 user-cluster resamples**, resample users then compute the original weighted ratio `sum_i w_i d_i / sum_i w_i` for each replicate. For H2, average three frozen null outcomes *within each event first*, then bootstrap across users. Report unadjusted paired 95% percentile intervals and Holm-adjusted p-values for the three main directional contrasts. Replicates are based on selected users, not three null seeds as independent cohorts. Per-date/user-overlap strata and observed call-rate differences are descriptive. The A1 sample has event-level target ID disjointness but not necessarily user-disjointness from original G5.

Primary hypotheses **before any new target quality**:
- H1 SASRec primary seed: F-aligned minus S-aligned under exactly identical F candidates.
- H1 GRU4Rec primary seed: same.
- H2 original fixed Full Memory minus per-event arithmetic average of exactly three temporal author-availability/time-marginal-preserving relation nulls, within the presealed 4096 subset.

One-sided user-cluster sign randomization (5,000 sign draws per user cluster) uses the same recorded user-cluster exchangeability/symmetry assumption as original G5, plus Holm familywise correction across **all three** primary comparisons. Also provide two-sided bootstrap intervals and all null/negative outcomes. No seed/model/metric substitution after reveal. The three null seeds are exactly 20261014, 20261015, 20261016; they are not independent future cohorts. Null nonfloor requirements are judged only **after** blind predictions have been signed/sealed, not tuned using labels.

## Fixed A2 DEV learning prescription

- 50,049 author DEV requests/12,628 users, `klm3_b1_full_dev_candidate_labels_seed20261012_v1/dev_pair_candidate_labels.csv`, existing registered SHA `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`. Source contains retrospective S labels only in DEV.
- Base frozen primary SASRec/GRU4Rec seed 20261012; no Base or Memory retraining.
- 12 pretarget features = seven shared `x_hist_event_count,x_hist_warm_count,x_hist_distinct,x_hist_repeat_max,x_hist_short_unique,x_memory_history_supported_share,x_candidate_log_count` plus five model-specific `x_<family>_base_margin,base_std,base_top_z,base_top_score,base_score_mean`. **At A3** score the same F roster and include full-candidate Base score summaries, NEVER retrospective target-retained S candidates as gate input.
- Two fixed HistGradientBoostingRegressor estimators per Base (S-aligned and F-aligned); max_iter=120, learning_rate=0.05, max_depth=3, min_samples_leaf=50, l2_regularization=1.0, early_stopping=False, random_state=20261012. Four-way user-disjoint GroupKFold produces complete DEV OOF scores. Threshold selected by original `frozen_gate.select_threshold` exactly once using S-utility labels for S-aligned and F-utility labels for F-aligned, optimizing signed mean DEV value with call cap floor(0.30*50049). Ties are indivisible; threshold None means never call. Finally fit four models on **all DEV only** and save private model files, prediction-feature ordering, policies and SHA before A3.
- Track both OOF DEV call fractions and *final-model fitted-DEV* call fractions (diagnostic, not threshold recalibration). A3 shall use unaltered DEV OOF threshold, and new B4-A realized call rate may differ; call fractions/points on the new target evaluation cannot be modified.
- **Important inferential caveat**: S arm is trained/calibrated with retrospectively target-retained 575-candidate DEV supervision while F uses full-active labels; this tests supervision-regime alignment and information entitlement, not algorithm architectural novelty or equal TRAIN label costs. A2 OOF full-cohort metrics are model-selection diagnostic, not a new independent evaluation; original G5 TEST must not reopen.
- A2 may run technically under existing restricted, nonredistributing DEV processing; **A3/A4 require separate rights and protocol/governance acceptance**, and private author IDs / new target labels remain inaccessible during A2.

**Status at freeze: protocol saved, A2 fitting not yet certified.**
