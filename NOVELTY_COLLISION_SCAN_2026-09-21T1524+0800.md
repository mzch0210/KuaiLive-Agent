# KuaiLive-Agent — Novelty / Collision Scan

**Snapshot timestamp:** 2026-09-21 15:24 +08:00  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Purpose:** preserve the 2026-09-21 web-based novelty review for future manuscript writing and future ChatGPT accounts.

---

# 1. Search focus

The scan deliberately searched beyond “memory recommender” and included the closest neighboring problem formulations:

- selective memory recommendation;
- memory-augmented recommendation;
- uncertainty-guided recommendation;
- adaptive fast/slow recommendation;
- dynamic routing / mixture of experts;
- selective prediction / abstention;
- live-stream recommendation;
- repeat-consumption recommendation;
- dynamic room recommendation;
- cost-aware routing.

The paper should not attempt novelty claims on any one of these generic categories individually.

---

# 2. Closest collision map

## Collision A — DS-Frame: Recommender System as Slow and Fast Thinkers

**Venue/status:** accepted CIKM 2026; arXiv:2609.02671.  
**Core idea:** fast sequential recommender + iterative slow recommender + learned selector + controllable computation budget.

### Collision level

**High** for:

- selective routing;
- adaptive inference;
- accuracy–efficiency trade-off;
- user-state-dependent routing.

### Why the present paper remains distinct

DS-Frame’s slow path is globally stronger than its fast path. Its central question is approximately:

> When should more computation be allocated to the stronger slow model?

Our setting is:

> When does a globally inferior explicit memory specialist become locally superior to a strong identity-aware sequential base?

This is the single most important conceptual distinction.

Source: https://arxiv.org/abs/2609.02671

---

## Collision B — GUIDER: Uncertainty Guided Dynamic Re-ranking for LLM Recommenders

**Venue:** AAAI 2026.  
**Core idea:** decomposes uncertainty for LLM recommendation and adapts reranking behavior dynamically.

### Collision level

**Medium–high** for:

- confidence / uncertainty-guided adaptation;
- conditional recommendation behavior;
- dynamic inference.

### Distinction

GUIDER is an LLM reranking / uncertainty framework. It does not study an explicit memory specialist that is globally worse than the base, nor specialist-minus-base utility, persistent-identity controls, or temporal regime changes in specialist utility.

Source: https://ojs.aaai.org/index.php/AAAI/article/view/38639

---

## Collision C — MemRec: Collaborative Memory-Augmented Agentic Recommender System

**Venue:** ACL 2026.  
**Core idea:** collaborative memory graph managed by a lightweight memory model and used by a heavier LLM recommender.

### Collision level

**High** for generic claims such as:

- memory-augmented recommendation;
- memory-enhanced recommender;
- agentic memory for recommendation.

### Distinction

MemRec studies semantic/collaborative memory inside an LLM-agent recommendation architecture. The present project instead studies whether an explicit relationship-memory specialist has **positive conditional relative utility beyond a strong sequential base**, including cases where memory is globally worse.

Do not market the current system as an “agentic recommender” to avoid unnecessary collision.

Source: https://aclanthology.org/2026.acl-long.2061/

---

## Collision D — Mixture-of-Experts recommenders / dynamic expert routing

Examples include 2025–2026 session-aware and sequential MoE recommenders that use context-dependent expert selection.

### Collision level

**Medium** for:

- dynamic expert selection;
- context-conditioned routing;
- specialist language.

### Distinction

Conventional MoE systems typically learn multiple peer experts inside one architecture. The present work uses a **separately interpretable memory specialist** and studies its signed utility **relative to a strong base**. The key empirical condition is unusual: the specialist is globally inferior but locally beneficial.

Representative source:

- https://www.mdpi.com/2079-9292/15/4/825

---

## Collision E — LiveRec

**Work:** Live streaming recommendation under dynamic item availability and repeat consumption.  
**Dataset:** Twitch 100k benchmark and full Twitch interaction dataset.

### Collision level

**High** for:

- dynamic availability motivation;
- repeat-consumption motivation;
- sequential live-stream recommendation.

### Distinction

LiveRec is a direct live-stream sequential recommendation lineage, but not a selective explicit-memory utility framework.

Source: https://github.com/JRappaz/liverec

---

## Collision F — MRB4LS: Live streaming recommendation based on multiple types of repeated behaviors

**Venue:** Expert Systems with Applications, 2025.  
**Core idea:** graph modeling of repeated enter/chat/gift behavior.

### Collision level

**Medium–high** for repeat-behavior motivation and live-stream domain.

### Distinction

MRB4LS directly incorporates repeated behavior into a graph recommender. It does not ask whether an explicit memory specialist is globally inferior yet conditionally useful, nor learn specialist-minus-base utility.

Source: https://doi.org/10.1016/j.eswa.2025.128217

---

## Collision G — DCGLive: Room Matters

**Venue:** WWW 2026.  
**Core idea:** dynamic room-level collaboration modeling among users, rooms, and streamers.

### Collision level

**High** for the live-room task and dynamic room representation.

### Distinction

DCGLive is a strong room-dynamics recommender, not a selective memory-utility method. It is therefore best treated as a domain/SOTA comparator or reviewer-defense baseline, not as a conceptual collision.

Source: https://doi.org/10.1145/3774904.3792241

---

## Collision H — OneLive

**Date:** 2026.  
**Core idea:** dynamic unified generative framework for industrial live-stream recommendation with dynamic tokenization, time-aware attention, efficient decoding, and multi-objective alignment.

### Collision level

**Medium** for:

- live-stream temporal dynamics;
- real-time systems motivation;
- industrial recommendation framing.

### Distinction

OneLive addresses dynamic generative modeling rather than conditional value of explicit memory.

Source: https://arxiv.org/abs/2602.08612

---

## Collision I — KuaiLive-M3

**Date:** 2026.  
**Core contribution:** new multimodal / multidomain / multifeedback live-stream recommendation dataset and benchmarks.

### Collision level

**Low** for method novelty, **high relevance** for external validation and contemporary benchmark positioning.

Source: https://arxiv.org/abs/2607.24862

---

# 3. Selective prediction / abstention literature

Selective prediction broadly studies when a model should abstain based on confidence, risk, or cost. This literature means the paper should not claim novelty for the generic idea “make decisions only when confident.”

The present work differs because it does not abstain from prediction. It predicts the **relative utility of a second specialist** and escalates selectively.

Likewise, generic model-routing / cost-aware RAG literature shows that expected utility and compute-aware routing are active topics. The paper’s novelty must therefore stay at the **specialist-relative utility phenomenon in recommendation**, not generic conditional execution.

---

# 4. What appears genuinely distinctive after the scan

As of 2026-09-21, no retrieved work was found that simultaneously establishes the following chain:

1. **strong sequential base**;
2. **explicit memory as a separate, interpretable specialist**;
3. the memory specialist is **globally inferior** to the base;
4. model learns **specialist-minus-base conditional relative utility** rather than generic uncertainty/difficulty;
5. selective use significantly improves the strong base;
6. improvement survives **explicit persistent-identity absorption** in a Dual-ID base;
7. the prevalence of positive memory utility changes sharply across **strict temporal regimes**;
8. the paper separates **selector cost** from **specialist invocation cost** and shows that lower invocation frequency need not imply lower end-to-end latency.

This combination is the defensible novelty position.

---

# 5. Novelty claims that are unsafe

Do **not** claim:

- first memory recommender;
- first selective recommender;
- first uncertainty-aware recommender;
- first dynamic routing recommender;
- first adaptive inference recommender;
- first recommender using mixture of experts;
- first live-stream recommender modeling repeated behavior;
- first agentic memory recommender.

These would collide with existing literature.

---

# 6. Safer novelty language

Recommended wording:

> **Rather than assuming that an auxiliary memory model is globally stronger, we study the more difficult regime in which explicit memory is inferior on average yet beneficial on identifiable subsets. We formulate memory use as prediction of conditional specialist-minus-base utility, and show that this utility persists after persistent identity is absorbed by a strong sequential baseline and changes substantially across temporal regimes.**

Alternative:

> **Our focus is not generic selective computation but the conditional value of an explicit memory specialist relative to a strong sequential recommender.**

Avoid “first”; use “we study”, “we identify”, “we show”, “we provide evidence that”.

---

# 7. Paper-title implication

The current preferred title remains well positioned:

> **Learning When Memory Helps: Conditional Specialist Utility for Live-Streaming Recommendation**

Why this is safer than alternatives:

- “memory” names the domain mechanism;
- “conditional specialist utility” distinguishes it from generic memory augmentation;
- “live-streaming recommendation” anchors the application;
- avoids fast/slow, agentic, uncertainty-aware, and MoE buzzwords already occupied by nearby 2026 work.

---

# 8. Related-work structure recommended after collision scan

The Related Work section should have four explicit contrasts:

1. **Live-stream recommendation and repeat consumption** — LiveRec, MRB4LS, DCGLive, OneLive, KuaiLive-M3.
2. **Memory-augmented recommendation** — including MemRec and adjacent semantic-memory systems.
3. **Adaptive / uncertainty-aware recommendation** — DS-Frame and GUIDER.
4. **Dynamic expert routing / selective prediction** — MoE and abstention literature.

End the section with the unresolved gap:

> Existing work studies stronger memory architectures, stronger slow models, uncertainty-guided adaptation, or context-dependent experts. It does not directly characterize the case where an explicit memory specialist is globally inferior to a strong base but has predictable positive relative utility on subsets whose prevalence changes across temporal regimes.

---

# 9. Search conclusion

**Novelty status: defensible but framing-sensitive.**

The paper remains novel if it is written around:

- conditional specialist utility;
- global inferiority vs local complementarity;
- persistent-identity control;
- temporal regime dependence;
- selector-vs-specialist cost decomposition.

The paper becomes much less novel if it is written as:

- memory-augmented recommender;
- adaptive recommendation;
- uncertainty-guided routing;
- fast/slow recommender;
- agentic memory recommender.
