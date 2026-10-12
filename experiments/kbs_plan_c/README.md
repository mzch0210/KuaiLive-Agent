# KBS Plan C G0 — execution record (2026-10-12)

**G0 implementation started.** This is an audit-only branch. It does not read or evaluate a TEST target, change any existing main.tex/S1-S9 evidence, download KLM3 or train models.

## Ground truth carried forward

- Twitch LiveRec 44,221 TEST events: frozen primary C1/C3 policy evidence.
- Original KuaiLive 10,222 TEST events: previously inspected C2 same-cohort diagnostics.
- Historical 2026-09-19 project plan calls **KuaiLive-M3 a future untouched in-domain confirmation**, not a completed run. The M3 files are not present in the tracked project tree. Local user-host caches remain unverified.
- Official KLM3 benchmark's per-user chronological 80/10/10 author-level CDR protocol is different from the globally chronological split proposed for E1; final choice must be reviewed and frozen before TEST.

## G0 execution gates

1. **Hosted CI:** synthetic unit tests; check protocol draft; produce a read-only audit report.
2. **User-host:** on an owner-approved manual dispatch from main, check RTX3090, RAM, free disk, known KuaiLive checkpoint caches, and *only specified root-level M3 filenames*. No recursive home scan; no raw dataset access.
3. **Data preflight (pending):** independently check license, source overlap, chronological validity, candidate availability and data footprint on an approved source; do not optimize with or view TEST utility.
4. **Freeze (pending):** define E1/E2/E3 dataset split, candidate ranking unit, Base families, all gate objectives, test contrasts, multiplicity plan and checksum manifests.

## Execution-efficiency principles

- Reuse the original proven ReChorus/LiveRec code, existing 3090 virtualenv and model caches; never retrain merely to recreate known KuaiLive/Twitch metrics.
- On M3, train each new Base only once per prespecified seed; produce one same-event Base score vector and one fixed Memory score vector, then share both across Utility, Difficulty, specialist-quality, uncertainty and history gates.
- Use GitHub-hosted CPU for OOF gate training, thresholds, bootstraps, comparison tests and evidence packaging; use the RTX3090 only for neural training and required large candidate scoring.
- Keep the `kuailive-gpu-3090` concurrency group, cache integrity, SHA256 and checkpoint provenance.
- Every TEST selector is a DEV-frozen pointwise policy; hindsight top-m is reported separately and is not relabeled as frozen deployment.

## Sources

- [KLM3 official benchmark](https://github.com/imgkkk574/KuaiLive-M3)
- [Original KuaiLive release](https://zenodo.org/records/16565801)
- [KBS S1 dataset/source protocol](../../manuscript/kbs_latex/SUPPLEMENTARY_S1_DATASET_PROTOCOL_2026-10-10.md)
- [GitHub self-hosted runner guidance](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
