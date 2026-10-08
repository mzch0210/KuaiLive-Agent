# KBS fixed-checkpoint candidate-regime diagnostic — analysis protocol

**Status:** prospective specification for a *post-hoc diagnostic*, not a new confirmatory untouched-test protocol.  
**Date:** 2026-10-08. **Work branch:** `kbs-fixed-checkpoint-diagnostic-20261008`.  
**Original KBS P1.3 policies, frozen TEST labels, manuscript and source results:** unchanged.

## Motivation and already-established facts

The earlier KuaiLive sampled-active result (Base approximately 0.607844; Memory approximately 0.565887) and the later evidence-state decomposition (Base approximately 0.617142; Memory approximately 0.565887) use different Base scoring outputs, even though they cover 10,222 underlying user–time–target instances. The decomposition uses `seed-20260918/dual_id_results/per_user_test.csv.gz`. Full-active scores were produced by another workflow and may depend on distinct training checkpoints. Therefore the previously observed sign reversal cannot alone identify an isolated candidate-set effect.

Sampled-active comprises the frozen positive plus 574 negatives; full-active uses the legally active rooms at event time. Candidate-wise standardization is performed separately for the two branches **within each candidate set**; this is part of the candidate-environment treatment and is not held constant numerically.

## Research questions

**D1 (primary diagnostic):** With the same *verified* room and streamer model checkpoint hashes and the same user–time–target instances, does the sign/magnitude of `Memory NDCG@10 – Base NDCG@10` change between the original sampled-active and full-active candidate sets?

**D2 (diagnostic decomposition):** How much of this difference arises from Base performance changes versus Memory performance changes, overall and within the represented / recoverable-but-unrepresented / unavailable partitions? Report denominators, especially the small recoverable stratum.

**D3 (optional, conditional):** Do paired differences have consistent direction across a second existing and checksum-verified checkpoint pair, **without** adding new hyperparameter searches?

**D4 (optional low-cost validity audit):** In Twitch's ten-minute observation-step records, how often does an earlier-observed interaction's last-observed step overlap a target step? This is an offline observability diagnostic only.

## Stage A — preflight (GitHub-hosted; begin first)

1. Query GitHub Actions metadata for all *named* source run IDs and artifacts. Do not download large archives just to discover that checkpoints have expired.
2. Audit source provenance: original sampled Base, seed-20260918 Base, full-active model and legal-candidate metadata, frozen room-to-streamer mapping. Preserve run IDs, artifact IDs, timestamps and Git SHAs.
3. Search repository and existing self-hosted cache manifest for **both** original room and streamer checkpoints. A scored per-user CSV or inference log is **not** an interchangeable checkpoint.
4. Produce machine-readable `preflight.json` with artifact status, plus `preflight.md` with feasible next stage. Do not auto-trigger retraining. A missing checkpoint is a valid audited outcome.

Expected runs to audit:
- `35554842873` — KuaiLive room-collision data.
- `35559499838` — latency checkpoints (historically 14-day retention).
- `35580324870` — full-active dual-ID results.
- `35729896175` — Base-seed robustness results (per-user predictions; may not include model weights).
- `35829433706` — evidence-state closure and decomposition.
- `35571827672` — sampled-gate compression artifact.

## Stage B — fixed-checkpoint dual candidate scoring (conditional)

**Gate:** both room and streamer checkpoints must exist, be readable, match the pinned ReChorus model configuration, and have SHA-256 recorded. Verify aligned room/streamer datasets, target IDs, and candidate lists before scoring.

- Precompute each user's 64-dimensional room/streamer hidden vectors **once** per checkpoint for a given evaluation phase; avoid redundant Base forward passes.
- For each user, derive both candidate lists, score the **union** of room candidates and deduplicate repeated streamer IDs, then extract both sampled and full subsets. Apply the frozen Dual-ID coefficient and separate candidate-wise z-scoring for each subset.
- Read the original `neg_items` to reproduce the exact sampled candidate list; do not simulate a new set of 574 negatives.
- Compute Memory scoring consistently over each candidate set, retaining training popularity and pre-target histories. Do not tune Memory weights, the Base mixing coefficient, or the Utility gate against TEST.
- For transparency, report both (i) fixed originally selected coefficient and (ii), **only if already frozen in the source**, an explicitly tagged development-selected native coefficient. Never claim that the latter isolates a single-candidate-set manipulation.
- Pair by immutable identifiers: `user_id, time, target_item`. Audit exact cardinality, duplicates, candidate containment, room/streamer mapping, empty / tie cases, and active target fallback.
- Prefer existing checkpoint and candidate caches; if exact original weights are unavailable, **stop and report the limitation**. Re-training a new Base requires a separately versioned deviation and cannot be labeled an exact checkpoint replication.

**Efficiency:** one embedding encoding per user and checkpoint; shared candidate-score cache; `torch.inference_mode()`; batched embedding matrix/vector products on a GPU when safely available, with bounded batches; persistent cache keyed by checkpoint hash + candidate-source hash. Keep only final per-user metrics and optional checksum summaries, not giant dense score tensors. Pin CPU BLAS threads for parallel jobs. The RTX 3090 self-hosted runner is optional; use hosted resources for preflight/statistics.

## Stage C — pre-specified inference (parallel independent light jobs)

Use user-paired values `d_{u,c}=u_{10}(M,x_{u,c})-u_{10}(B,x_{u,c})`; report
`mean(d_full) - mean(d_sampled)`, and the identity
`difference = (Memory_full–Memory_sampled) – (Base_full–Base_sampled)`.

- Deterministic user-level bootstrap (5,000 draws; fixed documented seed), two-sided 95% percentile CI. Sampling unit is user, not room candidate.
- Report NDCG@10 and H@10; paired event count, active candidate sizes and confidence intervals.
- State-specific means, counts, paired changes, and contribution `P(S=s) × state mean` under each regime. State label consistency across candidate regimes is checked.
- Technical success criteria: exhaustive alignment, no missing scores, correct identity reconstruction (tolerance < 1e-10), and complete provenance. **Result signs and p-values are not success criteria**.
- Record both successful and null outcomes. The tests are post-hoc mechanism/validity diagnostics, *not* a second untouched test or a policy-tuning exercise.

## Interpretation / decision table

1. Fixed checkpoint retains reversal: candidate construction measurably changes the operational relative ranking value under that Base; does **not** establish intrinsic evidence information changes.
2. Fixed checkpoint changes magnitude but no sign flip: narrow the claim to conditional candidate-regime sensitivity.
3. Weak or checkpoint-dependent effects: report observed regime comparisons and downgrade causal candidate-set explanation.
4. Checkpoint absent: use original frozen results with provenance and caveat; do not silently mix runs or retrain for a favorable outcome.

## Manuscript boundaries

Do not change Section 1–4 or the sole main outline until the diagnostic and provenance report have been reviewed. Existing TEST selection policies remain frozen. A new TEST evaluation, if scientifically justified, must be labeled a **post-hoc audited comparison**. No new ranking model, memory or gate hyperparameter search.

## External methodological motivation

Pereira, Said, and Santos, *On the Reliability of Sampling Strategies in Offline Recommender Evaluation*, RecSys 2025, DOI: 10.1145/3705328.3748086. Candidate sampling can change model ordering; pairing and provenance are necessary, but not sufficient, for causal claims.


## Authorized extension — one new fixed diagnostic Base (2026-10-08)

The original KuaiLive Room/Streamer checkpoint pair was not recoverable from
the reviewed GitHub and 3090 caches. The user authorized one newly trained
post-hoc diagnostic Base, explicitly separate from the original checkpoint.

The original candidate-data artifact from Actions run 35554842873 also expired.
Data reconstruction is now a prerequisite rather than an optional optimization.

Scientific and execution boundaries:

1. Rebuild input data on GitHub-hosted CPU using official KuaiLive Zenodo
   record 16565801, the original project exporters and seed 20260918.
   Require 10,222 users and 575 sampled candidates, capture MD5/SHA-256,
   and DO NOT claim bytewise equivalence to an expired input.
2. Train exactly one new fixed Room/Streamer Base checkpoint pair with pinned
   ReChorus revision and original model training hyperparameters. Preserve
   both trained checkpoints, data/model SHA-256 and provenance in artifacts.
3. Hold room-mixture weight 0.10 fixed for both candidate regimes, do not
   search over mixtures or retune any gate on TEST.
4. Evaluate each user under sampled and full active sets with identical
   learned Base weights and Memory definition. Encode user sequence once
   per model and phase; retain independent candidate-wise score normalization.
5. Run DEV structural checks first. Label any TEST diagnostic explicitly
   post-hoc, distinct from the earlier untouched held-out policy evaluation.
6. Aggregate paired user-level statistics and evidence-state decomposition
   under prespecified tests, preserving outcomes irrespective of direction.
7. Keep the author's original Sections 1–4, main writing outline, and all
   original experiment artifacts untouched until scientific review.

Preflight failures (no training performed): 37741207359 lacked sklearn;
37741380787 lacked gh CLI; 37741589624 discovered expired frozen-data artifact.
Corrections: temporary isolated dependencies and the official artifact API,
followed by deterministic hosted regeneration of unavailable inputs.

Data rebuild Actions: 37741843252.
Synthetic code-integrity Actions: 37742133747 (passed).
Branch: kbs-fixed-checkpoint-diagnostic-20261008.
