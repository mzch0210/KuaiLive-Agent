# N12 | KBS 单一主线与全文结构重构执行方案

日期：2026-10-14。执行起点：N11已验证39页主文、45页补充材料；N11 Draft PR #5。状态：**PLAN ONLY**。本分支只存储计划，不修改主稿、补充材料、模型与任何冻结实验输出。

## A. 中心科学命题与实验归属

唯一中心命题：**一个已确定的显式viewer–creator关系知识源，其增量排名价值由既有Base、可用候选环境与历史证据共同界定；这种条件性价值能通过预结果特征被估计，改善有明确调用约束的知识选择，而固定候选下的真实历史对照提供来源有效性证据。**

RQ1（知识价值的定义和条件性）：固定Memory相对于不同Base的互补价值何时出现，候选环境变化如何影响效用标签？主证据Twitch历史互补性、原KuaiLive配对10,222房间事件full-vs-sampled反转；多任务仅做互补而非严格跨数据集因果对照。

RQ2（估值监督能否影响选择）：Full-F候选一致的相对效用监督与实际选择决策是否一致且有后果？主证据原M3冻结47,575 TEST、两类Base三次拟合、B4-A同期间额外30,000目标H1；DEV F/S转移结果作为解释性佐证。不能称严格等调用：SAS F/S 8,704/9,105、GRU 8,629/9,168，差距超过预先规定的1个百分点。

RQ3（知识源有效性）：保持Full-F候选及Memory scorer不变，真实历史关系排列是否优于遵守时间与小时作者活动约束的Null？主证据B4-A嵌套4,096个额外目标H2 +0.031145，CI [0.027389,0.035098]，Holm p 0.000600；B2 1,024 DEV控制为支撑性实验。不能声称孤立某一关系变量因果性；原B4-A同队列TRAIN-only popularity非退化门槛在A4前**NOT VERIFIED**。

系统成本是应用边界而不是第四个独立科学贡献。Always Memory新目标加权F NDCG 0.348744 > SAS/GRU选择0.305446/0.304530；原G3/E2点式Utility在matched DEV timing 1.769ms > Always Memory 0.692ms。现有实验只证明外生Memory调用约束下的选择质量，不证明部署经济效益或净运行速度更优。

**逻辑布局**：定义固定知识增量价值（RQ1）→检验其候选对齐监督和选择后果（RQ2）。RQ3为RQ1知识来源提供**并行有效性检验**，不是RQ2在时间上的因果后果。原Intro P1→P2→P3连续箭头应改变成分支架构，不暗示已验证因果中介。

## B. 新七节投稿论文目录与职责

1. **Introduction**：问题背景→知识使用价值的具体研究缺口→Base/candidate条件性→研究方法概述→RQ1-3与三项关联贡献。正式提及数据集仅说明协议角色，不在此罗列历史阶段。
2. **Related Work**：2.1显式知识与Memory留存、表示及融合（SAMD、MHGFCL）；2.2基于效用的专家选择（learning-to-defer、DS-Frame）；2.3候选敏感评价和直播推荐（sampled metrics）。最后统一归纳价值定义和决策研究的差距；不在每段重复“we do not invent...”
3. **Knowledge Valuation and Selective Use**：融合原Problem Formulation和Base-Relative Framework。3.1 ranking unit与decision context；3.2 fixed trained Base及Short/Long/Pop 0.45/0.45/0.10 Memory；3.3 event gain Δ和conditional η；3.4 candidate-aligned S/F supervision和pretarget features；3.5 frozen invocation-capped selection。Target-dependent evidence state及回顾性分解只保留必要诊断定义，复杂展开迁Supplement。
4. **Experimental Design**：开篇一张任务/证据等级表。Twitch streamer frozen TEST、KuaiLive room matched retrospective paired诊断、M3 author initial global-time TEST、额外same-period 30k及nested 4096预结果锁定、DEV探索与设备延迟独立分级；固定模型比较、公平信息、训练DEV OOF、统计估计量、20-cell权重、用户聚类CI和3个预登记Holm检验分开陈述。详细seed/hardware/互换哈希下沉Supplement，但主稿仍须能独立理解每个结果。
5. **Results**：5.1 RQ1 historical complementarity and candidate-regime dependence（Twitch+原KuaiLive）；5.2 RQ2 candidate-aligned valuation improves knowledge-use selection（原M3 + 30k H1，DEV为解释）；5.3 RQ3 authentic source validity at fixed F candidates（4,096 H2主表，B2为探索）；5.4 Invocation and operating boundary（Always Memory准确率及设备实测成本）。各节采用research question→fixed comparison→primary outcome→interpretation→next question桥接，不按实验计划执行次序组织。
6. **Discussion**：6.1固定显式知识源在下游的相对决策价值；6.2候选环境是效用定义和监督条件的一部分；6.3来源有效性、采样/时间外推与有真实调用上限时的系统应用。限制在此集中解释，而不是每段自我否定；与SAMD/MHGFCL/DS-Frame的研究对象边界继续清楚。
7. **Conclusion**：正面总结中心发现和知识系统启示，并适当界定落地前仍需验证的条件，不重复整张实验年表，也不以“not a generic routing algorithm”收尾。

## C. 主文13张现有表格的迁移准则

现状：Experimental Setup有2张，Experimental Results有11张，形成过多并列叙事。本轮目标是约6–8张有独立论证作用的主文表，而不是规定页数硬上限；任何被移动的结果必须可由正文指向Supplement。

| N11 table label | N12处理 | 原因 |
| --- | --- | --- |
| tab:exp-datasets | 主文改成证据层级表 | 建立三平台和M3三种证据身份 |
| tab:exp-methods | 移Supplement；正文比较方法简述 | 避免与Method重复 |
| tab:results-evidence-states | 压缩为主文代表数据/图，详细表移Supplement | Twitch后验历史切片非主验证 |
| tab:results-factorial | 主文RQ1 | 候选集反转及因子差异核心 |
| tab:results-m3-dev-regime-transfer | 明确DEV性质后移Supplement | 不能与冻结H1同级 |
| tab:results-twitch-policy | 视版面用主文精简对照或移详表Supplement | 保留独立Twitch TEST贡献 |
| tab:results-m3-policy | 主文RQ2 | 原始M3冻结核心决策对照 |
| tab:results-m3-robustness | 主文简表，详细逐fit Supplement | 两类Base三seed非常重要 |
| tab:results-m3-b4a-supervision | 主文RQ2完整保留 | 30k H1加权效应、95% CI、真实F/S调用 |
| tab:results-m3-dev-source | 移Supplement | Short/Long/Pop组成解释性DEV实验 |
| tab:results-m3-additional-relation-identity | 主文RQ3完整保留 | 4096真实历史Null核心和Popularity验收边界 |
| tab:results-feature-ablation | 移Supplement | Twitch DEV特征解释、保留可访问性边界 |
| tab:results-n10-cost | 主文保留准确数字的小表或句子，完整表Supplement | 反证不可隐藏，但不是主贡献 |

主图建议“一个中心知识价值对象、预结果使用选择与旁路来源检验”的概念图，及一个“真实推理过程/离线监督信息隔离”的框架图。避免旧P1→P2→P3箭头错误呈现为直接因果中介。原Twitch状态图是否留主文依其支持RQ1的独立价值决定。

## D. 文字改写与重复控制的不可突破门槛

- 核心结论必须有“研究问题→固定比较→数值证据→合理解释”结构，避免表述像历史阶段报告。
- Abstract应以科学问题、方法对象、关键实证、可转移的知识系统见解为主；不用以否定自我贡献结束。
- “Our study does not require a new generic deferral theorem” 改成积极说明与已有deferral的关系并指出新增的知识价值操作化和实验后果。
- “same-period, not a future test, unverified floor, not cost saving”全部需要保留，但是定义于Experimental Design、在对应Results醒目报告一次、Discussion集中解释其科学边界；不在Intro/Related Work/Conclusion循环辩解。
- 不能将False candidate regime标签误写为真实线上可见的目标；目标相关历史状态为后验解释，DEV S采样特定目标保留用于监督构造，线上推断使用pretarget features。
- 严格区分原M3 Utility gate、DEV S/F gate及新冻结30k F-aligned gate，防止错称同一种执行实现。256DEV计时为原点wise Utility，不是新的B4-A vectorized F-aligned。
- 不依赖自创“突破性”“首个”“最优”措辞。KBS官方重视原创、知识系统和决策支持，与本文关系在于具体知识估值研究而非声称新门控算子。

## E. 实施阶段与每阶段必要交付

**N12-0：基线事实锁定与全段落映射（P0）**：冻结N11 LaTeX、最终39p/45p和A4/A5已发布SHA；制作每段/公式/表格→新章节/补充位置矩阵，列出保留、精简、合并、移入Supplement、删除的具体理由。验收：之前10项科学修改都能追踪到新主稿落点和补充位置，零A4重开。

**N12-1：论文论证蓝图（P0）**：完成三个RQ的命题/数学定义/主要对照/实证结论/审稿界限矩阵，修正概念图的P3旁路位置，冻结主图表预算。验收：只看标题、摘要草稿和Intro末尾即可说出一个中心命题，任何RQ无重复功能。

**N12-2：Introduction与Related Work（P0）**：重写背景→研究缺口→核心问题→贡献，并按三文献谱系解释已有工作；只保留可核查的新颖性。验收：无重复自我辩驳/过度否定；近邻真实DOI一致。

**N12-3：方法合并（P0）**：将旧第3/4章去重并统一Δ、η、Z、S/F、门控和Short/Long/Pop定义；保留预目标可见性和训练信息边界。验收：无双重定义、无在线target leakage、无模型换名混淆；数学公式和技术对象可以直接映射到实验。

**N12-4：Experimental Design重构（P0）**：首先组织证据等级，其次训练/冻结/候选/估计量/统计；独立写清全新target ID与新时间段的区别；保留20-cell权重和三假设Holm。验收：读者无需Supplement就能区分哪个是DEV探索、哪个原TEST、哪个同期间额外目标、哪个系统诊断。

**N12-5：Results按RQ重组（P0）**：把各数据集拆到应支持的研究问题，主表优先让原M3 TEST、30k H1、4096 H2可见，移DEV细表且真实重建Supplement引用。验收：每节结尾明确回答本RQ，段间通过明确科学逻辑自然过渡；源数字完全锁定。

**N12-6：Discussion、Conclusion、Abstract统一（P1）**：在Results完全稳定后重新书写，做到正面、证据支持的学术表达，科学边界集中不分散。验收：三处表达同一核心贡献；所有成本反证和未验证验收仍在适当位置；无堆砌式实验清单。

**N12-7：Supplement与自动一致性（P0）**：被迁移的正文表必须进入补充；S10.15–18先保持不变，必要的新Supplement节仅为确实需要新增的证据导航，不重跑统计。更新N11 CI中强制8节/5结果子节硬编码为新7节/4结果小节，同时**保留或加强**10项claim coverage、模型身份、冻结SHA、指标与引用检查。双PDF编译、查溢出/孤页/表格/交叉引用、正确正文图表指标。验收：文献引用和label全部解析，所有科学结果一字不丢，篇幅紧凑但不按虚构KBS页数上限删证据。

**N12-8：KBS编辑式三角评阅与投稿门槛（P0）**：编辑检验主题的重要性和一致性，方法审稿检验封存与评价独立性、Null和call-budget边界，系统审稿核验Always Memory反证/运行成本的适用条件。每个Major comment指出正文可答位置，不再写项目内部语言。最后作者本人确认署名、CRediT、AI辅助研究与写作披露、数据使用与共享权、COI/funding、现行KBS投稿要求及cover letter。科研质量验收≠自动投稿批准。

## F. 不允许的捷径和停止规则

- 不跑新TEST、不开A4、不调门控阈值、Null seed或H1/H2原样本；不将后揭盲检查追溯称为已完成预登记。
- 所有H1/H2原冻结值和CI/Holm、原M3结果、负面Always Memory成本/精度都必须保持；任何移表/合章丢一个结果就回退该章节到前一稳定提交。
- 无官方依据时不声称KBS的强制页数、摘要字数或特定结构；减少篇幅是改善阅读效率的副产物，不是科研目标。
- 不因避免“负面语气”而删除实际不利的学术事实；仅将科学边界移到它们真正解释的实验和讨论位置。
- 必须先通过N12-0/1映射，才能开始N12-2及之后的逐章重写。各阶段独立Git提交、完整Diff及主张证据审计，N11分支保持原样，所有PR保持Draft直至责任作者审阅。

## G. 来源与复审接口

- KBS官方范围：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
- Zhong et al. SAMD (KBS 2026)：https://www.sciencedirect.com/science/article/pii/S0950705126002388
- Xie et al. MHGFCL (KBS 2026)：https://www.sciencedirect.com/science/article/abs/pii/S0950705126004132
- 当前N11审计：manuscript/kbs_latex/N11_FINAL_KBS_EDITORIAL_LANDING_AND_COHERENCE_AUDIT_2026-10-14.md
- 当前N10 C0–C6状态：manuscript/kbs_latex/N10_ROUTE_C_CURRENT_EXECUTION_STATUS_2026-10-14.json
