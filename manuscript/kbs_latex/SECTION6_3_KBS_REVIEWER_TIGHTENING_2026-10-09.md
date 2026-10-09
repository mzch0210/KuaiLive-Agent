# Simulated KBS reviewer-style tightening of Section 6.3

**Review date:** 2026-10-09  
**Manuscript subsection:** [6.3 Candidate-Regime Dependence of Relative Utility](main.tex)  
**Scope:** The requested reviewer-style revision touches only the Section 6.3 prose/table in `main.tex`, the sampled-metrics bibliographic record, and the explicitly scoped review/provenance/status documents. Sections 1–5 and reviewer-tightened 6.1–6.2 have not been rewritten. Section 6.4 onward and the abstract remain unwritten.  
**Scientific baseline:** [verified P0/P1 experiment ledger](../../KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md); [original full KuaiLive manuscript archive](section6_3_kuailive_migration_source.tex), which remains intact; [P0/P1 artifact run 37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645).  
**Status:** Reviewer-style revisions and final PDF build/visual validation completed; coauthor approval pending. This is an internal simulated peer review, not a decision from KBS reviewers.

## Reviewer verdict before revision

The empirical diagnostic is relevant to the manuscript's claim that relationship evidence has *conditional operational value relative to a particular Base*. The major risk is that a nominally impressive sign reversal could be mistaken for (i) a new general inconsistency of sampled recommender metrics, (ii) a causal decomposition of candidate size versus normalization, or (iii) three independent confirmations based on distinct populations. The outcome must be framed as a **fixed-score, paired, post-hoc** analysis supporting the boundary of the valuation principle, rather than a second gate-performance result.

## Line-by-line objections and corrections

| ID | Priority | Reviewer concern about previous text | Academic correction now in 6.3 |
|---|---|---|---|
| R01 | P0 | Merely saying the advantage “reverses” could suggest Memory itself improves in absolute terms. | Report Base and Memory *absolute* NDCG in both native candidate regimes; both absolute ranking scores decrease; only the **Memory−Base ordering** changes. |
| R02 | P0 | A 2×2 factorial design can be mistaken for a randomized causal intervention. | Call the analysis a **two-order, path-averaged algebraic allocation** under fixed raw scores, referring to existing Section 5 formula; explicitly exclude causal identification. |
| R03 | P0 | Candidate membership sounds synonymous with candidate count. | Explain that the factor includes candidate cardinality, composition, and ranking difficulty; the current four-cell design cannot isolate these ingredients. |
| R04 | P0 | Large membership allocation can be incorrectly read as “100.87% of variance explained.” | Report both allocations and their signed sum; explicitly say they are **not shares of statistical explained variance**. |
| R05 | P0 | Sampled/full ranking reversal is not generically new. | Cite Krichene and Rendle's final 2022 *Communications of the ACM* published version; distinguish known relative-order inconsistency from the paper's **specialist-minus-Base, fixed-model context diagnostic**. |
| R06 | P1 | Same-TEST P0/P1 can look like a separate untouched confirmatory test. | Open and close with **post-hoc** status; clarify no independent held-out test or zero-shot gate-transfer evidence. |
| R07 | P1 | Three checkpoints might be misreported as three independent user samples. | Explicitly identify **three training realizations on the same 10,222 users**, with 3/3 direction agreement but no population-of-seeds confidence claim. |
| R08 | P1 | User-bootstrap intervals and seed SD quantify distinct uncertainty. | Specify bootstrap CIs condition on frozen checkpoints/evaluation events while the sample SD comes from only three trained checkpoint pairs. |
| R09 | P1 | It would be inaccurate to call the tiny negative normalization contribution robustly nonzero across all seeds. | The main text says it is **not uniformly distinguishable from zero** across seeds; seed 20260920's conditional CI crosses zero. |
| R10 | P1 | A recoverable-state conclusion could become a history-recovery mechanism story. | State that 206 recoverable cases contribute **−0.00222** to the mean regime shift, while represented and unavailable cases contribute positively; diagnostic target-relative states are not causal mediators. |
| R11 | P1 | Main text may resemble a run diary and duplicate the supplement. | One four-cell table and five short, evidence-focused result/qualification paragraphs. Omit checkpoint SHA hashes, per-seed full tables, historical scoring-anchor disputes, command logs and per-state detailed panels from main text. |
| R12 | P1 | Claims could extend implicitly to online preferences, causal behavior, or selector transfer. | Do not infer online preference, business outcome or expert-gate portability from this post-hoc ranking comparison. |

## Fixed numeric reconciliation (do not change)

- Matched KuaiLive sample: **10,222 unique user–time–target events**. $S$ is a 575-room target-plus-negative sampled-active candidate subset of $F$, the full-active eligible set.
- Training seed `20260918`, fixed room-alpha `0.125`: native sampled Memory−Base **−0.04120411** (Base 0.60709158, Memory 0.56588746); native full Memory−Base **+0.04630669** (Base 0.38571242, Memory 0.43201911).
- Four candidate/score-reference cells: **SS −0.04120411; SF −0.04141760; FS +0.04761085; FF +0.04630669**. Off-diagonal scoring configurations do not describe deployed policies.
- P0 FF−SS: **+0.08751080** with 3,000-user paired-bootstrap 95% CI **[+0.08209796,+0.09325975]**; two-order membership **+0.08826963** CI **[+0.08286671,+0.09397065]**; normalization **−0.00075883** CI **[−0.00117294,−0.00035507]**. These two allocations sum to the native-protocol shift by identity, not by an estimated model fit.
- P1 per-seed FF−SS: `20260918 +0.08751080`, `20260919 +0.08363134`, `20260920 +0.08408403`. Across-seed mean **+0.08507539**, sample SD **0.00212124**, **3/3 negative SS and positive FF**. Mean membership **+0.08563348**, mean normalization **−0.00055809**. Per-seed normalization-reference CI for 20260920 **[−0.00052317,+0.00017555]** spans zero.
- Fixed target-relative states: represented **4,589**, recoverable **206**, unavailable **5,427**. Prevalence-weighted across-seed contributions **+0.038689**, **−0.002216**, **+0.048603**. No increase in state prevalence can explain the paired regime shift, and the recoverable group contributes in the opposite direction.

## Main-text vs supplementary evidence policy

**Keep in Section 6.3:** fixed experimental unit, definitions of native versus analytical cells, one readable 2×2 NDCG contrast table, original-seed paired change and CI, two signed allocations, three-seed mean/SD and exact direction consistency, the qualitative state mechanism caution, plus the post-hoc and known-literature boundaries.

**Retain outside the main manuscript for Supplementary S5/S8:** full per-seed SS/SF/FS/FF values, all within-seed bootstrap intervals, original checkpoint and input SHA256 hashes, exact identity tests, train/setup manifests, state-level per-seed rows, alternate historical model provenance comparisons and per-run resource details. These already exist in [the research ledger](../../KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md); the *formal submission supplementary package* is still to be assembled and its tables linked by their final labels.

**Still not performed:** P2 independent negative-sampling sizes/draws; absent this, the membership allocation cannot establish that the shift is attributable to *candidate count* alone. Do not describe optional experiments as completed.

## Publication-version check

Krichene, W., and Rendle, S., *On sampled metrics for item recommendation*, **Communications of the ACM** **65**(7), 75–83 (2022), DOI [10.1145/3535335](https://doi.org/10.1145/3535335) is the more recent **published journal** version of the formal KDD 2020 proceedings paper. Checked against [dblp 2022 journal record](https://dblp.org/rec/journals/cacm/KricheneR22) and [dblp KDD 2020 record](https://dblp.org/rec/conf/kdd/KricheneR20). `kbs_references.bib` replaces the existing `krichene2020sampled` record with this 2022 journal metadata while preserving the internal key to avoid changing the already frozen Section 5 citation token. No 2020/2022 duplicate of the same work was added. [The prior publication audit](RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md) has been updated accordingly.

## Acceptance requirements

1. Verify that the **post-revision** LaTeX source compiles and the displayed bibliography prints the 2022 *Communications of the ACM* citation.
2. Visually inspect the actual Section 6.3 page(s) in the compiled PDF for the full table, readable cell headings, connected prose, and no stranded post-hoc qualifier.
3. Confirm that 6.1–6.2 and Sections 1–5 source bodies remain unchanged, apart from the bibliographic reference-resolution update.
4. Mark 6.3 reviewer-tightened only after the matching-commit build and visual check succeed; coauthor approval remains a distinct gate.

**Interpretive standard:** KBS explicitly includes recommender systems and intelligent decision support and calls for original AI contributions balancing theoretical and practical study ([official journal scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)). This paper's defensible increment in 6.3 is the bounded context-dependence of the fixed specialist's Base-relative utility, not newly proving a generic property of sampled ranking metrics.

## Completed source, compilation, and PDF inspection

The final Section 6.3 text is committed in [`a1eb2f65`](https://github.com/mzch0210/KuaiLive-Agent/commit/a1eb2f6560b1af1f5d62e26f4358790534a29570). Subsequent commits updated only review/provenance/workspace records. The matching [GitHub Actions build #37882832573](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37882832573) **completed successfully** and uploaded [PDF/log artifact #11595053815](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37882832573/artifacts/11595053815). The compiled PDF has **24 pages**.

**Actual rendered-document verification:**

- Section 6.3 starts on PDF page 19. Its first paragraph reports the full native-protocol contrast with both absolute model scores; the second paragraph ends on page 19 with a complete sentence about the signed allocation identity.
- On page 20, the crossed 2×2 factorial table is complete, its rows and headers legible, and the standalone interpretive paragraph distinguishes *descriptive algebraic allocation* from causal effects and known sampled-ranking inconsistency. The three-seed and retrospective history-state analyses both finish before references begin on page 21. No orphaned "The..." line remains at the page boundary.
- The bibliography on page 24 displays *Communications of the ACM* **65**(7) (2022) 75–83, DOI **10.1145/3535335**, rather than the older 2020 KDD entry. Only one Krichene–Rendle work is cited, with the prior internal key retained.
- There were **zero fatal LaTeX errors** and no new Section 6.3 overfull boxes. The existing 5.51282-pt overfull paragraph at source lines 141–142 occurs in an earlier chapter and was deliberately left untouched.
- Static source comparison against the pre-review manuscript confirmed **Sections 1–5 and 6.1–6.2 unchanged byte-for-byte**; only the Section 6.3 body and reference metadata changed in the paper. All labels and BibTeX keys resolve.

**Final scoped decision:** Section 6.3 now meets the requested simulated KBS reviewer-style tightening and source/build/visual gates. Scientific conclusions remain **bounded, post-hoc, and noncausal**. Full user-event data, detailed seed tables and provenance still need assembly and final stable numbering in the actual submission Supplementary S5/S8. Final coauthor scientific approval remains outstanding.
