# Section 6.3 — candidate-regime dependence: scholarly evidence and writing audit

**Date:** 2026-10-09  
**Manuscript:** [Section 6.3, Candidate-Regime Dependence of Relative Utility](main.tex)  
**Scope:** Section 6.3 only; Sections 1–5 and reviewer-tightened 6.1–6.2 are unchanged. The [verbatim original KuaiLive section](section6_3_kuailive_migration_source.tex) is retained as a research migration archive; the new section is a concise paper-facing reorganization, not a direct pasted experiment log.

## Final experimental provenance

- [Verified KuaiLive P0/P1 result ledger](../../KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md); successful [GPU run 37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645).
- [P0 factorial result artifact 11538678848](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538678848): 10,222 paired events per seed, 2×2 cells and user-level paired 95% intervals (3,000 draws).
- [P1 trained model artifact 11538867565](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538867565): seeds 20260919 and 20260920 checkpoint pairs; seed 20260918 was verified cached from the preceding same-checkpoint diagnostic.
- [Evaluation code](../../analysis/kbs_kuailive_factorial.py) and [workflow](../../.github/workflows/kbs-kuailive-factorial-seeds.yml). The experimental protocol, algebraic allocation and bootstrap unit are defined in [manuscript Section 5](main.tex).

## Main 2×2 evidence: seed 20260918

Rows are the rank candidates; columns are the candidate population furnishing the branch-specific z-score moments. S is the same sampled-active candidate subset of F; shared users, targets, histories, raw checkpoint scores, Memory and fixed room-fusion weight 0.125. The two diagonal cells correspond to native scoring protocols; mixed cells are deliberately nonnative diagnostic combinations.

| Memory−Base NDCG@10 | Reference S | Reference F |
|---|---:|---:|
| Ranked S | **−0.04120411** | −0.04141760 |
| Ranked F | +0.04761085 | **+0.04630669** |

- P0 paired difference FF−SS: **+0.08751080**, 95% user-paired CI **[+0.08209796,+0.09325975]**.
- Two-order candidate-membership allocation: **+0.08826963**, 95% CI **[+0.08286671,+0.09397065]**.
- Two-order normalization-reference allocation: **−0.00075883**, 95% CI **[−0.00117294,−0.00035507]**.
- P0 native sampled Base **0.60709158**, Memory **0.56588746**; full-active Base **0.38571242**, Memory **0.43201911**. The fact that both absolute NDCG values decrease under a larger ranking universe must not be obscured.
- Membership + normalization = FF−SS to numerical precision; **the components are not causally identified effects** or variance shares. Candidate membership bundles cardinality, composition and challenge.

## P1 seeds: fixed dataset, independent checkpoint initializations

| Training seed | Sampled S/S contrast | Full F/F contrast | FF−SS | Membership | Normalization |
|---|---:|---:|---:|---:|---:|
| 20260918 | −0.04120411 | +0.04630669 | +0.08751080 | +0.08826963 | −0.00075883 |
| 20260919 | −0.05157020 | +0.03206113 | +0.08363134 | +0.08438602 | −0.00075469 |
| 20260920 | −0.04903770 | +0.03504633 | +0.08408403 | +0.08424480 | −0.00016077 |

Three-seed mean FF−SS **+0.08507539**, between-seed sample SD **0.00212124**; mean membership **+0.08563348**, mean normalization **−0.00055809**. All 3/3 seeds have sampled-negative and full-positive Memory−Base; these are independent training realizations of the same model and **same 10,222 evaluation users**, not three independent user samples or a reliable full seed-distribution CI. The normalization reference allocation's per-user CI at seed 20260920 includes zero; avoid claiming significance for its sign across seeds. The seed SD and per-user bootstrap CIs have different uncertainty meanings.

## Target-relative state decomposition (supporting evidence only)

- Counts fixed under paired candidate ranking: represented **4,589**; recoverable-but-unrepresented **206**; unavailable **5,427**. Each assigned using the observed target; none is a prospective routing feature.
- Across-seed mean shifts: represented **+0.086179**, recoverable **−0.109972**, unavailable **+0.091546**.
- Prevalence-weighted contributions to mean FF−SS: **+0.038689**, **−0.002216**, **+0.048603**, summing to **+0.085075** up to rounding.
- Consequently, positive full-minus-sampled shifts are **not** caused by recovering more history or increasing the benefit of the small recoverable-state group. State-level changes are descriptive and sensitive to a recoverable group of only 206 cases.

## Inferential and scientific-writing boundaries

1. **Post-hoc evidence:** The KuaiLive test population had been inspected in earlier candidate comparisons; the P0/P1 results are supporting diagnostic analyses, not a second independently frozen selector trial. Twitch's single frozen Utility-gate TEST in Section 6.2 retains its own independent evidentiary status.
2. **No causal decomposition:** The factorial is an algebraic two-path average holding raw scores fixed under defined scoring interventions, not a randomized experiment that isolates the cause of historical value change.
3. **No naive sampling claim:** The mismatch between sampled and full candidate metrics should not be advertised as a newly discovered generic fact. Earlier published analyses document that sampled ranking metrics can change relative method comparisons. The distinctive research observation is the resulting `Memory−Base` utility's dependence on the particular incumbent, candidate population and relationship source.
4. **No claim about online preference or transactions:** Unobserved candidate rooms are not verified negatives; offline NDCG may not equal user preference or actual commerce outcomes.
5. **Minimal manuscript exhibits:** Main text carries one 2×2 table and four explanatory paragraphs; per-seed results, checkpoint hashes, state tables, bootstrap provenance and run chronology remain in the evidence record and planned supplementary S5/S8.
6. **Literature version (updated 2026-10-09):** The existing internal key `krichene2020sampled` now resolves to the formally published 2022 *Communications of the ACM* journal version (65(7):75–83, DOI [10.1145/3535335](https://doi.org/10.1145/3535335)), superseding the earlier 2020 KDD metadata without adding a duplicate citation. The original Section 5 citation token remains unchanged; Section 6.3 now also cites the same finalized journal record, explicitly distinguishing known sampled-metric ranking inconsistency from this manuscript's specific Memory–Base utility diagnostic. See [reviewer audit](SECTION6_3_KBS_REVIEWER_TIGHTENING_2026-10-09.md) and [updated publication audit](RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md).

## Final first-draft build and page review

- The final staged manuscript source was committed as [`94ac9289`](https://github.com/mzch0210/KuaiLive-Agent/commit/94ac9289be00d381e2c8b98562a905712ef6ec81). This is a concise first draft, **not** a reviewer-tightened acceptance-ready Section 6.3. Sections 1–5 and 6.1–6.2 were not edited in this drafting task.
- [GitHub Actions build 37880277301](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37880277301) completed successfully on the matching manuscript commit and uploaded [PDF/LaTeX log artifact 11594088285](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37880277301/artifacts/11594088285).
- The final 24-page PDF was rendered and pages **19–20** visually inspected. The 2×2 table has all four expected cells and legible column headers; the candidate-allocation paragraph finishes on page 19, and the complete three-seed and state-contribution explanation finishes on page 20 before the References heading. No table clipping or orphaned scientific limitation sentence remains.
- The LaTeX log contains **zero fatal errors** and no newly introduced Section 6.3 overfull warnings; a pre-existing 5.51 pt overfull paragraph at earlier manuscript lines 141–142 remains outside this scope. A full author-level typesetting review will be needed when Sections 6.4–8 are later added.
- Numerical identity checks against the frozen results ledger remained unchanged throughout writing; 20260918 P0 2×2, all three P1 seeds, 3,000 user resamples and the recoverable group n=206 retain their original meanings.

**Editorial status:** Section 6.3 first scholarly draft completed, verified against P0/P1 artifacts, successfully compiled and page-inspected. A separate KBS reviewer-style tightening and coauthor review remain pending. Sections 6.4–6.5, Discussion, Conclusion and Abstract remain unwritten.
