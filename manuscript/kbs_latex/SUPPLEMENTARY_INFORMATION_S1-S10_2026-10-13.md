---
title: "Supplementary Information"
subtitle: "Candidate-Regime Supervision for Selective Relationship Memory Use in Live-Streaming Recommendation"
author: "Anonymous manuscript — Knowledge-Based Systems"
date: "21 October 2026"
fontsize: 9pt
geometry: margin=0.76in
colorlinks: true
linkcolor: black
urlcolor: blue
toc: true
toc-depth: 1
header-includes:
  - \usepackage{microtype}
  - \setlength{\emergencystretch}{3em}
  - \sloppy
---

**Scope.** This manuscript-specific supplement supports claims C1–C3 across three distinct protocols: Twitch/LiveRec streamer ranking (44,221 frozen TEST events), original KuaiLive room ranking (10,222 previously examined paired target events), and KuaiLive-M3 full-active author ranking (47,575 forward-time frozen TEST events from 12,533 users). Twitch and M3 offer **two separately fitted and frozen specialist-selection TEST evaluations**; the original KuaiLive room study supports retrospective candidate-regime diagnostics, not a third independent selection TEST. All observations are conditional on the declared Base, target unit, candidate universe and time protocol.

**Statistical convention.** Unless stated otherwise, percentile bootstrap intervals condition on the evaluated user cohort, fitted model, candidate set and frozen policy. Twitch and original KuaiLive retain their original resampling and retrospective scopes. New M3 TEST evidence includes 5,000 user-cluster paired bootstrap resamples and 5,000 user-cluster sign randomizations under an approximate sign-symmetry null; three predeclared comparisons are Holm-adjusted **within each of six fitted Base/seed conditions**, not in one global family of 18 tests. Training seeds, sampled candidate draws and user-cluster replicates must not be mistaken for independent population replications. M3 thresholds share a maximum-30%-on-DEV selection rule; TEST invocation fractions are not necessarily equal or capped.

**Access.** The public [KuaiLive dataset](https://zenodo.org/records/16565801) and [LiveRec/Twitch repository](https://github.com/JRappaz/liverec) are governed by their own access and redistribution terms. The companion [research-code repository](https://github.com/mzch0210/KuaiLive-Agent) documents the protocols, model provenance and aggregate results. Derived event-level TEST rankings, processed event bundles and checkpoint weights are not currently represented as stable public downloadable research objects; workflow artifacts may expire and are not permanent archival records. Any future deposit, redistribution permission and final data-availability wording require verification and approval by the responsible author.

---

# S1. Data sources, event construction, and temporal eligibility


### S1.1 Public provenance and study populations

The experiments use **KuaiLive** (Qu et al., SIGIR 2026; public release at [Zenodo record 16565801](https://zenodo.org/records/16565801), code and documentation at [the dataset repository](https://github.com/imgkkk574/KuaiLive)) and the public **LiveRec/Twitch** dataset (Rappaz, McAuley, and Aberer, RecSys 2021; [original repository](https://github.com/JRappaz/liverec)). These are distinct datasets, not exchangeable replications of one experiment. No privately sourced viewers, user surveys, or collected business outcomes are used.

The **KuaiLive original public dataset** describes clicks and other live-room activity, room-session start/end timestamps, and a mapping from time-bounded rooms to persistent streamers. These source-level numbers are **not** identical to the analyzed cohort. The eligible **study cohort** consists of **10,222 users**, each with one development and one test target selected after filtering and deduplication. The training prefix precedes the last two retained interactions for each user. The penultimate interaction is DEV; the last is TEST. Earlier DEV events become eligible history before the TEST target, whereas the global creator-popularity prior is calculated from the training portion only. Personal attributes in the original public dataset are not interpreted as user-preference outcomes in this study.

The **Twitch LiveRec source** was assembled from ten-minute snapshots of observable chat/viewer activity. Start and stop fields denote the first and last *observations*, not guaranteed physical entrances/exits. Availability and repeated streamer consumption follow the LiveRec protocol. The filtered study event panels contain **46,878 DEV** and **44,221 frozen TEST** single-target events. Twitch's primary sequential Base has maximum history context **L=16**. The raw LiveRec source documents a 100k-user benchmark subset and a wider observation dataset; cohort counts here refer only to the processed experimental split and should not be labeled original dataset totals.

### S1.2 Decision-time information boundaries

For a user u and step t, the event's observed relevant creator/room y is used **only for retrospective evaluation, target-state characterization, and DEV supervised training**. The selectable feature vector is constructed without observing y. Eligible history contains prior interactions under the canonical dataset-specific time rule, and candidate availability is reconstructed at the corresponding decision time.

**KuaiLive:** an active room has `start_timestamp ≤ t < end_timestamp` (half-open interval). Native sampled-active evaluation places the observed positive room alongside **574 distinct contemporaneously eligible non-target rooms**, uniformly sampled without replacement under its frozen sampler. Thus 575 is **total candidates, positive included**; “negative” means *not the currently observed positive*, **not necessarily never previously interacted with**. An explicit audit finds 433 of the original 10,222 users have at least one original sampled negative room occurring in their earlier interaction history. Full-active ranks eligible rooms at the same instant while retaining an observed positive if its recorded session availability is inconsistent. In the fixed-checkpoint P0 and P2 replays the sampled set is a subset of its matching full set; no target is duplicated. Candidate size and membership, consequently the score-normalization reference and ranking difficulty, change across regimes.

**Twitch:** candidates are streamers available at the ten-minute crawl step. A pre-target record enters the canonical relationship history if its recorded observation start is strictly before the target step; the training-only popularity prior requires training-eligible records. A stricter split-end eligibility criterion was analyzed as a separate **sensitivity**, not substituted for the canonical test definition. Due to the ten-minute data resolution, the manuscript makes no stronger claim about exact human session timing.

The diagnostic evidence states are computed **after** y is observed: *represented* if target creator occurs in the Base's input window; *recoverable-but-unrepresented* if only older eligible history contains the creator; *unavailable* otherwise. They are mutually exclusive, exhaustive, target-relative analysis groups—not deployable selector inputs, and “represented” is not evidence that an internal embedding encoded the relationship.

### S1.3 KuaiLive-M3 global forward-time author protocol

The M3 study is **not** another room-level evaluation of the original 10,222 KuaiLive targets. Its ranked unit is the persistent author_id, while room activity determines availability; source room-session identities are not equated with the old release's internal creator identifiers. The locked global temporal boundaries are **TRAIN before 2026-03-23 12:00:00**, **DEV from this point until 2026-03-27 14:00:00**, and **TEST from 2026-03-27 14:00:00 onward**, using the dataset's timezone-naive recorded clock consistently without claiming a UTC offset. The indexed TRAIN pool contains **24,995,148** interactions, with deterministic, outcome-independent post-eligibility selection yielding **50,049 DEV** and **47,575 TEST** requests, of which TEST represents **12,533 users**.

M3 requires at least two earlier observations and a TRAIN-known target author. At event time, candidates comprise distinct TRAIN-known authors currently represented by at least one active live room; this is an **author-level full-active roster** (TEST mean **32,166.632**, median **31,065**), not 575 sampled candidates. A **4,096-event × 575-author DEV** panel is separately used for neural checkpoint selection, not for final TEST scoring or a replicated old-room candidate-regime intervention. M3 uses global time-forward split and does **not** assert disjoint users across TRAIN/DEV/TEST.

History is processed prequentially in observed time and source-order ties: strictly earlier TRAIN/DEV and already observed earlier TEST-period events can update subsequent target-free user histories, including earlier TEST observations outside the sampled evaluation cohort. Neither the current selected target nor any future target is available to Base, Memory or the gate before its prediction. The author Base uses its frozen input representation of previous eligible TRAIN-known authors (context length 16). Fixed Memory uses the latest ten **all-author** prior interactions for Short and all historical author occurrences for Long, including earlier authors unseen during TRAIN, which occupy recency positions and contribute to the maximum historical normalization count even though they cannot be ranked as current candidates. Memory weights remain **Short 0.45, Long 0.45, TRAIN-only popularity 0.10**.

The scientific G0F intent lock describes a DuckDB hash over user, author, room, timestamp-in-milliseconds, source event identifier and seed. The final G1 executable deterministic cohort used DuckDB's **typed-timestamp** hash input rather than a literal timestamp_ms transformation. This implementation difference is a provenance qualification, not proof of byte-identical conformance with the initial expression. The locked final G1 protocol SHA256 is **bf6234eb95ecb24a568b2e7556846c41c4f3e1fdcd7774397003beaf56341a3c** and TEST cohort SHA256 is **e60da60672ea1921dd3a5fccfb0aa76a3a06d50834e8080a07b2465777c9bdb1**. The resulting cohort and hashes were frozen before TEST outcomes were evaluated, with no target-based changes.

Source: [G0F lock](https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/G0F_PRETEST_PROTOCOL_2026-10-12.json), [six-fit G5 frozen registry](https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/G5_PRETEST_SIX_BASE_FROZEN_REGISTRY_2026-10-12.json) and [G5 chronological held-out procedure](https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/G5_ONE_SHOT_HELDOUT_EXECUTION_PROTOCOL_2026-10-12.md).

### S1.4 Candidate and identity validation

KuaiLive predicts rooms, but relationship Memory aggregates prior events by the mapped streamer; several candidate rooms can therefore share a specialist score. Twitch ranks streamers directly. Deterministic item identifiers break score ties. Source-file train/DEV/TEST byte hashes, matched cohort identity, historical model mappings, and session eligibility guards are pinned in **S2/S5**. Raw public data and derived processed candidate lists should not be treated as the same downloadable artifact; the derived lists are reconstructable only with the documented code, preprocessing and fixed RNG choices.

For the original KuaiLive P0 files, SHA256: **train** `ad91413537175b9f6e9013c525a552b6004cc00e029b41360f08519e0735b5b4`; **DEV** `46dd3081688468c89acf6366d36d87c122fa45850ddb69320c05da9de94a9f54`; **TEST** `3491862df4de5cfb487fbd21c2f62c2d1d62acac110f852cc83c019dfcc6e956`. These fingerprints identify the **P0 processed Room files**, not checksums for the original Zenodo dataset archive or all platform variants. They were checked from [source artifact 11534262601](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37741843252/artifacts/11534262601).

### S1.5 Evidence and access statement

Data-provenance evidence: [KuaiLive official dataset repository](https://github.com/imgkkk574/KuaiLive), [KuaiLive Zenodo record](https://zenodo.org/records/16565801), [LiveRec original repository](https://github.com/JRappaz/liverec), [KuaiLive active-room exporter](https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n12-single-thesis-restructure-plan-20261014/src/kuailive_agent/export_rechorus_room.py), and the [P2 source-pinned eligibility audit](https://github.com/mzch0210/KuaiLive-Agent/blob/main/manuscript/kbs_latex/SECTION6_STAGE3_3A_FEASIBILITY_AND_SCIENTIFIC_BOUNDARIES_2026-10-10.md). The original datasets' access and license conditions govern further distribution. This supplement references public repositories and **does not redistribute proprietary or anonymized raw interaction files**. Preserve the precise derivation pipeline rather than infer fields or raw source SHA values not available in the evidence records.

**Boundary:** KuaiLive post-hoc TEST analyses and Twitch frozen one-shot TEST serve **different evidentiary purposes**. No source cohort is a random sample of all live-streaming platform users. These protocol definitions are observational; neither a sampled non-target nor a lack of recorded history proves negative preference or true ignorance.

### S1.6 Data availability and archival status

The publicly cited LiveRec and KuaiLive upstream releases remain subject to their own access and redistribution terms. The companion repository provides reproducibility code, methodological records, aggregate evaluation results and checksum manifests. Derived event-level TEST rankings, processed source bundles and checkpoint files have not been published as stable downloadable research objects. Workflow artifacts are time-limited; a workflow identifier is not equivalent to a persistent data deposit.

A future stable reproducibility release should include a versioned code/environment snapshot, verified upstream source revisions, deterministic cohort and candidate-building rules, model and policy SHA256s, and appropriately shareable processed outputs or a documented restricted-access procedure. Any deposit, DOI or permission to redistribute derived interactions requires a separate factual check and author approval; none is claimed at this stage. For the final journal submission, specify public upstream sources separately from unavailable derivative files in a precise Data Availability Statement. The journal-specific requirements must be checked against the final Knowledge-Based Systems Guide for Authors. Elsevier's current general [supplementary requirements](https://www.elsevier.support/publishing/answer/what-are-the-requirements-for-my-supplementary-material) and [research-data guidance](https://www.elsevier.com/researcher/author/tools-and-resources/research-data) inform, but do not replace, those journal-specific requirements.

---

# S2. Model training, frozen evaluation, and artifact provenance


### S2.1 Freeze hierarchy and fit/evaluation boundary

This supplement records **what was fixed, when it was scored, and which comparisons may use post-outcome information**. A source or workflow date is an archive provenance datum, **not** a substitute for an independently timestamped preregistration.

**Table S2.1. Evidence-tier and training/freeze boundaries.**

| Evidence tier | Dataset | Fit/selection information | Evaluation status | Appropriate scientific claim |
|---|---|---|---|---|
| Primary pointwise Utility policy | Twitch/LiveRec TEST, 44,221 events | LiveRec Base and DEV-trained 14-feature Utility estimator; threshold chosen on 46,878 DEV OOF events | **Single frozen TEST evaluation** | Conditional selector value versus matched Base; retrospective Difficulty at realized call count |
| DEV-only sensitivity panels | Twitch DEV, 46,878 events | Existing OOF vectors and fixed ranking models; separate retrained context Bases when specified | **Development-only exploratory diagnosis** | Subgroup patterns, observed finite-grid sensitivity |
| Original/native and fixed P0/P1 candidate comparison | KuaiLive previously studied TEST, 10,222 users | Regime-native trained models or explicitly frozen seed-20260918 checkpoint pair; frozen candidate lists | **Post-hoc matched diagnostic** | Candidate-protocol dependence, descriptive 2x2 score allocation |
| Additional P2 negative draws | Same KuaiLive TEST users | Frozen original P0 checkpoints and Memory, 3 prespecified RNG streams × 3 sizes | **Retrospective sampling sensitivity** | Directional stability over the 9 inspected lists |
| Efficiency replay | Separate KuaiLive cached sampled-active CPU workload | Warm cached histories and archived event-level route masks | **Controlled component timing only** | Measured scoring overhead, not production latency |
| Independent frozen M3 policy TEST | M3 author ranking, 47,575 later-period TEST events / 12,533 users | SASRec + GRU4Rec × three trained seeds; five pointwise objective-specific policies and thresholds DEV-frozen before label-blind TEST | **One-shot frozen TEST** after outcome-blind G5-A ranking | Relative-utility decision gains, actual TEST call fractions and within-fit three-Holm tests |
| M3 RTX 3090 warmed DEV replay | 256 prespecified M3 DEV author-ranking requests | Frozen primary SASRec, fixed Memory and DEV Utility gate | **Controlled offline component/path timing** | Unconditional Memory is faster in this measured path; not production end-to-end cost |

No Twitch TEST labels enter the fitted Utility threshold, ranking features or its pointwise decision. The observed frozen TEST invocation count (**6,650 of 44,221; 15.04%**) is a *post-selection statistic*. Difficulty orders its scores retrospectively across the same TEST batch to match that count. The hindsight Oracle alone uses observed TEST utility labels. Neither comparator supplies an independently frozen online fixed-budget guarantee.

### S2.2 Twitch model and utility estimator details

The designated Base uses the official availability-aware LiveRec architecture with context/repeat components enabled, Base context **16**. The fixed Memory expert has normalized Long interaction counts, Short maximum recency-decayed strength over the most recent **10** eligible user–creator events (decay 3), and training-derived normalized log popularity, combined **0.45/0.45/0.10**. The Utility regressor is histogram gradient boosting with **maximum** 200 iterations, learning rate **0.05**, depth **3**, minimum leaf **50**, L2 regularization **1**; **14** observable features comprise six history and eight Base-score summaries. The maximum configured iterations must not be confused with **81 fitted trees** reported for a separately measured KuaiLive HGB CPU benchmark.

Five-fold **out-of-fold DEV** predictions were constructed with one target per user and shuffled KFold (original seed **20260918**). The threshold was chosen by DEV ranking-utility policy performance, ties favoring fewer Memory calls, then frozen for the one-shot TEST evaluation. The original DEV historical operation selected **6,563 / 46,878** events, not the **6,650** invocations observed subsequently on TEST. The 5%, 10%, 15%, 20% and 30% grid in S7 simply **replays existing DEV OOF scores** and does not retune the frozen TEST threshold.

Original source-of-record evidence:
- [DEV fitted Utility/Difficulty run 35698158121](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35698158121), [artifact 10680854557](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35698158121/artifacts/10680854557).
- [Frozen one-shot TEST run 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303), [result artifact 10684864297](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303/artifacts/10684864297).
- [DEV feature/Memory originals run 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454), [artifact 10688746451](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454/artifacts/10688746451).

The frozen TEST one-user bootstrap uses **5,000** paired percentile resamples, conditional on trained models, threshold and exact selection. It excludes threshold/model fitting and feature selection uncertainty; the DEV OOF grid does not constitute another independent test.

### S2.3 KuaiLive fixed-P0 versus native-policy checkpoint identities

The designated Dual-ID Base consists of two SASRec encoders (room and streamer identities), each with 64-dimensional embeddings, one attention layer, four heads, maximum history 50; their scores are separately z-standardized over the eligible candidates before a linear fusion. **Different protocols must retain different fit provenance**: the native sampled policy reports a development-selected room coefficient **0.1**, whereas the **P0/P1/P2 paired candidate experiment freezes** a sampled-development-selected coefficient **0.125**; native and paired Base NDCG values are therefore **not interchangeable**. Never assume an auxiliary KuaiLive 0.61714 Base checkpoint matches the paired P0 0.60709 checkpoint.

**Table S2.2. KuaiLive fitted checkpoint fingerprint table.**

| Paired KuaiLive checkpoint seed | Room-SASRec checkpoint SHA256 | Streamer-SASRec checkpoint SHA256 | Training identity |
|---|---|---|---|
| 20260918 | `b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7` | `82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945` | Original replayed P0 model pair |
| 20260919 | `395d1b1c881d20cbda5d24c36c30685fd1524a0ec98586c8c71ad7c245505b2a` | `9f1b11cf27e0c802f71bb8b1bef646bb392b28d560e3aabda03f36fe01e2b637` | P1 newly fitted pair |
| 20260920 | `84c4ef5e45592fc480096dfe4e501046ede37c1f936484ed83f3bd56e1f49191` | `7043b275b56a75fd5d7aeadfd7e69d5447128ce9f55f3bd6a0f275a24dd2d144` | P1 newly fitted pair |

The first model pair and processed train/DEV/TEST inputs were independently rehashed from archived original file **bytes**, and each of **10,222** event-level sampled/full Base and Memory outcomes was reproduced before P2 generated any new candidate lists. Three fitted training seeds share the **same users** and report across-initialization SD rather than independent sample replication. For detailed estimator outcomes and source identifiers, see S5/S8.

- Original training/paired factorial run: [37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645), [factorial artifact 11538678848](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538678848); original source model/data artifacts [11536890439](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476/artifacts/11536890439), [11534262601](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37741843252/artifacts/11534262601).
- Original ReChorus code revision **c164ec4303cc20ddcfbd1b57de366a481811d1e5** for the fixed experimental pipeline.
- P2 code [analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py); execution [38014145900](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900) with [result artifact 11655273833](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900/artifacts/11655273833).

**Completeness limitation:** A matched SHA256 for **every historical native-policy Twitch/KuaiLive Base checkpoint** is not established by the source files examined in the project ledger. The exact checkpoint identities listed above apply to P0/P1/P2, not all historical native-policy baselines. Missing upstream hash entries are **unverified**, not assumed equal to any existing model.

### S2.4 KuaiLive-M3 source, training and prospective policy freeze

Six independent author-encoder fits use **SASRec** and **GRU4Rec** with three prespecified training seeds each (20261012, 20261013, 20261014), 64-dimensional author representations and context length 16. Each checkpoint was selected from the 4,096-request, 575-author DEV screening panel; a separate **50,049-event full-active DEV** panel supplies group-disjoint five-fold OOF gate fitting and threshold selection. Three supervised histogram gradient-boosting models predict respectively specialist-minus-Base event NDCG@10, negative Base event NDCG@10 and standalone specialist event NDCG@10. Two deterministic objectives use the negative Base top-score margin (Uncertainty) and prior interaction count (History). All use the same **12 pre-outcome features** when appropriate: five Base-score summaries and seven history/candidate summaries; the specialist-support share can be determined from prior histories and eligible authors without first executing the full Memory scorer.

For each of the five objectives, a pointwise score threshold is frozen after maximizing DEV OOF selection gain under **at most 30% DEV Memory invocations**, selecting all tied threshold scores together. Actual TEST invocations are not constrained to the same percentage. G5-A [action 38225946950](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38225946950), private event-level outputs retained on User-host, scored all six frozen Bases and the same fixed Memory into seven **target-blind Top-10** lists per event; no current target label, event-level TEST NDCG or model/threshold tuning was available to this step. Its output manifest recorded frozen prediction/checkpoint digests (artifact **11736962620**). The subsequent G5-B [action 38226690320](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38226690320) read target labels once, verified frozen input digests and computed the full TEST metric/inference aggregate (artifact **11735868084**). The original G5-A registry SHA256 is **39217c59f54f133fea8c7c0e1691ebc32c7082a53a7452c10f16a25fd48ad29c**. No TEST-based threshold changes, omitted user requests or favorable seed selection occurred.

**Table S2.3. M3 independent Base checkpoint and policy-threshold file SHA256s.** These fingerprints denote source bytes of six checkpoint files and six DEV-frozen threshold JSON files, respectively; three supervised gate-model SHA256s per fit are individually retained in the [complete frozen registry](https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/G5_PRETEST_SIX_BASE_FROZEN_REGISTRY_2026-10-12.json).

| Model / training seed | Base checkpoint SHA256 | Five-policy threshold JSON SHA256 |
|---|---|---|
| SASRec 20261012 | 18fb25d68970e73661a4b1418f5be05e7f8bed678d097533adf3cf1d9964d17e | 1aeaf5451d8dbf77dab423159f364e57911cfce286861f01c71c526d25dab2f7 |
| GRU4Rec 20261012 | 6c83dcb2e76f86e1018af467c0b0494f09b5d552c885700e92ea657cd9cc8d1a | 45f48d75d49963392c8b10f3e04b965263881f5575b54ac5a9de1ebe08168b75 |
| SASRec 20261013 | bb627ec2cc39313548c1eff64583aac4a010847967e595bdace01de4c8dabd32 | 7f2e51c212e7fd4a049f57c36e44cc6ba73b7b0a8fe2d66e6d0f5749a578eedf |
| GRU4Rec 20261013 | 6847482a2a4722b5a324be20ffc8960030d6367942c3d0f21ef53db7f1d75128 | 68df8647912ee97147b043c3a3c6a70237fb70ca4c0f5779da45c05bdeda3708 |
| SASRec 20261014 | ab60a3d71cfd007b74296b5bb16bb95927d03a167c9e8d7d2fedc5995f2acd84 | 1221d45961e6c8d59a006ff92dade5ffd98f7a05ba415af5e368addac264af9d |
| GRU4Rec 20261014 | afb11b7ae7d4fad1b60545649461992dd064b0370a72904cc4337b880f0e3ad0 | e151e39c3d5ce6c76481f0af2a88a24f2a55d6efdc4d12ddfd56351897179bdd |

The G5-A full-roster ranking resolves numerical score ties by exact score equality and ascending author identity among tied authors. Earlier DEV/other ranking implementations used a tolerance on near-equal scores in some checks. These are protocol-specific frozen conventions, not retroactively normalized after TEST outcomes. Target-defined relationship states and hindsight Oracles never enter the prospective policy's features or decisions.

### S2.5 Statistical freeze checklist

All performance results are NDCG@10 computed over one positive target per evaluated event, with HR@10 secondary where shown. Mean *paired* differences are calculated on the **same** users within a protocol. Twitch TEST intervals: 5,000 paired-user bootstrap resamples. KuaiLive P0/P2: 3,000. One user-target per protocol row permits user bootstrap; if global-time panels contain repeated users, user-cluster resampling is required. The S4/S7 DEV intervals condition on observed target-defined group membership, OOF scores, the event-ranking masks and their selected budgets. No reported pointwise CI is a multiple-comparison-adjusted simultaneous confidence region.

The integrity target is **claim-to-artifact reproducibility**, not unrestricted access to private model training hardware. GitHub Actions artifact retention is finite; the appendices report run IDs, SHA values where verified, and reconstruction code but do not promise a permanent archival DOI unless one is actually minted.

---

# S3. Designated Base and auxiliary comparator performance under bounded training protocols


### S3.1 Purpose and comparison policy

This appendix documents why the designated sequential Bases are credible operational references for the scientific estimand **Memory minus a fixed Base**, rather than claiming they are universally optimal recommenders. KuaiLive and Twitch have different tasks, item units, architectures, histories and availability protocols; **never compare their absolute NDCG values as if they were one leaderboard**. Within-platform comparisons are reported only at the corresponding candidate and event protocols. Auxiliary model training budgets differ; this table is descriptive and not an exhaustively tuned state-of-the-art contest.

### S3.2 Twitch DEV: same frozen users/targets/candidates

All four rows below correspond to the same **46,878 Twitch DEV events**, with strict-before-target history reconstruction. Auxiliary small sequential architectures were trained for **five epochs** under a restricted BPR-based configuration; they are **not** proven equivalently tuned or directly comparable in capacity with the official LiveRec model.

**Table S3.1. Twitch same-event DEV baselines.**

| DEV method | NDCG@10 | HR@10 | Role/qualification |
|---|---:|---:|---|
| Official LiveRec Base | **0.571853** | **0.749712** | Designated frozen reference, context plus repeat component |
| GRU4Rec-small | 0.257268 | 0.387623 | Auxiliary BPR-trained model, five training epochs |
| SASRec-small | 0.171488 | 0.272260 | Auxiliary BPR-trained model, five training epochs |
| Popularity | 0.085889 | 0.145932 | Non-personalized baseline |

The frozen LiveRec pipeline's 46,878 matched user/target/step triples were reconstructed without identity mismatches; score comparisons use the same target and availability-aware candidates. Primary source: [Twitch comparison run 35815886641](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35815886641), [archived structured results 10732332430](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35815886641/artifacts/10732332430), files `twitch_dev_strong_base_benchmark.csv` and `.json`. The original source JSON explicitly says the smaller architecture alternatives are not exhaustive reproductions.

### S3.3 KuaiLive: same frozen evaluation protocol, distinct from paired P0

The comparison below is an **independent KuaiLive strong-reference panel** evaluated under its own matched active-room 575-candidate protocol. It **does not reuse** the P0/P1 room/streamer checkpoint pair of the §6.3 factorial study. For newly trained GRU4Rec and ContraRec–BERT4Rec, the configuration was selected **by DEV NDCG@10**, and TEST was intended for reporting only. Learning-rate configurations were limited and unequal across models.

**Table S3.2. KuaiLive matched 575-candidate baselines.**

| KuaiLive method | DEV NDCG@10 | TEST NDCG@10 | Experimental role |
|---|---:|---:|---|
| Dual-ID SASRec, auxiliary benchmark checkpoint | **0.621344** | **0.617142** | Designated benchmark Base in this separate panel |
| Streamer-SASRec component | 0.611519 | 0.609928 | Within-panel encoder branch |
| ContraRec–BERT4Rec | 0.4054 | 0.3703 | Limited grid, selected configuration lr=0.0005, best epoch 30 |
| Room-SASRec component | 0.355284 | 0.315369 | Within-panel encoder branch |
| Popularity | 0.296755 | 0.289446 | Same-protocol nonpersonalized ranking |
| GRU4Rec | 0.2788 | 0.2716 | Limited grid, lr=0.0005, best epoch 1 |

The full-precision original metrics are archived, and displayed values are rounded to avoid false numerical precision for parsed trainer logs. Source: [comparison result 35820514662](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35820514662), [artifact 10733131820](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35820514662/artifacts/10733131820), files `kuailive_strong_base_benchmark.csv`, `.json`, and `RECOVERY_PROVENANCE.json`. The GPU training occurred in [run 35814173574](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35814173574); the later result recovery parsed immutable logs after the first controller's metric parser failed on a punctuation detail. It **did not retrain models**. Full rerunnable training commands and original logs should accompany any separately deposited reproduction archive.

### S3.4 M3 six-fit designated author-incumbent reference

The M3 study uses two author-level Base model families, **SASRec and GRU4Rec**, trained independently with the same three stated seeds. Both output rankings over the exact same full-active TRAIN-known author roster as fixed Memory, and all five gate policies select among these matched rankings. They are **designated reference incumbents**, not an exhaustive globally optimized benchmark. They are also distinct from the old original KuaiLive Dual-ID *room* Base (whose 575-candidate P0 sampled TEST NDCG is 0.6070916) and from the auxiliary KuaiLive 575-room baseline panel in Table S3.2.

M3 frozen TEST Always Base NDCG@10 across the six fits is **0.258004, 0.260033, 0.258811, 0.260649, 0.258673 and 0.258400** (ordered by training seed and model family as in Table S8.4). The same fixed author-Memory NDCG@10 is **0.346792** in all six cases. This stronger unconditional Memory reference must be shown alongside the budget-calibrated Utility results; it is not evidence of state-of-the-art absolute recommendation performance. The 4,096 × 575-author DEV checkpoint panel does not establish full-active M3 TEST comparability with the old 575-room benchmarks.

### S3.5 Preventing cross-protocol baseline misidentification

**Table S3.3. Non-equivalent KuaiLive Base checkpoints.**

| Experimental comparison | KuaiLive sampled Base TEST NDCG@10 | May be paired with P0 Memory 0.565887? |
|---|---:|---|
| Native/historical sampled-active policy | **0.60784** | **No**, different training/fusion protocol |
| Separate reference competitiveness bundle | **0.617142** | **No**, different checkpoint |
| Matched candidate P0 source, 20260918, α_room=0.125 | **0.6070916** | **Yes**; P0 sampled Memory = 0.5658875 |
| P0 matched full-active | **0.3857124** | **Yes**; P0 full Memory = 0.4320191 |

Different score normalization/reference candidate sets also prevent swapping sampled/full Base scores in a single event-level paired difference. The P0 event-level contrast must be computed with its original checkpoint, candidate universe and score-standardization rule: **−0.041204 sampled, +0.046307 full, shift +0.087511**.

**Reviewer-relevant boundary:** Under unequal training budgets, these checks support a designated reasonable fixed Base, not a claim that every comparator has been equivalently optimized or that the method is state of the art. Rerunning all baseline grids is not necessary for the paper's restricted Base-relative estimand, but a future broader SOTA claim would require a separately designed tuning-fair benchmark.

---

# S4. Memory component and history-horizon diagnostics

## S4.1 Specification and reproduction

We replay the following fixed-scoring specialist rankings on identical available-streamer candidates: Popularity only (training-only normalized log-popularity); Short only (last 10 pre-target user–creator events with exponential recency decay); Long only (historical creator-specific count divided by the highest such count for that user); Short+Long (equal weights; ranking-equivalent to the 0.45/0.45 coefficients without popularity); and frozen Full Memory (0.45 Short + 0.45 Long + 0.10 Popularity). The original archived evaluator reproduced the frozen Full Memory ranks, NDCG@10 and HR@10 **with zero mismatches**, as well as candidate counts and history lengths.

Represented, recoverable-but-unrepresented and unavailable states use the **observed target**, making them retrospective groups rather than features available to a deployment selector.

## S4.2 Complete DEV component results

**Table S4.1. DEV component scoring by target-evidence state.**

| Target history state | Events | Ranker | NDCG@10 | Base | Ranker−Base | 95% paired bootstrap CI |
|---|---:|---|---:|---:|---:|---|
| Overall | 46,878 | Popularity only | 0.08589 | 0.57185 | −0.48596 | [−0.48989, −0.48193] |
| Overall | 46,878 | Short only | 0.39574 | 0.57185 | −0.17612 | [−0.17928, −0.17303] |
| Overall | 46,878 | Long only | 0.52761 | 0.57185 | −0.04424 | [−0.04722, −0.04130] |
| Overall | 46,878 | Short+Long | 0.52081 | 0.57185 | −0.05104 | [−0.05393, −0.04825] |
| Overall | 46,878 | Full Memory | 0.52170 | 0.57185 | −0.05016 | [−0.05307, −0.04741] |
| Represented | 24,541 | Popularity only | 0.10554 | 0.85972 | −0.75417 | [−0.75839, −0.74993] |
| Represented | 24,541 | Short only | 0.74451 | 0.85972 | −0.11521 | [−0.11959, −0.11076] |
| Represented | 24,541 | Long only | 0.84720 | 0.85972 | −0.01251 | [−0.01549, −0.00952] |
| Represented | 24,541 | Short+Long | 0.84671 | 0.85972 | −0.01300 | [−0.01599, −0.01003] |
| Represented | 24,541 | Full Memory | 0.83977 | 0.85972 | −0.01995 | [−0.02307, −0.01693] |
| Recoverable | 5,879 | Popularity only | 0.07861 | 0.30201 | −0.22340 | [−0.23230, −0.21448] |
| Recoverable | 5,879 | Short only | 0.01293 | 0.30201 | −0.28908 | [−0.29699, −0.28092] |
| Recoverable | 5,879 | Long only | 0.63890 | 0.30201 | +0.33688 | [+0.32767, +0.34628] |
| Recoverable | 5,879 | Short+Long | 0.58673 | 0.30201 | +0.28471 | [+0.27585, +0.29355] |
| Recoverable | 5,879 | Full Memory | 0.53298 | 0.30201 | +0.23097 | [+0.22177, +0.24036] |
| Unavailable | 16,458 | Popularity only | 0.05918 | 0.23900 | −0.17982 | [−0.18475, −0.17486] |
| Unavailable | 16,458 | Short only | 0.01242 | 0.23900 | −0.22658 | [−0.23127, −0.22197] |
| Unavailable | 16,458 | Long only | 0.01131 | 0.23900 | −0.22770 | [−0.23243, −0.22312] |
| Unavailable | 16,458 | Short+Long | 0.01131 | 0.23900 | −0.22770 | [−0.23243, −0.22312] |
| Unavailable | 16,458 | Full Memory | 0.04338 | 0.23900 | −0.19562 | [−0.20033, −0.19088] |

The above CIs are the **original 5,000-user-resample percentile intervals for Ranker−Base** within each fixed group. They are conditional on fitted rankings and retrospective group assignments, unadjusted for 20 comparisons.

## S4.3 Direct same-user paired variant comparisons

We additionally compare the original variant-specific NDCG@10 of the identical **5,879 recoverable DEV users**, rather than subtracting marginal CIs. The new 5,000-replicate user-paired percentile bootstrap uses seed 20261012. All 20 original mean Variant−Base results were reproduced within 1e−12 before the new pairing.

**Table S4.2. Paired component comparisons in recoverable DEV.**

| Recoverable DEV contrast | Mean difference | Conditional paired 95% CI |
|---|---:|---|
| **Long only − Full Memory** | **+0.10592** | **[+0.10096, +0.11061]** |
| Short+Long − Full Memory | +0.05374 | [+0.04956, +0.05792] |
| Long only − Short+Long | +0.05217 | [+0.04918, +0.05508] |
| Short only − Full Memory | −0.52005 | [−0.52720, −0.51288] |
| Popularity only − Full Memory | −0.45437 | [−0.46295, −0.44594] |

The Long-only versus Full Memory contrast is **negative** in the unavailable subgroup (−0.03208), underscoring state dependence rather than universal superiority.

## S4.4 Interpretation and uncertainty limits

The observed recoverable subgroup shows stronger performance for the long-history ranking variant than for the originally fixed Full Memory. However, changing component scores also changes candidate ordering, score ties and interactions among retained components. This is **not causal identification** of the information contribution of each term, not a newly selected expert, and not justification for modifying the previously frozen policy. The bootstrap keeps Base, group membership and variant scores fixed, excludes training and model-choice uncertainty, and is exploratory without multiplicity control. The scientific inference remains **operational and Base-relative** under the specified evaluation protocol.

## S4.5 Reproducibility

Original artifact input SHA256s:

- Event scores: `b84e187290a7df2918e3bd050c4ab0a6a2baac611f72eb72f8616c7634c0644b`.
- Original 20-row table: `cc97794c49431c547ccf08a29da96bc275a900ed78a9ae71674b748b05e0750a`.

All rows and new paired contrasts can be reproduced without training or TEST access using [the stage-2 DEV replay source](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_section6_stage2_dev_replay.py). The original rank-level arrays remain available in Actions artifact 10688746451. 


---

# S5. Paired candidate-regime factorization and fixed-checkpoint negative-draw sensitivity

## S5.1 Matched experiment identity and safeguard checks

We preserve **n=10,222** one-target-per-user KuaiLive evaluation events, the original Room- and Streamer-SASRec checkpoints from seed 20260918, eligible history, target timestamps, candidate availability logic, Memory rule and fusion coefficient (room 0.125; streamer 0.875). The complete full-active candidate set is defined at each event time; metadata reports that every observed target was active. The full-active set has **575–13,266 eligible rooms per event** (mean **8,269.11**, median **8,131.5**), with each positive target included exactly once.

The original fixed 575 protocol and full-active protocol are first reproduced **user by user**, comparing six archived event-level scores: sampled/full Base, sampled/full Memory, and their two differences. The original-data equality guard passes at absolute tolerance 1e−11; these results **must be replicated before** new sampling. Original model hashes: Room `b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7`, Streamer `82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945`; train, DEV and TEST dataset SHA256s are in the original P2 provenance manifest.

The negative-sampling pool follows the original exporter: **active eligible rooms except the current positive target**. It does not exclude all earlier user interactions; the original 575 lists contain prior-history negative intersections for 433 unique users. Changing this definition would alter the original tested protocol. New samples are uniform without replacement from this time-specific pool; the observed positive is always added. P2 samples only from the frozen **full-active score vectors** and does not retrain or re-encode any user per draw.

## S5.2 Original P0 matched factorial benchmark

For fixed original sampled candidates S (575 items including the target) nested in full-active F, the original paired contrast is:

**Table S5.1. Historical P0 candidate-reference 2×2.**

| Ranked candidate set | S z-score reference | F z-score reference |
|---|---:|---:|
| S | −0.04120411 | −0.04141760 |
| F | +0.04761085 | +0.04630669 |

Entries are mean **Memory−Base NDCG@10**. Native S/S uses Base 0.60709158 and Memory 0.56588746; native F/F uses Base 0.38571242 and Memory 0.43201911. The within-event F/F minus S/S difference is **+0.08751080** (original paired bootstrap 95% CI **[+0.08210,+0.09326]**, 3,000 user resamples). The two-order algebraic allocation is ranked-candidate membership **+0.08826963** and branch z-score normalization reference **−0.00075883**, summing exactly to the native shift. The crossed S/F and F/S configurations are **analytical**, not independent operational policies or causal interventions.

## S5.3 Prespecified new candidate-draw protocol

The P2 sizes and RNGs were committed before the first scored outcome: **128, 256, 575 candidate rooms including one positive**, with **three independent prespecified RNG streams** 20261010, 20261011 and 20261012 for each size. The **original 575 negative list** is separately preserved as a reference; full-active is the same fixed reference under all new draws. A total of nine new full-cohort candidate conditions were computed. Original checkpoints, Base/Memory logits, historical events, active-room eligibility, preprocessing and alpha remain unchanged. No seed, user or condition was selected based on its result.

A 3,000-resample user-paired percentile bootstrap (same user indices across compared policies) gives **pointwise conditional CIs** for each draw's Memory−Base mean and full-minus-sampled shift. These intervals condition on original models and observed users; they do not incorporate the choice of candidate sizes/draw seeds, hypothetical independent negative-draw distributions, model fitting or TEST selection. There is **no familywise multiplicity adjustment**.

## S5.4 All nine P2 outcomes

**Table S5.2. Nine predeclared P2 negative-draw results.**

| Sample size (positive included) | Draw seed | Base NDCG@10 | Memory NDCG@10 | Memory−Base | 95% CI for Memory−Base | F/F − sampled | 95% CI for F/F−sampled |
|---|---:|---:|---:|---:|---|---:|---|
| **128** | 20261010 | 0.726025 | 0.645648 | **−0.080377** | [−0.086764, −0.073864] | **+0.126683** | [+0.119936,+0.133530] |
| 128 | 20261011 | 0.726010 | 0.646158 | −0.079852 | [−0.086162, −0.073125] | +0.126159 | [+0.119471,+0.133256] |
| 128 | 20261012 | 0.726867 | 0.647608 | −0.079260 | [−0.085593, −0.072616] | +0.125566 | [+0.118770,+0.132659] |
| **256** | 20261010 | 0.675502 | 0.607702 | **−0.067800** | [−0.074253, −0.060869] | **+0.114107** | [+0.107907,+0.120613] |
| 256 | 20261011 | 0.676118 | 0.607526 | −0.068593 | [−0.075296, −0.061703] | +0.114899 | [+0.108514,+0.121534] |
| 256 | 20261012 | 0.674257 | 0.606676 | −0.067581 | [−0.074182, −0.060755] | +0.113888 | [+0.107533,+0.120214] |
| **575** | 20261010 | 0.607331 | 0.565142 | **−0.042189** | [−0.048747, −0.035141] | **+0.088495** | [+0.082897,+0.094078] |
| 575 | 20261011 | 0.607060 | 0.566137 | −0.040922 | [−0.047656, −0.033802] | +0.087229 | [+0.081500,+0.092836] |
| 575 | 20261012 | 0.606207 | 0.564586 | −0.041621 | [−0.048239, −0.034708] | +0.087927 | [+0.082273,+0.093542] |
| Original **575** | Original historical list | 0.607092 | 0.565887 | **−0.041204** | [−0.047850, −0.034175] | **+0.087511** | original P0 bootstrap: [+0.08210,+0.09326] |
| **Full-active** | Original complete population | 0.385712 | 0.432019 | **+0.046307** | [+0.039990,+0.053289] | 0 | — |

The original-575 and full-active CIs above are P2's **conditional resample** estimates except where the original P0 interval is expressly identified; the original-575 shift CI is from the original P0 rather than implying an independently fixed rerun confidence band. All signed P2 means have been recomputed directly from the archived **10,222 × 65** per-user outcome matrix, with no missing or duplicated events.

All **nine** prespecified sampled candidate means are negative and all F/F minus sampled means positive. Within each size, the between-draw mean (and min–max over just three draws) is:

**Table S5.3. P2 between-draw descriptive ranges.**

| Sampled size | Mean sampled Memory−Base across draws | Observed three-draw range | Mean F/F−sampled | Range of F/F−sampled |
|---|---:|---|---:|---|
| 128 | −0.079829 | [−0.080377,−0.079260] | +0.126136 | [+0.125566,+0.126683] |
| 256 | −0.067991 | [−0.068593,−0.067581] | +0.114298 | [+0.113888,+0.114899] |
| 575 | −0.041577 | [−0.042189,−0.040922] | +0.087884 | [+0.087229,+0.088495] |

These ranges are **descriptive**, not empirical 95% sampling-distribution CIs or independent dataset replicates; all runs reuse the same checkpoint and TEST users.

## S5.5 Scoring-reference allocation under independent draws

For each sample size and draw, the crossed 2×2 design satisfies the event-level algebraic identity $\Delta_{FF}-\Delta_{SS}=A_{\mathrm{membership}}+A_{\mathrm{normalization}}$.

Across the three fixed draws per size, the means of these **descriptive path-averaged terms** are:

**Table S5.4. P2 two-order algebraic allocation.**

| Sampled size | Candidate-membership allocation | Score-normalization-reference allocation | Net full-minus-sampled shift |
|---|---:|---:|---:|
| 128 | +0.129023 | −0.002887 | +0.126136 |
| 256 | +0.115923 | −0.001625 | +0.114298 |
| 575 | +0.088562 | −0.000678 | +0.087884 |

The allocation algebra is checked on **every original user and every new draw**, maximum numerical identity discrepancy on the order of machine epsilon. "Membership" encompasses count, which negative items are included, the available rank competition and consequent scoring task difficulty; this table **cannot causally separate** those mechanisms. Likewise, z-score-reference terms should not be conflated with a controlled rank-normalization intervention in the live system.

## S5.6 Interpretation for C2 and relation to related literature

This controlled fixed-checkpoint replay strengthens the **bounded** original C2 finding: the sign reversal between the specified sampled-active and full-active candidate regimes persists over the nine inspected negative lists across three positive-inclusive sample sizes. The result **does not** establish universality over all draws, user populations, models or platforms; repeated negative draws on the *same* events are not independent TEST replications. The shared full-active reference makes the sign check transparent, not an independent benchmark.

The known general fact that sampled ranking metrics can invert model orderings is due to prior work (Krichene and Rendle, *On Sampled Metrics for Item Recommendation*, CACM 65(7):75–83, 2022, DOI 10.1145/3535335; original KDD 2020). Our result is about the **observed Base-relative utility of a fixed interpretably scored relationship specialist on KuaiLive rooms**, not a new sampled-metric theorem, new gate training method, or causal attribution to sample count.

**Presentation in the main article:** The RQ1 candidate-regime result is summarized in the Results subsection on relationship value; this supplement retains the per-draw outcomes, confidence intervals, original-rank reproduction and factorization. The three alternative *training*-seed model realizations are reported separately in S8, not as nine new independent checkpoint seeds. The paired-draw estimates and the three independently trained checkpoint realizations address distinct sources of uncertainty.

## S5.7 Archive manifest and exact source protocol

- Original factorial run/artifact: 37751814645 / 11538678848.
- P2 source commit and run: d88222e924e6c66bdaf27cb1700fad8309284a05 / 38014145900.
- P2 archived artifact: **11655273833**, `kuailive-p2-frozen-candidates-38014145900`.
- `p2_predeclared_draws.csv`: all nine sample-size/seed condition means.
- `p2_user_bootstrap.csv`: fixed-draw 3,000-user-bootstrap conditional per-draw CIs and crossed-factor allocation intervals.
- `p2_per_user_fixed_checkpoint.csv.gz`: complete 10,222-user/65-column score matrix, actual archived Base/Memory values and paired contrasts.
- `p2_protocol_and_provenance.json`: model/data checksums, source run IDs, eligibility, sample sizes, RNG streams and whether original P0 replay passed.
- [Predeclared design](https://github.com/mzch0210/KuaiLive-Agent/blob/main/manuscript/kbs_latex/SECTION6_STAGE3_P2_PREDECLARED_PROTOCOL_2026-10-10.md), [scientific audit](https://github.com/mzch0210/KuaiLive-Agent/blob/main/manuscript/kbs_latex/SECTION6_STAGE3_P2_RESULTS_2026-10-10.md), [source code](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py).

The first two GitHub-hosted workflow attempts failed **before model scoring** because of incorrect cross-run artifact selection/extraction options; the third run performed all hard guards. This execution history is fully retained to prevent conflating code/infrastructure retries with scientific draw retries.


---

# S6. Base context-length, target recurrence, and memory-history definition sensitivity


### S6.1 Research purpose and invariant evaluation population

These are **Twitch DEV-only diagnostics**, comprising **46,878** one-target-per-user events. They examine whether fixed Memory's relative value changes alongside independently trained Base input contexts and retrospectively measured target-creator recurrence. No results in this section were used to change the original frozen Twitch TEST Utility threshold. Subgroups are defined using the **observed target creator** and therefore cannot be treated as pre-outcome selector rules.

The context comparison uses maximum Base lengths **L=8,16,32**; **each Base has separately trained parameters**. For a scientifically interpretable same-specialist comparison, the canonical frozen P1.2 L16 Memory rank and NDCG@10 are reused identically at all three Base lengths. The first secondary aggregation failed because an evaluator introduced an extra split-end history filter and thereby changed Memory for some users; that run is **excluded**. The repaired run restored canonical Memory exactly, and all event identities and Memory ranks then passed deterministic invariant checks.

### S6.2 Overall ranking scores by independently trained Base context

**Table S6.1. Overall Base context models and fixed Memory.**

| Base maximum context L | Events | Base NDCG@10 | Frozen Memory NDCG@10 | Memory−Base | 95% paired-user CI |
|---|---:|---:|---:|---:|---|
| 8 | 46,878 | 0.526194 | 0.521696 | **−0.004498** | [−0.007557, −0.001274] |
| 16 (canonical) | 46,878 | 0.571853 | 0.521696 | **−0.050157** | [−0.053065, −0.047313] |
| 32 | 46,878 | 0.596627 | 0.521696 | **−0.074931** | [−0.077665, −0.072274] |

**Interpretation:** with this same frozen Memory scorer, the overall relative gain becomes more negative as the separately trained Base becomes stronger on these DEV events. **It is not a controlled estimate of history-window length holding model weights fixed**; training realizations change with L.

### S6.3 Retrospective target-history state comparisons

**Table S6.2. Context-specific history state results.**

| Base L | Target-relative state | Events | Memory−Base NDCG@10 | Pointwise 95% paired CI |
|---|---|---:|---:|---|
| 8 | Represented | 19,486 | +0.002711 | [−0.000388,+0.005816] |
| 8 | Recoverable | 10,934 | +0.260425 | [+0.252876,+0.267791] |
| 8 | Unavailable | 16,458 | −0.189036 | [−0.193834,−0.184418] |
| 16 | Represented | 24,541 | −0.019951 | [−0.022857,−0.016806] |
| 16 | Recoverable | 5,879 | +0.230969 | [+0.221915,+0.240344] |
| 16 | Unavailable | 16,458 | −0.195620 | [−0.200376,−0.191109] |
| 32 | Represented | 28,158 | −0.023089 | [−0.026163,−0.019946] |
| 32 | Recoverable | 2,262 | +0.188605 | [+0.175262,+0.202654] |
| 32 | Unavailable | 16,458 | −0.199848 | [−0.204481,−0.195050] |

Each row uses **the target's presence in that Base context**. Group denominators change with L, while the unavailable-event set remains the same. The original frozen L16 Memory has identical event-level outcomes in each context panel.

### S6.4 Matched-user state transitions

For the exact same users whose previously recoverable target becomes represented as Base context length increases:

**Table S6.3. Paired history-state transitions.**

| Base L transition | Recoverable → represented users | Change in Memory−Base | 95% paired CI | Change in frozen Memory | Change in Base |
|---|---:|---:|---|---:|---:|
| 8 → 16 | 5,055 | **−0.447482** | [−0.457672,−0.437300] | 0 | +0.447482 |
| 16 → 32 | 3,617 | **−0.432288** | [−0.443811,−0.420543] | 0 | +0.432288 |

On these matched users, the Memory-minus-Base difference necessarily equals the **negative change in Base NDCG** because canonical Memory is unchanged. The result is compatible with increasing Base adequacy for an older relationship but **cannot isolate causality from visibility alone**: independently trained Base parameters, context and candidate score behavior differ.

### S6.5 Target-creator recurrence distance under fixed L=16

The diagnostic distance is the number of eligible prior user interactions back to the most recent occurrence of the **observed target creator**, not wall-clock time or prediction-time known target features.

**Table S6.4. Target recurrence-distance bins.**

| Last prior occurrence (interactions ago) | Events | Memory−Base NDCG@10 | 95% pointwise CI |
|---|---:|---:|---|
| 1–4 | 13,963 | +0.04606 | [+0.04276,+0.04938] |
| 5–8 | 5,556 | −0.06511 | [−0.07180,−0.05852] |
| 9–16 | 5,027 | −0.15268 | [−0.16096,−0.14455] |
| 17–32 | 3,621 | +0.25668 | [+0.24486,+0.26827] |
| 33–64 | 1,716 | +0.20707 | [+0.18985,+0.22384] |
| ≥65 | 537 | +0.12965 | [+0.10092,+0.15807] |
| No eligible prior target creator | 16,458 | −0.19562 | [−0.20025,−0.19099] |

The pattern is **non-monotonic**, with positive short-repeat and longer-than-base-visible pockets separated by a negative intermediate band. These are descriptive, non-multiplicity-adjusted observations with confounding by user activeness, target identity and candidate difficulty. A target-specific distance is unavailable to the pre-outcome selector.

### S6.6 Repaired-source provenance and replication restrictions

- Canonical frozen L16 DEV/Memory event source: [DEV run 35698158121](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35698158121), original artifact 10680854557; L16 immutable OOF SHA256 `9757064252c097934fa31f10a68e11bb43853ca1132aaa49da2b9794f60d3816`.
- Separate L8/L32 original Base training: [GPU intervention run 35830028173](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35830028173), artifact 10752233546.
- **Corrected/authoritative aggregation:** [run 35877647543](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35877647543), [artifact 10757614400](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35877647543/artifacts/10757614400). Its archived `context_length_overall.csv`, `context_length_state_summary.csv` and `context_length_transitions.csv` reproduce the values above.
- Initial evaluator mismatch: **50/46,878** user history lengths drifted by 51 eligible records; **15** Memory ranks and **14** Memory NDCG values were affected. The repaired aggregator **reuses canonical Memory**, rather than ignoring a mismatch or weakening checks. See [repair explanation](https://github.com/mzch0210/KuaiLive-Agent/blob/main/KBS_CONTEXT_LENGTH_INTERVENTION_REPAIR_2026-09-23_RUN35877647543.md).
- Recency: [DEV run 35725938757](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35725938757), [original summary](https://github.com/mzch0210/KuaiLive-Agent/blob/main/KBS_ROBUSTNESS_RESULTS_2026-09-22.md). The DEV recency/conditional CIs are not new held-out confirmation.

No Base context or recency result from this section changes the one-shot Twitch TEST selector, and no wording should imply unseen online session intervals from ten-minute crawl data.

---

# S7. DEV feature-family comparisons and independently frozen M3 invocation policies

## S7.1 Existing prediction evidence and common-budget protocol

The original artifact contains **46,878 unique DEV user events**, each with the same Base and fixed Memory NDCG@10 and 5-fold OOF predicted relative utility and predicted Base difficulty for three feature families: history-only (6 features), Base-score-only (8), and their combination (14). These saved prediction vectors were **replayed without fitting any new model**, modifying thresholds or examining TEST labels.

We compared five exact batch-level invocation fractions: **5%, 10%, 15%, 20%, and 30%**. The corresponding integer budgets were chosen by floor(n×fraction+0.5): **2,344; 4,688; 7,032; 9,376; 14,063**. For each family and prediction target, events are sorted by its existing OOF prediction in descending order; the original event row order deterministically breaks ties. The top m events use Memory and all others use Base; decisions are compared on exactly the **same users**.

This exact top-m operation is a **retrospective batch comparison**; it is not the primary Utility policy's DEV-frozen pointwise threshold or an online deployable hard-budget rule. The budget grid was set before running the current replay, but the development data had previously supported OOF learning and the original operating-point choice. No new held-out inference follows.

**Replay guards passed:** archived OOF/source-table SHA256s; all user IDs unique; event-level utility identity; all six original **6,563-call** Utility/Difficulty selection masks identical to the original; original three Utility-vs-Base means reproduced to absolute error below 1e−12. The 6,563-point is the **historical DEV-selected 14.00017%** operating count, not an independently chosen 15% and not the separate frozen TEST's 6,650 calls.

## S7.2 Same-count Utility-selection performance

Values below are **mean NDCG@10 gains versus the same DEV Base** (Base NDCG@10 = 0.5718534); NDCG estimates and paired intervals are conditional on the original OOF predictions and exact count.

**Table S7.1. Equal DEV invocation-rate feature comparisons.**

| DEV Memory call budget | m calls | History-only Utility | Base-score-only Utility | Combined Utility |
|---|---:|---:|---:|---:|
| 5% | 2,344 | +0.00221 | +0.00220 | **+0.00598** |
| 10% | 4,688 | +0.00349 | +0.00232 | **+0.00774** |
| 15% | 7,032 | +0.00371 | +0.00137 | **+0.00832** |
| 20% | 9,376 | +0.00406 | +0.00045 | **+0.00792** |
| 30% | 14,063 | +0.00311 | **−0.00282** | **+0.00736** |
| Original K=6,563 (14.00017%) | 6,563 | +0.00372 | +0.00160 | **+0.00838** |

The **combined features** obtain the highest observed Utility gain at each of the five specified percentages, but the gain is **non-monotonic** with the invocation count. Base-score-only selection becomes detrimental at 30% in this DEV replay. This qualified result supplements, rather than supersedes, the one-point feature-family table in the main Results.

### Confidence intervals for combined Utility versus Base

**Table S7.2. Combined Utility paired bootstrap intervals.**

| DEV call budget | Combined mean Utility−Base gain | Conditional paired 95% CI |
|---|---:|---|
| 5% | +0.00598 | [+0.00513, +0.00685] |
| 10% | +0.00774 | [+0.00665, +0.00884] |
| 15% | +0.00832 | [+0.00704, +0.00962] |
| 20% | +0.00792 | [+0.00649, +0.00940] |
| 30% | +0.00736 | [+0.00574, +0.00906] |
| Historical K=6,563 | +0.00838 | [+0.00714, +0.00966] |

## S7.3 Direct pairwise comparisons, including the Difficulty objective

In addition to separate Utility gains, all comparisons below directly subtract **same-user selected-ranking utility under identical m calls**: Combined versus History-only, Combined versus Base-score-only, and Combined Utility versus Combined Difficulty. These are **DEV OOF batch-top-count comparisons**, not separately fitted alternative online policies.

**Table S7.3. DEV feature/target direct paired contrasts.**

| Budget | Direct paired comparison | Mean NDCG@10 difference | Conditional paired 95% CI |
|---|---|---:|---|
| 5% | Combined − History | +0.00377 | [+0.00284, +0.00472] |
| 5% | Combined − Base-score | +0.00379 | [+0.00307, +0.00450] |
| 5% | Combined Utility − Combined Difficulty | +0.00356 | [+0.00285, +0.00425] |
| 10% | Combined − History | +0.00425 | [+0.00309, +0.00538] |
| 10% | Combined − Base-score | +0.00542 | [+0.00446, +0.00646] |
| 10% | Combined Utility − Combined Difficulty | +0.00569 | [+0.00468, +0.00671] |
| 15% | Combined − History | +0.00461 | [+0.00336, +0.00579] |
| 15% | Combined − Base-score | +0.00695 | [+0.00579, +0.00814] |
| 15% | Combined Utility − Combined Difficulty | +0.00746 | [+0.00630, +0.00863] |
| 20% | Combined − History | +0.00386 | [+0.00273, +0.00502] |
| 20% | Combined − Base-score | +0.00747 | [+0.00608, +0.00884] |
| 20% | Combined Utility − Combined Difficulty | +0.00933 | [+0.00802, +0.01063] |
| 30% | Combined − History | +0.00424 | [+0.00310, +0.00542] |
| 30% | Combined − Base-score | +0.01018 | [+0.00865, +0.01170] |
| 30% | Combined Utility − Combined Difficulty | +0.01321 | [+0.01171, +0.01471] |
| Historical 6,563 | Combined − History | +0.00466 | [+0.00347, +0.00588] |
| Historical 6,563 | Combined − Base-score | +0.00678 | [+0.00564, +0.00793] |
| Historical 6,563 | Combined Utility − Combined Difficulty | +0.00713 | [+0.00602, +0.00828] |

The 3,000-replicate **paired percentile bootstrap** resamples the 46,878 unique DEV users with replacement and holds OOF models, predicted scores, selected masks and counts fixed (seed 20261010). All reported intervals are **pointwise and unadjusted**; the table contains overlapping exploratory comparisons and does not establish familywise significance or across-all-budget dominance.

## S7.4 Statistical interpretation

This analysis uses precomputed cross-fitted OOF prediction vectors, so the score for an event is not generated from a regressor fitted on that event. Nevertheless, the same DEV population has been used for earlier feature design, model and threshold selection. Report these as **conditional descriptive sensitivity estimates**, not unbiased uncertainty intervals incorporating nested tuning/model-fitting variability. The exact top-m decision uses an evaluation batch, unlike the independent TEST's frozen pointwise threshold, and cannot establish serving-time cost, fair online budget guarantees, external KuaiLive transfer, causal feature complementarity or universal superiority over learning-to-defer alternatives.

The bounded conclusion is that **the original combined history + Base-score feature family supports positive relative-utility selection gains across this finite DEV operating grid**, with direct paired comparisons versus the restricted feature families and a Base-Difficulty objective. This is relevant to C3 but **not a new test of the frozen selector**.

## S7.5 M3 independently DEV-frozen gates and realized TEST invocation

The M3 design differs from S7.1–S7.4, which analyze \emph{Twitch DEV only} through retrospective exact top-m batches. In M3, five independent pointwise operating rules per trained Base are frozen from **50,049 full-active DEV requests** under a **maximum 30% DEV call constraint**. Utility predicts Memory-minus-Base NDCG@10; Difficulty predicts negative Base NDCG@10; Specialist predicts standalone Memory NDCG@10. These three objectives use their own DEV-group-OOF-fitted histogram gradient-boosting models on the common **12 observable pre-outcome features**. The two deterministic alternatives rank by negative Base top-two-score margin (Uncertainty) and total earlier user activity (History), respectively. All methods use inclusive frozen score-threshold comparisons, calling all threshold-tied events together.

The **47,575-event later-period M3 TEST** was scored once with fixed thresholds. The realized invocation count of a frozen pointwise rule depends on the new event distribution: 30% calibrated on DEV does not guarantee 30% on TEST. Table S7.4 provides the exact number and rate for every policy, preserving unequal TEST calls rather than retrospectively matching them. These are not system wall-clock cost fractions. The source is the original G5-B **aggregate.json**, [action #38226690320](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38226690320), artifact **11735868084**, with the frozen scientific and implementation registry in S2.

**Table S7.4. Actual frozen M3 TEST specialist calls, count and percent of 47,575 events.**

| Base / training seed | Utility | Difficulty | Specialist Quality | Uncertainty | History |
|---|---:|---:|---:|---:|---:|
| SASRec 20261012 | 13,899 (29.215%) | 14,227 (29.904%) | 14,067 (29.568%) | 14,358 (30.180%) | 16,876 (35.472%) |
| GRU4Rec 20261012 | 13,736 (28.872%) | 14,431 (30.333%) | 14,233 (29.917%) | 14,192 (29.831%) | 16,876 (35.472%) |
| SASRec 20261013 | 13,187 (27.718%) | 14,426 (30.323%) | 14,257 (29.967%) | 13,990 (29.406%) | 16,876 (35.472%) |
| GRU4Rec 20261013 | 13,628 (28.645%) | 14,311 (30.081%) | 14,242 (29.936%) | 14,170 (29.785%) | 16,876 (35.472%) |
| SASRec 20261014 | 13,423 (28.214%) | 14,106 (29.650%) | 14,168 (29.780%) | 14,397 (30.262%) | 16,876 (35.472%) |
| GRU4Rec 20261014 | 13,842 (29.095%) | 14,327 (30.115%) | 14,181 (29.808%) | 14,323 (30.106%) | 16,876 (35.472%) |

Always Base uses **zero** Memory calls and Always Memory uses **47,575 (100%)** in each fixed model condition. The History policy's common 35.472% TEST rate does not invalidate its frozen DEV calibration but establishes that a strict online 30% cap **was not implemented**. The pointwise Utility rules invoke Memory on **27.718%–29.215%** of TEST requests. Comparisons among the five policies therefore share a DEV selection protocol, not the same realized TEST number of calls; neither matching TEST calls after revealing outcomes nor modifying thresholds is part of the frozen experiment.

A resource-aware evaluation would additionally measure the Base's execution, candidate and history preparation, gate prediction and conditional Memory cost under the intended workload. S9 reports only the available bounded warmed scoring evidence and does not infer a production efficiency improvement.

## S7.6 Reproducibility

Original archive member SHA256s:

- OOF predictions: `25b5e560ce67d16221e483e9c18cad679eb28525ce0a8279ae91555726547627`.
- Original 3-family comparison: `58d835e0ae53c43fe1ae522fdefee83374ba4ae58900968ea741780cffe92e48`.

Reproduction source: [analysis/kbs_section6_stage2_dev_replay.py](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_section6_stage2_dev_replay.py). Input files reside in archived artifact **10688746451**. Its output tables contain **all six prediction orderings at the five budgets plus the original 6,563-call reference**, and direct paired contrasts for each; the entire output can be regenerated from archived inputs without model training. 


## S7.7 Nested-DEV direct versus two-stage estimator sensitivity (exploratory)
This exploratory analysis complements the frozen selection evidence in Sections S7.1–S7.6. It is **post-G5 exploratory DEV evidence**, not part of the original confirmatory G5 TEST.

The Direct estimator learns the event NDCG@10 increment of Memory over the fixed Base. The Two-stage estimator separately learns Memory and Base NDCG@10, then subtracts. Both target the same conditional expectation by linearity; they are alternative implementations, not different deferral theories.

The evaluation uses 50,049 full-active M3 DEV events from 12,628 users with twelve decision-time features, the primary SASRec and GRU4Rec training seed (20261012), five outer user-disjoint validation folds and four inner group folds per outer training subset for OOF threshold calibration under a maximum 30% inner-DEV Memory-call criterion. TEST outcomes were not used for the new experiment.

**Table S7.5. Exploratory nested-DEV comparison (2,000 paired user-cluster bootstrap replications).**

| Base | Estimator | DEV NDCG@10 | Gain over Base | Memory calls | Direct−Two-stage NDCG difference (95% CI) |
|---|---|---:|---:|---:|---|
| SASRec | Direct | 0.302678 | +0.044511 | 14,980 (29.931%) | +0.001352 [+0.000422,+0.002198] |
| SASRec | Two-stage | 0.301326 | +0.043159 | 14,693 (29.357%) | — |
| GRU4Rec | Direct | 0.302989 | +0.044018 | 14,716 (29.403%) | +0.000051 [−0.000822,+0.000907] |
| GRU4Rec | Two-stage | 0.302939 | +0.043967 | 14,751 (29.473%) | — |

Direct invokes Memory 287 more times on SASRec, so its gain is not an equal-call-quality superiority result. The GRU4Rec interval crosses zero. Always Memory DEV NDCG@10 was 0.343509. Neither the two-regressor gate overhead nor an actual external service cost was measured. The analysis cannot establish generic superiority to published Learning-to-Defer or DS-Frame algorithms.

Code: `analysis/kbs_plan_c/n2_d1_nested_dev_pilot.py`; successful [GitHub Actions #38339908528](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38339908528); verified aggregate summary SHA256 `b944e791e4797f97892bbbddb6f6729014a00cc3bc11e3cb6f1229b207897706`. This is not a claim of durable public hosting of event-level data.

---

# S8. Distinct KuaiLive room-seed diagnostics and M3 frozen author-ranking robustness


### S8.1 Separate model-seed uncertainty from sampled-negative-draw uncertainty

S8 evaluates **three independent fitted KuaiLive Dual-ID checkpoint pairs**, with fixed 10,222 TEST events, original sampled-575 candidate sets, matched full-active sets, fusion coefficient **α_room=0.125**, eligibility/history and Memory scorer. This is **P1, three model training realizations**, not P2's **three independent negative-list RNG streams applied to one original model**. Both are retrospective analyses on the same previously examined KuaiLive TEST users and neither supplies new independent datasets or a new frozen Twitch policy evaluation.

For each checkpoint pair, event-level raw Room/Streamer scores over full-active candidates are reused by exact subset extraction for sampled candidates. The two-order allocation of ranked membership versus z-score reference is computed on the same users, with 3,000 paired user bootstrap resamples **conditional on each trained checkpoint**.

### S8.2 Complete across-training-seed outcomes

**Table S8.1. Seed-wise KuaiLive fixed candidate comparison.**

| Room/Streamer training seed | Sampled 575 Memory−Base (SS) | Full-active Memory−Base (FF) | FF−SS | 95% within-seed user-paired CI | Ranked-membership allocation | Score-reference allocation |
|---|---:|---:|---:|---|---:|---:|
| 20260918 | −0.04120411 | +0.04630669 | **+0.08751080** | [+0.08209796,+0.09325975] | +0.08826963 | −0.00075883 |
| 20260919 | −0.05157020 | +0.03206113 | **+0.08363134** | [+0.07804704,+0.08938187] | +0.08438602 | −0.00075469 |
| 20260920 | −0.04903770 | +0.03504633 | **+0.08408403** | [+0.07853540,+0.08945325] | +0.08424480 | −0.00016077 |

**All three fitted pairs exhibit sampled-negative/full-positive relative-utility sign reversal.** Across the *three checkpoint pairs* the unweighted mean FF−SS is **+0.08507539** and the sample SD is **0.00212124**; observed range **[+0.08363134,+0.08751080]**. This three-seed SD is a *descriptive training-initialization statistic*, **not** a user-bootstrap uncertainty interval or population-level confidence estimate. In particular, a small seed SD should not be read as independent cohort replication.

The 20260920 score-reference allocation has within-user 95% CI **[−0.00052317,+0.00017555]**, spanning zero. The numerical sign of a small allocation in one condition must not be advertised as significant for every seed. The membership and normalization allocations always sum *algebraically* to FF−SS, but they do not identify counterfactual interventions that vary candidate count alone.

### S8.3 State-wise contribution to the regime shift

The observed-target retrospective state membership is **identical** for sampled and full candidate evaluations: **4,589 represented**, **206 recoverable-but-unrepresented**, **5,427 unavailable** out of 10,222 users. These groups cannot be used as a deployment selector. The table reports each group's **across-training-seed mean FF−SS**, along with its prevalence-weighted contribution to the overall mean difference.

**Table S8.2. Across-seed history-state decomposition.**

| Retrospective target state | Users | Across-seed mean paired shift | Weighted contribution to aggregate shift |
|---|---:|---:|---:|
| Represented | 4,589 | **+0.086179** | **+0.038689** |
| Recoverable-but-unrepresented | 206 | **−0.109972** | **−0.002216** |
| Unavailable | 5,427 | **+0.091546** | **+0.048603** |
| **All users** | **10,222** | **+0.085075** | **+0.085075** |

The approximately 2% recoverable group contributes **negatively** to the aggregate sampled/full shift; thus the reversal is **not** explained by more recoverable history or larger regime gains in that group. It is driven largely by the represented and unavailable groups in this paired scoring protocol. This is a decomposition of matched ranking utility, **not causal mediation**.

### S8.4 Original checkpoint fingerprint table

**Table S8.3. Checkpoint SHA fingerprints.**

| Training seed | Room checkpoint SHA256 | Streamer checkpoint SHA256 |
|---|---|---|
| 20260918 | `b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7` | `82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945` |
| 20260919 | `395d1b1c881d20cbda5d24c36c30685fd1524a0ec98586c8c71ad7c245505b2a` | `9f1b11cf27e0c802f71bb8b1bef646bb392b28d560e3aabda03f36fe01e2b637` |
| 20260920 | `84c4ef5e45592fc480096dfe4e501046ede37c1f936484ed83f3bd56e1f49191` | `7043b275b56a75fd5d7aeadfd7e69d5447128ce9f55f3bd6a0f275a24dd2d144` |

### S8.5 M3 six fitted author-ranking Bases on one frozen forward-time TEST

The following **M3 author-ranking** evidence is entirely distinct from the original **KuaiLive room-ranking** P1/P2 studies in S8.1–S8.4. The designated Base families are SASRec and GRU4Rec, trained separately at seeds 20261012, 20261013 and 20261014, evaluated without TEST-based refitting on a common **47,575-event / 12,533-user** later-period cohort. All six models share the same eligibility/candidate rosters and the unchanged relationship Memory. The M3 neural models differ by fitted initialization, not by independent observed user samples. TEST full-active median candidate count is **31,065** warm eligible authors.

**Table S8.4. Six-incumbent M3 TEST NDCG@10.**

| Base / training seed | Always Base | Always Memory | Utility | Difficulty | Specialist Quality | Uncertainty | History |
|---|---:|---:|---:|---:|---:|---:|---:|
| SASRec 20261012 | 0.258004 | 0.346792 | **0.302866** | 0.282479 | 0.279558 | 0.289373 | 0.279789 |
| GRU4Rec 20261012 | 0.260033 | 0.346792 | **0.304004** | 0.284321 | 0.281829 | 0.290891 | 0.281964 |
| SASRec 20261013 | 0.258811 | 0.346792 | **0.301766** | 0.282803 | 0.281608 | 0.288136 | 0.280249 |
| GRU4Rec 20261013 | 0.260649 | 0.346792 | **0.303016** | 0.284147 | 0.282428 | 0.290004 | 0.282095 |
| SASRec 20261014 | 0.258673 | 0.346792 | **0.303058** | 0.283020 | 0.280272 | 0.289374 | 0.280143 |
| GRU4Rec 20261014 | 0.258400 | 0.346792 | **0.303549** | 0.283472 | 0.280543 | 0.289235 | 0.280461 |

Within each fitted Base the frozen Utility policy exceeds Always Base and all four alternative gate objectives. On the primary SASRec 20261012 fit, Always Base/Utility/Always Memory HR@10 are **0.387620 / 0.455681 / 0.533873**, confirming the same ordering under hit rate. However, **Always Memory has higher absolute NDCG@10 than Utility in every M3 condition**; Utility is a choice under a specified call constraint, not the unconstrained best-ranked policy. For complete realized call fractions see Table S7.4.

### S8.6 Preregistered M3 paired inference: 18 contrasts, six conditional Holm families

The G0F scientific plan predeclared exactly three one-sided primary contrasts for each designated M3 Base: Utility versus **Always Base**, **Difficulty**, and **Specialist Quality**. All three policies use pre-outcome rules fitted/frozen on DEV, except Always Base which uses no Memory. Within each of the six trained model/seed configurations, 5,000 **user-cluster paired bootstrap** resamples over 12,533 users produce pointwise percentile 95% CIs and 5,000 **user-cluster random-sign** replicates provide a one-sided test of the relevant null under an approximately sign-symmetric cluster difference assumption. The original G5-B evaluation applies Holm's correction to **the three comparisons separately within each fit**. All 18 adjusted p-values are **0.0005998800** (rounded below to 0.000600); the raw Monte Carlo floor is **1/5001 = 0.0001999600**, not zero. This does not establish one global Holm-controlled error rate across all 18 correlated tests or reflect uncertainty from retraining the Base/gate.

**Table S8.5. Every prespecified M3 Utility-minus-comparator TEST contrast, paired mean NDCG@10 and 95% user-cluster CI; one-sided 5,000 sign randomizations with within-fit Holm(3) correction.**

| Base / seed | Utility minus | Mean paired Δ NDCG@10 | 95% user-cluster CI | Raw one-sided p | Holm(3) adjusted p |
|---|---|---:|---|---:|---:|
| SASRec 20261012 | Always Base | +0.044862 | [+0.042805, +0.046915] | 0.000200 | 0.000600 |
| SASRec 20261012 | Difficulty | +0.020387 | [+0.018370, +0.022442] | 0.000200 | 0.000600 |
| SASRec 20261012 | Specialist Quality | +0.023308 | [+0.021177, +0.025508] | 0.000200 | 0.000600 |
| GRU4Rec 20261012 | Always Base | +0.043971 | [+0.042001, +0.046024] | 0.000200 | 0.000600 |
| GRU4Rec 20261012 | Difficulty | +0.019683 | [+0.017580, +0.021775] | 0.000200 | 0.000600 |
| GRU4Rec 20261012 | Specialist Quality | +0.022175 | [+0.020009, +0.024408] | 0.000200 | 0.000600 |
| SASRec 20261013 | Always Base | +0.042955 | [+0.041000, +0.044987] | 0.000200 | 0.000600 |
| SASRec 20261013 | Difficulty | +0.018963 | [+0.016955, +0.021069] | 0.000200 | 0.000600 |
| SASRec 20261013 | Specialist Quality | +0.020158 | [+0.018101, +0.022293] | 0.000200 | 0.000600 |
| GRU4Rec 20261013 | Always Base | +0.042367 | [+0.040359, +0.044484] | 0.000200 | 0.000600 |
| GRU4Rec 20261013 | Difficulty | +0.018868 | [+0.016771, +0.021032] | 0.000200 | 0.000600 |
| GRU4Rec 20261013 | Specialist Quality | +0.020588 | [+0.018542, +0.022831] | 0.000200 | 0.000600 |
| SASRec 20261014 | Always Base | +0.044385 | [+0.042441, +0.046415] | 0.000200 | 0.000600 |
| SASRec 20261014 | Difficulty | +0.020038 | [+0.018054, +0.022055] | 0.000200 | 0.000600 |
| SASRec 20261014 | Specialist Quality | +0.022786 | [+0.020679, +0.024965] | 0.000200 | 0.000600 |
| GRU4Rec 20261014 | Always Base | +0.045149 | [+0.043166, +0.047204] | 0.000200 | 0.000600 |
| GRU4Rec 20261014 | Difficulty | +0.020077 | [+0.018071, +0.022175] | 0.000200 | 0.000600 |
| GRU4Rec 20261014 | Specialist Quality | +0.023005 | [+0.020873, +0.025251] | 0.000200 | 0.000600 |

The relative advantage over the strongest non-Utility alternative, the **Base-margin Uncertainty proxy**, is consistently positive (**+0.01301 to +0.01431**) but is **secondary**. It is neither one of the three preregistered primary tests nor a direct empirical comparison with a separately implemented GUIDER system. Each contrast is paired within its fitted Base's observed users, and the six fitted model results share the same user cohort and cannot be multiplied into independent data replications.

### S8.7 M3 expected random allocation and hindsight bounds

**Table S8.6. M3 TEST expected Random@30 and hindsight Oracles (NDCG@10).** These are outcome-conditional reference calculations: the Random@30 value is a conditional expectation rather than a separately drawn frozen randomized policy, and both Oracles use realized target labels and are not deployable.

| Base / seed | Random@30 expected | Hindsight Oracle@30 | Hindsight Oracle unbounded |
|---|---:|---:|---:|
| SASRec 20261012 | 0.284640 | 0.388135 | 0.388333 |
| GRU4Rec 20261012 | 0.286060 | 0.391644 | 0.391707 |
| SASRec 20261013 | 0.285204 | 0.388484 | 0.388652 |
| GRU4Rec 20261013 | 0.286491 | 0.391146 | 0.391182 |
| SASRec 20261014 | 0.285108 | 0.389147 | 0.389327 |
| GRU4Rec 20261014 | 0.284917 | 0.391062 | 0.391227 |

The G5 one-shot target-blind inference followed by label-only confirmation is documented in S2. The complete data and TEST performance source is [G5-B frozen result archive](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38226690320) artifact **11735868084** and the [accepted G5 scientific result report](https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md). The material permits checking the frozen aggregate but does not expose user- or event-level TEST targets.

### S8.8 Original KuaiLive evidence status and incomplete generalization

The exact P0 model pair is byte-matched to the earlier same-checkpoint archive; the other two pairs were newly trained in original GPU job [37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645), with compact result artifact [11538678848](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538678848) and checkpoint artifact [11538867565](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538867565). The complete original scientific ledger is [KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md](https://github.com/mzch0210/KuaiLive-Agent/blob/main/KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md).

P2 candidate-list sensitivity is **separately tabulated in S5**, using one frozen 20260918 checkpoint and 128/256/575 candidates at three RNG streams per size. **Neither the 3 P1 trained-model seeds nor the 9 P2 candidate conditions count as additional independent dataset replications.** The original native KuaiLive policy, cross-protocol strict transfer and external dataset generalization cannot be inferred from these matched P0/P1/P2 metrics.

---

# S9. Computational resource and efficiency evidence

## S9.1 Experimental conditions

The main controlled-scoring benchmark uses KuaiLive 575-candidate sampled-active room recommendation, a two-branch (Room/Streamer) Dual-ID SASRec Base, history cap `L=50`, embedding dimension `d=64`, and 14 pre-outcome selector features. Inference is CPU-only, single thread, batch size one. Three GitHub-hosted CPU replicas each run 1,200 warmed queries (3,600 timing observations per model/pipeline); the sampled queries are deterministic within a replica. Hardware is **not homogeneous across replicas**; the benchmark reports pooled descriptive estimates and does not identify population-level hardware variability. Candidate feeds, user-level history descriptors and cache state were materialized before timing. Loading, feature-cache rebuild, updating relationship state, network I/O, queuing and concurrency were not measured.

The executable source is [`analysis/gate_compression_latency.py`](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/gate_compression_latency.py), which actually executes the fitted gate predictor as part of the selective pipeline. Crucially, its branch decision uses the **precomputed frozen test route mask**, not the new predictor output computed during timing. This isolates the runtime path for prespecified decisions but is not a test of fully autonomous online gating correctness. The individual gate-only microbenchmark uses preconstructed input vectors; its latency cannot simply be added to selective-pipeline timing to reconstruct full latency.

## S9.2 Same-panel KuaiLive cost comparison

**Table S9.1. Controlled CPU timing panels.**

| Pipeline / component | Memory invocation share | Mean latency (ms) | P50 (ms) | P95 (ms) |
|---|---:|---:|---:|---:|
| Dual-ID Base | 0% | 0.990585 | 1.039273 | 1.275783 |
| Selective HGB | 14.2536% | 2.006624 | 2.026013 | 2.904929 |
| Selective Ridge | 30.9920% | 1.387248 | 1.290124 | 2.147706 |
| Selective Tiny-MLP | 10.3698% | 1.271907 | 1.277168 | 2.039375 |
| HGB prediction only (precomputed features) | Not applicable | 0.617416 | 0.671539 | 0.697656 |
| Ridge prediction only (precomputed features) | Not applicable | 0.002422 | 0.002404 | 0.002675 |
| Tiny-MLP prediction only (precomputed features) | Not applicable | 0.005755 | 0.006092 | 0.006452 |
| Memory scoring (cached state) | Not applicable | 0.490254 | 0.484797 | 0.600424 |

All rows above belong to the **same gate-compression timing panel**, recovered and assembled in successful formal run 35730086758. The 95th percentile is a pooled descriptive percentile, **not** a user-cluster bootstrap confidence interval. The three hosts are not randomized production replicas. End-to-end (warmed scoring pipeline) HGB excess mean latency is `2.0066239936 - 0.9905847453 = 1.0160392483 ms`, equivalent to a **2.025696×** ratio to Base. Means and component measurements are not additively exact because the timed paths and preparatory computations differ.

**Policy-utility comparability limit:** HGB, Ridge and Tiny-MLP here use different learned decisions and different Memory invocation frequencies. The companion gate-compression accuracy frontier reports distinct TEST NDCG gains, so lower Ridge/Tiny-MLP latency is not an independently established **fixed-policy, fixed-budget, equal-utility** efficiency improvement. An equal-quality latency claim requires predeclared matched invocation budgets, selection-policy retraining/freeze rules and paired evaluation on the same query workload.

## S9.3 Distinct historical benchmark (do not combine with S9.2)

The older inference-latency benchmark, reaggregated from available replica artifacts by formal run 35730086758, reports **Dual-ID mean 0.760784 ms**, **frozen 14.25% selective HGB mean 2.336902 ms**, and pooled P95 **1.259947 / 3.173842 ms**, respectively. These measurements originate in a **different benchmark path**; their respective means must not be paired with S9.2 rows when calculating overhead. Original workflow 35559499838 had failing/skipped stages, but the later successful formal aggregation explicitly recovered the archived per-replica timing outputs; the formal aggregation and its immutable inputs, not the original workflow's overall status, are the evidence record. Do not report this older comparison in the main text except with explicit provenance.

## S9.4 Complexity with stated assumptions

Let `C` be the candidate count, `L` the Base sequence length, `d` the attention embedding size, `F` the number of gate input descriptors, `T` the number of fitted regression trees and `D` their maximum depth. For **two one-layer, standard dense-attention sequence encoders** with a simple candidate-embedding scoring head, a *schematic* forward-pass expression is `O(2(L²d + Ld² + Cd))` (assuming no additional large modules, fixed number of heads and cached embeddings). It is **not** a formal bound for model loading, data materialization, candidate construction, full user-state feature extraction or the surrounding serving system.

Under cached relationship-history maps, specialist candidate scoring is approximately `O(C)` with a separate relationship cache of order `O(R_u)` for per-user relationship entries. Rebuilding these maps or updating them with new user activity is a different operation whose time and memory costs are excluded from the small warmed scoring path. Feature extraction depends on the availability of cached user descriptors and on the candidate score vector; computing Base-confidence statistics generally requires inspecting candidate scores (`O(C)` or more depending on exact order statistics), and should not be treated as free. A trained single-output histogram gradient-boosted tree ensemble with `T` trees and maximum depth `D` requires at most `O(TD)` sequential node visits for ordinary tree traversal per query, excluding feature preparation. The fitted experimental HGB has **81 boosting iterations** with maximum depth 3, and the input contains **14 observable features**. Ridge scoring is `O(F)` for the affine mapping (excluding scaling preparation); a 14–16–1 dense Tiny-MLP forward map is `O(FH+H)` for `H=16`, excluding cache and infrastructure overhead.

The qualitative accounting identity is Base score computation + feature extraction + gate execution + specialist candidate scoring **conditional on the route decision**. An invocation fraction `p` affects only the last term's expected frequency under a fixed workload. Without measurements of the remaining terms and identical policies, the fraction `p` is neither a latency guarantee nor a throughput/GMV/engagement estimate.

## S9.5 File footprint and process memory

**Table S9.2. Separate legacy timing condition.**

| Measurement | Observed value | Meaning / caveat |
|---|---:|---|
| Room + streamer model checkpoint files | 303.851841 MiB | Two serialized model checkpoints, not total process RAM |
| HGB fitted estimator file | 0.104691 MiB | Serialized `joblib` artifact; not per-query activation memory |
| Ridge coefficient/scaler arrays | 0.000328 MiB | Array payload only |
| Tiny-MLP/scaler arrays | 0.002174 MiB | Array payload only |
| Memory relationship cache (serialized) | 4.307323 MiB | Pickled popularity/history objects for the measured dataset |
| Peak resident set (stack materialization probe) | 875.625 MiB | Separate process-level `ru_maxrss` high-water mark, not a per-query increment |

The resident-set probe loaded checkpoint weights, gate artifacts, train/dev files and cached user state. The memory mapping does **not** imply those allocations remain resident identically in production, nor may serialized sizes be summed to reconstruct peak RSS. The test used a distinct measurement phase from latency; results are runtime/environment-specific.

## S9.6 KuaiLive-M3 warmed RTX 3090 DEV author-ranking replay

This measurement is distinct from the original 575-room CPU replay in S9.1–S9.5. It used **256 predetermined DEV author-ranking requests**, an RTX 3090 (24 GB), the frozen primary SASRec Base (seed 20261012), fixed relationship Memory and frozen Utility gate. Memory was selected on **80/256 = 31.25%** of replay requests. The source analysis verified the sparse pre-gate history-support feature against the frozen M3 computation. The replay reconstructed historical state before timing; the prepared-input path excludes that work.

**Table S9.3. M3 warmed offline DEV replay, ms/event; each path has 256 observations.**

| Execution path | Mean | Median | P90 | P95 |
|---|---:|---:|---:|---:|
| Always Base | 1.4245 | 0.8317 | 1.0875 | 1.1797 |
| Always Memory | **0.8033** | **0.7744** | 1.1019 | 1.2505 |
| Utility selective total | **1.8018** | 1.6778 | 2.3888 | 2.7046 |
| Base within selected path | 0.7284 | 0.7209 | 0.8711 | 0.8987 |
| Sparse feature computation | 0.2395 | 0.2380 | 0.3307 | 0.3572 |
| Frozen gate inference | 0.6207 | 0.6201 | 0.6511 | 0.6597 |
| Memory branch, zero if unused | 0.2132 | 0.0000 | 0.7872 | 0.9188 |

In these measured warmed DEV conditions, Always Memory is faster than Utility routing (0.8033 versus 1.8018 ms/event mean). The separate M3 frozen TEST also shows higher unconditional ranking quality for Memory (NDCG@10 0.346792) than for Utility (0.301766–0.304004). Therefore no unconditional deployment or net speed advantage is established. The 256-event offline timing excludes earlier history-state reconstruction, incremental state updates, active-room interval maintenance, input loading, scheduling, network effects, GPU contention and optimized batch serving. The standalone Base mean differs from the Base component mean within selective execution; one should not add the measured components to infer unobserved service latency.

Original cost source: [Action #38223495966](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38223495966), artifact **11734923392**, aggregate.json; frozen Base checksum 18fb25d68970e73661a4b1418f5be05e7f8bed678d097533adf3cf1d9964d17e. No TEST target evaluation occurred in this DEV measurement.

## S9.7 Reproducibility audit and critical exclusions

- Formal run: [35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758), complete [artifact 10694941935](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758/artifacts/10694941935).
- Gate compression: [35571827672](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35571827672), 3 successful replicas and pooled final artifacts.
- Scripts: [formal aggregation](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_formal_efficiency.py), [cache probe](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_efficiency_stack_probe.py), [gate-compression benchmark](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/gate_compression_latency.py), and [replica aggregation](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/aggregate_inference_latency.py).
- Nontransferability: frozen Twitch selection uses 6,650/44,221 = **15.04%**, official LiveRec Base and availability-aware streamer candidates. **No Twitch end-to-end latency was measured**, so KuaiLive milliseconds are not transferable to it.
- Selection-mask replay, cache assumptions, heterogeneity of hosts and absence of queueing, online feature recomputation or network I/O prevent deployment-level SLAs or claimed cost reductions.
- 


---

## Source hierarchy and bibliographic anchors

Two separately DEV-frozen held-out decision settings provide the main selection evidence: Twitch [TEST run 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303) on 44,221 streamer requests and KuaiLive-M3 author ranking [target-blind G5-A 38225946950](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38225946950) followed by [one-shot target evaluation G5-B 38226690320](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38226690320) on 47,575 requests. They have independently fitted selectors and different candidate definitions. Original KuaiLive paired room candidate diagnostics are retrospective analyses from 37751814645 and 38014145900. Twitch exploratory DEV sources include 35698158121, 35713931454, 35724784990, 35725938757, 35877647543 and 37959745609. Original KuaiLive room CPU and new M3 RTX3090 warmed DEV measurements represent separate workloads. Dated G4 reports saying TEST had not run reflect their historical stage and are superseded for final scientific conclusions by the completed G5 report, without overwriting that historical record. All source hashes refer only to their specified artifacts, not to unverified historical binary files.

**References.** Qu et al. (2026), *KuaiLive: A Real-time Interactive Dataset for Live Streaming Recommendation*, SIGIR 2026 ([official repository](https://github.com/imgkkk574/KuaiLive)); Rappaz, McAuley and Aberer (2021), *Recommendation on Live-Streaming Platforms: Dynamic Availability and Repeat Consumption*, RecSys 2021, 390–399 ([source](https://github.com/JRappaz/liverec)); Krichene and Rendle (2022), *On Sampled Metrics for Item Recommendation*, *Communications of the ACM*, 65(7), 75–83, [DOI 10.1145/3535335](https://doi.org/10.1145/3535335). The last work precedes this study; sampled metric ranking inconsistency is not claimed as a new theorem.

---

# S10. Matched Candidate-Regime Supervision, Relationship Sources and Decision Sensitivity

**Evidence map.** Sections S10.1–S10.14 document the M3 DEV candidate-regime supervision, allocation, source-interaction and sensitivity analyses; S10.15 reports the previously unevaluated same-period 30,000-target frozen-policy comparison; S10.16 and S10.18 document its nested 4,096-target historical-source checks and the remaining original control limit. S10.17 separates DEV-only path timing, and S10.19 preserves complete secondary results and earlier source tables. The DEV sections reuse a single development cohort and are not independent held-out TEST replications; the additional-target evidence belongs to the same recording period, not a later prospective cohort. Each section retains its original scientific scope and source identity.

## S10.1 Experimental cohort, ranking unit and comparison target

Both B1 and B2 use the **same 50,049 KuaiLive-M3 DEV events from 12,628 user clusters**, with author (persistent creator) as the ranking unit. The incumbent rankers are one frozen SASRec primary seed and one frozen GRU4Rec primary seed, each trained before these analyses. The Memory specialist is the fixed corrected all-prior-history Short/Long/Popularity ranker, not a jointly retrained auxiliary neural model. All policies target the ranking of eligible TRAIN-known active authors at event time.

Let F denote the full-active ranking-candidate regime; let S denote a deterministic **575 target-retained sampled** retrospective evaluation regime. A sampled observation retains the subsequently observed author only in the offline calculation of $u_{10}$ labels; target retention is not an observable decision-time feature, not an online generation procedure, and not a justification for assigning realized target information to a gate.

Let $\Delta_r(x)=u_{10}(M,x;r)-u_{10}(B,x;r)$ for $r\in\{S,F\}$. B1 estimates separate selectors trained on $\Delta_S$ or $\Delta_F$ and compares their decisions on held-out full-active events. The exploratory contrast $V_F(\pi_F)-V_F(\pi_S)$ is reported alongside each policy's realized Memory invocations. Candidate membership changes number, identity and competition jointly; no isolated candidate-count causal effect is claimed.

## S10.2 Nested fitting, frozen selection and statistical scope

The analysis used **five outer GroupKFold splits by user** and **four inner GroupKFold splits** within each outer training partition, with no users shared across fitting and validation folds. Predictors used twelve fixed pre-outcome features comprising seven history/candidate descriptors and five Base-score summaries. The regression class was `HistGradientBoostingRegressor`, with 120 iterations, learning rate 0.05, maximum depth 3, minimum leaf size 50, $\ell_2$ penalty 1, and no early stopping; these post-G5 nested fits are distinct from the original frozen M3 TEST predictors with 200 iterations. Inner out-of-fold predictions determine a single pointwise score threshold under the original at-most-30%-of-inner-DEV invocation target, with indivisible score ties. Outer subjects are only scored after calibration and are not used to pick a retrospective best threshold or match outer call counts.

The pure S→F arm fits to Delta_S and calibrates only with S supervision, then evaluates on outer F. The F→F arm fits and calibrates on F labels from outer-training users. The regime-adapted→F arm includes S and F labels and regime descriptors during outer-training, calibrates on F inner labels, and **has access to F supervision**; it is neither label-free adaptation nor an improvement beyond native F→F.

Descriptive 95% confidence intervals were constructed from 2,000 paired user-cluster percentile bootstrap draws. The user-disjoint outer folds characterize generalization to held-out users within the existing DEV period, not an independently chronological TEST; five folds on one cohort are not five independent prospective test cohorts. All B1/B2 arm choices were devised after original G5 outcome review; these confidence intervals do not enter the frozen G5 registered Holm testing family. Original G5 TEST remains unopened for these analyses.

## S10.3 Candidate supervision, full-ranking policy utility

**Table S10.1. Candidate-aligned and sampled-label transfer evaluated on identical full-active author-ranking DEV events.**

| Incumbent | S→F NDCG@10; calls | F→F NDCG@10; calls | Adapted→F NDCG@10; calls | F→F − S→F (paired 95% user CI) |
| --- | --- | --- | --- | --- |
| SASRec | 0.296499; 14,988 | 0.302658; 15,016 | 0.301847; 14,954 | 0.006159 [0.004835, 0.007543] |
| GRU4Rec | 0.298123; 15,001 | 0.303093; 14,762 | 0.303000; 14,989 | 0.004970 [0.003550, 0.006369] |

The F-aligned rule improves quality relative to S supervision in both incumbent families under their observed invocation rates. Adapted-to-F does not exceed native F→F; its training includes the full-supervision information that is unavailable to a pure S-trained policy. The absolute reference NDCG@10 for Always Memory on these full-active DEV events is 0.343509, above these selectors; the result supports the decision relevance of candidate-aligned valuation **under a stipulated invocation rule**, not unconditional or latency superiority.

## S10.4 Five knowledge sources and candidate-regime comparisons

The specialist source conditions are: the fixed full 0.45 Short + 0.45 Long + 0.10 popularity mixture, Long-only, Short-only, training-only popularity, and a deliberately broken within-event historical-score placement placebo. The original mixture was not retuned. Under F, Full Memory yields 0.343509 NDCG@10 versus Long-only 0.333231; under S, Full yields 0.668498 versus Long-only 0.773602. The source ordering reverses. Short-only obtains 0.273839 F and 0.407506 S, popularity-only 0.022215 F and 0.197796 S, and placement placebo 0.007576 F and 0.189571 S.

This demonstrates source-dependent evaluation differences on fixed historical score constructions. The placebo is not a globally margin-preserving history randomization. Extremely weak controls cannot isolate the specific contribution of correct viewer--creator identity when selectors almost never choose those experts.

## S10.5 Source-dependent selection transfer and information availability

For original twelve-feature selectors, full-candidate aligned-minus-sampled-trained decision-quality differences were:

**Table S10.2. Historical knowledge source and candidate-supervision transfer losses under the original twelve-feature selector.**

| Memory source | SASRec difference | GRU4Rec difference | Interpretation |
| --- | ---: | ---: | --- |
| Full | 0.006159 | 0.004970 | Matched users, similar but nonidentical calls |
| Long-only | 0.010605 | 0.010262 | Larger transfer penalty than Full under this feature panel |
| Short-only | 0.020694 | 0.020291 | Strong call-rate shift confounds same-budget interpretation |
| Popularity-only | 0.000000 | 0.000010 | Near-zero invocation floor |
| Relationship shifted | 0.000020 | 0.000014 | Very weak source; near-zero invocation floor |

In the Short-only condition, SASRec S→F invokes Memory 171 times and F→F 14,766 times; GRU4Rec corresponding calls are 141 and 14,851. These raw contrasts must **not** be described as equal-budget causal decision regret.

To probe whether direct relation-history descriptors affect transfer, the same experiments were repeated with just six pretarget features (candidate-count summary plus five Base-score descriptors), rather than the original twelve. For Full Memory the transferred-policy difference falls to 0.001814 SASRec and 0.001607 GRU4Rec, compared with 0.006159 and 0.004970 under twelve features. The six-feature control is not literally history-free: Base score representations still encode user behavioral history; reducing feature dimension and richness can also affect approximation. The contrast identifies a conditional **information dependence**, not a single isolated causal relationship-history channel.

## S10.6 Decision value across specialist-invocation constraints

The full-active, candidate-aligned Direct relative-utility selector was evaluated under pre-specified inner-DEV Memory-call maxima of 0%, 10%, 20%, 30%, 50%, 70%, 90% and 100%. Training and threshold selection use the same 5-outer by 4-inner user-disjoint scheme and the same single-head HGB model as Section S10.2; only the OOF invocation limit changes. The 100% condition permits unconstrained threshold selection and **does not force** every event to use Memory. All quality values are measured over identical held-out outer-user full-active ranking events; actual outer call rates can exceed inner development limits.

**Table S10.3. Development candidate-aligned policy quality versus natural Memory invocation rate.**

| Inner call-rate maximum | SASRec Memory calls | SASRec F NDCG@10 | GRU4Rec Memory calls | GRU4Rec F NDCG@10 |
| --- | ---: | ---: | ---: | ---: |
| 0% | 0 | 0.258167 | 0 | 0.258971 |
| 10% | 5,001 | 0.278263 | 5,006 | 0.279025 |
| 20% | 9,946 | 0.291381 | 9,904 | 0.292962 |
| 30% | 15,016 | 0.302658 | 14,762 | 0.303093 |
| 50% | 25,081 | 0.319654 | 25,230 | 0.320478 |
| 70% | 34,980 | 0.332695 | 34,831 | 0.332078 |
| 90% | 44,768 | 0.341040 | 45,164 | 0.341051 |
| 100% | 50,006 | 0.343495 | 49,770 | 0.343363 |
| Always Memory (unrestricted fixed reference) | 50,049 | 0.343509 | 50,049 | 0.343509 |

The 30% condition reproduces the original Full-to-Full development comparison exactly. Removing the invocation limit brings the learned policy very close to Always Memory: it invokes the specialist on 99.91% (SASRec) and 99.44% (GRU4Rec) of cases while remaining slightly below unconditional Memory accuracy. The corresponding unrestricted-versus-30%-rule differences are +0.040837 (SASRec, paired user CI [0.038750, 0.042806]) and +0.040270 (GRU4Rec, CI [0.038163, 0.042302]); these contrasts have markedly different realized call counts and do not represent equal-cost benefits. The observation clarifies why policy quality under a stipulated specialist-call allocation rule should not be equated with an empirically justified production resource constraint.

## S10.7 Matched decision-target controls

To test whether incremental ranking utility is a more decision-relevant signal than request difficulty or expert standalone quality, four DEV-only objectives were compared on the same full-active events and nested user splits. Direct predicts Memory-minus-Base event NDCG; Two-stage subtracts separate estimates of Memory and Base event NDCG; Base Difficulty predicts negative Base event utility; and Specialist Quality predicts Memory event utility. All use the same twelve decision-time inputs and HGB hyperparameters, although Two-stage fits two prediction heads rather than one. All policies are calibrated using the same original inner OOF utility-gain threshold rule, and their actual outer Memory invocations are not retroactively equalized.

**Table S10.4. Objective controls on matched full-active M3 DEV NDCG@10.**

| Maximum inner calls | Base | Direct value | Two-stage | Base difficulty | Memory quality |
| --- | --- | ---: | ---: | ---: | ---: |
| 10% | SASRec | 0.278263 | 0.277864 | 0.263151 | 0.261710 |
| 10% | GRU4Rec | 0.279025 | 0.278802 | 0.264451 | 0.262982 |
| 30% | SASRec | 0.302658 | 0.301348 | 0.282295 | 0.278220 |
| 30% | GRU4Rec | 0.303093 | 0.302974 | 0.283554 | 0.279202 |
| 50% | SASRec | 0.319654 | 0.319178 | 0.305321 | 0.303104 |
| 50% | GRU4Rec | 0.320478 | 0.319608 | 0.306720 | 0.302253 |

At the 30% inner limit, Direct minus Two-stage yields +0.001310 SASRec (95% paired user CI [0.000419, 0.002179]; Direct invokes Memory 318 more times) and +0.000119 GRU4Rec (CI [-0.000767, 0.000955]; Direct invokes Memory 59 fewer times). Across the three budgets, Direct and Two-stage estimates remain close in rank utility, as anticipated from their common population estimand. The greater differences against Difficulty and Specialist Quality support the relevance of predicting the *relative* value of this fixed source rather than either model's standalone expected quality; they do not establish new deferral mathematics or strict equal-resource superiority. Exact score/rank fusion of two complete candidate vectors was not evaluated because such vectors were not established as available from the frozen DEV utility-source records.

## S10.8 Reproducibility and evidence hierarchy

B1 paired candidate sources and nested transfer correspond to GitHub Actions runs `38364829652` and `38365477972`; the private paired DEV source digest is `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`. The B2 nested ablation was completed in run `38369503457` and its public aggregates are archived in `B2_NESTED_DEV_SOURCE_SPECIFICITY_AGGREGATE_2026-10-13.json`. A separate read-only audit (run `38382393789`) rehashed the B1/B2 private sources, confirmed the corrected full-candidate source lineage, and verified 50,049 unique DEV event IDs and 12,628 users without exporting identifiable event rows. The N9-P0 claim-source register links each result to its public evidence artifact.

The original Twitch/M3 frozen TEST results remain the independent decision evaluations; the 10,222-room sampled/full comparison is retrospective; B1/B2/A1/A2 are post-G5 exploratory analyses of the **same M3 DEV cohort**. Their uncertainty intervals do not extend the frozen G5 multiple-testing family. The study makes no production serving-cost or target-aware online sampling claim. The sampled-metric non-preservation precedent is Krichene and Rendle (KDD 2020).


## S10.9 Supervision-induced knowledge-use decisions

The B1 F- and S-supervised policies were refitted with the original 12 pre-outcome features, 120-iteration HGB, five outer by four inner user-disjoint folds and at most 30% inner OOF Memory calls. Their original full-active NDCG and natural outer Memory-call totals reproduced exactly. On the same 50,049 full-active outer-held-out DEV author requests, we compute the policy disagreement probability $D_{S,F}=P(\pi_S(Z)\neq\pi_F(Z))$ and the identity
$V_F(\pi_F)-V_F(\pi_S)=\mathbb{E}[(\pi_F(Z)-\pi_S(Z))\Delta_F(X)]$.
The identity is an accounting decomposition, not a novel decision theorem. Both policies have similar realized total invocations but can allocate them to different requests.

**Table S10.5. F-aligned versus S-supervised choice changes and relative utility, post-G5 M3 DEV.**

| Base | Different decisions | F-only Memory calls | S-only Memory calls | Mean $\Delta_F$ on F-only requests | Mean $\Delta_F$ on S-only requests |
| --- | ---: | ---: | ---: | ---: | ---: |
| SASRec | 10,672 (21.32%) | 5,350 | 5,322 | 0.133417 | 0.076194 |
| GRU4Rec | 11,517 (23.01%) | 5,639 | 5,878 | 0.126600 | 0.079135 |

For SASRec, the added-call contributions average $+0.014262$ full-ranking NDCG across all 50,049 events, offset by $-0.008102$ from calls removed, for an exact net $+0.006159$ (paired user 95% CI [0.004835, 0.007543]). The corresponding GRU4Rec contributions are $+0.014264$ and $-0.009294$, yielding $+0.004970$ (CI [0.003550, 0.006369]). These are naturally realized calls, not strictly equal-budget causal treatments. Corrected-S was not fitted: the target-retained 574-negative-without-replacement construction is documented, but the existing scalar sampled top-10 labels do not by themselves establish a justified ranking-utility correction estimator with the necessary rank/score information and assumptions. In particular, it would be incorrect to relabel supervision that uses full-active outer-training outcomes as S-only correction.

## S10.10 Paired historical-source by candidate-regime interaction

The same matched DEV events permit estimation of a *fixed knowledge-source utility* interaction, distinct from the nested *decision-regret* interactions presented above. Define $d_{F,i}=u_F(M_{\mathrm{Full}},i)-u_F(M_{\mathrm{Long}},i)$ and $d_{S,i}=u_S(M_{\mathrm{Full}},i)-u_S(M_{\mathrm{Long}},i)$, where Full retains the original 0.10/0.45/0.45 mixture and Long-only the original long component. The paired interaction $I_i=d_{F,i}-d_{S,i}$ is averaged across 50,049 identical ranked targets; 95% percentile intervals resample **12,628 users**, with 2,000 user-cluster draws.

**Table S10.6. Fixed-source knowledge utility and candidate-regime dependence on matched author requests.**

| Estimand | Mean event NDCG@10 | 95% user-cluster interval |
| --- | ---: | --- |
| Full minus Long-only, full-active F | +0.010278 | [+0.007906, +0.012668] |
| Full minus Long-only, target-retained sampled S | −0.105104 | [−0.108326, −0.101683] |
| Source × regime interaction, F minus S gap | +0.115382 | [+0.111724, +0.119065] |

The interaction is heterogeneous across pre-outcome user history strata: the mean across quartiles of distinct historical creators is approximately 0.048267, 0.106528, 0.130050 and 0.176801. These are descriptive subdivisions of the **same** DEV sample, not independent experiments or identified causal moderators. The top-10 event metric has substantial exact-zero mass: 46,462 events have a zero Full-minus-Long difference in at least one regime, 27,800 have a three-way sign-category difference including zero, and only 66 have strictly opposite **nonzero** source-gap signs. The mean source ordering reversal must therefore not be interpreted as widespread event-level positive-to-negative switches.

## S10.11 Conditional net decision value under hypothetical use costs

The empirical A1 quality--call curve was evaluated against all alternative A1 invocation-limit policies and the fixed Always Base/Always Memory endpoints, using the **actual outer-call rate** $q(\pi)$:
$J_{\lambda}(\pi)=V_F(\pi)-\lambda q(\pi)$.
Here $\lambda\geq0$ is an assumed shadow price in units of expected ranking NDCG per additional Memory call. This analysis sets incremental full-path gate overhead to **zero only for the hypothetical envelope calculation**, and does not measure monetary, energy or production-latency costs.

Over the observed-policy upper envelope, the 30%-inner-limit policy is optimal for $\lambda\in[0.084516,0.111321]$ on SASRec and $\lambda\in[0.083119,0.104379]$ on GRU4Rec. At zero shadow cost, Always Memory maximizes the observed M3 DEV ranking quality. Other budget-limited policies dominate at other assumed shadow-price intervals; the complete machine-readable policy envelope is archived in \`N9_G1_E2_SHADOW_PRICE_ENVELOPE_PUBLIC_AGGREGATE_2026-10-13.json\`. These thresholds are point estimates from the existing 50,049 DEV events. The public A1 per-arm aggregates do not preserve the joint user-level score covariance needed to bootstrap uncertainty around frontier switch points; no confidence interval for $\lambda$ is inferred.

## S10.12 Time- and activity-preserving relation-null feasibility

To examine whether a credible historical-identity placebo could avoid the near-zero utility of the B2 score-placement shift, a separate exploratory pilot selected 128 late-period DEV requests involving 126 users **by their pre-outcome timestamps**. It used 547,992 earlier historical events for those users. Within hourly bins completed before the earliest selected request, pairs of viewer--creator interaction author labels were exchanged only when the two viewers differed, the two authors differed, and both authors were active at *both* original interaction times according to the sealed room-availability intervals. This preserves each user's event timestamps/count and exact per-hour author event marginals within the selected prefix. The deterministic pilot rewired 63,619 pairs (127,238 events, 23.22% of the pilot histories). Original Full and Long-only Memory F/S scores reproduced the fixed B1/B2 event scores before manipulation.

For these **pilot events only**, Full Memory under full-active F yielded 0.396585 NDCG@10 before the relation-identity intervention and 0.384386 afterward. Under retrospective sampled S the corresponding values were 0.661360 and 0.669835. The latter comparison reverses direction and is not evidence of a uniform identity-specific advantage. The placebo remained far above the F popularity-only 0.037155 baseline, with positive full-ranking NDCG on 68 of 128 null-scored requests (72 of 128 original). Thus the predeclared non-floor feasibility gate passed.

The intervention is restricted to an historical prefix of selected users, and these 128 late-period DEV requests have no independent inferential interval or independent TEST status. A full 50,049-event relation-identity study would need to prevent same-hour future-history swaps from affecting earlier requests; such a temporally valid full-cohort analysis was **not performed**. The pilot confirms control feasibility, not causal historical relation-identity specificity. These scope restrictions are essential when interpreting the aggregate source interaction above.

## S10.13 Exact-zero contribution to candidate-regime source interaction

To distinguish candidate-set-induced top-ten truncation effects from strict source preference reversals, we analyze the **same 50,049 M3 author DEV requests and 12,628 users** underlying B2 and E3a. Let $d_F(i)=u_{10}(M_{\mathrm{Full}},F,i)-u_{10}(M_{\mathrm{Long}},F,i)$, $d_S(i)=u_{10}(M_{\mathrm{Full}},S,i)-u_{10}(M_{\mathrm{Long}},S,i)$ and $I_i=d_F(i)-d_S(i)$. Each request is assigned to one of nine cells according to the exact signs of $d_F$ and $d_S$. Each signed contribution equals the sum of $I_i$ in the cell divided by **all 50,049 requests**.

**Table S10.7. Nine-cell decomposition of Full-minus-Long knowledge utility, fixed source under full-active F versus offline target-retained sampled S candidates.**

| Sign under F | Sign under S | Number of events | Contribution to mean $I$ |
|:---:|:---:|---:|---:|
| − | − | 1,927 | +0.010020 |
| − | 0 | 10,542 | -0.050444 |
| − | + | 25 | -0.000248 |
| 0 | − | 8,524 | +0.104801 |
| 0 | 0 | 18,728 | +0.000000 |
| 0 | + | 1,101 | -0.009706 |
| + | − | 41 | +0.000457 |
| + | 0 | 7,567 | +0.056234 |
| + | + | 1,594 | +0.004268 |

The nine contributions sum exactly to **+0.115382**. The paired 2,000-resample user-cluster 95% interval for the total is **[0.111573, 0.119111]**. In **46,462 requests (92.83%)**, $d_F$ or $d_S$ is zero, and their signed contributions sum to **+0.100885 (87.44% of the net positive mean)**. This 87.44% is a **signed net-accounting share**, not the proportion of absolute effects or an estimated causal mediation fraction. In contrast, 66 requests exhibit opposite strictly nonzero signs. Nonzero-gap requests contribute the remaining +0.014497. The large net interaction largely reflects support changes and signed cancellation across regimes. It cannot be used alone to establish uniquely relational identity effects or a new sampled-ranking metric inconsistency theorem.

## S10.14 Time-valid historical identity perturbation on a stratified M3 DEV sample

An additional analysis tests the role of **historically correct user--creator pairing** while holding each request's full-active candidate roster fixed. Before observing these perturbation outcomes, **1,024 requests from 992 distinct M3 DEV users** were frozen in a 4×4 stratification of recorded time and pretarget interaction-history activity (64 requests per cell), excluding 128 events previously examined during feasibility testing. These requests are a subset of the *same post-G5 DEV cohort*, **not a new TEST population**. Original Full and Long-only F/S ranking scores were regenerated event by event, with maximum absolute NDCG deviation $5.55\times10^{-17}$ from the frozen B1/B2 labels.

A relationship-null swaps historical author labels across *different users* within recorded-time hourly windows. Each substitution requires two distinct authors available at **both original event times**, and maintains each user's interaction count and timestamps as well as each author's per-hour event count. Substitutions in an hour are **activated only after that hour ends**; requests inside the currently open hour retain their unchanged prior events. Original target identity, Base checkpoints and both F/S candidate rosters are fixed, with S retained only as a retrospective target-containing evaluation protocol. The same historical scoring code, run with an **empty substitution mapping**, exactly reproduced original Full and Long-only NDCG for all 1,024 requests; thus the effect below is not an artifact of switching rank implementations.

Three random null seeds were fixed before score inspection (20261014, 20261015, 20261016). They draw from the **same users and requests** and should not be counted as independent holdouts. A total of 4,276,963 selected-user pretarget historical records were eligible; each seed rewired approximately **3.36 million (78.6%)** with per-hour activity and cross-author availability checks, and every request had at least one activated changed historical relation. Bootstrap confidence intervals use **2,000 paired user-cluster samples per seed**.

**Table S10.8. Original and time-preserving-null ranking quality.**

| Fixed null seed | Null Full F NDCG | Original−null F | 95% user-cluster CI for F gain | Null Full S NDCG | Original−null S | Null F top-10 hits |
|---|---:|---:|---|---:|---:|---:|
| 20261014 | 0.306491 | 0.032858 | [0.023317, 0.042538] | 0.622740 | 0.041156 | 487 |
| 20261015 | 0.303804 | 0.035544 | [0.026723, 0.045122] | 0.623869 | 0.040027 | 481 |
| 20261016 | 0.305321 | 0.034027 | [0.023890, 0.044384] | 0.618221 | 0.045675 | 476 |

Original Full Memory obtains **0.339348** under F and **0.663896** under S on these identical requests. The full-active real-minus-null effect averages **+0.034143** across the three *null assignments*, with seed-specific estimates ranging **+0.032858 to +0.035544**. It has no CI obtained by pretending the three assignments are independent datasets. All three single-seed paired-user 95% interval half-widths are below the prespecified **0.015** analysis-precision target, so the planned optional 2,048-event expansion was not undertaken.

The controls remain meaningful: their Full F NDCG is **0.303804–0.306491**, well above popularity-only **0.021867**, with **476–487** target-hit events in the top ten. Null Full S is **0.618221–0.623869**. Each seed passed the prespecified non-floor checks, including coverage and perturbation strength. The Long-only original-minus-null F effect is **+0.030490 to +0.035344**. These effects demonstrate the ranking consequences of disturbing historical author identity *under a fixed current candidate universe*, rather than relying solely on comparing sampled and full-ranking metrics.

The intervention is deliberately strong and disrupts repeated user--author pairs and higher-order co-interaction patterns despite preserving the stated temporal/degree/availability marginals. The **78.6% change fraction** is notably greater than the earlier 128-event pilot's 23.2%; those results are not direct replications under identical intervention intensity. No relation-identity average treatment effect under all possible alternative nulls, new independent chronological TEST, or operational resource saving is established. The user- and author-linked private exchange maps were retained in restricted analysis storage and were not redistributed. Dataset-version terms and any release of derived interaction records remain subject to author review.

Reproduction provenance is recorded in the [closed-hour swap construction](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_plan_c/n9_route_b_b2_real_closed_hour_swap_dev.py), [three-seed ranking replay](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_plan_c/n9_route_b_b2_1024_real_relation_null_scoring.py), and [public parity aggregate](https://github.com/mzch0210/KuaiLive-Agent/blob/main/experiments/kbs_plan_c/N9_ROUTE_B_B2_1024_THREE_SEED_SAME_SCORER_VERIFIED_2026-10-14.json). Source parity, chronological checks, and no TEST access are documented in the stored provenance manifests.

## S10.15 Same-period additional-target supervision alignment

The B4-A examination selects **30,000 previously unevaluated ranking target event IDs** (10,387 users), from 4,723,652 eligible residual KuaiLive-M3 interactions in the original **March 27–31, 2026 TEST-source recording interval**. It excludes all 47,575 original G5 ranking-evaluation target IDs, but *not* necessarily their users or observations used in prior prequential historical contexts; **these are not newly collected future-period data**. A nested 4,096-event subset (3,059 users) was independently sealed for historical-source perturbation (S10.16).

Before new target labels were opened, the selection procedure partitioned eligible requests into twenty cells (five source dates × four within-date quartiles of *pretarget* history length). A source-event-ID-seeded, label-blind ordering chose 1,500 requests per cell. The main sample SHA-256 is be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14; the nested SHA-256 is 40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059. Original G1 source identity/clock compatibility, both Base checkpoints, four A2 HGB models, OOF thresholds and the 30,000 Full-F target-blind rankings were checked and sealed before the first A4 label access. Source actions: [A3 H1 seal](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38517170015), [H2/final seal](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38517502835), [independent prereveal audit](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38518563975), [the one successful A4 label reveal](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38518785650), and [A5 independent numerical reconstruction](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38519174441). The earlier A4 YAML-only failed triggers did not start a label-reading job.

The primary estimand expands each observation using the preregistered weight $w_i=N_{h(i)}/n_{h(i)}$, where $N_h$ is the number of eligible residual events and $n_h$ the frozen sample size in its date × history cell. For event value $y_i$, the fixed-weight estimator is $\widehat{\mu}_{w}(y)=\frac{\sum_i w_i y_i}{\sum_i w_i}$. The main Kish effective weight sample size is **26,849.29** (30,000 raw request observations, not 26,849 independent viewers). User-cluster paired bootstrap percentile 95% intervals use **5,000 resamples**; 5,000 one-sided user-cluster sign-randomizations assume approximate cluster-sign symmetry. Holm adjusts exactly the **three prespecified B4-A directional hypotheses** (SASRec F vs S, GRU4Rec F vs S, authentic Full Memory vs mean of three fixed history nulls), not the earlier exploratory DEV comparisons.

The two frozen primary-seed 20261012 Base families, SASRec and GRU4Rec, use the same Full Memory score recipe. Each has an S-aligned HGB gate trained on retrospectively target-retained 575-item sampled candidate DEV labels and an F-aligned HGB gate trained on full-active DEV ranking labels. Both arms use **identical twelve pre-outcome Full-F features, the full-active TRAIN-known author roster, and fixed DEV-derived gate thresholds at B4-A target time**. The S roster occurs as DEV supervision, **not** a target-dependent online candidate generator. The 30% specialist-invocation limit applies to DEV user-disjoint OOF threshold fitting, not to a retrospectively enforced TEST quota.

**Table S10.9. Additional M3 targets, fixed full-active F ranking, 20-cell natural population weighting.**

| Frozen policy | Weighted F NDCG@10 | Realized Memory calls | Unweighted call rate | Weighted call rate |
| --- | ---: | ---: | ---: | ---: |
| SASRec Always Base | 0.259307 | 0 | 0% | 0% |
| SASRec S-aligned | 0.300055 | 9,105 | 30.350% | 30.537% |
| SASRec F-aligned | **0.305446** | **8,704** | **29.013%** | **29.203%** |
| GRU4Rec Always Base | 0.260058 | 0 | 0% | 0% |
| GRU4Rec S-aligned | 0.300945 | 9,168 | 30.560% | 30.809% |
| GRU4Rec F-aligned | **0.304530** | **8,629** | **28.763%** | **29.008%** |
| Always Memory (shared) | **0.348744** | 30,000 | 100% | 100% |

The SASRec F-minus-S paired contrast is **+0.005391** (95% user-cluster CI **[+0.003646,+0.007174]**, three-test Holm-adjusted one-sided $p=0.000600$); GRU4Rec is **+0.003585** (CI **[+0.001599,+0.005576]**, adjusted $p=0.000800$). The F-aligned fixed gates make **401** and **539 fewer calls**, respectively. However, their realized unweighted call differences (**1.337** and **1.797 percentage points**) exceed the prespecified approximately equal-budget interpretation threshold of **1.0 pp**. Thus the evidence concerns quality and calls under **natural frozen-policy operation**, not a strict equal-call comparison. Always Memory remains more accurate at 100% specialist invocation. All five daily subgroup effects are descriptively positive, but shared users and one collection period prevent treating them as independent validation datasets. The DEV supervision labels also differ in available information, so the contrast does not isolate generic model architecture.

## S10.16 Frozen relationship-history null confirmation and remaining control limits

The precommitted nested **4,096 targets / 3,059 users** use separate $N_h/n_h$ poststratification for the same eligible population, with Kish effective weight size **3,659.42**. The authentic Full Memory ranker and three previously frozen closed-hour relation-null seeds (**20261014, 20261015, 20261016**) rank **identical Full-F candidate rosters** for each target. Their historical-author substitutions pair events from different viewers within hourly source-time bins, require both creators to be active at both original event times, preserve per-user interaction timestamps/counts and original author-hour margins, and activate only after the swapped source hour ends. The current evaluation target author was not supplied to its own prediction. Around **76.78–76.80%** of relevant historical source edges were rewired, modifying user–author repetition and higher-order structure in addition to direct historical identity alignment.

**Table S10.10. Natural-population weighted full-candidate NDCG@10 for authentic and three relationship-null histories (one frozen 4,096-target cohort).**

\begin{center}
\begin{tabular}{@{}lr@{}}
\toprule
Relation condition & Weighted Full-F NDCG@10 \\
\midrule
Authentic original Full Memory & \textbf{0.334942} \\
Null seed 20261014 & 0.303905 \\
Null seed 20261015 & 0.304689 \\
Null seed 20261016 & 0.302796 \\
Mean of the three within-request null NDCGs & 0.303797 \\
Authentic minus within-request mean null & \textbf{+0.031145} \\
\bottomrule
\end{tabular}
\end{center}

The last paired effect has 95% user-cluster CI **[+0.027389,+0.035098]**, Holm-adjusted one-sided $p=0.000600$. Null seeds are **three randomizations on the same requests**, not three independent cohorts; for inference the three null utilities are averaged **within event** before applying the 5,000-draw cluster procedure. Original and null rankings were SHA-sealed before A4; [H2 pre-outcome seal](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38517502835) and [A5 independent paired audit](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38519174441) substantiate this separation.

The observed null histories are not collapsed controls: each retains **1,903–1,913** top-ten positive targets across the 4,096 requests, Full-F NDCG above **0.10** and above **30%** of the authentic reference, and substantial time/availability-valid rewiring. **One prespecified control diagnostic remains NOT VERIFIED:** the planned margin between each null's F NDCG and a fixed TRAIN-popularity-only ranker on *these same newly evaluated targets*. This popularity benchmark was not sealed or scored before the A4 label reveal. The complete original nonfloor acceptance family therefore cannot be described as fully passed; we do not retrospectively change scores, seeds or thresholds to repair this limitation.

This historical intervention is strong and changes higher-order relations along with identity assignments; it is not an isolated treatment effect for a single relation semantics. The same-period B4-A evidence improves frozen target-specific confirmation of candidate-aligned supervision and authentic relational history value, **not** independent future-time validation, user-disjoint replication, causal identification of a unique microscopic relation property, or a demonstrated economic/latency advantage of selective Memory over Always Memory. Private event, user, author and edge-level outputs remain restricted to the secure analysis cache and are not part of the public supplement.

## S10.17 DEV-only counterbalanced Base, Memory and Utility path timing

A post-B4-A **exploratory DEV-only** cost audit evaluates the previously frozen G3/E2 SASRec Utility selector alongside Always Base and Always Memory, without reopening any B4-A A4 outcomes. The cohort comprises **256 distinct DEV requests** at predetermined positions in the 50,049-request cohort, each with its causal pretarget historical state and contemporaneous Full-F TRAIN-known active-author roster. The same requests, original Base checkpoint, original Utility model and original DEV OOF threshold were reused. A target author's identity was not an input to the full-F candidate construction. The history-support gate feature matched the existing corrected DEV feature for each request. The selected Top-10 was exactly the corresponding Base or Memory Top-10 in all **768** replays.

Each request underwent the three paths in cyclically rotated order over **three repetitions**, with CUDA synchronization on an RTX 3090 before and after each scored branch; 16 warmup events were excluded. The resulting 768 timings *per path* are repetitions on only 256 requests, not 768 independently sampled requests. This benchmark concerns the **original pointwise Utility gate**, not a timed version of the newer B4-A vectorized F-aligned gate.

**Table S10.11. Full-F original SASRec DEV warmed offline path time in milliseconds, 256 requests × three counterbalanced repetitions.**

| Frozen path | Mean | Median | P95 | P99 |
| --- | ---: | ---: | ---: | ---: |
| Always Base | 0.72759 | 0.72228 | 0.87052 | 0.92766 |
| Always Memory | **0.69165** | **0.65672** | 1.08878 | 1.45743 |
| Frozen Utility selective | 1.76941 | 1.70132 | 2.29003 | 2.52290 |

The selector made **80/256 = 31.25%** Memory calls per repetition, or 240/768 across repeated paths. Component means were 0.49876 ms Base scoring, 0.37267 ms feature construction, 0.55889 ms HGB inference, and 0.13205 ms conditional Memory work (including no-call events). Python, ranking and synchronization overhead mean these component subtotals should not be confused with the complete path latency.

**Offline source setup is measured separately**, not converted into online per-request latency: the source scan of 30,307,513 G1 causal rows and historical snapshot preparation took 36,365.796 ms for the batch; sweeping all room-author activity intervals and constructing the 256 candidate lists took 10,808.702 ms. Warmup cost was 156.526 ms and excluded. Peak allocated GPU memory was 254,739,968 bytes and the measured process RSS peak was 2,003,344 kB (PyTorch 2.4.1+cu124). These metrics do not measure online incremental state maintenance, production batching, network/queueing, energy, or money.

The underlying original G3 replay projects the author column while scanning a G1 stream with TRAIN/DEV/TEST-marked rows, **skipping TEST-marked rows before adding authors to any DEV historical state**. No private B4-A A1/A4 outcomes were accessed and no new TEST event ranking metrics calculated. Accordingly, do not claim no TEST-tagged source column was *physically projected* during the global scan; the supported claim is no B4-A target outcome use or TEST evaluation.

The earlier single-pass warmed G4 DEV microbenchmark reported means of 1.4245/0.8033/1.8018 ms for Always Base/Memory/Utility. Its order sensitivity and incomplete source accounting differ, but both real timing exercises show that fewer calls do not automatically make this Utility implementation faster than unconditional Memory. The new [C2-B Actions run](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38530526158) and the audit report N10_ROUTE_C_C2B_MATCHED_DEV_COST_AND_R2_VERDICT_2026-10-14.md identify exact source SHAs, device, full warm execution and limitations. Thus the supported decision claim concerns **quality under a stated specialist-call budget**, not proven online resource savings.

## S10.18 Frozen relation-history null controls: B2 DEV versus B4-A H2

The B2 1,024-request/992-user post-G5 exploratory DEV historical-null study and the B4-A 4,096-request/3,059-user presealed additional-target H2 analysis use the same family of fixed-F candidate-preserving, time-valid, author-hour-margin-preserving, closed-hour activated historical-source permutations. Both use fixed original Full Memory scoring and the three null seeds 20261014, 20261015 and 20261016. The seeds are three interventions on one cohort in each study, not three independent cohorts.

**Table S10.12. Historical-null validity and popularity diagnostics on the two distinct cohorts.**

| Validity check | DEV (1,024) | Added targets (4,096) |
| --- | --- | --- |
| Fixed Full-F candidates | PASS | PASS |
| Scorer / Top-10 parity | PASS | PASS |
| Time, hourly margin, active | PASS | PASS |
| Post-hour-only swaps | PASS | PASS |
| History edges rewired | ~78.62% | ~76.78–76.80% |
| Original Full-F NDCG | 0.339348 | 0.334942 (weighted) |
| Null 20261014 | 0.306491 | 0.303905 (weighted) |
| Null 20261015 | 0.303804 | 0.304689 (weighted) |
| Null 20261016 | 0.305321 | 0.302796 (weighted) |
| Cohort TRAIN Popularity | **0.021867, verified** | **Not frozen before A4** |
| Null above Popularity | **PASS (DEV)** | **NOT VERIFIED AS PREDECLARED** |
| Independent later TEST | No | No |

The B4-A Null rankings retain 1,903–1,913 positive Top-10 outcomes and each has weighted Full-F NDCG above 0.10, but these **partial nondegeneracy indicators do not establish the missing same-cohort TRAIN-popularity margin**. The B2 completed control cannot be imported to certify B4-A. Any check performed for this missing B4-A margin after A4's first reveal would be post hoc and cannot retroactively establish a pre-unseal acceptance condition.

The historical intervention also changes repeated viewer–creator pairs and higher-order structures, not solely a single semantic relation. The measured original-versus-null contrast establishes nontrivial value of the *whole authentic source arrangement* under strong constrained rewiring, not the unique causal effect of one relation feature. Both cohorts are from an already accessed overall M3 source; the B4-A additional targets do not provide future-period transfer. Independent [C3-A frozen public audit #38530145391](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38530145391) supports the distinctions without additional TEST evaluation.


## S10.19 Supporting evidence for relationship utility and candidate-aligned decisions

This section preserves the complete source tables underlying the main article’s retrospective history-state, DEV candidate-supervision and pretarget feature analyses. These analyses complement the main frozen selection and authentic-history comparisons. Each table retains its original evaluation cohort, candidate regime and statistical interpretation; development analyses are explicitly distinguished from held-out evaluation.

**Table S10.13. Retrospective relationship-evidence states on frozen Twitch TEST (44,221 streamer-ranking requests).**

| Retrospective evidence state | Events | Base NDCG@10 | Memory NDCG@10 | Memory − Base | User-bootstrap 95% CI |
| --- | ---: | ---: | ---: | ---: | --- |
| Represented | 24,285 | 0.86102 | 0.84167 | −0.01935 | [−0.02234, −0.01633] |
| Recoverable outside Base input | 5,539 | 0.30181 | 0.52225 | **+0.22045** | [+0.21140, +0.23001] |
| Unavailable in prior history | 14,397 | 0.21948 | 0.03734 | −0.18215 | [−0.18681, −0.17715] |

The three groups sum to all 44,221 frozen Twitch TEST events. The 95% intervals use 5,000 user-paired bootstrap resamples within each group. Group membership is computed from the observed target **only after the outcome**; the labels are neither predictive features nor information available to an online policy. The corresponding main-text figure visualizes the same retrospective state contrast across development and held-out events.

**Table S10.14. M3 exploratory DEV user-disjoint candidate-supervision transfer (50,049 author-ranking DEV events; 12,628 users).**

| Base | Training supervision → evaluation candidates | Full-F NDCG@10 | Realized Memory calls |
| --- | --- | ---: | ---: |
| SASRec | Sampled S → full F | 0.296499 | 14,988 |
| SASRec | Full F → full F | **0.302658** | 15,016 |
| SASRec | Full-label adapted → full F | 0.301847 | 14,954 |
| GRU4Rec | Sampled S → full F | 0.298123 | 15,001 |
| GRU4Rec | Full F → full F | **0.303093** | 14,762 |
| GRU4Rec | Full-label adapted → full F | 0.303000 | 14,989 |

The sampled S labels are constructed retrospectively by retaining the observed positive author on DEV; all real policy features are computed from full-F candidates and earlier information. The adapted condition uses full-F training labels on outer-fold training users rather than label-free adaptation. Actual outer-fold calls are not strictly equalized. The full-supervised gains over S-supervised are **+0.006159** (SASRec; paired 95% CI [+0.004835, +0.007543]) and **+0.004970** (GRU4Rec; [+0.003550, +0.006369]); 10,672/50,049 (21.32%) and 11,517/50,049 (23.01%) decisions disagree, respectively. This is an **exploratory DEV** analysis, not an independent held-out TEST or an additional prespecified hypothesis family. Additional DEV methodology and mechanism details remain in earlier S10 sections.

\newpage

**Table S10.15. M3 exploratory DEV historical-component ranking under identical events but different candidate regimes (50,049 events).**

| Fixed knowledge source | Full-active F NDCG@10 | Retrospective sampled S NDCG@10 |
| --- | ---: | ---: |
| Full Memory (unchanged mixture) | **0.343509** | 0.668498 |
| Long-only | 0.333231 | **0.773602** |
| Short-only | 0.273839 | 0.407506 |
| TRAIN-only author popularity | 0.022215 | 0.197796 |
| History-score-placement control | 0.007576 | 0.189571 |

The historical-source composition, sampled ranking and information content refer to the same development events. The history-placement control does not maintain global user–author marginals. On matched full-F events, Full minus Long-only is +0.010278 with user-paired 95% CI [+0.007906, +0.012668]; on sampled S it is −0.105104, CI [−0.108326, −0.101683]. This does **not** identify an independent source-specific causal mechanism, since the candidate and evaluation regime change.

**Table S10.16. Twitch DEV-only OOF ablation of pretarget feature families (46,878 events; 6,563 retrospectively matched Memory invocations).**

| Gate feature family | Dimensions | NDCG@10 gain over DEV Base | Paired 95% CI | Spearman correlation |
| --- | ---: | ---: | --- | ---: |
| History descriptors | 6 | +0.00372 | [+0.00256, +0.00490] | 0.14791 |
| Base-score descriptors | 8 | +0.00160 | [+0.00048, +0.00270] | 0.09109 |
| History + Base scores | 14 | **+0.00838** | [+0.00713, +0.00963] | **0.18990** |

The common DEV count was selected by the combined-feature fit. Its 95% intervals resample fixed, fitted OOF event-level outcomes. This ablation is **not** additional frozen TEST and does not isolate a causal effect of any one feature. 

The frozen 30,000-target candidate-supervision contrasts and the nested 4,096-target authentic-versus-null history comparison are reported in the main Results. Supplementary S10.15–S10.18 provide the related sampling, statistical, source-control and measured-cost details, including the unverified original cohort-specific popularity acceptance condition.
