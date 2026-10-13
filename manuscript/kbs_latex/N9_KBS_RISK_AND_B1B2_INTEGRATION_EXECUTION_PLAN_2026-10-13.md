# N9 | KBS 三项学术风险降低与 B1/B2 正式入稿执行计划

**2026-10-13；PLAN ONLY。** 本文件为下一阶段执行计划，不表示新实验、主稿修订或独立 TEST 已完成。

## 0. 冻结基线与三个风险

**原主稿**：main.tex Git blob 40be249de52c0ae423b793c0dd4c55f2fdd69f46，605 行、八章、11 个主图表；S1–S9 blob f5575d29ac3de222a04f78b48698cae119eac0bf，原 N8 投稿状态 HOLD。**此阶段不修改这两份稿件、G5 TEST 或 R0 主张。**

原 Twitch 冻结 TEST：Utility NDCG@10 0.58983，Base 0.58211，Always Memory 0.53980，Memory calls 15.04%。原 M3 六拟合冻结 TEST：Utility 优于四个特定对照目标，但 Always Memory 在主种子达到 0.34679，高于 Utility 0.30287；256 条 warmed DEV 事件 Memory 路径 0.803ms、Utility 1.802ms。原 KuaiLive 10,222 room 的 S/F 差异是 retrospective 诊断。

**B1/B2 尚未入论文**：两项结果是 G5 后设计、**同一**50,049 M3 author DEV/12,628 用户、SASRec 与 GRU4Rec 各一个主种子的探索性实验。B1 在 5×4 用户互斥折中 F→F 相对 S→F NDCG +0.006159（95% 用户 CI [0.004835,0.007543]）和 +0.004970（[0.003550,0.006369]）。B2 Full/Long-only 在完整 F 上 .343509/.333231、在 sampled S 上 .668498/.773602，顺序发生逆转；真实历史成分、决策特征、弱 placebo 的地板效应和 call-rate drift 都必须忠实呈现。

风险排序：**R1** 已有 Learning-to-Defer 与知识融合对方法原创性的挑战；**R2** 为什么在 M3 比 Always Memory 更值得选择；**R3** 条件价值、候选制度与选择决策组合的重要性。R3 经 B1/B2 实质缓解但未完全解决；R1/R2 仍重大。

**核心定位（暂定）**：对固定历史关系知识专家，排序增量效用取决于 incumbent 和实际候选制度；候选一致的监督与真实历史信息共同影响后续知识使用决策。不能宣称通用 deferral、sampled-metric 非保序的首创，也不能将 30% calls 解释成实测生产成本节约。

**执行策略**：研究线 A0→A1→A2→A3；论文线 P0→P1（与 A0–A2 并行）→P2→P3（A3 后定稿）；独立新数据及投稿责任线 T0/T1/T2。先制作 B1/B2 可追溯稿件内容，待关键验证决定方法或价值评价定位后，再统一修订主文标题、摘要、引言、讨论与结论。

