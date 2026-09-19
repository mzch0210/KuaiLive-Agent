# KuaiLive-Agent — Project Status, Optimized Main Experiment Plan, and Compute Feasibility

**Snapshot timestamp:** 2026-09-19 19:16:38 EEST (UTC+03:00) / 2026-09-19 16:16:38 UTC  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Purpose of this file:** provide a self-contained handoff for another GPT account/research collaborator so they can understand the project state, validated findings, novelty risks, the frozen research claim, the next main experiments, and the GitHub Actions compute constraints without reconstructing the full chat history.

---

## 1. Current research question and recommended framing

The project began by asking whether an explicit memory/planning agent could outperform strong sequential recommendation baselines in livestream commerce recommendation. The evidence now rejects the simple claim that an always-on agent is superior.

The strongest current formulation is:

> **When does explicit memory provide positive marginal predictive utility beyond a strong sequential recommender, and can that value be predicted well enough to invoke memory selectively?**

Recommended working title:

> **Learning When to Invoke Memory: Confidence-Guided Selective Memory Augmentation for Live-Streaming Recommendation**

Avoid using **“When Should a Recommender Think?”** as the main title/framing. A direct 2026 collision exists with DS-Frame, *Recommender System as Slow and Fast Thinkers* (CIKM 2026 / arXiv 2609.02671), which already studies Fast/Slow systems, learned routing, difficult users, long histories, and accuracy–efficiency trade-offs.

The contribution should therefore be framed as **conditional relative utility estimation for an explicit memory expert**, not generic routing, generic adaptive computation, generic uncertainty-aware recommendation, or “agentic recommendation” in the broad sense.

Core formalization:

\[
\Delta_{memory}(x) = U(\text{MemoryExpert},x)-U(\text{BaseSequential},x)
\]

Learn:

\[
\hat{\Delta}_{memory}(x)=f(\text{user state},\text{base-model confidence})
\]

Invoke memory only if:

\[
\hat{\Delta}_{memory}(x)>\tau
\]

Use the terms **marginal predictive utility**, **conditional relative utility**, or **memory escalation**. Do **not** call this a causal treatment effect because there is no randomized intervention.

---

## 2. Data and current task definition

### 2.1 Current primary development dataset

KuaiLive public dataset, scope restricted to:

`live_content_category == "shop"`

Current retained shop sample:

- raw click rows: 4,909,515
- retained shop clicks: 446,952
- retained users: 15,114
- retained streamers: 51,521
- retained live rooms: 197,789
- eligible leave-one-out users: 10,222
- train: 419,841 events
- dev: 10,222 events
- test: 10,222 events

### 2.2 Important current task limitation

Most validated results so far predict **streamer_id**, not **live_id / room-level targets**.

This is scientifically important. The official KuaiLive preprocessing ultimately maps author/streamer interactions to the contemporaneous `live_id`, and WWW 2026 DCGLive explicitly establishes room-level dynamics as a central live-streaming recommendation problem.

Therefore the next main task should be:

> **Primary: next live-room recommendation.**

The memory expert should store persistent user–streamer affinity, while the prediction target is the ephemeral current live room:

\[
Score(room)=BaseRoomScore(room)+MemoryAffinity(streamer(room))
\]

Keep current streamer-level prediction only as a **secondary relationship-memory analysis**.

This room-level experiment is the first major kill gate for the current story: if selective-memory gains disappear completely when the target changes from streamer to room, the current mechanism may have been overly favored by repeated-streamer prediction.

---

## 3. Current validated results

### 3.1 Initial transparent memory/planning policies

On 999 active-at-time negatives before strong-baseline correction, the main result was:

- `MemoryFusion` was the strongest transparent policy overall.
- `MemoryPlanner` slightly beat `LongMemory` but did **not** beat `MemoryFusion`.
- Always-on planning therefore failed the original hypothesis.

Representative three-seed means:

- MemoryFusion NDCG@10 ≈ 0.4933
- MemoryPlanner NDCG@10 ≈ 0.4859
- LongMemory NDCG@10 ≈ 0.4818
- Popularity NDCG@10 ≈ 0.2068

Interpretation: memory mattered; fixed planning did not provide general incremental value.

### 3.2 Heterogeneity findings

Planner-vs-MemoryFusion benefit was not monotonic in state complexity. It showed an approximately U-shaped pattern:

- low complexity: positive planning delta
- intermediate complexity: negative
- high complexity: positive

Long-memory contribution showed a much cleaner mechanism:

- history 1–2: near zero
- 3–5: small positive
- 6–10: larger
- 11–30: large
- 31–100: larger
- 101+: very large

Time reasoning helped primarily for users with high temporal regularity.

These findings motivated **selective invocation** rather than always-on planning.

### 3.3 Strong official sequential baselines

Official ReChorus SASRec/TiSASRec validation used a fair fixed candidate protocol of **574 legal active-at-time negatives + 1 positive** for every user.

Best configuration selected on dev:

- SASRec
- lr = 5e-4
- history_max = 50
- embedding = 64
- one layer

Strong baseline result:

- SASRec test NDCG@10 = **0.6101**
- SASRec test HR@10 = **0.7333**

Best TiSASRec was slightly weaker (~0.6039 NDCG@10).

This invalidated any claim that the transparent memory model alone beats a tuned strong sequential recommender.

### 3.4 Fair residual validation / Selective Agent v1

Using full per-user SASRec rankings, the project learned a dev-only gate to predict when `MemoryFusion` would beat SASRec.

Selective v1:

- SASRec NDCG@10 ≈ 0.61010
- Selective v1 ≈ 0.61442
- absolute gain ≈ +0.00432
- relative gain ≈ +0.71%
- bootstrap 95% CI strictly positive

Long-history users were the main subgroup where explicit memory could beat SASRec.

### 3.5 Selective Agent v2 — frozen validation

Locked primary v2 gate:

- model: HistGradientBoosting residual regressor
- agent alternative: MemoryFusion
- user-state inputs:
  - log history length
  - repeat rate
  - preference entropy
  - preference drift
  - time regularity
  - state complexity
- SASRec confidence/ambiguity inputs:
  - score std/range
  - top-score margins
  - top-score z-score
  - normalized score entropy
  - top-10 score mass
- threshold selected using **5-fold OOF dev predictions only**
- test used for one-shot evaluation

Frozen CI result:

| Method | Test NDCG@10 |
|---|---:|
| Always MemoryFusion | 0.567697 |
| Tuned SASRec | 0.610098 |
| **Selective Memory v2 (HGB primary)** | **0.623232** |
| ExtraTrees combined (secondary) | 0.625406 |

Primary v2:

- absolute delta = **+0.013134**
- relative delta = **+2.15%**
- paired user-level bootstrap 95% CI = **[+0.010114, +0.016310]**
- gate invokes MemoryFusion for 1,628 / 10,222 users = **15.93%**

Ablation evidence:

- history threshold only: ~0.61555
- state-only HGB: ~0.61558
- state-only Ridge: ~0.61639
- state + SASRec confidence Ridge: ~0.62178
- state + confidence Tree: ~0.62356
- state + confidence HGB: ~0.62323

Interpretation: the gain is not just “long history”. Base-model confidence/ambiguity adds substantial information about when memory is useful.

### 3.6 OOF split robustness

Across five different OOF fold random seeds:

- test NDCG@10 range ≈ 0.6200–0.6232
- all deltas positive
- all bootstrap CI lower bounds positive

### 3.7 Candidate-sampling robustness

Five active-negative sampling seeds all showed significant improvement:

| Candidate seed | SASRec | Selective v2 | Relative gain |
|---|---:|---:|---:|
| 20260918 | 0.610098 | 0.623232 | +2.15% |
| 20260919 | 0.609109 | 0.622921 | +2.27% |
| 20260920 | 0.605386 | 0.616594 | +1.85% |
| 20260921 | 0.609905 | 0.619280 | +1.54% |
| 20260922 | 0.605990 | 0.615309 | +1.54% |

Across all five:

- mean absolute delta = **+0.01137**
- mean relative gain = **+1.87%**
- minimum absolute delta = **+0.009319**
- minimum bootstrap CI lower bound = **+0.006659**

Thus the v2 result is not explained by one favorable candidate-negative sample.

### 3.8 Global temporal preliminary robustness

A leakage-aware global temporal landmark split used 80%/90% global time cutoffs:

- users: 3,878
- train rows: 280,706
- dev rows: 3,878
- test rows: 3,878
- candidates: 574 negatives + 1 positive

Results:

- SASRec test NDCG@10 = **0.493621**
- Always MemoryFusion = **0.499498**
- Selective v2 = **0.518484**
- absolute selective delta = **+0.024862**
- relative gain = **+5.04%**
- bootstrap 95% CI = **[+0.018044, +0.031789]**

This is encouraging, but the current temporal target is the **first** future-window event. RecSys 2025 work on global timeline splits indicates GTS-Last / GTS-Successive are more representative robustness protocols than GTS-First. Therefore this +5.04% result is **preliminary temporal robustness**, not the final temporal headline.

---

## 4. Novelty collision risk as of this snapshot

### 4.1 DS-Frame — HIGH collision at the high-level framing

`Recommender System as Slow and Fast Thinkers` (CIKM 2026 / arXiv 2609.02671) already contains:

- fast sequential recommender
- slow refinement path
- learned selector
- difficult-user routing
- longer-history users as a difficult subgroup
- computation-budget trade-off

Therefore avoid claiming novelty in “when should a recommender think?”, generic fast/slow inference, or learned adaptive routing.

Our defensible distinction must be:

> predict the **relative utility of a different inductive-bias expert — explicit persistent memory — over the strong sequential base**, rather than simply spending more computation on latent refinement.

### 4.2 GUIDER / uncertainty-aware recommendation — MEDIUM/HIGH collision

AAAI 2026 GUIDER already uses principled uncertainty decomposition to adapt recommendation/reranking.

Therefore current score entropy/margins should initially be called **confidence/ambiguity signals**, not principled uncertainty.

The method’s distinction is:

> confidence is used to estimate **memory marginal utility**, not directly to rerank/diversify recommendations.

### 4.3 DCGLive — HIGH importance as a domain-specific competitor

WWW 2026 DCGLive is a room-level dynamic graph model for live-stream recommendation and explicitly models user–streamer–room dynamics and new-room cold start.

Therefore room-level evaluation and DCGLive comparison are necessary for a high-quality live-recommendation paper.

### 4.4 LiveRec — important classical live-specific baseline

RecSys 2021 LiveRec established dynamic availability and repeat streamer consumption as core live-stream recommendation factors.

The paper should not claim that dynamic availability or repeat consumption are new observations.

### 4.5 KuaiLive-M3 — high-value untouched in-domain confirmation

Released in 2026 with 21,938 users, ~35M live interactions, multimodal live content, cross-domain short-video behavior, and questionnaire feedback.

Do not use KuaiLive-M3 to tune the architecture after seeing test results. Freeze the current method first.

---

## 5. Frozen main scientific claim

The claim to test going forward is:

> **A strong sequential recommender should remain the default. Explicit persistent memory should be escalated selectively when user-state and base-model confidence indicate positive conditional relative utility.**

Do not claim:

- “Agent beats SASRec” in general.
- “First selective recommender.”
- “First uncertainty-aware recommender.”
- “First memory recommender.”
- causal business/GMV lift.
- current MemoryFusion is an LLM agent.

The current MemoryFusion is a transparent memory expert. An LLM/tool-using layer, if added later, is a separate phase.

---

## 6. Optimized main experiment plan

The plan is intentionally reduced to five research questions. The goal is not “more experiments”; every experiment must eliminate a plausible collision-based alternative explanation.

### RQ1 — Effectiveness on the correct live-room task

**Question:** Does selective persistent memory improve strong recommendation when the target is the ephemeral live room rather than the already persistent streamer identity?

Primary task:

- KuaiLive Shop
- target = `live_id`
- memory key = persistent streamer relationship
- candidate set = legal active rooms at target timestamp

Compare:

1. Popularity / BPRMF
2. GRU4Rec
3. SASRec
4. TiSASRec
5. LiveRec
6. DCGLive
7. Always Memory
8. Always Base+Memory fusion
9. **Selective Memory v2**

Primary metrics:

- NDCG@10
- HR/Recall@10
- MRR

Statistics:

- paired user-level bootstrap, >=5,000 resamples
- absolute and relative delta
- Holm correction for multiple primary baseline comparisons

**Kill criterion:** if Selective Memory does not beat the strongest room-level base with CI lower bound > 0, do not retain a broad effectiveness claim.

### RQ2 — Distinctiveness from generic adaptive computation / routing

**Question:** Is the benefit specifically from selecting an explicit memory expert, or would generic slow computation / any router work equally well?

Must include DS-Frame as direct competitor.

Matched-budget experiment:

- same base backbone
- same candidate protocol
- match extra-path invocation rates (e.g. 5%, 10%, 20%, 30%)

Compare:

- random routing at matched rate
- history-length threshold routing
- DS-Frame slow path
- optional FamouSRec / heterogeneous MoE router
- **Selective Memory escalation**

Report:

- NDCG@10 vs invocation rate
- NDCG@10 vs wall-clock latency
- p50/p95 inference latency
- optional FLOP/parameter/memory overhead

**Interpretation rule:** if Selective Memory does not beat DS-Frame at matched budget, the paper must not claim that memory escalation is generally better than adaptive computation; it can still claim a distinct interpretable specialist.

### RQ3 — Mechanism and confidence calibration

**Question:** What information predicts positive memory utility?

Required ablations:

- history length only
- user state only
- raw base confidence only
- state + raw confidence
- state + calibrated confidence
- one epistemic uncertainty estimator (prefer 3-seed ensemble variance or MC dropout)
- oracle router
- random matched-rate router

Calibrate on dev only.

Report calibration diagnostics where applicable:

- ECE
- Brier score
- NLL

The desired conclusion is not necessarily “better uncertainty estimator wins”. A useful result would also be that cheap margins/entropy are sufficient for memory escalation.

### RQ4 — Evaluation robustness

#### RQ4a Full active candidate ranking

Make the main candidate protocol:

> rank against all legal currently-active candidates at the target timestamp.

Keep the existing 574-negative × 5-seed protocol as robustness only.

Use streaming/per-user ranking; do not materialize a giant dense user×candidate matrix.

#### RQ4b Temporal protocol

Replace GTS-First as the final headline with:

- GTS-Last
- **GTS-Successive** as preferred realistic temporal evaluation

The current GTS-First +5.04% remains preliminary evidence only.

**Kill criterion:** GTS-Successive should preserve a positive Selective-vs-Base delta; otherwise downgrade temporal-generalization claims.

### RQ5 — Frozen external confirmation and cost

Freeze the method before external data.

Recommended dataset roles:

1. **KuaiLive** — development dataset.
2. **KuaiLive-M3** — untouched in-domain confirmation.
3. **LiveRec Twitch 100k** — untouched cross-platform confirmation.

On external datasets:

- architecture/features remain frozen
- base model trains on train
- gate learns on dev
- test is evaluated once

At least one untouched dataset should show a positive bootstrap CI lower bound before claiming a generalizable principle.

Secondary live-commerce outcomes where supported:

- long-view
- comment
- like
- gift
- repeat vs novel streamer
- head vs tail streamer

Do not make causal GMV or purchase claims.

---

## 7. Experiment execution priority

### Phase A — highest priority / immediate

1. Implement KuaiLive **room-level** primary task.
2. Validate Selective Memory v2 on room-level target.
3. Implement full-active room candidate ranking.
4. Implement GTS-Last and GTS-Successive.

Decision point: if room-level mechanism survives, continue. If not, reassess before investing in expensive external baselines.

### Phase B — collision-defense experiments

5. Port/implement DS-Frame on the same backbone/protocol.
6. Implement/evaluate LiveRec.
7. Run DCGLive using suitable GPU infrastructure.
8. Run matched-budget routing/latency curves.

### Phase C — freeze and external confirmation

9. Freeze Selective Memory v2.
10. LiveRec Twitch 100k confirmation.
11. KuaiLive-M3 target-domain confirmation using external/self-hosted compute if needed.

### Phase D — optional enhancements

12. Confidence calibration / epistemic estimator.
13. Secondary engagement outcomes.
14. Only after the memory-escalation paper is stable, consider a genuine LLM/tool-using Agent layer.

---

## 8. GitHub Actions compute feasibility

### 8.1 Current repository / runner facts

This repository is public.

As of this snapshot, GitHub documentation states that standard public-repository GitHub-hosted Linux runners (`ubuntu-latest` / `ubuntu-24.04`) provide approximately:

- 4 vCPU
- 16 GB RAM
- 14 GB SSD

Standard hosted runners for public repositories are free/unlimited in runner minutes. A GitHub-hosted job has a maximum execution time of 6 hours.

Observed project wall-clock evidence:

- official 8-job SASRec/TiSASRec grid: ~3 h 03 min total wall-clock with parallel jobs
- four additional candidate-seed validations + preparation + summary: ~1 h 12 min wall-clock
- global temporal single frozen validation: ~26.5 min wall-clock

Thus ordinary KuaiLive CPU experiments are demonstrably feasible on current public standard runners.

### 8.2 Feasibility matrix

| Planned experiment | Standard GitHub-hosted runner? | Assessment |
|---|---|---|
| KuaiLive room-level preprocessing | **Yes** | GREEN. Existing 2.6 GB extracted KuaiLive fits 14 GB; stream/chunk processing. |
| Room-level SASRec/TiSASRec | **Yes** | GREEN/YELLOW. Existing streamer task completes comfortably under 6 h; room item universe is larger, so monitor memory and checkpoint size. |
| Full-active ranking | **Yes, if streaming** | GREEN/YELLOW. Score per user/event; never build full dense user×room matrices. |
| GTS-Last / GTS-Successive | **Yes** | GREEN. Closely related global-temporal run already finished in ~26 min. Successive may increase evaluation volume but can be sharded. |
| 5-seed robustness | **Yes** | GREEN. Proven by existing four-seed parallel workflow. |
| HGB gate / bootstrap / calibration | **Yes** | GREEN. Cheap relative to recommender training. |
| DS-Frame | **Probably yes on CPU with adaptation** | YELLOW. Public code supports CPU fallback when GPU is disabled, but defaults to GPU and SwanLab. Freeze small grid, disable tracking, keep each job <6 h. |
| LiveRec Twitch 100k | **Likely yes** | GREEN/YELLOW. 3M interactions / 100k users is substantially smaller than its full dataset and should be manageable with careful preprocessing. |
| DCGLive original implementation | **No, not on standard runner as-is** | RED. The released code calls `.cuda()` throughout, builds dense identity matrices, and materializes interaction-length embedding trajectories. Requires CUDA and substantial GPU memory or a major sparse/CPU rewrite. |
| KuaiLive-M3 full raw dataset | **No** | RED. Public release is ~61.1 GB, well above the 14 GB runner disk. |
| KuaiLive-M3 live-only targeted files | **Possibly preprocessing only** | YELLOW/RED. `live_interaction.csv` alone is ~4.57 GB; streamed preprocessing may fit, but 35M live interactions can make CPU SASRec training exceed the 6 h job cap. Prefer GPU/self-hosted. |
| Full KuaiLive-M3 multimodal experiment | **No** | RED. Multiple files are multi-GB and full dataset is ~61 GB; requires external/self-hosted storage/compute. |
| Large LLM agent inference/training | **No on standard runner** | RED unless using an external API; standard public runner has no GPU. |

### 8.3 The real GitHub bottlenecks

#### A. No GPU on standard runners

This is the main blocker for DCGLive and any serious LLM-based model.

The DCGLive release currently:

- selects a CUDA device;
- moves the model and tensors using `.cuda()`;
- creates dense `torch.eye(num_items)`, `torch.eye(num_users)`, and `torch.eye(num_streamers)` tensors;
- creates per-interaction embedding trajectories.

Therefore “just set CPU” is not sufficient. Either:

1. use a self-hosted GPU runner;
2. use a paid GitHub GPU larger runner if the GitHub account/organization plan supports it;
3. run DCGLive externally and import frozen predictions/results;
4. perform a substantial sparse implementation rewrite.

Option 1 or 3 is preferred for research integrity and time efficiency.

#### B. 14 GB standard-runner disk

KuaiLive (~0.8 GB zip / ~2.6 GB extracted) is fine.

KuaiLive-M3 (~61.1 GB) is not.

If attempting live-only KuaiLive-M3 on GitHub:

- download only required files;
- convert CSV to compact parquet incrementally;
- delete raw CSV immediately after conversion;
- avoid downloading multimodal embeddings unless specifically needed;
- do not cache the raw dataset in Actions artifact storage.

#### C. Six-hour job cap

Most current experiments are below the cap. For any task at risk:

- shard seeds/configurations into separate matrix jobs;
- checkpoint every epoch;
- separate preprocessing, training, prediction export, and analysis;
- reuse small prepared artifacts rather than rerunning raw preprocessing;
- for GTS-Successive, shard users/time windows if evaluation becomes long.

For genuinely >6 h single-model training, move to self-hosted runner (self-hosted jobs can run much longer) or GPU infrastructure.

#### D. Artifact storage, not CPU minutes, may become the hidden limit

GitHub standard public runners are free, but artifact storage quotas still depend on account plan. GitHub documentation currently lists roughly:

- GitHub Free: 500 MB artifact storage
- GitHub Pro: 1 GB
- cache default: 10 GB per repository

This project has already produced some large temporary artifacts (e.g. ~140 MB candidate-seed prepared data and ~90 MB full ranking artifact). Future room-level prediction exports can quickly exhaust artifact storage.

Recommended artifact policy:

- large prepared datasets: retention 1–7 days
- full raw prediction matrices: retention 3–7 days, only when needed
- keep compressed per-user ranks/scores instead of candidate-level matrices
- permanent results: tiny CSV/JSON/Markdown committed to repo
- do not upload KuaiLive/KLM3 raw data due license and storage
- save reproducibility manifests/hashes permanently

### 8.4 Concurrency

GitHub currently documents standard-hosted concurrency limits of at least 20 jobs for Free accounts, 40 for Pro, 60 for Team, and higher for Enterprise.

The project currently needs at most ~4–8 parallel CPU training jobs for most grids, so concurrency is not a practical blocker.

### 8.5 Recommended compute allocation

**Keep on GitHub standard public runners:**

- KuaiLive preprocessing
- room-level SASRec/TiSASRec
- full-active evaluation
- GTS-Last / Successive
- candidate seeds
- DS-Frame CPU feasibility / final CPU runs if <6 h
- LiveRec Twitch 100k
- all gate/calibration/statistics

**Move off standard GitHub runners:**

- DCGLive final baseline
- KuaiLive-M3 full validation
- any multimodal KuaiLive-M3 experiment
- large LLM agent experiments

Best practical setup:

> keep GitHub Actions as the orchestration/reproducibility layer, attach a self-hosted GPU runner for GPU-heavy baselines and KuaiLive-M3, then upload only compact metrics/predictions back to the public workflow.

This preserves one reproducible experiment interface without forcing every workload onto a 4-core CPU VM.

---

## 9. Compute-aware schedule / decision gates

### Gate 1 — room-level survival

Run on standard GitHub Actions.

If Selective Memory fails to beat the strongest room-level baseline, stop and revisit the mechanism before GPU spending.

### Gate 2 — robust evaluation

If Gate 1 passes, complete:

- full active candidates
- GTS-Last
- GTS-Successive

Still standard GitHub Actions.

### Gate 3 — collision defense

Run DS-Frame CPU and LiveRec first on GitHub. Only after Selective Memory remains competitive should GPU resources be spent on DCGLive.

### Gate 4 — external confirmation

Use Twitch 100k first because it is feasible on GitHub and gives cross-platform evidence.

If Twitch confirms the effect, invest in KuaiLive-M3 using external/self-hosted GPU/storage.

This ordering prevents expensive GPU/data work before the central room-level claim is secure.

---

## 10. Reproducibility and statistical rules to freeze now

1. Dev chooses all thresholds/hyperparameters; test is one-shot.
2. Report all candidate seeds, not the best seed.
3. Paired user-level bootstrap for primary deltas.
4. >=5,000 bootstrap draws for final tables.
5. Holm correction across primary multiple baseline comparisons.
6. Store exact dataset hash / split timestamp / model commit / random seed.
7. Never change the external-validation architecture after observing external test results.
8. Distinguish exploratory KuaiLive findings from confirmatory external results.
9. Do not claim causal business impact.
10. Current memory expert is not an LLM agent.

---

## 11. Key current GitHub runs

- Official ReChorus grid success: `35319808840`
- Fair residual recovery: `35436149252`
- Selective Agent v2 frozen validation: `35447655392`
- Candidate-seed robustness: `35448130301`
- Global temporal robustness: `35448150972`

Current frozen result files already in repository:

- `SELECTIVE_AGENT_V2_RESULTS.md`
- `SELECTIVE_AGENT_V2_ROBUSTNESS_RESULTS.md`

---

## 12. External references that motivate the optimized plan

1. DS-Frame — *Recommender System as Slow and Fast Thinkers*, 2026: https://arxiv.org/abs/2609.02671
2. DCGLive — *Room Matters: Dynamic Room-level Collaboration Information Modeling for Live Streaming Recommendation*, WWW 2026: https://doi.org/10.1145/3774904.3792241
3. GUIDER — *Uncertainty Guided Dynamic Re-ranking for Large Language Models Based Recommender Systems*, AAAI 2026: https://ojs.aaai.org/index.php/AAAI/article/view/38639
4. LiveRec — *Recommendation on Live-Streaming Platforms: Dynamic Availability and Repeat Consumption*, RecSys 2021: https://github.com/JRappaz/liverec
5. KuaiLive: https://github.com/imgkkk574/KuaiLive
6. KuaiLive-M3 paper: https://arxiv.org/abs/2607.24862
7. KuaiLive-M3 benchmark: https://github.com/imgkkk574/KuaiLive-M3
8. GitHub-hosted runner specs: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
9. GitHub Actions billing/allowances: https://docs.github.com/en/billing/concepts/product-billing/github-actions
10. GitHub Actions limits: https://docs.github.com/en/enterprise-cloud@latest/actions/reference/limits

---

## 13. Short handoff summary for the next GPT/researcher

The project has already demonstrated that:

- always-on explicit memory/planning does not beat a tuned SASRec;
- a dev-learned Selective Memory gate does;
- the gain is robust to five candidate-sampling seeds;
- preliminary global temporal evaluation strengthens the gain;
- long history plus base-model ambiguity/confidence explains much of the memory-escalation value.

However, the main novelty risk is now high if framed as generic adaptive fast/slow recommendation because DS-Frame exists. The paper must instead test and defend the narrower claim that **explicit persistent memory is a specialist with predictable conditional relative utility beyond strong sequential modeling**.

The next mandatory experiment is **room-level KuaiLive**. If the effect survives there, proceed to full-active/GTS-Successive, DS-Frame/LiveRec/DCGLive collision-defense baselines, then freeze the design and validate externally on Twitch and KuaiLive-M3.

GitHub Actions is sufficient for most KuaiLive CPU work and Twitch 100k. It is not sufficient, as currently provisioned, for the original CUDA-heavy DCGLive code or the full 61 GB KuaiLive-M3 workload. Use GitHub Actions as the reproducibility/orchestration layer and add external/self-hosted GPU compute only after the room-level kill gate passes.
