# KuaiLive-Agent → KBS: project-level scientific review and Section 7 Stage-1 continuation

**Review date:** 2026-10-10  
**Repository:** [mzch0210/KuaiLive-Agent](https://github.com/mzch0210/KuaiLive-Agent)  
**Authoritative manuscript:** [main.tex](main.tex) on `main` (the accepted 7.1–7.2 wording is sourced from commit [aa1d511d](https://github.com/mzch0210/KuaiLive-Agent/commit/aa1d511df190c9ec0a7dd29ae538636bc8d646f4)).  
**Approved constraints:** [submission-oriented outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md); [Section 7 writing plan](SECTION7_KBS_DISCUSSION_WRITING_PLAN_2026-10-10.md); [four-stage Sections 1–6 review](KBS_FOUR_STAGE_ARGUMENT_RESTRUCTURING_REVIEW_2026-10-10.md); [Section 7.1–7.2 independent review](SECTION7_1_7_2_KBS_REVIEWER_TIGHTENING_2026-10-10.md); [unified S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md).

## 1. Executive scientific assessment

The defensible KBS contribution is **a decision-relevant assessment of persistent relationship evidence relative to a specified incumbent ranker and candidate environment**. The paper does not need a newly invented historical-memory architecture or a general routing theorem to make that contribution; it needs a clear operational estimand, a trustworthy frozen selector comparison, and an explicit explanation of where the estimand changes meaning.

The evidence chain is coherent:

1. **C1: operational relative evidence value.** A fixed Short–Long–Popularity specialist is worse than the LiveRec Base in aggregate but provides substantial favorable ranking utility in a retrospectively defined recoverable-history subgroup.
2. **C3: predictive decision value.** An observable pre-outcome Utility policy makes better choices than always-Base and a retrospectively matched-count Base-Difficulty comparator on the one frozen Twitch TEST cohort. This directly operationalizes why *relative* utility rather than absolute difficulty matters.
3. **C2: context dependence.** A fixed-checkpoint KuaiLive comparison shows that the operational sign of that same kind of specialist–Base utility contrast changes with the candidate-ranking protocol. A crossed score-reference allocation and repeated seed/draw analyses characterize this specific reversal; they do not isolate a causal list-size effect.
4. **Explanatory boundaries.** Twitch DEV history/feature/component diagnostics and the separate KuaiLive CPU timing protocol explain interpretation and costs, without serving as independent tests of the frozen Twitch gate.

The original Sections 1–6 were reorganized around this logic before Section 7 was started. The canonical manuscript currently has **six complete main sections plus Discussion subsections 7.1 and 7.2**; subsections 7.3–7.5, Conclusion, and Abstract remain to be written. Bibliography and a unified supplementary manuscript exist. This is a strong *evidence-defined writing baseline*, not a completed submission package.

## 2. Verified quantitative and inferential anchors

| Claim / status | Principal numerical anchor | Design and required interpretation |
|---|---|---|
| C1 global Memory contrast | Twitch frozen TEST `n=44,221`, Base `0.58211`, always-Memory `0.53980`, Memory–Base `−0.04232` | Negative overall benefit is a substantive finding, not a writing defect. |
| C1 recoverable state | Twitch frozen TEST `n=5,539`, Memory–Base `+0.22045` | Target-dependent retrospective group; cannot be passed as a serving-time label. |
| C3 fixed Utility selector | Twitch frozen TEST Utility–Base `+0.00772`, 95% user-paired CI `[+0.00641,+0.00903]`; `6,650/44,221` selections (15.04%) | DEV OOF threshold and fitted predictor frozen before one-shot TEST; policy gain is modest but positive. |
| C3 equal-count control | Utility–Difficulty `+0.00644`, 95% paired CI `[+0.00528,+0.00762]`; selected Memory–Base `+0.05136`, unselected `−0.05890` | Difficulty uses *retrospective TEST-batch top-m* based on the Utility policy’s observed count, not a deployable fixed pointwise comparator. Subgroup differences are derived summaries, not new independent hypothesis tests. |
| C3 predictive headroom | Spearman `0.173`; approximately `11.7%` of the two-fixed-ranker same-count hindsight Oracle improvement recovered | Meaningful decision ranking does not imply pointwise utility calibration, globally optimal deferral, or online economic impact. |
| C2 matched KuaiLive contrast | `n=10,222` same user–time–target events; sampled Memory–Base `−0.04120`, full `+0.04631`; shift `+0.08751` | Fixed checkpoint pair, histories, raw scores and sampled DEV fusion; **previously inspected TEST**, therefore a post-hoc candidate-regime diagnostic rather than independent prospective TEST. |
| C2 crossed allocation | Ranked membership `+0.08827`, z-score reference `−0.00076` | Algebraically sums to `+0.08751`. Membership bundles candidate count, identity, and competition; not an isolated causal effect. |
| C2 repeat settings | Three independently trained KuaiLive checkpoint pairs on the same 10,222 users, and nine candidate draws across three sampled sizes | Directional stability **within that cohort/protocol**; do not pool nine draws as independent datasets. |
| Mechanisms | DEV recoverable Long-only `0.63890`, Full `0.53298`; unavailable Long-only minus Full `−0.03208` | State-specific trade-off does not authorize replacing the predesignated Full expert after observing subgroup outcomes. |
| Resources | Separate warmed KuaiLive CPU Base `0.991 ms`, Selective HGB `2.007 ms`; `+1.016 ms` or `2.03×` mean; 14.25% benchmark Memory calls | Archived routing-mask replay and separately fitted 81-tree HGB; not a measured latency reduction from the frozen Twitch policy. |

Principal sources: [main.tex](main.tex), [S4](SUPPLEMENTARY_S4_MEMORY_COMPONENTS_DRAFT_2026-10-10.md), [S5](SUPPLEMENTARY_S5_CANDIDATE_REGIME_P2_DRAFT_2026-10-10.md), [S8](SUPPLEMENTARY_S8_MODEL_SEED_ROBUSTNESS_2026-10-10.md), [original argument evidence audit](KBS_ARGUMENT_DRIVEN_REVISION_AUDIT_2026-10-10.md). Values were checked against the original manuscript and relevant supplementary sections, rather than imported from earlier chat paraphrases.

## 3. Project-level assessment from a KBS reviewer perspective

### Strengths that should structure the submitted paper

- **Unified scientific object.** C1–C3 now share `Δ_M=u_K(M,x)−u_K(B,x)` and the conditional quantity `η_r(z)`. Chapter roles are distinct: Introduction defines the decision gap; Related Work establishes the fusion/deferral literature boundary; Problem sets the value estimand; Framework constructs the fixed expert and observable predictor; Experiments specify evidence tiers; Results report effects; Discussion interprets them.
- **Frozen positive decision experiment.** The paired Twitch TEST policy evaluation directly supports a bounded claim of decision benefit, which is more compelling than subgroup analysis alone.
- **Explicit negative evidence.** Always-Memory’s aggregate loss explains why conditional invocation is a real question. The measured compute penalty grounds the design discussion in a practical trade-off rather than an assumed benefit.
- **Matched environment analysis.** The KuaiLive full-versus-sampled comparison tests an important operational issue: a fixed specialist may be ranked against different candidate universes, changing which ranking rule appears preferable.
- **Source-backed reproducibility.** The manuscript, formal estimand, fixed scorer, linked evidence audit, CIs, supplementary tables and CI build are available for scholarly verification.

### Remaining reviewer risks, in descending practical importance

**P1 — conceptual distinctiveness within KBS.** A reviewer may regard the mathematical utility difference as straightforward and the routing estimator as standard. The contribution must be expressed as a *knowledge-value design and evaluation principle*, demonstrated through condition-specific historical evidence and explicit expert–Base/candidate dependence. Do not represent simple subtraction or histogram boosting as new general methodology. Section 7.5 should provide the corresponding constructive system-design synthesis.

**P1 — strength of decision comparator and transfer evidence.** The frozen Twitch Utility result is one held-out selector validation against always-Base and matched-count Difficulty, not superiority over fully tuned modern deferral schemes. The equal-call comparator is not an online hard-budget rule. Future improvements require competitive specialist-selection baselines with symmetric tuning and independent frozen replications, but the present paper should report exactly what was tested.

**P1 — different evidentiary status of Twitch and KuaiLive.** Twitch C3 is a frozen one-shot TEST decision experiment. The matched KuaiLive C2 result reuses previously inspected TEST users, and the different room/streamer ranking units, Base models and candidate protocols preclude equating the two as external gate replications. Maintain this distinction once clearly in 7.4, rather than repeating defensive qualifications in every paragraph.

**P1 — candidate-regime identification.** The sign reversal is scientifically important but partly adjacent to established sampled-ranking-metric literature. The present addition lies in the fixed Memory-minus-Base decision context and crossed score-reference comparison. The allocation is descriptive; effects of size, composition and ranking competition require controlled perturbations to separate.

**P1 — historical evidence versus serving-time observability.** Represented/recoverable/unavailable states require the observed target. Decision-time Utility uses 14 pre-outcome features. A submission that blurred this distinction would appear to have label leakage; the current source keeps the boundary. Section 7.3 should connect the two without converting diagnostic groups into an executable rule.

**P1 — practical value and cost.** `+0.00772` utility on a frozen offline ranking task is meaningful within the protocol, but the separate KuaiLive CPU benchmark shows additional mean latency, not savings. An observed call fraction cannot justify production throughput, energy or user-impact claims. Section 7.4 should state this in a single compact scope paragraph, and 7.5 should propose budget-aware validation.

**P2 — supplementary/archive and submission-package finish.** The unified S1–S9 file is extensive and compiled, yet final coauthor review, long-term preservation of retention-limited CI artifacts, current KBS file/declaration requirements, and complete Section 7/Conclusion/Abstract are pending. These are submission-readiness issues, not reasons to relabel existing data.

## 4. Section 7 Stage-1 continuation: accepted manuscript text versus remaining writing

### Source inspection

- **7.1 — Operational Value Is Base- and Context-Dependent:** Two concise scholarly paragraphs connect Base-relative incremental utility to Twitch recoverable-history heterogeneity and the model/specification dependence from separately trained contexts and Long-only/Full DEV comparisons. The cited fusion/reliability/negative-transfer literature is used as scientific context, rather than a claim of a new intrinsic value theory.
- **7.2 — Interpreting Conditional Evidence and Candidate Regimes:** Three paragraphs connect the retrospective state diagnosis to paired KuaiLive candidate environments; credit established sampled-ranking inconsistency; interpret the `+0.08827 / −0.00076` allocation without candidate-size causality; report robustness at its proper repeated-checkpoint and negative-draw levels; and transition into the observable decision problem for 7.3.
- **Integrity:** Each subsection’s numerical, methodological and literature statements has an explicit anchor in Sections 3–6 and S4/S5/S8. Target-state retrospectivity and the distinct statistical units are preserved. Existing labels and citations are retained. The accepted `main.tex` source was not altered in this continuation because no material scientific or rhetorical error requiring re-opening 7.1 or 7.2 was found.

### Independent first-stage acceptance gate

| Gate | Decision | Basis |
|---|---|---|
| Interpret C1+C2 without redefining C1–C3 | **PASS** | Two distinct subsection arguments; no new theorem, intrinsic value metric or causal candidate-count claim |
| Separate retrospective diagnostic states from deployment features | **PASS** | 7.2 explicit retrospective wording, 7.1 observed-target condition, Section 4 source |
| Use real paired numbers and attribute variability correctly | **PASS** | Main §6.1/6.3 and S4/S5/S8 corroboration |
| Distinguish known sampled-metric theory from this study | **PASS** | Krichene and Rendle 2022 credited explicitly; comparison framed at the fixed specialist–Base decision |
| Conform to accepted KBS scholarly tone and avoid Results duplication | **PASS within Stage 1** | Argumentative synthesis, restrained citations, no run chronology in manuscript prose |
| Current accepted source PDF build | **PASS for aa1d511d** | [GitHub Actions #38031685746](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38031685746), successful; [PDF/log artifact #11662401005](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38031685746/artifacts/11662401005), reported 26 pages, layout checked in prior audit |
| Independent journal peer review / coauthor sign-off | **OPEN** | Editorial acceptance above is an internal source and evidence check only |

**Stage-1 editorial decision:** **Retain the already finalized 7.1 and 7.2 unchanged.** The first planned writing increment is already complete and successfully compiled; rewriting it in this continuation would undo accepted changes without new evidence. This decision is intentionally *not* an approval of the full Discussion or full paper.

## 5. Next authorized writing increments under the original plan

**Increment 2 — 7.3 From Relative Utility to Selective Decisions:** Two to three concise paragraphs led by the expected-gain identity and the frozen Twitch TEST Utility–Base and equal-call Utility–Difficulty contrasts; interpret selected versus non-selected relative utility; compare established learning-to-defer work; use the 0.173 predictive rank correlation and 11.7% Oracle margin to calibrate decision claims; avoid a new optimization theorem or an online budget guarantee.

**Increment 3 — 7.4 Validity Boundaries:** Three compact paragraphs separating one-shot TEST versus DEV/post-hoc KuaiLive evidence, target-defined label versus observable features and candidate-state sampling, and measured CPU scoring overhead versus live serving. This should contain the substantive boundary discussion instead of importing a defensive audit-log style into Results.

**Increment 4 — 7.5 Implications for Knowledge-Based Recommendation:** Two paragraphs deriving a constructive design principle: assess historical evidence via **paired model-relative ranking actions**, characterize both history and candidates, and evaluate conditional choice with computational costs. Give a prioritized externally testable research agenda rather than restating results.

**Final Section 7 gate:** Review all five subsections together against the approved central thesis, source C1–C3 and S1–S9; audit all numeric claims and citation keys; compile and inspect an exact matching source PDF. **Then** draft Section 8 and, once the complete interpretation is stable, Abstract. Do not silently treat successful compilation as peer-review acceptance.

## 6. Source-provenance distinction

This review **directly inspected** the current repository, authoritative `main.tex`, original Section 7 plan and acceptance audit, and selected S4/S5/S8 evidence. The precise source-matching 26-page PDF acceptance was **independently confirmed as a successful GitHub Actions run** and read from its prior recorded visual review; no new PDF was generated because no manuscript source changed. No new experiments, test selection, parameter search or unverified performance claims were introduced by this report.
