# KBS-targeted paper outline — compact manuscript guidance

**Snapshot date:** 2026-09-22  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Status:** core experiment chain CLOSED; P1.3 untouched one-shot test CLOSED/FROZEN; DEV-only Memory sensitivity and finite-context stress CLOSED. Strong-base competitiveness, formal complexity/efficiency, and training-seed robustness remain journal-strengthening work and must not be described as completed until closed.  
**Authoritative KBS outline:** this file.  
**General provenance skeleton:** `PAPER_SKELETON_2026-09-22_POST_P1_3.md`

---

# 1. KBS positioning

Position the manuscript as a **conditional knowledge-specialist decision framework** for recommendation, not as a generic live-stream application, a new sequential backbone, or an LLM-agent paper.

Preferred positioning:

> **Relationship memory is a regime-dependent specialist. The methodological problem is to estimate its incremental specialist-minus-base utility and invoke it only when its persistent relationship knowledge is expected to improve ranking.**

The KBS framing should emphasize: machine-learning methodology, explicit relationship knowledge, prediction/decision under heterogeneous regimes, interpretable mechanism evidence, and practical accuracy–cost trade-offs.

---

# 2. Recommended title

## Primary

> **Learning When Relationship Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Alternative

> **Conditional Specialist Utility of Relationship Memory in Sequential Recommendation**

Use **relationship memory** rather than generic **memory** to distinguish the explicit persistent user–creator knowledge source from LLM memory or generic memory networks.

---

# 3. Central thesis

> **Explicit relationship memory is not globally superior to a strong sequential recommender. Its marginal predictive value changes across recommendation regimes and is structured by relationship visibility relative to the base model’s finite context and by recency regime. The dominant complementary region occurs when a persistent relationship falls outside the visible sequential context, while a separate ultra-recent repeat pocket shows that the effect is not monotonic in distance. This conditional value can be exploited by learning specialist-minus-base utility rather than generic case difficulty.**

Evidence is organized at three levels:

1. **regime:** candidate and temporal changes alter aggregate Memory–Base ordering;
2. **mechanism:** relationship visibility and recency explain where persistent long-term relationship information is complementary rather than redundant or absent;
3. **decision:** user/history state and base-confidence information jointly help identify memory-solvable events.

---

# 4. Four principal contributions

## Contribution 1 — Conditional specialist-utility formulation

Let `B` denote the strong sequential base, `M` the relationship-memory specialist, and `u_K(A,x)` event-level ranking utility:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x),
\qquad
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The paper reframes the question from **“Is Memory globally better?”** to **“When is its incremental utility positive?”**

## Contribution 2 — Relative-utility routing rather than generic difficulty routing

Estimate `\hat\eta(z)` from observable user/state and base-confidence information and invoke Memory selectively. Compare against Always Base, Always Memory, matched-budget Difficulty routing, and exact-budget Oracle headroom.

## Contribution 3 — Relationship visibility and recency mechanism

Show that Memory utility changes sign according to whether the target relationship is visible inside the sequential context, known only from older history, or unseen. Use the DEV-only finite-context stress test to show a sharp positive shift outside the LiveRec context boundary while retaining a distinct ultra-recent positive pocket. Component evidence attributes the long-horizon effect to persistent long-term relationship strength rather than popularity or short-term recurrence.

## Contribution 4 — Multi-regime, cross-platform, frozen held-out validation

Validate the conditional-specialist principle across KuaiLive candidate/temporal regimes and a strong official LiveRec/Twitch base, culminating in an untouched one-shot external test with no post-test rescue tuning.

---

# 5. Decision-theoretic motivation

If invoking the specialist incurs incremental cost `c(x)` and cost weight `lambda`, the idealized binary decision is

\[
\pi^*(z)=\mathbf 1\left[
\mathbb E[\Delta_m(X)\mid Z=z]
>
\lambda\,\mathbb E[c(X)\mid Z=z]
\right].
\]

With negligible or approximately fixed incremental cost, this reduces to

\[
\pi^*(z)=\mathbf 1[\eta(z)>0].
\]

Treat the learned gate as a **plug-in estimator for this specialist decision problem**, not as a claim of a new general decision-theory theorem. Prediction errors matter most near the routing boundary; high event-level calibration is not required if the estimator can reliably separate a useful positive-utility tail.

---

# 6. Five research questions

**RQ1 — Regime.** How does the aggregate value of relationship memory change across candidate and temporal regimes?  
**RQ2 — Decision.** Can specialist-minus-base utility be estimated well enough to improve a strong Base, and does it contain decision-relevant information beyond generic Difficulty?  
**RQ3 — Mechanism.** Does relationship visibility relative to the Base context, together with recency regime, explain Memory complementarity, and is the positive outside-context effect carried by persistent long-term relationship information?  
**RQ4 — Transfer.** Do selective effectiveness and the visibility/recency mechanism reproduce on a second live-stream platform with a strong domain-specific base and untouched held-out evaluation?  
**RQ5 — Deployment.** What can be predicted from observable state/confidence, how much Oracle headroom remains, and what accuracy–invocation–latency trade-off follows from specialist use?

Feature-family ablations belong under RQ2/RQ5; component ablations and context-window diagnostics belong under RQ3 rather than being separate research questions.

---

# 7. Recommended manuscript structure

## 1. Introduction

- Motivate the tension between rapidly changing live candidates and persistent user–creator relationships.
- Establish why a strong sequential/identity-aware base is necessary before attributing value to explicit Memory.
- Introduce the central paradox: **Always Memory can be worse while selective Memory is useful.**
- Define specialist-minus-base utility and distinguish it from generic difficulty.
- State the four contributions and mention the frozen cross-platform validation.
- Keep the narrative order explicit: **paradox → regime reversal → incremental-utility framing → Utility vs Difficulty → finite-context/long-term mechanism → recency nuance → frozen Twitch transfer → Oracle-gap/deployment limitation.**

## 2. Related Work

### 2.1 Sequential, repeat-aware, and long-term recommendation
Cover finite-context sequence models, repeated-consumption behavior, and long-term preference/relationship modeling.

### 2.2 Explicit relationship knowledge
Distinguish the transparent relationship-memory specialist from latent ID embeddings, knowledge graphs, retrieval augmentation, and LLM memory.

### 2.3 Adaptive routing, gating, Learning-to-Defer, and mixture-of-experts
Acknowledge generic routing as prior art. Explicitly distinguish **internal feature-fusion gating** from this paper’s **event-level decision to invoke an external relationship specialist based on specialist-minus-base utility**.

### 2.4 Difficulty-aware learning and recommendation under regime shift
Distinguish generic difficulty—“where is the Base weak?”—from specialist utility—“where does this particular information source improve the Base?” Connect candidate and temporal shifts to evaluation validity.

## 3. Problem Formulation and Decision Rule

Define legal candidates, Base `B`, Memory specialist `M`, `u_K`, `Delta_m`, `eta(z,r)`, Difficulty as a separate target, matched-budget controls, and the cost-aware routing rule. Relationship horizon/context-distance diagnostics are **analysis-only** and are never used as online gate features.

## 4. Conditional Relationship-Memory Specialist Framework

### 4.1 Strong sequential bases
KuaiLive identity-aware sequential base and frozen official LiveRec availability-aware/repeat-aware base.

### 4.2 Explicit relationship-memory specialist
Frozen transferred score:

\[
0.45\,Short + 0.45\,Long + 0.10\,Popularity.
\]

### 4.3 Relative-utility estimator
Scientific HGB gate using state + base-confidence features; lighter selectors are used for deployment analysis rather than to redefine the scientific result.

### 4.4 Matched-budget controls and serving cost
Difficulty uses the same observable information/model family but predicts base error; Oracle is analysis-only. Total cost includes selector overhead and specialist invocation.

## 5. Experimental Design

### 5.1 Datasets and strong-base context
KuaiLive and Twitch/LiveRec, with a compact competitiveness benchmark used to show that the chosen Base is not a weak reference point. Treat this table as context for the scientific comparison, not as a leaderboard contribution.

### 5.2 Candidate and temporal regimes
Sampled-active, full-active, standard temporal split, and strict temporal variants.

### 5.3 Frozen external protocol
Summarize the dev-freeze → untouched-test principle in the main text; detailed P1.1/P1.2/P1.3 audit chronology belongs in the Appendix/reproducibility section.

### 5.4 Metrics and inference
Primary NDCG@10, secondary H@10, paired user-level bootstrap, exact matched budgets.

### 5.5 Robustness and mechanism checks
Keep the main text focused on purpose rather than execution detail:

- component × relationship-visibility/horizon ablation;
- state/confidence feature-family ablation;
- Memory-parameter sensitivity on DEV without retuning the frozen test policy — **closed**;
- finite-context/recency stress test on DEV — **closed**;
- training-seed robustness — **pending; do not report as completed until closed**;
- formal complexity and empirical efficiency analysis — **pending; distinguish from the already available latency/compression evidence**.

---

# 8. Four scientific findings

## Finding 1 — Global Memory ordering is regime-dependent

Use KuaiLive sampled-active, full-active, and strict-temporal evidence to establish that aggregate model ordering is not a fixed property of Memory.

Headline evidence:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active Memory−Base changes sign to approximately `+0.03367`, while native Selective−Base is about `+0.05345`;
- strict temporal Selective−Base rises to about `+0.07282` / `+0.09743`.

**Interpretation:** candidate and temporal regime changes alter both specialist prevalence and aggregate value.

## Finding 2 — Relative utility is more decision-relevant than generic difficulty

Use matched-budget comparisons as the main evidence, leading with KuaiLive and reserving the untouched Twitch result as later external confirmation after the mechanism is established.

- KuaiLive Utility−Difficulty: about `+0.00546` sampled-active and `+0.01443` full-active.
- Feature-family evidence belongs here as a mechanism check: State+Confidence is stronger than either family alone, and Confidence-only is clearly weaker, so relative utility is not reducible to base uncertainty.

Central statement:

> **Hard cases are not necessarily memory-solvable cases.**

## Finding 3 — Relationship visibility and recency explain complementarity

Establish the mechanism first on frozen DEV evidence, then show untouched TEST replication.

Relationship-horizon sign structure:

| Relationship regime | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| recent-visible | −0.01995 | −0.01935 |
| **long-horizon-only** | **+0.23097** | **+0.22045** |
| unseen | −0.19562 | −0.18215 |

Component evidence sharpens the explanation: on long-horizon-only DEV events, Long-only yields `ΔNDCG@10 = +0.33688`, while Short-only and Popularity-only are negative; Long-only remains negative outside its matching information regime.

The finite-context stress test makes the mechanism more precise. On LiveRec DEV, a 16-interaction visibility boundary almost exactly recovers the frozen horizon split: last seen within 16 interactions is negative (`−0.01980`), while last seen beyond 16 is strongly positive (`+0.23057`). However, the relationship is **not monotonic**: there is a separate positive ultra-recent repeat pocket at distance 1–4 (`+0.04606`), whereas distances 5–16 are negative.

Mechanism statement:

> **Persistent relationship Memory is most complementary when relevant relationship knowledge is outside the strong sequential Base’s visible context, but recency introduces a distinct ultra-recent repeat regime; the effect should therefore be described in terms of relationship visibility plus recency, not “farther is always better.”**

Memory-parameter sensitivity belongs here as robustness rather than model selection: reasonable perturbations preserve the recent-visible negative / long-horizon positive / unseen negative sign pattern.

## Finding 4 — Frozen transfer confirms the principle, while deployment headroom remains

After the mechanism exposition, present the untouched Twitch test as confirmatory transfer evidence rather than as another development result.

- Exact same budget `K=6,650`: Base `0.58211`, Difficulty `0.58340`, Selective Utility `0.58983`.
- Selective−Base `+0.00772`, 95% CI `[+0.00641,+0.00903]`.
- Utility−Difficulty `+0.00644`, 95% CI `[+0.00528,+0.00762]`.
- Untouched-test event-level Spearman is modest (`~0.173`), but the frozen top utility stratum has strongly positive realized utility.
- The current Twitch router captures only about `11.7%` of same-budget Oracle gain.

Defensible statement:

> **Useful specialist escalation requires sufficiently informative relative-utility ranking, not precise event-level calibration; the untouched transfer result supports the principle while the large Oracle gap leaves substantial room for better utility estimation.**

Efficiency should be reported as a compact accuracy–latency–invocation/footprint frontier. Formal complexity, throughput, peak-memory, and model-size claims should enter the manuscript only after the dedicated efficiency analysis is closed.

---

# 9. Main tables and figures

Keep the main paper visually economical:

- **Figure 1:** strong Base + explicit relationship-memory specialist + relative-utility router and cost-aware decision rule.
- **Table 1:** strong-base context plus KuaiLive regime results.
- **Table 2:** matched-budget Utility vs Difficulty results; organize the text so KuaiLive establishes the decision result before Twitch is used as frozen external confirmation.
- **Figure 2:** **dual-panel mechanism figure** — Panel A: relationship-regime sign reversal with DEV and untouched TEST estimates; Panel B: DEV context-distance stress with the 16-step boundary and the separate 1–4 ultra-recent positive pocket.
- **Table 3:** compact mechanism/robustness evidence: component ablation, feature-family ablation, and Memory-parameter stability. Add training-seed robustness only after it is actually completed.
- **Figure 3:** Utility vs Difficulty selection composition by relationship regime.
- **Figure/Table 4:** accuracy–latency–invocation/footprint frontier; add formal complexity/throughput/peak-memory/model-size fields only after the dedicated efficiency analysis closes.
- **Appendix:** complete component/sensitivity matrices, H@10, all CIs, baseline implementation details, eventual seed-by-seed results, complexity derivations, freeze-chain hashes, CPU/GPU audit, and full P1 chronology.

---

# 10. Discussion priorities

1. **What counts as knowledge:** explicit persistent user–creator relationship information, separate from finite-context latent sequence representation.
2. **Why Memory helps conditionally:** complementarity outside the visible context, redundancy/harm in much of the recent-visible region, a distinct ultra-recent repeat pocket, and absence of recoverable relationship signal for unseen cases.
3. **Why Difficulty is insufficient:** Base weakness is not equivalent to availability of complementary specialist information.
4. **What remains unsolved:** modest event-level utility correlation and large Oracle headroom motivate better utility estimation rather than a claim of near-optimal routing.
5. **External validity boundary:** two live-stream platforms, offline predictive ranking utility, no causal business-lift claim.

---

# 11. Claim guardrails

Do not claim:

- Memory is globally superior or inferior independent of regime;
- Memory utility increases monotonically with relationship distance;
- Long-only is a globally superior recommender;
- generic routing/gating/deferral is novel;
- feature-fusion gating and specialist invocation are the same problem;
- generic Difficulty identifies memory-solvable events;
- event-level utility is well calibrated or close to Oracle;
- current Memory is an LLM/agentic recommender;
- causal GMV/conversion/satisfaction lift;
- relationship horizon or context-distance diagnostics are available as online routing features;
- P1.3 was tuned after test access;
- unfinished seed/efficiency/competitiveness checks are completed evidence;
- cross-platform generalization beyond the evaluated live-stream settings.

Preferred overarching sentence:

> **Relationship memory is a regime-dependent knowledge specialist: its aggregate value changes with the recommendation regime, while conditional specialist-minus-base utility identifies when persistent relationship information is complementary to a strong finite-context sequential recommender; this complementarity is structured by relationship visibility and recency rather than by a monotonic horizon effect.**
