# N15 P1 — Implementation status and restricted-source execution gate

**2026-10-27. P1 CODE/SYNTHETIC QA PASS, PRIVATE DEV SCIENTIFIC RUN NOT YET PERFORMED.** Baseline N14 immutable. Current N15 source in draft PR #9.

## Implemented

- `analysis/kbs_plan_c/n15_p1_matched_budget_dev.py`: frozen B1 DEV file metadata + SHA check, 50,049 rows/12,628 users, original 12 pretarget variables, SASRec and GRU4Rec fixed HGB capacity; 5 outer user-disjoint group folds and held-out model scores.
- Exact top-k per fold at q=0.10,0.20,0.30,0.40; deterministic SHA256 stable original DEV row-index tie ordering, independent of target identity/labels. At any q both arms receive exactly the same raw number of calls in every fold.
- For each family and quota: observed F and S full-candidate NDCG; identity check versus `mean[(pi_F-pi_S)*Delta_F]`; call partition and exploratory user-bootstrap CI at q=.30; explicit Always Base/Always Memory adverse references.
- `analysis/kbs_plan_c/test_n15_p1_matched_budget_dev.py`: five fully synthetic tests for exact calls, permutation invariance, tied scores, invalid input/empty quota, allocation-value identity and reproducible cluster uncertainty.
- `.github/workflows/kbs-n15-p1-matched-budget-source-qa.yml`: public hosted syntax/test/scope check; Actions [#40508328475](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40508328475) public-synthetic-qa **SUCCESS**.

## Scientific distinctions and caveats

1. N15 `exact_batch_topk` is an **offline fold-batch allocation** with access to all fold request scores. It is NOT a feasible causal-time online streaming serving algorithm. In original B4-A H1, policy decisions used frozen DEV-calibrated thresholds and naturally realized call rates; N15 batch matching is a **different policy comparison estimand**.
2. The two arms train on different label information (F full, S uncorrected target-retained sampled); matched calls do not eliminate this information difference or prove a pure intervention on labels.
3. User-disjoint outer-fold fitting protects evaluated DEV rows from direct in-sample label fitting, but B1/G2 source, feature/algorithm selection and N15 quota design have been chosen after earlier DEV analyses. New N15 DEV is therefore **exploratory**; no claim of independent confirmation.
4. The current script evaluates the existing Full Memory source ONLY. Full-vs-Long knowledge-interaction component remains a gated later extension; it is **not silently claimed completed**.
5. No 20-cell B4-A population weights are applied to original DEV. Calls and rankings are unweighted original DEV metrics; do NOT compare them as identical estimands to B4-A population-weighted results.
6. User bootstrap resamples observed held-out decisions at fixed fitted policies; it does not account for repeated policy refitting or the multi-stage model selection process. Label as descriptive uncertainty.
7. Stable original row-index hashed tie key depends on input CSV ordering, protected by exact SHA. The row index is neither a target label nor an online identifier.

## Decision gate for self-hosted private source run

**Met:** public code compiles, tests pass, SHA/schema/info scope enforced, no private outputs in source.

**Still required before private execution:**
- Confirm self-hosted resource authorized/available for N15 and verify access rights to original restricted cache; do not assume that presence of old self-hosted workflows is authorization to access private data.
- Confirm correct private source directory `$HOME/.cache/kuailive-agent-kbs/klm3_b1_full_dev_candidate_labels_seed20261012_v1` and unmodified B1 source SHA.
- Approve N15 aggregate-only output on an isolated immutable path, without raw rows or model weights in Actions artifacts.
- Inspect source-run diagnostics and actual group split parity. No TEST/B4-A revealed target outcome reads.
- Before conducting future independent P3, separately freeze hypothesis family, model, budget, data, legal conditions and valid new cohort. P3 currently HOLD.

**Gate status:** P1_ENGINEERING_PASS / PRIVATE_DEV_RUN_HOLD / KBS_SUBMISSION_HOLD.

This file reports **no new empirical NDCG number**, no accepted KBS-level novelty verdict, and no independent human referee.
