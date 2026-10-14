# N10-C6 | KBS referee-style screening and submission gates (human signoff pending)

Date 2026-10-14 | **technical evidence consolidation pass; human submission approval HOLD**. This is an author-side self-review workflow and does **not** represent external peer review, journal editorial endorsement or permission to submit private data.

## Evidence and QA reviewed

- C0 frozen evidence source guard actions #38528489454 and #38528837682 success; core B4-A frozen SHA and primary claims unchanged.
- C1 KBS nearby work: Zhong et al. 2026 SAMD now in both BibTeX and Related Work; MHGFCL/DS-Frame/KDD sampled metrics and learning-to-defer acknowledged. An explicit P1→P2→P3 paper diagram distinguishes valuation, consequential supervision and historical-source validity.
- C2-A public-only 50,049 DEV quality/call frontier #38529277271 success; zero-overhead shadow price not equated to practical cost.
- C2-B real RTX 3090 matched 256 distinct DEV, 3 counterbalanced repeats #38530526158 success: Always Memory 0.69165ms mean vs original Utility 1.76941ms, exactly 31.25% calls. Complete source preprocessing separately timed, but production network/concurrency and online incremental state maintenance not observed. This times original pointwise Utility, not vectorized B4-A F-aligned HGB.
- C3-A historical-null completeness #38530145391 success: B2 1024 DEV original 0.339348/three nulls 0.306491,0.303804,0.305321 with same-cohort TRAIN-only popularity 0.021867 **PASS**; B4-A H2 original 0.334942/three nulls 0.303905,0.304689,0.302796 with original prereveal same-cohort popularity margin **NOT VERIFIED**.
- C4 scientific adjudication report N10_ROUTE_C_C4_THREE_RISK_SCIENTIFIC_ADJUDICATION_2026-10-14.md, preserved frozen B4-A three one-sided Holm-corrected comparisons, all same-period target constraints.
- C5 current source has two new supplement sections S10.17-S10.18, a restrained evidence diagram, official SAMD citation and the adverse DEV benchmark. See successful base C5 PDF build #38531636561; subsequent layout tidy/rebuild status must be checked before final artifact release.
- C6 automated [citation/claim check #38532371661](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38532371661) **SUCCESS**; 35 unique BibTeX entries, 26 distinct cited keys, no undefined or duplicate bib keys, source/S10 claim consistency asserted. Three adversarial static unit tests pass. Further visual PDF QA must use *latest* successful C5 run.

## Reviewer persona E — editorial desk scope and originality

**Question:** Does defining marginal Memory utility and a decision gate add anything not present in conditional memory selection, knowledge fusion and adaptive routing? Is the KBS knowledge-systems scope more than application-level NDCG improvements?

**Evidence:** Distinct P1/P2/P3 exposition and Fig. 1, direct SAMD/MHGFCL/DS-Frame plus sampled NDCG and defer acknowledgement. B4-A H1 connects candidate-dependent training labels to use-time actions on a frozen same-F roster; H2 fixed-F authentic relation arrangement reveals knowledge-source information. Twitch, original KuaiLive, and M3 report distinct ranking units.

**Judgment:** **BOUNDARY-DEFENSIBLE, NOT ORIGINALITY RISK-FREE.** A novelty claim for first memory gate, first expert routing or first sampled metric inversion is unsupported. Author should reread first six pages for redundancy and ensure each contribution states a testable knowledge-use consequence.

## Reviewer persona M — statistical integrity, labels and mechanism

**Question:** Are H1/H2 genuinely independent, equally budgeted, isolated causal effects with completed null controls?

**Evidence:** B4-A A1 pre-sealed 30k main/4096 nested targets; zero old G5 **evaluated target-ID** overlap, not user/source-period independence. Prediction SHA sealed before the one successful A4 reveal; A5 reconstructs frozen weighted values and user-cluster intervals. Holm corrected exactly three registered directional B4-A tests. F/S actual call fraction differences 1.337/1.797 pp exceed originally specified ±1 pp near-equal criterion. S DEV supervision retrospectively retains target in sampled candidate labels; online test uses common pretarget F descriptors. Three H2 seeds act on one nested sample; ~76.8% source edge rewiring also changes higher-order repeats.

**Judgment:** **STRONG_BOUNDED_INTERNAL_EVIDENCE; NOT COMPLETELY CAUSAL OR NEW-PERIOD EXTERNAL.** Original popularity floor NOT VERIFIED AS PREDECLARED. Do not repeat A4, adjust weights or seeds, or call same March 2026 collection period an independent future TEST.

## Reviewer persona S — operational plausibility and intervention semantics

**Question:** Why route to a slower specialist if Always Memory is more accurate and already faster than the combined selector?

**Evidence:** M3 additional-target Always Memory weighted Full-F NDCG 0.348744 vs SAS/GRU F-aligned 0.305446/0.304530; earlier warmed G4 and new N10 real 3090 timing both observe the original Utility selection path slower than unconditional Memory. C2-B component means expose Base+observable feature+HGB overhead. N9 theoretical ideal shadow price has units NDCG per avoided call, not USD or ms; no measured external quota or paid retrieval resource.

**Judgment:** **DEPLOYMENT BUSINESS CASE HOLD; CONDITIONAL INVOCATION ALLOCATION SCIENTIFICALLY VALID.** The authors can claim better ranking subject to an explicit *stipulated specialist-call limit*, but not lower production cost, performance superiority to Always Memory, or practical need for a call cap without external justification. The frozen older Utility timing is not proof that a future batch-optimized F gate cannot improve cost.

## Submission author signoff checklist — open, no invented declaration

- [ ] Final author order, affiliations, corresponding author; replace or manage the temporary Anonymous Authors according to current KBS review procedure.
- [ ] Each real participant approves full manuscript and the truth of author contributions/CRediT, funding and conflict declarations; disclose relevant computational and editorial assistance.
- [ ] The current Elsevier Generative AI policies (updated 2026) require separate disclosure for substantive AI-assisted manuscript preparation and reproducible Methods description for AI use in research work. Actual tools, usage boundaries, and extent of human verification must be supplied and checked by authors. Policy: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals .
- [ ] Read KBS's live Guide for Authors during actual submission for required format and data availability: https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors . Do not assume a maximum page length from a generic Elsevier template.
- [ ] Confirm dataset original scientific-use permission and particular reuse/redistribution rights and reviewer visibility for derived user–author relation records. Private ID/event/edge maps are not public merely because code/aggregates are; when necessary use an accurate data-availability statement rather than uploading private rows. Elsevier cross-journal research data policy: https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-guidelines .
- [ ] Check bibliography publication metadata/DOIs and final PDF figures/table overflow, S1-S10.18 appendix, matching citation keys, sources with correct experimental evidence tiers.
- [ ] Confirm no author wishes to claim operational speed/cost advantage without a separately verified externally meaningful constraint. If such a claim remains central, conduct independent development before submission, do not retrofit A4.
- [ ] Obtain informed actual human author approval of the final text, data use, AI declaration, and cover letter before merging PR or submitting.

## Decision

**Recommendation for this scientific design:** retain the knowledge-valuation / candidate-aligned supervision / fixed-history-source chain as the central empirical KBS contribution, and the honestly bounded invocation-constrained selector problem as a secondary method implication. The C2 negative benchmark and incomplete B4-A popularity predeclared floor are necessary transparency, not publication reasons to remove genuine positive frozen H1/H2.

**C6 status:** author-side source integrity and reviewer simulation PASS, final submission **HOLD** for human author declarations, unresolved rights and final preview signoff. No submission claimed and PR stays draft.
