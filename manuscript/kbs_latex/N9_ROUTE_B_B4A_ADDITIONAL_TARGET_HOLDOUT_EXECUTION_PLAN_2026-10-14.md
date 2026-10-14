# N9 Route B — B4-A 同期未评价目标的单次冻结验证执行方案

**制定日期：2026-10-14。状态：PLAN ONLY / D0 metadata audit not yet executed。投稿 HOLD。**
**研究定位不变：conditional relationship-knowledge valuation and decision support；不主张新型 Memory selector。**
本文 B4-A 是在**原 KuaiLive-M3 同一采集时期**内，以此前未被 G5 作为目标评价的事件进行 *additional held-out-target evaluation*。不是 2026 年 4 月以后的新数据，不是独立采集的 forward-time TEST，不能宣称绝对从未被任何脚本读取。

## 0. 项目依据与关键纠错

已核查的 G1/G5 源码和报告：
- `experiments/kbs_plan_c/G1_FIXED_DATA_BUNDLE_ACCEPTANCE_2026-10-12.md`：原始合格 TEST 区间共有 **5,124,893** 个匹配直播间与互动时刻的合格交互；G5 实际固定评价目标 **47,575**；约 **5,077,318** 个事件未进入 G5 的目标评价集。**这些只是候选上界，尚未核实 B4-A 所需 TRAIN-known 目标作者、至少两个历史事件、有效 roster 等资格**。
- 目标 TEST 区间从 **2026-03-27 14:00:00** 开始，原始数据收集至 2026-03-31；采用 **原始 timezone-naive 共享时钟顺序**，不得未经证明将其称作真实 UTC。TRAIN/DEV 截点 2026-03-23 12:00:00；DEV/TEST 截点 2026-03-27 14:00:00。
- 数据源 Hugging Face 固定版本 `138d213a23e261ed3094d27ed8a4b867fb9143fe`，输入 SHA、G1 导出 SHA、原 G5 47,575 目标 SHA 和六组既有 Base 模型及 threshold SHA 均已有注册。继续以 **原版原始字节**为准，不改动原 G5 抽样及实验。
- G1 旧哈希为 `hash(user_id, author_id, live_id, observed_at, source_event_id, seed)`，**包含当前目标 author_id**，因此不能将旧哈希复制为 B4-A“目标盲态选择器”。B4-A 改为受控守门者先核实已冻结的合法资格，再以 **SHA256(source_event_id || 新协议公开 seed)**（或仅使用无标签事件元数据）生成一个可复现、不依赖目标作者、目标排序或效用的优先次序。
- G5-A 的 `causal_stream_sealed.parquet` 已把未评价的 TEST 交互当作后续请求的 **past-event prequential history**，且 G1 数据准备确实读过所有事件的 `author_id`。因此不能说 B4-A 作者标签“从未由任何程序接触”：只能通过角色/输出隔离与日志检查，验证未曾作为这些目标的排名评价/调参反馈使用、并保证 B4-A prediction-before-label 单次冻结。
- 所有后 G5 的 B1/B2、E1/E2/E3a、B2 1,024 三种子关系身份结果都属于 50,049 M3 DEV（后者是其子集），不能在 B4-A 使用后重新调参。现有主稿 37 页、S1–S10 编译通过，**本计划不修改主稿，也不启动模型或读取 B4-A 标签**。

官方数据：KuaiLive-M3 https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3 ; benchmark https://github.com/imgkkk574/KuaiLive-M3 。KBS scope https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 。同一数据上的重复适应性检验会损害推断保证，参见 Dwork et al. (Science 2015), DOI 10.1126/science.aaa9375。以上仅说明设计必要性，不代表 B4-A 已获得任何结果。

## 1. B4-A 希望解决什么、不能解决什么

**核心验证（RQ3 / R1）：** 当 Base 与 Memory、同一时刻 full-active F 候选集与预测时可用的决策特征都相同，基于完整 F 值监督训练的固定知识调用策略是否在**新增、目标级不重叠**的评价请求上优于基于 retrospective target-retained S 值监督训练的策略？效果必须按 *full-active F NDCG@10* 和 **实际 specialist 调用比例**一起报告。

**机制验证（R3）：** 正确用户—作者历史对应相对于严格时间合法、用户活动时间与作者小时边际不变、保持排序能力的关系随机化，在**同一 F 候选集**下是否仍有稳定的增量价值？

**不解决：** 真实 2026 年 4 月以后跨时间/跨平台的外部泛化；真实部署成本是否优于 Always Memory；多源关系身份的单变量因果效应；创新路由定理或 sampled-NDCG 一致性新理论。即使这两个测试都支持主张，也只能将论文增强为 *同一采集期中的一次额外冻结目标验证*。

## 2. 执行总览：A0–A7 闸门

| 阶段 | 工作 | 所需权限/输入 | 结果和验收 |
|---|---|---|---|
| **A0** | 数据许可、原 G5 访问历史、候选池与模型来源资格审计 | 原版 G1/G5 SHA、有限元数据；不访问新目标评价质量 | `B4A_A0_BLIND_ELIGIBILITY_AND_LINEAGE.json`；PASS / HOLD |
| **A1** | 受限资格过滤和样本盲态冻结，排除原 G5 目标 | 原始 TEST 元数据；受控资格程序可使用作者 ID *仅判定 warm/room eligibility*，隔离其标签输出 | `B4A_A1_SEALED_SAMPLE_MANIFEST.json`、保密事件 ID 清单 SHA、分层/用户数 |
| **A2** | DEV-only 两种监督模型最终拟合与阈值冻结；一次性主要统计协议 | 既有 50,049 DEV、固定 SASRec/GRU4Rec、未打开 B4-A 评价标签 | 回放实现/权重/门控/阈值 SHA，检验与成本约束冻结 |
| **A3** | 完整候选 F 的 **目标盲态**一次评分；同时生成独立机制子集的无标签三种子对照评分 | A1/A2 PASS，历史输入 strictly earlier than each request | 每目标 top-10 与决策 checksum，**不得算 NDCG、不得读取当前目标作者** |
| **A4** | 核验全部 target-blind 文件 SHA 后 **one-shot** 打开作者标签 | 科学负责人批准，A3 所有预测和对照均已冻结 | 只运行一次评价脚本，不得因结果不佳重训/变更比较 |
| **A5** | 用户聚类配对区间、预定比较及多重性校正 | 固定 A4 无改写评价文件 | 完整正负结果、公平调用表、null nonfloor 检查、审计日志 |
| **A6** | B4-A 科学判定；B4-B 是否继续 HOLD | A5 完整结果 | `B4A_A6_INDEPENDENT_REFEREE_VERDICT.md` |
| **A7** | 只按 A6 裁决定点融入 KBS 正文/补充材料、投稿检查 | A6；人类许可/作者确认 | source→claim、PDF、投稿免责声明；SUBMISSION 未获确认不得 GO |

**不得通过实验结果触发增加样本、改比较方向、筛选有利 Base seed 或调整 S/F 监督规则。**

## 3. A0：资格与历史接触审计 —— 必须先做

**数据版本和合法性**
1. 重新核对 source revision `138d213...`、原 G1 raw `live_interaction.csv` 与 `live_room_meta.parquet` SHA256、G1 causal stream 与房间区间 SHA；发现不同版本即 HOLD。
2. 核对来源许可：KuaiLive-M3 论文对非商业许可的描述与 Hugging Face dataset metadata 的 CC BY-SA 标识存在差异；责任作者须明确 **该固定版本用于论文验证和只公开聚合结果**的资格，并就原始关系边/衍生数据的上传设单独禁止/允许规则。不要向 GitHub 上传用户、作者、互动边和真正 TEST 目标名单。
3. 审计 G5 及其后代码/私有 artifacts 是否有任何对剩余事件的 target rank、target-dependent gain/label、根据这些评价结果的模型选择；仅作为 **较早已发生历史**参与预序列回放，应记录为 history exposure，不等同于对应事件作为评价目标。无法厘清的事件/群体标记不合格。

**合法候选池**：从原 G1 的全时序数据中筛选 `split=TEST`、`source_event_id` 不属于旧 47,575 G5 目标、`prior_events>=2`、当前 `author_id` 属于固定 TRAIN-known warm universe、原 G1 一致 `room.open<=event_time<room.close` 的事件。补充元数据：请求时间分布、唯一用户数、源时间跨度、原 DEV/G5 用户重叠率、后续 F roster 大小、稀疏/高频用户覆盖、上一阶段影响用户与时间窗口。不在公开日志输出作者标签。

**双角色隔离**：一份只运行在受限计算环境、允许读取目标作者 *核对资格* 的 `eligibility steward`，只向后续 `blind scorer` 交付 (source_event_id, user_id, original timestamp, sealed eligibility bit, SHA)，不交付当前 `author_id`。A4 在另一条经 SHA 验证的标签解封路径读取当前作者。由同一 host 执行也必须落实代码/文件权限和独立日志，不能口头称绝对 outcome-blind。

**最重要的禁止项**：不得以旧 G1 hash 的 author-id 输入来决定新的目标优先次序；不得复用已经看过效果的 47,575 G5 请求；不得把 5,077,318 个余量全部称作 warm、有效候选或未被任何研究过程接触。

A0 PASS 的可审计产物：合法余量与排除原因的**聚合计数**、时间/用户覆盖、受限与评估角色读取日志、数据许可确认状态、估计 CPU/GPU 预算及候选可复用性。若实际残余不满足主样本统计精度 / 用户覆盖，立即 HOLD 或在尚未读任何结果前另立缩小统计目标的协议，不得事后偷改。

## 4. A1：新评价目标队列冻结（暂定工程规模）

**建议规模：主目标 30,000 请求；其中另外预定 4,096 请求用于关系身份机制分析。** 这是执行和统计设计的**拟定规模，不是已完成功效分析**；A0 应当用 DEV 的 user-cluster 方差/预期有效用户数进行 outcome-free B4-A 精度可行性评估，确认最低可检测效应与计算预算。若不通过，必须在任何 B4-A target reveal / targeting 前修订冻结协议。

- 优先在原 TEST 区间的 **时间分层（如整日期/时间四分位）× 决策前历史活跃分层**按预定配额取样，覆盖原区间而非只挑效果看好的最后一天。配额仅依据不涉及当前标签的 metadata；在各层按 `SHA256("B4A-V1" || fixed_seed || source_event_id)` 升序选取；同一事件绝不同时归属 G5 目标。
- 4,096 机制样本按**另一预定 seed/hash**在主 30,000 内分层选定；前述 128 pilot 与 1,024 DEV 机制样本因属于 DEV，自然不会落入 B4-A TEST，但必须执行事件 ID 不重叠审计。
- 记录总请求数、唯一用户数、候选 roster 分布和旧 G5/DEV 用户重叠率；**用户不重叠作为可报告的增强条件，不能事后只保留表现较好的无交叉用户**。如果足够多完全独立 G5 用户，可事前冻结主要或次要 user-disjoint 敏感性分析；否则保留整个预定义样本并做用户聚类推断。
- 准备机密 `B4A_30000_TARGET_IDS.sealed` 和 `B4A_4096_RELATION_NULL_TARGET_IDS.sealed`（最终文件名/数量按 A0 锁定），并仅提交其 SHA256、固定 seed、摘要统计和不可更改的时钟/来源摘要到仓库。
- 所有采样和微秒/纳秒单位归一化必须有单元测试、逐事件原 G1 时间戳一致性和全覆盖校验；不得把原 source timezone-naive 时间单方面转换为实际 UTC。
- 设计 **不可改写/版本化** 执行文件，避免失败 rerun 自动覆盖第一次预测/评价；预测尚未开目标时，技术失败可修复且每次更换代码都需新 SHA 与变更日志。

## 5. A2：两条科学问题的可比策略与统计协议冻结

**H1，主论文 RQ3 验证：** 在同一 full-active F author candidate universe 中比较基于 F-aligned versus retrospective S-aligned 增量知识价值标签训练的两个固定 gate。
- Base：SASRec 与 GRU4Rec 各固定**原主 seed 20261012**；不追求 SOTA 模型调优。其余两颗 Base seed 的附加复现只有在 A2 之前明示为次要检验并冻结计算与多重性，否则本轮不跑。
- Memory：原冻结显式 viewer--creator 专家（0.45 长期、0.45 近期、0.10 仅 TRAIN 流行度）。保留原模型权重、历史 max counts、train-known authors、candidate tie convention、历史时序。
- 监督：S-to-F 与 F-to-F **相同 12 个只包含请求前信息和 F 的 Base 打分特征**、相同 HGB(max_iter=120, learning_rate=.05, max_depth=3, min_samples_leaf=50, l2=1.0) 结构与训练预算。S 标签在 **DEV 训练期**是保留真实 target 的 retrospective 575 sampled protocol；S 与 F 都只在相同真实 F 候选集上预测与评价。禁止把 S 的目标保留信息以任何方式当作新 TEST gate 特征。
- 实施上的重要差异：B1 的 **5 outer × 4 inner OOF** 用于 DEV 评估，不是一个已冻结可直接部署到新 TEST 的单独生产 gate。A2 应从现有 DEV 一次性构造最终两套 full-DEV 训练模型，并通过 DEV **用户分组 OOF** 提前确定各自不超过 30% 调用的决策阈值，全部 SHA 锁定；新 TEST 不重新校准。
- 主结果：两个 gate 的 F NDCG@10 差、两个实际 Memory 调用比例/次数与各自较 Always Base、Always Memory 的水平；要求发生在相同固定候选集和模型上。S→F 的训练信息较少，优于 S 只能解释 **评价制度一致性的训练监督价值**，不能解释为新型 gate 架构性能。
- 可比预算规则：共同 **DEV ≤30% 调用上限**，保留 TEST 自然实现的 calls 差。报告真实调用差，不宣称严格等次数。如自然调用比例差超过事先定的 **1.0 个百分点**，则比较只能作为预算非严格匹配的描述；可增加 **预先规定的、仅用 DEV 校准**的同目标调用比例方案作为敏感性检查，但不得根据 B4-A 结果调整阈值。用 E2 的预先定义 lambda 网格表示成本依赖，不把 lambda 当成实际收费。

**H2，关系身份机制验证：** 在提前固定的 B4-A 4,096 请求中保持同一个 F 活跃作者候选集，比较真实固定 Full Memory 与三个预先固定的 **闭合小时、双向作者时刻可用、用户时间不变、作者每小时活动边际不变** 的关系对照。
- 三个 seed 固定 `20261014, 20261015, 20261016`，且沿用 B2 的同代码原始对照 scorer 及无交换自校验。
- 所有 null 必须在目标揭盲前完成原始/置乱 **target-blind top-10** 预测。历史中较早发生的 TEST 事件可作为先验历史，但当前/未来请求 target 不得影响当次预测；source hour 在闭合后才启用置乱。
- 预先设定 nonfloor 诊断（Full F 超出 popularity floor、足够多 top-10 命中、结构保持率/有效更改覆盖），且**nonfloor 不通过即判定机制实验无效**，不可尝试改 seed/弱化置乱来“救”效果。
- 本轮 B2 DEV 的约 78.6% 强干预会改变重复 user-author 对与高阶关系，H2 只能检验“时序/活动边际保持的强关系扰动敏感性”，不能证明某单一关系机制的净因果贡献。

**预先声明的 confirmatory 统计比较集合（拟冻结在 A2）**：
1. SASRec 主 seed：F-aligned − S-aligned 的 30%-DEV-cap gate full F NDCG@10；
2. GRU4Rec 主 seed：同一比较；
3. 4,096 关系子集：真实 Full − **逐请求三个 null NDCG 的预先取平均** under identical F。
采用 **按 user 的 5,000 次配对 cluster bootstrap 95% two-sided CI**；主假设方向若预先声明为单侧，用原 G5 相同的 **5,000 次 user-cluster sign-randomization** 估计原始单侧 p 值，明确其聚类差值符号对称性假设，再对三项主假设的 p 值使用 Holm familywise 校正；同时披露未经校正的区间/原始 p、全部检验/无效结果、请求/用户数、效应方向和异质性。三个 null seed 对同一目标的随机化**不是三个独立 TEST**；对 H2 先在每请求内平均 null 分数再进行用户聚类推断，另报告三 seed 单独数值和 bootstrap 描述性区间。整体分析经过原 G5、B1/B2 多轮研究提出，因此即使 A2 现在冻结，也应保守称为 **预先锁定的追加测试**，而非最初全项目先验注册。

## 6. A3/A4：必须坚持 one-shot prediction-before-outcome

**A3（全部盲态计算）：**
- 在同一条单次、严格按用户时间排列的私有流中，复用 Base 的作者 embedding 和单次 full-active roster；共享 Memory 长/短/流行度计算、F 候选集和 12 维可用特征。
- 使用目标盲态的事件 ID/用户 ID/观测时钟和**严格早于请求时刻**的历史（同一时间戳用原始稳定行顺序），对主 30,000 输出两 Base × 两 gate 的固定 decisions，以及 Base、Memory 的 top-10 作者 token；可附加原 G5 frozen Utility gate 与 Always Base/Memory 等事前确定的对照。
- 对嵌套 4,096 机制请求输出三 seed 置乱 Memory top-10，以及对应原始同代码、无交换控制的 top-10。**不要读/打印/缓存当前目标 author label、NDCG、HR、优势差值。**
- 在私有目录保存 SHA256/数据、模型、代码、阈值、candidate roster、feature schema/顺序、预测/决策数组、事件排序及每步日志。仓库只放 metadata/hashes 和 resource use。任何依赖揭盲后的再评分均禁用。
- GPU 利用率优化以 **真实吞吐、总 wall-clock 与 source stream IO** 为准：单次 CPU historical roll-forward + active roster sweep，GPU 批处理固定 SASRec/GRU4Rec；避免对同一 30k 队列重复扫描全 35M 事件，避免六颗 seed 无效重算；先在**无标签的合成数据**验证代码 parity。
- A3 验收：每目标完整预测/决策覆盖、无未来历史和 source clock 错位、原 G5 共用 scorer 规则通过 synthetic tests、全部文件 SHA 冻结、所有 blind columns 白名单、null 三种子非 floor 的**目标盲态代理检查**通过（真实 NDCG floor只能在 A4 后验证，不能在 A3 声称通过）。

**A4（单次揭盲）：** 独立程序先确认 A3 SHA、目标不可见日志及 frozen comparisons，再从受限 label vault 只读 `author_id` 映射到预先固定目标 ID，计算原封不动的 full F top-10 rank、NDCG/HR 和所有 frozen policies。目标属于有效 F roster 而不在 top-10 时，NDCG/HR 计为零；**目标不属于应有的 F roster 则属于资格／实现矛盾，必须触发完整性错误和显式审计，不能简单计零或根据结果删除**；不能按结果剔除病例、改变模型或再次揭盲并称第二次独立 TEST。即使方向不利，也保留结果。

## 7. A5/A6：报告、失败分支和论文使用规则

| 审计结果 | 允许的论证 | 禁止的论证 |
|---|---|---|
| A0/A1 资格或源 SHA 失败 | 数据资格不可确认，B4-A HOLD | 以未审计余量证明模型有效 |
| 盲态 A3 或因果 history/score parity 失败 | 技术问题，尚无有效结果 | 用无效或已泄漏预测做检验 |
| H1/H2 都有稳定正向支持 | **同一期额外目标集验证了决策监督与关系扰动的可移植性** | 新采集时间段、完全跨平台或“普适因果” |
| H1 正向、H2 null 无效/不显著 | 强化决策后果，关系身份仍限定 DEV | 以 H1 代替机制识别 |
| H2 正向、H1 不成立 | 身份敏感性存在，策略训练监督的决策优势无法移植 | 宣称完整贡献已独立确认 |
| 主要效果为零或负向 | 如实报告 DEV 与追加同期开奖中的差异、重新评估学术贡献 | 倒选 seed、补抽样本或删掉不利结果 |
| Already TEST time-period 的用户/历史有重叠 | 以准确的 **additional same-period held-out-target evaluation** 表述 | "independent new time-period TEST" |

**论文接入（仅 A6 确认后）**：§5 明确 B4-A 的同期补充目标集、抽样条件/角色盲态/作者 ID 历史接触、主次对照、决策预测解封时间；§6.3 报告 H1、调用率及 Always Memory；§6.4 报告 H2、nonfloor 和与 DEV 的差异；§7 讨论旧 G5 同时段与多轮探索带来的证据限制；S10 新增完整 SHA、不同用户/时间层结果与统计。待全部数值检查后才调整摘要与结论。不能事先写入正面效果。

## 8. 人类许可/投稿闸门和最初行动

**科学执行前的硬条件**：固定数据版本合法学术研究许可经作者确认；受限用户/作者历史只在 self-host 执行；若存在完整派生事件名单/关系边公开的许可风险，则仅可发布合法的匿名汇总；模型 checkpoint 与受限原始数据不得上传 GitHub。B4-A 结果不自动解除 KBS 投稿 HOLD，还需 CRediT/利益冲突/AI 辅助科研与写作声明/当前指南/最后一轮人工学术审查。

**建议立即执行的第一步是 A0 metadata-only audit**，输出原 TEST 余量中实际符合 warm author、原 G1 可用性、历史数量、与已评价目标不重叠条件的 **数量、用户数、时间范围与队列有效覆盖**，核对完整禁止集。只有 A0 PASS，才能通过 A1/A2 生成真正的预先冻结一份 **30,000 主目标、4,096 机制子集**，然后进入 A3 的盲态预测。

**本文件仅为执行方案；没有创建 B4-A 新 TEST、没有计算 B4-A 结果、没有打开剩余目标事件进行评价，也没有更改 `main.tex` 或 S1–S10。**
