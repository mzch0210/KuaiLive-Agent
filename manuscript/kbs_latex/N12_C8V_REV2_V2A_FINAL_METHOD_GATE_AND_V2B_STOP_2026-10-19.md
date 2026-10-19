# N12 C8V Rev2 — V2a 方法选择裁决及 V2b 停止记录

**日期：2026-10-19。裁决状态：ANALYST_METHOD_GATE_COMPLETE / V2B_NOT_RUN_BY_DESIGN_FOR_CURRENT_CANDIDATES / INDEPENDENT_METHODS_REVIEW_PENDING。** 本裁决不等于所有可能的 corrected-S 在理论或实践上无效，也不等于已接受或完成 external peer review。不改动主稿、补充材料、冻结原 TEST/B4-A，也不新增策略训练。原 KBS PR #6 保持 Draft。

## 1. 为什么当前科学问题与 prior art 并非同一个估计对象

本稿固定前结果特征 `Z`、完整候选 `F`、训练好的 Base `B` 和历史专家 `M`，关心 `eta_F(Z)=E[u_10(M;F)−u_10(B;F)|Z]` 对 **预目标调用位置**及完整F排名价值的影响。

- Krichene & Rendle, KDD 2020, *On Sampled Metrics for Item Recommendation*: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ 。强调sampled top-K ranking metrics不保全量模型间排序，提出按照bias/MSE改善**采样指标估计**，不证明本项目单事件`eta_F(Z)`校正或策略等预算效应。
- Subbiah, Rendle & Aggarwal, CIKM 2024, *Improved Estimation of Ranks for Learning Item Recommenders with Negative Sampling*: https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ 。为WARP/LambdaRank训练提供改进ranking estimates；一般训练时rank correction已有先例，但其方法及结论不能作为N12的新方法首创，也不能未经推导直接移植成基于575抽样、单正例Top10的Memory−Base条件监督。
- Mao, Mohri & Zhong, ICML 2024, *Regression with Multi-Expert Deferral*: https://proceedings.mlr.press/v235/mao24d.html 。已有pretrained incumbent加专家委托、instance-dependent cost和学习选专家理论。故N12不能以“新`Delta`/新selective invocation算法”主张创新。
- Mandi et al., JAIR 2024, *Decision-Focused Learning*: https://mlanthology.org/jair/2024/mandi2024jair-decisionfocused/ 。预测目标与下游决策不一致是成熟领域。N12的差异只在固定历史关系知识源、实际候选协议、从监督差异到请求级调用重新配置的具体实证联系。

## 2. 已有事实及诊断：同一DEV不是独立新增TEST

| 检验层 | 原执行与核心观察 | 允许结论 / 不允许结论 |
| --- | --- | --- |
| B1原三臂 50,049 DEV、同 cohort | S→F/F→F/Adapted→F；SAS 0.296499/0.302658/0.301847；GRU 0.298123/0.303093/0.303000；run #38365477972 | 证实已有的训练策略差异；Adapted使用F训练标签**不是sampled-only校正**；不重复相同三臂 |
| selfhost私有源、128抽查 F/S parity | 50,049私有源 SHA通过（#39230682113），128原DEV事件两套评分器+Memory F/S全部0标签差异（#39232305650） | 说明可以从原源重建；不是新训练或新TEST |
| 合成单专家与联合差异 | #39235271548、#39236652772，评价指标与joint Delta可得出不同方法排序 | 可以否定“单专家MSE改善足以推出joint/selector改善”；不能推出所有校正器不可能 |
| 50,049既有 DEV 逐事件joint label诊断 | #39237415095，两job PASS，F/S SHA匹配，full N 14,022–53,762，zero sampled monotonicity violations | 固定后验比较，**不属于独立确认**，也没有训练选择器或调TEST |

既有DEV真实 `Delta_F=u_F(M)-u_F(B)` 标签核对如下：

| 候选方法 | SAS joint Delta MSE | GRU joint Delta MSE | SAS sign-only toy regret | GRU sign-only toy regret | 裁决 |
| --- | ---: | ---: | ---: | ---: | --- |
| 原始未校正S | 0.154547688 | 0.156083555 | 0.072524733 | 0.072382293 | 原已完成对照，复用 |
| `rank_expansion` | **0.193363048** | **0.193387100** | **0.074677682** | **0.074585882** | 平均有符号bias接近零，但逐事件paired MSE和toy regret更差；**拒绝作为自动V2b默认方法** |
| `uniform_prior_posterior` | 0.082977598 | 0.087528999 | 0.072524733 | 0.072382293 | MSE有改善，但未经验证均匀全量rank先验、平均Delta严重向零收缩、toy regret不改善；**不批准为具有科学解释力的corrected-S方法** |

Toy sign-only gate以`estimated_delta>0`即调用，**不限制Memory预算、不拟合真实pretarget Z、不按用户组训练**，不是原B1实际30% capped selector。不应选用toy sign准确率、toy regret或上述joint MSE表现来宣称有更佳DEV/TEST的**冻结策略**。

## 3. 停止当前V2b的充分方法学理由（不是“corrected-S皆无效”）

- 目标对象首先是`eta_F(Z)`及受限决策配置，而非总体排名指标或单个评分器的MSE；现成两方法没有提供条件效用一致性保证、独立可验证的先验约束或可用的预算策略推导。
- `rank_expansion`针对采样排名`R_hat=1+(N−1)X/574`的线性校正，对非线性截断`u_10(R_hat)`没有逐事件无偏性；在真实既有DEV的joint loss/zero-cost toy regret均比原S差。
- `uniform_prior_posterior`人为令full rank在1..N均匀，没有有效的数据产生机制支撑（尤其两评分器采样负例**共享**、ranking overlap影响Delta误差的联合结构）。缩小MSE可能仅表示shrinkage，原toy regret未改善。
- 早期`regime_adapted_to_full`已用全量F训练标签；它不是“不知道F标签的sampled-only corrected-S”替代。
- 50049 DEV之上继续尝试大量参数及选择赢家，会加重同一已探索cohort上的方法选择偏差，不产生独立统计复现；不能转而使用已揭盲B4-A 30000 TEST挑选校正公式。

**因此当前已具体提出并测试的两种correction candidates → V2b = NOT_RUN_BY_DESIGN；理由 = NO_SCIENTIFICALLY_VALID_AND_DECISIVE_CONDITIONAL_POLICY_ESTIMATOR_IDENTIFIED。** “未排除一切合理校正后S接近F的可能性”仍属于必须在文稿中披露的外部竞争解释，不能写成“corrected-S rejected by experiments”。

## 4. 什么情况才能重新打开V2b？

只有后续有**不同于原B1/当前两种启发式**、数学定义完整且目标可解释的估计器，才可提出新的单独申请。申请需包括：(i) `eta_F(Z)`或可以明确连接它的paired conditional risk估计目标；(ii) 使用信息合同（只用S抽样标签、N、pretarget Z、训练折内估计先验时是否引入额外F labels），并和已完成F-assisted Adapted区别；(iii) Base/Memory**共享同一采样候选**下的联合误差及stop condition；(iv) **不使用G5/B4-A已揭盲TEST调参**；(v) 在DEV上预先固定user-group nested folds、政策calibration、自然calls/匹配调用资源的解释；(vi) 非零科学增量假设及可靠独立人审签。否则不存在自动继续训练的责任。

## 5. I2衔接与论文当前边界

当前37页主稿已将证据对象写为“tested sampled-candidate S”并承认严格等调用未识别，但**尚未显式说明corrected-S这个现实替代解释并未做政策检验**，近邻CIKM2024 rank-correction文献是否已覆盖亦需另核引文。I2应先完成修改点核查，仅对必要句子提出小范围修改：

- Related Work / Discussion：说明sampled metric consistency与训练时sampled rank correction均为先例，不将N12描述为统计校正算法。
- RQ2/Discussion：界定与**original uncorrected target-retained S**政策比较；保留已完成三臂`Adapted→F`使用F标签的区别，审稿人不能误以为第三臂是合法corrected-S。
- Limitations：认可一种适合paired conditional utility的有效correction**或许**会缩小F与S差异，目前没验证，也未宣称不可能。
- 不搬入全部50,049 DEV校正方法后验数据到论文主Results当作新独立发现；作为内部稳健性审计/可解释风险记录即可，是否在Supplement引用需作者评估。
- 不改变原冻结政策质量、用户cluster CI、H2限界、11张原Results表、原公式或原C6/7数字合同。

**推荐论文路径：A — evidence-bounded empirical KBS evaluation of candidate-regime-indexed knowledge-use labels**。作者/真实独立同行科学审阅**未签署**；I2接下来先写出精确改稿建议（no broad restructuring），再由作者确定是否实际修改并提交最后QA。PR仍Draft，未投稿。
