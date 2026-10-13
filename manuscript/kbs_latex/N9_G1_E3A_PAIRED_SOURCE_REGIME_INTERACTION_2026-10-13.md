# N9–G1 / E3a | Paired Full-versus-Long relationship source × candidate-regime interaction

**Result: PASS on exact pre-existing B2 private DEV source, successful [Actions #38388691201](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38388691201).** Post-G5 exploratory analysis on **50,049 author events, 12,628 users**, no G5 TEST access or model retraining. Exact B2 source SHA reverified; four raw source means matched original report to 3e-6.

## Distinct scientific estimand
For each paired event, compute $d_{F,i}=u_F(M_{Full},i)-u_F(M_{Long},i)$ and $d_{S,i}=u_S(M_{Full},i)-u_S(M_{Long},i)$. The source×candidate interaction $I_i=d_{F,i}-d_{S,i}$ is **fixed-source ranking utility**, not B2's previously published *selector-regret interaction*.

| Paired event-level effect | Mean NDCG@10 | 95% user-cluster interval |
|---|---:|---|
| Full−Long under full-active F | **0.010278** | [0.007906, 0.012668] |
| Full−Long under target-retained sampled S | **-0.105104** | [-0.108326, -0.101683] |
| Source × regime (F gap − S gap) | **0.115382** | [0.111724, 0.119065] |

Intervals are 2,000 paired **user-cluster** percentile bootstrap replicates (seed 20261013). The observed interaction is positive with an interval above zero, supporting source-dependence of candidate-regime valuation **on this shared DEV cohort**, not new prospective replication, isolated candidate-set-size causality or correct viewer–creator identity-specific causal effects.

## Additional decision-time conditional evidence

Quartiles are defined using the observed DEV distribution of **pre-outcome** features, without conditioning on target-derived evidence states; tied values can collapse quartile boundaries.

| Decision-time descriptor quartiles | Q1 interaction | Q2 | Q3 | Q4 |
|---|---:|---:|---:|---:|
| x_candidate_log_count | 0.116313 | 0.125565 | 0.110448 | 0.109205 |
| x_hist_distinct | 0.048267 | 0.106528 | 0.130050 | 0.176801 |
| x_hist_event_count | 0.077324 | 0.109576 | 0.129672 | 0.144988 |
| x_hist_repeat_max | 0.107888 | 0.122066 | 0.124978 | 0.106775 |
| x_sasrec_base_std | 0.077518 | 0.114434 | 0.139062 | 0.130517 |


Historical distinctness and history event count show appreciable conditional differences in the interaction, which motivates a more rigorous source-identity-controlled design, but does not isolate an intervention. The **same users can appear across descriptor strata**, and intervals for strata should not be treated as independent replications or a confirmatory multiplicity family.

## Important sign and zero-mass diagnostic

- Strictly opposite, **nonzero** sign of Full-minus-Long source quality between F and S: **66 events** (0.132%).
- Events with at least one source gap exactly zero: **46462** (92.83%).
- Three-way sign-category change **including transitions into/out of zero**: **27800** (55.55%).
- Opposite nonzero directions: sampled negative→full positive 41; sampled positive→full negative 25.

These distinctions are crucial: the large **aggregate** source ordering reversal is not evidence that many individual event-level source utility differences strictly swap positive and negative signs. Event NDCG@10 has substantial zero mass because relevant items often lie beyond the top ten.

## What this resolves and what it does not

E3a strengthens **R3** by putting user-paired uncertainty on the real source×candidate interaction and exposing its dependence on predecision history and candidate score structure. It does **not** establish causal identity specificity or explain how much is due purely to generic sampled metrics. A strengthened non-floor, degree/time-preserving historical control (conditional E3b) remains valuable only if feasible without leakage or artificial floor collapse.

This is a new **exploratory DEV** analysis prompted after the B1/B2 outcomes were known. It does not modify G5 Holm tests and should not be described as an independently frozen TEST. Recommended article placement after G4: compact paired interaction estimate in §6.4; detailed quartile/sign diagnostics in S10.

Reproducibility: `analysis/kbs_plan_c/n9_g1_e3a_source_candidate_interaction_dev.py`; workflow `.github/workflows/kbs-n9-g1-e3a-paired-source-interaction-dev.yml`; [public safe source result](../../experiments/kbs_plan_c/N9_G1_E3A_PAIRED_SOURCE_CANDIDATE_PUBLIC_AGGREGATE_2026-10-13.json). Private event rows remain on the authorized host.
