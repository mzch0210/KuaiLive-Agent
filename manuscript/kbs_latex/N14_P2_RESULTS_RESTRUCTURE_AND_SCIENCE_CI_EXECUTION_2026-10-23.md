# N14 P2 — Results scope reset and source-preserving CI execution log

**Date:** 2026-10-23
**Branch:** `kbs-n14-single-question-scope-reset-20261023`; Draft PR #8 based on N13.
**P0/P1 frozen sources:** N13 `main.tex` blob `1467c5ae4fbda0135e822b00be0f7741c5129498`; Supplement blob `778fa2cf8e584ffea83e2b56ccba4f6278455172`.

## Executed in this P2 source-edit batch

1. Created `N14_N13_COMPLETE_RESULTS_RESEARCH_ARCHIVE_2026-10-23.tex` before changing the manuscript. It preserves the complete N13 Results section, seven intact original table blocks, one diagnostic figure, all previously reported Results prose and their scientific caveats. It is a source archive, not included for typesetting in the narrowed N14 paper. N13 PR #7 remains unchanged.
2. Replaced N14 `main.tex`'s six RQ Results subsections and seven main tables with four focused subsections and the two original unaltered main table bodies:
   - Candidate-regime sensitivity on 10,222 previously observed **room** events (diagnostic, not main H1 cohort).
   - 30,000 additional same-period M3 **author** events, F/S separately frozen complete policies, 20-cell weighted full-F NDCG, original Holm family, raw and population-weighted invocation fractions, uncorrected sampled-label comparator.
   - 50,049 DEV request switches as descriptive allocation evidence, not mediator or new TEST.
   - Adverse Always-Memory accuracy and legacy pointwise selector timing plus unanswered corrected-S/online-cost conditions.
3. Added `analysis/kbs_plan_c/n14_p2_science_archive_contract.py`, a placement-independent scientific audit. It retains the original 11-table inventory, requires two literal frozen source table blocks in N14 main and all seven unchanged in the N13 archive, validates all **49 migrated S10.19 numeric cells by original row/source identity**, and checks the original three-test Holm family, H2 disclosure, DEV request denominators, mismatched actual calls and adverse cost/quality evidence. It does not load private TEST rows or re-estimate anything.
4. Added `.github/workflows/kbs-n14-p2-focused-science-dual-pdf.yml`, isolated to the N14 branch. The main job runs the independent N14 science contract then compiles/checks the N14 paper PDF. The second job continues the same complete S1–S10.19 supplement PDF construction and verification. Original N13 science workflows/fixtures were not altered or disabled.
5. Initial Actions [#39895943665](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39895943665) caught a **new P2 verifier regex escape mistake** before PDF build; it was corrected by commit `6b55afa7b7cba867d3ccf6385a923d332d274d2b`. This was an implementation correction, not a change in scientific assertions.
6. Follow-up run [#39896006515](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39896006515) was pending when this record was prepared. Do **not** claim final P2 CI acceptance before confirming its jobs and source SHA.

## Scope warning and handoff

The **Results-only P2 pass does not complete P3/P4**. Introduction, concept figure, broader Methods/Experimental Design, Discussion, Conclusion and the old journal Supplement may still discuss Twitch and RQ3. Those sections must be aligned in later source edits; the temporary mismatch cannot be treated as a submission-ready paper. P5 must create a focused journal Supplement while retaining the complete archived original H2 three-test Holm family, historical-source prereveal NOT VERIFIED status and all prior source tables.

No new sample, TEST reveal, corrected-S policy, model training, threshold tuning or new cost estimates were introduced.
