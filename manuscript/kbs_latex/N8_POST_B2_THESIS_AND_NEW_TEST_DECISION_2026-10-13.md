# N8-RD: B1/B2 后的统一学术命题、KBS 近邻比较与独立 TEST 必要性裁决

**日期：2026-10-13。** 对象：`KuaiLive-Agent` Knowledge-Based Systems 稿件 `main.tex`（commit-independent frozen blob `40be249de52c0ae423b793c0dd4c55f2fdd69f46`），S1–S9 frozen blob `f5575d29ac3de222a04f78b48698cae119eac0bf`。

**证据等级**：原 Twitch/M3 G5 独立冻结 TEST 不动；原 KuaiLive room 回顾性 TEST 不动；新 B1/B2 均为**在原 G5 结果已揭示之后定义、采用同一 DEV cohort、嵌套用户互斥的探索性机制检验**。本文件是审稿式科学裁决，**不是新的实验记录、完成的 TEST 或期刊编辑意见**。

## 1. Executive decision

**推荐：研究主张采取“条件知识价值的候选制度一致评估及决策后果”而非“提出新型专家路由器或生产成本节省”。B1/B2 使第三项组合贡献风险 R3 有实质性改善，但目前仍是 PARTIALLY MITIGATED，R1（近邻原创性）和 R2（M3 无约束 Always Memory 更好且预热路径更快）仍然重大。**

**New independent TEST = CONDITIONAL GO / EXECUTION HOLD。** 若拟将新的“同一任务的候选监督失配→选择损失＋关系来源差异”提升成主文中心、可确认的跨时间发现，一次**事先冻结协议、全新未揭示 outcome 的独立后续时间段**显著增加说服力；但目前仓库及 B1/B2 运行记录只证明存在已揭示的 50,049 DEV 和原已完成 G5 TEST，**尚未证明有合规、完全未查看的额外 cohort**。绝不把重分 DEV 五折、重跑已揭示的 G5 TEST、改变 Base seed 或选取有利既有时间段写成 fresh TEST。没有 eligible holdout 时，本次不授权任何新 TEST。

**不要为新 TEST 牺牲最关键的科学区别**：既有 sampled-metric 文献和 L2D 已分别建立采样比较失真与条件选择；本稿新的经验价值只在于针对**明确、固定、来源可解释的历史关系知识专家**，控制 Base/时间前信息/候选上下文后，说明监督目标失配对**同一 F 排序任务的 held-out gate quality**具有可观察决策后果，并分析历史证据来源与特征的作用。当前仍是应用/测量/决策实证贡献，**不是普适因果定理、崭新路由目标函数、SOTA routing 或生产资源节省**。

## 2. 对原 31 页稿件和 B1/B2 的命题—证据逐项评估

| 科学推理层 | 既有投稿级证据 | B1/B2 新增证据 | 支持程度 / 不能推出 |
|---|---|---|---|
| **C1：关系知识相对价值是有条件的** | Twitch 44,221 streamer TEST：Base .58211, Memory .53980，Utility .58983, calls 15.04%；M3 original TEST 六 fitted Base 共一 author cohort，Memory 整体较强；retrospective target-history 分类 | B2 同一 50,049 DEV：F full .343509；Long .333231；Short .273839；Popularity .022215；shifted placebo .007576 | **强经验支持**：固定历史知识与平均精度不等同；但对目标的“recoverability”是事后诊断；Memory 是特定设计不是可推广最优 |
| **C2：候选环境影响 value target** | 原 KuaiLive 10,222 room TEST **已查看**的 575 vs full 符号逆转，兼有 score-reference 变化 | M3 同一 author DEV，Full Memory vs Long-only：F .343509 > .333231；S .668498 < .773602 | **多任务描述证据有力**，M3 新增同事件来源次序逆转；不单独辨认候选 count，且 S 是**保留已揭示目标的离线采样评价** |
| **C3：价值估计对 gate 选择有后果** | Twitch frozen Utility 胜 Base 与 Always Memory；M3 G5 frozen Utility 在六拟合上对四个指定规则 NDCG 更高、实际 calls 更少，但 **低于 Always Memory** | B1 同批 F DEV：F→F 比纯 S→F +.006159 SASRec（95% 用户 CI [.004835,.007543]）、+.004970 GRU4Rec（[.003550,.006369]）；B2 Long-only +.010605/+ .010262；仅六特征 Full 降为 +.001814/+ .001607 | **首次同 M3 排序任务连通 C2→C3**；B1 观察实际 calls 29–30% 并非完全同率，Short-only 则 S→F 近零调用而 F→F ~15,000 calls；conditional adaptation 使用 F 训练标签，不能宣传 label-free |
| **C4：关系知识源专属性** | 固定 Short/Long/Popularity 专家、历史可恢复子群（后验） | B2 Short/Long 有明显 F 绝对质量，Popularity/shifted 很差；两套特征面板差异 | **部分、不是因果识别**：shifted 仅同事件循环放置、非保留 user/author marginals 的置换；弱控制几乎不被调用有地板效应；Base 分数仍编码历史；模型容量/特征量也变化 |
| **C5：稀缺调用/经济正当性** | M3 G5 Always Memory ~.34679 > Utility .30177–.30400；256-event warmed DEV Memory .803ms < Utility 1.802ms | B1/B2 policy 在每 outer fold 基于 OOF ≤30% 的人为计次 cap 训练；无新的 serving path 测量 | **未解决**。可研究规定调用约束下的质量，但不能写实际 latency/token/cost/energy 的节省 |

因此应在论文中心采用 **C1+C2→C3+bounded C4** 的知识价值使用主线；C5 要限定为实验所指定的资源约束边界，不能当作已经量化的业务收益。

## 3. 一个可审核的 KBS 主论点（英文 argument card）

> **Central claim (empirical and scope-limited).** The value of an explicitly defined relationship-memory specialist in live recommendation is an incumbent- and candidate-regime-relative ranking quantity rather than an intrinsic property of its stored history. On matched decision events, supervision from a mismatched candidate regime changes the value signal used to decide whether to invoke that specialist and can impair full-candidate decision quality; historical relationship components and decision-time evidence determine how strongly this matters. Consequently, candidate-aligned relative-utility evaluation is necessary for interpreting selective use of fixed relationship knowledge under a specified invocation rule.

**严谨的三个递进学术贡献：**

1. **Knowledge-value estimand**：统一在同一 incumbent、同一候选 F 下量化固定关系知识相对效用；支持 Twitch/M3 两种排序单位下历史互补模式（不是提出新采样指标）。
2. **Candidate-regime to decision link**：将 candidate-regime 的 value-label shift 从已知 sampled-metric warning 提升为**同一 author-ranking 任务的 downstream selection sensitivity**。原 KuaiLive room 只作历史配对诊断；**B1 一律标 DEV exploratory**。
3. **Source-specific knowledge-use analysis**：将 Long、Short、Popularity 和 broken-history placebo 的 F/S 排序与嵌套选择对照交叉分析，指出真实长期历史和 online-before-target 特征影响不同制度下的效用预测；**B2 一律标 DEV exploratory，不宣称新的通用选路方法**。

**明确不应出现在题目/摘要/Highlights 的词**：new state-of-the-art selector；cost-saving/deployment-ready；causally proves candidate count；first to demonstrate sampled-metric rank reversal；new consistency theorem；six independent test cohorts；optimal Memory mixture；prospective online target-retained sampled candidate generator。

## 4. 核验过的近邻领域及“究竟新在哪里”

| 原始文献（优先官方来源） | 已经解决的对象 | 本文剩余可辩护的区别 | 新增验证缺口 |
|---|---|---|---|
| Krichene & Rendle, KDD 2020, *On Sampled Metrics for Item Recommendation*, DOI 10.1145/3394486.3403226，https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ | 采样 ranking metrics 不能保留全量模型优劣，甚至期望下 | 把 candidate-sensitive **Memory−Base utility label** 与同事件 **trained selection policy quality** 联系（不是声称首次发现 rank reversal） | S target-retained 是 outcome-dependent **离线评估**，不是原生在线候选 generator；需 independent F test |
| Narasimhan et al., NeurIPS 2022, *Post-hoc estimators for learning to defer to an expert*, https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html | 固定 predictor 后的 post-hoc expert defer、代价条件与 loss 形式 | 基于**关系来源与候选制度定义的 ranking NDCG** 的实际研究对象；不得声称 defer 准则首创 | 与同样 frozen 容量的强 direct/two-stage defer proxy / 同预算公平基线进一步对齐 |
| Mao et al., ICML 2024, *Regression with Multi-Expert Deferral*, https://proceedings.mlr.press/v235/mao24d.html | 单、双阶段专家 deferral、bounded loss、instance cost 的方法与理论 | 不改动其基础理论，以透明关系 source 为固定知识专家，将**candidate regime**视为价值 target 的组成 | 若主张新方法，必须有足够方法层面的独立改进，当前没有 |
| Yuan et al., CIKM 2026 accepted manuscript, *Recommender System as Slow and Fast Thinkers*, arXiv:2609.02671, https://arxiv.org/abs/2609.02671 | sequential recommendation fast/slow path、budgeted selector、质量－计算权衡，含 routing analysis | 本稿的专家是**显式不变的关系知识 ranker**而非 learned slow refinement；研究 utility-label alignment 和 evidence origin，而非 routing 新架构 | 其主文有更完整实际预算/成本代理分析；本稿仅人为 invocation count |
| Xie et al., KBS 341 (2026) 115673, DOI 10.1016/j.knosys.2026.115673, https://www.sciencedirect.com/science/article/pii/S0950705126004132 | 长短兴趣知识多视图融合和多头门控，有多个数据集和消融 | 本稿**不重新训练知识融合编码器**，检验固定外部关系知识相对 incumbent 的最终**decision utility** | 弱专家／历史 placebo 地板效应；缺真实保边际控制 |
| Yerragunta et al., KBS 346 (2026) 116167, DOI 10.1016/j.knosys.2026.116167, https://www.sciencedirect.com/science/article/pii/S0950705126008932 | KB evidence pruning 与多层 conditional gating 互补/重叠，受控实验解释效用来源 | B2 使 relation source × gating/candidate interaction 可在同一排序任务分析 | 审稿人可能要求更强因果或新 test，而非仅观察 |

KBS **官方 scope** 明确包括推荐系统、知识工程、智能预测与决策支持，兼顾方法和应用，但强调原创性：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 。这证明**主题适配**，**不**证明 KBS 录用前景。

## 5. 新独立 TEST 是不是必须做？

**判定：对于“强化后的集成机制主张”，新独立 TEST 强烈建议，且提交该主张为确认性中心结果时应视为条件必要；对于严格限于原 frozen G5 和 B1/B2 探索性解释的经验论文，它不是学术规范的绝对强制项。**

| 研究/投稿选择 | 审稿强度与风险 | 新 TEST 决定 |
|---|---|---|
| **A. 以原 N8 31 页、原两项 frozen TEST 为主，B1/B2 放 supplement，清楚标 exploratory** | 协议诚实、可及早准备稿件；但 R3 “组合重要性”未获独立主结果支持，R1 原创性与 R2 部署场景大风险 | **不是逻辑硬必须**，但严谨的 KBS 编辑可能认为贡献不足 |
| **B. 提升 C1+C2→C3+C4 为论文主线，争取改善 KBS 新颖性/科学说服力** | 同任务机制链明显更完整；B1/B2 同一已揭示 DEV 且潜在后验选择，需避免新发现“事后确认” | **优先选择，但只有在全新未揭示、授权样本可得时启动新 TEST** |
| **C. 声称部署/预算效率（M3 优于 Always Memory）** | 现有证据直接相反，更多 F/S 测试无法弥补 | **NO-GO**，除非先有独立生产级成本定义、路径和条件，否则勿改主张 |

**现在不给新 TEST 自动 GO 的三个独立原因：**
1. **科学身份**：当前没有被核查的原始未揭示 outcome cohort；旧 G5 TEST 已看，B1/B2 DEV 已反复分析。重分用户和新 seed 不创建 independent TEST。
2. **鉴别效力**：仅确认 +.006 NDCG 仍可能被认为是 L2D + sampled metric 的既有现象叠加。新 TEST 必须预先明确 source × regime × decision 的**可拒绝原假设**，并包含不能靠 weak-floor 解释的 baseline/对照；否则耗费算力并不解决 R1。
3. **部署意义**：B1/B2 的 30% threshold cap 是事先定义的*分析规则*，不是实际稀缺来源。必须保留 Always Memory 质量与真实成本反例。

**当前结论：NEW TEST ELIGIBILITY = HOLD (evidence of unused lawful outcome cohort missing); PROTOCOL DESIGN = GO; NEW TEST EXECUTION = HOLD.** 不声称“需要更多实验”已经得到新数据授权。

## 6. 可执行的最小下一阶段（优先级按科学信息增益排列）

**D0 — Author-level contribution choice (no GPU, GO now).** 保留唯一中央论点、精简三项贡献，分开 original frozen TEST / retrospective room / post-G5 nested DEV 层级；优先构思单一 `knowledge source -> candidate-aligned value -> selective use` 示意图与一张 B1/B2 的主要配对表，其余消融与运行证明置 S。单列解答 “为什么 30% 调用规则在业务上重要？”；在没有数据时承认仅规范型 invocation regime。不得把 B1/B2 写成事先确认性比较。

**D1 — Fresh-holdout existence+rights gate (metadata only, ZERO outcome access).** 由合法数据持有人提供新候选时间范围、事件/用户去标识聚合数量、尚未作为任何 train/dev/test/浏览分析的证据、数据访问与许可/隐私使用边界、目标作者资格及可用 F roster 元数据。必须避开已评估原 G5 TEST / B1/B2 DEV 和原 KuaiLive 10,222 room。**此 gate 只可检查 outcome-free 时间区间/许可，不得读取 target 标签**；看不到可用样本则 END，无新增 TEST。

**D2 — Mechanism decision test design (after D1 GO, before labels):** 两位 author-level rankers SASRec/GRU4Rec 选定、Full relation specialist；预定每项比较的 full-active 评价、S 目标保留**仅离线**标签、源消融/对照、主效用对比、自然 calls + 合理调用匹配的 decision-quality curves、cluster unit、校正统计 family、拒绝域、效应 practical threshold（须明确依据 post-G5 DEV 选取）。纯 S→F 绝不以 F 标签校准；任何 F→F 训练数据只来自已允许的 prior labeled training pool 而非 new TEST；所有新候选事件 pre-outcome candidate/prequential history timing 一次冻结。注册文件 hash/commit，防止结果后挑 baseline.

**D3 — One-shot genuinely unseen outcome evaluation (D1+D2 PASS only).** 仅冻结模型、阈值、候选代码与源规则对新 cohort 运行一次；优先 1 Base seed × 2 families，是否加 seeds 只能在看 new TEST 标签前定。同步展示 Always Base、Always Memory、Utility/F-to-F、pure S-to-F、strongest defer control、历史源有效对照。报告 cluster 95% CI 和 multiplicity 对应 prespecified family。统计功效取决于群数/方差，**不能从 50,049 DEV 直接推断新 cohort 一定显著**。

**D4 — Manuscript integration + independent editorial audit (no assumption of success).** 若新 TEST GO 且支持独立机制，重构 abstract/§1/§2/§6/§7/§8 与 S 分工，并明确原 TEST／新 test 研究身份；若 FAIL，保留新结果、主动收缩主张而非换 TEST。最终依然需要数据许可/可复现 archive、作者 AI 声明与签名、KBS 门户当前要求处理。

## 7. 下一阶段 STOP 判据与核心监督

- **STOP science**：只是 S vs F 指标平均差，未展示 held-out policy-quality；强 control 得到相同改善；同预算曲线下效果消失；来源对照只靠几乎从不调用的弱专家制造。
- **STOP integrity**：新 TEST 事实上已经被任何原实验用于阈值调节或作者看过真实标签；样本取自已揭示 G5 cohort；per-user group leakage；缺合法权利/隐私合规证据；需要改写 frozen G5 比较结果。
- **STOP deployment claim**：不能以 calls 替代可验证的时延或成本；在现实 Always Memory 更准更快条件下，不宣称质量–计算收益。
- **Work that should proceed even if D1 HOLD**：研究贡献提炼、探索性 B1/B2 正文/补充分工设计、近邻文献审查、稿件实质技术准确性与信息密度提升；但不得提前提交没有作者批准的图表重构。

**Review conclusion:** R3 **partially mitigated**; new independent test **conditional and presently not authorized**, R1/R2 still materially open; N8 scientific coherence is not equivalent to submission-ready; original submission **HOLD** retained.

## 8. Evidence pointers (exact repo, not synthetic links)

- Original N8 manuscript: `manuscript/kbs_latex/main.tex`
- B1: `experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md`
- B2: `experiments/kbs_plan_c/B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md`
- B2 readback machine aggregates: `experiments/kbs_plan_c/B2_NESTED_DEV_SOURCE_SPECIFICITY_AGGREGATE_2026-10-13.json`
- N8 risk report: `manuscript/kbs_latex/N8_KBS_INDEPENDENT_REFEREE_REPORT_2026-10-13.md`
- Original acceptance/frozen protocol: `experiments/kbs_plan_c/G0F_PRETEST_PROTOCOL_2026-10-12.json` and `experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md`
- User-supplied rights/unused-cohort confirmation: **not in the checked public repo evidence at time of decision**; must not invent.
