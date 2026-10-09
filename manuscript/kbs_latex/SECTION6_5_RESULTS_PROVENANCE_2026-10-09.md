# Section 6.5 — Computational Considerations: primary evidence and interpretation audit

**Date:** 2026-10-09  
**Canonical manuscript:** [main.tex](main.tex), Section 6.5 (`sec:results-efficiency`), new Table `tab:results-efficiency`.  
**Manuscript insertion commit:** [86aa425b](https://github.com/mzch0210/KuaiLive-Agent/commit/86aa425ba8dd032c13d34106a6c723907e33b43d).  
**Research status:** New scholarly first draft using **pre-existing** efficiency measurements; no newly trained models, rerun timings, or revision of frozen Twitch TEST selection. This is not a reviewer-tightened subsection or coauthor-approved submission text.

## Primary source and permitted inference

- The formally completed source is [KBS formal CPU complexity/efficiency run #35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758) (job `106753206152`; successful; [formal evidence artifact 10694941935](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758/artifacts/10694941935)). The source scripts are [formal aggregation](../../analysis/kbs_formal_efficiency.py), [stack-memory probe](../../analysis/kbs_efficiency_stack_probe.py), and the [hosted workflow](../../.github/workflows/kbs-formal-efficiency-hosted.yml).
- The principal Table 7 latency panel uses **the gate-compression benchmark measurements**, assembled in that run from [run #35571827672](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35571827672), with three successful replicas and frozen KuaiLive scientific gate masks. The timed implementation is [`analysis/gate_compression_latency.py`](../../analysis/gate_compression_latency.py). The formal aggregator also contains an **older, separate latency panel** from archived replica artifacts, whose Base/HGB values are 0.76078/2.33690 ms; **never mix these two timing panels as if from the same benchmark**.
- **Scope:** 575-candidate KuaiLive sampled-active room ranking, two Dual-ID SASRec branches, maximum history 50, 64-dimensional embeddings; preconstructed batch-size-one candidate feeds, precomputed user history/state, warm caches, one PyTorch inference thread; 1,200 timed single-query observations per replica, three GitHub-hosted CPUs. Reported P95 is the pooled sample 95th percentile, not a bootstrap confidence bound or an SLA. Model-loading, dataset parsing, history rebuilding, cache refresh, network transfer, and production concurrency are outside the timed section.
- The benchmark executes real gate inference within each selective-query measurement but chooses specialist usage from a **replayed, previously computed scientific route mask** rather than applying the freshly computed prediction to take the branch in the timed loop. This ensures the scientific budget decisions are consistent; it does not by itself prove identical behavior in an online serving system.
- The frozen **Twitch** policy from [Section 6.2](SECTION6_2_RESULTS_PROVENANCE_2026-10-09.md) invoked 6,650 / 44,221 Memory choices (15.04%), on a different dataset and official LiveRec Base. It was **not** timed by the KuaiLive CPU benchmark, whose HGB policy called Memory 14.2536% of the events in that protocol. Invocation rates on the two platforms must never be equated.

## Main-table source values (single, matching timing panel)

| KuaiLive pipeline | Memory call rate | mean latency, ms | pooled P95, ms |
|---|---:|---:|---:|
| Dual-ID Base | 0 | 0.9905847453 | 1.275783 |
| Selective HGB | 0.142536 | 2.0066239936 | 2.904929 |
| Selective Ridge | 0.309920 | 1.3872480322 | 2.147706 |
| Selective Tiny-MLP | 0.103698 | 1.2719066392 | 2.039375 |

The HGB stack's **measured excess latency** is `2.0066239936 - 0.9905847453 = 1.0160392483 ms`; the **latency ratio** is `2.025696`. Within the **same current gate-compression timing panel**, the fitted HGB gate's prediction-only mean is `0.6174156514 ms`, and the cached Memory lookup alone has mean `0.4902538906 ms`. These are separately measured operations; do not claim their sum exactly reproduces the full selective stack.

The lower Ridge/Tiny-MLP means do not hold decision behavior, Memory call rate or NDCG gain fixed; they are **different learned rules**. Do not present this as a drop-in quality-preserving acceleration of the frozen Twitch Utility model or infer that one gate is universally more efficient.

## Formal complexity and memory provenance

- KuaiLive Dual-ID computation: two one-layer SASRec encoders and candidate scoring; the formal implementation writes `O(2(L^2 d + L d^2 + Cd))` as an illustrative per-query expression.
- Cached relationship Memory candidate scoring: `O(C)` after cache construction, with `R_u`-dependent user relationship state and additional cache maintenance costs.
- HGB: 14 observable features; `n_iter_=81` fitted trees and maximum depth 3 in this benchmark; prediction traversal roughly `O(TD)`, with architecture/code/hardware-dependent constant factors.
- Two frozen Dual-ID checkpoint files occupy **303.851841 MiB**, the HGB serialized estimator **0.104691 MiB**, and the serialized popularity/history cache **4.307323 MiB**.
- The separate process-loading probe reached **875.625 MiB peak resident set size**, including interpreter/imports, dual weights, gate artifacts and materialized cached user state. This is a process/runtime measurement, **not** the serialized cache footprint, resident GPU memory, or an inherent architecture constant.
- The actual online work is at least Base inference plus feature extraction, gate prediction and conditional Memory scoring; the **invocation fraction alone does not determine wall-clock cost**.

## Writing/claim guardrails

1. Lead with the distinction between frozen Twitch TEST Memory invocation **15.04%** and unmeasured Twitch latency.
2. Report the selected auxiliary KuaiLive timing panel coherently: Base **0.991 ms** vs. Selective HGB **2.007 ms**, with latency **increasing**, not decreasing. The original outline mentions **0.76 ms / 2.34 ms**, which belongs to a distinct legacy panel and is not mathematically inconsistent. If that older pair is later quoted, identify it as such rather than blending metrics.
3. The equal-rate condition does **not** apply to Ridge/Tiny-MLP; comparison is illustrative, not a matched-utility cost frontier.
4. No measured online deployment, GMV or engagement lift, service-level throughput/cost reductions, device-independent latency or cross-dataset timing generalization is asserted.
5. The main text confines itself to one short experiment table and directly relevant cost interpretation; full hardware, train-grid, accuracy--latency, memory and artifact SHA details are candidates for the later efficiency supplement.
6. The final 6.5 source was inserted before the bibliography hook. Earlier Sections 1--5 and 6.1--6.4 were preserved byte-for-byte; Section 7, Section 8 and Abstract are still unwritten.

**Build and review gates:** The exact Section 6.5 insertion commit [86aa425b](https://github.com/mzch0210/KuaiLive-Agent/commit/86aa425ba8dd032c13d34106a6c723907e33b43d) passed [GitHub Actions PDF build #37948687922](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37948687922), uploading [PDF/log artifact #11625220289](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37948687922/artifacts/11625220289). The matching LaTeX log reports a 28-page PDF and no new overfull line for 6.5; the earlier-section overfull line (5.51282 pt, lines 141–142) persists. The final source includes no 6.5 reviewer-style revision yet. Rendered-PDF visual inspection, independent KBS reviewer-style tightening, supplement assembly and coauthor sign-off remain pending. Compilation is not final typographic approval.
