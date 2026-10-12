# KBS Plan C — G3 full-active DEV checkpoint scoring, Memory protocol correction

**Status (at authoring):** Both frozen G2 Bases have completed full-active DEV scoring on **all 50,049 events**. Provisional Memory scores are **not accepted** because an original-definition discrepancy was discovered before interpreting outcomes; corrected all-history replay was separately launched, preserving the Base ranks. Neither step accessed TEST.

## Base-only authoritative values

| Fixed checkpoint | Full-active DEV NDCG@10 | Full-active DEV HR@10 |
|---|---:|---:|
| SASRec, seed20261012, epoch 3 | **0.2581674381** | **0.3901376651** |
| GRU4Rec, seed20261012, epoch 3 | **0.2589714713** | **0.3915562749** |

A same-event full-active ranking of ~14k–54k warm author candidates (median around 34k) is fundamentally different from the 575-active-author DEV checkpoint selection task, where NDCG@10 was ~0.648/0.651. Avoid comparing the absolute values as if obtained under identical candidate regimes.

**Evidence:** [successful full-active G3 run #38211598562](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38211598562), aggregate artifact `11728824517`; 50,049 valid DEV events; 339.4 seconds reported evaluation runtime. Corresponding event-level rows remain in the private persistent User-host cache, `~/.cache/kuailive-agent-kbs/klm3_g3_dev_fullactive_base_memory_v2`; only nonidentifying aggregates uploaded. Base checkpoint checksums were verified before scoring.

## Memory definition verification and correction (before acceptance)

The **earlier completed Twitch/KuaiLive specialists** count:
- Short: past **10 consecutive historical events** (not last 10 *warm* events), `max exp(-distance/3)` per historical author.
- Long: past author frequency divided by the **maximum over all authors in the user's prior history**, not the maximum among only TRAIN-known candidate authors.
- Train popularity: frozen normalized log count.
- Fixed linear combination: 0.45 Short + 0.45 Long + 0.10 Train popularity.

Exact previous source references: `analysis/liverec_p12_dev_memory.py` (`_build_strict_histories`) and `analysis/room_level_selective_agent.py` (`histories`, `memory_scores`). The initial M3 G3 scorer omitted train-unseen prior authors when measuring recency slots/Long normalization. This was an **implementation mismatch** rather than a potentially adverse scientific result, and it was independently detected by code-level comparison before any adopted Memory results.

### Efficiency-preserving correction

The corrected implementation `analysis/kbs_plan_c/g3_replay_correct_memory.py` replays *all* eligible TRAIN + earlier DEV histories in one streaming pass, representing unknown-to-TRAIN historical authors as recency-slot-consuming zeros and retaining the all-author Long normalization denominator. It then reuses the **unchanged exact** author-roster and SASRec/GRU4Rec ranks from the completed G3 run. No second full-candidate neural Base inference or model fitting occurs. The corrected file is required to pass `kbs-plan-c-full-active-dev-paired-v2` with `memory_corrected_from_all_history=true`; the E2 gate-fitting function enforces that flag and will reject the provisional G3 file.

Corrected workflow: [G3 Memory-only correction](https://github.com/mzch0210/KuaiLive-Agent/actions/workflows/kbs-plan-c-g3-corrected-memory.yml). All corrections and synthetic tests are tracked in Git commits; aborted first attempts are preserved in the Actions run list. Do **not** present initial Memory–Base deltas from G3 v1 as evidence.

## Remaining items

- Accept corrected Memory rankings and relative gains across both Bases on identical full-active DEV candidates.
- Run pre-registered five user-disjoint DEV OOF gates (Utility, Difficulty, Specialist Quality, Uncertainty, History), freeze pointwise budget thresholds, and preserve all negative results.
- Then evaluate further independent training seeds and one-shot sealed TEST under the frozen protocol. None of the 47,575 sealed TEST outcomes have yet been used.
