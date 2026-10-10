# Stage 4 — Independent KBS Editor/Reviewer Audit, Claim-Evidence Acceptance and Submission Readiness

**Date:** 2026-10-10  
**Scope:** Existing **§§1–7**, formally published nearest prior art, integrated **S1–S9**, PDF display QA, journal-facing requirements and next-stage writing readiness.  
**Status:** **Gate 4-A (seven-chapter scientific/rhetorical review) PASS; Gate 4-B (exact-source PDF source/visual integrity) PASS; final submission readiness HOLD** until §8 Conclusion, Abstract, author-reviewed declarations and final submission materials exist. This seven-chapter review does not constitute a complete submission.

**Authoritative paper outline:** [KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md).  
**Evidence:** [S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md).  
**Prior work packages:** [Stage-1 paragraph/fact freeze](STAGE1_ARGUMENT_GATE1_ACCEPTANCE_2026-10-10.md), [Stage-2 argument tightening](STAGE2_ARGUMENT_REVISION_AND_GATE2_REVIEW_2026-10-10.md), [Stage-3 scholarly/source audit](STAGE3_RELATED_WORK_METHOD_PROTOCOL_COHERENCE_AUDIT_2026-10-10.md).  
**Stage-4 source precision update:** [commit 70adf0c](https://github.com/mzch0210/KuaiLive-Agent/commit/70adf0c4620fa7454f6a4fd71e955f0eb9c32721), canonical [main.tex](main.tex), exact source blob **37c0b5fbefb945174aa13b18da80d8af87b502a3**.  
**Original Stage-3 source:** [db6f9654](https://github.com/mzch0210/KuaiLive-Agent/commit/db6f96545fdbdede198f4a129a29f6db0735a92b), blob **afee37b087dee507f908e0d16816cd462daf7823**.  
**Pre-correction PDF:** [GitHub Actions #38040591733](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38040591733), corresponding 28-page PDF and logs [artifact #11665259920](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38040591733/artifacts/11665259920).  
**Final source-matched build PASS:** [GitHub Actions #38041650582](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38041650582), source commit 70adf0c, [PDF/log artifact #11666461686](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38041650582/artifacts/11666461686). Generated a 28-page PDF; compile, PDF validity and artifact upload passed with zero overfull hboxes, undefined citations/references and fatal errors.

## I. Independent editorial verdict (different from earlier self-acceptance)

**Scientific identity is now coherent:** the manuscript examines when a separately specified historical relationship ranker provides additional *ranking decision value relative to a trained incumbent and eligible candidate universe*. This is an empirical knowledge-valuation and conditional-use question, not a newly discovered subtraction theorem, a generic deferral theory or an independently validated cross-platform utility router.

For KBS, the strongest framing is the **operational value of historical knowledge for AI-assisted ranking decisions**:
- C1: event-wise Base-relative specialist utility and Twitch retrospective history-state heterogeneity;
- C3: pre-outcome conditional utility estimates used by a DEV-frozen Twitch selector and validated on held-out TEST;
- C2: KuaiLive paired fixed-ranker comparison showing candidate-regime-dependent measured marginal utility.

**The prescribed Results order must remain §6.1(C1)→§6.2(C3)→§6.3(C2)**, which follows a Twitch conditional-value→decision-validation chain before the KuaiLive companion context boundary. §7 then interprets complementarity, candidate regime, selection utility, inference boundaries and practical knowledge-decision consequences. This is the outline's real organization, rather than three independent contributions mechanically ordered C1→C2→C3.

**Journal-facing judgment:** a defensible KBS submission concept with carefully bounded offline evidence, but not a guarantee of acceptance and not yet a completed manuscript. An editor/reviewer could still ask whether the operational valuation + routing target has sufficient conceptual advance beyond existing L2D, sampled-metric and evidence integration methods. The paper's defense is the **joint knowledge-use question and two distinct empirical phenomena**, not raw novelty of the mathematical utility difference or gate. Do not claim universal transfer or online speedup to answer that objection.

## II. Claim–evidence–interpretation cross-chapter ledger

| Claim | Inception / formal object | Empirical support | Legitimate Discussion-level conclusion | Inadmissible strengthening |
|---|---|---|---|---|
| **C1: source value is incumbent-relative** | §1 research question; §3 \(\Delta_M=u_K(M,x)-u_K(B,x)\); §4 fixed relationship specialist | §6.1 **44,221 frozen Twitch TEST events**: Base NDCG@10 **0.58211**; always Memory **0.53980** (delta **−0.04232**). Recoverable target-history subset **5,539**, delta **+0.22045**; §6.4 DEV component/history-capacity checks; S4/S6 | Knowledge can be valuable conditionally even if a globally applied fixed specialist underperforms; complementarity is relative to incumbent effective history and the assessed ranking | The history-state label is a legal serving feature; the trained Base's internal information content is causally identified; Memory is globally superior |
| **C3: anticipated relative value supports expert choice** | §3 \(\eta_r(z)\), expected selection gain; §4 **14 pre-outcome** features; §5 threshold and comparator protocol | §6.2 DEV-frozen Twitch TEST Utility **0.58983**; Utility–Base **+0.00772** (95% CI [+0.00641,+0.00903]); Utility–Difficulty **+0.00644** ([+0.00528,+0.00762]); **6,650** calls, 15.04%; S2/S7 | Specialist-relative benefit provides a more suitable decision target for choosing Memory than incumbent difficulty alone in this setup | Equal-count Difficulty is independently frozen for future serving; this is a newly proved general deferral objective; a post-hoc subgroup result is an independent validation |
| **C2: candidate context changes measured marginal utility** | §3 regime variable, §5 matched candidate and crossed-standardization protocol | §6.3 **10,222** already examined KuaiLive TEST events, fixed event/rankers: sampled **−0.04120**, full **+0.04631** (shift **+0.08751**); membership allocation **+0.08827**, score-reference **−0.00076**; S5/S8 | Historical specialist value must be evaluated against the actually ranked alternatives, beyond target-history-state prevalence | Pure candidate-*count* causality has been isolated; three training pairs × nine draws are 27 independent cohorts; same Twitch utility gate has been transferred to KuaiLive |
| **Compute and serving value** | §5 CPU protocol; §6.5/S9 | Twitch selective invocation **15.04%**; **distinct warmed KuaiLive HGB replay** Base **0.991 ms**, selective **2.007 ms**, overhead **+1.016 ms** (**2.03×**) | Decision benefit and computational cost are separate design dimensions; measured selection incurs extra warmed scoring work | General runtime saving, production end-to-end latency, net engagement/GMV improvement, quality-cost Pareto superiority |
| **Evaluation interpretation** | §3 single-positive \(u_K\); §5 room vs streamer tasks; targeted TEST labels | Twitch one-positive availability-aware streamer ranking; KuaiLive next-room ranking within eligible sampled/full active candidates | Within-protocol **offline ranking** evidence and a descriptive two-protocol comparison | Actual causal user watch-time, revenue or full-population relevance improvement |

**All core claim values** were checked for preserved literal presence in the current source, with referenced precision/uncertainty provenance located in existing S1–S9; these are provenance checks, not newly performed training or bootstrap calculations.

## III. Independent referee-style assessment by criterion

### R1. Central problem and originality — scientifically coherent; residual publication competition risk

The Introduction poses the same Base-relative knowledge-use question as the formal outline. Related Work distinguishes history modeling, knowledge/evidence integration, general expert choice and sampled evaluation, treating the latest closest published work as **actual prior art**. The **C1→C3 Twitch chain** is supported by a DEV-frozen / held-out TEST comparison. **C2 KuaiLive** independently supports an *interpretive condition on measured specialist utility*, not predictive-gate transfer. §7.5 makes the three dimensions into a single useful design viewpoint rather than a list of experiments.

The work remains vulnerable to a novelty-focused KBS referee who demands an algorithmically novel estimator or multi-platform frozen policy. This is an **external acceptance risk (P1 editorial risk)**, not a discovered contradiction or an instruction to overstate existing findings. Direct literature confrontation, empirical specificity and bounded conclusion are the most defensible response absent new trials.

### R2. Methodology and internal validity — PASS within evidence tier

\(\Delta_M\), \(\eta_r\), the threshold \(a_\tau(Z)\) and the expected-gain identity are internally compatible. Observed-target evidence states and target-recurrence bins are never substituted for pre-outcome selector inputs. The important fairness limitation is explicit: the Base-Difficulty comparator is given **retrospective TEST-batch top-\(m\)** with \(m\) set by actual Utility invocations, while **Utility's per-request threshold** alone was frozen on DEV. KuaiLive C2 uses the previously examined same TEST events and a descriptive crossed candidate-membership/score-reference decomposition; it is not an independent untouched policy TEST.

The three trained KuaiLive model pairs and nine added sampled draws assess distinct robustness axes. The latter draws concern one original fixed model pair and the same cohort. DEV-only feature/Memory/history sensitivity is not presented as a further independent TEST. User-paired bootstrap uncertainty remains conditional on the selected models and events.

### R3. Experimental competitiveness and cost — adequate for the stated scientific object, not all desired comparisons

Platform-specific Bases are fully specified, the KuaiLive reference competitiveness checks include several other models, and heterogeneity in tuning budgets is disclosed. This **does not establish a globally optimized state-of-the-art benchmark across incompatible room/streamer protocols**, which is unnecessary for the paired conditional value estimand but may be questioned by reviewers concerned with robustness to *alternative strong incumbents*. CPU measurements show **positive extra latency** for a distinct HGB benchmark and cannot substantiate a serving-efficiency advantage.

A future strongest-evidence extension would be an independently frozen policy against additional capable bases or a prospective candidate-regime gate evaluation **if** the paper seeks claims of broad selector transfer; the current restricted evidence does not force such new claims.

### R4. Academic prose, chapter responsibility and layout — PASS subject to final-manuscript completion

§1 states the motivating knowledge-use problem. §2 places it among published alternatives. §3 formalizes the decision target; §4 instantiates the three-component mechanism; §5 specifies target time, candidate eligibility, frozen models, comparison access and uncertainty; §6 provides observations in the outline's order; §7 interprets complementarity, environment and choice. The Discussion is no longer a second full Results table and maintains scientifically essential boundaries.

**One actual editorial precision issue was corrected in this Stage:** The §5 compared-methods **table caption** previously said “Predictive models use development training,” which can be read as incorrectly stating that Base models are trained on DEV. The new caption states Base is trained on **TRAIN**, Utility/Difficulty regression is fitted on **DEV**, the Utility threshold is frozen before **TEST**, and the equal-count controls use the observed TEST Utility call count for retrospective event selection. This is a scientifically important information-access distinction, not merely cosmetic text.

Other scientific boundaries (retrospective history labels, sampled metric, negative overall Memory result, positive CPU overhead) remain. No indiscriminate removal of “not” or “only” took place.

### R5. Full-page visual and technical check — base PDF inspected, final source PDF acceptance recorded separately

**Actual initial 28-page source-matched PDF** from commit \`db6f9654\` was downloaded, examined via \`pdfinfo\`, text extraction and render of **all 28 pages** (not just a Discussion excerpt). Pages 1–28 have readable text and no PDF-extraction block beyond the page rectangle. Four seven-page contact sheets were visually reviewed; key full pages (including Figure 1 on page 8 and the Utility result on page 17) were inspected at greater resolution. Figure 1 is legible, result tables and bibliography are positioned within margins, and no caption overlay or blank/orphaned float page was detected. The observed table/chart layout does not show content loss.

On that 28-page PDF, main chapter positions are Introduction p1, Related Work p2, Problem Formulation p4, Framework p7, Setup p10, Results p15, Discussion p21, References p24. The **first page has no Abstract** because it has not yet been written; absence is a completion blocker, not a PDF rendering error. Final page-by-page QA must be repeated at least for changed front matter / last pages when §8/Abstract are added.

**After the one-caption edit** (commit 70adf0c), the final exact-source [build #38041650582](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38041650582) **PASSED**. The 28-page PDF was downloaded and its updated Table 2 on page 13 rendered and examined at high resolution: no clipping, collision, orphaning or table overflow is visible. The full previous-version 28-page visual review and focused final-source table recheck jointly establish Stage-4 PDF integrity at the current scope. After writing the Abstract, Conclusion and author declarations, a fresh full-pagination audit will be required.

### R6. Referencing and formal publication metadata — PASS in validated scope

The source contains **49 unique \`\\label\` names**, no duplicate labels or missing \`\\ref/\\eqref\`, and **28 cited BibTeX keys**, all present in **29 BibTeX records**. No original citation keys have been removed by Stage 4. The sole unused record \`yue2026collappa\` is nonblocking source cleanup. Explicit supplementary table references S4.1, S4.2, S5.2, S6.1, S6.4, S7.1 and S9.1 occur in the integrated supplement.

Nearest formally published references have been cross-checked against publisher/proceedings pages:
- Chen et al., **MemRec, ACL 2026**, https://aclanthology.org/2026.acl-long.2061/, DOI 10.18653/v1/2026.acl-long.2061.
- Xu et al., **GUIDER, AAAI 2026**, https://ojs.aaai.org/index.php/AAAI/article/view/38639, DOI 10.1609/aaai.v40i19.38639.
- Mozannar and Sontag, **ICML/PMLR 2020**, https://proceedings.mlr.press/v119/mozannar20b.html; Narasimhan et al., **NeurIPS 2022**, https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract-Conference.html.
- Montreuil et al., **AISTATS/PMLR 2026**, https://proceedings.mlr.press/v300/montreuil26b.html.
- Krichene and Rendle, **Communications of the ACM 65(7):75–83 (2022)**, DOI 10.1145/3535335.
Publication information in the current BibTeX conforms in these checked cases; **this is not an assertion that all 29 records underwent new complete publisher metadata re-verification in Stage 4**. Preserve the existing formal-publication audit for broader coverage.

## IV. Official journal and publishing policy audit (as distinct from third-party advice)

**Journal fit:** Elsevier's official [KBS aims/scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) encompasses knowledge-based/artificial intelligence systems, recommender systems, decision support and theory–application balance. The subject fits; acceptance still requires a defensible conceptual and empirical increment.

**Journal guide accessibility limitation:** The [KBS-specific Guide for Authors](https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors) was not directly retrievable through automated public web access (HTTP 403); **do not substitute a third-party template's rules for official KBS-specific hard requirements**. Elsevier's generic ["Your Paper Your Way"](https://www.elsevier.com/subject/next/guide-for-authors) page opened is explicitly labeled for **Next journals**, so it is informative background rather than proven controlling KBS policy. Before uploading, the author must inspect the KBS-specific guide inside ScienceDirect/Editorial Manager and validate details such as required Highlights, abstracts, title-page/anonymization, statements, supporting files and article type.

**Publisher-wide generative AI policy, updated in 2026:** [Elsevier official policy](https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals). Where ChatGPT or similar tools contribute to manuscript preparation beyond basic spelling/grammar checking, a **separate generative-AI-use declaration immediately before References** is required, specifying tool and use and confirming human review and full author responsibility. Tools used *within research methods* should be described reproducibly when materially relevant. This project used ChatGPT to assist manuscript drafting/editing and reference organization, so a **true author-reviewed declaration** is a submission requirement; do not fabricate a claim that all human coauthors have already reviewed and approved it.

**Disclosure and author fields:** The current LaTeX contains \`\\author{Anonymous Authors}\`, no verified full authors/affiliations, no definitive funding, competing-interest, CRediT or data/code availability statement. These cannot be filled from guesses. Collect/confirm them with human authors at submission-package stage; do not invent funding or assume no conflicts.

## V. Independent risk disposition and what is genuinely still open

| Risk class | Finding | Disposition |
|---|---|---|
| **P0 scientific contradiction** | None detected in current specified contribution scope | **0 open** |
| **P1 scientific/narrative inconsistency** | None detected within C1–C3 definitions and the evidence hierarchy after precision correction | **0 open inside §§1–7** |
| **P1 external reviewer judgment (not a manuscript factual error)** | Novelty might be judged incremental relative to general L2D and sampled metric research; nonuniform baseline tuning and distinct-platform overhead affect breadth of claims | **Live editorial risk; address in cover letter and carefully scoped Conclusion; optional extra data only if widening claims** |
| **P1 required final-manuscript components** | **No Abstract, no §8 Conclusion, author record placeholder and no author-confirmed declarations** | **Submission HOLD** |
| **P2 source cleanup** | One uncited BibTeX record, final KBS-specific Guide for Authors rules not independently retrievable, exact final-source PDF visual recheck to close | **Do at final package stage** |

**Gate-4 disposition:** **PASS for current §§1–7 substantive review and matching-PDF technical integrity.** The seven-chapter research narrative is suitable as a stable base for writing §8 Conclusion. **Do not call the whole manuscript “submission-ready” yet.** The next authoring sequence should be (1) §8 factual bounded Conclusion; (2) concise independent Abstract; (3) Highlights and truthful AI/data/funding/author declarations, possibly in separate submission files; (4) final current KBS-specific author-guide and final PDF whole-page review. Avoid reopening accepted §§1–7 for incremental stylistic preferences unless a concrete contradiction appears.
