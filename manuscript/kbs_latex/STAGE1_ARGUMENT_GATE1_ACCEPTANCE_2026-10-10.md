# 第一阶段验收：大纲—正文—证据的论证主线与修订基线

**审查日期：2026-10-10。阶段：Gate 1（对照分析与事实冻结）——PASS。**  
**执行边界：** 仅新增修订审计 Markdown 文件；\`main.tex\`、投稿导向大纲及 S1–S9 未改变，且未作模型训练、TEST 调参、数值重估或修改实验结果。

### 1. 中心命题、主张顺序与两条证据链

大纲明示的中心问题为：

> The central problem is whether a fixed specialist instantiated from historical relationship evidence improves ranking relative to the trained base on a given event and candidate regime.

这一命题在学术正文中的实质是：**历史关系知识是否应当改变一个既有推荐模型的排序，要由它相对于指定 Base 的增量排序效用决定；价值可随目标历史状态与候选排序环境变化，并能在已验证的 Twitch 条件下通过预先可观测信息支持选择性使用。**

不能把这一命题偷换为以下三种未证实主张：新通用学习延迟/路由算法、跨平台零样本门控复现、候选数量独立的因果影响。本文“General formulation”只表示形式上适用于固定替代排序器，不等于实证外推已被测试。

**大纲预先固定的呈现逻辑为：**
1. **主实证决策链（Twitch）：** §6.1 C1（有 Base 情况下的历史证据条件互补）→ §6.2 C3（pre-outcome relative Utility → DEV-frozen TEST decision improvements）；
2. **并行评价情境链（KuaiLive）：** §6.3 C2（固定事件/固定 ranker 的候选环境变更 → measured incremental value 的符号变化）；
3. **补充解释链：** §6.4 DEV-only 特征/历史诊断 + §6.5 warmed CPU成本 → §7 从两条证据链提炼 knowledge-based recommendation 的 **decision-oriented valuation** 含义。

**严禁为了编号排列而调整 §6.2/§6.3 次序。** C2 是使知识价值的解释**明确依赖 ranking environment**的结果，它不等于 Twitch Utility gate 已在 KuaiLive 发生迁移。

### 2. 逐章主张—证据—解释—职责审查

| 章节 | 应完成的不可替代学术任务（大纲） | 目前可核实证据位置 | 第一阶段发现的主要偏差 | 下一阶段预期修复结果 |
|---|---|---|---|---|
| **§1 Introduction** | 建立“已有 Base 表征 → 额外知识会冗余/互补 → 必须评价新增决策价值”的中心矛盾；以 Twitch 与 KuaiLive 两项互补发现预览 C1–C3 | 大纲 §1.1–1.3；§6.1–§6.3 | 科学张力被场景及实验概述削弱；缺少强而简练的知识使用研究问题过渡 | 引言独立阅读可复述一个主命题、两条证据链、三个贡献 |
| **§2 Related Work** | 正确划开“扩大历史表征/融合证据”与“知识专家相对于既有 Base 的决策价值”，承认 prior L2D 与 sampled metrics | 已发表 MemRec/ GUIDER/ DCGLive、ICML/NeurIPS L2D、CACM sampled metrics | 研究 gap 及对照语句略重复，存在“否定别人工作”代替正面提出问题的倾向 | 一个明确 gap 段落，论证为何该固定关系专家的事件级条件收益值得研究 |
| **§3 Problem Formulation** | 依次定义 offline event NDCG \(\to\Delta_M\to\eta_r\to E[a\eta_r]\to\) regime-level decomposition | §§3.1–3.5 及公式 | 数学主线清楚，少量“后续章节处理什么”的叙述式串联 | 数学对象不动，流程性过渡精简，信息访问边界一致 |
| **§4 Framework** | 把决策对象实例化为 trained Base、独立固定关系 Memory、14 个可观测特征及 selective expert use | Figure 1、§§4.1–4.5、S2/S3 | 方法准确，但部分段落强调组件流水和交叉引用而不强调决策必要性 | 一条 Base→预测相对收益→条件调用的可执行机制 |
| **§5 Experimental Setup** | 一次性固定拆分、候选协议、比较器信息访问、Bootstrap 和独立 CPU 实验 | §§5.1–5.5、S1–S3/S5/S9 | 大体正确；其他章节重复这些 protocol/boundary，§5 职责未充分集中 | 将必要限制性技术披露留主文，其余 run/provenance 留 S1–S9 |
| **§6 Experimental Results** | 依大纲先讲条件效用→选择收益→候选环境，再作 DEV 诊断与独立成本测量 | §6.1 TEST 图/表；§6.2 TEST 选择表；§6.3 KuaiLive 四格；§6.4 DEV；§6.5 S9 | 主结果可信，但 §6.4/§6.3 过程及数值密集；§6.4 的实验列表缺少统一解释职责 | 每节首句揭示发现、核心图表支持、最后一句推出一个有限科学结论 |
| **§7 Discussion** | 解释 C1 的 Base-relative complementarity、C2 的候选环境条件性、C3 的选择意义及知识系统设计启示 | §§7.1–7.5；§6 全部已验收数据 | 13 段中 12 段需要不同强度的编辑，主要是复述 §6 数字/方法限制，而非数据错漏 | 讨论回答“发现意味着什么”，不再成为第二版 Results/Methods 或未来工作清单 |

**当前结构与其学术质量分开评价：** LaTeX 编译、科学数字与引用的先前检查已通过，并不等于上述段落职责也已完成。第一阶段的 P1 评级为**表达和论证风险**，不抹去过去的技术完整性成绩。

### 3. 逐段审查统计与决定

基于冻结版本 \`main.tex\` blob \`5222d53e...\`，对 §§1–7 **95 个 prose units** 实际检查、编号、映射到大纲和证据（不含贡献 \`\\item\`、浮动表/图、公式环境，已在矩阵中另行建非正文账）。

| 章节 | 已审正文段落 | P1 编辑优先级 | P2 编辑优先级 | KEEP |
|---|---:|---:|---:|---:|
| §1 | 6 | 4 | 1 | 1 |
| §2 | 8 | 2 | 4 | 2 |
| §3 | 17 | 0 | 7 | 10 |
| §4 | 12 | 0 | 5 | 7 |
| §5 | 13 | 0 | 1 | 12 |
| §6 | 26 | 4 | 15 | 7 |
| §7 | 13 | 12 | 0 | 1 |
| **合计** | **95** | **22** | **33** | **40** |

**逐段矩阵：** [STAGE1_PARAGRAPH_ARGUMENT_MATRIX_2026-10-10.md](STAGE1_PARAGRAPH_ARGUMENT_MATRIX_2026-10-10.md)；**任务级执行队列：** [STAGE1_P1_P2_EDIT_QUEUE_2026-10-10.md](STAGE1_P1_P2_EDIT_QUEUE_2026-10-10.md)（12 个 P1 主任务与 12 个 P2 配套任务）。

### 4. 对 KBS 学术写作规范的实际执行解释

**正式期刊定位：** [Elsevier Knowledge-Based Systems 官方范围](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)包括知识驱动和其他 AI 系统、推荐系统与预测决策支持，并强调理论/实践之间的平衡。本论文贡献需体现 *knowledge-value assessment and decision making*，不局限为直播推荐技巧。

**常规权威编辑原则：** [Elsevier Guide for Authors](https://www.elsevier.com/subject/next/guide-for-authors)指出 Results 应清楚简练，Discussion 应讨论研究结果的意义而不是重复完整结果，同时 Experimental 部分须允许独立研究者复现。这是 Elsevier 一般性结构指导，**不声称是 KBS 特定的强制 word limit 或标题模板**。

因此：
- 不能删掉 Memory 的整体负收益、KuaiLive CPU 正开销、未独立验证的候选效应与同队列证据界限；
- 可以去掉重复的 \`not a new…\`, \`not proven…\`, \`previously examined...\`, \`originally retained because...\`，或将其迁回集中有效性段落与方法/补充材料；
- 不能以单纯计数 \`not\` / \`only\` 的减少作为文字质量指标。改善的标准是**主张—证据—解释的连贯性、同一事实跨章只承担必要职责**。

### 5. Gate 1 实际一致性检查

| 核查项 | 实际结果 | Gate |
|---|---|---|
| 当前分支与基线 | \`main\` 在第一阶段开始前指向 \`f7cd9e7f48827eaded4109684bda70ee0e84d9ee\` | 基线取得 |
| \`main.tex\` blob | \`5222d53e071987d651e3d5cb2f1a7a51c8323954\`，**当前读取仍完全相同** | PASS |
| 大纲 blob | \`89734dbec9f852fcb728b2ef3a767d19ebe22109\`，**未改变** | PASS |
| 集成补充 S1–S9 blob | \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\`，**未改变** | PASS |
| BibTeX blob（引用基线） | \`358e6599711421ac609cb1956cfc9cd122cdc341\` | 读取固定 |
| 逐段覆盖 | 95/95 唯一 ID，段落位置在源码行号中；P1 22、P2 33、KEEP 40 | PASS |
| 编辑任务 | A01–A12、B01–B12 均列出明确受影响段落、修改要求与验收标准 | PASS |
| 核心数字和证据 | 16 组代表性冻结数值均可在主稿字符串中定位；完整冻结清单更长且指向 S1–S9 | PASS（静态文本一致性；不是重跑实验） |
| 缺少 Abstract / §8 | 明确标记 **未撰写**，未冒称投稿稿完整 | PASS（范围清晰） |
| 第一阶段主稿变更 | **无**，只新增 stage-one 审查 Markdown | PASS |
| Gate 1 总状态 | 中心命题、问题映射、编辑优先级及证据冻结均可复核 | **PASS** |

**提交完成的不意味着第二阶段完成。** Gate 2 仍需对 §1/§6/§7 改写后的实际主稿做独立科学叙事审查、固定证据 diff 检查和源码匹配 PDF 编译；其后才应协调 §2–§5。

### 6. 下一阶段的强制依赖

执行顺序按冻结 [执行队列](STAGE1_P1_P2_EDIT_QUEUE_2026-10-10.md)：

**§1 学术张力及贡献定位 → §6（6.1/6.2/6.3 保持大纲顺序，6.4/6.5 压缩过程）→ §7（7.1–7.5 一次综合修订）→ 交叉章审稿 → §2–§5 一致性协调 → 全文最终验收。**

每次修改均要保存新源码 commit 和旧 \`main.tex\` blob 对照，确保没有 TEST 调参、变量定义漂移、证据符号变化、错误外推或未核验正式文献混入。
