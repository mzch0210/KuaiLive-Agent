# Supplementary S9 — Computational resource and efficiency evidence (staged draft)

**Status:** Source-checked supplementary **draft**, not yet formatted or incorporated into the submitted supplement. This record retains numerical details deliberately condensed from canonical Section 6.5.  
**Draft date:** 2026-10-09.  
**Scientific baseline:** [KBS formal efficiency run 35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758) and [gate-compression run 35571827672](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35571827672); the tested selection policy in this table is *KuaiLive*, not the independently frozen Twitch selector.

## S9.1 Experimental conditions

The main controlled-scoring benchmark uses KuaiLive 575-candidate sampled-active room recommendation, a two-branch (Room/Streamer) Dual-ID SASRec Base, history cap `L=50`, embedding dimension `d=64`, and 14 pre-outcome selector features. Inference is CPU-only, single thread, batch size one. Three GitHub-hosted CPU replicas each run 1,200 warmed queries (3,600 timing observations per model/pipeline); the sampled queries are deterministic within a replica. Hardware is **not homogeneous across replicas**; the benchmark reports pooled descriptive estimates and does not identify population-level hardware variability. Candidate feeds, user-level history descriptors and cache state were materialized before timing. Loading, feature-cache rebuild, updating relationship state, network I/O, queuing and concurrency were not measured.

The executable source is [`analysis/gate_compression_latency.py`](../../analysis/gate_compression_latency.py), which actually executes the fitted gate predictor as part of the selective pipeline. Crucially, its branch decision uses the **precomputed frozen test route mask**, not the new predictor output computed during timing. This isolates the runtime path for prespecified decisions but is not a test of fully autonomous online gating correctness. The individual gate-only microbenchmark uses preconstructed input vectors; its latency cannot simply be added to selective-pipeline timing to reconstruct full latency.

## S9.2 Same-panel KuaiLive cost comparison

| Pipeline / component | Memory invocation share | Mean latency (ms) | P50 (ms) | P95 (ms) |
|---|---:|---:|---:|---:|
| Dual-ID Base | 0% | 0.990585 | 1.039273 | 1.275783 |
| Selective HGB | 14.2536% | 2.006624 | 2.026013 | 2.904929 |
| Selective Ridge | 30.9920% | 1.387248 | 1.290124 | 2.147706 |
| Selective Tiny-MLP | 10.3698% | 1.271907 | 1.277168 | 2.039375 |
| HGB prediction only (precomputed features) | Not applicable | 0.617416 | 0.671539 | 0.697656 |
| Ridge prediction only (precomputed features) | Not applicable | 0.002422 | 0.002404 | 0.002675 |
| Tiny-MLP prediction only (precomputed features) | Not applicable | 0.005755 | 0.006092 | 0.006452 |
| Memory scoring (cached state) | Not applicable | 0.490254 | 0.484797 | 0.600424 |

All rows above belong to the **same gate-compression timing panel**, recovered and assembled in successful formal run 35730086758. The 95th percentile is a pooled descriptive percentile, **not** a user-cluster bootstrap confidence interval. The three hosts are not randomized production replicas. End-to-end (warmed scoring pipeline) HGB excess mean latency is `2.0066239936 - 0.9905847453 = 1.0160392483 ms`, equivalent to a **2.025696×** ratio to Base. Means and component measurements are not additively exact because the timed paths and preparatory computations differ.

**Policy-utility comparability limit:** HGB, Ridge and Tiny-MLP here use different learned decisions and different Memory invocation frequencies. The companion gate-compression accuracy frontier reports distinct TEST NDCG gains, so lower Ridge/Tiny-MLP latency is not an independently established **fixed-policy, fixed-budget, equal-utility** efficiency improvement. An equal-quality latency claim requires predeclared matched invocation budgets, selection-policy retraining/freeze rules and paired evaluation on the same query workload.

## S9.3 Distinct historical benchmark (do not combine with S9.2)

The older inference-latency benchmark, reaggregated from available replica artifacts by formal run 35730086758, reports **Dual-ID mean 0.760784 ms**, **frozen 14.25% selective HGB mean 2.336902 ms**, and pooled P95 **1.259947 / 3.173842 ms**, respectively. These measurements originate in a **different benchmark path**; their respective means must not be paired with S9.2 rows when calculating overhead. Original workflow 35559499838 had failing/skipped stages, but the later successful formal aggregation explicitly recovered the archived per-replica timing outputs; the formal aggregation and its immutable inputs, not the original workflow's overall status, are the evidence record. Do not report this older comparison in the main text except with explicit provenance.

## S9.4 Complexity with stated assumptions

Let `C` be the candidate count, `L` the Base sequence length, `d` the attention embedding size, `F` the number of gate input descriptors, `T` the number of fitted regression trees and `D` their maximum depth. For **two one-layer, standard dense-attention sequence encoders** with a simple candidate-embedding scoring head, a *schematic* forward-pass expression is `O(2(L²d + Ld² + Cd))` (assuming no additional large modules, fixed number of heads and cached embeddings). It is **not** a formal bound for model loading, data materialization, candidate construction, full user-state feature extraction or the surrounding serving system.

Under cached relationship-history maps, specialist candidate scoring is approximately `O(C)` with a separate relationship cache of order `O(R_u)` for per-user relationship entries. Rebuilding these maps or updating them with new user activity is a different operation whose time and memory costs are excluded from the small warmed scoring path. Feature extraction depends on the availability of cached user descriptors and on the candidate score vector; computing Base-confidence statistics generally requires inspecting candidate scores (`O(C)` or more depending on exact order statistics), and should not be treated as free. A trained single-output histogram gradient-boosted tree ensemble with `T` trees and maximum depth `D` requires at most `O(TD)` sequential node visits for ordinary tree traversal per query, excluding feature preparation. The fitted experimental HGB has **81 boosting iterations** with maximum depth 3, and the input contains **14 observable features**. Ridge scoring is `O(F)` for the affine mapping (excluding scaling preparation); a 14–16–1 dense Tiny-MLP forward map is `O(FH+H)` for `H=16`, excluding cache and infrastructure overhead.

The qualitative accounting identity is Base score computation + feature extraction + gate execution + specialist candidate scoring **conditional on the route decision**. An invocation fraction `p` affects only the last term's expected frequency under a fixed workload. Without measurements of the remaining terms and identical policies, the fraction `p` is neither a latency guarantee nor a throughput/GMV/engagement estimate.

## S9.5 File footprint and process memory

| Measurement | Observed value | Meaning / caveat |
|---|---:|---|
| Room + streamer model checkpoint files | 303.851841 MiB | Two serialized model checkpoints, not total process RAM |
| HGB fitted estimator file | 0.104691 MiB | Serialized `joblib` artifact; not per-query activation memory |
| Ridge coefficient/scaler arrays | 0.000328 MiB | Array payload only |
| Tiny-MLP/scaler arrays | 0.002174 MiB | Array payload only |
| Memory relationship cache (serialized) | 4.307323 MiB | Pickled popularity/history objects for the measured dataset |
| Peak resident set (stack materialization probe) | 875.625 MiB | Separate process-level `ru_maxrss` high-water mark, not a per-query increment |

The resident-set probe loaded checkpoint weights, gate artifacts, train/dev files and cached user state. The memory mapping does **not** imply those allocations remain resident identically in production, nor may serialized sizes be summed to reconstruct peak RSS. The test used a distinct measurement phase from latency; results are runtime/environment-specific.

## S9.6 Reproducibility audit and critical exclusions

- Formal run: [35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758), complete [artifact 10694941935](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758/artifacts/10694941935).
- Gate compression: [35571827672](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35571827672), 3 successful replicas and pooled final artifacts.
- Scripts: [formal aggregation](../../analysis/kbs_formal_efficiency.py), [cache probe](../../analysis/kbs_efficiency_stack_probe.py), [gate-compression benchmark](../../analysis/gate_compression_latency.py), and [replica aggregation](../../analysis/aggregate_inference_latency.py).
- Nontransferability: frozen Twitch selection uses 6,650/44,221 = **15.04%**, official LiveRec Base and availability-aware streamer candidates. **No Twitch end-to-end latency was measured**, so KuaiLive milliseconds are not transferable to it.
- Selection-mask replay, cache assumptions, heterogeneity of hosts and absence of queueing, online feature recomputation or network I/O prevent deployment-level SLAs or claimed cost reductions.
- This is **staged Supplementary S9 material**, not a claim that an Elsevier-ready supplemental PDF has been assembled or approved.
