# B2 full 50,049-event DEV relationship-knowledge source ablation: run-level evidence

**Date:** 13 October 2026. **B2-1 technical pilot:** PASS. **B2-2 full computation and private SHA-guard checks:** PASS. **B2-2 public artifact delivery:** HOLD due to GitHub Actions upload transport failure. **B2-3 user-disjoint choice-quality/knowledge-specificity experiment:** NOT YET RUN. All findings remain **POST-G5 EXPLORATORY DEV**, not a new frozen independent TEST.

## Original source and primary evidence

1. Preregistered-before-run [B2 scientific protocol](B2_RELATIONSHIP_KNOWLEDGE_SPECIFICITY_PROTOCOL_2026-10-13.md) and [128-event pilot audit](B2_STAGE1_RELATIONSHIP_MEMORY_PARITY_AND_PROTOCOL_QA_2026-10-13.md).
2. [B2 full calculation run #38367721633](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38367721633), original Git source commit `dd1ecab0512174814fe754f692153e61394591f4`. Code executed on the private self-hosted runner with **no model retraining and no G5 TEST accesses**, reading only G1/DEV, B1 private paired DEV and TRAIN-index/room-history files.
3. The private process printed `{"status":"PASS","n_events":50049,"parity":{"F":0,"S":0},...}` and finished **161.97 s**. The *next* workflow step read the final persisted private `summary.json`, checked all 50,049 event rows, 12,628 users, both zero-difference Full Memory outcomes and the existence of a 64-hex-character private CSV digest, and printed: `B2 full five-arm source ablation complete; no TEST or private IDs exported`.
4. **The run's final GitHub Action status is FAILURE solely because `actions/upload-artifact@v4` timed out during CreateArtifact with `ECONNRESET` at 08:17:48 UTC**. The job log shows the scoring and aggregate schema checks succeeded *before* that failure. Do not conflate an artifact delivery failure with scientific invalidity.
5. Source rows and full `summary.json` persist on the private self-host at `klm3_b2_full_dev_memory_source_ablation_seed20261013_v1` and are not overwritten. [Recovery-only run #38368505958](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38368505958) is designed to verify the persisted source and retry *only the safe aggregate*, not recompute rankings. At the time of this report creation it was **QUEUED**. Its outcome is **not presumed**.

## B2-2 observed full DEV results (from completed process's console aggregate)

| Memory evidence arm | F (full-active) NDCG@10 | S (575 sampled target-retained) NDCG@10 |
|---|---:|---:|
| Original Full Memory (0.10 P + 0.45 Short + 0.45 Long) | **0.343509** | 0.668498 |
| Long-only | 0.333231 | **0.773602** |
| Short-only | 0.273839 | 0.407506 |
| TRAIN popularity-only | 0.022215 | 0.197796 |
| History-score circular placement placebo | 0.007576 | 0.189571 |

**Main observation:** Full Memory is better than Long-only on F but worse than Long-only on S, even though both use the same 50,049 pretarget DEV events and unchanged author Base. This is evidence of a candidate-regime-dependent comparison between two **relationship knowledge source configurations**, not yet evidence that this difference causes conditional *selection policy* regret, because B2-3 is pending.

Short-only retains some utility; popularity-only and within-event scrambled historical evidence are much weaker in NDCG. These are valid diagnostic controls but do **not** establish that any observed downstream selector benefit is knowledge-specific until that downstream comparison has been performed. The cyclic historical placement null preserves only the within-event multiset of history scores and does not simulate a globally plausible retrained expert.

## Efficiency and data integrity

| Execution component | Measured wall time |
|---|---:|
| Corrected all-prior history scan (CPU, once) | 38.05 s |
| Active roster plus five full/sampled Memory variants (CPU) | 123.40 s |
| Total B2 full source labeling | **161.97 s** |
| New GPU Base scoring | **None; reused B1 original frozen full/sampled Base outcomes** |
| Full Memory F, S mismatches versus original corrected G3 and B1 | **0, 0** |

The small B2 pilot on 128 DEV events required 46.8 s largely due to fixed CPU streams; the all-cohort pass amortized this cost. Higher GPU busy percentage would not reduce time in this CPU relationship-scoring stage. No protected identities or per-event score vectors have been uploaded.

## Stop/GO decision

**B2-1 PASS. B2-2 private computation PASS; artifact delivery HOLD. B2-3 remains HOLD until the SHA-verified aggregate is recovered and a new full DEV certified-source gate is committed.**

The prepared B2-3 nested source `analysis/kbs_plan_c/b2_nested_knowledge_specificity_dev.py` and guarded workflow `.github/workflows/kbs-b2-nested-dev-knowledge-specificity.yml` will fit both Base families on identical 5×4 user-disjoint DEV folds under two predictor panels: (i) original 12 pretarget features and (ii) only pretarget candidate count plus Base score summaries (no directly computed user relation-history features). Primary effect for R3: compare *policy-regret penalty* `F→F − S→F` across Full, Long-only, Short-only, Popularity-only and relationship-shifted Memory **with paired user-cluster confidence intervals**. This is strictly post-G5 DEV exploration; the original TEST is sealed.

**Scientific conclusion at this stage:** Results suggest the evidence carried by genuine longitudinal interactions matters to raw rank quality, and candidate regimes alter which fixed Memory configuration ranks better. They are **not enough yet** to close the R3 integrated-knowledge-system scientific-contribution risk. R2 (Always Memory faster/stronger than limited Utility in M3) also remains unresolved.

## Completion addendum — B2-3 succeeded; original artifact failure remains historical

**13 October 2026, later stage closure.** The above upload HOLD reflects the **original** first full-score job; it does not mean that B2-3 was never completed. The full 50,049 DEV score source remained intact on the self-host. After repeated transient GitHub `download-artifact` / `upload-artifact` errors, a no-checkout/no-action/no-upload self-host workflow [#38369503457](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38369503457) successfully **rehash-verified the persisted private source and completed all nested comparisons** (two Base families × five Memory sources × original 12 features / candidate-plus-Base-only feature control). The safe aggregated result was recovered directly from successful run logs, with private nested results SHA256 `80aaa58e194a3e39188dc5807f2c3b913e1e5378df7dce254dbe3ca1d65e7d74`. No TEST or private user/candidate rows were exported.

**B2 full implementation/scientific DEV protocol = PASS; R3 integrated contribution risk = PARTIALLY MITIGATED and not author-confirmed or independently TEST-validated.** Read the current authoritative [B2 complete source and policy analysis](B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md) and [machine-readable four-panel aggregate](B2_NESTED_DEV_SOURCE_SPECIFICITY_AGGREGATE_2026-10-13.json). Under exact full candidate evaluation, Long-only is less accurate than Full Memory but more accurate under sampled outcome evaluation; the downstream S→F policy-regret and history-free-control patterns are detailed there. The failure record here should be retained for provenance, not described as an active scientific data blocker.
