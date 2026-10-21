# N12 Rev2.2 E1 | 最近邻先例—单一实证贡献对照审查

**2026-10-20 | E1 ANALYST SOURCE REVIEW COMPLETE, HIGH SCIENTIFIC NOVELTY RISK RETAINED; 真实独立学者未签署。** 没有修改论文正文、References、Supplement或任何冻结实验；E0来源矩阵为输入。

## 一句可以保留的贡献主张

在固定Base与历史关系Memory专家、明确的完整候选环境中，**相同知识专家的增量效用标签因离线候选协议而异；既有同队列DEV的请求调用换位以及独立封存但同采集期的30k完整候选政策比较，进一步揭示该标签差异怎样传递到实际知识使用决策与其排名结果。** 对照仅指原始未经统计校正、目标后保留的575-candidate S；不构成算法理论首创、严格等calls因果识别、独立未来时段复现、线上资源收益。

## 最近邻研究的真实范围

| 首要先例（核验原文摘要） | 先例已经回答 | N12补充的具体实证对象 | 不能推广的边界 |
| --- | --- | --- | --- |
| Krichene & Rendle, KDD2020, *On Sampled Metrics for Item Recommendation* (https://research.google/pubs/on-sampled-metrics-for-item-recommendation/) | sampled ranking metric不保持full相对model ranking；提出bias/MSE修正 | 学习**哪条离线相对Memory−Base监督**，及其如何影响预目标专家调用和冻结完整候选政策 | 采样不一致/指标纠偏非本文新理论；RQ1并不单独保证可投稿创新 |
| Subbiah, Rendle, Aggarwal, CIKM2024, *Improved Estimation of Ranks for Learning Item Recommenders with Negative Sampling* (https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/) | 负采样训练WARP/LambdaRank时排名估计及校正 | 原S与F的**配对条件效用**及调用决策；V2发现MSE不等于政策损失 | 合理sampled-only corrected-S训练后的政策未验证；不能宣称校正类方法失败 |
| Mao, Mohri, Zhong, ICML2024 *Regression with Multi-Expert Deferral* (https://proceedings.mlr.press/v235/mao24d.html) | 预训练专家、分阶段学习、实例相关cost和专家委托理论 | 一个实际的历史关系知识源、动态作者候选、完整排名效用标签与冻结Policy组成的具体证据链 | 相对收益/defer/预算阈值均非新算法或通用决策理论 |
| Qian et al., arXiv:2607.24010, 2026-07-27 *When Should Active RAG Retrieve? A Budget-Aware Evaluation of Utility, Calibration, and Cost* (https://arxiv.org/abs/2607.24010) | 边际检索效用、realized usage与名义预算区别、阈值偏差、trigger cost分解 | 非生成式任务里的历史关系Memory对**当前动态完整候选排序**的相对价值标签与调用重新分配 | 预印本（当前不标正式期刊/会议已发表）；N12缺乏新版F门控真实端到端成本与服务quota依据，不能称首创边际调用价值 |

## 三个必须可反驳的KBS科研问题

1. **“已知采样指标失真+已知deferral为何不是拼装？”** 可检验新增事实：原50,049 DEV下21.32%/23.01% **请求决策**换位，且换入平均Memory value更高；原同期间30k已封存F/S完整策略结局。旧G2分解是代数身份，无独立机制因果推断；该组合是否构成足够创新仍标**HIGH/HUMAN REVIEW**。
2. **“只是不同阈值和更宽松预算？”** 同30k SAS +.005391 NDCG且F少401调用，GRU +.003585且F少539调用，为**observed F/S frozen policy operating points**；仍不满足原1pp近等调用（差1.337/1.797pp），不能证明纯标签或同资源一般规律。
3. **“只比较弱S，不比较Always Memory、已纠偏S？”** 无约束Always Memory更准；corrected-S训练策略未跑；V2方法诊断不能否定别的校正器。论文只能论述受显式外部quota限制时的请求分配，在具体原始S对照上取得优势，未验证实时成本节约。

## E1证据和正文审核结论

当前Intro lines 37–51与Discussion 603–608已经说明“固定知识源增量效用→候选制度监督→调用分配”，并且自己否定新deferral/sample metric theorem。因此**不建议大改Introduction标题或重写contributions**。真正增益来自E2把两组同30k F更高质量且调用更少的已知运行点表述得更易审阅，并在E3明确预算仅属外部约束以及RQ3图文措辞风险。若后续审阅确定已有句子充分，则E4不应重复插入同一限制。

**裁决：E1 ANALYST_PASS_FOR_PRECISE_CONTRAST, NOVELTY_HIGH_CONTESTABLE**。不是审稿人接受、不是新的理论创新，独立人审E6仍需判定。进入E2/E3时仅审查原结果和source、不重跑模型。