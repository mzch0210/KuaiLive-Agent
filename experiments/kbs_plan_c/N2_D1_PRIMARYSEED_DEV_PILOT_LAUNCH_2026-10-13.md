# N2-D1 parallel DEV pilot — launch and scientific boundary

**Date:** 2026-10-13. **Mode:** two Base families × primary train seed 20261012, already-fitted and byte-verified corrected DEV event cache. **No extra Base training and no original G5 TEST access.**

Entry point: \`analysis/kbs_plan_c/n2_d1_nested_dev_pilot.py\`. Synthetic guards: \`test_n2_d1_nested_dev_pilot.py\`. Workflow: \`.github/workflows/kbs-n2-d1-dev-pilot.yml\`.

This pilot differs intentionally from an invalid pooled-DEV threshold re-use: five outer user-disjoint heldout folds, four inner user-disjoint folds on each outer training subset. Each inner fold fits the 12-feature HGB estimators for direct target \`Y_M-Y_B\` and for two-stage \`Y_M\`, \`Y_B\`. Frozen thresholds are fitted only to inner OOF predictions + their training DEV event utilities under original \`score>=threshold\` and <=30% calls. Fresh regressors are refitted to outer training users, then pointwise selection and NDCG computed on the outer held-out users. All 50,049 DEV events appear once as outer validation. The two policies estimate the same conditional value in population because conditional expectation is linear.

**Hard protections:** Original source \`summary.json\` and \`dev_full_active_pairs.csv\` must match byte SHA, corrected Memory version, DEV-only, pre-outcome 12 features, exactly 50,049 events, no shared user between inner/outer train and validation. Self-host data and fitted models never upload; aggregate metrics only. Reruns refuse overwriting existing private output. No new confirmatory TEST family and no published NeurIPS 2022/DS-Frame complete algorithm implementation claim.

The historical G5 TEST is already revealed; new DEV estimates can only be called post-G5 exploratory even if nested. The manuscript §6 is independently revised at N3 from existing accepted observations; add no new D1 result to manuscript until a real run has been verified and evidence tier is disclosed.

**Execution status must be checked from GitHub Actions, not presumed from a commit.** Self-host may still be offline or job may fail data checks; status is pending until verified.
