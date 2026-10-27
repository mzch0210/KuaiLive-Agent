# N15 P1 — Equal-budget knowledge-use decision feasibility protocol

**Date 2026-10-27 · state: PROTOCOL_ONLY / NO EXPERIMENT RESULT.** P0 documents: `N15_P0_SCIENTIFIC_BASELINE_AND_RISK_REGISTER_2026-10-27.md` and `N15_P0_EXISTING_EXPERIMENT_EXCLUSION_AND_GATE_MATRIX_2026-10-27.md`.

## 1. Objective, data tier, and protected outcomes

Ask, without claiming method originality: on common event-time full-active candidate rosters and equal specialist-call quotas, how much full-F NDCG changes when the gate supervision target is uncorrected target-retained sampled-S vs full-active F relative Memory−Base utility?

DEV exploratory first: original 50,049 M3 Author DEV requests / 12,628 users; source `klm3_b1_full_dev_candidate_labels_seed20261012_v1/dev_pair_candidate_labels.csv`, SHA256 `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`; frozen Base/M. S uses exactly 575 retrospective target-retained candidate labels for offline training ONLY, never as inference feature. F uses complete active F labels. New policy evaluation uses common full-F candidate outcomes. No original G5 or B4-A TEST optimization, no claim of confirmatory inference from revisited DEV.

### Critical limitation surfaced from code review

- `analysis/kbs_plan_c/n9_b4a_a2_fit_dev_gate.py` fits OOF DEV gates and freezes scalar thresholds optimized to signed S or F **label** value; thresholds are not exact-call evaluation selectors.
- `analysis/kbs_plan_c/b1_nested_regime_transfer_dev.py` and `n9_g2_e1_supervision_decision_switches_dev.py` perform user-disjoint nested DEV and original full-policy comparisons. Existing post-G5 exploratory DEV is reused and highly analyzed.
- `N9_B1B_DECISION_CALL_FAIRNESS_AUDIT_PUBLIC_2026-10-14.json` computes net-call upper bounds, not actual equal-budget quality.
- **Per-request private evaluation rows and scores are not publicly available** in this repository. Public aggregate files alone cannot reconstruct exact matched allocations; do not infer or fabricate numerical outcome.

## 2. Proposed exact batch policy and estimand (offline, not online)

For a fixed partition of evaluation events into a batch `g`, a predeclared call count `k_g=floor(q*n_g)`, and a fixed gate scoring function `s_r(Z)` where `r ∈ {F,S}`, define `pi_{r,q,g}` as the indicator of the top `k_g` scores **within that batch**. Break score ties using a SHA256 ordering of stable, pretarget evaluation record keys and a registered seed; never using `Delta_F`, target identity or true label. (Do not publish the record keys.)

Default `q = 0.30`. The main output for architecture `b` is
`D_q^b = weighted_mean_g[u_F(B)+pi_F*(u_F(M)-u_F(B))] - weighted_mean_g[u_F(B)+pi_S*(u_F(M)-u_F(B))]`.
Also calculate the direct paired allocation form `weighted_mean[(pi_F-pi_S)*Delta_F]`; it MUST match within floating-point tolerance. Both policies call exactly `sum_g k_g` events. When weights vary, raw call equality does NOT guarantee weighted call-mass equality; report both and pre-register either **equal counts** (primary) or a separate **weighted-resource constraint**, not both conflated.

**Batch partition decision to freeze before execution:** for DEV feasibility, use the original user-disjoint *outer-fold* evaluation sets and batch by outer fold. Do not use labels of the evaluated fold to tune scores. For a later independent future cohort, define batches before collecting/revealing labels (e.g. day × history stratum, only if available pretarget) and measure any batch size/arrival-time lookahead. Under batch ranking, future request score access is an offline allocation assumption; do not call it causal real-time feasible.

### Important nested validation condition

Existing B1/G2 nested DEV fitting computes supervised policies and thresholds on outer training groups. The new P1 scorer must maintain that separation for outer validation; do **not** select scores/thresholds on the same outer fold using its full-F outcomes. To avoid mixing original B4-A final fitted-on-all-DEV models with DEV outcomes, regenerate DEV outer predictions only on approved private host, with original group splits / HGB model capacity, or verify matching frozen out-of-fold score files from original run. Do not use fitted-in-sample scores as cross-fitted evaluation.

Compare fixed F/S regression scores under *common downstream batch top-k*, not original separately calibrated thresholds. Label and model fitting access differ (F labels vs S labels), and this contrast is a total information-and-policy comparison, not a strict label-only randomized causal effect.

## 3. Diagnostic breakdown (predeclare before looking)

Partition decisions into both-call, F-only, S-only, neither. Under EXACT equal counts in each batch, counts of F-only and S-only equal per batch (ties resolved deterministically). Compute F-only vs S-only full-F incremental utility, paired weighted utility contributions, and user-cluster uncertainty as **descriptive DEV**. Do not conflate switched request fraction with fraction of Memory calls.

Conditional exploratory moderators (all pretarget): `x_candidate_log_count`, `x_memory_history_supported_share`, `x_hist_repeat_max`. Freeze discretization from outer-train partition or predeclared quantiles, never choose cut points to maximize outer-eval separation. Note the first variable is the F roster count and cannot isolate candidate ID/difficulty.

## 4. Source × supervision pilot

Start with fixed Full vs Long-only, because original `B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md` showed Long-only **larger** supervision regret than Full and weak popularity/history-null can have performance floor. For each source, use the same full-F candidates, pretarget features, user splits, F/S labels, HGB capacity, exact batch q, and independent source-specific training fits. Define `I_q = D_q(Full)-D_q(Long)` only after verifying the Full and Long source scores, features, provenance and utility scales. Compare absolute utility, positive-value support, and normalized/scaled sensitivity descriptively; no monotone historical-semantic claim. If original B2 data lack necessary complete per-event quality or matched information, mark NOT_IDENTIFIABLE_FROM_AVAILABLE_ARTIFACT and STOP, not produce surrogate numbers.

## 5. Input and leakage checks

Required private fields on DEV: stable *internal* pretarget event identifier, user cluster, allowed outer-fold ID, 12 original features, base full-F u10, memory full-F u10, S/F training labels, two cross-fitted scores per architecture/source, and eligible full roster size. Existing B1 and B2 source manifests and hashes must match. Request values must be finite, candidate roster consistent, no current positive in `Z`, no overlap of outer train/test users, no downstream leakage from label-to-score. No per-event uploads or private model files in GitHub.

Optional stratum weights require source-confirmed definition; do not apply B4-A twenty-cell population weights to the unrelated original DEV unless scientifically valid weights are established.

## 6. P1 analyses and reporting

- Main feasibility table: Base, source, q, n rows, user clusters, calls F/S, unweighted/weighted call rates, weighted/unweighted quality F/S, D_q, paired allocation identity residual, descriptive cluster interval.
- Decision exchange: both/F-only/S-only/neither counts and F-labelled delta utility summaries; tie frequency and deterministic-resolution audit.
- Original unmodified thresholds and original B1/G2 policies remain separate benchmarks for historical reconciliation, not pooled estimands.
- Source interaction: Full minus Long D_q, acknowledge baseline specialist strength and floor.
- Sensitivity q=.10, .20, .40 **only predeclared**; do not search quotas for positive effects.
- Report the sample-population, information-entitlement difference, offline nature, shared DEV reuse, and absence of real measured external resource scarcity.

## 7. Pre-execution feasibility conditions

- [ ] Restricted host source and model/artifact rights confirmed.
- [ ] Original full DEV csv SHA and B1/G2/B2 provenance matched.
- [ ] Original GroupKFold indexing, source time, user separation and HGB fit contract reproduced.
- [ ] Frozen cross-fitted scores available, or complete rerun on DEV approved.
- [ ] Batch partitions, `q`, tie-breaking and relative-value conventions frozen independent of outcomes.
- [ ] No TEST/B4-A revealed target labels touched for tuning.
- [ ] No private row/identifier/model export to public git.
- [ ] User-cluster and any sampling weight protocol verified.
- [ ] Source × supervision analysis input sufficiency documented.

**Gate P1 at document creation = METHOD_DESIGN_READY / PRIVATE_SOURCE_AND_HOST_EXECUTION_NOT_YET_VERIFIED / EXPERIMENT_NOT_RUN.** There are no new NDCG, confidence intervals or causal claims in this file.

## 8. Future independent test (P3) is separately gated

On *new eligible* held-out events, freeze batch definitions, q, model selection and novel multiplicity family independently from old B4-A 3-test Holm; never re-register old TEST results as a new confirmation. If no new data exist, only DEV exploratory evidence or bounded posthoc sensitivity is available.
