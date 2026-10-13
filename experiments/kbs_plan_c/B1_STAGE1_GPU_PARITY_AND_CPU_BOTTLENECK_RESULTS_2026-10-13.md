# B1 Stage 1 — exact corrected-DEV score parity and GPU/CPU throughput audit

**Date:** 2026-10-13. **Evidence status:** post-G5 DEV exploratory, **B1-1 PASS**. The B1-2 full DEV candidate-label generation and B1-3 nested selection-policy comparison **have not been performed**. All existing N8 manuscript, S1–S9 and G5 TEST evidence remain unchanged.

## Provenance

- Actual successful [GitHub Actions #38363722383](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38363722383), source commit `d0fe8ec40d86eeba7f519e3123e9fdeee5b3da28`, hosted safety and self-host pilot both SUCCESS.
- Source: `analysis/kbs_plan_c/b1_dev_regime_pilot.py`; deterministic **128 time-spread corrected DEV** events, frozen SASRec and GRU4Rec seed 20261012, original all-history-corrected Memory score, same frozen full-active roster.
- Aggregate artifact: GitHub Actions ID `11795409087`, file `summary.json` SHA256 **`9443eae52b6adb0abb18552d2fc6d2011adf19c6d30347713676b0982da299b5`**. The aggregate was independently downloaded and parsed, not inferred from CI summary. No private users, event IDs or candidate scores were published; G5 TEST was not opened and no model was fitted.
- The first run [#38363446623](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38363446623) computed **zero** rank errors but mistakenly raised a failure because Python treated the nonempty `errors` dictionary as truthy even when its values were all zero. The condition was fixed to `any(errors.values())`, and the rerun passed. This was **an acceptance-script bug, not a ranking mismatch**.

## A. Exact ranking identity

| Criterion | Actual result |
|---|---|
| Selected DEV evaluation events | 128 (fixed time-spread indexes) |
| Full-active author candidate count | 14,723–53,738 |
| Offline sampled active authors | Exactly 575, target-retained **only as evaluation label** |
| SASRec full-active rank disagreement vs corrected frozen DEV | **0** |
| GRU4Rec full-active rank disagreement vs corrected frozen DEV | **0** |
| Fixed corrected Memory full-active rank disagreement vs corrected frozen DEV | **0** |
| Frozen checkpoint provenance and corrected DEV source SHA | Verified |
| Private identity upload / G5 TEST access / model training | **No / No / No** |

**This passes the hard B1-1 parity gate, not the B1-3 scientific decision-effect gate.**

On the same 128 DEV events, the mean NDCG@10 values are:

| Ranker | Full-active | Target-retained sampled (575) |
|---|---:|---:|
| SASRec | 0.216478 | 0.612042 |
| GRU4Rec | 0.232707 | 0.630009 |
| Memory | 0.362053 | 0.718584 |

Accordingly Memory−SASRec NDCG is +0.145574 full versus +0.106542 sampled; Memory−GRU4Rec +0.129345 full versus +0.088575 sampled. These are **selected-pilot observations**, not user-cluster inferential results, not population estimates, and not proof of candidate-induced selector regret or decision recovery. The target-retained sampled construction is a retrospective **label**: no label-dependent sampled score statistics are provided to a deployed gate.

## B. GPU batching performance (real RTX3090)

Warm, synchronized GPU-only FP32 vocabulary GEMM; throughput in event-context vectors scored/s, not end-to-end recommender serving:

| GPU batch | SASRec events/s | GRU4Rec events/s |
|---:|---:|---:|
| 12 | 18,582 | 29,790 |
| 32 | 47,172 | 60,337 |
| 64 | 81,164 | 89,301 |
| 128 | 117,366 | 120,148 |
| 256 | 128,622 | 129,696 |

GPU batch 256 beats batch 12 by **6.92× SASRec** and **4.35× GRU4Rec** pure-GPU throughput under this test. Batch 128 already attains most of the performance without unnecessarily large temporary tensors. Recorded peak GPU allocation for the 128-event pilot: **1,324.5 MiB**. These are workload-specific measured throughputs, not evidence of total GPU busy percentage or full production savings.

## C. Actual end-to-end wall-clock breakdown

| Phase | Seconds |
|---|---:|
| Frozen Base loading/DEV context encoders | 1.668 |
| All-prior causal history stream replay | **35.758** |
| Activity interval → time-specific live roster | **10.146** |
| Two-Base large-batch GPU full-vocabulary scoring | **0.447** |
| Corrected Memory, sampled/full rank calculation | 0.132 |
| Total (includes microbench/other staging) | 48.933 |

The dominant bottleneck in this **small pilot** is one-time CPU event history/roster I/O rather than GPU kernel throughput. Raising CUDA utilization by performing redundant GPU work is not an optimization; increasing *meaningful scoring events per replayed history/roster* is. The original code's per-event Python sorting was tested separately to see whether it mattered.

## D. CPU roster optimization negative result

- [GitHub Actions #38364127320](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38364127320), source `analysis/kbs_plan_c/b1_fast_roster_dev_check.py`.
- 256 DEV time points, same author identity/order **0 mismatch**, same max-active-room diagnostics.
- Frozen original: **10.826 s**; vectorized active-count/flatnonzero: **10.661 s**, only **1.015×** speedup (~1.5%). Results from aggregate `11796400027`, independently parsed.
- Therefore do **not** make a gratuitous algorithmic change just to optimize Python active-key sorting. A substantial share of the fixed cost lies in streaming room intervals and preparing event-time eligibility; amortize/reuse that scan over the whole DEV cohort.

## E. Efficiency and scientific next-stage contract (B1-2)

1. **Reuse already corrected original full-active DEV ranks and NDCG as the F labels.** The pilot has now independently verified exact frozen-score parity on 128 events. The full F labels are manifest/SHA locked. This avoids recomputing 50,049 × (14k–54k) scores unnecessarily for B1-2.
2. **Run one causal history replay and one time-ordered availability scan for the 50,049 DEV events**, shared by both Base families and sampled-candidate offline outcomes. Retain private event-level derived files only on self-host and refuse overwrites; do not export identities.
3. Generate deterministic 575-candidate target-retained sampled outcome sets; they are **offline metric labels only**. Keep features derived exclusively from full-active pretarget history/eligibility/Base outputs. Do not expose positive target in online gate features or build a fictional prospectively target-retained candidate generator.
4. GPU-score only the sampled candidates in sufficiently large batches (start testing 128/256/512) using frozen item weights, maintain original FP32/tie semantics, and capture GPU-only vs CPU preprocessing separately. Reuse checkpoints and base context representations, without retraining.
5. Only after paired all-DEV S-label cache/sha is validated, run **B1-3** pure S→F vs F→F vs candidate-aware→F within matched user-disjoint outer DEV folds, with strict no-F-label access in the pure S→F training/calibration arm; report natural TEST-like DEV calls and fairness-adjusted budget curves separately. No G5 TEST read.
6. Any B1-3 positive result is **post-G5 exploratory DEV evidence** until confirmed on genuinely fresh unseen data.

**Verdict:** B1-1 **PASS**, GPU workload throughput measured, primary full-pilot CPU bottleneck explained. B1-2 and B1-3 **not yet executed**; R3 knowledge-system contribution remains open until the choice-loss/recovery link is actually demonstrated.
