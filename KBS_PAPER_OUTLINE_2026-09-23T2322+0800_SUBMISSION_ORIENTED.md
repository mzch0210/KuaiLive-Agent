# Submission-oriented manuscript outline for *Knowledge-Based Systems*

> **INDEPENDENT / NON-AUTHORITATIVE MANUSCRIPT OUTLINE**  
> This document is a paper-facing writing outline. It does not replace frozen experimental protocols, immutable test results, or prior authoritative snapshots unless explicitly promoted by the authors.

**Generated:** 2026-09-23T23:22+08:00  
**Target journal:** *Knowledge-Based Systems*  
**Project:** `mzch0210/KuaiLive-Agent`

---

# Proposed title

## Preferred

> **When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation**

## Conservative alternative

> **Base-Relative Value of Relationship Memory in Live-Streaming Recommendation**

The title should foreground the scientific question and the Base-relative valuation concept rather than generic routing or gating.

---

# Abstract

Structure the abstract around one scientific question, one mechanism result, one decision result, and one held-out validation result.

1. **Problem.** Strong sequential recommenders compress or truncate interaction history, while auxiliary historical evidence is not automatically useful because its value depends on what the Base already represents and on the operating recommendation regime.
2. **Formulation.** Treat persistent relationship Memory as a transparent specialist and define event-level specialist-minus-base ranking utility.
3. **Mechanism.** Characterize represented, recoverable-but-unrepresented, and unavailable relationship evidence; report frozen DEV-to-TEST replication and the context-length intervention showing that the same persistent evidence loses marginal value once a larger Base context represents it.
4. **Decision.** Predict specialist-relative utility rather than generic Base difficulty; show that Utility more strongly enriches recoverable events whereas Difficulty disproportionately selects unavailable events under the same invocation budget.
5. **Validation.** Report the KuaiLive regime reversal and the frozen Twitch/LiveRec untouched TEST result.
6. **Qualification.** State that evidence state structures but does not uniquely determine utility and that substantial Oracle headroom remains.

Prioritize two quantitative anchors rather than a long result list:

- **Mechanism:** recoverable-to-represented transitions under context expansion reduce specialist-minus-base utility by approximately `0.42–0.45` NDCG@10 while canonical Memory is fixed.
- **Held-out decision:** on untouched Twitch/LiveRec TEST, Selective Utility improves over Base by `+0.00772` NDCG@10 and over exact-budget Difficulty by `+0.00644`.

Avoid introducing the paper as a new gating architecture, new Memory network, or generic Learning-to-Defer method.

---

# 1. Introduction

## 1.1 Motivation and scientific gap

Establish the following argument in sequence:

1. Sequential recommenders obtain strong performance by representing a bounded or compressed interaction history.
2. Auxiliary evidence sources may retain information absent from the current Base representation, but more evidence is not necessarily useful: it may be redundant, unavailable for the target, or harmful in the current decision regime.
3. Existing recommendation research extensively studies **how to integrate** long/short-term, multimodal, collaborative, or knowledge signals; a distinct question is whether an auxiliary source has **positive marginal value relative to the current Base** for a particular event.
4. Persistent user–creator relationships in live-stream recommendation provide a transparent setting in which the same target-specific evidence can be represented by the Base, recoverable only from older history, or unavailable.
5. This motivates **Base-relative evidence valuation** rather than judging the specialist by standalone accuracy or routing merely on Base difficulty.

Use the central sentence:

> **The central problem is not whether more historical evidence improves recommendation, but whether that evidence is incremental relative to the information already represented by the Base.**

## 1.2 Research questions

Use four research questions.

**RQ1 — Regime dependence.** How does aggregate relationship-Memory value change across recommendation regimes, and can those changes be decomposed into evidence-state composition and state-specific specialist utility?

**RQ2 — Base-relative mechanism.** How do represented, recoverable-but-unrepresented, and unavailable relationship evidence structure specialist utility, and does changing Base visibility capacity alter the marginal value of the same persistent evidence?

**RQ3 — Specialist decision.** Can specialist-minus-base utility be estimated from deployment-observable user/state and Base-confidence information well enough to improve a strong Base, and does it identify specialist-helpful events more effectively than generic Base Difficulty under the same invocation budget?

**RQ4 — Robustness, transfer, and deployment.** Do the conditional-specialist findings survive alternative explanations, independent Base realizations, frozen cross-platform evaluation, and practical accuracy–invocation–latency constraints?

## 1.3 Contributions

Use exactly three headline contributions.

### C1 — Base-relative evidence valuation

Formulate a transparent auxiliary relationship-evidence source as a specialist whose value is measured by its **marginal ranking utility relative to a strong Base**, not by standalone specialist performance and not by Base difficulty alone.

### C2 — Evidence-state mechanism with Base-visibility intervention

Identify represented, recoverable-but-unrepresented, and unavailable relationship-evidence states; show frozen DEV-to-TEST replication of strong conditional heterogeneity; and provide DEV-only intervention evidence that the same persistent evidence loses specialist advantage when a larger Base context comes to represent it.

### C3 — Conditional specialist decision with multi-regime and frozen validation

Show that Utility and Difficulty select materially different event compositions at an exact matched budget, connect this difference to specialist-helpful evidence states, and validate selective specialist use across KuaiLive regimes, strong Base controls, independent seeds, and an untouched second-platform TEST.

Do **not** claim novelty for generic gating, mixture-of-experts, Learning-to-Defer, long/short-term modeling, multimodal/evidence fusion, or the weighted Memory formula itself.

---

# 2. Related Work

Organize Related Work around the nearest conceptual neighbors rather than a broad catalogue.

## 2.1 Sequential, repeat-aware, and long-term recommendation

Cover short-term intent, long-term preference, repeat behavior, and finite-context sequential modeling.

Positioning boundary:

> The contribution is not jointly modeling long- and short-term preference; it is evaluating the **marginal value of a separately maintained persistent relationship-evidence source relative to the Base representation**.

## 2.2 Knowledge-aware, multimodal, and auxiliary-information recommendation

Discuss adaptive fusion, complementarity, redundancy suppression, denoising, and reliability-aware evidence modeling.

Positioning boundary:

> Representation-level fusion asks how heterogeneous signals should be integrated; **Base-relative evidence valuation asks whether a particular auxiliary source is incremental enough to be worth using at all**.

## 2.3 Learning-to-Defer, expert routing, and selective prediction

Acknowledge expert allocation, deferral, and accuracy–cost optimization as established problems.

State explicitly:

> The paper does not propose a new general deferral theory. It studies a recommendation-specific evidence valuation problem and uses a relative-utility estimator to operationalize selective specialist use.

Define the Difficulty model as a **mechanistic control**, not as a representative baseline for all prior routing methods:

> Difficulty tests whether Base weakness alone is sufficient to identify relationship-specialist value; it is not intended as a proxy for all expert-routing or Learning-to-Defer approaches.

## 2.4 Negative transfer and harmful auxiliary evidence

Use negative transfer as a conceptual connection: auxiliary information can be redundant or harmful when it lacks positive marginal value relative to the Base. Do not claim a causal negative-transfer mechanism.

## 2.5 Live-stream recommendation

Motivate persistent user–creator relationships, repeated viewing, active-room candidate dynamics, and temporal availability as properties that make Base-relative evidence valuation scientifically meaningful.

## 2.6 Nearest-work differentiation table

Include a compact table in the manuscript or Supplementary Material.

| Nearest direction | Typical question | Distinction of this paper |
|---|---|---|
| Adaptive long/short-term gating | How should heterogeneous or temporal preference signals be fused? | Whether a separate relationship-evidence source has positive **Base-relative marginal value** |
| Multimodal complementarity / redundancy | How can complementary information be extracted and noisy/redundant content suppressed? | Event-level specialist-minus-base utility rather than representation-level fusion |
| Reliability-aware recommendation | How reliable are interaction/content signals? | Whether target-specific persistent evidence is incremental relative to a strong Base |
| Expert networks / MoE | Which representation or expert should process an input? | Transparent evidence specialist with an interpretable availability/visibility mechanism |
| Learning-to-Defer | How should inputs be assigned to predictors/experts under loss or cost? | Recommendation-specific characterization of **why** this specialist is useful on some events |
| Negative-transfer methods | How can harmful transferred information be reduced? | Conditional marginal value of one persistent evidence source relative to Base representation |

The purpose of this table is precise differentiation, not a claim that adjacent work is inferior or absent.

---

# 3. Problem Formulation

## 3.1 Recommendation event and event-level ranking utility

Let `x` be a recommendation event, `B` a strong sequential Base, and `M` a relationship-memory specialist. For the single relevant target at cutoff `K`, define event-level NDCG utility explicitly:

\[
u_K(A,x)=
\begin{cases}
1/\log_2(r_A(x)+1), & r_A(x)\le K,\\
0, & r_A(x)>K,
\end{cases}
\]

where `r_A(x)` is the 1-indexed rank of the target under model `A`.

Define specialist-minus-base utility:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

This is the primary Base-relative evidence-value quantity.

## 3.2 Conditional utility estimation

For deployment-observable information `z` and recommendation regime `r`:

\[
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The learned selector estimates `\hat\eta(z)` without access to analysis-only relationship-state labels.

## 3.3 Decision rule

For a cost-sensitive deployment setting:

\[
\pi^*(z)=\mathbf 1\left[
\mathbb E[\Delta_m(X)\mid Z=z]
>
\lambda\,\mathbb E[c(X)\mid Z=z]
\right].
\]

For the experiments with an exact invocation budget `B_q`, define the policy as selecting the top `B_q` events by predicted utility:

\[
\pi_{B_q}=\operatorname{Top}_{B_q}\{\hat\eta(z_i)\}.
\]

Use this bridge to align the formal decision rule with the exact-budget evaluation protocol.

## 3.4 Regime-level decomposition

Let `S` denote Base-relative evidence state. Then:

\[
\mathbb E[\Delta_m\mid R=r]
=
\sum_s P(S=s\mid R=r)\,\mathbb E[\Delta_m\mid S=s,R=r].
\]

This separates:

- **state-composition change:** `P(S=s|R=r)`;
- **state-specific utility change:** `E[Δ_m|S=s,R=r]`.

Treat this as an analytical decomposition rather than a new theorem.

---

# 4. Base-Relative Evidence Valuation Framework

## 4.1 Strong sequential Bases

Describe the two reference Bases:

- KuaiLive identity-aware Dual-ID sequential Base;
- official LiveRec availability-aware and repeat-aware Base for Twitch.

Use comparator results only to establish that these are credible strong references under the evaluation protocol. Avoid SOTA or leaderboard claims.

## 4.2 Transparent relationship-memory specialist

Use the frozen transferred specialist score:

\[
0.45\,Short + 0.45\,Long + 0.10\,Popularity.
\]

Explain the three components and tie-breaking rule.

The specialist is intentionally transparent so that evidence availability and marginal utility remain inspectable. Do not present this weighted formula as the methodological novelty.

## 4.3 Base-relative relationship-evidence states

For Base context length `L`, define:

- `V_L(x)=1` if the target creator appears in the Base-visible input sequence;
- `H(x)=1` if the target creator exists in canonical pre-target history outside that visible sequence.

| Empirical state | `V_L(x)` | `H(x)` | Interpretation |
|---|---:|---:|---|
| recent-visible | 1 | any | **represented evidence** |
| long-horizon-only | 0 | 1 | **recoverable but unrepresented evidence** |
| unseen | 0 | 0 | **unavailable target-specific evidence** |

These states are **analysis concepts only**, never selector features.

Do not treat them as deterministic utility classes. The intended abstraction is:

\[
\Delta_m
=
f(\text{Base-relative evidence state},\text{operating regime}),
\]

with recency as a finer within-state modifier.

## 4.4 Relative-utility estimator

Estimate `\hat\eta(z)` from observable user/history state and Base-confidence features. The HGB implementation is operational rather than the source of novelty.

## 4.5 Difficulty control, Oracle, and serving cost

Use a matched model family and the same observable information for the generic Difficulty control.

- **Difficulty:** tests whether Base weakness alone identifies useful specialist invocation.
- **Oracle:** exact-budget upper bound for analysis only.
- **Serving analysis:** Base cost + selector overhead + invoked specialist cost, including latency/throughput and memory/cache footprint.

---

# 5. Experimental Design

## 5.1 Complementary roles of the two platforms

Explain why the two datasets serve distinct identification roles rather than treating them as two interchangeable benchmarks.

### KuaiLive

Use for:

- candidate-regime reversal;
- temporal-regime effects;
- selective decision gains;
- state-specific candidate-regime decomposition.

### Twitch / LiveRec

Use for:

- strong official Base;
- frozen DEV discovery and untouched TEST validation;
- evidence-state replication;
- context-length intervention;
- Utility/Difficulty/Oracle selection-composition analysis.

## 5.2 Recommendation regimes

Describe sampled-active, full-active, standard temporal, and strict temporal regimes where applicable. Make candidate construction and temporal availability differences explicit.

## 5.3 Frozen validation protocol

Main-text summary:

> **DEV discovery and policy freeze → untouched one-shot TEST evaluation.**

Keep hashes, immutable artifacts, complete chronology, and execution provenance in reproducibility materials.

## 5.4 Metrics and statistical inference

Primary metric: NDCG@10.  
Secondary metric: H@10 / HR@10 as appropriate.

Use:

- paired user-level bootstrap intervals;
- exact matched invocation budgets;
- mean ± SD and sign consistency across independent Base training seeds.

Do not reinterpret within-seed bootstrap intervals as across-seed confidence intervals.

## 5.5 Evidence hierarchy

Explicitly distinguish evidential roles.

### Primary confirmatory evidence

- frozen DEV relationship-state structure;
- untouched TEST replication;
- frozen selective-utility TEST result.

### Primary mechanistic strengthening

- DEV-only context-length intervention with canonical Memory held fixed;
- within-event recoverable→represented transitions;
- fixed-composition KuaiLive candidate-regime decomposition;
- Utility/Difficulty/Oracle selection composition at matched budgets.

### Secondary robustness and refinement

- component attribution;
- alternative-explanation stratification;
- positive-delta fractions;
- Memory-parameter sensitivity;
- context-distance consistency and fine recency bins;
- feature-family ablation;
- independent training seeds;
- strong-Base comparator checks;
- complexity and efficiency.

This hierarchy should control the order and strength of claims in the Results section.

---

# 6. Results

## 6.1 RQ1: Aggregate specialist value is regime-dependent

Begin with the paradox rather than the mechanism.

Key KuaiLive aggregate results:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active: Memory−Base approximately `+0.03367`, native Selective−Base approximately `+0.05345`;
- strict temporal: Selective−Base approximately `+0.07282` / `+0.09743`.

### Candidate-regime decomposition

For sampled-active versus full-active, use the same 10,222 events and show that evidence-state prevalence is identical while aggregate Memory−Base reverses from `−0.05125` to `+0.03367`.

| Base-relative state | Sampled Δ | Full-active Δ | Full−Sampled shift | 95% CI |
|---|---:|---:|---:|---:|
| represented | +0.11508 | +0.19261 | +0.07752 | [+0.07046,+0.08472] |
| recoverable-but-unrepresented | +0.17779 | +0.08049 | −0.09731 | [−0.14897,−0.04647] |
| unavailable | −0.20060 | −0.10251 | +0.09809 | [+0.08988,+0.10649] |

Conclusion:

> **Regime dependence is not reducible to changing state prevalence; candidate regime can change specialist value within the same evidence state.**

Do not generalize this fixed-composition conclusion to temporal regimes without direct decomposition evidence.

## 6.2 RQ2: Base-relative evidence state structures specialist utility

### Frozen DEV → untouched TEST replication

| Evidence state | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| represented | −0.01995 | −0.01935 |
| recoverable-but-unrepresented | **+0.23097** | **+0.22045** |
| unavailable | −0.19562 | −0.18215 |

Interpret these as Twitch/LiveRec conditional patterns, not universal signs.

### Context-length Base-visibility intervention

Keep canonical Memory fixed (`NDCG@10 = 0.52170`) while varying Base context:

| Base context | Base NDCG@10 | Memory−Base | 95% CI |
|---:|---:|---:|---:|
| 8 | 0.52619 | −0.00450 | [−0.00756,−0.00127] |
| 16 | 0.57185 | −0.05016 | [−0.05307,−0.04731] |
| 32 | 0.59663 | −0.07493 | [−0.07766,−0.07227] |

Use within-event state transitions as the principal mechanism result:

| Transition | n | Δ before | Δ after | change | 95% CI |
|---|---:|---:|---:|---:|---:|
| L8→L16 recoverable→represented | 5,055 | +0.29388 | −0.15360 | **−0.44748** | [−0.45767,−0.43730] |
| L16→L32 recoverable→represented | 3,617 | +0.25755 | −0.17474 | **−0.43229** | [−0.44381,−0.42054] |
| L8→L32 recoverable→represented | 8,672 | +0.27782 | −0.14114 | **−0.41896** | [−0.42685,−0.41112] |

Conclusion:

> **Persistent relationship evidence has strongly Base-relative marginal value: when a larger Base context comes to represent the same evidence, specialist advantage contracts sharply.**

Use **interventional support**, not causal theorem, in the wording.

### Component attribution and recency refinement

Report compactly in the main text:

- Long-only on recoverable DEV events: `ΔNDCG@10 = +0.33688`;
- Short-only and Popularity-only: negative in the same regime;
- recency is non-monotonic, including a positive `1–4` pocket.

Move the full distance-bin table and detailed sensitivity matrices to Supplementary Material.

## 6.3 RQ3: Specialist solvability is not Base difficulty

Start with exact-budget performance, then explain the result through event composition.

### Selection composition on frozen Twitch DEV

Population prevalence:

- represented `52.35%`;
- recoverable `12.54%`;
- unavailable `35.11%`.

| Router | Represented | Recoverable | Unavailable |
|---|---:|---:|---:|
| Utility selection share | 29.70% (`0.57×`) | 34.13% (**`2.72×`**) | 36.17% (`1.03×`) |
| Difficulty selection share | 11.98% (`0.23×`) | 20.89% (**`1.67×`**) | 67.13% (**`1.91×`**) |
| Oracle selection share | 50.39% | 43.00% (**`3.43×`**) | 6.61% |

Conclusion:

> **Base Difficulty disproportionately identifies hard-but-unavailable events, whereas relative Utility more strongly targets events containing recoverable specialist evidence.**

Relationship-state labels remain post-hoc analysis variables and are not used by the selector.

## 6.4 RQ4: Frozen second-platform validation and robustness

### Untouched Twitch/LiveRec TEST

At exact budget `K=6,650` (`15.04%` invocation):

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

> **Precise event-level calibration remains difficult, but coarse specialist-value ranking is sufficient to identify a useful positive tail.**

### Robustness summary

Keep main text concise and move detailed matrices to Supplementary Material:

- recoverable-state positive utility remains positive across history length, creator exposure, candidate count, and repeat-propensity strata;
- Memory sensitivity preserves the main Twitch state signs;
- independent Base seeds preserve `Selective > Base` and `Utility > Difficulty`;
- same-protocol comparator checks establish credible strong Bases without SOTA claims.

## 6.5 Deployment trade-off

Report accuracy versus invocation rate, latency/throughput, and memory/cache footprint. Treat deployment evidence as practical validation rather than a separate algorithmic contribution.

---

# 7. Discussion

## 7.1 Evidence valuation before evidence integration

Emphasize the methodological implication:

> **An auxiliary evidence source should not be evaluated solely by standalone predictive strength; its value depends on what the Base already represents in the current recommendation regime.**

This is the main conceptual bridge from live-stream relationship Memory to the broader KBS audience.

## 7.2 Evidence state structures but does not determine utility

Use the three states as an explanatory coordinate, not a universal taxonomy of signs.

- Twitch: represented is negative in aggregate, recoverable strongly positive, unavailable negative.
- KuaiLive: represented can be positive, and state-specific utility changes when the candidate regime changes despite fixed state prevalence.

Therefore avoid `state → fixed sign`. Use:

\[
\Delta_m=f(\text{evidence state},\text{operating regime}),
\]

with recency as a finer modifier.

## 7.3 Why relative Utility differs from Difficulty

Explain that Base weakness is not sufficient: some difficult events contain no target-specific evidence that the relationship specialist can recover. Use the selection-composition result to connect mechanism to decision performance.

## 7.4 Transparency versus architectural complexity

Defend the simple specialist as a scientific design choice: its transparency makes evidence availability, component attribution, and marginal value inspectable. Do not argue that the weighted specialist is architecturally superior to learned long-memory models.

## 7.5 Relationship to deferral and expert-routing theory

State that the paper instantiates a fixed-specialist decision problem rather than advancing generic deferral theory. The scientific contribution is the evidence-valuation mechanism and its recommendation-specific consequences.

## 7.6 Remaining headroom

Use modest utility-ranking correlation and limited Oracle capture to identify better utility estimation as the principal algorithmic opportunity for future work.

## 7.7 Limitations and external validity

Explicitly limit conclusions to:

- evaluated live-stream platforms;
- strong finite-context sequential Bases;
- explicit persistent user–creator relationship evidence;
- offline ranking outcomes.

Do not imply causal effects on satisfaction, engagement, conversion, or GMV.

---

# 8. Reproducibility and Data Availability

Add a short formal section in the paper or immediately before the Conclusion.

Report:

- public datasets and access sources;
- code repository;
- frozen experiment commits;
- preprocessing and candidate construction;
- random seeds;
- immutable DEV/TEST policy-freeze procedure;
- Supplementary reproducibility package with full parameter tables, hashes, and detailed robustness outputs;
- Data Availability Statement consistent with Elsevier requirements.

Keep workflow failures/recoveries and low-level CI logs out of the main manuscript; preserve them only in the reproducibility package where they are needed for auditability.

---

# 9. Conclusion

Close with three points only:

1. **Scientific finding:** relationship Memory has no fixed global ordering relative to a strong Base; its marginal value is Base-relative and regime-dependent.
2. **Mechanism:** recoverable persistent evidence is especially valuable when absent from the Base representation, and its specialist advantage contracts when the Base comes to represent the same evidence.
3. **Decision implication:** specialist-minus-base utility is more appropriate than generic Base difficulty for selective relationship-specialist use, although current utility estimation remains far from Oracle.

Avoid introducing new limitations, literature, or claims in the Conclusion.

---

# Main figures and tables

## Figure 1 — Base-relative evidence valuation framework

Show:

- strong finite-context Base;
- transparent relationship-memory specialist;
- conceptual evidence states;
- deployment-observable features feeding `\hat\eta(z)`;
- specialist-minus-base utility decision;
- optional cost / exact-budget decision boundary.

Mark evidence states as analysis concepts rather than selector inputs.

## Table 1 — Regime performance and fixed-composition decomposition

Combine compact KuaiLive regime results with sampled-active/full-active state-specific utility shifts. Make visually clear that the candidate-regime sign reversal occurs with unchanged state prevalence.

## Figure 2 — Signature mechanism figure

Prioritize this as the manuscript's central scientific figure.

### Panel A — Frozen evidence-state replication

DEV and untouched TEST Memory−Base for represented, recoverable, and unavailable states.

### Panel B — Base-context intervention

Show `L=8/16/32`, canonical Memory fixed, and within-event recoverable→represented transitions with approximately `0.42–0.45` decline in specialist-minus-base utility.

Move fine context-distance bins to Supplementary Material unless space permits a small inset.

## Table/Figure 3 — Utility versus Difficulty

Combine:

- exact-budget NDCG@10 / H@10;
- selected-state composition;
- enrichment relative to population;
- Oracle composition as an analysis upper bound.

## Table 4 — Frozen second-platform TEST and robustness summary

Keep the primary held-out results in the main table. Put full sensitivity, seed, comparator, and alternative-explanation matrices in Supplementary Material.

## Figure/Table 5 — Accuracy–invocation–latency/footprint frontier

Use only if space allows; otherwise move detailed serving curves to Supplementary Material and retain one compact deployment summary in the main text.

---

# Supplementary Material structure

## S1. Dataset preprocessing and candidate construction
## S2. Frozen protocol and reproducibility details
## S3. Full Base comparator results
## S4. Memory component and parameter sensitivity
## S5. Context-distance and recency-bin analyses
## S6. Alternative-explanation stratification
## S7. Feature-family ablations and training-seed results
## S8. Complexity, latency, throughput, and footprint details
## S9. Additional bootstrap intervals and H@10 tables

---

# Claim discipline to maintain during drafting

Supported manuscript-level claims:

- relationship Memory is regime-dependent rather than globally ordered against Base;
- Base-relative evidence state strongly structures specialist utility in Twitch/LiveRec;
- recoverable-but-unrepresented evidence is the dominant positive Twitch relationship-memory regime;
- frozen DEV state structure reproduces on untouched TEST;
- controlled context-length intervention supports a Base-relative visibility interpretation;
- evidence state does not uniquely determine utility across regimes;
- Utility and Difficulty select materially different event compositions at the same budget;
- Utility better enriches recoverable events, while Difficulty disproportionately selects unavailable events;
- selective Utility improves strong Bases in the evaluated settings and transfers under frozen second-platform evaluation;
- substantial Oracle headroom remains.

Avoid claims of:

- a universal theory of auxiliary evidence valuation;
- fixed utility signs for represented/recoverable/unavailable states;
- a universal context-length threshold;
- causal proof that visibility alone determines specialist utility;
- generic novelty in gating, MoE, Learning-to-Defer, long/short-term modeling, or feature fusion;
- SOTA / leaderboard superiority;
- calibrated event-level utility prediction or near-Oracle routing;
- generalization beyond the evaluated live-stream settings.
