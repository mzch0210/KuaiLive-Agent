# KBS paper outline — theory-refined academic guidance

> **INDEPENDENT / NON-AUTHORITATIVE OUTLINE**  
> This document is a manuscript-structure guide for paper development. It does not replace frozen experimental protocols or prior authoritative snapshots unless explicitly promoted by the authors.

**Generated:** 2026-09-23T14:41+08:00  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Project:** `mzch0210/KuaiLive-Agent`

---

# 1. Paper positioning

Position the manuscript as a study of **Base-relative evidence valuation and conditional specialist use in recommendation**, instantiated through explicit persistent user–creator relationship evidence.

## 1.1 General scientific question

> **When is an auxiliary evidence source genuinely incremental relative to what a strong Base already represents?**

This is the higher-level methodological question. The paper should then instantiate it in live-stream recommendation:

> **When does persistent relationship evidence provide incremental ranking value beyond a strong finite-context sequential recommender, and can that marginal value be predicted well enough to govern selective specialist use?**

The paper should not be positioned as:

- a new generic gating, mixture-of-experts, selective-prediction, or Learning-to-Defer method;
- a new long/short-term recommendation architecture;
- an LLM-agent or agentic-recommendation system;
- a claim that relationship Memory is globally superior to a strong sequential Base;
- a live-stream application paper whose novelty rests mainly on the domain;
- a generic external-knowledge integration or feature-fusion paper.

Use **relationship evidence**, **persistent relationship representation**, and **relationship-memory specialist** as the primary terminology. When using the word *knowledge*, clarify that the specialist is separate from the Base representation but uses the same underlying interaction data rather than an external dataset.

Preferred framing:

> **Relationship Memory is a regime-dependent specialist. Its value is not determined by the amount of history alone, but by whether target-specific evidence is already represented in the Base’s visible sequence, remains recoverable only from older history, or is unavailable. Specialist-minus-base utility therefore measures Base-relative evidence value rather than standalone specialist strength.**

---

# 2. Recommended title

## Primary

> **Learning When Relationship Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Conservative alternative

> **Conditional Specialist Utility of Relationship Memory in Live-Streaming Recommendation**

Retain **Live-Streaming Recommendation** in the title unless additional conventional sequential-recommendation domains are evaluated. The conceptual discussion may generalize to auxiliary evidence valuation, but the title and empirical claims should remain within the evaluated domain.

---

# 3. Central thesis and novelty boundary

## 3.1 Central thesis

> **Explicit relationship Memory has no fixed global ordering relative to a strong sequential Base. Its marginal ranking utility depends on the Base-relative state of target-specific relationship evidence and on recency. Evidence that is already represented in the Base is often redundant, evidence that remains recoverable only from older history forms the dominant positive specialist regime, and unavailable evidence cannot be repaired by the relationship specialist. This structured heterogeneity explains why Base difficulty is not equivalent to specialist solvability and motivates specialist-minus-base utility as the decision target.**

## 3.2 Base-relative evidence valuation before evidence integration

The paper should distinguish two questions:

1. **Evidence integration:** how should multiple representations or information sources be fused?
2. **Evidence valuation:** does a particular auxiliary evidence source contain positive marginal value relative to what the Base already represents?

This paper addresses the second question first.

The core methodological distinction is:

> **Before asking how to integrate additional evidence, ask whether that evidence is genuinely incremental relative to the Base representation.**

Accordingly, the paper should contrast **Base-relative evidence valuation** with representation-level feature fusion, multimodal fusion, long/short-term aggregation, or generic expert routing.

## 3.3 Defensible novelty

The contribution should be presented as a combined scientific contribution rather than novelty in any single standard component:

1. formulate a transparent **Base-relative evidence valuation** problem through specialist-minus-base ranking utility;
2. identify interpretable **Base-relative relationship-evidence states** that structure specialist benefit and harm;
3. show that **Base difficulty and specialist solvability are decisionally distinct** under exact matched invocation budgets;
4. demonstrate that aggregate specialist value changes with recommendation regime and validate the conditional-specialist principle under strong Base models and a frozen second-platform untouched test.

Do not claim novelty for gating, expert selection, long/short-term modeling, evidence fusion, external information integration, or complementarity in isolation.

---

# 4. Principal contributions

Use three main contributions in the Introduction.

## Contribution 1 — Base-relative evidence valuation and specialist decision

Formulate relationship Memory as a specialist whose value is defined relative to a strong Base:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x),
\]

where `B` is the Base, `M` the relationship specialist, and `u_K` event-level ranking utility.

For observable routing information `z`, estimate:

\[
\eta(z)=\mathbb E[\Delta_m(X)\mid Z=z].
\]

The methodological emphasis is not the difference formula itself, but the change in evaluation target: an auxiliary evidence source is judged by its **marginal utility relative to the Base**, not by standalone accuracy and not by Base difficulty alone.

Use this quantity to motivate selective specialist invocation and compare it with a matched-budget generic Difficulty target.

Explicitly relate the formulation to Learning-to-Defer and expert routing. Do not present it as a new general deferral theory.

## Contribution 2 — Representation-relative relationship-evidence states

Characterize specialist utility through three empirical relationship states and interpret them as Base-relative evidence states:

| Empirical state | Base-relative evidence interpretation |
|---|---|
| recent-visible | **represented evidence** |
| long-horizon-only | **recoverable but unrepresented evidence** |
| unseen | **unavailable target-specific evidence** |

The principal mechanism claim is:

> **Persistent relationship evidence is most complementary when it remains recoverable from older history but is no longer represented in the Base’s visible sequence.**

Recency further qualifies this structure: the ultra-recent positive pocket shows that specialist utility is not a monotonic function of relationship distance.

This contribution should be framed as an interpretable characterization of **specialist solvability**, not as a generic claim that long-term preference is important.

## Contribution 3 — Multi-regime and frozen external validation

Validate the conditional-specialist principle across:

- KuaiLive candidate and temporal regimes;
- strong-Base controls;
- independent Base training seeds;
- a second live-stream platform using a strong official LiveRec Base;
- a frozen DEV-to-untouched-TEST protocol;
- matched-budget Difficulty and Oracle controls;
- accuracy–invocation–latency/footprint analysis.

Treat strong-base competitiveness, parameter sensitivity, seed robustness, and efficiency as validity evidence rather than separate headline contributions.

---

# 5. Formal problem formulation

Let `x` denote a recommendation event, `B` a strong sequential Base, `M` an explicit relationship-memory specialist, and `u_K(A,x)` event-level ranking utility at cutoff `K`.

## 5.1 Specialist-minus-base utility

Define:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

For observable information `z` and recommendation regime `r`:

\[
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The learned selector estimates `\hat\eta(z)` without using analysis-only relationship-state labels.

If specialist invocation incurs incremental cost `c(x)` with cost weight `\lambda`, the idealized decision is:

\[
\pi^*(z)=\mathbf 1\left[
\mathbb E[\Delta_m(X)\mid Z=z]
>
\lambda\,\mathbb E[c(X)\mid Z=z]
\right].
\]

For approximately fixed or negligible incremental cost, the rule reduces to selecting positive expected specialist utility.

Treat this as a task-specific decision formulation, not a new theorem in deferral, selective prediction, or cost-sensitive routing.

## 5.2 Regime-level decomposition

Let `S` denote the Base-relative relationship-evidence state. Aggregate specialist utility in regime `r` can be decomposed as:

\[
\mathbb E[\Delta_m\mid R=r]
=
\sum_s
P(S=s\mid R=r)
\,\mathbb E[\Delta_m\mid S=s,R=r].
\]

This decomposition provides an analytical bridge between regime-level reversals and event-level specialist heterogeneity.

Interpretation:

> **Aggregate Memory value can change because recommendation regimes change the composition of evidence states, the state-specific utility of the specialist, or both.**

Do not claim that prevalence shift alone explains the observed regime reversal unless explicitly demonstrated.

## 5.3 Difficulty versus specialist solvability

Define generic Base Difficulty conceptually as high expected loss or low utility of `B`. Difficulty answers:

> Where is the Base weak?

Specialist-relative utility answers:

> Where can this particular specialist improve the Base?

These differ because a difficult event may contain no target-specific evidence recoverable by the specialist.

The key conceptual relation is:

\[
\text{Base difficulty}
\not\Rightarrow
\text{specialist solvability}.
\]

This distinction should connect the relationship-state mechanism to the routing result.

---

# 6. Base-relative relationship-evidence states and mechanism

Let:

- `V(x)=1` if the target creator appears in the exact visible input sequence used by the Base;
- `H(x)=1` if the target creator appears in chronological pre-target history outside that visible sequence.

Define three analysis states:

| Relationship state | `V(x)` | `H(x)` | Base-relative evidence state | Interpretation |
|---|---:|---:|---|---|
| recent-visible | 1 | any | represented | target-specific relationship evidence is already represented in the Base input |
| long-horizon-only | 0 | 1 | recoverable but unrepresented | target-specific relationship evidence exists in older history but is outside the visible Base sequence |
| unseen | 0 | 0 | unavailable | no prior target-specific relationship evidence is available to this specialist |

These labels are **diagnostic only**. They must never be described as online selector features.

## 6.1 Confirmatory relationship-state evidence

Present the frozen DEV structure and untouched TEST replication together:

| Relationship state | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| recent-visible | −0.01995 | −0.01935 |
| **long-horizon-only** | **+0.23097** | **+0.22045** |
| unseen | −0.19562 | −0.18215 |

The main interpretation is not that a numerical horizon is universally optimal. The result supports the proposition that specialist utility depends on whether relevant evidence is already represented, recoverable but unrepresented, or unavailable.

## 6.2 Mechanism attribution

Use component evidence to identify which specialist information source is associated with the positive recoverable-but-unrepresented regime.

On long-horizon-only DEV events:

- Long-only: `ΔNDCG@10 = +0.33688`;
- Short-only: negative;
- Popularity-only: negative.

Interpretation:

> **The positive outside-visible-sequence effect is associated specifically with persistent long-term relationship evidence rather than generic popularity or short-term recurrence.**

Do not claim Long-only is globally superior.

## 6.3 Context-distance consistency diagnostic

The LiveRec Base uses an exact 16-step visible sequence, and the relationship-state definition already refers to that visible context. Therefore the 16-step distance result is a **consistency diagnostic and refinement**, not an independent validation of the relationship-state definition.

Report that:

- last seen within 16 interactions: Memory−Base `−0.01980`;
- last seen beyond 16 interactions: Memory−Base `+0.23057`.

Use this analysis to show alignment between the coarse diagnostic states and actual distance structure, not to claim a universal 16-step threshold.

## 6.4 Recency refinement

Distance-bin evidence shows:

- 1–4: `+0.04606`;
- 5–8: `−0.06511`;
- 9–16: `−0.15268`;
- 17–32: `+0.25668`;
- 33–64: `+0.20707`;
- 65+: `+0.12965`;
- unseen: `−0.19562`.

Therefore the defensible mechanism is:

\[
\text{specialist utility}
\approx
f(\text{Base-relative evidence state},\ \text{recency regime}),
\]

not a monotonic distance law.

The 1–4 positive pocket should be treated as DEV-only mechanism refinement unless independently confirmed under a frozen protocol.

---

# 7. Research questions

**RQ1 — Regime dependence.** How does the aggregate value of explicit relationship Memory change across candidate and temporal recommendation regimes, and how can this variation be interpreted through the composition and utility of Base-relative evidence states?

**RQ2 — Specialist solvability mechanism.** Under what visibility and recency conditions is target-specific relationship evidence represented, recoverable but unrepresented, or unavailable relative to a strong finite-context Base, and which specialist component is associated with the positive recoverable regime?

**RQ3 — Specialist decision.** Can specialist-minus-base utility be estimated from observable user/history state and Base-confidence information well enough to improve a strong Base, and does this target contain decision-relevant information beyond generic Base Difficulty?

The logical bridge between RQ2 and RQ3 should be explicit:

> **RQ2 explains why the specialist is solvable or unsolvable in different evidence states; RQ3 asks whether that latent conditional value can be predicted indirectly from observable features.**

**RQ4 — Robustness and transfer.** Do the selective advantage and relationship-state sign structure survive independent Base realizations and reproduce on a second live-stream platform under a frozen untouched evaluation protocol?

**RQ5 — Deployment.** What accuracy–invocation–latency/footprint trade-off follows from specialist use, how informative is the utility estimator, and how much same-budget Oracle headroom remains?

---

# 8. Method section structure

## 8.1 Strong sequential Bases

Describe:

- KuaiLive identity-aware Dual-ID Base;
- frozen official LiveRec availability-aware and repeat-aware Base.

Use same-protocol comparator evidence only to establish credible scientific reference models. Avoid SOTA or leaderboard claims.

## 8.2 Explicit relationship-memory specialist

Use the frozen transferred score:

\[
0.45\,Short + 0.45\,Long + 0.10\,Popularity.
\]

Explain each component transparently.

The specialist is intentionally simple and interpretable so that the availability and marginal value of persistent relationship evidence can be separated from Base representation-learning complexity.

Do not present the weighted formula as the algorithmic novelty.

## 8.3 Relative-utility estimator

Estimate `\hat\eta(z)` from observable state and Base-confidence features.

The HGB selector is operational rather than the source of novelty.

The selector does not observe diagnostic relationship-state labels. Its task is to infer expected specialist value from deployment-available proxies.

## 8.4 Generic Difficulty control

Use the same observable information and a comparable model family to estimate Base difficulty.

Evaluate Utility and Difficulty under **exact matched invocation budgets**.

Conceptual distinction:

> **Difficulty asks where the Base is weak; Utility asks where this particular specialist can recover useful incremental evidence.**

Do not generalize the Difficulty control to all existing deferral or routing methods.

## 8.5 Oracle and serving cost

Use the exact-budget Oracle only as an analysis upper bound.

Serving analysis should include:

- Base inference;
- selector overhead;
- specialist invocation;
- throughput;
- memory/model/cache footprint where relevant.

Invocation rate alone is not a sufficient compute proxy.

---

# 9. Experimental design

## 9.1 Datasets and evaluation regimes

Use:

- KuaiLive;
- Twitch/LiveRec.

Evaluate sampled-active, full-active, standard temporal, and strict temporal regimes where applicable.

## 9.2 Frozen external validation

Summarize the external protocol in the main paper as:

> **DEV discovery and policy freeze → untouched one-shot TEST evaluation.**

Move complete chronology, hashes, execution guardrails, and recovery provenance to the Appendix/reproducibility materials.

## 9.3 Metrics and inference

Primary:

- NDCG@10.

Secondary:

- H@10 / HR@10 as appropriate.

Statistical reporting:

- paired user-level bootstrap;
- exact matched invocation budgets;
- across training seeds: mean ± SD and sign consistency.

Do not reinterpret within-seed bootstrap intervals as across-seed confidence intervals.

## 9.4 Mechanism evidence hierarchy

### Confirmatory evidence

- frozen DEV relationship-state sign structure;
- untouched TEST replication of the same three-state structure.

### Mechanism attribution

- Long-only / Short-only / Popularity-only by relationship state.

### DEV-only refinement

- context-distance consistency diagnostic;
- distance-bin recency analysis;
- ultra-recent 1–4 pocket.

Maintain this evidential hierarchy in the Results wording.

## 9.5 Robustness and validity

Report:

- Memory-parameter sensitivity;
- state/confidence feature-family ablation;
- independent deep Base training seeds;
- strong-base competitiveness;
- formal complexity and empirical efficiency.

## 9.6 Alternative-explanation analyses

Where feasible without altering frozen policies, stratify the long-horizon-only effect by plausible observable confounders:

- user history length;
- target creator popularity/exposure frequency;
- candidate-set size or active-room density;
- user repeat propensity.

The aim is not causal identification. The aim is to assess whether the observed relationship-state effect is trivially explained by one dominant observable factor.

Also report, where feasible:

\[
P(\Delta_m>0\mid \text{relationship state})
\]

alongside mean `Memory−Base`, so the mechanism is not supported only by group averages.

## 9.7 Optional high-value mechanism intervention

If an additional DEV-only strengthening experiment is undertaken, vary Base context length and test whether the positive specialist region shifts with the Base visibility boundary, e.g.:

\[
L\in\{8,16,32\}.
\]

This would strengthen the interpretation that complementarity tracks Base visibility capacity rather than a fixed numerical horizon.

Treat this as optional strengthening, not a prerequisite for the frozen test claim.

---

# 10. Results section structure

## 10.1 Finding 1 — Aggregate specialist value is regime-dependent

Establish the paradox first.

Headline KuaiLive evidence:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active: Memory−Base approximately `+0.03367`, native Selective−Base approximately `+0.05345`;
- strict temporal: Selective−Base approximately `+0.07282` / `+0.09743`.

Interpretation:

> **A single global Memory-vs-Base ordering is not an adequate scientific characterization. Aggregate specialist value is regime-dependent.**

Use the regime-level decomposition to motivate two explanatory axes:

1. how often each Base-relative evidence state occurs;
2. how much utility the specialist provides within each state.

Avoid claiming that either axis alone fully explains the regime reversal unless directly supported.

## 10.2 Finding 2 — Base-relative evidence state and recency structure specialist utility

Lead with the three-state frozen DEV → untouched TEST sign replication.

Then present component attribution.

After the confirmatory evidence, introduce the DEV-only context-distance and recency refinement.

Conservative section conclusion:

> **Across the evaluated LiveRec/Twitch setting, the dominant positive Memory regime occurs when target-specific relationship evidence remains recoverable from older history but is no longer represented in the Base’s visible sequence. Represented and unavailable states are negative in aggregate, while a separate ultra-recent positive pocket rules out a monotonic distance interpretation.**

## 10.3 Finding 3 — Specialist solvability is not Base difficulty

Compare Utility routing against exact-budget Difficulty routing.

Central conceptual result:

\[
\text{hard for Base}
\neq
\text{solvable by relationship specialist}.
\]

Use the evidence-state interpretation to explain the difference: unseen events can be difficult while containing no target-specific evidence recoverable by the specialist.

Report feature-family evidence showing that combined observable state + Base confidence is stronger than either family alone, while preserving the rule that relationship-state labels are analysis-only.

## 10.4 Finding 4 — Frozen second-platform transfer confirms useful conditional utility

Twitch/LiveRec untouched TEST:

- exact same budget `K=6,650`;
- invocation rate `15.04%`;
- Base NDCG@10 `0.58211`;
- Always Memory `0.53980`;
- Difficulty exact-K `0.58340`;
- Selective Utility `0.58983`;
- Selective−Base `+0.00772`, 95% CI `[+0.00641,+0.00903]`;
- Utility−Difficulty `+0.00644`, 95% CI `[+0.00528,+0.00762]`.

Secondary H@10:

- Base `0.75503`;
- Selective Utility `0.76448`;
- Difficulty exact-K `0.75252`;
- Selective−Base `+0.00945`;
- Utility−Difficulty `+0.01196`.

Also report:

- event-level predicted vs realized utility Spearman ≈ `0.173`;
- Oracle exact-K NDCG@10 `0.64806`;
- current router captures about `11.71%` of Oracle gain.

Interpretation:

> **Precise event-level utility calibration remains difficult, but coarse specialist-value ranking is already sufficient to identify a useful positive tail.**

Do not claim near-Oracle routing or accurate event-level utility prediction.

## 10.5 Finding 5 — Robustness and deployment evidence

Summarize:

- Memory sensitivity preserves the main relationship-state signs;
- independent Base training seeds preserve `Selective > Base` and `Utility > Difficulty`;
- strong-base comparator checks establish credible reference models without SOTA claims;
- formal complexity and empirical latency results characterize deployment trade-offs.

Keep these as support for the main scientific claims rather than headline contributions.

---

# 11. Figures and tables

## Figure 1 — Base-relative evidence valuation and selective specialist use

Depict:

1. strong finite-context Base;
2. separate persistent relationship-memory specialist;
3. three conceptual Base-relative evidence states: represented, recoverable-but-unrepresented, unavailable;
4. observable user/state + Base-confidence features feeding the utility estimator;
5. specialist-minus-base utility decision;
6. optional cost threshold.

Clearly mark the three evidence-state labels as **analysis concepts**, not online routing features.

## Table 1 — Regime-level performance and strong-Base context

Include compact KuaiLive regime results and credible comparator positioning.

## Figure 2 — Relationship-evidence mechanism

Panel A:

- recent-visible / represented;
- long-horizon-only / recoverable-but-unrepresented;
- unseen / unavailable;
- DEV and untouched TEST Memory−Base values.

Panel B:

- distance bins `1–4`, `5–8`, `9–16`, `17–32`, `33–64`, `65+`, unseen;
- mark the 16-step Base visibility boundary as a consistency reference;
- annotate the ultra-recent repeat pocket and outside-context positive region.

## Table 2 — Utility versus Difficulty under exact matched budgets

Report both NDCG@10 and H@10 where appropriate.

## Table 3 — Mechanism attribution and robustness

Include:

- Long-only / Short-only / Popularity-only;
- feature-family ablation;
- Memory sensitivity sign consistency;
- Base training-seed summary.

## Figure 3 — Selection composition and specialist solvability

Compare which relationship states are selected by Utility and Difficulty at the same budget.

The purpose is explanatory rather than to expose relationship-state labels as online features.

## Figure/Table 4 — Accuracy–invocation–latency/footprint frontier

Treat this as deployment evidence rather than a separate methodological contribution.

---

# 12. Related Work structure

## 12.1 Sequential, repeat-aware, and long-term recommendation

Discuss methods that model short-term intent, long-term preference, repeated behavior, and finite sequential context.

Novelty boundary:

> The paper does not claim novelty for jointly modeling long- and short-term preference. It studies the **marginal value of a separate persistent relationship-evidence source relative to a strong Base representation**.

## 12.2 Knowledge-aware, multimodal, and auxiliary-information recommendation

Discuss work on heterogeneous knowledge, multimodal content, denoising, reliability, complementarity, and adaptive fusion.

Novelty boundary:

> Existing fusion work primarily asks how heterogeneous evidence should be integrated. This paper first asks whether a particular evidence source is **incremental relative to the Base** and therefore worth using at all.

This subsection should establish the distinction between:

- representation-level fusion/complementarity;
- **Base-relative evidence valuation**.

## 12.3 Learning-to-Defer, expert routing, and selective prediction

Acknowledge that generic expert assignment and accuracy–cost trade-offs are established problems.

State explicitly:

> The paper does not propose a new general deferral theory. Its contribution is to characterize and exploit the structured conditional utility of a transparent relationship-evidence specialist in recommendation.

## 12.4 Negative transfer and harmful auxiliary evidence

Use negative transfer as a conceptual connection:

> Auxiliary evidence can be redundant or harmful when it lacks incremental information relative to the Base.

Do not claim a causal negative-transfer mechanism unless directly identified.

## 12.5 Live-stream recommendation

Position the domain as a setting in which persistent user–creator relationships, active-room candidate dynamics, repeated viewing, and temporal availability make conditional relationship evidence scientifically meaningful.

Do not claim that live-stream recommendation itself is the methodological novelty.

---

# 13. Discussion structure

## 13.1 Auxiliary evidence value is Base-relative

Emphasize:

> **An evidence source should not be evaluated solely by standalone predictive strength; its scientific and operational value depends on what the Base already represents.**

A simple specialist can have high marginal value when it contains missing evidence, while a powerful auxiliary model can be redundant when its information is already represented.

## 13.2 Represented, recoverable, and unavailable evidence

Interpret the three relationship states as a practical taxonomy of specialist solvability.

Avoid presenting the taxonomy as a universal law; it is an empirical conceptualization supported in the evaluated live-stream settings.

## 13.3 Why Difficulty is insufficient

Explain that Base weakness says nothing about whether the relationship specialist has recoverable target-specific evidence.

Connect this directly to the Utility-over-Difficulty matched-budget result.

## 13.4 Regime dependence and state composition

Use the regime-level decomposition to explain why global Memory ordering can reverse across candidate and temporal settings.

Avoid asserting a complete causal explanation unless state-prevalence and state-specific changes are explicitly quantified.

## 13.5 Transparency versus model complexity

Justify the simple relationship specialist as a methodological choice that separates evidence availability from representation-learning complexity.

## 13.6 Remaining utility-estimation headroom

Use modest Spearman correlation and limited Oracle-gain capture to motivate future work on better utility estimation rather than claiming solved routing.

## 13.7 External validity

Limit claims to the evaluated live-stream settings, strong finite-context Bases, and explicit relationship evidence.

Do not imply universal sequential-recommendation generalization.

---

# 14. Claim boundaries

## Supported claims

- relationship Memory is regime-dependent rather than globally ordered against Base;
- the dominant positive Twitch/LiveRec regime is recoverable-but-unrepresented relationship evidence;
- represented and unavailable relationship states are negative in aggregate in the evaluated setting;
- recency introduces a non-monotonic qualification;
- specialist-relative Utility and generic Base Difficulty are decisionally distinct;
- Utility routing improves a strong Base under matched budgets in the evaluated settings;
- the frozen second-platform untouched test supports transfer of the conditional-specialist principle;
- current utility estimation leaves substantial Oracle headroom.

## Unsupported or overbroad claims

Do not claim:

- a universal theory of auxiliary evidence valuation;
- a universal 16-step threshold;
- monotonic improvement with relationship distance;
- globally superior Long-only Memory;
- novel generic gating, MoE, L2D, or selective prediction;
- that generic Difficulty represents all prior routing methods;
- that relationship-state labels are online features;
- external knowledge beyond the interaction dataset;
- causal explanation of conversion, satisfaction, or GMV;
- calibrated event-level utility prediction;
- near-Oracle specialist selection;
- SOTA or leaderboard superiority;
- generalization beyond evaluated live-stream settings.

---

# 15. Abstract guidance

Recommended logical order:

1. **Problem:** Additional historical evidence is not automatically useful because its value depends on what the Base already represents.
2. **Formulation:** Define relationship Memory as a specialist and evaluate its specialist-minus-base utility.
3. **Mechanism:** Show that utility is structured by Base-relative relationship-evidence state and recency.
4. **Decision:** Predict specialist-relative utility rather than generic Base difficulty.
5. **Evidence:** Report multi-regime KuaiLive results and frozen untouched Twitch/LiveRec validation.
6. **Qualification:** Note that utility prediction remains imperfect and substantial Oracle headroom remains.

Avoid introducing the paper as a new gating architecture.

---

# 16. Introduction guidance

Recommended argument sequence:

1. Strong sequential recommenders compress or truncate user history into finite representations.
2. Auxiliary evidence sources can recover information outside that representation, but more evidence is not automatically useful.
3. Existing recommendation work has extensively studied how to fuse long/short-term, multimodal, collaborative, or knowledge signals; the under-addressed question is whether an auxiliary source is **incremental relative to the Base** for a particular decision event.
4. Relationship Memory provides a transparent testbed for this question because target-specific relationship evidence may be represented, recoverable only from older history, or unavailable.
5. This motivates specialist-minus-base utility rather than standalone Memory quality or Base difficulty.
6. Present the three contributions.

A strong central sentence is:

> **The central problem is not whether more historical evidence improves recommendation, but whether that evidence is incremental relative to the information already represented by the Base.**

A second sentence can connect mechanism to decision:

> **This Base-relative evidence state determines specialist solvability, while selective routing asks whether that latent value can be inferred from deployment-observable signals.**

---

# 17. Preferred manuscript narrative

Use the following order throughout the paper:

> **regime paradox → Base-relative evidence valuation → evidence-state mechanism → specialist solvability versus Base difficulty → selective decision → frozen transfer → robustness and deployment limitations**

The conceptual chain should remain visible across Introduction, Method, Results, and Discussion:

\[
\boxed{
\text{Recommendation regime}
\rightarrow
\text{Base-relative evidence state}
\rightarrow
\text{specialist solvability / incremental utility}
\rightarrow
\text{specialist decision}
}
\]

This chain is the preferred organizing principle of the manuscript.