# N15 P1-B — Full-vs-Long source × supervision interaction gate

**2026-10-28 · implementation complete; public synthetic QA PASS; private DEV execution queued. No P1-B empirical result is claimed in this report.**

## Objective

Extend the N15 P1-A exact-call sensitivity analysis to the source dimension, using only the already-certified B1 and B2 original DEV artifacts. The primary estimand is

`D_source(q) = NDCG10_F(F-supervised source-specific selector) - NDCG10_F(S-supervised source-specific selector)`

and the source-by-supervision interaction is

`I(q) = D_full(q) - D_long_only(q)`.

This measures whether the F-vs-S supervision gap in the offline exact-call policy differs between Full and Long-only Memory. It does not identify a randomized label-only causal effect.

## Implemented

- `analysis/kbs_plan_c/n15_p1b_source_supervision_interaction_dev.py`
- `analysis/kbs_plan_c/test_n15_p1b_source_supervision_interaction_dev.py`
- `.github/workflows/kbs-n15-p1b-source-interaction-dev.yml`

The public preflight has passed in Actions run [#40622237969](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40622237969): syntax compilation, five synthetic-only tests (quota exactness, permutation invariance, ties, invalid inputs, allocation identity, interaction identity, deterministic cluster bootstrap), and static source-scope checks. It reads no private files.

## Source and design gates

- B1 source is required to match schema, scope, event/user counts, exact frozen SHA256 `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`, and `test_accessed=false`.
- B2 source is required to match its own private manifest SHA, full-cohort 50,049 events/12,628 users, B1 source SHA, zero Full-F/S parity mismatches, target-retained sampling labels offline-only, no new TEST opened, no retraining, and prior nested selector not already fitted.
- B1 and B2 rows are joined by internal event_id and must have identical event coverage, user assignment, Base scores, Full scores, and original 12 pretarget features. Any mismatch aborts before model fitting.
- For each Base family, source, and supervision target, fit a separate fixed-capacity HGB regressor on outer training users and score held-out users. Same five outer user-disjoint folds, same 12 features, same seed/capacity, same protected row-index tie rule and exact q∈{.10,.20,.30,.40} calls per outer fold.
- Evaluate both source-specific policies on the matching source's full-active F incremental utility. Report Full and Long-only absolute metrics, positive incremental-value support, F/S source-specific D gaps, and `I(q)`, with user-cluster bootstrap intervals explicitly labelled descriptive.
- No B4-A population weights, no TEST/G5 files, no per-event rows, no model weights, no user IDs or event IDs in output. Aggregate-only JSON is the sole artifact.

## Current execution state

- Public synthetic-only preflight: **PASS**.
- Private B1/B2 source check + run: **QUEUED/PENDING**, Actions run [#40622237969](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40622237969). A second push queued a duplicate run [#40622271751](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40622271751); concurrency is serialized.
- **No source-interaction number, sign, confidence interval or scientific result is available yet.** Do not infer it from the prior B2 threshold policy results: those used a different estimand and had natural call-rate drift.
- If private source hash/schema/parity fails, the experiment must stop and record `NOT_IDENTIFIABLE_FROM_AVAILABLE_ARTIFACT`; no substitute labels or fabricated aggregates.
- Even if the run succeeds, result remains reused, post-G5 exploratory DEV; P3 fresh independent cohort and KBS submission decision remain HOLD.

## Literature boundary

Krichene & Rendle (KDD 2020) already establish that sampled top-k ranking metrics can reverse model comparisons. The contribution must therefore not be framed as discovering generic sampled-metric inconsistency; it can only be a source-specific decision-quality mechanism if the gated interaction is stable, interpretable, and later prospectively confirmed.


## Completed run — 2026-10-28

**Status corrected: COMPUTATION PASS; results available; interpretation remains DEV_EXPLORATORY_ONLY.**

Successful latest run: [Actions #40622271751](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40622271751). Aggregate-only artifact: [n15-p1b-source-interaction-dev-aggregate](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40622271751/artifacts/12788126538). Artifact ZIP SHA256: 6aab1febf65a5fde75535c69ec0040e14970501058e05021e14abaa66153e214. The run checked 50,049 DEV events and 12,628 users; B1/B2 source parity passed; no TEST labels were accessed.

At the primary quota q=0.30 (15,014 calls per policy/source):
- SASRec: D_Full=+0.006133; D_LongOnly=+0.011180; interaction I=-0.005047, descriptive user-cluster 95% interval [-0.007022,-0.003235].
- GRU4Rec: D_Full=+0.005398; D_LongOnly=+0.010291; interaction I=-0.004893, descriptive user-cluster 95% interval [-0.006725,-0.003070].

The interaction is negative at all four predeclared quotas (0.10, 0.20, 0.30, 0.40) for both Base families; all eight descriptive intervals exclude zero. At q=0.30, Long-only also has more switched decisions than Full (SASRec 8,221 vs 5,338 F-only/S-only pairs; GRU4Rec 7,812 vs 5,786), with larger mean full-F utility separation between exchanged decisions.

Interpretation: under this fixed offline equal-call policy, the F-vs-S supervision gap is consistently smaller with Full than with Long-only. This is not a causal source effect, independent replication, real-time feasibility result, or TEST confirmation. P1-B and P1-A reuse the same DEV cohort; their agreement is a parity/estimand-sensitivity check, not independent evidence. Preserve P3 and KBS submission decision as HOLD pending a fresh eligible cohort or a defensible non-causal manuscript framing.
