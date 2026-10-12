# G2 execution ledger — M3 dual Base checkpoint training (2026-10-12)

**Current stage:** Full TRAIN-only training job dispatched to RTX 3090. The run has **not** been verified completed when this ledger was authored; no DEV optimum and no TEST score is claimed.

## Sources and reproducibility

- G1 pretest protocol [G0F](G0F_PRETEST_PROTOCOL_2026-10-12.json), SHA256 `bf6234eb95ecb24a568b2e7556846c41c4f3e1fdcd7774397003beaf56341a3c`.
- Frozen source bundle: [G1 acceptance](G1_FIXED_DATA_BUNDLE_ACCEPTANCE_2026-10-12.md), 24,995,148 TRAIN events, 897,025 TRAIN-known authors; 50,049 DEV events and **47,575 sealed TEST events**.
- Shared TRAIN-only index: [successful dual GPU pilot #38205456901](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38205456901), artifact **11726594270** with `index_manifest.json`, `sasrec_pilot_report.json`, `gru4rec_pilot_report.json`.
- Training code [g2_train_base.py](../../analysis/kbs_plan_c/g2_train_base.py), synthetic tests [test_g2_train_base.py](../../analysis/kbs_plan_c/test_g2_train_base.py).
- **Full checkpoint training launched:** [G2 full TRAIN Action #38205618676](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38205618676).
- **DEV checkpoint selection scientific protocol frozen before any DEV checkpoint metrics:** [G2_DEV_CHECKPOINT_SELECTION_PREDECLARED_2026-10-12.json](G2_DEV_CHECKPOINT_SELECTION_PREDECLARED_2026-10-12.json).
- Post-training DEV-only selection workflow: [kbs-plan-c-g2-dev-selection.yml](../../.github/workflows/kbs-plan-c-g2-dev-selection.yml); hosted synthetic causal-history tests [#38205972728](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38205972728) passed.

## Actual 3090 pilot results (true TRAIN, not DEV nor TEST)

| Metric | SASRec | GRU4Rec |
|---|---:|---:|
| 3090 batch size | 512 | 512 |
| Training updates | 120 | 120 |
| Runtime in training loop | **1.83 s** | **1.69 s** |
| PyTorch peak tensor VRAM | **1.096 GiB** | **1.081 GiB** |
| Observed pilot TRAIN sampled-negative cross-entropy | **3.465045** | **3.391106** |

Pilot numbers are **not** accuracy estimates and exclude G1/index loading. Both models train with TRAIN-only sequence history (L=16, D=64), one positive and 32 training negatives per event, shared precomputed author vocabulary and history index. Training batches use a deterministic 50/50 mixture of uniform and train-popularity-power(0.75) negatives; cross-entropy is over the positive and sampled training candidates. SASRec uses a one-layer, four-head causal Transformer; GRU4Rec a 64-dimensional single-layer GRU. These are compact compatible architecture implementations, **not strict source-identical reimplementations** of any external official leaderboard baseline. G2 strong-Base claims require actual DEV comparison and honest quality reporting.

The very first real pilot [#38205344760](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38205344760) halted upon a nonfinite SASRec loss caused by left padding plus masking. The model was corrected to right-shift valid sequence items prior to causal attention, and short-history finite-loss/gradient tests were added. Only the corrected pilot is treated as successful.

## Full TRAIN budget (preset prior to DEV metrics)

- Model families: SASRec and GRU4Rec, each independently fitted on the same 3090, never concurrently.
- Main seed: **20261012**; context length **16**; item embedding **64**.
- Each family: batch size **1,024**, **24,410** updates per epoch, **3** epochs; **75,005,?** sampled windows overall (correction: exact total = `24,410 × 1,024 × 3 = 74,987,520`). Draws are **with replacement** from eligible TRAIN events; these are approximately three full-TRAIN-size *sample-equivalent* epochs, **not** three independent complete deterministic passes.
- Learning rate **0.001**; 32 train-only negatives per window; finite-loss checks, gradient norm clipping.
- Every epoch checkpoint is retained on User-host in `~/.cache/kuailive-agent-kbs/klm3_g2_seed20261012_epoch3_v1/{sasrec,gru4rec}/`; log/checkpoint hashes reported to GitHub artifact after successful completion.
- No extra-model hyperparameter exploration, adaptation or seed stopping based on TEST.

## DEV checkpoint selection planned and test guard

- `G2_DEV_CHECKPOINT_SELECTION_PREDECLARED_2026-10-12.json` freezes 4,096 fixed DEV target events, one true active author plus 574 other distinct active warm authors, using a consistent candidate roster for every model/epoch.
- DEV pretarget contexts include previous chronological TRAIN/DEV events; any authors not known to TRAIN are omitted from train-vocabulary sequences; cases with no warm known history are assigned the fixed TRAIN-popularity fallback. These counts must be reported.
- Choose checkpoint with highest DEV sampled-active NDCG@10; earliest epoch resolves ties. Follow with full-active DEV analysis. Neither checkpoint training nor DEV selection reads TEST ranking outcomes.
- IMPORTANT: 575-candidate DEV screen is a **model-selection proxy**, not the primary full-active confirmatory ranking metric, which must be computed separately.

## Provenance nuance to preserve

The G0F draft describes hashing `timestamp_ms`, whereas the executed G1 DuckDB sampler passed a typed TIMESTAMP into its fixed hash. The **actual resulting DEV/TEST cohort is byte-frozen and unrelated to model utility**, with SHA256 recorded in the G1 acceptance manifest. This mismatch is disclosed; do not silently rewrite the historical preregistration. The scientific split boundaries and hash seed have not changed. The G2 code consumes the already frozen cohort and does not resample it.
