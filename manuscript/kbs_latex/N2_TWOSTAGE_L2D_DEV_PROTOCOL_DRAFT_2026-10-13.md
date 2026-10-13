# N2-D1 — DEV-only fixed-expert two-stage deferral comparator: prospective-design DRAFT

**Design date: 2026-10-13. Status: DRAFT, authorized only as a proposal, not a run or an externally timestamped preregistration.** The author may approve a future DEV-only exploratory experiment. **NO change to original G5-A/G5-B, no use of G5 TEST outcomes or event-level metrics, no automatic workflow execution.**

## Scientific question

Given a trained fixed recommender `B`, a transparent and fixed Memory ranker `M`, and the same candidate environment, is modeling the event-level incremental gain directly more informative for **these constrained routing policies** than estimating Base and Memory utility separately and subtracting their conditional expectations? The target is event-wise single-positive NDCG@10.

### Deferral-prediction conditions

- Existing "Direct" learner: regression `y_direct = y_memory - y_base` with fixed 12 pre-outcome descriptors `Z`.
- New "TwoStage" learner: separately regress `y_memory` and `y_base` with **the same model class, feature access, split, and hyperparameter search budget**; difference of held-out predictions = `s_two_stage`.
- Optional "binary benefit" descriptive learner `I(y_memory > y_base)` can be explored **only after the first two-model comparison is declared as the primary DEV exploratory contrast**; do not treat sign-only labels as optimizing NDCG magnitude.
- Gate action `a=1` selects Memory, `a=0` selects Base; when serving the two-stage learner requires inference of two regressors versus one, so **report gate latency if runtime advantages are even mentioned**.
- Public references: Narasimhan et al. (NeurIPS 2022) https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html ; Mozannar & Sontag (ICML 2020) https://proceedings.mlr.press/v119/mozannar20b.html . **This is an operational two-stage deferral-inspired comparator, not necessarily an implementation of every published algorithm or theorem.**

## Immutable input eligibility and leak guards

1. Per-Base DEV file is the accepted G3/G4 `dev_full_active_pairs.csv` verified against source aggregate manifest SHA. Exactly **50,049** full-active author ranking events; `split == DEV`, valid unique `event_id`, valid `user_id`; same `memory_ndcg10`, family-specific `sasrec_ndcg10` or `gru4rec_ndcg10`.
2. Exactly five Base-score + seven pre-history/candidate descriptors, same as existing gate; all `x_...` sources must be pre-outcome and strictly event-time available. TARGET utility columns are **labels only**, not selector features.
3. User grouping for folds; no user ID overlaps across an evaluation fold and its training/fitting set. No original target-defined recoverable states, no target author IDs, no future stream sessions or any metric on private TEST.
4. Numeric finite/range checks and exact accepted Memory correction: 0.45 Short(last10 of all prior author events) +0.45 Long(all prior authors incl TRAIN unseen denominator) +0.10 TRAIN-derived Pop; no rescoring new target labels or changing Memory rule. The actual event-level utilities are already in paired DEV cache.
5. Each fitting seed/checkpoint audited against the G4 accepted six-fit SHA/manifest. Missing cache or invalid SHA => **HOLD**; do not substitute reconstructed data from already exposed TEST.

## Fair user-group nested DEV evaluation

A. Split 50,049 events by user into **five outer user-disjoint folds**. Each outer fold is a held-out exploratory validation cohort; it cannot be used for selecting models/hyperparameters/thresholds or changing features.

B. Within each outer training cohort only, use inner GroupKFold (e.g. four folds) to produce out-of-fold estimates for both strategies. Fit the model / hyperparameters under identical fixed resource options, calibrate a pointwise threshold from inner OOF scores under a prespecified **at most 30% of the inner-training DEV events** Memory-call rule. The exact calibration/score tie convention must be fixed before running; reports show the *outer* realized specialist-call rate, which may drift and is not forcibly set to 30%.

C. Train final direct and two-stage regressors on the outer-training users, apply the frozen within-outer chosen thresholds to the held-out outer users. Concatenate five outer held-out masks/predictions to calculate single population paired DEV metrics. This **nested DEV** construction is not a new frozen prospective TEST and is still exploratory for paper-level scientific claims because the study was designed after G5 observations.

D. If an exactly realized *outer fold* 30% comparison is desirable, it is a **separate retrospective test-batch count-matched sensitivity**, not a pointwise production policy; report it separately and never call it a prospective quota. Do not move threshold after observing outer-fold outcomes.

E. Baseline policy includes Always Base, Always Memory, published original five DEV OOF gate objectives where exact evaluation protocol makes comparison meaningful. **Do not compare original DEV OOF optimization score to nested outer OOF as if they were equally unbiased.** Recreate Direct under the nested scheme for a matched comparator.

### Evaluation and reporting

- Per fold and pooled: mean NDCG@10, relative NDCG vs Always Base, call count/rate, paired user-cluster bootstrap CI on strategy difference, user clusters and candidate universe; additional supplementary Spearman correlation with label if desired.
- Gate runtime: two-stage requires 2× HGB or comparable, Direct requires 1×; do not claim lower total computational cost on the basis of Memory calls. Timings must be measured on same held-out DEV events, device, batch size and warmup/counterbalanced sequence if recorded.
- All fitted seeds share event cohorts and therefore correlated; report directional consistency not independent datasets, no new global 18-test Holm correction. Source group bootstrap on nested DEV is **conditional/exploratory**, not post-selection confirmatory TEST inference.
- Publish a negative result if two-stage ties/wins; a method that uses an existing expert selection principle is not misleadingly declared “ours is always better” simply because a named baseline is weaker under a restricted feature proxy.

## Execution feasibility and explicit stop rules

**Low training cost conditional on DEV cache availability**, because all six Base checkpoints and Memory score panels already exist. Existing CPU-based `analysis/kbs_plan_c/train_gate_oof.py` uses scikit-learn HistGradientBoostingRegressor and GroupKFold, providing a starting point. However its current protocol is a five-fold OOF plus threshold selected on same OOF DEV, not the nested honest comparison described here; **new implementation and tests are required**.

- Before implementation: check User-host availability, SHA256sum of paired DEV file per seed, privacy/data rights, full feature parity. If absent => HOLD / no surrogate TEST.
- Before running: create new isolated script and workflow with `DEV_ONLY` checks, unique output path, no original policy overwrite; make an explicit author-approved new-run record with source SHA; run synthetic unit tests confirming no fold overlap/no outcome leakage.
- If no independent new TEST is available after exploratory result: report in supplemental **DEV-only exploratory** manner if scientifically useful; otherwise retain existing G5 and refrain from claims of superiority over L2D/DS-Frame.
- Independently scored external later-period data or a new eligible task is needed to upgrade novel comparator claims to a new confirmatory study. NEW experimental prior claim must be frozen before those new outcomes are inspected.

**This document is an approved design recommendation, not a completed or authorized run.**
