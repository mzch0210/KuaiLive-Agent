---
title: "Supplementary Information"
subtitle: "When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation"
author: "Anonymous manuscript — Knowledge-Based Systems"
date: "10 October 2026"
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

**Scope.** This manuscript-specific supplement reports the public data protocols, model freezing, conditional uncertainty, full numerical experiments and source provenance for C1–C3. Main text conclusions do not change. Retrospective KuaiLive TEST and exploratory Twitch DEV are **not** independent confirmation of the one-shot frozen Twitch TEST Utility selector.

**Statistical convention.** Unless noted, percentile bootstrap intervals condition on observed users, trained checkpoints, exact candidate draws and policies. Three fitted checkpoint seeds, three negative-list random seeds and user-bootstrap replicates are distinct uncertainties. None represents independent data replications or multiplicity-adjusted simultaneous inference.

**Access.** The public [KuaiLive dataset](https://zenodo.org/records/16565801) and [LiveRec/Twitch repository](https://github.com/JRappaz/liverec) have separate licenses; archived GitHub Actions artifacts may expire and cannot be represented as permanent public DOIs. [Companion research code](https://github.com/mzch0210/KuaiLive-Agent).

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

### S1.3 Candidate and identity validation

KuaiLive predicts rooms, but relationship Memory aggregates prior events by the mapped streamer; several candidate rooms can therefore share a specialist score. Twitch ranks streamers directly. Deterministic item identifiers break score ties. Source-file train/DEV/TEST byte hashes, matched cohort identity, historical model mappings, and session eligibility guards are pinned in **S2/S5**. Raw public data and derived processed candidate lists should not be treated as the same downloadable artifact; the derived lists are reconstructable only with the documented code, preprocessing and fixed RNG choices.

For the original KuaiLive P0 files, SHA256: **train** `ad91413537175b9f6e9013c525a552b6004cc00e029b41360f08519e0735b5b4`; **DEV** `46dd3081688468c89acf6366d36d87c122fa45850ddb69320c05da9de94a9f54`; **TEST** `3491862df4de5cfb487fbd21c2f62c2d1d62acac110f852cc83c019dfcc6e956`. These fingerprints identify the **P0 processed Room files**, not checksums for the original Zenodo dataset archive or all platform variants. They were checked from [source artifact 11534262601](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37741843252/artifacts/11534262601).

### S1.4 Evidence and access statement

Data-provenance evidence: [KuaiLive official dataset repository](https://github.com/imgkkk574/KuaiLive), [KuaiLive Zenodo record](https://zenodo.org/records/16565801), [LiveRec original repository](https://github.com/JRappaz/liverec), [KuaiLive active-room exporter](https://github.com/mzch0210/KuaiLive-Agent/blob/main/manuscript/kbs_latex/src/kuailive_agent/export_rechorus_room.py), and the [P2 source-pinned eligibility audit](https://github.com/mzch0210/KuaiLive-Agent/blob/main/manuscript/kbs_latex/SECTION6_STAGE3_3A_FEASIBILITY_AND_SCIENTIFIC_BOUNDARIES_2026-10-10.md). The original datasets' access and license conditions govern further distribution. This supplement references public repositories and **does not redistribute proprietary or anonymized raw interaction files**. Preserve the precise derivation pipeline rather than infer fields or raw source SHA values not available in the evidence records.

**Boundary:** KuaiLive post-hoc TEST analyses and Twitch frozen one-shot TEST serve **different evidentiary purposes**. No source cohort is a random sample of all live-streaming platform users. These protocol definitions are observational; neither a sampled non-target nor a lack of recorded history proves negative preference or true ignorance.

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

### S2.4 Statistical freeze checklist

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

### S3.4 Preventing cross-protocol baseline misidentification

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

**Submission organization:** One concise robustness paragraph appears in Results Section 6.3; all per-draw outcomes, confidence intervals, original rank reproduction and factorization belong here. The three alternative *training*-seed model realizations are reported separately in S8, not as nine new independent checkpoint seeds. The paired-draw estimates and the three independently trained checkpoint realizations address distinct sources of uncertainty.

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

# S7. Twitch DEV out-of-fold feature-family invocation budgets

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

## S7.5 Reproducibility

Original archive member SHA256s:

- OOF predictions: `25b5e560ce67d16221e483e9c18cad679eb28525ce0a8279ae91555726547627`.
- Original 3-family comparison: `58d835e0ae53c43fe1ae522fdefee83374ba4ae58900968ea741780cffe92e48`.

Reproduction source: [analysis/kbs_section6_stage2_dev_replay.py](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_section6_stage2_dev_replay.py). Input files reside in archived artifact **10688746451**. Its output tables contain **all six prediction orderings at the five budgets plus the original 6,563-call reference**, and direct paired contrasts for each; the entire output can be regenerated from archived inputs without model training. 


---

# S8. KuaiLive training-initialization sensitivity and evidence-state decomposition


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

### S8.5 Evidence status and incomplete generalization

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

## S9.6 Reproducibility audit and critical exclusions

- Formal run: [35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758), complete [artifact 10694941935](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758/artifacts/10694941935).
- Gate compression: [35571827672](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35571827672), 3 successful replicas and pooled final artifacts.
- Scripts: [formal aggregation](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_formal_efficiency.py), [cache probe](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/kbs_efficiency_stack_probe.py), [gate-compression benchmark](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/gate_compression_latency.py), and [replica aggregation](https://github.com/mzch0210/KuaiLive-Agent/blob/main/analysis/aggregate_inference_latency.py).
- Nontransferability: frozen Twitch selection uses 6,650/44,221 = **15.04%**, official LiveRec Base and availability-aware streamer candidates. **No Twitch end-to-end latency was measured**, so KuaiLive milliseconds are not transferable to it.
- Selection-mask replay, cache assumptions, heterogeneity of hosts and absence of queueing, online feature recomputation or network I/O prevent deployment-level SLAs or claimed cost reductions.
- 


---

## Source hierarchy and bibliographic anchors

The main one-shot frozen Twitch TEST evaluation is [run 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303). DEV diagnostics include runs 35698158121, 35713931454, 35724784990, 35725938757, 35877647543 and 37959745609. KuaiLive fixed-model candidate diagnostics are post-hoc runs 37751814645 and 38014145900. The warm CPU benchmark is a separate workload. All recorded hashes are tied to their stated source files and must not be silently generalized to historical unverified checkpoint binaries.

**References.** Qu et al. (2026), *KuaiLive: A Real-time Interactive Dataset for Live Streaming Recommendation*, SIGIR 2026 ([official repository](https://github.com/imgkkk574/KuaiLive)); Rappaz, McAuley and Aberer (2021), *Recommendation on Live-Streaming Platforms: Dynamic Availability and Repeat Consumption*, RecSys 2021, 390–399 ([source](https://github.com/JRappaz/liverec)); Krichene and Rendle (2022), *On Sampled Metrics for Item Recommendation*, *Communications of the ACM*, 65(7), 75–83, [DOI 10.1145/3535335](https://doi.org/10.1145/3535335). The last work precedes this study; sampled metric ranking inconsistency is not claimed as a new theorem.
