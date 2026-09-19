# Selective Agent v2 — Frozen Validation Results

Status: **PASS**

Reproducible GitHub Actions run: **35447655392**  
Commit: `07f4434774302b01097435815ec6ae5a9e59a7ce`

## Protocol lock

The primary v2 gate was fixed before v2 test evaluation:

- Base recommender: tuned SASRec (`lr=5e-4`, `history_max=50`), selected on dev from the existing SASRec/TiSASRec grid.
- Candidate protocol: frozen KuaiLive-Shop evaluation with 574 negatives + 1 positive per user.
- Users: 10,222.
- Agent alternative: MemoryFusion.
- Primary gate: HistGradientBoosting residual regressor.
- Gate inputs:
  - user state: log history length, repeat rate, preference entropy, preference drift, time regularity, state complexity;
  - SASRec uncertainty/confidence: score standard deviation/range, top-score margins, top-score z-score, normalized softmax entropy, and top-10 softmax mass.
- All model fitting and threshold selection use dev only.
- The gate threshold is selected from 5-fold OOF dev predictions.
- Test is evaluation-only.

## Headline result

| Method | Test NDCG@10 | Absolute delta vs SASRec | Relative delta |
|---|---:|---:|---:|
| MemoryFusion always | 0.567697 | -0.042401 | -6.95% |
| Tuned SASRec | 0.610098 | — | — |
| **Selective Agent v2 — HGB primary** | **0.623232** | **+0.013134** | **+2.15%** |
| ExtraTrees combined (secondary) | 0.625406 | +0.015308 | +2.51% |
| Multi-module HGB router | 0.620108 | +0.010010 | +1.64% |

Primary HGB paired user-level bootstrap 95% CI for the NDCG@10 delta:

**[+0.010114, +0.016310]**

The primary gate invokes MemoryFusion for **1,628 / 10,222 users (15.93%)**.

Mean history length:

- selected for MemoryFusion: **122.22**
- retained on SASRec: **26.89**

## Ablation evidence

| Gate | Test NDCG@10 | Delta vs SASRec |
|---|---:|---:|
| History-length threshold only | 0.615551 | +0.005453 |
| HGB, user-state only | 0.615582 | +0.005484 |
| Ridge, user-state only | 0.616386 | +0.006288 |
| Ridge, state + SASRec confidence | 0.621776 | +0.011678 |
| Tree depth 3, state + SASRec confidence | 0.623557 | +0.013459 |
| **HGB, state + SASRec confidence** | **0.623232** | **+0.013134** |
| ExtraTrees, state + SASRec confidence | 0.625406 | +0.015308 |

The main incremental gain therefore comes from combining **memory-state features with base-model uncertainty/confidence**, rather than from history length alone.

## OOF split robustness

The primary HGB gate was repeated with five different 5-fold OOF split seeds; each seed selected its threshold using dev only.

- test NDCG@10 range: **0.620012 – 0.623232**
- absolute delta range: **+0.009914 – +0.013134**
- minimum bootstrap CI lower bound: **+0.007516**

Thus the v2 gain is not dependent on one favorable OOF partition.

## Multi-module router

A router choosing among SASRec, MemoryFusion, LongMemory and ShortMemory also beats SASRec, but is weaker than the binary SASRec-vs-MemoryFusion primary gate:

- NDCG@10: **0.620108**
- delta: **+0.010010**
- bootstrap 95% CI: **[+0.007027, +0.012908]**
- actions on test: SASRec 8,858; MemoryFusion 756; LongMemory 541; ShortMemory 67.

This suggests that the current publishable mechanism is primarily **selective escalation to explicit fused memory**, not fine-grained routing among multiple memory modules.

## Interpretation

The evidence now supports a stronger formulation than an always-on agent recommender:

> A strong sequential recommender should remain the default. Explicit memory reasoning should be invoked selectively when user-history state and the base recommender's own uncertainty indicate that the sequential model is likely to leave utility on the table.

This changes the research claim from “Agent beats SASRec” to **“learning when to invoke explicit memory can significantly improve a strong sequential recommender.”**

## Remaining limitations / next robustness gates

1. The current result uses one frozen negative-sampling seed; replicate across multiple candidate seeds.
2. Add a global temporal split in addition to per-user leave-one-out.
3. Add exposure-aware robustness using KuaiLive `negative.csv` where appropriate; do not claim IPS/SNIPS without valid propensities.
4. Test whether the selective gain survives additional strong sequential/retrieval baselines under exactly the same candidates.
5. Evaluate secondary engagement outcomes (long view, comment/like/gift) without causal claims.
6. Current MemoryFusion is a transparent memory module, not an LLM agent; any later LLM/tool-using phase should be evaluated as an additional layer, not substituted into these frozen results.
