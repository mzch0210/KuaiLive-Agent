# KBS KuaiLive same-checkpoint diagnostic — execution and evidence ledger

**Date:** 2026-10-08  
**Status:** Dataset provenance confirmed; analysis controller and hosted preflight prepared. **No new GPU paired TEST result at time of writing.**  
**Nature:** Post-hoc diagnostic for candidate-regime comparability. The previous frozen scientific and policy results remain unchanged.

## Why this diagnostic is necessary

The historical KuaiLive candidate-regime state decomposition shows sampled Memory−Base = -0.05125 and full-active Memory−Base = +0.03367 on 10,222 matched events. However, sampled and full-active model/fusion configurations were not completely identical, and distinct sampled Base NDCG@10 anchors (0.60784 and 0.61714) appear in different reporting contexts. The historical sign reversal is real *within those logged protocols* but does not alone isolate candidate-set changes.

This controlled diagnostic fixes one **newly trained** Room-SASRec + Streamer-SASRec checkpoint pair, a single fusion alpha selected on **sampled DEV only**, one fixed Memory definition, and the same TEST user–time–target events. Only the candidate set and its associated candidate-wise z-standardization are allowed to change. It yields paired differences; it is not a randomized causal experiment.

## Pre-existing diagnostic-branch work examined

- GPU training run [37741589624](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37741589624) failed while downloading the expired `room-collision-data-35554842873` artifact. It did **not** establish that training itself failed.
- The subsequent candidate reconstruction run [37741843252](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37741843252) succeeded, producing `kbs-posthoc-regenerated-inputs-37741843252` (artifact ID **11534262601**, 90-day retention).
- The separate branch's source/statistics preflight [37742133747](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37742133747) succeeded. Those tests are not a substitute for validating the new main-branch GPU runner.
- The new hosted [input provenance audit 37744831516](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37744831516) succeeded. Its report artifact ID is **11535446629**. Regenerated `train.csv`, `dev.csv`, `test.csv` and `export_meta.json` are **byte-for-byte identical** to the still-retained frozen strong-base input bundle (artifact ID **10730951727**). This proves identity to that archived bundle, not to every expired artifact or model weight.

### Fixed input identity hashes

| Frozen room input | SHA256 |
|---|---|
| train.csv | ad91413537175b9f6e9013c525a552b6004cc00e029b41360f08519e0735b5b4 |
| dev.csv | 46dd3081688468c89acf6366d36d87c122fa45850ddb69320c05da9de94a9f54 |
| test.csv | 3491862df4de5cfb487fbd21c2f62c2d1d62acac110f852cc83c019dfcc6e956 |
| export_meta.json | 821d06dd0d7335cc49bf892490f7b9098a53bb8467da6de438a30c975c6cb459 |

The audit verified 10,222 users and 575 sampled candidates (1 target + 574 negatives).

## New main-branch execution

- Scientific evaluator: [`analysis/kbs_kuailive_same_checkpoint.py`](analysis/kbs_kuailive_same_checkpoint.py).
- GPU controller: [`.github/workflows/kbs-kuailive-same-checkpoint.yml`](.github/workflows/kbs-kuailive-same-checkpoint.yml).
- Hosted preflight: [37744161280](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37744161280) passed. Later preflight runs confirm updates can be parsed and compiled.
- The private RTX 3090 job remains intentionally **manual and owner-guarded**. A push invokes *only* the inexpensive hosted preflight, not the private GPU.

### Owner execution steps

1. Open [KBS KuaiLive same-checkpoint diagnostic](https://github.com/mzch0210/KuaiLive-Agent/actions/workflows/kbs-kuailive-same-checkpoint.yml).
2. Select **Run workflow**, branch **main**, and check `confirm_owner_run=true`; this preserves the private runner's owner-only security gate.
3. Inspect the paired GPU job: completion is contingent on immutable input matches, synthetic tests, checkpoint writes and user/event membership checks. No scientific sign or significance threshold is used as a technical pass/fail criterion.

### Efficiency and reproducibility

- Avoid re-downloading Zenodo and recomputing candidates: restore the already-tested 110 MB input artifact only on a private cache miss.
- Verify all four canonical SHA256 values and the persistent cache's complete payload manifest.
- Reuse the *same* checkpoint pair for both candidate regimes. Cache the trained pair with SHA256 to avoid retraining after a downstream failure. Upload both weights and their checksums with 90-day retained results.
- Select one fusion alpha on DEV using the sampled protocol. On TEST, score each full-active event **once**, subset the exact raw scores for sampled candidates and independently apply candidate-wise normalization.
- Report primary paired overall \\(\Delta_{full}-\Delta_{sampled}\\), each regime's Base and Memory NDCG@10, and state-specific shifts with paired user-level bootstrap CIs. Store `per_user_paired_test.csv.gz`, `sampled_dev_alpha_grid.csv`, `report.json`, model hashes, and resource logs.
- Label result as a **new post-hoc same-checkpoint protocol**, not a retrofit of the historical frozen sampled/full-active comparisons.

### Inference rules

**Sign persists:** stronger evidence of regime-dependent operational specialist value under held-fixed models and alpha, though candidate-wise score normalization also changes.

**Sign attenuates or disappears:** describe historical reversal with explicit competing configuration effects, revise Introduction and Results language; never suppress the result.

**Runtime/provenance guard fails:** do not interpret incomplete outputs; fix the engineering issue and re-run without looking for favorable scientific direction.

**Existing Twitch untouched TEST:** the previously frozen LiveRec policy, thresholds, rankings and inference remain immutable and are not re-tuned by this diagnostic.

## Manuscript coordination

The updated [submission-oriented outline](KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md) retains Sections 1–4 and restructures the remaining article as Sections 5 Experimental Setup, 6 Experimental Results, 7 Discussion, and 8 Conclusion. The new diagnostic is a pending panel within Section 6.1, not a completed numeric result. Resolve all Base/protocol label discrepancies before finalizing its prose or main-text figures.
