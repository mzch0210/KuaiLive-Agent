# KBS paper outline — evidence-updated academic guidance

> **INDEPENDENT / NON-AUTHORITATIVE OUTLINE**  
> This document is a manuscript-structure guide for paper development. It does not replace frozen experimental protocols or prior authoritative snapshots unless explicitly promoted by the authors.

**Generated:** 2026-09-23T22:47+08:00  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Project:** `mzch0210/KuaiLive-Agent`

---

# 1. Paper positioning

Position the manuscript as a study of **Base-relative evidence valuation and conditional specialist use in recommendation**, instantiated through explicit persistent user–creator relationship evidence.

## 1.1 General scientific question

> **When is an auxiliary evidence source genuinely incremental relative to what a strong Base already represents?**

Instantiate this question in live-stream recommendation:

> **When does persistent relationship evidence provide incremental ranking value beyond a strong finite-context sequential recommender, how does that value change with the recommendation regime and Base representation capacity, and can it be predicted well enough to govern selective specialist use?**

The manuscript should not be positioned as:

- a new generic gating, mixture-of-experts, selective-prediction, or Learning-to-Defer method;
- a new long/short-term recommendation architecture;
- an LLM-agent or agentic-recommendation system;
- a claim that relationship Memory is globally superior to a strong sequential Base;
- a generic external-knowledge integration or feature-fusion paper;
- a universal theory of relationship evidence states.

Use **relationship evidence**, **persistent relationship representation**, **Base-relative evidence state**, and **relationship-memory specialist** as the primary terminology. When using *knowledge*, clarify that the specialist is separate from the Base representation but is derived from the same underlying interaction history rather than an external dataset.

Preferred framing:

> **Relationship Memory is a regime-dependent specialist whose value is defined relative to what the Base already represents. Target-specific evidence can be represented in the Base, recoverable only from older history, or unavailable; however, these states structure rather than deterministically fix specialist utility. Recommendation regime and Base representation capacity jointly determine the marginal value of the specialist.**

---

# 2. Recommended title

## Primary

> **Learning When Relationship Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Conservative alternative

> **Conditional Specialist Utility of Relationship Memory in Live-Streaming Recommendation**

Retain **Live-Streaming Recommendation** in the title. The conceptual discussion may generalize to auxiliary evidence valuation, but empirical claims should remain within the evaluated live-stream settings.

---

# 3. Central thesis and novelty boundary

## 3.1 Central thesis

> **Explicit relationship Memory has no fixed global ordering relative to a strong sequential Base. Its marginal utility is Base-relative: it depends on the state of target-specific evidence relative to the Base representation, on recommendation regime, and on recency. Recoverable-but-unrepresented evidence forms the dominant positive specialist regime in Twitch/LiveRec, while intervention on Base context length shows that the same persistent evidence loses substantial marginal value once a larger Base context comes to represent it. At the same time, KuaiLive candidate-regime results show that evidence state alone does not determine utility: state-specific specialist value can change even when state composition is unchanged. This structured heterogeneity explains why Base difficulty is not equivalent to specialist solvability and motivates specialist-minus-base utility as the decision target.**

## 3.2 Evidence valuation before evidence integration

Distinguish two questions:

1. **Evidence integration:** how should multiple representations or information sources be fused?
2. **Evidence valuation:** does a particular auxiliary evidence source have positive marginal value relative to what the Base already represents in the current regime?

This paper addresses the second question first.

Core methodological distinction:

> **Before asking how to integrate additional evidence, ask whether that evidence is genuinely incremental relative to the Base representation and recommendation regime.**

Contrast Base-relative evidence valuation with representation-level feature fusion, multimodal fusion, long/short-term aggregation, and generic expert routing.

## 3.3 Defensible novelty

Present novelty as the combined scientific contribution of:

1. a transparent **Base-relative evidence valuation** formulation through specialist-minus-base ranking utility;
2. an interpretable **evidence-state framework** for represented, recoverable-but-unrepresented, and unavailable relationship evidence;
3. **interventional support** that specialist utility changes when Base visibility capacity changes while persistent relationship evidence is held fixed;
4. direct evidence that **Base difficulty and specialist solvability are decisionally distinct** under exact matched invocation budgets;
5. evidence that recommendation regime changes aggregate specialist value through changes in state-specific relative utility and, potentially in other regimes, state composition.

Do not claim novelty for gating, expert selection, long/short-term modeling, evidence fusion, external information integration, or complementarity in isolation.

---

# 4. Principal contributions

Use three main contributions in the Introduction.

## Contribution 1 — Base-relative evidence valuation and specialist decision

Define specialist-minus-base utility:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x),
\]

where `B` is the Base, `M` the relationship specialist, and `u_K` event-level ranking utility.

For observable routing information `z`, estimate:

\[
\eta(z)=\mathbb E[\Delta_m(X)\mid Z=z].
\]

The methodological emphasis is not the difference formula itself, but the evaluation target: an auxiliary evidence source is judged by its **marginal utility relative to the Base**, not by standalone accuracy and not by Base difficulty alone.

Use this quantity to motivate selective specialist invocation and compare it with a matched-budget generic Difficulty target. Explicitly relate the formulation to Learning-to-Defer and expert routing without claiming a new general deferral theory.

## Contribution 2 — Base-relative relationship-evidence states with visibility intervention

Characterize specialist utility through three empirical relationship states:

| Empirical state | Base-relative interpretation |
|---|---|
| recent-visible | **represented evidence** |
| long-horizon-only | **recoverable but unrepresented evidence** |
| unseen | **unavailable target-specific evidence** |

The principal mechanism claim should be:

> **Persistent relationship evidence is strongly complementary when it remains recoverable from older history but is not represented in the Base’s visible sequence; when the same evidence becomes represented by enlarging Base context, its marginal specialist value falls sharply.**

This mechanism is qualified by two observations:

- recency is non-monotonic, including an ultra-recent positive pocket;
- evidence state is not a universal utility sign rule, because state-specific utility also changes with recommendation regime.

Frame this contribution as an interpretable characterization of **Base-relative specialist solvability**, not as a generic claim that long-term preference is important.

## Contribution 3 — Multi-regime, decision-composition, and frozen external validation

Validate the conditional-specialist principle through:

- KuaiLive candidate and temporal regimes;
- regime-by-state decomposition;
- exact-budget Utility-versus-Difficulty selection composition;
- alternative-explanation stratification;
- strong-Base controls and independent Base training seeds;
- a second live-stream platform using a strong official LiveRec Base;
- a frozen DEV-to-untouched-TEST protocol;
- matched-budget Difficulty and Oracle controls;
- accuracy–invocation–latency/footprint analysis.

Treat strong-base competitiveness, parameter sensitivity, seed robustness, and efficiency as validity evidence rather than separate headline contributions.

---

# 5. Formal problem formulation

Let `x` denote a recommendation event, `B` a strong sequential Base, `M` an explicit relationship-memory specialist, and `u_K(A,x)` event-level ranking utility at cutoff `K`.

## 5.1 Specialist-minus-base utility

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

For observable information `z` and recommendation regime `r`:

\[
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The learned selector estimates `\hat\eta(z)` without using diagnostic relationship-state labels.

If specialist invocation incurs incremental cost `c(x)` with cost weight `\lambda`, the idealized decision is:

\[
\pi^*(z)=\mathbf 1\left[
\mathbb E[\Delta_m(X)\mid Z=z]
>
\lambda\,\mathbb E[c(X)\mid Z=z]
\right].
\]

Treat this as a task-specific decision formulation rather than a new theorem in deferral, selective prediction, or cost-sensitive routing.

## 5.2 Regime-level decomposition

Let `S` denote the Base-relative evidence state. Aggregate specialist utility in regime `r` is:

\[
\mathbb E[\Delta_m\mid R=r]
=
\sum_s P(S=s\mid R=r)\,\mathbb E[\Delta_m\mid S=s,R=r].
\]

This decomposition separates two possible sources of regime change:

1. **state-composition change:** `P(S=s|R=r)` changes;
2. **state-specific utility change:** `E[Δ_m|S=s,R=r]` changes.

The KuaiLive sampled-active versus full-active comparison provides a useful identified case: the same 10,222 events are evaluated under both candidate regimes, so evidence-state prevalence is identical, yet aggregate Memory−Base reverses from `−0.05125` to `+0.03367`. The reversal therefore cannot be attributed to state-prevalence change in this comparison and is associated with state-specific utility changes.

Report the state-specific shifts:

| Base-relative state | Sampled Δ | Full-active Δ | Full−Sampled shift | 95% CI |
|---|---:|---:|---:|---:|
| represented | +0.11508 | +0.19261 | +0.07752 | [+0.07046,+0.08472] |
| recoverable-but-unrepresented | +0.17779 | +0.08049 | −0.09731 | [−0.14897,−0.04647] |
| unavailable | −0.20060 | −0.10251 | +0.09809 | [+0.08988,+0.10649] |

Interpretation:

> **Evidence state structures specialist utility, but recommendation regime can change the magnitude—and potentially the sign—of utility within a state.**

Do not extrapolate the fixed-composition result to temporal regimes unless separately demonstrated.

## 5.3 Difficulty versus specialist solvability

Difficulty asks:

> Where is the Base weak?

Specialist-relative utility asks:

> Where can this particular specialist improve the Base?

These differ because a difficult event may contain no target-specific evidence recoverable by the specialist:

\[
\text{Base difficulty}\not\Rightarrow\text{specialist solvability}.
\]

The decision analysis should therefore examine not only final performance but also the composition of selected events.

---

# 6. Base-relative relationship-evidence states and mechanism

Let:

- `V_L(x)=1` if the target creator appears in the exact visible input sequence of a Base with context length `L`;
- `H(x)=1` if the target creator exists in canonical chronological pre-target history outside that visible sequence.

Define:

| Relationship state | `V_L(x)` | `H(x)` | Base-relative state |
|---|---:|---:|---|
| recent-visible | 1 | any | represented |
| long-horizon-only | 0 | 1 | recoverable but unrepresented |
| unseen | 0 | 0 | unavailable |

These labels are **diagnostic only** and must never be described as online selector features.

## 6.1 Confirmatory relationship-state evidence

Present the frozen DEV structure and untouched TEST replication together:

| Relationship state | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| recent-visible | −0.01995 | −0.01935 |
| **long-horizon-only** | **+0.23097** | **+0.22045** |
| unseen | −0.19562 | −0.18215 |

The supported interpretation is that specialist utility depends strongly on the relationship between persistent evidence and the Base representation. Do not interpret these Twitch signs as a universal cross-regime taxonomy.

## 6.2 Context-length intervention: changing Base visibility while holding Memory fixed

Use the DEV-only `L∈{8,16,32}` intervention as direct strengthening evidence for the Base-relative visibility interpretation.

Canonical Memory is held fixed across all three contexts (`NDCG@10 = 0.52170`), while Base context length changes:

| Base context | Base NDCG@10 | Memory−Base | 95% CI |
|---:|---:|---:|---:|
| 8 | 0.52619 | −0.00450 | [−0.00756,−0.00127] |
| 16 | 0.57185 | −0.05016 | [−0.05307,−0.04731] |
| 32 | 0.59663 | −0.07493 | [−0.07766,−0.07227] |

State-specific results preserve a positive recoverable-but-unrepresented region while its prevalence shrinks as Base context expands:

| Context | represented Δ | recoverable Δ | unavailable Δ |
|---:|---:|---:|---:|
| 8 | +0.00271 | +0.26042 | −0.18904 |
| 16 | −0.01995 | +0.23097 | −0.19562 |
| 32 | −0.02309 | +0.18861 | −0.19985 |

The strongest analysis is within-event transition evidence. When the same event moves from **recoverable-but-unrepresented** to **represented** solely because Base context expands, Memory remains unchanged while specialist-minus-base utility falls sharply:

| Transition | n | Δ before | Δ after | change | 95% CI |
|---|---:|---:|---:|---:|---:|
| L8→L16 recoverable→represented | 5,055 | +0.29388 | −0.15360 | **−0.44748** | [−0.45767,−0.43730] |
| L16→L32 recoverable→represented | 3,617 | +0.25755 | −0.17474 | **−0.43229** | [−0.44381,−0.42054] |
| L8→L32 recoverable→represented | 8,672 | +0.27782 | −0.14114 | **−0.41896** | [−0.42685,−0.41112] |

Interpretation:

> **The value of persistent relationship evidence is genuinely Base-relative: when a larger Base context comes to represent the same evidence, the marginal specialist advantage collapses.**

This is **interventional support**, not a universal causal theorem. Context length is not claimed to be the only determinant of specialist utility.

## 6.3 Mechanism attribution

On long-horizon-only DEV events:

- Long-only: `ΔNDCG@10 = +0.33688`;
- Short-only: negative;
- Popularity-only: negative.

Interpretation:

> **The positive recoverable-but-unrepresented effect is associated specifically with persistent long-term relationship evidence rather than generic popularity or short-term recurrence.**

Do not claim Long-only is globally superior.

## 6.4 Context-distance consistency diagnostic

Because the original LiveRec state definition already refers to the exact 16-step visible context, the distance result is a **consistency diagnostic**, not an independent mechanism validation:

- within 16 interactions: Memory−Base `−0.01980`;
- beyond 16 interactions: `+0.23057`.

Use this result to connect the coarse state partition to observed distance structure.

## 6.5 Recency refinement

Distance-bin evidence:

- 1–4: `+0.04606`;
- 5–8: `−0.06511`;
- 9–16: `−0.15268`;
- 17–32: `+0.25668`;
- 33–64: `+0.20707`;
- 65+: `+0.12965`;
- unseen: `−0.19562`.

Therefore:

\[
\text{specialist utility}
\approx
f(\text{Base-relative evidence state},\text{recommendation regime},\text{recency}),
\]

not a monotonic distance law.

## 6.6 Alternative-explanation robustness

Within long-horizon-only DEV events, the positive Memory−Base effect remains positive with 95% bootstrap intervals above zero across strata of:

- user history length: approximately `+0.217` to `+0.250`;
- target creator prior exposure: approximately `+0.154` to `+0.323`;
- candidate count: approximately `+0.212` to `+0.270`;
- repeat propensity: approximately `+0.187` to `+0.289`.

This does not establish causality. It supports the narrower conclusion that the positive recoverable-state effect is not trivially eliminated by any one of these observable factors.

---

# 7. Research questions

**RQ1 — Regime dependence.** How does aggregate relationship-Memory value change across candidate and temporal regimes, and do regime-level reversals arise from evidence-state composition, state-specific specialist utility, or both?

**RQ2 — Base-relative specialist solvability.** Under what visibility and recency conditions is target-specific relationship evidence represented, recoverable but unrepresented, or unavailable, and does changing Base visibility capacity alter the marginal utility of the same persistent evidence?

**RQ3 — Specialist decision.** Can specialist-minus-base utility be estimated from observable user/history state and Base-confidence information well enough to improve a strong Base, and does it identify specialist-solvable events more effectively than generic Base Difficulty at the same invocation budget?

Logical bridge:

> **RQ2 explains how Base-relative evidence state structures specialist solvability; RQ3 asks whether that latent value can be inferred from deployment-observable proxies.**

**RQ4 — Robustness and transfer.** Do the selective advantage and core conditional-specialist structure survive alternative explanations, independent Base realizations, and a frozen second-platform untouched evaluation?

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

The specialist is intentionally transparent so that evidence availability and marginal value can be separated from representation-learning complexity.

## 8.3 Relative-utility estimator

Estimate `\hat\eta(z)` from observable state and Base-confidence features. The HGB selector is operational rather than the source of novelty.

The selector does not observe diagnostic evidence-state labels.

## 8.4 Generic Difficulty control

Use the same observable information and a comparable model family to estimate Base difficulty. Evaluate Utility and Difficulty under **exact matched invocation budgets**.

## 8.5 Oracle and serving cost

Use the exact-budget Oracle as an analysis upper bound only. Report Base inference, selector overhead, specialist invocation, throughput, and memory/model/cache footprint where relevant.

---

# 9. Experimental design

## 9.1 Datasets and regimes

Use KuaiLive and Twitch/LiveRec, with sampled-active, full-active, standard temporal, and strict temporal regimes where applicable.

## 9.2 Frozen external validation

Main-paper summary:

> **DEV discovery and policy freeze → untouched one-shot TEST evaluation.**

Move full chronology, hashes, execution guardrails, and provenance to reproducibility materials.

## 9.3 Metrics and inference

Primary: NDCG@10.  
Secondary: H@10 / HR@10 as appropriate.

Use:

- paired user-level bootstrap;
- exact matched invocation budgets;
- mean ± SD and sign consistency across training seeds.

## 9.4 Evidence hierarchy

### Confirmatory

- frozen DEV relationship-state sign structure;
- untouched TEST replication.

### Interventional support

- DEV-only `L=8/16/32` context-length intervention with canonical Memory held fixed;
- within-event recoverable→represented transitions.

### Mechanism attribution

- Long-only / Short-only / Popularity-only.

### Decision explanation

- Utility/Difficulty/Oracle selection composition under the same budget.

### Robustness and refinement

- alternative-explanation stratification;
- Memory sensitivity;
- context-distance consistency;
- distance-bin recency analysis;
- independent Base training seeds;
- strong-base competitiveness;
- efficiency.

Maintain this hierarchy in the Results wording.

## 9.5 Regime decomposition

For candidate-regime comparisons where the same event set is preserved, report both:

\[
P(S=s\mid R)
\]

and

\[
E[\Delta_m\mid S=s,R].
\]

Use the sampled-active/full-active comparison to show that a global sign reversal can occur with **identical state prevalence**, implying a state-specific utility shift rather than a composition shift.

## 9.6 Selection composition at exact matched budgets

On Twitch frozen DEV, report population prevalence and selected shares.

Population:

- represented `52.35%`;
- recoverable-but-unrepresented `12.54%`;
- unavailable `35.11%`.

Utility selection:

- represented `29.70%` (`0.57×` enrichment);
- recoverable `34.13%` (**`2.72×`**);
- unavailable `36.17%` (`1.03×`).

Difficulty selection:

- represented `11.98%` (`0.23×`);
- recoverable `20.89%` (**`1.67×`**);
- unavailable `67.13%` (**`1.91×`**).

Oracle selection:

- represented `50.39%`;
- recoverable `43.00%` (**`3.43×`**);
- unavailable `6.61%`.

Interpretation:

> **Utility is better aligned with specialist-solvable evidence states, while generic Difficulty disproportionately concentrates on unavailable events.**

Relationship-state labels remain analysis-only and were not selector inputs.

## 9.7 Positive-fraction and alternative-explanation reporting

For Twitch DEV, also report:

- represented: `P(Δ>0)=0.1742`;
- recoverable: `P(Δ>0)=0.6438`;
- unavailable: `P(Δ>0)=0.0374`.

This complements group means and reduces the risk that the mechanism is interpreted as an artifact of a few extreme events.

---

# 10. Results section structure

## 10.1 Finding 1 — Aggregate specialist value is regime-dependent, and candidate-regime reversal is driven by state-specific utility change

Establish the aggregate paradox first:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active: Memory−Base approximately `+0.03367`, native Selective−Base approximately `+0.05345`;
- strict temporal: Selective−Base approximately `+0.07282` / `+0.09743`.

Then use the sampled/full decomposition:

- same 10,222 events;
- identical evidence-state prevalence;
- aggregate Memory−Base reverses from `−0.05125` to `+0.03367`;
- all three state-specific utility shifts are non-zero with bootstrap intervals excluding zero.

Section conclusion:

> **Regime dependence is not reducible to changing proportions of evidence states. Candidate regime can change the value of the specialist within the same evidence state.**

Do not claim the same decomposition mechanism for temporal regimes without direct analysis.

## 10.2 Finding 2 — Base-relative evidence state structures specialist utility, and visibility intervention changes marginal value

Lead with the frozen DEV → untouched TEST three-state replication.

Then present the context-length intervention as the strongest mechanism strengthening result:

- canonical Memory is fixed;
- Base context expands from 8 to 16 to 32;
- recoverable events become represented;
- on those same events specialist-minus-base utility falls by approximately `0.42–0.45` NDCG@10.

Then present component attribution, alternative-explanation stratification, and recency refinement.

Conservative conclusion:

> **Persistent relationship evidence is most valuable when it is available to the specialist but not represented by the current Base; when the Base comes to represent the same evidence, specialist marginal utility declines sharply. Evidence state structures but does not uniquely determine utility because recommendation regime and recency also matter.**

## 10.3 Finding 3 — Specialist solvability is not Base difficulty

Start with the exact-budget performance difference, then explain it using selection composition.

Central result:

\[
\text{hard for Base}\neq\text{solvable by relationship specialist}.
\]

Key explanatory evidence:

- Utility enriches recoverable events `2.72×` versus `1.67×` for Difficulty;
- Difficulty enriches unavailable events `1.91×`, whereas Utility is near population prevalence (`1.03×`);
- Oracle strongly enriches recoverable events (`3.43×`) while suppressing unavailable events.

This result should be used to explain **why** Utility can outperform Difficulty rather than merely restating the performance difference.

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

> **Precise event-level utility calibration remains difficult, but coarse specialist-value ranking is sufficient to identify a useful positive tail.**

## 10.5 Finding 5 — Robustness and deployment evidence

Summarize:

- long-horizon positive utility persists across observable-factor strata;
- Memory sensitivity preserves the main Twitch relationship-state signs;
- independent Base training seeds preserve `Selective > Base` and `Utility > Difficulty`;
- strong-base comparator checks establish credible reference models without SOTA claims;
- formal complexity and empirical latency characterize deployment trade-offs.

---

# 11. Figures and tables

## Figure 1 — Base-relative evidence valuation and selective specialist use

Depict:

1. strong finite-context Base;
2. separate persistent relationship-memory specialist;
3. conceptual Base-relative states: represented, recoverable-but-unrepresented, unavailable;
4. observable user/state + Base-confidence features feeding the utility estimator;
5. specialist-minus-base utility decision;
6. optional cost threshold.

Mark evidence-state labels as analysis concepts, not routing features.

## Table 1 — Regime-level performance and regime decomposition

Include compact KuaiLive regime results and the sampled-active/full-active state-specific utility decomposition.

The table should make visually clear that candidate-regime reversal occurs with unchanged state prevalence.

## Figure 2 — Base-relative relationship-evidence mechanism

Use two main panels.

### Panel A — Confirmatory evidence-state structure

Show DEV and untouched TEST Memory−Base for represented / recoverable / unavailable states.

### Panel B — Context-length visibility intervention

Show `L=8/16/32` and highlight within-event recoverable→represented transitions. Emphasize that canonical Memory is fixed and that the decline in specialist-minus-base utility is produced by stronger Base representation.

Move fine distance bins to a supplementary figure or secondary panel unless space permits. The intervention now deserves priority over the earlier distance-only diagnostic.

## Table 2 — Utility versus Difficulty under exact matched budgets

Report performance and selection composition together or as adjacent panels:

- matched-budget NDCG/H@10;
- represented / recoverable / unavailable selection shares;
- enrichment relative to population;
- Oracle composition as an analysis upper bound.

## Table 3 — Mechanism attribution and robustness

Include:

- Long-only / Short-only / Popularity-only;
- alternative-explanation strata;
- positive-delta fractions;
- feature-family ablation;
- Memory sensitivity sign consistency;
- Base training-seed summary.

## Figure/Table 4 — Accuracy–invocation–latency/footprint frontier

Treat this as deployment evidence rather than a separate methodological contribution.

---

# 12. Related Work structure

## 12.1 Sequential, repeat-aware, and long-term recommendation

Discuss short-term intent, long-term preference, repeated behavior, and finite sequential context.

Novelty boundary:

> The paper does not claim novelty for jointly modeling long- and short-term preference. It studies the **marginal value of a separate persistent relationship-evidence source relative to a strong Base representation**.

## 12.2 Knowledge-aware, multimodal, and auxiliary-information recommendation

Discuss heterogeneous knowledge, multimodal content, denoising, reliability, complementarity, and adaptive fusion.

Novelty boundary:

> Existing fusion work primarily asks how heterogeneous evidence should be integrated. This paper first asks whether a particular evidence source is **incremental relative to the Base** and therefore worth using at all.

## 12.3 Learning-to-Defer, expert routing, and selective prediction

Acknowledge generic expert assignment and accuracy–cost trade-offs as established problems.

State explicitly:

> The paper does not propose a new general deferral theory. Its contribution is to characterize and exploit the structured conditional utility of a transparent relationship-evidence specialist in recommendation.

## 12.4 Negative transfer and harmful auxiliary evidence

Use negative transfer as a conceptual connection only. Auxiliary evidence can be redundant or harmful when it lacks incremental information relative to the Base.

## 12.5 Live-stream recommendation

Position the domain as a setting in which persistent user–creator relationships, active-room candidate dynamics, repeated viewing, and temporal availability make Base-relative evidence valuation scientifically meaningful.

---

# 13. Discussion structure

## 13.1 Auxiliary evidence value is Base-relative

Emphasize:

> **An evidence source should not be evaluated solely by standalone predictive strength; its operational value depends on what the Base already represents.**

The context-length intervention provides direct support: holding Memory fixed while expanding Base context sharply reduces specialist marginal utility on events whose evidence becomes represented.

## 13.2 Evidence state structures but does not fix utility

Use the three-state taxonomy as a practical description of specialist solvability, but explicitly note the KuaiLive result:

> represented evidence is negative in Twitch/LiveRec aggregate analysis but positive in KuaiLive candidate regimes.

Therefore the correct abstraction is not `state → fixed sign`, but:

\[
\text{specialist utility}
=
f(\text{evidence state},\text{recommendation regime},\text{recency},\text{Base}).
\]

## 13.3 Why Difficulty is insufficient

Connect the matched-budget selection composition to the performance result. Difficulty identifies many hard-but-unavailable events; Utility better enriches events for which persistent relationship evidence is recoverable.

## 13.4 Regime dependence is not only state composition

Use the KuaiLive candidate comparison to show that global ordering can reverse even when evidence-state prevalence is unchanged. This strengthens the regime argument and prevents an overly simple prevalence-only explanation.

## 13.5 Transparency versus model complexity

Justify the simple specialist as a methodological choice that makes evidence availability and marginal value inspectable.

## 13.6 Remaining utility-estimation headroom

Use modest Spearman correlation and limited Oracle-gain capture to motivate better utility estimation rather than claiming solved routing.

## 13.7 External validity

Limit claims to evaluated live-stream settings, strong finite-context Bases, and explicit persistent relationship evidence.

---

# 14. Claim boundaries

## Supported claims

- relationship Memory is regime-dependent rather than globally ordered against Base;
- in Twitch/LiveRec, recoverable-but-unrepresented evidence is the dominant positive relationship-memory regime;
- the frozen DEV three-state structure reproduces on untouched TEST;
- DEV-only context-length intervention supports a **Base-relative visibility mechanism**: when the same persistent evidence becomes represented by a larger Base context, specialist-minus-base utility drops sharply;
- KuaiLive candidate-regime reversal occurs despite identical evidence-state prevalence and is associated with state-specific utility shifts;
- long-horizon positive utility is not trivially eliminated by stratification on history length, target exposure, candidate count, or repeat propensity;
- Utility and Difficulty select materially different evidence-state compositions at the same budget;
- Utility more strongly enriches recoverable events, whereas Difficulty disproportionately selects unavailable events;
- Utility routing improves a strong Base under matched budgets in the evaluated settings;
- the frozen second-platform untouched test supports transfer of the conditional-specialist principle;
- current utility estimation leaves substantial Oracle headroom.

## Unsupported or overbroad claims

Do not claim:

- a universal theory of auxiliary evidence valuation;
- that represented evidence is always redundant or negative;
- that recoverable evidence is always positive in every recommendation regime;
- that evidence-state prevalence alone explains regime reversal;
- that context length is the only determinant of specialist utility;
- a universal 16-step threshold;
- a causal theorem from the context-length intervention;
- monotonic improvement with relationship distance;
- globally superior Long-only Memory;
- novel generic gating, MoE, L2D, or selective prediction;
- that generic Difficulty represents all prior routing methods;
- that relationship-state labels are online features;
- external knowledge beyond the interaction dataset;
- causal conversion, satisfaction, or GMV effects;
- calibrated event-level utility prediction;
- near-Oracle specialist selection;
- SOTA or leaderboard superiority;
- generalization beyond evaluated live-stream settings.

---

# 15. Abstract guidance

Recommended logical order:

1. **Problem:** More historical evidence is not automatically useful because value depends on what the Base already represents and on the recommendation regime.
2. **Formulation:** Define relationship Memory as a specialist and evaluate specialist-minus-base utility.
3. **Mechanism:** Show frozen relationship-state heterogeneity and context-length intervention evidence that marginal specialist value falls when the same evidence becomes represented by the Base.
4. **Decision:** Show that Utility and Difficulty select different event compositions; Utility better targets recoverable evidence.
5. **Evidence:** Report multi-regime KuaiLive results and frozen untouched Twitch/LiveRec validation.
6. **Qualification:** Note that evidence state does not determine utility alone and that substantial Oracle headroom remains.

If space permits, prioritize the context-length transition result over the fine recency-bin result in the Abstract because it provides stronger support for the Base-relative mechanism.

---

# 16. Introduction guidance

Recommended argument sequence:

1. Strong sequential recommenders compress or truncate user history into finite representations.
2. Auxiliary evidence can recover information outside that representation, but more evidence is not automatically useful.
3. Existing recommendation work has extensively studied how to fuse long/short-term, multimodal, collaborative, or knowledge signals; the under-addressed question is whether an auxiliary source is **incremental relative to the Base** for a particular event and regime.
4. Relationship Memory provides a transparent testbed because target-specific evidence may be represented, recoverable only from older history, or unavailable.
5. The same evidence can change from recoverable to represented when Base visibility capacity changes, making Base-relative evidence valuation empirically testable.
6. Base difficulty is insufficient because hard events may contain no specialist-recoverable evidence.
7. Present the three contributions.

Central sentence:

> **The central problem is not whether more historical evidence improves recommendation, but whether that evidence is incremental relative to the information already represented by the Base.**

Mechanism-to-decision sentence:

> **Base-relative evidence state structures specialist solvability, while selective decision making asks whether that latent marginal value can be inferred from deployment-observable signals.**

Regime qualification sentence:

> **Evidence state is not a fixed utility label: the value of the same type of relationship evidence can change with candidate regime and Base representation capacity.**

---

# 17. Preferred manuscript narrative

Use the following order throughout the paper:

> **regime paradox → Base-relative evidence valuation → evidence-state structure → visibility intervention → specialist solvability versus Base difficulty → selective decision → frozen transfer → robustness and deployment limitations**

The organizing chain should be:

\[
\boxed{
\text{Recommendation regime / Base representation}
\rightarrow
\text{Base-relative evidence state}
\rightarrow
\text{specialist solvability / incremental utility}
\rightarrow
\text{specialist decision}
}
\]

The new evidence requires one additional qualification throughout the manuscript:

> **Base-relative evidence state is an explanatory coordinate, not a deterministic utility class. Specialist utility is jointly conditioned by state, recommendation regime, recency, and Base representation capacity.**
