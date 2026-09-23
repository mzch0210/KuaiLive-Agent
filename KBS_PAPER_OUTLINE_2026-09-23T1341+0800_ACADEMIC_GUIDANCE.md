# KBS paper outline — academic guidance version

> **INDEPENDENT / NON-AUTHORITATIVE OUTLINE**  
> This file is a manuscript-structure proposal and does not replace the frozen experimental protocol or the current authoritative outline unless explicitly promoted by the authors.

**Generated:** 2026-09-23T13:41+08:00  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Project:** `mzch0210/KuaiLive-Agent`  
**Primary source outline:** `KBS_PAPER_OUTLINE_2026-09-23T1317+0800_MECHANISM_RESTRUCTURED.md`

---

# 1. Paper positioning

Position the manuscript as a **conditional knowledge-specialist framework for recommendation**.

The paper should ask a knowledge-centered question:

> **When does explicit persistent user–creator relationship knowledge provide incremental ranking value beyond a strong finite-context sequential recommender, and how should that conditional value govern specialist invocation?**

The manuscript should not be positioned as:

- a new generic gating or mixture-of-experts method;
- a new long/short-term recommendation architecture;
- an LLM-agent or agentic-recommendation paper;
- a claim that relationship Memory is globally superior to a strong sequential model;
- a live-stream application paper whose novelty rests mainly on the application domain.

The preferred KBS framing is:

> **Relationship Memory is a regime-dependent knowledge specialist. Its incremental value depends on whether persistent relationship evidence is already visible to the Base, available only outside the Base’s finite context, or absent altogether. Recency introduces an additional non-monotonic structure. A specialist-relative utility estimator can exploit this heterogeneity more effectively than generic hard-case routing.**

---

# 2. Recommended title

## Primary

> **Learning When Relationship Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Mechanism-forward alternative

> **When Is Relationship Knowledge Complementary? Conditional Specialist Utility in Sequential Recommendation**

## Conservative alternative

> **Conditional Specialist Utility of Relationship Memory in Sequential Recommendation**

Use **relationship memory** or **persistent relationship knowledge** rather than generic *memory* whenever ambiguity with LLM memory or generic memory networks is possible.

---

# 3. Central thesis and novelty boundary

## 3.1 Central thesis

> **Explicit relationship Memory has no fixed global ordering relative to a strong sequential Base. Its marginal ranking utility varies across recommendation regimes and is structured by the visibility of target-specific relationship evidence relative to the Base’s finite context, together with recency. Persistent relationship evidence is most complementary when the relationship is historically known but no longer visible inside the Base context; it is largely redundant or harmful when already visible, and cannot be recovered when the relationship is unseen. A separate ultra-recent repeat pocket shows that the effect is not monotonic in distance. This conditional structure motivates specialist-minus-base utility as the routing target rather than generic case difficulty.**

## 3.2 Defensible novelty

The novelty should be presented as the combination of four elements:

1. **Specialist-relative utility formulation:** evaluate the incremental value of one explicit knowledge source relative to a strong Base rather than asking whether Memory is globally better.
2. **Knowledge-complementarity mechanism:** characterize when persistent relationship evidence is complementary, redundant, or unavailable relative to the Base’s visible sequential context.
3. **Decision distinction:** demonstrate that specialist-minus-base utility is not equivalent to generic Base difficulty under exact matched invocation budgets.
4. **Frozen multi-regime validation:** validate the principle across candidate and temporal regimes, independent Base realizations, and a second live-stream platform with an untouched one-shot test.

Do not claim novelty for gating, long/short-term modeling, expert selection, or external knowledge integration in isolation.

---

# 4. Formal problem formulation

Let `x` denote a recommendation event, `B` a strong sequential Base, `M` an explicit relationship-memory specialist, and `u_K(A,x)` event-level ranking utility at cutoff `K`.

Define specialist-minus-base utility:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

For observable routing information `z` and recommendation regime `r`, define:

\[
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The learned selector estimates `\hat\eta(z)` and invokes the specialist when predicted incremental value justifies the additional serving cost.

If specialist invocation has cost `c(x)` and cost weight `\lambda`, the idealized decision is:

\[
\pi^*(z)=\mathbf 1\left[
\mathbb E[\Delta_m(X)\mid Z=z]
>
\lambda\,\mathbb E[c(X)\mid Z=z]
\right].
\]

For approximately fixed or negligible incremental cost, this reduces to a positive-utility decision.

Treat this as a task-specific decision formulation, not as a new general theorem in Learning-to-Defer or selective prediction.

---

# 5. Relationship-knowledge states and mechanism

Use empirically grounded state variables rather than abstract claims that Memory itself is empty or complete.

Let:

- `V(x)=1` if the target creator relationship is visible inside the Base’s finite sequential context;
- `H(x)=1` if the target creator was observed in older history outside that visible context.

This yields three principal diagnostic states:

| Relationship state | `V(x)` | `H(x)` | Knowledge interpretation | Observed aggregate Memory role |
|---|---:|---:|---|---|
| recent-visible | 1 | any | target relationship already represented in visible context | largely redundant / harmful |
| long-horizon-only | 0 | 1 | target relationship historically known but outside Base context | **complementary** |
| unseen | 0 | 0 | no prior target-specific relationship evidence | strongly harmful / no recoverable relationship signal |

The diagnostic state labels are **analysis-only** and must not be described as online selector features.

## 5.1 Dominant mechanism

The main mechanism claim should be:

> **Persistent relationship evidence is most valuable when it remains available from older history but is no longer visible to the finite-context Base.**

This interpretation is supported by the held-out sign structure:

| Relationship state | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| recent-visible | −0.01995 | −0.01935 |
| **long-horizon-only** | **+0.23097** | **+0.22045** |
| unseen | −0.19562 | −0.18215 |

## 5.2 Mechanism attribution

Use component evidence to identify which information source carries the positive outside-context effect.

On long-horizon-only DEV events:

- Long-only: `ΔNDCG@10 = +0.33688`;
- Short-only: negative;
- Popularity-only: negative.

The interpretation should be specific:

> **The outside-context gain is attributable to persistent long-term relationship evidence rather than to generic popularity or short-term recurrence.**

Do not claim that Long-only is a globally superior recommender.

## 5.3 Finite-context diagnostic

Treat the 16-interaction result as **post-hoc DEV-only mechanism refinement**, not as a pre-specified held-out hypothesis.

On LiveRec DEV:

- the frozen horizon grouping is almost exactly recovered by a 16-interaction visibility boundary;
- last seen within 16 interactions: Memory−Base `−0.01980`;
- last seen beyond 16 interactions: Memory−Base `+0.23057`.

This supports the interpretation that the dominant positive regime aligns with relationship evidence falling outside the Base’s visible context.

Do not present `16` as a universal boundary.

## 5.4 Recency qualification

Distance-bin evidence shows a non-monotonic pattern:

- 1–4: `+0.04606`;
- 5–8: `−0.06511`;
- 9–16: `−0.15268`;
- 17–32: `+0.25668`;
- 33–64: `+0.20707`;
- 65+: `+0.12965`;
- unseen: `−0.19562`.

Therefore the paper should describe the mechanism as:

\[
\text{Memory utility}
\approx
f(\text{relationship visibility relative to Base context},\ \text{recency regime}),
\]

not as a monotonic horizon law.

---

# 6. Research questions

**RQ1 — Regime dependence.** How does the aggregate value of explicit relationship Memory change across candidate and temporal recommendation regimes?

**RQ2 — Knowledge complementarity.** Under what relationship-visibility and recency conditions does persistent relationship evidence become complementary to, redundant with, or unavailable to a strong finite-context sequential recommender, and which Memory component carries the positive outside-context effect?

**RQ3 — Specialist decision.** Can specialist-minus-base utility be estimated from observable user/history state and Base-confidence information well enough to improve a strong Base, and does this target contain decision-relevant information beyond generic Difficulty?

**RQ4 — Robustness and transfer.** Do the selective advantage and the relationship-state mechanism survive independent Base realizations and reproduce on a second live-stream platform under a frozen untouched evaluation protocol?

**RQ5 — Deployment.** What accuracy–invocation–latency/footprint trade-off follows from specialist use, how informative is the utility estimator, and how much same-budget Oracle headroom remains?

---

# 7. Method section structure

## 7.1 Strong sequential Bases

Describe:

- the KuaiLive identity-aware Dual-ID Base;
- the frozen official LiveRec availability-aware/repeat-aware Base.

Use comparator evidence only to establish that these are credible scientific reference models. Do not make state-of-the-art or leaderboard claims.

## 7.2 Explicit relationship-memory specialist

Use the frozen transferred score:

\[
0.45\,Short + 0.45\,Long + 0.10\,Popularity.
\]

Explain each component transparently. The methodological purpose is to expose a persistent relationship knowledge source whose availability and marginal value can be diagnosed separately from the Base representation.

Do not present this weighted formula as the main algorithmic novelty.

## 7.3 Relative-utility estimator

Use observable state and Base-confidence features to estimate `\hat\eta(z)`.

The HGB model is the scientific selector used in the frozen result. Its role is to operationalize the specialist decision, not to constitute the main contribution.

## 7.4 Difficulty control

Use the same observable information and comparable model family to predict Base error/difficulty.

Evaluate Utility and Difficulty under **exact matched invocation budgets**.

The conceptual distinction is:

> **Difficulty asks where the Base is weak; Utility asks where this particular specialist improves the Base.**

## 7.5 Oracle and cost-aware analysis

Use exact-budget Oracle only as analysis-only upper-bound headroom.

Serving cost should include:

- Base inference;
- selector overhead;
- specialist invocation;
- model/cache footprint where relevant.

Invocation rate alone should not be used as a compute proxy.

---

# 8. Experimental design

## 8.1 Datasets and evaluation settings

Use:

- KuaiLive;
- Twitch/LiveRec.

Evaluation regimes should include sampled-active, full-active, standard temporal, and strict temporal settings where applicable.

## 8.2 Frozen external validation

The main paper should summarize the protocol as:

> **DEV discovery and policy freeze → untouched one-shot TEST evaluation.**

The Appendix should document the full P1 chronology, hashes, guardrails, implementation details, and recovery provenance.

The main text should not be dominated by audit chronology.

## 8.3 Metrics and inference

Primary metric:

- NDCG@10.

Secondary metric:

- H@10.

Statistical reporting:

- paired user-level bootstrap;
- exact matched budgets;
- training-seed robustness summarized with mean ± SD and sign consistency.

Do not reinterpret within-seed bootstrap intervals as across-seed confidence intervals.

## 8.4 Mechanism evidence

Separate confirmatory evidence from exploratory refinement.

### Confirmatory evidence

- frozen DEV relationship-state sign structure;
- untouched TEST replication of the same sign structure;
- component × relationship-state attribution.

### DEV-only mechanism refinement

- 16-step finite-context reconstruction;
- distance-bin recency analysis;
- ultra-recent 1–4 positive pocket.

This distinction should be explicit in the Results narrative.

## 8.5 Robustness and validity

Report:

- Memory-parameter sensitivity;
- state/confidence feature-family ablation;
- independent deep Base training seeds;
- strong-base competitiveness;
- formal complexity and empirical efficiency.

## 8.6 Alternative-explanation checks — recommended strengthening

If feasible without changing frozen policies, add stratified diagnostic analyses to test whether the long-horizon-only gain is merely a proxy for another factor.

Recommended stratifications:

- user history length;
- target creator popularity/exposure frequency;
- candidate-set size or active-room density;
- user repeat propensity.

The desired interpretation is not that the mechanism is fully causal, but that the outside-context effect is not trivially explained by one obvious observable confounder.

Also report, where feasible:

\[
P(\Delta_m>0\mid \text{relationship state})
\]

in addition to mean `Memory−Base`, so that the mechanism is not supported only by group averages.

---

# 9. Results section structure

## 9.1 Finding 1 — Global Memory ordering is regime-dependent

Establish the paradox first.

Headline KuaiLive evidence:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active: Memory−Base approximately `+0.03367`, native Selective−Base approximately `+0.05345`;
- strict temporal: Selective−Base approximately `+0.07282` / `+0.09743`.

Main interpretation:

> **Aggregate Memory value is regime-dependent; a single global Memory-vs-Base ordering is not an adequate scientific characterization.**

Use this result to motivate mechanism analysis rather than to claim that Selective always dominates every fixed strategy in every regime.

## 9.2 Finding 2 — Relationship visibility and recency explain knowledge complementarity

Present the three-state DEV→TEST sign structure first.

Then present component attribution.

Only after the confirmatory evidence should the paper introduce the DEV-only 16-step reconstruction and distance-bin analysis.

The section should end with the conservative mechanism statement:

> **Across the evaluated LiveRec/Twitch setting, the dominant positive Memory regime occurs when a previously observed relationship lies outside the Base’s finite visible context. Recent-visible and unseen relationships are negative in aggregate, while an additional ultra-recent repeat pocket prevents a monotonic-distance interpretation.**

## 9.3 Finding 3 — Specialist-relative Utility is more decision-relevant than Difficulty

Lead with the conceptual distinction:

- hard does not imply memory-solvable;
- unseen events can be difficult while offering no target-specific relationship evidence for Memory to recover.

Report:

- KuaiLive Utility−Difficulty under matched budgets;
- state/confidence feature-family evidence;
- training-seed sign consistency;
- relationship-state composition of Utility vs Difficulty selections.

Central statement:

> **Base weakness is not sufficient evidence that a relationship specialist possesses complementary information.**

## 9.4 Finding 4 — Frozen transfer confirms the principle but leaves substantial headroom

Untouched Twitch TEST:

- exact budget `K=6,650`;
- Base NDCG@10 `0.58211`;
- Difficulty exact-K `0.58340`;
- Selective Utility `0.58983`;
- Selective−Base `+0.00772`, 95% CI `[+0.00641,+0.00903]`;
- Utility−Difficulty `+0.00644`, 95% CI `[+0.00528,+0.00762]`;
- utility/realized Spearman approximately `0.173`;
- same-budget Oracle gain captured approximately `11.7%`.

Interpretation:

> **Useful specialist escalation requires sufficiently informative utility ranking, not precise event-level calibration. The large Oracle gap shows that utility estimation remains far from solved.**

Do not hide the modest correlation or Oracle gap; use them to define the method’s boundary and future research direction.

---

# 10. Figures and tables

## Figure 1 — Conditional knowledge-specialist framework

Show:

`Strong finite-context Base` + `Persistent relationship-memory specialist` + `relative-utility estimator` → invocation decision.

Clearly separate:

- observable online selector features;
- analysis-only relationship-state/context-distance diagnostics.

## Table 1 — Strong-base context and regime dependence

Combine compact same-protocol Base comparisons with KuaiLive candidate/temporal regime results.

Purpose: establish a credible Base and the regime-dependent paradox, not a leaderboard.

## Figure 2 — Core mechanism figure

### Panel A: relationship states

For recent-visible / long-horizon-only / unseen, show:

- Base visibility;
- older-history availability;
- DEV and untouched TEST Memory−Base effects;
- interpretation: redundancy / complementarity / no recoverable target-specific relationship signal.

### Panel B: context distance and recency

Plot:

`1–4`, `5–8`, `9–16`, `17–32`, `33–64`, `65+`, `unseen`.

Mark:

- Base context boundary at 16 for this LiveRec configuration;
- ultra-recent positive pocket;
- outside-context positive region.

The figure should make clear that the effect is structured but non-monotonic.

## Table 2 — Mechanism attribution and robustness

Include compact evidence for:

- Long-only / Short-only / Popularity-only;
- Memory-parameter sign stability;
- selected relationship-state prevalence / positive-utility prevalence if available;
- selected alternative-explanation stratifications if added.

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

> **Difficulty allocates more calls to hard-but-memory-unsolvable events, whereas Utility concentrates specialist use more effectively where relationship evidence is recoverable.**

## Figure/Table 4 — Accuracy–cost frontier

Report:

- accuracy;
- invocation rate;
- selector latency;
- end-to-end latency;
- throughput;
- memory/model footprint.

Keep deployment evidence subordinate to the scientific mechanism and decision contribution.

---

# 11. Related Work structure

## 11.1 Sequential, temporal, repeat-aware, and long-term recommendation

Cover finite-context sequence models, interval/time-aware methods, repeat behavior, long-term preference, and identity-aware recommendation.

Do not claim that prior recommendation ignores long-term information.

The relevant gap is narrower:

> **Prior work models long- and short-term signals, but the conditional incremental value of an explicit persistent relationship knowledge source relative to a strong finite-context Base is less well characterized.**

## 11.2 Knowledge-enhanced recommendation and information complementarity

Cover knowledge-aware, multimodal, collaborative-knowledge, and external-information recommendation.

Recent KBS work already studies adaptive fusion, heterogeneous information reliability, complementarity, redundancy, and negative transfer. Therefore distinguish this paper by emphasizing **event-level specialist-relative knowledge utility**, not feature-fusion novelty.

## 11.3 Adaptive routing, mixture-of-experts, selective prediction, and Learning-to-Defer

Acknowledge that expert routing and cost-aware deferral are established research areas.

Make the distinction explicit:

> **The paper does not propose a new generic deferral theory. It studies a specific external knowledge specialist whose usefulness can be mechanistically related to whether target-specific relationship evidence is visible, outside-context, or absent, and evaluates a specialist-relative utility target against same-budget generic Difficulty.**

## 11.4 Negative transfer and harmful auxiliary information

Use this literature as conceptual support for the observation that more knowledge is not necessarily beneficial.

Connect recent-visible and unseen harm to the broader question of when additional information becomes redundant, noisy, or misleading.

Do not reframe the entire paper as a negative-transfer method.

## 11.5 Mechanistic interpretation in recommendation

Distinguish this work from user-facing explainable recommendation.

The paper explains **why a knowledge source helps or hurts under different information states**, rather than generating natural-language or path-based explanations for individual recommendations.

---

# 12. Discussion structure

## 12.1 Knowledge complementarity rather than knowledge accumulation

More historical information is not automatically better.

Its value depends on whether it adds target-specific evidence unavailable to the Base in the current decision context.

## 12.2 Redundancy, complementarity, and absence

Use these three concepts to interpret relationship Memory more precisely than a generic short-term/long-term dichotomy.

## 12.3 Recency as a second mechanism axis

The ultra-recent positive pocket shows that relationship visibility alone is not a complete explanation.

Do not overgeneralize the 16-step boundary.

## 12.4 Why Difficulty is insufficient

A hard event can be difficult because the Base lacks signal, while the specialist may also lack relevant relationship evidence.

This is the central reason to use specialist-relative utility.

## 12.5 Relationship to Learning-to-Defer

Position L2D and expert routing as methodological antecedents.

The paper’s contribution is domain- and knowledge-source-specific characterization of specialist utility, not generic routing theory.

## 12.6 Relationship to negative transfer

Interpret harmful Memory invocation as evidence that auxiliary knowledge can induce negative transfer when it is redundant or lacks event-relevant signal.

Use this as a conceptual connection, not a causal claim.

## 12.7 Utility-estimation headroom

The modest event-level correlation and large Oracle gap indicate that reliable specialist-utility estimation remains an open problem.

Future work should prioritize better relative-utility estimation rather than merely increasing Memory complexity.

## 12.8 External validity

Limit claims to:

- the evaluated KuaiLive and Twitch/LiveRec settings;
- offline predictive ranking utility;
- the studied Base and relationship-Memory constructions.

Do not claim causal GMV, conversion, satisfaction, or unrestricted cross-platform generalization.

---

# 13. Claim guardrails

Do **not** claim:

- Memory is globally superior or inferior independent of regime;
- generic gating, MoE, Learning-to-Defer, or selective prediction is novel;
- long/short-term modeling itself is novel;
- the HGB selector is the principal methodological contribution;
- adding external knowledge to sequential recommendation is novel in itself;
- Memory utility increases monotonically with relationship distance;
- `16` is a universal memory/context boundary;
- Long-only is globally superior;
- relationship-state or context-distance labels are online selector features;
- Base confidence alone identifies memory-solvable events;
- generic Difficulty identifies specialist-solvable events;
- event-level utility is well calibrated or near Oracle;
- three seeds establish seed invariance;
- strong-base comparisons establish SOTA superiority;
- the current Memory specialist is an LLM/agentic recommender;
- the post-hoc DEV distance refinement was pre-specified before the untouched test;
- P1.3 was used for policy tuning;
- the mechanism is causal;
- the mechanism is universal beyond the evaluated designs;
- offline gains imply causal business lift.

Preferred overarching sentence:

> **Relationship Memory is a regime-dependent knowledge specialist: its incremental value depends on whether target-specific relationship evidence is already visible to, outside the finite context of, or unavailable to a strong sequential Base, with recency introducing an additional non-monotonic structure; specialist-relative utility can exploit this heterogeneity more effectively than generic hard-case routing.**

---

# 14. Abstract blueprint

The abstract should contain five moves:

1. **Problem:** persistent relationship knowledge can complement a sequential recommender but may also be redundant or harmful.
2. **Formulation:** define specialist-minus-base ranking utility and selective invocation.
3. **Mechanism:** identify the relationship-visibility × recency structure, emphasizing outside-context complementarity and non-monotonic recency.
4. **Validation:** report multi-regime KuaiLive evidence and frozen untouched Twitch/LiveRec confirmation against strong Bases and same-budget Difficulty.
5. **Boundary:** note useful selective gains despite modest pointwise utility correlation and substantial remaining Oracle headroom.

Do not lead with HGB, weighted Memory components, or architecture inventory.

---

# 15. Recommended Introduction contribution paragraph

The Introduction should present contributions in this order:

1. **Conditional specialist formulation.** We formulate explicit relationship Memory as a knowledge specialist and define specialist-minus-base ranking utility as the relevant decision quantity.
2. **Knowledge-complementarity mechanism.** We identify a relationship-visibility × recency structure in which historically known but currently outside-context relationships form the dominant positive Memory regime; visible and unseen relationships are negative in aggregate, while an ultra-recent repeat pocket prevents a monotonic-distance explanation.
3. **Specialist-relative decision.** We show that predicting relative Utility is more decision-relevant than predicting generic Base Difficulty under exact matched invocation budgets and across independent Base training seeds.
4. **Frozen multi-regime validation.** We validate the principle across candidate/temporal regimes and a second-platform untouched one-shot test, and quantify the associated accuracy–cost trade-off and remaining Oracle headroom.

---

# 16. Recommended narrative order for the full paper

Use the following order consistently in the Abstract, Introduction, Results, and Discussion:

> **regime paradox → specialist-relative formulation → knowledge-complementarity mechanism → Utility vs Difficulty decision → frozen transfer → robustness → deployment/headroom limitations**

This ordering keeps the mechanism as a central scientific contribution while preserving routing as the method that exploits the mechanism rather than the novelty claim itself.
