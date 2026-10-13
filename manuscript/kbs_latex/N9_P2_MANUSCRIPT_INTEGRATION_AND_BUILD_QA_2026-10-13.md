# N9-P2 — B1/B2 and decision-support robustness manuscript integration & source/PDF QA

**Date 2026-10-13. Technical status: P2 INTEGRATION AND BUILD PASS; scientific journal submission remains HOLD pending P3, human-author signoff and unresolved bounded research risks.**

## 1. Frozen lineage and successful builds

- Original canonical `main.tex` blob before N9: `40be249de52c0ae423b793c0dd4c55f2fdd69f46`; new canonical `main.tex` blob: `2d99f068dc6fc9dcb5085c0f398a71f46f1b6ffd`. New article is still eight sections, now **11 tables and 2 figures**; no new Base re-training or G5 TEST result edits.
- Original supplementary S1–S9 source blob `f5575d29ac3de222a04f78b48698cae119eac0bf` is **left unchanged**. New integrated S1–S10 source blob `4856be8aa2e92886922f9f1a0065e18fb13dbf9e` begins with the byte-identical original S1–S9 source (trailing whitespace aside), appends the new evidence section and is the updated source for N9.
- [Main article build #38383802641](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38383802641): SUCCESS; latest PDF output 35 pages and artifact 11804004496. Existing nonfatal 3.47pt overfull hbox remains subject to copyediting; first-pass citation/reference warnings are not the same as final unresolved key errors.
- [Integrated supplementary S1–S10 build #38384252296](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38384252296): SUCCESS; 34 published-source captioned tables, 5 landscape tables and 24 SHA256 line-wrapping corrections in LaTeX postprocessor; all source-count, math/symbol and PDF fatal-error guards PASS. Artifact 11804803346.
- The original S1–S9 postprocessor and original S1–S9 build workflow are untouched; N9 uses separate `analysis/kbs_n9_supplement_tex_postprocess.py` and `.github/workflows/kbs-n9-s1-s10-supplement-build.yml`.

## 2. Source-to-manuscript integration

| Source | Current scientific manuscript role | Evidence class |
| --- | --- | --- |
| Original Twitch TEST and M3 six-fit TEST | §6.1–6.2 primary conditional knowledge value and supervised selection; original comparative/familywise scope unchanged | Original frozen independent TEST |
| Original 10,222-room candidate comparison | §6.3 retrospective candidate-regime interpretation | Already-inspected diagnostic |
| B1 same-author sample/full policy supervision | §3 candidate-indexed utility contrast, §5 nested exploration, §6.3 six-policy table and user paired differences | Post-G5 50,049-event exploratory DEV |
| B2 knowledge-source ablation | §5 source protocol, §6.4 five-source F/S table and 12-vs-6 feature interpretation | Same DEV cohort as B1 |
| N9-A1 quality versus invocation constraints | §6.5 and §7 conditional decision value; S10.6 detailed frontier | Post-G5 same-cohort DEV, not measured production savings |
| N9-A2 Direct/Two-stage/standalone objectives | §6.5 and §7 decision-target sensitivity; S10.7 comparison table and call caveats | Post-G5 same-cohort DEV; raw fusion not run |

## 3. Static source checks independently rerun after editing

- Every `\\ref` and `\\eqref` key in the current main article has a corresponding `\\label`; all citation keys referenced by main LaTeX exist in `kbs_references.bib`.
- All 56 main labels are unique. Main article includes 11 tables and 2 figures. New `tab:results-m3-dev-regime-transfer` and `tab:results-m3-dev-source` labels are correctly paired with references.
- Exactly one S10 top-level section and four S10 table captions appear in the combined supplement. The entire prior S1–S9 body is retained unmodified as its prefix.
- Original frozen G5 TEST statuses and project claims remain in original archival reports; no assertion of a new independent TEST was made.

## 4. Non-negotiable interpretations and remaining P3 actions

- **R1 BOUNDED**: no new gate theory and no full matched raw score-fusion or published L2D/DS-Frame reproduction. The scientific difference is candidate-/incumbent-relative knowledge-value supervision and downstream decision consequences.
- **R2 BOUNDED scientific decision support / HOLD deployment advantage**: A1 almost always calls Memory at unrestricted thresholds, and M3 Always Memory remains higher in full ranking utility with lower warmed DEV execution time. No net latency or economic saving is established.
- **R3 BOUNDED and partially mitigated**: B1/B2 use the same 50,049 post-G5 DEV events. S is retrospective target-retained sampled evaluation, weak history placebo does not preserve global marginals, and Short-only incurs severe call-rate drift. New independent TEST eligibility remains HOLD pending lawful unexposed data.
- P3 must inspect full PDF visually, check typesetting/caption adequacy, remove residual nonfatal overfull, verify citations and manuscript-to-supplement text boundaries, check novelty presentation and source-to-claim numbers, and finish author-controlled data rights, AI disclosures, authorship and journal-specific submission files.

**Decision: P2 TECHNICAL PASS, P3 SCIENTIFIC/SUBMISSION HOLD.** Code and Results remain subject to human author review and acceptance.
