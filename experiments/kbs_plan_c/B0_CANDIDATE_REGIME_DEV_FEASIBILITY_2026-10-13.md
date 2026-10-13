# B0 — M3 DEV 候选环境迁移实验的源码与私有缓存可行性闸门

**2026-10-13；B0 仅检查可行性，不训练、不运行 B1，不访问 G5 TEST 标签。**

## 问题及决策

下一阶段的真正科学问题并非仅复制已知 sampled NDCG 失真，而是能否在**同一 M3 DEV 事件、同一冻结 SASRec/GRU4Rec 与修正 Memory** 下构造 sampled/full-active 两种候选排序，研究训练候选环境失配对 **full-active 外层 held-out 选择策略** 的效用影响。

**静态代码闸门：CONDITIONAL PASS（需 self-host 实测来源验证）。**

## 源码检查结果

| B0 组件 | 源码事实 | 可行性判定 |
|---|---|---|
| 原始 DEV cohort | `klm3_plan_c_g1_v1/dev_cohort.parquet`（50,049 条）和 `causal_stream_sealed.parquet` | 如 self-host 仍在，可严格回放决策前历史 |
| 完整作者候选 roster | `available_room_intervals.parquet`、TRAIN-known `authors.npy`，`g3_dev_full_active.py:author_availability()` | 可以按事件时间重建 sorted 活跃 TRAIN-known 作者 |
| 候选数目 | M3 full-active 数千至数万作者，远多于 sampled checkpoint 575 | 必须对真实评分矩阵重算每个制度下事件 rank |
| 固定 Base | `klm3_g2_seed20261012_epoch3_v1/{sasrec,gru4rec}` + `klm3_g2_checkpoint_dev_selected_v1.json` | 若 SHA 和权重存在，可**仅重评分**，不重训 |
| Memory | 正式修复的 `g3_replay_correct_memory.py` 会把 TRAIN-unseen 的已知历史作者纳入 recency slots 和 all-author Long 归一化 | B1 必须沿用**修正后**规则，不能从 G3 暂存未修正 Memory 推断 sampled 得分 |
| 原 G3/G4 aggregate cache | `dev_full_active_pairs.csv` 每事件记录 NDCG、rank、候选数和 12 特征；源码中不存完整 candidate×score 列表 | **无法仅通过该 CSV 重建 sampled rank**；需要运行冻结模型 + 候选评分器。 |
| G2 checkpoint panel | 4,096 DEV × 575 候选 `checkpoint_candidate_tokens.npy` | 只能用于选择 checkpoint；**不能**冒充完整 50,049 事件的 sampled candidate 对照 |
| 信息边界 | G1 TRAIN/DEV 时间、目标保留的 sampled rank evaluation 与 pretarget gate features 必须分开 | `candidate_count` 等决策前元数据可用；正例 inclusion 不能作为在线特征 |
| 验证 | 5 outer user-disjoint × 4 inner OOF，所有策略在同一 full-active DEV outer events 上评价 | 仅 B1 使用。B0 不拟合选择器 |

**重要评分路径判断：** M3 冻结 Base 的 `score_batch` 使用候选的 encoder item embeddings 与预计算 context representation 的点积，原则上不存在原 KuaiLive 双 ID 的「基于候选集合重新标准化后融合」步骤。B1 仍须对每套真实候选计算相应的 Base 排序、Memory 排序和**决策前可见**的 score-distribution features；从 full-active `event-level aggregate` 直接拿值不成立。Sampled checkpoint 对目标正例的保留是**回顾性评价协议**，不能将真实目标作为在线输入。

## 真实 B0 执行与安全性

- 检查程序：[analysis/kbs_plan_c/b0_candidate_regime_dev_feasibility.py](../../analysis/kbs_plan_c/b0_candidate_regime_dev_feasibility.py)
- [GitHub Actions #38361051746](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38361051746)
- Hosted source syntax/explicit DEV-only checks: **PASS**.
- Self-host source SHA/检查点 SHA、50,049 DEV CSV 完整性、8 个 DEV 时刻作者 roster 重建：**该文件初建时为 RUNNING；最终状态需通过成功作业和上传的 aggregate json 确认**。
- 唯一上传的字段包括源完整布尔量、模型权重 digest 判定、DEV 样本/用户总数、候选数量范围和 roster 重建 PASS；不含 event_id、user_id、author_id、任意候选 score 向量、private 文件内容或 TEST 记录。

## B1 起跑前科学闸门

1. **真实 B0 必须 PASS**：全部 G1/INDEX/G2/G3 修正后 DEV 缓存与冻结 checkpoint SHA 一致，最小 8 个 DEV 时刻 live roster 全部可重建。
2. 用固定主种子先建立**最小端到端只读 DEV 重评分试点**，明确 GPU/缓存时间和存储开销；失败 STOP 不作六种子全量。
3. sampled regime 的构造必须不泄漏 outer held-out target 给 gate：目标保留式采样只能定义离线 outcome scoring；threshold/样本分组只能用训练 DEV。
4. 要区分 pure S→F（不许用 F 效用结果校准）与经过明确说明的 F-DEV adaptation；所有策略仍在**完全相同的 outer F** 数据上评价，在自然 calls 和公平预算曲线两方面都报告。
5. 只有 full-active heldout **policy** 出现稳定且实际重要的 regret / candidate-aware recovery，再考虑 B2 历史知识专属性实验或真正新的独立 TEST；仅看到 NDCG label 漂移属于已有采样评价常识，不算 R3 解决。

**范围声明：** 此阶段不修改 N8 已验收 31 页主稿、34 页合并补充材料、G5 registry/TEST，且未运行任何新拟合。

## B0 final independent source and self-host verification — PASS (2026-10-13)

The earlier statement **"self-host running/conditional PASS" is superseded** by this final evidence-based acceptance.

### Failure analysis and transport repair

- [Original B0 run #38361051746](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38361051746) failed exclusively in self-host `actions/checkout@v4`: `git fetch` to `github.com:443` encountered `curl 28` TCP connect timeouts on **all three attempts** and exited 128. Hosted source syntax audit passed. **All actual DEV validation steps had been skipped** on that first run.
- Replaced self-host git checkout with a tightly scoped GitHub-hosted **artifact relay**: hosted job packages `b0_candidate_regime_dev_feasibility.py`, `g3_dev_full_active.py`, `g2_train_base.py` and SHA256SUMS; self-host downloads and verifies that exact artifact with no `github.com` Git fetch. No private data are present in the code bundle.
- [Recovery run #38362497343](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38362497343), source commit `9e2ee9fc1cbb09c9719ea1cc007c3487a5c3a8e6`: **hosted-source-safety SUCCESS; private-dev-cache-gate SUCCESS; overall SUCCESS**. Both user-host source checking and eight DEV roster probes completed; zero job-log errors.

### Read-back from the real, uploaded aggregate artifact

Artifact: `kbs-b0-m3-candidate-regime-dev-aggregate`, GitHub Actions ID `11794918018`, 30-day retention. Inner `summary.json` SHA256: `684cb34af90f5a29b27da7b65d68bcd423198101da1f7572dea8cd24b23d5459`. The result was **independently downloaded and parsed**, not inferred from job success alone.

| Check | Observed result | Verdict |
|---|---|---|
| Frozen G1 derived source / TRAIN index / G2 DEV screen / corrected G3 DEV pairs | All 14 named mandatory private source files found | PASS |
| Corrected paired DEV source manifest and CSV | `kbs-plan-c-full-active-dev-paired-v2`, complete DEV-only, SHA verified | PASS |
| DEV identity and scope | **50,049 events; 12,628 distinct users**; DEV rows only | PASS |
| All-event full-active candidate count | min **14,022**, max **53,762** | PASS |
| Frozen SASRec model | primary seed 20261012 checkpoint present; expected SHA verified | PASS |
| Frozen GRU4Rec model | primary seed 20261012 checkpoint present; expected SHA verified | PASS |
| 8 reconstructed time-based DEV rosters | min **22,934**, max **53,379** candidates, all target-positive authors present | PASS |
| Source event identities or candidate IDs uploaded | None uploaded; aggregate-only artifact | PASS |
| New model training / G5 TEST accessed | **False / False** | PASS |
| Per-candidate Base/Memory score vectors already saved | **False** | B1 must recompute exact rankings from frozen models and corrected history |

### Acceptance and handoff

**B0 = PASS: `PASS_RECONSTRUCTIBLE_REQUIRES_FROZEN_BASE_RESCORING`.** This certifies source availability, corrected DEV identity, frozen model artifacts and minimal roster reproducibility; it does **not** certify a full 50,049-event sampled/full-active re-scoring experiment, candidate-regime transfer result or statistically significant policy benefit. The M3 Base scores are item-embedding dot products and can be regenerated on frozen model weights without training new Base models; corrected Memory must be reconstructed from all pretarget historical interactions, including TRAIN-unseen historical authors.

**B1 first stage:** design a low-cost read-only DEV subset scored in both candidate regimes, validate exact full-active ranks against the already frozen corrected DEV paired source, then build nested user-disjoint policy comparisons. Sampled target-retention remains an offline evaluation protocol, never a decision-time feature. The full prior G5 TEST must remain unopened.

**N8 manuscript and supplementary scientific evidence remain frozen and unchanged.**
