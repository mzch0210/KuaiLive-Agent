# N14 P5 — Journal Supplement versus Research Archive Split

**Date:** 2026-10-27  
**Branch:** `kbs-n14-single-question-scope-reset-20261023`; Draft PR #8.  
**Accepted P4 baseline:** [GitHub Actions #40470280561](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40470280561), both main and original complete-supplement jobs successful on commit `a6df39c379975c9d146727350200209550cb3518`.

## Actual changes

1. The complete original `SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md` **remains byte-for-byte unchanged** at git blob `778fa2cf8e584ffea83e2b56ccba4f6278455172`, retaining all original 47-page science content and S10.19 provenance.
2. Created `SUPPLEMENTARY_INFORMATION_N14_FOCUSED_2026-10-27.md` as the **new N14 journal supplement**. It has six focused sections: task/feature information, complete policy/evaluation design, exact full-candidate ranking & weighted calls, shared DEV allocation, original third Holm member / incomplete H2 prespecified check, and adverse baselines / full research-archive pointers. It copies the previously frozen S10.9 policy table and S10.14 DEV table verbatim. The study's primary full-NDCG values and CI sources are referenced without re-estimating.
3. Explicitly retained the **three-member prereveal Holm family**, the nested 4,096-target authentic-vs-null comparison's +0.031145 and its **NOT VERIFIED same-cohort TRAIN-only Popularity** pre-reveal acceptance check. The study is not promoted back into a separate paper-level research question.
4. Retained primary 30,000 same-period targets, four user-disjoint DEV folds / 120-iteration final refit, original uncorrected target-retained sampled comparator, unequal raw and weighted invocation rates, Always Memory ranking advantage and adverse original pointwise gate timings.
5. Kept all source/Methods/Results archives and original C7 table-cell fixtures untouched. The N14 placement-independent science validator still checks **11** original table sources, **7** full Results archive blocks and the **49** migrated S10 cells in the original archived Supplement. New focused-supplement presence checks were added on top, not substituted for those source checks.
6. A **separate N14 focused-TeX postprocessor** was added: the old S1–S10 postprocessor demands 14 hashes, at least 23 historical tables and at least 3 landscape tables, which cannot be satisfied by an intentionally narrowed six-section journal Supplement. The new postprocessor requires exactly two copied original policy/DEV tables and permits cryptographic-hash line breaks; this change does not alter the full historical audit or bypass the original frozen table-cell checks.

## Submission / science integrity status

- Source facts (original unreleased derivative files, codes/checkpoint fingerprints) are not claimed to be public permanent deposits.
- The focused PDF is supplementary **to this one-question manuscript**; the full old results remain findable and auditable, not surreptitiously deleted.
- Retained source science results do not become a second 'new' paper by virtue of archiving them. Any future separate paper must delineate overlapping outcomes, protocol/novelty increments and appropriate disclosure.
- KBS's exact final supplementary-upload, data-availability, and anonymization requirements; author/AI/CRediT/rights declarations; external originality gap; and final journal GO/HOLD decisions are unresolved author-owned gates.
- New same-source N14 dual-PDF validation: [Actions #40470794191](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40470794191), pending when this log was created. **Do not report CI acceptance until both jobs finish successfully.**

## P5 acceptance checklist

- [x] Focused supplement source drafted, main paper and full project science archive preserved.
- [x] H1 weighted/raw policy contrasts and identical DEV trace included.
- [x] Original third H2 Holm member and NOT VERIFIED prereveal subgate disclosed.
- [x] 11 original table blocks and 49 source-cell frozen audit retained.
- [ ] Same-source PDF success and visual/content check on focused journal Supplement.
- [ ] P6/P7 independent source/claim cohesion and editorial acceptance gate.
