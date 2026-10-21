# N12-C6.0 | Independent Novelty-to-Evidence Stress Test and Editorial Decision

**审查日期**：2026-10-19。**执行性质**：实际开展的 C6.0 文献核验、冻结结果对照和科学主张压力测试；非新实验、非作者/匿名同行评审，也非C6全部完成。**起点**：N12 C5 已完成，最近通过 CI #38864362019（36p main / 47p supplement）；基线主稿为此前已通过的 N12 分支版本。**决定**：**PASS TO C6.1 / C6.2 ONLY AFTER NARROWING（有条件继续）**。学术新颖性是否达到KBS最终要求仍是开放的编辑风险，不得将本报告称作外部审稿认可。

## 1. 核心判断（先说明哪些是已知工作）

在固定历史viewer–creator关系Memory $M$、既有Base $B$和实际候选环境$F$下，论文对知识使用效用的操作化对象为
\[
\Delta_r(x)=u_{10}(M,x;C_r)-u_{10}(B,x;C_r),\quad
\eta_r(z)=\mathbb{E}[\Delta_r(X)\mid Z=z,R=r].
\]
这一公式和按预测收益路由并非新的学习理论。采样候选上的排名指标不能保证保持模型排序也是成熟结果。N12最可辩护的增量是**把候选评价环境差异引入固定外部知识源的相对效用监督目标，并在相同实际F候选环境下验证冻结知识选择策略的决策后果**。本文的证据是经验方法学贡献（empirical decision-target/evaluation contribution），不是一般化deferral算法、因果识别定理或生产部署节约。

统一逻辑：
1. RQ1：定义相对于现有Base及当前候选的知识决策价值；original KuaiLive room 10,222 paired events从sampled −0.04120到full +0.04631，但候选数、身份及竞争同时改变；Twitch 44,221 streamer TEST证明固定历史源在Base较好时仍可能对部分事件有补充价值。
2. **RQ2（核心科学落点）**：相同M3 author-ranking cohort中，以不同候选 regime 的 $\Delta_S/\Delta_F$ 训练/校准冻结政策；实际F候选上的政策质量不同。DEV将绩效差异进一步分解为约21–23%请求的调用重新分配；额外30k同期间冻结H1给出独立于原已评价TEST事件ID的主要策略结局证据。
3. RQ3（平行）固定当下F候选及评分器，验证真实历史排列较时间/活动受限Null有信息；**不能写成RQ2已识别的关系语义机制，或RQ2导致RQ3的中介**。
4. Invocation/cost只给出适用边界。

## 2. 经过公开一手来源核验的近邻文献矩阵

| 先例及状态 | 确认的先例贡献 | N12剩余差异 | 审稿挑战/必答位置 |
| --- | --- | --- | --- |
| **Krichene & Rendle, KDD 2020**, DOI **10.1145/3394486.3403226** | sampled ranking metric可能不保持full metric上的相对模型比较，即使取期望也不保证 | N12比较**用sampled/full知识增益作为选择器监督标签**后，对下游F调用决策产生的差异 | 不是首次发现metric inconsistency；Intro的RQ1→RQ2桥及Discussion不得混同sampler偏差与决策影响 |
| **Mao, Mohri & Zhong, ICML 2024**, *Regression with Multi-Expert Deferral*, PMLR 235:34738–34759 | 固定预测器+学习的defer策略、多专家及损失/成本形式、理论分析 | 研究特定外部历史关系源的candidate-indexed **learning target/decision consequences**，不提出新deferral定理 | η预测、预算阈值不能当原创算法；Related Work明确已有expert selection |
| **Yuan et al., *Recommender System as Slow and Fast Thinkers***，**arXiv:2609.02671（2026预印本）** | fast/slow推荐、学习型路由和受控计算预算、效率/准确度权衡 | N12固定外部历史关系M而非新slow iterative learner，主张是标签对齐而非效率新颖性 | 不将preprint说成已发表期刊文献；解释为何Always Memory胜精度及旧路由更慢 |
| **Zhong et al., SAMD**, *Knowledge-Based Systems* **338:115496 (2026)**, DOI **10.1016/j.knosys.2026.115496** | 应用场景感知地决定个人记忆的保留/写入，并检验记忆管理后续效用 | N12不优化write/retention，而是**已经固定的源在本次Base排名中的边际使用价值** | 不能声称首次对记忆做任务依赖价值评估 |
| **Xie et al., MHGFCL**, *Knowledge-Based Systems* **341:115673 (2026)**, DOI **10.1016/j.knosys.2026.115673** | 协同/语义/结构KG多视图与对比学习，采用多头门控融合 | N12固定Short/Long/Pop评分器便于监督目标审计，**不是新KG表示/融合架构** | 要明确relationship memory只是可追踪历史关系证据，不偷换成KG语义推理 |
| **Yerragunta et al.**, *Dynamic conditional gating mechanisms for Question Answering over incomplete Knowledge Bases*, *KBS* **346:116167 (2026)**，DOI **10.1016/j.knosys.2026.116167** | KB证据改进、动态门控、组合/受控比较 | N12具体问题是candidate mismatch下的推荐价值标签；RQ3并不是source×selector完整因果factorial | 尤其不能夸大“同时检验来源和使用”自动等于创新的交互设计 |
| **Cañamares, Castells & Moffat, 2020**, *Offline evaluation options for recommender systems*, DOI **10.1007/s10791-020-09371-3**；**RecSys 2025** *On the Reliability of Sampling Strategies in Offline Recommender Evaluation*, DOI **10.1145/3705328.3748086** | 离线评价协议选择、exposure/sampling bias会影响推断 | N12可专注明确的F协议下预目标知识使用决策，不延伸为online counterfactual welfare | H1真实标签依赖日志曝光；无IPS/随机暴露，不能推断线上改善 |

**来源（出版商/会议/正式arXiv记录；页面或摘要核实，不冒充精读全部付费全文）：**

- https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ （KDD原文摘要；DOI见 ACM KDD records）
- https://proceedings.mlr.press/v235/mao24d.html
- https://arxiv.org/abs/2609.02671
- https://www.sciencedirect.com/science/article/pii/S0950705126002388
- https://www.sciencedirect.com/science/article/pii/S0950705126004132
- https://www.sciencedirect.com/science/article/pii/S0950705126008932
- https://doi.org/10.1007/s10791-020-09371-3
- https://doi.org/10.1145/3705328.3748086

C6.2如需补加Yerragunta或离线评估文献，应先核对主稿BibTeX条目/与现有引用的语义相关性，**不为堆文献而盲目添加**。上述相关性比较基于可查阅官方摘要和本地冻结方法，不声称穷尽2026年最新全部研究。

## 3. C6.0 科学主张逐条裁决（Claims Register）

| ID / 当前主张 | 关键源位置与固定结果 | 已有先例与竞争性解释 | 裁决 / 允许的最强表述 |
| --- | --- | --- | --- |
| C01 “构建新的增量知识价值指标Δ及条件期望η” | main.tex §§3.3–3.5，原9个公式冻结 | 一般loss difference、VOI、learning-to-defer已有同类决策对象 | **NARROW**：操作化并固定B/M/C的评价合同；不能称新理论、首个框架 |
| C02 “知识相对价值在候选环境下变化” | RQ1 original KuaiLive paired room 10,222; M−B S −0.04120, F +0.04631；Twitch 44,221 | 既有sampled metric inconsistency；S/F改变候选身份/数量/竞争，不单独识别大小效应 | **KEEP AS EMPIRICAL DIAGNOSTIC**：固定pair与paired regime shift，非采样理论创新 |
| C03 “候选对齐监督导致更好的知识使用策略” | RQ2额外同期间M3 30,000/10,387 users、20-cell加权；SAS F−S **+0.005391** CI **[0.003646,0.007174]**, Holm **0.000600**；GRU **+0.003585** CI **[0.001599,0.005576]**, Holm **0.000800**；main Table tab:results-m3-b4a-supervision | 仅展示train/test一致不足新；S/F调用分别8704/9105、8629/9168，超1pp，自身带有不同校准与阈值；单一同期群体 | **KEEP AS PRIMARY BOUNDED CONTRIBUTION**：相同F评价下**完整DEV冻结策略的观测差异**；不得写strict equal-budget label-only causal effect |
| C04 “候选监督错配使调用重新分配” | N9_G2_E1探索性50,049 DEV/12,628 users；SAS10672/21.32%、GRU11517/23.01%不同调用；switch-on δ均值0.133417/0.126600 vs switch-off0.076194/0.079135 | same DEV cohort and adaptive exploration；从代数恒等式可分解policy value，非新定理；switch-on/off均**正值**，不是避免负效用 | **KEEP EXPLORATORY MECHANISTIC SUPPORT**：高收益分配与政策分歧；绝不冒充30k事件分解或独立验证 |
| C05 “source×candidate是关系专有的可识别交互” | B2五源50,049 DEV：Full/Long/Short/Popularity/placebo。Long-only 12-feature transfer penalty SAS0.010605、GRU0.010262 **高于Full**；Short-only大penalty伴随近零S调用 | 低质量控制有floor、信息合同变化、gate调用差巨幅；普通ranker也可能出现 | **REMOVE STRONG IDENTITY-SPECIFIC/CAUSAL INTERACTION**；可谨慎讨论非单调 source composition sensitivity，不能提出先验单调定律 |
| C06 “真实历史本身比受约束Null好” | nested4096/3059 users；authentic0.334942 vs null mean0.303797，差 **+0.031145** CI **[0.027389,0.035098]**, Holm **0.000600**；3 seeds same cohort | 改变重复配对及高阶结构，约76.8%rewired；原B4-A同队列TRAIN-only popularity floor prereveal **NOT VERIFIED** | **KEEP WITH EXPLICIT H2 VALIDITY CAVEAT**：针对composite历史排列的受限源有效性证据；不得称所有预承诺验收PASS或特定语义因果机制 |
| C07 “选择器提升M3推荐精度” | original47575 TEST, SAS Base0.25800, frozen Utility0.30287, Always Memory0.34679, 29.21% Memory calls；6 fits same TEST events | Utility better than Base/comparators, but worse than unconditional Memory，且fits非独立群体 | **KEEP UNDER EXOGENOUS INVOCATION LIMIT ONLY**，不称全面最佳准确率 |
| C08 “使用Memory更少意味着更快/节约” | 旧pointwise Utility256DEV×3：1.769 ms vs Always M 0.692 ms；30k Always M 0.348744 > F policy0.305446/0.304530 | 计时非新vectorized F gate，也非生产部署；真实Memory调用稀缺性未测 | **REMOVE COST-SAVING CONCLUSION**；只留运行边界，若要经济主张需新工作负载与实际约束 |
| C09 “对未来时间和在线用户有效” | 30000与原TEST同2026-03-27至03-31 period，只事件ID不同，且与nested4096共享样本；单正反馈NDCG | 同期、共用户/历史、日志曝光偏差、rank units不同 | **REMOVE FUTURE-TIME AND ONLINE GENERALIZATION**；只允许指定离线协议与群体 |
| C10 “论文是系统性的知识价值评价研究” | 既有method§3、RQ1→RQ2和RQ3平行结构，3 datasets、两类M3 Base | 内容可以被看作general routing+metric sampling案例；没有新的知识表示结构 | **KEEP CONDITIONALLY**：定位为知识系统的**价值监督目标与实际决策评价**；需要C6.2在摘要/结论把该连接写清楚 |

## 4. 主要编辑挑战、响应与剩余等级

**Challenge 1（P0）：简单拼接 Krichene + learning-to-defer？** 现有模型和阈值理论不足以独立证明方法学首创。防守点在于固定外部知识源、B/C相对效用目标、候选错配到冻结policy的实证链以及探索性的switch allocation剖析；但“training/evaluation regime match should work”可能仍被视为直观结果。**风险：仍为P0；允许以审慎empirical methodological insight写作，不标为完全解决**。

**Challenge 2（P0）：F/S是否strict equal call？** 否，30k的原容忍要求未达；尽管F政策质量更高且自然调用较少，解释对象是两个独立冻结策略整体。后揭盲threshold equalization不得做。**风险：已通过正确界定estimand部分缓解，仍不能支持强因果措辞。**

**Challenge 3（P0）：所谓relationship knowledge是否只是重复频次？** Memory确为Short/Long/Pop显式计数/衰减评分器，不是新KG语义推理。RQ3受限Null显示真实历史排列信息含量，未孤立特定semantic factor；H2 floor缺口降低预验收可信度。**风险：P0，需诚实数据源定义且不能夸大**。

**Challenge 4（P0）：效用选择为何比直接用Always M实用？** 对M3无约束精度/实测旧延迟均不能形成优势。只有外生的访问配额、授权/成本约束下才是合理应用问题，而此类真实部署约束尚未实测。**风险：P0，当前只保留有限调用策略评价**。

**Challenge 5（P1）：跨平台与独立再现？** 任务不同，H1追加TEST event IDs非后续时间且可能用户重复；没有在线随机曝光数据。**风险：P1，必须显著限制外推**。

**Challenge 6（P1）：knowledge-source × gate的交互机制是否完整验证？** B2 Long-only反例和Short-only严重call imbalance否定简单解释；受控source与supervision完全交叉的独立confirmatory因果证据不存在。**风险：P1，不需凭空创造第四RQ**。

## 5. 建议的研究贡献与可用措辞

**Primary contribution（建议Intro第二条）**：
> We examine candidate-regime alignment as a property of the supervision target for deciding when to use a fixed relationship-memory ranker. Holding the evaluation candidates, decision-time feature contract, base models and specialist fixed, we compare frozen F- and sampled-label-supervised policies on additional author-ranking events; F-aligned policies achieve higher full-candidate ranking utility, though realized invocation counts differ.

**Supporting RQ1**：
> We characterize incumbent-relative relationship-memory utility under observed history and candidate regime changes, including a paired sampled-to-full value reversal; this extends sampled-metric concerns to the supervision label used for knowledge-use decisions rather than claiming a new inconsistency theorem.

**Parallel RQ3**：
> With current full candidates and the memory-scoring rule fixed, authentic historical arrangements outperform constrained randomized histories on the evaluated cohort. The intervention is composite and its original same-cohort prereveal nondegeneracy floor remains unverified.

**Overall conclusion**：
> Candidate indexing is not merely an offline metric-reporting convention; for a fixed external knowledge source it is part of the decision-supervision contract. Offline estimates remain tied to their candidate protocol and observed logging policy, and reduced specialist invocations do not automatically establish net serving savings.

**Forbidden or requires new evidence**: “first generic memory gate”; “novel consistent estimator”; “equal-cost causal effect”; “semantic causality of repeated pair alone”; “independent future-period validation”; “production-time savings”; “Always Memory dominated”; “all preregistered Null validity acceptance checks passed”.

## 6. C6.0 gate outcome and requirements for C6.1

- **Outcome**：**PASS_TO_EDIT_WITH_BOUNDED_EMPIRICAL_CLAIMS**，即执行了公开论文摘要/出版信息及冻结实验对照，准许推进 C6.1 现有证据决策链与之后的 C6.2 稿件重写；不是“论文创新性对所有审稿人已成立”，也不是C6阶段PASS。
- **必须落实**：①将21–23% DEV开关重分配和新/弃调用平均增益落实成合理解释；②H1无strict equal-call判断与H2 floor须在投稿稿件中保持醒目；③强source identity×gate交互主张删除；④修改旧Discussion和Abstract用语前先定义exact claim text；⑤新C6 scientific guard替换过时的C5 prefix/suffix冻结，并双PDF构建后才能C6整阶段PASS。
- **停止条件**：如C6.2改写只能剩下“train F, test F优于S”而没有决策后果机制和源有效性，请退回科研定位审查；不得靠更多形容词装成新理论。

## 7. 冻结证据与直接可查链接

- 现行论文主稿：manuscript/kbs_latex/main.tex（Results RQ2/RQ3）
- N12-C5最终QA：manuscript/kbs_latex/N12_C5_RQ_RESULTS_EVIDENCE_LANDING_EDITORIAL_QA_2026-10-16.md
- B1相同用户分组nested DEV报告：experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md
- B2知识源组成及6/12特征敏感性：experiments/kbs_plan_c/B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md
- G2/E1真实选择事件差异分解：manuscript/kbs_latex/N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md
- G2可公开机器聚合：experiments/kbs_plan_c/N9_G2_E1_SUPERVISION_DECISION_SWITCHES_PUBLIC_AGGREGATE_2026-10-13.json
- C5原始Results冻结fixture：analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json

**执行声明**：未触达/解封私有原TEST，未训练新模型，未变更阈值、数据或CI，未修改main.tex；该独立审查记录本身不构成新统计结果，也未获得责任作者签署。