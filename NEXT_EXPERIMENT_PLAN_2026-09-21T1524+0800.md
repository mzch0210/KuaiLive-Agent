# KuaiLive-Agent — Revised Next Experiment Plan (P0 / P1 / P2)

**Snapshot timestamp:** 2026-09-21 15:24 +08:00  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Purpose:** self-contained handoff for future ChatGPT accounts / collaborators. This file audits the old P0/P1/P2 priorities and defines the recommended priorities after completion of room-level identity control, GTS temporal validation, DS-Frame collision defense, exact matched-budget analysis, and inference-latency / gate-compression experiments.

---

## 1. Executive decision

The old priority plan should now be **retired and replaced**.

Legacy plan:

- **Old P0:** GTS-Last / GTS-Successive temporal validity.
- **Old P1:** DS-Frame matched-budget direct / collision comparison.
- **Old P2:** full-active ranking.

Assessment:

- Old P0 was correct and is now **completed with a strong pass**.
- Old P1 was correct and is now **completed sufficiently for the paper’s collision-defense purpose**.
- Old P2 remains scientifically important and should now be **promoted**, because sampled-candidate dependence is one of the clearest remaining internal-validity objections.

The research should now enter a **paper-closing phase**, not a model-expansion phase.

---

## 2. What has already been closed

### Temporal validity — CLOSED

GTS-Last and GTS-Successive both strongly pass the frozen event-level + user-cluster bootstrap criterion.

Key conclusion:

- ordinary LOO: memory is globally inferior but selectively useful;
- strict temporal shift: memory becomes broadly useful;
- selective routing expands from ~14% to ~60–75% and preserves ~94–97% of full-memory gain.

Do not spend more compute on another near-duplicate temporal split unless a reviewer later requests it.

### Identity shortcut — CLOSED

Dual-ID room+streamer baseline strongly absorbs persistent identity yet selective memory still improves it.

This is a central mechanism result and does not need another identity baseline unless a reviewer requests one.

### Generic adaptive-computation collision — CLOSED for current paper

DS-Frame streamer and streamer-projected room defenses are sufficient to establish the mechanism distinction:

- DS slow path globally > fast path;
- Memory globally < identity-aware base;
- selective Memory still improves the base.

Direct official room-ID DS-Frame training should **not** be retried under the current official full-softmax objective on the 1.18M-room universe. The hosted-CPU failure reflects implementation/objective scaling mismatch; sampled-softmax or aggressive batch changes would alter the scientific comparator.

### Inference cost — CLOSED

Three-replica CPU latency and gate-compression experiments are complete.

Key systems result:

- selector complexity can dominate selective-memory overhead;
- Ridge is ~255x cheaper than HGB at selector inference and achieves higher test NDCG in the current room identity-control test, but at a higher memory invocation rate;
- therefore cost must be decomposed as base + selector + invocation × specialist cost.

No need to rerun broad latency experiments unless full-active ranking creates a materially different serving path.

---

# 3. Revised priorities

## NEW P0 — Submission-critical internal validity and mechanism closure

These tasks should be completed before manuscript drafting is treated as final.

### P0.1 — Full-active live-room ranking on the frozen primary task

**Why now:** this is the largest remaining internal-validity gap. The main frozen comparisons use 574 legal active negatives + positive. Multiple seeds show candidate robustness, but this does not fully rule out sampled-negative dependence.

Protocol:

- target = `live_id`;
- legal candidates = **all rooms active at target timestamp**;
- same frozen room/streamer Dual-ID checkpoints;
- same MemoryFusion semantics;
- same frozen HGB gate where feature semantics allow direct reuse;
- streaming/per-user scoring; do not materialize a dense user × all-room matrix;
- report Dual-ID, Always Memory, Selective HGB;
- if feasible also report Ridge deployment variant as secondary.

Primary statistics:

- NDCG@10;
- HR/Recall@10;
- paired user bootstrap >= 5,000;
- invocation rate;
- average active candidate count and candidate-count distribution.

Decision rule:

> If Selective-vs-Dual-ID remains positive with CI lower bound > 0, sampled-negative dependence is substantially closed. If it disappears, downgrade the broad room-level effectiveness claim and explicitly frame the method as candidate-regime dependent.

### P0.2 — Conditional-utility heterogeneity / calibration figure

No heavy retraining should be needed.

Construct dev/test analyses using frozen per-user relative utility predictions:

1. sort events/users by predicted `hat(Delta_memory)`;
2. split into deciles (or ventiles if stable);
3. report realized `Memory - Base` NDCG contribution / rank utility per bin;
4. report fraction of users with positive realized utility in each bin;
5. optionally report cumulative gain as escalation budget increases.

Desired scientific message:

> The gate is not merely identifying “hard users”; predicted relative utility is monotonic with realized specialist advantage.

This figure directly supports the paper’s central construct and should be more important than another generic baseline.

### P0.3 — Dual-ID gate-information ablation

The original SASRec v2 experiment already shows state+confidence > state-only, but the final paper’s strongest baseline is Dual-ID. Therefore reproduce the essential ablation under the room-level identity-control setting:

- history threshold only;
- user state only;
- base confidence only;
- state + confidence;
- optional Ridge vs HGB estimator comparison.

Do not search hyperparameters on test.

Primary question:

> Does base confidence still add predictive information after persistent identity is explicitly modeled?

This is higher value than adding more generic uncertainty estimators.

### P0.4 — Statistical consistency cleanup

Bring all headline collision-defense results to the same resampling standard:

- projected-room DS matched-budget currently uses 2,000 bootstraps;
- rerun / recompute with **5,000 bootstrap resamples** using the already frozen predictions;
- no retraining;
- preserve all exact-K budgets and dev-selected slow variant.

This is cheap and removes an avoidable methodological inconsistency.

### P0 completion criterion

P0 is complete when:

- full-active ranking is resolved;
- one clear conditional-utility calibration/decile figure exists;
- Dual-ID state/confidence ablation exists;
- all headline CIs use a consistent bootstrap standard.

At that point, begin full manuscript drafting even if P1 is still running.

---

## NEW P1 — External validity with one untouched public dataset

The paper currently has very strong internal/mechanistic evidence but one primary development dataset family. A single untouched external confirmation would materially improve generalizability claims and journal positioning.

### Preferred P1 dataset — LiveRec Twitch 100k

Why first:

- public;
- 100k users, ~3M interactions in the benchmark subset;
- dynamic stream availability;
- repeat consumption is a first-class property;
- cross-platform relative to Kuaishou;
- CPU feasibility is better than the full Twitch dataset;
- scientifically close to the “persistent streamer relationship” aspect of memory.

Important limitation:

- LiveRec’s public benchmark is streamer/channel-centered rather than KuaiLive live-room-centered.

Therefore its role is **external confirmation of the conditional-specialist principle**, not replication of every room-level claim.

Frozen external protocol:

- freeze architecture and feature definitions before looking at test;
- train base on train;
- fit gate/threshold on dev only;
- evaluate test once;
- preserve dynamic availability legality;
- report Always Memory, Base, Selective;
- bootstrap by user.

External pass criterion:

> Positive Selective-vs-Base mean delta with 95% CI lower bound > 0.

If positive: the paper can make a much stronger generalization claim.

If null/negative: do not tune against test. Report the result and narrow the claim to KuaiLive-like room/streamer settings.

Source:

- LiveRec code/data: https://github.com/JRappaz/liverec

### Alternative / second P1 candidate — KuaiLive-M3

KuaiLive-M3 is public and contains 21,938 users, 35M live interactions, 111M short-video interactions, multimodal segment embeddings and explicit questionnaire feedback.

Its official live recommendation benchmarks are largely author-level. It is valuable for an in-domain confirmation of persistent relationship memory and temporal user preference, but because it shares the Kuaishou ecosystem it is weaker than Twitch as a cross-platform external validity test.

Source:

- https://arxiv.org/abs/2607.24862
- https://imgkkk574.github.io/KuaiLive-M3/

### P1 recommendation

Run **LiveRec Twitch 100k first**. Only run KuaiLive-M3 as a second external dataset if schedule and compute permit.

---

## NEW P2 — Optional expansion / reviewer-defense work

Do only after P0, and preferably after one P1 external confirmation.

### P2.1 — KuaiLive-M3 second external confirmation

Use for stronger within-domain generalization and potentially explicit satisfaction analysis.

### P2.2 — DCGLive reproduction / stronger room-dynamics baseline

DCGLive (WWW 2026) is the closest live-room dynamics competitor. Include if compatible compute becomes available and if its protocol can be matched without changing the frozen task.

Do not delay submission indefinitely for this baseline if the released implementation requires materially different data semantics or unavailable GPU resources.

### P2.3 — Richer uncertainty estimators

Examples:

- ensemble variance;
- MC dropout;
- calibrated probability features.

Low priority now. Existing evidence already shows cheap margins/entropy are useful, and the paper’s novelty is not “best uncertainty estimator”.

### P2.4 — Secondary behavioral outcomes

Only where public data supports valid labels:

- repeat vs novel streamer;
- head vs tail streamer;
- comments / likes / gifts;
- long-view / engagement.

Do not introduce causal GMV or purchase-lift claims.

### P2.5 — Genuine LLM / tool-using agent extension

Explicitly separate from the current paper. Current MemoryFusion should not be rebranded as an LLM agent. A true agentic extension can become a later paper once the selective-memory mechanism paper is stable.

---

## 4. Tasks that should be dropped or deprioritized

### DROP — another attempt at official direct room-ID DS-Frame on hosted CPU

Reason:

- 1.18M room universe;
- official PRL full-item scoring / full-softmax path;
- ~75.5M parameters in direct room setup;
- runner shutdown without Python exception;
- changing batch/objective/sampled softmax would make the comparator scientifically non-equivalent.

The streamer-projected room adapter already answers the mechanism-collision question more cleanly.

### DEPRIORITIZE — more matched-negative seeds

Five candidate seeds already show positive CIs. Full-active ranking is more informative than a sixth/seventh sampled-negative seed.

### DEPRIORITIZE — more generic recommender baselines

The paper already has tuned sequential baselines, identity-aware Dual-ID, memory ablations and DS adaptive-computation collision defense. Another conventional backbone is lower value than full-active ranking or external validation.

### DEPRIORITIZE — replacing HGB as the universal primary gate

Ridge is a strong deployment variant but changing the primary gate would require redoing the full GTS/robustness chain. Keep HGB as the frozen scientific primary and use Ridge/tiny-MLP for systems trade-off analysis.

---

## 5. Priority order in one table

| Priority | Task | Scientific purpose | New training? | Must finish before submission? |
|---|---|---|---|---|
| **P0** | Full-active live-room ranking | close sampled-candidate dependence | no major retraining expected | **Yes** |
| **P0** | Utility decile/calibration analysis | directly validate conditional utility construct | No | **Yes** |
| **P0** | Dual-ID state/confidence ablation | prove gate uses more than state/history | light | **Yes** |
| **P0** | DS projected bootstrap 5k | statistical consistency | No | **Yes** |
| **P1** | LiveRec Twitch 100k external validation | cross-platform generalization | Yes | Strongly preferred |
| **P1/P2** | KuaiLive-M3 validation | second in-domain/public confirmation | Yes | Optional before first submission |
| **P2** | DCGLive | live-room SOTA defense | likely yes / GPU | Optional |
| **P2** | richer uncertainty | mechanism refinement | light/moderate | No |
| **P2** | secondary behaviors | breadth | varies | No |

---

## 6. Recommended execution sequence

1. **Full-active room ranking** first because it is the only remaining experiment that could materially overturn the main room-level effectiveness interpretation.
2. In parallel, compute **conditional-utility decile/calibration** from frozen outputs.
3. Run **Dual-ID state/confidence ablation**.
4. Recompute DS projected matched-budget CIs with **5,000 bootstraps**.
5. Freeze manuscript main tables/figures.
6. Start **LiveRec Twitch 100k** untouched external confirmation.
7. Draft full manuscript while external run executes.
8. Only then decide whether KuaiLive-M3 / DCGLive are worth the delay.

---

## 7. Revised decision logic

### If P0 full-active ranking passes

Proceed with the strong central thesis:

> memory is a globally inferior but conditionally complementary specialist whose utility varies by state and temporal regime.

### If P0 full-active ranking weakens but remains positive

Keep the mechanism claim, narrow the absolute effectiveness claim, and emphasize candidate-regime sensitivity.

### If P0 full-active ranking becomes null/negative

Do not tune to rescue it. Reframe the paper around conditional utility under sampled active-candidate retrieval settings and treat full-active ranking as a limitation / boundary condition.

### If P1 Twitch passes

Upgrade the conclusion from “KuaiLive evidence” to a broader cross-platform principle.

### If P1 Twitch fails

Do not retune on test. Narrow generalization claims and treat the result as evidence that specialist utility depends on platform/data regime — which is itself consistent with the paper’s regime-dependent thesis.

---

## 8. Updated P0/P1/P2 verdict

The **old** P0/P1/P2 plan was reasonable at the time and produced exactly the high-value evidence it was designed to obtain. It should not be mechanically continued because two of its three kill gates are now closed.

The **new** priorities should be:

- **P0 = full-active/internal-validity + direct utility-mechanism closure**;
- **P1 = one untouched external public dataset (prefer Twitch LiveRec 100k)**;
- **P2 = second external dataset / DCGLive / richer uncertainty / secondary outcomes**.

This ordering minimizes the risk of spending large compute on low-information experiments while leaving a reviewer-visible internal-validity gap unresolved.
