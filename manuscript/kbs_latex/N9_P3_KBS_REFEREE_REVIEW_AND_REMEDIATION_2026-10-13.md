# N9-P3 — Independent KBS-style manuscript review and remediation

**13 October 2026 | Status: EDITORIAL SCREENING COMPLETE; targeted corrections committed; full submission gate remains HOLD.**

Reviewed against the current eight-section article `main.tex`, assembled Supplementary S1–S10, frozen Twitch and M3 evidence, the post-G5 B1/B2/A1/A2 audits, and official journal/literature records. This is a *reviewer-style evidence audit* and not an assertion that KBS editors or independent human referees have evaluated the paper.

## 1. Editorial recommendation: major-revision quality control, not immediate submission

The KBS scope explicitly includes knowledge engineering, recommendation, and intelligent decision support; the article has a defensible **empirical knowledge-valuation-to-decision** question. Its novelty is **not a new Memory router**. The specific scientific chain now visible in the article is: (i) incumbent-relative conditional value of fixed historical evidence, (ii) candidate-regime sensitivity of the value supervision target, and (iii) decision consequences of candidate-aligned or mismatched supervision in held-out development users, with source-specificity diagnostics.

The paper remains vulnerable to three bounded research risks rather than editorial formatting alone. Text editing cannot transform exploratory DEV into independent confirmation, supply a missing real deployment cost, or identify causal historical source effects from a weak placebo. Submit only claims the evidence actually supports.

### R1 — Scientific differentiation of the decision-support contribution: BOUNDED

Known foundations: conditional expert allocation and two-stage regression deferral are covered by Mozannar and Sontag (ICML 2020), Mao, Mohri and Zhong (ICML 2024), and adaptive recommendation inference by DS-Frame (2026). Sampled candidate metrics can reverse algorithm comparisons (Krichene and Rendle, KDD 2020). The manuscript's incremental observation is that the candidate regime used **to supervise the fixed specialist's relative value** changes later specialist-choice quality **when both policies are evaluated on the same F author-ranking events**. B2 also shows historical-knowledge source order changes with F/S evaluation. This is a coherent applied empirical contribution, not a proof that the constituent theoretical concepts originated here.

**P3 revision performed:** strengthened the concluding Related Work synthesis to distinguish a matched knowledge-valuation-to-decision study from the individual prior art, avoiding universal priority claims. Cite primary literature rather than a sweeping first-of-kind assertion.

**Open:** no fully scored simple rank/score fusion alternative, no globally margin-preserving source placebo, and no genuinely new holdout; these delimit any claim of generalized scientific distinctiveness.

### R2 — Decision quality versus an operational reason to ration the specialist: BOUNDED

The frozen Twitch and M3 tests support performance of the specified relative-utility policy against selected decision objectives at observed natural calls. They do **not** verify a production cost saving. Unconditional Memory is stronger on M3 TEST, and the warmed replay finds it faster than the full gate path. A1's unrestricted DEV learned choice calls Memory on 99.91%/99.44% of cases and remains fractionally worse than Always Memory. A2 validates relative-increment targets against standalone difficulty/quality across 10%, 30%, and 50% inner limits but Direct and Two-stage are close, with unequal realized invocations.

**P3 verdict:** the scientific decision-support claim is defensible if expressly conditional on a stated invocation allocation requirement. No measured real-world scarcity, legal access restriction, serving-cost advantage or unconstrained optimality may be implied.

### R3 — Integrated importance and relationship knowledge specificity: BOUNDED

B1 and B2 strengthen the continuity from conditional utility to candidate alignment to knowledge selection. Both remain **post-G5 exploratory on the same 50,049-event/12,628-user M3 DEV cohort**; user-group-held-out outer folds do not establish a fresh temporal TEST. Sampled target retention is used **only** to construct retrospective labels; it is not a deployable generator. Long-only versus Full memory ranking reverses across F/S; Short-only contrasts have large Memory-call drift, popularity and shifted-history controls have near-zero decision floors, and the shifted placement does not preserve global user–author margins.

**P3 revision performed:** explicitly separated user-disjoint DEV generalization from chronological TEST in §5 and S10, and retained noncausal language for source/feature ablations.

**Open:** stronger margin-preserving historical control and independent prospective replication remain optional *claim-strengthening* work; their absence precludes causally strong generalization.

## 2. Source and inferential-tier quality gates

| Evidence source | Claim admitted in the main article | Statistical interpretation |
| --- | --- | --- |
| Twitch frozen TEST: 44,221 streamer events | Positive conditional recovery value and Utility gains at 6,650 calls | Original held-out inference; Difficulty/Oracle retrospectively TEST-count matched |
| M3 G5 TEST: 47,575 author events / 12,533 users | Utility vs specified DEV-frozen objectives across six Base fits; Always Memory remains strongest | Three primary comparisons Holm-corrected *within each Base fit*, not across 18 or independent samples |
| Original KuaiLive: 10,222 room events | Within-event sampled/full sign change and candidate/reference factorial accounting | Already examined retrospective comparisons, not new author-level decision TEST |
| B1/B2/A1/A2: 50,049 DEV author events / 12,628 users | Supervision-to-decision transfer; historical component dependence; budget frontier and decision-target controls | Post-G5 exploration; 5 outer × 4 inner group-disjoint folds; CIs descriptive, not in G5's preregistered family |

B1 F-aligned minus S-supervised outer NDCG@10: SASRec **+0.006159**, user 95% CI [0.004835,0.007543]; GRU4Rec **+0.004970**, CI [0.003550,0.006369]. Realized calls not exactly matched. No inference that three candidate regimes or multiple Base fits represent independent experimental populations.

## 3. Targeted P3 corrections completed in repository

1. **§2 distinction from prior theory strengthened:** the empirically investigated interface is candidate-indexed relative-knowledge supervision and downstream decision quality. This better supports the article's decision-support identity.
2. **§5 estimator difference disclosed:** original frozen TEST regressors used 200 boosting iterations whereas post-G5 nested B1/B2/A1/A2 development comparisons used 120. This avoids confusing differing protocols.
3. **§7 repetitive novelty defensiveness tightened:** removed an extra duplicate explanation of what the work does not claim while keeping the candidate-composition limitation.
4. **§5 and S10 temporal-boundary terminology corrected:** GroupKFold by user is not a new forward-time holdout.
5. **Supplement S10 polished:** mathematical symbols returned to inline math, analysis verbs moved from instructions to completed experimental Methods, exact read-only private-source hash audit recorded, and redundant provenance text shortened for layout.
6. **Reference metadata corrected:** Abbas and Hazen, *On the Value of Information Across Decision Problems*, `Decision Analysis` 22(1):1–13 is a **2025 issue article** (first published online August 2024); `kbs_references.bib` uses 2025.
7. **Preserved scientific evidence:** original S1–S9 remains unchanged as a prefix of the integrated supplement, and frozen G5 TEST, historical run records and statistical family were not regenerated.

## 4. Visual/PDF and citation review

The preceding successful main article preview contained **35 letter-size pages**, 11 tables and 2 figures. Its rendered first page, main results pages, discussion and conclusion show no major visible cropping or overlapping table content on inspected pages. A 3.47-point nonfatal overfull line in the context notation and minor underfull warnings remain editorial copyediting points, not evidence changes. The S1–S10 preview contained **38 pages** with 34 source captioned tables, including 5 landscape tables. Sampled pages and all S10 pages were visually inspected; their math and tables were rendered. The earlier S10 preview left a low-content final page. The redundant concluding provenance paragraph was tightened, subject to confirmation in the newest rebuilt PDF.

Static scrutiny of the prior P2 source found **56 unique labels with no unresolved internal label targets**, no missing BibTeX citation keys and no omitted S10 section/table labels. The new §2 and §5 edits are subject to the final updated CI rebuild check. This audit does not replace a proofreader's complete page-by-page judgment or external DOI verification of every citation.

Journal and literature sources:
- KBS official scope: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
- Relative deferral: https://proceedings.mlr.press/v119/mozannar20b.html ; https://proceedings.mlr.press/v235/mao24d.html
- Sampled ranking issues: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Direct KBS neighbor, MHGFCL: https://www.sciencedirect.com/science/article/pii/S0950705126004132
- Related path-evidence recommender, KAPER: https://www.sciencedirect.com/science/article/abs/pii/S0950705126009627
- Abbas/Hazen bibliographic record: https://pubsonline.informs.org/doi/10.1287/deca.2024.0187

## 5. P3 HOLD and acceptance conditions

- **Author-verified writing and research-code AI disclosures** under Elsevier's updated 2026 policy; the assistant cannot certify author oversight. See `N9_P3_AUTHOR_CONFIRMATIONS_AND_DISCLOSURE_DRAFT_2026-10-13.md`.
- **Data license and redistribution review:** original KuaiLive repository advertises CC BY-NC-SA 4.0; KuaiLive-M3's hosting dataset card advertises CC BY-SA 4.0. Verify licenses at the exact dataset release and distinguish downstream data access from code licensing. Do not publish private identifiers/checkpoints without rights.
- Confirm final source PDF build statuses and any new layout warnings; reconfirm exact bibliography/figure/table references in the latest commit.
- Resolve authorship, contribution, conflicts of interest, funding, consent/ethics where applicable, data/code availability language, and journal submission forms with accountable human authors.
- No fresh independent TEST is authorized or verified; strong generalization claims remain barred, and A2 rank-score fusion remains unexecuted without full per-candidate score vectors.
- P3 may be **TECHNICAL QA PASS** after latest builds; **SUBMISSION READY** requires all human approvals and an acceptable bounded contribution statement.

**Review recommendation:** continue with targeted, claim-bounded revision and author approvals; do not launch an algorithm-novelty project or claim the three academic risks have disappeared.

## 6. Final 2026-10-13 post-edit automated verification

The final eight-section main manuscript compiles successfully in [Actions #38385740136](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38385740136), PDF artifact **11805083249**. The final combined supplementary S1–S10 compiles in [Actions #38385758028](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38385758028), PDF artifact **11805871234**. Inspection of the latter PDF established **37 letter-size pages**, one page fewer than the earlier S10 preview after tightening duplicated source text. The paper's final main Git blob is `774cece1e35951c2d50af12ac398eb9f3bd3ff74`; final combined supplement Git blob is `60d6ccb319f0229218d91b656408505df2630e70`; bibliography blob is `30adb848df85cc1cb2e7a2d884afee376baf7841`.

The final source scan confirmed eight main sections, **11 tables and two figures**, **56 unique labels** with zero dangling `ref/eqref` keys, zero missing citation keys relative to the current BibTeX, ten supplemental sections, four S10 captions, and unchanged S1–S9 text prefix. The bibliography now records Abbas–Hazen in the correct 2025 volume issue. The after-edit `GroupKFold` versus forward-time-TEST distinction and the 120-versus-200-iteration estimator clarification are present in the main manuscript.

**Gate verdict: P3 TECHNICAL EDITORIAL QA PASS; scientific risk tier remains BOUNDED; publisher submission remains HOLD until accountable author declarations, rights checks and final human approval.**
