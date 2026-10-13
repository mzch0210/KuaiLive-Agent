# N9–G3 | History-identity placebo source readiness and pilot gate

**Date 2026-10-13 | METADATA-ONLY ELIGIBILITY PASS; E3b PILOT NOT YET EXECUTED.** [Read-only GitHub Actions #38389532148](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38389532148) accessed parquet metadata and filesystem existence only; did not read private event/outcome rows, open G5 TEST, retrain any model or export personal records.

## Available causal/roster input types
| Frozen self-host asset | Verified existence and schema | Safe metadata count |
| --- | --- | ---: |
| G1 causal history `causal_stream_sealed.parquet` | source_event_id, user_id, author_id, observed_at, split, prior_events, live_id | **35,432,406 history rows** |
| G1 eligible live room intervals `available_room_intervals.parquet` | author_id, live_id, open_ts, close_ts | **6,537,125 interval rows** |
| G1 `dev_cohort.parquet` | event_id/timestamp/user and author descriptors | **50,049 DEV rows** |
| G2 author index and DEV event snapshots | Both files exist | Content not inspected |

These **metadata-only** checks establish that temporal ordering and author eligibility can be *investigated*; they **do not** prove that a degree/time-marginal-preserving rewiring is feasible, valid, fair or non-floor.

## Why E3b is still scientifically useful
E3a verified the Full-versus-Long interaction on paired 50,049 DEV author events: +0.115382 (user 95% CI [0.111724,0.119065]). E1 verified that S/F supervision changes **21.32% SASRec / 23.01% GRU4Rec** of chosen events and reallocates Memory calls toward higher realized marginal-value events. These strengthen the integrated empirical result but cannot tell whether **correct historical viewer–creator identity** has a unique effect beyond general user activity, author popularity, candidate competition or sampled top-10 metric properties.

## Required E3b pilot and stop criteria before a full experiment
1. **Rights gate:** researchers confirm private dataset/release licenses, local authorized processing and no release of identifiers or reconstructed edges.
2. **Design gate:** freeze one exact random seed and pretarget time bins; permit swap of *past* user–creator edges only within causal windows and eligible historical authors. Preserve per-user prior event count, time distribution, per-author degree in relevant bins, candidate-eligibility definitions, and verify whether last-ten and long-term score formation can be recomputed without future information.
3. **Source parity gate:** reproduce original corrected Full Memory score and B2 Long-only scores on a time-stratified DEV pilot before applying placebo. No altered Base weights.
4. **Control strength gate:** on an initial 128–256-event **preselected** DEV subset, measure placebo score range, history-support coverage, event-level full/sampled rank utility and expert-call eligibility. A near-zero-call/floor control fails as an identity-specific mechanism test, not as evidence for superiority of the real memory.
5. **Compute gate:** reuse one causal stream pass and single event-time roster sweep, avoid re-scoring 50,049 events unless meaningful control passes. Record overall CPU processing, any GPU work and wall time.
6. **Interpretation:** if the intervention modifies margins, breaks temporal chronology, leaks target, or creates artificially powerless experts, stop and retain a **source-sensitivity** (not causal relation-identity) statement in KBS manuscript.

**Gate verdict:** input-file metadata readiness PASS; **experimental design validation, permitted data processing and non-floor control pilot PENDING**. No G4 STRONG judgement and no main/S10 changes are authorized by this metadata check.
