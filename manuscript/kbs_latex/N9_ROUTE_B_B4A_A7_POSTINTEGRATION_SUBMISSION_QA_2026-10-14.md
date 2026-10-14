# B4-A A7 | Post-integration submission QA and evidence lock

Date: 2026-10-14. Status: **TECHNICAL QA PASS; SCIENTIFIC CLAIMS BOUNDED; HUMAN KBS SUBMISSION SIGNOFF PENDING.**

## One-shot completed evidence

- B4-A A0/A1: 4,723,652 residual eligible source events; label-blind frozen 30,000 previously unevaluated ranking target event IDs (10,387 users), with nested 4,096 targets (3,059 users). Zero intersection with 47,575 previously scored G5 target IDs. **Same March 27–31 2026 source recording interval, not an independent new future period or fully unseen source.**
- A2: four DEV-only fixed HGB gate models and original eligible-population 20-cell poststratified estimands. A3: before target labels, locked Base/Full Memory Top-10, frozen F/S decisions and all three H2 relation-null Top-10. Sources: [H1 action #38517170015](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38517170015), [H2 action #38517502835](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38517502835), [independent prereveal #38518563975](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38518563975).
- A4 first-and-only successful [one-shot unseal #38518785650](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38518785650): SASRec F-minus-S +0.005391, CI [+0.003646,+0.007174], Holm p 0.000600; GRU4Rec +0.003585, CI [+0.001599,+0.005576], Holm p 0.000800; authentic relation history minus three-null eventwise mean +0.031145, CI [+0.027389,+0.035098], Holm p 0.000600. Original 20-cell eligible-population weights; 5k user-cluster CI draws and three precommitted tests. [Independent A5 reconstruction #38519174441](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38519174441) reproduces the frozen means from SHA-verified paired event metrics.
- A6 scientific verdict in N9_ROUTE_B_B4A_A6_REFEREE_RISK_ADJUDICATION_2026-10-14.md: R1 materially strengthened but novelty/editorial scope bounded; R2 deployment business case **NOT PROVEN**; R3 additional same-period fixed-target evidence strong but external temporal generalization and microscopic causal mechanism bounded. Neither original G5 nor earlier DEV test families were retrospectively refitted.

## Essential unfavorable or incomplete findings

- SASRec F versus S calls: 8,704 versus 9,105 (1.337 pp different). GRU4Rec: 8,629 versus 9,168 (1.797 pp). Both exceed the predeclared 1 pp approximate equality threshold; not a strict equal-budget treatment.
- Always Memory NDCG 0.348744 exceeds both selective F policies (0.305446/0.304530); measured deployment cost or latency reduction over unconditional Memory has not been established.
- The H2 controls retain >1,900 top-ten positives and 0.302796–0.304689 full-F weighted NDCG with ~76.8% history changes, but the predeclared same-cohort TRAIN-popularity-only **nonfloor gap was not scored before A4**. Complete original nonfloor certification is **NOT VERIFIED**; do not repair it by post-result tuning.
- Three null seeds are randomized source histories for the **same** 4,096 requests, not independent sampled cohorts. Their creator-history permutations also alter repeat pairs and higher-order patterns.

## A7 current paper/supplement QA completed

- Revised eight-section main.tex integrates B4-A in Abstract, Experimental Setup, Results, Discussion and Conclusions without removing Always Memory or changing frozen G5 claims.
- Integrated SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md now has **S10.15** (same-period additional-target supervision) and **S10.16** (historical-source null and limits), plus tables S10.9/S10.10. The previous missing supplement-reference gap is closed.
- A7 PDF Actions [#38523544564](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38523544564) had **both jobs SUCCESS**. Main PDF is **40 US-letter pages**; supplementary PDF **44 pages**. Cross-source B4-A numerical assertions, original S1–S10 top-level structure, all S10.1–S10.16 subsections, new table claims, CI LaTeX logs, and PDF text extraction passed.
- Full-page render review inspected the new manuscript supervision table, null paragraph and supplementary S10.15/S10.16 layout. S10.14's formerly clipped raw code paths were replaced by short linked source names; final supplement LaTeX log contains no overfull box warnings. Text includes explicit missing nonfloor diagnostic and unequal call rates.
- GitHub artifacts: main **11874448417** and supplement **11875151972**; both attached to the successful A7 workflow, not newly generated TEST metrics. The PDFs are publication-preview files, not yet submitted copies.

## Remaining author/editor decisions (not new computational experiments)

Confirm author order and affiliations, complete CRediT/AI-assistance/COI/funding/data-rights and ethics declarations as applicable, and check final KBS template/journal formatting, exact references and cover letter. Confirm permission before distributing any private derived interaction files; the metadata discrepancy was **not** used to halt already permitted internal B4-A scientific execution. The draft pull request remains unmerged, and KBS submission is not claimed complete.

No new A4 run, target reveal, sample/model/threshold change, or new population inference is authorized by this QA document.
