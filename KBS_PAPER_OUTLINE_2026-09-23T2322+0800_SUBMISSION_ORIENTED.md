# Submission-oriented manuscript outline for *Knowledge-Based Systems*

> **INDEPENDENT / NON-AUTHORITATIVE MANUSCRIPT OUTLINE**  
> This document is a paper-facing writing outline. It does not replace frozen experimental protocols, immutable test results, or prior authoritative experimental snapshots unless explicitly promoted by the authors.

**Updated:** 2026-10-08

> **Writing control:** Only modify the manuscript sections explicitly assigned to the current writing stage. Do not fill Abstract, all of Section 6, Discussion and Conclusion in a single editing pass.  
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

**Status: outline only; not yet drafted in the canonical LaTeX manuscript.** Write it after the evidence-bearing Results and interpretive Discussion have been reviewed, rather than before.

- **Research gap:** relationship evidence can be redundant or beneficial relative to a trained Base, and its operational value depends on the user event and candidate regime.
- **Method:** one fixed transparent relationship-memory expert; event-level Memory-minus-Base NDCG@10; pre-outcome conditional-utility prediction and selective invocation.
- **Primary frozen evidence:** Twitch one-shot TEST, 44,221 events, positive Utility–Base and Utility–Difficulty paired differences, equal invocation-count control.
- **Complementary diagnosis:** KuaiLive 10,222 paired events, the P0 candidate-membership/standardization allocation and P1 three independent checkpoint seeds, clearly marked **post-hoc**.
- **Boundaries:** conditional, model-relative, offline evidence; no isolated causal membership effect or zero-shot gate transfer.

Avoid advertising a new general routing theorem, intrinsic information-value theory, or a causal online impact claim. Validate the final abstract against KBS-specific current submission instructions at the abstract-writing stage.

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

Preview only two complementary discoveries without importing experiment-run chronology:

1. **Conditional evidence utility and decision benefit.** On Twitch, Memory is inferior to the Base in aggregate but substantially beneficial for a recoverable-history subgroup; a DEV-trained Utility selector outperforms Base and the equal-invocation-count Difficulty control on untouched TEST. Retrospective subgroup labels do not enter the online-facing selector.
2. **Dependence on the ranking environment.** In KuaiLive, sampled-active versus full-active candidates reverse the operational Memory–Base ordering on paired events. In a fixed-score factorial decomposition, most of the resulting difference is allocated to the ranked-candidate universe rather than its z-score reference, with consistent direction across 3 independently trained base seeds.

Keep detailed context-capacity and confidence-interval numbers in Results, not the introductory motivation.

## 1.3 Contributions

Three claims, in academic rather than workflow language:

**C1 — Operational Base-relative evidence valuation.** Define and analyze the event-level ranking contribution of a fixed relationship-memory specialist relative to a specified trained Base and candidate universe. The subtraction itself is not asserted as a novel theorem.

**C2 — Conditional structure and operating-context dependence.** Identify history-state heterogeneity in frozen Twitch evidence and characterize candidate-regime variation through paired KuaiLive comparisons. State descriptions are retrospective; the candidate-membership/normalization allocation is descriptive, not causally isolated.

**C3 — Practical conditional expert choice.** Using only pre-outcome history and Base descriptors, learn a relative-Utility selector that achieves positive frozen TEST gains versus Base and an exact-count Difficulty comparator. This is not claimed to be a new general learning-to-defer method or zero-shot transfer of one gate.

**Scope.** Two live-stream platforms, one-positive offline ranking protocols and their trained model families; no causal engagement or GMV inference.

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

## 2.5 Research gap synthesis

The canonical manuscript no longer includes a redundant positioning table. Conclude Related Work with one paragraph distinguishing the paper's scientific object: **conditional marginal ranking value of a fixed, interpretable specialist against an established Base**, and its use for decision making. Keep source comparisons tied to published journal and conference papers as documented in the [formal publication audit](manuscript/kbs_latex/RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md).

---

# 3. Problem Formulation

The revised LaTeX manuscript is canonical for Section 3. Reserve $m$ for the invoked-event count and use $\Delta_M$ for Memory-minus-Base utility throughout; retain only general selection mathematics here, while DEV/OOF details belong to Section 5.

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

**Related audit:** [Sections 1–4 retrospective academic assessment](manuscript/kbs_latex/SECTIONS1-4_RETROSPECTIVE_ACADEMIC_AUDIT_2026-10-08.md). Its P0 symbol and fusion-weight consistency items have now been resolved in the canonical LaTeX manuscript; the audit remains the rationale and change history.

---

# 6. Experimental Results

**Staged narrative: observed conditional value → predictive decision value → candidate-context boundary.** As of 2026-10-09, **the new Twitch evidence-heterogeneity Section 6.1 has been drafted in the canonical LaTeX manuscript** with one figure and one complementary table. Sections 6.2–6.5 remain writing plans and have not been drafted. The formerly completed KuaiLive P0/P1 Section 6.1 is preserved verbatim in [`section6_3_kuailive_migration_source.tex`](manuscript/kbs_latex/section6_3_kuailive_migration_source.tex) for a later, independently reviewed Section 6.3 migration; it is not currently in the compiled main manuscript. The frozen Twitch policy validation remains planned for 6.2, separate from the post-hoc KuaiLive diagnostic.

## 6.1 Heterogeneous Utility of Relationship Memory

**Question:** Under which retrospective history conditions does Memory improve upon the Base?

Twitch DEV→TEST state-conditional Memory−Base NDCG@10: represented `−0.01995 → −0.01935` (TEST n=24,285), recoverable `+0.23097 → +0.22045` (n=5,539), unavailable `−0.19562 → −0.18215` (n=14,397). All subgroup CI values should be taken from the frozen one-shot run [35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303).

**Current Section 6.1 exhibits:** Figure 2 plots DEV and TEST state-conditional Memory−Base deltas (with TEST 95% paired bootstrap intervals), while its compact table reports TEST state counts, Base/Memory absolute NDCG@10 and paired intervals. The two displays have distinct functions. The states are target-relative diagnostic categories and are unavailable to the serving selector. Status: **reviewer-style tightening completed, frozen evidence and final compiled PDF visually checked; pending coauthor approval**. See [the detailed Section 6.1 review log](manuscript/kbs_latex/SECTION6_1_KBS_REVIEWER_TIGHTENING_2026-10-09.md).

## 6.2 Decision Value of Predicting Relative Utility

**Question:** Can observable relative-Utility predictions improve specialist choice compared with predicting Base difficulty?

**Primary frozen evidence:** [Twitch one-shot TEST #35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303), n=44,221; Always-Base NDCG@10 `0.58211`, Always-Memory `0.53980`, Utility `0.58983`, matched-count Difficulty `0.58340`, hindsight Oracle `0.64806`. Utility vs Base `+0.00772` [`+0.00641,+0.00903`], Utility vs Difficulty `+0.00644` [`+0.00528,+0.00762`]. Realized Utility invocations `6,650`, or `15.04%`; H@10 Utility `0.76448` versus Base `0.75503`.

Use DEV-only group-composition evidence to explain why Difficulty is not equivalent to expert solvability: recoverable enrichment Utility/Difficulty ~2.72×/1.67×, unavailable ~1.03×/1.91×. Selection labels are never target-state features. Explicitly flag the modest Spearman correlation `0.173` and approximately `11.7%` of hindsight Oracle potential gain captured.

**Main Table 4:** exact-count, target-label-permission-aware policy comparison. This is the paper's strongest independent frozen decision evidence; highlight it early.

## 6.3 Candidate-Regime Dependence of Relative Utility

**Question:** How stable is a fixed specialist's apparent benefit when the ranked candidate universe changes?

**Controlled KuaiLive diagnostic:** 10,222 paired events, sampled DEV fusion room alpha 0.125, identical Memory and fixed model pair. Original seed sampled Memory−Base `−0.04120`, full-active `+0.04631`; paired shift `+0.08751` with P0 replay-bootstrap 95% CI [`+0.08210,+0.09326`].

**P0 four-cell protocol factorization** (`S/F` ranked candidates × `S/F` standardization reference): `SS=−0.04120`, `SF=−0.04142`, `FS=+0.04761`, `FF=+0.04631`. Two-path allocations: candidate membership `+0.08827` [`+0.08287,+0.09397`], normalization reference `−0.00076` [`−0.00117,−0.00036`]. These are algebraic and protocol-dependent, not random-intervention causal effects.

**P1 checkpoint training-seed panel**: `20260918: +0.08751`, `20260919: +0.08363`, `20260920: +0.08408`; three-seed mean `+0.08508` and SD `0.00212`, 3/3 sampled negative/full positive. Target-relative state counts `4,589/206/5,427` do not change across paired candidate sets; the smallest recoverable subgroup contributes negatively to the paired shift. Do **not** claim long-history recovery drives the aggregate reversal.

**Main Table 5:** compact four-cell protocol decomposition. Model-seed rows, checkpoint hashes, state-by-seed contributions and historical protocol comparisons belong in **Supplementary S5/S8**, with full provenance [P0/P1 evidence ledger](KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md). Sampling size/draw sensitivity (P2) is still proposed, **not completed**.

## 6.4 Robustness and Alternative Explanations

**Twitch DEV-only pre-outcome feature-family ablation** ([run #35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454)): equal 6,563-event selection count. Relative-Utility gain over Base: history six features `+0.00372`, Base confidence eight features `+0.00160`, combined 14 features `+0.00838`. OOF Spearman `0.14791,0.09109,0.18990`, respectively. This supports descriptive complementarity without deriving a causal synergy or treating the DEV ablation as an additional untouched test.

**History capacity:** DEV-only separately trained LiveRec bases with lengths `8,16,32`, Base NDCG@10 `0.52619,0.57185,0.59663`, canonical Memory `0.52170`. Matched recoverable→represented shifts of Memory−Base about `−0.42` to `−0.45`; changing context length is confounded with model retraining. Supplementary controls include common-candidate KuaiLive strong-base checks, weight/recency sensitivity and temporal robustness.

**Main Table 6:** compact DEV-only feature-family ablation, labelled as exploratory. Unresolved/optional sensitivity must not be written as measured.

## 6.5 Computational Considerations

Separate invocation rate from measured overhead. [Formal CPU benchmark run #35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758) reports, for its distinct 575-candidate KuaiLive setup on three hosted CPU replicas, mean Dual-ID latency approximately `0.76 ms` and selective-HGB pipeline approximately `2.34 ms` at nominal 14.25% expert invocation. These are **not** timings for the Twitch held-out policy. Do not claim net latency savings or online engagement/transaction impact from offline results.

---

# 7. Discussion

## 7.1 Operational Value Is Base- and Context-Dependent

A fixed historical relationship source is not guaranteed to add ranking utility. The estimand compares `u_K(M,x)−u_K(B,x)` under a specified candidate regime; it is not intrinsic information content. Explain how an overall inferior specialist can nevertheless help a subset of users.

## 7.2 Interpreting Conditional Evidence and Candidate Regimes

Contrast Twitch's positive `recoverable` subgroup with KuaiLive's unchanged state prevalence and its positive represented/unavailable contributions under candidate swaps. Candidate count, composition and task difficulty remain inseparable within the candidate-membership allocation; score-reference standardization is a small descriptive factor in P0. Discuss noncausal state partitions and separately trained context-length bases.

## 7.3 From Relative Utility to Selective Decisions

Explain why generic Base difficulty and expert solvability differ; refer to the frozen Twitch matched-budget gains and DEV feature-family ablation. Retain limits: test Spearman `0.173`, 11.7% of hindsight Oracle gap captured. No new general Learning-to-Defer theory or optimal serving-cost result.

## 7.4 Validity Boundaries

Differentiate one-shot frozen Twitch policy verification from repeated KuaiLive post-hoc TEST analyses; three KuaiLive seeds are independent model initializations, not three independent data trials. Consider candidate sampling, ten-minute Twitch observation resolution, selection threshold calibration, historical checkpoint provenance, one-positive logged labels, no causal commercial impact, and absence of zero-shot gate transfer.

## 7.5 Implications for Knowledge-Based Recommendation

Recommend `incremental, model-relative decision assessment` of interpretable auxiliary specialists, conditioned on both history and the incumbent ranker's candidate universe. Future work: independent datasets, isolated candidate-hardness sampling, larger seed pools, calibrated budget-aware serving, and online evaluation.

---

# 8. Conclusion

The canonical manuscript conclusion remains **unwritten** and must later synthesize three findings without adding numbers: (i) persistent relationship history is conditionally useful against a strong Base, (ii) a DEV-frozen relative-Utility selector improves untouched Twitch ranking despite the expert's inferior aggregate results, and (iii) KuaiLive's sign reversal persists across three model seeds and is described primarily by ranked-candidate changes in a post-hoc algebraic attribution. Scope remains operational, offline, model- and regime-dependent.

---

# Submission and supplementary package (outside numbered scientific sections)

**Front matter:** title, author/affiliation metadata, abstract (problem–operational quantity–conditional structure–one held-out result–boundary), keywords. Prepare separate Highlights only as required by the journal's current Guide for Authors; Elsevier's general guidance describes 3–5 highlights of at most 85 characters each but does not, by itself, prove KBS-specific mandatory status. See https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript .

**After main text:** unnumbered declarations prepared according to the current journal submission form: acknowledgements/funding, CRediT, competing interests, data/code availability, supplementary materials, and references. Verify exact heading order against KBS's live Guide for Authors rather than assuming a universal Elsevier format; its public guide may be access-restricted. Generic official reproducibility/ethics background: https://www.elsevier.com/en-gb/about/policies-and-standards/publishing-ethics .

## Main-text display budget and linkage

| Item | Main-text purpose | Primary evidentiary status |
|---|---|---|
| Figure 1 | Decision framework and retrospective evidence route | Method definition |
| Tables 1–2 | Datasets and comparison design | Frozen protocols |
| Table 3 | DEV/TEST relationship-state heterogeneity | Frozen Twitch TEST groups, descriptive |
| Table 4 | Twitch Base/Memory/Utility/Difficulty/Oracle | **Frozen independent one-shot TEST** |
| Table 5 | KuaiLive four-cell regime decomposition | **Completed post-hoc P0/P1** |
| Table 6 | Twitch feature-family OOF ablation | DEV-only exploratory |
| Efficiency paragraph | Implemented CPU costs, no speedup promise | Separate KuaiLive CPU benchmark |

The paper-facing LaTeX currently has four Section 6 tables plus two Section 5 tables; renumbering may change across layouts. Preserve scientific roles, not literal table numbers, when moving exhibits to Supplementary.

## Supplementary Materials

- **S1 — Dataset provenance and exact eligibility.** Zenodo/official sources, checksum, protocol-level event identifiers, activity timing and streamer/room map rules.
- **S2 — Training and freeze record.** Hyperparameters, independent training seeds, DEV OOF threshold, untouched TEST sequence and artifact hashes.
- **S3 — Comparator performance.** Same-candidate strong-base scorecards, baselines and checkpoint provenance.
- **S4 — Relationship-memory components.** Short/Long/Popularity, horizon and weight sensitivities.
- **S5 — Candidate swap and other regime diagnostics.** Completed P0 [run 37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645): full 2×2 user-level results, 3,000-replicate paired bootstrap, exact replay, all guards, checkpoint SHA256, and reconciliation with earlier same-checkpoint run 37746520476. Include precise explanation of the descriptive two-path allocation and the historical sampled Base 0.60784 versus 0.61714 provenance ambiguity.
- **S6 — Context-length details.** Canonical Memory invariants, separately retrained Base hashes, nested evidence-state transitions, recency bins.
- **S7 — Selection analyses.** Development calibration/ranking diagnostics, state composition, threshold sensitivity, feature-family ablations.
- **S8 — Robustness and external validity.** P1 three-seed checkpoint panel (20260918/19/20), confidence intervals and state-level decomposition from [verified results ledger](KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md); alternative regimes, strong-base and feature ablations. P2 candidate negative-sampling sensitivity remains unexecuted.
- **S9 — Resource and reproducibility audit.** Hardware, latency, throughput, cache footprint, complete scripts and artifact-to-claim matrix.

## Mandatory claim/source gates before finalizing Section 6

1. **No isolated causal attribution.** The new matched-checkpoint sign reversal is stronger evidence of candidate-regime-dependent *operational* utility; candidate membership and its score standardization change jointly. Historical configurations remain separate.
2. **No numeric consolidation by visual similarity.** The \\(0.60784\\) versus \\(0.61714\\) sampled Base values belong to potentially different experimental contexts; resolve provenance first.
3. **No post-hoc test retuning.** Never use same-checkpoint paired diagnostics, context-length DEV evidence or per-state TEST outcomes to reselect the original frozen Utility threshold.
4. **No isolated context-visibility causality.** L8/L16/L32 has separately trained bases.
5. **No target leakage into selector features.** Evidence states, realized \\(\Delta_M\\) and target ranks are analysis/supervision outputs, not serving features.
6. **No journal policy fabrication.** Check KBS-specific declarations, file requirements and formatting against the actual journal guide at submission time.

*Editorial status, 2026-10-09: The canonical LaTeX manuscript contains Sections 1–5 and the newly drafted Twitch Section 6.1. The former KuaiLive 6.1 has been archived without alteration for eventual 6.3. Sections 6.2–6.5, Discussion, Conclusion and Abstract remain unwritten and will be developed in separate reviewed stages. P0/P1 evidence is complete and archived; optional P2 negative-sampling sensitivity is unexecuted.*
