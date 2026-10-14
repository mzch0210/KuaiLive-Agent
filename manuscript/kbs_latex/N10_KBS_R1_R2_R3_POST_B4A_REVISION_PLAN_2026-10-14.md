# N10 | KBS三个学术风险：B4-A后路线C修改执行方案

2026-10-14 | 状态：PLAN_ONLY。基线：PR #3 A7，主稿40页，补充材料44页。此文件仅制定方案；没有重跑TEST、A4或修改科学结果。

## 1. 科学定位与三个风险

研究主线：将固定关系记忆来源在指定Base与当前候选环境下的增量排名价值定义为知识使用价值，验证预结果条件估值能否指导有约束的调用，及固定F候选条件下历史关系排列是否真正含有有效信息。

- R1：新颖性与重要性，仍为中等风险。必须把已知deferral、sampled-ranking metric inconsistency与通用gating同本文的知识对象、目标标签、候选环境和历史特异性实验区别开。
- R2：选择决策的资源/运行价值，残余风险最高。B4-A中F-aligned比S-aligned NDCG高、自然Memory调用少，但差距1.337/1.797个百分点不满足旧的1pp近等预算阈值；Always Memory NDCG 0.348744优于两个F选择策略0.305446/0.304530，旧256-DEV warmed offline replay的Always Memory约0.803ms、Utility约1.802ms。不得把少调用自动解释为端到端成本节约。
- R3：真实关系知识来源证据内部很强，但仍有机制归因及Null对照限制。冻结B4-A 4,096目标同F候选的original-minus-3-null加权差为+0.031145，约76.8%历史边重连同时扰动重复对/高阶关系。TRAIN-popularity对照的完整非退化预声明指标没有在A4揭盲前计算/锁定，因此不得追认已通过。

注意B4-A样本来自2026-03-27至31同一旧M3 TEST采集时期：main 30,000目标/10,387用户，nested 4,096目标/3,059用户，零旧G5评价目标ID重叠，但与G5可共享用户/历史观测；不是新日期独立TEST。A4已经一次性评价，不得重跑、重新开标签、再调阈值/模型/Null seed。

## 2. C0 | 核验冻结基线与构建claim-source登记（P0）

先建立每一项核心科学陈述对应的样本、代码、冻结SHA、GitHub Actions、估计量、CI/p、适用边界表。旧G5和B4-A A0–A7历史输出只读。拒绝DEV新增脚本访问B4-A A4 private labels或重写旧仓储。自动测试对照主稿和S10数字，确认含R2反证和R3缺失的TRAIN-popularity floor条件。

交付：source-and-claim-register、不可变输入列表和DEV-only access tests。
验收：原始结论不漂移；没有A4再次调用、私有数据公开或重选择试验。

## 3. C1 | R1原创知识系统贡献、2026近邻文献对照（P0，首选）

阅读并核实原文DOI：
- Zhong et al. (2026), Scene-aware memory discrimination: Deciding which personal knowledge stays, KBS 338:115496, DOI 10.1016/j.knosys.2026.115496（**当前main.tex和bib尚未收录**）；它是记忆写入/保留，本研究是固定历史知识在下游排名中的有条件读取/调用。
- Xie et al. (2026), Fusing multi-head gating and focused-view contrastive learning for knowledge-aware recommendation, KBS 341:115673, DOI 10.1016/j.knosys.2026.115673；知识融合与固定知识的边际决策价值不可混同。
- Yuan et al. (2026), Recommender System as Slow and Fast Thinkers, arXiv:2609.02671（预印本，切勿误称期刊接受），说明预算自适应路由已有近邻。
- Krichene and Rendle, On Sampled Metrics for Item Recommendation, KDD 2020，已证明采样指标不保持完整排名的模型排序。
- 既有Mozannar / Narasimhan / Mao learning-to-defer及SeqRec、KuaiLive原始论文。

任务：
1. 建立相近工作矩阵，列研究对象、知识处理阶段、候选集、估值目标、训练信息、决策输出、实验有效性和真正创新的差异。
2. 将本文贡献改写成P1 incumbent-relative explicit relationship knowledge value，P2 candidate-aligned supervision affects decisions，P3 authentic history arrangement has incremental value under fixed F。
3. 将P1–P3对应的最强证据、机制和限制分别明确附在Intro/Related Work与Discussion，不以新gating算法或sampled NDCG定理冒领新颖性。
4. 主文增加一张可由源信息核对的知识估值→候选监督→选择决策→固定来源Null的统一研究框架图。设计简明，具体数值需源可追溯。

交付：文献核对表、贡献边界矩阵、P1–P3定位稿及图示设计。
验收：读摘要/贡献段和图即可区分本文与SAMD、MHGFCL、DS-Frame、KDD sampled-metrics的独立研究增量；新增参考文献真实可核。

## 4. C2 | R2决策价值、等预算与真实计算成本（P0，重点突破）

C2-A：只使用已冻结DEV OOF记录和已有B1/B2预结果特征，核对Always Base、Always Memory、Utility、Difficulty、Specialist Quality、Random@budget及F/S监督的真实调用率和F-NDCG。绘制预先指定的quality-versus-invocation图。另提供仅DEV的等调用预算敏感性：阈值只在既定DEV训练/验证划分上决定，严格复核相同实际call count；标注为post-B4-A DEV探索，不作为新独立TEST，也不可事后调整B4-A门控或对当前TEST重评分。不能用整个测试批次的效用最优top-k伪称线上可执行门控。

C2-B：测量真正的增量路径成本，在相同DEV目标、TRAIN-known F候选、固定设备和批次上比较Always Base、Always Memory、Fixed Utility/F-aligned policy。计时和记录history retrieval、active roster construction、Base encoding/scoring、12 gate features、HGB prediction、Memory score、sorting、传输等。区分共享、条件分支和重复执行成本；同时提供cold/warm、均值、median、p95、吞吐量、CPU/GPU峰值资源。如用CUDA需要同步，固定线程/输入/运行顺序，多次测量并公开脚本环境；旧256 DEV timing 0.803/1.425/1.802ms须保留，不以新数据覆盖不利结论。

C2科学门槛：
- 如果选择政策确实在可定义资源预算内形成优良的quality-cost前沿，讨论对应条件与限制。
- 如果端到端仍较Always Memory慢或成本更高，必须**STOP任何部署效率优势主张**；将研究主张限制在“有外生Memory调用约束的知识分配质量”，外生约束不可仅凭模型调用比例杜撰。
- 经济/权限/在线服务成本没有测量时禁止声称真实节约。

交付：调用率和质量曲线、系统级分解账本、基准测量脚本、device/runtime说明、R2是否具有部署优势的正反结论报告。
验收：每个延迟和资源结论有原始DEV运行日志及正确共享计算口径，不存在少调用自动等于更快的逻辑。

## 5. C3 | R3关系机制与完整负对照审计（P0 + 可选P1）

C3-A必须先完成：
- 并列B2 DEV和B4-A H2控制表，记录同F候选、相同score实现、closed-hour激活、author-hour marginal/time/availability、实际rewired%、Null NDCG、Null positive Top-10、TRAIN-popularity-only差值和每一门槛是否真被验证。
- B4-A TRAIN-popularity floor必须明确为NOT VERIFIED AS PREDECLARED，不能在已揭盲后补算而声称原始预登记通过。
- 写明关系Null同时改变重复对和高阶结构，因此证据支持具体历史关系排列的总效用，不能归因于独立单一pair属性。

C3-B可选DEV机制敏感性：
- 如C3-A后仍有明显审稿机制质疑，在已接触的DEV上事前记录固定样本、Null种子、目标强度（候选20%、50%、80%档，以实际可实现交换率为准）、有效时间可用性边界，并在读效用前封存Null地图SHA。
- 所有条件同一DEV目标、固定F roster和原Memory scorer，检验强度—效用响应及跨用户依赖；多seed不视为多独立数据集。DEV实验仅生成探索性机制证据。
- 可选基于已有Full/Long/Short/Popularity成分的局部机制表，避免将复合扰动解释成某一关系变量的因果估计。若收益有限直接停止，不为更多p值扩大实验。

交付：R3源/时间/候选/统计验证矩阵及可选DEV强度敏感性图和源SHA。
验收：所有未评估的预声明对照以NOT VERIFIED登记；新的DEV实验不会改变原A4/H2结果或恢复所谓新TEST身份。

## 6. C4 | 综合裁定与决定实际论文claim（P0）

按最新R1/R2/R3证据召开一次独立审稿清单裁定：
- R1须是可被证伪、可与已有知识存储/融合/通用路由工作区别的研究命题。
- R2如果缺乏实测端到端/经济优势，主张只能是固定调用数约束下的策略选择，保留Always Memory绝对准确率更高、旧warmed路径更快的反证。
- R3在complete nonfloor未通过审计时只能称部分非退化控制支持；联合历史结构扰动，不能说隔离了某一种关系机制。
- 保留同时间段而非真正新时间段验证的独立性限制。

**新未来数据不是本轮硬性要求**。只有存在可合法获取、未曾参与开发选择和独立日期/来源的公开数据，并有真实可审计时，另外冻结协议开展，不把旧M3未评价ID当时间新分布。

交付：允许/禁止发表的claims register及针对三风险的最新独立裁定。
验收：论文正反结果同时可见，没有因结果不利删除指标。

## 7. C5 | 依结论逐章投稿级修改（P0）

执行顺序：
1. Abstract/Introduction与Related Work：把三命题串为一条完整知识系统主线；引用SAMD、MHGFCL、DS-Frame等并准确标注发表状态；题目除非定位必须改变尽量维持。
2. Problem/Method：明确定义Base、候选、关系知识、边际效用Delta及条件价值eta，区别收益估值、调用约束与真正成本；历史与标签可见性严格。
3. Experimental Setup：分别标记Twitch TEST、KuaiLive已回看配对、M3 G5 TEST、post-G5 DEV、B4-A same-period冻结新增目标与本轮DEV探索；明示哪些有Holm、样本用户聚类与权重。
4. Results：围绕“关系知识增量价值→候选环境下监督变化→决策结果→来源真实性→资源/成本边界”整合；重点表保留B4-A H1/H2与Always Memory参照；新增C2/C3结果按证据等级安放。
5. Discussion/Conclusion：提炼可迁移知识系统评价规程，实用的约束条件与未解决外部效度；集中陈述限制，避免散落自我否定，绝不删不利结果。
6. Supplement S1–S10：保留旧冻结源，新增DEV敏感性与成本审计细节，主表/补充引用一致；不公开私人IDs、作者关系及Null映射。

交付：逐节文稿、主文证据链图、新增DEV/系统成本表、补充材料版本与双向引用索引。
验收：不改变冻结NDCG/CI/p/调用数；主文主线清楚、图表密度合理、理论与实际边界恰当、阅读不必重走研究项目历史。

## 8. C6 | 三维度模拟审稿与终稿QA（P0）

分为编辑初筛（KBS scope+novelty）、方法审稿（数据泄漏/历史/Null/置信区间/同时间段独立性）、系统审稿（调用约束/真实延迟/Always Memory反例）三个独立检查维度。每项必须有精确主文定位和run/source证据或诚实限制。

按投稿时有效KBS Guide for Authors检查匿名审稿、文章格式、图表、参考文献及Supplement规则；不要据老模板擅自设定页数上限。编译最新主文与Supplement PDF，检查渲染、交叉引用、BibTeX、DOI、缺失图片、AI标注等。

Elsevier 2026期刊政策：实质性AI辅助稿件写作需声明；若AI用于实验设计、代码开发、数据分析，需在Methods可复现描述。最终声明、作者及机构、CRediT、COI、资助、数据和私有派生交互记录共享许可均由责任作者审核。政策：https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals 。

交付：编辑/方法/系统三份问题清单、最终claim-source索引、投稿级主PDF/补充PDF、引用审计、投稿声明清单与cover letter要点。
验收：关键审稿问题均有可核查答复，A4未重跑，责任作者核准后才决定将Draft PR合并main并投稿。

## 9. 依赖、排序和停止规则

| 阶段 | 优先级 | 依赖 | 是否必须 |
| --- | --- | --- | --- |
| C0 证据冻结 | P0 | A7 | 必须 |
| C1 新颖性和文献 | P0 | C0 | 必须 |
| C2 价值和系统成本 | P0 | C0，可与C1证据审查并行 | 必须核验；没有可靠运行器则如实报告 |
| C3-A Null与负对照审计 | P0 | C0 | 必须 |
| C3-B DEV强度敏感性 | P1 | C3-A/C2评估完成 | 按审稿风险收益决定 |
| C4 科学裁定 | P0 | C1 C2 C3已完成项 | 必须 |
| C5 逐章整合 | P0 | C4 | 必须 |
| C6 最终review与QA | P0 | C5 | 必须 |

永久约束：不再打开或重做B4-A A4；不借TEST结果调参；不将新DEV标成独立TEST；不将post hoc popularity检查追认预登记通过；不遗漏Always Memory的反例；不把具体关系历史联合扰动称作孤立微观因果；不发布私有交互原始行或置换映射。

外部来源：
KBS官方范围：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
SAMD：https://www.sciencedirect.com/science/article/pii/S0950705126002388
MHGFCL：https://www.sciencedirect.com/science/article/pii/S0950705126004132
DS-Frame：https://arxiv.org/abs/2609.02671
Sampled metrics：https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
本项目当前A7 QA：manuscript/kbs_latex/N9_ROUTE_B_B4A_A7_POSTINTEGRATION_SUBMISSION_QA_2026-10-14.md 。
