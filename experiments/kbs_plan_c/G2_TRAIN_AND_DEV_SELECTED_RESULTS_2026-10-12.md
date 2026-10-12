# KBS Plan C — G2 dual-Base completion and DEV checkpoint selection (2026-10-12)

**Verified stage: G2 TRAIN model fitting and 4096-event sampled-active DEV checkpoint selection complete.** G2 does not yet include the preregistered full-active DEV evaluation or Base/Memory paired utility analysis. E1–E3 held-out TEST is **unopened**.

## Provenance and validated workflows

- Official M3 fixed source, valid TRAIN/DEV bundle and previously sealed TEST: [G1 accepted data](G1_FIXED_DATA_BUNDLE_ACCEPTANCE_2026-10-12.md).
- Actual two-Base training [GitHub Actions #38205618676](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38205618676), overall **success**, artifact **11728063522**: `index_manifest.json`, `sasrec_train_report.json`, `gru4rec_train_report.json`.
- Shared checkpoint selection [GitHub Actions #38208337267](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38208337267), overall **success**, artifact **11727834708**: `dev_screen_manifest.json`, `dev_selection.json`.
- Frozen before inspecting DEV checkpoint performances: [G2_DEV_CHECKPOINT_SELECTION_PREDECLARED_2026-10-12.json](G2_DEV_CHECKPOINT_SELECTION_PREDECLARED_2026-10-12.json), SHA256 `91b4bdd566eb1f29240cb94ae3aa4eea87185facc5e525056455045ec90c27b7`.
- G1 time/hash protocol SHA256 `bf6234eb95ecb24a568b2e7556846c41c4f3e1fdcd7774397003beaf56341a3c`.
- TRAIN index contains **24,995,148 events**, **21,938 users** and **897,025 author tokens**. The event sequence index was shared between the two Base families.

## Full TRAIN fitting

Both models were trained using TRAIN-only contexts (L=16, D=64), seed `20261012`, 3 full-size *replacement-sampled equivalents* of TRAIN (24,410 updates × 1,024 windows × 3 epochs). 32 TRAIN-drawn negatives per event. No DEV outcomes used for gradient fitting, and no TEST file opened.

| Epoch | SASRec TRAIN sampled CE | GRU4Rec TRAIN sampled CE |
|---|---:|---:|
| 1 | 1.1059713458 | 0.7474015573 |
| 2 | 0.5053694209 | 0.3744886113 |
| 3 | 0.4014584775 | 0.2976139942 |

TRAIN wall-clock time (including checkpoint save within fit): **1,203.71 s** SASRec and **1,067.84 s** GRU4Rec (about 37.86 minutes combined). Torch-reported peak allocated CUDA tensor memory: **1.100 GiB** and **1.088 GiB**. This is not the total GPU memory footprint or complete workflow wall time.

## Fair DEV checkpoint screen

The same **4,096 DEV targets** and a **fixed 575 active distinct warm-author candidate panel per target** were used for *every* epoch and both models. TEST targets were not read. The preceding DEV context construction used 50,049 DEV targets, found nonempty prior warm-user contexts for all 50,049, and used no TEST events in histories. Each sampled DEV target's true author was verified present in its active candidate roster. Roster sizes on the 4,096 selected DEV events ranged from 14,072 to 53,758, median **33,955**.

| Base | Epoch | DEV sampled-active NDCG@10 | DEV sampled-active HR@10 |
|---|---:|---:|---:|
| SASRec | 1 | 0.6161054515 | 0.7487792969 |
| SASRec | 2 | 0.6426906446 | 0.7761230469 |
| **SASRec** | **3 — selected** | **0.6482458376** | **0.7800292969** |
| GRU4Rec | 1 | 0.6348399694 | 0.7619628906 |
| GRU4Rec | 2 | 0.6487916778 | 0.7753906250 |
| **GRU4Rec** | **3 — selected** | **0.6512420790** | **0.7795410156** |

The DEV-selected checkpoint identity is predeclared **max NDCG@10 then earliest epoch on ties**. Both models selected epoch 3. At epoch 3, GRU4Rec minus SASRec NDCG@10 is **+0.0029962414** (roughly +0.30 percentage points), while GRU4Rec minus SASRec HR@10 is **−0.0004882813**. Without per-event paired uncertainty this small observed difference does **not** establish a statistically meaningful model superiority, and both models must remain eligible Base comparators.

## Selected checkpoint SHA256

- **SASRec seed20261012 epoch 3**: `18fb25d68970e73661a4b1418f5be05e7f8bed678d097533adf3cf1d9964d17e`.
- **GRU4Rec seed20261012 epoch 3**: `6c83dcb2e76f86e1018af467c0b0494f09b5d552c885700e92ea657cd9cc8d1a`.

All epoch-1/2 checkpoints were also persisted and individually hash-identified in training reports. Checkpoints live solely on the authorized user-host under `~/.cache/kuailive-agent-kbs/klm3_g2_seed20261012_epoch3_v1/{sasrec,gru4rec}`; do not upload model files or derived user traces to public GitHub.

## Essential scientific interpretation and remaining gates

1. **Sampled DEV screening ≠ full-active candidate evaluation**. There are ~33,955 concurrent warm candidate authors at the median sampled DEV target; rank distributions at 575 candidates will differ, potentially significantly. No M3 full-active NDCG@10 has been produced in this stage. The new M3 author-ranking task differs from the original KuaiLive room-ranking task, so its absolute metrics are not directly exchangeable.
2. **TRAIN CE of sampled next-item prediction is not a direct comparative measure of ranking accuracy**. The two neural architectures' training CE values are not used for checkpoint selection; the DEV sampled-active rank metric is.
3. **These are compact common-protocol SASRec/GRU4Rec implementations** (a one-layer causal Transformer and a single-layer GRU with D=64), not independently verified strongest benchmark implementations. This supports alternate-Base robustness evaluation, but does not alone substantiate a state-of-the-art competitiveness claim.
4. The observed single-seed NDCG difference (about 0.003) is descriptive. A paired user-cluster bootstrap or paired event analysis and independent training seeds would be necessary before any superiority or seed-robustness claim.
5. The G0F protocol preregisters additional random seeds `20261013` and `20261014` for cross-seed claims; no such models were trained here. Avoid retrospective run selection based on favorable DEV scores.
6. Next complete **full-active DEV Base vs fixed Memory** paired metrics on the *same* frozen author/event/candidate membership, cache compact event-level Base score summaries, memory difference and selector features, and train/freeze E2 gates. For computational efficiency, reuse DEV state and online author roster once across both Bases and do GPU-scored active authors in bounded chunks rather than materializing 50,049×~34k candidate matrices. The sealed 47,575-event TEST remains untouched until all policies and contrasts are frozen.
7. Past failure [pilot #38205344760](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38205344760) was a padding/attention NaN issue; only corrected stable training and subsequent DEV results are accepted. Original Twitch/KuaiLive results are unaffected.

**Current decision: G2 TRAIN/checkpoint-selection PASS; G2 full-active DEV and E2 gate-fitting still pending. Do not report these sampled DEV values as the paper's confirmatory M3 results.**
