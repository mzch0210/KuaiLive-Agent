# N12 Rev3.2 — 以论点驱动的全文连贯性与科学编辑重组计划

**2026-10-20 | PLAN ONLY / NO MANUSCRIPT MODIFICATION / NO SCIENTIFIC RE-ESTIMATION / NO SUBMISSION.**
**唯一基准**：\`mzch0210/KuaiLive-Agent\` 分支 \`kbs-n12-single-thesis-restructure-plan-20261014\`；审查时 HEAD \`4cefa161434f0e32d977b7f95b7d581637a721e1\`；冻结的最后论文科学commit \`a686cd07ce80f8d4090aae720c0e583f39f73176\`；主文 \`main.tex\` Git blob \`e5043a2fae305cfcdca49fefa3650732c927d1a4\`（640行、现有七个section）；\`SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md\` blob \`bb7d11074445988ecf637f895dad55084fc9577b\`（1155行、S1–S10.19）。Rev3.0 C7 #39398148734/C8V #39398148731主文39p、Supplement47p均成功。PR #6 **Draft**。

## A. 为什么必须是新型“编辑责任重排”而不是又一次局部修辞补丁

历史回溯：
1. \`KBS_ARGUMENT_DRIVEN_REVISION_PLAN_2026-10-10.md\` 已明确记录论文的长期通病：结果章过多实验管理语言、跨段落防御性范围限定。
2. \`KBS_PAPER_SECOND_PASS_SUBMISSION_NARRATIVE_REVISION_PLAN_2026-10-11.md\` 与 \`KBS_THESIS_FIRST_REVISION_MASTERPLAN_2026-10-13.md\` 已提出单一主线、Results discovery-first、Discussion 不要再报数字。
3. \`N11_FINAL_KBS_EDITORIAL_LANDING_AND_COHERENCE_AUDIT_2026-10-14.md\` 做过节数、冗余表与阶段标签清理，技术验收成功。
4. \`N12_SINGLE_THESIS_KBS_MANUSCRIPT_RESTRUCTURE_PLAN_2026-10-14.md\` 已合并问题/框架为第三章、七章结构、RQ3并行分支及迁移数据表；\`N12_C2_INTRODUCTION_RELATED_WORK_EDITORIAL_REVIEW_2026-10-14.md\`、\`N12_C3_UNIFIED_METHOD_SCIENTIFIC_EDITORIAL_AUDIT_2026-10-14.md\` 和 C5/C6 又已各自修订、双PDF验收。
5. \`N12_C8N_DECISION_ALLOCATION_NOVELTY_REWRITE_QA_2026-10-19.md\`、Rev2.2 E2、Rev3.0 P0–P4 为防科学夸大再将多个限制性解释写回Abstract、贡献、RQ2、Discussion、Conclusion；虽然科学上准确，却造成**段落逻辑破碎、贡献弱化、重复警示**。Rev3.0仅新增五篇近邻文献，没改变正文核心问题。
6. Rev3.1 KuaiRec X0-B真实文件运行成功，但Big→Small严格历史方案NO-GO；没有新可纳入论文的科学数据，X1/X2不启动。因此本轮修订必须承诺**只重组既有研究**。

历史教训：已有多次“全文改写—新审稿风险—加入防御补丁—全文改写”的循环。**本次先锁定每个事实的唯一讲述职责，再改Results和Methods，再改前后文；不再用新增大量边界语句表现严谨**。PDF/CI PASS是技术充分性，不是语言/论证连贯性的验收。

## B. 不得改变的科学主张与证据合同

**唯一主论点**：
> In the studied offline live-streaming settings, the candidate regime used to supervise the incumbent-relative value of an already fixed historical relationship source affects which requests receive that source and the full-candidate quality of the resulting frozen ranking policies.

与已有文献的必要区别是**knowledge-call allocation/policy-level downstream consequences**，不是首次发现sampled top-K偏差，不是新deferral或sample-correction算法。RQ1解释为何价值有候选/基线依赖；RQ2 H1主证据、G2 DEV描述调用调配；RQ3独立parallel检验真实历史来源，**不是RQ1→RQ2→RQ3因果中介**。系统成本是应用边界，不是第四贡献。

事实底线：
- Twitch streamer TEST 44,221：recoverable-but-unrepresented subgroup 5539 的Memory−Base +0.22045；后验目标条件，仅诊断。Twitch pointwise Utility Frozen TEST 6650/44221 calls、NDCG .58983 vs Base .58211；其Difficulty同TEST count retrospective-match。
- 原KuaiLive **room**相同10222 previously examined events：S/F相对增益 −0.04120/+0.04631，已做候选成员/score reference分解；只是paired retrospective diagnostic，**不能并列称3个独立TEST**。
- M3 **author**原始47575 TEST：六fits共享人群；primary Utility .30287 vs Base .25800，Always Memory .34679。原M3 DEV为50049 events/12628 users。
- M3额外同期封存30000 IDs、10387 users，H1 frozen F−original uncorrected S：SAS +.005391 CI [.003646,.007174]，F/S calls 8704/9105；GRU +.003585 CI [.001599,.005576]，calls 8629/9168；自然差1.337/1.797pp，超过旧1pp近等调用阈值；F和S为**不同训练监督/DEV阈值的完整冻结策略**；加权NDCG、未加权调用不能误称同预算、标签单因素因果或真成本优势。
- G2同50049 M3 DEV调用换位：SAS 10672(21.32%)，GRU 11517(23.01%)；属于事后同DEV解释性allocation accounting，不冒称H1中介或独立确认。
- H2嵌套4096：auth .334942 vs三固定历史null事件均值 .303797，差+.031145 CI [.027389,.035098]；composite强历史干预，独立来源有效性支持但非单一语义因果。**原4096队列自己的pre-unseal TRAIN-only Popularity接受检查NOT VERIFIED**，不可从1024 DEV借用。
- 新目标Always Memory full NDCG .348744更高；原点式Utility GPU256-DEV回放1.769ms vs Always Memory .692ms；新vectorized-F gate未测真实完整production cost；不声称服务节约。
- 同采集期额外事件≠未来期间TEST，用户/历史可重叠；原S是target-retained 575且uncorrected，corrected sampled-only comparator尚未合法证明。NI-1g V2b NO-GO、NI-2/3不授权；旧TEST不得再次用于新策略搜索。
- 所有数值、置信区间、权重、statistical families、模型checkpoint、Memory 0.45/0.45/0.10、pretarget information contract，以及主文原九Method公式、七张Results表的**科学单元**必须不可变；允许表位置/文字压缩，但必须保留对应source-of-record和必要交叉引用。

## C. 目标论文架构：一项中心结论，两个支撑方向

**阅读时应构成的逻辑：**
长期关系源可能补充或重复现有ranker → 其可用价值取决于Base与候选 → sampled regime由此可能制造错误的use-time training label → 比较F/S冻结调用策略的full-ranking后果（H1） → 从DEV allocation trace解释选择集合为何不同（非独立因果机制） → 真实历史来源相对约束历史null仍有独立信息（H2） → 在资源限制及日志评价条件下如何理解这一经验规律。

**新七章、章节唯一职责**：

| 章 | 关键要回答 | 主文保留 | 应下沉到Supplement/科学审计 |
| --- | --- | --- | --- |
| 1 Introduction | 现实张力与唯一未充分回答的request-level consequence是什么？ | 4–5段按问题递进、窄gap、研究对象、设计和正面贡献；一张单一schema（可复用现图） | 统计表、采集年表、逐个“not a...” |
| 2 Related Work | 与knowledge representation、deferral、sampled-evaluation三脉络有何非平凡关系？ | 近邻KDD/AAAI/TORS/RecSys/ICML/KBS准确但不逐段自辩；最后一段研究缺口 | 论文外部对抗矩阵、referee回应逐条记录 |
| 3 Valuation & Policy | Δ_r、η_r、F/S supervision 和部署可见Z、π分别是什么？ | 固定Base/Memory、重要公式和value→pretarget decision单图；简短历史诊断定义只在真正引用时出现 | 公式重复的“不是新定理”、回顾状态拆分、细节参数 |
| 4 Experimental Design | 样本等级、比较单位、信息权限、stats怎样保证对应RQ？ | 单一data/evidence-role表；H1独立event ID同采集期、F/S S-unadjusted、分配阈值和calls、H2控制、真实称量方法 | 长种子/host/run IDs/软件执行年表；重复的method table可合并或下沉 |
| 5 Results | 哪些是主发现、什么是支撑解释？ | 下文结果顺序；完整H1与H2 effect、CIs、actual calls | 六fit全矩阵、九格拆分、所有budget frontier、失败/修复日志 |
| 6 Discussion | 这些结果使knowledge-use decision设计应有什么变化？ | 机制解释、与先例真实区别、真实部署条件、合并科学边界（不是Results数字复述） | 每个实验旁“not a causal/not TEST”重复否定 |
| 7 Conclusion | 本文凭哪些证据建立了哪条可传递的方法论认识？ | 正面回答one-sentence thesis；一条审慎、非空泛的future agenda | 再列一次局限目录、否定算法首创清单 |

**建议Results内部调整**（最终小节名可按通顺性改，不固定图表页数）：
- **5.1 Value depends on incumbent history and candidate regime**：Twitch outcome-defined解释＋原room F/S反转，作为研究问题的实证铺垫，结尾导出政策监督。
- **5.2 Primary result: full-candidate supervision changes frozen policy outcomes**：在起段用2–3句交代原M3 frozen incumbent/Utility对照，再立刻交付H1 30k表，真实Calls/weighted effect及必要一次局限。
- **5.3 Explaining which requests change specialist use**：G2 same-DEV F-only/S-only、不同的mean Δ、net accounting，明确这是supporting DEV不解释为H1原因。
- **5.4 Utility selection across fixed incumbents**：浓缩Twitch TEST和M3原47575 six-fits的基础决策对照；可合理提前少量setup信息以确保5.2可读，详细fit值转S8。
- **5.5 Authentic history matters under fixed F candidates**：H2主表与Composite null、一个明晰的pre-unseal cohort-specific failure disclosure；Full/Long/Short与1024 DEV附录。
- **5.6 Operating regime and latency**：简洁呈现quota=stated policy objective、Always Memory accuracy、warmed tested-gate latency；保留精确信息不能把负面结果删除。

**避免新型结构错误**：5.4作为5.2的支撑，并非后来的确认实验；H1仍由same-source新IDs评价；H2为parallel source check，不能画政策提升→历史关系证明箭头；Twitch/room/M3不同ranking units永不汇成统一Meta estimate。

## D. 反向清理矩阵：负面事实在哪里出现、最多如何出现

原则：每个边界必须**可发现、准确、对结论有约束**，但不当作全文章节首句和尾句的习惯性修饰。不是简单删除not/cannot统计，不为改善“正面感受”遮蔽重大失败。

| 类别 | 正文一次讲清的位置 | 其它位置合理但更短的承担方式 | 不能删去 |
| --- | --- | --- | --- |
| generic originality免责声明 | Related Work末尾+Discussion与具体前案对比，不重复五次“not theorem” | Abstract只讲真正新证据；Contributions不再每条都带否定句 | 不得宣称sampled指标或deferral数学由本文首创 |
| 原S weak comparator / corrected-S缺失 | Experimental Design S/F label合同；Discussion一段具体未排除替代解释 | Results H1注明“uncorrected S” | 不得冒称corrected-S表现已经比较 |
| H1不等调用、差1.337/1.797pp | H1 Results表及紧邻结果文本，讨论解释比较估计对象 | Methods说明DEV cap不确保future calls；如Abstract保留一句complete-policy自然调用 | 绝不能改称strict matched-calls / isolated label effect |
| H2 prespecified Popularity gate missing | H2 Methods描述控制预设；H2 Results/表注直接如实NOT VERIFIED；Discussion分析它对source-validity权重的影响 | Conclusion无需重复精确校验名 | 不可隐藏遗漏、不可以post hoc补测试冒充pre-unseal |
| same-period additional cohorts & cross-task unit | Experimental Design evidence table；Discussion external/generalization | 表注写same-period and nested | 不得写prospective future-period或user-disjoint replication |
| Always Memory superiority / slow old Utility | Operating Results真实benchmark & Discussion implications | Abstract如需评价成本只写“under stated call constraints” | 不得称production speed/monetary savings |

**每段功能标注**：研究问题/方法界定/证据/因果解释/机制反例/范围边界/承接中的一个为主；“既不是A又不是B也不是C”重复否定句如无新增可证实信息则改为主动正面陈述；含真实failed requirement的句子单独归位后保持可检索。对句子“not”的数量只作定位辅助，绝不做删除配额。

## E. 补充材料（47页）重新分层，而非无差别删减

当前已定位的硬问题：
1. Supplement frontmatter仍为 **13 October 2026**，晚于该日期的H1/H2、S10内容出现后未同步。
2. S5.6原“Results Section 6.3”，当前Results第五章，属于已失效的手工编号。
3. S7.7仍称“final combined S1–S9 submission supplement”，实际含 S10.19。
4. S10含19个连续递增append阶段，核心H1/H2真正评价结果晚于大量探索性实验；S10.19再次汇总基础Twitch/M3表，造成主题回跳与重复。
5. S9.6旧256-DEV warmed trial(.8033 Memory/1.8018 Gate)与S10.17新版 counterbalanced(.69165/.769? **正确为1.76941** Gate)只因不同计时方案并存；正文应对接新版，旧实验给简短不同条件提示，不删除任何来源事实。
6. S1.5 链接\`manuscript/kbs_latex/src/kuailive_agent/export_rechorus_room.py\`不存在；实际repo路径\`src/kuailive_agent/export_rechorus_room.py\`，需要在不改代码事实下修正链接。
7. 旧“G0F intent vs G1 implementation”真实偏差、原H2 pre-unseal未验证、S2 SHA/实验冻结必须保留，但主要属于reproducibility/validity audit，不宜充满每一段解释。
8. 标题\`SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md\`可暂保文件名以维持CI路径；需改元数据日期/交叉引用，不先重命名以免破坏流程；最终文件名如需更改需CI全局更新。

**目标组织（建议保持S1–S10兼容编号）**：
S1 数据单位/时序/feedback；S2冻结与复现协议；S3 designated incumbent fairness；S4关系组件与历史诊断；S5候选候选对照与9 draws；S6 Twitch历史范围与recency；S7 pretarget selection、OOF、目标对照；S8六seed与原M3 TEST完整对照；S9资源、早晚测量在一个可对照子节；S10按**10-A policy supervision（DEV→frozen H1）/10-B source validity（DEV→H2）/10-C ancillary explanations/validity**分组，可通过移动文字与交叉引用保留旧S10.x永久指示映射。若调整Supplement编号，必须提交 old→new migration map并核验每个正文S10引用，不能静默更名。

**原则**：博士论文式“全部过程记录”转为可复现的研究补充材料。GitHub保留failed-run的工程审计文件与完整SHA；发表Supplement保留用于验证证据和关键异常真实性的简明信息与精准持久链接。不要仅为减少篇幅删除可重复性说明。

## F. 唯一执行顺序：先论证结构，后文字，最后抽象

| Phase | 可执行工作（按依赖顺序） | 必须交付 | 硬验收条件 |
| --- | --- | --- | --- |
| **W0 只读锁定** | 固定科学源sha/blob，抽取主文每段“唯一论证职责”和句间衔接；建立existing→target章节paragraph table、图表/引文source-of-truth总账 | \`REV3_2_W0_CLAIM_ROLE_AND_PARAGRAPH_MOVE_MATRIX.md\`；原论文全部关键结果checksum | **不得**编辑本文科学源，确认没有额外重复的过往计划再走回头路 |
| **W1 单页storyboard** | 写5句完整论证：problem→gap→estimand→H1 main result→meaning；标明RQ1→RQ2，RQ3 parallel；明确Methods/Results/Figure职责 | \`REV3_2_W1_ONE_PAGE_ARGUMENT_STORYBOARD.md\`、single-figure sketch和关键结果摆放草图 | 人工模拟首次阅读：不看旧项目报告就能说出研究矛盾及新意；每项主张有唯一段落owner |
| **W2 Results first（第一科学源修改）** | 从原Results拆出H1在前、G2解释、M3/Twitch决定性对照、H2、resource；主动语态改写回归研究问题；优先保留原表科学值/label，必要移详表至S | \`main.tex\` Results结构修订+数字单元迁移表+章节“首尾桥接句” | H1首读约1–2个Results子节内出现；每结果小节遵循question→design→result→meaning→transition；不能冒称因果中介 |
| **W3 Methods/Design align** | 重排Methods的研究对象/定义/信息权限与Experimental Design证据等级、对照统计，remove重复scheme图和重复方案表；方法数量参数只出现一次 | 同一science branch的Methods/Design修订、formula integrity审计 | 9核心方法公式保持数学等价，Z pretarget、sampled target-retention offline-only、call calibration、20cell weights、Holm family和History null controls不丢 |
| **W4 Intro/Related Work revise** | 依完成的Results重写动机、对象、RQ与贡献；相关工作收束在真实closest prior与明确新增经验estimand，不增不必要文献 | Intro/Related与Figure1叙事图最终版 | 标题、首段、RQ/Contributions和H1结果目标一致；RQ3不再画成H1结果之后的因果 |
| **W5 Discussion/Conclusion** | 实证解释与已知理论对话；一个集中operational+validity subsection；结论正面给knowledge-system policy-design lesson，不重列工作日志/主要数字 | Discussion/Conclusion最终版与负面事实留存清单 | 不引入新的结果、理论首创、经济效益；每个必需边界仍准确、可被审稿人找到 |
| **W6 Supplement sync** | 按 S1–S10科研功能排序清理日期、失效小节指针、断链、重复表、旧计时条件；工程故障详情留在独立GitHub audit | Supplement重编、S10 old→new定位、source link checker、官方数据/版权待核验清单 | 与主稿的所有S10引文一一匹配、保留H1/H2关键统计和pre-unseal缺失控制；所有关键来源可重建 |
| **W7 Frontmatter last** | 从最终结果回写摘要、Contributions、标题可选变体、Highlights；以积极陈述中心贡献，但必要边界准确 | abstract/Highlights完整草稿和字数检查 | 不宣称KBS特殊摘要限制已验证；实际Guide由作者核准后finalize；Highlights 3–5条且遵守各自适用最新规定 |
| **W8 Technical + human acceptance** | 新C7/C8V在最新科学sha完整跑、全图表/参考文献/交叉引用/负面事实自动比对、PDF关键页目视；人工“从Introduction到Conclusion不看GitHub”连读 | 全文连续阅读评审（至少编辑+独立同行如可获）、科学源SHA、双PDF和差异审查、修改close-out matrix | 技术QA + academic readability双门均通过；author P5授权/AI披露/版权/KBS guide仍未完成不能提交 |

**分阶段CI实施原则**：每个源改动先静态比较、必要时阶段构建；最终W8重新以新科学SHA执行C7/C8V双成功+PDF抽查，旧\`a686...\`结果不能代替。旧指纹型guard若因正当段落/图表迁移会fail，需更新期望fixture与“科学不变量”的守卫，而不是删除保护或把格式差异当科研失败。若方法公式必须移动，先对formula bodies和rank utility的符号等价性审核，再更新locator；原科学语义不允许由修辞变更偷偷移位。

## G. 质量测试矩阵：双层审核，防止同样问题再次出现

**第一层：科学完整性自动化**：
- 数值/CI：Twitch, 10222 room, 47575 original, 50049 DEV, H1/30k/SAS/GRU, H2/4096, experimental seed/reset, weighted versus unweighted rates, cost truth；来自原冻source，不反向以新论文为事实。
- 九方法公式与值函数、S/F定义、Z权限、选择政策、3-Holm families、M3 20-cell weights，图表与文本无矛盾。
- \`Original KuaiLive room\` ≠ \`M3 author\`；\`same period extra event IDs\` ≠ \`new future cohort\`；\`retrospective equal test-call difficulty\` ≠ \`frozen pointwise policy\`；\`composite null\` ≠ \`isolated semantic causality\`。
- 保存包含负面事实的锚点：H1 calls unequal; original S uncorrected; corrected-S not actually tested; H2 prereveal gate NOT VERIFIED; Always Memory better & legacy gate slower; no actual production savings.

**第二层：以读者为中心的人工验收**：
1. 摘要第1–2句就能识别研究难题；各贡献 bullet 写实际发现而不以免责语作结。
2. 各章第一段说明上一章为什么带来本章需求；末段形成下一章承接，不出现前文从未定义的标签和突然转换。
3. 每个结果小节中的第一句是学术问题，前100–150词内有足够事实/主要对照，不先列运行手续。
4. 图1与Method流程图若仍两幅，功能不同（research causal/evidence map vs deployed time-information flow）；否则合并一幅防冗余。
5. 抽走某段反复免责声明后，科学边界仍在Methods/Results/Validity处容易检索；若不是，必须恢复必需事实，而非为“流畅”掩盖。
6. 从Twitch streamer→KuaiLive room→M3 author只在研究对象确实变化时提醒一次，不每段重复“not same protocol”。
7. Discussion每段必须提出超越重述数字的解释、与近邻对照或限制适用推理；Conclusion不再重述完整缺陷清单。
8. S1–S10应能从主文表注迅速找到细节，链接真实存在；不要残留“Section6.3”“S1–S9”“13 October”作为最终时态。
9. 不强制特定字数、固定39/47页或绝对删掉所有\`not\`；任何“篇幅更短/语气更积极”仅是次要指标，科学真实性更优先。

**验收失败停止条件**：任何冻结统计变化、实验身份被错误升级、pretarget泄漏、新增未证算法首创、遗漏H2 prereveal缺口、成本反向叙述、旧QA脚本因强制旧section order错误pass/overlook → 当阶段PAUSE，回到source evidence；不直接合并。没有新scientific work authorization不得训练/评价H1/G5或改NI-1g。

## H. 编辑修订与KBS适配的正式来源

- KBS 官方目标：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051；knowledge-based intelligent decisions与原创性，论文结构应能让编辑一眼识别**what is known/what this evidence adds**。scope match并非guaranteed novelty。
- Elsevier publication writing: https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/how-to-write-the-results-section-of-a-research-paper/ 强调Results objective/concise、负面结果要保留；https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/steps-to-write-excellent-discussion-in-manuscript/强调Discussion解读、对照与限制，而非重复Results；https://www.prod.webpresence.elsevier.com/connect/the-condensed-read-how-to-structure-a-science-paper 主张先Methods/Results/Discussion后Intro/Abstract。均是**通用编辑建议**，不擅自作为KBS专属格式上限。
- KBS官方Guide：https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors 。具体摘要字数、匿名制度、data statement/highlights上传格式、AI披露等由真实责任作者通过可访问portal核实。
- 原则：Rev3.2让现有科学贡献可读、可比较、可辩护，不声称修辞重组消除weak-S、strict equal-call、missing prereveal H2或实际resource proof这些实质研究限制。

**即时执行状态**：本文件创建后，仅计划文档新增；\`main.tex\`、\`kbs_references.bib\`、Supplement、Highlights与所有冻结实验均未改变，原Rev3.0 C7/C8V PDF PASS仍指向旧科学源。W0–W8**尚未执行**；PR #6继续Draft，真实人类独立审查、责任作者声明/数据许可/AI披露、最终KBS Guide审查及GO仍PENDING。
