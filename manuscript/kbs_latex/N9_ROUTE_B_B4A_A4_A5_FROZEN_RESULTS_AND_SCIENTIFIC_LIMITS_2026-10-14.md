# B4-A A4/A5 | Frozen same-period held-out target confirmation: complete findings

**2026-10-14 | A4 PASS one-shot; A5 PASS independent numerical reconstruction; PRELIMINARY SCIENTIFIC REVIEW, not yet submission approval.**

## Source and verification status

- Frozen main 30,000 request targets / 10,387 users; H2 nested 4,096 / 3,059 users. Same March 27–31, 2026 M3 TEST-source collection interval as original G5, with **zero overlap in selected target event IDs** but not necessarily user-disjointness and not new chronological data.
- A1 SHA main be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14; H2 40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059.
- A3 completely sealed predictions and all null Top-10 before A4. Source parity #38516927128, H1 #38517170015, H2/final A3 lock #38517502835, independent prereveal #38518563975 all SUCCESS. A4 first/only outcome unseal [#38518785650](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38518785650) SUCCESS, 2026-10-14. No subsequent model/threshold/sample/seed tuning.
- A5 independent reconstruction [#38519174441](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38519174441) SUCCESS; complete SHA of the private A4 paired metrics verified; three weighted means reconstruct A4 values to numerical precision. Supplementary per-source-date and source-validity aggregates [#38519266946](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38519266946) SUCCESS.
- Primary estimand: natural eligible residual TEST-source request population mean, 20 date × pretarget-history-quartile poststratification cells, frozen weights N_cell/n_cell. 5,000 user-cluster paired bootstrap draws, 5,000 user-cluster sign randomizations (conditional on user-cluster sign symmetry), Holm familywise adjustment across the EXACT three preregistered directional contrasts. Equal-cell averages or daily analyses are not independent primary findings.

## H1 — downstream candidate-supervision alignment at full-active F

| Fixed Base (seed 20261012) | S-aligned weighted F NDCG@10 | F-aligned weighted F NDCG@10 | Paired F−S | User-cluster 95% CI | Holm p |
| --- | ---: | ---: | ---: | --- | ---: |
| SASRec | 0.300055 | **0.305446** | **+0.005391** | [0.003646, 0.007174] | 0.000600 |
| GRU4Rec | 0.300945 | **0.304530** | **+0.003585** | [0.001599, 0.005576] | 0.000800 |

- Baselines: Always Base SASRec 0.259307, GRU4Rec 0.260058; fixed Always Memory **0.348744** weighted F NDCG@10 on the 30k, higher than both constrained gates.
- **Realized, not retrospectively equalized, unweighted Memory calls**: SASRec F=8,704/30,000 (29.013%) versus S=9,105 (30.350%), gap 1.337 percentage points; GRU F=8,629 (28.763%) versus S=9,168 (30.560%), gap 1.797 pp. F-aligned makes **401 / 539 fewer calls** and higher weighted ranking accuracy in these fixed policies, but this is NOT a strict equal-count intervention. Weighted realized fractions SAS F 29.203% vs S 30.537%, GRU F 29.008% vs S 30.809%.
- In all five source-date descriptive groups SAS/GRU F−S effects were positive (SAS range approximately +0.00122...+0.00734; GRU +0.00124...+0.00467). Five dates in the SAME data and shared users are not five independently sampled external tests.
- The S-aligned strategy's retrospective DEV supervision used target-retained 575-author S labels. At new TEST time both policies used identical full-F pre-outcome descriptors and full-F candidate rosters; this is a **supervision alignment** result, NOT superior generic gating architecture or equal training label information.

## H2 — original relation-history arrangement under unchanged F candidates

- Frozen real Full Memory weighted F NDCG@10 **0.334942** on the 4,096 nested targets; three pre-registered null values (seeds 20261014/15/16): 0.303905, 0.304689, 0.302796. Per-request average-null value 0.303797. **Original minus average null +0.031145**, 95% user-cluster CI **[+0.027389,+0.035098]**, Holm p **0.000600**.
- Three nulls use the SAME 4,096 requests, user histories and F roster, not independent samples; source author-hour activity and per-user source event times held fixed, swaps only activate after their historical source hour closes. Approximately **76.78–76.80% of relevant historical edges rewired**, disrupting repeated pairs and higher-order structure.
- A5 nonfloor indicators PASS for each null: F NDCG above both 0.10 and 30% of original F; 1,903–1,913 null Top-10 positive cases; source-history rewiring above 10%. **However, the predeclared margin above the fixed TRAIN-popularity benchmark was not scored/sealed for these added targets and cannot be certified retrospectively without violating the one-shot discipline. This nonfloor subgate remains NOT VERIFIED.** Accordingly, do not claim all placebo acceptance diagnostics are fully established; this limits the maximal mechanism-strength wording.
- Within each of five source dates, the descriptive real-minus-average-null weighted effect is positive (approximately +0.0274...+0.0367). Not an independent chronology-forward cohort.
- This is evidence that the **specific full historical identity arrangement** contributes under the stated strong, time-valid perturbation, not the isolated causal effect of just one relational property.

## KBS scientific implications and remaining constraints

- R1 contribution originality: significant strengthenings of candidate-indexed incumbent-relative historical knowledge value and its request-level downstream decisions, with a further fixed-candidate authentic-versus-rewired source contrast. No new sampled-metric consistency theorem or learning-to-defer routing theorem.
- R2 deployment: **BOUNDED**. F alignment has superior NDCG and fewer realized specialist calls than S alignment here, but there is no proof that selecting Memory is economically or latency superior to Always Memory; Always Memory remains more accurate and the earlier warmed offline path was faster. Do not claim universal net serving-cost saving.
- R3 integrated contribution: **STRONG WITHIN ADDITIONAL FROZEN SAME-PERIOD TARGETS**, with causality and complete popularity-floor qualification bounded. No temporal external/generalization guarantee.
- B4-A A4/A5 scientifically informative; targeted B4-A A6 referee-style adjudication and A7 evidence-aligned manuscript/S10 integration can proceed. Keep KBS submission HOLD until final author metadata/data-use/AI disclosure, references, sources and publisher-compliant PDF QA.
