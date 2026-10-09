# KBS reviewer-style tightening — Results §6.1

**Date:** 2026-10-09  
**Manuscript section:** [§6.1 Heterogeneous Utility of Relationship Memory](main.tex).  
**Scope constraint:** Only §6.1 text, its Figure 2 and Table 3 were revised. Sections 1–5, the archived KuaiLive §6.3 source and not-yet-drafted §6.2–6.5/Discussion/Conclusion/Abstract were left intact.  
**Primary empirical evidence:** [Frozen Twitch one-shot TEST workflow 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303), evaluation job 106686133973, 44,221 target events, 5,000 paired bootstrap replicates; developmental group estimates cross-checked against [DEV component/horizon experiment 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454), job 106700833375.  
**Editorial standard:** Results should report research-question-linked findings in clear, concise prose with nonredundant figures and tables, while interpretation of wider causes belongs in Discussion. This is an **internal simulated peer review**, not a real journal's decision or an assertion that KBS mandates a particular subsection length.

## P0: Source truth and substantive inference

| Issue | Before tightening | Editorial correction and current status |
|---|---|---|
| P0-A: The subgroup results are retrospective | Target state was identified as retrospective but the phrase “depends strongly on evidence state” could be read causally or as a serving-time feature. | Explicitly distinguish association stratified by **realized target creator** from pre-outcome routing. No causal inference or deployable state oracle implied. |
| P0-B: Two evaluation windows are not two independent datasets | “Signs match development” might suggest independent replication. | Call these two chronological evaluation windows of Twitch; matching signs describes within-dataset consistency, not cross-dataset replication or a new independent untouched selector test. |
| P0-C: Aggregate effect lacked interval despite numerical claim | Memory 0.53980 versus Base 0.58211, difference −0.04232 with no CI. | Report frozen TEST paired mean −0.04232 and 95% CI [−0.04521, −0.03950] from one-shot run; subgroup CIs remain faithful to the same run. |
| P0-D: DEV/TEST subgroup numbers could come from different settings | DEV group values and TEST group values need fixed Memory definition. | Both results explicitly refer to the fixed full-memory specialist (not popularity-only or short-long-only), using the official LiveRec base protocol on the appropriate chronological windows. |
| P0-E: Preserve theory and methods definitions | Risk of re-defining `Δ_M`, state definitions, or bootstrap in Results. | Reuse §3/§4 definition, refer to state definitions once; table defines paired conditional mean; 5,000 replicates identified in table caption. No new method theorem. |

## P1: Evidence presentation and academic style

| Line-level edit | Reviewer concern | Resolution |
|---|---|---|
| R01: First sentence | “We first examine whether…” was expansive and repetitive. | Shorten to a single empirical question: uniform or heterogeneous incremental utility. |
| R02: Overall comparison | Under-specified uncertainty for negative aggregate result. | Add exact paired CI without p-value invention or “significance” overstatement. |
| R03: State linkage | Section 4 is the owner of state definition. | Cite Section 4 directly; avoid re-deriving state equations. |
| R04: Main comparison | Figure, table and prose repeated all DEV/TEST numbers and test CIs. | Figure now emphasizes DEV→TEST pattern; table provides numeric TEST scores and exact intervals; prose gives only overall and most decisive subgroup deltas. |
| R05: State naming | Long label “recoverable-but-unrepresented” obscures caption/table scan. | Define in prose, use “Recoverable” in the table and figure; full three-state definition remains in Framework. |
| R06: Figure readability | Whiskers were shorter than plotted symbol radii, producing apparent black dots rather than interpretable 95% intervals. | Remove whiskers from Figure 2 and provide the numerical intervals in Table 3; show DEV open and TEST filled points connected within state, explicitly stating connections are visual guides, not paired user trajectories. |
| R07: Figure/table roles | Substantial visual duplication of TEST point estimates and CIs. | Distinct roles: figure compares chronological windows; table quantifies TEST n, two absolute models and bootstrap uncertainty. |
| R08: Table parsing | Original final column combined effect and 95% CI into an overlong tight cell. | Give effect and CI separate columns under meaningful headings. |
| R09: Model comparison logic | Aggregate inferior Memory needed a stronger explanation for why subgroup results matter. | Place negative overall estimate before conditional results, and report positive recoverable subgroup as a contrast, not as generic Memory superiority. |
| R10: Causal and multiple-testing language | Risks confusing exploratory states with causal mechanism or independent confirmatory tests. | Use “stratification is descriptive,” reserve causal mechanism and generality for Discussion; avoid unreported subgroup-multiplicity-adjusted claims. |
| R11: Serving-time leakage | Target creator is required to compute state; not available to selector. | Put a single decisive non-leakage limitation immediately before segue to §6.2. |
| R12: Transition | Last sentence previously reiterated nondeployability at length. | End with one research question motivating pre-outcome Utility estimation; **do not draft §6.2**. |

## Exact source cross-check

| Metric | Frozen TEST | Development |
|---|---:|---:|
| Population n | 44,221 | 46,878 |
| Represented n | 24,285 | 24,541 |
| Recoverable n | 5,539 | 5,879 |
| Unavailable n | 14,397 | 16,458 |
| Represented Memory–Base | −0.01935012; CI [−0.02234267, −0.01632736] | −0.01995126 |
| Recoverable Memory–Base | +0.22044597; CI [+0.21139676, +0.23000868] | +0.23096894 |
| Unavailable Memory–Base | −0.18214811; CI [−0.18680734, −0.17715296] | −0.19562009 |
| Overall Memory–Base | −0.04231595; CI [−0.04521093, −0.03949774] | not reported in §6.1 |

TEST conditional NDCG@10 source values: represented Base 0.86102241 and Memory 0.84167228; recoverable Base 0.30180595 and Memory 0.52225192; unavailable Base 0.21948429 and Memory 0.03733618. The three disjoint TEST counts sum to 44,221. All CIs are within-state user/event paired 5,000-replicate bootstrap intervals from the original frozen reporting task. The TEST aggregate numbers are likewise from that run. The DEV-only group statistics were already computed before the TEST analysis; no DEV numbers were retuned to match later outcomes.

## Original PDF visual observation and follow-up

The first compiled version (Actions run [37875699664](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37875699664), artifact [11592361414](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37875699664/artifacts/11592361414)) was inspected as a rendered PDF. Figure 2 plus Table 3 floated to the beginning of page 17 and separated a sentence spanning pages 16–17. The plotted confidence-interval whiskers were effectively concealed by dot markers, while Table 3's combined estimate/CI cell was dense. **These concrete presentation defects motivated R04–R08**. The revised figure/table need an additional compiled PDF visual check before calling layout fully approved.

## Acceptance gate for this section

- Verify the revised whole-paper LaTeX compiles; labels and citations resolve on final passes.
- Inspect the actual PDF page(s) containing Figure 2 and Table 3, ensuring no clipped values, awkward page-flow interruption, or unreadable table columns.
- Confirm the new figure does not imply same-event DEV/TEST pairing (the connecting lines are merely visual correspondence of group identity).
- Leave §6.2, the KuaiLive §6.3 archive, the abstract and Discussion untouched.

## Official editorial source references

- [Elsevier, How to Write the Results Section](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/how-to-write-the-results-section-of-a-research-paper/): organize findings by research question and avoid duplicating figures/tables in prose.
- [Elsevier, Concise guide on structuring scientific papers](https://www.prod.webpresence.elsevier.com/connect/the-condensed-read-how-to-structure-a-science-paper): Results versus Discussion separation; self-explanatory figures.
- [Knowledge-Based Systems official scope](https://shop.elsevier.com/subjects/journals/physical-sciences-and-engineering/computer-science/artificial-intelligence/artificial-intelligence-expert-systems-and-knowledge-based-systems): this paper's relevance to recommender systems and intelligent decision support.

## Final build and visual verification

The revised §6.1 passed [GitHub Actions run 37876933951](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37876933951) at commit `441838fc9747c592f36ca80d847822dbc055310b`, with [compiled PDF and logs (artifact 11592638016)](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37876933951/artifacts/11592638016). The 21-page compiled PDF was inspected after rendering: Figure 2 and Table 3 share page 17 below the complete analysis text, both are legible, and the page-16/page-17 sentence boundary was recast at a full stop rather than an interrupted clause. Figure 2 contrasts DEV vs TEST estimates without visually negligible interval whiskers; the full 5,000-bootstrap test intervals appear in the separately headed final table column. The LaTeX workflow completed successfully; no fatal errors and no Section 6.1 overfull-box warnings appeared. One small 5.51-pt overfull paragraph in preexisting Section 2 remains outside this subsection's scope.

**Status:** §6.1 is reviewer-tightened, experiment-source checked, statically validated, successfully compiled and PDF-visually reviewed. This is an editorial-stage approval, **not** coauthor sign-off or a journal's assessment. Future changes to §6.2–6.5 and the paper abstract remain separate tasks.
