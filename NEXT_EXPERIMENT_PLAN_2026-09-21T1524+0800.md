# KuaiLive-Agent — Revised Next Experiment Plan (P0 / P1 / P2)

**Original snapshot:** 2026-09-21 15:24 +08:00  
**Revision:** 2026-09-21, after paper-skeleton / novelty / protocol audit  
**Current phase:** paper-closing / validity-closure, not model-expansion.

---

# 1. Executive decision

Completed questions should remain closed:

- strict temporal validity: **closed**;
- persistent-streamer identity shortcut: **closed**;
- generic adaptive-computation collision: **closed sufficiently**;
- selector/inference latency: **closed**.

The remaining high-information risks are:

1. sampled-candidate dependence;
2. whether the selector really tracks **specialist-minus-base utility**, not only generic base difficulty;
3. whether state + confidence remains informative under the final Dual-ID base;
4. direct room-level competitor compatibility;
5. cross-platform external validity.

Do not add broad model families unless a specific reviewer-risk analysis justifies them.

---

# 2. P0-A — Full-active live-room ranking (highest-risk remaining experiment)

## Why it remains the top validity test

The final ordinary-regime room result still uses target + 574 legal active negatives. Five sampled-negative seeds are positive, but full-active ranking is the cleanest answer to candidate-sampling dependence.

## Critical protocol correction

The old plan treated full-active as if only the evaluation candidate list changed. That is not true in the frozen implementation:

- room and streamer SASRec scores are z-normalized **within the candidate set** before Dual-ID fusion;
- confidence features (std, range, margins, normalized entropy, top-10 softmax mass) depend on candidate-set size/distribution.

Therefore 575 → full-active changes the Dual-ID representation and gate feature distribution. Full-active must be reported in two pre-specified modes rather than interpreted as one undifferentiated transfer test.

## P0-A1 — Strict-transfer stress test

Purpose: test whether the original sampled-regime policy transfers under candidate-universe expansion.

Freeze from the sampled-active regime:

- Dual-ID fusion alpha;
- HGB architecture/model where feature definitions are computable;
- decision threshold;
- MemoryFusion semantics.

Recompute only quantities mechanically required by the new candidate universe. Do **not** use full-active test for calibration.

Interpretation:

> transfer robustness of the frozen sampled-candidate policy.

A failure here does not by itself prove the memory mechanism is invalid because candidate-dependent feature calibration has shifted.

## P0-A2 — Full-active-native evaluation

Purpose: answer the scientific validity question under the correct candidate universe.

Allowed on **full-active dev only**:

- select room/streamer fusion alpha;
- recompute full-active confidence features;
- refit utility estimator;
- choose escalation threshold.

Then evaluate full-active test once.

No test-driven rescue tuning.

## Shared frozen semantics

- target = `live_id`;
- candidates = all legally active rooms satisfying start <= t < end;
- no future/inactive rooms;
- same frozen room/streamer SASRec checkpoints;
- same MemoryFusion relationship-memory definition;
- same user-state feature semantics;
- chunk/stream scores; never construct dense user × million-room tensors.

## Report

For both A1 and A2:

- NDCG@10;
- HR/Recall@10;
- paired user bootstrap >= 5,000;
- invocation rate;
- active candidate-count mean/median/p10/p90/p95/max;
- wall-clock and peak-memory descriptive metadata.

Also report sampled-active 575 beside both full-active variants.

## Decision rule

Primary scientific pass is **A2**:

- Selective − Dual-ID > 0;
- 95% CI lower bound > 0.

A1 is a transfer/stability diagnostic, not the sole validity criterion.

If A2 is weak positive: narrow effect-size language.  
If A2 is null/negative: do not rescue on test; define sampled-active ranking as an empirical boundary condition.

---

# 3. P0-B — Conditional-utility mechanism closure (run now)

This is the central conceptual analysis and should become Main Figure 2.

## P0-B1 — Utility calibration / heterogeneity

Using the frozen Dual-ID test artifact:

1. sort by frozen predicted relative utility;
2. deterministic equal-sized deciles;
3. realized `Memory − Dual-ID` NDCG@10 per decile;
4. positive-realized-utility fraction per decile;
5. Spearman rank association;
6. cumulative selective gain vs invocation budget.

Desired conclusion:

> predicted memory-relative utility tracks realized specialist advantage.

Do not call this probabilistic calibration unless a calibrated probability is explicitly modeled; “utility stratification / monotonicity” is safer.

## P0-B2 — Generic-difficulty control at matched budget

Train on dev, with exactly the same state+confidence features:

- utility router target: `Memory − Base`;
- difficulty router target: base ranking loss / `1 − Base NDCG@10`.

On frozen test, invoke Memory for **exactly the same K users/events** as the frozen HGB utility router.

Report:

- Base;
- relative-utility router;
- difficulty router;
- paired bootstrap for utility − difficulty.

This is the direct answer to the reviewer objection that the selector merely escalates hard cases.

## P0-B3 — Oracle headroom

Report:

- exact-K oracle: select the K largest realized `Memory − Base` deltas;
- unrestricted oracle: invoke Memory exactly where realized delta > 0;
- fraction of oracle gain captured by the frozen selector.

Purpose: distinguish gate-estimation headroom from specialist-model headroom.

## Current execution

Implemented in:

- `analysis/conditional_utility_closure_dual_id.py`
- `.github/workflows/conditional-utility-closure-dual-id.yml`

The workflow reuses frozen Dual-ID artifacts; it does **not** retrain the base recommender.

---

# 4. P0-C — Dual-ID information-source ablation (run with P0-B)

The earlier state/confidence evidence was mainly tied to the earlier SASRec-v2 chain. The final paper needs the minimal ablation under the final Dual-ID base.

Required rows:

- history threshold;
- state-only HGB;
- confidence-only HGB;
- state + confidence HGB;
- frozen state+confidence primary row clearly marked as the scientific source of truth.

All threshold/model selection remains dev-only. No test hyperparameter search.

Primary question:

> Does base confidence add useful information about memory-relative utility after persistent streamer identity has already been absorbed into the Dual-ID base?

Do not turn this into a gate-architecture benchmark.

---

# 5. P0-D — DCGLive compatibility audit (promoted from P2)

DCGLive / “Room Matters” (WWW 2026) is a direct modern room-level live-stream competitor with public KuaiLive code. Its repository provides a KuaiLive training/evaluation path.

Run a **compatibility audit before any expensive training**.

Compare:

- target definition;
- data subset;
- temporal split;
- candidate/exposure construction;
- negative sampling/full ranking semantics;
- room/streamer identity representation;
- metric definitions.

Decision:

- if the official setup can be mapped to the frozen next-live-room task without redefining the task, promote DCGLive to a submission baseline;
- if not, document the incompatibility explicitly and keep it as related work rather than manufacturing an invalid numeric comparison.

Do not delay P0-A for a large DCGLive retraining attempt.

---

# 6. P0-hygiene — Statistical consistency cleanup

Recompute the DS streamer-projected matched-budget bootstrap with 5,000 resamples.

- no retraining;
- frozen predictions;
- same exact-K budgets;
- same dev-selected slow variant.

This is useful statistical hygiene but is not a scientific kill gate.

---

# 7. P1 — One untouched cross-platform external validation

## Preferred dataset: LiveRec Twitch 100k

Reference repository: https://github.com/JRappaz/liverec

It provides:

- 100k users;
- ~3M interactions;
- ~162.6k streamer/channel items;
- dynamic availability;
- repeat-consumption structure;
- a different platform from Kuaishou.

## Important adjustment

Do **not** make vanilla SASRec the only external base if the official LiveRec implementation can be reproduced reasonably. LiveRec itself explicitly models current availability and repeat consumption, so the strongest validation is:

> strong availability/repeat-aware base vs Always explicit memory vs Selective memory.

A vanilla SASRec row can remain as a reference baseline.

## Frozen external protocol

Before inspecting test outcomes:

- freeze train/dev/test split;
- freeze availability construction;
- freeze strong base architecture/configuration from dev;
- define explicit relationship-memory specialist from history only;
- transfer the state/confidence feature definitions that are semantically valid;
- fit gate/threshold on dev only;
- evaluate test once;
- bootstrap by user.

Success criterion:

- Selective − strong Base > 0;
- 95% CI lower > 0.

If null/negative: no test retuning. Treat it as a cross-platform boundary on the prevalence/predictability of memory utility.

Role in the paper:

> cross-platform validation of the conditional relationship-memory principle, not replication of KuaiLive room-vs-streamer identity geometry.

---

# 8. P2 — Optional expansion

## P2.1 — KuaiLive-M3

Useful contemporary within-ecosystem validation, but weaker externality than Twitch.

## P2.2 — Richer uncertainty estimators

Ensemble variance / MC dropout / calibrated confidence. Low priority because the paper is not about discovering the best uncertainty estimator.

## P2.3 — Secondary behavioral outcomes

Repeat vs novel streamer, head/tail, engagement/satisfaction where valid. Do not introduce causal GMV/purchase claims.

## P2.4 — Genuine LLM/agentic extension

Separate paper direction. Do not rebrand current MemoryFusion as an LLM agent.

---

# 9. Work that stays closed / dropped

## CLOSED — temporal validity

GTS-Last and GTS-Successive already establish regime dependence.

## CLOSED — persistent identity shortcut

Dual-ID already absorbs room/streamer identity and Selective remains significantly above the base.

## CLOSED — generic adaptive-computation collision

DS-Frame comparisons are sufficient for this paper; do not claim routing superiority.

## CLOSED — latency/gate cost

HGB/Ridge/tiny-MLP evidence is sufficient unless full-active serving changes implementation materially.

## DROP — another official direct room-ID DS-Frame full-softmax attempt

The ~1.18M room universe makes the unchanged official objective impractical; sampled-softmax modifications would change scientific equivalence.

## DEPRIORITIZE — more sampled-negative seeds

Five are enough. Full-active is higher-information.

## DEPRIORITIZE — more generic sequential backbones

Low marginal value relative to P0-A/B/C/D.

---

# 10. Execution order from this revision

## Already launched

1. **P0-B + P0-C**: utility calibration, difficulty control, oracle headroom, Dual-ID information ablation using frozen artifacts.

## Immediate engineering

2. **P0-A**: implement full-active streaming scorer with two protocols (A1 strict-transfer, A2 dev-native).
3. **P0-D**: DCGLive compatibility audit in parallel; only train if protocol mapping is scientifically valid.
4. **P0-hygiene**: DS projected 5k bootstrap.

## After P0

5. Freeze main figures/tables and update paper skeleton with actual P0 outcomes.
6. Run **P1 LiveRec Twitch 100k**, preferably against a reproduced strong LiveRec availability/repeat-aware base.
7. Decide on P2 only after target-journal decision and P1 outcome.

Manuscript drafting proceeds in parallel throughout; do not wait for P1 to write the Introduction/Related Work/Methods.

---

# 11. Stopping rules by journal

## ESWA first

Recommended submission minimum:

- P0-A full-active;
- P0-B conditional-utility mechanism closure;
- P0-C Dual-ID information ablation;
- P0-D compatibility audit with either valid DCGLive result or explicit incompatibility rationale;
- statistical cleanup;
- polished deployment framing.

P1 strongly preferred but not necessarily a hard blocker if P0 is strong.

## KBS / Information Sciences

Successful P1 materially strengthens the generalized specialist-utility claim.

## IPM

P0-B and temporal-regime interpretation are especially important; emphasize information value/confidence and regime dependence.

---

# 12. Final hierarchy

> **P0 = full-active internal validity + direct relative-utility-vs-difficulty mechanism closure + final-base information ablation + room-competitor compatibility.**  
> **P1 = one untouched cross-platform validation on Twitch with a strong availability-aware base.**  
> **P2 = same-ecosystem contemporary validation / richer uncertainty / secondary outcomes / future LLM extension.**

The project remains in paper-closing mode. New experiments should be admitted only when they close a specific reviewer-visible validity or novelty gap.
