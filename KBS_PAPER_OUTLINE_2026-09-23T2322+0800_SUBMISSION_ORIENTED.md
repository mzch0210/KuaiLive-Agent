# Submission-oriented manuscript outline for *Knowledge-Based Systems*

> **INDEPENDENT / NON-AUTHORITATIVE MANUSCRIPT OUTLINE**  
> This document is a paper-facing writing outline. It does not replace frozen experimental protocols, immutable test results, or prior authoritative experimental snapshots unless explicitly promoted by the authors.

**Updated:** 2026-10-08  
**Target journal:** *Knowledge-Based Systems*  
**Project:** `mzch0210/KuaiLive-Agent`

---

# Proposed title

## Preferred

> **When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation**

## Conservative alternative

> **Base-Relative Value of Relationship Memory in Live-Streaming Recommendation**

The title should foreground the scientific question and the Base-relative valuation concept rather than generic routing, gating, or memory architecture.

---

# Abstract

Structure the abstract around one scientific question, one mechanism result, one decision result, and one held-out validation result.

1. **Problem.** Strong sequential recommenders process bounded or compressed histories. A fixed auxiliary specialist may have positive, zero, or negative operational ranking value relative to the base, depending on the candidate regime and event; this difference is not an intrinsic measure of evidence information.
2. **Operationalization.** Instantiate persistent relationship evidence through a transparent relationship-memory specialist and measure its event-level marginal ranking utility relative to a strong base recommender. Avoid implying that the measured quantity is an intrinsic, model-independent information value of history.
3. **Mechanism.** Characterize represented, recoverable-but-unrepresented, and unavailable relationship evidence; report development analysis, untouched held-out test replication, and context-capacity comparisons across independently retrained bases. Visibility transitions are associated with changes in relative utility but do not isolate visibility as their sole cause.
4. **Decision.** Estimate conditional specialist-minus-base utility rather than generic base difficulty; show that Utility more strongly enriches recoverable events whereas Difficulty disproportionately selects unavailable events under the same invocation budget.
5. **Validation.** Report the KuaiLive regime reversal reproduced by a completed same-checkpoint/same-alpha post-hoc diagnostic (paired full-minus-sampled Memory−Base `+0.08751`, 95% CI `[+0.08183,+0.09311]`), alongside the independently frozen Twitch/LiveRec held-out policy benefit.
6. **Qualification.** A candidate-set swap also changes candidate-wise score standardization; this diagnostic is observational rather than isolated causal identification, uses one newly trained checkpoint pair, and does not upgrade the historical test to new confirmatory evidence. The recoverable-but-unrepresented group's relative advantage *shrinks* in full-active, so the aggregate reversal is not a simple long-history-recovery effect. Specialist value is operational and considerable Oracle headroom remains.

Prioritize two headline quantitative anchors in the abstract rather than a dense result list:

- **Candidate-regime evidence (supporting post-hoc diagnostic):** under one fixed checkpoint pair and DEV-selected alpha, full-minus-sampled Memory−Base is `+0.08751` NDCG@10 (95% paired CI `[+0.08183,+0.09311]`).
- **Frozen held-out decision:** on untouched Twitch/LiveRec TEST, Selective Utility improves on Base by `+0.00772` NDCG@10 and on exact-count Difficulty by `+0.00644`.

Keep the `0.42–0.45` context-capacity association as a central Section 6.2 mechanism finding without overstating visibility causality.

Avoid introducing the paper as a new gating architecture, new Memory network, generic Learning-to-Defer method, or universal theory of information value.

---

# 1. Introduction

The formal manuscript Introduction is the canonical guide for this section. Do not reintroduce an explicit RQ list into the main text.

## 1.1 Motivation and scientific gap

Establish the following sequence:

1. Strong sequential recommenders represent recent or compressed interaction history.
2. Auxiliary evidence can be redundant, unavailable, or complementary relative to that representation.
3. Existing work extensively studies how heterogeneous evidence should be integrated, selected, denoised, or weighted; a distinct question is whether a fixed auxiliary specialist contributes positive marginal ranking utility relative to the current base for a specific event.
4. Persistent user–creator relationships in live-stream recommendation provide a transparent empirical setting in which target-specific evidence may already be represented, remain recoverable from older history, or be unavailable.
5. This motivates **Base-relative evidence valuation**, operationalized through a transparent fixed specialist rather than interpreted as intrinsic information value.

Use the central sentence:

> **The central problem is whether a fixed specialist instantiated from historical relationship evidence improves ranking relative to the trained base on a given event and candidate regime.**

## 1.2 Empirical motivation

Preview only three facts:

- aggregate specialist ordering reverses across KuaiLive candidate regimes, with a completed post-hoc same-checkpoint, same-alpha paired shift of `+0.08751` (95% CI `[+0.08183,+0.09311]`);
- conditional evidence-state structure identified in pre-specified Twitch/LiveRec development analysis reproduces on untouched held-out test data;
- in a development-only context-capacity comparison, matched instances moving from recoverable to base-input-visible exhibit approximately `0.42–0.45` lower specialist-minus-base NDCG@10; Memory is fixed but each Base is separately trained, so the decline reflects Base improvement and is consistent with, not an isolated test of, a visibility interpretation.

Do not reproduce the full result matrix in the Introduction.

## 1.3 Contributions

Use exactly three headline contributions.

### C1 — Operational Base-relative valuation

> Quantify the event-level marginal ranking utility of a fixed, transparent relationship-memory specialist relative to a strong base, without treating this difference as model-independent information content of history.

### C2 — Conditional relationship-evidence structure

> Characterize retrospective target-history visibility and recency; examine their association with specialist-relative utility across regimes, and corroborate the structure through untouched held-out replication and context-capacity comparisons of separately trained bases, without claiming isolated visibility causality.

### C3 — Conditional decision and validation

> Estimate specialist-minus-base utility for pre-outcome selection and test its value relative to predicted base-difficulty controls across KuaiLive regimes, independent training seeds, and an untouched Twitch/LiveRec held-out test.

End the Introduction with a scope sentence: the formulation can describe fixed auxiliary specialists more generally, but the empirical claims remain limited to the evaluated live-stream platforms, candidate protocols, and ranking outcomes.

Do **not** claim novelty for generic gating, mixture-of-experts, Learning-to-Defer, long/short-term modeling, evidence selection, multimodal fusion, or the weighted relationship-memory formula itself.

---

# 2. Related Work

Organize Related Work around nearest conceptual neighbors, using one concise positioning statement per subsection rather than repeated defensive contrasts.

## 2.1 Sequential and long-horizon recommendation

Cover strong sequential encoders and later work that broadens or enriches historical representation, including recent intent-driven augmentation (IDMARec, KBS 2025) and multi-interest / multi-granular modeling (DSMGRec, KBS 2025).

Positioning boundary:

> The contribution is not broader history encoding; it is an empirical and decision-focused analysis of the ranking-utility advantage of a separately scored relationship-evidence specialist over a trained base.

## 2.2 Auxiliary evidence integration, selection, reliability, and harmful information

Cover:

- adaptive multi-source and long/short-term fusion;
- multimodal complementarity, redundancy suppression, and denoising;
- reliability-aware evidence modeling;
- preference-relevant evidence selection, including KAPER-style path evidence selection;
- conditional evidence gating;
- negative transfer / harmful auxiliary information;
- value-of-information as a decision-theoretic conceptual neighbor.

Positioning boundaries:

> Evidence integration or selection asks how information should be represented, filtered, or used downstream; **Base-relative evidence valuation asks what operational marginal ranking value a fixed auxiliary specialist contributes relative to a trained base.**

> Evidence reliability does not imply positive Base-relative marginal utility, and the current formulation does not claim model-independent intrinsic information value.

## 2.3 Expert routing, selective prediction, and Learning-to-Defer

Acknowledge post-hoc deferral, two-stage expert allocation, multiple-expert routing, and cost-sensitive decision making as established problems.

State explicitly:

> The paper does not propose new general deferral theory. It studies the conditional marginal ranking value of one transparent recommendation specialist and uses an estimator of that quantity for selective invocation.

Difficulty remains a **mechanistic control**, not a representative baseline for all L2D methods.

## 2.4 Live-streaming and repeat-aware recommendation

Cover dynamic availability, viewer–streamer interactions, repeated viewing, interaction decay, and richer viewer–channel relation modeling.

Positioning boundary:

> Live streaming supplies the empirical environment in which Base-relative relationship evidence can be studied; repeat modeling itself is not the methodological novelty.

## 2.5 Positioning summary table

Retain a compact three-column table:

| Research line | Primary objective | Difference in focus |
|---|---|---|
| Sequential / long-horizon recommendation | Encode broader history | Residual utility of a separate relationship-evidence specialist |
| Auxiliary fusion / evidence selection | Integrate, filter, or select evidence | Operational marginal ranking value relative to a trained base |
| Reliability / denoising | Estimate trustworthiness or informativeness | Reliable evidence may still be redundant relative to the base |
| Value of information | Quantify benefit of acquiring information | Ranking contribution of an already defined fixed specialist |
| L2D / expert routing | Assign instances to predictors/experts | Characterize the utility structure of one interpretable evidence specialist |
| Live-stream recommendation | Model dynamic availability and repeat behavior | Empirical setting for Base-relative evidence valuation |

The purpose is precise differentiation, not a claim that adjacent work is absent or inferior.

---

# 3. Problem Formulation

The revised LaTeX manuscript is canonical for Section 3. Reserve (m) for the invoked-event count and use (\Delta_M) for Memory-minus-Base utility throughout; retain only general selection mathematics here, while DEV/OOF details belong to Section 5.

## 3.1 Recommendation setting and event-level ranking utility

Distinguish the pre-outcome decision context

\[
\xi=(u,t,\mathcal C_{u,t},\mathcal H_{u,t})
\]

from the evaluated event `x=(ξ,y)`. Under candidate regime `r`, use `ξ_r=(u,t,C^{(r)}_{u,t},H_{u,t})` and `x_r=(ξ_r,y)`. The same underlying user–time–target instance can yield distinct full ranking events under alternative candidate sets. Models and selectors receive `ξ_r`, not the observed target `y`.

For one relevant target at cutoff `K`, define event-level NDCG utility:

\[
u_K(A,x)=
\begin{cases}
1/\log_2(r_A(y\mid\xi)+1), & r_A(y\mid\xi)\le K,\\
0, & r_A(y\mid\xi)>K.
\end{cases}
\]

Because rank utility is candidate-set relative, candidate construction can alter Base-relative specialist value even when underlying user–target history is unchanged.

## 3.2 Base-relative specialist utility

Define

\[
\Delta_M(x)=u_K(M,x)-u_K(B,x).
\]

Interpretation boundary:

> `Δ_M` is the **operational marginal value** of persistent relationship evidence as instantiated by fixed specialist `M` relative to fixed base `B`; it is not intrinsic or model-independent information value.

## 3.3 Conditional relative utility

For regime `r` and deployment-observable information `z`:

\[
\eta_r(z)=\mathbb E[\Delta_M(X)\mid Z=z,R=r].
\]

`R` indexes the event-generating/evaluation condition and need not be a selector feature. Analysis-only evidence-state labels, target `y`, realized ranks, and realized `Δ_M` are excluded from `Z`.

For a serving action `a`, define selective utility in prose or inline and retain the expected-gain identity:

\[
\mathbb E[u_K^{sel}-u_K(B)\mid R=r]
=
\mathbb E[a(Z)\eta_r(Z)\mid R=r].
\]

This is the decision rationale for predicting conditional relative utility rather than generic base difficulty.

## 3.4 Selective invocation and equal-count comparison

Define the primary learned policy as a **development-frozen pointwise threshold** on estimated conditional relative utility:

\[
a_{\tau_r}(z)=\mathbf 1[\hat\eta_r(z)>\tau_r].
\]

Select \(\tau_r\) using out-of-fold development utility; fit the final regressor on development data and freeze both model and threshold before held-out test access. The realized held-out invocation count is an **outcome of the fixed policy**, not a predetermined exact budget.

For matched comparison, let \(m=\sum_i a_{\tau_r}(z_i)\) be the frozen utility policy's realized evaluation-set invocation count. The Difficulty control uses **top-\(m\)** predicted base-difficulty scores, and the analysis-only Oracle uses **top-\(m\)** realized \(\Delta_M\) values. Both are **offline, batch-level matched-budget controls**; neither is the serving rule of the primary Utility selector. Use deterministic tie-breaking.

The frozen Utility threshold is sensitive to the score distribution; it is not calibration-free. Offline top-\(m\) controls require only an ordering, but assume the evaluation batch is available. An unevaluated cost-optimization equation was removed from the main Problem Formulation; serving-cost extensions belong in the later Discussion as prospective work rather than an asserted empirical contribution. Avoid claiming online hard-budget guarantees or a new routing theorem.

## 3.5 Regime-level decomposition

Let `S` be a mutually exclusive and exhaustive partition of Base-relative evidence states. Then

\[
\mathbb E[\Delta_M\mid R=r]
=
\sum_sP(S=s\mid R=r)\,\mathbb E[\Delta_M\mid S=s,R=r].
\]

This separates evidence-state composition from state-specific specialist utility. Treat it as analytical decomposition, not causal theory.

---

# 4. Base-Relative Evidence Valuation Framework

Section 4 is an implementation and design-rationale chapter, not a second problem formulation or an experiment log. Reuse the Section 3 definitions of \(B,M,Z,S,\Delta_M,\hat\eta_r\) without rederiving them. The methodological distinction is an **operational comparison of ranking utility between a separately specified relationship specialist and a credible fixed base**. Such a comparison does not by itself identify intrinsic evidence information, model-independent complementarity, or a new memory, HGB, or deferral algorithm.

Explain three linked design choices: (1) a strong fixed Base is a meaningful ranking reference; (2) separately scored relationship history permits analysis of short-term, long-term, and popularity evidence; and (3) development-supervised relative-utility prediction tests whether this specialist's conditional contribution informs pre-outcome decisions. Do not claim model-independent intrinsic evidence value or causal identification.

## 4.1 Strong sequential base recommenders

Describe KuaiLive Dual-ID with room and streamer branches, candidate-wise standardization, and room-level prediction target. For Twitch, describe official LiveRec with context and repeat components enabled, the 16-interaction main input, and temporal streamer availability. Preserve separate base training for different context lengths and do not treat changing input length as an isolated visibility intervention. Leave SOTA/comparator results to Sections 5–6.

## 4.2 Transparent relationship-memory specialist

Use the fixed score

\[
s_M=0.45\,Short+0.45\,Long+0.10\,Popularity.
\]

Define Short as the maximum exponentially decayed strength over at most ten most recent visits (decay scale three); Long as creator count normalized by the user's highest creator count; Popularity as log1p train-eligible counts scaled over observed creators. Explain deterministic ties and room-to-streamer mapping. An unavailable target-specific relationship may still yield a nonzero popularity score.

**History timing must follow the relevant protocol.** According to official LiveRec documentation, start and stop are the first and last ten-minute crawl steps at which a user was observed in a streamer's chat, rather than verified session-entry or completion instants. Primary Twitch P1.2/P1.3 exports include records observed before the target step (start earlier than target), whereas popularity is based on records last observed before the training boundary. Auxiliary strict-split analysis additionally restricts its pool by last-observed step before the split endpoint, then by first-observed step before target. Do not mix these retrospective eligibility rules or claim sub-interval real-time observability; retain a temporal-resolution limitation.

Present the weighted specialist as a transparent evidence carrier, not a new memory network or an intrinsic information-value function.

## 4.3 Base-relative relationship-evidence states

Operationalize target-relative visibility \(V_L(x)\) in the base input and relationship presence \(H(x)\) in protocol-eligible history. The mutually exclusive and exhaustive states are represented (shorthand for input-visible, not proven learned internally), recoverable-but-unrepresented, and unavailable. Do not assume universal utility signs.

State and target-relative interaction distance are retrospective analysis variables, never selector inputs. The exact history-eligibility rule should match the platform and analysis protocol.

## 4.4 Observable features and conditional relative-utility estimation

Specify six history descriptors and eight Base-score descriptors for the 14-feature Twitch estimator. Score descriptors are statistics, not calibrated uncertainty probabilities. Temporal regularity uses a 144-step phase. The top-10/top-11 margin requires at least 11 eligible candidates; the export checks this.

The percentile reference is **platform-specific**: Twitch uses a full unlabeled DEV empirical distribution shared across OOF folds and applied to TEST, while KuaiLive derives history-feature ranks from split-eligible pre-target history pools. Neither uses TEST target labels to fit the selection rule. Describe HGB configuration (200 iterations, learning rate 0.05, depth 3, minimum leaf size 50, L2 regularization 1). Five-fold OOF DEV predictions support **supervised threshold selection**, not an unbiased evaluation of the learned threshold. Train the final estimator on DEV; freeze estimator, features, transforms and threshold before untouched TEST.

Distinguish the two kinds of transfer:
- **KuaiLive candidate-regime strict transfer:** sampled-active estimator and threshold retained under full-active candidate construction, versus separately developed native full-active policy.
- **Twitch cross-platform validation:** Memory structure and weights reused, but the utility estimator and threshold fitted on Twitch DEV. This reproduces the principle across platforms; it is not zero-shot transfer of gate parameters.

The primary Utility selector uses a development-frozen pointwise threshold. Its held-out quality depends on decision utility and score-scale stability, unlike offline equal-budget ranking controls that depend only on score ordering.

## 4.5 Specialist selection and matched-budget controls

Describe serving and offline evaluation without rederiving Section 3. Serving-like execution calculates the Base and observable features before conditionally invoking the specialist; offline analysis scores both rankings.

- **Utility:** DEV-frozen threshold, with realized held-out invocation count.
- **Difficulty:** HGB trained on Base loss using the same observable feature family; select offline top-m predicted difficulty cases matching Utility's realized count.
- **Oracle:** offline top-m realized specialist-minus-base utility, never deployable.

Move extensive freeze chronology, base comparisons, statistical inference, and hardware metrics to Sections 5–6 or Supplementary. Avoid claiming calibrated event-cost optimization or a deployed real-time system.

---

# 5. Experimental Setup

**Publication function.** Present an intelligible and reproducible research design, not a chronology of experiment development. Maintain a clear distinction between the originally frozen policy evaluation and subsequent post-hoc diagnostic evidence, without importing run logs or reviewer-defense language into the main text. The canonical English LaTeX Section 5 has been structurally rewritten and compiled; this outline must follow that five-subsection design.

## 5.1 Datasets and Prediction Tasks

Describe KuaiLive (next-room targets, streamer-level memory identity, per-user leave-last-two-out, 10,222 DEV/TEST matched events, sampled-active 575-room versus full-active candidates) and Twitch/LiveRec (next-streamer targets, ten-minute crawl observations, chronological availability, 46,878 DEV and 44,221 TEST targets, 16-step base context). Explain the training-only popularity prior, target-eligible past history and distinct observation semantics, avoiding unwarranted negative-preference or precise viewer-session claims.

**Table 1 — Primary datasets and evaluation settings.** One row per platform; columns identify ranking unit, target-based split and candidate construction, and DEV/TEST event counts. Supplementary protocol records complete TRAIN/DEV/TEST scale and date/candidate distributions once independently audited.

## 5.2 Baselines and Compared Methods

Identify the strong platform-specific references: KuaiLive Dual-ID SASRec (with room and streamer branches) and Twitch LiveRec, supported by KuaiLive popularity, single-branch SASRec, GRU4Rec and ContraRec--BERT4Rec controls. Cite Section 4 for Memory's fixed Short/Long/Popularity definition instead of rederiving it. Compare Always-Base, Always-Memory, selective Utility, equal-count Difficulty and hindsight Oracle. State the Oracle's hindsight status once and explain that learned gates are independently fit on each platform's DEV set.

**Table 2 — Compared methods and experimental roles.** Organize rows by scientific purpose, not by the execution status of workflows.

## 5.3 Experimental Protocols

Briefly describe data-split model fitting, DEV-selected fusion and Utility thresholds, main one-event-per-user OOF KFold versus global-time user GroupKFold, test-time parameter freezing, and dataset-specific history-feature reference transformations. Organize regime experiments as native sampled/full, strict transfer, and a paired same-checkpoint candidate-swap with matched users, fixed weights/alpha/history, full-set raw scores and sampled subsetting. Define the paired delta by Equation eq:paired-regime-shift. **One necessary inference boundary:** the paired swap changes candidate membership and candidate-wise normalization together, and was a retrospective supporting diagnostic rather than a new untouched test. Keep hashes, alphas, running times and artifacts in the Supplementary Material.

## 5.4 Evaluation Metrics and Statistical Analysis

Specify NDCG@10 (one target per event), HR@10, invocation frequency, per-user paired contrasts, 95% percentile bootstrap and user-cluster resampling for multi-event data. The original candidate-swap uses 3,000 user-resampling replicates. Distinguish between-user bootstrap uncertainty and independent checkpoint-seed variation; exploratory subgroups do not warrant unadjusted multiple-confirmation claims.

## 5.5 Implementation Details

Report only necessary core settings: ReChorus SASRec base (64-dimensional embeddings, one attention layer, four heads, length 50), Twitch LiveRec context/repeat configuration (length 16), and HGB estimator configuration (200 iterations, 0.05 rate, depth 3, leaf minimum 50, regularization 1). Full implementation commits, data preprocessing logs, run IDs, checkpoint manifests and extended robustness matrices belong in the Supplementary Material. Do not suggest that offline invocation rate establishes deployment latency.

**Related audit:** [Sections 1–4 retrospective academic assessment](manuscript/kbs_latex/SECTIONS1-4_RETROSPECTIVE_ACADEMIC_AUDIT_2026-10-08.md). Its P0 symbol and fusion-weight consistency items remain open until checked against the entire manuscript and applied consistently.

---

# 6. Experimental Results

Order results around empirically testable propositions, not the chronology in which GitHub workflows ran. Section headings state findings without implying causality. Use **held-out TEST** for frozen policy performance and **DEV/diagnostic** for supplementary mechanisms.

## 6.1 Candidate-regime reversal persists under a fixed checkpoint pair

**Scientific role.** Test whether candidate-regime sensitivity survives controlling the historical model-checkpoint and fusion-weight mismatch. Distinguish (A) historical regime-specific operational comparisons from (B) the completed, single-checkpoint post-hoc diagnostic. Neither is a randomized trial isolating candidate membership from candidate-wise score normalization.

**A. Historical observation (frozen protocol; not pooled with B).** On 10,222 matched KuaiLive events, the frozen regime-decomposition record reports sampled-active Base `0.61714`, Memory `0.56589`, Memory−Base `−0.05125`; native full-active Base `0.39835`, Memory `0.43202`, Memory−Base `+0.03367`. Another planning-context sampled Base `0.60784` remains separately attributed until its exact checkpoint, fusion coefficient, and source artifact are reconciled. Historical regime parameters need not coincide.

**B. Completed same-checkpoint diagnostic (supporting evidence).** [GPU run 37746520476](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476); artifact ID `11536890439`; `n=10,222` matched users/events, `alpha_room=0.125` selected on sampled DEV, one newly trained room+streamer checkpoint pair, identical Memory definition, and 3,000 paired user-bootstrap replicates. Sampled events are a verified subset of the corresponding full-active candidates; model hashes and event identities are recorded.

| NDCG@10, *new paired protocol* | Sampled-active | Full-active |
|---|---:|---:|
| Base | 0.60709 | 0.38571 |
| Memory | 0.56589 | 0.43202 |
| Memory−Base | **−0.04120** | **+0.04631** |
| 95% paired bootstrap CI for Memory−Base | [−0.04820, −0.03414] | [+0.03978, +0.05297] |

**Full-minus-sampled Memory−Base shift: `+0.08751`, 95% paired user-bootstrap CI `[+0.08183,+0.09311]`.** The reproduced sign reversal rules out historical *between-regime checkpoint/alpha mismatch* as necessary for this new diagnostic's reversal. It does not isolate candidate membership as a causal mechanism. The new Base values do not replace historical Base anchors and were never used to reselect frozen-policy thresholds.

**C. Fixed evidence-state composition; differential conditional shifts.** The target-relative states are unchanged across paired candidate regimes, so prevalence cannot explain the reversal in this matched population:

| Retrospective state | n (share) | Sampled Δ | Full Δ | Full-minus-sampled paired shift [95% CI] |
|---|---:|---:|---:|---|
| represented | 4,589 (44.89%) | +0.12859 | +0.21650 | **+0.08790** [+0.08023,+0.09557] |
| recoverable-but-unrepresented | 206 (2.02%) | +0.18445 | +0.08248 | **−0.10197** [−0.15224,−0.05221] |
| unavailable | 5,427 (53.09%) | −0.19335 | −0.09898 | **+0.09437** [+0.08602,+0.10214] |

The weighted shift decomposes as `+0.03946` (represented), `−0.00205` (recoverable), and `+0.05010` (unavailable), totaling `+0.08751`. Hence the shift is driven primarily by increased represented relative gains and *less negative* unavailable cases, **not** increasing recoverable prevalence or benefit. Do not describe the KuaiLive reversal as evidence that full-active provides more long-horizon relationship information. The recoverable group's conditional Memory advantage remains positive but is smaller.

**Main Figure 2.** Prefer separate panels for (A) historical operational contrasts and (B) new matched-checkpoint paired contrasts/CIs; show subgroup shifts in a compact Figure 2C or supplementary table. Label old/new model identities and candidate rules. Avoid putting two configurations into an apparently unified paired series.

**Limitations and staged follow-up plan (PROPOSED; not executed).** The completed controlled result uses a single newly trained checkpoint pair/seed, an already-studied TEST population, and candidate-wise standardization that co-varies with candidate membership. The efficiency-optimized [follow-up experimental plan](KBS_KUAILIVE_FOLLOWUP_EXPERIMENT_PLAN_2026-10-08.md) prioritizes (P0) a no-retraining four-cell candidate/reference-normalization decomposition with an exact algebraic attribution, then (P1) two additional training seeds under fixed alpha and cached-data/checkpoint reuse, with (P2) negative-sampling sensitivity only if needed. All remain post-hoc supporting evidence; do not insert results into Sections 5–7 before execution and audit.

## 6.2 Relationship-evidence states and relative utility

**Twitch pre-specified DEV → untouched TEST replication.** State-conditional Memory−Base (DEV → TEST):
represented \\(-0.01995\\) → \\(-0.01935\\); recoverable \\(+0.23097\\) → \\(+0.22045\\); unavailable \\(-0.19562\\) → \\(-0.18215\\). Never universalize state-specific signs.

**Context-capacity association (DEV only).** Show separately trained LiveRec Base contexts \\(L=8,16,32\\) with Memory held canonical and identical: Base NDCG@10 \\(0.52619,0.57185,0.59663\\), Memory NDCG@10 \\(0.52170\\). Matched recoverable-to-represented transitions have specialist-minus-base changes \\(-0.44748\\), \\(-0.43229\\) and \\(-0.41896\\). Explicitly note the algebraic opposite Base-utility changes when Memory is fixed; context-length and retraining co-vary.

**Main Figure 3 — Relationship-state and context-capacity evidence.** Panel A DEV/TEST conditional differences; Panel B context lengths and transition estimates, displaying both Base improvement and Memory−Base contraction. No causal arrow labeled “visibility effect.”

Place Short/Long/Popularity component attribution and nonmonotonic recency refinements in a concise paragraph; extended tables in Supplementary.

## 6.3 Utility-based selection differs from base difficulty

**Matched-count comparison.** Distinguish the frozen Utility pointwise threshold from offline Difficulty top-\\(m\\) and Oracle top-\\(m\\). Report realized TEST invocation rate and NDCG@10, H@10 with paired intervals for Utility–Base and Utility–Difficulty.

**Selection-composition explanation (Twitch DEV).** Recoverable selection enrichment \\(2.72\\times\\) for Utility versus \\(1.67\\times\\) for Difficulty; unavailable event enrichment approximately \\(1.03\\times\\) versus \\(1.91\\times\\). Emphasize interpretation: difficulty is not the same as specialist solvability. Analysis-only target-relative states are never decision features.

**Main Table 3 — Exact-count outcome and composition comparisons.** Put target-free serving policy information in a separate panel from retrospective evidence-state composition.

## 6.4 Held-out test evidence and generalization scope

**Twitch/LiveRec untouched one-shot TEST.** Base NDCG@10 \\(0.58211\\); Utility \\(0.58983\\); Difficulty \\(0.58340\\). Utility–Base \\(+0.00772\\) [\\(+0.00641,+0.00903\\)]; Utility–Difficulty \\(+0.00644\\) [\\(+0.00528,+0.00762\\)]; Utility invocations \\(6650/\\text{TEST}\\), rate \\(15.04\\%\\). State explicitly that this uses a Twitch-fitted DEV selector, **not zero-shot gate transfer** from KuaiLive.

**Main Table 4 — Confirmatory held-out results.** Include test size, frozen budget realized by Utility, TEST Base/Memory/Utility/Difficulty, paired effect intervals and H@10 in a compact table.

**Interpretation.** A positive held-out relative gain supports conditional decision value, but predicted-versus-realized utility correlation (Spearman ~0.173) and Oracle headroom (Oracle NDCG@10 0.64806) limit utility-estimator quality claims.

## 6.5 Robustness, competing explanations and cost

Summarize independent training seeds, common-protocol strong-base comparisons, memory-weight sensitivity, feature-family ablations, alternative-explanation strata and throughput. State which claims are robust and which remain model- or regime-specific; avoid SOTA language.

**Main Table 5 or supplementary exhibit** — one compact ablation/seed/efficiency summary; long tables, cost curves and exact environments belong in Supplementary. The method is not claimed to be a calibrated cost-optimal online system.

---

# 7. Discussion

## 7.1 What is measured by Base-relative evidence valuation?

The operational \\(u_K(M,x)-u_K(B,x)\\) is a **model- and regime-dependent** performance contrast. Interpret persistent history through its fixed specialist instantiation, not as an intrinsic content/value metric.

## 7.2 Why visibility and available history do not determine utility

Differentiate the newly controlled KuaiLive regime reversal from Twitch's history-visibility pattern. With fixed KuaiLive state prevalence, represented gains increase, unavailable penalties ease but remain negative, and recoverable gains *decrease* in full-active; thus the reversal is not a simple recovery of long-horizon information. Candidate membership and candidate-wise normalization co-vary. State groups are retrospective analysis partitions, not a causal law or universal utility signs.

## 7.3 From specialist utility to selective decisions

Explain the difference between evidence-based expert solvability and generic base difficulty. Discuss the decision-theoretic value of predicting conditional specialist-minus-base utility, without claiming novel L2D theory or a calibrated cost policy.

## 7.4 Scope, threats to validity and limitations

Address:
- frozen test and separate subsequent diagnostics, DEV OOF threshold selection, multiple analytic comparisons;
- historical KuaiLive checkpoint/alpha provenance differences versus the completed same-checkpoint post-hoc diagnostic; single new checkpoint pair/seed, reused TEST population, and candidate-wise z-normalization changing with membership;
- independently retrained context-length bases and inability to isolate visibility causally;
- ten-minute Twitch crawl resolution, eligibility semantics, offline logged data, candidate protocols;
- portability of the principle versus non-transferability of fitted gate parameters;
- imperfect utility estimates and far-from-Oracle selection;
- lack of online satisfaction, watch-time, sales or GMV causal measurements.

## 7.5 Implications for knowledge-driven recommender design

The design takeaway is to **assess the marginal decision value of an explicitly specified evidence specialist relative to a credible incumbent**, not to assume all longer-term memory is useful. Outline future work on calibrated relative-utility estimation and deployment-cost validation without claiming those were tested here.

---

# 8. Conclusion

One short section, no new results: (i) operational specialist contribution is reference- and regime-dependent; (ii) retrospective relationship evidence states reveal interpretable conditional structure but do not entail universal signs or causal claims; (iii) a DEV-frozen specialist-utility selector improves offline ranking in the supported protocols, with material estimation headroom. Report that regime reversal persists in the completed same-checkpoint paired diagnostic (`+0.08751` paired shift, 95% CI `[+0.08183,+0.09311]`), but qualify the change as protocol dependent, post-hoc, and not isolated causal membership evidence.

---

# Submission and supplementary package (outside numbered scientific sections)

**Front matter:** title, author/affiliation metadata, abstract (problem–operational quantity–conditional structure–one held-out result–boundary), keywords. Prepare separate Highlights only as required by the journal's current Guide for Authors; Elsevier's general guidance describes 3–5 highlights of at most 85 characters each but does not, by itself, prove KBS-specific mandatory status. See https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript .

**After main text:** unnumbered declarations prepared according to the current journal submission form: acknowledgements/funding, CRediT, competing interests, data/code availability, supplementary materials, and references. Verify exact heading order against KBS's live Guide for Authors rather than assuming a universal Elsevier format; its public guide may be access-restricted. Generic official reproducibility/ethics background: https://www.elsevier.com/en-gb/about/policies-and-standards/publishing-ethics .

## Main-text display budget and linkage

| Display item | Core content | Empirical status |
|---|---|---|
| Figure 1 | Base-relative specialist valuation and decision/analysis separation | Design diagram |
| Table 1 | Dataset, temporal split and candidate protocols | Verify counts/protocol |
| Table 2 | Models and selector comparability | Methods, DEV choices |
| Figure 2 | Historical regime contrasts separated from new same-checkpoint results and paired shift intervals | **COMPLETED supporting diagnostic** |
| Figure 3 | Twitch state replication and context-capacity association | Frozen DEV/TEST + DEV diagnostic |
| Table 3 | Utility vs Difficulty exact-count decision/composition | Frozen analysis |
| Table 4 | One-shot Twitch held-out TEST | Frozen results |
| Table 5 (optional) | Seeds/ablation/efficiency summary | Secondary |

## Supplementary Materials

- **S1 — Dataset provenance and exact eligibility.** Zenodo/official sources, checksum, protocol-level event identifiers, activity timing and streamer/room map rules.
- **S2 — Training and freeze record.** Hyperparameters, independent training seeds, DEV OOF threshold, untouched TEST sequence and artifact hashes.
- **S3 — Comparator performance.** Same-candidate strong-base scorecards, baselines and checkpoint provenance.
- **S4 — Relationship-memory components.** Short/Long/Popularity, horizon and weight sensitivities.
- **S5 — Candidate swap and other regime diagnostics.** Run `37746520476`, artifact `11536890439`, DEV-selected alpha `0.125`, fixed model SHA256s (room `b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7`; streamer `82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945`), candidate-subset and target guards, user-level paired differences and CIs, and historical/new-protocol reconciliation. Archive a durable independent evidence report since workflow artifacts expire.
- **S6 — Context-length details.** Canonical Memory invariants, separately retrained Base hashes, nested evidence-state transitions, recency bins.
- **S7 — Selection analyses.** Development calibration/ranking diagnostics, state composition, threshold sensitivity, feature-family ablations.
- **S8 — Robustness and external validity.** Training seeds, alternative-explanation strata, temporal-regime details.
- **S9 — Resource and reproducibility audit.** Hardware, latency, throughput, cache footprint, complete scripts and artifact-to-claim matrix.

## Mandatory claim/source gates before drafting Section 6

1. **No isolated causal attribution.** The new matched-checkpoint sign reversal is stronger evidence of candidate-regime-dependent *operational* utility; candidate membership and its score standardization change jointly. Historical configurations remain separate.
2. **No numeric consolidation by visual similarity.** The \\(0.60784\\) versus \\(0.61714\\) sampled Base values belong to potentially different experimental contexts; resolve provenance first.
3. **No post-hoc test retuning.** Never use same-checkpoint paired diagnostics, context-length DEV evidence or per-state TEST outcomes to reselect the original frozen Utility threshold.
4. **No isolated context-visibility causality.** L8/L16/L32 has separately trained bases.
5. **No target leakage into selector features.** Evidence states, realized \\(\Delta_M\\) and target ranks are analysis/supervision outputs, not serving features.
6. **No journal policy fabrication.** Check KBS-specific declarations, file requirements and formatting against the actual journal guide at submission time.

*Editorial status, 2026-10-08: Sections 1–4 remain the reviewed LaTeX scientific baseline; Section 5 now exists in the canonical compiled manuscript. The same-checkpoint diagnostic completed successfully (run 37746520476) and is incorporated solely as **supporting post-hoc evidence**. Sections 6–8 are the remaining drafting targets; historical and frozen-policy results preserve their independent experimental identities.*
