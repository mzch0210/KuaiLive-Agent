# Section 5 — KBS-style line-by-line reviewer tightening

**Date:** 2026-10-08  
**Artifact:** [Canonical LaTeX manuscript](main.tex), Section 5 `Experimental Setup`.  
**Status:** Editing pass completed; review recorded after direct verification against the project's KuaiLive/Twitch frozen-protocol scripts and current same-checkpoint evidence.  
**Scope constraint:** Sections 1–4 unchanged, Section 6 not filled with unverified numbers; six Section 5 subsections and two experiment-design tables retained.  
**Editorial frame:** KBS favors substantive, original AI research with an appropriate balance of methodological explanation and practical evidence; this document is a **review-style** internal audit, not a claim to be a real journal review.

## Major reviewer concerns addressed

### P0-A — Over-generalized percentile preprocessing (5.3)

**Previously:** The manuscript described a full-DEV unlabeled ECDF reference as though both platforms used exactly that frozen transform.

**Repository check:** `analysis/liverec_p1_complete_policy_freeze.py` and `analysis/liverec_p1_dev_gate_fit.py` validate a Twitch DEV-fitted ECDF reused on TEST, with a shared outcome-free DEV reference across OOF folds. The KuaiLive baseline feature extractor `analysis/room_level_selective_agent.py::user_features` computes cross-user percentile ranks from the `train` or `train+dev` eligible past-history pool for the relevant prediction split. This is `not` the identical DEV-frozen ECDF semantics. Neither uses TEST target labels to fit the router.

**Revision:** Explicitly separate the implementations and the outcome-free versus target-dependent information boundaries. **Remaining paper action:** report per-platform feature transformation/source manifests and do not assert universal DEV-reference scaling in Sections 4–6.

### P0-B — Cross-validation type differs for repeated-user temporal protocol (5.3)

**Previously:** “five-fold shuffled OOF” applied to every protocol.

**Repository check:** Primary one-target-per-user KuaiLive (`analysis/dual_id_room_baseline.py`) and Twitch (`analysis/liverec_p1_dev_gate_fit.py`) use `KFold(n_splits=5, shuffle=True, random_state=20260918)`. Global-time multiple-event KuaiLive (`analysis/global_temporal_dual_selective.py`) uses `GroupKFold(n_splits=5)` grouped by user.

**Revision:** State this distinction directly. **Remaining paper action:** check that every subsequent global-time report uses grouped, not event-independent, inference.

### P0-C — Candidate-set changes are not an isolated causal intervention (5.1, 5.4)

**Previously:** Broad “operating regime” descriptions underemphasized the joint change in candidate membership and within-candidate z-score reference. The historical and post-hoc matched-checkpoint contexts risked conflation.

**Repository check:** `analysis/kbs_kuailive_same_checkpoint.py` uses one checkpoint pair, sampled-DEV-selected room alpha `0.125`, one TEST target per user, and nested candidate arrays; it re-standardizes room and streamer scores within each candidate set. The post-hoc matched-checkpoint result is recorded in `KBS_KUAILIVE_SAME_CHECKPOINT_RESULTS_2026-10-08.md`.

**Revision:** Identify both changing dimensions and clarify `historical regime-specific` versus `completed supporting post-hoc` protocol comparisons. Do not claim isolated candidate-membership causality.

### P0-D — Sampled evaluation and relevance semantics (5.1)

**Previously:** “active negatives” could be read as verified user dislikes; sampled metrics could be mistaken for estimates of full-candidate NDCG.

**Revision:** Call these contemporaneously active `unobserved` evaluation negatives; state sampled NDCG is not an unbiased proxy for full-active NDCG. Cite Krichene & Rendle (KDD 2020; DOI `10.1145/3394486.3403226`) added to the manuscript's BibTeX database.

### P0-E — Test-label access and matched-count control permissions (5.2, 5.3)

**Previously:** “Test targets used for decisions?” obscured the difference between an offline comparison budget selected from TEST pre-outcome Utility outputs and Oracle labels used to maximize hindsight utility.

**Revision:** Table 2 distinguishes the `m` realized by the frozen Utility selector from hindsight access to TEST outcomes. Base Difficulty uses predicted base loss, not realized TEST loss; Oracle remains nondeployable. The primary threshold is still pointwise and not a hard online quota.

## Sentence-level revision register

Each change was made directly to `main.tex`. Identifiers are editorial checks, not algorithm changes.

| ID | Section | Reviewer concern | Tightening action |
|---|---|---|---|
| R01 | 5 opening | Generic positioning; possible intrinsic value claim | Replace with two falsifiable empirical purposes and within-protocol definition |
| R02 | 5.1 | Vague dataset scope/release trace | Name interaction domain and provenance requirement |
| R03 | 5.1 | Room and streamer identity ambiguity | Clarify prediction unit versus relationship carrier |
| R04 | 5.1 | Chronology and leakage ambiguity | Identify leave-last-two-out, 10,222 users, and legal TEST history |
| R05 | 5.1 | Candidate interval, sampled metric and negative-label ambiguity | Half-open intervals, observed-vs-unobserved candidates, cite sampled metric caveat |
| R06 | 5.1 | Ten-minute timestamps could imply exact arrival/exit | Define first/last observed crawl steps and legal streamers |
| R07 | 5.1 | Primary vs strict history semantics conflated | Explicit first-observed eligibility and stricter split-end sensitivity |
| R08 | Table 1 | Caption imprecise on evaluated units | DEV/TEST event counts distinguished from interactions |
| R09 | Table 1 | Undocumented global-time numbers in core table | Remove unquantified row; retain protocol discussion and supplement trace |
| R10 | Table 1 | Twitch caption unclear about length and availability | Clarify step-level candidates and base length |
| R11 | 5.2 | Generalized alpha and weak-baseline positioning | Identify original 0.1/0.9 vs new alpha identities; name GRU4Rec / ContraRec--BERT4Rec with common candidates |
| R12 | 5.2 | Overstated platform architecture equivalence | Distinguish Twitch LiveRec from KuaiLive Dual-ID |
| R13 | 5.2 | Difficulty and Oracle comparison wording long | Clarify prediction targets, offline top-m controls and deployability |
| R14 | Table 2 | Table caption hides realized budget | Make budget/status explicit |
| R15 | Table 2 | Ambiguous test target/decision heading | Target outcome at selection time stated directly |
| R16 | Table 2 | Offline Difficulty budget conflated with test label | Specify DEV loss fit, TEST-derived unlabeled `m` |
| R17 | Table 2 | Oracle indistinguishable from forecast | Label realized TEST utility, hindsight-only |
| R18 | 5.2 | “Cross-platform transfer” too broad | Clarify selector refit and distinct threshold on Twitch |
| R19 | 5.3 | Insufficient separation of training and serving information | Enumerate forbidden target/rank/state features |
| R20 | 5.3 | Incomplete OOF protocol | HGB parameters, quantile grid, KFold vs GroupKFold, tie rule |
| R21 | 5.3 | **P0** false universal percentile claim | Platform-specific outcome-free reference semantics; unbiasing caveat |
| R22 | 5.4 | Historical vs new estimands mixed | Distinguish native full-active / strict transfer from new paired diagnostic |
| R23 | 5.4 | “Same model” overinterpreted | Specify fixed weights/alpha/history, candidate-wise normalization changes together |
| R24 | 5.4 | Post-hoc TEST may be called second confirmation | Strict evidence hierarchy and no sign-dependent selection |
| R25 | 5.5 | Ambiguous metric comparison unit | Require event-paired protocol-specific deltas, invocation count/rate |
| R26 | 5.5 | Unit of bootstrap and independent seeds mixed | User bootstrap vs cluster resampling; seed SD vs CI |
| R27 | 5.5 | Offline invocation claims could imply online speedup | Efficiency conditional on measured hardware/batch conditions |
| R28 | 5.6 | Reproducibility source/checkpoint ambiguity | Pin ReChorus source commit and separate new vs historic checkpoint identities |
| R29 | 5.6 | Non-durable GitHub artifacts could be called archived | Require independently retained outputs for submission |

## LaTeX-source integrity addendum

A reviewer-style content audit must inspect the typeset source, not merely a successful CI exit code. During the post-edit check, 26 literal `emph{...}` tokens (missing their command backslash) and one unescaped percentage sign were detected and corrected in `main.tex`. The Twitch methods paragraph was also shortened to avoid a new overfull line. All 25 remaining intentionally emphasized spans now have valid `\\emph{...}` commands; the Section 5 text contains no unescaped `%` tokens. All manuscript citation keys, labels and cross-references have a corresponding definition in the sources. This addendum concerns only LaTeX presentation, not scientific protocol changes.

## Explicit remaining verification work (NOT silently resolved)

1. **Source dataset scale and DOI/release number:** the main text deliberately does not invent raw user/interaction totals. Fill Table 1 with further audited figures if complete, immutable source metadata can be cited.
2. **Historical native/full vs paired Base provenance:** keep numeric results, checkpoint SHA256s, fusion alphas and candidate regimes separate in Section 6.1. Reconcile historical sampled Base values `0.60784` and `0.61714` before creating comparative result tables.
3. **Twitch implementation nuance:** retain first-observed step historical replay versus strict-split-end analysis. Do not describe ten-minute observed windows as exact arrivals/departures.
4. **Future P0/P1 factorial/seed analyses:** they are separate `post-hoc` supporting experiments. Do not revise original policy threshold, re-label repeated TEST use as new untouched test evidence, or insert results into Section 5 based on still-running or unverified outputs.
5. **Final reproducibility supplement and submission checklist:** produce durable data/code/checkpoint links; verify the `Knowledge-Based Systems` live Guide for Authors for journal-specific declarations rather than assuming that general Elsevier options are mandatory for every journal.
6. **Visual layout:** inspect compiler output for narrow-cell overflow, widow/orphan text and cross-reference placement; a passing PDF compilation is necessary but not sufficient for typographic approval.

## External authoritative background

- [*Knowledge-Based Systems*, Elsevier journal description](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051). Its emphasis on innovative AI methods and a balance of theory and application motivates the methodological focus.
- [Krichene & Rendle (2020), *On Sampled Metrics for Item Recommendation*](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/), KDD, DOI `10.1145/3394486.3403226`.
- [Elsevier research data statement guidance](https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-statement) for transparent, availability-qualified data/code descriptions; consult the journal-specific author instructions at submission.

## Final build verification

- **Build:** [GitHub Actions 37753518887](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37753518887), successful for the finalized LaTeX source commit `775afc40bbf9f6b1635733e7222d35d8b27b3e91`.
- **PDF and log artifact:** [11539111133](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37753518887/artifacts/11539111133), `kbs-manuscript-build-37753518887`.
- **Checks:** compile, generated PDF existence, artifact upload, manuscript cross-reference/BibTeX key static audit, and TeX emphasis/percentage escape validation passed. No fatal LaTeX errors; final passes show only small pre-existing overfull paragraph warnings in Sections 1–4 (approx. 1–2 pt), not the new Twitch paragraph. Typeset visual approval remains a separate editorial task.

**Editorial conclusion:** The edited Section 5 is significantly tighter on selection fairness, data temporal semantics, candidate protocol identity, target leakage, bootstrap units and claims scope. No extra experimental performance has been inferred from prose editing; scientific results remain located in Section 6 and its evidence sources.
