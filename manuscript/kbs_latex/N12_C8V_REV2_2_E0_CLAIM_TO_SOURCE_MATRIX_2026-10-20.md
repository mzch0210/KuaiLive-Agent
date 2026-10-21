# N12 Rev2.2 E0 | 论文论点—原始证据位置矩阵（2026-10-20）

**状态：E0 PUBLIC-REPOSITORY SOURCE-TO-CLAIM AUDIT COMPLETE；独立人工科研审阅未签署。** 本报告通过GitHub读取当前 `main.tex` blob `c713811acf5c6c47df3e5cb34ee8a7af5cc4ff5e`、Rev2.2新计划、I0的14个证据对象总账及N9原DEV报告；本次未读取私有原始事件或重跑TEST，不制作新估计或CI。上一轮完整PDF真实成功为C8V #39351014765与C7 #39351014645，38p主文/47p补充材料；**不是**Rev2.2新编译。

| 主张/审稿质疑 | 当前主文定位 | 直接来源（原已完成） | 正确统计总体与最大可说结论 | E0裁定和建议 |
| --- | --- | --- | --- | --- |
| 中心对象 | Intro lines 37–52; Section3 110–213; Discussion 603–608 | C6 fixed equations; Krichene KDD2020和Mao ICML2024 | 固定Base、Memory、完整F：增量NDCG是已有定义方式而非新理论 | **ALREADY_BOUNDED**，不要重写为新算法；E1差异矩阵需具体对照 |
| Twitch complementarity | Results 384–418 | I0 RQ1_TWITCH；P1.3 success [#35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303) | 44,221 frozen streamer events；recoverable 5,539是**结果后定义**，不作为预测器事前特征 | PASS，保存来源和单列研究单位 |
| KuaiLive room候选变化 | Results 421–442 | same-checkpoint room [#37746520476](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476)、factorial [#37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645) | 10,222以前已检查room-ranking事件，same checkpoint换候选协议的关联结果；候选身份和大小交织 | PASS，**不等同M3作者任务，不写为样本量单一因果效应** |
| 原始M3基线 | Results 385–387；Methods 264、291–318 | G5_ORIGINAL_M3_POLICY账目 | 47,575个原M3 TEST事件，六fit使用同一TEST队列，不是六个独立TEST | PASS，防6次独立性的错读 |
| G2监督改变实际调用 | Discussion 613–615, Intro contribution line 50 | 50,049 DEV/12,628 users；G2 run [#38389150075](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38389150075) | 10,672/11,517 requests切换（21.32%/23.01%）；两个换入/换出组均有正的平均Memory增益；纯代数policy分解，不是因果新定理/独立验证 | **E2核心解释来源**；不要把21%视为Memory调用份额或独立30k效果 |
| RQ2冻结政策质量+调用 | Results 513–536；Table B4-A 526–527 | B4A_H1_NEW_EVENT_ID_SUPERVISION账目、既有B4-A原H1报告 | 30,000额外**同记录期** event IDs；SAS NDCG F/S .305446/.300055且calls 8704/9105；GRU .304530/.300945、calls 8629/9168；分别+0.005391/+0.003585，95% CI和Holm按既有报告 | **E2强化“同一次冻结运行点，质量更高且Memory calls更少”**，强调非严格等调用、不是总体cost/新预算前沿 |
| 预算差和选择器成本 | Results 573–599；Discussion 617、626 | N9_A1_EIGHT_BUDGET_FRONTIER（DEV）；N10_C2B_LEGACY_DEVICE_PATH | SAS/GRU H1 F/S realized calls差1.337pp/1.797pp >1pp；Always Memory额外30k NDCG .348744 >F门控SAS .305446；旧pointwise Utility测得延迟不利，新vectorized门控成本未测 | **ALREADY_DISCLOSED**，E3仅整合；绝不可改为真实吞吐/成本收益 |
| RQ3历史Null | Results 537–572；Discussion 622 | B4A_H2_NESTED_HISTORY_NULL账目 | 4,096嵌套于同30k，三seed同样本；authentic−Null +.031145；联合扰动历史结构；original TRAIN-only Popularity prereveal子门槛 **NOT VERIFIED** | **E3明确文字风险**：Fig RQ3 line 74写“valid historical nulls”，与部分未验证前置条件不完全相容；建议改为“constrained historical randomizations”，保留原图其他项 |
| corrected-S竞争解释 | Related Work line 100; RQ2 line 514; Discussion 624 | 原B1三臂；V2自托管[#39232305650](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39232305650)、50,049 DEV标签诊断[#39237415095](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39237415095) | 原S未校正且目标后保留575；Adapted用F标签；两简单校正并非训练后合法corrected-S政策，不能排除其它条件效用校正 | **ALREADY_FIXED_BY_REV2.1**：不要再重复增加限制。 |
| 可外推性与目标选择偏差 | Methods 267–288; Discussion 624–626 | G5/B4-A原始分割协议 | 额外IDs不等于未来独立期间，可能共用户/历史；离线观测正例受到先前曝光决策 | PASS，别加未经验证的IPS/线上改善 |
| 投稿原创性与人类审阅 | Discussion 603–608; I2-D包 | KDD2020, CIKM2024, ICML2024; I2-D内审报告 | KBS可能关注知识系统与决策支持，但采样修正、defer和相对价值本身已有基础 | **OPEN_HIGH_NOVELTY_RISK**；E1必须逐项先例差异审查，E6真正人审不能用AI代签 |

## 已存在材料去重

- Rev2.1已经新增CIKM2024引用、原S未经校正说明、corrected-S尚未检验限制；它们是 **DONE**，非Rev2.2要重做。
- N9 A1八预算已有原DEV聚合结果，不要重做预算扫描或在同30k混画“新全局Pareto前沿”。
- N9 G2已完成同一50,049 DEV的调用决策切换代数分解；不用新训练再验证这个恒等式。
- 图Fig1“valid historical nulls”是本轮找到的**明确待校正修辞风险**；不等于声称原论文所有Null指标均失败。应该具体限定而不是把RQ3整体删除。
- 原V2 50,049标签诊断不能上升为新增独立TEST或新trained policy。

## E0完成与E1入口

**E0裁定：PASS_SOURCE_MAPPING_WITH_ONE_WORDING_RISK_OPEN**。本次仅核对公开版本/先例来源，对冻结原始统计的历史QA复用既有通过记录，不声称逐原始行重新验算。本轮不改论文科学源码；下一阶段E1对四项先行研究产生“已有方法 vs 本文额外的实证对象 vs 残余缺口”矩阵，随后E2同cohort质量−调用联合审计及E3负面边界。E0报告不是外部同行认可。
