# KBS 论文“中心论点优先”整稿结构性修订总计划（2026-10-13）

**性质：待执行的正式编辑方案；本文件的提交不意味着主稿已被重写，也不构成新的实验或期刊录用判断。**
**目标期刊：Knowledge-Based Systems（KBS）。**
**版本锚点：** 仓库 main 在制订计划时为 ed2a8d8de0c602fd9a45920b792858788e49e183；主稿 manuscript/kbs_latex/main.tex 的 Git blob 为 f46540dce8b076e08937e8f5912048eeff994ad1；参考文献 kbs_references.bib 为 a33cb506fc2d08b422232a10e91a9d06c44044f5；合并补充材料 S1–S9 为 3f9413f8ffe2a2ff1ef70640a3820d81b281055f；R8 主稿已编译为 37 页、补充材料 33 页。此前 R0–R7 的技术性 PASS 并不等于独立 KBS 科学叙事验收。
**范围：** 对仓库 377 条树条目进行源文件地图核查，优先复核最新八章、合并 S1–S9、R0 12 项证据矩阵、G0F/G5 冻结方案与 six-Base registry、G4/G5 成果、原 KuaiLive P0/P1/P2、Twitch 原冻结对照以及此前 G0–G5/R0–R8 编辑与风险记录。早期状态报告和分节 S4/S7 等历史草稿只用作溯源，不得覆盖最新 G5 或 R6 版本。项目代码和工作流用于核实证据链；不声称本计划已逐行运行或独立重算所有原始数据。

## I. 总体编辑决策：研究主线、层级和核心张力

### 唯一中心科学问题
在已有序列推荐模型已经使用用户历史的前提下，固定的长期用户—创作者关系证据在当前候选集合中是否仍产生额外排名价值？能否利用决策时可获得的特征预测这种特定专家相对已有模型的额外价值，从而改善给定 Memory 调用约束下的推荐选择？

### 建议中心结论（正文主线）
**The marginal ranking value of a fixed relationship-memory specialist is conditional on the incumbent and candidate context; estimating this event-level value supports better specialist selection under a specified invocation constraint.**
这是现有研究可以验证的“测量—理解—选择”链条，不是新通用 learning-to-defer 理论、普适候选数因果定律，也不是已证实的生产级成本优化结论。

### 三个相互衔接的学术问题（不是三篇小论文）
- **RQ1 / C1：Value.** 固定 Memory 相对具体 Base 的增量排名价值是否异质？主要 Twitch 冻结 TEST 的 Memory 负总体/可恢复历史正子群，与 M3 固定 Memory 在六 Base 对照下正总体。跨任务符号不归因于某一单因子。
- **RQ2 / C2：Context.** 为什么“知识价值”定义必须包含候选排序环境？原始 KuaiLive 相同 10,222 个 room 事件、固定 raw scorers 的 sampled-active/full-active 配对逆转；2×2 allocation 是候选成员与规范化参照的协议内描述，不是孤立候选数量因果效果。其作用是解释测量目标，不能宣称已独立验证 C3。
- **RQ3 / C3（主要决策结果）：Decision.** 预测固定 Memory−Base 的 NDCG@10 而非 Base 难度/专家单独精度，能否获得更好的给定调用设计下选择？Twitch DEV-frozen Utility/回顾性同次数 Difficulty；M3 五种 DEV-frozen pointwise 规则与六 Base、同一 TEST 用户群。
- **横向边界 / Decision versus deployment：** M3 无条件 Memory 0.346792 高于全部 Utility 0.301766–0.304004；仅在预热 256 DEV 事件测量路径 Memory 0.8033ms 小于 Utility 1.8018ms。基于设定的 Memory 调用约束做的“选择质量”结论，与系统总时延/部署最优性结论不同；把这一反直觉结果组织为知识使用与系统资源约束的科学讨论，而不是反复的自我否定。
- **结果章编辑顺序：C1 → C3 → C2 → 支持性证据 → 资源讨论。** 这是“先给出主冻结发现、再解释候选依赖”的呈现顺序；理论逻辑和引言中先界定 candidate-conditioned estimand，并不意味着 C2 的事后实验为 C3 的先决因果证据。

## II. 证据状态与不可更改的结论边界（每一阶段共同适用）

| 证据身份 | 固定结果或协议 | 论文可声称什么 | 绝不能偷换成什么 |
|---|---|---|---|
| Twitch / LiveRec 冻结 TEST | 44,221 streamer events；Base 0.58211、Memory 0.53980、Utility 0.58983；Utility 调用 6,650 / 44,221（15.04%）；Utility−Base +0.00772 | 当前冻结 Utility 在对应 Base 和测试环境下提高 NDCG；可恢复但 Base 当前输入不可见的目标上 Memory 有正相对价值 | Difficulty 回顾性 TEST top-m 匹配不得写成另一个 pointwise frozen TEST 规则 |
| 原 KuaiLive 房间候选配对诊断 | 10,222 相同 room targets，样本 575、full active；Memory−Base −0.04120411 / +0.04630669、paired shift +0.08751080；接受口径 CI [0.08210,0.09326] | 现有排序协议内的候选依赖标签逆转；membership/reference 分配为描述性 | 新的 untouched TEST、新的 author 任务复现、独立候选数因果效应 |
| M3 一次性冻结 TEST | 47,575 author events，12,533 users，全量 TRAIN-known available authors，TEST 中位候选 31,065；SASRec/GRU4Rec 各 3 seeds | 五种 DEV-frozen selector 的 out-of-time 单次 TEST；六拟合用于架构/初始化稳健性 | 六个独立数据集、room 任务、person-disjoint holdout、跨平台模型迁移 |
| M3 策略比较 | Utility 各 fit 0.301766–0.304004；Primary seed Utility 0.302866、Difficulty 0.282479、Specialist 0.279558、Uncertainty 0.289373、History 0.279789；TEST Utility 调用率 27.718–29.215% | 六 fit 上 Utility 相对四项指定选择目标获得更高 NDCG，且在观测 TEST 中调用 Memory 次数更少；报告质量和 calls 双维度 | “所有替代算法的最优 Pareto 前沿”“严格同一 TEST 预算”“最低延迟”；未经检验的 Uncertainty 差异不是预注册主检验 |
| M3 统计 | 三个主对照 Utility−(Base,Difficulty,Specialist)，每 fit Holm(3)，5,000 user-cluster bootstrap/sign flips；全部 fit 共用用户 | 各拟合内预先指定的显著结果和区间 | 全球 18 次比较的总体 FWER 或六个独立人群的泛化 |
| 资源与 baseline | M3 warmed 256 DEV 条件 Memory 0.8033ms、Utility 1.8018ms；M3 Memory NDCG 0.346792；原 KuaiLive CPU 575-room 是独立测试环境 | 真实计时条件下的选择路径开销；指出何种资源成本假设才能使调用约束有部署意义 | 净服务速度提高、少调用就能少总计算、隐含的真实外部调用价格 |
| 证据保管 | G0F pretest protocol、six-Base registry、G5-A label-blind→G5-B label reveal、R0 matrix、最终 R6 组合 S1–S9 | 披露可核对的聚合统计及明确限制的数据可用性 | 伪造永久 DOI、强行公开可能有许可证/隐私限制的事件级记录，或把早期“TEST 未完成”快照当现状 |

具体可信源的优先级：G5 原 one-shot 结果与冻结注册文件 > 当前 R0 证据矩阵和 R6 验收核对 > 主稿与最新 S1–S9 > 历史任务阶段成果；遇到小数、bootstrap 设置或样本来源冲突必须查原接受的 artifact/代码，不按叙事有利性挑选。科学结果不得因编辑目标重设或二次挖掘 TEST。

## III. 写作标准：哪些修改属于提高学术水平，哪些属于证据遮蔽

### 建立逐段“主张—功能—证据—位置”矩阵
重新基于**最新**主稿 646 行和 Abstract，生成当前段落矩阵；2026-10-11 的 94-paragraph 审计是扩展 M3 之前的历史基线，不能沿用其旧行号和状态。每个正文自然段标注：
1. 一个明确且可验证的主要科学命题；
2. 服务 RQ1 / RQ2 / RQ3 / Methods / alternative explanation / validity 中的哪一项；
3. 显示证据、精确表图或已发表文献链接；
4. 是否主实验 / 事后诊断 / DEV-only / 计算条件；
5. 主文保留、合并、移动 S1–S9、删除重复、改为 Discussion 的动作和理由。
不得只用消除 negative-words 统计判定质量；必须人工复核哪些是有效的科学限制。

### 五类高风险语言与处理规则
- **防御式 novelty 定位**：“not a new generic theorem / not a universal router”等只在与近邻文献比较处集中交代一次，不在引言、公式、图注、Results、Discussion 和 Conclusion 反复重复。
- **阶段/实验日志口吻**：“newly frozen / original P0 / previously inspected / one-shot run / G5 stage / six files”优先转化为科学上必要的 temporal prospective vs retrospective evidence distinction；run ID、hash、操作阶段和工具日志在 Supplement/溯源说明，不在正文反复出现。
- **协议防错冗余**：DEV 30% vs realized TEST calls，575 screening vs room sampled 575，Twitch 14 features vs M3 12、prequential TEST earlier history、six fits shared cohort，在 §5 一次充分定义，其他章节仅在影响推断时最简重述。
- **结果先限定再报告**：将段首改为 discovery-first，数值和用户聚类误差随后给出；合理限制放在就近方法说明或 Discussion 集中整理。
- **不能删的科学事实**：Twitch 平均 Memory 负效应；M3 Always Memory 的更高 NDCG 和较低预热计时；真实 TEST 不同调用率；per-fit Holm 非 global；非因果 candidate allocation；人群、排序单位、候选集差异；数据来源与授权限制。
三条语体验收：每个结果子节第一实质段都有可单独引用的结果发现；每节末尾形成对中心论题的解释；§7 新增解释而非平移 §6 句子。全文不得以重复 “not ... / does not ... / cannot ...” 作为论证脉络。

## IV. 八章与主图表的目标责任分工

| 主文部分 | 应承担的唯一职责 | 编辑方式（依据 2026-10-12 主稿布局） | 主文与 Supplement 界限 |
|---|---|---|---|
| Abstract / title | 用一个研究问题串起 C1→C3 并交代 C2 的解释角色 | 等主结论固定后重写目前 197 词摘要；避免“三个实验逐一流水账”；标题在最后按“条件性知识价值”与“选择决策”定位比选 | 无 run ID/授权/所有方法清单 |
| §1 Introduction（现约 L35–51） | 从已训练 Base 的冗余/互补张力推到条件价值估计及选择问题 | 4–6 连续论证段，重新安排 gap、估计对象、为何 ranking candidates 影响这个对象、两冻结决策场景和三层贡献；避免反复自限定 | 不填统计表和许可过程 |
| §2 Related Work（L52–77） | 正面界定离贡献最近的研究缺口 | 围绕 knowledge representation/fusion、expert selection/L2D、candidate ranking environment 三种比较，优先详细回应 CKLF、MHGFCL、KAPER、Yerragunta、MemRec、GUIDER、Mozannar/Sontag、Narasimhan、Krichene/Rendle；已有原理归功前人 | 不虚构 head-to-head KBS competitor 实验 |
| §3 Problem Formulation（L78–161） | 定义指定 Base+Memory+候选上下文的 ΔM、η、选择目标 | 保留核心数学等式、不可观测目标与可观测输入划分；更精炼地将 TEST budget 细节、特定 tie 语义、预验收顺序移至 §5 | 执行细节归 §5/S2/S7 |
| §4 Framework（L162–247） | 解释框架本质：固定关系专家、可见的特征、估计和选择 | 建立技术读者可以复述的单一工作机制；保留清晰 Memory Short/Long/Popularity 公式和图；Twitch 14维/M3 12维及平台历史特性压缩，移 §5/S1–S3 | 不扩大为训练出“通用算法” |
| §5 Experimental Setup（L248–350） | 一次说明三任务、选定 Base、对照公平性、冻结与统计规则 | 一张三协议表和精炼 comparator/protocol/statistics；清楚区分 Twitch retrospective count-match、M3 五 pointwise DEV freeze；给出 rates 和 Holm 的定义；按需引用 S | 对样本构建、checkpoint SHA、timestamp/hash、模型超参提供补充材料链接 |
| §6.1 C1（L351–416） | 证明额外知识的增量值是条件性的 | Twitch state contrast 和 M3 fixed Memory/Base 汇成一条科学发现；State 标签事后定义不可作 online gate feature | 详细 DEV component variation 放 S4/S6 |
| §6.2 C3（L417–478） | 最核心：证明预测特定专家的增量价值有选择信息 | Twitch 冻结结果 + M3 五冻结对照，把六拟合 NDCG 与实际 Memory calls 的联合优势置于正文重点；主预注册三对照与 Uncertainty secondary 分明；不以调用次数不严格相等为首句 | 30 个调用率全矩阵和 18 CI/Holm 在 S7/S8 |
| §6.3 C2（L479–507） | 解释 ranking candidate context 是价值估计的一部分 | same-event room 575 / full signed reversal + 2×2 成员/参照分解；避免把 old room 变成 M3 replication 或 pure count cause | P1 三 seed / P2 nine negative draws、完整状态分解在 S5/S8 |
| §6.4 Mechanistic support（L508–564） | 以少量最贴近核心论文的结果解释 ΔM 可预测性与可恢复历史 | 保留一个聚合稳健性展示（六 Base 与主要比较）和最直接的 history+Base descriptors OOF 结论；将多组历史窗口、组件逐条结果缩到综合性段落；每项解释与 RQ1/RQ3 对齐 | 原始 S4/S6/S7/S8 保持完整表 |
| §6.5 Resource context（L564–591） | 统一 call quality 与实际 computation 的区分 | 展示 Realized TEST calls、Always Memory 和 256 DEV warmed path；CPU old room 与 M3 GPU 分属不同测量，不合并成本单位 | 微秒级 path 分解和全部分位数在 S9 |
| §7 Discussion（L592–633） | 从经验结果抽象出知识科学意义及可检验边界 | 精炼为 3 主论点：（1）知识价值是 Base/candidate-relative；（2）对固定专家的相对价值预测比 Base difficulty/standalone quality 更针对决策；（3）调用约束有意义的条件和反直觉 Always Memory 结果。独立小段讨论 external validity 而非通篇自辩 | 不重复 §6 所有数值或哈希 |
| §8 Conclusion（L634–646） | 结论总结科学命题、主要已证实证据和意义 | 2–3 逻辑紧密段，末尾为知识系统评价与决策启示；不以整段“没有证明的事情”收尾 | 无追加实验计划/过程回顾 |

**主图表信息架构建议：** 当前主文有 2 图 + 9 表，S1–S9 29 张表。保留框架图；考虑一张清晰的 6 Base × Utility 改善/三主比较的效应与区间图（仅从既有冻结源生成）；以一个关键表并列 primary SASRec 的 five gate NDCG + realized TEST calls + Always Memory；保留三协议表、Twitch 控制表、KuaiLive paired 2×2、M3 warmed cost。建议用“每个主文图表必须能服务某项 RQ”挑选，避免硬性张数/页数指标。不要重新分析冻结 TEST 做未经声明的新显著性发现。

## V. 正式分阶段执行安排（名称 N0–N8，避免与历史 R0–R8 混淆）

每阶段：先记录**基线和差异**，再修改**限定范围**，然后独立学术审阅和源/PDF检查；提交一个可回滚 commit 和一份结论简短的 PASS/HOLD 记录。严重问题阻断下一阶段；必须让下一审稿者从“科学问题与验证”而不是 git chronology 评价稿件。

### N0 — 完整现版本证据/章节责任地图（P0，先于正文改写）
- 输入：main.tex、S1–S9、G0F/G5、原 Twitch 和原 KuaiLive P0/P1/P2、R0 12 条矩阵、R6–R8、已发表最近邻文献。
- 操作：建立当前全段落 thesis-function-evidence map、图表用途表、原始数据/统计等级和重复语句位置；对 9 表 2 图逐项注明“supporting RQ / supplementary candidate”。
- 输出：N0_CLAIM_PARAGRAPH_EVIDENCE_MAP.csv（含当前真实源码定位）、N0_STRUCTURAL_RISKS.md 和 immutable source ledger。
- PASS：重要定量值 100% 有来源、每段/主表均有明确功能、证据层级无混淆；更新 R0 12 问题不能先行宣称全关闭；本阶段不改正文。

### N1 — 核心论点与 KBS 创新定位的独立审稿关（P0）
- 先写一页 research-question / nearest-prior-work / answer / why-it-matters；逐项回应“只是 L2D”“与现有 knowledge gating 有何不同”“为何 candidate metric prior 不覆盖新发现”“在 Memory 更优更快时选择为何必要”。
- 预先决定两种合法论文定位：**方案 A（默认）**：evaluation + decision-quality，在限定 Memory-call 设计下报告 Utility 的比较收益；**方案 B（有独立新证据才能采用）**：真实服务资源受限的 routing 方法。无法证明真实资源代价时禁止选 B。
- 输出：中心一句、3 RQ/贡献/主要图表、old vs proposed narrative gap matrix、对近邻论文的客观比较。
- PASS：从 title/abstract/§1 到 §6/§7/§8 中每一核心动词都有相同的、可核对的结论；没有未验证的“首创”“系统加速”“SOTA 优胜”；完成新实验是否需要的科学决策（见 N2）。
- 只修改蓝图，不修改实验。

### N2 — 补充实验必要性/可行性决策关（P0 决策，默认不做新实验）
- 对四类审稿疑点逐项判定缺口：更强 designated Base 公平性；对既有 deferral/selection 的合适同条件对照；真正业务 external expert-call 成本及生产条件；候选依赖的独立/可识别性。
- 先利用已有 S3 强 Base 和 G4 真实 warmed path 证据，评估能否合理限定论文主张而无需再训模型。若保留 A 定位，原则上可先完成当前证据结构性改稿，成本/算法实验为条件性加分项。
- 若审稿前确需新实验：先写独立 protocol、资源预算、DEV 分析、预定义主指标和公平对照；申请合法的**新 holdout**，不得在 G5 已揭示 TEST 中微调阈值并冒充新确认；若只能重分析已有 TEST，标注 exploratory，绝不改写原 G5 的 preregistered inference。
- 输出：N2_EXPERIMENT_DECISION.md，逐项 KEEP CURRENT / DEV DIAGNOSTIC / NEW INDEPENDENT TEST / OUT OF SCOPE（带理由、风险降低路径）。
- PASS：不存在“文字解决经济性”的偷换；如需新增模型/实验有固定方案与独立确认条件；否则明确冻结现在所有主结果继续进入正文修订。

### N3 — 先重构 §6 的主证据展示（P0）
- 先处理 6.1→6.2→6.3 主线，再处理 6.4 DEV diagnostics，最后 6.5 cost；每小节按 “finding → pivotal evidence → scientific interpretation → necessary scope”。
- 主要新增“六拟合五 selector + actual calls”的对比解释；如制作区间图，只使用已接受的用户聚类 CI 数据。Always Memory 在主表和文本中保持显著可见，但以科学张力讨论。
- 把冗余的 P0/P1/P2、DEV 历史窗口结果分流补充材料，不删除已支持的解释链；避免把 S8 全量表复制回主文。
- 输出：§6 源码 diff、结果-图表说明矩阵、原聚合与格式小数逐字段核验表。
- PASS：不读 supplement 就能理解 C1/C3/C2 的证据身份和最强发现；无“DEV cap = TEST hard cap”；所有原数值、CI 及种子/队列标签不变；实验图表未裁切；没有因想改善叙事而将 exploratory 强称 confirmatory。

### N4 — §3–§5 方法统一和信息分层（P0）
- §3 仅保留 event NDCG、ΔM、条件期望与选择目标及 candidate-regime 概念；§4 仅讲 Base/Memory/Utility architecture 和透明 expert；§5 承担 **一次性** 方法变体/数据/统计身份。
- 同时精查 M3 真实 all-prior Short/Long history、TRAIN-known candidate 和 4,096×575 checkpoint screening、Twitch 14 vs M3 12 features、M3 inclusive tie vs 早期 DEV numerical tolerance、prequential observed past TEST；S1–S3/S7 留完整实现。
- 输出：§3–5 diff、main-vs-S1/S2/S3/S7 ownership map。
- PASS：数学含义没被“简化”删除；不重复讲同一方法边界超过必要次数；可复现性在主文+Supplement 联合阅读时完整；不产生 target leakage。

### N5 — §1–§2 的研究动机和近邻工作再组织（P0）
- 根据稳定结果写 Introduction：Base 已吸收历史→外部知识相对值可能冗余/互补→候选环境影响可用标签→预测相对价值改善条件使用→三证据身份。
- Related Work 不是竞品清单；组织 3 组以说明各先前论文解决了什么、本稿补充哪个“测量和冻结决策”问题。已有 L2D、知识门控、MemRec、GUIDER、sampled metrics 恰当归因，不应通过弱化前人成果夸大自身原创性。
- 输出：§1–2 diff、reference-to-claim matrix；必要时更新经过出版商核验的 citations。
- PASS：盲读者前 2–3 页能概述单一贡献与主要发现；每个贡献在后文可定位且没有 3 个并列不相干“创新”；不冗长预告整个实验经过。

### N6 — §7–§8 与 Abstract、title、Highlights 统一（P0）
- §7 重构为知识价值相对性、价值预测与不同专家选择信号、真实调用/部署张力三类解释，并独立处理外部效度；删去重复 §6 的表格读数与审计语气。
- §8 结论回应主要科学问题和 3 RQ，明确最重要的实证结论和何时适用；保留不容删去的 Memory 部署反例，但不用满段否定结束。
- 最后撰写新的 Abstract、3–5 条 Highlights 和检查题目/关键词，保证与 main figures and tables 一致；不把 G5 独立冻结证据写成跨平台迁移。
- 输出：§7–8 + frontmatter source diff、一页题目/摘要/贡献一致性审查。
- PASS：Discussion 每段新增结果以外的学术解释，不是“限制条目式罗列”；结论无需先读每张补充表仍可自足；摘要同时陈述重要正结果与反直觉 Memory 结果。

### N7 — 全文语体/重复清理、S1–S9 同步和投稿可读性（P1）
- 按最新源码重建重复限制/流程日志和重复背景的 location register，人工逐条删除、合并或归位；适当压缩 37 页主文但**不设置 KBS 未证实的页数上限**，版面缩短不是独立 PASS。
- 主文图表保留核心 2–3 信息层，完整训练 hash、全部 6×5 rates、18 CI/Holm、原 P2 draws 与 latency breakdown 保存在现有 combined S1–S9。修改补充材料只在明确主文引用改变/内容错误时必要，历史独立 S1... 文件不是可自动替代的最终合并稿。
- 禁止用简单关键词删除规则误删实际方法限制，重点人工评估 “not/only/retrospective/frozen/DEV/TEST” 重复句；保持 academic argument 而非 release notes。
- 输出：全篇 redundancy-and-location log、合并 supplement 对应表、图表清单。
- PASS：每一段均有科学用途；正文不包含 GitHub run IDs/提交验收日志；主文与 S1–S9 统计和表号吻合；关键负结果与版权/数据边界不被遮蔽。

### N8 — 独立 KBS 审稿模拟、实验记录和投稿级终验（P0）
- 三个独立视角：**编辑**（KBS fits, contribution clarity, abstract, novelty）；**方法审稿人**（Base quality, leakage, policy fairness, inferential family, Memory cost paradox）；**写作/可复现性审稿人**（概念、图表、主辅分配、引用、PDF、data release）。
- 逐项形成 Major/Minor objection、定位、可执行修复和证据来源，而不是泛泛 PASS。重大方法疑点未被证据解决时标注 HOLD 并回到 N2 或缩窄 claim。
- 全文四重验收：（i）每个 RQ 对应主结论和主图表；（ii）全部 12 条既有 R0 P0/P1 无复发，连同新论证问题的审查关闭；（iii）exact source LaTeX CI + main/S1–S9 PDF 逐页图表/引用检查；（iv）作者确认的署名、CRediT、funding、competing interests、生成式 AI 披露、数据代码可用性/权限、KBS 实际 Guide for Authors。
- 作者责任不可由系统代签；没有合法可存档文件/DOI 时不得写有；如果 KBS 实际门户对于 Highlights、匿名审稿、图像、摘要字数有特殊要求，使用最新 portal rules，不将 Elsevier 通则当作 KBS 专属规则。
- 输出：N8_KBS_INDEPENDENT_REFEREE_REPORT.md、claim-to-source_final_audit、source/build artifacts、submission checklist。**只在作者信息、授权和全稿科学审查完成后宣布 SUBMISSION READY。**

## VI. 必须跨阶段追踪的重大审稿风险

| ID | 问题 | 处理主阶段 | 验收/应对 |
|---|---|---|---|
| NV-01 / P0 | 与 L2D 和已发表知识门控的原创性差异仍不鲜明 | N1,N5,N8 | 解释“测量的排名相对专家价值 + candidate dependency + 双冻结决策证据”，不自称新通用定理；近邻文献逐项核验 |
| NV-02 / P0 | Always Memory 在 M3 更准且预热路径更快，约束的实际必要性未验证 | N1,N2,N3,N6,N8 | 保留反例；论文 A 定位时只讨论有约束下 decision-quality；如主张生产部署优势则 N2 必须提供新成本证据 |
| NV-03 / P0 | 全文断裂、Results 像实验记录、Discussion 复述 | N0,N3,N5,N6,N7 | 三 RQ 互相支撑；每节 discovery-first；减少防御性/版本过程重复而不删除科学限制 |
| NV-04 / P1 | M3 五规则没有同一实际 TEST 调用次数，主推理未覆盖 Uncertainty | N0,N3,N4,N8 | 清楚并列实际 calls/NDCG；可报告观测 quality–call 双优势；three Holm 仅 Base/Difficulty/Specialist；Uncertainty 为 secondary |
| NV-05 / P1 | Base 强度与成熟 deferral 竞品不够公平全面 | N1,N2,N5,N8 | 依据 S3 诚实缩窄 incumbent-relative claim；如需要跨方法 superiority，设计同数据/调参/资源公平、独立 holdout 对比 |
| NV-06 / P1 | RQ2 candidate reversal 与 sampled metrics 已知现象重合、不是单因子因果识别 | N1,N3,N5,N6 | 将其作为 fixed Memory ΔM 的排名环境依赖实例、2×2 描述而非新排名指标理论 |
| NV-07 / P1 | 部分数据和模型不能永久公开、Artifacts 到期 | N0,N7,N8 | 许可证/隐私核查，尽可能冻结可公开代码和聚合/manifest；持久 archive 需真实存在，不能猜 DOI |
| NV-08 / P1 | 统计家族、时序和三个排序单位的跨节一致性 | N0,N3,N4,N7,N8 | full-author M3 ≠ room KuaiLive，六模型 shared users；G5 标签揭示顺序不变；Twitch 14 vs M3 12 保持 |

## VII. 可复查的执行和变更控制

1. **不修改已冻结科学事实**：不能重新训练原 G5 主 Base、再调 G5 TEST 阈值、调整主假设/CI、重命名 TEST 数据含义、以有利样本取代完整六 fit；所有新研究独立记账。
2. **建立科学编辑分支或每阶段唯一串行 commit**：不并行互相覆盖 main.tex；每阶段保留 git blob SHA、修改范围、source diff、QA 记录；更新主稿前保证开发分支与仓库现状一致。
3. **断言驱动 QA**：统计数值/符号、事件数、图表标签与引用匹配、latexpdf 通过之外，另评估“RQ 在每章的回应”“每个图表是否必需”“近邻研究差异是否真实”“概念术语是否保持恒定”；可编译不等于学术叙事验收。
4. **改稿阶段不可伪造独立性**：如由同一助手审稿，应称内部 reviewer-style audit；外部同行评审只有真人独立评价才可这样表述。
5. **时间与硬预算**：不预设工作完成时间、不预设追加实验的运行资源和必胜率；任何新实验在 N2 做成本-收益、可用 holdout 与环境确认。
6. **Gate 标准**：每阶段以 PASS / PARTIAL / HOLD 结束，列已修改文件、实质性问题及其证据、未解决问题和下一阶段入口；允许 HOLD/回滚，防止“全部通过但全文仍散乱”。
7. **本文件只作为新 N 系列编辑路线图**。历史 R0–R8 的证据与验收报告原样保留，但其学术写作结论不构成本方案的免责条款。

## VIII. 作者和编辑的关键决策

- **默认允许先执行 N0、N1，而不要求追加实验**。N2 才判定是否需要高价值强 Base / 成熟 expert-routing 对照、真实成本约束或更严格独立 candidate sensitivity。
- 若最终仍只有现有 G5，再优先将稿件写成“知识价值条件性与约束下预测性分配”的实证和方法评估，而非通用 routing framework；目标是最大限度发挥真实证据的学术解释能力。
- 保留主论点问题导向的标题候选：现有 “When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation” 可继续作为基线；不要在主实验重构前为迎合热点改成无法验证的 agent architecture / efficiency 标题。
- Abstract、Highlights、作者声明在 N6/N8 修订结束后定稿；含实质性 AI 辅助的整理、写作与重构须按 [Elsevier 作者 AI 政策](https://www.elsevier.com/en-au/about/policies-and-standards/generative-ai-policies-for-journals)由作者审核和披露。通用 [Elsevier Highlights 要求](https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript)为 3–5 条、每条不超过 85 字符，但 KBS 是否要求须以期刊官方 Guide 为准。

## IX. 公开出版源核验与对照研究（2026-10-13）

- KBS 官方目标与范围：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
- Xie et al., 2026, KBS MHGFCL, DOI 10.1016/j.knosys.2026.115673；https://www.sciencedirect.com/science/article/pii/S0950705126004132
- Kim et al., 2026, KBS KAPER, DOI 10.1016/j.knosys.2026.116236；https://www.sciencedirect.com/science/article/pii/S0950705126009627
- Yerragunta et al., 2026, KBS incomplete-KB conditional gating, DOI 10.1016/j.knosys.2026.116167
- Mozannar & Sontag, 2020, Consistent Estimators for Learning to Defer to an Expert；https://proceedings.mlr.press/v119/mozannar20b.html
- Narasimhan et al., 2022, Post-Hoc Estimators for Learning to Defer to an Expert；https://research.google/pubs/post-hoc-estimators-for-learning-to-defer-to-an-expert/
- Krichene & Rendle, 2020, On Sampled Metrics for Item Recommendation；https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Elsevier current journal author AI policies：https://www.elsevier.com/en-au/about/policies-and-standards/generative-ai-policies-for-journals
- KBS Guide for Authors（自动访问可能有 403）：https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors

**本计划总裁决：继续修订值得，但真正 P0 是 N0–N1 统一论点、N3 发现优先的 Results 和 N6 知识科学含义的 Discussion；不是先再做一轮机械 proofread，也不是预设全部新增实验。**
