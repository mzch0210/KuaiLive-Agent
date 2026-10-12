# R2 — Experimental Setup integration: manuscript and PDF acceptance

**Date:** 2026-10-12. **Gate:** R2 PASS for Section 5; overall eight-section manuscript NOT yet submission-ready. R3–R8 remain. The frozen model, G0F/G5 TEST result files and S1–S9 were not edited.

## Accepted source and reproducible build

- [Main source](main.tex) GitHub blob SHA: a78dc243669c9b7741be5b977e9dcb80deb082ab.
- [Bibliography](kbs_references.bib) SHA: 1f1486382439069b6cdae64d9e1738b696c64a6a; verified Holm (1979), Scandinavian Journal of Statistics 6(2):65–70, DOI 10.2307/4615733, added.
- R2 final scientific source commit: c6dd65aeb0d1b990a6206dcecc4d36f2ac192de3.
- [GitHub Actions final LaTeX build #38235478501](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38235478501) **SUCCESS**; artifact 11740318869, compiled PDF and logs. PDF: **31 pages**, 457,615 bytes, preprint Letter format; NOT a finished KBS submission artifact. Final log has **zero overfull hbox warnings**, zero undefined citations/references found. Earlier 18.49pt table and 15.48pt inline math overflows corrected; actual PDF pages 12–14 visually inspected.
- Static source verification: all five Section 5 subsection headers, two method/protocol tables, unchanged original KuaiLive D_i/A_C/A_R equations, zero unmatched section crossrefs, zero missing citation keys and zero duplicated labels.

## Scientific revisions actually performed

**§5.1, task and dataset identity.** Three separate protocols now distinguish frozen Twitch available-streamer TEST (46,878 DEV / 44,221 TEST); original KuaiLive live-room same-event 575 sampled-active vs full-active retrospective pair (10,222 targets); and new later-period KuaiLive-M3 **author** ranking (24,995,148 indexed TRAIN, 50,049 DEV, **47,575 frozen TEST, 12,533 users**). M3 full-active TEST candidate count median **31,065** eligible authors; M3's 4,096 × 575-author DEV checkpoint screening is stated to be different from the full-active experiment and old 575-room C2 candidate regime.

**§5.2, baselines and compared methods.** Preserves old KuaiLive Dual-ID base and official Twitch LiveRec; adds M3 SASRec + GRU4Rec × training seeds 20261012, 20261013, 20261014 and separately scored fixed historical relationship Memory. Twitch has **14 pre-outcome features**. M3 has **12** (five Base-score and seven shared history/roster descriptors). Supervised Utility / Difficulty / Specialist Quality objectives and heuristic Uncertainty / History each use frozen DEV pointwise selection thresholds; Twitch Difficulty and hindsight Oracle still use *retrospectively TEST-count-matched* allocations. The compared-method table now distinguishes all types.

**§5.3, training and freeze.** M3 user-group-disjoint 5-fold OOF on the 50,049 full-active DEV events; each of five objectives maximizes DEV selected gain under an at-most-30% **DEV** invocation constraint and freeze pointwise threshold. No TEST retuning or enforced equal/hard TEST rate. M3 history uses strictly previous TRAIN/DEV/earlier TEST interactions in a documented **prequential** setting; target-blind rank/gate decisions are frozen before current TEST label scoring. Exact same old KuaiLive paired candidate membership/reference algebra is retained.

**§5.4, inference.** Distinguishes original Twitch 5,000 paired resamples, original KuaiLive 3,000 paired user resamples, and new M3 5,000 paired **user-cluster** bootstrap CIs plus 5,000 user-cluster sign flips under a sign-symmetry assumption. M3 preregistered one-sided Utility vs (Always Base, Difficulty, Specialist) contrasts are Holm-corrected **within each of six model/seed triples**; no global familywise 18-comparison error control is claimed. Uncertainty is secondary; six fits share the same TEST user cohort.

**§5.5, implementation.** Separates old Dual-ID 50-history Base, Twitch input context16, M3 author SASRec/GRU4Rec 64-dimensional/context16 implementation. Notes protocol-specific deterministic score ties and source cohort sampling hash implementation variance, details to S1–S2 in R6. Invocation fraction is not proven latency saving.

## R0 twelve-issue closure schedule

See detailed [machine-readable 12-issue tracker](R2_R0_P0_P1_ISSUE_CLOSURE_TRACKER_2026-10-12.json). Stage **first correction** and **full paper issue closure** are distinct:

| R0 issue | First action in R2 | Residual editing stage |
|---|---|---|
| P0-01 old two-task framing | §5 now has three task-specific protocols | R5 Introduction, Discussion, Conclusion; R8 |
| P0-02 sole Twitch frozen TEST statement | §5 distinguishes Twitch and five M3 DEV-frozen policies | R3 Results; R6 supplements; R8 |
| P0-03 false equal TEST call budget | §5 separates DEV optimization cap and realized TEST rate | R3 result rate table; R4 formulation; R8 |
| P0-04 M3 Always Memory/cost counterevidence omitted | Methods state call rate is not elapsed cost | **R3 §6.5**, R5 §7, R6 S9 |
| P0-05 ranked room/author units, 14/12 features, 575 screening | §5 complete methodological identity correction | R4 Framework, R6 S1–S3; R8 |
| P0-06 incorrect inference family and multi-seed independence | §5 corrects user clusters, three-Holm per fit, same cohort | R3 quantitative TEST tables; R6 S8; R8 |
| P1-01 G0F hash description vs implementation | §5 records source rule and discrepancy | R6 S1, R8 |
| P1-02 differing historical tie tolerance | §5 discloses protocol-specific conventions | R6 S2, R8 |
| P1-03 out-of-date S1–S9 Twitch-only scope | No supplement changes in R2 | **R6**, R8 |
| P1-04 distinction from L2D and KBS knowledge gating | R1 has literature-gap blueprint | **R5 §2/§7; R7** novelty review |
| P1-05 old stage reports saying TEST not run | Completed G5 is authoritative | **R6** current result index, R8 |
| P1-06 expiring Actions artifacts | Exact original hashes and URLs preserved | **R6/R8** privacy-safe reproducible archival material |

**No 12-issue paper-wide R0 ticket is prematurely marked CLOSED**, because other main sections and S1–S9 still use the pre-M3 evidence structure. R8 performs final global closure.

## R2 submission-readiness gate

- **R2 PASS:** Section 5 formal methods and statistics are coherent; all three ranked tasks, five frozen M3 gates and true invocation-rate semantics have been written; old paired room formulas preserved; Bib and PDF compile; no overfull boxes after PDF correction.
- **Overall HOLD:** Current §1/§3–4/§6–8, full supplementary S1–S9, and Abstract/declarations require future stages. New PDF has grown from 29 to 31 pages before R3–R6 de-duplication.
- **Next R3:** Results must add independent M3 frozen TEST (including actual calls and Always Memory), separate original candidate regime, six fitted Base robustness, all primary inferential scopes and unfavorable warmed cost, while replacing rather than appending old results.
