# N12-C8V V1 | 近邻先行研究、创新性可防守范围及 corrected-S 替代解释核查

日期：2026-10-19。**V1文献/现有证据分析报告已完成；独立于主要改稿者的科研审读尚未签署**。本文件是内部方法学压力测试，不是实际KBS同行审稿意见、检索穷尽证明、corrected-S实验或接收预测。N12 Draft PR #6，主稿本轮基线为修复V0后37p/47p。V0真实科学语义+冻结结果+双PDF run #39218602150 **BOTH JOBS SUCCESS**；相关状态由V0执行报告另行记录。本文并不修改论文正文/补充/实验或原TEST。

## 1. 科学核心主张与原先例重叠的四层分解

研究对象为固定viewer–creator Short/Long/Popularity专家M、已经训练的Base B、实际完整候选F、预结果特征Z，标签为 Δ_r=u_10(M,C_r)−u_10(B,C_r)，监督预结果调用政策 π_r(Z)。实际科学问题：
> Do candidate regimes used to form Base-relative value labels alter which decisions receive a fixed external historical specialist and the downstream full-candidate ranking value of those frozen assignments?

必须分四层区分：
(1) sampled rank-metric winner inconsistency **已知**；
(2) conditional relative advantage/defer-to-expert **已知**；
(3) downstream decision-focused learning **已知**；
(4) 真实候选环境与retrospective sampled candidate supervision之间**在固定Memory/B/特征的请求级调用配置和F决策质量上产生可见差异**：这是本文的**特定实证落点**，不是新一般定理。不能由结果自发推导“历史关系知识专属机制”或“所有合理校正的S监督都劣于F”。

## 2. 已核实文献：先例–差异–来源证据–竞争解释矩阵

| 近邻公开研究（版本与范围） | 已有的最接近结果、方法/估计对象 | N12独立的**可证**实证对象 | 当前直接证据 | 未排除的替代解释与裁决 |
| --- | --- | --- | --- | --- |
| **Krichene & Rendle, KDD 2020**, *On Sampled Metrics for Item Recommendation*, DOI 10.1145/3394486.3403226 | ranking metrics采样可不保全量模型优劣、期望亦不保证；提出bias/MSE等校正方法并进行评估。研究主要是**采样的排名评价统计量**。 | 将candidate-indexed排名指标作为每请求 **Memory−Base效用学习标签**，再问标签误差是否映射至Memory调用配置和最终F决策；不是首创sampled inconsistency。 | original KuaiLive paired S −.04120/F+.04631；同一M3 DEV 50,049上的S/F开关分配和额外30k完整F冻结策略结局 | **P0**：原S是未经验证校正的target-retained抽样指标；没有对比valid corrected-S。一般metric纠偏可能减少或消除所测试策略差异。此文献的校正公式/渐近性质不能在未核实信息充分性的情况下直接搬到当前每请求Δ监督对象。 |
| **Li et al., KDD 2020**, *On Sampling Top-K Recommendation Evaluation* | 对采样Top-k HR与全量HR的关系提出mapping/校准路径，特别是HR/Recall对象，而不是N12的单正例NDCG及条件专家收益。 | 可检验的候选相关**知识调用监督后果**，不是新rank-sampling映射。 | RQ2同评价F与请求分解 | **P1**：进一步证明存在不同评价校正方案；不能把特定HR修正无条件套入NDCG。需要V2方法适用性。 |
| **Ihemelandu & Ekstrand, WI-IAT 2023**, *Candidate Set Sampling for Evaluating Top-N Recommendation*, DOI 10.1109/WI-IAT59888.2023.00018 | 明确研究候选选择策略与popularity bias对Top-N离线指标的交互，模拟sampled/full测量偏差。 | N12不声称首次发现动态候选/受欢迎度共同影响排名；关注**该偏差当作知识使用决策标签**的后续policy层影响。 | M3 F vs S supervised policies & operational calls；B2 source composition | **P1/P0**：S/F差异可能源自普通ranker/popularity/candidate统计，而非特定关系知识机制；V3需声明反例。 |
| **Mao, Mohri & Zhong, ICML 2024**, *Regression with Multi-Expert Deferral* | 已支持pretrained predictor+learned deferral、多bounded regression losses、instance/label costs及一致性保证。 | N12研究标签所在的 **candidate evaluation regime**；不是发明Δ期望、defer规则或最优限额选择算法。 | 固定的B/M、同Z、outer DEV、冻结H1 | **P0**：若除一般专家委托外仅剩“训练评价一致更好”，创新性不足；N12没有新数学定理，不应虚构。 |
| **Mandi et al., JAIR 2024**, *Decision-Focused Learning: Foundations, State of the Art, Benchmark and Future Opportunities*, DOI 10.1613/JAIR.1.15320 | decision-focused目标已在ML和优化中广泛建立；综述梯度/非梯度策略、组合目标及经验基准。 | 不以“从预测到决策”标新；直接考察外部Memory使用的**候选条件化相对NDCG标签**与request-level allocation。 | G2 E1 DEV switch + H1 policy comparison | **P0**：若未证明独特知识系统场景机制，仍可能是DFL一般思想在现有路由器上的应用。 |
| **Qian et al., 2026-07-27 arXiv v1 PREPRINT**, *When Should Active RAG Retrieve? A Budget-Aware Evaluation of Utility, Calibration, and Cost*, arXiv:2607.24010 | 对retrieval vs no retrieval定义逐example边际正确率效用；区分exact top-k非部署前沿、DEV→holdout deployable阈值、conservative预算、harm和predecision cost；揭示换证据源会变效用和router排序。特别其BUR用预测P(help)−P(harm)进行效用排序。 | N12处理**动态推荐候选榜单本身决定两套固定排序器的相对NDCG标签**，对比full-label vs 574-target-retained sampled-label训练，再看同F下调用开关与结局；Qian研究QA答案/证据检索而非该推荐候选标签实验。 | RQ1 paired room reversal、M3 DEV决策开关、30k H1 | **P0**：Base-relative knowledge utility、预算router、成本/阈值区别**已被直接先例覆盖**，不可称N12首创。Qian不同QA任务并不自动否定N12的特定标签错配结果。作者版本为预印本，不能误说已被KBS/会议接收。 |
| **Yuan et al., 2026-09 arXiv PREPRINT**, *Recommender System as Slow and Fast Thinkers* (DS-Frame), arXiv:2609.02671 | 推荐fast/slow推断与学习selector、受限计算额度、五数据集提升。 | N12处理预先存在的固定历史关系专家的**标签协议与使用决策**而非新的slow/refinement架构或速度提升。 | N12固定Short/Long/Popularity源、A4额外政策 | **P1**：动态路由/约束推荐领域先例近；实际部署额度未测量，不应凭call次数推出省时。 |
| **Zhong et al., KBS 2026** SAMD, DOI 10.1016/j.knosys.2026.115496 | personal knowledge按application scene在**记忆写入/保留**阶段作筛选，控制构造效率/质量。 | N12已固定历史源，评估**使用时**相对Base的收益，而不决定保存何条记忆。 | 固定memory scorer、RQ3历史null对照 | **P1**：不能声称“首次任务依赖判断记忆价值”；知识类型不同，不能认为应用差异即全新知识理论。 |
| **Xie et al., KBS 2026** MHGFCL, DOI 10.1016/j.knosys.2026.115673 | 知识图协同/语义/结构多视图、对比学习、多头门控融合与长短期偏好区分。 | N12不是KG、GNN或知识表示创新；固定透明历史专家可用于**知识边际价值的可审计决策评价**。 | fixed scorer + source composition ablations | **P1**：知识系统新颖性需要由“知识使用评价对象”承担，不能靠KGR架构首创。 |

来源真实性边界：KDD/PMLR/JAIR正式论文的官方网站、WI-IAT作者书目/DOI、Elsevier期刊论文页；Qian与DS-Frame以2026 arXiv预印本的正式页面/HTML为准。未宣称精读付费全文或穷尽所有截至2026-10-19的论文。**V1没有发现足以证明N12候选价值监督实验被某篇直接完整重复的同对象结果；但是“检索未发现”不是“存在新颖性”证明。**

### 直接可查研究来源
- Krichene/Rendle KDD2020: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Li et al. KDD2020: https://www.kdd.org/kdd2020/accepted-papers/view/on-sampling-top-k-recommendation-evaluation.html
- Ihemelandu/Ekstrand WI-IAT2023: https://mdw.ekstrandom.net/pubs/wi-sampled-eval
- Mao et al. ICML2024: https://proceedings.mlr.press/v235/mao24d.html
- Mandi et al. JAIR2024: https://mlanthology.org/jair/2024/mandi2024jair-decisionfocused/
- Qian et al. Active RAG arXiv2026: https://arxiv.org/html/2607.24010
- DS-Frame arXiv2026: https://arxiv.org/abs/2609.02671
- SAMD KBS2026: https://www.sciencedirect.com/science/article/pii/S0950705126002388
- MHGFCL KBS2026: https://www.sciencedirect.com/science/article/pii/S0950705126004132

## 3. 最有威胁的三条竞争解释：当前证据的裁决

### V1-Q1：是否只是“不一致且未校正”的sampled labels？
**尚未排除，P0。** 原S用在完整候选中事后保留观测目标后均匀无放回抽574 negatives，575 total；作为 **offline label** 而不是部署时目标可见输入。原B1私有CSV中公开报告仅能确认sampled top-10 NDCG scalar、F NDCG和若干candidate-count特征；尚不能确认完整sampled rank、候选scores、采样概率/seed及校正所需信息对DEV逐请求充分。Krichene式bias/MSE校正主要评价完整排名**指标估计**，而N12要估计$\eta_F(Z)=E[u_F(M)-u_F(B)\mid Z]$。将某个总体采样指标校正直接称为“逐事件无偏的Knowledge Δ监督”是不成立的推论，必须在V2a核验统计估计对象、rank censorship、sampling law及样本映射后，才允许进行三臂 DEV pilot。若corrected-S无法真实实现，应报告数据不足及有限主张，不得说corrected-S已被证明无效。

### V1-Q2：是否知识来源特有的创新？
**未被识别，P0/P1。** DEV B2显示Long-only 12-feature监督迁移regret SAS 0.010605、GRU 0.010262高于Full (0.006159、0.004970)，Short-only约0.020694/0.020291但S policy几乎不调用Memory (SAS171 vs F14766；GRU141 vs F14851)；Popularity/placebo近零regret至少部分是无调用floor。6-feature去直接关系描述后Full regret缩小到SAS0.001814、GRU0.001607，但predictor信息合同同时变化，不能隔离来源因果效果。RQ3真实历史优于复合重排null只验证历史源含有信息，不证明F/S监督效果是关系身份语义独有。V3必须给出支持/探索/未识别等级，不能硬造relations-only机制。

### V1-Q3：为何不是普通DFL/Active RAG？
**可防守但不强，P0。** 强调选择器的**监督目标由当前候选集合定义**，比较原始S生成的相对NDCG标签和完整F标签对**固定B与M**的分配及F排名结局，与Active RAG的答案correctness差值/检索预算原生问题不完全相同。Qian已给出exact vs deployable frontiers和serving overhead的细分，N12必须坦诚未完整覆盖这些方面；离线30k F策略质量+0.005391/0.003585且调用数少401/539是**完整冻结策略**的优势，不是等调用纯label因果效应或可部署成本更低。DEV21.32/23.01%的请求switch及on/off增量贡献仅为**探索性代数分解**，不能当独立机制实验。

## 4. 可接受科学主张和不可接受主张

**允许的最强版本**：
> For the fixed relationship-memory expert and two M3 incumbents examined, using full-candidate rather than the tested uncorrected, retrospectively target-retained sampled-candidate relative-utility labels changes the allocation of Memory invocations and yields better frozen policy ranking quality under full-candidate evaluation. The development switch accounting explains which evaluated requests contribute, while original historical arrangements independently carry ranking information relative to the tested constrained history nulls.

需要同时保留：原本DEV探索与30k同期间H1的区别、SAS/GRU各自的调用数、H1不严格等预算、H2已通过部分nonfloor但原同cohort TRAIN-only Popularity门槛未认证、Always Memory更好无约束准确率、旧pointwise计时不等于新F门控。

**不可宣称**：首次Base-relative知识效用/decision-focused selection；首次candidate-sampling metric inconsistency；所有corrected-S更差；关系来源特有因果定律；等额度纯label效应；future-period独立确认；online真实效用或生产部署节约。

## 5. V1验证裁决与独立审查状态

**Analyst novelty stress test: COMPLETED, verdict NARROW_AND_PROCEED_TO_V2A_FEASIBILITY.** 不是KBS“创新性达标PASS”；与V0不同，V1必须有一位没有参与此前主文改稿的学术同事就近邻先例、客观比较和核心贡献给出独立签名/意见后才能标完整“V1 REVIEW GATE PASS”。

优先级建议：
1. **V2a corrected-S 信息充分性审查**：只读代码/schemas、元数据，明确full-rank可重建的必要条件，禁止先跑校正实验；若不可行，发可复核的HOLD理由。
2. **V3 B2 source-candidate矩阵**：必须承认Long-only反例、Short-only不等calls、Popularity floor；不应把一般候选问题包装成知识关系机制。
3. **V4成本/预算检查** 只有在论文本来就想主张真实部署收益时才需要新数据；当前bounded submission无此必要。
4. C8作者Go/No-go独立于V1专家签名，不得由本报告代签。

**本文档更新代码/实验状态**：没有更改main.tex、Highlights、BibTeX、数据、模型、TEST、阈值或原冻结统计；仅完成公开文献 + 已有GitHub DEV汇总的科学比较。未经独立读者审核不可称已经获得第三方审稿认可。
