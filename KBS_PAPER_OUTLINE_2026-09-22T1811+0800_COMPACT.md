# KBS-targeted paper outline — compact post-strengthening version

**Snapshot timestamp:** 2026-09-22 18:11 +08:00  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Status:** core experiment chain CLOSED; P1.3 untouched one-shot test CLOSED/FROZEN; KBS-oriented DEV mechanism strengthening CLOSED.  
**Supersedes for current KBS writing:** `KBS_PAPER_OUTLINE_2026-09-22T1810+0800_POST_STRENGTHENING.md` for manuscript planning, while preserving that file as a detailed evidence snapshot.  
**General source skeleton:** `PAPER_SKELETON_2026-09-22_POST_P1_3.md`

---

# 1. KBS positioning

KBS explicitly covers recommender systems and E-service personalization, machine-learning methodology, knowledge representation/engineering, prediction and decision systems, and computational intelligence. The manuscript should therefore be positioned as a **conditional knowledge-specialist decision framework**, not as a generic live-stream application, a new sequential backbone, or an LLM-agent paper.

Preferred positioning:

> **Relationship memory is a regime-dependent specialist. The methodological problem is to estimate its incremental specialist-minus-base utility and invoke it only when its persistent relationship knowledge is expected to improve ranking.**

Current KBS sources checked on 2026-09-22:

- KBS scope: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
- Recent KBS sequential-recommendation example: https://www.sciencedirect.com/science/article/pii/S0950705126009603

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

The evidence supports this at three levels:

1. **regime level:** candidate and temporal changes can alter aggregate Memory–Base ordering;
2. **mechanism level:** positive long-horizon utility is specifically carried by the long-term relationship component;
3. **decision level:** user/state and base-confidence information are complementary for identifying memory-solvable events.

---

# 4. Four principal contributions

## Contribution 1 — Conditional specialist-utility formulation

Let `B` be the strong sequential base, `M` the relationship-memory specialist, and `u_K(A,x)` event-level ranking utility:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

For observable state `Z=z` and regime `R=r`:

\[
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The paper reframes the question from **“Is Memory globally better?”** to **“When is its incremental utility positive?”**

## Contribution 2 — Relative-utility routing rather than generic difficulty routing

Estimate `\hat\eta(z)` from user/state and base-confidence features and invoke Memory selectively. Compare against Always Base, Always Memory, same-budget Difficulty routing, and exact-budget Oracle headroom.

## Contribution 3 — Relationship-horizon mechanism with component evidence

Memory utility changes sign across recent-visible, long-horizon-only, and unseen relationships. A DEV-only component ablation shows that the positive long-horizon effect is specifically attributable to the **long-term relationship signal**, rather than popularity or short-term recurrence.

## Contribution 4 — Multi-regime, cross-platform, frozen held-out validation

Validate the principle across KuaiLive candidate and temporal regimes and a strong official LiveRec/Twitch base, culminating in a frozen one-shot untouched Twitch test.

---

# 5. Light decision-theoretic motivation

If specialist invocation has incremental cost `c(x)` and cost weight `lambda`, an idealized policy selects Memory when:

\[
\mathbb E[\Delta_m(X)\mid Z=z] > \lambda\,\mathbb E[c(X)\mid Z=z].
\]

With negligible or approximately fixed incremental cost, this reduces to:

\[
\mathbb E[\Delta_m(X)\mid Z=z]>0.
\]

Present this as formal motivation, not as a new general theorem. It links the utility formulation to the measured accuracy–invocation–latency trade-off.

---

# 6. Research questions

**RQ1.** Is explicit relationship memory globally better or worse than a strong sequential/identity-aware base?  
**RQ2.** Can specialist-minus-base utility be predicted well enough to improve ranking?  
**RQ3.** Does relative-utility routing contain decision-relevant information beyond generic base difficulty?  
**RQ4.** Which candidate, temporal, and relationship-horizon regimes determine Memory utility?  
**RQ5.** Is the long-horizon effect specifically carried by the long-term relationship component?  
**RQ6.** Do user/state and base-confidence feature families provide complementary information for relative-utility estimation?  
**RQ7.** Does the conditional-specialist principle transfer to a second live-stream platform with a strong domain-specific base?  
**RQ8.** What accuracy–invocation–latency trade-off follows from selector complexity and specialist use?

---

# 7. Recommended manuscript structure

## 1. Introduction

- Motivate the tension between rapidly changing live candidates and persistent user–creator relationships.
- Establish why a strong sequential/identity-aware base is necessary before attributing value to explicit Memory.
- Introduce the central paradox: **Always Memory can be worse while selective Memory is useful.**
- Define specialist-minus-base utility and distinguish it from generic difficulty.
- State the four contributions and mention two-platform frozen validation.

## 2. Related Work

### 2.1 Sequential and repeat-aware recommendation
### 2.2 Long-term preference and explicit relationship knowledge
### 2.3 Adaptive routing, Learning-to-Defer, and mixture-of-experts
### 2.4 Recommendation under candidate and temporal regime shift

The novelty claim should remain in the **utility target and specialist mechanism**, not generic routing.

## 3. Problem Formulation

Define legal candidates, Base `B`, Memory specialist `M`, `u_K`, `Delta_m`, `eta(z,r)`, generic difficulty, the selective policy, matched-budget controls, and the optional cost-aware decision rule.

Explicitly state that **relationship horizon is analysis-only** and is never used as an online gate feature.

## 4. Conditional Relationship-Memory Specialist Framework

### 4.1 Strong sequential bases
- KuaiLive Dual-ID sequential base.
- Frozen official LiveRec availability-aware/repeat-aware base.

### 4.2 Explicit relationship-memory specialist
Frozen transferred score:

\[
0.45\,Short + 0.45\,Long + 0.10\,Popularity.
\]

### 4.3 Relative-utility estimator
Frozen HGB scientific gate using state + base-confidence features.

### 4.4 Matched-budget Difficulty and Oracle
Difficulty predicts base error with the same observable feature family/model family; Oracle uses realized `Delta_m` only for headroom analysis.

### 4.5 Serving cost
Total cost includes both selector overhead and specialist invocation.

## 5. Experimental Design

### 5.1 Datasets and strong-base protocols
KuaiLive and Twitch/LiveRec.

### 5.2 Candidate and temporal regimes
Sampled-active, full-active, standard temporal split, and strict GTS variants.

### 5.3 External freeze protocol
P1.1 strong-base reproduction → P1.2 DEV-only Memory/gate freeze → P1.3 untouched one-shot test.

### 5.4 Metrics and inference
Primary NDCG@10, secondary H@10, paired user-level bootstrap, exact matched budgets.

### 5.5 DEV-only KBS mechanism analyses
Two post-freeze explanatory analyses that do **not** modify P1.3:

1. Memory component × relationship horizon;
2. State-only vs Confidence-only vs Full feature-family OOF ablation.

---

# 8. Main Result I — Global model ordering is regime-dependent

Use one compact table/figure to establish the regime-level result.

### KuaiLive sampled-active
- Base NDCG@10: **0.60784**
- Always Memory: **0.56589**
- Selective: **0.62102**
- Selective−Base: **+0.01317**

### KuaiLive full-active
- sampled Memory−Base ≈ **−0.04196**
- full-active Memory−Base ≈ **+0.03367**
- native Selective−Base ≈ **+0.05345**

### Strict temporal GTS
- GTS-Last Selective−Base: **+0.07282**
- GTS-Successive Selective−Base: **+0.09743**

**Main interpretation:** aggregate Memory ordering is a property of the evaluation regime, not a fixed property of the specialist.

Detailed CIs and invocation rates belong in the result table rather than the outline text.

---

# 9. Main Result II — Relative utility is more decision-relevant than generic difficulty

Use matched-budget comparisons as the principal evidence.

### KuaiLive
- sampled-active Utility−Difficulty: **+0.00546**
- full-active Utility−Difficulty: **+0.01443**

### Twitch untouched P1.3 test, exact same budget `K=6,650`

| Policy | NDCG@10 |
|---|---:|
| Base | 0.58211 |
| Always Memory | 0.53980 |
| Difficulty exact-K | 0.58340 |
| **Selective Utility** | **0.58983** |
| Oracle exact-K | 0.64806 |

Primary effects:

- Selective−Base: **+0.00772**, 95% CI **[+0.00641,+0.00903]**
- Utility−Difficulty: **+0.00644**, 95% CI **[+0.00528,+0.00762]**

Central statement:

> **Hard cases are not necessarily memory-solvable cases.**

Keep H@10 and Oracle-capture details in the main result table or Appendix rather than repeating them in the outline.

---

# 10. Main Result III — Relationship horizon explains when Memory helps

DEV → untouched TEST replication:

| Relationship horizon | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| recent-visible | −0.01995 | **−0.01935** |
| **long-horizon-only** | **+0.23097** | **+0.22045** |
| unseen | −0.19562 | **−0.18215** |

Mechanism statement:

> **The largest complementary value of explicit relationship memory arises when a persistent relationship is known from older history but is absent from the sequential model’s finite visible context.**

Use repeat/novel only as a secondary comparison showing that the conventional split masks the positive long-horizon and negative unseen regimes.

---

# 11. Main Result IV — The long-term relationship component drives the long-horizon effect

This section should stay concise and answer one reviewer-facing question: **what actually causes the long-horizon gain?**

DEV-only component ablation on long-horizon-only events:

- **Long only:** `ΔNDCG@10 = +0.33688`, 95% CI `[+0.32767,+0.34628]`;
- Full frozen Memory: `+0.23097`;
- Short only and Popularity only are strongly negative.

Crucially, Long-only remains negative on recent-visible and unseen events. Therefore the result is not “Long is a better global recommender”; it is:

> **Persistent long-term relationship strength is highly useful only in the matching information regime where that relationship exists outside the base model’s finite context.**

**Placement rule:** put the full five-component × three-horizon matrix, H@10 values, reconstruction guards, and all secondary CIs in the detailed Results table / Appendix, not in the narrative outline.

---

# 12. Main Result V — State and confidence are complementary for relative-utility estimation

This section should answer whether the Utility gate is merely a disguised base-confidence heuristic.

Under the same exact DEV budget `K=6,563`:

| Features | Utility gain vs Base | Utility−Difficulty |
|---|---:|---:|
| State only | **+0.00372** | **+0.00522** |
| Confidence only | **+0.00160** | **+0.00165** |
| **State + Confidence** | **+0.00838** | **+0.00713** |

The full feature set is strongest, while Confidence-only is clearly weaker. This supports two claims:

1. relative specialist utility is **not reducible to generic base uncertainty**;
2. user/history state and base confidence provide complementary decision information.

**Placement rule:** keep Spearman values, family-specific optimal thresholds, exact replay tolerances, and invocation-mask guards in the detailed Results/Appendix. They are validation details rather than headline contributions.

---

# 13. Main Result VI — Utility estimation identifies a useful positive tail, not precise event-level utility

On untouched Twitch test, predicted vs realized utility Spearman is only about **0.173**. However, frozen utility strata remain directionally ordered and the top stratum has strongly positive realized utility.

Defensible statement:

> **Useful specialist escalation requires sufficiently informative relative-utility ranking, not accurate event-level calibration.**

Do not claim precise per-event utility prediction.

---

# 14. Accuracy–cost analysis

Use a compact frontier figure/table rather than listing every timing number in the narrative.

Core message:

- HGB is the frozen scientific selector;
- Ridge/tiny-MLP substantially reduce gate overhead;
- invocation rate alone does not determine total serving cost.

The detailed latency/accuracy values belong in the frontier table.

---

# 15. Discussion

## 15.1 What counts as knowledge here
Relationship Memory is an explicit structured source of persistent user–creator knowledge, separate from the finite-context sequential representation.

## 15.2 Why Memory helps only conditionally
- recent-visible: redundant with Base;
- long-horizon-only: complementary persistent relationship signal;
- unseen: no relationship evidence exists.

The component ablation directly supports this explanation.

## 15.3 Why Difficulty is insufficient
Difficulty asks where the Base is weak; relative utility asks where this particular specialist contains complementary information. The feature-family ablation shows this distinction cannot be reduced to base confidence alone.

## 15.4 Remaining headroom
Twitch Selective captures only about **11.7%** of same-budget Oracle gain, motivating better utility estimation rather than a claim of near-optimal routing.

## 15.5 Limitations
- two live-stream platforms;
- offline predictive ranking utility, not causal business lift;
- relationship horizon is diagnostic, not an online gate input;
- explicit non-LLM Memory specialist;
- modest event-level utility correlation;
- post-P1.3 component/feature analyses are DEV-only explanatory analyses and cannot alter the frozen test policy.

---

# 16. Recommended main tables and figures

Keep the main paper visually economical.

- **Figure 1:** framework — strong Base + explicit relationship-memory specialist + relative-utility router.
- **Table 1:** KuaiLive regime results — sampled-active, full-active, strict temporal.
- **Table 2:** Utility vs Difficulty matched-budget results on KuaiLive and Twitch.
- **Figure 2:** relationship-horizon sign reversal with DEV and untouched TEST estimates.
- **Table 3:** compact mechanism evidence — component ablation plus feature-family ablation, showing only headline effects.
- **Figure 3:** Utility vs Difficulty selection composition by relationship horizon.
- **Figure/Table 4:** accuracy–latency–invocation frontier.
- **Appendix:** complete component matrix, H@10, all CIs, feature-family thresholds/Spearman, reconstruction guards, freeze-chain hashes, CPU/GPU audit, and secondary robustness.

---

# 17. Claim guardrails

Do not claim:

- Memory is globally superior or inferior independent of regime;
- Long-only is a globally superior recommender;
- generic routing/deferral is novel;
- Confidence-only explains specialist utility;
- event-level utility is well calibrated;
- current Memory is an LLM/agentic recommender;
- causal GMV/conversion/satisfaction lift;
- relationship horizon is available as an online routing feature;
- P1.3 was tuned after test access;
- the current router is close to Oracle.

Preferred overarching sentence:

> **Relationship memory is a regime-dependent knowledge specialist: its largest incremental value arises when persistent relationships fall outside the sequential model’s finite context, and this value can be identified more effectively by specialist-relative utility than by generic difficulty.**

---

# 18. Paper readiness

- KuaiLive internal validity / candidate / temporal evidence: **CLOSED**.
- LiveRec strong-base reproduction: **CLOSED/FROZEN**.
- P1.2 DEV Memory + utility policy: **CLOSED/FROZEN**.
- P1.3 untouched one-shot test: **CLOSED/FROZEN**.
- KBS component mechanism analysis: **CLOSED, DEV-only**.
- KBS gate feature-family analysis: **CLOSED, DEV-only**.

The empirical program is now sufficiently complete for manuscript drafting. Further experiments should be added only in response to a clearly identified journal/reviewer need, not by reopening the frozen Twitch test or expanding the benchmark mechanically.
