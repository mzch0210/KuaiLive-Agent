# R0: Claim–protocol–evidence traceability and source consistency audit

**Date:** 2026-10-12  
**Stage:** R0 of the Plan C KBS integrated revision master plan.  
**Decision:** **R0 CORE EVIDENCE PASS; EXISTING MANUSCRIPT UPDATE HOLD.** The traceability matrix is established and the central values are auditable. Six high-priority manuscript discrepancies must be corrected in R2–R6 before any revised PDF is submission-ready. **This R0 does not modify the original eight-section manuscript, combined S1–S9, frozen TEST policies, or outcome data.**

**Machine-readable register:** [12-row R0 claim–protocol evidence JSON](R0_PLAN_C_CLAIM_PROTOCOL_EVIDENCE_MATRIX_2026-10-12.json).

## 1. Sources actually inspected

| Evidence tier | Original source | Evidence checked |
|---|---|---|
| Current manuscript | [main.tex](main.tex), 552 lines, and [S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md), approximately 70.9 KB | Existing C1/C2/C3 values, §5 old two-setting design, §6–8 interpretation, old supplement scope |
| Pre-TEST protocol | [G0F scientific freeze](../../experiments/kbs_plan_c/G0F_PRETEST_PROTOCOL_2026-10-12.json) and [six-Base frozen G5 registry](../../experiments/kbs_plan_c/G5_PRETEST_SIX_BASE_FROZEN_REGISTRY_2026-10-12.json) | Two Base architectures × three training seeds; five DEV-frozen gate objectives; three declared M3 primary comparisons; frozen 47,575 TEST cohort |
| G5-A outcome-blind test | [Actions #38225946950](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38225946950), artifact 11736962620, original manifest.json read | Completed 47,575 TEST events, no TEST target label read by G5-A; median 31,065 active warm-author candidates; registry SHA checked |
| G5-B one-shot TEST | [Actions #38226690320](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38226690320), artifact 11735868084, **original aggregate.json unzipped and inspected** | Six Base × five policy NDCG/HR, calls and realized rates, 12,533 users, eighteen primary contrasts and their Holm adjustment |
| G4 independent seed DEV | [Actions #38222994275](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38222994275), artifact 11735102444; [Gate OOF #38223562473](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38223562473), artifact 11734898639 | Four extra-seed 50,049-event full-active Base panels and the corresponding frozen DEV five-objective policy metrics |
| G4 warmed replay cost | [Actions #38223495966](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38223495966), artifact 11734923392, **original aggregate.json unzipped and inspected** | 256 DEV events, measured cost of each warmed path and test limitations |
| Existing accepted scientific report | [G5 paper-facing TEST report](../../experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md) | Verified that cited main G5 values agree with original downloadable aggregate |

Github Actions artifacts are retention-limited and not archival DOIs. The accepted private event-level M3 rows are not publicly attached and were not re-read for this audit. This R0 independently checked the aggregate bytes but did not retrain models or recompute individual TEST event ranks.

## 2. Three noninterchangeable study identities

| Protocol attribute | A — Twitch/LiveRec | B — Original KuaiLive | C — New KuaiLive-M3 |
|---|---|---|---|
| Ranked target | Available **streamer** | Time-bounded **live room** | Persistent **author / creator** |
| Split/evaluation | Historical DEV 46,878; **44,221 frozen TEST events** | Per-user chronological leave-last-two-out; 10,222 same-event examined TEST users | Global time-forward TRAIN ~24,995,148; DEV 50,049; **TEST 47,575 / 12,533 users** |
| Candidates | Crawl-time eligible streamers | Sampled **575 active rooms** versus paired same-event full-active rooms | All currently eligible **TRAIN-known active authors**; median TEST **31,065**, no 575 test cap |
| Base architecture | LiveRec availability/context-16/repetition | Fixed Dual-ID SASRec room + streamer fusion | SASRec and GRU4Rec **each trained with seeds 20261012/13/14** |
| Gate input | **14** pre-outcome features | No newly DEV-frozen independent TEST policy confirmation | **12** pre-outcome features; five DEV-frozen objective-specific pointwise rules per fitted Base |
| Role | C1 and frozen C3; retrospective equal-count Difficulty on TEST | C2 paired candidate-regime mechanism diagnostic; previously examined TEST | C1 and independent later-period C3 **one-shot frozen TEST**; six correlated fitted models, not six datasets |
| History | Observed events strictly prior to crawl step | Prior user–creator events; DEV interaction can precede TEST | Strictly prior events, including **earlier observed TEST events in prequential history**; current/future target never allowed in gate inputs |

Do **not** pool NDCG levels or pretend B room ranking equals C author ranking. The new M3 **4,096-event × 575-author** panel is a DEV checkpoint-selection screen, not a replicated same-event C2 candidate-size intervention. No zero-shot transfer of the Twitch gate to M3 was tested.

## 3. C1–C3 source ledger

### C1: Base-relative historical evidence value

- **Twitch frozen TEST, n=44,221:** Base NDCG@10 **0.58211**, Memory **0.53980**, Δ(Memory−Base) **−0.04232** with paired CI [−0.04521, −0.03950]. Historical **recoverable** target-defined subgroup n=5,539: Base **0.30181**, Memory **0.52225**, Δ **+0.22045**, CI [+0.21140, +0.23001]. These retrospective target states are never gate features. Sources: current main §6.1, S1/S6.
- **M3 one-shot TEST, n=47,575:** Fixed Memory **0.3467924591**, while all six independently fitted Base models obtain approximately **0.258004–0.260649** on the exact same full-active author candidate cohorts. Primary SASRec 20261012 Base **0.2580038643**, Memory−Base **+0.0887885948**. Source: original G5-B aggregate, accepted report §2.
- **Permissible:** Fixed historical Memory's marginal value depends on incumbent, task and candidate context. **Not permissible:** The Twitch/M3 mean-sign contrast isolates any one of model architecture, domain, time, candidate count or changed objective as a causal explanation.

### C2: Same-event candidate-regime dependence, original KuaiLive only

- Fixed Dual-ID raw rankers, fixed 10,222 matched user/target events, **575 sampled-active rooms**: Memory−Base **−0.04120411**. On contemporaneous full-active room candidates: **+0.04630669**. Paired difference **+0.0875108**, 3,000 paired-user bootstrap CI **[+0.08210,+0.09326]**.
- The crossed membership/standardization descriptive allocation attributes **+0.08826963** to membership and **−0.00075883** to normalization reference. This aggregates candidate count, composition and competition and is **not** a separately identified pure candidate-count causal effect.
- Sources: current main §6.3, S5 and S8. The M3 full-author task is complementary empirical scope, **not** an independent replicated same-event C2 intervention.

### C3: Predict specific Memory's marginal NDCG improvement

- **Twitch frozen TEST:** Utility **0.58983**, Always Base **0.58211**, paired Utility−Base **+0.00772** CI [+0.00641,+0.00903]; 6,650/44,221 **15.04%** DEV-frozen pointwise calls. Difficulty **0.58340**, Utility−Difficulty **+0.00644** CI [+0.00528,+0.00762], **but Difficulty's TEST call count is retrospectively matched** to Utility and is not a frozen pointwise TEST rule. Nondeployable same-count Oracle **0.64806**. Sources: current main §6.2, S7.
- **M3 frozen TEST:** Utility **0.301766–0.304004** across six Base fits; all five policies were fixed on DEV and scored TEST without outcome-based threshold changes. Utility beats four other objectives; Uncertainty is the strongest non-Utility in all six (secondary comparison, not one of the three preregistered confirmatory contrasts). Fixed Always Memory at **0.346792** outperforms all Utility gates on absolute quality.

| Six M3 frozen Base fits | Always Base | Utility | Difficulty | Specialist Quality | Uncertainty | History | Always Memory |
|---|---:|---:|---:|---:|---:|---:|---:|
| SASRec / 20261012 | 0.258004 | **0.302866** | 0.282479 | 0.279558 | 0.289373 | 0.279789 | **0.346792** |
| SASRec / 20261013 | 0.258811 | **0.301766** | 0.282803 | 0.281608 | 0.288136 | 0.280249 | **0.346792** |
| SASRec / 20261014 | 0.258673 | **0.303058** | 0.283020 | 0.280272 | 0.289374 | 0.280143 | **0.346792** |
| GRU4Rec / 20261012 | 0.260033 | **0.304004** | 0.284321 | 0.281829 | 0.290891 | 0.281964 | **0.346792** |
| GRU4Rec / 20261013 | 0.260649 | **0.303016** | 0.284147 | 0.282428 | 0.290004 | 0.282095 | **0.346792** |
| GRU4Rec / 20261014 | 0.258400 | **0.303549** | 0.283472 | 0.280543 | 0.289235 | 0.280461 | **0.346792** |

### The 30%-DEV-budget issue: test call rates are NOT equal

This **raw G5-B artifact** table is required to avoid overstating fairness and calling a DEV cap an online TEST quota.

| Frozen Base | Utility TEST % | Difficulty TEST % | Specialist TEST % | Uncertainty TEST % | History TEST % |
|---|---:|---:|---:|---:|---:|
| SASRec 20261012 | 29.2149 | 29.9044 | 29.5681 | 30.1797 | 35.4724 |
| SASRec 20261013 | 27.7183 | 30.3226 | 29.9674 | 29.4062 | 35.4724 |
| SASRec 20261014 | 28.2144 | 29.6500 | 29.7803 | 30.2617 | 35.4724 |
| GRU4Rec 20261012 | 28.8723 | 30.3332 | 29.9170 | 29.8308 | 35.4724 |
| GRU4Rec 20261013 | 28.6453 | 30.0809 | 29.9359 | 29.7846 | 35.4724 |
| GRU4Rec 20261014 | 29.0951 | 30.1146 | 29.8077 | 30.1061 | 35.4724 |

All were selected with at most 30% DEV calls **during DEV optimization**, then frozen pointwise. TEST call fractions drifted and were **not forcibly capped, equalized or retuned**. Post hoc TEST reallocation would destroy the frozen prospective policy comparison. Main §5–6 must report **both NDCG and actual calls** and must not say the five M3 methods had exactly equal TEST call counts.

### TEST inferential identity

- Three preregistered M3 one-sided primary contrasts: Utility−Always Base, Utility−Difficulty, Utility−Specialist.
- Each of six Base/seed blocks evaluated on the **same 12,533 TEST users**, using 5,000 user-cluster paired bootstrap draws and 5,000 user-cluster random-sign replicates. Holm adjusts the **three comparisons within each Base/seed**; 18 primary tests are **not** one globally Holm-protected family. All have adjusted p approximately **0.00059988** (Monte Carlo floor), and positive paired 95% CIs as in accepted G5 report §3.
- Sign-flip significance assumes approximately sign-symmetric user-cluster null differences. Three fitted seeds are **correlated replications on the same data**, not independently sampled datasets.
- Utility−Uncertainty is an important **secondary** descriptive TEST gap; do not silently label it one of the G0F three primary tests.

### Descriptive budget and computational cost

- M3 seed20261012/SASRec TEST: exact conditional expected Random@30 **0.284640**; retrospective, nondeployable budget Oracle@30 **0.388135**, unlimited hindsight Oracle **0.388333**. This differs from Twitch's retrospectively count-matched 6,650-call Oracle; neither is a prospective deployable oracle.
- **Actual 256-event DEV warmed offline cost audit (RTX3090, SASRec main seed):** Always Base mean **1.4245 ms**, fixed Memory mean **0.8033 ms**, Utility selective path mean **1.8018 ms**. Selected sample calls 80/256 (31.25%). Histories, candidate availability and weights were prepared before timing; network, IO, state maintenance, scheduling and contention are excluded. It is **not production latency**.
- Given fixed Memory both higher NDCG on M3 TEST and cheaper on the measured warmed DEV path, the paper cannot claim a general net speedup or unconditional deployment advantage. An artificial expert-call fraction does not demonstrate a real economic scarcity constraint.

## 4. Mandatory source-conflict register

| Flag | Priority | Verified conflict and current location | Required later edit |
|---|---|---|---|
| **R0-P0-01** | P0 | Current main Introduction, §5 opening (~line 240), dataset table (~lines 253–267) and Conclusion treat **only Twitch + original KuaiLive** | R1/R2/R5 must introduce **third separate M3 author task** and refresh contributions and validity limits |
| **R0-P0-02** | P0 | §5 compared-methods (~274–301) and S1–S9 introduction (~line 19) imply **only Twitch Utility is independently frozen** | Distinguish Twitch Utility-frozen + retrospectively matched Difficulty from **five fully DEV-frozen M3 gates** |
| **R0-P0-03** | P0 | §3/§5 equal-count narrative (~127–137, ~274–278, ~323) lacks M3 TEST realization details | State **DEV cap, TEST rate drift**, publish all five rates; no uniform strict 30%-TEST-call assertion |
| **R0-P0-04** | P0 | Current cost §6.5/§7 and supplement S9 concern older KuaiLive replay only | Include M3 adverse warm latency comparison and Always Memory unconditional quality dominance; no net-speedup claim |
| **R0-P0-05** | P0 | §4 Base (~183–188), 14-feature method (~225), §5 table and Stats/Implementation | Disambiguate **room/author**, **14 Twitch versus 12 M3 features**, distinct split, **575 sampled DEV screening versus full TEST author set** |
| **R0-P0-06** | P0 | §5 statistical protocol (~323–325) does not describe M3 confirmatory tests | Show paired 12,533-user clustering, sign-symmetry, **three-Holm within each of six blocks**, no global-18 FWER guarantee |
| **R0-P1-01** | P1 | Original G0F sampler description names a timestamp_ms hash field; G1 created frozen cohorts using DuckDB typed timestamp | Transparently document frozen cohort SHA and implementation discrepancy; do not misstate preregistration as byte-for-byte executable identical |
| **R0-P1-02** | P1 | Earlier DEV Memory rank scorer uses 1e−12 tie tolerance; G5 frozen top10 implementation uses exact-score/author-ID tie order | Document tie convention per frozen protocol; if ever checked, do label-free audit only, **never alter G5 TEST rules post-outcome** |
| **R0-P1-03** | P1 | S1–S9 scope note states old main text claims unchanged and Twitch sole independent policy TEST | R6 synchronize supplement S1–S3/S7–S9, preserve old Twitch and room diagnostics |
| **R0-P1-04** | P1 | §2 and §7 discuss generic learning-to-defer and knowledge fusion | Differentiate fixed Memory's relative ranking evidence from existing general-purpose gating/deferral; avoid claiming the latter invented |
| **R0-P1-05** | P1 | G4/Audit older documents still include historical “TEST not yet run” statuses | Do not copy obsolete snapshot into current manuscript; cite final G5 as source of truth, keep logs as history |
| **R0-P1-06** | P1 | Actions artifacts have retention and event-level rows remain on User-host | R6/R8 secure stable reproducibility plan with primary public data, code, exact hashes; do not publicize private event IDs |

**Interpretation:** The P0 items are **main-text contradictions and omitted safeguards**, not failed experiments. They block the revised manuscript, but R0 evidence identity work is sufficiently complete for R1 to proceed.

## 5. R0 checks and scope of verification

**Passed:** C1/C2/C3 numeric signs and paired scopes checked against original main and supplemental; frozen G0F and six checkpoints verified against G5-A report; raw G5-B aggregate checked for **all six** methods, five rates and 18 conditional primary test outcomes; G4 original cost archive checked; old §5 and S1–S9 opening statement checked for obsolete identity claims.

**Not performed / not claimed:** R0 did not rebuild checkpoints, re-open event-level TEST targets, rerun 5,000 bootstrap draws, verify every ancillary number in all 70.9 KB S1–S9 line by line, prove cross-release person disjointness, or verify unpublished specific KBS format limits. Existing accepted source-code SHA and original run outputs remain the authority.

Reproducibility relevance from official publisher guidance: https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-statement and https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-guidelines . Journal-specific submission checklist remains for R8 rather than being invented at R0.

## 6. Gate acceptance and handoff

| R0 requirement | Verdict |
|---|---|
| Separate Twitch, original KuaiLive and M3 ranking/evaluation identities | **PASS** |
| Map C1–C3 plus cost and budget to exact frozen evidence artifacts | **PASS** |
| Inspect G5 original aggregate, six model conditions, all TEST actual rates and model-specific three-Holm tests | **PASS** |
| Record six P0 integration issues and six P1 audit cautions | **PASS** |
| Eight-section main and S1–S9 already consistent with accepted M3 TEST | **NO — deliberately unchanged at R0** |
| Positive production net speedup established | **NO — contradicted by observed warmed cost condition** |

**R0 decision: CORE EVIDENCE PASS; R1 SCIENTIFIC ARGUMENT BLUEPRINT AUTHORIZED.** Manuscript revision/submission remains blocked pending six R0-P0 corrections through R2–R6. Do not use the R0 ledger to change archived G0F or G5 frozen outcomes. Future revision writing should retain academic argumentation, not chronicle GitHub Actions runs.
