# N12-C8V Rev2.2 | Path A 科学贡献与审稿说服力提升计划

**制定：2026-10-20｜类型：PLAN ONLY｜执行优先级：Path A 科学论证增强后开展真实独立学术审阅｜当前未执行正文改稿。**

## 0. 本轮计划的确定前提与适用范围

**论文源与技术基线**：GitHub \`mzch0210/KuaiLive-Agent\` 分支 \`kbs-n12-single-thesis-restructure-plan-20261014\`；I2最小编辑科学提交 \`7e4c5a6f616e22226f55e2396815d48cc838bf96\`，\`main.tex\` **38 页**、完整Supplement **47 页**，真实CI \`#39351014765\` 与 \`#39351014645\` 双job均PASS；原I2-D **内部**科学审阅已完成，**真实独立人类科研审阅没有签署**，责任作者未签最终GO，KBS未投稿。当前源码经后续治理提交仍保持同一科学内容。本文方案不得把Rev2.2计划文件提交当作新论文CI。

**用户研究路线**：仍是用户明确选择的 **Path A：以已有可靠实证为核心，论证清晰且承认局限，不以新增实验追求伪理论创新**。Rev2.1已修订Related Work的CIKM2024先例、RQ2原S的uncorrected定义、Discussion corrected-S开放竞争解释；**不要把已经完成的这三处写成待执行任务**。保留I0原始证据总账和完整多轮N8/N9/N10/N11/N12历史。Rev2.2不是重新写论文、生成第四个RQ或开启下一轮方法竞赛。

**约束**：不解封/重评分G5或B4-A原TEST，不以已揭盲30k挑新策略/阈值，不重训B1三臂、不重做B2五来源、G1 source×candidate、A1八预算、A2 Direct/Two-stage、G2 switch分析、不重试H2伪事前验收、不重新解释原统计总体，不作在线收益/端到端成本/新时间泛化声称。允许**只读复用已经发表在本仓库报告的聚合结果与LaTeX**，不制造补充p值或“matched-call CI”。论文正文的修改在E4阶段才开始，全部要经过E5的真实双PDF和科学守卫。

## 1. 科学定位：应该增强什么，而非重新声称什么

**中心主张：** 对固定外部历史关系Memory专家和指定Base，\`Δ_F(x)=u_10(M;x,F)-u_10(B;x,F)\`由当前可选集合定义；训练时用不同候选协议形成的 **离线增量效用标签**会改变有限外部知识调用的*具体请求配置*及其完整候选冻结策略表现。论文实证的政策对照严格限于 **F vs 原始未校正、目标后保留的575-candidate S**；RQ3是一条同一固定专家的**平行、复合历史来源敏感性证据**，并非RQ2机制的特异性因果证明。

**现有最强证据，必须保持原估计对象**：
- RQ1 Twitch \`44,221\` one-shot streamer ranking（\`#35708072303\`）与早期KuaiLive \`10,222\`既有room ranking固定checkpoint F/S对比（\`#37746520476\`，factorial \`#37751814645\`）。这不是M3 author task，亦不能隔离候选数量效应。
- RQ2 50,049请求/12,628用户**共同探索性DEV**：B1原S/F/Adapted三臂及G2调用差异，SAS \`10,672/50,049=21.32%\`、GRU \`11,517/50,049=23.01%\`不同请求调用；G2显示两个被交换群平均Memory相对效用都为正，解释是**有限调用重新排序**而不只是规避负效用。
- 主要冻结H1：额外 **30,000未评分事件ID、同一采集期间而非独立未来时段**；SAS F−S \`+0.005391\` 95%CI \`[+.003646,+.007174]\`，GRU \`+0.003585\` CI \`[+.001599,+.005576]\`；SAS F/S calls \`8704/9105\`（F少401），GRU \`8629/9168\`（F少539）。**仅在这两个实测冻结完整政策运行点上**F同时有更高NDCG和更少\`Memory\`调用。两方法natural calls差\`1.337/1.797\`个百分点，超过预设1pp近等调用容忍；不得叫严格等资源因果优势、完整Pareto前沿或实际成本节省。
- RQ3 H2嵌套4096 / 同三seed真实vs联合rewired历史Null：\`+.031145\` CI \`[+.027389,+.035098]\`；原同队列 \`TRAIN-only Popularity\` 预揭盲验收 \`NOT VERIFIED\`，其他原Null质量与rewire检查不能代替；三seed不独立，source null变多个历史结构。
- 负面与边界：同30k中无约束Always Memory更高准确率（如SAS \`.348744\` > F-selective \`.305446\`）；旧pointwise Utility测得\`1.76941ms\` vs Always Memory \`.69165ms\`（DEV 256×3），新vectorized F selector未实测服务延迟。**无真实服务稀缺成本实测时，预算是显式假定的决策约束**。
- V2 \`#39230682113\` self-host source SHA、\`#39232305650\` 128 locked DEV S/F 0 mismatch、合成纠偏 \`#39235271548\`/联合相同负例 \`#39236652772\`、已存50,049 DEV joint标签诊断 \`#39237415095\`。校正后单专家指标改善**不保证**paired Δ或policy更优；尚未训练合理 sampled-only corrected-S gate。现有两启发式不达方法门槛，不意味着所有校正失败。当前 **V2b NOT_RUN_BY_DESIGN**。

## 2. 最接近先行研究：必须主动对齐的差异，而非堆引文

| 先例 | 学界已有贡献 | N12能提出的严格新增实证对象 | 风险 |
| --- | --- | --- | --- |
| Krichene & Rendle (KDD 2020) | sampled metric全量不一致、bias/MSE指标修正 | 监督候选制度变化是否改变**固定外部知识专家调用的请求集合和真实完整F冻结政策** | “sampled ranking失真”本身不新 |
| Subbiah, Rendle & Aggarwal (CIKM 2024) | 负采样训练WARP/LambdaRank时的rank estimates改善 | 原封存575 S与F的**配对相对知识价值、同sample共享负例、下游调用后果**；未验证所有corrected-S | 不能把V2的启发式方法写成新理论或证明校正无效 |
| Mao, Mohri & Zhong (ICML 2024)及learning-to-defer | 预训练专家、实例相关cost与委托学习 | 一个**候选制度定义的历史知识增量效用监督合同**及多级证据审计 | 相对收益、选专家、损失函数都不是原创 |
| Qian et al. (2026-07-27 arXiv:2607.24010) *When Should Active RAG Retrieve?* | 边际检索效用、目标预算/实际usage偏离、threshold与gate overhead分解；**预印本/非已证实正式期刊论文** | 非语言生成检索的 **live-ranking历史关系来源 × 当前完整候选 × 请求级Memory调用** 的领域实证，承认budget/latency没有关闭 | 不得称首次发现知识调用效用、召回预算迁移或调用开销 |

**优先来源（先保留链接，再做BibTeX与引用核验）**：
- https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ （CIKM2024, DOI 10.1145/3627673.3679943）
- https://proceedings.mlr.press/v235/mao24d.html
- https://arxiv.org/abs/2607.24010 （Qian等，**2026预印本**）
- https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 （KBS期刊范围包含推荐和决策支持，但scope适配不等于原创性通过）

## 3. Rev2.2 唯一提升阶段（严格顺序，除作者签署外均可从现有证据完成）

### E0：原始论文/来源和目标冻结（NEXT）
**输入**：当前\`main.tex\`、\`kbs_references.bib\`、\`Highlights.txt\`、S1–S10、Rev2.1 I2-C QA、I2-D人审材料、I0 14项估计对象总账。
**工作**：确认最终I2后的实际Git blob SHA、主文38p/Supp47p源和CI run、原RQ1–RQ3表/图/公式/效应、B1/G2/A1/N10等已有证据的准确主文和S章节位置；映射“现已陈述/重复风险/缺漏”以及上一轮Rev2.1已完成的三处修订。特别核对Fig RQ3 \`valid historical nulls\`是否在原预验收缺口下过强。
**交付**：\`N12_C8V_REV2_2_E0_CLAIM_TO_SOURCE_MATRIX_2026-10-20.md\`，每项至少 \`claim→original report/run→cohort/estimand→current text anchor→supported/bounded/open→exact action\`。
**PASS**：无需私有TEST；原始数据、参照策略、Call数量与原定义全部一致。若证据不清，先HOLD相关修辞修改。

### E1：P0 创新性竞争先例与“一条实证发现”的最小论证
**工作**：据KDD/CIKM/ICML/2026 Active RAG各做“已被先例解决/本文额外观测/仍无法推断”的逐项矩阵；展示论文方法定义并非新理论。对照现稿Introduction contributions、Related Work、Discussion \`What Is New About Candidate-Indexed Knowledge Value?\`及Conclusion，确认是否已覆盖；**只对真正有信息增量的句子提出改动**。拒绝夸大“关系语义独有”、“算法更优”。
**交付**：\`E1_PRIOR_ART_AND_ONE_THESIS_CONTRAST.md\`，一句中心主张、一张先例差异对照、三条可反驳问题与对应原实验证据。
**PASS**：能直接回应“sampling inconsistency+deferral为什么还值得发表”；若不能，仅记HIGH独立贡献风险而不以形容词替代验证。

### E2：P0 RQ2 冻结政策质量–Memory调用联合论证
**工作**：复用H1 SAS/GRU原完整政策结果（SAS F fewer 401 calls、GRU fewer 539），按**同30k同配置**明确 F/S quality和realized counts；用G2单个50,049 DEV cohort的call-switch分解解释“变了哪些请求”；A1八预算frontier**只用于同DEV的探索性条件背景**，不能在H1 30k上重扫quota或构建新frontier；不要跨不同cohort画错误混合Pareto线。明确固定策略联合观察≠相同调用因果识别，并保留call percentage-point差。若附新表/图，只能是**基于已报告聚合数字的紧凑可复现陈述**，不新增主Results表、不伪造CI。
**交付**：\`E2_FROZEN_QUALITY_CALL_ACCOUNTING.md\` 与对现稿RQ2/Discussion/Operational Conditions的句级patch建议；双模型数值和分母复查。
**PASS**：每个call数与效应和cohort一一对应；原F高效+少calls是两个**observed policy operating points**，不等于真实整体算力/吞吐降低，也不证明所有调用上限F都优。

### E3：P0/P1 Always-Memory、资源约束、V2与RQ3的竞争解释统一审查
**工作**：
1. 维持无约束Always Memory在M3更准及旧pointwise gate实测慢；明定 **外部明确的Memory调用quota是条件，不是已测成本瓶颈**。若加形式化预算决策式，先查论文Section3是否已存在相同方程——**禁止重复新“创新公式”**。分开质量排序、自然calls、预算达成、门控overhead四对象；受Qian2026启发只做诚实归类，不能声称执行过新F gate timing。
2. V2纠偏：原S是uncorrected、Adapted F-assisted、合法sampled-only corrected-S实际policy仍未检验。50,049 DEV的三种纠偏标签\`MSE/toy regret\`只属后验诊断，不能再作为新独立TEST或证实新S策略失败。
3. RQ3：回看 \`Fig RQ3 valid historical nulls\`、Table/Results/Discussion是否将部分预验收变成“validated all”或“独立3个Null样本”；若文本过强仅做精确限定为 **constrained historical randomizations with incomplete prereveal subgate**。历史联动变化使其只能support source sensitivity，不是单一关系语义因果。
4. 同30k新增IDs但同录制期、可能跨G5重叠用户历史；原既定正例可能有曝光选择偏差。禁止凭空使用IPS/因果在线结论。
**交付**：\`E3_ALTERNATIVES_COST_AND_NULL_BOUNDARIES.md\`，每一项 \`claim→observed evidence→not-identified→required exact wording\`。
**PASS**：负面结果完整可见；无“已证实部署资源节约”“已排除corrected-S”“H2完全预注册通过”的陈述。

### E4：受控正文最小增强（仅在E0–E3逐项核实后）
**原则**：精确句级编辑，而不是补第四个RQ、重新写摘要、另造方法名、修改冻表、移动S章节。最优先考虑四个位置：
- \`Introduction contributions\`：让第二贡献成为“实际请求调用分配与额外同期间冻结完整F策略结果”的闭合证据链，而非泛化新门控算法；若当前文本已足够则**不改**。
- \`Discussion/What Is New\`：一个紧凑的先例差异结论；Qian2026仅当近邻确有相关信息且文本缺漏时添加为明确标示的**预印本**，并核对BibTeX。
- \`RQ2/From Supervision Regime.../Operational Conditions\`：突出原已出现的**F高质量、Memory calls更少**两个冻结点；沿用原G2的换位分解和A1已有quota背景；仍解释非严格等调用，避免制造同预算点或线上成本主张。
- \`RQ3 Fig/Discussion\`：若核查确认\`valid historical nulls\`措辞过强，收紧为\`constrained historical randomizations\`，并保持原Popularity prereveal NOT VERIFIED；不更改原图对应数据和绘图拓扑。
V2限制原Rev2.1已补，**不要机械重复**。原Abstract/Conclusion/Highlights除非与小修改出现矛盾，不要求再次改；评估是否确有必要缩短摘要，但KBS当前portal单篇限制须核验后再断言。
**交付**：可审计的最小\`main.tex\`/必要BibTeX差异、修改前后source anchor说明；\`E4_EDITORIAL_SCIENTIFIC_DIFF.md\`。
**PASS**：原11 Results表、7主文+4Supplement、17行49迁移单元格、原公式、效应/CIs/p、所有历史采样母集/状态均无改变；每一个新增句子可追溯既有数据/先例。

### E5：完整科学锁定QA和双PDF验收
**运行**：经版本变更触发 C8V I2 Path A semantic+BibTeX gate 和 C7 frozen Results/full Supplement cell audit；如修改figure title须通过现有文义守卫，必要时**只按明确科学限定扩展测试，不关闭旧guard**。逐份PDF核对图注/Introduction contribution/Discussion/Related Work与引用，LaTeX logs没未定义文献/交叉引用和overfull，且双PDF都真正构建成功。
**交付**：\`E5_CI_AND_SCIENTIFIC_SOURCE_CONSISTENCY_REPORT.md\`，含run IDs、head SHA、页数、两套PDF工件ID/摘要、所有守卫PASS和人工逐段勘验状态。
**PASS**：两组真实CI工作流，主文/完整Supplement各自SUCCESS；变成39p或仍38p均不属于自动失败。CI技术PASS≠KBS创新性通过。
**BLOCK**：任一原始冻结证据/显著性/同队列身份或否定限制被破坏，必须修正，否则不能推进人审。

### E6：真实独立科研审阅与作者GO/NO-GO（承接Rev2.1的I2-D及C8-A）
**工作**：在E5之上发给真实推荐系统/知识系统/方法学研究者现稿、最接近先例矩阵和I2-D包；要求判断 **(i) 创新性是否超出已知sampled bias + learning-to-defer的平凡组合，(ii) 原始uncorrected S和自然calls差异能否接受，(iii) RQ3作为supporting/null证据的权重，(iv) 假定quota但旧计时负面能否承担应用动机，(v) corrected-S开放解释是否需要更强验证**；真实审阅者有身份、日期、书面独立意见及利益冲突披露；AI内部模拟审稿不能代签。责任作者形成响应矩阵、实际作者信息、CRediT/COI/Funding/AI使用等真实声明，并**亲自决定**KBS GO/NO-GO。
**交付**：\`E6_REAL_EXTERNAL_REVIEW_AND_AUTHOR_DECISION.md\`（初始全部PENDING），最终可提交档案和长期PDF/复现实验元数据归档。
**关键判定**：
- **GO**：人审认为bounded empirical主张仍具足够KBS原创贡献，所有数字与范围守卫PASS，作者认可并完成现行KBS投稿核验；
- **REVISION**：只针对写作边界或已存在材料的遗漏补丁，不重新打开TEST；
- **NO-GO/另立项目**：真实审稿人指出要证明显著更新的机制/外推/成本/统计校正策略优势，则**另起预注册独立研究**，不偷偷把V2b重纳入当前Path A。

## 4. 工作量控制、决策门槛和优先顺序

**P0（先做）**：E0原文/源核对→E1先例差异→E2同一冻结cohort质量+调用联合含负面对照→E3受限场景+V2/RQ3科学边界。
**P1（随后）**：E4至多若干句/必要文献最小改稿→E5双PDF+科学保护；发现原主文已经说清者不改，不为了“完成任务”加冗长段落。
**P0不可替代**：E6真实外部人审和责任作者审批；I2-D内部审阅已完成不意味着外部学者有意见。

**停止规则（科学意义）**：若E1无法说明超出已知先例的独立贡献，应明确留\`HIGH NOVELTY RISK\`供真实学者判定，不用宣传词强行自证；若E2差异仅反映政策不同threshold，应坚持“observed complete policy”措辞；若Qian2026与论文仍近乎同构，不得靠跨领域标签制造原创性；若任何预算/cost/RQ3声称需要新数据，不作本计划下新实验。新增DEV或TEST试验全部在路径A **STOP**。如此可提高论证可信度，却不能保证KBS录用。

## 5. 风险与验收总账（防重复遗漏）

| 审稿质疑 | 建议反驳证据 | 改进后最大可说到哪一步 | 未解决的独立科学问题 |
| --- | --- | --- | --- |
| 采样+defer的平凡组合 | RQ1现场候选定义→B1/G2调用切换→冻结同期间30k政策 | 一个已固定外部历史关系专家的candidate-indexed supervision-to-allocation实证链 | 单纯组合是否具有KBS所需创新等级 |
| F/S预算不等 | 原H1 NDCG、8704/9105与8629/9168真实调用、G2同DEV切换 | F较S**在观测冻结运行点**质量高且calls更少 | 强严格等调用F标签因果效应 |
| Always Memory更准 | 旧A1八预算+原Always Memory对照 | 条件约束下调用分配有研究价值；无约束常直接Memory最好 | 实际quota是否必要、端到端新门控成本 |
| corrected-S可弥补F/S | V2合成与同50k DEV标签诊断+原B1三臂 | 原未校正S是明确实验对照，简单纠偏不能自动推断改善政策 | 合法paired conditional校正训练后的真实政策效果 |
| RQ3 H2未完成pre-reveal子验收 | 原4096 Null证据和已披露缺口 | 复合历史来源敏感性支持证据 | 特定关系语义因果、原Popularity前置子检验 |
| 新时段、真实用户结果缺失 | 时间戳、30k event ID排除、离线正例定义 | 同采集期历史验证、离线ranking performance | 真正时间外独立泛化/线上用户因果影响 |

**技术历史来源**：\`N12_C8V_REV2_EVIDENCE_LEDGER.json\`（14估计对象/8cohorts）、\`N12_C8V_REV2_1_I2D_SCIENTIFIC_ADVERSARIAL_AUDIT_AND_HUMAN_REVIEW_PACKET_2026-10-20.md\`、\`N12_C8V_REV2_1_I2C_DUAL_PDF_FINAL_QA_2026-10-20.md\`、\`N12_C8V_REV2_V2A_FINAL_METHOD_GATE_AND_V2B_STOP_2026-10-19.md\`。本方案选择性引用它们，不重做一套相互竞争的实证总账。

## 6. 期刊与投稿边界

KBS官方范围明确包括recommender systems/e-service personalization和intelligent decision support，强调原创创新与知识系统实践：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051。此为**范围适配**而非审稿结论。官方Guide for Authors仍须在投稿前由真实作者从能访问的期刊页面核对最新特殊要求；Elsevier通用Highlights支持页面称3–5点，且是否强制与具体长度必须看目标期刊作者指南：https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript 。

原C8-A作者身份/AI贡献/数据存取权/伦理/费用/归档签署继续有效。旧CI PDF artifacts预计2026-12-19过期；需在到期前由获授权者存长期档案，本计划不在未经授权情况下复制私有原始事件/模型。数据集license元数据差异本身**不自动阻断投稿**，但个别私有再分发或隐私权益仍需事实核查。

## 7. 计划状态声明

**Rev2.2 PLAN AUTHORED / E0–E6 NOT YET EXECUTED.** 当前38/47 PDF最后成功来源是旧I2-C run \`#39351014765\` 和 \`#39351014645\`。新计划本身不触发科学PDF构建，也不表示外部人审通过。Rev2.1此前已完成的I2-A/B/C和内部I2-D不得写回“未执行”。V2b依旧 \`NOT_RUN_BY_DESIGN_FOR_CURRENT_CANDIDATES\`。PR #6仍Draft，作者未提交KBS。
