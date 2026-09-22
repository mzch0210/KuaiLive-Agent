# KuaiLive-Agent — Post-P1.1 Academic Paper Skeleton

**Snapshot date:** 2026-09-22  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Phase:** P0 closed; LiveRec P1.1 strong-base reproduction closed; P1.2–P1.3 external memory validation pending.  
**Supersedes for current writing:** `PAPER_SKELETON_2026-09-21T2012+0800.md` while preserving earlier snapshots for provenance.

---

# 1. Recommended title

## Primary

> **Learning When Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

## Alternative

> **When Does Memory Help? Regime-Dependent Utility of Explicit Relationship Memory in Live-Streaming Recommendation**

Avoid centering the title on generic adaptive computation, uncertainty routing, agentic recommendation, or generic memory augmentation.

---

# 2. Core thesis

> **Explicit relationship memory has no fixed global ordering relative to a strong sequential recommender. Its marginal ranking utility varies across user states, candidate universes, and temporal regimes. Conditional relative-utility estimation can exploit this heterogeneity beyond fixed model choice and generic hard-case routing.**

KuaiLive establishes the main regime-dependent memory result. LiveRec/Twitch is the external validation environment, not yet evidence of cross-platform memory gain until P1.2–P1.3 are frozen.

---

# 3. Novelty boundary

The paper does **not** claim invention of generic instance-wise expert routing. The defensible contribution is the combination of:

1. an explicit **relationship-memory specialist** separated from a strong sequential base;
2. direct estimation of **specialist-minus-base ranking utility** rather than generic difficulty;
3. evidence that memory utility changes across candidate and temporal regimes;
4. matched-budget evidence that relative-utility routing contains information beyond base difficulty;
5. serving evidence that selector complexity and specialist invocation jointly determine cost;
6. cross-platform validation against a strong availability-aware, repeat-aware LiveRec base, once P1.2–P1.3 are complete.

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

No. KuaiLive shows aggregate Memory-vs-Base ordering changes across candidate and temporal regimes.

## RQ2 — Can memory-relative utility be predicted beyond identity and generic base difficulty?

Yes on KuaiLive: selective gain survives the strong Dual-ID control and matched-budget utility routing exceeds generic difficulty routing.

## RQ3 — How do candidate and temporal regimes change memory utility?

Candidate expansion and strict temporal shift materially change both the aggregate Memory−Base sign and escalation prevalence.

## RQ4 — What is the effectiveness–invocation–latency trade-off?

Selector cost is part of the serving budget; invocation rate alone is not a sufficient compute proxy.

## RQ5 — Does the conditional-specialist principle transfer to another live-stream platform with a strong domain-specific base?

P1.1 establishes a faithful LiveRec/Twitch base and strong repeat-vs-novel performance heterogeneity. P1.2–P1.3 must determine whether **memory-relative utility itself**, rather than generic target difficulty, transfers cross-platform.

---

# 6. Core evidence

## C1 — Regime-dependent relationship-memory utility on KuaiLive

- sampled-active: Memory < Dual-ID globally, but Selective > Dual-ID;
- full-active: Memory > Dual-ID and native Selective > both fixed choices;
- strict temporal GTS: Memory becomes broadly useful and escalation prevalence rises substantially.

## C2 — Relative utility contains information beyond generic difficulty

Matched-budget relative-utility routing significantly outperforms same-feature base-difficulty routing in sampled-active and full-active regimes.

## C3 — Strong-base and validity controls

The result survives the streamer-heavy Dual-ID identity control, full-active candidate ranking, strict temporal evaluation, information ablations, and adaptive-computation collision checks.

## C4 — Selective-inference cost includes selector complexity

HGB remains the frozen scientific selector; lighter gates show that invocation rate and end-to-end latency need not move together.

## External validation status — LiveRec P1.1 CLOSED

The official strong LiveRec base is frozen on Twitch 100k using dev-only model selection and untouched test ranking.

Frozen dev result at the selected checkpoint:

| Slice | H@1 | NDCG@10 |
|---|---:|---:|
| Overall | 0.3930 | 0.5719 |
| Repeat target | 0.6824 | 0.8599 |
| Novel target | 0.0928 | 0.2730 |

Interpretation at skeleton level: **the external task contains strong regime heterogeneity and a strong repeat-aware base.** This motivates testing incremental relationship-memory utility beyond signals already captured by LiveRec; it does not by itself establish that Memory helps on Twitch.

---

# 7. Narrative logic

1. Live-stream recommendation combines ephemeral content with persistent creator relationships.
2. A strong sequential/identity-aware base is required before attributing value to explicit memory.
3. KuaiLive shows a sampled-regime paradox: Always Memory can be worse while selective Memory is useful.
4. Relative-utility estimation explains exploitable within-regime heterogeneity better than generic difficulty routing.
5. Candidate and temporal changes alter the prevalence and aggregate sign of memory utility.
6. LiveRec P1.1 shows the external platform has a strong repeat-aware base and large repeat/novel performance heterogeneity.
7. The external test therefore asks whether **incremental memory utility can be localized beyond repeat consumption already modeled by the base**.
8. Serving conclusions must account for both specialist invocation and selector cost.

---

# 8. Recommended manuscript structure

1. **Introduction** — setting, strong-base requirement, regime-dependent memory utility, contributions.
2. **Related Work** — live-stream recommendation; repeat/sequential models; memory; adaptive routing; Learning-to-Defer/MoE.
3. **Problem Formulation** — `B`, `M`, `Delta_m`, `eta(z,r)`, legal candidates, dev-only policy learning.
4. **Selective Relationship-Memory Framework** — base, memory specialist, utility estimator, routing policy.
5. **Experimental Setup** — KuaiLive protocols plus LiveRec/Twitch external protocol.
6. **Main Results** — sampled paradox, utility vs difficulty, full-active reversal, temporal transition.
7. **Mechanism and Robustness** — utility strata, information ablations, robustness controls.
8. **Accuracy–Cost Analysis** — selector/invocation/latency trade-off.
9. **External Validation** — P1.1 strong-base freeze; P1.2 memory-relative utility; P1.3 untouched test.
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
- **External Table:** LiveRec Base / Always Memory / Selective / matched-budget Difficulty Router, with repeat/novel breakdown; base row is frozen, remaining rows await P1.2–P1.3.
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
- the LiveRec repeat/novel performance gap proves where Memory will help;
- cross-platform memory transfer before P1.2–P1.3 are frozen.

Preferred overarching sentence:

> **Relationship memory is a regime-dependent specialist: its aggregate value can change across candidate and temporal regimes, while conditional relative-utility estimation reveals exploitable within-regime heterogeneity beyond fixed model choice and generic hard-case routing.**

---

# 11. Current paper readiness

- **P0 KuaiLive internal validity/mechanism:** CLOSED.
- **P1.0 LiveRec data/protocol audit:** CLOSED.
- **P1.1 LiveRec strong-base reproduction:** CLOSED and frozen.
- **P1.2 LiveRec dev-only Memory + utility analysis:** NEXT.
- **P1.3 untouched LiveRec test:** pending; must remain one-shot after P1.2 freeze.

The manuscript should now treat LiveRec as an active external-validation section rather than a placeholder, while withholding any cross-platform memory-effect claim until P1.3.