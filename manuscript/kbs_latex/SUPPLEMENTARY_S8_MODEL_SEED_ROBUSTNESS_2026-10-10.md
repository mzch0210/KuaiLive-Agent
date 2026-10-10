# S8. KuaiLive training-initialization sensitivity and evidence-state decomposition

### S8.1 Separate model-seed uncertainty from sampled-negative-draw uncertainty

S8 evaluates **three independent fitted KuaiLive Dual-ID checkpoint pairs**, with fixed 10,222 TEST events, original sampled-575 candidate sets, matched full-active sets, fusion coefficient **α_room=0.125**, eligibility/history and Memory scorer. This is **P1, three model training realizations**, not P2's **three independent negative-list RNG streams applied to one original model**. Both are retrospective analyses on the same previously examined KuaiLive TEST users and neither supplies new independent datasets or a new frozen Twitch policy evaluation.

For each checkpoint pair, event-level raw Room/Streamer scores over full-active candidates are reused by exact subset extraction for sampled candidates. The two-order allocation of ranked membership versus z-score reference is computed on the same users, with 3,000 paired user bootstrap resamples **conditional on each trained checkpoint**.

### S8.2 Complete across-training-seed outcomes

| Room/Streamer training seed | Sampled 575 Memory−Base (SS) | Full-active Memory−Base (FF) | FF−SS | 95% within-seed user-paired CI | Ranked-membership allocation | Score-reference allocation |
|---|---:|---:|---:|---|---:|---:|
| 20260918 | −0.04120411 | +0.04630669 | **+0.08751080** | [+0.08209796,+0.09325975] | +0.08826963 | −0.00075883 |
| 20260919 | −0.05157020 | +0.03206113 | **+0.08363134** | [+0.07804704,+0.08938187] | +0.08438602 | −0.00075469 |
| 20260920 | −0.04903770 | +0.03504633 | **+0.08408403** | [+0.07853540,+0.08945325] | +0.08424480 | −0.00016077 |

**All three fitted pairs exhibit sampled-negative/full-positive relative-utility sign reversal.** Across the *three checkpoint pairs* the unweighted mean FF−SS is **+0.08507539** and the sample SD is **0.00212124**; observed range **[+0.08363134,+0.08751080]**. This three-seed SD is a *descriptive training-initialization statistic*, **not** a user-bootstrap uncertainty interval or population-level confidence estimate. In particular, a small seed SD should not be read as independent cohort replication.

The 20260920 score-reference allocation has within-user 95% CI **[−0.00052317,+0.00017555]**, spanning zero. The numerical sign of a small allocation in one condition must not be advertised as significant for every seed. The membership and normalization allocations always sum *algebraically* to FF−SS, but they do not identify counterfactual interventions that vary candidate count alone.

### S8.3 State-wise contribution to the regime shift

The observed-target retrospective state membership is **identical** for sampled and full candidate evaluations: **4,589 represented**, **206 recoverable-but-unrepresented**, **5,427 unavailable** out of 10,222 users. These groups cannot be used as a deployment selector. The table reports each group's **across-training-seed mean FF−SS**, along with its prevalence-weighted contribution to the overall mean difference.

| Retrospective target state | Users | Across-seed mean paired shift | Weighted contribution to aggregate shift |
|---|---:|---:|---:|
| Represented | 4,589 | **+0.086179** | **+0.038689** |
| Recoverable-but-unrepresented | 206 | **−0.109972** | **−0.002216** |
| Unavailable | 5,427 | **+0.091546** | **+0.048603** |
| **All users** | **10,222** | **+0.085075** | **+0.085075** |

The approximately 2% recoverable group contributes **negatively** to the aggregate sampled/full shift; thus the reversal is **not** explained by more recoverable history or larger regime gains in that group. It is driven largely by the represented and unavailable groups in this paired scoring protocol. This is a decomposition of matched ranking utility, **not causal mediation**.

### S8.4 Original checkpoint fingerprint table

| Training seed | Room checkpoint SHA256 | Streamer checkpoint SHA256 |
|---|---|---|
| 20260918 | \`b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7\` | \`82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945\` |
| 20260919 | \`395d1b1c881d20cbda5d24c36c30685fd1524a0ec98586c8c71ad7c245505b2a\` | \`9f1b11cf27e0c802f71bb8b1bef646bb392b28d560e3aabda03f36fe01e2b637\` |
| 20260920 | \`84c4ef5e45592fc480096dfe4e501046ede37c1f936484ed83f3bd56e1f49191\` | \`7043b275b56a75fd5d7aeadfd7e69d5447128ce9f55f3bd6a0f275a24dd2d144\` |

### S8.5 Evidence status and incomplete generalization

The exact P0 model pair is byte-matched to the earlier same-checkpoint archive; the other two pairs were newly trained in original GPU job [37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645), with compact result artifact [11538678848](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538678848) and checkpoint artifact [11538867565](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538867565). The complete original scientific ledger is [KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md](../../KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md).

P2 candidate-list sensitivity is **separately tabulated in S5**, using one frozen 20260918 checkpoint and 128/256/575 candidates at three RNG streams per size. **Neither the 3 P1 trained-model seeds nor the 9 P2 candidate conditions count as additional independent dataset replications.** The original native KuaiLive policy, cross-protocol strict transfer and external dataset generalization cannot be inferred from these matched P0/P1/P2 metrics.