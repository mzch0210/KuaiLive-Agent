# N10 Route C | C0/C1 execution status

Date: 2026-10-14. Research branch: kbs-n10-route-c-c0-c1-20261014 (based on frozen B4-A A7 PR #3).
**C0 PASS; C1 near-neighbor verification, positioning matrix and BibTeX PASS; C2-A PUBLIC DEV ARCHIVED FRONTIER VERIFIED; C2-B FULL-PATH BENCHMARK NOT STARTED.**

## C0 — passed read-only public evidence validation

- Source audit script: analysis/kbs_plan_c/n10_c0_public_freeze_audit.py. It validates the exact Git blob SHA of nine frozen public G5/B4-A A0/A1/A2/A4/A5/A6/A7 evidence sources; initial C0 separately verifies the two unchanged A7 manuscript blobs. The mutable later C5 paper text is not treated as an immutable original experiment artifact.
- Verifies original G5 47,575 target events; residual eligible 4,723,652; frozen new same-period 30,000 main/10,387 users and nested 4,096/3,059; zero overlap with original evaluated G5 target IDs, without wrongly calling them new-period TEST or user-disjoint. A2 models and DEV 50,049/12,628 user-disjoint OOF freeze, 20-cell natural population weights and Kish ESS confirmed.
- Protected B4-A results: SASRec F−S +0.005391 (95% CI [0.003646,0.007174], Holm p 0.000600), GRU4Rec +0.003585 ([0.001599,0.005576], p 0.000800), authentic history minus mean of three nulls +0.031145 ([0.027389,0.035098], p 0.000600).
- Required adverse results: F and S Memory calls SAS 8,704 versus 9,105, GRU 8,629 versus 9,168; realized call rates differ >1 pp. Always Memory weighted NDCG 0.348744 exceeds two F policy NDCGs 0.305446/0.304530. B4-A same-cohort TRAIN-popularity floor remains **NOT VERIFIED AS PREDECLARED**.
- Original source lock action #38517170015, H2 SHA action #38517502835, independent prereveal #38518563975, first and only successful A4 #38518785650, independent A5 #38519174441 and manuscript/supplement action #38523544564 are linked by evidence register. All C0 execution is public-only, does not access private target labels/rows, fit gates, or score A4.
- [Initial C0 frozen source + tests #38528489454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38528489454) **SUCCESS**. [Extended C0+C1 bibliography tests #38528837682](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38528837682) **SUCCESS**.

## C1 — completed positioning and bibliographic work

- Publisher confirms Zhong et al. (2026) *Scene-aware memory discrimination: Deciding which personal knowledge stays*, Knowledge-Based Systems 338:115496, DOI 10.1016/j.knosys.2026.115496. Its task prioritizes personal interactions to **record/retain** according to scene; it also evaluates downstream personalization, so conditional memory usefulness per se is not new. The six publisher-confirmed author names and DOI are now a unique BibTeX key zhong2026samd in kbs_references.bib.
- Publisher confirms Xie et al. (2026) *Fusing multi-head gating and focused-view contrastive learning for knowledge-aware recommendation*, KBS 341:115673, DOI 10.1016/j.knosys.2026.115673. Its research is adaptive knowledge-graph multi-view feature fusion, not incumbent-relative downstream use of a fixed specialist.
- Institutionally verified Yuan et al. *Recommender System as Slow and Fast Thinkers* is **accepted CIKM 2026** and available as arXiv:2609.02671; it is not a KBS paper. Its adaptive inference routing is a strong antecedent.
- Krichene/Rendle (KDD 2020) established sampled-metric inconsistency; expert delegation has established learning-to-defer foundations. No sampled-metric theorem or general gating algorithm is claimed as new.
- Detailed literature matrix, P1/P2/P3 falsifiable contributions and Intro/Related Work draft: manuscript/kbs_latex/N10_C1_KBS_NOVELTY_BOUNDARY_MATRIX_2026-10-14.md. The manuscript body is **not yet edited**; this stage has inserted the verified new BibTeX entry only. Actual in-text SAMD citation and prose go into C5 after C2/C3 result adjudication.

## C2 readiness — source audit only, no new GPU experiment

- Existing measured negative cost evidence: experiments/kbs_plan_c/G4_EXTRA_SEED_FULL_ACTIVE_DEV_GATE_AND_COST_RESULTS_2026-10-12.md and analysis/kbs_plan_c/g4_latency_dev_replay.py. RTX3090 warmed 256 DEV requests: Always Base mean 1.4245 ms, Always Memory 0.8033 ms, Utility selection 1.8018 ms. These microbenchmarks exclude historic state construction, roster IO, production networking and queueing; do not assert live-serving efficiency.
- Existing N9_G1_E2_SHADOW_PRICE_ENVELOPE_PUBLIC_AGGREGATE_2026-10-13.json represents DEV-only idealized policy frontiers at zero gate overhead. Shadow lambda is expected NDCG per specialist call, neither real money nor elapsed ms.
- Next actionable C2-A task: verify and plot DEV-only natural call/quality frontier from frozen public aggregate. C2-B: benchmark full DEV system paths under matched hardware, candidate sets, time state, warm/cold cache and counterbalanced order, reporting mean/p50/p95 and shared vs avoidable work. No TEST label reread/retuning allowed. If Memory remains both more accurate and faster, R2 deployability must remain bounded.

## C2-A — public DEV source-only execution completed

- Reconstructed frozen public policy data (Git blob SHA 047411dfd4b6554e0601c60bf5787dac249da7c3) using analysis/kbs_plan_c/n10_c2a_public_dev_frontier.py; [GitHub Actions #38529277271](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38529277271) SUCCESS.
- SASRec: fixed max-30%-inner DEV policy 15,016/50,049 calls (30.0026%); F NDCG 0.302658 vs Always Memory 0.343509, quality gap 0.040851. Its direct idealized break-even shadow price relative to Always Memory is 0.058361 NDCG per avoided Memory call.
- GRU4Rec: 14,762/50,049 calls (29.4951%); F NDCG 0.303093 vs Always Memory 0.343509, gap 0.040416. Direct break-even is 0.057324 NDCG per avoided call.
- The optimized frontier of *all* recorded policies has additional switching points. The 30%-inner policy is the estimated archived upper-envelope optimum only within selected shadow-price ranges (SASRec 0.084516–0.111321; GRU4Rec 0.083119–0.104379). These lambda units are **hypothetical NDCG per call**, NOT monetary saving, milliseconds, or a measured production latency.
- Source HGB policy definitions/candidates are DEV-only and the fixed public summary assumes **zero incremental gate overhead**. The earlier G4 256-event warmed real execution had selective 1.8018 ms vs Always Memory 0.8033 ms. Hence no real cost dominance is claimed. This C2-A action did not train or recalibrate gates, use an outcome from a newly evaluated TEST request, or touch the frozen A4 data.
- Next C2-B must explicitly include gate and shared computation overhead, compare matched request/candidate histories across all routes, and report p50/p95/cold/warm. If complete path costs remain unfavorable, limit R2 to a clearly externally justified invocation cap.

## Overall gates

| Stage | Status |
| --- | --- |
| C0 frozen public evidence and leakage guard | PASS |
| C1 near-neighbor references, P1/P2/P3 positioning, draft | PASS_FOR_C2 (body integration pending C5) |
| C2-A public-only frozen DEV budget/call-quality audit | PASS, source CI #38529277271 |
| C2-B matched full-path DEV efficiency | NEXT; no new execution measured |
| C3 negative/null condition audit | NOT RUN |
| C4 scientific adjudication | NOT RUN |
| C5 integration of revised main and supplement | NOT RUN |
| C6 final referee and KBS PDF QA | NOT RUN |

KBS submission and the corresponding pull request remain under review. No repeated A4 execution or private derived relationship disclosure.
