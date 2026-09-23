# KBS paper outline — revised academic guidance

> **INDEPENDENT / NON-AUTHORITATIVE OUTLINE**  
> This document is a manuscript-structure guide. It does not replace frozen experimental protocols or prior authoritative snapshots unless explicitly promoted by the authors.

**Generated:** 2026-09-23T13:56+08:00  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Project:** `mzch0210/KuaiLive-Agent`

---

# 1. Paper positioning

Position the manuscript as a study of **conditional specialist value in recommendation**, using explicit persistent user–creator relationship evidence as the specialist information source.

The central scientific question is:

> **When does explicit persistent relationship evidence provide incremental ranking value beyond a strong finite-context sequential recommender, and how should that conditional value govern specialist invocation?**

The paper should not be positioned as:

- a new generic gating, mixture-of-experts, selective-prediction, or Learning-to-Defer method;
- a new long/short-term recommendation architecture;
- an LLM-agent or agentic-recommendation system;
- a claim that relationship Memory is globally superior to a strong sequential Base;
- a live-stream application paper whose novelty rests mainly on the domain;
- a generic external-knowledge integration paper.

Use **relationship evidence**, **persistent relationship representation**, or **relationship-memory specialist** as the primary terminology. When using the word *knowledge*, clarify that the specialist is separate from the Base representation but uses the same underlying interaction data rather than an external dataset.

Preferred framing:

> **Relationship Memory is a regime-dependent specialist. Its incremental value depends on whether target-specific historical evidence is already represented in the Base’s visible sequence, remains available only in older history, or has not been observed. Recency introduces an additional non-monotonic structure. Specialist-relative utility can exploit this heterogeneity more effectively than routing merely on Base difficulty.**

---

# 2. Recommended title

## Primary

> **Learning When Relationship Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Conservative alternative

> **Conditional Specialist Utility of Relationship Memory in Live-Streaming Recommendation**

Retain **Live-Streaming Recommendation** in the title unless additional conventional sequential-recommendation domains are evaluated. Avoid broadening the title to generic sequential recommendation beyond the current evidence base.

---

# 3. Central thesis and novelty boundary

## 3.1 Central thesis

> **Explicit relationship Memory has no fixed global ordering relative to a strong sequential Base. Its marginal ranking utility varies across recommendation regimes and according to the availability of target-specific historical evidence relative to the Base’s finite visible context. Historically known but currently outside-context relationships form the dominant positive Memory regime; visible and unseen relationships are negative in aggregate, while an ultra-recent positive pocket prevents a monotonic-distance interpretation. This structured heterogeneity motivates specialist-minus-base utility as a decision target rather than generic Base difficulty.**

## 3.2 Defensible novelty

The contribution should be presented as a **combined scientific contribution**, not as novelty in any single standard component.

The strongest novelty boundary is:

1. characterize the **conditional incremental utility** of an explicit relationship specialist relative to a strong Base;
2. identify an interpretable **relationship-visibility × recency structure** associated with specialist benefit and harm;
3. show that **specialist-relative utility and generic Base difficulty are decisionally distinct** under matched invocation budgets;
4. validate these findings under regime changes, independent Base realizations, and a frozen second-platform untouched test.

Do not claim novelty for gating, expert selection, long/short-term modeling, external information integration, or complementarity in isolation.

---

# 4. Principal contributions

Use three main contributions in the Introduction to avoid contribution inflation.

## Contribution 1 — Conditional specialist decision formulation

Formulate relationship Memory as a specialist evaluated by its incremental ranking utility relative to a strong Base:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x),
\]

where `B` is the Base, `M` the relationship specialist, and `u_K` event-level ranking utility.

For observable routing information `z`, estimate:

\[
\eta(z)=\mathbb E[\Delta_m(X)\mid Z=z].
\]

Use this quantity to motivate selective specialist invocation and compare it directly with a matched-budget generic Difficulty target.

This contribution is an application-specific specialist-relative formulation. It should be explicitly related to Learning-to-Defer and expert routing rather than presented as a new general deferral theory.

## Contribution 2 — Relationship-visibility × recency mechanism

Characterize how specialist utility changes across diagnostic relationship states:

- **recent-visible:** target relationship already represented in the Base’s visible sequence;
- **long-horizon-only:** target absent from the visible Base sequence but present in older pre-target history;
- **unseen:** target absent from both the visible sequence and older pre-target history.

The principal mechanism claim is:

> **Persistent relationship evidence is most complementary when it remains available from older history but is no longer represented in the Base’s visible sequence.**

Qualify this with the observed ultra-recent positive pocket, which shows that specialist utility is structured by both visibility and recency rather than increasing monotonically with distance.

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

Define:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

For observable information `z` and regime `r`:

\[
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The learned selector estimates `\hat\eta(z)` without using analysis-only relationship labels.

If specialist invocation incurs incremental serving cost `c(x)` with cost weight `\lambda`, the idealized decision is:

\[
\pi^*(z)=\mathbf 1\left[
\mathbb E[\Delta_m(X)\mid Z=z]
>
\lambda\,\mathbb E[c(X)\mid Z=z]
\right].
\]

For approximately fixed or negligible incremental cost, the rule reduces to selecting positive expected specialist utility.

Treat this equation as a task-specific decision formulation. Do not claim a new theorem in deferral, selective prediction, or cost-sensitive expert routing.

---

# 6. Relationship states and mechanism

Let:

- `V(x)=1` if the target creator appears in the exact visible input sequence used by the Base;
- `H(x)=1` if the target creator appears in chronological pre-target history outside that visible sequence.

Define three analysis states:

| Relationship state | `V(x)` | `H(x)` | Interpretation |
|---|---:|---:|---|
| recent-visible | 1 | any | target-specific evidence already represented in the Base input |
| long-horizon-only | 0 | 1 | target-specific evidence exists only in older history |
| unseen | 0 | 0 | no prior target-specific relationship evidence is available |

These labels are **diagnostic only** and must never be described as online selector features.

## 6.1 Confirmatory relationship-state evidence

Present the frozen DEV structure and untouched TEST replication together:

| Relationship state | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| recent-visible | −0.01995 | −0.01935 |
| **long-horizon-only** | **+0.23097** | **+0.22045** |
| unseen | −0.19562 | −0.18215 |

The main interpretation is not that a particular numerical horizon is universally optimal, but that **specialist benefit depends on whether relevant relationship evidence is already represented, only historically available, or absent**.

## 6.2 Mechanism attribution

Use component evidence to identify the information source associated with the positive long-horizon regime.

On long-horizon-only DEV events:

- Long-only: `ΔNDCG@10 = +0.33688`;
- Short-only: negative;
- Popularity-only: negative.

Interpretation:

> **The positive outside-visible-sequence effect is associated specifically with persistent long-term relationship evidence rather than generic popularity or short-term recurrence.**

Do not claim Long-only is globally superior.

## 6.3 Context-distance consistency diagnostic

The LiveRec Base uses an exact 16-step visible sequence, and the relationship-state definition already refers to that visible context. Therefore the 16-step distance result should be treated as a **consistency diagnostic and refinement**, not as an independent validation of the relationship-state definition.

Report that:

- last seen within 16 interactions: Memory−Base `−0.01980`;
- last seen beyond 16 interactions: Memory−Base `+0.23057`.

Use this analysis to show that the coarse diagnostic states align with actual distance structure, not to claim discovery of a universal 16-step threshold.

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
f(\text{relationship visibility},\ \text{recency regime}),
\]

not a monotonic distance law.

The 1–4 positive pocket should be treated as DEV-only mechanism refinement unless independently confirmed under a frozen protocol.

---

# 7. Research questions

**RQ1 — Regime dependence.** How does the aggregate value of explicit relationship Memory change across candidate and temporal recommendation regimes?

**RQ2 — Relationship-state mechanism.** Under what visibility and recency conditions does persistent relationship evidence become complementary, redundant, or unavailable relative to a strong finite-context Base, and which specialist component is associated with the positive outside-context effect?

**RQ3 — Specialist decision.** Can specialist-minus-base utility be estimated from observable user/history state and Base-confidence information well enough to improve a strong Base, and does this target contain decision-relevant information beyond generic Base Difficulty?

**RQ4 — Robustness and transfer.** Do the selective advantage and relationship-state sign structure survive independent Base realizations and reproduce on a second live-stream platform under a frozen untouched evaluation protocol?

**RQ5 — Deployment.** What accuracy–invocation–latency/footprint trade-off follows from specialist use, how informative is the utility estimator, and how much same-budget Oracle headroom remains?

---

# 8. Method section structure

## 8.1 Strong sequential Bases

Describe:

- KuaiLive identity-aware Dual-ID Base;
- frozen official LiveRec availability-aware and repeat-aware Base.

Use same-protocol comparator evidence only to establish that these are credible scientific reference models. Avoid SOTA or leaderboard claims.

## 8.2 Explicit relationship-memory specialist

Use the frozen transferred score:

\[
0.45\,Short + 0.45\,Long + 0.10\,Popularity.
\]

Explain each component transparently.

The specialist is intentionally simple and interpretable so that the availability and marginal value of persistent relationship evidence can be diagnosed separately from Base representation-learning complexity.

Do not present the weighted formula as the algorithmic novelty.

## 8.3 Relative-utility estimator

Estimate `\hat\eta(z)` from observable state and Base-confidence features.

The scientific selector is HGB in the frozen result. Its role is operational, not the source of novelty.

## 8.4 Generic Difficulty control

Use the same observable information and a comparable model family to estimate Base difficulty.

Evaluate Utility and Difficulty under **exact matched invocation budgets**.

The conceptual distinction is:

> **Difficulty asks where the Base is weak; Utility asks where this particular specialist improves the Base.**

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

If an additional DEV-only strengthening experiment is undertaken, the highest-value intervention is to vary Base context length and test whether the location of positive specialist complementarity shifts with the Base visibility boundary.

For example:

\[
L\in\{8,16,32\}.
\]

This would provide stronger evidence that complementarity tracks Base visibility capacity rather than a fixed numerical horizon.

Treat this as optional strengthening, not a prerequisite for the main frozen test claim.

---

# 10. Results section structure

## 10.1 Finding 1 — Global Memory ordering is regime-dependent

Establish the paradox first.

Headline KuaiLive evidence:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active: Memory−Base approximately `+0.03367`, native Selective−Base approximately `+0.05345`;
- strict temporal: Selective−Base approximately `+0.07282` / `+0.09743`.

Interpretation:

> **Aggregate Memory value is regime-dependent; a single global Memory-vs-Base ordering is not an adequate scientific characterization.**

Use this finding to motivate conditional specialist analysis.

## 10.2 Finding 2 — Relationship visibility and recency structure specialist utility

Lead with the three-state frozen DEV → untouched TEST sign replication.

Then present component attribution.

After the confirmatory evidence, introduce the DEV-only context-distance and recency refinement.

Conservative section conclusion:

> **Across the evaluated LiveRec/Twitch setting, the dominant positive Memory regime occurs when a previously observed relationship is absent from the Base’s visible sequence but remains available in older history. Recent-visible and unseen relationships are negative in aggregate, while a separate ultra-recent positive pocket rules out a monotonic-distance explanation.**

## 10.3 Finding 3 — Specialist-relative Utility is more decision-relevant than generic Difficulty

Lead with the distinction:

- difficult does not imply specialist-solvable;
- unseen events can be difficult while providing no target-specific historical evidence for the relationship specialist.

Report:

- KuaiLive Utility−Difficulty under matched budgets;
- state/confidence feature-family evidence;
- training-seed sign consistency;
- relationship-state composition of Utility versus Difficulty selections.

Central statement:

> **Base weakness is not sufficient evidence that a relationship specialist possesses complementary information.**

## 10.4 Finding 4 — Frozen transfer confirms the principle while substantial headroom remains

Untouched Twitch TEST:

- exact budget `K=6,650`;
- Base NDCG@10 `0.58211`;
- Difficulty exact-K `0.58340`;
- Selective Utility `0.58983`;
- Selective−Base `+0.00772`, 95% CI `[+0.00641,+0.00903]`;
- Utility−Difficulty `+0.00644`, 95% CI `[+0.00528,+0.00762]`;
- event-level utility/realized Spearman approximately `0.173`;
- same-budget Oracle gain captured approximately `11.7%`.

Interpretation:

> **Useful specialist escalation requires sufficiently informative utility ranking rather than precise pointwise utility prediction. The large Oracle gap shows that utility estimation remains far from solved.**

Do not hide the modest correlation or Oracle gap.

---

# 11. Figures and tables

## Figure 1 — Conditional relationship-specialist framework

Show:

`Strong finite-context Base` + `Persistent relationship-memory specialist` + `relative-utility estimator` → invocation decision.

Separate visually:

- observable online selector features;
- analysis-only relationship-state/context-distance diagnostics.

## Table 1 — Strong-base context and regime dependence

Combine compact same-protocol Base comparisons with KuaiLive candidate/temporal regime results.

Purpose: establish credible Bases and the regime-dependent paradox, not leaderboard superiority.

## Figure 2 — Core relationship-state mechanism figure

### Panel A: relationship-state sign structure

For recent-visible / long-horizon-only / unseen, show:

- Base visible-sequence status;
- older-history availability;
- DEV and untouched TEST Memory−Base effects;
- interpretation: largely redundant/harmful, complementary, or no recoverable target-specific relationship signal.

### Panel B: context distance and recency refinement

Plot:

`1–4`, `5–8`, `9–16`, `17–32`, `33–64`, `65+`, `unseen`.

Mark the 16-step visible-context boundary as a property of the evaluated LiveRec configuration, not as an independently discovered or universal threshold.

Highlight the ultra-recent positive pocket and the outside-visible-sequence positive region.

## Table 2 — Mechanism attribution and robustness

Include compact evidence for:

- Long-only / Short-only / Popularity-only;
- Memory-parameter sign stability;
- positive-utility prevalence by relationship state if reported;
- selected alternative-explanation strata if reported.

Move full matrices to the Appendix.

## Table 3 — Relative Utility vs Difficulty

Report KuaiLive first and frozen Twitch confirmation second.

Include:

- exact invocation budgets;
- Base;
- Difficulty;
- Selective Utility;
- Utility−Difficulty;
- Oracle headroom.

## Figure 3 — Selection composition

Compare Utility and Difficulty invocation composition by relationship state.

Primary visual message:

> **Difficulty can spend budget on hard-but-relationship-unsolvable events, whereas Utility better concentrates specialist use where historical relationship evidence is actionable.**

## Figure/Table 4 — Accuracy–cost frontier

Report:

- ranking quality;
- invocation rate;
- selector latency;
- end-to-end latency;
- throughput;
- memory/model footprint.

Keep deployment evidence subordinate to the principal scientific claims.

---

# 12. Related Work structure

## 12.1 Sequential, temporal, repeat-aware, and long-term recommendation

Cover finite-context sequence models, temporal/interval-aware approaches, repeat behavior, long-term preference, identity-aware recommendation, and long-context variants.

Do not claim that prior recommendation ignores long-term information.

The gap is narrower:

> **Prior work models long- and short-term signals, but the conditional incremental value of a separate persistent relationship representation relative to a strong finite-context Base is less well characterized.**

## 12.2 Knowledge-enhanced and multi-source recommendation

Cover knowledge-aware, multimodal, collaborative-knowledge, and external-information recommendation.

Recent KBS work already studies adaptive gating, multi-source reliability, complementary cues, redundancy reduction, and negative transfer. Therefore distinguish this paper through **event-level specialist-relative utility and relationship-state evidence**, not generic information fusion.

Representative comparison anchors should include recent KBS work on:

- multi-head gating for knowledge-aware recommendation;
- adaptive in-context expert networks for sequential recommendation;
- collaborative-knowledge alignment;
- negative transfer in sequential recommendation.

## 12.3 Adaptive routing, mixture-of-experts, selective prediction, and Learning-to-Defer

Acknowledge expert routing and cost-aware deferral as established methodological antecedents.

The manuscript should state explicitly:

> **The present work does not propose a new generic deferral theory. It studies a particular relationship specialist whose incremental utility has an interpretable relationship-state structure, and evaluates specialist-relative utility against matched-budget generic Difficulty.**

Do not equate all Learning-to-Defer methods with Difficulty routing.

## 12.4 Harmful auxiliary information and negative transfer

Use negative-transfer literature to motivate why more historical or auxiliary information need not improve ranking.

Connect harmful specialist invocation to redundancy or lack of event-relevant relationship evidence without asserting causal equivalence with established negative-transfer mechanisms.

## 12.5 Mechanistic interpretation in recommendation

Distinguish the paper from user-facing explainable recommendation.

The purpose is to explain **when a specialist information source helps or hurts relative to a strong Base**, not to generate natural-language explanations for individual recommendations.

---

# 13. Discussion structure

## 13.1 Conditional value rather than information accumulation

More history is not automatically better. Specialist value depends on whether target-specific evidence adds information not effectively represented in the current Base input.

## 13.2 Why the mechanism is not merely “longer history wins”

Discuss jointly:

- Always Memory can be globally harmful;
- unseen cases remain harmful despite Base difficulty;
- recent-visible and long-horizon-only have opposite signs;
- the 1–4 pocket breaks a monotonic distance account;
- Long-only attribution is regime-specific rather than globally dominant.

## 13.3 Why Difficulty is insufficient

A difficult event may be difficult because useful evidence is absent from both Base and specialist.

This motivates specialist-relative utility rather than hard-case routing alone.

## 13.4 Relationship to Learning-to-Defer

Position deferral/expert-routing literature as methodological context.

The paper’s contribution lies in the relationship-specialist problem characterization and empirical utility structure rather than new generic routing theory.

## 13.5 Simplicity and interpretability of the specialist

Explain that the transparent Memory formulation is a methodological design choice that makes specialist evidence and failure modes diagnosable.

Avoid implying that greater architectural complexity would necessarily strengthen the scientific contribution.

## 13.6 Utility-estimation headroom

The modest pointwise association and large Oracle gap should be discussed as an open problem in specialist-utility estimation.

Future work should prioritize better relative-utility estimation and stronger context-capacity interventions rather than merely increasing Memory complexity.

## 13.7 External validity

Limit claims to:

- the evaluated KuaiLive and Twitch/LiveRec settings;
- offline predictive ranking utility;
- the studied Base and relationship-Memory constructions.

Do not infer causal GMV, conversion, satisfaction, or unrestricted domain generalization.

---

# 14. Claim guardrails

Do **not** claim:

- Memory is globally superior or inferior independent of regime;
- generic gating, MoE, Learning-to-Defer, expert routing, or selective prediction is novel;
- specialist-minus-base utility is a new general deferral theorem;
- long/short-term modeling itself is novel;
- adding external knowledge to recommendation is novel;
- the relationship specialist uses an external dataset;
- the HGB selector is the principal methodological novelty;
- Memory utility increases monotonically with relationship distance;
- the 16-step boundary is independently discovered or universal;
- Long-only is globally superior;
- relationship-state or context-distance labels are online selector features;
- Base confidence alone identifies specialist-solvable events;
- generic Difficulty represents all prior expert-routing methods;
- event-level utility is well calibrated or near Oracle;
- three seeds establish seed invariance;
- strong-base comparisons establish SOTA superiority;
- the current specialist is an LLM/agentic recommender;
- post-hoc DEV recency refinement was pre-specified before the untouched test;
- the observed mechanism is causal or universal;
- offline gains imply causal business lift.

Preferred overarching sentence:

> **Explicit relationship Memory is a regime-dependent specialist: its incremental value depends on whether target-specific historical evidence is already represented in the Base’s visible sequence, remains available only in older history, or has not been observed; recency adds a non-monotonic structure, and specialist-relative utility exploits this heterogeneity more effectively than routing merely on Base difficulty.**

---

# 15. Abstract blueprint

The abstract should contain five moves:

1. **Problem:** persistent relationship evidence can complement a sequential recommender but can also be redundant or harmful.
2. **Formulation:** define specialist-minus-base ranking utility and selective invocation.
3. **Mechanism:** report the three relationship states and non-monotonic recency structure.
4. **Validation:** summarize KuaiLive multi-regime evidence and frozen untouched Twitch/LiveRec confirmation against strong Bases and same-budget Difficulty.
5. **Boundary:** acknowledge useful selective gains despite modest pointwise utility association and substantial remaining Oracle headroom.

Do not lead with HGB, Memory weights, “agent,” or architecture inventory.

---

# 16. Recommended Introduction contribution paragraph

The Introduction should present three contributions in this order:

1. **Conditional specialist decision formulation.** We formulate explicit relationship Memory as a specialist and estimate specialist-minus-base ranking utility, contrasting this target with generic Base Difficulty under matched invocation budgets.
2. **Relationship-state mechanism.** We identify a visibility × recency structure in which historically known but currently outside-context relationships form the dominant positive Memory regime; visible and unseen relationships are negative in aggregate, while an ultra-recent positive pocket rules out a monotonic-distance explanation. The three-state sign structure reproduces on untouched held-out data, while finer distance patterns are treated as DEV-only refinement.
3. **Multi-regime and frozen validation.** We validate the conditional-specialist principle across candidate/temporal regimes, independent Base realizations, strong-reference models, and a second-platform frozen one-shot test, and quantify the associated accuracy–cost trade-off and remaining Oracle headroom.

---

# 17. Recommended narrative order

Use the following order consistently across the Abstract, Introduction, Results, and Discussion:

> **regime paradox → specialist-relative formulation → relationship-state mechanism → Utility vs Difficulty decision → frozen transfer → robustness → deployment and utility-estimation limitations**

This ordering keeps the scientific contribution centered on **when persistent relationship evidence adds value beyond a strong Base**, while treating routing as the decision mechanism that exploits the discovered heterogeneity rather than as the novelty claim itself.
