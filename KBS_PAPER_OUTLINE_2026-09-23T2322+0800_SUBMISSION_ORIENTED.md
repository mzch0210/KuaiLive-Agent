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
5. **Validation.** Report the KuaiLive regime reversal and the untouched Twitch/LiveRec held-out test result.
6. **Qualification.** State that evidence state structures but does not uniquely determine utility, the measured evidence value is operationalized through the fixed specialist, and substantial Oracle headroom remains.

Prioritize two quantitative anchors rather than a long result list:

- **Mechanism:** recoverable-to-represented transitions under context expansion reduce specialist-minus-base utility by approximately `0.42–0.45` NDCG@10 while canonical Memory is fixed.
- **Held-out decision:** on untouched Twitch/LiveRec TEST, Selective Utility improves over Base by `+0.00772` NDCG@10 and over exact-budget Difficulty by `+0.00644`.

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

- aggregate specialist ordering reverses across KuaiLive candidate regimes;
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

The current LaTeX manuscript is canonical for Section 3. Keep the section concise and avoid theorem inflation.

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
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

Interpretation boundary:

> `Δ_m` is the **operational marginal value** of persistent relationship evidence as instantiated by fixed specialist `M` relative to fixed base `B`; it is not intrinsic or model-independent information value.

## 3.3 Conditional relative utility

For regime `r` and deployment-observable information `z`:

\[
\eta_r(z)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

`R` indexes the event-generating/evaluation condition and need not be a selector feature. Analysis-only evidence-state labels, target `y`, realized ranks, and realized `Δ_m` are excluded from `Z`.

For a serving action `a`, define selective utility in prose or inline and retain the expected-gain identity:

\[
\mathbb E[u_K^{sel}-u_K(B)\mid R=r]
=
\mathbb E[a(Z)\eta_r(Z)\mid R=r].
\]

This is the decision rationale for predicting conditional relative utility rather than generic base difficulty.

## 3.4 Development-frozen selective invocation and matched-budget evaluation

Define the primary learned policy as a **development-frozen pointwise threshold** on estimated conditional relative utility:

\[
a_{\tau_r}(z)=\mathbf 1[\hat\eta_r(z)>\tau_r].
\]

Select \(\tau_r\) using out-of-fold development utility; fit the final regressor on development data and freeze both model and threshold before held-out test access. The realized held-out invocation count is an **outcome of the fixed policy**, not a predetermined exact budget.

For matched comparison, let \(m=\sum_i a_{\tau_r}(z_i)\) be the frozen utility policy's realized evaluation-set invocation count. The Difficulty control uses **top-\(m\)** predicted base-difficulty scores, and the analysis-only Oracle uses **top-\(m\)** realized \(\Delta_m\) values. Both are **offline, batch-level matched-budget controls**; neither is the serving rule of the primary Utility selector. Use deterministic tie-breaking.

The frozen Utility threshold is sensitive to the score distribution; it is not calibration-free. Offline top-\(m\) controls require only an ordering, but assume the evaluation batch is available. A theoretical cost rule \(a_r^*(z)=\mathbf 1[\eta_r(z)>\lambda\kappa_r(z)]\) is an optional deployment interpretation, not an evaluated calibrated cost policy. Avoid claiming online hard-budget guarantees or a new routing theorem.

## 3.5 Regime-level decomposition

Let `S` be a mutually exclusive and exhaustive partition of Base-relative evidence states. Then

\[
\mathbb E[\Delta_m\mid R=r]
=
\sum_sP(S=s\mid R=r)\,\mathbb E[\Delta_m\mid S=s,R=r].
\]

This separates evidence-state composition from state-specific specialist utility. Treat it as analytical decomposition, not causal theory.

---

# 4. Base-Relative Evidence Valuation Framework

Section 4 is an implementation and design-rationale chapter, not a second problem formulation or an experiment log. Reuse the Section 3 definitions of \(B,M,Z,S,\Delta_m,\hat\eta_r\) without rederiving them. The methodological distinction is an **operational comparison of ranking utility between a separately specified relationship specialist and a credible fixed base**. Such a comparison does not by itself identify intrinsic evidence information, model-independent complementarity, or a new memory, HGB, or deferral algorithm.

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

State complexity uses percentile transforms derived from the full **outcome-free DEV feature distribution** and shared across OOF regression folds, not fold-specific empirical distribution estimates. Frozen DEV references are applied to TEST. Describe HGB configuration (200 iterations, learning rate 0.05, depth 3, minimum leaf size 50, L2 regularization 1). Five-fold OOF DEV predictions support **supervised threshold selection**, not an unbiased evaluation of the learned threshold. Train the final estimator on DEV; freeze estimator, features, transforms and threshold before untouched TEST.

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

# 5. Experimental Design

## 5.1 Complementary roles of the two platforms

Treat the platforms as complementary experimental environments rather than interchangeable benchmarks.

### KuaiLive

Use for:

- candidate-regime reversal;
- temporal-regime effects;
- selective decision gains;
- fixed-composition state-specific candidate-regime decomposition.

### Twitch / LiveRec

Use for:

- credible official strong base;
- pre-specified development analysis and untouched held-out test validation;
- evidence-state replication;
- context-capacity intervention;
- Utility/Difficulty/Oracle selection-composition analysis.

## 5.2 Recommendation regimes

Describe sampled-active, full-active, standard temporal, and strict temporal regimes where applicable. Make candidate construction and temporal availability differences explicit because event-level rank utility is candidate-set relative. In paired candidate-regime comparisons, retain the same underlying user–time–target instances, but treat their candidate-specific rankings as distinct full recommendation events.

## 5.3 Pre-specified held-out validation protocol

Main-text summary:

> **Development-only policy/OOF threshold selection → freeze feature transforms, models, and threshold → untouched one-shot held-out TEST evaluation; subsequently match offline control budgets to the frozen Utility policy's realized test invocation count.**

Use `pre-specified`, `policy freeze`, and `untouched held-out test` in the manuscript. Keep immutable hashes, artifacts, chronology, and workflow provenance in reproducibility materials rather than the narrative Results text.

## 5.4 Metrics and statistical inference

Primary metric: NDCG@10.  
Secondary metric: H@10 / HR@10 as appropriate.

Use:

- paired user-level bootstrap intervals;
- identical realized invocation budgets for offline Difficulty/Oracle controls determined by the frozen-threshold Utility policy;
- mean ± SD and sign consistency across independent base training seeds.

Do not reinterpret within-seed bootstrap intervals as across-seed confidence intervals.

## 5.5 Evidence hierarchy

### Primary confirmatory evidence

- pre-specified development relationship-state structure;
- untouched held-out TEST replication;
- untouched held-out selective-utility TEST result.

### Primary mechanistic strengthening

- development-only context-capacity comparison with canonical Memory fixed and Base independently retrained at each input length;
- matched-instance recoverable→represented transitions interpreted with corresponding Base-utility changes, not as an isolated causal effect;
- fixed-composition KuaiLive candidate-regime decomposition;
- Utility/Difficulty/Oracle selection composition under exact matched budgets.

### Secondary robustness and refinement

- component attribution;
- alternative-explanation stratification;
- positive-delta fractions;
- Memory-parameter sensitivity;
- context-distance consistency and fine recency bins;
- feature-family ablation;
- independent training seeds;
- strong-base comparator checks;
- complexity and efficiency.

This hierarchy should determine result order and claim strength.

---

# 6. Results

Use descriptive result headings rather than `RQ1`--`RQ4` labels in the manuscript.

## 6.1 Aggregate specialist value is regime-dependent

Begin with the paradox rather than the mechanism.

Key KuaiLive aggregate results:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active: Memory−Base approximately `+0.03367`, native Selective−Base approximately `+0.05345`;
- strict temporal: Selective−Base approximately `+0.07282` / `+0.09743`.

### Candidate-regime decomposition

For sampled-active versus full-active, use the same 10,222 underlying user–time–target instances and show that evidence-state prevalence is identical while aggregate Memory−Base reverses from `−0.05125` to `+0.03367`.

| Base-relative state | Sampled Δ | Full-active Δ | Full−Sampled shift | 95% CI |
|---|---:|---:|---:|---:|
| represented | +0.11508 | +0.19261 | +0.07752 | [+0.07046,+0.08472] |
| recoverable-but-unrepresented | +0.17779 | +0.08049 | −0.09731 | [−0.14897,−0.04647] |
| unavailable | −0.20060 | −0.10251 | +0.09809 | [+0.08988,+0.10649] |

Conclusion:

> **Regime dependence is not reducible to changing state prevalence; candidate regime can change the operational marginal value of the same specialist within the same evidence state.**

Do not generalize this fixed-composition conclusion to temporal regimes without direct decomposition evidence.

## 6.2 Base-relative evidence state structures specialist utility

### Pre-specified development → untouched held-out test replication

| Evidence state | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| represented | −0.01995 | −0.01935 |
| recoverable-but-unrepresented | **+0.23097** | **+0.22045** |
| unavailable | −0.19562 | −0.18215 |

Interpret these as Twitch/LiveRec conditional patterns, not universal state signs.

### Context-capacity and Base-visibility comparison

Keep canonical Memory fixed (`NDCG@10 = 0.52170`) while varying base context:

| Base context | Base NDCG@10 | Memory−Base | 95% CI |
|---:|---:|---:|---:|
| 8 | 0.52619 | −0.00450 | [−0.00756,−0.00127] |
| 16 | 0.57185 | −0.05016 | [−0.05307,−0.04731] |
| 32 | 0.59663 | −0.07493 | [−0.07766,−0.07227] |

Use matched-instance evidence-state transitions as a convergent diagnostic; the same specialist is held fixed but each context-length Base is trained separately, so a contraction in specialist-minus-base utility is algebraically equal to improved Base utility:

| Transition | n | Δ before | Δ after | change | 95% CI |
|---|---:|---:|---:|---:|---:|
| L8→L16 recoverable→represented | 5,055 | +0.29388 | −0.15360 | **−0.44748** | [−0.45767,−0.43730] |
| L16→L32 recoverable→represented | 3,617 | +0.25755 | −0.17474 | **−0.43229** | [−0.44381,−0.42054] |
| L8→L32 recoverable→represented | 8,672 | +0.27782 | −0.14114 | **−0.41896** | [−0.42685,−0.41112] |

Conclusion:

> **The operational marginal value of the fixed relationship specialist is strongly Base-relative: when a larger base context comes to represent the same persistent relationship evidence, specialist advantage contracts sharply.**

Use **context-capacity comparison across separately trained bases with associated input-visibility changes**, not an isolated visibility intervention or causal proof. Explicitly report Base retraining, Base-utility differences, and the identity `Δ(L')−Δ(L)=u_K(B_L)−u_K(B_L')` when `M` is unchanged.

### Component attribution and recency refinement

Report compactly in the main text:

- Long-only on recoverable DEV events: `ΔNDCG@10 = +0.33688`;
- Short-only and Popularity-only: negative in the same regime;
- recency is non-monotonic, including a positive `1–4` pocket.

Move full distance-bin and parameter-sensitivity matrices to Supplementary Material.

## 6.3 Conditional relative utility is not generic base difficulty

Start with exact-budget performance, then explain the result through event composition.

### Selection composition on pre-specified Twitch DEV

Population prevalence:

- represented `52.35%`;
- recoverable `12.54%`;
- unavailable `35.11%`.

| Selector | Represented | Recoverable | Unavailable |
|---|---:|---:|---:|
| Utility selection share | 29.70% (`0.57×`) | 34.13% (**`2.72×`**) | 36.17% (`1.03×`) |
| Difficulty selection share | 11.98% (`0.23×`) | 20.89% (**`1.67×`**) | 67.13% (**`1.91×`) |
| Oracle selection share | 50.39% | 43.00% (**`3.43×`**) | 6.61% |

Conclusion:

> **Base Difficulty disproportionately identifies hard-but-unavailable events, whereas conditional relative Utility more strongly targets events containing recoverable specialist evidence.**

Relationship-state labels remain post-hoc analysis variables and are not used by the selector.

## 6.4 Untouched second-platform validation and robustness

### Twitch/LiveRec held-out TEST

Under the frozen Utility threshold, the realized test count is `m=6,650` (`15.04%` invocation); Difficulty and Oracle use this exact budget offline:

- Base NDCG@10 `0.58211`;
- Always Memory `0.53980`;
- Difficulty `0.58340`;
- Selective Utility `0.58983`;
- Selective−Base `+0.00772`, 95% CI `[+0.00641,+0.00903]`;
- Utility−Difficulty `+0.00644`, 95% CI `[+0.00528,+0.00762]`.

Secondary H@10:

- Base `0.75503`;
- Selective Utility `0.76448`;
- Difficulty `0.75252`;
- Selective−Base `+0.00945`;
- Utility−Difficulty `+0.01196`.

### Utility-estimation headroom

- predicted-versus-realized utility Spearman ≈ `0.173`;
- Oracle exact-budget NDCG@10 `0.64806`;
- current router captures approximately `11.71%` of Oracle gain.

Interpretation:

> **The development-frozen Utility threshold identifies a useful positive tail despite imperfect event-level correspondence; offline matched-budget Difficulty and Oracle controls clarify selection quality. Unlike offline top-`m` selection, the frozen threshold depends on score scale as well as ordering.**

Do not describe current utility estimates as calibrated.

### Robustness summary

Keep main text concise and move detailed matrices to Supplementary Material:

- recoverable-state positive utility remains positive across history length, creator exposure, candidate count, and repeat-propensity strata;
- Memory sensitivity preserves the main Twitch state signs;
- independent base seeds preserve `Selective > Base` and `Utility > Difficulty`;
- same-protocol comparator checks establish credible strong bases without SOTA claims.

## 6.5 Deployment trade-offs

Report accuracy versus invocation rate, latency/throughput, and memory/cache footprint. Treat cost-thresholding as a deployment interpretation and practical frontier, not as an empirically calibrated cost-optimization contribution unless an explicit cost model is evaluated.

---

# 7. Discussion

## 7.1 Operational evidence valuation before evidence integration

Main implication:

> **An auxiliary evidence source should not be judged solely by standalone predictive strength; in this study its operational value is measured through the marginal ranking contribution of a fixed specialist relative to the current base and regime.**

This is the main bridge from live-stream relationship memory to the broader KBS audience.

## 7.2 Evidence state structures but does not determine utility

Use the three states as explanatory coordinates rather than a universal taxonomy of signs.

- Twitch: represented is negative in aggregate, recoverable strongly positive, unavailable negative.
- KuaiLive: represented can be positive, and state-specific utility changes when candidate regime changes despite fixed state prevalence.

Therefore avoid `state → fixed sign`; treat recency and operating regime as modifiers.

## 7.3 Why conditional relative Utility differs from Difficulty

Explain that base weakness is not sufficient: some difficult events contain no target-specific evidence that the relationship specialist can recover. Use selection composition to connect mechanism to decision performance.

## 7.4 Transparency versus architectural complexity

Defend the simple specialist as a scientific design choice: transparency makes evidence availability, component attribution, and marginal value inspectable. Do not argue that the weighted specialist is architecturally superior to learned long-memory models.

## 7.5 Relationship to evidence selection, VOI, deferral, and expert routing

State four boundaries succinctly:

- evidence selection/fusion concerns what information to retain or integrate;
- classical VOI concerns decision value of acquiring information;
- deferral/routing concerns instance allocation among predictors/experts;
- this study characterizes the operational marginal ranking value of one fixed transparent evidence specialist relative to a trained base.

Do not claim general deferral or information-value theory.

## 7.6 Remaining utility-estimation headroom

Use modest predicted-versus-realized association and limited Oracle capture to identify improved relative-utility ranking as the principal future algorithmic opportunity. Under exact-budget decisions, emphasize ordering quality; discuss absolute calibration only for threshold/cost deployment.

## 7.7 Limitations and external validity

Explicitly limit conclusions to:

- evaluated live-stream platforms and candidate protocols;
- strong finite-context sequential bases;
- explicit persistent user–creator relationship evidence as instantiated by the fixed specialist;
- offline ranking outcomes.

Do not imply causal effects on satisfaction, engagement, conversion, or GMV. Do not claim model-independent intrinsic evidence value or generalization to arbitrary auxiliary specialists.

---

# 8. Reproducibility and Data Availability

Add a short formal section immediately before the Conclusion.

Report:

- public datasets and access sources;
- code repository;
- experiment commits and released artifacts sufficient to reproduce reported results;
- preprocessing and candidate construction;
- random seeds;
- development-only analysis, policy-freeze, and untouched held-out test procedure;
- Supplementary reproducibility package with parameter tables, hashes, and detailed robustness outputs;
- Data Availability Statement consistent with Elsevier requirements.

Keep workflow failures/recoveries and low-level CI logs out of the narrative manuscript; preserve them in the audit/reproducibility package where needed.

---

# 9. Conclusion

Close with three points only:

1. **Scientific finding:** the fixed relationship-memory specialist has no fixed global ordering relative to a strong base; its operational marginal ranking value is Base-relative and regime-dependent.
2. **Mechanism:** recoverable persistent evidence is especially valuable in the Twitch setting when absent from the base representation, and specialist advantage contracts when the base comes to represent the same evidence.
3. **Decision implication:** conditional specialist-minus-base utility is more appropriate than generic base difficulty for selective specialist use under matched budgets, although current utility ranking remains far from Oracle.

Avoid introducing new limitations, literature, or claims in the Conclusion.

---

# Main figures and tables

## Figure 1 — Base-relative evidence valuation framework

Show (i) eligible context and fixed Base ranking, (ii) persistent user–creator relationship history feeding the transparent Short / Long / Popularity specialist when invoked, and (iii) a separate offline supervision/diagnostic path: target plus two rankings supply \(\Delta_m\), while target-relative history supplies \(S_L\). The online selector uses observable \(Z\) and a DEV-frozen utility threshold only. Never draw target-relative diagnostic states as online gate features or infer a deployed online budget from offline matched controls.

## Table 1 — Regime performance and fixed-composition decomposition

Combine compact KuaiLive regime results with sampled-active/full-active state-specific utility shifts. Make visually clear that candidate-regime sign reversal occurs with unchanged state prevalence.

## Figure 2 — Signature mechanism figure

### Panel A — Pre-specified development → untouched held-out test state replication

Show Memory−Base for represented, recoverable, and unavailable states.

### Panel B — Context-capacity comparison with retrained Base

Show `L=8/16/32`, canonical Memory fixed, separately retrained Base checkpoints, and matched-instance recoverable→represented transitions with approximately `0.42–0.45` decline in specialist-minus-base utility. Label corresponding Base gains and avoid an isolated-visibility causal arrow.

Move fine context-distance bins to Supplementary Material unless space permits a small inset.

## Table/Figure 3 — Conditional relative Utility versus Difficulty

Combine:

- exact-budget NDCG@10 / H@10;
- selected-state composition;
- enrichment relative to population;
- Oracle composition as an analysis upper bound.

## Table 4 — Untouched second-platform TEST and robustness summary

Keep primary held-out results in the main table. Put full sensitivity, seed, comparator, and alternative-explanation matrices in Supplementary Material.

## Figure/Table 5 — Accuracy–invocation–latency/footprint frontier

Use only if space permits; otherwise move detailed serving curves to Supplementary Material and retain one compact deployment summary in the main text.

---

# Supplementary Material structure

## S1. Dataset preprocessing and candidate construction
## S2. Pre-specified validation protocol and reproducibility details
## S3. Full base comparator results
## S4. Memory component and parameter sensitivity
## S5. Context-distance and recency-bin analyses
## S6. Alternative-explanation stratification
## S7. Feature-family ablations and training-seed results
## S8. Complexity, latency, throughput, and footprint details
## S9. Additional bootstrap intervals and H@10 tables

---

# Claim discipline to maintain during drafting

Supported manuscript-level claims:

- the fixed relationship-memory specialist is regime-dependent rather than globally ordered against the base;
- `Δ_m` operationalizes the specialist's marginal ranking contribution relative to a fixed base and is not intrinsic model-independent information value;
- Base-relative evidence state strongly structures specialist utility in Twitch/LiveRec;
- recoverable-but-unrepresented evidence is the dominant positive Twitch relationship-memory regime;
- pre-specified development state structure reproduces on untouched held-out TEST;
- development-only context-capacity comparisons with separately retrained bases are consistent with Base-relative visibility and improved Base representation quality;
- evidence state does not uniquely determine utility across regimes;
- conditional relative Utility and Difficulty select materially different event compositions at the same exact budget;
- Utility better enriches recoverable events, while Difficulty disproportionately selects unavailable events;
- the frozen Utility threshold benefits from useful utility scoring and a transferable score scale; offline top-`m` controls require only useful ordering;
- selective Utility improves strong bases in the evaluated settings and transfers under untouched second-platform evaluation;
- substantial Oracle headroom remains.

Avoid claims of:

- a universal theory of auxiliary evidence valuation;
- intrinsic or model-independent value of relationship evidence;
- fixed utility signs for represented/recoverable/unavailable states;
- a universal context-length threshold;
- causal proof that visibility alone determines specialist utility;
- generic novelty in evidence selection, gating, MoE, Learning-to-Defer, long/short-term modeling, or feature fusion;
- SOTA / leaderboard superiority;
- calibrated event-level utility prediction or near-Oracle routing;
- generalization beyond the evaluated live-stream settings or arbitrary auxiliary specialists.