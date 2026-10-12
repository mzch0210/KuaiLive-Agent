# G5｜KBS 八章全文独立审稿、证据追溯、正式文献与源匹配 PDF 全面验收

**审查日期：2026-10-12。审查性质：Independent KBS reviewer-style full-manuscript audit，非实验重跑、非期刊录用评议结果。**

> **审查决定：八章科学正文与当前 29 页 LaTeX/PDF 的 G5 技术/论证 Gate：PASS，附明示审稿风险；整套投稿材料：HOLD。**  
> 本文已有清晰且有证据支撑的 C1→C3 主验证和 C2 候选情境补充证据；无需为了收紧写作而重新生成实验事实。**但尚未具备直接正式提交条件**：缺 Abstract、真实作者及通讯作者资料、正式 AI 使用披露等作者批准的信息。额外强 Base / 冻结跨情境验证可增强竞争力，但不得以目前数据冒充已经完成。

## 0. 审稿依据、版本及可重现审计输入

**本次实际重新读取的仓库主稿：** [main.tex](main.tex)，Git **blob \`4a8d07da093bd350339c68f1617d98de1a32780f\`**，对应 G4 稳定源码 [commit 42d6db84f7aaf72cb5ce01fa6b70e970946c14e5](https://github.com/mzch0210/KuaiLive-Agent/commit/42d6db84f7aaf72cb5ce01fa6b70e970946c14e5)。

- [正式投稿导向大纲](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md)：blob \`89734dbec9f852fcb728b2ef3a767d19ebe22109\`。
- [S1–S9 集成补充材料](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md)：blob \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\`。
- [正式参考文献 BibTeX](kbs_references.bib)：blob \`358e6599711421ac609cb1956cfc9cd122cdc341\`。
- [G0 冻结 C1/C3/C2 追溯表](G0_FROZEN_BASELINE_CLAIM_EVIDENCE_TRACEABILITY_2026-10-11.md)、[G1](G1_INTRO_RELATED_WORK_KBS_REVIEWER_ACCEPTANCE_2026-10-11.md)、[G2](G2_RESULTS_DISCOVERY_FIRST_REVIEWER_ACCEPTANCE_2026-10-12.md)、[G3](G3_DISCUSSION_SCIENTIFIC_INTERPRETATION_REVIEW_2026-10-12.md) 和 [G4](G4_METHOD_PROTOCOL_AND_CONCLUSION_COHERENCE_AUDIT_2026-10-12.md) 科学核查与 provenance。
- **本次 PDF 以精确源码 GitHub Actions 构建产物为准**：[run #38194254351](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38194254351)，[PDF 与日志 artifact #11723150138](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38194254351/artifacts/11723150138)。实际下载 ZIP 内 \`main.pdf\` **445,293 bytes，29 页**；不能使用旧轮次 PDF 冒充这一版本。

**正式的外部标准：**
1. [KBS 官方期刊描述](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)：原创 AI/知识驱动系统、推荐与个性化、智能决策支持、理论与实践兼顾。
2. [Elsevier 最新期刊生成式 AI 政策（2026-08）](https://www.elsevier.com/en-au/about/policies-and-standards/generative-ai-policies-for-journals)：实质性 AI 辅助写作需单独披露，报告工具名称、用途、作者审阅及责任，不可将 AI 列为作者。
3. [Elsevier 官方投稿检查清单](https://www.elsevier.support/publishing/answer/is-there-a-submission-checklist-i-can-use)：核实署名、单位、通讯作者、图表、参考文献和适用声明。
4. [Elsevier 官方 Highlights 说明（2026-06）](https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript)：是否强制取决于**目标期刊** Guide for Authors；通用的 3–5 点建议不能未经核实套用为 KBS 强制规则。
5. **可核查范围边界：** 本次尝试直接获取 [KBS 当前专属 Guide for Authors](https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors)，站点返回 403。故本审查**不宣称独立核实了 KBS 对 Abstract 字数、Highlights 必需性、单篇页数或图形摘要的现行特别规则**；正式投稿前必须在作者/投稿系统可访问的官方页面逐条核对。

## I. 八章主线独立盲审（科学内容 PASS）

**中心命题：** 对于指定训练后的 incumbent Base 和 eligible candidate regime，历史关系证据的操作性价值由固定专家能够增加的排序效用定义；该相对收益的决策前估计能在相应条件下指导专家选择。

| 章节、代码位置 | 应承担的独立科学职责 | 观察到的正文内容与衔接 | 独立结论 |
|---|---|---|---|
| **§1 Introduction (L31–47)** | 从强 Base 已有历史表示与额外关系证据的冗余/互补张力出发，提出何时知识有新增价值、能否预测，区分两条证据链 | 开篇问题与 C1/C3/C2 贡献逐项匹配，Twitch frozen policy 与 KuaiLive paired context 已有明确分工 | **PASS** |
| **§2 Related Work (L48–71)** | 与真实已发表的历史知识/协作记忆、L2D/uncertainty routing、直播候选评价三类最邻近研究对话 | 承认 L2D、GUIDER、MemRec、Krichene/Rendle 的在先贡献，不称 Δ 或 sampled-metric reversal 为新理论 | **PASS, with novelty-depth reservation** |
| **§3 Problem Formulation (L72–151)** | 以 one-positive \`u_K\` 建立 \`Δ_M\`→\`η_r\`→\`a\`→期望选择收益，定义 target-state 描述性分解 | 决策上下文/事后 target 的信息分界明确；公式与论文中心问题一致，候选制度也是效用定义的一部分 | **PASS** |
| **§4 Framework (L152–236)** | 给出两个平台不同 Base、固定透明 Memory、14 项前验特征和 gate 实际执行链 | 对象清晰，Memory fixed 0.45/0.45/0.10，Figure 1 有离线标签路径与调用路径区分；不是新 memory-agent architecture | **PASS** |
| **§5 Experimental Setup (L237–331)** | 明确 split、候选资格、固定专家/指定 Base、Utility DEV threshold、Difficulty hindsight matched calls、KuaiLive 配对候选构造及 bootstrap | Train/DEV/TEST、目标可见性、不同 model-family 和候选协议均清楚；原始 Base scores 与标准化 reference 区分正确 | **PASS** |
| **§6 Results (L332–499)** | 主要发现 C1→C3→C2，DEV 消融作为支持，CPU 正开销独立报告 | 所有核心冻结效应值/CI 都在对应图表，三类证据分开；负平均 Memory 表现未隐藏，未将诊断当选择器二次 TEST | **PASS** |
| **§7 Discussion (L500–539)** | 超越数值重复：知识互补、候选情境、专家机会 vs Base 难度、有效性与成本、设计原则 | 与正式 L2D、MemRec、GUIDER、sampled metric 建立明确理论/经验层级的关系；对跨平台和部署没有过度声称 | **PASS, scope-specific** |
| **§8 Conclusion (L540 onwards)** | 回答研究问题与统一知识决策推论，避免复制 §7.5 未来工作清单 | 三段总结 Twitch frozen selection 和 KuaiLive candidate context 的差异，末段形成适用于已评价离线设置的综合科学结论 | **PASS；无需重复改写** |

**独立主线判断：** 目前文本已经不再是八组独立实验报告；其中心问题在 Intro–Definition–Method–Evidence–Interpretation–Conclusion 之间具有逐层推进。与 G0 前的评估相比，G1–G4 的主要 P1 叙事缺口已得到有效处理。此判断**不是 KBS 接收率预测**，也不意味着文本已超过所有可能的创新性审稿要求。

## II. Reviewer 对三个贡献的实证挑战

### C1 — 固定专家相对于 incumbent 的条件互补

- **Twitch TEST** 44,221 one-positive 事件；NDCG@10 Base \`0.58211\`、Always-Memory \`0.53980\`；原始配对 Δ **−0.04232**。Recoverable target state n=5,539，mean specialist-minus-Base **+0.22045**，有 paired/cluster bootstrap 区间。
- 这个对照足以证明**总平均表现与条件效用可能分离**。状态是 target-defined retrospective，不是服务端直接得到的观测；文中已保持这点。
- **解释边界：** recoverable beyond input window 的效应不是 Memory 内部因果机制识别，也不能单独证明现有 Base 表示缺失全部该关系信息。不同历史窗口 Base 是分别训练的开发分析。

### C3 — 冻结策略的知识使用决策价值

- Twitch TEST Base \`0.58211\`、Utility \`0.58983\`、Difficulty \`0.58340\`；主文报告冻结 Utility−Base **+0.00772**（95% CI **[+0.00641,+0.00903]**），Utility−Difficulty **+0.00644**（**[+0.00528,+0.00762]**）。Memory 6,650/44,221 ≈ **15.038%**。真正预先冻结的是 **Utility pointwise threshold**；Difficulty/Oracle 的 TEST top-\`m\` 是 batch-level retrospective equal-call controls。
- 模型对比并不证明泛化的新 deferral 理论；科学增量在固定历史知识专家的 relative-ranking opportunity Target 及其离线冻结验证。
- Spearman **0.173**、约 **11.7%** hindsight Oracle gain recovery 显示选择估计已有正排序价值，但还有较大空间。不要把选择策略描述为成本最优。
- **内部显示精度检查：** 五位小数已四舍五入的表格均值直接相减可与报告的未舍入 paired mean 相差 **0.00001**（如 0.53980−0.58211≈−0.04231 vs raw paired −0.04232；0.58983−0.58340≈0.00643 vs raw paired +0.00644）。此属正常显示精度差异，不是经 G5 已证实的数据错误；若未来审稿人质疑，可在脚注一次性说明“differences computed before rounding”。

### C2 — 候选情境与知识价值

- **KuaiLive** 同一已检查 TEST cohort 的 10,222 配对 user--time--target 事件：Memory−Base sampled **−0.04120**、full-active **+0.04631**、paired shift **+0.08751**。
- 2×2 crossed 候选/reference allocation 的**纯数值复核**：A_C=(0.04761+0.04120+0.04631+0.04142)/2 = **+0.08827**；A_R=(−0.04142+0.04120+0.04631−0.04761)/2 = **−0.00076**；两项相加 = +0.08751。三状态的 4,589+206+5,427=10,222，状态分布不变。
- **解释边界：** 已有 sampled metrics 工作早已证明排序模型相对评价可能改变；本稿额外研究的是该现象在固定历史关系专家 incremental knowledge valuation 中的具体后果。训练种子和九个 sampled draws 使用同一 cohort，不能作为独立外部验证；membership mixes size/composition/competition，不是候选数量的孤立因果证明。

### R — 真正计算资源事实

- 另一个 warmed KuaiLive HGB replay 的平均耗时 Base \`0.991\`ms、Selective HGB \`2.007\`ms，额外约 **1.016ms / 2.03×**；Twitch 15.04% invocation 与此成本 benchmark 属不同设置。主稿已明确报告真实正开销而非加速。

**实证结论：** 当前限定在 **指定 Base、固定透明 Memory、Twitch frozen TEST selection + KuaiLive paired candidate regimes** 的主张已经具备可核查的对应证据。统计置信区间解释应继续限于观察队列、模型配置和冻结选择。**G5 未重新训练、重新 bootstrap 或验算所有原始事件，只复核可观察源和统计报告逻辑**。

## III. 最近正式发表研究：真实贡献与剩余接受风险

| 直接相邻工作（官方正式页面） | 已有研究实际做什么 | 本稿可主张的增量 | Reviewer 仍可能追问 |
|---|---|---|---|
| [MemRec, ACL 2026](https://aclanthology.org/2026.acl-long.2061/) | agentic collaborative memory graph/上下文构建及蒸馏 | 指定独立关系专家相对于 trained Base 的增量 ranking utility 与何时使用 | 是否离开简单 fixed heuristic 后仍成立？ |
| [GUIDER, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38639) | 利用 data/model uncertainty 调整 LLM reranking | 以 specialist-specific expected utility 为决策目标，与 Base Difficulty 区别 | 可否与**同等预算的真正冻结 confidence/uncertainty gate** 对照？ |
| [Mozannar & Sontag, ICML 2020](https://proceedings.mlr.press/v119/mozannar20b.html)、[Narasimhan et al., NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html) | 一般 expert deferral/cost/已训练 Base 上后验路由 | 对历史关系知识的 fixed-ranker ranking-specific operational valuation + offline frozen choice study | 科学创新是通用方法还是解释性的实证研究？须坚持后者 |
| [Krichene & Rendle, CACM 2022](https://doi.org/10.1145/3535335) | sampled ranking metrics 可改变模型排序 | 候选环境使“这一历史知识专家是否比 incumbent 有用”的操作性判断翻转 | 可否固定数量只改变 hardness/composition 来解耦？ |
| [DCGLive, WWW 2026](https://doi.org/10.1145/3774904.3792241) | 直播 room/streamer collaboration 强方法 | 不宣称优于其官方异质 task 结果；指定可复现 Base 上评估关系专家增量 | 强 Base 与现代最近邻 comparator 的公平优化预算是否足够？ |
| [KBS 官方范围](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) | 原创 AI 方法/知识系统/推荐/决策支持 | 对知识来源是否值得用于当前 ranking 做可操作、有边界的研究 | 单一 frozen gate TEST 的实证广度能否支撑 KBS 竞争力？ |

**实际核验：** 文献均有真实主办方/出版社正式页面，文章研究目标与正文比较方向基本一致。全部 29 个 BibTeX 条目并未在 G5 中逐一重新向 publisher 校验，因此不能声称“29/29 官方元数据全量人工认证”。源文件含 **29 BibTeX 条、正文 28 个独立引用键**；\`yue2026collappa\` 未在主文引用，编译参考文献实际只列被引用条目，属于 P2 清理项、不是本轮科学错误。[Abbas & Hazen DOI 10.1287/deca.2024.0187](https://pubsonline.informs.org/doi/full/10.1287/deca.2024.0187) 的出版社建议引用年是 **2024**，虽该文出现在 2025 年第 22(1) 卷；现有 \`year=2024\` 并不应仅凭卷期改为 2025。

**最重要的剩余 P1（接受竞争力，而非 manuscript P0）：** 现有实证只在 **Twitch frozen TEST** 验证了 Utility gate；KuaiLive 是 already-examined candidate comparison 而非第二个冻结策略检验。未保证与新一代、同预算训练强 Base 的普适增益。面对要求 broad generality 的审稿人，最有价值的可选增强是对新的公平优化 incumbent/candidate setting **prospectively freeze** 新 Utility gate 与真正 DEV-frozen comparator 后进行独立评估。只有作者决定扩大结论时才把这一点转为新增实验必需项。不能通过更漂亮的 Conclusion 掩盖现有证据边界。

## IV. 论文规范、论证密度与语气的最终判断

- **主线：PASS。** 不再出现明显分散的三项“并列发明”，而是 C1 conditional value → C3 pre-outcome selection 与 C2 operating context 补充诊断。§3–5 实现逻辑与 §6 数值一致。
- **原有反复自我限定：基本解决。** 当前方法章保留关键 target-only、equal-count、within-cohort、descriptive、overhead 说明；Discussion 主要进行知识价值与已发表研究的解释性对话。重复的过程报告已减少且不再支配章节。不能以“not/only”词频代替学术标准。
- **Related Work 与 Discussion：PASS with novelty reservation。** 本稿正面承认前人发明的 deferral 与 sampled metrics。真正的论文定位必须是 **conditional incremental value of historical relationship knowledge for a designated recommender**，不是 general deferral theorem、memory architecture 或 universal candidate-size effect。
- **Methods/Stats：PASS within observable evidence。** 清晰区分 TRAIN→DEV OOF→Twitch fixed threshold→TEST，同次数 hindsight comparator 不是可部署 frozen alternative；KuaiLive fixed raw score/reference 标准化无信息访问混淆。
- **Conclusion：PASS。** 与 §7.5 学术功能不同，未夸大跨平台路由与计算收益。不建议第五次无目标的英语修辞改写。

## V. G5 精确源码完整 PDF 视觉与工程验收（PASS）

| 检查 | 本次实际结果 |
|---|---|
| 来源对应 | [Actions run #38194254351](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38194254351) 使用 G4 \`42d6db84\`，构建已成功 |
| 编译统计 | 最终 **29 pages / 445293 bytes**，0 Overfull hbox、无最终未定义 citations / references；构建已含 PDF verification |
| 真实性 | **重新从 artifact #11723150138 提取 main.pdf** 到 G5 独立审稿工作目录，不以以前 local filename 作证 |
| 文字边界 | PyMuPDF 逐页遍历 **所有 29 页**文本块，**0 页面外溢**、0 空白/极端低文字页；\`pdftotext -layout\`、\`pdfinfo\` 与官方 build 报告一致 |
| 视觉检查 | 将 **p1–p15 和 p16–p29 全部 29 页**分别渲染为双份 contact sheet 并逐页视觉浏览；第 1 页 title/frontmatter、p8 Figure 1、p12–13 方法表、p16 Twitch 状态图/表、p18 策略与候选表、p19 DEV 诊断表、p24–25 结论/参考文献过渡以及 p29 末页均可见；无明显裁切、图表叠压、标题孤立或异常空白 |
| 页面章节导航 | §1 p1；§2 p3；§3 p5；§4 p7；§5 p10；§6 p15；§7 p21；§8 p24；References p25–29 |
| 交叉引用 | 8 个一级章节、28 个 \`\\subsection\`、**50** 个唯一 label，\`\\ref/\\eqref\` 全部有目标 |
| 文献 | 28 个实际引用键、29 个 BibTeX 条、全部正文引用键已定义；无“引用存在却无条目” |
| 提交规范 | 当前 PDF 无 Abstract 且作者为 **Anonymous Authors** 占位；这是投稿材料问题，不是排版成功可以忽略的问题 |

**视觉 QA 边界：** contact-sheet 浏览 + PDF 文本块边界自动检查足以排除大多数明显裁切/遮挡，但不等于逐字符校对或经真实作者批准的校样。新增 Abstract/署名/声明后 PDF 分页必变，必须重新构建并做最终全稿校对；本 G5 PASS 仅属于**当前 29 页源稿**。

## VI. 科学修订 vs 正式投稿包：分别验收

### A. 当前八章科学正文（G5 Gate：PASS with documented reservations）

- P0 科学矛盾或明显伪造/错误引用：**本次未发现**。这不表示实验原始数据已全量重放或通过外部复制验证。
- P1 已由 G0–G4 正文修改解决的叙事问题：引言研究张力、正式最近邻比较、结果发现优先、Discussion 科学解释、方法/协议一致性。无需要立刻重新排版或重写的剩余 P1 **写作缺陷**。
- P1 仍然真实的审稿竞争力保留项：**新的 prospectively frozen selector replication / 强 Base 对照广度**。其必要性取决于目标期刊审稿标准和作者想主张的泛化范围，不能假装已解决。
- P2 清理项：多出的未引用 \`yue2026collappa\` BibTeX 条目（不会渲染到 References）；若受众对 paired raw-difference 的 0.00001 显示差异敏感，可加一次明确 “differences computed before rounding” 的图表注。均非科学 blocking error。

### B. 正式 KBS 投稿包（**HOLD / NOT SUBMISSION-READY**）

1. **Abstract 缺失 — 必须补写。** 从 C1/C3 Twitch frozen selection、C2 KuaiLive candidate regime 和重要结果构造紧凑正式摘要；不能在尚未验收前随机承诺所有平台提升。
2. **作者身份 / 单位 / 通讯作者仍为占位 — 作者提供并核实。** 当前 \`\\author{Anonymous Authors}\` 不能作为常规最终署名直接提交。是否采用匿名审稿版须以目标投稿系统实际要求为准。
3. **2026 年更新的 Elsevier AI-writing declaration — 需要真实作者确认后形成。** 本项目使用 AI 进行了实质性段落重写及组织修改，属于须披露的类别；官方政策要求工具名称、使用目的、作者审阅和最终责任。**不能由 AI 模拟真实作者作出已审阅/批准保证**。
4. **作者正式声明**：利益冲突、资助、CRediT、数据/代码可用性、伦理或授权（仅在适用情况下）；不得捏造无资助、无冲突、全体作者批准或特定数据许可。
5. **Highlights 与 KBS 特别格式**：Elsevier 一般支持 3–5 点 Highlights，但**此类文件是否对 KBS 强制，及其字数/图形摘要/主文长度特别要求未从 KBS Guide 直接核实**。要在正式投稿页面检查后补齐；不用第三方转载猜测现行强制标准。
6. **全稿新 PDF 终检**：Abstract/作者及声明写入后，重新核验章节、图/表引用、metadata、格式、页面及主文/补充材料分工，再由真实作者签发提交版本。

## VII. 审稿综合建议与下一步工作界面

**G5 结论：当前八章已具备清晰一致的学术主论点、可查的 C1/C3/C2 实证及必要的可复现协议。G0–G5 第二轮“论证主线优先”修订和现版本全文 PDF 质量门槛已达成。** 不建议为了追求语言“更积极”而删掉真实的负效用、成本或独立性条件，也不建议无证据地将 KuaiLive C2 说成同一 gate 的跨平台验证。

**后续默认队列（不需要另一次无目标的全文重写）：** 以当前稳定八章为依据，先独立撰写并 reviewer-tighten **Abstract** 和文献适当的 **Highlights**；收集真实作者/单位/声明并按 Elsevier 2026 AI 政策披露；对 KBS 专属 Guide 验证格式；最后做**包含新增 frontmatter 和声明的全稿新 PDF 校验**。如果作者希望进一步提升 broad-generalization 竞争力，可另行批准**独立冻结的新强 Base / 新候选 regime gate replication**，不把它作为已有证据的既成事实。

**冻结说明：** 本 G5 审查只新增独立 referee 报告和项目进度信息。论文 \`main.tex\`、科学数据、原始结果、\`kbs_references.bib\` 及 S1–S9 **未在 G5 修改**。
