# KBS paper outline — mechanism-centered restructuring draft

> **NON-AUTHORITATIVE / INDEPENDENT SNAPSHOT — DO NOT USE AS A SILENT REPLACEMENT FOR THE CURRENT AUTHORITATIVE OUTLINE**
>
> This file is a KBS-oriented restructuring proposal created to preserve provenance and avoid accidental overwrite or misuse. It **supersedes nothing** unless the authors explicitly promote it later.

**Generated timestamp:** 2026-09-23T13:17+08:00  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Authoritative source outline at creation:** `KBS_PAPER_OUTLINE_2026-09-22T1811+0800_COMPACT.md`  
**Source outline blob SHA:** `f46a712b1d0dc81f41418ec469173994d02fe93b`  
**General provenance skeleton:** `PAPER_SKELETON_2026-09-22_POST_P1_3.md`  
**Purpose of this snapshot:** restructure the paper so that the empirically validated **relationship-visibility × recency knowledge-complementarity mechanism** becomes a principal scientific contribution, while routing remains the decision method that exploits this heterogeneity rather than the novelty claim by itself.  
**Experiment status inherited from the authoritative outline:** core chain CLOSED; P1.3 untouched test CLOSED/FROZEN; DEV-only Memory sensitivity and finite-context analyses CLOSED; formal complexity/efficiency CLOSED; deep Base training-seed robustness CLOSED; strong-base competitiveness CLOSED on KuaiLive and Twitch/LiveRec.

---

# 1. KBS positioning

Position the paper as a **conditional knowledge-specialist decision framework grounded in an empirically validated knowledge-complementarity mechanism**.

Do **not** position it as:

- a generic live-stream application paper;
- a new sequential-recommendation backbone;
- a generic gating / mixture-of-experts contribution;
- an LLM-agent paper;
- a claim that relationship Memory is globally superior.

Preferred KBS framing:

> **A persistent relationship-memory specialist is valuable when it contains recommendation-relevant knowledge that is complementary to, rather than redundant with or unavailable to, a strong finite-context sequential recommender. Its incremental utility is jointly structured by relationship visibility and recency, and this heterogeneity can be exploited by estimating specialist-minus-base utility rather than generic case difficulty.**

Why this framing fits KBS:

1. it treats persistent user–creator relationship information as an explicit knowledge source rather than merely another latent feature block;
2. it formulates specialist invocation as a prediction/decision problem under heterogeneous knowledge regimes;
3. it provides mechanism evidence explaining **when and why** the external knowledge source is complementary, redundant, or unavailable;
4. it connects methodological effectiveness to deployment cost and decision quality rather than reporting accuracy alone.

This KBS-fit rationale is a manuscript-positioning judgment, not evidence that KBS acceptance is guaranteed.

---

# 2. Recommended title

## Primary

> **Learning When Relationship Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Mechanism-forward alternative

> **When Is Relationship Knowledge Complementary? Conditional Specialist Utility in Sequential Recommendation**

## Conservative alternative

> **Conditional Specialist Utility of Relationship Memory in Sequential Recommendation**

Use **relationship memory** or **persistent relationship knowledge**, not generic “memory,” whenever ambiguity with LLM memory or generic memory networks is possible.

---

# 3. Central thesis

> **Explicit relationship memory is not globally superior to a strong sequential recommender. Its marginal predictive value changes across recommendation regimes because the information carried by persistent user–creator relationships may be redundant with the Base’s visible context, complementary when a known relationship falls outside that context, or unavailable when no relationship has been observed. Recency adds a distinct ultra-recent repeat regime, so the mechanism is not monotonic in distance. This conditional knowledge value can be exploited by estimating specialist-minus-base ranking utility rather than generic case difficulty.**

The evidence should be organized in the following causal/narrative order:

1. **Regime:** aggregate Memory–Base ordering changes under candidate and temporal regimes.
2. **Knowledge mechanism:** relationship visibility and recency explain where persistent relationship information is complementary, redundant, or unavailable.
3. **Decision:** specialist-minus-base utility is a more appropriate routing target than generic Base difficulty.
4. **Validation:** the mechanism and selective decision advantage survive strong-base controls, independent Base training seeds, and a frozen untouched cross-platform test.
5. **Deployment:** useful escalation does not require near-perfect pointwise utility calibration, but selector cost and specialist invocation jointly determine practical value.

---

# 4. Four principal contributions — reordered for KBS

## Contribution 1 — Conditional specialist-utility formulation

Let `B` denote a strong sequential Base, `M` the explicit relationship-memory specialist, and `u_K(A,x)` event-level offline ranking utility:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x),
\qquad
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The paper reframes the scientific question from:

> “Is Memory globally better than the Base?”

into:

> **“When does this explicit knowledge source provide positive incremental utility beyond the Base?”**

The formulation is deliberately specialist-relative. It does not claim a new general decision-theory theorem.

## Contribution 2 — Relationship-visibility × recency knowledge-complementarity mechanism

Identify three principal relationship-knowledge states relative to the Base:

| Knowledge state | Base context contains target relationship? | Persistent Memory contains target relationship? | Expected role of Memory | Observed sign |
|---|---:|---:|---|---:|
| recent-visible | yes | yes | largely redundant / potentially harmful | negative aggregate |
| long-horizon-only | no | yes | **complementary** | **strongly positive** |
| unseen | no | no | no recoverable relationship knowledge | strongly negative |

The mechanism is sharpened by an independent DEV finite-context diagnostic:

- a **16-interaction visibility boundary** almost exactly reproduces the frozen relationship-horizon split;
- within 16 interactions, aggregate Memory−Base is negative;
- beyond 16 interactions, Memory−Base becomes strongly positive;
- however, distance 1–4 forms a separate positive **ultra-recent repeat pocket**, so the mechanism is **not** “farther is always better.”

Component evidence attributes the outside-context benefit specifically to persistent long-term relationship strength: on long-horizon-only DEV events, Long-only is strongly positive while Short-only and Popularity-only are negative.

The contribution is therefore not “long-term preference matters.” The stronger statement is:

> **Persistent relationship knowledge is most valuable when it is relevant and available to the specialist but outside the strong Base’s currently visible sequential context; recency creates an additional local regime that prevents a monotonic-distance interpretation.**

## Contribution 3 — Relative-utility decision rule beyond generic difficulty

Estimate `\hat\eta(z)` from observable user/history state and Base-confidence features, and selectively invoke `M`.

Compare against:

- Always Base;
- Always Memory;
- exact-matched-budget generic Difficulty routing;
- exact-budget Oracle headroom.

Core distinction:

> **Base weakness is not equivalent to specialist knowledge availability. Hard cases are not necessarily memory-solvable cases.**

Routing/gating itself is prior art. The contribution is the **specialist-relative target** and the empirical demonstration that it better identifies cases where this particular external knowledge source improves the Base.

## Contribution 4 — Multi-regime, cross-platform, frozen held-out validation

Validate the conditional-specialist principle across:

- KuaiLive sampled-active and full-active candidate regimes;
- standard and strict temporal settings;
- strong-base controls and independent Base training seeds;
- a strong official LiveRec/Twitch Base;
- a frozen DEV → untouched one-shot TEST protocol with no post-test rescue tuning.

Treat training-seed robustness and strong-base competitiveness as targeted validity evidence, not separate headline contributions or SOTA claims.

---

# 5. Conceptual knowledge mechanism

The mechanism should be made explicit before introducing the learned router.

Let `K_B(x)` denote recommendation-relevant relationship information represented in the Base’s currently visible context and `K_M(x)` denote persistent relationship information accessible to Memory.

Use this only as an explanatory abstraction, not as an estimable information-theoretic identity.

### State A — visible + known: redundancy

When the target relationship is already represented in the Base context:

\[
K_M(x) \approx K_B(x)
\]

Memory contributes little incremental information and may introduce scoring bias or overwrite a stronger context-sensitive Base estimate.

### State B — outside-context + known: complementarity

When a target relationship exists historically but falls outside the Base context:

\[
K_M(x) \not\subseteq K_B(x), \qquad K_M(x) \neq \varnothing
\]

Memory contains recommendation-relevant relationship knowledge unavailable to the finite-context Base. This is the dominant positive regime.

### State C — unseen: unavailability

When no prior target relationship exists:

\[
K_M(x)=\varnothing
\]

A weak Base prediction does not imply that Memory has useful information to recover. This explains why generic Difficulty can over-select memory-unsolvable events.

### Recency qualification

Do not reduce the mechanism to the three coarse states alone. The distance analysis identifies a separate positive 1–4 interaction pocket, followed by negative 5–16 distances and a strong positive shift at 17+.

Therefore the defensible mechanism is:

\[
\text{Memory complementarity}
\approx f(\text{relationship visibility relative to Base context},\ \text{recency regime})
\]

not:

\[
\text{Memory utility increases monotonically with distance.}
\]

The relationship-horizon and distance diagnostics remain **analysis-only** and must not be presented as online gate features.

---

# 6. Decision-theoretic motivation

If invoking the specialist incurs incremental cost `c(x)` and cost weight `\lambda`, the idealized binary decision is

\[
\pi^*(z)=\mathbf 1\left[
\mathbb E[\Delta_m(X)\mid Z=z]
>
\lambda\,\mathbb E[c(X)\mid Z=z]
\right].
\]

With negligible or approximately fixed incremental cost:

\[
\pi^*(z)=\mathbf 1[\eta(z)>0].
\]

The HGB gate is a plug-in estimator for this decision problem. It is not itself the primary novelty.

Prediction quality should be evaluated according to the decision task: accurate global event-level calibration is not necessary if the estimator can reliably rank a useful positive-utility tail. This is especially important because the untouched Twitch test has only modest event-level Spearman correlation while still yielding a significant selective gain.

---

# 7. Five research questions — mechanism-centered version

**RQ1 — Regime dependence.** How does the aggregate value of explicit relationship memory change across candidate and temporal recommendation regimes?

**RQ2 — Knowledge complementarity.** Under what relationship-visibility and recency conditions does persistent relationship knowledge provide information that is complementary to, redundant with, or unavailable to a strong finite-context sequential recommender, and which Memory component carries the outside-context benefit?

**RQ3 — Specialist decision.** Can specialist-minus-base utility be estimated well enough from observable state and Base-confidence information to improve a strong Base, and does this target contain decision-relevant information beyond generic Difficulty?

**RQ4 — Frozen transfer and robustness.** Do the selective advantage and the relationship-visibility/recency mechanism reproduce under independent Base realizations and on a second live-stream platform with a frozen strong Base and untouched held-out evaluation?

**RQ5 — Deployment.** What utility can be predicted from observable information, how much Oracle headroom remains, and what accuracy–invocation–latency/footprint trade-off follows from specialist use?

Mapping of secondary analyses:

- component × relationship regime → RQ2 mechanism attribution;
- finite-context distance diagnostic → RQ2 mechanism validation;
- Memory-parameter sensitivity → RQ2 robustness;
- state/confidence feature families → RQ3/RQ5;
- training-seed robustness → RQ3/RQ4;
- strong-base competitiveness → RQ4 validity context;
- formal complexity/efficiency → RQ5.

---

# 8. Recommended manuscript structure

## 1. Introduction

Recommended narrative order:

**paradox → regime dependence → incremental-utility formulation → knowledge-complementarity mechanism → Utility vs Difficulty decision → frozen transfer → deployment/headroom limitation**.

The Introduction should establish five points quickly:

1. live-stream recommendation combines rapidly changing candidates with persistent user–creator relationships;
2. a strong finite-context sequential/identity-aware Base already contains substantial relationship information, so explicit Memory should not be assumed beneficial;
3. the empirical paradox is that Always Memory can be worse while selective Memory improves the Base;
4. the key mechanism is whether persistent relationship knowledge is **redundant with, outside, or absent from** the Base’s visible context, with an additional recency effect;
5. this motivates estimating specialist-minus-base utility rather than routing generic hard cases.

Suggested mechanism sentence for the Introduction:

> **The key issue is not memory strength in isolation, but knowledge complementarity: persistent relationship information is most valuable when it remains available to the specialist yet falls outside the strong sequential Base’s visible context; when it is already visible it is largely redundant, and when the relationship is unseen there is no relationship knowledge to recover.**

Immediately qualify this with the non-monotonic recency result so the paper does not imply a universal horizon law.

## 2. Related Work

### 2.1 Sequential, repeat-aware, temporal, and long-term recommendation

Cover finite-context sequence modeling, repeated-consumption behavior, temporal intervals, long-term preference, and identity-aware recommendation.

### 2.2 Explicit relationship knowledge and knowledge-enhanced recommendation

Distinguish the paper’s transparent user–creator relationship knowledge from:

- latent ID embeddings;
- knowledge-graph semantics;
- multimodal/content knowledge;
- retrieval augmentation;
- LLM world knowledge;
- generic memory networks.

The key literature gap is not “existing models ignore long-term information.” Recent KBS work already models long/short-term interests and multiple knowledge sources. The defensible gap is **when an explicit persistent relationship knowledge source is complementary to a strong finite-context Base and how that conditional value should drive invocation**.

### 2.3 Adaptive routing, gating, Learning-to-Defer, and mixture-of-experts

Acknowledge generic gating as established prior art. Recent KBS work already uses adaptive gating for heterogeneous knowledge/view fusion; therefore do not make gating novelty claims.

Distinguish:

- **internal representation/feature fusion** from
- **event-level invocation of an external relationship specialist based on its predicted incremental utility over a frozen/strong Base**.

### 2.4 Difficulty-aware learning and decision under heterogeneous regimes

Separate:

- “Where is the Base weak?” from
- “Where does this particular knowledge specialist improve the Base?”

Connect candidate/temporal shifts to changes in specialist prevalence and aggregate ordering.

### 2.5 Mechanism-oriented recommendation analysis

Position the relationship-visibility analysis as **mechanistic interpretation of knowledge utility**, not user-facing explanation generation.

Clarify that the paper explains why an external knowledge source helps or hurts under different information states rather than generating natural-language recommendation explanations.

## 3. Problem Formulation and Knowledge States

### 3.1 Recommendation event and legal candidate set

Define event `x`, legal candidates, Base `B`, Memory specialist `M`, and ranking utility `u_K`.

### 3.2 Specialist-minus-base utility

Define `\Delta_m`, `\eta(z,r)`, and the distinction from generic Difficulty.

### 3.3 Relationship knowledge states

Introduce visible-known / outside-context-known / unseen as **analysis concepts**, with explicit warning that horizon/distance labels are not online router inputs.

### 3.4 Cost-aware decision rule

Introduce `\pi^*(z)` and matched-budget evaluation.

## 4. Conditional Relationship-Memory Specialist Framework

### 4.1 Strong sequential Bases

- KuaiLive identity-aware Dual-ID Base;
- frozen official LiveRec availability-aware/repeat-aware Base.

### 4.2 Explicit relationship-memory specialist

Frozen transferred score:

\[
0.45\,Short + 0.45\,Long + 0.10\,Popularity.
\]

Explain Short, Long, and Popularity as transparent scoring components. Do not oversell this formula as the algorithmic novelty.

### 4.3 Relative-utility estimator

Scientific HGB gate using observable state + Base-confidence features.

### 4.4 Matched-budget controls

Difficulty receives the same observable information/model family but predicts Base error. Oracle is analysis-only.

### 4.5 Serving cost

Total selective cost = Base inference + selector overhead + specialist invocation cost. Invocation rate alone is not a sufficient compute proxy.

## 5. Experimental Design

### 5.1 Datasets and strong-base context

KuaiLive and Twitch/LiveRec. Use compact same-protocol competitiveness evidence only to establish credible Bases, not to claim leaderboard superiority.

### 5.2 Candidate and temporal regimes

Sampled-active, full-active, standard temporal split, and strict temporal variants.

### 5.3 Frozen external protocol

Main text: DEV freeze → untouched TEST.

Appendix: complete P1.1/P1.2/P1.3 chronology, hashes, guardrails, recovery provenance, and implementation details.

### 5.4 Metrics and inference

- primary: NDCG@10;
- secondary: H@10;
- paired user-level bootstrap;
- exact matched invocation budgets;
- across training seeds: mean ± SD + sign consistency, without misusing within-seed bootstrap CIs as across-seed confidence intervals.

### 5.5 Mechanism validation and robustness

Separate **mechanism validation** from generic robustness:

**Mechanism attribution / validation**

- relationship-regime sign structure;
- component × relationship-regime ablation;
- 16-step finite-context reconstruction;
- distance-bin recency analysis including 1–4 pocket.

**Robustness / validity**

- Memory-parameter sensitivity on DEV only;
- state/confidence feature-family ablation;
- independent deep Base training seeds;
- strong-base competitiveness;
- formal complexity and empirical efficiency.

---

# 9. Four scientific findings — reordered

## Finding 1 — Global Memory ordering is regime-dependent

KuaiLive establishes that aggregate Memory value is not a fixed model property.

Headline evidence:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active: Memory−Base changes sign to approximately `+0.03367`, while native Selective−Base is about `+0.05345`;
- strict temporal: Selective−Base rises to about `+0.07282` / `+0.09743`.

Interpretation:

> **Candidate and temporal regimes change both specialist prevalence and aggregate utility; a single global Memory-vs-Base ordering is scientifically misleading.**

This motivates looking for a mechanism that explains within- and across-regime heterogeneity.

## Finding 2 — Relationship visibility and recency explain knowledge complementarity

Lead this section with the frozen DEV mechanism and untouched TEST replication:

| Relationship regime | DEV Memory−Base | TEST Memory−Base | Mechanistic interpretation |
|---|---:|---:|---|
| recent-visible | −0.01995 | −0.01935 | relationship already visible → redundancy / harm |
| **long-horizon-only** | **+0.23097** | **+0.22045** | **known but outside context → complementarity** |
| unseen | −0.19562 | −0.18215 | no recoverable relationship knowledge |

### Mechanism attribution

On long-horizon-only DEV events:

- Long-only `ΔNDCG@10 = +0.33688`;
- Short-only is negative;
- Popularity-only is negative.

Long-only is not globally superior; it becomes useful specifically in the information regime matching its knowledge source.

### Finite-context mechanism validation

On LiveRec DEV:

- frozen relationship horizon is almost exactly reproduced by a 16-interaction visibility boundary;
- last seen within 16: Memory−Base `−0.01980`;
- last seen beyond 16: Memory−Base `+0.23057`.

The independent reconstruction supports the interpretation that the positive long-horizon effect corresponds to relationship information outside the strong Base’s finite visible context rather than being merely an arbitrary grouping artifact.

### Recency qualification

Distance bins show:

- 1–4: `+0.04606`;
- 5–8: `−0.06511`;
- 9–16: `−0.15268`;
- 17–32: `+0.25668`;
- 33–64: `+0.20707`;
- 65+: `+0.12965`;
- unseen: `−0.19562`.

Therefore:

> **Relationship visibility explains the dominant outside-context complementarity, while recency introduces a distinct ultra-recent repeat pocket. The effect is structured, not monotonic.**

Memory-parameter sensitivity strengthens this finding: reasonable DEV-only perturbations preserve the recent-visible negative / long-horizon positive / unseen negative sign structure.

## Finding 3 — Relative utility is more decision-relevant than generic difficulty

After establishing the knowledge mechanism, show why it implies a different decision target.

Core logic:

- Difficulty asks whether the Base is weak.
- Utility asks whether **this specialist has complementary information that improves the Base**.
- Unseen events can be hard for the Base while also being unsolvable by relationship Memory.

Evidence:

- KuaiLive Utility−Difficulty is positive in sampled-active and full-active settings;
- State+Confidence is stronger than either family alone;
- Confidence-only is clearly weaker, so utility is not reducible to Base uncertainty;
- across three independently trained Base realizations, Selective remains above Base and Utility remains above matched-budget Difficulty in all three seeds despite varying invocation rates.

Central statement:

> **Hard cases are not necessarily memory-solvable cases because difficulty does not encode the availability of complementary specialist knowledge.**

Do not claim seed invariance; three seeds are targeted robustness evidence.

## Finding 4 — Frozen transfer confirms the principle while substantial decision headroom remains

Use compact strong-base comparisons first to establish that the scientific Bases are credible references.

Then present untouched Twitch TEST as confirmatory evidence:

- exact budget `K=6,650`;
- Base NDCG@10 `0.58211`;
- Difficulty exact-K `0.58340`;
- Selective Utility `0.58983`;
- Selective−Base `+0.00772`, 95% CI `[+0.00641,+0.00903]`;
- Utility−Difficulty `+0.00644`, 95% CI `[+0.00528,+0.00762]`;
- event-level utility Spearman `~0.173`;
- same-budget Oracle gain captured `~11.7%`.

Interpretation:

> **The frozen test confirms that useful specialist escalation requires informative relative-utility ranking rather than precise event-level calibration. The large Oracle gap is a limitation and a concrete future direction for better utility estimation.**

Efficiency evidence belongs here or in a dedicated short subsection: accuracy–latency–invocation/footprint frontier, formal complexity, throughput, peak memory/model size, and selector efficiency.

---

# 10. Main tables and figures

Keep the main paper visually economical and mechanism-centered.

## Figure 1 — Conditional knowledge-specialist framework

Show:

`Strong finite-context Base` + `Persistent relationship-memory specialist` + `relative-utility estimator` → specialist invocation decision.

Explicitly separate:

- observable online gate features;
- analysis-only relationship visibility / context-distance diagnostics.

## Table 1 — Strong-base context and regime dependence

Compact same-protocol Base comparisons + KuaiLive sampled/full/temporal regime results.

Purpose: establish a credible Base and the regime-dependent paradox, not a leaderboard.

## Figure 2 — Core mechanism figure (central figure of the paper)

### Panel A — Relationship knowledge states

Visualize recent-visible / long-horizon-only / unseen with:

- whether Base sees relationship;
- whether Memory has persistent relationship knowledge;
- DEV and untouched TEST Memory−Base estimates;
- semantic labels: **redundant**, **complementary**, **unavailable**.

### Panel B — Context distance and recency

Plot 1–4 / 5–8 / 9–16 / 17–32 / 33–64 / 65+ / unseen with CIs.

Mark:

- 16-step Base context boundary;
- ultra-recent 1–4 positive pocket;
- outside-context positive region.

This figure should visually falsify the simplistic “farther is always better” interpretation.

## Table 2 — Mechanism attribution and robustness

Compact rows for:

- Long-only / Short-only / Popularity-only by relationship state;
- Memory-parameter sign stability;
- selected finite-context diagnostic statistics.

Detailed matrices go to Appendix.

## Table 3 — Relative Utility vs Difficulty

KuaiLive first, frozen Twitch confirmation second.

Report exact budgets, Selective−Base, Utility−Difficulty, and Oracle headroom.

## Figure 3 — Selection composition

Utility vs Difficulty invocation composition by relationship regime.

Main visual message: Difficulty spends more budget on hard-but-unseen events; Utility better concentrates specialist calls where relationship knowledge is recoverable.

## Figure/Table 4 — Accuracy–cost frontier

Accuracy, invocation rate, selector latency, end-to-end latency, throughput, and footprint for HGB and lighter selectors.

Do not turn this into a separate algorithmic contribution.

## Appendix

Include:

- all H@10 results and CIs;
- full component/sensitivity matrices;
- complete seed-by-seed results;
- strong-base benchmark implementation details;
- complexity derivations;
- freeze-chain hashes;
- CPU/GPU audit;
- KuaiLive benchmark recovery provenance;
- complete P1 chronology;
- exact definitions of all analysis-only relationship labels.

---

# 11. Discussion priorities

1. **What counts as knowledge.** The paper studies explicit persistent user–creator relationship information, not generic “memory” and not LLM memory.

2. **Complementarity rather than accumulation.** More historical information is not automatically better. Its value depends on whether it adds information unavailable to the Base in the current decision context.

3. **Redundancy, complementarity, unavailability.** These three states provide a more useful interpretation than “short term versus long term” alone.

4. **Recency prevents a monotonic horizon story.** The 1–4 pocket is scientifically important because it shows that the outside-context mechanism is dominant but not the only positive regime.

5. **Why Difficulty is insufficient.** A hard case may provide no specialist-recoverable relationship information; decision targets must be specialist-relative.

6. **Why routing is not the novelty.** Gating and expert selection are established ideas. The contribution is the specialist-relative knowledge-utility formulation, mechanism evidence, and frozen validation.

7. **Strong Base interpretation.** Same-protocol comparator checks establish that the Base is credible; they do not establish state-of-the-art superiority.

8. **What the untouched test proves.** It confirms the frozen conditional-specialist principle and mechanism sign structure under a second live-stream setting; it does not establish unrestricted cross-domain generalization.

9. **What remains unsolved.** Pointwise utility prediction is modest and only ~11.7% of same-budget Oracle gain is captured, leaving substantial utility-estimation headroom.

10. **External validity.** Two live-stream platforms, offline predictive ranking utility, no causal GMV/conversion/satisfaction claim.

---

# 12. Claim guardrails

Do **not** claim:

- relationship Memory is globally superior or globally inferior independent of regime;
- generic routing, gating, MoE, or Learning-to-Defer is novel;
- the HGB selector is the methodological novelty;
- “long-term preference modeling” itself is novel;
- Memory utility increases monotonically with relationship distance;
- `16` is a universal relationship-memory boundary;
- Long-only is a globally superior recommender;
- relationship-horizon or context-distance labels are available as online gate features;
- Confidence alone identifies memory-solvable cases;
- generic Difficulty identifies specialist-solvable cases;
- event-level utility is well calibrated or near Oracle;
- three training seeds establish seed invariance;
- strong-base competitiveness is a SOTA/leaderboard result;
- current Memory is an LLM/agentic recommender;
- P1.3 was tuned after test access;
- causal business lift;
- cross-platform generalization beyond the evaluated live-stream settings;
- a universal law of “knowledge complementarity” beyond the tested design.

Preferred overarching sentence:

> **Relationship memory is a regime-dependent knowledge specialist: its incremental value depends on whether persistent relationship information is redundant with, complementary to, or unavailable beyond a strong finite-context sequential representation, with recency introducing an additional ultra-recent regime; estimating specialist-minus-base utility can exploit this heterogeneity more effectively than generic hard-case routing.**

Preferred conservative mechanism sentence:

> **Across the evaluated LiveRec/Twitch setting, the dominant positive Memory regime occurs when a previously observed relationship lies outside the Base’s finite visible context, while recent-visible and unseen relationships are negative in aggregate; distance analysis further identifies a separate ultra-recent positive pocket.**

Preferred decision sentence:

> **The results support specialist-relative utility as a decision target: a weak Base prediction is not sufficient evidence that a relationship specialist possesses complementary knowledge.**

---

# 13. Abstract blueprint

A future abstract should contain five moves in this order:

1. **Problem:** explicit persistent relationship knowledge can be useful but is partly redundant with strong sequential models and can be harmful when no recoverable relationship exists.
2. **Formulation:** define specialist-minus-base ranking utility and selective invocation.
3. **Mechanism:** show relationship visibility × recency structure, including outside-context complementarity and the ultra-recent pocket.
4. **Validation:** multi-regime KuaiLive + frozen untouched Twitch/LiveRec confirmation against strong Bases and same-budget Difficulty.
5. **Boundary:** useful selective ranking despite modest pointwise correlation, with substantial Oracle headroom remaining.

Avoid leading the abstract with HGB, Memory weights, “agent,” or an architecture inventory.

---

# 14. Introduction contribution paragraph blueprint

Recommended contribution order in the eventual manuscript:

1. **We formulate relationship Memory as a conditional knowledge specialist** and define specialist-minus-base ranking utility as the decision quantity of interest.
2. **We identify and validate a relationship-visibility × recency knowledge-complementarity mechanism:** persistent relationship information is strongly useful when known to Memory but outside the Base’s visible context, largely redundant/harmful in much of the visible region, and unavailable for unseen relationships; an ultra-recent positive pocket rules out a monotonic horizon explanation.
3. **We show that predicting specialist-relative utility is more decision-relevant than predicting generic Base difficulty**, under exact matched invocation budgets and across independent Base training seeds.
4. **We validate the principle across candidate/temporal regimes and a frozen second-platform one-shot test**, and quantify the resulting accuracy–invocation–latency/footprint trade-off and remaining Oracle headroom.

---

# 15. KBS-oriented external literature/positioning scan used for this restructuring

This section is **provenance for the outline restructuring**, not intended to be copied verbatim into the manuscript and not a substitute for the final Related Work search.

## KBS official scope

The current KBS description explicitly includes machine-learning methodology/algorithms, knowledge representation/engineering, recommender systems and e-service personalization, and intelligent decision/prediction systems, while emphasizing both theory and practical study. This supports foregrounding the paper as a knowledge-specialist prediction/decision framework rather than as a domain-only application.

## Recent KBS examples relevant to novelty boundaries

- **Xie et al., 2026, “Fusing multi-head gating and focused-view contrastive learning for knowledge-aware recommendation,” KBS 341, Article 115673, DOI `10.1016/j.knosys.2026.115673`.** Uses multi-head adaptive gating and explicitly distinguishes long-term interests and short-term preferences. Implication: generic gating and long/short modeling should not be framed as this paper’s novelty.

- **Huo et al., 2026, “A multi-level contrastive learning framework with reliability estimation for multimodal recommendation,” KBS 348, Article 116352, DOI `10.1016/j.knosys.2026.116352`.** Explicitly models heterogeneous reliability at content/interaction levels. Implication: KBS accepts heterogeneity-aware recommendation framing, but the present paper should differentiate itself through specialist-relative knowledge complementarity rather than generic uncertainty/reliability.

- **Zhu et al., 2026, “Beyond feature concatenation: Mutual information-driven fusion for multimodal sequential recommendation,” KBS 341, Article 115778, DOI `10.1016/j.knosys.2026.115778`.** Frames multimodal sequential recommendation around complementary cues and redundancy suppression. Implication: the present paper should make clear that its complementarity is between an explicit persistent relationship knowledge specialist and a strong finite-context Base at the event-decision level, not merely representation fusion.

- **Yue et al., 2026, “Collaborative knowledge and personalized preference alignment for sequential recommendation,” KBS 347, Article 116234, DOI `10.1016/j.knosys.2026.116234`.** Integrates external/collaborative knowledge with sequential preference modeling. Implication: “adding external knowledge to sequential recommendation” is too broad a novelty claim; the conditional availability/complementarity mechanism is the more defensible distinction.

- **Kim et al., 2026, “Leveraging graph path evidence for explainable recommender systems,” KBS 347, Article 116236, DOI `10.1016/j.knosys.2026.116236`.** Uses explicit relational evidence for explainable recommendation. Implication: this paper should describe its interpretability as **mechanistic interpretation of specialist knowledge utility**, not user-facing explanation generation.

## Positioning conclusion from the scan

The literature scan strengthens the case for the following novelty boundary:

> **Do not sell gating, long/short preference modeling, external knowledge integration, or explanation in isolation. Sell a specialist-relative knowledge-utility formulation backed by a frozen, cross-platform mechanism showing when persistent relationship knowledge is complementary, redundant, or unavailable relative to a strong finite-context sequential Base.**

A full submission-ready Related Work section should still conduct a broader systematic search covering Learning-to-Defer/selective prediction, MoE/expert routing, sequential recommendation with long-term memory, repeat-aware recommendation, and knowledge-source complementarity outside KBS.

---

# 16. Manuscript readiness and next actions

The core experiment chain is already CLOSED. This restructuring does **not** justify changing the frozen Twitch Memory, gate family/features, threshold, state transforms, or policies using P1.3 outcomes.

Priority order from this snapshot:

1. manuscript writing using the reordered contribution logic **formulation → mechanism → decision → validation**;
2. construct Figure 2 as the central mechanism figure before drafting the Results narrative;
3. write Related Work around the stricter novelty boundary above;
4. assemble Table 2 mechanism attribution and Table 3 exact-budget Utility-vs-Difficulty evidence;
5. preserve all P1 freeze/provenance details in Appendix rather than allowing audit chronology to dominate the main narrative;
6. update README/project-facing language only after the authors decide whether this restructuring becomes authoritative.

**This file remains an independent restructuring snapshot until explicitly promoted.**
