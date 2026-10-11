# KBS 八章独立复审：逐段主张、章节职责及学术语体矩阵

**日期：2026-10-11；状态：审查已完成，未经允许未改动主稿。**

- 原始文件：`main.tex` blob `fa73ba31a56edd96f6eeaca272214b98bf4a9a9d`，共 94 个可以审查的正文文本单元（公式、表、图、引言 contribution itemize 另列保护）。以旧代码行号加段落 ID 定位；执行改写后必须更新锚点。
- 优先级：**P1 23，P2 35，KEEP 36**。P1 是**投稿论证优先级**，并不表示实验错误。正文未直接改动，既有 §1–§8 和 S1–S9 原数据在本轮继续冻结。
- 核查依据：[权威大纲](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md)、[KBS 官方范围](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)、[Elsevier Results/Discussion 写作指导](https://scientific-publishing.webshop.elsevier.com/publication-process/how-to-write-a-journal-article-from-a-thesis/)。

## 与上一轮主观评估相比，经原文核查后作出的纠正

1. **八章主结构及第六章 C1→C3→C2 顺序已经与大纲一致；“整篇论文没有主线”是过度概括。** 真正缺口是对最接近研究的差异论证较弱、§6 辅助诊断主次不鲜明和 §7 科学解释与结果复述的区别不够清晰。
2. **章节过多不是独立问题**。§3–§5 的小节与正式定义或复现协议存在必要对应关系，不可强行并章；§2、§7 的短小节优先考虑语义合并。
3. **“很多限定词=不符合学术规范”不成立**。不可删 target-label 事后性、Twitch DEV frozen、Difficulty TEST equal-count、KuaiLive evaluated-cohort、candidate decomposition 非独立因果、正向 CPU overhead。可以压缩的是这些限定跨节重复出现时的过程性叙述。
4. **文献边界是真实投稿风险而非创新点缺失定论**。ACL 2026 MemRec、AAAI 2026 GUIDER、ICML/NeurIPS L2D、CACM 2022 sampled-metric 研究早已存在。本稿创新应是固定关系知识专家的 incumbent-relative operational value 与实证条件/决策选择的交叉，不可称差值函数或一般 defer 理论首次提出。

## 汇总

| 章 | 文本单元 | P1 | P2 | KEEP |
|---|---:|---:|---:|---:|
| §1 | 6 | 3 | 2 | 1 |
| §2 | 6 | 3 | 3 | 0 |
| §3 | 17 | 0 | 6 | 11 |
| §4 | 12 | 0 | 7 | 5 |
| §5 | 13 | 0 | 6 | 7 |
| §6 | 26 | 10 | 7 | 9 |
| §7 | 11 | 7 | 4 | 0 |
| §8 | 3 | 0 | 0 | 3 |
| **合计** | **94** | **23** | **35** | **36** |

## 逐段可执行映射

| 单元 | 旧行号 | 原小节 | 级别 | 编辑动作及科学理由 |
|---|---:|---|---|---|
| S1-P01 | 33 | Introduction | P1 | 与下一段重复研究缺口；以强 Base 下关系知识冗余/互补形成张力 |
| S1-P02 | 35 | Introduction | P1 | 将已有融合研究真正缺少的决策对象写清，不再复述 P01 |
| S1-P03 | 37 | Introduction | P2 | 压缩重复问题陈述与过早的证据层级解释 |
| S1-P04 | 39 | Introduction | P1 | 由研究问题引出两条互补证据链；避免像结果预告和流程概述 |
| S1-P05 | 41 | Introduction | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S1-P06 | 47 | Introduction | P2 | 压缩重复问题陈述与过早的证据层级解释 |
| S2-P01 | 53 | Sequential and Long-Horizon Recommendation | P2 | 收紧已有研究比较；少分类罗列 |
| S2-P02 | 57 | Auxiliary Evidence Integration and Reliability | P1 | 重点比较已发表 MemRec/知识融合的知识表示目标与操作效用评价 |
| S2-P03 | 59 | Auxiliary Evidence Integration and Reliability | P2 | 收紧已有研究比较；少分类罗列 |
| S2-P04 | 63 | Expert Routing and Learning-to-Defer | P1 | 将 L2D、post-hoc deferral、GUIDER 的相近性作为实质对话，避免只列名字 |
| S2-P05 | 67 | Live-Streaming and Repeat-Aware Recommendation | P2 | 收紧已有研究比较；少分类罗列 |
| S2-P06 | 71 | Research Gap | P1 | 研究缺口精确回应既有 sampled-metric 结论与增量知识使用决策的区别 |
| S3-P01 | 76 | Problem Formulation | P2 | 保留数学定义，压缩与方法重复的衔接/重复限定 |
| S3-P02 | 81 | Recommendation Setting and Event-Level Ranking Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P03 | 83 | Recommendation Setting and Event-Level Ranking Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P04 | 92 | Recommendation Setting and Event-Level Ranking Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P05 | 97 | Base-Relative Specialist Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P06 | 102 | Base-Relative Specialist Utility | P2 | 保留数学定义，压缩与方法重复的衔接/重复限定 |
| S3-P07 | 104 | Base-Relative Specialist Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P08 | 109 | Conditional Relative Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P09 | 115 | Conditional Relative Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P10 | 117 | Conditional Relative Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P11 | 124 | Conditional Relative Utility | P2 | 保留数学定义，压缩与方法重复的衔接/重复限定 |
| S3-P12 | 126 | Conditional Relative Utility | P2 | 保留数学定义，压缩与方法重复的衔接/重复限定 |
| S3-P13 | 131 | Selective Invocation and Equal-Count Comparison | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P14 | 136 | Selective Invocation and Equal-Count Comparison | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P15 | 138 | Selective Invocation and Equal-Count Comparison | P2 | 保留数学定义，压缩与方法重复的衔接/重复限定 |
| S3-P16 | 143 | Regime-Level Utility Decomposition | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S3-P17 | 150 | Regime-Level Utility Decomposition | P2 | 保留数学定义，压缩与方法重复的衔接/重复限定 |
| S4-P01 | 156 | Base-Relative Evidence Valuation Framework | P2 | 保留组件实现，优化公式/系统流程的对应关系 |
| S4-P02 | 187 | Strong Sequential Base Recommenders | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S4-P03 | 189 | Strong Sequential Base Recommenders | P2 | 保留组件实现，优化公式/系统流程的对应关系 |
| S4-P04 | 194 | Transparent Relationship-Memory Specialist | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S4-P05 | 196 | Transparent Relationship-Memory Specialist | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S4-P06 | 205 | Transparent Relationship-Memory Specialist | P2 | 保留组件实现，优化公式/系统流程的对应关系 |
| S4-P07 | 210 | Base-Relative Relationship-Evidence States | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S4-P08 | 221 | Base-Relative Relationship-Evidence States | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S4-P09 | 226 | Observable Features and Conditional Relative-Utility Estimation | P2 | 保留组件实现，优化公式/系统流程的对应关系 |
| S4-P10 | 228 | Observable Features and Conditional Relative-Utility Estimation | P2 | 保留组件实现，优化公式/系统流程的对应关系 |
| S4-P11 | 233 | Specialist Selection and Matched-Budget Controls | P2 | 保留组件实现，优化公式/系统流程的对应关系 |
| S4-P12 | 235 | Specialist Selection and Matched-Budget Controls | P2 | 保留组件实现，优化公式/系统流程的对应关系 |
| S5-P01 | 241 | Experimental Setup | P2 | 完整保留关键复现协议，减少多处介绍同一信息 |
| S5-P02 | 247 | Datasets and Prediction Tasks | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S5-P03 | 249 | Datasets and Prediction Tasks | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S5-P04 | 252 | Datasets and Prediction Tasks | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S5-P05 | 273 | Baselines and Compared Methods | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S5-P06 | 275 | Baselines and Compared Methods | P2 | 完整保留关键复现协议，减少多处介绍同一信息 |
| S5-P07 | 300 | Experimental Protocols | P2 | 完整保留关键复现协议，减少多处介绍同一信息 |
| S5-P08 | 303 | Experimental Protocols | P2 | 完整保留关键复现协议，减少多处介绍同一信息 |
| S5-P09 | 311 | Experimental Protocols | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S5-P10 | 317 | Experimental Protocols | P2 | 完整保留关键复现协议，减少多处介绍同一信息 |
| S5-P11 | 322 | Evaluation Metrics and Statistical Analysis | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S5-P12 | 324 | Evaluation Metrics and Statistical Analysis | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S5-P13 | 329 | Implementation Details | P2 | 完整保留关键复现协议，减少多处介绍同一信息 |
| S6-P01 | 334 | Experimental Results | P2 | 保留真实结果，将方法/种子/额外诊断明细在主文与 S1–S9 间合理分工 |
| S6-P02 | 339 | Heterogeneous Utility of Relationship Memory | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P03 | 341 | Heterogeneous Utility of Relationship Memory | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P04 | 343 | Heterogeneous Utility of Relationship Memory | P2 | 保留真实结果，将方法/种子/额外诊断明细在主文与 S1–S9 间合理分工 |
| S6-P05 | 398 | Decision Value of Predicting Relative Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P06 | 400 | Decision Value of Predicting Relative Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P07 | 402 | Decision Value of Predicting Relative Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P08 | 404 | Decision Value of Predicting Relative Utility | P1 | selected/unselected 条件均值属于原测试的辅助描述，原则上移 S7 |
| S6-P09 | 406 | Decision Value of Predicting Relative Utility | P1 | DEV 状态富集作为辅助诊断，合并为支持相对收益预测的一句解释 |
| S6-P10 | 408 | Decision Value of Predicting Relative Utility | P2 | 保留真实结果，将方法/种子/额外诊断明细在主文与 S1–S9 间合理分工 |
| S6-P11 | 432 | Candidate-Regime Dependence of Relative Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P12 | 434 | Candidate-Regime Dependence of Relative Utility | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P13 | 452 | Candidate-Regime Dependence of Relative Utility | P2 | 保留真实结果，将方法/种子/额外诊断明细在主文与 S1–S9 间合理分工 |
| S6-P14 | 454 | Candidate-Regime Dependence of Relative Utility | P1 | 训练种子方向性在主文合并报告，细表留 S8 |
| S6-P15 | 456 | Candidate-Regime Dependence of Relative Utility | P1 | 固定 checkpoint 上九个采样 draws 与 P14 合并，细表留 S5 |
| S6-P16 | 458 | Candidate-Regime Dependence of Relative Utility | P2 | 保留真实结果，将方法/种子/额外诊断明细在主文与 S1–S9 间合理分工 |
| S6-P17 | 463 | Robustness and Alternative Explanations | P1 | §6.4 开头明示两项科学解释任务而不是诊断实验导航 |
| S6-P18 | 465 | Robustness and Alternative Explanations | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P19 | 484 | Robustness and Alternative Explanations | P1 | 局部专家参数网格压缩为一项稳健性发现，证据留 S4 |
| S6-P20 | 486 | Robustness and Alternative Explanations | P1 | Long-only/Full tradeoff 服务信息互补解释，减少数值/流程积累 |
| S6-P21 | 488 | Robustness and Alternative Explanations | P1 | 不同 Base 历史窗口分别训练，不将共变误说成历史长度单独因果效应 |
| S6-P22 | 490 | Robustness and Alternative Explanations | P1 | 回归距离事后分组结果主要留 S6，主文只保留与 C1 的联系 |
| S6-P23 | 492 | Robustness and Alternative Explanations | P1 | 以关于信息冗余/互补的判断收束 §6.4，少重复全篇口号 |
| S6-P24 | 497 | Computational Considerations | P2 | 保留真实结果，将方法/种子/额外诊断明细在主文与 S1–S9 间合理分工 |
| S6-P25 | 499 | Computational Considerations | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S6-P26 | 501 | Computational Considerations | P2 | 保留真实结果，将方法/种子/额外诊断明细在主文与 S1–S9 间合理分工 |
| S7-P01 | 509 | Operational Value Is Base- and Context-Dependent | P1 | 从结果重复上升到知识互补的可解释科学认识 |
| S7-P02 | 511 | Operational Value Is Base- and Context-Dependent | P1 | Base 训练变化和长/短期组件作为机理旁证，避免重报数字 |
| S7-P03 | 516 | Interpreting Conditional Evidence and Candidate Regimes | P2 | 主文解释优先，重要证据界限保留一次 |
| S7-P04 | 518 | Interpreting Conditional Evidence and Candidate Regimes | P1 | 明确已知 sampled metric 与固定关系知识专家价值解释的边界 |
| S7-P05 | 523 | From Relative Utility to Selective Decisions | P1 | 解释专家增量机会与 Base 困难请求的目标不等价 |
| S7-P06 | 525 | From Relative Utility to Selective Decisions | P2 | 主文解释优先，重要证据界限保留一次 |
| S7-P07 | 527 | From Relative Utility to Selective Decisions | P1 | 针对 L2D、post-hoc 和 GUIDER 进行真正文献对话 |
| S7-P08 | 532 | Validity Boundaries | P2 | 主文解释优先，重要证据界限保留一次 |
| S7-P09 | 534 | Validity Boundaries | P2 | 主文解释优先，重要证据界限保留一次 |
| S7-P10 | 539 | Implications for Knowledge-Based Recommendation | P1 | 不重复 C1–C3 摘要，形成学科层面有条件的知识使用原则 |
| S7-P11 | 541 | Implications for Knowledge-Based Recommendation | P1 | 压缩 Future Work 清单；与 §7.4 归位成本与适用范围 |
| S8-P01 | 546 | Conclusion | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S8-P02 | 548 | Conclusion | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |
| S8-P03 | 550 | Conclusion | KEEP | 保留：承担现有定义、核心证据或关键复现职责；最后核对与全文论点一致性 |

## 非普通段落的冻结资产

- Intro C1–C3 项目符号贡献列表：范围保留，不称新一般 L2D 定理或 sampled ranking 首次发现。
- §3 全部公式、§4 Memory 固定系数及 14 个 pre-outcome 特征、Figure 1，以及 §5 TEST/DEV 拆分与比较器信息访问：**必须保留正确科学意义**。
- §6 Twitch 冻结 TEST（44,221）与 KuaiLive 固定事件候选环境配对（10,222），全部主结果、CI、主要图表与 S1–S9 provenance：**不重新编造数值、不移动到新独立 TEST**。
- CPU Base 0.991ms、selective 2.007ms 的**正向时间开销**、独立 HGB/replay 条件不能被改写成服务加速。
- 已收紧 §8 结论原则上保持稳定，Abstract 暂未写；最终 KBS 专门投稿要求与作者声明另行处理。

**修订执行工作流：** [第二轮正文主线优先修订计划](KBS_PAPER_SECOND_PASS_SUBMISSION_NARRATIVE_REVISION_PLAN_2026-10-11.md)。每次修改要记录 `旧段落 ID→新位置/合并/转 S→差异证据→审稿验收`，不能仅通过否定词减少量评价“学术质量”。
