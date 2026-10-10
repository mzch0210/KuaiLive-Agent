# S3. Designated Base and auxiliary comparator performance under bounded training protocols

### S3.1 Purpose and comparison policy

This appendix documents why the designated sequential Bases are credible operational references for the scientific estimand **Memory minus a fixed Base**, rather than claiming they are universally optimal recommenders. KuaiLive and Twitch have different tasks, item units, architectures, histories and availability protocols; **never compare their absolute NDCG values as if they were one leaderboard**. Within-platform comparisons are reported only at the corresponding candidate and event protocols. Auxiliary model training budgets differ; this table is descriptive and not an exhaustively tuned state-of-the-art contest.

### S3.2 Twitch DEV: same frozen users/targets/candidates

All four rows below correspond to the same **46,878 Twitch DEV events**, with strict-before-target history reconstruction. Auxiliary small sequential architectures were trained for **five epochs** under a restricted BPR-based configuration; they are **not** proven equivalently tuned or directly comparable in capacity with the official LiveRec model.

| DEV method | NDCG@10 | HR@10 | Role/qualification |
|---|---:|---:|---|
| Official LiveRec Base | **0.571853** | **0.749712** | Designated frozen reference, context plus repeat component |
| GRU4Rec-small | 0.257268 | 0.387623 | Auxiliary BPR-trained model, five training epochs |
| SASRec-small | 0.171488 | 0.272260 | Auxiliary BPR-trained model, five training epochs |
| Popularity | 0.085889 | 0.145932 | Non-personalized baseline |

The frozen LiveRec pipeline's 46,878 matched user/target/step triples were reconstructed without identity mismatches; score comparisons use the same target and availability-aware candidates. Primary source: [Twitch comparison run 35815886641](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35815886641), [archived structured results 10732332430](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35815886641/artifacts/10732332430), files \`twitch_dev_strong_base_benchmark.csv\` and \`.json\`. The original source JSON explicitly says the smaller architecture alternatives are not exhaustive reproductions.

### S3.3 KuaiLive: same frozen evaluation protocol, distinct from paired P0

The comparison below is an **independent KuaiLive strong-reference panel** evaluated under its own matched active-room 575-candidate protocol. It **does not reuse** the P0/P1 room/streamer checkpoint pair of the §6.3 factorial study. For newly trained GRU4Rec and ContraRec–BERT4Rec, the configuration was selected **by DEV NDCG@10**, and TEST was intended for reporting only. Learning-rate configurations were limited and unequal across models.

| KuaiLive method | DEV NDCG@10 | TEST NDCG@10 | Experimental role |
|---|---:|---:|---|
| Dual-ID SASRec, auxiliary benchmark checkpoint | **0.621344** | **0.617142** | Designated benchmark Base in this separate panel |
| Streamer-SASRec component | 0.611519 | 0.609928 | Within-panel encoder branch |
| ContraRec–BERT4Rec | 0.4054 | 0.3703 | Limited grid, selected configuration lr=0.0005, best epoch 30 |
| Room-SASRec component | 0.355284 | 0.315369 | Within-panel encoder branch |
| Popularity | 0.296755 | 0.289446 | Same-protocol nonpersonalized ranking |
| GRU4Rec | 0.2788 | 0.2716 | Limited grid, lr=0.0005, best epoch 1 |

The full-precision original metrics are archived, and displayed values are rounded to avoid false numerical precision for parsed trainer logs. Source: [comparison result 35820514662](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35820514662), [artifact 10733131820](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35820514662/artifacts/10733131820), files \`kuailive_strong_base_benchmark.csv\`, \`.json\`, and \`RECOVERY_PROVENANCE.json\`. The GPU training occurred in [run 35814173574](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35814173574); the later result recovery parsed immutable logs after the first controller's metric parser failed on a punctuation detail. It **did not retrain models**. Full rerunnable training commands and original logs should accompany any separately deposited reproduction archive.

### S3.4 Preventing cross-protocol baseline misidentification

| Experimental comparison | KuaiLive sampled Base TEST NDCG@10 | May be paired with P0 Memory 0.565887? |
|---|---:|---|
| Native/historical sampled-active policy | **0.60784** | **No**, different training/fusion protocol |
| Separate reference competitiveness bundle | **0.617142** | **No**, different checkpoint |
| Matched candidate P0 source, 20260918, α_room=0.125 | **0.6070916** | **Yes**; P0 sampled Memory = 0.5658875 |
| P0 matched full-active | **0.3857124** | **Yes**; P0 full Memory = 0.4320191 |

Different score normalization/reference candidate sets also prevent swapping sampled/full Base scores in a single event-level paired difference. The P0 event-level contrast must be computed with its original checkpoint, candidate universe and score-standardization rule: **−0.041204 sampled, +0.046307 full, shift +0.087511**.

**Reviewer-relevant boundary:** Under unequal training budgets, these checks support a designated reasonable fixed Base, not a claim that every comparator has been equivalently optimized or that the method is state of the art. Rerunning all baseline grids is not necessary for the paper's restricted Base-relative estimand, but a future broader SOTA claim would require a separately designed tuning-fair benchmark.