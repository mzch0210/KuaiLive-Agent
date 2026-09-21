# KuaiLive-Agent — Revised Next Experiment Plan (P0 / P1 / P2)

**Snapshot timestamp:** 2026-09-21 15:24 +08:00  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Purpose:** self-contained handoff for future ChatGPT accounts / collaborators.  
**Current phase:** paper-closing / validity-closure phase, not model-expansion phase.

---

# 1. Executive decision

The earlier project priorities were appropriate and produced high-value evidence:

- temporal validity: **closed**;
- identity shortcut: **closed**;
- adaptive-computation collision: **closed sufficiently for this paper**;
- inference latency / cost: **closed**.

The next plan should therefore **not** continue adding large baseline families. The main remaining risks are:

1. sampled-candidate dependence;
2. whether predicted conditional utility is visibly calibrated to realized specialist advantage;
3. whether the final Dual-ID gate still needs state + confidence, not only the earlier SASRec gate;
4. single-platform external validity.

The correct strategy is: **P0 closes internal validity and the central mechanism; P1 tests cross-platform external validity; P2 is optional reviewer-defense / expansion work.**

---

# 2. Work that is already complete and should not be reopened

## CLOSED — strict temporal validity

GTS-Last and GTS-Successive both strongly pass the frozen event-level + user-cluster bootstrap criteria.

Scientific result:

- ordinary LOO: memory is globally inferior but selectively useful;
- temporal shift: memory becomes broadly useful;
- invocation expands from ~14% to ~60–75%;
- Selective preserves ~94–97% of full-memory gain.

Do not spend compute on another near-duplicate temporal split unless requested by reviewers.

## CLOSED — persistent-identity shortcut

Dual-ID explicitly models room and streamer sequences; dev fusion is 90% streamer weighted. Memory remains globally inferior, yet frozen Selective improves Dual-ID by +0.01317 with positive CI.

No further identity baseline is currently required.

## CLOSED — generic adaptive-computation collision

DS-Frame is now adequately covered for mechanism differentiation:

- official streamer-level PRL comparison;
- exact matched-budget routing;
- streamer-projected live-room collision defense.

Direct official room-ID PRL should not be retried under the unchanged full-softmax objective on the ~1.18M room universe. The failed run reflects the official implementation/objective scaling, not a semantic mapping error.

## CLOSED — inference latency and gate cost

Three-replica warmed CPU latency + gate compression are complete.

Key finding:

- HGB selector cost is a major component of end-to-end overhead;
- Ridge is dramatically cheaper and is faster end-to-end despite invoking memory more often;
- invocation rate alone is not a valid compute proxy.

Do not rerun broad latency experiments unless P0 full-active ranking requires a materially different serving implementation.

---

# 3. NEW P0 — submission-critical internal validity + mechanism closure

These tasks have the highest expected information value and should be completed before the results section is frozen.

## P0.1 — Full-active live-room ranking

### Why this is the most important remaining validity test

The current primary room-level evaluations use the positive plus 574 legal active-at-target negatives. Five frozen candidate seeds all produce positive CIs, but a reviewer can still ask whether the effect depends on sampled ranking.

A full-active evaluation directly closes that objection.

### Frozen protocol

- target = `live_id`;
- candidates = **all legally active rooms at the target timestamp**;
- no future rooms / no inactive rooms;
- reuse frozen room + streamer Dual-ID checkpoints;
- reuse MemoryFusion semantics;
- preserve frozen HGB utility policy wherever the feature definition is unchanged;
- score candidates in streaming/chunked form; never construct dense user × million-room tensors;
- primary comparison: Dual-ID vs Always Memory vs Selective HGB;
- Ridge deployment variant secondary only.

### Report

- NDCG@10;
- HR / Recall@10;
- paired user-cluster bootstrap >= 5,000;
- invocation rate;
- mean / median / quantiles of active candidate count;
- computational feasibility / wall-clock as descriptive systems metadata.

### Decision rule

- **Pass:** Selective − Dual-ID mean > 0 and 95% CI lower > 0.
- **Weak positive:** keep the mechanism claim but narrow the effectiveness claim.
- **Null/negative:** do not tune to rescue. Explicitly define sampled-active candidate ranking as a boundary condition.

### Priority judgment

**Keep as P0.** This remains the only remaining experiment that could materially weaken the main room-level effectiveness interpretation.

---

## P0.2 — Conditional-utility heterogeneity / calibration analysis

### Why it matters

This analysis directly visualizes the paper’s central construct and is more valuable than another conventional baseline.

### Frozen analysis

Using dev-selected utility scores and frozen test outputs:

1. sort users/events by predicted `hat(Delta_memory)`;
2. divide into deciles (or ventiles if stable);
3. compute realized `Memory − Base` utility per bin;
4. report fraction of positive realized utility per bin;
5. plot cumulative realized gain vs escalation budget;
6. optionally add rank correlation / monotonic trend test.

### Desired conclusion

> Predicted relative utility tracks realized specialist advantage; the gate is not merely a generic difficulty detector.

### Priority judgment

**Promote to P0 and run in parallel with P0.1.** It is cheap and directly supports the new conceptual thesis.

---

## P0.3 — Dual-ID state / confidence information ablation

The earlier frozen SASRec-v2 chain already shows state+confidence > state-only. However, the final strongest base is Dual-ID, so the paper should replicate the minimal information-source ablation under this base.

### Required variants

- history / simple threshold;
- state only;
- confidence only;
- state + confidence;
- optional HGB vs Ridge estimator comparison as secondary.

No test hyperparameter search.

### Main question

> Does base confidence still contribute useful relative-utility information after persistent identity has already been absorbed by the Dual-ID model?

### Priority judgment

**Keep as P0**, because it links the method claim to the final primary base.

---

## P0.4 — Statistical consistency cleanup

Recompute the DS streamer-projected matched-budget bootstrap using **5,000 resamples** instead of the earlier 2,000.

- no retraining;
- frozen predictions;
- same exact-K budgets;
- same dev-selected slow variant;
- same user-cluster bootstrap semantics.

### Priority judgment

**Keep as P0 but lowest P0 cost/urgency.** It is cheap and removes an avoidable inconsistency.

---

# 4. NEW P1 — one untouched cross-platform external validation

## Preferred dataset: LiveRec Twitch 100k

### Why it is currently the best external test

LiveRec provides:

- 100k-user public benchmark subset;
- ~3M interactions;
- ~162.6k streamer items;
- dynamic item availability;
- explicit repeat-consumption motivation;
- cross-platform validation outside Kuaishou.

Source: https://github.com/JRappaz/liverec

### Important limitation

LiveRec’s target item is the streamer/channel rather than an ephemeral `room_id`. Therefore it cannot replicate the exact room-vs-streamer identity-control geometry of KuaiLive.

Its role should be stated narrowly:

> **cross-platform validation of the conditional-specialist principle under dynamic availability and repeat consumption**, not replication of every room-level mechanism claim.

### Frozen external protocol

Before inspecting test results:

- freeze base architecture;
- define explicit memory specialist using train-history-only repeat/relationship signals;
- freeze user-state/confidence feature definitions where transferable;
- fit gate / threshold on dev only;
- evaluate test once;
- respect dynamic item availability;
- report Base / Always Memory / Selective;
- bootstrap by user.

### External success criterion

Selective − Base mean > 0 with 95% CI lower > 0.

If null/negative:

- no test retuning;
- report honestly;
- narrow generalization claims;
- interpret as another boundary on specialist-utility regimes, consistent with the paper’s broader thesis.

### Priority judgment

**Keep as P1, not P0.** For ESWA the paper may already be publishable after P0; for KBS / Information Sciences, a successful external dataset would materially strengthen the general mechanism claim.

---

# 5. P2 — optional expansion / reviewer defense

## P2.1 — KuaiLive-M3

Public 2026 dataset:

- 21,938 users;
- 35M live interactions;
- 111M short-video interactions;
- timestamped segment-level multimodal embeddings;
- questionnaire-based explicit feedback.

Source: https://arxiv.org/abs/2607.24862

Use only if schedule allows. It strengthens within-domain external confirmation but is still Kuaishou ecosystem data, so it is weaker than Twitch for cross-platform generalization.

## P2.2 — DCGLive stronger live-room dynamics baseline

DCGLive (WWW 2026) is the closest room-level dynamics competitor and directly models evolving room-streamer-user collaboration.

Source: https://doi.org/10.1145/3774904.3792241

Run only if:

- public code/data semantics can be matched to the frozen next-live-room task;
- compute is reasonable;
- no task redefinition is required.

Do not delay submission indefinitely for this baseline if the protocols are materially incompatible.

## P2.3 — richer uncertainty estimators

Examples:

- ensemble variance;
- MC dropout;
- calibrated probabilistic confidence.

Low priority. The novelty is not “best uncertainty model.” Existing margin/entropy features already establish that base confidence matters.

## P2.4 — secondary behavioral outcomes

Possible only where valid labels exist:

- repeat vs novel streamer;
- head vs tail;
- engagement signals;
- explicit satisfaction on KuaiLive-M3.

Do not introduce causal GMV/purchase claims.

## P2.5 — genuine LLM / agentic extension

Separate paper direction. Current MemoryFusion should not be rebranded as an LLM agent merely because 2026 memory-agent literature is active.

---

# 6. Tasks to drop / deprioritize

## DROP — another official direct room-ID DS-Frame hosted-CPU attempt

Reason:

- ~1.18M room universe;
- official PRL full-item path;
- ~75.5M parameters;
- previous runner shutdown during scoring/training;
- sampled-softmax / aggressive batch changes alter scientific equivalence.

The streamer-projected room adapter already answers the collision question more cleanly.

## DEPRIORITIZE — more sampled-negative seeds

Five seeds already remain positive. Full-active ranking is more informative.

## DEPRIORITIZE — more generic recommender backbones

The current evidence includes tuned sequential baselines, room/streamer identity control, memory variants, temporal validation, and adaptive-computation collision defense. Another standard backbone has low marginal value.

## DEPRIORITIZE — replacing HGB as the universal scientific primary gate

Ridge is an excellent deployment variant. Retrofitting the entire robustness/GTS chain to Ridge would consume significant compute without materially strengthening the core mechanism claim.

---

# 7. Recommended execution order

## Immediate parallel work

1. **P0.1 Full-active ranking** — highest-risk experiment.
2. **P0.2 Utility decile/calibration** — cheap, high conceptual value.
3. **P0.4 DS projected bootstrap 5k** — cheap cleanup.

## Then

4. **P0.3 Dual-ID state/confidence ablation**.
5. Freeze main result tables and figures.
6. Begin full manuscript writing immediately; do **not** wait for P1 to start drafting.
7. Run **P1 LiveRec Twitch 100k** as the external confirmation.
8. Decide whether P2 KuaiLive-M3 / DCGLive is worth the delay based on the target journal and P1 outcome.

---

# 8. Target-journal-dependent stopping rule

## If targeting ESWA first

Minimum recommended before submission:

- P0.1 full-active ranking;
- P0.2 utility calibration;
- P0.3 Dual-ID information ablation;
- P0.4 bootstrap consistency;
- polished paper with strong application + deployment framing.

P1 external validation is strongly preferred but not necessarily a hard blocker if P0 is strong.

## If targeting KBS / Information Sciences

A successful P1 external dataset becomes much more valuable because the manuscript’s conceptual claims are more general.

## If targeting IPM

P0.2 and temporal-regime interpretation are especially important; information-value interpretation may matter more than another model baseline.

---

# 9. Final P0 / P1 / P2 verdict

The revised priorities are scientifically reasonable and should be retained with one adjustment from earlier planning:

> **Manuscript drafting should begin in parallel with P0 rather than after all new experiments are finished.**

Final hierarchy:

- **P0 = full-active internal validity + direct conditional-utility mechanism closure + statistical cleanup**;
- **P1 = one untouched cross-platform external validation, preferably LiveRec Twitch 100k**;
- **P2 = second external dataset / DCGLive / richer uncertainty / secondary outcomes**.

This order minimizes the risk of spending large compute on low-information additions while leaving a reviewer-visible validity gap unresolved.
