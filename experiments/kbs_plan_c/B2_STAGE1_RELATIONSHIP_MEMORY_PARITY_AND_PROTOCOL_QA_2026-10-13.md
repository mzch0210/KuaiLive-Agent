# B2 Stage 1 — DEV-only relationship evidence ablation pilot and QA

**13 October 2026 | Status:** B2-1 **PASS**, B2-2 full and B2-3 nested comparisons staged. This report records actual results of the 128-event technical pilot. It does **not** establish a statistically significant knowledge-specific mechanism or independent TEST validation.

## Execution and provenance

- [Successful B2-1 GitHub Actions #38367455403](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38367455403), self-host `kuailive-3090-01`; code source SHA `58a83227456f79928da37cb891c330d2dd2e70a2`, workflow trigger commit `ff6f226963323bb5a3a4d9db52a07e1341906582`.
- Aggregate artifact `kbs-b2-128-dev-memory-source-aggregate`, ID `11797710826`, was downloaded and parsed; original aggregate-only `summary.json` exists. Only aggregate fields, no private events/users/candidate identities, uploaded.
- All five arm definitions and scientific stop criteria are recorded in the **pre-execution** [B2 protocol](B2_RELATIONSHIP_KNOWLEDGE_SPECIFICITY_PROTOCOL_2026-10-13.md).
- All 128 sampled DEV points selected before scoring at fixed time-spread indices; original frozen Base models unchanged; B1 full-active and 575-target-retained sampled Base metrics are reused.

## Exact corrected Memory parity

| Check | Result |
|---|---|
| Original Full Memory F vs corrected DEV score | **0 discrepancies** |
| Original Full Memory S vs B1 sampled score | **0 discrepancies** |
| DEV sample size | 128 |
| Original causal history events scanned | 30,307,513 |
| Sampled candidate count | exactly 575 |
| New model training / G5 TEST access / private IDs exported | **No / No / No** |

The scorer correctly preserves the fact that TRAIN-unknown prior author interactions consume short-recency slots, and long-term normalization uses **all** prior authors. A mismatching full-Memory source would have halted the experiment, so these exact checks are essential before interpreting ablations.

## Observed exploratory score means on this small pilot

| Fixed auxiliary expert | Full-active NDCG@10 | 575-candidate sampled NDCG@10 |
|---|---:|---:|
| Full Short+Long+Popularity | 0.362053 | 0.718584 |
| Long-only | **0.371307** | **0.783582** |
| Short-only | 0.254015 | 0.415561 |
| Popularity-only | 0.018408 | 0.146985 |
| Relationship-shifted null | 0.010210 | 0.139957 |

**Do not call this a final scientific superiority ranking**: these are 128 hand-picked-by-timeline events, no paired user-cluster CI, no gate routing comparison, and no independent fresh TEST. Long-only exceeding Full Memory in this small group is a potentially useful hypothesis about fixed `0.10/0.45/0.45` weights, not evidence of a universally better knowledge model. The null cyclic-shift control preserves the event-level multiset of historical support scores but does not preserve globally realistic user–author history, so it is an **evidence placement placebo**, not a new ranking expert or exact user-history permutation.

## Performance

One causal-history pass took **35.55 s**, one candidate-roster stream plus five component/scoring variants took **10.74 s**, and total **46.8 s**. No GPU-based Base re-scoring was necessary; rerunning Base merely to inflate GPU utilization would decrease execution efficiency. All relevant inputs and private rows remained on self-host.

## Stage handoff and acceptance gate

B2-1 source parity **PASS**. B2-2 full DEV source calculation has been launched via [GitHub Actions #38367721633](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38367721633); **its success is not presumed by this report**. Nested B2-3 is deliberately gated on an explicit later full-source certificate: 50,049 DEV rows, exact F and S full-memory parity, and no TEST access. If B2-2 fails, B2-3 will not execute. All B2 results are exploratory after G5/B1.

**Editorial/scientific guard:** Even an accurate Long-only result cannot by itself establish that conditional value, candidate-regime sensitivity and specialist decision jointly form a new knowledge-system contribution; the decisive test is the matched held-out B2-3 source-specific selection/transfer interaction, and its evidence remains post-G5 DEV until independent confirmation.
