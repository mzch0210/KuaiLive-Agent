# Plan C G0 — Verified resource audit (2026-10-12)

**Source of record:** [GitHub Actions run #38199905345](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38199905345), `user-host-g0` artifact ID **11724479979** (`user_host_g0.json`). The first attempt #38199834411 stopped at a pre-checkout marker guard, before any GPU inspection. The corrected retry completed.

## Actual user-host resource inventory

| Item | Observed value |
|---|---|
| GPU | NVIDIA GeForce RTX 3090 |
| CUDA-visible VRAM | **23.56 GiB** |
| NVIDIA driver | **580.159.03** |
| PyTorch | **2.4.1+cu124** |
| CUDA usable | **yes** |
| Available system RAM at audit | **59.47 GiB** |
| Cache-volume free disk | **1162.48 GiB** |
| Python | **3.12.3** |
| Original KuaiLive paired data/model cache dirs | **4/4 present** with SHA256SUMS manifests |
| M3 default root `~/.cache/kuailive-agent-kbs/klm3` | **not present**; no evidence of M3 files at this one path |

Cache directory presence and a SHA manifest are **not** equivalent to rehashing all underlying data/model bytes; a subsequent reuse must run `sha256sum -c`. The bounded M3 root check is **not an exhaustive disk search**.

**G0 resource decision: PASS. G0 data/protocol decision: HOLD.**
No download, model training, existing-test change, or future TEST label examination was executed. Reported `test_accessed=false` and `models_trained=false`.

## Official external protocol and data source review

- [Official KLM3 benchmarks](https://github.com/imgkkk574/KuaiLive-M3): separate target-author CDR with *per-user chronological 80/10/10* and other tasks; no existing benchmark uses this manuscript's proposed global-time eligibility protocol by default.
- [Official KLM3 Hugging Face repository](https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3/tree/main): **61.1 GB** full release. Required initial live-only inputs total approximately **4.81 GB** (`live_interaction.csv` 4.57 GB + `live_room_meta.parquet` 238 MB), before validation of any additional identity mapping requirements.
- [Official project website](https://imgkkk574.github.io/KuaiLive-M3/): describes academic research use; the HF repository displays `cc-by-sa-4.0`. Verify any data distribution/derived-data rules against the original authors and source metadata before publishing files.
- The historical project [Sep 19 plan](../../PROJECT_STATUS_AND_MAIN_EXPERIMENT_PLAN_2026-09-19T161638Z.md) planned KLM3 as *future* validation; old S1 documents original KuaiLive/Twitch results, not a completed M3 run.

## Remaining G0-D checks before training

1. Resolve data rights, pin an immutable upstream source version and inspect its actual field/header schema and timestamp semantics.
2. Download **only** required live-domain files into a persistent user-host cache, with source hash validation and disk checks; do not fetch multimodal embeddings or the 61.1GB archive for E1 by default.
3. Audit candidate availability, room-to-author identity and repeated historical relations, with no TEST metric or expert-utility comparison.
4. Audit possible source/date/user overlap with the original KuaiLive release and classify external-independence correctly.
5. Freeze E1/E2/E3 data splits, eligibility criteria, comparator feature-access fairness, DEV OOF procedure, thresholds and confirmatory statistical comparisons *before* held-out evaluation.
6. Only then train the first M3 Base once on user-host; reuse per-event Base/Memory scores for all five CPU gate objectives.

The CPU-only [frozen-gate interface](../../analysis/kbs_plan_c/frozen_gate.py) is tested on synthetic DEV/Test-score fixtures; it does not by itself produce trained HGB estimators, true M3 scores, or empirical strategy performance.
