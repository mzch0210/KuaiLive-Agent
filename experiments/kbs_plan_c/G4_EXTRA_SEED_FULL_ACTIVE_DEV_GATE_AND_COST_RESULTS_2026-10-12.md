# Plan C G4 — three-seed full-active DEV Utility robustness and warmed cost audit

**Status:** G4 complete for the planned six independently trained author-level Base checkpoints; **TEST remains locked**. Real production/online serving-cost claims are **not** established, although an honest warmed DEV microbenchmark is available.

## Audit sources and reproducibility

- [G4 extra-seed full-active Base scoring #38222994275](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38222994275) — **success**, artifact `11735102444`, four new Base rank panels on exactly **50,049** DEV events using identical source candidates and the **same corrected** Memory scores.
- [G4 independent extra-seed five-policy OOF freeze #38223562473](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38223562473) — **success**, artifact `11734898639`; each model uses the same user-disjoint 5-fold method and pointwise max-30%-call DEV threshold protocol.
- [G4 warmed serving-path cost #38223495966](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38223495966) — **success**, artifact `11734923392`; 256 fixed DEV events, correct real-data sparse pre-gate feature parity, no TEST observations or re-training.
- Prior main seed source/selection: [G3/E2 accepted DEV report](G3_E2_DEV_RESULTS_REVIEW_2026-10-12.md).
- Full G4 source outputs remain on private User-host. Source frozen G1 protocol SHA256 `bf6234eb95ecb24a568b2e7556846c41c4f3e1fdcd7774397003beaf56341a3c`; old corrected DEV pair SHA256 `e144d9ed4c155b51a182a58150ea17d797b3eb4ee0dac0475ccba1d34f277e8f`.
- All DEV data were reused; **no TEST file opened** in these runs. The 20261013/14 models were fit with distinct training seeds and chosen checkpoints on the same 4,096 × 575 panel **before** their full-active DEV evaluation.

## 1. Memory advantage across six independent Base fits

| Family | TRAIN seed | Full-active DEV Base NDCG@10 | Same Memory NDCG@10 | Memory − Base |
|---|---:|---:|---:|---:|
| SASRec | 20261012 | 0.258167 | 0.343509 | **+0.085342** |
| SASRec | 20261013 | 0.258210 | 0.343509 | **+0.085300** |
| SASRec | 20261014 | 0.258777 | 0.343509 | **+0.084732** |
| GRU4Rec | 20261012 | 0.258971 | 0.343509 | **+0.084538** |
| GRU4Rec | 20261013 | 0.262965 | 0.343509 | **+0.080544** |
| GRU4Rec | 20261014 | 0.259072 | 0.343509 | **+0.084438** |

All six full-active DEV paired differences are positive. **Memory is a fixed, shared comparator**; the six numbers above are correlated through the same users, memory and candidate events. They are neither six independent data replications nor six independent significance tests. All models share the same TRAIN events and hyperparameters; only model initialization/training randomness differs.

## 2. Utility routing consistency at identical max-30% DEV calls

| Base family / seed | Utility NDCG@10 | Uncertainty NDCG@10 | Difficulty NDCG@10 | Utility − strongest non-Utility |
|---|---:|---:|---:|---:|
| SASRec / 20261012 | **0.302764** | 0.288516 | 0.282508 | **+0.014248** |
| SASRec / 20261013 | **0.302316** | 0.287290 | 0.281900 | **+0.015026** |
| SASRec / 20261014 | **0.302619** | 0.287922 | 0.283069 | **+0.014697** |
| GRU4Rec / 20261012 | **0.303531** | 0.288866 | 0.283805 | **+0.014665** |
| GRU4Rec / 20261013 | **0.304125** | 0.292028 | 0.286580 | **+0.012097** |
| GRU4Rec / 20261014 | **0.303103** | 0.289003 | 0.284075 | **+0.014100** |

Specialist-quality and History comparators were also executed and are below Uncertainty for all six fits. The ranking **Utility > Uncertainty > Difficulty > Specialist > History** is exactly the same for all six. Pointwise gate thresholds are frozen from *user-group-disjoint OOF DEV predictions*, but thresholds were selected on the same OOF DEV outcomes. Thus these are **discovery-phase conditional** improvements: without an independent TEST we must not state holdout significance or population generalization.

Three-seed mean ± sample SD, two architectures evaluated separately:

| Metric | SASRec (mean ± sample SD) | GRU4Rec (mean ± sample SD) |
|---|---:|---:|
| Always Base | 0.258385 ± 0.000340 | 0.260336 ± 0.002277 |
| Utility selected | **0.302566 ± 0.000229** | **0.303586 ± 0.000513** |
| Strongest comparator Uncertainty | 0.287909 ± 0.000613 | 0.289966 ± 0.001787 |

Three-seed variability is **descriptive**; this does not justify a seed-level t-test with `n=3` given correlated evaluation cases. Final preregistered three one-sided utility contrasts plus Holm must be evaluated on the independent TEST.

## 3. Real 3090 warmed DEV replay cost: negative net efficiency result

The separate source-confirmed benchmark timed **256** deterministic DEV events on the same single RTX 3090 with the primary-seed SASRec Base and DEV-frozen Utility policy (80 specialist calls; realized event subsample rate 31.25%). It also verified that the sparse history-support gate feature was numerically equivalent on all 256 real sampled DEV histories/candidate panels.

| Path | Mean ms per event | Median ms per event | p95 ms per event |
|---|---:|---:|---:|
| Always Base | 1.4245 | 0.8317 | 1.1797 |
| Always Memory | **0.8033** | **0.7744** | 1.2505 |
| **Utility selective** | **1.8018** | **1.6778** | 2.7046 |
| Pre-gate sparse/summary feature assembly only | 0.2395 | 0.2380 | 0.3572 |
| Gate inference only | 0.6207 | 0.6201 | 0.6597 |

**Crucial finding:** The complete selective path is **slower** than the fixed Memory-only path under the stated warmed replay conditions even though expert calls occur less often. The sparse gate feature improves internal compute feasibility but does **not** make a 30%-call policy automatically faster. The current performance objective should be phrased as **decision quality subject to a specialist-call limit**, with honest explicit per-request overhead, not as empirically demonstrated speed/cost reduction.

**Latency caveats:** This is a 256-event warmed **offline replay** with fixed pre-existing per-user causal state and active author candidate data. The source manifest excludes historical user-state maintenance, room availability construction, IO/network, batching/scheduling and GPU contention. Warmup/order effects exist (the Base-only mean is inflated relative to its median and to the second Base invocation in the selective path); compare full paths qualitatively rather than treating mean ratios as production-valid speedup estimates. It is *not* a defensible production end-to-end latency number. A follow-up counterbalanced benchmark, if publication cost claims are central, is justified.

## 4. Research audit and acceptance decision

- **G4 full-active multi-seed Base/Memory and five-route DEV science:** **PASS**.
- **Sparse support-feature functional equivalence on real histories:** **PASS** (n=256).
- **Exploratory serving-cost analysis:** **COMPLETE** with a negative result; actual production latency/cost reduction claims **unsupported**.
- **E1/E2/E3 on untouched TEST:** **NOT EXECUTED** (47,575 frozen event cohort). Independent confirmation remains the decisive next gate.
- **Original old Twitch and old KuaiLive evidence:** unchanged; do not retune.
- **G5 next:** freeze *all* six checkpoint hashes and final gate model/threshold hashes; verify pretarget-only features and candidate policy in a synthetic TEST harness, then perform **one-shot TEST**, reporting Always Base, Always Memory, Random@30 expectation, each frozen selector, hindsight nondeployable Oracle, per-user paired CIs and preregistered Holm-corrected three contrasts. Preserve all negative or insignificant comparisons.

**KBS positioning:** stronger empirical support for **relative-utility-based invocation decisions at a specified call budget**, rather than a general speedup claim or unconditional NDCG dominance over Always Memory.
