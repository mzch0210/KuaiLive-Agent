# KBS 八章投稿竞争力第二轮独立核验与“论证主线优先”精确修订计划

**2026-10-11 | 状态：核验及修订计划完成；主稿、实验代码、S1–S9 尚未修改。**

**当前科学基线：** [八章 LaTeX 正文](main.tex)，Git blob \`fa73ba31a56edd96f6eeaca272214b98bf4a9a9d\`；[权威投稿大纲](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md)，blob \`89734dbec9f852fcb728b2ef3a767d19ebe22109\`；[集成 S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md)，blob \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\`；前八章全文 [94 个正文文本单元第二次独立逐段审查](KBS_SECOND_PASS_94_PARAGRAPH_AUDIT_2026-10-11.md)。

**期刊与写作依据：** [Knowledge-Based Systems 官方目标和范围](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)将原创人工智能、知识系统、推荐与智能决策支持、理论和实践相结合列为重点；[Elsevier 的 Results / Discussion 作者建议](https://scientific-publishing.webshop.elsevier.com/publication-process/how-to-write-a-journal-article-from-a-thesis/)强调主结果呈现简洁、Discussion 重在解释和与已有文献联系。均不构成“KBS 必须有 N 字或 M 个小节”的格式规则。

**2026 年正式发表最近邻校验：**
- [MemRec (ACL 2026 long paper)](https://aclanthology.org/2026.acl-long.2061/)，已有 agentic collaborative-memory graph construction and distillation；
- [GUIDER (AAAI 2026)](https://ojs.aaai.org/index.php/AAAI/article/view/38639)，已有 uncertainty-guided dynamic recommendation reranking；
- [Learning to Defer (ICML 2020)](https://proceedings.mlr.press/v119/mozannar20b.html) 及 [post-hoc deferral (NeurIPS 2022)](https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html)，已有 expert-versus-base predictive selection；
- [Krichene & Rendle, CACM 2022](https://doi.org/10.1145/3535335)，已有 sampled ranking metrics/model comparison inconsistency；
- [Xie et al., KBS 2026, 115673](https://doi.org/10.1016/j.knosys.2026.115673)，同目标期刊中正式发表的 knowledge-aware gating / fusion 对照。

## I. 先确认评估真实程度：三项纠偏与四项确证

### 不宜延续的过度判断

1. **“尚未形成任何中心论点”不准确。** 官方大纲、§1、§3、§6、§8 均明确以固定关系专家相对于训练后 Base 及候选集的增量排序价值为中心。问题是多个章节对这一论点的**重复表述多于递进论证**。
2. **“小节多必然违反学术规范”不准确。** §3 五组形式化对象与 §5 数据/比较器/统计职责很明确，不应机械删除必要 headings；§2 和 §7 的过短比较/解释小节更值得优化。
3. **“大量 not/DEV/TEST = 自我否定”不准确。** 目标历史状态是事后标签、Difficulty 只做 TEST top-m 等次数对照、KuaiLive 是已检查 TEST 的后验候选诊断、2×2 是描述性 allocation、CPU replay 有正向 overhead；全部是论文有效性的必要条件，绝不能为“积极语言”删除。

### 经源码核查确实存在、影响 KBS 说服力的问题

- **P1-N1：研究问题的论证张力不够集中。** §1 S1-P01/02（LaTeX L33/35）两次阐明 Base-relative gap，导致“现有 Base 已能利用什么/为什么要评价额外知识”的矛盾未充分推进。
- **P1-N2：最近邻工作的具体关系未被充分阐明。** §2 全部 6 个文本段落分别列举历史/融合/L2D/直播工作，真实引用已有但科学比较基本压缩到每段最后一句；尤其需要明确本稿对已有 L2D、MemRec、采样指标提出的**知识决策解释**而非新通用算法。
- **P1-N3：辅助实验主次失衡。** §6.2 S6-P08–P09、§6.3 S6-P14–P15、§6.4 S6-P17–P23 罗列了选中组均值、DEV 状态富集、seed/draw、Memory 组件、Base 历史窗口和目标 recency；这些主要服务 **(a) pre-outcome prediction sources** 与 **(b) complementarity with what the incumbent sees** 两项解释任务。
- **P1-N4：Discussion 中重复 Results 多于新增科学解释。** §7.1–7.3 反复报告历史状态、candidate membership、Utility 和 Difficulty 及实验边界；§7.5 的 “operational value in context” 再次接近 §1/§8 话语。需要通过理论/经验对话形成比结果更高一级的命题，而不是仅压短文字。

**真正的外部 P1 审稿风险**：本文没有贡献通用新 L2D 定理；C2 的 sampled metric reversal 与已发表研究有联系；对 Base 的强度和外部候选/平台推广的证据有限。必须精确定位已有 C1/C3/C2 的结合贡献，不能靠文字改写假装已验证跨平台 gate、净延迟改善、独立候选数量因果效应。

## II. 不可变的单一主论点与章节证据路线

**大纲中心问题：** “The central problem is whether a fixed specialist instantiated from historical relationship evidence improves ranking relative to the trained base on a given event and candidate regime.”

**可作为英文段落过渡使用的科学命题，不是需逐章复述的口号：**
> Historical relationship evidence has operational value when a fixed specialist improves an incumbent's ranking under the relevant candidate context; estimates of this incumbent-relative advantage can guide selective knowledge use.

**两条独立且互补的证据链：**
1. **主结果 Twitch = C1 → C3**：同一指定 Base 下历史关系知识总体不利、recoverable subgroup 平均正效用；DEV 冻结 Utility policy 的 independent held-out TEST 比较证明预测相对收益可改善选择。
2. **候选情境 KuaiLive = C2**：固定 pair 与 10,222 个已检查 TEST 事件上 sampled-active/full-active 的 relative ranking contrast 符号反转；paired 2×2 分配系描述性；3 trained pairs 和 fixed pair 的 9 draws 是同队列敏感性，不是新独立 gate 检验。

**真实负结果与计算事实**：Memory aggregate Twitch **0.53980 < 0.58211**；Utility Twitch **0.58983**，versus Difficulty **0.58340** at 6,650 retrospective matched TEST calls；KuaiLive sampled **−0.04120** versus full **+0.04631**；warmed CPU Base **0.991ms** versus selective HGB **2.007ms**。保持所有 frozen 数字和置信区间。

**绝对不变：** Results 的 **§6.1 C1 → §6.2 C3 → §6.3 C2** 先后顺序。C1/C2/C3 标签编号不是实验呈现顺序的理由。

## III. 必须先做的“全篇论证图”而非立即全章重写

在任何修改 \`main.tex\` 前，以 [94 段矩阵](KBS_SECOND_PASS_94_PARAGRAPH_AUDIT_2026-10-11.md) 为底建立一个单页 traceability 表，列为：

\`主张 ID → Intro 提问 → Related Work 竞争解释 → §3 定义 → §4 实现 → §5 信息访问/对照 → §6 数据 → §7 解释 → §8 结论 → S1–S9 来源\`。

**必须检查三种关系：**
- **前向完整性**：每个核心主张最终有冻结事实支持；Method 不引入无法检验的能力承诺。
- **后向独立性**：每一个重要 Results 解释能指回 Intro 的科学问题与准确观测；§7 不是第二份 Results。
- **跨平台证据层次**：不能把 KuaiLive 用于说明 gate deployment 或把 Twitch target-state 分组当在线可观察特征。

合格后才允许正式修改正文；使用该表作为所有阶段的返工判据，**绝不重新做没有具体缺陷的单节 tightening**。

## IV. 正式修改顺序（任务 ID、源码定位、所需产物及验收）

### 阶段 A — 中心科学问题与最近邻定位（先 §1，后 §2）

| 编号 | 源稿定位 | 实施动作 | 验收标准 |
|---|---|---|---|
| **A1（P1）** | §1 S1-P01/02, L33/35 | 把“强序列 Base 已获取部分历史关系 → 额外关系历史可能冗余/互补 → 应检验固定知识专家在特定请求的增量价值”写成连续论证，不要在两段重复提出同一 gap | 独立阅读引言首两段，能说明研究矛盾以及为何现有 evidence fusion/表示增强不能替代 operational assessment |
| **A2（P1）** | §1 S1-P03/04、Contribution \`itemize\` | 直播场景只解释历史关系可持续、候选环境可变这两个变化源；预览 Twitch 冻结选择与 KuaiLive 后验候选评价的互补性，贡献与之逐一吻合 | C1/C3/C2 是**证据递进**而非三个分散“成果”，没有推导出跨平台 gate |
| **A3（P1）** | §2 S2-P01–06 | 可试行将五个过短 headings 精简为 **3 个主题**：(i) history & knowledge representation/fusion，(ii) L2D / specialist relative choice，(iii) live ranking and candidate-based evaluation。各主题至少出现一次“别人精确解决了什么、本文有何不同研究对象”的具体对照 | 所有保留/新引研究均可追溯正式版；对 MemRec、GUIDER、L2D、Krichene 不作稻草人化比较，不声称 Δ、采样反转和通用 defer 首创 |
| **A4（P1）** | §2 Research Gap + §1 C1–C3 | 与审稿人可能的 strongest alternative interpretation 对话：何以不是现有 L2D 的直接迁移或 sampled metric 的再次发现？把主张收束为历史关系知识对**incumbent 的任务级价值评价与选择**的联合证据 | 不夸大理论新颖性，但能清楚回答 KBS 审稿人的“为什么值得发表” |

**标题调整只在实际段落对照确认有利时执行**。不为凑固定 700/900 字或减少 subsection 数机械增减内容；增补文献仅限对创新区别有直接贡献的最新正式出版工作。

### 阶段 B — 结果证据由“实验日志”转为“发现序列”（重点 §6，保持 6.1–6.3 顺序）

| 编号 | 源稿定位 | 实施动作 | 验收标准 |
|---|---|---|---|
| **B1（P2）** | §6.1 S6-P02–04 | 保留 aggregate disadvantage 与 recoverable large positive 对比，结尾导向“能否在不见 target 的条件下预测有利请求” | state 后验性在主文清晰，表/图各有独立用途 |
| **B2（P1）** | §6.2 S6-P08–10 | 以 Utility–Base 和 Utility–Difficulty 的 frozen TEST 证据为主，selected/unselected 和 DEV enrichment 作为解释，详细诊断主依 S7；保留 oracle gap 的真实大小 | 同调用数对照不是 prospectively frozen Difficulty threshold；不把 selected-mask 均值当独立第二次验证 |
| **B3（P1）** | §6.3 S6-P11–16 | 核心 pair reversal 与 2×2 crossed-score allocation 主文完整保留；three trained seeds 与 nine candidate draws 合并为简洁方向性稳健陈述、数值仍在 S5/S8；对 sampled-metric 文献的理论含义留给 §7 | 不能把九 draws 说成三模型 pair × 九组试验；不声称 candidate count 因果；主文和 Supplement 完整匹配 |
| **B4（P1）** | §6.4 S6-P17–23 | 以两条解释轴重组：**history+Base score descriptors predict relative utility**；**Memory components and incumbent history coverage change complementarity**。将七参数 grid 和 target-specific recency 作为辅助 DEV 证据归 S4/S6，主文保留必要结果与 §6.4 feature table | 不将 DEV OOF 消融、重训长度变体当 untouched TEST；§6.4 结尾是新结果层面发现而不是新“我们没有做什么” |
| **B5（P2）** | §6.5 S6-P24–26 | 正面报告真实 KuaiLive CPU overhead 与单独 benchmark 条件，避免层层解释 caching/mask/complexity | 15.04% Twitch call rate 不等于服务速度收益，正向 overhead 绝不删除 |

**重要原则：** 该阶段的成功不是少了多少文字，而是主文表格/图/段落全部直接支持 C1/C3/C2；原始数值、CI、Figure 2、policy table、crossed-factorial table、DEV ablation table 和 S1–S9 保持可追溯。

### 阶段 C — Discussion 从结果复述变成可检验的知识系统解释（重点 §7）

| 编号 | 源稿定位 | 编辑目标 | 验收标准 |
|---|---|---|---|
| **C1（P1）** | §7.1 S7-P01/02 | 把 relationship evidence 对现有 Base 的 **redundancy/complementarity** 写成科学解释，联系已有知识融合/负迁移文献；避免将 retrospec state 说成直接已证明内部表示缺失 | 比 §6.1 新增一个清楚的解释，而不是重新报告 subgroup gain |
| **C2（P1）** | §7.3 S7-P05–07 | 对 expert opportunity vs Base Difficulty、决策目标与既有 L2D 理论的差异做实质对话；引用最近正式版，论述 Utility 选择为何符合研究问题 | 不能把既有 conditional selection/expected utility 原理说成本文新理论；不能忽视 0.173/11.7% 的预测局限 |
| **C3（P1）** | §7.2 S7-P03/04 | 解释已知 candidate sampling ranking comparison 问题为何会改变“应使用哪一项历史知识”的操作性判定；同时说明固定-scores crossed reference 的描述范围 | 从已知 sampled-metric 文献推出的**特定知识评价启示**清楚，而非声称首次发现 sample reversal |
| **C4（P1/P2）** | §7.4/7.5 S7-P08–11 | 保留 Twitch/KuaLive 离线证据层次与单独 CPU 代价；减少结果数字、证据声明和未来工作重复。可尝试合并为 “Scope and Implications” **仅在实文可读性变好时** | 每个段落新增解释价值；与已完成 §8 final Conclusion 区分：§7 谈为何/对研究意味着什么，§8 讲本文实际建立了什么 |

**讨论结构建议（可试稿比较，不强制）：**
- 方案 C-A：保留原 7.1–7.5，实质重写重复性段落；
- 方案 C-B：合并成 **3–4 个含义清楚的小节**，例如 (1) Incumbent-relative complementarity and selective use，(2) Candidate-context valuation，(3) Scope and knowledge-system implications。
使用独立 reviewer 盲审选择更有科学解释密度的版本，**不能仅以少两个 headings 作为改进证据**。

### 阶段 D — 对稳定 §3–§5 作最小必要的责任归位；§8 仅一致性检查

| 编号 | 修改范围 | 动作 | 验收 |
|---|---|---|---|
| **D1（P2）** | §3 S3-P01–17 | 保持全部数学式及其依赖次序，压缩多次解释同一 Δ/η/threshold 的说明；formal states 是 descriptive decomposition | 科学对象和公式完全一致，target-only 不进 serving |
| **D2（P2）** | §4 S4-P01–12 | Figure 1、固定专家评分、强 Base、14 个 pre-outcome 特征、选择规则各司其职；把重复执行细节导向 §5/S2 | 不更改 0.45/0.45/0.10，系统结构不失去可复现性 |
| **D3（P2）** | §5 S5-P01–13 | 使 TEST/DEV freeze、Twitch pointwise threshold 与 Difficulty TEST top-m、KuaiLive fixed-pair crossed candidate 归到唯一清晰协议位置；重复模型参数或采样细节转 S1/S2/S5/S8 | Data leakage 和对照公平性明确，关键 protocol 仍可从主文理解，不能把必要 protocol 全挪走 |
| **D4（KEEP/P2）** | §8 S8-P01–03 | 仅对照经过修改的 §1/§7 复核术语和两条证据链；无具体矛盾不再重复重写 | Conclusion 保持科学准确且不成为 Discussion 副本 |

## V. 完全独立于文字修订的“追加实验是否值得”决策关口

这些不是上述 A–D 写作改进的默认前置条件，按主张广度分为：

**现有冻结证据足以支持的限定结论：**
- Twitch fixed Base、fixed Memory 的 realized conditional value；
- Twitch DEV-frozen Utility selection 在一次 untouched TEST 对 Base 和 retrospective matched-count Difficulty 的增益；
- KuaiLive fixed-ranker/candidate-protocol 下的 measured sign reversal 和描述性因素 allocation。

**只有打算扩大主张时才评估新增证据：**
1. 若宣称对“不同强 Base 普遍有效”，应对额外公平优化的强 incumbent 建立新的 prospectively frozen gate；S3 非统一训练预算下的数值不能自然替代。
2. 若宣称“跨平台/候选情境 gate generalization”，应在独立候选协议或 held-out new evaluation cohort 上提前冻结 threshold/feature transforms 并验证，不可将 KuaiLive 已检查 TEST 候选反转解释为已验证 transfer。
3. 若宣称“candidate count 的独立因果作用”，需要等数量而不同组成/难度的 controlled sampling；现有 membership term 包含 count/composition/competition。
4. 若宣称部署速度/资源节省，应做 pointwise full-path end-to-end 测量；现有独立 warmed KuaiLive HGB replay **实际增加**平均运行时。

**如何决定是否需要新实验：** 先完成 A–C 的完整学术对照，再做 KBS reviewer-style novelty challenge；如果强审稿问题涉及当前主张必需的科学依据而非推广雄心，则升级为新的实验需求并单独制定方案。绝不能默默以“语言优化”增强未被测试的结论。

## VI. 投稿级学术表达规范：该删与不能删

**减少：** 重复 gap 句、每段 “we first / then / lastly”，反复说明 “not general theorem / not serving feature / not causal count / previously inspected TEST”，重复的 seed/run/mask/path 比较过程，Results 与 Discussion 对同一三组数值的逐字复述，空泛 future work 列表。

**保留：** 必要证据等级及科学信息访问、负平均效用、positive CPU overhead、target-dependent 后验分组、Difficulty retrospective TEST top-m、KuaiLive post-hoc protocol、candidate decomposition 非孤立因果、不同 Base separately trained。

**优先用正面陈述呈现可被支持的研究发现：**
- 不以 “This is not a new deferral theory” 开段；可写 “For a fixed relationship specialist, predicting its advantage over the incumbent addresses a different ranking decision from identifying hard requests.”
- 在 §6 主文写 “The paired candidate comparison reverses the relative ranking of fixed models under the studied protocols”，而把 membership mixes composition/count 的解释放 §5+§7 各一次。
- 在计算成本写 “The warmed scoring benchmark adds 1.016 ms over Base under its measured conditions”，避免笼统声称“选择性调用更高效”。

**禁止只统计否定词来验收。** 高水平学术写作的检验标准是每段的**明确研究命题 + 精确证据 + 非重复新增解释**。

## VII. 修订实施管理和正式验收门槛

| Gate | 执行动作 | 独立审稿通过条件 |
|---|---|---|
| **G0 科学冻结** | 保存原稿源码 SHA、outline、BibTeX、S1–S9 SHA；建立 94 段→C1/C3/C2 traceability | 不存在找不到冻结来源的核心实验断言；主张与大纲一致 |
| **G1 主张形成** | A1–A4 §1/2 修改与引文正式发表版核验 | 审稿人只看 §1/2 就可说明 Base-relative 问题与 MemRec/GUIDER/L2D/sampled metrics 的实质区别 |
| **G2 实证叙事** | B1–B5 §6 修改，保留原顺序与主图表 | TEST vs DEV、三种证据等级和 S1–S9 全部准确；Results 主文不成为运行日志 |
| **G3 机制解释** | C1–C4 §7 修改并与 §6 逐段反向对照 | Discussion 每段提供超出 Results 的理论/机制/文献解释，无明显重复 §8 |
| **G4 方法保护** | D1–D4 §3–5/§8 最小修改 | 所有数学意义、固定参数、特征/标签可观测性、候选资格及 comparator 信息访问保持完整 |
| **G5 KBS 完整论文审查** | 全文 reviewer-style 复核创新、证据、语体、引用、图表、LaTeX、PDF | 未解决 P0 科学矛盾为 0；主要叙事 P1 有明确证据支撑与修订 diff；提供主张→证据矩阵，最终源码 PDF 编译/版面无异常 |

**每次 GitHub 正文编辑必须遵守：**
1. 只改获准章节，先获取最新 blob SHA；保留 commit 和段落映射日志。
2. 数值、公式、浮动图表、S1–S9 默认 frozen；如确需修改须先做证据 provenance 复核与单独授权说明。
3. 源码差异与冻结 baselines 比较，检查 citations、cross-references、公式、图/表编号与 PDF 编译状态。
4. 若改动影响已确定的证据等级，先停止合并，核对原始数据，不通过修辞掩盖矛盾。
5. 只有 G5 后才撰写 **Abstract、Highlights 和作者核实的声明**；最新 KBS-specific Guide for Authors 的具体要求另行通过官方页面或投稿系统核对，不猜测字数限制。

**本计划与前次四阶段计划的区别**：此次不是再次把所有章节重写一遍，而是对已存在的中心论点进行**精确论证递进修复**，把真实 reviewer-risk (近邻增量与 Discussion 科学解释) 同正常的科学限定和已有可复现性分开。**下一步实际编辑从 G0 的 traceability 锁定及 A1 开始，而不是先把 §7 或 §6 大段文字任意精简。**
