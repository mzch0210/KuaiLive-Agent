# N9-A2 | Direct relative-value and strong objective controls on matched M3 DEV

**Date: 2026-10-13. Executed DEV-only decision-target component: PASS. Direct score/rank fusion: HOLD (raw per-candidate scores not attested).** [Successful self-hosted run #38383262381](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38383262381) validated the inlined source against the public Git blob before fitting, checked the exact B1 source SHA and copied no private event rows. G5 TEST remains unchanged.

## 1. Why these controls address a decision-support rather than algorithm-novelty claim

The scientific question is whether **incumbent-relative ranking-value prediction** is a useful decision signal compared with predicting Base error, Memory standalone quality, or predicting both utilities separately. All four scored policy objectives use the same Base and specialist, the same twelve pre-outcome features and **5 outer × 4 inner user-disjoint DEV splits**, and original HGB model hyperparameters; threshold is selected from inner OOF gain on F full-active event NDCG and applied pointwise to outer users. Natural observed Memory-call rates are reported, without retroactive equal-count adjustment. Predeclared inner max rates: **10%, 30%, 50%**.

Arms: Direct Δ predicts Memory−Base NDCG; Two-stage predicts Memory and Base event NDCG with **two separate HGB heads** then subtracts; Difficulty predicts negative Base NDCG; Specialist Quality predicts Memory NDCG alone. Two-stage has two fitted prediction heads rather than the single fitted head of Direct/Difficulty/Specialist. This is a matched **L2D-style realizable proxy and decision-target contrast**, not replication of all published L2D or DS-Frame methods. No full ranking-score fusion is tested here.

## 2. Source-frozen nested DEV NDCG@10

| Budget | Base | Direct Δ | Two-stage | Difficulty | Specialist quality | Direct calls | Two-stage calls |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10% | SASRec | 0.278263 | 0.277864 | 0.263151 | 0.261710 | 5001 | 4950 |
| 10% | GRU4Rec | 0.279025 | 0.278802 | 0.264451 | 0.262982 | 5006 | 4900 |
| 30% | SASRec | 0.302658 | 0.301348 | 0.282295 | 0.278220 | 15016 | 14698 |
| 30% | GRU4Rec | 0.303093 | 0.302974 | 0.283554 | 0.279202 | 14762 | 14821 |
| 50% | SASRec | 0.319654 | 0.319178 | 0.305321 | 0.303104 | 25081 | 25088 |
| 50% | GRU4Rec | 0.320478 | 0.319608 | 0.306720 | 0.302253 | 25230 | 24867 |

30% Direct Δ accurately reproduces the previously accepted B1/A1 full-aligned nested results and calls: SASRec 0.302658031270 (15,016 calls), GRU4Rec 0.303093158251 (14,762 calls). The A2 source therefore meets the previously stipulated numerical parity gate.

### Direct-minus-Two-stage paired comparisons

| Budget | Base | Direct − Two-stage | Paired user 95% CI | Calls difference |
|---:|---|---:|---|---:|
| 10% | SASRec | 0.000400 | [-0.000252, 0.001014] | 51 |
| 10% | GRU4Rec | 0.000223 | [-0.000454, 0.000892] | 106 |
| 30% | SASRec | 0.001310 | [0.000419, 0.002179] | 318 |
| 30% | GRU4Rec | 0.000119 | [-0.000767, 0.000955] | -59 |
| 50% | SASRec | 0.000477 | [-0.000537, 0.001480] | -7 |
| 50% | GRU4Rec | 0.000870 | [-0.000126, 0.001888] | 363 |

At 30% inner maximum, SASRec Direct improves NDCG by 0.001310 (user 95% CI [0.000419, 0.002179]) with **318 additional Memory invocations**; this cannot establish same-call superiority. GRU4Rec difference 0.000119 has an interval crossing zero and Direct invokes Memory 59 **fewer** times. In other budgets, Direct and Two-stage remain close and most paired intervals cross zero. Their common target is the same conditional expected increment by linearity; their finite-sample estimators differ.

### Distinct decision targets

At 30%, Direct Δ exceeds Base Difficulty by **0.020363** (SASRec; user CI [0.018404, 0.022309]) and **0.019539** (GRU4Rec; CI [0.017595, 0.021517]). It also exceeds Specialist Quality by **0.024438** and **0.023891**, respectively. These are matched users with similar but not strictly identical natural calls; the 10% and 50% panels show the same relative ordering for these four specified objectives. This provides additional exploratory support for **decision relevance of relative-knowledge utility** rather than general superiority to arbitrary routing algorithms.

## 3. Reconciliation and caveats

An earlier N2-D1 exploratory DEV study compared Direct and Two-stage under a related five-by-four-fold protocol and found a comparably modest implementation difference. The new A2 study **does not substitute for it or create a new independent cohort**: it reuses B1's exact F source, fold structure and threshold parity to align with A1. Both share the same 50,049 DEV events / 12,628 users and single primary Base seed per family. A2 user intervals are descriptive post-G5 bootstrap estimates, not part of G5's registered Holm family. A2 is not a fully compute-matched deferral-algorithm comparison; two-stage uses two regression heads. Scores and objectives are not novel algorithms.

No raw per-candidate Base/Memory vectors with exact candidate eligibility were verified in A0, so simple score fusion/rank fusion is not yet executed. The study cannot prove routing deployment cost advantage, nor does it force change to the locked **knowledge-value assessment + decision-support** scientific thesis.

## 4. Risk effect and next gate

- **R1** scientific differentiation: stronger decision-target effect with Direct and Two-stage consistency; novelty remains a **BOUNDED knowledge-valuation-to-decision contribution**, not a new deferral algorithm.
- **R2** actual policy quality: relative-value supervision is supported over the two weaker objective proxies across three DEV budgets, while A1 demonstrates nearly-universal Memory selection without a call limit. Real scarcity/cost remains unverified.
- **R3** B1/B2 matched source × candidate × downstream decision findings remain exploratory; this A2 study checks decision-target alternatives but is not a new independent mechanism confirmation.
- **A3 decision** can now evaluate an explicitly scoped decision-support claim; a complete score/rank-fusion comparison requires separate candidate score availability or justified bounded F-rescoring. Do not manufacture it from per-event NDCG.

Source: `analysis/kbs_plan_c/n9_a2_decision_target_controls_dev.py` and `.github/workflows/kbs-n9-a2-decision-target-controls-dev.yml`. Private full summary is stored on self-host as `klm3_n9_a2_target_controls_seed20261012_v1/summary.json` with only safe aggregates printed to this successful job log.
