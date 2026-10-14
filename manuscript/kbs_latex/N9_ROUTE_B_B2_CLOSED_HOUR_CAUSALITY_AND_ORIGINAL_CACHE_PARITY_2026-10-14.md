# N9 Route B — B2 closed-hour time-valid null protocol and 1,024 DEV cached source verification

**2026-10-14 | Implementation + synthetic test PASS; original label cache parity PASS; full 1,024-event real historical null NOT RUN; research rights/actual original-scoring parity HOLD.** No original G5 TEST or manuscript change.

## I. Executed algorithm verification

Code `analysis/kbs_plan_c/n9_route_b_temporal_null_engine.py` (Git blob `9716794fac37fbeb3711bf3ee9084ed8f4c04df8`) constructs **independent per-UTC-hour seeds**, proposes distinct-user, distinct-author swaps and rejects a proposed swap unless both old and new authors were active at both original source times. It guards exact per-hour author interaction marginals and preserves every user's event count/time.

**Critical causal activation rule:** A source history edge at time `s` can use its swapped author in a target request at time `t` only if `s<t` **AND** the entire source hour closed at or before `t`: `hour_end(s)<=t`. The same open-hour history remains original. Seeds depend only on the source hour and the fixed experiment seed, so adding any later bins cannot change decisions in already closed historical bins.

Run [Actions #38499302003](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38499302003) succeeded with **six synthetic unit tests**, including same-hour future event leakage, counterbalanced per-hour author activity, future-bin independence, ineligible author rejection, invalid time/source-ID rejection, and input batch order invariance.

This proves the **pure temporal-null transformation invariants on synthetic inputs**, not on the real 1,024 DEV events. In particular, one cannot yet treat the prior 128 late-quarter prefix swap as an implementation of the new closed-hour rolling design.

## II. Frozen 1,024 author DEV source integrity

The earlier exact pre-outcome sample was created under [Actions #38498724492](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38498724492): **1,024 requests, 992 distinct users**, 16 chronological/history-activity strata × 64 events, original 128 pilot excluded. Its private sample SHA256 is `6ad1a0753e181ac638636c278d226832b08d90d7d4867019910c61b96d7507da`.

After sample freezing, read-only [Actions #38499469077](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38499469077) verified exact private sample SHA, B1/B2 source SHA, same DEV user/event identities and original Full Memory **cached F and S NDCG event-by-event agreement**. No chronological source stream rerun, new Memory scoring or edge swap was performed.

| Fixed historical knowledge expert on 1,024 sealed DEV events | Original full-active F NDCG@10 | Offline target-retained sampled S NDCG@10 |
| --- | ---: | ---: |
| Full Memory | 0.339348 | 0.663896 |
| Long-only | 0.338699 | 0.767314 |

Descriptive Full-minus-Long F gap **+0.000649**, S gap **−0.103418**; descriptive difference-of-gaps **+0.104067**. These are merely previously generated scores on the pre-frozen subset. **Not an independent TEST, no user confidence interval newly claimed, no relation identity-null effect measured.** Sample estimates differ from the full 50,049 DEV cohort and must not be used for opportunistic sample changes.

Reproducibility: `experiments/kbs_plan_c/N9_ROUTE_B_B2_1024_CACHED_SOURCE_PARITY_PUBLIC_2026-10-14.json`; frozen code `analysis/kbs_plan_c/n9_route_b_b2_cached_scoring_source_parity.py`. No event/author IDs appear in public output.

## III. Dataset rights audit: a discrepancy needing resolution before derived data sharing

The public KuaiLive-M3 paper's available full-text excerpt (arXiv:2607.24862, §3.1.6) describes **CC BY-NC-SA 4.0** non-commercial research/education release (https://arxiv.org/abs/2607.24862). The original KuaiLive repository explicitly uses **CC BY-NC-SA 4.0** (https://github.com/imgkkk574/KuaiLive), while the current Hugging Face KuaiLive-M3 dataset listing shows **cc-by-sa-4.0** (https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3). These licensing representations differ. The Hugging Face repository's README.md is currently minimal; a listing badge should not be treated as conclusive permission covering every dataset collection.

This is a **rights clarification issue**, not a finding that non-commercial analysis is prohibited. The authors should verify the governing terms for the **exact M3 files/version** in the self-host cache, how anonymized user/author IDs may be used, and whether derived relation-edge snapshots may be redistributed. Maintain anonymized ID/edge records only on the authorized host and publish only aggregates pending that check. This document is not legal advice.

## IV. Still-required hard gates before a real B2 mechanism verdict

1. Verify the exact input schema/datetime units and time ordering of the private `causal_stream_sealed.parquet`, including the correct treatment of train/prior-DEV history and no use of TEST interactions. Pure synthetic success is insufficient.
2. Freeze one adapter that applies the per-hour independently generated cross-active swaps to requests **only after each hour fully closes**, and specify how users with multiple requests in the same hour are handled.
3. Confirm actual source-hour author availability against `available_room_intervals.parquet`, fixed event roster, stable shortlist sample identities and exact user/author histories; validate changed-edge coverage and no-floor Memory capacity.
4. Execute **fresh original scoring-path replay on frozen 1,024 DEV requests** and match source F/S Full/Long NDCG against the existing B1/B2 event labels **before** using placebo scores. Current B1/B2 cache-to-cache agreement does **not** satisfy this.
5. Confirm study data rights and private relationship-edge processing authority with responsible authors. Retain the three pre-frozen null seeds `20261014/20261015/20261016`; no cherry-picked resampling. Use user-cluster paired uncertainty once scores exist.
6. **Only then** run the first 1,024-event E3b control. Expanding to 2,048 must follow the frozen interval-precision rule, never a desired effect sign. Full 50,049 DEV and fresh TEST remain unauthorized.

Scientific interpretation must account for B1A's finding that 0.100885/0.115382 of the DEV mean source×candidate interaction is associated with zero difference under at least one evaluation regime. E3b has to test the additional effect of historically correct *identity* while keeping the null's ranking signal non-trivial; it must not be used simply to reconfirm sampled-top-10 non-preservation.

Literature: Ren et al., *Randomizing growing networks with a time-respecting null model*, Physical Review E 97, 052311 (2018), https://doi.org/10.1103/PhysRevE.97.052311 ; KBS official journal scope https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 . Neither source by itself validates this project-specific control.

## Stage ruling

`B2_TEMPORAL_ALGORITHM_SYNTHETIC_PASS`; `B2_1024_DEV_CACHED_LABEL_SOURCE_PASS`; `B2_1024_REAL_REPLAY_AND_RELATION_NULL_HOLD`. All three scientific risks **remain bounded**, not resolved. Existing 36-page main and 39-page S1–S10 remain the submission working version; no scientifically new results have yet warranted another manuscript rewrite. `SUBMISSION_HOLD`.
