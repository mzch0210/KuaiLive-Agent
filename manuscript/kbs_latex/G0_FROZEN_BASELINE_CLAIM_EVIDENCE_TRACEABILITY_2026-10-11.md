# G0｜八章 KBS 科学主张—证据双向追溯与修订前冻结基线

**执行日期：2026-10-11；阶段：第二轮 G0（主张与证据追溯）。**  
**状态：G0 通过（在当前限定的三项贡献与实验证据范围内）；G1–G5 尚未执行。**  
**修改范围：仅新增审计文件和项目索引；绝不以本 G0 记录替代原始实验或修改论文正文。**

## 0. 原始来源层级与版本冻结

**与本轮工作同步重新取得的 GitHub blob SHA：**

| 冻结对象 | 当前 blob SHA | 实际职责 |
|---|---|---|
| [主稿 \`main.tex\`](main.tex) | \`fa73ba31a56edd96f6eeaca272214b98bf4a9a9d\` | 已完成的 §1–§8、数学式、实际图表及其数据 |
| [投稿导向大纲](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md) | \`89734dbec9f852fcb728b2ef3a767d19ebe22109\` | 原研究命题、C1–C3、主张及叙事职责 |
| [完整补充材料 S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md) | \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\` | 数据、实现、冻结边界、抽样敏感性及独立 CPU 测量 |
| [\`kbs_references.bib\`](kbs_references.bib) | \`358e6599711421ac609cb1956cfc9cd122cdc341\` | 引用与正式发表元数据 |
| [八章 94 段审计矩阵](KBS_SECOND_PASS_94_PARAGRAPH_AUDIT_2026-10-11.md) | \`d4d5e125863f0a543462f8fdb3bef386721bc79d\` | 原句级 P1/P2/KEEP 编辑任务锚点 |
| [第二轮 G0–G5 修订计划](KBS_PAPER_SECOND_PASS_SUBMISSION_NARRATIVE_REVISION_PLAN_2026-10-11.md) | \`03955dbd9a0df7be8069ee40043ad05cf90ecfa8\` | 任务、允许范围、准入与验收条件 |

**重要优先级：** 大纲文件自己明确标注 **INDEPENDENT / NON-AUTHORITATIVE MANUSCRIPT OUTLINE**。其科学写作路线是本次组织依据，**不能凌驾于冻结实验协议、主稿已核实结果或原始实验 provenance 之上**。若编辑用语与实证身份不一致，优先核对方法和 S1–S9 的原始来源，不依据叙事计划推翻实验事实。

**零改动承诺：** G0 不执行训练、推断、统计重估、TEST 自适应阈值选取、S1–S9 覆写或投稿表述重写。后续 G1–G5 必须逐次比较上述旧 SHA，不能以“以前已经审查”代替差异核对。

## 1. 单一中心论点与真正的证据顺序

大纲明示的科学问题：

> The central problem is whether a fixed specialist instantiated from historical relationship evidence improves ranking relative to the trained base on a given event and candidate regime.

**可被全部章节共享、但不应逐章反复复述的中心答案：**

> Historical relationship evidence has operational value through the incremental ranking benefit of a specified specialist relative to its incumbent and eligible candidates; a pre-outcome estimate of this value can inform selective knowledge use.

**证据路线不是“C1→C2→C3”简单编号排序**：
- **Twitch：C1→C3**，有 frozen TEST 历史状态条件效用证据与 DEV-frozen 选择门控的独立 TEST 实证。
- **KuaiLive：C2**，10,222 条已检查 TEST 同队列上 fixed-pair candidate-protocol 的配对评价诊断，不是 Twitch 选择器的跨平台迁移验证。
- **共同结论：** *incumbent-relative and candidate-regime-relative knowledge valuation* 提供有明确适用条件的知识使用决策认识，不证明一般在线服务效益。

## 2. 主张 × 章节 × 来源的双向追溯矩阵（G0 核心产物）

下表以**已有真实标签和段落位置**链接从研究动机到可检验事实，再到讨论与结论；其中 §7 和 §8 的角色严格分离。

| Claim | §1 问题/贡献与 §2 已有研究对照 | §3 形式对象 | §4 对应实现 | §5 实验/合法信息访问 | §6 直接观测事实 | §7 理论/知识解释 | §8 最终回答 | S1–S9 原始支撑与证据层级 |
|---|---|---|---|---|---|---|---|---|
| **C1：Base-relative historical evidence value and conditional complementarity** | §1 前两段、C1；§2 Sequential/long-horizon、fusion/reliability、negative transfer。对应 94 段矩阵 S1-P01/02、S2-P01/02/03 | \`eq:event-ndcg\`、\`eq:delta-memory\`；event-level NDCG@10 和固定专家相对于固定 Base 的 \`Δ_M\` | \`fig:framework\`、\`sec:framework-base\`、\`sec:framework-memory\`、\`eq:diagnostic-states\`，历史状态只描述真实 target 的输入覆盖 | \`sec:exp-data\`：Twitch LiveRec frozen TEST、可用主播/时间边界，指定 Base 固定 Memory | \`sec:results-heterogeneity\`，Figure \`fig:results-evidence-states\`、Table \`tab:results-evidence-states\`。44,221 Twitch TEST，Base **0.58211**、Memory **0.53980**、mean Δ **−0.04232**；recoverable subgroup n=**5,539**，Δ **+0.22045** | \`sec:discussion-operational-value\`：已有 Base 表示的信息可与持久关系证据形成条件互补；§6.4 的不同重训 Base 和 Memory 组件仅为 DEV 解释，不是独立机制因果识别 | §8 P1：整体较弱却在可恢复历史目标群体平均有利，因此有情境依赖的相对排序价值 | **主证据：Twitch frozen TEST 主文结果**；S1/ S2 数据和统计冻结；S4/S6 为 **DEV 分析**，只作补充解释 |
| **C3：prediction of relative specialist benefit for pre-outcome selection** | §1 冻结 Twitch 选择证据与 C3；§2 Expert Routing/L2D、GUIDER。94 段 S1-P04、S2-P04/06 | \`eq:eta\`、\`eq:expected-selective-gain\`、\`eq:utility-threshold\`；目标是 Memory−Base 的条件期望，非 Base 独自困难度 | \`sec:framework-estimation\`、\`sec:framework-controls\`；14 项决定前历史/Base score 特征与 HGB Utility 估计器 | \`sec:exp-comparators\`、\`tab:exp-methods\`、\`sec:exp-freeze\`：Base TRAIN、Utility/Difficulty DEV 拟合、Utility pointwise threshold DEV 冻结；Difficulty/Oracle 的 TEST **top-m 是事后等调用次数** | \`sec:results-decision\`、\`tab:results-twitch-policy\`：Utility **0.58983**，Base **0.58211**，Difficulty **0.58340**；Utility−Base **+0.00772**、Utility−Difficulty **+0.00644**，m=**6,650**；TEST Spearman **0.173**、约 **11.7%** hindsight-Oracle gain 回收 | \`sec:discussion-selective-decisions\`：请求难 ≠ Memory 相对增益高；区别于通用学习 defer 理论，实证检验特定历史知识专家使用时机 | §8 P2–P3：前验特征可预测足以帮助选择的 relative value，并在 Twitch 冻结 TEST 支持条件调用 | **主证据：Twitch frozen TEST 一次评价**，S2 实现/冻结；S7 **DEV-only OOF** 历史/Base 特征族诊断。Difficulty matched-count batch comparator 不得被称作可部署冻结阈值 |
| **C2：candidate environment affects measured relationship-specialist value** | §1 候选变化、C2；§2 Live Streaming、sampled metrics Krichene/Rendle。S1-P03/04、S2-P05/06 | \`eq:event-ndcg\` 的候选上下文、\`eq:regime-decomposition\`；候选集变化时相对效用的观察分解 | \`sec:framework-base\` 双 ID Base；\`eq:memory-scoring\` streamer 关系专家映射至可用 room，target-state 同一事件保持不变 | \`sec:exp-data\` sampled/full active room；\`sec:exp-regimes\`、\`eq:paired-regime-shift\`、\`eq:factorial-allocations\`；固定事件、checkpoint/原始 scores，交叉 ranked candidates/reference | \`sec:results-regimes\`、\`tab:results-factorial\`：10,222 对，sampled **−0.04120**→full **+0.04631**，paired **+0.08751**；membership allocation **+0.08827**、reference **−0.00076**；3 trained checkpoint pairs 和单原始 pair 的 9 draws 均为同队列敏感性 | \`sec:discussion-candidate-regimes\`：已知 sampled metric/model ranking 问题进一步影响“关系知识是否产生决策收益”的操作性判断 | §8 P2–P3：知识价值必须按实际候选环境解释；该证据**并不直接支持跨平台 gate generalization** | **主证据：already-inspected KuaiLive TEST 的配对诊断**；S5 固定 checkpoints + 9 original-pair draws；S8 3 trained pairs + state decomposition。Membership allocation **descriptive**，未独立识别 candidate count 因果效应 |
| **R（成本与实际系统范围；不是 C4 新贡献）** | §1 并未承诺在线效率；§2 已知 experts 有 cost，但不能据此推断本稿节能 | Selective invocation fraction 不等于端到端 latency 的数学结论 | \`sec:framework-controls\` 决策由 Base score/features + gate + conditional Memory 组成 | \`sec:exp-freeze\` 和 S9，独立 warmed KuaiLive HGB/cache replay，**不同于 Twitch policy** | \`sec:results-efficiency\`：Twitch policy 使用 Memory **15.04%**；KuaiLive warmed CPU Base **0.991 ms**、Selective HGB **2.007 ms**，额外 **+1.016 ms** ≈ **2.03×** | \`sec:discussion-validity\`、\`sec:discussion-implications\`：真实 overhead 与选择增益分别衡量 | §8 P3 只断言指定离线任务内 conditional value，没有低延迟或 GMV/用户观看时长结论 | **S9 独立 warmed replay**；原始精度为 Base \`0.990585\` ms、HGB \`2.006624\` ms、差 \`1.016039\` ms；无需将资源测量伪装成端到端在线部署 |

**从表反推的判断：**
1. **Forward audit PASS**：三个贡献在 §1 均有明确起点，在 §3–5 形成可检验对象/条件，并在 §6 具有不同类型的实证支持；§8 的三段未新增未被观测的泛化主张。
2. **Backward audit PASS for evidence existence, editorial P1 remains**：§6.1、6.2、6.3 的核心数字、模型身份、比较器资格均可回指 §3–5；但 §7 的部分解释目前仍重复 §6 的数据和方法边界、§2 的最近邻工作比较较薄。这是**后续 G1/G3 的叙事缺口**，不是 G0 数值或科学来源缺失。
3. **Cross-platform audit PASS with explicit scope**：Twitch 选择器 DEV-frozen/TEST，KuaiLive 是 already-inspected TEST paired-regime diagnostic；G1–G5 必须持续保证二者不混为同一选择策略的双平台验证。

## 3. 不能因为改善学术语气而删除的科学不变量

### 3.1 方法与变量

- 公式：\`eq:event-ndcg\`，\`eq:delta-memory\`，\`eq:eta\`，\`eq:expected-selective-gain\`，\`eq:utility-threshold\`，\`eq:regime-decomposition\`，\`eq:paired-regime-shift\`，\`eq:factorial-allocations\` 均冻结数学意义。
- 固定 Memory 是 \`Short--Long--Popularity\`，不等于新增端到端 memory-agent architecture；14 个 pre-outcome features；target history states/recoverable 属**retrospective labels**。
- 不改变 Twitch 16-context designated Base 与分别重训 8/16/32 context DEV 检查的区别；不改变 KuaiLive room/streamer 两 ID 和 sampled/full-active candidate task 身份。
- 不把“历史存在”与“有因果增量价值”同一化；不把总体负效用删去。

### 3.2 证据与推论边界

- Twitch held-out TEST **44,221**；Utility threshold 事先由 DEV OOF 定，TEST 6,650 invocation 是**实际输出统计**而非强制固定预算。
- **Difficulty** 的训练目标来自 DEV，其 TEST 选取按 Utility 既定 TEST 调用次数进行 retrospective batch top-m；该对照有公平等次数的解释价值，但不等于两个门控都拥有独立 DEV-frozen serving thresholds。
- **KuaiLive** 使用 already examined 10,222 TEST paired events，3 checkpoint pairs 和 9 draws 不独立于同一 user cohort；candidate membership 变化混合 count/identity/hardness/competition，2×2 crossreference 是 algebraic allocation **非因果识别**。
- **CPU** 独立 warmed HGB replay 测得正开销；Twitch Memory 15.04% invocation 不能与该 benchmark 合成统一的 time-saving 叙述。
- **目标指标**是 one-positive offline NDCG@10，不能自动推出线上 watch time、engagement、GMV、真正知识可靠性或跨模型 family 泛化。

### 3.3 最近邻正式发表文献边界

G0 仅验证“需要保护哪些既有思想”并锁定现有 BibTeX 的出版来源，**不重新修改正文文献**：

- [KBS 官方 aims/scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)：知识 AI 系统、推荐、决策支持和理论/应用平衡。此定位不等于 KBS 必须有新的通用定理。
- [Chen et al., MemRec, ACL 2026](https://aclanthology.org/2026.acl-long.2061/)：协作图记忆的构建/蒸馏，并非本稿第一个使用“Memory”的发明。
- [Xu et al., GUIDER, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38639)：不确定性指导动态重排序；相对 Memory-minus-Base Utility 的专门目标仍需在 G1 与之准确比较。
- [Mozannar & Sontag, ICML 2020](https://proceedings.mlr.press/v119/mozannar20b.html) 和 [Narasimhan et al., NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html)：predictor/expert deferral 已建立；本稿目标不是发明 general learning-to-defer。
- [Krichene & Rendle, CACM 2022, DOI 10.1145/3535335](https://doi.org/10.1145/3535335)：已知 sampled item ranking metric inconsistency；本稿的 C2 必须强调该现象如何关联到固定关系专家的**操作性价值判断**。BibTeX key \`krichene2020sampled\` 沿用旧别名，但其记录实际 year=2022，**出版元数据正确，不以 key 片段认定论文年份**。

## 4. 本次 G0 的静态实际检查记录

**成功执行的检查，均来自本轮重新读取的当前 SHA：**

| 项目 | 结果 | 质量门槛 |
|---|---|---|
| 一级章 | **8**（Introduction→Conclusion） | PASS |
| Math/reference label | **50，全部唯一** | PASS |
| \`\\ref/\\eqref\` | 所有实际引用均有 label | PASS |
| 正文 BibTeX citations | **28 个 distinct keys**，对应 \`kbs_references.bib\` **29 条记录** | PASS |
| 不在 BibTeX 的 cited keys | **0** | PASS |
| 未被主文引用的 BibTeX 记录 | **1：\`yue2026collappa\`** | Non-blocking P2 cleanup，G1/G5 可处理 |
| 主文冻结数值 | 对 **23 个代表性核心数字串**执行存在性校验，缺失 0 | PASS：静态字符串核验，非重跑指标 |
| 核心公式 label | 上述 **8 个**均存在 | PASS |
| S1–S9 | **9 个 section header** 均存在 | PASS |
| 第二轮 94 段矩阵 | **94 个 unique IDs**，**P1=23/P2=35/KEEP=36** | PASS |
| 公开期刊与正式最近邻 | 核对期刊官方站、ACL/AAAI/PMLR/NeurIPS 主办方正式页面；BibTeX 现有 5 个关键键与之相符 | PASS（**仅所检关键工作**，非全部 29 条文献逐一重新认证） |
| 摘要与作者声明 | Abstract 仍未写，作者字段仍为 placeholder | **另属投稿包 blocker，不阻断第二轮 G0–G5 正文修订** |

**重要验证边界：** G0 只验证已发表事实与现有来源的可追溯性，不重新执行全量训练、bootstrap、计算延迟或整份 PDF 的视觉检查。G1–G5 每改动 \`main.tex\` 后必须分别通过源码差异与 CI/PDF 验收。

## 5. G0→G1 交付界面与明确停止条件

**G0 PASS 的含义：** 当前限定的 C1/C3/C2 证据及其来源已建立可查链条，原始稿件可进入以投稿论证质量为目标的 G1 文字修改；这**不意味着审稿人必然接受其创新强度**，也不意味着 G1–G5 无需再检查局部科学措辞。

**G1 准入清单：**
1. 仅授权 §1 Introduction 与 §2 Related Work 的定向修订，前七章其它部分和 §8 保留已冻结主张。
2. 从 [第二轮 94 段矩阵](KBS_SECOND_PASS_94_PARAGRAPH_AUDIT_2026-10-11.md) 的 \`S1-P01/P02/P04\`、\`S2-P01–P06\` 着手，先调整重复问题陈述，再进行最近邻的正面研究区别论证；全部引文优先正式出版记录。
3. 每次写入 GitHub 都附旧/新源 SHA、段落 ID 和修改后的学术论证检查；仅修相应章节，不能改变冻结 TEST 结论、方法/历史资格及算法结果。
4. G1 修改完成须建立新的 §1→§2→§6/§7/§8 交叉章“审稿人能否复述中心发现”的验收记录，之后才进入 G2 Results 组织修改。
5. **STOP**：任何语体编辑引入 novel L2D theorem、cross-platform transferred Utility gate、pre-outcome target-defined state、isolated causal candidate-count claim、net production time saving、new test statistical significance，都必须先定位 S1–S9 的证据并重新审查；禁止先合并再“降调”。

**后续总顺序：** G1（引言+文献）→G2（§6 核心结果叙事）→G3（§7 增量学术解释）→G4（§3–5 最小归位、§8 一致性）→G5（八章独立最终投稿论证/源码/PDF 全面检查），再处理尚未撰写的 Abstract、Highlights 和经过作者确认的投稿声明。
