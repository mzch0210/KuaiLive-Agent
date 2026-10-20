# N12 / KBS 创新性风险缓解与精准优化提升执行方案（Rev3.0，PLAN-ONLY）

**2026-10-20 | PLAN_APPROVED_FOR_REVIEW, EXECUTION_NOT_STARTED | 单一路径：先修实际缺口，再由科研准入条件选择投稿或增量研究。**

> 本文件属于**研究与投稿计划**，不是论文内容改动、数据复算、方法新颖性通过、真人外审报告或投稿授权。除本计划文件外，不修改主文和 Supplement。每一阶段必须单独留存可追溯 commit、验证记录和否定性结果。

## 0. 核实的基线与不可再做清单

- Repo：`mzch0210/KuaiLive-Agent`，分支 `kbs-n12-single-thesis-restructure-plan-20261014`；计划前 HEAD `8e00688913f42d35b82867042068a19b902bd188`。PR #6 Draft。
- 最后通过 C7/C8V **真正双 PDF** 的科学源 SHA `36d9c3f2daed116061f12722db56448f371de60e`，Actions C7 #39364334815/C8V #39364334948，main 38 pages、Supplement 47 pages。之后 NI 文档 commits 不意味着已有 PDF 重建。Rev2.2-R1 E0–E5 DONE，E6 真人独立研究者评价及责任作者最终 GO/NO-GO PENDING。
- **已完成的不可重复事项**：Twitch 44,221 held-out TEST；原 room 10,222 paired sampled/full；M3 50,049 DEV 原 S/F/Adapted B1 三臂；G2 21.32%/23.01% request switches及换入换出效用分解；原G5 47,575 TEST 共享六 fits；A1 8档 quota 和 A2 Direct/Two-stage; H1同期额外30000 IDs独立冻结 complete policies; H2嵌套4096 composite historical nulls；N9/N10/N12来源/统计/PDF审核；V2a两 heuristic sampled correction诊断；NI-1b–f公共synthetic, NI-1g final NO-GO。
- 已验证 H1 SAS F−原未经校正S +.005391 95% CI [.003646,.007174]、GRU +.003585 [.001599,.005576]，自然 F/S calls SAS 8704/9105、GRU 8629/9168；即**观察到** F质量更高、Memory调用次数更少，但不同训练标签及门控校准、自然calls差1.337/1.797pp（>原1pp容差）意味着不是严格matched-call标签单因子因果效应。加权NDCG与未加权calls不能任意组合宣称经济收益或全局 Pareto frontier。
- H2 Authentic−constrained null +.031145 CI [.027389,.035098]，三null同4096 cohort, 多种历史结构共同变化、TRAIN-only Popularity prereveal subgate **NOT VERIFIED**。Always Memory未受配额时更准；旧门控比Always Memory慢；新vectorized F门控未正式测时。V2b NOT_RUN_BY_DESIGN，并未排除所有合理sampled-only corrected S。
- 现稿 `main.tex` 的 Abstract、Introduction、Related Work、Results、Discussion 已围绕唯一bounded经验主张，已有上述局限。**默认不整稿重写**。尤其不将NI synthetic tests或同 DEV分解当独立新结果，不重启旧已揭盲 G5/B4-A TEST。

## 1. 唯一投稿科学定位与 KBS 门槛

**主张**：在固定 Incumbent B、固定 viewer–creator Memory M、真实可用候选 F 的特定知识系统契约下，监督标签所依赖的候选制度 S/F 不只改变离线排名评价，还会重新分配请求级知识使用；另封存同采集期 H1 完整政策显示 F-aligned 比**原未经校正** target-retained S-aligned 在 full-F NDCG 更好、自然 Memory calls 更少。RQ1为背景证据、RQ3是复合 source validity 并行证据，非独立新算法或已证明的机制中介。

**最高创新性质疑**：“已知 sampled metric inconsistency + known deferral，拿 weak uncorrected-S 作baseline，其结果可以预料。”必须用最近邻文献对照和**新增可否证事实**应答，不能只提高摘要措辞。KBS官方 https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 确认 recommender systems/intelligent decision support 在范围，但要求 original/innovative；范围合格不等于novelty PASS。

## 2. P0｜最近邻 prior-art + claim-by-claim adversarial risk gap（必须、先执行）

**输入**：旧E1/E2、现稿 Related Work 约第102行、`kbs_references.bib`、NI-1g、官方一手文献。

**实地发现**：现稿已有KDD2020与CIKM2024，但没有明确引用：
1. Jin et al., AAAI2021, *On Estimating Recommendation Evaluation Metrics under Sampling*, DOI 10.1609/aaai.v35i5.16537, https://ojs.aaai.org/index.php/AAAI/article/view/16537 ；
2. Li et al., AAAI2023, *Towards Reliable Item Sampling for Recommendation Evaluation*, DOI 10.1609/aaai.v37i4.25561, https://ojs.aaai.org/index.php/AAAI/article/view/25561 ；
3. Ihemelandu & Ekstrand 2023, *Candidate Set Sampling for Evaluating Top-N Recommendation*, https://arxiv.org/abs/2309.11723 。

**任务**：核对论文原文方法、目标指标、采样信息和前提条件，形成“已有结果—现稿真新增—仍开放”矩阵；对KDD2020、AAAI2021/2023、2023 candidate sampling、CIKM2024、ICML2024 deferral、2026 KBS SAMD/已有知识路由文献作逐命题挑战。禁止用“没有完全相同的streamer dataset”论证新颖。用真实论文DOI/作者从原出版页核实BibTeX，至少AAAI2021/2023纳入正文；2023 candidate sampling 按通读关联度决定纳入。优先在 Related Work `Candidate-Dependent Ranking` 一处补一小段、如必要在 Discussion 只增加精确 cross-reference；**不重写标题/摘要/三项贡献/所有Results**。

**交付**：`REV3_P0_PRIOR_ART_CLAIM_COLLISION_MATRIX.md` + `REV3_P0_BIB_AND_TEXT_MINIMAL_DIFF.md`；记录逐条新增、未新增/为何不改、近邻先例有何不可克服质疑；参考文献未经证实不得加入。

**通过门**：补齐真实近邻且没有新 overclaim；明确“与已有采样校正/deferral不同”是限定的任务级经验对象，**不**提出原始算法先创；如果某篇已有文章已直接做同等完整策略比较，升级NOVELTY_FATAL并阻断自动投稿。

## 3. P1｜出版合规与跨章一致性（必须，与P0并行但在任何发稿前）

**阶段职责**：
- 比对 Abstract/Introduction/RQ2/RQ3/Discussion/Highlights/cover letter中的 F-vs-**uncorrected**-S、自然calls不同、非strict label-only causal、同采集期新IDs、G2同DEV、H2复合null与未验证子门槛、Always Memory更准确/旧门控时延更差。只改**发现的真实矛盾**，其余L0。
- 作者本人核准真实作者/机构/联系邮箱/CRediT/利益冲突/资助/伦理、KuaiLive/LiveRec及checkpoint权属/数据许可/再分发权限，提供无敏感行的可复现脚本+汇总、合法受限数据访问路径，绝不公示私有events/models。
- Elsevier **2026更新的官方AI政策** https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals ：实质性稿件AI帮助需单独声明，AI参与研究设计/方法/分析应在Methods可复现说明。具体事实只能由作者/实际工作流审计核准，严禁AI代签、臆造工具版本或声称只做语法润色。
- 核查KBS官方Guide https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors 及投稿portal要求：现公共获取 403，因此**Highlights字符限额、Abstract字数、图摘/匿名/文件类型等本次未验证**；必须由有权限的真人登录页面逐项验收，不可套用其他Elsevier期刊规格。
- 在2026-12-19历史GitHub Actions工件过期前由获授权者保存原 main/supplement和source/checksum，不上传受限原始数据。

**交付**：`REV3_P1_AUTHOR_AND_PUBLISHER_COMPLIANCE.md`（逐项 VERIFIED/PENDING/NOT_APPLICABLE + 证据归属）；`REV3_P1_SCIENCE_CONTRACT_DIFF.md`，其中文本无必改风险时可**NO CHANGE**。E6 真人预审是既有项目质量目标，但**不是经确认的KBS强制条件**；作者可在披露内部AI审查局限后自行承担投稿决定。

**通过门**：作者身份证明/相关声明/AI披露/来源权利与真实Guide缺失项均由责任人确认；不能为了追求自动CI绿色掩盖实际合规不确定性。

## 4. P2｜最小科学改稿 + 版本冻结双PDF（P0/P1执行发现真实缺口后）

仅采纳已核实的新引用与必要一句式范围修正。若无新发现，相关章节严格保持原状；任何 NI-1b–f 合成效用数值都不得当作现实M3新结果。修改后做精确git-diff、BibTeX有效性、全文交叉引用和C7/C8V全部真实CI，检视最终 main PDF 相关段落及Supplement引用；存档原稿与新稿双SHA/工件来源、科学diff、异常日志。绝不删除语义守卫、重计算或更改冻结统计。

**交付**：`REV3_P2_ACCEPTED_SOURCE_DIFF.md`、`REV3_P2_DUAL_PDF_QA.md`及实际新的两个工作流run IDs/产物；预计篇幅不能当成验收目标。

## 5. P3｜有条件新增证据：三条互不偷换的科研路线

**P3-A 真实资源成本/价值合同（低到中成本，解决实用价值而非自动产生算法novelty）**：在科研数据使用权限允许下，先文档明确系统是否真的限制Memory调用、限制何种GPU时间/吞吐/成本；再对最新vectorized F gate、Base、候选构造、Memory、Always Memory，在**新且有权访问的DEV或不含target的中立benchmark**上测硬件、预热、批尺寸、p50/p95/吞吐、门控与ranker总耗时。禁止用旧256DEV warmed timing代表新版。若Always Memory仍更快且更准，必须公开否定部署节约，只保留hypothetical quota。交付 `REV3_P3A_RESOURCE_CONTRACT_PROTOCOL.md`、`...RESULTS.md`（只有授权执行才有RESULTS）。准入：先有可证伪成本假设、许可、设备和明确计时协议；不许用已揭盲TEST挑模型。

**P3-B 独立未来时期评价（中到高成本，解决外推）**：必须获得真实**晚于原2026年3月**、新记录且具有权利的新作者-活跃候选流及user histories；事先审查F候选快照是否可复现。冻结现有F/S**原始完整政策**，另以分离的训练/校准数据确定如需threshold。新评价只做一次，报告两类baseline、配对用户CI、候选分布漂移、实际calls；用户重复/新旧时期信息依赖需披露。允许负结果，若 F 不复现则收缩现稿外推范围。**如果只比较旧F与旧uncorrected-S**，它解决时间外推，**不**解决weak-S竞争者或strict-budget因果识别。交付 `REV3_P3B_FUTURE_COHORT_FEASIBILITY.md`、预注册、hash、blind evaluation结果；数据不存在则STOP，不得复用原B4-A TEST假装新时期。

**P3-C 真正的 corrected-S vs F 与严格资源公平（最高研究代价/潜在科学增量；目前BLOCKED）**：NI-1g 的 S-only信息合同、统计辨识/有效区间与错设风险、方法近邻增量、作者批准、独立数据**全部**满足后才可单独授权。设置原S、合理 corrected-S、F 三臂，确保同Base/Memory、同F评估、同pretarget Z、清楚的sampling-label信息、user-group nested fit与相同资源度量。严格区分在线按DEV校准的pointwise调用率与离线TEST批处理 topK恰好等次数，后者不得冒称可在线部署。报告质量–calls完整对照、实际成本与多重比较族、置信区间和包括corrected-S追平/超越F的否定性结果；不能用旧已揭盲G5/H1挑修正方法/阈值。若NI-1g阻断未解除则**V2b与NI-2/3继续NOT_STARTED**。

**非默认备选理论支线**：只有发现明确超出AAAI2021/2023的 joint conditional policy-value 识别/有效有限样本regret新论证、可由独立数学审阅与数据检验时，才能新注册；不得连续追加17/32/64-state toy或把EM/LP命名成新算法。

## 6. P4｜审稿人最强反驳和科学裁决（P2通过后）

模拟严格审稿人最强质疑：已知sampled metric bias + existing deferral；弱且未经校正S；H1 calls不同；无真实quota成本；多次复用同DEV和六fits共享TEST；H2 composite Null & one pre-reveal unverified subgate；缺少新时间复制；AI/数据许可。每项标记 **ANSWERED_EXISTING / ANSWERED_NEW / OPEN_FATAL / OPEN_DISCLOSED**，要求指出原论文具体表/式/来源，不得以更多审查报告数量和CI通过解释创新性。报告可明确 GO risk remains HIGH。

**交付**：`REV3_P4_ADVERSARIAL_EDITOR_PACKET_AND_CONTRIBUTION_DELTA.md`。如果只有“写得更好”没有新科学数据，应定性为 SUBMISSION_READINESS_IMPROVED, NOVELTY_UNCHANGED。

## 7. P5｜单次投稿决定（责任作者独享）

| 判断 | 严格条件 | 行动 |
| --- | --- | --- |
| CONDITIONAL_GO_KBS | P0/P1/P2科学+来源+法务真实通过；无已知致命新近先例；作者书面接受 HIGH novelty风险 | 保持原文 bounded empirical，准备cover letter，责任作者登录 KBS portal决定投稿，PR 从Draft转Ready需另行明确授权 |
| HOLD_FOR_NEW_SCIENCE | 有已获许可、可取得的未来数据或满足NI-1g的有效新方法；能形成事前可证伪、非重复增量 | 单独预注册 P3; 设真实取得日期和STOP条件，旧稿保持可随时决定 |
| REDIRECT | 作者不愿承担 KBS 风险、新数据/方法通道无条件启动或最近邻完全重合 | 对照下一期刊 Guide 后再定策略，不承诺备选期刊更易接受 |
| STOP_NI | 没有可辨识sampled-only支持/没有合法新数据，只继续堆积synthetic | 完全停止NI科研，原结果如实保存 |

不可声称人类独立学者审稿已完成；也不把这项项目自定优选门槛说成KBS法规要求。

## 8. 任务依赖、交付顺序和退出判据

- **短期约0–2周**：P0最近邻文献碰撞审查、P1作者合规准备、P2精确差异（仅必要时）+双 PDF；P4内部editorial包。阶段完成不自动认定原创性风险下降，只认定准备度提高。
- **中期2–8周（可选，仅门槛通过）**：优先P3-A resource protocol/合法计时与P3-B新时间数据可行性；若没有授权与真实新增信息则STOP，不强行启动。
- **长期>8周（可选）**：P3-B一次新时间队列确认；P3-C只有NI-1g另行方法批准及新评价数据的科学门槛通过才设计/执行。失败如实写出，不在旧TEST挑赢家。

最低执行门：每一 P-stage 先说明问题、具体新增科学信息、预注册结论边界、数据权利、预决策可见特征、对照先例、停止条件及产物；研究负责人确定每段开始与结束。

**计划终极成功标准**：不是“实验数变多”，而是：真实新文献缺口修复、科学主张完全对齐、作者合规可以签署、编辑可验证所有负面结果；如有新研究，必须确实解决 corrected-S/fair call/temporal validation 之一并产生不能由旧B1/G2/H1/NI简单重复的可证伪知识。任何一个新增结果都不得推断现有论文的统计对象之外的结论。

**PLAN-ONLY**。N12原稿38页+47页、原E0–E5、NI-1g NO-GO 和所有冻结TEST均保持原样；用户下一步明确授权后才进入P0/P1实施。