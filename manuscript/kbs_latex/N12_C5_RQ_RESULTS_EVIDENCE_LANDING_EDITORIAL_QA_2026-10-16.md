# N12-C5 | RQ-centered Results reconstruction and source-by-source evidence landing

Date: 2026-10-16. Stage: C5 scientific source revisions completed, manuscript and S10 supplement revised. The final source, figure/table, and two-PDF verification completed in GitHub Actions run #38864362019. This is a research-writing audit and not a new TEST analysis.

## 1. Structural and conceptual argument

The older five Results subsections told overlapping experimental stories: historical complementarity, sample/full candidate results, gate experiments, relational controls and execution cost, with DEV exploratory detail interwoven among primary frozen evidence. N12-C5 reorganizes them into **four question-led sections** without changing the underlying experiments or original source claims:

- **5.1 RQ1: When Is Relationship Knowledge Incrementally Valuable?** Twitch/LiveRec original streamer TEST (negative unconditional Memory but large recoverable group) and original KuaiLive same-event sampled-active versus full-active room-ranking reversal. This defines knowledge value as jointly incumbent/history/candidate-conditioned. The retrospective Twitch state figure and the original KuaiLive factorial comparison remain in main. The full Twitch 3-state numeric/CI table moves intact to S10.19 Table S10.13.
- **5.2 RQ2: Does Candidate-Aligned Value Supervision Improve Knowledge Use?** Twitch frozen-pointwise versus retrospectively count-matched comparator; M3 original 47,575 author TEST, six checkpoint fits and Holm within-fit inference; most prominently, original source-period 30,000 different target IDs H1 F-aligned/S-aligned frozen SAS/GRU evaluation with actual natural calls. The M3 50,049 DEV S/F transfer and Twitch DEV feature ablation are only explanatory follow-up, their complete numeric tables preserved as S10.19 Tables S10.14 and S10.16.
- **5.3 RQ3: Does Authentic Relationship History Matter with Fixed Candidates?** The frozen nested 4,096 H2 original-versus-three-closed-hour null table is **first primary evidence**, with 1,024 DEV null and Full/Long sampled/full interactions as supporting analysis. Full DEV knowledge-source component results live in S10.19 Table S10.15.
- **5.4 Operational Conditions: Invocation Limits and Measured Scoring Cost.** Explicitly reports limits and hypothetical per-call utility disutility, higher absolute Always Memory scores, unfavorable measured original Utility gate latency with original GPU means; refuses to imply an established serving-cost saving. The original N10 cost evidence table remains in the main manuscript.

Each subsection now begins with the relevant question, follows fixed comparisons with estimates/CI where warranted and bridges to the next RQ based on what the preceding evidence has not demonstrated. The source-validity RQ3 is **parallel to RQ2 and not a claimed causal mediator**.

## 2. Lossless original Results table disposition

| Original N11 source table | New location | Status |
| --- | --- | --- |
| tab:results-evidence-states | Supplementary **Table S10.13**; original Twitch figure still in main | Fully preserved including n, Base, Memory, deltas and CIs |
| tab:results-factorial | Main RQ1 | Exact frozen table LaTeX |
| tab:results-m3-dev-regime-transfer | Supplementary **Table S10.14**, main RQ2 cites and explains | Full six DEV rows, rates and caveats |
| tab:results-twitch-policy | Main RQ2 | Exact frozen table LaTeX |
| tab:results-m3-policy | Main RQ2 | Exact frozen table LaTeX |
| tab:results-m3-robustness | Main RQ2 | Exact frozen table LaTeX |
| tab:results-m3-b4a-supervision | Main RQ2 | Exact frozen 30k H1 table LaTeX |
| tab:results-m3-dev-source | Supplementary **Table S10.15**, main RQ3 cites | Full five component rows |
| tab:results-m3-additional-relation-identity | Main RQ3 | Exact frozen 4096 H2 table LaTeX |
| tab:results-feature-ablation | Supplementary **Table S10.16**, main RQ2 cites | Full DEV dimension/gain/CI/correlation |
| tab:results-n10-cost | Main Operational Conditions | Exact frozen timing table LaTeX |

The raw original complete N12-C4 Results source, all original eleven LaTeX table blocks and original figure are locked in \`analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json\`. In case of any loss, this is the canonical original source for restoring the numeric content. The C5 auditor enforces that 7 primary main table blocks are **exact unchanged source text** and that the four relocated tables' complete numbers appear in S10.19, with no dangling main refs.

## 3. Results and limitations that are not eligible for stylistic deletion

- Twitch 44,221 TEST NDCG base 0.58211 vs Memory 0.53980; recoverable-but-unrepresented 5,539 requests improve +0.22045 only in hindsight-defined groups, not at known serving labels.
- Original KuaiLive 10,222 same room targets, sampled Memory--Base −0.04120 vs full-active +0.04631, paired +0.08751; candidate set-size, identity, competition change jointly, not a single causal size effect.
- Original M3 author 47,575 TEST, six fits on the same users, primary SAS Utility 0.30287 vs Base 0.25800, Always Memory 0.34679; 29.21% frozen Utility calls, no guaranteed equal-budget comparison.
- Frozen additional source-period target IDs 30,000: SAS Full-minus-S +0.005391, CI [0.003646,0.007174], Holm p 0.000600, F/S calls 8704/9105. GRU +0.003585, CI [0.001599,0.005576], Holm p 0.000800, F/S calls 8629/9168. The achieved 1.337/1.797 pp call differences surpass nominal 1 pp equivalent-budget band. M3 same period, not independently collected later TEST, user/history may overlap.
- Frozen nested 4096 same-period authentic Full Memory 0.334942 vs within-event null mean 0.303797, Δ +0.031145, CI [0.027389,0.035098], Holm p 0.000600; 3 null seeds reuse the same cohort and strong rewiring changes repeated-pair and high-order structure. The original pre-unseal additional-cohort TRAIN-only popularity margin remains **NOT VERIFIED**, never retroactively certified by DEV.
- Under additional-target unconstrained ranking Always Memory weighted F NDCG 0.348744 exceeds SAS F policy 0.305446 / GRU F policy 0.304530. Counterbalanced warmed 256 DEV ×3 original pointwise Utility is 1.769ms vs Always Memory 0.692ms; this has not measured the newly trained additional-target F-aligned gate or online production costs.
- The earlier methods/protocols' exact 9+2 mathematical blocks and no-target-leakage contracts remain intact. No TEST author label re-unseal, no retraining, no new p-values or altered seeds.

## 4. Source QA requirements and next stage

C5 source gate \`analysis/kbs_plan_c/n12_c5_rq_results_evidence_audit.py\` tests the entire frozen prefix and Discussion+Conclusion suffix, four RQ headings, original table source hashes/content, exact original 9+2 equations, 7 retained tables, full S10.19 migrated rows, original H1/H2/negative-cost values and BibTeX/cross-refs. Successful two-PDF compilation and page-level check additionally required before passing C5.

**C6 next**: harmonize Abstract, Discussion and Conclusion to the new RQ progression, concentrate necessary validity limits rather than repeated defensive negative statements, and check the same single research thesis from abstract to the final claim. C7/8 still require full joint supplement, references, reviewer/editor simulation and author rights/disclosure signoff before any submission. C5 does not authorize PR merge or journal submission.

External editorial orientation: Official Elsevier Knowledge-Based Systems journal page; Krichene & Rendle (KDD 2020) on sampled ranking inconsistency and Zhong et al. SAMD (KBS 2026) on memory admission, which emphasize clear distinctions between retained knowledge, selection and candidate-dependent ranking evaluation.


## 5. Final source, two-PDF and visual acceptance

**Latest full dual-PDF CI**: [GitHub Actions run #38864362019](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38864362019), main-paper and complete-supplement **both SUCCESS**.

| Final output | Pages | Artifact ID | PDF SHA-256 | Verdict |
| --- | ---: | ---: | --- | --- |
| Revised main paper | **36** (C4 was 38) | 12030572470 | bbf9734ef3e3fa0d8b76f5b71d9230fc07a51df319202523b4c1315592f8de1b | PASS |
| Complete S1–S10.19 supplement | **47** (C4 was 45) | 12029844052 | e8edd16ad45b55643559264908ec040d3b3eb4f5be32a83f43d9f57895985463 | PASS |

- C5 automated scientific verifier succeeded: original source prefix and Discussion/Conclusion suffix unchanged; all original 9+2 complete mathematics blocks unchanged; exactly 4 Results roles; all original 11 scientific tables traceable to 7 preserved main LaTeX blocks + 4 S10.19 tables; original frozen H1/H2, user clusters, unequal natural Memory invocations, original H2 missing acceptance check and unfavorable scoring time retained.
- Main and Supplement XeLaTeX/PDF logs: **zero overfull text boxes, zero unresolved references or citation warnings**, no fatal LaTeX errors. Final PDF text checked on main Results pp20–28 (RQ1–RQ3 and operational cost). All primary tables are visible without clipping.
- Supplement S10.19 captions and tables inspected pp46–47. Caption of supplementary Table S10.15 initially orphaned at bottom of p46; corrected with LaTeX page break. **Final verified PDF page 47 shows S10.15 heading immediately followed by its complete table and then S10.16.**
- S10.19's reader-facing prose was edited to remove process labels, stage names and internal source-file provenance; complete edit history and original LaTeX labels remain traceable in this audit file and the immutable C5 original-Results fixture. No empirical table has been recomputed.
- Seven main Results tables preserve their original complete frozen LaTeX blocks. Two original experimental-design tables remain in main (9 main manuscript tables total), with the 4 moved supporting result tables published in the supplemental S10.19 subsection.
- **C5 completed.** The N12 manuscript at this stage has the new Introduction, Related Work, Method, Experimental Design and Results, but **Abstract, Discussion and Conclusion remain the prior N11 version pending N12-C6**. The current 36p/47p pair is a rigorous phase-complete interim reviewer draft, not a submission-approved final paper.

**Next N12-C6**: rewrite Abstract, Discussion and Conclusion to the one-thesis/RQ1–RQ3 argument, concentrate rather than delete truthful constraints, and remove remaining project-style chronology from submission prose. N12-C7–C8 will then complete whole-paper/supplement source QA, journal-style referee simulation and owner signoff.
