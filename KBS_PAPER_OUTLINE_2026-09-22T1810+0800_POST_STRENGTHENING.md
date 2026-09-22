# KBS-targeted paper outline — Post-strengthening freeze

**Snapshot timestamp:** 2026-09-22 18:10 +08:00  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Target journal:** *Knowledge-Based Systems* (KBS)  
**Status:** core experiment chain CLOSED; P1.3 untouched one-shot test CLOSED/FROZEN; KBS-oriented DEV mechanism strengthening CLOSED.  
**Supersedes for current KBS writing:** `KBS_PAPER_OUTLINE_2026-09-22T1740+0800.md` while preserving it for provenance.  
**General source skeleton:** `PAPER_SKELETON_2026-09-22_POST_P1_3.md`

---

# 1. KBS positioning

KBS explicitly lists **recommender systems and E-service personalization**, machine-learning methodology, knowledge representation/engineering, prediction and decision systems, and computational intelligence among its leading topics. Its scope emphasizes a balance between theory and practical study and encourages new intelligent models, methods, systems, and software tools. Recent 2026 KBS articles continue to publish sequential-recommendation methods and work centered on complementary knowledge and preference modeling.

This paper should therefore be positioned as a **knowledge-specialist decision framework**, not as a generic live-stream application, a new backbone leaderboard, or an LLM-agent paper.

Preferred positioning:

> **Relationship memory is a regime-dependent specialist. The methodological problem is to estimate its conditional specialist-minus-base utility and invoke it only when its incremental relationship knowledge is expected to improve ranking.**

Current sources checked on 2026-09-22:

- KBS scope: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
- Recent KBS sequential recommendation example: https://www.sciencedirect.com/science/article/pii/S0950705126009603
- Additional 2026 KBS sequential recommendation examples: https://www.sciencedirect.com/science/article/pii/S0950705126005046 and https://www.sciencedirect.com/science/article/pii/S0950705126009007

---

# 2. Recommended title

## Primary

> **Learning When Relationship Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Alternative

> **Conditional Specialist Utility of Relationship Memory in Sequential Recommendation**

Use **relationship memory** rather than generic **memory** to distinguish the explicit persistent user–creator knowledge source from LLM memory, generic memory networks, or retrieval augmentation.

---

# 3. Central thesis

> **Explicit relationship memory is not globally superior to a strong sequential recommender. Its marginal predictive value is regime-dependent, becomes strongly positive when persistent relationships fall outside the base model’s finite context, and can be exploited by learning specialist-minus-base utility rather than generic case difficulty.**

The post-strengthening evidence now supports this statement at three levels:

1. **regime level:** candidate and temporal changes can alter aggregate Memory–Base ordering;
2. **mechanism level:** the long-term relationship component specifically carries the positive long-horizon effect;
3. **decision level:** state and confidence information are complementary for predicting relative specialist utility, while generic difficulty remains a weaker routing target.

---

# 4. Four principal contributions

## Contribution 1 — Conditional specialist-utility formulation

Let `B` be the strong sequential base, `M` the relationship-memory specialist, and `u_K(A,x)` event-level ranking utility:

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

For observable state `Z=z` and recommendation regime `R=r`:

\[
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

The paper reframes the question from **“Is Memory globally better?”** to **“When is its conditional incremental utility positive?”**

## Contribution 2 — Relative-utility routing rather than generic difficulty routing

Estimate `\hat\eta(z)` from user/state and base-confidence information and escalate to Memory selectively. Compare against:

- Always Base;
- Always Memory;
- same-feature / same-budget Difficulty routing;
- exact-budget Oracle headroom.

This separates **memory-solvability** from generic model difficulty.

## Contribution 3 — Relationship-horizon mechanism with component-level evidence

Memory utility changes sign across:

- `recent-visible`: the relationship is already inside the sequential context;
- `long-horizon-only`: the relationship exists in older history but falls outside the current finite context;
- `unseen`: no historical relationship exists to recover.

The new DEV-only component ablation shows that the positive long-horizon effect is specifically driven by **long-term relationship strength**, not popularity or short-term recurrence.

## Contribution 4 — Multi-regime, cross-platform, frozen held-out validation

Validate the principle across:

- KuaiLive sampled-active and full-active candidate regimes;
- strict temporal GTS regimes;
- a strong official LiveRec/Twitch base;
- a frozen one-shot untouched Twitch test.

P1.3 reproduces both selective effectiveness and the relationship-horizon sign pattern without test tuning.

---

# 5. Light decision-theoretic motivation

If Memory invocation has incremental cost `c(x)` and cost weight `lambda`, an idealized policy selects Memory when:

\[
\mathbb E[\Delta_m(X)\mid Z=z]
>
\lambda\,\mathbb E[c(X)\mid Z=z].
\]

When cost is negligible or approximately fixed, this reduces to:

\[
\mathbb E[\Delta_m(X)\mid Z=z]>0.
\]

This should be presented as a **formal motivation for selective specialist use**, not as a claim of a new general decision-theory theorem. It provides a natural bridge to the measured accuracy–invocation–latency analysis.

---

# 6. Research questions

**RQ1.** Is explicit relationship memory globally better or worse than a strong sequential/identity-aware base?  
**RQ2.** Can specialist-minus-base utility be predicted well enough to improve ranking?  
**RQ3.** Does relative-utility routing contain decision-relevant information beyond generic base difficulty?  
**RQ4.** Which candidate, temporal, and relationship-horizon regimes determine Memory utility?  
**RQ5.** Is the long-horizon effect actually carried by the long-term relationship component?  
**RQ6.** Which observable feature families support relative-utility estimation: user/state information, base confidence, or both?  
**RQ7.** Does the conditional-specialist principle transfer to a second live-stream platform with a strong domain-specific base?  
**RQ8.** What accuracy–invocation–latency trade-off follows from selector complexity and specialist use?

---

# 7. Recommended manuscript structure

## 1. Introduction

1. Live-stream recommendation combines fast-changing legal candidate availability with persistent user–creator relationships.
2. Strong sequential/identity-aware recommenders already absorb much recent behavior, so explicit relationship memory need not help globally.
3. Introduce the central paradox: **Always Memory can be worse while selective Memory is beneficial.**
4. Introduce `Delta_m` and distinguish **difficulty** from **specialist utility / memory-solvability**.
5. State the four contributions above.
6. Mention two-platform validation and the frozen one-shot external test early.
7. Avoid “agent memory” as the main framing; emphasize explicit relationship knowledge and conditional specialist use.

## 2. Related Work

### 2.1 Sequential and repeat-aware recommendation

Finite-context sequence modeling, repeated-consumption behavior, identity-aware recommendation, and strong domain baselines.

### 2.2 Long-term preference and explicit relationship knowledge

Distinguish the paper’s transparent relationship-memory signal from latent ID embeddings, knowledge graphs, LLM memory, and retrieval augmentation.

### 2.3 Adaptive routing, Learning-to-Defer, and mixture-of-experts

Acknowledge instance-wise routing as prior art. The contribution is not generic routing; it is the **specialist-minus-base utility target** and the mechanism determining when this particular knowledge specialist is complementary.

### 2.4 Recommendation under candidate and temporal regime shift

Explain why legal candidate sets and time shifts can alter observed global model ordering.

## 3. Problem Formulation

Define:

- legal active candidate set;
- Base `B` and Memory specialist `M`;
- `u_K`, `Delta_m`, and `eta(z,r)`;
- generic base difficulty as a distinct target;
- threshold routing policy;
- matched-budget controls;
- optional cost-aware decision rule.

Explicitly state that **relationship horizon is analysis-only** and is never used as an online gate feature.

## 4. Conditional Relationship-Memory Specialist Framework

### 4.1 Strong sequential bases

- KuaiLive: streamer-heavy Dual-ID sequential base;
- Twitch: frozen official LiveRec availability-aware/repeat-aware base.

### 4.2 Explicit relationship-memory specialist

Frozen transferred score:

\[
0.45\,Short + 0.45\,Long + 0.10\,Popularity.
\]

Clarify components:

- Short: last-10 relationship recurrence with exponential distance decay;
- Long: strict pre-target creator count normalized by the user’s maximum creator count;
- Popularity: train-only streamer popularity.

### 4.3 Relative-utility estimator

Frozen HGB scientific gate using:

- state features;
- base-confidence features.

### 4.4 Matched-budget Difficulty and Oracle

Difficulty uses the same observable feature family and model family but predicts `1−Base NDCG@10`. Oracle ranks by realized `Delta_m` and is analysis-only.

### 4.5 Serving cost

Total serving cost includes selector overhead and specialist invocation; invocation rate alone is not a compute proxy.

## 5. Experimental Design

### 5.1 Datasets and strong-base protocols

KuaiLive and Twitch/LiveRec.

### 5.2 Candidate regimes

Sampled-active and full-active legal candidate universes.

### 5.3 Temporal regimes

Standard leave-out and strict GTS variants.

### 5.4 External freeze protocol

P1.1 strong-base reproduction → P1.2 DEV-only Memory/gate freeze → P1.3 untouched one-shot test.

### 5.5 Metrics and inference

Primary NDCG@10, secondary H@10, paired user-level bootstrap, exact matched budgets.

### 5.6 KBS mechanism-strengthening analyses

Both analyses are **DEV-only** and were run after P1.3 was frozen; neither changes the frozen P1.3 policy or test result:

1. Memory component × relationship-horizon ablation;
2. State-only vs Confidence-only vs Full gate feature-family OOF ablation.

---

# 8. Main Result I — Global model ordering is regime-dependent

## KuaiLive sampled-active

- Dual-ID Base NDCG@10: **0.60784**
- Always Memory: **0.56589**
- Selective HGB: **0.62102**
- Selective−Base: **+0.01317**, CI ≈ **[+0.01025,+0.01607]**
- invocation: **14.25%**

Interpretation: global Memory harm does not imply zero conditional value.

## KuaiLive full-active

Average candidate universe ≈ **8,269**.

- sampled Memory−Dual ≈ **−0.04196**
- full-active Memory−Dual ≈ **+0.03367**
- native full-active Selective ≈ **0.45180**
- Selective−Dual ≈ **+0.05345**, CI **[+0.04825,+0.05884]**

Interpretation: aggregate ordering can flip under a different legal candidate universe.

## KuaiLive strict temporal GTS

GTS-Last:

- Base 0.49616
- Memory 0.57369
- Selective 0.56897
- Selective−Base +0.07282, CI [0.06239,0.08309]
- invocation 59.8%

GTS-Successive:

- Base 0.40301
- Memory 0.50368
- Selective 0.50043
- Selective−Base +0.09743, CI [0.09003,0.10506]
- invocation 74.73%

Interpretation: time shift changes both specialist prevalence and aggregate utility.

---

# 9. Main Result II — Relative utility is more decision-relevant than generic difficulty

## KuaiLive sampled-active, same 14.25% budget

- Difficulty: 0.61556, gain +0.00772
- Utility HGB: 0.62102, gain +0.01317
- Oracle: 0.68531, gain +0.07746
- Utility−Difficulty: **+0.00546**, CI **[+0.00266,+0.00846]**

## KuaiLive full-active

- Utility−Difficulty: **+0.01443**, CI **[+0.01094,+0.01791]**
- Utility captures ≈ **50.3%** of same-budget Oracle gain
- predicted vs realized utility Spearman ≈ **0.240**

## Twitch P1.3 untouched test, exact same budget K=6,650

| Policy | NDCG@10 |
|---|---:|
| Base | 0.58211 |
| Always Memory | 0.53980 |
| Difficulty exact-K | 0.58340 |
| **Selective Utility** | **0.58983** |
| Oracle exact-K | 0.64806 |

- Selective−Base: **+0.00772**, 95% CI **[+0.00641,+0.00903]**
- Utility−Difficulty: **+0.00644**, 95% CI **[+0.00528,+0.00762]**
- invocation: **15.04%**
- Oracle gain captured: **11.71%**

H@10:

- Base 0.75503
- Utility 0.76448
- Difficulty 0.75252
- Utility−Base +0.00945, CI [0.00776,0.01117]
- Utility−Difficulty +0.01196, CI [0.01033,0.01364]

Central statement:

> **Hard cases are not necessarily memory-solvable cases.**

---

# 10. Main Result III — Relationship horizon explains when Memory helps

## DEV → untouched TEST replication

| Relationship horizon | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| recent-visible | −0.01995 | **−0.01935** |
| **long-horizon-only** | **+0.23097** | **+0.22045** |
| unseen | −0.19562 | **−0.18215** |

P1.3 test CIs:

- recent-visible: −0.01935 [−0.02234,−0.01633]
- long-horizon-only: **+0.22045 [+0.21140,+0.23001]**
- unseen: −0.18215 [−0.18681,−0.17715]

Mechanism statement:

> **The largest complementary value of explicit relationship memory arises when a persistent relationship is known from older history but is absent from the sequential model’s finite visible context.**

Repeat/novel is less informative:

- repeat Memory−Base = −0.01475
- novel Memory−Base = −0.07392

The nominal novel group mixes positive long-horizon cases with strongly negative unseen cases.

---

# 11. Main Result IV — Component ablation identifies the source of the long-horizon effect

The KBS DEV-only strengthening workflow exactly reconstructed all 46,878 frozen P1.2 events:

- candidate-count mismatches: **0**
- history-length mismatches: **0**
- Full Memory rank mismatches: **0**
- Full Memory NDCG@10 mismatches: **0**
- Full Memory H@10 mismatches: **0**

## Long-horizon-only DEV results

| Memory component | NDCG@10 | Δ vs Base | 95% CI |
|---|---:|---:|---:|
| Popularity only | 0.07861 | −0.22340 | [−0.23230,−0.21448] |
| Short only | 0.01293 | −0.28908 | [−0.29699,−0.28092] |
| **Long only** | **0.63890** | **+0.33688** | **[+0.32767,+0.34628]** |
| Short + Long | 0.58673 | +0.28471 | [+0.27584,+0.29355] |
| Full frozen Memory | 0.53298 | +0.23097 | [+0.22177,+0.24036] |

Corresponding long-horizon H@10 changes:

- Long only: **+0.40619**
- Short + Long: **+0.40500**
- Full Memory: **+0.32387**
- Short only: −0.54533
- Popularity only: −0.44208

This gives direct component-level evidence that the long-horizon mechanism is carried by the **persistent long-term relationship signal**. Short-term recurrence and popularity cannot explain the positive effect; adding them to Long actually dilutes the long-horizon ranking gain.

## Other horizon regimes

Long-only remains non-beneficial outside the long-horizon regime:

- recent-visible ΔNDCG@10: **−0.01251**
- unseen ΔNDCG@10: **−0.22770**

Thus the component result strengthens rather than weakens the conditional-specialist interpretation: **Long is highly useful in its matching information regime, but still should not be globally activated.**

Aggregate DEV Long-only is still worse than Base:

- Long-only NDCG@10 0.52761
- Long-only−Base **−0.04424**, CI [−0.04722,−0.04130]

---

# 12. Main Result V — Gate feature families are complementary, and confidence alone is insufficient

The DEV-only feature-family experiment exactly replayed the frozen Full HGB OOF evidence:

- Full utility prediction max absolute error: **<1e−16**
- Full difficulty prediction max absolute error: **2.22e−16**
- Full utility invocation-mask mismatches: **0**
- recovered threshold: **0.004734357474290205**
- frozen K: **6,563**

Primary comparison uses the same exact K=6,563 for all families.

| Feature family | Utility Spearman | Utility NDCG@10 | Utility gain vs Base | 95% CI | Difficulty NDCG@10 | Utility−Difficulty | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| State only | 0.14791 | 0.57557 | **+0.00372** | [+0.00256,+0.00490] | 0.57035 | **+0.00522** | [+0.00408,+0.00636] |
| Confidence only | 0.09109 | 0.57346 | **+0.00160** | [+0.00048,+0.00270] | 0.57180 | **+0.00165** | [+0.00070,+0.00263] |
| **State + Confidence** | **0.18990** | **0.58023** | **+0.00838** | **[+0.00713,+0.00963]** | 0.57311 | **+0.00713** | **[+0.00602,+0.00825]** |

Interpretation:

1. **Confidence-only works, but weakly.** Relative utility is therefore not reducible to a generic uncertainty/confidence heuristic.
2. **State-only is more informative than Confidence-only**, supporting the role of interaction/history state in memory-solvability.
3. **Full State+Confidence is strongest**, indicating complementary information across the two feature families.
4. The same-family Difficulty routers are substantially weaker; State-only Difficulty even falls below Base at the fixed K.

The family-specific descriptive optimal-threshold results show the same ordering:

- State-only optimal gain: +0.00430 at 23.996% invocation;
- Confidence-only optimal gain: +0.00287 at 7.001% invocation;
- Full optimal/frozen gain: **+0.00838 at 14.000% invocation**.

This strengthens the claim that the gate learns **specialist-specific relative utility**, not simply generic hardness.

---

# 13. Main Result VI — Utility estimation identifies a useful positive tail rather than precise event-level utility

On untouched Twitch test:

- predicted vs realized utility Spearman: **0.173**
- D1–D8: negative realized Memory−Base
- D9: approximately neutral (−0.0014)
- D10: **+0.0724** realized versus ≈ +0.080 predicted

The defensible claim is **coarse relative-utility ranking / positive-tail identification**, not accurate event-level regression or calibration.

---

# 14. Accuracy–cost analysis

KuaiLive mean latency:

- Dual Base: 0.9906 ms
- cached Memory: 0.4903 ms
- HGB gate: 0.6174 ms
- Ridge gate: 0.00242 ms
- tiny MLP gate: 0.00576 ms
- Selective HGB: 2.0066 ms
- Ridge selective: 1.3872 ms
- MLP selective: 1.2719 ms

Accuracy:

- HGB 0.62102, +0.01317
- Ridge 0.62388, +0.01603, invocation 30.99%
- MLP 0.61708, +0.00923, invocation 10.37%

Interpretation: selector overhead is material; invocation prevalence alone is not a serving-cost proxy.

---

# 15. Discussion structure

## 15.1 What counts as knowledge in this paper

Relationship Memory is an explicit structured source of persistent user–creator knowledge, separate from the latent finite-context sequential representation.

## 15.2 Why Memory helps only conditionally

- recent-visible: redundancy with the Base;
- long-horizon-only: complementary persistent relationship signal;
- unseen: absent relationship evidence.

The component ablation now directly supports this interpretation.

## 15.3 Why Difficulty fails

Difficulty asks **“where is Base weak?”** Relative utility asks **“where does this particular specialist contain complementary information?”** These are not equivalent.

The feature-family ablation further shows that relative utility is not reducible to Base confidence alone.

## 15.4 Remaining Oracle headroom

Twitch test Utility captures only **11.71%** of same-budget Oracle gain. Present this as evidence for substantial future utility-estimation headroom, not as a weakness to hide.

## 15.5 Limits

- two live-stream platforms;
- offline predictive ranking utility, not causal business lift;
- relationship horizon is diagnostic, not an online input;
- transparent non-LLM Memory specialist;
- modest event-level utility correlation;
- P1.3 is permanently frozen and cannot be reused for selection/tuning;
- mechanism ablations are DEV-only and should be reported as explanatory analyses, not as new test-tuned models.

---

# 16. Recommended main tables and figures

**Figure 1 — Framework.** Strong sequential Base + explicit relationship-memory specialist + conditional relative-utility gate; distinguish observable gate features from diagnostic relationship-horizon labels.

**Table 1 — KuaiLive sampled-active main result.** Base / Memory / Utility / Difficulty / Oracle.

**Figure 2 — Regime map.** Candidate and temporal regimes with aggregate Memory−Base sign and invocation prevalence.

**Table 2 — Matched-budget conditional utility.** Utility vs Difficulty vs Oracle across KuaiLive regimes.

**Figure 3 — Relationship-horizon mechanism.** Twitch DEV→untouched TEST recent-visible / long-horizon-only / unseen effects with confidence intervals.

**Table 3 — P1.3 one-shot external validation.** Base / Memory / Utility / Difficulty / Oracle; NDCG@10, H@10, invocation and paired CIs.

**Figure 4 — Why Utility beats Difficulty.** Selected-event relationship-horizon composition.

**Table 4 — Component-level mechanism.** Popularity / Short / Long / Short+Long / Full Memory by relationship horizon. Make the long-horizon Long-only row visually central.

**Table 5 — Gate information ablation.** State-only / Confidence-only / Full at exact K=6,563, including Utility and same-family Difficulty.

**Figure 5 — Positive-tail identification.** Frozen utility strata vs realized Memory−Base on DEV and TEST.

**Figure/Table 6 — Accuracy–invocation–latency frontier.** HGB / Ridge / tiny MLP.

**Appendix.** Identity controls, full-active details, strict temporal details, P1 freeze chain, one-shot audit hashes, CPU/GPU compatibility audit, full component H@10 table, hyperparameters, secondary robustness.

---

# 17. Claim guardrails

Do **not** claim:

- Memory is globally inferior or superior independent of regime;
- generic routing/deferral is novel;
- relationship horizon is available to the online gate;
- high pointwise utility prediction accuracy;
- near-Oracle performance;
- LLM/agentic Memory;
- causal GMV/conversion/satisfaction lift;
- generalization beyond the two evaluated live-stream settings;
- that the DEV-only strengthening analyses changed or optimized P1.3;
- that Full is statistically superior to each feature-family ablation unless a direct paired family-vs-family comparison is explicitly reported.

Preferred abstract-level claim:

> **Across two public live-stream settings, explicit relationship memory exhibits strongly heterogeneous marginal utility. A relative-utility gate improves strong sequential recommendation while outperforming same-budget difficulty routing. Held-out analysis localizes the largest complementary value to previously observed relationships outside the base model’s finite context, while DEV-only component ablation identifies the long-term relationship signal as the source of this effect and feature-family ablation shows that state and confidence information are complementary for utility estimation.**

---

# 18. Submission readiness

- **Core KuaiLive evidence:** CLOSED.
- **P1.1 LiveRec strong base:** CLOSED/FROZEN.
- **P1.2 Twitch DEV policy/mechanism:** CLOSED/FROZEN.
- **P1.3 untouched one-shot test:** CLOSED/FROZEN; `primary_success=true`, `mechanism_replication=true`.
- **KBS Experiment A — component × horizon:** CLOSED, exact frozen Full-Memory reconstruction passed.
- **KBS Experiment B — gate feature families:** CLOSED, exact frozen Full-OOF replay passed.

The empirical program required for the current KBS submission is now **CLOSED**. Further work should prioritize manuscript writing, figures/tables, literature positioning, and reproducibility packaging rather than additional model/data-set expansion.
