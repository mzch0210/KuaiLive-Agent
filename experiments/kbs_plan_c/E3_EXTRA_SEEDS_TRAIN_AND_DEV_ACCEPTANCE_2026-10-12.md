# Plan C E3: Preregistered additional model seeds — successful TRAIN and DEV checkpoint acceptance

**Date:** 2026-10-12  
**Scope:** New M3 author-ranking, exact same TRAIN-only author sequence index and same 4096-event × 575-active-author DEV checkpoint panel. **No full-active alternative-seed scoring, gate re-fitting, latency confirmation, or held-out TEST evaluation was performed in the two accepted runs.**

## Actual completed GitHub Actions

- [Two preregistered extra-seed TRAIN fits, run #38214570522](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38214570522): **success**, artifact **11734243605**, includes all four TRAIN reports and G2 index manifest. The 3090 reused the already frozen, provenance-verified 24,995,148-event TRAIN index and ran each fit sequentially.
- [Identical DEV checkpoint selection, run #38221813306](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38221813306): **success**, artifact **11735010738**, two per-seed JSON files.
- [Original main seed20261012 completion](G2_TRAIN_AND_DEV_SELECTED_RESULTS_2026-10-12.md).
- Both extra-seed DEV manifests have **identical DEV panel SHA256** `45e62c995a37bb7654dac153f75c661bc88822d0a71afe77daba5865b3274778`, **identical TRAIN index SHA256** `dea9911d5234539f41dc7d49eb8a780e76029c2182e17277ccb79bfa726066fc`, and `test_data_opened=false` / `test_rankings_calculated=false`.

## DEV model selection (4096 fixed target events, 575 active warm author candidates each)

| Base family | Seed | Epoch 1 NDCG@10 | Epoch 2 NDCG@10 | Epoch 3 NDCG@10 | **Selected epoch and score** |
|---|---:|---:|---:|---:|---|
| SASRec | 20261012 | 0.616105 | 0.642691 | 0.648246 | **3 / 0.648246** |
| SASRec | 20261013 | 0.621413 | 0.645543 | 0.650481 | **3 / 0.650481** |
| SASRec | 20261014 | 0.616960 | 0.638266 | 0.645982 | **3 / 0.645982** |
| GRU4Rec | 20261012 | 0.634840 | 0.648792 | 0.651242 | **3 / 0.651242** |
| GRU4Rec | 20261013 | 0.637314 | **0.649687** | 0.649221 | **2 / 0.649687** |
| GRU4Rec | 20261014 | 0.632900 | 0.644226 | 0.644531 | **3 / 0.644531** |

**Descriptive three-seed means ± sample standard deviation:** SASRec **0.648236 ± 0.002250**; GRU4Rec **0.648487 ± 0.003513**. Three seeds cannot substantiate statistical architecture superiority; the architecture order switches at seeds 20261013 and 20261014. Best epoch for GRU4Rec seed20261013 is **2**; do not silently use epoch 3 or select all models by TRAIN loss.

## Exact selected checkpoint SHA256

| Family | Seed | Epoch | Checkpoint SHA256 |
|---|---:|---:|---|
| SASRec | 20261012 | 3 | `18fb25d68970e73661a4b1418f5be05e7f8bed678d097533adf3cf1d9964d17e` |
| SASRec | 20261013 | 3 | `bb627ec2cc39313548c1eff64583aac4a010847967e595bdace01de4c8dabd32` |
| SASRec | 20261014 | 3 | `ab60a3d71cfd007b74296b5bb16bb95927d03a167c9e8d7d2fedc5995f2acd84` |
| GRU4Rec | 20261012 | 3 | `6c83dcb2e76f86e1018af467c0b0494f09b5d552c885700e92ea657cd9cc8d1a` |
| GRU4Rec | 20261013 | 2 | `6847482a2a4722b5a324be20ffc8960030d6367942c3d0f21ef53db7f1d75128` |
| GRU4Rec | 20261014 | 3 | `afb11b7ae7d4fad1b60545649461992dd064b0370a72904cc4337b880f0e3ad0` |

## New-seed GPU training cost

| Seed | SASRec TRAIN fit | GRU4Rec TRAIN fit |
|---|---:|---:|
| 20261013 | 1271.84 seconds | 1014.77 seconds |
| 20261014 | 1228.41 seconds | 1113.94 seconds |

Total additional recorded fit time was **4,628.96 seconds (~77.15 minutes)** excluding GitHub workflow setup and DEV checkpoint selection. PyTorch peak allocated tensor memory was **1.100 GiB** SASRec and **1.088 GiB** GRU4Rec. These measures do not equal end-to-end serving latency or total GPU VRAM reservation.

## Remaining E3 scientific acceptance gates

These experiments demonstrate stability of **DEV model checkpoint-screen quality**, *not yet* stability of relationship Memory value, relative Utility routing or statistical contrast under varying train seeds. The missing scientific steps are:

1. **G4 ALT-BASE paired full-active DEV**: for each independently trained 20261013/14 model family, compute its Base on the frozen 50,049 DEV events and exact warm-active author candidate sets. Reuse original corrected Memory ranks and stored source identities. No need to replay corrected Memory or refit original G2 Base.
2. Fit each new-seed gate from the **same complete DEV feature panel** using 5-fold group-disjoint OOF and freeze its pointwise max-30% threshold before reading any held-out TEST. Preserve the full-rank source hashes, model identities and failed outcomes.
3. **Actual deployment-cost test** of sparse history-support gate preprocessing and selected Memory path; a 30% invocation fraction is not evidence of a 70% end-to-end speedup.
4. Only after test protocol and all seed policies are frozen, execute the planned **47,575-event independent TEST** once with user-cluster paired intervals and preregistered Holm correction.

The source dataset's official author CDR benchmark uses a **per-user chronological 80/10/10 split**, not the globally chronological, time-live candidate-ranking protocol applied here. Do not compare the absolute M3 NDCG numbers to official CDR leaderboard results without a protocol-aligned control.
