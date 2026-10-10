# KBS 投稿级全文论证与学术表达修订计划（大纲对齐版）

**制定日期：2026-10-10。**  
**最新执行状态（2026-10-10）：第一阶段 Gate 1 通过、第二阶段 Gate 2 通过；第三阶段已实际完成 §2–§5 协调修订和源码级学术审查。** 最新主稿为 [db6f9654](https://github.com/mzch0210/KuaiLive-Agent/commit/db6f96545fdbdede198f4a129a29f6db0735a92b)，匹配构建 [#38040591733](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38040591733) 的结果以对应工作流和验收报告为准。详见 [第二阶段报告](STAGE2_ARGUMENT_REVISION_AND_GATE2_REVIEW_2026-10-10.md) 与 [第三阶段报告](STAGE3_RELATED_WORK_METHOD_PROTOCOL_COHERENCE_AUDIT_2026-10-10.md)。初版四阶段任务文字作为历史计划保留；第四阶段全篇独立审稿及 §8/Abstract 仍在后续范围。  
**权威大纲：** [KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md)。  
**当前主稿：** [main.tex](main.tex)，截至制定时具有 §§1–7，缺 §8 Conclusion、Abstract。  
**补充证据：** [SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md)。  
**已完成的前次技术验收：** [Section 7 整体跨章审查](SECTION7_COMPLETE_CROSS_SECTION_CROSS_CHAPTER_KBS_AUDIT_2026-10-10.md)。

## 一、基本判断：恢复大纲的论证路线，而不是重新发明主线

**大纲已经确定中心论点及对应的证据组织。** 之前将“全文缺少连贯学术叙事”等同于“大纲中的科学论点不存在”，不准确。真正需要纠正的是**正文的科学问题、实证贡献和解释性文字之间没有始终保持同一条主线**。此前已通过的编译、引用、数据与局部 reviewer-style 精修不能替代全篇的学术论证验收。

**大纲原文中心命题（§1.1）：**

> The central problem is whether a fixed specialist instantiated from historical relationship evidence improves ranking relative to the trained base on a given event and candidate regime.

**投稿时建议坚持的英文科学主张（只作为写作定盘星，不机械重复进各节）：**

> Historical relationship evidence has context-dependent marginal ranking value relative to a trained incumbent: its contribution varies with accessible history and the eligible candidate environment, and pre-outcome estimates of this relative value can guide selective specialist use.

这一定盘星是**知识价值的操作性、情境性及其决策用途**。论文不是一个“新记忆模型 + 新路由器 + 采样指标发现”的并列组合，更不是已被证明跨平台通用的知识调度算法。

**大纲已固定的三个贡献：**
- **C1：** 指定 Base / 固定 Memory / 指定候选集下的事件级增量排序价值，及 Twitch 目标历史状态异质性；`\Delta_M` 减法本身不是新理论。
- **C2：** KuaiLive 固定事件及 checkpoint 下的候选环境依赖性，候选 membership/reference 的两路径分解仅为描述性；目标状态是事后诊断，而非 serving 特征。
- **C3：** Twitch DEV 训练及阈值冻结、TEST 一次性评估的 pre-outcome Utility 选择，对照 Base 和 TEST 批次事后匹配调用次数的 Difficulty；不等于泛化的新 Learning-to-Defer 理论。

**大纲的结果呈现顺序必须尊重：** `6.1 conditional value → 6.2 predictive decision value → 6.3 candidate-context boundary`。不能仅为追求 C1/C2/C3 编号顺序而调换 6.2/6.3。两项相互补充的发现为：**Twitch：知识条件价值与冻结选择验证**；**KuaiLive：相同知识专家的候选情境依赖性**。因此正文应区分一条**实证决策链 C1→C3**和一条**评价情境解释链 C2**，再在 Discussion 中将它们综合为统一的知识使用原则；不能暗示已有一个跨 Twitch 和 KuaiLive 共同验证的情境自适应门控策略。

## 二、KBS 投稿定位及写作检验

KBS 官方范围（[Elsevier 官方期刊介绍](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)）涉及知识驱动 AI、推荐系统、预测决策支持及理论/应用平衡。本稿的审稿竞争力应来自：
1. 明确的 **knowledge-as-decision-evidence** 对象，而不只是加入历史记忆提升指标；
2. 对 **相对价值为何随已有 Base 和候选环境而变化** 的有限但有力、可追溯的解释；
3. 一个 **决策前可用、可在冻结 TEST 上验证** 的知识选择机制；
4. 把实用开销放在正确的证据等级，并将已正式发表的 L2D、知识融合、sampled metrics 文献作为前人工作准确比较。

Elsevier 的一般编辑写作指导（[Results 与 Discussion 职责区分](https://www.elsevier.com/connect/11-steps-to-structuring-a-science-paper-editors-will-take-seriously)、[Discussion 写作](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/steps-to-write-excellent-discussion-in-manuscript/)）要求结果清晰、讨论解释科学意义而非重复数字，恰好对应当前问题。这不是 KBS 特有的强制篇幅要求；不可把一般投稿文章的建议冒充 KBS Guide for Authors 具体格式规定。

## 三、固定证据与不可更改的科学边界

**修订范围为论文论证与文字组织，不重新拟合模型、不进行 TEST 再调参、不篡改已冻结结果。** 写作时的最小“锁定数据表”如下。

| 科学用途 | 已锁定事实 | 禁止误述 |
|---|---|---|
| C1 / Twitch | 44,221 TEST；Base 0.58211，Always-Memory 0.53980；recoverable n=5,539、Memory−Base +0.22045 | 无条件普遍优于 Base；目标相关状态作为在线特征 |
| C3 / Twitch | Utility 0.58983、与 Base +0.00772、与事后等次数 Difficulty +0.00644；6,650 调用/15.04%；TEST Spearman 0.173，约 11.7% hindsight Oracle headroom | Difficulty 是独立冻结的在线预算策略；Twitch 选择器跨平台零样本有效 |
| C2 / KuaiLive | 10,222 配对 TEST 事件；sampled-active −0.04120、full-active +0.04631；shift +0.08751；membership +0.08827 / score reference −0.00076 | 采样数量的单独因果效应；KuaiLive 是新冻结 TEST 策略验证 |
| 鲁棒性 | 三个独立训练 checkpoint pair；额外九个 sampled draws 属于**原始固定 pair**下的三种大小 × 三个随机种子 | 三组模型×九组列表是 27 次独立试验 |
| 计算 | 单独 KuaiLive warmed CPU scoring：Base 0.991 ms，Selective HGB 2.007 ms，增加 +1.016 ms、约 2.03×；调用分布与 Twitch 不同 | Twitch 选择策略已经证明延迟下降、收益超过计算开销或在线商业增益 |

统计置信区间、原始 provenance、参数、候选构建和 S1–S9 不随修辞偏好修改；任何数值改动必须先回到源证据。**已报告负面现象是研究结果，不应被“正面表达”删掉。**

## 四、章节级修订地图：最小充分改写，而非逐章无差别推倒

| 位置 | 当前问题 | 修改动作 | 严格保留 |
|---|---|---|---|
| §1 Introduction | 研究问题、实证发现、贡献列表虽俱全，但少数段落仍像文献/实验概述；尚未建立可持续追踪的中心张力。 | 用大纲 §1.1 的科学矛盾组织段落：**已有历史表示能力 → 额外知识可能冗余/互补 → 需在具体 Base/候选下估计价值 → Twitch 决策证据与 KuaiLive 情境证据 → C1–C3**。强调知识系统的 operational decision question。引言正文**不另造显式 RQ1/RQ2/RQ3 列表**（大纲已禁止）。 | 现有标题、两种数据集身份、C1–C3、事实上的不同证据层级 |
| §2 Related Work | 文献类别和已发表最近邻基本齐备，但部分段落以“别人做 X、我们不做 X”结束，缺乏正面连接。 | 每组文献围绕一个学术比较轴收束：representation vs added decision value；reliability/fusion vs incremental utility；general deferral vs history-specialist ranking objective；sampled metrics vs knowledge-value evaluation。保留 MemRec、GUIDER、DCGLive 的正式发表引用。 | 已核验文献版本；不堆砌无比较价值的新引用 |
| §3 Problem Formulation | 公式准确，部分句子将实施限制和实验步骤带入概念论证。 | 保留 event/ranking utility → \Delta_M → \eta_r → expected policy gain → regime/state decomposition 的链条，合并重复解释，将 DEV/TEST、comparator 具体细节集中 §5。 | 全部数学等式、符号及 target/post-outcome 信息边界 |
| §4 Framework | 组件说明较完整，主机制“为什么选此知识专家、为何该输入构成可观测决策”仍可更突出。 | 用一条机制线解释 incumbent、单独 Memory、observable relative-utility estimator、selective choice 之间的职责；确保 Figure 1 与正文叙述一致。少写“后来在§5定义”式流程性过渡。 | Base/Memory 配方、图的事实含义、训练和选择过程 |
| §5 Experimental Setup | 规范性信息必要，但部分冻结、候选规则和解释边界出现在 §3–§7 多处。 | 在 §5 明确一次性给出 dataset/split、candidate regimes、Twitch TEST freeze、Difficulty 同次数 retrospective batch control、offline metric/paired bootstrap、资源实验条件。把证明可复现的细节与主文问题直接相关的条件留在 §5；实验日志归 S1–S9。 | 避免 target leakage 的全部关键定义、合法时间范围、结果可复现性 |
| §6.1 Heterogeneous Value | 研究发现清楚，但部分解释/限制与 §7.1 重叠。 | 首句“发现”先行，保留核心 State 图/表；精确给出整体劣势与 recoverable 正收益，段尾解释对 C1 的意义。 | 主图、冻结 TEST、状态由目标确定的事实 |
| §6.2 Relative-Utility Choice | 冻结证据最有说服力，但与 §7.3 比较的描述重复。 | 用“what relative utility selection delivers”连接 §6.1；主文保留 Utility/Base/Difficulty/Oracle 核心表现及公平性信息；机制解释留给 §7.3。 | TEST 数据、置信区间、Difficulty 的事后 matched m |
| §6.3 Candidate Regime | 分解和种子/抽样结果信息密集，容易呈现为并列实验清单。 | 按“相同事件/固定专家 → 排序环境改变 → 效用反转 → membership/reference 描述性解释 → 不同变异源支持方向稳定”组织。主文保留四格表和一组关键分解值，抽样表格等细节交 S5/S8。 | 全部已有指标与描述性而非因果解释 |
| §6.4 Robustness | DEV feature/memory/length/recurrence 等多类实验集中，掩盖其对应的主研究问题。 | 划分成“选择预测依据”“历史知识与 Base 表示互补”“候选/时间效度”三类；主文每类只选支持论点的核心结果，其余在 S3/S4/S6/S7。明确 DEV-only 而非新 TEST。 | 主文已有的明确支持链；不可选择性隐去反例 |
| §6.5 Cost | 计时条件与重要观察交织；读者可能误把低调用率看作省时。 | 先报告 **实际平均延迟增长**，再解释原因（base、feature、gate、conditional Memory）；单独说明缓存/回放条件并链接 S9；不在 Results 反复长篇讨论未来工程。 | HGB 与其他策略不是同质量/同预算测试 |
| §7.1–7.3 | 反复呈现结果值与相对效用定义，机制和文献联系尚可加深。 | 从 C1 提炼 incumbent-relative complementarity；从 C2 提炼 operational valuation depends on ranked alternatives；从 C3 提炼 expert solvability versus Base Difficulty 的知识选择含义。每节**以一句学术解释开头、给一个最必要证据、以一句新推论结束**，不再充当第二版 Results。 | 已证实结果、published closest-work distinctions、准确的信息访问边界 |
| §7.4 | 三段约 270 词多为实验边界复述，降低 Discussion 主要观点密度。 | 优先压缩为约 **140–190 词** 的集中有效性段落或紧凑小节：一条证据等级、一条离线 observability/candidate 定义、一条实际 compute/transfer 限制。实验细节以 §5/§6/S1–S9 为支撑。**字数为编辑目标，非硬阈值。** | Twitch TEST vs KuaiLive post-hoc，诊断标签 vs pre-outcome，正的 CPU overhead |
| §7.5 | 已有一体化思想，但研究展望仍可能覆盖设计原则。 | 用 Base--specialist / event / candidate unit 的 **incremental knowledge decision value** 做结论性设计命题。第二段收束其用于知识评价与调用的实施条件；未来工作压缩至必要验证方向。 | 不宣称新算法定理、通用部署优势；与 §8 作用区分 |

**明确不做的改动：** 不为了 C1–C2–C3 编号顺序改变第六章的**大纲既定结果顺序**；不人为增加主文 figure/table；不将“目标相关 recoverable”当作在线可观察的 gate 特征；不将已报告的限制性证据删光，也不把所有方法透明度信息移出主文。

## 五、语言编辑规则：学术自信与实证克制同时成立

逐段赋予主要角色：**问题/主张（claim）—定义与机制（method）—证据（evidence）—解释（interpretation）—必要边界（scope）**。一段只承担一个主要职责；跨章出现的同一数字通常只在 Results 报完整，Introduction 提方向性发现，Discussion 讲解释意义。

**三类句子区别处理：**
1. **必须保留：** 实际观察到的负面结果，以及防止因果、数据泄漏、可用性和统计外推误读的最小限定；其位置应集中、清晰。
2. **应压缩或迁移：** 反复出现的 `DEV-frozen`、`previously examined TEST`、`not independently frozen online`、`not causal candidate count`、checkpoint/seed/mask 等流程说明，在 §5/S1–S9 首次完整交代，Results/Discussion 只在可能误解时一句提醒。
3. **应删掉/改写：** 强调“我们没有做什么”“选择保留旧模型是因为……”“该组分析不是……”的连续防御句及 run/commit/analysis history。用正面解释的学术句式承接，底层边界仍必须可追溯。

**范式示例（在正文修改时视语境使用，并非替换全部边界）：**
- 从 `This is a descriptive allocation ... does not isolate a causal candidate-count effect.` 转向 `Within the evaluated protocol, changes in the ranked alternatives account for the dominant share of the observed specialist-value contrast.`，同时在方法或相邻句保留其成员项混合 count/composition/competition 的限定。
- 从 `The frozen Twitch TEST comparison supports this distinction at the policy's realized specialist-use count.` 转向 `Predicting specialist-relative benefit identifies more valuable opportunities to invoke historical evidence than predicting incumbent difficulty alone in the evaluated setting.`，并将具体实验比较放在 §6.2。
- 从 `The measured overhead motivates prospective end-to-end timing ...` 转向 `The decision value of auxiliary knowledge must be weighed against the cost of acquiring and applying that knowledge.`，同时保持 §6.5 中对正开销的实际报告。

**禁止作为验收方式：** 删除全部 `not`/ `only`、机械缩短篇幅、将离线推论改写成“工业落地验证”、以语气更强替代证据。

## 六、四阶段执行安排及每阶段验收关口

### 阶段一：建立大纲—正文论证对照矩阵，冻结事实与修订范围

- 为 §1–§7 的每个段落标注：其解决的大纲问题、主要学术功能、所支持的 C1/C2/C3、原始证据指针、是否重复、是否含过程性/防御式表述。
- 绘制 **claim–evidence–interpretation–chapter** 矩阵，特别保留 Twitch 一次冻结政策与 KuaiLive 同队列候选诊断的分离。
- 建立待修改语句清单，按 P1（论证中断或贡献模糊）/P2（冗余和语体）分级；保留未修改的源稿快照和科学结果摘要。
- **输出：** 全文段落审计矩阵、编辑优先级清单、修订前主张冻结表和 GitHub 源码版本。
- **Gate 1：** 不更改大纲核心命题、C1–C3、6.1→6.2→6.3 顺序；明确每一实验属于何种证据等级。

### 阶段二：优先修复高影响的第 1、6、7 章叙事

依赖关系：**§1 引言的科学问题陈述 → §6 事实上的发现顺序与重点 → §7 机制解释和知识决策启示**。

1. §1：在现有引言基础上突出 tension、operational knowledge question、Twitch/KuaiLive 两条互补证据；避免为了篇幅要求空泛扩写，也不新加显式 RQ 列表。
2. §6.1–6.3：原有排序不变、数值和主表不变，逐节调整 topic / transition / final interpretation；使每节首尾分别回答一项大纲问题。
3. §6.4–6.5：将开发诊断和性能成本分工明确；减少 run/protocol chronology 在结果叙事中的占比。
4. §7.1–7.5：在 §§1 和 6 稳定后一次性综合改写，减少重复数值、压缩 §7.4、防止 §7.5 退化成未来实验清单。专门检查 Discussion 是否真正比 Results 多了一层知识决策解释。
- **输出：** §1/§6/§7 针对性的 LaTeX diff、逐段原因、证据不变清单与 PDF 预览。
- **Gate 2：** 引言的核心张力能由 §6 的主要证据回答，§7 不再重复详细结果而能清楚阐述科学意义；没有新增未经支持的外推。

### 阶段三：协调 §2–§5 与全文学术表述

- §2：按“最近邻—对应差异—本文的增量问题”组织，正式发表版本优先，维持已核验 MemRec/GUIDER/DCGLive/deferral 文献真实信息。
- §3–§4：压缩重复解释，保持数学公式、模型配方和流程图不变，确保 `Delta_M`、`eta_r`、`a(Z)` 的定义及决策时间信息一致。
- §5：集中承载 split/freeze/comparator/candidate/统计协议，补足从 §6–§7 移回的必要复现信息。
- 纵向检查所有标题、术语（Base, Memory, Utility, Difficulty, candidate regime）、§末过渡段、表注、引用、补充材料和所有负面/过程性表达。
- **输出：** §§2–5 协调版本、术语一致性清单、审稿级语言问题消除报告、完整 main.tex 初稿。
- **Gate 3：** 理论定义与实际对照、训练/测试隔离和因果限定的文本一致；不因压缩而失去复现所需的主文信息。

### 阶段四：全篇 KBS 独立叙事审查与投稿级冻结

- **双重审稿视角：** KBS 读者是否能够独立概括研究问题、为何需要这项研究、知识系统层面的原创认识；方法审稿人是否能够逐项追溯 C1–C3 的精确证据和边界。
- **对照检查：** 引言的主张 ↔ 正式大纲 ↔ §3/§4 的对象 ↔ §5 的设置 ↔ §6 的表、图、数值 ↔ §7 的解释 ↔ S1–S9；所有 2026 正式发表文献的正文表述与 BibTeX 保持一致。
- **验收内容：** LaTeX 编译、引用/交叉引用/图表编号、关键数字校核、全文分页视觉检查、科学定位和同行审稿风格评估；列出 remaining P0/P1/P2 项。
- **Gate 4：** P0/P1 科学论证矛盾归零，P2 仅余不妨碍学术叙事的编辑事项；主稿和补充材料同一证据版本。项目进入 §8 Conclusion → Abstract → Highlights/Declaration/Author Info 等正式投稿工作。
- **不能以单一 Gate 代替另外 Gate：** 构建成功≠叙事通过；文风积极≠限定消失；审稿通过≠已证明录用概率。

## 七、具体完成判据（可机械检查与人工审稿联合验证）

**主线连贯性**
- 不看 Contributions 列表，只读 §1 的开头及末尾、§6.1/6.2/6.3 首尾、§7.1/7.3/7.5，能够自然复述**一个** Base-relative knowledge-use 科学主张。
- 每个 P1 主张具有一个明确证据链，而不是由不同平台的实验合并成为未测试的跨平台算法声称。
- 本文与知识融合、MemRec、GUIDER、L2D、sampled metrics 的贡献区别在 Introduction/Related Work/Discussion 一致。

**论证职责**
- §3 只负责定义事件、相对效用和决策对象；§4 负责实例化；§5 负责操作性协议；§6 负责新证据；§7 负责其科学含义。
- §6.4 不再是互不衔接的 DEV 诊断罗列；§7.4 的比例与边界足以防止误解但不淹没知识系统原理。
- 主表/图只承担一个清晰的证据任务；不重复在各节全文列举所有数值。

**学术表达**
- 每段主题句直接回答一个研究问题或提供一个有据可查的解释；过程/限制性句集中在真正影响科学推论处。
- 负面结果原样保留，但删掉明显自我辩护和 run/checkpoint 过程叙事。
- 句子不凭空宣称因果、真实用户行为改善、Latency saving、普适专家优势、跨平台 selector transfer。

**投稿技术**
- 已引用参考文献均有真实正式发表版本；图表和 supplementary citation 指针准确；PDF 全部页面可读；当前无 Abstract/Conclusion 状态在最后一阶段前不得冒称投稿完成。

## 八、过程控制和审稿风险排序

**P1 先改：** §1 的中心张力；§6 每节发现的科学角色和连续性；§7 的解释增量与重复/防御句；Twitch frozen vs KuaiLive post-hoc 的跨章证据角色。  
**P2 同步处理：** §2–§5 的叙事与术语，少量图表标签、源证据指针、未被引用的 BibTeX 记录；最终格式要核查 KBS 当前 Guide for Authors。  
**不默认追加实验：** 只有 Gate 2–4 识别到“必须提出而原实验不能支持”的 P0/P1 关键科学主张时，才单独提出试验需求及收益/成本选择；不能用更大范围结论去迫使已完成研究追加不必要的实验。

**执行顺序为“对照矩阵与冻结 → §§1/6/7 论证修复 → §§2–5 协调与全篇语言整理 → 独立审稿及投稿冻结”。** 全程保留 GitHub 原始版本、独立 commit 与对应构建记录，不以“局部审稿通过”代替完整研究叙事通过。
