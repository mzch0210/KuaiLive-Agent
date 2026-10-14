# B4-A A2 — DEV-only final decision models and pre-reveal statistical contract

**2026-10-14 | A2 PASS (TECHNICAL). B4-A main and relation-mechanism target labels remain SEALED. A3/A4 HOLD pending rights and pre-unblinding authorization. No manuscript changes and no new TEST NDCG.**

## 1. What was executed

Four fixed HGB regression gates (S-aligned and F-aligned per fixed 20261012 SASRec/GRU4Rec encoder) were fitted on the **same 50,049 M3 author DEV requests from 12,628 users**, using the previously verified B1 source file `dev_pair_candidate_labels.csv`, private SHA256 `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`. Base weights, Memory expert and original G5 TEST were not retrained or reopened. No A1 main/identity event list or B4-A target author labels were read during A2 model fitting.

- Final model source: `analysis/kbs_plan_c/n9_b4a_a2_fit_dev_gate.py`, [Actions #38506691232](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38506691232), **SUCCESS**.
- 12 input features per model, exact seven history/candidate plus five frozen Base score descriptors. S-aligned arm is *trained and calibrated* on retrospective target-containing 575-candidate DEV utility labels, but at A3 **both** arms will receive the same **F full-active candidate-set pretarget features**, not target-retained S features.
- Four-way GroupKFold gives user-disjoint *DEV OOF* predictions used once to set each gate's pointwise call threshold with `frozen_gate.select_threshold` under the original 30% DEV cap. Then a final estimator of identical HGB capacity (max_iter 120, max_depth 3, learning_rate .05, min_samples_leaf 50, l2 1, early_stopping False, seed 20261012) was fit on **all DEV**.
- Private model artifacts are persisted at `~/.cache/kuailive-agent-kbs/klm3_n9_route_b_b4a_a2_dev_frozen_final_gates_v1/private_models`. Only model SHA, threshold, feature schema and aggregate OOF diagnostics were published.
- Four private model SHA checks and G5-compatible pretarget feature-contract / 256-DEV-row prediction checks passed in [Actions #38506978008](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38506978008). The QA test opened no TEST data. Details: `experiments/kbs_plan_c/N9_ROUTE_B_B4A_A2_MODEL_CONTRACT_PUBLIC_2026-10-14.json`.

## 2. Frozen models and diagnostic values (DEV only)

| Fixed Base model | DEV label supervision | User-disjoint OOF threshold | OOF specialist calls | OOF F NDCG@10 (diagnostic) | Private model SHA256 |
|---|---|---:|---:|---:|---|
| SASRec seed 20261012 | S-aligned | +0.0460826706 | 15,012 / 50,049 | 0.296979 | `3d31df6148222a7702c2dab050c8d09aac9b84c30306c1815069a9141e02fd61` |
| SASRec seed 20261012 | F-aligned | +0.1006933071 | 15,011 / 50,049 | 0.301985 | `4af0daae533c7856cca6c7df6a8cf022cbc29e161de9aed3bb4ecdfdadd359da` |
| GRU4Rec seed 20261012 | S-aligned | +0.0492285907 | 15,000 / 50,049 | 0.297323 | `3d9dae323ba0111a298e803618827cfe223a7d8da190cdf43f6ebefb32022e88` |
| GRU4Rec seed 20261012 | F-aligned | +0.0969799446 | 15,014 / 50,049 | 0.303762 | `b06c27223b32934a21c17c7ad0e9006deec92012b406b6716f778f85b8b63fda` |

The full-DEV 4-fold OOF F-aligned minus S-aligned diagnostic differences are **+0.005005 SASRec** and **+0.006440 GRU4Rec**; decision-disagreement rates are approximately **21.31%** and **23.01%** respectively. These are **DEV-derived model selection/calibration diagnostics**, not unbiased new independent B4-A estimates. Both S and F decisions are based on the same serving F features, but the supervisory training targets embody unequal offline information.

**Invocation caveat:** The actual fitted-DEV call fraction of the *final all-DEV fit* is 30.1944% for SASRec F, 30.1864% SASRec S, 29.7628% GRU F and 29.8507% GRU S. This **does not invalidate** the frozen OOF ≤30% call cap, which is the calibrated constraint. B4-A realized call rates need not equal the DEV budget and must be reported without post-TEST rethresholding. Fitted-DEV call rates must not be misreported as OOF or prospective realized TEST rates.

## 3. Original population-weighted estimand locked before target reveal

A1 selected **30,000 / 10,387 users** (1,500 per 20 cells) and a nested **4,096 / 3,059 users** relation-control subset from the original TEST source period. This is a balanced design and does not reproduce the original source prevalence. The main scientific estimand is therefore the **eligible residual target population's post-stratified event-weighted expected F NDCG@10** (and aligned call fraction); the simple equal-cell average is secondary.

Using the same G1 warm-author eligibility rules, original-source-time dates and *within-day pretarget-history quartiles*, all **20 natural source cell totals** were recomputed and frozen **without opening target scores/labels**. [Actions #38506781299](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38506781299) **SUCCESS**, total 4,723,652:
- Main 30k: `w_cell=N_original_cell/1500`, range **63.7347–203.0080**, Kish effective sample size **26,849.29**.
- Relation-control 4096: `w_cell=N_original_cell/n_mechanism_cell`, range **436.54–1,577.78**, Kish effective sample size **3,659.42**.
- Source: `experiments/kbs_plan_c/N9_ROUTE_B_B4A_A2_POPULATION_WEIGHTS_2026-10-14.json`. The frozen 20 cells exactly match A1 date and history-quartile definitions. These effective sizes measure weight dispersion, not independent unseen users.

**Primary three comparisons:** SASRec F-aligned − S-aligned, GRU4Rec F-aligned − S-aligned and original fixed Full Memory − mean of three frozen time-/activity-valid null Memory scores in the 4,096 nested group. Per-target same-candidate comparisons, weighted paired user-cluster 5,000-resample percentile 95% intervals and predeclared Holm correction across 3 directional tests; seed nulls must be averaged within each event before user resampling. User-cluster sign randomization for one-sided p-values retains the original G5 sign-symmetry assumption. Daily, call-rate, equal-cell and G5-user-disjoint contrasts are secondary. Actual B4-A sample author labels have not been opened; no p-values or B4-A ranking outcomes exist at A2.

## 4. Next-stage A3 eligibility and remaining HOLDs

- Locked main private sample digest: `be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14`; nested relation sample digest: `40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059`; old 47,575 G5 target event-ID overlap **zero**. No new collection-period data.
- A3 must execute as one *target-blind* historical stream, reuse fixed full-active TRAIN-known candidate rosters, original corrected fixed Memory scoring, frozen 12-feature schema and private 4 DEV-trained gate objects. At a selected source event, capture the history *before* processing the current author; append current event to history only for subsequent events. The current target author **must not be used to construct candidate set, predictive features, gate action or top-ten rank list**.
- Record prediction/top-ten/decision SHA first; only A4 with independently validated A3 hashes can read target label(s) once. Any future information, source timezone mismatch, dropped target request, private SHA change or scoring-path failure => HOLD without ranking-claim upgrade.
- **Dataset rights**: confirm the precise KuaiLive-M3 version's license, use of private interaction derivatives, anonymization safeguards, ability to perform new TEST processing, and permissible aggregation. Original G1 metadata and previous DEV training do not alone certify permission for new studies. Responsible human investigator approval remains pending.
- B4-A can provide **additional same-period held-out-target confirmation only**. It cannot be called future independent TEST, independent new-time cohort or cost-saving deployment test. Original G5 TEST and the 37-page manuscript/S1–S10 remain unchanged. Submission remains HOLD.

**A2 final result: PASS_DEV_ONLY_MODEL_AND_WEIGHT_FREEZE. A3: HOLD_PENDING_RIGHTS_AND_TARGET_BLIND_EXECUTION_GATE; A4: HARD HOLD_UNTIL_A3_SIGNED_FROZEN_PREDICTIONS.**
