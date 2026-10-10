# S6. Base context-length, target recurrence, and memory-history definition sensitivity

### S6.1 Research purpose and invariant evaluation population

These are **Twitch DEV-only diagnostics**, comprising **46,878** one-target-per-user events. They examine whether fixed Memory's relative value changes alongside independently trained Base input contexts and retrospectively measured target-creator recurrence. No results in this section were used to change the original frozen Twitch TEST Utility threshold. Subgroups are defined using the **observed target creator** and therefore cannot be treated as pre-outcome selector rules.

The context comparison uses maximum Base lengths **L=8,16,32**; **each Base has separately trained parameters**. For a scientifically interpretable same-specialist comparison, the canonical frozen P1.2 L16 Memory rank and NDCG@10 are reused identically at all three Base lengths. The first secondary aggregation failed because an evaluator introduced an extra split-end history filter and thereby changed Memory for some users; that run is **excluded**. The repaired run restored canonical Memory exactly, and all event identities and Memory ranks then passed deterministic invariant checks.

### S6.2 Overall ranking scores by independently trained Base context

| Base maximum context L | Events | Base NDCG@10 | Frozen Memory NDCG@10 | Memory−Base | 95% paired-user CI |
|---|---:|---:|---:|---:|---|
| 8 | 46,878 | 0.526194 | 0.521696 | **−0.004498** | [−0.007557, −0.001274] |
| 16 (canonical) | 46,878 | 0.571853 | 0.521696 | **−0.050157** | [−0.053065, −0.047313] |
| 32 | 46,878 | 0.596627 | 0.521696 | **−0.074931** | [−0.077665, −0.072274] |

**Interpretation:** with this same frozen Memory scorer, the overall relative gain becomes more negative as the separately trained Base becomes stronger on these DEV events. **It is not a controlled estimate of history-window length holding model weights fixed**; training realizations change with L.

### S6.3 Retrospective target-history state comparisons

| Base L | Target-relative state | Events | Memory−Base NDCG@10 | Pointwise 95% paired CI |
|---|---|---:|---:|---|
| 8 | Represented | 19,486 | +0.002711 | [−0.000388,+0.005816] |
| 8 | Recoverable | 10,934 | +0.260425 | [+0.252876,+0.267791] |
| 8 | Unavailable | 16,458 | −0.189036 | [−0.193834,−0.184418] |
| 16 | Represented | 24,541 | −0.019951 | [−0.022857,−0.016806] |
| 16 | Recoverable | 5,879 | +0.230969 | [+0.221915,+0.240344] |
| 16 | Unavailable | 16,458 | −0.195620 | [−0.200376,−0.191109] |
| 32 | Represented | 28,158 | −0.023089 | [−0.026163,−0.019946] |
| 32 | Recoverable | 2,262 | +0.188605 | [+0.175262,+0.202654] |
| 32 | Unavailable | 16,458 | −0.199848 | [−0.204481,−0.195050] |

Each row uses **the target's presence in that Base context**. Group denominators change with L, while the unavailable-event set remains the same. The original frozen L16 Memory has identical event-level outcomes in each context panel.

### S6.4 Matched-user state transitions

For the exact same users whose previously recoverable target becomes represented as Base context length increases:

| Base L transition | Recoverable → represented users | Change in Memory−Base | 95% paired CI | Change in frozen Memory | Change in Base |
|---|---:|---:|---|---:|---:|
| 8 → 16 | 5,055 | **−0.447482** | [−0.457672,−0.437300] | 0 | +0.447482 |
| 16 → 32 | 3,617 | **−0.432288** | [−0.443811,−0.420543] | 0 | +0.432288 |

On these matched users, the Memory-minus-Base difference necessarily equals the **negative change in Base NDCG** because canonical Memory is unchanged. The result is compatible with increasing Base adequacy for an older relationship but **cannot isolate causality from visibility alone**: independently trained Base parameters, context and candidate score behavior differ.

### S6.5 Target-creator recurrence distance under fixed L=16

The diagnostic distance is the number of eligible prior user interactions back to the most recent occurrence of the **observed target creator**, not wall-clock time or prediction-time known target features.

| Last prior occurrence (interactions ago) | Events | Memory−Base NDCG@10 | 95% pointwise CI |
|---|---:|---:|---|
| 1–4 | 13,963 | +0.04606 | [+0.04276,+0.04938] |
| 5–8 | 5,556 | −0.06511 | [−0.07180,−0.05852] |
| 9–16 | 5,027 | −0.15268 | [−0.16096,−0.14455] |
| 17–32 | 3,621 | +0.25668 | [+0.24486,+0.26827] |
| 33–64 | 1,716 | +0.20707 | [+0.18985,+0.22384] |
| ≥65 | 537 | +0.12965 | [+0.10092,+0.15807] |
| No eligible prior target creator | 16,458 | −0.19562 | [−0.20025,−0.19099] |

The pattern is **non-monotonic**, with positive short-repeat and longer-than-base-visible pockets separated by a negative intermediate band. These are descriptive, non-multiplicity-adjusted observations with confounding by user activeness, target identity and candidate difficulty. A target-specific distance is unavailable to the pre-outcome selector.

### S6.6 Repaired-source provenance and replication restrictions

- Canonical frozen L16 DEV/Memory event source: [DEV run 35698158121](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35698158121), original artifact 10680854557; L16 immutable OOF SHA256 \`9757064252c097934fa31f10a68e11bb43853ca1132aaa49da2b9794f60d3816\`.
- Separate L8/L32 original Base training: [GPU intervention run 35830028173](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35830028173), artifact 10752233546.
- **Corrected/authoritative aggregation:** [run 35877647543](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35877647543), [artifact 10757614400](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35877647543/artifacts/10757614400). Its archived \`context_length_overall.csv\`, \`context_length_state_summary.csv\` and \`context_length_transitions.csv\` reproduce the values above.
- Initial evaluator mismatch: **50/46,878** user history lengths drifted by 51 eligible records; **15** Memory ranks and **14** Memory NDCG values were affected. The repaired aggregator **reuses canonical Memory**, rather than ignoring a mismatch or weakening checks. See [repair explanation](../../KBS_CONTEXT_LENGTH_INTERVENTION_REPAIR_2026-09-23_RUN35877647543.md).
- Recency: [DEV run 35725938757](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35725938757), [original summary](../../KBS_ROBUSTNESS_RESULTS_2026-09-22.md). The DEV recency/conditional CIs are not new held-out confirmation.

No Base context or recency result from this section changes the one-shot Twitch TEST selector, and no wording should imply unseen online session intervals from ten-minute crawl data.