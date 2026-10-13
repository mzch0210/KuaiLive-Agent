# B1: 从候选评价环境迁移到知识选择决策的 DEV-only 探索性实验

**研究身份**：原 G5 TEST 结果揭示后制定；仅用于 B1 DEV（不加入 G5 既有 Holm confirmatory family）。**研究问题**：对固定 Base、修正后 Memory 和同一批作者排序请求，sampled 候选评价的知识增量效用目标能否迁移到 full-active 候选下的选择决策？显式候选上下文是否能够改善这种迁移？

## B1-1：首先证明评分实现没有改动科学对象

1. 固定 G1 的 50,049 DEV 事件及 source/event order，采用被核验的 SASRec/GRU4Rec 主种子（20261012）和 **corrected all-prior Memory**。
2. 对事件时间点由活动区间重建 TRAIN-known author 的完整候选。使用 frozen Base 原始模型仅做 inference；候选分数对比原 corrected DEV parquet/CSV 的 Base/Memory rank 和 NDCG。
3. 使用已有 G2 的规则：目标作者进入 **离线 outcome evaluation**，574 个其他候选从 event-time active roster 以冻结随机种子采样。这个目标保留方法不能作为部署中的在线 candidate generator，也**不能**将目标身份、目标保留的采样分布或采样后 top-score 统计输入 gate。
4. 首先 128 个时间分散的 DEV 事件；只要有一个 full-active rank 不一致就 HOLD 并核查 TF32/点积归约/tie semantics。没有通过 parity 不进入完整 DEV。
5. 在冻结 RTX3090 上比较不同 GEMM batch 的**纯 CUDA 时间、吞吐、峰值显存**，同时分别记录 CPU 历史 replay/roster 构造时间。不要仅用 `nvidia-smi` 的瞬时利用率判断优化成败。
6. 实验输入和私有身份全部留在 self-host。仅公开总数、每方法总体指标、重复性判断和性能概要。

## B1-2：若 B1-1 PASS，构造全部 DEV paired regimes

- 一次性按 event time 扫描并缓存正确历史快照与可用作者集合，两个 Base family 复用；只进行 checkpoint 推理，不发生任何新的 Base 参数更新或对 TEST 读写。
- GPU 优先批量预计算 Base context vectors，把 item embeddings 缓存在 GPU，通过较大 batch GEMM 得到 event×author logits。不得为了指标改变计算精度/tie semantics；应与原 fixed source 完全一致。
- sampled-vs-full 的 per-event **效用标签**可以使用已揭示的 DEV target 用于监督；门控 Z 必须严格 pretarget：历史计数、full-active 候选的决策时可观测 roster、与 Base 的合法输出描述符。S 与 F 标签训练时共享 Z（纯标签分布迁移对照），不能加入依赖 target inclusion 的 sampled score statistics。
- 50049 事件的所有私有 event-level results 只存 self-host 指定新目录且以 SHA256 来源 manifest 锁定；重复执行拒绝覆盖。

## B1-3：嵌套用户组 DEV 决策试验（只在 B1-2 锁定时启动）

- **Pure S→F**：在 S 标签上训练/校准，不允许使用 F-DEV label 选择阈值；在同一 outer-user F heldout 上评价自然调用率与质量。
- **F→F**：用各 outer-train DEV 内 F utility label 训练/校准（reference），在完全相同 outer F heldout 上评价。
- **Candidate-aware→F**：只用 outer-train 合法候选组元数据以及允许的 F 标签/混合制度标签预先确定校准策略。必须清楚写出是否享受 F label access；不能冒充纯跨制度 zero-shot transfer。
- 包括 Always Base、Always Memory、简单 Difficulty/History 对照；共同比较 F outer events 下 NDCG@10、Memory calls、其联合质量/成本前沿、`V_F(pi_F)-V_F(pi_S)` 的 user-cluster confidence interval 和目标信号 MAE/calibration。
- 分离自然实现的调用率与事后等次数“Oracle style”离线分析。S→F 的无 F label 校准不能被事后 equal-call threshold 替代。所有 seed/特征/折划分/统计规则需在首次读取新 B1 全量 DEV policy result 前文件冻结。
- 成功必须体现 **真实 held-out full-active policy regret** 和有实质意义的 decision recovery；如果只是 sampled NDCG 与 full NDCG 差异，则不得宣布新知识系统机制。

## B1 门槛

**B1-1 FAIL → 停止，修复与原 DEV 评分一致性；B1-1 PASS → B1-2 全体重评分；B1-2 未精确复现原 DEV 的 full-active ranking → 停止；B1-3 没有 stable decision regret/recovery → 科学 NO-GO，保留原三风险 R3 OPEN。**

**优化原则**：减少小批次内核启动、消除逐事件 GPU 传输、增大可承受 batch，完成严格数值 parity 后再考虑 pinned memory / CUDA Graph（只适用于静态形状），对 CPU 预处理单独优化。GPU 利用率不是论文指标，也不能作为研究结果的替代。

**引用**：PyTorch CUDA semantics, https://docs.pytorch.org/docs/stable/notes/cuda ；NVIDIA CUDA Graph最佳实践, https://docs.nvidia.com/dl-cuda-graph/latest/cuda-graph-basics/cuda-graph.html 。

**源码与追踪**：
- `analysis/kbs_plan_c/b1_dev_regime_pilot.py`
- `.github/workflows/kbs-b1-dev-regime-gpu-pilot.yml`
- 原 B0 验收：`experiments/kbs_plan_c/B0_CANDIDATE_REGIME_DEV_FEASIBILITY_2026-10-13.md`
- 冻结 G5 在本方案及结果中均保持不变。
