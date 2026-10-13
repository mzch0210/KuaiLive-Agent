# N9–G5/G6 | Targeted decision-support scientific revision and submission QA

**Date: 2026-10-13.** Scope: eight-section main article and integrated S1–S10. Scientific stance: *R1/R2/R3 BOUNDED, do not call them solved*. Main manuscript post-revision compile **PASS** ([Actions #38391955348](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38391955348)); supplementary final 39-page XeLaTeX build **PASS** ([Actions #38392829047](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38392829047)). Submission remains HOLD.

## Evidence-first G5 article update

The manuscript at `manuscript/kbs_latex/main.tex` (blob `dd57e309fca7ddd59f05d40512539d0ac31aa0c8`) retains the original eight-section argument with 11 tables and 2 figures. Revisions place mechanistic evidence where it belongs without creating a new architecture:
- Abstract, §1 and §7–8: candidate-aligned relative-knowledge supervision and **request-level allocation** rather than merely ranking-metric reversal; explicitly within an exploratory DEV regime.
- §6.3: exact B1-parity allocation analysis, **10,672 SASRec** and **11,517 GRU4Rec** changes in the requests selected for Memory at nearly equal natural calls (21.32% / 23.01%); the F-only requests have higher average realized specialist increment than S-only ones.
- §6.4: source×candidate interaction Full-minus-Long **+0.115382** with 95% paired user CI [0.111724,0.119065], properly distinguished from B2 *selector transfer regret*. **46,462** events with source gap zero in at least one regime, only **66** strict opposite nonzero source-gap events.
- §6.5: hypothetical all-policy net-utility upper envelope `J_lambda=F_NDCG-lambda*realized_calls`, with 30%-cap policy optimal only in [0.084516,0.111321] SASRec and [0.083119,0.104379] GRU4Rec NDCG-equivalent shadow-cost units. **Not an observed operating cost**. Main retained Always Memory's superior absolute M3 accuracy and faster warmed DEV replay.

## G5 supplementary integration

The new S1–S10 source `SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md` (blob `9577203f26d260fc778e20be8fcd1ca22142dd40`) retains the entire original S1–S9 source as an unchanged prefix, and expands S10 from eight to **twelve** subsections (six S10 scientific tables). Added:
- S10.9 request-level switch decomposition, label zero-mass and corrected-S feasibility restriction.
- S10.10 paired Full-versus-Long fixed-source interaction, pre-outcome strata and zero-mass accounting.
- S10.11 hypothetical net-value frontier, actual calls and unavailable threshold uncertainty.
- S10.12 **only a 128-event late-DEV history-null feasibility pilot**: 63,619 co-active author-label swaps within one-hour completed pretarget bins, user and author activity marginals preserved, original B1/B2 F/S rank parity, non-floor null quality. It does not claim full-cohort causal relation identity specificity.

## Source and technical QA

- Current eight-section article: **11 tables, two figures, 56 unique labels**, no undefined `ref/eqref` and no missing BibTeX keys in static current-source scan.
- Current supplement: ten top-level S sections, twelve S10 subsections, **six captioned S10 tables**, original S1–S9 unchanged. All new data and intervals have corresponding SHA-verified public aggregates or original frozen B1/B2 reports.
- Original Twitch TEST (44,221 events), original frozen M3 TEST (47,575 author events), their multiplicity family and old author's supplementary S1–S9 have not been re-executed, retuned or overwritten.
- Retrospective offline target-retained S rankings are not passed as a deployable online candidate generator; five-by-four user-disjoint nested DEV is not a new forward-time TEST.
- Original `G5` manuscript QA artifact remains historically preserved. New builds are separately versioned.
- Initial S1–S10 Pandoc-to-LaTeX attempt failed because a newly introduced raw `\\[...\\]` math block was parsed incorrectly by the frozen Markdown configuration, leaving `\\mathbb` outside math mode. Source was corrected to Pandoc-supported `$$...$$` display math, with final 39-page PDF build and fatal-error guard **PASS** after an explicit inline-math correction. Earlier failed builds are archived as debug attempts, not accepted evidence.

## Scientific and ethical HOLDs

1. **R1 BOUNDED:** no verified unbiased sampled-metric correction; corrected-S explicitly omitted; earlier metric non-preservation and conditional expert selection are established prior art.
2. **R2 BOUNDED:** shadow price is a hypothetical NDCG-equivalent parameter; real marginal access cost and full-path advantage unverified.
3. **R3 BOUNDED:** paired same-cohort source interaction and non-floor history-null pilot do not identify whole-cohort relation-identity causality; whole-cohort time-safe null/full independent TEST not executed.
4. **Submission HOLD:** publisher-specific AI-assisted scientific code/writing disclosures require human verification; data license and privacy release rights, named authorship/CRediT, conflicts, funding, ethics and author sign-off remain open.

**Outcome:** proceed to G6 final PDF and academic claim check; preserve scientifically bounded decision-support contribution regardless of journal submission timing.

## G6 verified final PDF artifacts and current technical status

- **Main article:** GitHub Actions [#38391955348](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38391955348), SUCCESS; 36-page final PDF in [artifact 11809810243](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38391955348/artifacts/11809810243).
- **S1–S10 integrated supplementary:** GitHub Actions [#38392829047](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38392829047), SUCCESS; 39-page final PDF in [artifact 11810671665](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38392829047/artifacts/11810671665). Structure, mathematical symbol, 36-caption table and fatal-error checks PASS.
- Both artifacts are publisher-style previews, not evidence of author submissions or acceptance by KBS. Original frozen TEST, experimental sources, privacy restrictions and bounded scientific claims unchanged.

**G6 TECHNICAL QA PASS; SUBMISSION HOLD for accountable human author rights, statements, journal checklist, and any author-chosen further confirmatory/temporal experiment.**
