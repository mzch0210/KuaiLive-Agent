# B1 — candidate-regime utility-supervision transfer and decision-quality results

**13 October 2026. Status: B1-1, B1-2 and B1-3 COMPLETED / source and scientific-scope PASS.** Evidence class is **post-G5 exploratory, nested user-disjoint DEV**. These results are not registered G5 TEST, do not supersede the six-fit M3 TEST and do not constitute independent replication of a novel generic L2D algorithm.

## 1. Verifiable sequence and source provenance

1. [Full-score parity pilot #38363722383](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38363722383): **128/128** corrected F DEV events, SASRec, GRU4Rec and corrected Memory rank mismatches all **zero**; no retraining/TEST. Aggregate artifact `11795409087`, SHA256 `9443eae52b6adb0abb18552d2fc6d2011adf19c6d30347713676b0982da299b5`.
2. [CPU roster identity/speed pilot #38364127320](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38364127320): **256/256** event-time candidate lists and ordering identical to original; original 10.826 s, vectorized 10.661 s (1.015x); avoid claims of material speedup from a change that has little effect.
3. [B1 full paired-label generation #38364829652](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38364829652): **50,049 M3 DEV events, 12,628 users**, fully corrected F labels byte-verified and reused; deterministically generated 575-candidate target-retained offline S labels. Two frozen Base primary seeds plus fixed corrected Memory, output event rows only on private self-host. Public aggregate artifact `11796376302`, summary JSON SHA256 `4601415a482c7487c1d6294581113eeab03d97d136b0f44cdd208107e53efc60`. Private new paired event file SHA256 `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`. Original corrected DEV F CSV SHA256 `e144d9ed4c155b51a182a58150ea17d797b3eb4ee0dac0475ccba1d34f277e8f`.
4. [Nested B1 DEV policy transfer #38365477972](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38365477972): **SUCCESS**, 5 outer user-disjoint × 4 inner user-disjoint folds, same held-out full-active DEV events across arms, source commit `dd7082f262374c41e7fa1d24f62ed30c4d088e00`. Results artifact `11796876868`, summary SHA256 `30185ad09e15a2b742c7202718096ca507ae0f8cf5d26f832e8b43ddd5727357`. The first attempt failed **before fitting** due to self-host Python missing the previously verified offline scikit-learn path; restored `scikit-learn 1.5` through `e2-py312-sklearn-v1` and reran successfully without regenerating labels.

All phases: **no G5 TEST labels, no Base retraining, no uploading user identities or scores**.

## 2. Scientific target, arm access and exclusions

**Key problem:** Do sampled-candidate relative-utility labels provide the same constrained selection decisions when ranked candidates in fact cover all active TRAIN-known authors? Candidate membership is generated retrospectively from event-time eligible roster with a revealed target retained for **offline ranking label computation**. It is never an online decision-time feature or evidence of deployable target-retained sampling.

- **Pure S→F:** exactly twelve **F pre-outcome features**, learned delta target (u_S(M)-u_S(B)), and OOF threshold calibrated against **S labels only**. The S arm never uses F labels for fitting or threshold choice. F labels become available only to assess each held-out outer-user request.
- **F→F:** same twelve features, same HGB regressor capacity/hyperparameters and user splits; learned delta target and inner calibration both aligned to F.
- **Regime-adapted→F:** augments matched S and F training rows with a regime indicator and specified candidate log count, with **F labels available on outer-training DEV users**; its threshold is calibrated using F inner OOF labels. This is **in-domain adaptation**, not label-free domain transfer, and cannot be claimed superior to F→F.
- **Same original threshold objective:** (score\geq threshold), original `frozen_gate.select_threshold`, max 30% inner DEV OOF calls with indivisible ties. The **realized outer-F call fraction is not a forced 30% hard quota**.
- Fixed scikit-learn `HistGradientBoostingRegressor`: max_iter 120, LR .05, depth 3, leaf 50, L2 1, early stopping off. Primary fixed Base seed 20261012 in each of two families, same DEV users. 2,000 paired user-cluster percentile Bootstrap repetitions, descriptive; **no confirmatory G5 Holm family changed**.

## 3. Final decision quality on identical held-out full-active DEV ranking events

| Frozen Base | Arm | F-DEV NDCG@10 | Observed Memory calls | Rate |
|---|---|---:|---:|---:|
| SASRec | S→F | 0.296499 | 14,988 | 29.947% |
| SASRec | **F→F** | **0.302658** | 15,016 | 30.003% |
| SASRec | Regime-adapted→F | 0.301847 | 14,954 | 29.879% |
| GRU4Rec | S→F | 0.298123 | 15,001 | 29.973% |
| GRU4Rec | **F→F** | **0.303093** | 14,762 | 29.495% |
| GRU4Rec | Regime-adapted→F | 0.303000 | 14,989 | 29.949% |

**Fixed-policy full-active DEV references:** SASRec Always Base 0.258167, GRU4Rec Always Base 0.258971; Always Memory 0.343509 for both. Consequently, selection still does **not** establish superiority to unconditional Memory under unconstrained rank accuracy.

**Primary exploratory nested contrasts (difference in F NDCG@10, 95% paired user-cluster CI):**

| Comparison | SASRec Δ [95% CI] | GRU4Rec Δ [95% CI] |
|---|---|---|
| **F→F minus S→F** | **+0.006159** [0.004835, 0.007543] | **+0.004970** [0.003550, 0.006369] |
| **Regime-adapted→F minus S→F** | +0.005349 [0.004187, 0.006537] | +0.004877 [0.003653, 0.006106] |
| **Regime-adapted→F minus F→F** | **−0.000811** [−0.001590, −0.000055] | −0.000093 [−0.000920, 0.000758] |

All five individual outer validation folds have a positive **F→F minus S→F** quality difference in both Base families. These are matched cohort differences with user-cluster intervals; **they do not constitute independent unexposed TEST hypothesis confirmations**. SASRec F→F invokes Memory 28 more times than S→F, so its quality advantage is **not exactly equal-call**. GRU4Rec F→F uses **239 fewer Memory calls** while also ranking better than S→F. The regime-adapted strategy does **not** improve over F→F: for SASRec the exploratory interval for adapted-minus-F is negative; for GRU4Rec it crosses zero.

## 4. Full-cohort label shift and the knowledge-system R3 argument

| Full-cohort aggregate | Full-active F | Sampled S (575, offline retained target) |
|---|---:|---:|
| SASRec | 0.258167 | 0.646796 |
| GRU4Rec | 0.258971 | 0.643327 |
| Fixed Memory | 0.343509 | 0.668498 |
| Memory minus SASRec | **+0.085342** | **+0.021702** |
| Memory minus GRU4Rec | **+0.084538** | **+0.025171** |

The percentage of events whose **three-way sign category** (negative/zero/positive) differs between sampled and full environments is ~53.8% for each Base, **including changes to/from zero**. It must **not** be described as a 53.8% pure positive-to-negative sign reversal rate. The scientific claim with firmer evidence is the matched **actual policy-regret** contrast above, not a generic already-known sampled metric shift.

**Interpretation:** The experiment directly links (i) the candidate regime used to define relative Memory–Base NDCG labels and (ii) the quality of subsequent Memory-selection decisions when evaluated on full-active author rankings. Supervision aligned to F obtains higher held-out F utility than S supervision with the same Base, expert, predictor features and user folds. This constitutes **new exploratory support for the RQ2→RQ3 link** in the M3 task, improving the current paper's integrated knowledge-value account beyond the original cross-task juxtaposition. It is **not** a new generic learn-to-defer theorem or proof that candidate-aware learning beats F→F.

**Identification boundaries:** S is a target-retained offline metric/candidate design and does not represent a demonstrated live online candidate generator; S and F differ in number **and identity/composition/competition**, so no isolated causal effect of candidate count is proved. The study uses one trained SASRec and one GRU4Rec primary seed and one shared DEV cohort; it remains susceptible to post-G5 exploratory analysis decisions. B2 Short/Long/popularity and relationship-placebo controls are needed to verify whether the phenomenon is special to persistent relationship knowledge rather than a generic ranker comparison. Actual full-path Memory inference costs and deployment scarcity are not validated.

## 5. GPU/CPU experiment-efficiency assessment

The full 50,049-event S-label construction was executed in **113.08 wall seconds** on the self-host rather than recomputing each full-candidate ranking: one corrected causal history scan (38.15 s), one event-time active roster + sampled corrected Memory pass (72.23 s), both frozen Base checkpoints / full DEV context encoders (1.68 s), and only **0.50 s sampled-candidate GPU scoring/rank phase**. GPU peak allocated memory **594.8 MiB**, batch **512**. The small CUDA busy fraction is expected because the useful sampled scoring task is tiny relative to CPU history/interval preprocessing. **Optimizing useful wall time rather than artificially saturating GPU is the correct resource objective.**

The nested HGB fitting on the same paired DEV source completed in **8.72 CPU seconds** for SASRec and **8.65 CPU seconds** for GRU4Rec. It does not consume GPU to fit the gate. The prior isolated GPU-only matrix batch throughput improved about **6.9×/4.4×** when batch increased from 12 to 256 for SASRec/GRU4Rec, but this is not a blanket wall-time speedup guarantee.

## 6. Research decision and next stage

**B1 implementation & nested DEV science gate: PASS. R3 integrated-contribution risk: PARTIALLY MITIGATED, NOT CLOSED.** The full-active candidate-supervision mismatch produces an interpretable downstream policy-quality penalty and in-domain adaptation can largely recover performance, but it does not improve on directly using F targets and is not original independent TEST evidence.

**Recommended next research action: B2 identity-specific evidence ablation**, keeping the same F/S DEV events, user outer folds, Base fits and eligible candidate protocols. Compare full Short/Long/Popularity Memory with Long-only, Short-only, popularity-only and a legitimate user–creator-history permutation placebo. B2 is needed to show whether this measurable transfer link reflects *relationship knowledge* rather than candidate-sensitive ranker selection in general. Only if B2 demonstrates persistent nontrivial value and genuinely new unseen/authorized cohort becomes available should a new pre-frozen TEST and a substantive KBS main-text revision be undertaken.

**Main manuscript, S1–S9, original G5 TEST and original R0 claims were not modified by B1.** Results remain in an independent experimental scientific audit until an explicit manuscript revision decision is taken.
