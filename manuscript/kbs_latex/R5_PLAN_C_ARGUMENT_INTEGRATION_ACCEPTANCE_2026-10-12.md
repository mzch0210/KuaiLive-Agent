# R5 — Scientific argument integration and KBS-oriented editorial acceptance

**Date:** 2026-10-12  
**Stage:** R5 of [Plan C integrated revision plan](PLAN_C_KBS_INTEGRATED_REVISION_MASTERPLAN_2026-10-12.md)  
**Verdict:** **R5 PASS** for Introduction (§1), Related Work (§2), Discussion (§7) and Conclusion (§8). The **whole manuscript remains HOLD** until R6 supplemental integration, R7 independent KBS scientific referee review and R8 final scientific/PDF/submission audit.

**Scientific invariants:** No frozen G0F/G5 models, gate thresholds, test cohorts, outcomes, existing §3–6 results, original S1–S9 supplements or model files were changed in R5. Main source edits are confined to §1–2 and §7–8; the bibliography entries were unchanged.

## 1. Verified source, builds and independent PDF inspection

- Final [main.tex](main.tex) current GitHub blob **3e6711fa1526349a09e89dc79dad39b33eab44b4** after R5 source commits **b26315b080d0d58a8b0a41168f802c1885513943** (Introduction/Related Work) and **13ccead461bfb35e36ecf798cbc4a96831fddddf** (Discussion/Conclusion).
- [GitHub Actions R5 final compile #38240229963](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38240229963): **SUCCESS**; artifact **11742657653**. PDF **36 pages, 504,517 bytes**, Letter preprint layout. This is **not** a finished journal submission; author name is a placeholder and frontmatter abstract remains unwritten.
- Unpacked original workflow artifact and independently inspected PDF information and LaTeX logs. **Zero Overfull boxes, zero undefined references and citations, zero duplicated labels by complete-source static check.** Three underfull hbox warnings remain, including existing justification cases, without clipping.
- Inspected rendered PDF pages 1–4 and 28–34, including introduction contributions, Related Work, five Discussion subsections, Conclusion and bibliography. Main section starts: Introduction p.1; Related Work p.3; Discussion p.28; Conclusion p.31. No visible table clipping, paragraph collisions or corrupted symbols. No new pages added beyond the prior 36-page R4 intermediate manuscript.
- Original PDF event numbers and results checked against the R0/R3 accepted source ledger: two frozen decision TEST settings (Twitch 44,221; M3 47,575/12,533 users), original room paired n10,222, six M3 fitted models, Always Memory 0.34679 versus Utility range 0.30177–0.30400, warmed M3 Memory 0.803ms versus selective 1.802ms. Main conclusions have explicit boundaries.

## 2. Why the revisions are scientifically coherent rather than a chronological append

**§1 Introduction:** The scientific question is the fixed relationship specialist's *marginal* ranking utility relative to an already fitted incumbent, on the same eligible candidate set. A five-paragraph reasoning chain connects the available history, incumbent overlap, candidate sensitivity, pre-outcome relative-utility prediction and three evidence identities. Three hierarchical contributions are C1 operational value, C2 original room paired candidate-regime sensitivity and C3 two independent frozen ranking-task selection settings. The M3 frozen author TEST, six trained Base fits and five gate objective classes are acknowledged without conflating them with the old room task or independent six-population data. No generic gate/theorem originality or global speedup claim.

**§2 Related Work:** Three existing strands retained: (1) sequential/knowledge representation and fusion, (2) specialist selection and Learning-to-Defer, (3) live-streaming and candidate evaluation. Primary publisher records independently checked:
- KBS 2026 MHGFCL, DOI 10.1016/j.knosys.2026.115673, https://www.sciencedirect.com/science/article/pii/S0950705126004132
- KBS 2026 KAPER, DOI 10.1016/j.knosys.2026.116236, https://www.sciencedirect.com/science/article/pii/S0950705126009627
- KBS 2026 incomplete-KB dynamic gating, DOI 10.1016/j.knosys.2026.116167, https://www.sciencedirect.com/science/article/pii/S0950705126008932
- ICML 2020 Mozannar & Sontag, https://proceedings.mlr.press/v119/mozannar20b.html
- NeurIPS 2022 Narasimhan et al., https://research.google/pubs/post-hoc-estimators-for-learning-to-defer-to-an-expert/
- KDD 2020 sampled ranking metric study by Krichene & Rendle, https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- AAAI 2026 GUIDER uncertainty decomposition, https://ojs.aaai.org/index.php/AAAI/article/view/38639

Claims of algorithmic originality are bounded: gating, evidence selection, sampled-ranking inconsistency, and learning-to-defer are already known. Our empirical distinction is a **fixed historical relationship specialist, candidate-conditioned ranking difference, temporally correct observable inputs, and two prospective-protocol decision validations**. M3's Base-margin Uncertainty is not a replication of full GUIDER.

**§7 Discussion:** Reorganized five coherent arguments: (7.1) incumbent/context-dependent value with Twitch's negative and M3's positive overall Memory utility without one-factor causal attribution; (7.2) original KuaiLive same-event room candidate reversal and descriptive, not isolated causal, membership/reference allocation; (7.3) explicit relation to deferral methods and new M3 Utility versus four DEV-frozen alternatives, three-Holm within-fit tests, secondary Uncertainty and shared-cohort six-seed dependency; (7.4) genuine distinction between specialist-invocation quota and wall-clock cost, with strong adverse M3 evidence; (7.5) practical evidence-evaluation implications without claims that Memory must always be gated.

**§8 Conclusion:** Three compact scientific moves: (i) measured value of relationship history relative to incumbent/candidates; (ii) frozen Twitch and forward-time M3 selection evidence linked to original room candidate sensitivity; (iii) precise application bounds including **Always Memory higher accuracy and lower limited warmed latency** in M3.

## 3. Critical scientific and fairness constraints preserved

| Reviewer-sensitive topic | R5 treatment |
|---|---|
| Theoretical novelty | Relative-expert allocation anchored in established deferral; contribution is the measured ranking-specific knowledge use case and frozen comparison, not new general gating theorem. |
| Scope of "independent" validation | Two distinct frozen **TEST decision settings**; M3 includes 2 architectures×3 trained seeds all applied to the same TEST user population; original KuaiLive candidate analysis is post-hoc within a previously inspected cohort. |
| Twitch Difficulty | Retrospectively TEST call-count matched versus frozen Utility threshold, not a prospective pointwise Difficulty policy. |
| M3 five gate policies | DEV-frozen pointwise; TEST rates drift and are not exactly matched or guaranteed ≤30%, despite same DEV selection cap. |
| M3 statistical claims | Three preregistered primary contrasts per fit with within-fit Holm corrections and user-cluster intervals; no globally Holm-corrected 18-test family; Uncertainty secondary. |
| Candidate-regime causal attribution | Original same-room paired sign reversal is informative, but size, composition and competition change together. Cross Twitch/M3 signs do not identify the cause. |
| Online information leakage | M3 prequentially uses strictly earlier observed TEST interactions; current/future target unknown before decision. Target-defined states, Oracle are retrospective only. |
| Unconditional Memory / cost | On M3 Memory absolute NDCG 0.34679 > all Utility (0.30177–0.30400); 256-event warmed Memory 0.803ms < Utility route 1.802ms. No demonstrated speed gain or economic necessity of routing under this measured cost model. |
| Academic tone | Claim-first paragraphs, explicit citations, substantive methodological constraints integrated coherently rather than repeated process logs or apology-style lists. |

## 4. R0 12-issue register after R5 and source-of-truth boundaries

See the new machine-readable [R5 issue-closure tracker](R5_R0_P0_P1_ISSUE_CLOSURE_TRACKER_2026-10-12.json). **No R0 issue is marked entirely closed at the paper level before R6–R8**, although all new M3 main-text argumentative integration now resides in §§1–8.

- **P0-01,02:** Intro/Discussion/Conclusion now have correct three-protocol and two independent frozen-test framing; R6 supplements still stale.
- **P0-03:** Relative invocation-call constraint versus TEST realized-rate drift explicit; R6 S7 detailed rate matrix is outstanding.
- **P0-04:** Always Memory accuracy and unfavorable warmed-cost finding explicitly in both Results and Discussion, and Conclusion. R6 S9 pending.
- **P0-05:** Distinguish streamer, live-room, author recommendation tasks and 14/12 feature schemas; R6 S1–S3 remain.
- **P0-06:** Primary/secondary statistic and within-fit Holm scope consistent across main; complete S8 inference table awaits R6.
- **P1-01/02:** Source implementation-vs-G0F hash notation and tie convention disambiguation await S1/S2 replication detail in R6.
- **P1-03:** Combined S1–S9 still contains obsolete Twitch-only frozen TEST scope: **R6 must fix**.
- **P1-04:** Main Related Work strengthened against established L2D and KBS knowledge gating. **R7 independent scientific referee-style novelty challenge is still mandatory**.
- **P1-05:** Superseded earlier G4 "TEST not run" descriptions are dated historical records; R6 must reference final G5 source of truth without rewriting frozen history.
- **P1-06:** Time-limited Actions artifacts and limited public event-level data require a stable privacy-respecting reproducibility statement and artifact release plan in R6–R8.

## 5. Remaining work / next gate

**R5 verdict:** PASS for academic writing, new scientific argument and current front/back integration; original experiment numerical evidence unchanged. The 36-page preprint is not automatically within a verified KBS page/abstract limit and is not final; general Elsevier journals scope is consistent with knowledge-aware recommendation and decision support but no acceptance probability is claimed. KBS official journal description: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051.

**R6 next:** Synchronize S1–S9 to new three-protocol and two-freeze evidence identity; expand M3 complete six-Base/five-gate tables, all 18 user-cluster CI/Holm tests, five actual call fractions for each Base/seed, training/gate SHA and frozen prequential implementation, both distinct warmed execution-cost protocols and the negative Always Memory comparison. Preserve private raw TEST event data and old posthoc candidate analysis boundaries; no post-TEST model tuning or favorable result selection.

**R7/R8:** Independent reviewer-style novelty, economics and paper-level completeness critique, then final scientific/LaTeX/publishing checklist including Abstract, keywords, author information and declarations. Avoid assuming unavailable journal-specific submission word/page constraints. Continue rigorous editorial condensation if final manuscript grows; avoid removing adverse deployment evidence merely to save space.
