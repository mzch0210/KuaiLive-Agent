# KBS Plan C: Completion Audit and DEV Budget-Reference Results

**Date:** 2026-10-12  
**Canonical preregistration:** [G0F_PRETEST_PROTOCOL_2026-10-12.json](G0F_PRETEST_PROTOCOL_2026-10-12.json)  
**Scope:** New KuaiLive-M3 author-ranking under a global time-forward split; baseline models SASRec and GRU4Rec; frozen TEST cohort `47,575`. **None of the submitted M3 findings is yet an independent TEST outcome.**

## Executive conclusion

- Data engineering, fixed benchmark cohort, one-seed dual-Base training, full-active paired DEV and fair five-gate DEV OOF evaluation: **complete**.
- 20-seed deterministic Random@budget references, non-deployable budget-matched hindsight Oracle and descriptive budget curves: **complete** from already cached E2 DEV event labels and OOF predictions; no Base re-scoring required.
- Prespecified additional model seeds **20261013** and **20261014**: **TRAIN launched**, not yet accepted. Serial run [#38214570522](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38214570522); previously chosen hyperparameters and train-only index reused. [DEV checkpoint screen](../../.github/workflows/kbs-plan-c-e3-extra-seed-dev-selection.yml) configured to execute on successful train completion; it is **not** independent full-active DEV paired-utility replication.
- Computational-cost interpretation: sparse exact replacement for history-supported author candidate fraction **unit-test verified** [#38214776398](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38214776398), but production gate integration and real measured end-to-end selected-vs-always-Memory latency **not complete**.
- Definitive E1/E2/E3 confirmatory **TEST** and Holm-corrected user-cluster comparisons **not executed**. DEV policy thresholds were optimized on OOF DEV outcomes, so DEV bootstrap intervals are conditional.

## Source-of-record run list

| Purpose | Evidence | State |
|---|---|---|
| G0 source SHA, room/time/cohort audit | [#38203111463](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38203111463) | pass |
| G1 global time split and immutable DEV/TEST panels | [#38204470450](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38204470450) | pass |
| G1 DEV active warm-author candidate feasibility | [#38204794887](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38204794887) | pass |
| G2 first-seed dual neural Base fit | [#38205618676](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38205618676) | pass |
| G2 first-seed DEV model selection | [#38208337267](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38208337267) | pass |
| G3 full-active DEV Base and corrected Memory | [#38211598562](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38211598562), [#38212426384](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38212426384) | pass |
| E2 five DEV user-group OOF comparators | [#38212894692](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38212894692) | pass |
| E2 user-cluster conditional DEV bootstrap | [#38213440850](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38213440850) | pass |
| **NEW:** DEV random/budget Oracle frontier | [#38214257313](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38214257313), artifact `11731390590` | pass |
| **NEW:** sparse pre-gate feature exact synthetic parity | [#38214776398](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38214776398) | pass |
| **NEW:** two new prespecified train seeds | [#38214570522](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38214570522) | running when recorded |
| Future: full-active alt-seed paired ranking, DEV gate freeze | new workflow/result required | pending |
| Future: one-shot independent TEST and Holm three preplanned contrasts | scientific G5 | pending |

No original Twitch 44,221-event TEST or previously inspected original KuaiLive 10,222-event TEST was retuned for this Plan C.

## New budget-matched DEV results

Source: [#38214257313](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38214257313), `kbs-plan-c-e2-dev-budget-matched-v1`, 50,049 events, 20 prespecified Random draw seeds `20261012`–`20261031` at each budget. References are computed on the **same DEV paired outcome array**, **not TEST**. Hindsight Oracle uses realized positive per-event utility and is neither a deployable policy nor a frozen gate.

| DEV, 30%-cap policy or bound | SASRec Base | GRU4Rec Base |
|---|---:|---:|
| Always Base, 0% call | 0.258167 | 0.258971 |
| Uniform Random@30, exact conditional expectation | **0.283769** | **0.284332** |
| DEV-frozen pointwise Utility (29.993% actual calls) | **0.302764** | **0.303531** |
| **Hindsight budget Oracle@30 (up to 15,014 calls)** | **0.387544** | **0.390569** |
| Unrestricted hindsight Oracle (all positive relative-utility calls) | **0.387622** | **0.390634** |
| Always Memory, 100% calls | **0.343509** | **0.343509** |

The budget-matched upper bound is much more informative than comparing a 30%-budget gate to an unconstrained Oracle. Under the frozen budget, Utility recovers only **34.47%** (SASRec) and **33.86%** (GRU4Rec) of available hindsight Oracle incremental NDCG over Base on DEV; potential improvement in routing remains substantial. Calling every specialist yields higher mean NDCG but is a different and potentially more expensive budget.

**Random@30** is now represented both by its exact conditional expected value and 20 fixed-seed realization diagnostics; it must not be mislabeled as a pre-existing deployable stochastic policy in the original frozen five-gate comparison. **Utility top-k score budgets beyond 30%** are retrospective DEV rank-based curves, **not** a family of newly frozen pointwise deployment thresholds.

A summary of score-ranked DEV top-k Utility curves (descriptive, not independent) follows:

| Event call budget | SASRec Utility top-k DEV NDCG | GRU4Rec Utility top-k DEV NDCG |
|---|---:|---:|
| 10% | 0.278154 | 0.278819 |
| 20% | 0.291719 | 0.293022 |
| 30% | 0.302764 | 0.303531 |
| 50% | 0.319463 | 0.320271 |

These numbers do not supply a real-time production latency measurement. Do not infer a 70% Memory computation reduction from 30% invocation rate: the existing DEV pipeline materialized candidate-related Memory features ahead of the routing decision.

## Original protocol versus actual completion

The following **10 deliverables** form an explicit, non-weighted bookkeeping decomposition of the frozen scientific gates and later methodological improvements; the count is **not** a scientific success percentage.

| # | Planned deliverable | Observable completion | Status |
|---:|---|---|---|
| 1 | G0 verifiable independent-period source and timestamp integrity | source pinned and source checksum verified; independent *collection period*, not verified person-disjointness | **complete** |
| 2 | G1 globally chronological TRAIN/DEV/TEST, eligible active authors, fixed candidate roster | TRAIN 24,995,148; DEV panel 50,049; TEST panel 47,575 sealed | **complete** |
| 3 | G2 first seed SASRec and GRU4Rec fitted + fair DEV checkpoint screen | both complete, epoch 3 selected for both models | **complete** |
| 4 | G3 strict-prior full-active DEV Base/Memory pair, consistent fixed Memory formula | corrected all-history Memory, 50,049 paired DEV events | **complete** |
| 5 | E2 Utility/Difficulty/Specialist/Uncertainty/History user OOF and frozen 30% DEV policies | 12,628 users, both Base families, 5 fair objectives | **complete** |
| 6 | E2 budget-matched Random/Oracle references and conditional clustered DEV uncertainty | references, 5000 cluster bootstrap and 20 fixed Random draws computed | **complete** |
| 7 | E3 preregistered extra 2 train seeds and selected DEV checkpoints | new training workflow dispatched; same DEV screen wired after success | **in progress** |
| 8 | pre-gate feature cost de-circularization and measured production-style latency | sparse history-share equality passed; **not integrated or latency-benchmarked** | **partial** |
| 9 | G4 full-active DEV paired utilities and independently DEV-frozen gates across additional seeds, complete full production gate protocol | primary seed two architectures complete only; extra-seed paired DEV and gate freeze missing | **not complete** |
| 10 | G5 one-shot sealed TEST (47,575), fixed thresholds, paired user bootstrap and preregistered Holm correction | **No TEST effect score run** | **not started** |

**Bookkeeping:** 6 completed, 2 partly executed/in progress, 2 not completed or not started. These stages have very different scientific importance: the missing independent TEST cannot be replaced by any count or by positive DEV results.

### E1/E2/E3 science-package completion (not a percent)

- **E1** — New-period independent confirmation: dataset, split, model and gate ready on DEV; **TEST confirmation missing**. **Partial.**
- **E2** — Competing selector objectives: five fair DEV OOF policies, budget references and conditional DEV intervals ready for two Bases; **frozen TEST application and independent three-primary-contrast inference missing**. **Partial.**
- **E3** — Robustness to alternate learned Base: two distinct Base architectures complete on primary seed, extra two preplanned seeds dispatched; **extra-seed DEV relative-utility gate freeze and TEST robust comparisons missing**. **Partial.**

## Academic safeguards and remaining decision risks

1. **DEV-only optimism:** OOF predictions are user-disjoint but thresholds were optimized on the same OOF labels. Nested/bootstrap-freeze uncertainty does not become independent evidence without untouched TEST.
2. **True cost ambiguity:** The `x_memory_history_supported_share` feature can mathematically be obtained by sparse intersection of prior known-author keys with the sorted active author roster, with no full Memory scoring. Source: `analysis/kbs_plan_c/g4_sparse_gate_features.py`; corresponding GitHub-host unit-test run [#38214776398](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38214776398). This is **exact functional equivalence on synthetic invariance cases**, not yet a timed production feature implementation or complete pipeline equivalence on all 50,049 DEV rows.
3. **Always Memory effect:** Fixed Memory outperforms first-seed Base and budgeted Utility on M3 DEV. This reinforces importance of treating expert budget as an explicit objective and reporting budget-matched outcomes; it does not prove a cost saving.
4. **Task/domain comparability:** M3 is author-level full-active warm-candidate ranking and a March 2026 collection window; old paper's original KuaiLive is room-ranking and a May 2025 window. These are not identically distributed benchmarks and may contain some of the same underlying anonymous people.
5. **Protocol audit disclosure:** The G0F prose specified a hash field `timestamp_ms`, whereas G1 used DuckDB's typed timestamp representation. Selected DEV and TEST cohort bytes are frozen and labeled accordingly. Preserve this execution variance and avoid retrospective "preregistration perfectly matched" claims.
6. **Computational evidence:** G3 full-active DEV two-Base batch scoring used ~339.4 s; corrected Memory-only history replay used ~313.2 s, **not directly comparable per-request latencies**, because the two pipelines have different preprocessing/shared overheads.
7. **Further E4 candidate-regime manipulation** and **E5 runtime budget realism**, if included in the broader proposal, are extensions not yet fully executed. G2 575-candidate checkpoint screening is not an E4 full paired Memory candidate sensitivity experiment.

**Next acceptance gate:** finish both preregistered seed fits and DEV checkpoint screens, then select/cache their matched full-active DEV Base-vs-Memory utilities under unchanged history/roster protocol and freeze per-Base utility policies; independently time the sparse-gate pipeline. Only after checking gate feature exact parity, candidate identity, cost disclosure, all hypotheses and fixed policy thresholds should G5 one-shot TEST be performed. No TEST-guided retry or threshold change.
