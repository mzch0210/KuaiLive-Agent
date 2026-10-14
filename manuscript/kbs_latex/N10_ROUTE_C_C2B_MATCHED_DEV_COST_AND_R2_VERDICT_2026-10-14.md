# N10-C2B | Source-matched DEV costs and decision-validity verdict

Date: 2026-10-14 | **C2-B real execution PASS; R2 production/latency superiority NOT ESTABLISHED.** CI [#38530526158](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38530526158), both source-syntax and private GTX/RTX3090 hardware jobs SUCCESS, aggregate-only artifact **11878111459**. Source: analysis/kbs_plan_c/n10_c2b_dev_matched_cost.py. Source and results are new **DEV-only post-B4-A system diagnostic**, not a newly collected TEST.

## Matched design and integrity

- Frozen 256 distinct M3 full-active DEV author-ranking requests chosen by fixed linearly spaced positions from the existing original 50,049-request DEV cohort. The same 256 pretarget historical snapshots and TRAIN-known author-availability candidate rosters were reused across all paths.
- Original SASRec seed 20261012 Base checkpoint SHA: 18fb25d68970e73661a4b1418f5be05e7f8bed678d097533adf3cf1d9964d17e. Original G3/E2 DEV-fixed SASRec Utility gate; 12 pre-outcome features and existing threshold, neither retrained nor recalibrated. DEV corrected event CSV SHA e144d9ed4c155b51a182a58150ea17d797b3eb4ee0dac0475ccba1d34f277e8f. Original G1 protocol SHA bf6234eb95ecb24a568b2e7556846c41c4f3e1fdcd7774397003beaf56341a3c.
- Frozen causal-history snapshots taken **before current DEV event** and exact feature history-support parity checked. Full-F roster built by the target-blind interval sweep without passing the target author as an input. All three paths share each request's exact candidate roster.
- Base and Memory each rank the same candidate tokens. Utility chooses one of those two outputs, audited for all 768 repeated requests. No model training, resampling, seed selection or TEST metric recomputation.
- Three repetitions x 256 requests; within each request the path order is cyclically counterbalanced to reduce systematic warm-cache ordering bias. CUDA explicitly synchronized before and after each scored path; warmup excluded. GPU NVIDIA GeForce RTX 3090, PyTorch 2.4.1+cu124.
- **Important source-scan qualification:** The original source G3 history replay physically projects the G1 causal-stream author column while scanning TRAIN/DEV/TEST-tagged rows. It explicitly **skips split=TEST rows before updating DEV history state**, and does not read B4-A private A1/A4 files or compute any TEST metric. Thus the correct claim is *no B4-A target-outcome use*, not 'no bytes of a TEST-tagged Parquet column were ever projected'.
- The exact per-event sampled ranks are retained only inside the code's ephemeral memory for parity; artifact publishes only aggregate times and an irreversible digest, not viewer/creator/event IDs, scores, history graphs or TEST labels.

## Raw observed repeated warmed request-path times

| Real frozen path | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) |
| --- | ---: | ---: | ---: | ---: |
| Always Base | 0.72759 | 0.72228 | 0.87052 | 0.92766 |
| Always Memory | **0.69165** | **0.65672** | 1.08878 | 1.45743 |
| Frozen Utility selector | **1.76941** | **1.70132** | 2.29003 | 2.52290 |

Utility chose the Memory output 240 times over 768 repeated path invocations, exactly **80/256 = 31.25%** of distinct requests. The difference in mean elapsed path time between Utility and Always Memory is +1.07776 ms/request in this DEV design (Utility ~2.56× the Always Memory mean). Do not translate to production cost ratios or independent 768-user confidence intervals; the repeated timings share only 256 requests.

**Selector-path measured components** (descriptive means per 768 request invocations):
- Base forward/candidate score: 0.49876 ms.
- Observable feature extraction: 0.37267 ms.
- Pointwise frozen HGB prediction: 0.55889 ms.
- Conditional Memory scoring averaged across all calls and skips: 0.13205 ms.
- Combined whole-select path: 1.76941 ms. Do not overinterpret differences between stage sums and whole-path totals; feature/ranking/Python overhead and GPU synchronization are additional and overlapping in a staged measurement.

**Source-preparation cost (reported separately, NOT online per-request latency):**
- Full 30,307,513-row G1 causal history scan and DEV snapshot materialization: **36,365.796 ms over the batch**.
- Full interval-source sweep constructing 256 target-blind active F rosters: **10,808.702 ms over the batch**.
- Warmup: 156.526 ms, excluded.
- Source scans have batch amortization, I/O, and cold-cache characteristics, not the same cost semantics as stateful incremental streaming. Their totals must not be divided by 256 and called production end-to-end per-request cost.

Hardware resource context (descriptive, not economic cost): peak CUDA allocated **254,739,968 bytes**, process max RSS **2,003,344 kB**. The report does not measure production throughput, online live roster incrementality, external permission/invocation penalties, network/queueing, concurrent batching, monetary cost, or energy. The original G4 warmed one-pass result (Always Memory ~0.803ms; Utility ~1.802ms; Base ~1.425ms) likewise favored Memory over Utility; numerical discrepancies in Base timings are plausibly linked to counterbalanced warmup/order differences and should not be called model speedups.

## R2 scientific adjudication

**Empirically demonstrated:** the value-based selected strategy can improve Full-F ranking quality relative to a fixed Base and several comparator selection policies **under a stipulated specialist-invocation cap**. On same-period additional frozen B4-A targets, F-aligned vs S-aligned supervision had better NDCG and fewer *realized* calls, but not strictly matched call rates. On 50,049 DEV the hypothetical zero-gate-overhead shadow-price frontier shows contingent allocations: its lambda is **expected NDCG per Memory call**, neither ms nor dollars.

**Not demonstrated:** practical net throughput gain, real-world costs, latency dominance, or deployment savings over simply using fixed Always Memory. In this particular frozen G3/E2 Utility implementation the offline warm request path is actually slower. Since the experimental Memory algorithm is also consistently stronger in unconstrained M3 full-F ranking, operational justification requires independent evidence of external call scarcity, permissions or serving tradeoffs.

**C4/R2 recommended claim:** 'Pre-outcome estimates of incumbent-relative memory ranking value improve the allocation of a fixed memory specialist under an explicitly specified invocation count restriction; this evidence establishes *decision quality conditional on a hypothetical operational restriction*, not measured production efficiency.' New requests for economically motivated Memory calls require separately evidenced constraints.

**Important relevance bound:** This C2-B times the original G3/E2 SASRec Utility gate, **not the newer B4-A F-aligned HGB policy**, GRU4Rec, batched vectorized HGB routing, or production scheduler. It is evidence against broad unqualified efficiency assertions, not a theorem that every possible future implementation of a selective policy must be slower. Proper counterbalanced batch/online studies of F-aligned are future work if real cost saving becomes central to the paper.

## C2-B disposition

**COMPLETE FOR THE PLANNED R2 EVIDENCE REVIEW:** new source-matched device benchmark with fixed freeze, exact candidate parity, separated setup, mean/P95, and transparent negative finding. More optimized production serving measurements should not be run merely to produce a favorable narrative; C4 can now use the measured negative and constrain the paper accordingly.
