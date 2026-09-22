# KuaiLive-Agent — Post-P1.2 Academic Paper Skeleton

**Snapshot date:** 2026-09-22  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Phase:** P0 closed; LiveRec P1.1 strong-base reproduction closed; P1.2 dev-only memory/utility analysis closed and frozen; P1.3 untouched test next.  
**Supersedes for current writing:** `PAPER_SKELETON_2026-09-22_POST_P1_BASE.md` while preserving earlier snapshots for provenance.

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

KuaiLive establishes the main candidate/temporal regime result. LiveRec/Twitch now provides dev-frozen external mechanism evidence that memory can be globally harmful while strongly useful when persistent relationships fall outside the finite sequential context. Cross-platform test confirmation remains pending until the one-shot P1.3 test is executed.

---

# 3. Novelty boundary

The paper does **not** claim invention of generic instance-wise expert routing. The defensible contribution is the combination of:

1. an explicit **relationship-memory specialist** separated from a strong sequential base;
2. direct estimation of **specialist-minus-base ranking utility** rather than generic difficulty;
3. evidence that memory utility changes across candidate, temporal, and relationship-horizon regimes;
4. matched-budget evidence that relative-utility routing contains decision-relevant information beyond base difficulty;
5. serving evidence that selector complexity and specialist invocation jointly determine cost;
6. external validation against a strong availability-aware, repeat-aware LiveRec base, with dev mechanism evidence frozen and untouched test confirmation pending.

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

No. KuaiLive shows aggregate Memory-vs-Base ordering changes across candidate and temporal regimes; LiveRec dev shows another form of the same phenomenon, where Always Memory is globally worse despite strong positive utility in a specific relationship-horizon regime.

## RQ2 — Can memory-relative utility be predicted beyond identity and generic base difficulty?

Yes on KuaiLive, and independently on LiveRec dev: selective utility routing improves over the strong base and exceeds a same-budget generic difficulty router.

## RQ3 — How do candidate, temporal, and relationship-horizon regimes change memory utility?

Candidate expansion and strict temporal shift materially alter aggregate Memory−Base ordering on KuaiLive. On LiveRec dev, memory utility changes sign across recent-visible, long-horizon-only, and unseen relationships.

## RQ4 — What is the effectiveness–invocation–latency trade-off?

Selector cost is part of the serving budget; invocation rate alone is not a sufficient compute proxy.

## RQ5 — Does the conditional-specialist principle transfer to another live-stream platform with a strong domain-specific base?

P1.1 establishes the faithful LiveRec/Twitch base. P1.2 provides dev-frozen mechanism evidence: global Memory is harmful, but conditional utility is strongly positive for long-horizon relationships outside the base context, and relative-utility routing beats same-budget difficulty routing. P1.3 remains the untouched one-shot test confirmation.

---

# 6. Core evidence

## C1 — Regime-dependent relationship-memory utility on KuaiLive

- sampled-active: Memory < Dual-ID globally, but Selective > Dual-ID;
- full-active: Memory > Dual-ID and native Selective > both fixed choices;
- strict temporal GTS: Memory becomes broadly useful and escalation prevalence rises substantially.

## C2 — Relative utility contains information beyond generic difficulty

Matched-budget relative-utility routing significantly outperforms same-feature base-difficulty routing in sampled-active and full-active KuaiLive regimes.

LiveRec dev independently reproduces this mechanism: utility routing improves over the frozen base at a sparse invocation rate and clearly exceeds the exact-same-budget difficulty router.

## C3 — Relationship horizon explains external memory complementarity

On LiveRec dev, the frozen Memory specialist is globally worse than the strong base, but its marginal utility changes sharply by relationship horizon:

- **recent-visible:** Memory adds little or is harmful because the sequential base already sees the relationship;
- **long-horizon-only:** Memory is strongly beneficial because persistent relationship information exists outside the finite base context;
- **unseen:** Memory is strongly harmful because no historical relationship signal is available to recover.

This sign reversal is more informative than a conventional repeat/novel split, which mixes recoverable long-horizon relationships with truly unseen targets.

## C4 — Strong-base and validity controls

The KuaiLive result survives the streamer-heavy Dual-ID identity control, full-active candidate ranking, strict temporal evaluation, information ablations, and adaptive-computation collision checks.

LiveRec uses a frozen official strong base; P1.2 preserves the transferred Memory specialist and frozen dev-only utility-learning protocol without test inspection.

## C5 — Selective-inference cost includes selector complexity

HGB remains the frozen scientific selector; lighter gates show that invocation rate and end-to-end latency need not move together.

## External validation status — LiveRec P1.1–P1.2 CLOSED

Frozen P1.1 strong base dev NDCG@10 is approximately 0.5719.

Frozen P1.2 dev results establish the external mechanism pattern:

| Policy / regime | Dev NDCG@10 / marginal result |
|---|---:|
| LiveRec Base | 0.5719 |
| Always Memory | 0.5217 |
| Selective Utility Router | 0.5802 |
| Same-budget Difficulty Router | 0.5731 |
| Long-horizon-only Memory−Base | strongly positive (~+0.231) |
| Recent-visible Memory−Base | negative |
| Unseen Memory−Base | strongly negative |

Interpretation at skeleton level: **Memory is a relationship-horizon specialist, not a uniformly stronger recommender; relative utility is more decision-relevant than generic difficulty.** Untouched P1.3 test confirmation is still required before presenting these as final cross-platform test results.

---

# 7. Narrative logic

1. Live-stream recommendation combines ephemeral content with persistent creator relationships.
2. A strong sequential/identity-aware base is required before attributing value to explicit memory.
3. KuaiLive shows a sampled-regime paradox: Always Memory can be worse while selective Memory is useful.
4. Relative-utility estimation explains exploitable within-regime heterogeneity better than generic difficulty routing.
5. Candidate and temporal changes alter the prevalence and aggregate sign of memory utility.
6. LiveRec provides a strong repeat-aware external base, ruling out a weak-baseline explanation.
7. LiveRec dev shows why relationship horizon matters: explicit memory is harmful when no recoverable relationship exists, redundant when the relationship is already visible, and strongly useful when persistent relationships fall outside the finite sequential context.
8. A conventional repeat/novel split can mask these opposite memory effects.
9. Relative-utility routing outperforms generic hard-case routing because difficult cases are not necessarily memory-solvable cases.
10. Serving conclusions must account for both specialist invocation and selector cost.

---

# 8. Recommended manuscript structure

1. **Introduction** — setting, strong-base requirement, regime-dependent memory utility, contributions.
2. **Related Work** — live-stream recommendation; repeat/sequential models; memory; adaptive routing; Learning-to-Defer/MoE.
3. **Problem Formulation** — `B`, `M`, `Delta_m`, `eta(z,r)`, legal candidates, dev-only policy learning.
4. **Selective Relationship-Memory Framework** — base, memory specialist, utility estimator, routing policy.
5. **Experimental Setup** — KuaiLive protocols plus LiveRec/Twitch external protocol.
6. **Main Results** — sampled paradox, utility vs difficulty, full-active reversal, temporal transition.
7. **Mechanism and Robustness** — utility strata, information ablations, relationship-horizon analysis, robustness controls.
8. **Accuracy–Cost Analysis** — selector/invocation/latency trade-off.
9. **External Validation** — strong-base freeze, dev-frozen relationship-horizon mechanism, utility-vs-difficulty, untouched test.
10. **Discussion and Limitations** — regime dependence, external-transfer boundary, remaining oracle gap, non-causal interpretation.
11. **Conclusion** — ask when incremental relationship-memory utility is positive rather than whether Memory is globally better.

---

# 9. Main tables and figures

- **Figure 1:** strong base + relationship-memory specialist + relative-utility router.
- **Table 1:** sampled-active identity-aware effectiveness.
- **Figure 2:** conditional-utility stratification, utility-vs-difficulty, oracle headroom.
- **Table 2:** full-active strict-transfer/native results.
- **Figure 3:** candidate/temporal regime transition map.
- **Table 3:** state/confidence information ablations.
- **Figure/Table 4:** accuracy–latency–invocation frontier.
- **External Table:** LiveRec Base / Always Memory / Selective / matched-budget Difficulty Router, with repeat/novel and relationship-horizon breakdown; dev policy is frozen and test rows remain pending P1.3.
- **External Figure:** relationship-horizon sign reversal and/or predicted-utility strata versus realized Memory−Base utility.
- **Appendix:** secondary robustness, collision defense, development-chain details, external reproduction details.

---

# 10. Claim guardrails

Do not claim:

- Memory is globally inferior or globally superior independent of regime;
- generic routing/deferral is novel;
- utility estimates are well calibrated or near oracle;
- Selective always beats Always Memory;
- current MemoryFusion is an LLM/agentic recommender;
- causal GMV/conversion/satisfaction lift;
- official DCGLive scores are directly comparable under the frozen protocol;
- repeat/novel labels identify memory-solvable cases;
- the diagnostic relationship-horizon label is available as an online routing feature;
- dev P1.2 alone constitutes final external test confirmation;
- cross-platform test success before the one-shot P1.3 result is observed.

Preferred overarching sentence:

> **Relationship memory is a regime-dependent specialist: its aggregate value can change across candidate, temporal, and relationship-horizon regimes, while conditional relative-utility estimation reveals exploitable within-regime heterogeneity beyond fixed model choice and generic hard-case routing.**

---

# 11. Current paper readiness

- **P0 KuaiLive internal validity/mechanism:** CLOSED.
- **P1.0 LiveRec data/protocol audit:** CLOSED.
- **P1.1 LiveRec strong-base reproduction:** CLOSED and frozen.
- **P1.2 LiveRec dev-only Memory + utility analysis:** CLOSED and frozen.
- **P1.3 untouched LiveRec test:** NEXT; must remain one-shot with no rescue tuning.

The manuscript can now state a frozen external **dev mechanism replication**, but final external effectiveness claims should remain conditional until P1.3 is executed once.