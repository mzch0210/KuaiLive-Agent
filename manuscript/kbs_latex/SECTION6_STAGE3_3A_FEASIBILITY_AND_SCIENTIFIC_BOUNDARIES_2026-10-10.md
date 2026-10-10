# Section 6 Stage 3A — Evidence-boundary and P2 feasibility audit

**Date:** 2026-10-10. **Status:** Stage 3A evidence and input verification completed. The KuaiLive candidate-draw P2 is a separate retrospective scoring run, **not certified until historical P0 per-user replay and all prespecified draws pass**. Approved outline C1–C3 and the frozen Twitch TEST gate remain unchanged.

## 1. Scientific interpretation of Stage 2

**C1 / Memory components:** On Twitch DEV (n=46,878), the target-defined recoverable subset (n=5,879) has Base NDCG@10 0.30201, Long-only 0.63890, and frozen Full Memory 0.53298. The direct paired Long-only minus Full estimate is +0.10592 (95% conditional paired interval [+0.10096,+0.11061]). Long-only does not win universally: it trails Full in the unavailable subset (mean difference about −0.03208) and both variants trail Base on overall DEV. **Decision:** The fixed expert is a prespecified interpretable scoring rule, not an ex-post optimal mixture; component results are descriptive, target-dependent rankings and do not identify causal Long/Short/Popularity effects or permit revising the frozen expert after seeing TEST.

**C3 / multiple selection budgets:** Combined 14-feature Utility versus Base gains in original Twitch DEV OOF at 5/10/15/20/30% batch top-count are +0.00598, +0.00774, +0.00832, +0.00792, +0.00736. They exceed the two restricted groups on this finite grid; Base-score-only is negative at 30%. **Decision:** These are unadjusted pointwise bootstrap intervals conditional on fitted OOF predictions, choices and budgets, not simultaneous confidence bands, nested-hyperparameter uncertainty, a prospective online fixed-quota policy, or new TEST replication. Current main §6.4 and draft S4/S7 correctly limit their conclusions. No further Gate target model or strong-Base retraining is needed without a new concrete objection.

## 2. KuaiLive P2 feasibility directly confirmed from immutable source files

The exact original Room and Streamer P0 checkpoint files were recovered from [run 37746520476, artifact 11536890439](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476), and **both were hashed from downloaded ZIP content**:
- Room SHA256: b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7
- Streamer SHA256: 82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945

The original model-input [run 37741843252, artifact 11534262601](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37741843252) contains room/streamer maps, session intervals, and historical train, DEV and TEST CSVs; all three Room input SHA256s verified from downloaded bytes:
- Train: ad91413537175b9f6e9013c525a552b6004cc00e029b41360f08519e0735b5b4
- DEV: 46dd3081688468c89acf6366d36d87c122fa45850ddb69320c05da9de94a9f54
- TEST: 3491862df4de5cfb487fbd21c2f62c2d1d62acac110f852cc83c019dfcc6e956

Archived original per-user factorial scores are in [run 37751814645, artifact 11538678848](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645). That compact archive **does not contain per-event raw full-active Room/Streamer logits**, so those must be recomputed **once per event** from the exact original model pair, then checked against each of the **10,222 original user-level P0 outcomes**, before any new P2 results can be accepted.

**Important negative sampling rule:** The original room exporter [source](../../src/kuailive_agent/export_rechorus_room.py) draws at-time-active, distinct candidate rooms, excluding the current positive target but **not all historically interacted rooms**. Original 575-list TEST inspection shows 601 intersections with prior interacted rooms across 433 users. Consequently, excluding prior-room interactions from newly sampled candidates would **change the protocol**. For P2, uniformly draw without replacement from full-active eligible rooms except current target; include target once. Original full-candidate membership and exact room-session timing stay unchanged.

## 3. Stage 3B predeclared protocol and audit gates

Scientific status: P2 is **conditional retrospective sensitivity on previously inspected KuaiLive TEST**, not independent frozen validation or retraining. The [immutable-in-advance protocol](SECTION6_STAGE3_P2_PREDECLARED_PROTOCOL_2026-10-10.md) specifies three total candidate sizes **128, 256, 575**, three draws per size using fixed RNG seeds **20261010, 20261011, 20261012**, plus original 575 and full-active references. Same 10,222 users/events, P0 checkpoint SHA, Memory, alpha room **0.125**, per-branch standardization and target-rank convention. Primary quantities: signed Memory−Base NDCG@10 under each draw and fixed Full−Sampled contrast. Each condition has 3,000 paired user-bootstrap resamples conditional on fixed scores and draw. Between-draw dispersion is separate from user-bootstrap and earlier trained-model seed SD. The optional algebraic 2×2 allocation is descriptive and noncausal.

P2 must **abort** for any source mismatch, target/candidate eligibility mismatch, non-finite score, failure of ANY original per-user Base-SS/Base-FF/Memory/delta score at 1e−11 tolerance, incomplete user count or 2×2 identity failure. All nine draw outcomes, including null/negative reversals, must be reported. No TEST alpha, Memory weights or threshold can be tuned or outcome-based draws selected.

**Execution environment:** ephemeral **GitHub-hosted CPU only**, with read-only repository permission, not the project's private self-hosted GPU runner with its explicit owner-only confirmation guard. The initial hosted job [38013914045](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38013914045) failed during cross-run artifact retrieval (the download action defaulted to looking in its current run), before original TEST scoring or any P2 result. The pinned-run-ID correction is executed via a separate workflow. This is an infrastructure failure, not scientific evidence. The protocol and seeds were not revised in response.

## 4. Stage 3 decisions

- **3A completed**: scientific claim boundaries reviewed; original SHA-verified P0 models and inputs are recoverable; exact source sampling semantics identified.
- **3B conditional P2 initiated**: must verify score reproduction and all nine draws from a successful exact-source run; do not report success before it happens.
- **3C extra Gate objectives deferred**: the paper does not claim novelty from a universal optimal expert router or require new predictive targets to make C3 valid.
- **3D strong Base re-training, additional seeds and deployment throughput deferred**: the manuscript compares against its designated fixed Base and already documents limited baseline checks and measured resource overhead.
- **Publication step:** S1–S9 formal supplement packaging, cross-section checks and coauthor review remain open; leave original §6.3 unchanged unless full validated P2 warrants a carefully bounded supplemental statement.

**External primary method source:** Krichene & Rendle, *On Sampled Metrics for Item Recommendation*, Communications of the ACM 65(7):75–83 (2022), DOI [10.1145/3535335](https://doi.org/10.1145/3535335). General sampled-ranking inconsistency is previously established, not a new theorem from this manuscript.
