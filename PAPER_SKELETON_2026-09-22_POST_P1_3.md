# KuaiLive-Agent — Post-P1.3 Academic Paper Skeleton

**Snapshot date:** 2026-09-22  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Phase:** P0 closed; LiveRec P1.1 strong-base reproduction closed; P1.2 dev-only memory/utility analysis closed and frozen; P1.3 untouched one-shot test closed and frozen.  
**Supersedes for current writing:** `PAPER_SKELETON_2026-09-22_POST_P1_2.md` while preserving earlier snapshots for provenance.

---

# 1. Recommended title

## Primary

> **Learning When Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Alternative

> **When Does Memory Help? Regime-Dependent Utility of Explicit Relationship Memory in Live-Streaming Recommendation**

Avoid centering the title on generic adaptive computation, uncertainty routing, agentic recommendation, or generic memory augmentation.

---

# 2. Core thesis

> **Explicit relationship memory has no fixed global ordering relative to a strong sequential recommender. Its marginal ranking utility varies across user states, candidate universes, temporal regimes, and relationship horizons. Conditional relative-utility estimation can exploit this heterogeneity beyond fixed model choice and generic hard-case routing.**

KuaiLive establishes the candidate/temporal regime result. LiveRec/Twitch provides an independent strong-base external validation in which transferred Always Memory is globally harmful, but relationship memory is strongly useful when persistent user–streamer relationships fall outside the finite sequential context. A frozen dev-trained relative-utility router reproduces this conditional advantage on the untouched one-shot test and significantly outperforms an exact-same-budget generic difficulty router.

The paper therefore argues for **relationship memory as a regime-dependent specialist**, not as a uniformly stronger recommender.

---

# 3. Novelty boundary

The paper does **not** claim invention of generic instance-wise expert routing. The defensible contribution is the combination of:

1. an explicit **relationship-memory specialist** separated from a strong sequential/identity-aware base;
2. direct estimation of **specialist-minus-base ranking utility** rather than generic difficulty;
3. evidence that memory utility changes across candidate, temporal, and relationship-horizon regimes;
4. matched-budget evidence that relative-utility routing contains decision-relevant information beyond base difficulty;
5. a mechanism result showing that the largest positive memory utility occurs when persistent relationships are outside the sequential model's finite context, whereas recent-visible and truly unseen cases have negative incremental utility;
6. serving evidence that selector complexity and specialist invocation jointly determine cost;
7. one-shot external validation against a strong availability-aware, repeat-aware LiveRec base with all Memory weights, gate features, threshold, state transforms, and control policies frozen before test access.

Avoid all “first” claims and do not call current MemoryFusion an LLM agent.

---

# 4. Problem formulation

Let `B` denote the strong sequential base, `M` the explicit relationship-memory specialist, and `u_K(A,x)` event-level offline ranking utility.

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x)
\]

\[
\eta(z,r)=\mathbb E[\Delta_m(X)\mid Z=z,R=r]
\]

where `z` contains interaction/user state and base-confidence information and `r` denotes the recommendation regime.

Within a frozen regime, estimate `\hat\eta(z)` on development data and escalate to Memory when `\hat\eta(z)>\tau`.

`utility` means offline predictive ranking utility, not causal business lift.

---

# 5. Research questions

## RQ1 — Is relationship memory globally better or worse than a strong sequential base?

No. KuaiLive shows aggregate Memory-vs-Base ordering changes across candidate and temporal regimes. LiveRec/Twitch provides an independent instance of the same principle: Always Memory is significantly worse than the frozen strong base on both development and untouched test data even though Memory has a large positive advantage in a specific relationship-horizon regime.

## RQ2 — Can memory-relative utility be predicted beyond identity and generic base difficulty?

Yes. On KuaiLive, relative-utility routing improves over the strong identity-aware base and exceeds same-budget generic difficulty routing. On LiveRec/Twitch, the frozen dev-trained utility router reproduces the advantage on the untouched test: Selective−Base is significantly positive, and Utility−Difficulty remains significantly positive under exactly matched invocation budget.

## RQ3 — How do candidate, temporal, and relationship-horizon regimes change memory utility?

Candidate expansion and strict temporal shift materially alter aggregate Memory−Base ordering on KuaiLive. On LiveRec/Twitch, memory utility changes sign across recent-visible, long-horizon-only, and unseen relationships, with the same sign pattern on frozen dev and untouched test.

## RQ4 — What is the effectiveness–invocation–latency trade-off?

Selector cost is part of the serving budget; invocation rate alone is not a sufficient compute proxy. Lightweight selectors can reduce end-to-end latency even when their invocation prevalence differs from HGB.

## RQ5 — Does the conditional-specialist principle transfer to another live-stream platform with a strong domain-specific base?

Yes under the frozen LiveRec/Twitch protocol. P1.1 establishes the strong base, P1.2 freezes the transferred Memory specialist and utility policy on development data, and P1.3 provides one-shot held-out confirmation. The test reproduces all three central external findings: global Always Memory harm, strong positive long-horizon-only memory utility, and Selective Utility superiority over both Base and same-budget Difficulty routing.

---

# 6. Core evidence

## C1 — Regime-dependent relationship-memory utility on KuaiLive

- sampled-active: Memory < Dual-ID globally, but Selective > Dual-ID;
- full-active: Memory > Dual-ID and native Selective > both fixed choices;
- strict temporal GTS: Memory becomes broadly useful and escalation prevalence rises substantially.

This establishes that global model ordering depends on candidate and temporal regime rather than reflecting a fixed property of the Memory specialist.

## C2 — Relative utility contains information beyond generic difficulty

Matched-budget relative-utility routing significantly outperforms same-feature base-difficulty routing in sampled-active and full-active KuaiLive regimes.

LiveRec/Twitch reproduces the same distinction on the untouched one-shot test. With exactly matched test budget `K=6,650` (15.04% invocation):

- **Base NDCG@10:** 0.58211;
- **Selective Utility:** 0.58983;
- **Difficulty exact-K:** 0.58340;
- **Selective−Base:** +0.00772, 95% CI [+0.00641, +0.00903];
- **Utility−Difficulty:** +0.00644, 95% CI [+0.00528, +0.00762].

H@10 provides the same conclusion:

- **Base:** 0.75503;
- **Selective Utility:** 0.76448;
- **Difficulty exact-K:** 0.75252;
- **Selective−Base:** +0.00945, 95% CI [+0.00776, +0.01117];
- **Utility−Difficulty:** +0.01196, 95% CI [+0.01033, +0.01364].

Thus **hard case ≠ memory-solvable case**.

## C3 — Relationship horizon explains external memory complementarity

On the untouched LiveRec/Twitch test, transferred Always Memory remains globally worse than the strong base:

- **Always Memory NDCG@10:** 0.53980;
- **Memory−Base:** −0.04232, 95% CI [−0.04521, −0.03950].

Yet its marginal utility changes sharply by relationship horizon:

| Relationship horizon | n | Base NDCG@10 | Memory NDCG@10 | Memory−Base (95% CI) |
|---|---:|---:|---:|---:|
| recent-visible | 24,285 | 0.86102 | 0.84167 | −0.01935 [−0.02234, −0.01633] |
| **long-horizon-only** | **5,539** | **0.30181** | **0.52225** | **+0.22045 [+0.21140, +0.23001]** |
| unseen | 14,397 | 0.21948 | 0.03734 | −0.18215 [−0.18681, −0.17715] |

Interpretation:

- **recent-visible:** the sequential base already sees the relationship, so explicit Memory is redundant or harmful;
- **long-horizon-only:** persistent relationship information exists but falls outside the finite sequential context, producing the largest positive marginal Memory utility;
- **unseen:** no recoverable relationship exists, so Memory is strongly harmful.

This is a held-out replication of the P1.2 dev mechanism, not a post-test discovery.

## C4 — Repeat/novel is too coarse to identify memory-solvable events

On the one-shot test:

- repeat Memory−Base = −0.01475;
- novel Memory−Base = −0.07392.

The conventional novel group mixes long-horizon-only events, where Memory is strongly beneficial, with truly unseen events, where Memory is strongly harmful. Relationship horizon therefore provides a more mechanism-relevant diagnostic than repeat/novel status.

The relationship-horizon label remains **analysis-only** and is not an online gate feature.

## C5 — Relative-utility estimation provides useful ranking despite modest pointwise correlation

On the one-shot test, predicted versus realized event-level utility has Spearman `rho≈0.173`, so the gate should not be described as an accurate point predictor.

However, frozen dev-derived utility strata transfer coherently:

- D1–D8 have negative realized Memory−Base utility;
- D9 is approximately neutral (−0.0014);
- D10 is strongly positive (+0.0724), with predicted mean +0.0800.

The frozen threshold invokes Memory on 0% of D1–D8, about 38.6% of D9, and 100% of D10. The defensible claim is therefore **coarse relative-utility ranking / positive-tail identification**, not event-level calibration.

## C6 — Strong-base and validity controls

The KuaiLive result survives the streamer-heavy Dual-ID identity control, full-active candidate ranking, strict temporal evaluation, information ablations, adaptive-computation collision checks, and matched-budget difficulty controls.

LiveRec/Twitch uses the frozen official strong base and a transferred Memory definition. P1.3 was executed once after a dev-only policy freeze. Before test access, the workflow froze and verified:

- Memory weights and history semantics;
- utility-gate feature set and HGB family;
- threshold `0.004734357474290205`;
- dev-reference state transforms;
- final Difficulty control and exact-budget rule;
- same-K Oracle analysis rule.

No test-based rescue tuning is permitted.

## C7 — Selective-inference cost includes selector complexity

HGB remains the frozen scientific selector. KuaiLive latency experiments show that invocation rate alone is not a compute proxy: a lighter gate can have higher invocation prevalence while reducing total serving latency because selector overhead itself is material.

---

# 7. External validation — LiveRec/Twitch P1 CLOSED

## P1.1 strong-base reproduction

Frozen LiveRec dev NDCG@10 ≈ 0.57185 with a large repeat/novel performance gap, confirming a strong availability-aware, repeat-aware domain base.

## P1.2 development freeze

Development data establish the mechanism before test access:

- Base NDCG@10 = 0.57185;
- Always Memory = 0.52170;
- Selective Utility = 0.58023;
- same-budget Difficulty = 0.57311;
- Selective−Base = +0.00838, 95% CI [+0.00712, +0.00962];
- Utility−Difficulty = +0.00713, 95% CI [+0.00600, +0.00824];
- long-horizon-only Memory−Base ≈ +0.23097;
- recent-visible Memory−Base ≈ −0.01995;
- unseen Memory−Base ≈ −0.19562.

## P1.3 untouched one-shot test

All primary external findings reproduce under the frozen policy:

| Policy / mechanism | Untouched test result |
|---|---:|
| LiveRec Base NDCG@10 | 0.58211 |
| Always Memory NDCG@10 | 0.53980 |
| Selective Utility NDCG@10 | **0.58983** |
| Same-budget Difficulty NDCG@10 | 0.58340 |
| Selective−Base | **+0.00772**, 95% CI [+0.00641, +0.00903] |
| Utility−Difficulty | **+0.00644**, 95% CI [+0.00528, +0.00762] |
| Invocation rate | 15.04% (`K=6,650`) |
| Long-horizon-only Memory−Base | **+0.22045**, 95% CI [+0.21140, +0.23001] |
| Recent-visible Memory−Base | −0.01935, 95% CI [−0.02234, −0.01633] |
| Unseen Memory−Base | −0.18215, 95% CI [−0.18681, −0.17715] |
| Utility/realized Spearman | 0.1730 |
| Oracle exact-K NDCG@10 | 0.64806 |
| Oracle gain captured | 11.71% |

The frozen evaluator records `primary_success=true` and `mechanism_replication=true`.

Dev→test stability is substantive: the sign of Always Memory, Selective−Base, Utility−Difficulty, and all three relationship-horizon effects remains unchanged, with closely similar magnitudes.

External conclusion:

> **Relationship memory is a relationship-horizon specialist rather than a uniformly stronger recommender. Relative-utility estimation transfers well enough to identify a positive-utility tail and improve a strong domain base, whereas generic difficulty routing spends substantially more budget on hard but memory-unsolvable unseen events.**

---

# 8. Narrative logic

1. Live-stream recommendation combines ephemeral content with persistent creator relationships.
2. A strong sequential/identity-aware base is required before attributing value to explicit memory.
3. KuaiLive shows a sampled-regime paradox: Always Memory can be worse while selective Memory is useful.
4. Relative-utility estimation reveals exploitable within-regime heterogeneity beyond generic difficulty routing.
5. Candidate and temporal changes alter the prevalence and aggregate sign of memory utility.
6. LiveRec provides a strong repeat-aware external base, reducing the weak-baseline explanation.
7. Before test access, LiveRec dev shows why relationship horizon matters: explicit memory is harmful when no recoverable relationship exists, redundant when the relationship is already visible, and strongly useful when persistent relationships fall outside the finite sequential context.
8. A conventional repeat/novel split masks these opposite memory effects.
9. The frozen one-shot LiveRec test reproduces the dev sign pattern and confirms Selective Utility > Base and Selective Utility > same-budget Difficulty.
10. Generic difficulty is insufficient because many hard cases are truly unseen and therefore contain no relationship signal for Memory to recover.
11. Utility estimation need not be highly correlated event-by-event; coarse ranking that isolates a positive-utility tail can be sufficient for useful escalation.
12. Serving conclusions must account for both specialist invocation and selector cost.

---

# 9. Recommended manuscript structure

1. **Introduction** — setting, strong-base requirement, regime-dependent Memory utility, conditional-specialist thesis, contributions.
2. **Related Work** — live-stream recommendation; sequential/repeat-aware recommendation; long-term user/relationship memory; adaptive routing / Learning-to-Defer / MoE; recommender evaluation under regime shift.
3. **Problem Formulation** — `B`, `M`, `Delta_m`, `eta(z,r)`, legal candidates, dev-only policy learning, distinction between utility and difficulty.
4. **Selective Relationship-Memory Framework** — base, Memory specialist, utility estimator, threshold policy, same-budget controls.
5. **Experimental Setup** — KuaiLive candidate/temporal protocols plus LiveRec/Twitch freeze and one-shot external protocol.
6. **Main Results** — sampled paradox, relative utility vs difficulty, full-active reversal, strict temporal transition.
7. **Mechanism and Robustness** — information ablations, utility strata, relationship-horizon sign reversal, repeat/novel masking, strong-base controls.
8. **External Validation** — P1.1 base, P1.2 dev freeze, P1.3 untouched test, dev→test stability, exact-K difficulty and Oracle headroom.
9. **Accuracy–Cost Analysis** — selector/invocation/latency frontier and deployment implications.
10. **Discussion and Limitations** — modest pointwise utility correlation, remaining Oracle gap, horizon diagnostic not online-observable, two-platform boundary, offline/non-causal interpretation.
11. **Conclusion** — ask when incremental relationship-memory utility is positive rather than whether Memory is globally better.

---

# 10. Main tables and figures

- **Figure 1:** strong sequential base + relationship-memory specialist + relative-utility router; clearly separate online gate features from analysis-only relationship-horizon labels.
- **Table 1:** KuaiLive sampled-active identity-aware effectiveness: Base / Memory / Selective / Difficulty / Oracle where applicable.
- **Figure 2:** predicted relative-utility strata versus realized Memory−Base utility, with Utility vs Difficulty selection behavior.
- **Table 2:** KuaiLive full-active strict-transfer/native and strict-temporal results showing aggregate ordering changes.
- **Figure 3:** candidate/temporal regime transition map: aggregate Memory−Base sign and escalation prevalence.
- **Table 3:** state/confidence information ablations and strong-base robustness controls.
- **Figure/Table 4:** accuracy–latency–invocation frontier for HGB, Ridge, and tiny MLP gates.
- **Table 5 — External one-shot validation:** LiveRec Base / Always Memory / Selective Utility / exact-K Difficulty / exact-K Oracle with NDCG@10 and H@10, invocation rate, paired CIs, and dev→test comparison.
- **Figure 5 — Relationship-horizon mechanism:** recent-visible / long-horizon-only / unseen Memory−Base with dev and test confidence intervals; optional repeat/novel overlay showing masking.
- **Figure 6 — Gate mechanism:** Utility versus Difficulty invocation composition by relationship horizon, emphasizing that difficulty over-selects unseen cases.
- **Appendix:** detailed P1 freeze chain, one-shot guard, secondary robustness, collision defense, CPU/GPU compatibility audit, hyperparameters, and reproduction hashes.

---

# 11. Claim guardrails

Do not claim:

- Memory is globally inferior or globally superior independent of regime;
- generic routing/deferral is novel;
- utility estimates are well calibrated or near Oracle;
- high event-level utility prediction accuracy (test Spearman is only ~0.173);
- Selective always beats Always Memory in every candidate/temporal regime;
- current MemoryFusion is an LLM/agentic recommender;
- causal GMV/conversion/satisfaction lift;
- official DCGLive scores are directly comparable under the frozen protocol;
- repeat/novel labels identify memory-solvable cases;
- the diagnostic relationship-horizon label is available as an online routing feature;
- the current router explains most available Oracle headroom (test captures ~11.7%);
- cross-platform generalization beyond the two evaluated live-stream settings;
- that P1.3 was tuned after test access.

Preferred overarching sentence:

> **Relationship memory is a regime-dependent specialist: its aggregate value can change across candidate, temporal, and relationship-horizon regimes, while conditional relative-utility estimation reveals exploitable within-regime heterogeneity beyond fixed model choice and generic hard-case routing.**

Preferred external-validation sentence:

> **On a frozen strong LiveRec base, a dev-trained relative-utility router improves untouched test NDCG@10 while invoking Memory on only about 15% of events, and it significantly outperforms an exact-same-budget difficulty router; the largest positive Memory utility is concentrated in previously observed relationships that fall outside the base model's finite context.**

---

# 12. Current paper readiness

- **P0 KuaiLive internal validity/mechanism:** CLOSED.
- **P1.0 LiveRec data/protocol audit:** CLOSED.
- **P1.1 LiveRec strong-base reproduction:** CLOSED and frozen.
- **P1.2 LiveRec dev-only Memory + utility analysis:** CLOSED and frozen.
- **P1.3 untouched LiveRec one-shot test:** CLOSED and frozen; `primary_success=true`, `mechanism_replication=true`.

The core experimental chain is now **CLOSED**. Do not tune the Twitch Memory definition, gate family/features, threshold, state transforms, or policies using P1.3 outcomes.

The manuscript can now make a final held-out external claim at the level supported by the evidence:

> **The conditional-specialist principle transfers to a second live-stream platform with a strong domain-specific sequential base, including held-out replication of both selective effectiveness and the relationship-horizon mechanism.**

Remaining work should prioritize manuscript construction, presentation, targeted literature comparison, and only journal-motivated robustness checks that do not reuse P1.3 for model selection.
