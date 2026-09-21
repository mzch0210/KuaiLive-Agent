# LiveRec Twitch 100k — P1 External Validation Protocol

**Date frozen:** 2026-09-21  
**Dataset/code lineage:** JRappaz/liverec / RecSys 2021  
**Status:** protocol frozen before any external test-model result is inspected.

---

## 1. P1 question

> **Does conditional relationship-memory utility transfer to a different live-stream platform with dynamic availability and repeat consumption?**

This is a cross-platform test of the conditional-specialist principle. It is **not** intended to reproduce KuaiLive's ephemeral-room / persistent-streamer Dual-ID geometry.

---

## 2. Why LiveRec / Twitch 100k

The official LiveRec benchmark provides:

- 100k users;
- ~162.6k streamers;
- ~3M interaction rows;
- 6,148 ten-minute timesteps;
- dynamic availability;
- explicit repeat-consumption structure;
- a platform outside Kuaishou.

The UCSD dataset mirror exposes the 100k benchmark directly as `100k_a.csv` (~109 MB). The official repository expects the same five fields: user, stream, streamer, start, stop.

---

## 3. Freeze official data semantics

Preserve the official implementation's semantics rather than redesigning the split around KuaiLive.

### IDs

- factorize users and streamers in file order;
- +1 offset for padding, matching the official code.

### Availability

At timestep `s`, a streamer is a legal candidate iff at least one interaction row satisfies:

`start <= s < stop`.

Do not rank unavailable streamers.

### Time split

Let `max_step = max(max(start), max(stop))`.

- `pivot_1 = max_step - 500`;
- `pivot_2 = max_step - 250`.

Official windows:

- train target: `[0, pivot_1)`;
- validation target: `[pivot_1, pivot_2)`;
- test target: `[pivot_2, max_step)`.

For each user/split, reproduce the official `get_sequences` logic:

- retain interactions with `stop < split_end`;
- sort by start time;
- retain at most `seq_len + 1` most recent interactions;
- use the final interaction as target if its start lies within the split;
- use up to `seq_len` preceding interactions as model sequence.

Primary `seq_len = 16`, matching official defaults unless dev-only reproduction demonstrates a configuration issue.

---

## 4. Strong external base

### Primary base

Reproduce the official **LiveRec** model with both official repeat/context switches enabled:

- `fr_ctx = true`;
- `fr_rep = true`;
- official self-attentive availability-aware ranking;
- dev-only early stopping;
- no test tuning.

The official run script uses this configuration.

### Reference base

A vanilla SASRec-style sequential row may be added for context, but it must not be the only external baseline.

### Reproduction rule

Before adding Memory, verify that the base:

- ranks only currently available streamers;
- produces finite validation/test metrics;
- shows the expected repeat/new split behavior;
- has no test leakage.

If exact historical paper metrics cannot be reproduced because of modern dependency/runtime differences, freeze the closest faithful code path and document the discrepancy before inspecting selective-memory test results.

---

## 5. Explicit relationship-memory specialist

Use the same interpretable structure as KuaiLive, transferred to streamer/channel items.

For user `u` and available streamer `i`, compute from history strictly before the target:

- short-term relationship score: exponential recency over recent streamer visits;
- long-term relationship score: normalized visit frequency;
- train-only global streamer popularity.

Primary frozen score:

`MemoryFusion = 0.45 * short + 0.45 * long + 0.10 * popularity`.

Do not tune these coefficients on test.

For validation, memory history uses only information available before each validation target. For test, it may include chronologically prior train+validation observations exactly to the extent permitted by the official split protocol; no future/test-target information is allowed.

---

## 6. Transferable utility-gate features

### User / interaction state

Use the KuaiLive feature family where semantically valid:

- log history length;
- repeat rate;
- normalized preference entropy;
- recent-vs-older preference drift;
- temporal regularity adapted to discrete 10-minute timesteps;
- state complexity composite.

### Base confidence

Compute over the official current-availability candidate set:

- score std;
- score range;
- top1−top2 margin;
- top1−top5 margin;
- top10−top11 margin where candidate count permits;
- top1 z-score;
- normalized softmax entropy;
- top-10 softmax mass.

Candidate-count dependence is accepted because P1 uses one official availability regime throughout dev/test. Report candidate-count distribution.

---

## 7. Relative-utility selector

Primary scientific gate:

- HGB with the same frozen architecture family as KuaiLive;
- target on dev: event-level `Memory NDCG@10 − Base NDCG@10`;
- five-fold OOF dev predictions for threshold selection;
- fit final gate on all dev;
- evaluate untouched test once.

Primary test comparisons:

- Base;
- Always Memory;
- Selective Memory.

---

## 8. Generic-difficulty control

Using exactly the same state+confidence features:

- fit a base-difficulty HGB on dev (`1 − Base NDCG@10` or equivalent frozen event-level base loss);
- on test, invoke Memory for exactly the same `K` events/users as the primary utility router;
- compare Utility Router − Difficulty Router with paired user bootstrap.

This tests transfer of the core mechanism, not only effectiveness.

---

## 9. Oracle / heterogeneity analysis

Report:

- predicted-utility deciles vs realized `Memory − Base` utility;
- positive-realized fraction by decile;
- Spearman association;
- exact-K oracle at the learned router's budget;
- unrestricted realized-positive oracle;
- fraction of oracle gain captured.

Use “utility stratification,” not “calibration,” unless a true probability-calibration model is introduced.

---

## 10. Metrics and statistics

Primary:

- NDCG@10;
- HR@10 / Recall@10;
- invocation rate.

Secondary:

- repeat-target vs novel-target metrics, leveraging the official LiveRec distinction;
- candidate-count distribution.

Statistics:

- paired user-level bootstrap;
- >= 5,000 resamples for final primary comparisons.

---

## 11. Frozen success / failure criteria

### Primary external success

- `Selective − strong LiveRec Base > 0`;
- 95% paired-bootstrap CI lower bound > 0.

### Mechanism replication

Preferably:

- Utility Router − Difficulty Router > 0;
- 95% CI lower bound > 0.

### If null or negative

- do not retune on test;
- report the external boundary honestly;
- narrow cross-platform generalization claims;
- keep the KuaiLive regime-dependent mechanism as the primary result.

---

## 12. No-go rules

Do not:

- replace official dynamic availability with arbitrary sampled negatives;
- make vanilla SASRec the only external base if official LiveRec can be reproduced;
- tune memory weights/gate/threshold on test;
- drop repeat/new cases after seeing outcomes;
- redefine split windows after test inspection;
- claim causal engagement/conversion effects.

---

## 13. Execution stages

1. **Data/protocol audit** — reproduce official pivots, target counts, repeat ratio, active-candidate counts.
2. **Base reproduction** — official LiveRec with availability + repeat/context features.
3. **Dev-only memory/gate fitting** — no test outcome inspection.
4. **One-shot untouched test** — effectiveness + mechanism + bootstrap.
5. **Freeze external result** — success or boundary condition, with no rescue tuning.
