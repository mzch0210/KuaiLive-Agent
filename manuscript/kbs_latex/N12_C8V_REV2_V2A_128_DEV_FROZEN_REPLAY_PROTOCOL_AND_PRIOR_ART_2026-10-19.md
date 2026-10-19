# N12 C8V Rev2: Original B1 128-DEV frozen-rank replay and corrected-S method boundary

2026-10-19. **Bounded, same-sample original pipeline replication only. Not a corrected-S arm.**

- Existing GitHub self-hosted runner was checked in Actions #39230682113, and all original DEV source/cache/model hashes matched. Those files remain private.
- Added `.github/workflows/kbs-n12-v2a-dev-128-frozen-replay.yml`, run [#39231431695](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39231431695). It packages the pre-existing `b1_dev_regime_pilot.py` with its original scorer dependencies and manifests, uses existing frozen model checkpoints, and runs **128 preselected DEV** indices only. No new policy training, new TEST, or original output overwrite. Report schema `kbs-b1-stage1-frozen-dev-regime-pilot-v1` checks exact full-candidate rank against the accepted original G3 F record for Memory, SASRec and GRU4Rec. It recomputes sampled F/S summaries for those 128 but **does not currently compare each recomputed sampled metric to B1-2's original 50,049-row CSV**. That missing parity is a separate stronger follow-up, not presumed accomplished by this run.
- Hosted job validation cannot certify GPU result; **run #39231431695 must have both jobs success before calling bounded replay PASS**. Public output excludes event/user/author identities, raw candidate scores, history, checkpoint bytes, all original private paths and private CSVs.

## Method literature verified against first-party publication sources

- Krichene & Rendle (KDD 2020), [On Sampled Metrics for Item Recommendation](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/): sampled rank metrics may reverse relative model evaluations; bias/MSE corrections can improve *population metric estimation*. This neither requires nor establishes an exactly unbiased conditional **per-request** Base-relative NDCG utility label.
- Jin, Li, Mudrak, Gao & Liu (AAAI 2021), [On Estimating Recommendation Evaluation Metrics under Sampling](https://ojs.aaai.org/index.php/AAAI/article/view/16537): uses weighted likelihood / maximum entropy to recover *global rank distribution* to estimate top-k metrics. Again, not automatically an estimator of `E[Memory−Base full NDCG@10 | pretarget Z]` nor a guaranteed corrected selector.
- Li et al. (KDD 2020), [On Sampling Top-K Recommendation Evaluation](https://www.kdd.org/kdd2020/accepted-papers/view/on-sampling-top-k-recommendation-evaluation.html): sampling/full mapping shown for hit-ratio; not immediately transferable to NDCG conditional effect.

**Decision:** Only after source parity, selected estimator information contract and synthetic statistical validation may a genuinely distinct **corrected-S DEV-only** experiment be separately authorized. Original B1 S/F/Adapted three arms already done and must not be repeated. Original B4-A TEST/H2 sealed outputs must not be used to select a new correction.

V2a private source check: PASS; corrected estimator validity: PENDING; V2b: NOT AUTHORIZED. Reviewer/author scientific signoff: PENDING.
