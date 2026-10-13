# N9 | KBS 三项学术风险降低与 B1/B2 正式入稿执行计划

**2026-10-13；PLAN ONLY。** 本文件为下一阶段执行计划，不表示新实验、主稿修订或独立 TEST 已完成。

## 0. 冻结基线与三个风险

**原主稿**：main.tex Git blob 40be249de52c0ae423b793c0dd4c55f2fdd69f46，605 行、八章、11 个主图表；S1–S9 blob f5575d29ac3de222a04f78b48698cae119eac0bf，原 N8 投稿状态 HOLD。**此阶段不修改这两份稿件、G5 TEST 或 R0 主张。**

原 Twitch 冻结 TEST：Utility NDCG@10 0.58983，Base 0.58211，Always Memory 0.53980，Memory calls 15.04%。原 M3 六拟合冻结 TEST：Utility 优于四个特定对照目标，但 Always Memory 在主种子达到 0.34679，高于 Utility 0.30287；256 条 warmed DEV 事件 Memory 路径 0.803ms、Utility 1.802ms。原 KuaiLive 10,222 room 的 S/F 差异是 retrospective 诊断。

**B1/B2 尚未入论文**：两项结果是 G5 后设计、**同一**50,049 M3 author DEV/12,628 用户、SASRec 与 GRU4Rec 各一个主种子的探索性实验。B1 在 5×4 用户互斥折中 F→F 相对 S→F NDCG +0.006159（95% 用户 CI [0.004835,0.007543]）和 +0.004970（[0.003550,0.006369]）。B2 Full/Long-only 在完整 F 上 .343509/.333231、在 sampled S 上 .668498/.773602，顺序发生逆转；真实历史成分、决策特征、弱 placebo 的地板效应和 call-rate drift 都必须忠实呈现。

风险排序：**R1** 已有 Learning-to-Defer 与知识融合对方法原创性的挑战；**R2** 为什么在 M3 比 Always Memory 更值得选择；**R3** 条件价值、候选制度与选择决策组合的重要性。R3 经 B1/B2 实质缓解但未完全解决；R1/R2 仍重大。

**核心定位（暂定）**：对固定历史关系知识专家，排序增量效用取决于 incumbent 和实际候选制度；候选一致的监督与真实历史信息共同影响后续知识使用决策。不能宣称通用 deferral、sampled-metric 非保序的首创，也不能将 30% calls 解释成实测生产成本节约。

**执行策略**：研究线 A0→A1→A2→A3；论文线 P0→P1（与 A0–A2 并行）→P2→P3（A3 后定稿）；独立新数据及投稿责任线 T0/T1/T2。先制作 B1/B2 可追溯稿件内容，待关键验证决定方法或价值评价定位后，再统一修订主文标题、摘要、引言、讨论与结论。

## A. 研究验证线：直接降低 R1/R2

**A0 — 数据与强对照可行性闸门（第一步，无新训练）。** 核查 DEV 上逐事件 F/S Base/Memory 效用、用户组、决策前特征、冻结权重、inner OOF/outer heldout gate 分数与 hash。B1/B2 聚合数据**并未证明有逐候选 Base/Memory scores**；先查私有缓存，缺失时仅对所需 DEV 重评分，保持 original eligibility/tie/FP32 和 corrected all-prior Memory。一次时间有序历史/活动集扫描与大 batch GPU；分别量测 CPU/GPU/wall 耗时，不能以 GPU 使用率代替效率。交付 **N9_A0_SOURCE_AND_FUSION_FEASIBILITY.md**。A1 所需事件结果/user group 缺失则 HOLD；A2 缺融合分数则单独 HOLD。

**A1 — R2 无硬 30% 上限选择价值。** 同一 M3 DEV 50,049 事件、SASRec/GRU4Rec 冻结主种子、完整候选 F；采用 5 outer×4 inner user-disjoint 分组，只用 inner OOF 选择一个**预定的无上限**路由阈值，outer 只评价。对照 Always Base、Always Memory、原 30% Utility 与新规则；额外画用 inner 校准的 0/10/20/30/50/70/90/100% Memory 调用率—NDCG/HR 前沿，记录 outer 实际 calls/用户配对区间，**禁止从 outer 结果挑最好阈值当主结果**。Memory-first fallback 只有在选择前不需要先跑完整 Base 的特征下才能称实际提前路由；若有真实 mean/p95 latency 需同硬件、同 warmed regime。交付 **N9_A1_UNCONSTRAINED_POLICY_FRONTIER.md**。若仍不能超过 Always Memory 且无客观稀缺成本，R2 对“绝对质量/经济优势”判 NO-GO；对限定的价值测量问题仍可继续。

**A2 — R1 直接融合与 defer 对照。** 同一 F 作者候选中比较 Base、Memory、inner-DEV 调权的简单一参数 score fusion（含两个端点）及事先指定的 rank fusion 敏感性；两模型都被调用的执行开销须真实计入。比较已有 Direct relative-utility 和 Two-stage Specialist−Base 预测，同数据/用户折/模型容量/特征/DEV 调参机会/自然调用率；明确称其为 **L2D 风格可实现代理**，不得冒称复现所有 NeurIPS/ICML 理论方法。报告绝对 NDCG 与计算成本 Pareto、Always Memory、paired user CI。交付 **N9_A2_FUSION_DEFERRAL_BASELINES.md**。若简单融合在同成本上占优，不得继续宣传路由方法优势。

**A3 — 三风险与论文方向裁决。** 若无上限规则超 Always Memory 且公平融合/deferral 有独立收益，采用 **method-first**；若 Always Memory/融合更强但 B1/B2 的候选监督与知识来源机制稳定，采用 **valuation-first**（默认保守分支）；若强对照消除主张或来源难以合规复核，按 **scientific HOLD** 缩窄主张或审查期刊适配。交付 **N9_A3_THESIS_AND_RISK_VERDICT.md**，单独记录 R1/R2/R3 PASS/PARTIAL/HOLD，不得把任一新 DEV 分析加入原 G5 预注册统计家族。

