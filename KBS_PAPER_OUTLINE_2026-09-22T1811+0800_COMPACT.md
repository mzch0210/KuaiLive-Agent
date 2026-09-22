# KBS-targeted paper outline — compact manuscript guidance

**Snapshot date:** 2026-09-22  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Status:** core experiment chain CLOSED; P1.3 untouched one-shot test CLOSED/FROZEN; KBS mechanism-strengthening evidence available; additional journal-oriented robustness checks in progress.  
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

> **Explicit relationship memory is not globally superior to a strong sequential recommender. Its marginal predictive value changes across recommendation regimes, becomes strongly positive when persistent relationships fall outside the base model’s finite context, and can be exploited by learning specialist-minus-base utility rather than generic case difficulty.**

Evidence is organized at three levels:

1. **regime:** candidate and temporal changes alter aggregate Memory–Base ordering;
2. **mechanism:** positive long-horizon utility is specifically carried by persistent long-term relationship information;
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

## Contribution 3 — Relationship-horizon mechanism

Show that Memory utility changes sign across recent-visible, long-horizon-only, and unseen relationships. Component evidence attributes the positive long-horizon effect to persistent long-term relationship strength rather than popularity or short-term recurrence.

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
**RQ3 — Mechanism.** Does relationship horizon explain Memory complementarity, and is the positive long-horizon effect carried by the long-term relationship component?  
**RQ4 — Transfer.** Do selective effectiveness and the relationship-horizon mechanism reproduce on a second live-stream platform with a strong domain-specific base and untouched held-out evaluation?  
**RQ5 — Deployment.** What can be predicted from observable state/confidence, how much Oracle headroom remains, and what accuracy–invocation–latency trade-off follows from specialist use?

Feature-family ablations belong under RQ2/RQ5; component ablations belong under RQ3 rather than being separate research questions.

---

# 7. Recommended manuscript structure

## 1. Introduction

- Motivate the tension between rapidly changing live candidates and persistent user–creator relationships.
- Establish why a strong sequential/identity-aware base is necessary before attributing value to explicit Memory.
- Introduce the central paradox: **Always Memory can be worse while selective Memory is useful.**
- Define specialist-minus-base utility and distinguish it from generic difficulty.
- State the four contributions and mention the frozen cross-platform validation.

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

Define legal candidates, Base `B`, Memory specialist `M`, `u_K`, `Delta_m`, `eta(z,r)`, Difficulty as a separate target, matched-budget controls, and the cost-aware routing rule. Relationship horizon is **analysis-only** and is never used as an online gate feature.

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
KuaiLive and Twitch/LiveRec, with a compact competitiveness benchmark used to show that the chosen Base is not a weak reference point.

### 5.2 Candidate and temporal regimes
Sampled-active, full-active, standard temporal split, and strict temporal variants.

### 5.3 Frozen external protocol
Summarize the dev-freeze → untouched-test principle in the main text; detailed P1.1/P1.2/P1.3 audit chronology belongs in the Appendix/reproducibility section.

### 5.4 Metrics and inference
Primary NDCG@10, secondary H@10, paired user-level bootstrap, exact matched budgets.

### 5.5 Robustness and mechanism checks
Keep the main text focused on purpose rather than execution detail:

- component × relationship-horizon ablation;
- state/confidence feature-family ablation;
- Memory-parameter sensitivity without retuning the frozen test policy;
- context-window stress test of the finite-context mechanism;
- training-seed robustness;
- formal complexity and empirical efficiency analysis.

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

Use matched-budget comparisons as the main evidence.

- KuaiLive Utility−Difficulty: about `+0.00546` sampled-active and `+0.01443` full-active.
- Untouched Twitch test at exact same budget `K=6,650`: Base `0.58211`, Difficulty `0.58340`, Selective Utility `0.58983`.
- Selective−Base `+0.00772`, 95% CI `[+0.00641,+0.00903]`.
- Utility−Difficulty `+0.00644`, 95% CI `[+0.00528,+0.00762]`.

Central statement:

> **Hard cases are not necessarily memory-solvable cases.**

Feature-family evidence belongs here as a mechanism check: State+Confidence is stronger than either family alone, and Confidence-only is clearly weaker, so relative utility is not reducible to base uncertainty.

## Finding 3 — Relationship horizon explains complementarity

DEV → untouched TEST replication:

| Relationship horizon | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| recent-visible | −0.01995 | −0.01935 |
| **long-horizon-only** | **+0.23097** | **+0.22045** |
| unseen | −0.19562 | −0.18215 |

Mechanism statement:

> **The largest complementary value of explicit relationship memory arises when a persistent relationship is known from older history but is absent from the sequential model’s finite visible context.**

Component evidence sharpens this explanation: on long-horizon-only DEV events, Long-only yields `ΔNDCG@10 = +0.33688`, while Short-only and Popularity-only are negative; Long-only remains negative outside its matching information regime.

The context-window stress test should be used as a direct robustness test of this finite-context explanation, not as a new model-selection exercise.

## Finding 4 — Useful utility ranking is possible, but substantial deployment headroom remains

Combine the feature-family ablation, utility strata, Oracle gap, seed robustness, and efficiency evidence.

- State-only exact-budget gain vs Base: `+0.00372`;
- Confidence-only: `+0.00160`;
- State+Confidence: `+0.00838`.
- Untouched-test event-level Spearman is modest (`~0.173`), but the frozen top utility stratum has strongly positive realized utility.
- The current Twitch router captures only about `11.7%` of same-budget Oracle gain.

Defensible statement:

> **Useful specialist escalation requires sufficiently informative relative-utility ranking, not precise event-level calibration.**

Efficiency should be reported as a compact accuracy–latency–invocation/footprint frontier, with complexity and p50/p95/throughput details in the table or Appendix.

---

# 9. Main tables and figures

Keep the main paper visually economical:

- **Figure 1:** strong Base + explicit relationship-memory specialist + relative-utility router and cost-aware decision rule.
- **Table 1:** strong-base context plus KuaiLive regime results.
- **Table 2:** matched-budget Utility vs Difficulty results on KuaiLive and Twitch.
- **Figure 2:** relationship-horizon sign reversal with DEV and untouched TEST estimates; optionally overlay the context-window stress-test trend.
- **Table 3:** compact mechanism/robustness evidence: component ablation, feature-family ablation, parameter/seed stability headline results.
- **Figure 3:** Utility vs Difficulty selection composition by relationship horizon.
- **Figure/Table 4:** accuracy–latency–invocation/footprint frontier.
- **Appendix:** complete component/sensitivity matrices, H@10, all CIs, baseline implementation details, seed-by-seed results, complexity derivations, freeze-chain hashes, CPU/GPU audit, and full P1 chronology.

---

# 10. Discussion priorities

1. **What counts as knowledge:** explicit persistent user–creator relationship information, separate from finite-context latent sequence representation.
2. **Why Memory helps conditionally:** redundancy for recent-visible, complementarity for long-horizon-only, absence of recoverable signal for unseen.
3. **Why Difficulty is insufficient:** Base weakness is not equivalent to availability of complementary specialist information.
4. **What remains unsolved:** modest event-level utility correlation and large Oracle headroom motivate better utility estimation rather than a claim of near-optimal routing.
5. **External validity boundary:** two live-stream platforms, offline predictive ranking utility, no causal business-lift claim.

---

# 11. Claim guardrails

Do not claim:

- Memory is globally superior or inferior independent of regime;
- Long-only is a globally superior recommender;
- generic routing/gating/deferral is novel;
- feature-fusion gating and specialist invocation are the same problem;
- generic Difficulty identifies memory-solvable events;
- event-level utility is well calibrated or close to Oracle;
- current Memory is an LLM/agentic recommender;
- causal GMV/conversion/satisfaction lift;
- relationship horizon is available as an online routing feature;
- P1.3 was tuned after test access;
- cross-platform generalization beyond the evaluated live-stream settings.

Preferred overarching sentence:

> **Relationship memory is a regime-dependent knowledge specialist: its aggregate value changes with the recommendation regime, while conditional specialist-minus-base utility identifies when persistent relationship information is complementary to a strong finite-context sequential recommender.**
