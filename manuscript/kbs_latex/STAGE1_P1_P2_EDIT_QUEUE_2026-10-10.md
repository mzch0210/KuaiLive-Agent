# 第一阶段｜P1/P2 分级执行队列与审稿验收门槛

**状态：审查整改队列已建立；主稿尚未开始第二阶段重写。**

**基础文件：** [逐段审计矩阵（95 段）](STAGE1_PARAGRAPH_ARGUMENT_MATRIX_2026-10-10.md)、[冻结主张与源码基线](STAGE1_FROZEN_CLAIMS_AND_BASELINE_2026-10-10.md)、[权威论文大纲](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md)、[完整修订计划](KBS_OUTLINE_ALIGNED_ARGUMENT_REVISION_PLAN_2026-10-10.md)。

## 一、编辑诊断：大纲没有失效，主要失效点是正文组织

已对 §§1–7 **95 个 prose units** 进行逐段分类：**22 个 P1、33 个 P2、40 个 KEEP**。说明：
- P1 = 与主张推进、段落职责、最接近研究的贡献定位或证据层次相关的**优先编辑问题**；不是 22 个科学方法错误。
- P2 = 信息密度、复现细节位置、重复限定或语体调整；不等于应全部删减的 33 个段落。
- KEEP = 数学定义、关键协议、实验结果和可复现论证原则上保留，只做衔接和一致性检查。
- 严格区分「**负面事实**」（整体 Memory 低于 Base、不同状态收益有负有正、CPU overhead 正值）和「**消极文风**」（反复自我否定、解释实验过程和没有完成的工作）。前者不可删除。

**核心得失排序：** §1 的 *scientific tension* 尚不够聚焦，§6.4 的 DEV-only 诊断密度超过论证所需，§7 的价值解释与 Results、Methods 重合太多；§2–§5 基本建立了正确科学对象，主要进行术语和信息归位。

## 二、P1 执行队列：先解决哪些论证问题

| 任务 ID | 优先级 | 修改单元 | 精确编辑工作 | 必须保留的依据 | 第二阶段验收 |
|---|---|---|---|---|---|
| **A01** | P1 | §1 S1-P01–P04 | 按大纲 §1.1–1.2 建立“已有 Base 表示力 → 历史关系知识可能冗余/互补 → 决策级增量价值问题 → Twitch 条件性选择与 KuaiLive 情境依赖”的科学张力。减少论文执行步骤式的引入。 | 不新造 explicit RQ 列表；两平台证据类型不同 | 只读 §1 首尾即能说出研究问题及两条互补证据 |
| **A02** | P1 | §2 S2-P06、S2-P08 | 将最近邻的 generic L2D、uncertainty routing、sampled metrics 与本文的知识价值/决策评估问题正确区分；形成一个 Research Gap 结论，不重复“别人做 X、本文不做 X”。 | Mozannar/Narasimhan、GUIDER、Krichene 的正式出版记录 | 创新点定位与 Intro C1–C3 语义一致，不将 \`Δ_M\` 当新定理 |
| **A03** | P1 | §6 S6-P01（开场） | 恢复大纲原定结果叙事：条件价值（6.1）→ 相对价值选择（6.2）→ 候选环境边界（6.3），§6.4/6.5 是辅助诊断/成本。 | §6.1/6.2 的 Twitch frozen、§6.3 KuaiLive post-hoc | 不交换 §6.2 与 §6.3；Results 每小节增加可检验的科学任务句 |
| **A04** | P1 | §6.4 S6-P17 | 将“DEV 诊断实验罗列”改为支持何种解释的三类证据：可观测预测特征；关系知识与 Base 表示力的互补；目标定义/候选评价的有限边界。 | 现有五折 DEV OOF、S4/S6/S7，不能当成新 TEST | §6.4 首尾围绕可检验的主张，不按实验跑批顺序列章节 |
| **A05** | P1 | §6.4 S6-P20、S6-P23 | 删除/改写“保留 Full Expert 因为没有选择其他模型”这类模型决策追溯；强调 Long-only 相对 Full 的分组效用特征。移除末句中无关 checkpoint 旁注。 | Long-only recoverable +0.10592、unavailable 的不利面；Full 已固定 | 主文保留正反结果且没有暗示利用 TEST 自选专家 |
| **A06** | P1 | §7.1 S7-P01–P02 | 减少 \`Δ_M\` 公式、状态表和 Long-only 数值重复；解释在已有 Base 表示下知识为什么形成**可观测的排序互补性**，而非直接声称已识别内部因果机制。 | §3 operational definition、§6.1、S4/S6 | 本节比 §6.1 多一层科学解释，至少一个与先前文献的具体对照 |
| **A07** | P1 | §7.2 S7-P03–P05 | 用同一候选集下知识价值取决于竞争选项的观点组织；2×2/3 seed/9 draws 数值留 §6.3/S5/S8；明确 known sampled-metric issue → fixed-knowledge expert value interpretation。 | 10,222 paired、−0.04120→+0.04631；allocation 非 causal；3 pairs/one fixed pair 9 draws | 不做独立 candidate count 因果推论；本节具有独立 KBS 知识评价意义 |
| **A08** | P1 | §7.3 S7-P07–P08 | 与 §6.2 区分：不重复完整 Utility/Difficulty 数值与 selected/unselected 均值，解释估计专家相对收益与预测 Base Difficulty 的决策区别；承认已发表 deferral 的目标相关研究。 | 6,650 TEST matched-count，Difficulty retrospective top-m；TEST Spearman 0.173 | 不把 Utility 目标称为全新通用 L2D；不将事后 batch comparator 称在线冻结基线 |
| **A09** | P1 | §7.4 S7-P09–P11 | 约 140–190 英文词的集成有效性段落（可根据学术准确性略浮动）：Twitch frozen policy vs KuaiLive post-hoc；retrospective target state vs pre-outcome features；positive overhead vs unmeasured production latency。将 3 checkpoints、9 draws、10-minute、mask replay 的展开细节回 §5/§6/S1–S9。 | 严格保留 three-tier inference、one-positive NDCG、0.991/2.007 ms 的方向 | 不形成 lengthy limitations inventory，也不把负面事实消失 |
| **A10** | P1 | §7.5 S7-P12–P13 | 以一个 operational knowledge-use principle 收束：Base-relative valuation + history/candidate regime + pre-outcome selector；突出“知识存在/可靠/增量决策价值”的区别；压缩 Future Work 清单。 | C1–C3、大纲 §7.5、§6.5 CPU positive overhead | 明确与 §8 Conclusion 区别，避免重复结论与未来实验流水账 |
| **A11** | P1 | §§1↔6↔7 全局 | 逐段跑一轮“Introduction question—Results observed fact—Discussion conceptual inference”双向连接，检查每段是否推进同一个主张且证据不越界。 | 冻结证据表、各段 source anchors | 无无证据的概括性外推，也不把 C2/C3 写成同一平台跨环境 gate |
| **A12** | P1 | 全文结果/讨论语体 | 对所有 P1 段落做发表级 academic rhetoric 检查：从 \`we did not...\` / \`these are not...\` 转向支持充分的正面主张，边界在必要位置简练表达。 | 必须保护统计与推论限定 | 论文不再主要围绕“我们没做什么”展开，负面数据全部保留 |

**实施优先级**：A01→A03→A04/A05→A06–A10→A11/A12；A02 可在 §1 固定后与 §7.3 学术定位同步。**这不是按编号把 C1/C2/C3 拆成三个互不相干任务的顺序。**

## 三、P2 任务队列：集中归位，避免无差别压缩

| 任务 | 对应段落 | 必须执行的精修 | 对应章节证据保护 |
|---|---|---|---|
| **B01 §1 收束** | S1-P06 | 科学适用范围保留但压缩；不要用否定语气收尾 | 仅离线和指定模型、候选协议 |
| **B02 §2 文献比较** | S2-P01–P02、P05、P07 | 以最近邻所解决的具体问题为比较轴、减少模型名称并列堆叠 | 已正式发表版本/真实研究任务，不制造 SOTA 数值竞争 |
| **B03 §3 前向说明** | S3-P01、P06、P09、P11、P14–P15、P17 | 保留五个数学对象，去掉“第几节以后处理什么”的写作流程，matched-m 细节归 §5 | \`a(Z)\`、\`η_r\`、target-only labels 和 protocol 定义 |
| **B04 §4 流程/角色** | S4-P01、P03、P10–P12 | 图—正文一一对应，将 feature 配方与 comparison 方法分工清楚，删除反复的“详见§5” | 专家权重及 14 个 pre-outcome inputs、双平台 Base 任务 |
| **B05 §5 主稿协议** | S5-P01 及 §5 其他 KEEP 段落 | 形成方法边界的固定唯一叙述位置，而非大面积删减；保留写作转移后足够复现信息 | 数据时序、TEST 冻结、候选资格、Difficulty retrospective matched count、抽样/bootstrap |
| **B06 §6.1–6.2 紧缩** | S6-P02、P04–P05、P08–P10 | selected-group descriptive 不是新 independent validation；DEV subgroup enrichment 配置可迁至 S7 | 95% user-paired CI、TEST/DEV 标签、Oracle 同预算 |
| **B07 §6.3 精度与密度** | S6-P13–P16 | 只留决策环境反转、membership/reference 主要说明；模型种子 SD 与候选 draw 范围压缩 | S5/S8 分别独立模型种子与 fixed-pair draws |
| **B08 §6.4 DEV-only 余项** | S6-P19、P21–P22 | 参数网格、target recurrence 详细结果进入 S4/S6，主文保留结果对 C1/C3 的核心支持 | 事后指标与单独训练的不同 context Base |
| **B09 §6.5 费用路径** | S6-P24、P26 | 将真实 CPU 平均开销置于前景，理论量级和缓存解释压缩到 S9 | distinct HGB / archivemask replay / no speed-up |
| **B10 术语和证据等级** | §§3–7 KEEP+P2 段落 | 合并同一目标状态可观测性限定、离线 NDCG 特性和与泛化结论的重复说明 | 不漏掉目标泄漏、不同平台任务/候选集差异 |
| **B11 全文 BibTeX/引用** | §2 最近邻及整体 BibTeX | 保持正式发表 DOI/作者/年份一致；无须为引用数而增加文献；评估 1 条未被引用的记录是否保留 | 出版社/会议正式页面，24+新增记录审查日志 |
| **B12 术语规范化** | 全章 | \`Base\`/ \`Memory\`/ \`Utility\`/ \`Difficulty\`、\`candidate regime\`、\`score-reference\` 首次定义与后文统一 | 用术语清晰度替代反复列边界 |

## 四、转移/合并登记：修改不能损失科学信息

下列内容可以从叙事密集段落转移，但先确认其 **§5、§6 主文最低充分描述**与 S1–S9 的落点：

| 易重复内容 | 当前段落 | 建议稳定落点 | 不可迁移掉的最低科学信息 |
|---|---|---|---|
| 原始阈值、6,563 DEV vs 6,650 TEST、hindsight Difficulty count | §3 S3-P14/15、§6 S6-P05/07、§7 S7-P07 | §5 实验协议 + §6.2 主结果 + S2/S7 | 比较器不是同样冻结的线上阈值 |
| 三个训练 checkpoint pair × 九个 candidate draws 解释 | §6 S6-P14/15、§7 S7-P05/09 | §6.3 一句 + S5/S8 详细数据 | 九 draws 只在原始 fixed pair 上，非 27 trials |
| 2×2 membership/reference 分解表及显著值 | §6 S6-P12/13、§7 S7-P04 | §6.3 四格表和简要解释 + S8 | algebraic attribution 不等于 count-only causal |
| Long-only、Full、历史窗口变体、DEV 参数组 | §6 S6-P19/20/21/22、§7 S7-P02 | §6.4 一条主发现 + S4/S6 | Long-only 对不可用目标不利；不同 Base 分别训练 |
| 加权百分位 feature 和 selector 详细实现 | §4 S4-P10、§5 S5-P13 | §4 简要角色 + §5 参数 + S2 | 决策前可观测、参数不透支 TEST |
| CPU replay: 3 hosts、1200 queries、81-tree HGB、route masks/cache | §6 S6-P25/26、§7 S7-P11/13 | §6.5 实测开销+核心边界 + S9 全设置 | 2.007>0.991；不宣称 net online saving |
| 一正样本评价、Twitch 10-minute 观测精度 | §5 S5-P04/11、§7 S7-P10 | §5 实验定义 + S1，§7.4 一句最必要解释 | 不把 NDCG 当真实用户 engagement |

## 五、逐条验收记录的统一模板

第二阶段每个修改项必须记录：

| ID | 源段落 ID 与旧代码 blob | 新位置与文本 diff | 论证改善点 | evidence check | KBS reviewer disposition |
|---|---|---|---|---|---|
| Axx/Bxx | \`Sx-Pyy\`/旧 commit | 只改获准章节，记录合并/转移 | 是否显著推进中心科学问题 | C1/C2/C3 事实与证据位置不变 | \`PASS\`/\`REVISE\` |

**阶段一 Gate 1 通过条件：**
- 段落矩阵覆盖 §§1–7，全体有稳定编号与证据连接；P1/P2/KEEP 合计覆盖全部 95 个 prose units；
- 科学对象 C1–C3、6.1→6.2→6.3 和 Twitch/KuaiLive 两条证据链明确；
- 关键实验数据和不可删除的推论边界有 SHA 追溯；
- 任务具备明确修改动作、章节落点和验收条件，后续无需以猜测取代方案；
- \`main.tex\` 和集成 S1–S9 未随阶段一改变；
- 不将尚未完成的 Abstract、Conclusion 计入已完成范围。

**阶段二 Gate 2** 仍是未来工作：§1 和 §§6–7 按本队列修订并用 frozen-baseline diff 检查；完成后才进入 §2–§5 协调与全文语体优化。

