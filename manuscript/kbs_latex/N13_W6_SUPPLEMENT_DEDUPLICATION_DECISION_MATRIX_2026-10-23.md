# N13 W6 — Supplementary Evidence Deduplication Decision Matrix

**Review date:** 2026-10-23  
**Baseline supplement:** `SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md` blob `778fa2cf8e584ffea83e2b56ccba4f6278455172`.  
**Method:** Compare populations, model/estimator fitting, freeze status, invocation rule, numerical observations, inferential interpretation, references and table numbering **before** declaring any duplication. This is an editorial source map, not a new experimental result.

| Apparently repeated material | Evidence comparison | Disposition |
|---|---|---|
| S2.3 Table S2.2 versus S8.4 Table S8.3, old KuaiLive Room/Streamer checkpoint hashes | Both contain the same three seeds (20260918/19/20) and six identical SHA256 values, but S2 establishes checkpoint identity while S8 co-locates them with robustness checks. Removing the S8.3 table directly would create a gap in S8.1–S8.6 sequential table numbers and require controlled renumbering/revalidation. | **Exact fingerprint duplicate identified; postpone table elimination/renumbering**, retain both as a local evidence lookup for this submission iteration. No different source or result may be inferred from the repeated hashes. |
| S7.7 Table S7.5 versus S10.7 Table S10.4, Direct / Two-stage DEV comparison | S7.7 is a nested five-outer/four-inner user-disjoint comparison with a 30% inner quota; SAS Direct 0.302678 vs Two-stage 0.301326 and different actual calls, with dedicated 2,000-bootstrap uncertainty. S10.7 is a four-objective, 10/30/50% nested-decision-target comparison; at 30% SAS Direct 0.302658 vs Two-stage 0.301348 and different policy calls. These are not the same estimates, even if cohorts share an origin. | **Preserve both**, cross-study comparison requires protocol context; do not replace one table's cells with the other's. |
| S9.6 Table S9.3 versus S10.17 Table S10.11, M3 DEV GPU timing | S9.6 earlier single-pass 256-request warmed paths: Base/Memory/Utility means 1.4245/0.8033/1.8018 ms; S10.17 later 256-request by three counterbalanced repetitions: 0.72759/0.69165/1.76941 ms. Ordering, trials, source accounting and inference differ; neither measures vectorized F-aligned online serving. | **Preserve both with roles distinct**; S10.17 is the best available balanced timing reference, S9.6 documents a different measured path. Do not merge or average timings. |
| S10.19 relocated source tables versus main-text summary | S10.19 retains historical full table cells migrated from the main paper, protected by the C7 full-cell audit. Main discussion uses only salient claims with source pointers. | **Preserve S10.19 exactly**; do not delete for page-count optimization. |
| S10.15/S10.16 versus Results H1/H2 | Supplement contains cohort strata, weighted call shares, null checks and full source validity details; the main paper reports frozen headline effects and limits. | **Preserve complementary detail**; H2 same-cohort TRAIN-only Popularity prereveal subgate remains NOT VERIFIED. |
| S1.5, S1.6, S2.4, S3.3, S5.7, S6.1 infrastructure wording | The scientific evidence has been retained in accessible source/run IDs, accepted outputs and explicit exclusions. Internal host labels and troubleshooting prose did not establish additional independent tests. | **Six targeted editorial revisions already committed in W6**, not another data revision. |

## Frozen safety checks and external constraints

- The S10.1–S10.19 source substring was byte-for-byte unchanged during W6's first editorial pass.
- H1 weighted full-candidate policy effects (SAS +0.005391, GRU +0.003585), 20-cell weighted call fractions, and H2 authentic-minus-null +0.031145 with original incomplete prereveal control remain as recorded.
- No new corrected-S trained policy, matched-call re-estimation, future-period replication, or production efficiency result is introduced.
- Repository paths referenced in the supplement were checked against the current branch tree: 24 GitHub blob links resolved to existing repository paths; path existence does not prove third-party access rights, permanent artifacts, or validity of unverified data.
- Elsevier-wide research-data options permit an availability statement when data cannot be shared under applicable journal policies; specific KBS requirements and actual ownership/redistribution approval remain author-owned. Do not invent a DOI or dataset deposit.
- De-duplication **stops at this matrix** unless an exact, verified source-preserving table renumber/redirect plan is accepted. Compression is not a substitute for scientific completeness.

## W6-to-W8 handoff

W6 dual-PDF scientific build [Actions #39883705990](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39883705990) passed both `main-paper` and `complete-supplement` on commit `2b1620e3fc2b9f998209cc09cf6cc15ef3fe4be1`. The W8 report must record any subsequent source changes, CI runs and actual PDF hashes separately; project-log-only changes do not invalidate a same-source successful build.
