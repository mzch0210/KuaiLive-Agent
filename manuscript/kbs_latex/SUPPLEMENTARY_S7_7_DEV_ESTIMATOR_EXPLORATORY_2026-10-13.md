# Supplementary S7.7 — Exploratory nested-DEV estimator comparison

This independently recorded addendum complements S7.1–S7.6 and is intended for incorporation into the final combined S1–S9 submission supplement during N8. It is **post-G5 exploratory DEV evidence**, not part of the original confirmatory G5 TEST.

The Direct estimator learns the event NDCG@10 increment of Memory over the fixed Base. The Two-stage estimator separately learns Memory and Base NDCG@10, then subtracts. Both target the same conditional expectation by linearity; they are alternative implementations, not different deferral theories.

The evaluation uses 50,049 full-active M3 DEV events from 12,628 users with twelve decision-time features, the primary SASRec and GRU4Rec training seed (20261012), five outer user-disjoint validation folds and four inner group folds per outer training subset for OOF threshold calibration under a maximum 30% inner-DEV Memory-call criterion. TEST outcomes were not used for the new experiment.

**Table S7.5. Exploratory nested-DEV comparison (2,000 paired user-cluster bootstrap replications).**

| Base | Estimator | DEV NDCG@10 | Gain over Base | Memory calls | Direct−Two-stage NDCG difference (95% CI) |
|---|---|---:|---:|---:|---|
| SASRec | Direct | 0.302678 | +0.044511 | 14,980 (29.931%) | +0.001352 [+0.000422,+0.002198] |
| SASRec | Two-stage | 0.301326 | +0.043159 | 14,693 (29.357%) | — |
| GRU4Rec | Direct | 0.302989 | +0.044018 | 14,716 (29.403%) | +0.000051 [−0.000822,+0.000907] |
| GRU4Rec | Two-stage | 0.302939 | +0.043967 | 14,751 (29.473%) | — |

Direct invokes Memory 287 more times on SASRec, so its gain is not an equal-call-quality superiority result. The GRU4Rec interval crosses zero. Always Memory DEV NDCG@10 was 0.343509. Neither the two-regressor gate overhead nor an actual external service cost was measured. The analysis cannot establish generic superiority to published Learning-to-Defer or DS-Frame algorithms.

Code: `analysis/kbs_plan_c/n2_d1_nested_dev_pilot.py`; successful [GitHub Actions #38339908528](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38339908528); verified aggregate summary SHA256 `b944e791e4797f97892bbbddb6f6729014a00cc3bc11e3cb6f1229b207897706`. This is not a claim of durable public hosting of event-level data.
