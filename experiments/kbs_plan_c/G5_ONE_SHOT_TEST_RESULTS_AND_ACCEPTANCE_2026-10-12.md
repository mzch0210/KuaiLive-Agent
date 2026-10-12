# Plan C G5 — Independent forward-time held-out TEST: one-shot confirmation

**Status:** G5 ONE-SHOT PASS: 47,575 frozen TEST events, 12,533 user clusters. TEST outcomes read once in an independent label-reveal step **after** successful label-blind six-Base inference and SHA-verified DEV-frozen policies. The scientific conclusion is *matched-call-budget utility routing*, not unconditional quality or speed dominance.

**Source-of-record:** [G5 frozen registry](G5_PRETEST_SIX_BASE_FROZEN_REGISTRY_2026-10-12.json); [G5 execution protocol](G5_ONE_SHOT_HELDOUT_EXECUTION_PROTOCOL_2026-10-12.md); [G5-A target-blind Actions #38225946950](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38225946950), **success** artifact **11736962620**; [G5-B one-shot outcome confirmation #38226690320](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38226690320), **success**, artifact **11735868084**. Preflight [#38225118849](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38225118849) independently confirmed six Base weights + frozen policy + supervised gate-model SHA256 digests and the exact TEST cohort hash before either TEST scoring step.

## 1. Frozen model/target discipline

- G1 TEST input byte SHA256: \`e60da60672ea1921dd3a5fccfb0aa76a3a06d50834e8080a07b2465777c9bdb1\`. Predeclared cohort 47,575 events. G5-A G1 CHECKPOINT and policy registry SHA256: \`39217c59f54f133fea8c7c0e1691ebc32c7082a53a7452c10f16a25fd48ad29c\`.
- G5-A did **not** read the current selected event's TEST target-author label, compute any observed NDCG or refit gate/threshold. It did read all *strictly prior* eligible TRAIN/DEV/**TEST** interactions in a **prequential** user history replay, including previous TEST observations not sampled in the evaluation cohort. These previous TEST outcomes are permitted only as strictly previous history, never as current/future labels or model/policy-fitting targets. It stored frozen target-blind seven top10 author-token lists per TEST event (six fitted Bases and one unchanged fixed Memory), full-roster candidate counts and six × five gate scores/call masks. No target IDs, event score rows or user histories were publicly uploaded. Its private .npy arrays and SHA fingerprints were frozen before label reveal.
- G5-A work was **399.7 seconds** in its own manifest. Mean test warm-active candidate count **32,166.6**, median **31,065**, reflecting drift from DEV's median ~33,759. This candidate regime is full-active author-level, not the earlier 575-candidate model-selection screen or original KuaiLive room-ranking task.
- Only G5-B verified the G5-A private file SHA256 identities and read TEST target author labels. It calculated deterministic rank-position NDCG@10 and HR@10 without any model, feature, hyperparameter or threshold change.
- A pre-outcome initial CI [#38225810427](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38225810427) failed on Python syntax before it could reach the User-host or read TEST; the syntax and synthetic eligibility fixture were corrected before the successful G5-A. This correction **precedes** any TEST target scoring and is preserved rather than hidden.

## 2. Confirmatory full-active author ranking on TEST

Same exact 47,575 events and fixed Memory score for all six Base checkpoints.

| Base model | TRAIN seed | Always Base NDCG@10 | Utility NDCG@10 | Difficulty | Specialist | Uncertainty | History | Always Memory |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SASRec | 20261012 | 0.258004 | **0.302866** | 0.282479 | 0.279558 | 0.289373 | 0.279789 | **0.346792** |
| SASRec | 20261013 | 0.258811 | **0.301766** | 0.282803 | 0.281608 | 0.288136 | 0.280249 | **0.346792** |
| SASRec | 20261014 | 0.258673 | **0.303058** | 0.283020 | 0.280272 | 0.289374 | 0.280143 | **0.346792** |
| GRU4Rec | 20261012 | 0.260033 | **0.304004** | 0.284321 | 0.281829 | 0.290891 | 0.281964 | **0.346792** |
| GRU4Rec | 20261013 | 0.260649 | **0.303016** | 0.284147 | 0.282428 | 0.290004 | 0.282095 | **0.346792** |
| GRU4Rec | 20261014 | 0.258400 | **0.303549** | 0.283472 | 0.280543 | 0.289235 | 0.280461 | **0.346792** |

The five gate policy DEV threshold files were **unchanged**. Realized Utility call fractions on TEST varied naturally: SASRec seeds 20261012/13/14 respectively **29.215% / 27.718% / 28.214%**; GRU4Rec seeds **28.872% / 28.645% / 29.095%**. No TEST rate was forced to exactly 30%, and zero threshold retuning occurred. For primary seed SASRec, HR@10 was **0.387620 Base / 0.455681 Utility / 0.533873 Always Memory**; analogous positive relative HR differences occur in all six. Always Memory at 100% calls remains higher in both NDCG and HR than the ~28–29% call Utility policies, as expected under an unequal call budget.

Three-seed mean ± *sample* SD of TEST NDCG: SASRec Always Base **0.258496 ± 0.000432**, SASRec Utility **0.302563 ± 0.000697**; GRU4Rec Always Base **0.259694 ± 0.001162**, GRU4Rec Utility **0.303523 ± 0.000495**. Both model families consistently place Utility ahead of the strongest alternative Uncertainty (SASRec gap 0.01349–0.01368, GRU4Rec gap 0.01301–0.01431). These six checkpoints share common data and are not six disjoint population replications.

## 3. Preregistered three primary one-sided contrasts, paired user-cluster uncertainty

A **single 5,000-user-cluster-bootstrap** with paired same-user resampling and 5,000 user-cluster random-sign draws was applied across all 18 contrasts. Each model/seed has **three preregistered one-sided comparisons** corrected with Holm within that model/seed's 3-hypothesis family. Minimum resolvable raw p-value with 5,000 randomized draws is **1/5001 ≈ 0.000200**, and Holm-adjusted p-value for each of the 18 reported tests is **0.000600**, since all are at the resampling resolution floor.

| Frozen Base / seed | Utility − Base, Δ [95% paired cluster CI] | Utility − Difficulty, Δ [95% CI] | Utility − Specialist, Δ [95% CI] |
|---|---|---|---|
| SASRec / 20261012 | **+0.044862** [0.042805, 0.046915] | **+0.020387** [0.018370, 0.022442] | **+0.023308** [0.021177, 0.025508] |
| SASRec / 20261013 | **+0.042955** [0.041000, 0.044987] | **+0.018963** [0.016955, 0.021069] | **+0.020158** [0.018101, 0.022293] |
| SASRec / 20261014 | **+0.044385** [0.042441, 0.046415] | **+0.020038** [0.018054, 0.022055] | **+0.022786** [0.020679, 0.024965] |
| GRU4Rec / 20261012 | **+0.043971** [0.042001, 0.046024] | **+0.019683** [0.017580, 0.021775] | **+0.022175** [0.020009, 0.024408] |
| GRU4Rec / 20261013 | **+0.042367** [0.040359, 0.044484] | **+0.018868** [0.016771, 0.021032] | **+0.020588** [0.018542, 0.022831] |
| GRU4Rec / 20261014 | **+0.045149** [0.043166, 0.047204] | **+0.020077** [0.018071, 0.022175] | **+0.023005** [0.020873, 0.025251] |

Every prespecified comparison rejects the *user-cluster sign-symmetry null under the adopted random-sign procedure* after Holm adjusting **within its corresponding three-comparison group** (p_adj = 0.000600, all < 0.05). The sign-flip p-values rely on approximate symmetry of groupwise residual differences. **Do not** imply that the six model/seed blocks are independent or that a single familywise 18-test correction has been performed; do not report p-values as smaller than the method's Monte Carlo resolution. Unlike the earlier DEV conditional bootstrap, these metrics were computed on the held-out TEST **after DEV-trained policies and thresholds were frozen**.

## 4. Reference benchmarks and limitations

- Same-group **Always Memory**: **0.346792 NDCG@10 / 0.533873 HR@10**, about 0.043–0.045 NDCG higher than all six Utility policies. This is the most important absolute-quality comparison and cannot be omitted.
- Exact conditional expected Random@30 and hindsight Oracle@30 were also computed by each frozen Base on the same heldout event-level target utility arrays, **as secondary retrospective references**, not preselected deployable random or Oracle algorithms.
- For the primary seed, the hindsight budget Oracle@30 is **0.388135 SASRec / 0.391644 GRU4Rec**, substantially above the Utility policies. The available positive per-event utility is far larger than what the present DEV-trained gate captures. Oracle is label-using and cannot be deployed.
- The previously validated DEV **warmed microbenchmark** is unfavorable to any claimed net speedup: Always Memory mean 0.803 ms vs Utility selective ~1.802 ms per event on 256 sampled DEV events; excludes live ingestion, history maintenance and network. The 30% *expert-call* constraint is not established as a real *compute budget*. Thus the paper should explicitly define what scarce resource, if any, is genuinely limited; absent such justification, reviewers may see selective routing as unnecessary in this specific M3 regime.
- The test is a **new observation period** and globally forward-time cohort, not verified person-disjoint and not directly comparable in absolute NDCG with original KuaiLive room ranking. Prequential earlier-TEST histories are a stated protocol condition, not trained TEST labels or cross-sectional holdout blindness. Report this prominently.
- TEST method uses consistent target-blind full-active top10 ranking with score ties resolved by smaller author ID. Original prior G3 Memory verifier counted score differences within 1e-12 as ties; if this threshold distinction is material, quantify only using DEV or report an explicitly non-confirmatory robustness note. Do not change the TEST algorithm to improve results after label revelation.
- All event data/model bytes are on User-host; public GitHub receives only aggregate manifests, checksums and summary statistics. No TEST-based model refits, label-informed early stopping, threshold changes or selective result omission occurred.

## 5. KBS editorial conclusion and remaining paper work

**Scientific E1/E2/E3 packages are complete under the frozen Plan C protocol**, with independently forward-time TEST results for two Base architectures × three fitted seeds × five fair gate objectives and preregistered paired statistics. Main paper positioning: *predicting the incremental value of a fixed relationship-memory expert relative to a frozen incumbent is a useful decision signal when expert invocation is limited*. New M3 TEST data show stable direction and magnitude for the preregistered contrasts.

**However the efficiency/necessity challenge remains:** The expert alone was *both more accurate* than Utility and *cheaper in the limited warmed replay* in this regime. This is not a reason to conceal findings, but it is a genuine limit of deployment economics, and motivates a clear resource/accuracy formulation or multi-regime discussion. Do not infer "selective system reduces latency" or "Utility dominates Always Memory".

Recommended next action is **manuscript integration and independent referee-style synthesis**, not new tuning against TEST. All TEST evidence must be locked and any follow-up experiments declared exploratory and separate from the frozen confirmatory claim.
