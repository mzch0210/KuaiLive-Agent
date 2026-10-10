# 第一阶段｜前七章逐段学术论证审计矩阵

**状态：实际源码逐段检查已完成；这是第二阶段修改依据，不是主稿改写。**

- **主稿 GitHub 基线：** `main` commit `f7cd9e7f48827eaded4109684bda70ee0e84d9ee`；[main.tex](main.tex) blob `5222d53e071987d651e3d5cb2f1a7a51c8323954`。
- **权威大纲：** [投稿导向大纲](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md) blob `89734dbec9f852fcb728b2ef3a767d19ebe22109`。
- **证据材料：** [S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md) blob `067d4e5713eb927d8aab3dee3bf2dde512b314ed`。
- **审查准绳：** [修订计划](KBS_OUTLINE_ALIGNED_ARGUMENT_REVISION_PLAN_2026-10-10.md)；KBS 官方 [Aims & Scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)，Elsevier 官方 [Guide for Authors](https://www.elsevier.com/subject/next/guide-for-authors)。
- **正文范围：** §§1–7；§8 Conclusion 与 Abstract 尚未存在，不得标记为已验收。

## 1. 科学定盘星与信息结构

> **The central problem is whether a fixed specialist instantiated from historical relationship evidence improves ranking relative to the trained base on a given event and candidate regime.** （原大纲 §1.1）

**研究证据链**：Twitch: C1（条件性相对价值）→ C3（DEV 冻结的相对效用选择获得独立 TEST 改善）；KuaiLive: C2（已检查 TEST 事件中的候选环境依赖）；§7 将两链综合为知识决策解释，**不宣称跨平台转移门控已被验证**。

**大纲固定结果顺序**：§6.1 条件价值 → §6.2 选择决策 → §6.3 候选环境边界；保持不变。整体不因 C1/C2/C3 标签顺序而交换实验章节。

## 2. 审核口径、统计及非段落内容

- 逐段对象：LaTeX 正文独立段落（按空行、章节、环境及 `\\paragraph{}` 分界）；**共 95 个文本段落**，包括简短的章节导语。每个段落在本表中有唯一稳定编号 `Sx-Pyy`、源代码行号、贡献角色、优先级及操作。行号仅对此次冻结 blob 有效，后续改写必须用 ID + 原文锚点定位。
- **P1：** 科学论证推进弱、章节职责重复、读者可能误解创新或证据；**P2：** 信息位置/论述密度/学术语体的具体优化；**KEEP：** 必须保留的定义、指标、对照公平性及可追溯论证。
- **P1 22 段；P2 33 段；KEEP 40 段。** P1/P2 是**编辑工作量与审稿风险排序**，并非证明该段科学上有错或需要追加实验。
- **不计入 95 个文本段落的必要内容：** Introduction 的 C1–C3 三项 `\\item`（必须整体保留并与大纲核对）、§3 的数学环境、§4 的机制图、§5–6 的数据表/结果图及全部表题、脚注和 S1–S9。**独立图表/公式检查必须在 Gate 3/4 进行，不允许被“未计入段落”误解为可删。**
- **摘要和结论缺口：** 属修订后的后续撰写阶段，不能作为本轮 §1–7 的 P0 数据错误。

## 3. 逐段论证—证据—编辑行动矩阵

| 段 ID | LaTeX 行 | 当前位置 | 大纲贡献 | 级别 | 操作 | 具体编辑依据/指令 | 主要证据与来源 |
|---|---:|---|---|---|---|---|---|
| S1-P01 | 33–33 | Introduction | C1+C2+C3 | P1 | 重写论证或段落角色 | 重建强 Base 已具表示能力与额外关系证据是否增益的研究张力；减少教材式背景。 | 大纲 §1.1–1.3；§6.1/6.2 Twitch、§6.3 KuaiLive；C1–C3 |
| S1-P02 | 35–35 | Introduction | C1+C2+C3 | P1 | 重写论证或段落角色 | 以大纲的 evidence fusion→operational valuation 缺口推进，避免重复 §2 文献分类。 | 大纲 §1.1–1.3；§6.1/6.2 Twitch、§6.3 KuaiLive；C1–C3 |
| S1-P03 | 37–37 | Introduction | C1+C2+C3 | P1 | 保留事实并紧缩/重排 | 让直播场景服务于可检验的历史状态/候选环境问题，清楚区分 Twitch streamer 与 KuaiLive room。 | 大纲 §1.1–1.3；§6.1/6.2 Twitch、§6.3 KuaiLive；C1–C3 |
| S1-P04 | 39–39 | Introduction | C1+C2+C3 | P1 | 重写论证或段落角色 | 按大纲的两种互补发现说明 Twitch 冻结决策、KuaiLive 候选环境；减少流程先后描述。 | 大纲 §1.1–1.3；§6.1/6.2 Twitch、§6.3 KuaiLive；C1–C3 |
| S1-P05 | 41–41 | Introduction | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §1.1–1.3；§6.1/6.2 Twitch、§6.3 KuaiLive；C1–C3 |
| S1-P06 | 47–47 | Introduction | C1+C2+C3 | P2 | 移细节到 §5/S1–S9 或合并 | 现有通用性/离线边界属有效范围说明；移至与任务设置相邻处或压缩末句。 | 大纲 §1.1–1.3；§6.1/6.2 Twitch、§6.3 KuaiLive；C1–C3 |
| S2-P01 | 53–53 | Sequential and Long-Horizon Recommendation | C1+C2+C3 | P2 | 保留事实并紧缩/重排 | 文献对照要围绕长序列表示≠已有 Base 上的增量知识价值，减少重复自我对照。 | 正式出版最近邻：§2 引用；大纲 §2.1–2.5；贡献差异 C1/C2/C3 |
| S2-P02 | 57–57 | Auxiliary Evidence Integration and Reliability | C1 | P2 | 保留事实并紧缩/重排 | 整理融合、知识路径、MemRec 的真实能力与本文具体 estimand 的关系，避免罗列。 | 正式出版最近邻：§2 引用；大纲 §2.1–2.5；贡献差异 C1/C2/C3 |
| S2-P03 | 59–59 | Auxiliary Evidence Integration and Reliability | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 正式出版最近邻：§2 引用；大纲 §2.1–2.5；贡献差异 C1/C2/C3 |
| S2-P04 | 61–61 | Auxiliary Evidence Integration and Reliability | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 正式出版最近邻：§2 引用；大纲 §2.1–2.5；贡献差异 C1/C2/C3 |
| S2-P05 | 65–65 | Expert Routing and Learning-to-Defer | C3 | P2 | 保留事实并紧缩/重排 | 强调已有 L2D/post-hoc 专家分配的实质贡献，本文仅将固定关系知识置于事件排序差值框架。 | 正式出版最近邻：§2 引用；大纲 §2.1–2.5；贡献差异 C1/C2/C3 |
| S2-P06 | 67–67 | Expert Routing and Learning-to-Defer | C3 | P1 | 重写论证或段落角色 | 与 §2.5 的 gap 结尾重复；压缩或并入已有 deferral 段。 | 正式出版最近邻：§2 引用；大纲 §2.1–2.5；贡献差异 C1/C2/C3 |
| S2-P07 | 71–71 | Live-Streaming and Repeat-Aware Recommendation | C1+C2 | P2 | 保留事实并紧缩/重排 | 明确 LiveRec、KuaiLive、DCGLive 的任务差异，再引出场景价值，不作未经协议匹配的数值比较。 | 正式出版最近邻：§2 引用；大纲 §2.1–2.5；贡献差异 C1/C2/C3 |
| S2-P08 | 75–75 | Research Gap | C1+C2+C3 | P1 | 重写论证或段落角色 | 将 Research Gap 写成一段可证伪的知识决策研究缺口，与 §1 大纲中心命题同义。 | 正式出版最近邻：§2 引用；大纲 §2.1–2.5；贡献差异 C1/C2/C3 |
| S3-P01 | 80–80 | Problem Formulation | C1 | P2 | 保留事实并紧缩/重排 | 以数学对象顺序做一行入口；不要以正文写作步骤作为引言。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P02 | 85–85 | Recommendation Setting and Event-Level Ranking Utility | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P03 | 87–87 | Recommendation Setting and Event-Level Ranking Utility | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P04 | 96–96 | Recommendation Setting and Event-Level Ranking Utility | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P05 | 101–101 | Base-Relative Specialist Utility | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P06 | 106–106 | Base-Relative Specialist Utility | C1 | P2 | 保留事实并紧缩/重排 | 式后解释只保留 operational 比较的含义，避免与 §1、§7.1 重复。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P07 | 108–108 | Base-Relative Specialist Utility | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P08 | 113–113 | Conditional Relative Utility | C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P09 | 119–119 | Conditional Relative Utility | C3 | P2 | 保留事实并紧缩/重排 | 去掉不必要的'见第4节实现'流程导读；保留 η_r 的目标语义。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P10 | 121–121 | Conditional Relative Utility | C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P11 | 128–128 | Conditional Relative Utility | C3 | P2 | 保留事实并紧缩/重排 | 期望收益恒等式解释一次即可；7.3 专注其决策含义。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P12 | 130–130 | Conditional Relative Utility | C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P13 | 135–135 | Selective Invocation and Equal-Count Comparison | C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P14 | 140–140 | Selective Invocation and Equal-Count Comparison | C3 | P2 | 保留事实并紧缩/重排 | 计数非固定预算这一关键信息保留；避免在 §7 再三复述。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P15 | 142–142 | Selective Invocation and Equal-Count Comparison | C3 | P2 | 移细节到 §5/S1–S9 或合并 | matched-m 的定义与比较器具体 TEST 访问规则聚合进 §5.3。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P16 | 147–147 | Regime-Level Utility Decomposition | C2 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S3-P17 | 154–154 | Regime-Level Utility Decomposition | C2 | P2 | 保留事实并紧缩/重排 | 目标状态分解为描述性，保留但避免与 §7 限定重复。 | 大纲 §3；§3 数学式 (u_K, Δ_M, η_r, a, decomposition) |
| S4-P01 | 160–160 | Base-Relative Evidence Valuation Framework | C1 | P2 | 保留事实并紧缩/重排 | 图的机制与科学问题对齐：Base→价值预测→有条件使用，而非绘图操作说明。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P02 | 191–191 | Strong Sequential Base Recommenders | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P03 | 193–193 | Strong Sequential Base Recommenders | C1 | P2 | 保留事实并紧缩/重排 | Base 两个平台任务不同，联系知识价值比较；详细任务定义交 §5。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P04 | 198–198 | Transparent Relationship-Memory Specialist | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P05 | 200–200 | Transparent Relationship-Memory Specialist | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P06 | 209–209 | Transparent Relationship-Memory Specialist | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P07 | 214–214 | Base-Relative Relationship-Evidence States | C1+C2 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P08 | 225–225 | Base-Relative Relationship-Evidence States | C1+C2 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P09 | 230–230 | Observable Features and Conditional Relative-Utility Estimation | C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P10 | 232–232 | Observable Features and Conditional Relative-Utility Estimation | C3 | P2 | 移细节到 §5/S1–S9 或合并 | 保留准确的 0.4/0.4/0.2 特征构造；判断是否可紧凑转至实验参数/S2。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P11 | 237–237 | Specialist Selection and Matched-Budget Controls | C3 | P2 | 保留事实并紧缩/重排 | 明确推理时所能观测信息及决策依据；§3 数学定义不再重复。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S4-P12 | 239–239 | Specialist Selection and Matched-Budget Controls | C3 | P2 | 保留事实并紧缩/重排 | Difficulty 的目标差异在方法中一句交代，详细公平性协议仅写 §5。 | 大纲 §4；§4 Base/Memory/diagnostic states/14-feature predictor；S2/S3 |
| S5-P01 | 245–245 | Experimental Setup | C1+C2+C3 | P2 | 保留事实并紧缩/重排 | 突出两套实验分别测试哪项大纲命题，保持任务定义与科学证据对齐。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P02 | 251–251 | Datasets and Prediction Tasks / KuaiLive. | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P03 | 253–253 | Datasets and Prediction Tasks / KuaiLive. | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P04 | 256–256 | Datasets and Prediction Tasks / Twitch/LiveRec. | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P05 | 277–277 | Baselines and Compared Methods | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P06 | 279–279 | Baselines and Compared Methods | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P07 | 304–304 | Experimental Protocols / Training and model selection. | C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P08 | 307–307 | Experimental Protocols / Candidate-regime comparisons. | C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P09 | 315–315 | Experimental Protocols / Candidate-regime comparisons. | C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P10 | 321–321 | Experimental Protocols / Candidate-regime comparisons. | C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P11 | 326–326 | Evaluation Metrics and Statistical Analysis | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P12 | 328–328 | Evaluation Metrics and Statistical Analysis | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S5-P13 | 333–333 | Implementation Details | C1+C2+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | 大纲 §5；S1/S2/S3；Twitch frozen TEST、KuaiLive matched candidate、Difficulty matched m |
| S6-P01 | 338–338 | Experimental Results | C3(计算) | P1 | 重写论证或段落角色 | 按大纲规定 6.1→6.2→6.3 组织主线；避免实验日志式'我们先做了什么'。 | 大纲 §6；S2/S4/S5/S6/S7/S8/S9；§6 冻结/事后分级证据 |
| S6-P02 | 343–343 | Heterogeneous Utility of Relationship Memory | C1 | P2 | 保留事实并紧缩/重排 | 保留总体负收益与 recoverable 正收益的强对比；开头从结果命题出发。 | §6.1 Twitch frozen TEST；S2/S4 |
| S6-P03 | 345–345 | Heterogeneous Utility of Relationship Memory | C1 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | §6.1 Twitch frozen TEST；S2/S4 |
| S6-P04 | 347–347 | Heterogeneous Utility of Relationship Memory | C1 | P2 | 保留事实并紧缩/重排 | 目标状态不能服务时使用；只保留一处显著区分并推进到 6.2。 | §6.1 Twitch frozen TEST；S2/S4 |
| S6-P05 | 402–402 | Decision Value of Predicting Relative Utility | C3 | P2 | 保留事实并紧缩/重排 | 结果开头应提出可检验的 pre-outcome relative-utility 选择问题，训练细节归 §5。 | §6.2 Twitch DEV freeze/TEST；S2/S7 |
| S6-P06 | 404–404 | Decision Value of Predicting Relative Utility | C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | §6.2 Twitch DEV freeze/TEST；S2/S7 |
| S6-P07 | 406–406 | Decision Value of Predicting Relative Utility | C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | §6.2 Twitch DEV freeze/TEST；S2/S7 |
| S6-P08 | 408–408 | Decision Value of Predicting Relative Utility | C3 | P2 | 保留事实并紧缩/重排 | 选中/未选中条件均值为描述性，不要写成独立额外验证。 | §6.2 Twitch DEV freeze/TEST；S2/S7 |
| S6-P09 | 410–410 | Decision Value of Predicting Relative Utility | C3 | P2 | 移细节到 §5/S1–S9 或合并 | DEV 事后状态富集数据对机制是辅助说明，优先移到 S7/§6.4。 | §6.2 Twitch DEV freeze/TEST；S2/S7 |
| S6-P10 | 412–412 | Decision Value of Predicting Relative Utility | C3 | P2 | 保留事实并紧缩/重排 | Oracle 上界可保留，但不要在 §7 再次详细报告 gap 算术。 | §6.2 Twitch DEV freeze/TEST；S2/S7 |
| S6-P11 | 436–436 | Candidate-Regime Dependence of Relative Utility | C2 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | §6.3 KuaiLive paired previously inspected TEST；S5/S8 |
| S6-P12 | 438–438 | Candidate-Regime Dependence of Relative Utility | C2 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | §6.3 KuaiLive paired previously inspected TEST；S5/S8 |
| S6-P13 | 456–456 | Candidate-Regime Dependence of Relative Utility | C2 | P2 | 保留事实并紧缩/重排 | sampled metrics 文献定位以一句完成；效用变换的知识含义留 §7。 | §6.3 KuaiLive paired previously inspected TEST；S5/S8 |
| S6-P14 | 458–458 | Candidate-Regime Dependence of Relative Utility | C2 | P2 | 移细节到 §5/S1–S9 或合并 | 训练随机种子详细值与 SD 主文从简、表归 S8，绝不推断独立数据试验。 | §6.3 KuaiLive paired previously inspected TEST；S5/S8 |
| S6-P15 | 460–460 | Candidate-Regime Dependence of Relative Utility | C2 | P2 | 移细节到 §5/S1–S9 或合并 | 9 个列表为固定 checkpoint 追加抽样；主文仅报告方向稳定，表留 S5。 | §6.3 KuaiLive paired previously inspected TEST；S5/S8 |
| S6-P16 | 462–462 | Candidate-Regime Dependence of Relative Utility | C2 | P2 | 保留事实并紧缩/重排 | 状态构成不变解释替代假设，保留关键发现并减弱过宽的'排除一切'字样。 | §6.3 KuaiLive paired previously inspected TEST；S5/S8 |
| S6-P17 | 467–467 | Robustness and Alternative Explanations | C1+C3 | P1 | 重写论证或段落角色 | 将 §6.4 从 DEV 诊断项目列表重排为'选择特征证据—知识/基座互补—辅助边界'。 | §6.4 Twitch DEV-only；S3/S4/S6/S7 |
| S6-P18 | 469–469 | Robustness and Alternative Explanations | C1+C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | §6.4 Twitch DEV-only；S3/S4/S6/S7 |
| S6-P19 | 488–488 | Robustness and Alternative Explanations | C1+C3 | P2 | 移细节到 §5/S1–S9 或合并 | 局部七组参数枚举只保留影响 C1 的总结，详值留 S4。 | §6.4 Twitch DEV-only；S3/S4/S6/S7 |
| S6-P20 | 490–490 | Robustness and Alternative Explanations | C1+C3 | P1 | 保留事实并紧缩/重排 | Long-only 现象保留，避免'为何决定仍选 Full'的防御性过程回顾。 | §6.4 Twitch DEV-only；S3/S4/S6/S7 |
| S6-P21 | 492–492 | Robustness and Alternative Explanations | C1+C3 | P2 | 保留事实并紧缩/重排 | 不同历史长度分别训练，不宣称单因果因素；将数值集中在核心结果。 | §6.4 Twitch DEV-only；S3/S4/S6/S7 |
| S6-P22 | 494–494 | Robustness and Alternative Explanations | C1+C3 | P2 | 移细节到 §5/S1–S9 或合并 | target recurrence 事后分组只呈现有限关联；详值归 S6。 | §6.4 Twitch DEV-only；S3/S4/S6/S7 |
| S6-P23 | 496–496 | Robustness and Alternative Explanations | C1+C3 | P1 | 重写论证或段落角色 | 用正面解释性结论总结 §6.4，避免一句后追加无关 checkpoint 说明。 | §6.4 Twitch DEV-only；S3/S4/S6/S7 |
| S6-P24 | 501–501 | Computational Considerations | C3(计算) | P2 | 保留事实并紧缩/重排 | 先指出成本与收益双目标，再给 Twitch 调用率；不要暗示推理提速。 | §6.5 separate KuaiLive warmed CPU；S9 |
| S6-P25 | 503–503 | Computational Considerations | C3(计算) | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | §6.5 separate KuaiLive warmed CPU；S9 |
| S6-P26 | 505–505 | Computational Considerations | C3(计算) | P2 | 移细节到 §5/S1–S9 或合并 | 计算阶数若不能直接支撑讨论，可移 S9；主文保留成本来源。 | §6.5 separate KuaiLive warmed CPU；S9 |
| S7-P01 | 513–513 | Operational Value Is Base- and Context-Dependent | C1 | P1 | 重写论证或段落角色 | 不再重复 Δ_M 公式与 §6.1 数值；解释强 Base 下的可观测互补性。 | §3/§6.1/§6.4；S4/S6 |
| S7-P02 | 515–515 | Operational Value Is Base- and Context-Dependent | C1 | P1 | 保留事实并紧缩/重排 | Long-only 与 Base 长度敏感性留作一项简练解释，避免第二份结果列表。 | §3/§6.1/§6.4；S4/S6 |
| S7-P03 | 520–520 | Interpreting Conditional Evidence and Candidate Regimes | C2 | P1 | 重写论证或段落角色 | 先陈述候选环境为何改变知识价值的含义，减少原数值重复。 | §5/§6.3；S5/S8；CACM 2022 sampled metrics |
| S7-P04 | 522–522 | Interpreting Conditional Evidence and Candidate Regimes | C2 | P1 | 重写论证或段落角色 | 细致 2×2 分配已在 §6.3，Discussion 应解释候选竞争条件的系统意义。 | §5/§6.3；S5/S8；CACM 2022 sampled metrics |
| S7-P05 | 524–524 | Interpreting Conditional Evidence and Candidate Regimes | C2 | P1 | 移细节到 §5/S1–S9 或合并 | 3 training pairs 与固定 pair 的 9 draws 样本层次保留 §6/S5/S8，7.2 保留方向性一句。 | §5/§6.3；S5/S8；CACM 2022 sampled metrics |
| S7-P06 | 529–529 | From Relative Utility to Selective Decisions | C3 | KEEP | 保持并核查术语/引用 | 现有段落履行必要定义、方法或证据职责；后续只检查跨节连贯性及用词一致。 | §3/§6.2/§6.4；S2/S7；ICML/NeurIPS deferral |
| S7-P07 | 531–531 | From Relative Utility to Selective Decisions | C3 | P1 | 保留事实并紧缩/重排 | 不再罗列所有 TEST 数值；将相对收益优于 Base Difficulty 的认知作为解释。 | §3/§6.2/§6.4；S2/S7；ICML/NeurIPS deferral |
| S7-P08 | 533–533 | From Relative Utility to Selective Decisions | C3 | P1 | 保留事实并紧缩/重排 | 与通用 L2D、GUIDER 精确对话但避免防御式强调本文不做什么。 | §3/§6.2/§6.4；S2/S7；ICML/NeurIPS deferral |
| S7-P09 | 538–538 | Validity Boundaries | C1+C2+C3 | P1 | 移细节到 §5/S1–S9 或合并 | Twitch 一次冻结与 KuaiLive post-hoc 必须保留；Bootstrap、seeds/draws 细节回 §5/S8。 | §5–§6；S1/S5/S8/S9 |
| S7-P10 | 540–540 | Validity Boundaries | C1+C2+C3 | P1 | 移细节到 §5/S1–S9 或合并 | 目标状态非 serving 特征及 one-positive protocol 保留为有效界限；时间细节已在 §5/S1。 | §5–§6；S1/S5/S8/S9 |
| S7-P11 | 542–542 | Validity Boundaries | C1+C2+C3 | P1 | 移细节到 §5/S1–S9 或合并 | 实际 KuaiLive CPU 正开销不能删；gate/masks/cache 细节集中 §6.5/S9。 | §5–§6；S1/S5/S8/S9 |
| S7-P12 | 547–547 | Implications for Knowledge-Based Recommendation | C1+C2+C3 | P1 | 保留事实并紧缩/重排 | 升华同一知识决策原则：价值相对 Base 与候选集合且可用 pre-outcome 估计指导。 | C1–C3 解释性综合；§7.1–§7.4 |
| S7-P13 | 549–549 | Implications for Knowledge-Based Recommendation | C1+C2+C3 | P1 | 保留事实并紧缩/重排 | 减少 future work 清单，使通用设计原则更明确；成本条件与验证路径各一句。 | C1–C3 解释性综合；§7.1–§7.4 |

## 4. 贡献列表、图表与数学结构专项核对

| 非正文段落对象 | 科学职责 | 第一阶段判断 |
|---|---|---|
| Introduction C1–C3 三个 `\\item`（源码约 L43–45） | 价值定义、候选情境证据、pre-outcome 选择；是大纲冻结贡献 | **保留三项，不改称新数学定理、通用 L2D 或跨平台 gate**；第二阶段仅做写作衔接 |
| §3 event NDCG / `\\Delta_M` / `\\eta_r` / `\\mathbb E[a\\eta]` / regime decomposition | 科学对象、价值—选择的期望恒等式、解释性状态分解 | **完全冻结数学含义和先后定义**；减少别章重复公式即可 |
| §4 Figure 1 | Base、Memory、可观测特征与 offline target-state 的严格隔离 | 机制图逻辑保留；语言重写时图注/路径要一致 |
| §5 dataset/method 表和协议 | 构建候选及比较器信息访问、同队列配对、统计口径 | 复现关键信息必须继续在主文可见，细节 S1–S9 承担 |
| §6 现有状态图、冻结政策表、KuaiLive 四格分解表、DEV 消融表 | 各自支持 C1、C3、C2 与 DEV 辅助解释，职责不同 | **默认全部保留**；仅在主文文字重写后检查是否有重复图/表数据叙述 |

## 5. 第二阶段交接协议

按 [P1/P2 修改队列](STAGE1_P1_P2_EDIT_QUEUE_2026-10-10.md)执行。修改后逐条回查本矩阵行号和原文，记录：`段落ID → 保留/改写/合并/转移 → 新章节位置 → 关键事实校验 → reviewer sign-off`。绝不能把负结果的真实性或防止 target leakage 的科学限定当作“负面表达”删去。以 [冻结主张与证据基线](STAGE1_FROZEN_CLAIMS_AND_BASELINE_2026-10-10.md)核对不变项。
