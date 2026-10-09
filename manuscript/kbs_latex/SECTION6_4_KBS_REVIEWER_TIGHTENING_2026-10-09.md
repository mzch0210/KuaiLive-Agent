# Section 6.4 — simulated KBS reviewer-style tightening

**Date:** 2026-10-09  
**Scope:** Section 6.4 in [canonical main.tex](main.tex) only; prior Sections 1–5 and 6.1–6.3, frozen Twitch test policy/results, and unstarted 6.5/7/8/Abstract remain unchanged.  
**Manuscript source revision:** [78fb4db3](https://github.com/mzch0210/KuaiLive-Agent/commit/78fb4db3b7235b67781772f313a3b0d25a7dd7b9).  
**Evidence:** [original 6.4 provenance](SECTION6_4_RESULTS_PROVENANCE_2026-10-09.md); [Twitch OOF ablation run 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454); [Memory robustness record](../../KBS_ROBUSTNESS_RESULTS_2026-09-22.md); [repaired context experiment](../../KBS_CONTEXT_LENGTH_INTERVENTION_REPAIR_2026-09-23_RUN35877647543.md); [Twitch base comparison](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35815886641); [KuaiLive base comparison](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35820514662).  
**Review character:** Internal simulated reviewer critique, not an actual KBS editorial decision.

## Verdict

Section 6.4 is useful as **development-only robustness and explanatory evidence** but does not constitute new held-out policy confirmation, causal mechanism isolation, or an exhaustive state-of-the-art baseline survey. The revised text corrects three potential reviewer misunderstandings while retaining every main-paper numeric value and the single feature-family table.

## Three high-priority reviewer questions

### R1 / P0 — Does the DEV OOF feature-family comparison overclaim independent evidence?

**Verified implementation:** `analysis/liverec_kbs_gate_feature_family_ablation.py` runs five-fold shuffled `KFold` with one unique target/user, fixed HistGradientBoostingRegressor hyperparameters, and exact top-K evaluation. The common **K=6,563** is the original **14-feature combined model's DEV-selected operating count**, not an exogenous or feature-neutral budget. The same source reports different family-wise development-optimized counts: history-only **11,249**, Base-score-only **3,282**, and combined **6,563**. The exact-K gains are history-only **+0.00371838** [**+0.00255879,+0.00490140**], Base-score-only **+0.00160204** [**+0.00048171,+0.00270223**], and combined **+0.00838098** [**+0.00713085,+0.00962655**]. Corresponding Spearman coefficients are **0.147905**, **0.091090**, **0.189896**.

**Reviewer vulnerability:** Equal invocation counts remove the call-frequency confound but do **not** establish that the combined features win across invocation budgets, quantify an interaction, or provide an independently validated feature-family ranking. The reported percentile bootstraps resample realized OOF event differences with predictions and selected K held fixed; they omit training, feature-selection and operating-point selection variability. The outcome used for selecting the full model's original DEV threshold was already observed on DEV. A common shuffled-user OOF design does not substitute for an additional chronological evaluation window. No adjustment for multiple exploratory comparisons is reported. Intervals versus Base are not pairwise confidence intervals *between* feature families.

**Revision:** The main paragraph and caption explicitly identify K's provenance and conditional CI interpretation, characterize ranks as observed at this count, state modest correlations, and avoid causal synergy or fresh TEST language. No ablation model, frozen policy, threshold or TEST result was changed.

**Useful next study, not already executed:** On DEV, predefine a small invocation-rate grid (e.g. 5%, 10%, 15%, 20%, 30%), evaluate all families at each common K with paired *between-family* intervals, and use nested training/threshold selection or a held-out DEV period if a general feature-superiority claim becomes central. Do not select a new frozen TEST gate from these exploratory findings.

### R2 / P0 — Can the context-length contrast separate visibility from changed Base quality?

**Verified repaired evidence:** The canonical Memory NDCG@10 is exactly invariant at **0.52170** across L=8,16,32 on identical **46,878 DEV** events. Independently retrained Base NDCG@10 rises **0.52619 / 0.57185 / 0.59663**. Observed-target visibility transitions are recoverable→represented: L8→L16 **n=5,055**, relative-utility change **−0.44748** (95% [−0.45767,−0.43730]); L16→L32 **n=3,617**, **−0.43229** ([−0.44381,−0.42054]). On these subsets and by construction, because the Memory ranking is held invariant, the difference is **exactly the negative of the Base gain**.

**Reviewer vulnerability:** Each change in maximum context is accompanied by a separately trained model with different learned weights and possibly different optimization dynamics. The transition groups are identified using the *realized target* and hence are non-deployable descriptive strata; conditional selection of such transitions further limits extrapolation to all users. Neither the sharp conditional contrast nor bootstrap CIs identify the causal effect of making an otherwise identical model see more history.

**Revision:** The main section now states the retraining confound, explains the algebraic identity, includes transition sample sizes, treats the result as *consistent with* reduced specialist headroom rather than proof of visibility causing it, and explicitly labels the states retrospective.

**Potential additional controls, not executed:** Same-checkpoint masking/cropping L32 to L16/L8 at evaluation to fix weights (noting masking introduces distribution shift); or train matched multi-seed L8/L16/L32 Base panels with identical tuning budgets and record both global and subgroup base performance. Neither can on its own guarantee identification of an isolated visibility mechanism.

**Recency challenge:** DEV bins are non-monotone: 1–4 **+0.04606**, 5–8 **−0.06511**, 9–16 **−0.15268**, 17–32 **+0.25668**, 33–64 **+0.20707**, 65+ **+0.12965**. Relationship distance can be confounded by repetition, user activity, candidate difficulty and composition; avoid monotone age or sole-mechanism claims. Detailed sample sizes/CIs are in the existing [robustness record](../../KBS_ROBUSTNESS_RESULTS_2026-09-22.md).

### R3 / P0 — Does the strong-base comparison implicitly promise a comprehensive SOTA benchmark?

**Verified logs/configurations:** The Twitch official LiveRec DEV Base scores **0.571853** NDCG@10 on the common candidate protocol. Auxiliary `GRU4Rec-small` **0.257268** and `SASRec-small` **0.171488** are 64-dimensional, one-layer small implementations trained **five epochs** at fixed learning rates, with restricted model search. Their weak results do not establish that the designated Base beats well-tuned sequential SOTA. The independent KuaiLive competitiveness bundle reports Dual-ID TEST **0.6171415** and Streamer-SASRec **0.6099278**, only **+0.0072138** apart, with a limited ReChorus model/grid survey including GRU4Rec and ContraRec-BERT4Rec. Its Dual-ID checkpoint is **not** the same as the Section 6.3 paired diagnostic Base (**0.6070916** sampled-active), and these absolutes must not be mixed.

**Reviewer vulnerability:** Calling these comparators *strong baselines* can invite requests for stronger or newer well-tuned encoders, transparent hyperparameter grids, comparable candidate pools/training input, seed dispersion, standardized TEST scores and resource reporting. In particular, a large LiveRec–SASRec gap after only five epochs is not evidence of SOTA dominance. The paper's core claim is **Base-relative decision value**, not a leaderboard claim, but the suitability and reproducibility of the designated Base still matter.

**Revision:** The final 6.4 paragraph treats the comparisons as *limited protocol-specific competitiveness checks*, explicitly flags narrow training/tuning and checkpoint identities, and refuses exhaustive SOTA/general-Base claims.

**Prioritized study, if submission completeness is challenged:** First publish exact model sizes, data eligibility, negative sampling, candidate alignment, tuned grid, epochs/early-stopping and seed protocol in Supplementary S3; then reproduce at least one well-tuned modern sequential reference per platform under the same candidate task (or provide a well-justified canonical implementation), with DEV-only model selection, paired final evaluation and Base-relative Memory/Utility effects. This is a new experiment requirement, not evidence currently in the repository.

## Preserved evidence and scope guards

- **OOF ablation:** 46,878 DEV events; K=6,563, distinct from the frozen Twitch TEST's **6,650** calls among **44,221** TEST events. The five-fold OOF comparison is an exploratory development analysis; bootstrap intervals remain conditional and unadjusted.
- **Memory configuration sensitivity:** Seven **evaluated configurations including the reference**, not seven departures from the reference; the three retrospective state signs persist while effect magnitudes change.
- **Context study:** Only results from the **repaired** aggregation are used; Memory identity is checked. Independently retrained Base checkpoints prevent causal interpretation.
- **Frozen policy:** 6.2 remains the only frozen one-shot Twitch TEST selector claim; the 6.3 same-TEST KuaiLive analyses remain post-hoc.
- **Missing work:** KuaiLive P2 candidate negative-sampling size/draw robustness was not run; submission supplementary assembly and coauthor approval remain pending. These are not silently claimed to be complete.

## Completion and publication gate

The subsection was source-edited in [commit 78fb4db3](https://github.com/mzch0210/KuaiLive-Agent/commit/78fb4db3b7235b67781772f313a3b0d25a7dd7b9), and the source-range update was restricted to the existing 6.4 block. **Post-revision LaTeX compilation is confirmed for that exact commit:** [Actions run 37884535058](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37884535058) completed successfully, with [PDF/log artifact 11596011574](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37884535058/artifacts/11596011574). The log reports a 26-page PDF, no fatal compilation errors, and only the pre-existing 5.51282-pt overfull line in earlier source lines 141--142. **Independent rendered-page visual inspection of the revised PDF remains pending**; do not conflate compilation with visual approval. The current revision does not create a new scientific run or prove journal acceptability.

Recommended supplement allocation: S3 (baseline competition), S4 (Memory component/sensitivity), S6 (context/recency), S7 (OOF feature families and calibration), and S8 (regime/seed robustness). Keep the main 6.4 table compact, but do not submit with merely a promise of future supplementary material.
