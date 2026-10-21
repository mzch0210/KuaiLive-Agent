# N12-C6–C8 | Scientific Contribution, Evidence Integrity and KBS Review-Gate Amendment

日期：2026-10-19。类别：**N12 后续执行方案修订／计划文件，不是论文改稿、实验或审稿通过证明**。优先级：此文件对原 `N12_SINGLE_THESIS_KBS_MANUSCRIPT_RESTRUCTURE_PLAN_2026-10-14.md` 的 **C6–C8执行要求、验收/停止条件**具有优先效力；C0–C5已完成的事实、冻结结果和工程历史不变。本修订不得倒填为2026-10-14当时已作出的设计决策。

## 0. 真实起点、执行范围与不可更改的事实

- 工作分支 `kbs-n12-single-thesis-restructure-plan-20261014`、Draft PR #6，基线 HEAD `c09528d2ee46954291ab1e6362ce7ea098f63cd1`；PR 对照冻结 N11，而不是默认 `main`。原 N12-C0–C5 **PASS**、C6 **NEXT_NOT_STARTED**、C7/C8 **NOT_STARTED**。本次只修订方案，不变更这些执行状态；PR不得因此改为Ready或合并。
- 最后验证为 C5 Actions #38864362019：主文 **36页**、Supplement **47页**，两个PDF作业成功；七节投稿结构已确立；C6待改的 **Abstract、Discussion、Conclusion 仍为 N11 叙述版本**。主文现有 Results 为 RQ1、RQ2、RQ3、operational conditions 四部分；方法定义和9个原始公式、Experimental Design的2个原始公式、7个主文 Results 表和4个已迁往Supplement S10.19的 Results 表不得静默改算或丢失。
- 当前观察性研究以事件级 **NDCG@10** 为排名效用；不是干预性线上用户效用。Twitch streamer-ranking、KuaiLive room-ranking、M3 author-ranking的rank unit及人群不同，不得当成三次同质的独立复现。
- 30,000个额外M3 target IDs仅与原TEST已评价的事件ID分离，来自2026-03-27至2026-03-31 **同一采集期**，并非新时间窗口、user-disjoint或history-disjoint；nested 4,096含于30,000，不是额外独立样本。
- 本修订禁止对原A4/B4-A TEST窥视、改阈值、另择种子、重新计算冻结p/CI及结果；任何新增DEV分析应标识为**事后探索性**，绝不能追溯宣称预注册或外部验证。

## 1. 主贡献重新聚焦：要证明什么、不证明什么

### 1.1 唯一主线（主张的强弱阶梯）

> 对固定历史关系知识源M、既有基础排名器B和实际可用候选环境F，知识的下游增量价值定义为同一候选集合上Memory与Base事件级排名效用之差。**候选抽样改变了这一价值的离线监督目标，因而可能改变预结果知识调用策略及其最终F排名决策**；对真实历史源的固定候选Null检验提供独立的知识来源有效性证据。

主要科学落点为 **RQ2: candidate-aligned knowledge-value supervision and its downstream decision consequence**。RQ1揭示何以需要候选条件化价值标签；RQ3平行评价真实关系排列的信息含量，**不能写成RQ2通过RQ3的因果中介**。系统调用额度仅是应用条件，不能伪装成已证实部署节约。

- **已证实的经验层**：固定S/F训练方案在一组冻结、同期间额外M3目标上具有不同的最终F选择表现。SASRec F−S +0.005391（95% CI [0.003646,0.007174]，Holm p 0.000600），GRU4Rec +0.003585（[0.001599,0.005576]，Holm p 0.000800）。
- **较弱的解释层**：S/F标签目标不同，既有DEV诊断观察到约21–23%的选择转移及被替换请求的增量收益差异；这是提示监督—决策链条的探索性证据，不能直接证明每个错误调用都由候选监督单一因素造成。
- **暂不允许的因果层**：S/F调用数不相等（SAS 8,704/9,105，相差1.337个百分点；GRU 8,629/9,168，相差1.797个百分点，均超过旧1个百分点容忍），所以现有H1不能宣称**严格相同调用预算下的孤立标签效应**。对于原始冻结方案，可称“完整冻结策略的总体表现差异”，而不是“控制所有资源后的纯因果增益”。
- **并行的知识源证据**：nested 4,096真实历史F NDCG@10 0.334942 vs 三Null per-event mean 0.303797，差+0.031145（CI [0.027389,0.035098]，Holm p 0.000600）。约76.8%历史边重排同时改变重复配对及高阶结构，**不可孤立宣称特定语义关系机制**；三个seed共用同一样本。原B4-A同队列TRAIN-only Popularity prereveal nondegeneracy floor **NOT VERIFIED**，未按原验收条件事前满足，缺口不能由DEV floor或事后检查修复。
- **重要反证**：30k Always Memory加权F NDCG@10 0.348744 > 测试的F选择策略；原旧pointwise Utility在256 DEV×3的3090计时约1.769 ms > Always Memory约0.692 ms。该计时不是新B4-A vectorized F gate；不能称新gate已证实更慢，也不能从调用次数少推导总耗时、预算、能源或实际收益。

### 1.2 必须区分的三个层次

1. **定义/操作化**：`Δ_M(x;B,C)=u_10(M,x;C)-u_10(B,x;C)` 与 `η_r(z)=E[Δ_M(X)|Z=z,R=r]` 对现有相对损失、信息价值及learning-to-defer已有先例而言，不是自动成立的新理论/新算法。
2. **目标错配及实证结果**：sampled metric ranking inconsistency早已被研究；N12新增的可防守主张是**把候选对比从测量排名器推进到监督外部知识价值，再观察冻结选择策略在完整候选环境下的决策后果**。这是具体实证增量，不宣称首次发现采样指标失真或首次实现动态路由。
3. **机制/推广**：当前支持同协议内的综合关联与固定策略比较；未孤立识别“只替换监督标签，在严格等调用条件下”的完整机制，也未证实未来时间外推、线上干预效果或部署成本收益。论文强度必须随证据停止。

### 1.3 KBS创新性对照矩阵（编辑/方法评审必须逐行回答）

| 近邻工作 | 已覆盖的贡献 | N12可防守的差异 | 对应主文要求 |
| --- | --- | --- | --- |
| Krichene & Rendle, KDD 2020 | sampled-ranking指标不保证原模型优劣排序 | 在固定Base–Memory关系源上考察 **效用监督标签** 的错配及后续F实际选择 | Introduction缺口+RQ1→RQ2桥+Discussion明确“非重新发现不一致” |
| Mao, Mohri & Zhong, ICML 2024（及相关learning-to-defer） | 预训练预测器对专家委托、损失与成本条件化选择 | 不声称新的委托理论；研究特定候选环境的 **离线标签目标是否适用于知识使用决策** | Related Work+Method按问题对象说明，不将阈值/η称新算子 |
| Yuan et al., DS-Frame, arXiv 2026 | 推荐领域的fast/slow选择器及预算动态推理 | 不宣称首创预算门控、效率胜利；研究可审计的固定外部历史源与全候选监督 | 与Always Memory、实际设备计时并列解释 |
| Zhong et al., SAMD, KBS 2026 | 决定哪些个人记忆应保留以利下游 | N12不研究记忆写入/留存，而检验已固定来源在当前决策中的 **边际使用价值** | Related Work对比保留 vs 使用；定义知识来源 |
| Xie et al., MHGFCL, KBS 2026 | 新知识图多视图表示与门控融合 | N12不宣称新知识编码；其固定Short/Long/Pop历史证据使下游使用价值可审计 | Methods精确定义，可重复来源属性 |
| Yerragunta et al., KBS 2026 | 改善知识来源与动态门控的受控分析及交互 | N12的RQ3是并行来源验证，不是source×gate完整因果交互实验；缺的交互不可隐去 | Discussion列为待检验，禁止把两支相加当成因果链 |

**审稿性反诘**：如果删除“首次”“新算法”及“省成本”的表述，论文是否仍可以明确回答“候选评价不一致如何改变 knowledge-use supervision 和选择”的新问题？如果只剩“训练与测试应一致”的常识句，必须降级贡献表述，或单独启动下一阶段独立证据评估，不得靠润色过关。

## 2. RQ1–RQ3 的主张—证据—界限与防守接口

| 研究轴 | 有效的主声明 | 必须保留的反解释与不利证据 | 失败判据 |
| --- | --- | --- | --- |
| RQ1 / value context | 已确定的Memory对Base相对价值随历史环境和候选竞争集合变化；原KuaiLive 10,222配对room事件S -0.04120与F +0.04631、位移+0.08751 | F/S同时改变候选身份、数量与排序竞争，不能称候选数单独因果效应；Twitch事后可恢复分层不能成为可部署状态 | 用sampled inversion宣称新的排名采样理论 |
| RQ2 / primary decision contribution | DEV预目标特征的F-aligned label可用来训练冻结政策；在30k M3额外同期间目标上F策略总体F排名效用优于S策略 | 门控版本不可混、call-count差距超容忍、H1冻结表、20-cell加权/用户聚类/多重检验、非未来外部验证；Always Memory较高准确率 | 写成strict equal-call、online causal、future external验证或部署最优 |
| RQ3 / independent source validity | 当下候选和评分函数固定，真实历史排列优于closed-hour活动约束Null | 4096嵌套、三seed非独立、历史重排是composite、原prereveal floor未验证；DEV 1024只能作为探索 | 宣称孤立语义因果机制或补签原验收PASS |
| Operating boundary | 仅在 **外生的Memory调用约束** 存在时评价有限调用下的选择质量 | 无实测配额稀缺性；Always Memory精度高，旧Utility实测更慢；新F gate尚未作等工作量计时 | 把较少调用直接写成成本节省 |

## 3. C6——先科学论证、再改摘要/讨论/结论（强制P0门槛）

**状态**：NOT STARTED，原方案C6的“语言与统一叙事润色”升级为“**novelty-to-evidence gate + 文本修订 + 专用QA**”。不得由本文档产生虚假的C6完成状态。

### C6.0：科学贡献防守审查（须先完成再写稿）

- 建立`N12_C6_CLAIM_EVIDENCE_PRIOR_ART_STRESS_TEST_*.md`，逐项包含 claim 原文、对手能引用的最近邻研究及具体差异、冻结主证据与表/节位置、竞争性解释、不能声称的边界、编辑裁决（KEEP / NARROW / REMOVE / NEED NEW INDEPENDENT EVIDENCE）。
- 主张层次必须明确：**primary RQ2**，RQ1概念与配对证据支持，RQ3平行验证来源。每个Introduction贡献bullet在Results至少有一个具体定量证据；每个强解释在Discussion有对应限制；不得用H2替代H1机制识别。
- 固定策略`F vs S`是**策略整体比较**，不是固定调用下的纯标签因果效应。若不能证明等调用与旧1pp阈值，必须修改claim，不得对揭盲30k目标调整阈值使其追认合格。
- 对H2 `NOT VERIFIED` 的原pre-reveal floor，在主文明确其对预定nondegeneracy验收造成的缺口；检验是否需要降低“establish/causal”措辞。不得称H2通过全部预设控制。
- 文献来源审查：KDD sampled metric、ICML 2024 deferral、arXiv 2026 DS-Frame、KBS SAMD/MHGFCL/动态知识门控各自核查题名、版本、论文对象、可辩护差异、DOI/BibTeX或arXiv版本；不得为了凑创新点错误描述已有工作。

**C6.0 EXIT**：每条科学创新点能填完“近邻先例—本文新对象—实证结果—剩余替代解释”四列；若主要主张仅是“训练候选=评价候选更好”的一般常识，无足够决策级证据，记录**P0 NOVELTY GATE FAIL**，必须窄化稿件定位或转入经责任作者批准的新独立验证决策，不得直接把C6判PASS。

### C6.1：候选标签→价值预测→选择后果的论证链（优先利用已完成证据）

- 按相同估计对象区分`Δ_S/Δ_F`（目标标签差异）、相同信息合同`Z`与冻结预测器、`π_S/π_F`（政策）、最终F效用。明示S采样中事后保留目标只发生于**训练标签生成**，绝不是线上可见信息。
- 只从已冻结文字/DEV既有报告中审查约21–23%的转移和请求收益方向；核查样本、单位和是否按Base分列；**不新计算30k TEST上未报告的决策分歧**。可绘制一张概念性的、有数据出处的“监督目标偏移—policy差异—决策损失”证据表，不因合并表而捏造同一样本上的中介。
- 必须写清`F/S政策调用额度不等`这一竞争性解释；若新敏感性分析获批，**仅用DEV、标探索、先写analysis contract**；公平质量–调用前沿不是可从当前H1直接冒认的已验证事实。
- B2源组成DEV结果（Full/Long/Short/Popularity）如使用，仅描述非单调/带混杂的交互迹象和支持程度，不得声称有严格`knowledge source × supervisor` factorial identified causal interaction。
- RQ3用来回答`知识是否真的含有历史信息`，不强行连接为“source authenticity导致F监督优于S监督”。

### C6.2：写作与论文叙事修订

- **Abstract**：问题（candidate-dependent marginal knowledge value）→明确固定B/M及决策前监督对象→**主结果30k F/S**（给SAS/GRU数值、样本属性）→RQ1候选反转、RQ3历史Null作为支持→最后给正面但严格边界的知识系统见解。不可把六组阶段流水账当摘要；不强制虚构期刊字数限制。
- **Discussion**：建议三组逻辑角色：①相对价值属于`(source, incumbent, candidate regime)`并与现有委托算法/样本指标的区别；②采样候选监督目标的“指标偏差→政策误用”经验链及其边界，承认non-equal calls；③固定候选历史有效性、composite null、非验收floor、跨时间与离线曝光局限、外生配额与Always Memory不利精度/延迟。可调整小标题，但不增加不被证据支持的新节。
- **Conclusion**：一条可迁移的评价纪律：先固定知识来源、既有Base及真实候选，再用实际决策目标构建离线收益监督并检验policy与source；不宣称新defer定理、实测节约或外部未来窗口推广。不以大量“我们没有做……”收尾。
- **Highlights.txt / title / keywords / figure captions / Intro contribution bullets**：做全稿一致性扫描；必要时提出候选修改，在C6合并前连同源证据审计完成。Title可保留但须对应新的主要贡献；不得无理由改变冻结科研对象。
- 保留且显著准确表达：H1/H2数值、H2原floor未验证、B4-A同期间、call差、三个Null同队列、系统不利基线；正面写作不等于隐藏缺点。
- 若C6发现C2/Related Work引述不足，**允许受控的极小补引/解释编辑**，先记录变更范围和原有证据引用；不能因“C6只改三节”让必要的先例对照永久缺席。

### C6.3：CI与源追溯升级（阻断点，不能略过）

现存`analysis/kbs_plan_c/n12_c5_rq_results_evidence_audit.py`是 **C5阶段专用**：它以`main[:Results]`及`main[Discussion:]`整段FNV32与冻结fixture对比，恰好包括C6必须编辑的Abstract和Discussion/Conclusion。**直接复用必然出现误报失败**。在C6改文稿时必须：

1. 将旧C5 workflow/审计明确标成archival/stage-complete，保留其最后成功run与审计fixture作为历史证据；不要简单删除或绕过所有科学检查。
2. 引入`n12_c6_...scientific_contract.py`及新的C6双PDF workflow（名称可依repo风格），改为**按段落角色的允许变更清单**（frontmatter/Discussion/Conclusion/必要小范围Intro与bib），冻结原9+2数学公式、Sections 3–5的模型身份/比较/原始表格和所有已封存H1/H2核心值；检查latex labels、引用、章节结构、Supp指向、图表与统计人群。
3. 对历史源合同做源hash或语义字段比对，而不是使`Discussion`原字节不变；source contract还须验证负面Accuracy/Timing和H2未验收floor持续存在。若修改了旧C5脚本本体，也须保留可追溯的历史版本/CI报告，避免“通过”含义被改写。
4. 双PDF新构建、排版文字检索+视觉检查：abstract/Discussion/Conclusion准确出现在稿中，交叉引用无缺失/latex overfull，无悬挂表题。任何新增表/公式必须有出处、研究层级声明与源对照。
5. 不因C6 doc-only计划变更就误报论文已经执行新的C6 CI；C5最后成功PDF不可误称最终投稿版。

**C6 EXIT**：C6.0创新贡献审查明确PASS或如实报告风险，C6.1解释链成文，Abstract/Intro/Discussion/Conclusion/Highlights中心一致，新C6 SCIENCE QA + MAIN/SUPP PDF验证通过，独立评审能从文字区分“新贡献”与“旧方法”；否则保持C6 IN_PROGRESS/BLOCKED，不向C7伪推进。

## 4. C7——整稿科学闭环、补充材料和可复现审计（P0）

### C7.0 证据逐项对账（比原C5数字存在性检查更强）

- 做`claim→section/table/cell→population→candidate regime→estimator/uncertainty→frozen source artifact`的双向总账，主文所有定量声明都能反查源；对N11原Results 11张表逐个建立映射。
- C5现有源审计针对4张迁往Supplement的Markdown表，主要检查**标题存在和选定数值字符串存在**，不是每一格精确相等。C7新增全行/全单元格规范化匹配，区分rounding、百分号、小数与Markdown/LaTeX排版，冲突应报告，不可静默选择更好数字。
- 主文7张保留Results表仍应与原LaTeX完整块/冻结manifest对应；公式9+2严格追溯；引用必须指向实际的S10.13–16及S1–S10.19存在位置，无未引用的主张或孤表。图的标签/图例/对象在PDF中真实可读。

### C7.1 方法严谨性与复现边界

- 证据角色锁定：Twitch 44,221 streamer original TEST；KuaiLive 10,222 paired room retrospective；M3 original 47,575 author TEST/12,533 users and six **共享同一TEST的拟合**；30,000 same-period targets/10,387 users、4,096 nested/3,059 users；DEV only exploratory及256 DEV硬件计时；每一个出现的数值都写明所属层级。
- 复核20-cell weighted estimand、用户聚类CI、Holm检验家族与比较条数；保留S/F超出1pp、Original−Null composite、H2缺失original prereveal floor、Always Memory最优无约束精度、计时对象不是B4-A。任何数量或p值的错误需回看冻结artifact并留audit trail，不得“按文稿期望”再调统计。
- 记录可公开的执行命令、代码commit、环境、公开数据URL、训练/测试划分、模型权重与权限、seed、哈希、结果清单；无法公开的原始M3/日志/模型须分清`publicly reproducible`、`procedurally auditable but private data`、`not independently reproducible`。不可简单宣称所有结果都能由仓库公开从头复制。
- 校验相关数据集原始许可及用户隐私（如KuaiLive不同镜像/子集许可可能不一致）；不假定对所有派生物都有再分发授权。
- 明确单正反馈的离线NDCG、历史曝光偏差/无在线A/B、外推时间段不足、rank unit变化、用户重叠、数据集权益。若需要新增真实future-period/equal-cost生产研究，应走新的预先冻结协议且需责任作者同意，**不得把结果补进原B4-A既定H1/H2的预注册证据**。

### C7.2 版本与CI留档

- 新C7 workflow贯通main+supp PDF、BibTeX/引用、统一source-cells审计、PDF图表可读和对应摘要/Highlights，停用过时的C5 exact prefix/suffix contract。
- 封存C5最终36p/47p artifact ID及SHA；新C6、C7的PDF要各自给出新run、哈希和页数，不继承C5的PASS徽记。GitHub Actions工件如有过期风险，维护可长期核对的manifest/代码hash；不要公开受限制的原始数据。
- 与未更新的root README、历史报告、`N8_AUTHOR_SIGNOFF...`区分“历史里程碑”与“当前投稿口径”，仅在允许范围维护面向读者的最新入口；不能改写历史报告制造已批准状态。

**C7 EXIT**：全部冻结主要结果双向追溯通过、迁移表cell级准确、双PDF+公式/引文/图表QA、可复现性分级与许可数据审计完成、所有P0科学限制在主文适当位置可查，缺一不可。

## 5. C8——独立编辑/审稿挑战与作者最终决定（P0）

独立写出3份**不能预设好评**的referee memo及`major comment→evidence→manuscript location→resolution`的响应矩阵：

1. **KBS副编辑视角**：研究到底新在哪里？为什么不仅是Krichene采样指标+已有learning-to-defer的组合？固定Short/Long/Pop能否归类可审计的外部历史关系知识源？研究对知识系统设计留下了什么可验证的普适认识？若只是领域案例，是否显著不足以匹配KBS原创贡献？
2. **方法/统计审稿视角**：差异效应、实际调用差距>1pp、源/分层权重、同一期间/用户/历史共享、RQs是否正确平行、Null composite与Popularity floor未验收、离线单正反馈、校准/target-blind、TEST封存是否可独立验证；不得以漂亮置信区间掩盖识别薄弱。
3. **知识系统与部署审稿视角**：Memory独立准确率更优、旧Utility更慢、是否存在现实外生调用限制、真实知识与普通交互频次有什么区别、R3对R2是否真有解释作用、跨平台rank unit差异是否妨碍外推；不承诺未经测量的系统优势。

**三类决策**（逐条记录证据与行动）：
- `ACCEPT_WITH_BOUNDED_CLAIMS`：当前冻结证据足以支撑**有限的实证方法学贡献**，负面与局限如实保留，允许作者考虑投稿。
- `NARROW_OR_REFRAME`：相较prior art的新颖性、RQ3预验收缺口或等调用混杂不足以支撑强主张；收缩abstract/intro/discussion而非编造解决。
- `NEW_EVIDENCE_REQUIRED`：只有更强的独立新时间窗、严格预设固定调用/真实外生限制或源×监督交互实验才能支撑所期望的强科学/应用主张。**新实验另立预先设计+新独立数据预算，不得解封旧TEST做追认**。

最终主稿前置作者签署审批门槛：
- Author名单与顺序/CRediT、匿名投稿口径、Funding/COI、Data/code availability、数据授权与私有记录隐私、cover letter、Highlights及投稿站点当前实际要求。
- 根据Elsevier已发布的生成式AI政策，检查稿件准备使用的AI工具是否需在**参考文献前独立声明**工具名称、用途与作者人工核验责任；**作为研究方法实际使用的AI**则应在Methods可复现地说明（两者不可混为一谈）。正式措辞和合规由全部责任作者确认。
- 本修订**无权代替作者科研署名、伦理签署或自动发起KBS投稿**。PR #6保持Draft且不合并，直到C8明确作者签字与合规检查。

**C8 EXIT**：三份审稿memo+重大问题矩阵、编辑的Go/No-go理由、签署者明确批准、真实投稿材料和当前Guide for Authors核对均有记录；不得仅以CI绿色替代作者批准。

## 6. 执行依赖、文件交付和不可通过的停止条件

| 依赖顺序 | 必交付文件/代码（具体名称可依现有约定） | 决定权 |
| --- | --- | --- |
| C6.0 | `N12_C6_CLAIM_EVIDENCE_PRIOR_ART_STRESS_TEST_*.md`、文献DOI核对和六列贡献证据矩阵 | Novelty gate PASS/NARROW/FAIL |
| C6.1 | 冻结DEV证据的S/F监督—策略差异解释表、可辨别策略/训练标签谱系 | Mechanism/identification gate |
| C6.2 | main.tex的Abstract/Discussion/Conclusion及必要Intro细改、Highlights一致性、源diff审阅 | Editorial gate |
| C6.3 | 新的C6 source-science脚本、C6 dual-PDF workflow、新run、SHA/图文审查报告 | Scientific/technical gate |
| C7 | cell-level supplement迁移审计、claim ledger、provenance/licensing manifest、全稿PDF审计 | Audit gate |
| C8 | 三角referee memo、Major-reply矩阵、作者签署与投稿核对 | Human go/no-go |

**共同停止条件**：
- 任何初级方法/指标“首创”或新泛化定理主张没有真正文献与证据支撑；
- 把回顾性sampled label、目标已知history state当作线上pretarget可用；
- 把冻结H1说成equal-call，或B4-A原floor说成预揭盲已验收；
- 把历史Null解释成某单独关系语义的孤立因果机制，或把nested 4096看成独立新增样本；
- 隐瞒Always Memory的更高无约束NDCG或不利原Utility计时；声称新F门控实测节约；
- 把未做的未来期评估、补充DEV分析或新C6–C8 CI声称已经完成；
- 发生科学数字/table-cell不一致、源追溯断链或数据权益不明，仍继续到投稿。

## 7. 核验来源与科研留痕（2026-10-19公开可查；文献定位依据，不替代正文精读）

- Krichene & Rendle (KDD 2020), *On Sampled Metrics for Item Recommendation*: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Mao, Mohri & Zhong (ICML 2024), *Regression with Multi-Expert Deferral*: https://proceedings.mlr.press/v235/mao24d.html
- Yuan et al. (2026 arXiv preprint), *Recommender System as Slow and Fast Thinkers*: https://arxiv.org/abs/2609.02671
- Zhong et al. (KBS 2026), *Scene-aware memory discrimination*: https://www.sciencedirect.com/science/article/pii/S0950705126002388
- Xie et al. (KBS 2026), *Fusing multi-head gating and focused-view contrastive learning*: https://www.sciencedirect.com/science/article/pii/S0950705126004132
- Yerragunta et al. (KBS 2026), *Dynamic conditional gating mechanisms for Question Answering over incomplete Knowledge Bases*: https://www.sciencedirect.com/science/article/pii/S0950705126008932
- Knowledge-Based Systems期刊范围（Elsevier）：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
- Elsevier期刊AI政策（以作者最终投稿时有效版本为准）：https://www-prod.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
- 内部冻结论文与证据：`main.tex`、`N12_C1_RQ_ARGUMENT_AND_EVIDENCE_BLUEPRINT_2026-10-14.md`、`N12_C5_RQ_RESULTS_EVIDENCE_LANDING_EDITORIAL_QA_2026-10-16.md`、`N12_C0_C1_EXECUTION_STATUS_2026-10-14.json`、`analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json`及`analysis/kbs_plan_c/n12_c5_rq_results_evidence_audit.py`。

**执行状态最后确认**：本文仅提高未来C6–C8标准，不修改论文正文、冻结数学与实验结果，也不宣称新CI运行、审稿完成或作者批准。
