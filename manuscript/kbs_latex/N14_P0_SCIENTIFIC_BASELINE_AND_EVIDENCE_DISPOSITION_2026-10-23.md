# N14 P0 — Scientific baseline, complete evidence inventory and disposition register

**Date:** 2026-10-23
**Status:** SOURCE-LOCK AND SCOPE-CLASSIFICATION COMPLETE; NO SCIENTIFIC SOURCE EDIT OR NEW EXPERIMENT.
**Protected N13 parent:** commit `dd15b3ce1a9c6d0a7f34a542b5de10284767db04`; draft PR #7.
**Last proven same-source build:** Actions [#39883705990](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39883705990), on scientific-source commit `2b1620e3fc2b9f998209cc09cf6cc15ef3fe4be1`, both `main-paper` and `complete-supplement` succeeded.
**Main source blob:** `1467c5ae4fbda0135e822b00be0f7741c5129498`.
**Supplement source blob:** `778fa2cf8e584ffea83e2b56ccba4f6278455172`.
**Inherited CI:** N12 C7/C8V scientifically freezes original 11 Results tables (7 main, 4 relocated to Supplement S10.19), all core equations and exact method/claim words. These guards must remain active on N13 and may not simply be disabled to permit N14 restructuring.

## 1. New scope decision

N14's *only primary research question*:

**Does the candidate regime used to supervise the incumbent-relative value of a fixed historical relationship source affect the full-candidate ranking quality and allocation decisions of the resulting frozen selection policies?**

This is a complete-policy observational offline comparison, not a strict label-only causal experiment or matched-call optimization theorem.

- **Diagnostic premise:** Under the tested paired ranking context, sampled versus full-active candidate rosters change the realized Memory-minus-Base target. This phenomenon alone is not an original sampled-metric theorem.
- **Primary policy outcome:** On a separately frozen, same-period and event-ID-disjoint additional M3 author-ranking evaluation, the two learned complete policies differ in weighted full-candidate NDCG@10 and naturally realized Memory calls.
- **Interpretive trace:** Request-level DEV allocation accounting shows which 50,049 requests change the use of the same specialist. It is exploratory, algebraic accounting, and cannot mediate or independently confirm the separate additional-target result.
- **Guardrails, not contributions:** Always Memory accuracy advantage, call-rate inequality, legacy timing disadvantage, corrected-S untested alternative, label/exposure limits and restricted-data availability.
- **Excluded parallel RQ:** Authentic-history versus constrained-null source validity (H2), including its unresolved original acceptance subgate. It remains recorded in the complete research archive and Holm family, but no longer constitutes a paper-level research question.

## 2. Complete current science-family disposition

The entries below consolidate the project results relevant to N14, rather than treating every existing file as a new independent dataset. Disposition codes: `CORE` = main-text result; `DIAGNOSTIC` = brief supporting context; `INTERPRETATION` = descriptive policy accounting; `BOUNDARY` = adverse or necessary scientific qualification; `ARCHIVE` = retain exact project provenance outside the new main narrative; `NOT_ELIGIBLE` = scientifically unadmitted, unrun or unsupported method/data path.

| ID | Evidence and analysis population | Grounded result and evidence status | N14 disposition | Scientific owner / required preservation |
|---|---|---|---|---|
| D1 | KuaiLive Room 10,222 paired previously examined TEST events, same frozen checkpoint pair | Memory−Base sampled-active −0.04120; full-active +0.04631; within-pair change +0.08751 (membership +0.08827; reference normalization −0.00076). Candidate identity, competition and membership shift jointly; retrospective diagnostic. | `DIAGNOSTIC` 1 compact figure or paragraph; no isolated candidate-count causality | `tab:results-factorial`; Supplement S5; `SECTION6_STAGE3_P2_RESULTS_2026-10-10.md`; original full provenance remains archived |
| D2 | Twitch/LiveRec streamer TEST, 44,221 requests | Base 0.58211; Always Memory 0.53980; frozen Utility 0.58983 at 6,650 calls (~15.04%); hindsight history-state complementarity, not pretarget state. | `ARCHIVE`; not a separate N14 contribution | `tab:results-twitch-policy`; Supplement S3/S6/S7 and historical S10.19; preserve one-shot TEST record |
| D3 | Original KuaiLive M3 author-ranking TEST, 47,575 events / 12,533 users; 6 Base fits share same cohort | SASRec/GRU4Rec models with three seeds; Always Memory 0.34679, primary SAS Base 0.25800, Utility ~0.30287, invocation ~29%; 6 fits are not six independent tests. | `BOUNDARY` very compact model provenance / specialist reference; full frozen Utility and robustness results `ARCHIVE` | `tab:results-m3-policy`, `tab:results-m3-robustness`; Supplement S8 |
| D4 | M3 full-active DEV, 50,049 requests / 12,628 users | S/F supervision/transfer: SAS weighted/unweighted DEV policy NDCG 0.296499/0.302658 (F−S +0.006159); GRU 0.298123/0.303093 (+0.004970). Same exploratory DEV source; not a new held-out confirmation. | `INTERPRETATION`; do not foreground DEV p-values as independent new evidence | `N12_C6_RQ2_SUPERVISION_TO_DECISION_EVIDENCE_CHAIN_2026-10-19.md`; Supplement S10.14 |
| D5 | Same 50,049 DEV request trace, two Base families | Policy decisions disagree on 10,672/50,049 (21.32%) SAS and 11,517/50,049 (23.01%) GRU. F-only/S-only: SAS 5,350/5,322, GRU 5,639/5,878. Mean incremental value newly called versus displaced: SAS 0.133417 vs 0.076194; GRU 0.126600 vs 0.079135; both means positive. | `INTERPRETATION`; descriptive reallocation, not causal mediation and not proportion of calls | G2 decision switches public aggregates; Supplement S10.14 |
| P1 | Additional KuaiLive M3 author targets, 30,000 requests / 10,387 users; 2026-03-27 to 2026-03-31 source period; 20 date×pretarget-history cells | Same-period, event-ID-disjoint from original M3 TEST but not independent user/time cohort. Frozen S-policy from uncorrected target-retained 575-candidate labels versus F-policy from full-candidate labels, evaluated on same full-active candidates. | `CORE` sole primary frozen policy outcome | `tab:results-m3-b4a-supervision`; B4-A A4 #38518785650 and A5 #38519174441; `N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md` |
| P2 | Same additional 30k, weighted full-ranking NDCG@10 | SAS S 0.300055, F 0.305446, F−S +0.005391, paired user CI [0.003646,0.007174], Holm p 0.000600; GRU S 0.300945, F 0.304530, F−S +0.003585, CI [0.001599,0.005576], Holm p 0.000800. 5,000 user-cluster bootstraps/sign randomizations as frozen source. | `CORE` preserve exactly; not re-estimate after restructuring | B4-A A4/A5 signed aggregate, current `tab:results-m3-b4a-supervision` |
| P3 | Same additional 30k, separately frozen fitted policies | Unweighted Memory calls: SAS F/S 8,704/9,105, rates 29.013%/30.350%; GRU 8,629/9,168, 28.763%/30.560%. Population-weighted rates SAS 29.203%/30.537%, GRU 29.008%/30.809%. Actual gaps 1.337 and 1.797 unweighted percentage points exceed ~1pp near-equal-call original tolerance. | `CORE` resource estimand co-reported with ranking; **not** equal-resource/label-only effect | B4-A H1, Supplement S10.9; preserve distinction of weighted and raw calls |
| P4 | Same additional 30k Always Base/Always Memory | Always Memory 0.348744 weighted F NDCG exceeds F policies 0.305446 and 0.304530 (Always Base SAS 0.259307, GRU 0.260058). | `BOUNDARY` co-locate with primary table, prevent unrestricted-accuracy superiority claim | B4-A H1 |
| H1 | Additional 4,096 targets / 3,059 users nested within the above 30k, one cohort with three null random seeds | Authentic Full Memory 0.334942 vs average constrained null 0.303797; difference +0.031145, CI [0.027389,0.035098], Holm p 0.000600; constrained rewiring jointly alters multiple relation features. The cohort-specific TRAIN-only Popularity pre-reveal acceptance subgate was **NOT VERIFIED**. | `ARCHIVE` parallel research line; disclose in original 3-hypothesis family and preserve scientific shortfall, do not use as mediation | `tab:results-m3-additional-relation-identity`; Supplement S10.15–S10.19; B4-A H2 and A5; original pre-reveal record |
| I1 | Historical-component and candidate-regime sensitivity, M3 DEV | DEV S Long-only 0.773602 vs Full 0.668498; F Full 0.343509 vs Long-only 0.333231; component/source interactions descriptive and not source-causal isolation. | `ARCHIVE` (possibly single no-new-RQ footnote only if logically necessary) | S4, S10.10–S10.16; N9 source interaction reports |
| A1 | DEV model/objective and allocation controls | Direct/Two-stage/Difficulty/Specialist Quality, feature-family ablations, 8 budget values, gate compression models. Different folds and realized call rates prohibit treating every row as same-call new confirmation. | `ARCHIVE`; optionally brief comparator rationale | Supplement S7, S10.7, S9; N9 A1/A2 and original outputs |
| C1 | Original M3 SASRec 256 DEV requests×3 counterbalanced RTX 3090 replays, original pointwise Utility, not newer vectorized F selector | Utility mean 1.76941 ms/event versus Always Memory 0.69165 and Base 0.72759; production end-to-end, monetary savings and new F-path timing unmeasured. | `BOUNDARY` short adverse fact, complete methods/results `ARCHIVE` | `tab:results-n10-cost`; Supplement S10.17; N10-C2B |
| C2 | Older separate 256-request single-pass DEV replay | Base/Memory/Utility 1.4245/0.8033/1.8018 ms; not identical to C1, should not pool or average. | `ARCHIVE` distinct experiment | Supplement S9.6 |
| N1 | V2a/NI1b–g sampled-only correction/identifiability studies | Toy improvements, assumptions and synthetic checks completed; **NI1g NO-GO** for scientifically accepted real sampled-only corrected-S selector; V2b not run by design. Cannot claim all corrected S are invalid. | `BOUNDARY` competitor **not excluded**, no new trained-policy result | `NI1G_CORRECTED_S_METHOD_GATE_2026-10-20.md`; `N12_C8V_REV2_V2A_FINAL_METHOD_GATE_AND_V2B_STOP_2026-10-19.md` |
| N2 | Public KuaiRec Big→Small true-file feasibility audit | Real metadata audited; stringent historical author prehistory thin (7/1,411 user records with repeat author under the audited optimistic filter); **preselected new-experiment path NO-GO**. KuaiRand support not verified. | `NOT_ELIGIBLE` for any claim of new independent replication | `REV3_1_X0B_REAL_KUAIREC_FEASIBILITY_GATE_VERDICT_2026-10-20.md` |
| N3 | Other historical exposure/negative-click and component-null studies | Some feasibility, repair and DEV placebo tests exist; limited exposure support, non-causal source intervention, not a distinct one-shot modern external TEST. | `ARCHIVE` no proposal to rebrand as new confirmatory evidence | Supplement S4–S6/S10 and N9 source reports |

## 3. Prespecified testing-family integrity and secondary-results obligations

**Never retroactively redefine original multiplicity because N14 removes H2 as a main-text RQ.** B4-A contains exactly **three original prereveal directional contrasts**: two F-vs-S policy outcomes (SASRec and GRU4Rec) plus the authentic-vs-constrained-history H2 contrast. Report the original Holm-adjusted p-values and document all three tests and the H2 **NOT VERIFIED** subgate in accessible Supplement/archive provenance, even if only two H1 comparisons are headline results. No unannounced recomputed two-test Holm p-values.

**No silent deletion / selective concealment:** The original 11 Results source tables, 7 original main plus 4 originally migrated to S10.19, are frozen by `analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json` and scientific integrity fixtures. N13 remains the literal complete-table archive. N14 may move exact frozen source results to an explicitly labeled complete research archive and make the journal Supplement one-question-specific; either location must be findable, referenced and accompanied by limitations. A different journal Supplement scope is not permission to fabricate another preregistration.

## 4. Reproducibility and publication-rights status

- Public code, hashes and aggregate science-contract verification are auditable; independent end-to-end rerun of every restricted event-level source from scratch is **NOT established**.
- Raw KuaiLive releases, processed source identity, derived events, model checkpoints and public redistribution rights require **responsible-author verification**, not blanket assumed permission. See `N12_C7_CLAIM_SOURCE_REPRODUCIBILITY_AND_RIGHTS_REGISTER_2026-10-19.md`.
- Generative-AI drafting/restructuring activity needs verified human-author declaration under Elsevier's updated June 2026 policy; any AI-as-method activity has separate reproducibility/disclosure implications. No signature, author metadata or data-rights statement is supplied by this P0 report.
- Current N14 P0/P1 may only add research-planning and provenance documentation. It **must not** modify `main.tex`, Supplement, frozen tables, thresholds, scientific code, private data or PR #7.

## 5. P0 acceptance checklist

- [x] N13 science source, supplement blob, actual CI-success commit and 11-table invariant identified.
- [x] Every major original science family is assigned to CORE/DIAGNOSTIC/INTERPRETATION/BOUNDARY/ARCHIVE/NOT_ELIGIBLE.
- [x] Original Holm family, H2 unreconciled control and corrected-S/Kuairec NO-GO recorded without upgrading evidence.
- [x] Publisher/rights/AI author checks expressly left unresolved.
- [ ] No main-paper tables moved until N14-specific frozen-content and archive equivalence checks are ready (P2–P6).
