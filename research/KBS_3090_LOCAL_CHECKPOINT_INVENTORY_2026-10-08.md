# KBS diagnostic — RTX 3090 local checkpoint inventory

**Date:** 2026-10-08  
**Status:** completed, read-only local and archive inventory; no KuaiLive Dual-ID checkpoint pair identified in examined roots.

## Executed audits

- [Local model-file inventory, Actions 37740203565](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37740203565): **success**. Inspected 298 directories below the self-hosted runner user's home and hashed model-shaped files without deserialization.
- [Local project-archive / mounted-project inventory, Actions 37740339175](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37740339175): **success**. Inspected 640 directories, 2 eligible archives, and common **project-specific** mount paths if present. No model-bearing room/streamer archive members found.
- Both jobs passed runner identity and unprivileged user checks. No checkout, model loading, training, inference, TEST-label access, model file modification, or weight upload occurred.

## Found models

| Platform / origin | Local path relative to runner HOME | Size (bytes) | SHA-256 |
|---|---|---:|---|
| Twitch/LiveRec context L8 | `actions-runner/_work/KuaiLive-Agent/KuaiLive-Agent/context_intervention/L8/models/kbs_ctx_L8_64_0.1_64_2_8_rep_ctx.pt` | 42,067,828 | `e4b47285d2b8db541ec3369f872dab0c3f2c227da16e5fb30964bf0a269b8040` |
| Twitch/LiveRec context L32 | `actions-runner/_work/KuaiLive-Agent/KuaiLive-Agent/context_intervention/L32/models/kbs_ctx_L32_64_0.1_64_2_32_rep_ctx.pt` | 42,074,090 | `8c29471662bf111630c5563651d85f52c2f2e1fd9b80cffe67ceee0ffaaa4dd4` |

Those files are **not** interchangeable with the required KuaiLive ReChorus room and streamer Base checkpoints.

## Target checkpoint pair

No local `room.pt` or `streamer.pt` pair was found in the scanned user and project-specific directories. No model archive with matching checkpoint members was found. The original GitHub Actions latency room/streamer checkpoint artifacts were independently confirmed absent from available artifact inventory.

**Interpretation:** The original KuaiLive Dual-ID checkpoint pair is **not currently recoverable from the examined self-hosted caches or named historical Actions artifacts**. This is a bounded inventory conclusion, not proof the files do not exist on every mounted volume or another private backup.

## Next-stage guardrail

The proposed fixed-checkpoint dual-candidate re-scoring experiment remains blocked because its exact Base parameters cannot be proven. Do not silently substitute Twitch checkpoints, score CSVs, or a newly trained KuaiLive model.

If an independent backup is located, verify both file SHA-256 values, ReChorus SASRec model configuration, training lineage, room/streamer dataset IDs, scoring coefficient, and candidate-source hash **before** fixed-checkpoint evaluation. Otherwise a newly trained checkpoint would be a separately labeled post-hoc diagnostic Base, not an exact reproduction of the original frozen Base.

## Source artifacts

- [Model-file inventory metadata](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37740203565/artifacts/11533401632)
- [Archive inventory metadata](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37740339175/artifacts/11533951011)

These artifacts contain metadata and hashes only, **not weight bytes**.
