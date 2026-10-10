# KBS Sections 1–6: four-stage scholarly argument restructuring and reviewer audit

**Date:** 2026-10-10. **Primary research target:** *When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation*. **Frozen scientific authority:** submission-oriented outline C1–C3, exact official manuscript mathematics and study provenance in S1–S9. **No author-permitted scope extension:** no new retraining, new held-out experiments, TEST threshold refitting, benchmark substitution, or redefinition of novelty. This report records an editorial rewrite, not the creation of new scientific evidence.

## Stage 1 — Scientific argument map: complete

The [paragraph-level argument map](KBS_FULL_MANUSCRIPT_ARGUMENT_MAP_STAGE1_2026-10-10.md) audited all six existing numbered chapters and assigned each paragraph a research function. Its central statement is: *A persistent user–creator history helps a knowledge-based recommender only insofar as an instantiated specialist provides positive incremental ranking utility relative to the selected Base under the decision's candidate context; part of that conditional value can be estimated before the outcome.*

| Manuscript chapter | Nonoverlapping scientific responsibility | Central claim / reference |
|---|---|---|
| **1. Introduction** | Frame the unaddressed *incremental decision value of evidence* problem and list C1, C2, C3 distinctly | Why the current Base's competence matters to history value |
| **2. Related Work** | Synthesize rather than catalogue sequence learning, evidence fusion/reliability, expert routing, and live-stream contexts | Novel operational valuation question, not a new generic L2D rule or sampled-metric theorem |
| **3. Problem Formulation** | Formal estimands: event ranking utility, `Δ_M`, conditional `η_r`, selective gain identity, regime prevalence identity | Defines exactly what is being valued and when it is observable |
| **4. Framework** | Instantiation: fixed Dual-ID/LiveRec Bases, Short/Long/Popularity Memory, retrospective states and **pre-outcome** features | Implements a knowledge-informed alternative ranking and conditional choice |
| **5. Experimental Setup** | Reproducible populations, eligible candidate protocols, comparator information access, DEV selection and paired resampling | Makes the different evidence tiers and fair comparisons explicit |
| **6. Results** | Actual finding order: history-state heterogeneity → frozen decision benefit → matched candidate-regime dependence → explanatory robustness → computation cost | Demonstrates C1/C3/C2 as one logical scientific story |

The accepted original chapter and subsection order was maintained. Results deliberately present C3 before C2 because the selection question follows the observed C1 heterogeneity, while C2 establishes the context under which that measured decision value must be interpreted.

## Stage 2 — Structural and cross-chapter reorganization: complete

[Source change 8dd0c10a](https://github.com/mzch0210/KuaiLive-Agent/commit/8dd0c10accc1571fb34639fc7ebc376f2a0dd25b) revises **35 chapter-level paragraphs** without changing a mathematical equation, numerical table, figure, source citation key or LaTeX label.

- **Introduction:** a single knowledge-value question, complementary empirical tests, and three explicitly distinguished contributions.
- **Related Work:** each prior-work domain now ends at the relevant *decision-value* gap, rather than simply listing architectures and benchmarks. The known sampled ranking metric inconsistency is attributed to prior literature.
- **Problem Formulation:** retains the estimands and algebra but removes repeated comparator implementation details; the nature of retrospective top-m controls is elaborated in Experimental Setup instead.
- **Framework:** describes components and pre-outcome execution. Its specialist selection subsection no longer attempts to repeat the Methods protocol.
- **Experimental Setup:** retains the exact active candidate rule, training-selection logic, statistical units, factorial equations and uncertainty hierarchy; the heterogeneous auxiliary baseline and archival detail is referenced to S2/S3/S5/S8 rather than dispersed throughout the body.

**Residual science boundary:** Fair comparison to an external all-budget SOTA baseline is not claimed; the fixed specialist/value decision is the estimand.

## Stage 3 — Argument-first academic English: complete

[Source change 1df5df22](https://github.com/mzch0210/KuaiLive-Agent/commit/1df5df22d127a78e8b14954ce0b85ff48d50a594) revises **26 Results narrative paragraphs**. The final four-paragraph typesetting revision is [commit 21f67113](https://github.com/mzch0210/KuaiLive-Agent/commit/21f67113af8bc0d5ae5b75543214685a05f8432f); a subsequent source-only float-position refinement [a9c42b87](https://github.com/mzch0210/KuaiLive-Agent/commit/a9c42b8742a69e826b9010c112566cd1bef19e44) prevents the Figure 2 panel from occupying a nearly empty standalone page. The flow now uses **finding → direct matched evidence → necessary scientific boundary**, not an experiment-chronology or response-to-reviewer narrative.

- **6.1:** begins with the substantive result: overall Twitch Memory−Base −0.04232 despite recoverable-history +0.22045; connects the diagnostic observation to pre-outcome choice.
- **6.2:** emphasizes that DEV-frozen Utility actually chose higher-value events: +0.05136 selected, −0.05890 unselected versus +0.00855 retrospectively Difficulty-selected; preserves overall +0.00772 TEST Utility gain, paired CIs, the retrospective equal count, realistic Spearman 0.173 and ~11.7% Oracle headroom.
- **6.3:** establishes matched KuaiLive sampled −0.04120 versus full +0.04631 and +0.08751 shift. The 2x2, three fitted checkpoint seeds and nine negative-draw conditions retain independent interpretations. Sampled ranking inconsistency is recognized as prior work, not new theory.
- **6.4:** two diagnostic questions link observable selector features with specialist history components/recurrence/Base capacity. The Full versus Long-only tradeoff remains quantitative; no ex post selection of a new Memory specialist.
- **6.5:** presents Twitch invocation frequency separately from KuaiLive warmed CPU scoring cost (+1.016ms; 2.03x Base), conditional HGB tree and Memory candidate complexities, and the archived-mask routing limitation.

**Rhetorical effect size (mechanical, not scientific):** comparing the pre-rewrite accepted source with Stage-3 source, Section 6 shortened from approximately 2,451 to 2,109 whitespace-delimited words; literal qualifier terms such as 'not', 'cannot', 'post-hoc', 'retrospective', 'without', and 'only' decreased from approximately 33 to 13. This keyword tally is an editorial diagnostic, not a promise that every word has a uniformly positive sentiment. Scientifically negative effects and reproducibility-limiting facts are expressly retained.

## Stage 4 — Independent scientific and submission-source checks

**Baseline for invariant verification:** pre-rewrite frozen `main.tex` source commit [687814cc](https://github.com/mzch0210/KuaiLive-Agent/commit/687814ccca7884b3eee91121fcf8cd4e521e6531). Final editorial manuscript source at [a9c42b87](https://github.com/mzch0210/KuaiLive-Agent/commit/a9c42b8742a69e826b9010c112566cd1bef19e44), following the [21f67113](https://github.com/mzch0210/KuaiLive-Agent/commit/21f67113af8bc0d5ae5b75543214685a05f8432f) paragraph tightening and a local FloatBarrier-compatible Figure 2 placement correction.

| Independent check | Result | Notes |
|---|---|---|
| Exactly ten mathematical equation/align environments, byte-identical to prior accepted revision | **PASS** | No change to utility, policy or factorial formulae |
| Eight primary `figure`/`table` environments | **PASS** | No removed figure or table, unchanged event/CI values in exhibits |
| Current numbered chapters and subsections | **PASS** | All six chapter and 5 Results subsections preserved |
| Cross reference labels and BibTeX bibliography | **PASS** | 43 uniquely named `\\label`s, all `\\ref`/`\\eqref` resolved; 25 cited keys all present |
| Main-to-supplement Table Sx.y pointers | **PASS** | S5.2, S6.1, S6.4, S7.1 and S9.1 all present in the 23-table unified S1–S9 source |
| Primary effect and cohort identities | **PASS** | Original 44,221 Twitch, 6,650 selected, 10,222 KuaiLive, +0.00772 Utility, +0.08751 matched regime and −0.04232 overall Memory retained |
| Source-level scientific inferential limits | **PASS within stated protocols** | Target-defined states retrospective; DEV-only feature tests; KuaiLive P2 previously inspected TEST; Difficulty same-count batch control retrospective; benchmarked CPU mask replay remains separate |
| Final exact-source LaTeX PDF and rendered-page confirmation | **PASS**, [Actions #38027661198](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38027661198), [PDF artifact #11660413059](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38027661198/artifacts/11660413059) | **25 pages**, final §6.5 cost text on p.21 followed by References on p.21, no unreadable overflows or blank figure page |
| C1–C3 novelty definitions | **UNCHANGED** | Reorganized prose, not the outline's substantive claims |

### Exact-source final PDF proof

The accepted compilation is [GitHub Actions run 38027661198](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38027661198) at source commit **a9c42b8742a69e826b9010c112566cd1bef19e44**, [artifact 11660413059](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38027661198/artifacts/11660413059). The actual binary PDF and `main.log` were downloaded and inspected with PyMuPDF and visual page rendering. The compiled PDF is **25 pages**, with **zero new LaTeX errors, no overfull hboxes, no undefined citations or references**. The §6.1 figure and evidence table appear before §6.2 without a float-only page; Methods → Results and Results → References transitions are legible. **This passes the requested six-chapter source/PDF gate, not the complete eight-chapter submission gate** because the Abstract, Discussion and Conclusion remain unwritten.

## Remaining issues outside six-chapter editorial scope

1. **Abstract, Section 7 Discussion and Section 8 Conclusion remain unwritten.** They must synthesize the source-checked evidence without adding generic gate optimality or causal claims.
2. **S1–S9 is compiled and source-audited, but author / coauthor approvals, durable archive location for historical artifacts, and final live KBS-specific submission rules remain to be cleared.** Published GitHub Actions artifacts are retention-limited.
3. **Broader external validity and deployment:** no new independent full-scale KuaiLive gate TEST, causal candidate-count experiment or online production A/B is claimed. Existing restrictions are sufficient for C1–C3 as currently defined; future claims beyond that scope require dedicated evidence.
4. **Scholarly language verification:** final coauthor native-level English review should verify term capitalization (Base, Memory, Utility, Difficulty) and avoid interchanging event-level utility with user-level welfare or real business engagement.
5. **PDF layout resolved:** an initial Stage-3 build exposed four slight overfull lines (2.27pt, 1.77pt, 5.34pt and 5.49pt), removed by [21f67113](https://github.com/mzch0210/KuaiLive-Agent/commit/21f67113af8bc0d5ae5b75543214685a05f8432f). Rendered pages then exposed Figure 2 stranded on an almost empty page; [a9c42b87](https://github.com/mzch0210/KuaiLive-Agent/commit/a9c42b8742a69e826b9010c112566cd1bef19e44) permits top/here placement. The final 25-page PDF was downloaded and rendered: **Table 3 on p.15 and Figure 2 on p.16, both preceding the §6.2 text on p.16; §6.3 begins p.17; §6.4 begins p.19; §6.5 begins p.20 and ends p.21; References starts p.21**. No new blank page or text clipping, no overfull or undefined references. The sole remaining log notice is the benign LaTeX change of a `!h` float specifier to `!ht`.

## Editorial verdict

The six chapters now present a coherent, claim-driven evidence narrative while preserving fixed C1–C3 scientific meaning and empirical reproducibility. The revision directly addresses the user's concern about fragmented organization, repeated methods and defensive process language. This is a **stage-scoped editorial acceptance**, not a statement that the full paper is ready for submission or that negative results or important inference restrictions have been suppressed.

**External academic writing source:** [Elsevier, *How to Write the Results Section*](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/how-to-write-the-results-section-of-a-research-paper/); [Elsevier, *How to structure a science paper*](https://www.prod.webpresence.elsevier.com/connect/the-condensed-read-how-to-structure-a-science-paper); [official KBS aims and scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051). These are scholarly writing and journal-scope benchmarks, not invented article-length or manuscript-format prescriptions.