# KuaiLive-Agent — Post-P1.1 Experiment Plan

**Snapshot date:** 2026-09-22  
**Current phase:** P0 CLOSED; P1.0–P1.1 CLOSED; P1.2 dev-only memory/utility analysis NEXT; P1.3 untouched test pending.

---

# 1. Executive decision

Do **not** reopen KuaiLive model expansion and do **not** retrain the frozen LiveRec base.

The P1 pipeline remains valid, but P1.2 should add one mechanism layer before routing:

> distinguish relationship information already visible to the 16-step LiveRec context from relationship information available only in longer-term history.

This change is motivated by the frozen base result, not by any Memory or test outcome. The untouched test remains uninspected.

---

# 2. P1.1 — CLOSED / FROZEN

Strong official LiveRec base on Twitch 100k:

- official source lineage and frozen configuration preserved;
- dev-only checkpoint selection completed;
- selected checkpoint frozen;
- test ranking not inspected;
- overall dev NDCG@10 ≈ 0.5719;
- repeat-target dev NDCG@10 ≈ 0.8599;
- novel-target dev NDCG@10 ≈ 0.2730.

Interpretation: LiveRec is already a strong repeat-aware base, so external validation must test **incremental relationship-memory utility beyond the base context**, not merely whether repeat targets are easier.

---

# 3. P1.2 — Dev-only Memory + conditional-utility analysis

## P1.2A — Relationship-horizon audit — ADD

Before fitting any gate, partition dev targets using only history strictly before target:

1. **recent-visible relationship** — target streamer appears within the LiveRec `seq_len=16` base context;
2. **long-horizon-only relationship** — target streamer was seen earlier in user history but not within the current 16-step base context;
3. **unseen relationship** — target streamer has not appeared in prior user history.

Report Base, Memory, and `Memory−Base` by these three regimes.

Purpose: determine whether explicit relationship memory adds information that is genuinely outside the base context.

Do not route directly from these labels and do not use them to retune the base.

## P1.2B — Primary transferred MemoryFusion — KEEP FROZEN

Retain the pre-specified transferred specialist:

`MemoryFusion = 0.45 * short + 0.45 * long + 0.10 * popularity`.

Do **not** retune these weights after seeing P1.1.

Optional dev-only component diagnostics may report short, long, and popularity terms separately, but they must not redefine the primary Memory specialist or select a new test model.

## P1.2C — Utility gate — KEEP

- primary gate family: frozen HGB;
- target: event-level `Memory NDCG@10 − LiveRec NDCG@10`;
- state + base-confidence features computed strictly pre-target;
- OOF dev utility prediction for threshold selection;
- final gate fit on all dev only.

## P1.2D — Difficulty control — KEEP

Fit same-feature generic base-difficulty HGB and compare at exactly the primary utility router's invocation budget `K`.

Primary mechanism question remains:

> does relative-utility routing contain decision-relevant information beyond generic base difficulty?

## P1.2E — Required dev reporting — MODIFY

Report both:

- conventional **repeat vs novel** breakdown for comparability;
- primary mechanism breakdown by **recent-visible / long-horizon-only / unseen** relationship horizon.

Do not infer routing policy from subgroup difficulty alone.

---

# 4. P1.3 — Untouched one-shot test — UNCHANGED

Only after P1.2 is frozen:

Primary rows:

- frozen LiveRec Base;
- frozen transferred Always Memory;
- Selective Memory;
- matched-budget Difficulty Router;
- exact-K Oracle as analysis-only headroom.

Primary metrics:

- NDCG@10;
- HR/Recall@10;
- invocation rate;
- paired user bootstrap CI;
- repeat/novel breakdown;
- relationship-horizon breakdown;
- utility strata.

Primary success rule remains:

`Selective − LiveRec Base > 0` with bootstrap 95% CI lower bound > 0.

Mechanism replication remains:

`Utility Router − Difficulty Router > 0`, preferably with positive paired CI.

If null or negative, do not rescue-tune on test; preserve the result as an external boundary condition.

---

# 5. What should NOT change

Do not:

- retrain or retune the frozen LiveRec base;
- increase LiveRec sequence length after seeing dev results;
- replace the primary transferred MemoryFusion with a newly tuned specialist;
- route simply on `repeat`, `novel`, or base error;
- inspect test before P1.2 is frozen;
- add broad new backbones;
- reopen KuaiLive controls already closed in P0.

---

# 6. Updated stopping rule

The next decisive sequence is:

> **P1.2A relationship-horizon audit → P1.2B–D frozen Memory/utility/difficulty models → P1.2 freeze → one-shot P1.3 test → manuscript freeze.**

No P2 expansion unless the frozen P1 result exposes a specific reviewer-risk question.