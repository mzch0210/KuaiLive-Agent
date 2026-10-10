# S2. Model training, frozen evaluation, and artifact provenance

### S2.1 Freeze hierarchy and fit/evaluation boundary

This supplement records **what was fixed, when it was scored, and which comparisons may use post-outcome information**. A source or workflow date is an archive provenance datum, **not** a substitute for an independently timestamped preregistration.

| Evidence tier | Dataset | Fit/selection information | Evaluation status | Appropriate scientific claim |
|---|---|---|---|---|
| Primary pointwise Utility policy | Twitch/LiveRec TEST, 44,221 events | LiveRec Base and DEV-trained 14-feature Utility estimator; threshold chosen on 46,878 DEV OOF events | **Single frozen TEST evaluation** | Conditional selector value versus matched Base; retrospective Difficulty at realized call count |
| Feature/Memory/recency/context analysis | Twitch DEV, 46,878 events | Existing OOF vectors and fixed ranking models; separate retrained context Bases when specified | **Development-only exploratory diagnosis** | Subgroup patterns, observed finite-grid sensitivity |
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

| Paired KuaiLive checkpoint seed | Room-SASRec checkpoint SHA256 | Streamer-SASRec checkpoint SHA256 | Training identity |
|---|---|---|---|
| 20260918 | \`b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7\` | \`82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945\` | Original replayed P0 model pair |
| 20260919 | \`395d1b1c881d20cbda5d24c36c30685fd1524a0ec98586c8c71ad7c245505b2a\` | \`9f1b11cf27e0c802f71bb8b1bef646bb392b28d560e3aabda03f36fe01e2b637\` | P1 newly fitted pair |
| 20260920 | \`84c4ef5e45592fc480096dfe4e501046ede37c1f936484ed83f3bd56e1f49191\` | \`7043b275b56a75fd5d7aeadfd7e69d5447128ce9f55f3bd6a0f275a24dd2d144\` | P1 newly fitted pair |

The first model pair and processed train/DEV/TEST inputs were independently rehashed from archived original file **bytes**, and each of **10,222** event-level sampled/full Base and Memory outcomes was reproduced before P2 generated any new candidate lists. Three fitted training seeds share the **same users** and report across-initialization SD rather than independent sample replication. For detailed estimator outcomes and source identifiers, see S5/S8.

- Original training/paired factorial run: [37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645), [factorial artifact 11538678848](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538678848); original source model/data artifacts [11536890439](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476/artifacts/11536890439), [11534262601](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37741843252/artifacts/11534262601).
- Original ReChorus code revision **c164ec4303cc20ddcfbd1b57de366a481811d1e5** for the fixed experimental pipeline.
- P2 code [analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py](../../analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py); execution [38014145900](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900) with [result artifact 11655273833](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900/artifacts/11655273833).

**Completeness limitation:** A matched SHA256 for **every historical native-policy Twitch/KuaiLive Base checkpoint** is not established by the source files examined in the project ledger. The exact checkpoint identities listed above apply to P0/P1/P2, not all historical native-policy baselines. Missing upstream hash entries are **unverified**, not assumed equal to any existing model.

### S2.4 Statistical freeze checklist

All performance results are NDCG@10 computed over one positive target per evaluated event, with HR@10 secondary where shown. Mean *paired* differences are calculated on the **same** users within a protocol. Twitch TEST intervals: 5,000 paired-user bootstrap resamples. KuaiLive P0/P2: 3,000. One user-target per protocol row permits user bootstrap; if global-time panels contain repeated users, user-cluster resampling is required. The S4/S7 DEV intervals condition on observed target-defined group membership, OOF scores, the event-ranking masks and their selected budgets. No reported pointwise CI is a multiple-comparison-adjusted simultaneous confidence region.

The integrity target is **claim-to-artifact reproducibility**, not unrestricted access to private model training hardware. GitHub Actions artifact retention is finite; the appendices report run IDs, SHA values where verified, and reconstruction code but do not promise a permanent archival DOI unless one is actually minted.