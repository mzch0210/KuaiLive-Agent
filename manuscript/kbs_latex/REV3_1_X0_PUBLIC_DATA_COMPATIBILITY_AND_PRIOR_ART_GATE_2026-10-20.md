# Rev3.1 / X0 — 公开反馈数据与知识调用政策可靠性研究：初步可行性／最近邻排重审查

**2026-10-20 | X0-A OFFICIAL-METADATA & PRIOR-ART AUDIT COMPLETE / X0-B REAL FILE COVERAGE AND LEAKAGE AUDIT HOLD / NO X1 / NO X2 / NO MANUSCRIPT CHANGE。**

> 科学立场：本报告只验证**官方字段/下载/许可文件说明 + RecSys2025论文完整公开网页研究范围 + 项目已有资产**。本轮尚未下载并解包 KuaiRec/KuaiRand 的实际数据矩阵，未逐行计量历史有效率、作者映射或时间泄漏；尤其**未计算任何外部模型质量或政策结果**，不能声称数据适配性最终通过。X0-B的缺口将分门槛待解决，任何HOLD不能偷换成PASS。

## 0. 原项目当前冻结基线与“不是新研究”的部分

Repo \`mzch0210/KuaiLive-Agent\`, branch \`kbs-n12-single-thesis-restructure-plan-20261014\`; X0前HEAD \`bf1bb9516630458c9559d38cb3c29e901ce54f04\`。Rev3.0最近邻文献修订的最后论文科学源 \`a686cd07ce80f8d4090aae720c0e583f39f73176\`，Actions C7 #39398148734/C8V #39398148731 SUCCESS；39页 main / 47页 supplement，PR #6 Draft；NI-1g的V2b sampled-only corrected-S NO-GO 保持不变，原G5/H1均已揭盲。

对当前分支722个tracked文件（完整树不截断）定向排重：9月已有\`EXPOSURE_EPISODE_PROTOCOL.md\`对KuaiLive官方先前曝光未点击样本的方案，其更严格真实target瞬时同活跃房间候选设计仅1/10222满足10负样本；\`KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md\`已经做旧room候选成员×归一化2×2；\`N9_G1_E3A_PAIRED_SOURCE_REGIME_INTERACTION_2026-10-13.md\`已做50,049 DEV的Full−Long×F/S交互；\`N9_ROUTE_B_B2_1024_REAL_RELATION_IDENTITY_NULL_RESULTS_2026-10-14.md\`与H2已做关系身份结构随机化；G4、N10、A1/A2已经做旧gate latency/预算/决策目标。曾开展的有限上下文关系价值与历史短期支持已有报告\`KBS_ROBUSTNESS_RESULTS_2026-09-22.md\`。**重复曝光负例、关系随机化、预算或G2请求换位，不构成Rev3.1原创性提升**。

当前分支路径、相关代码及提交关键词\`KuaiRec\`/\`KuaiRand\`没有发现独立的“近完整反馈下关系Memory资源决策”公开验证；这是一项待确认的新研究主题，**不是**“世界范围内没人研究”的结论。

## 1. 官方公开资源与数据合同：X0-A逐项事实

| X0 项目 | KuaiRec | KuaiRand | 科学限制/验证责任 |
| --- | --- | --- | --- |
| 官方来源 | https://github.com/chongminggao/KuaiRec ; https://zenodo.org/records/18164998 | https://github.com/chongminggao/KuaiRand ; https://zenodo.org/records/10439422 | 官网文档确认；本轮未解压数据 |
| 规模与观测 | small 1,411用户×3,327 videos，共4,676,570，密度99.6%；big 7,176×10,728，共12,530,806，密度16.3% | 27K版本 27,285用户、3,203万item、3.22亿observations；Pure随机池7,583 videos，官网列随机样本1,186,059 | KuaiRec small **不是真实时刻全候选**；缺失0.4%与屏蔽作者有关，不可简单赋予0无偏负例 |
| 事件时间 | \`big_matrix.csv\`/ \`small_matrix.csv\`: \`time\`,\`date\`,\`timestamp\`；实际时序是否可以用big构造small评估user历史未核对 | \`time_ms\`,\`date\`,\`hourmin\`;官网包含random logs 2022-04-22..05-08, standard preceding 04-08..04-21 | 可见时间字段≠证明可泄漏安全地重建所有user/author历史 |
| creator连接 | \`item_daily_features.csv\`: \`video_id\`,\`author_id\`,\`upload_dt\`,\`visible_status\` | \`video_features_basic.csv\` 含 \`author_id\`,\`upload_dt\`、UI/policy字段在logs | creator mapping 是否稳定/非缺失、视频发行时间与历史有交集必须逐文件核验 |
| 反馈对象 | video watch_ratio 或阈值二值标签，属离线反馈代理量；可做多相关度全视频ranking | 12个曝光反馈信号、random vs standard policy，random替换约占0.37% interactions | near-complete feedback≠无偏用户满意、线上因果效用；随机曝光≠所有视频被独立随机展示 |
| 可用候选 | 3327个small items几乎都被用户测到反馈；item upload date存在 | random pool约7583视频，可能有投放/政策场景支持限制 | 必须按时间扣除未来尚未发布或不适用视频；KuaiRec的\`visible_status\`是“当前”而非历史快照 |
| 典型严重泄漏 | \`item_daily_features\` 同一天 \`show_cnt\`,\`play_cnt\`和其它daily aggregate不能用于该天更早请求Z；\`small_matrix\`目标用户后续观看不可进入train/history | \`video_features_statistic\` 按日统计，可能含请求后的聚合信息；Pure**不保留完整序列历史** | X0-B测试日期可得性和同时间戳tie稳定顺序，必要时禁用聚合字段 |
| 社交字段 | \`social_network.csv\`为**user–user**友谊关系，不是本研究的user–creator历史 | 同一user重复author观看可由时序日志重建（真实覆盖未知） | 必须明确Memory来自过去的user–creator视频行为，不能冒称朋友边就是观众-主播关系 |
| 许可证 | 官网GitHub \`LICENSE\`明确CC BY-SA 4.0；Zenodo公开记录Rights/License文字未在当前渲染中显示 | 官网GitHub \`LICENSE\`明确CC BY-SA 4.0；ZenodoRights/License亦缺具体显示 | 官网代码库许可证不自动确定各个Zenodo二次分发内容、派生记录是否符合许可/隐私；权利负责人审查前不释放原始行或creator edge |

元数据来源：KuaiRec README https://github.com/chongminggao/KuaiRec/blob/main/README.md 与 license https://github.com/chongminggao/KuaiRec/blob/main/LICENSE ; KuaiRand README https://github.com/chongminggao/KuaiRand/blob/main/README.md 与 license https://github.com/chongminggao/KuaiRand/blob/main/LICENSE ; Zenodo https://zenodo.org/records/18164998 、 https://zenodo.org/records/10439422 。

**X0外部资源实况**：下载页面声明KuaiRec最新Zenodo ZIP约432 MB，包含small/big矩阵；KuaiRand-Pure Zenodo压缩包约47.4MB，但纯版明确不适合要求完整时序的项目；如果作强时序研究应先考虑1K或27K并审查支持，不能因Pure易下载就代替。数据zip在本轮未成功获得，故这里的数据数字是**提供方统计，不是我们独立重算**。正式X0-B需要核对data artifact MD5/版本hash、压缩内文件目录及实际列值。

## 2. 最近邻必须逐命题对照：RecSys2025已做了什么？

**一手论文全文网页**：Pereira, Said, Santos, *On the Reliability of Sampling Strategies in Offline Recommender Evaluation*, RecSys2025 pp360–369, DOI 10.1145/3705328.3748086, https://doi.org/10.1145/3705328.3748086；开放预印本 https://arxiv.org/abs/2508.05398 。

**已经完成**：以KuaiRec nearly-full user-video test feedback矩阵当作评价truth代理；构造**24种日志生成器**（3种曝光/日志选择方案×8档稀疏水平）与共63个samplers、合计1512评价设置；面向推荐器**模型之间**比较，评估(1)resolution/tie (2) fidelity/Kendall tau (3) exposure robustness (4) model-ranking prediction vs ground truth；负采样从已观察positives保留并添候选负例；对相同用户项目日志/完整观测评价进行比较。使用KuaiRec本身、模拟偏差、同类sampled NDCG、model fidelity作为创新主张会**直接碰撞**该研究，不能作为N12原创新意。

**在查阅的论文正文中尚未看到作为主终点**：固定两位专家中的一位具有关系历史/知识memory，只在部分预目标请求调用；比较两个监督制度训练得出的选择策略在完整multi-feedback评价下的**相同资源约束决策值差**，并设置generic non-memory expert placebo。这个差别仅是**暂未看到直接相同科学对象**，不是证明首次提出，更不是本论文可立即得到新的发现。还需要与选择性预测/deferral literature对比，并在真实数据证明“memory-specific”而非通用模型ranking问题。

**严格禁止结论**：“Pereira 2025只研究采样不涉及曝光”——错误；“近完整KuaiRec天然有无偏用户长期福利”——错误；“所有采样问题首次用于知识调用”——证据不足。

## 3. X0 核心技术障碍：必须能定义独立且可复现的决策量

目标对象不是“两个评分器在某sample上谁好”，而是：
\`eta_G(z)=E[U_G(M)-U_G(B)|Z=z]\`与预先指定资源下完整反馈政策价值 \`V_G(pi_q)\`。这里\`G\`是KuaiRec small matrix事后watch-ratio-derived multi-relevance feedback，**不是直播F原来的single-positive NDCG**，也不是causal online return。

**必须审查的两种KuaiRec时序方案**：
- 方案一：big_matrix合法pre-target用户历史与已发布视频作者关系，用small_matrix近完整反馈**仅做evaluation**；要求真实user交集、视频作者stable映射、历史cutoff、评价日期与测试偏好观察日期相容。未知其有效用户样本数和跨矩阵时间关系，**不允许直接设为PASS**。
- 方案二：使用small_matrix某时间前缀形成过往关系，后续**且当时已经上传并合法曝光可用**的subcatalog形成评价；此时近完整矩阵对同一时间的“几乎全反馈”可能不再成立，不能同时声称完全反馈真值和严格chronological deployment。两者如无法兼容，需要重新限定静态离线偏好代理量，并解释静态偏好/可用性假设。

**必须审查的KuaiRand log design**：单用户有效randomized support和per-item/per-context exposure probabilities/propensity识别；所谓“均匀随机视频池”不等于整个APP候选空间均匀。若无法计算有效policy support/可信权重，不允许IPS/OPE/无偏full-feedback或真实政策价值主张。只能将随机日志作有明确支持范围的描述性稳健性，不冒称近完整随机反馈。

**统计/研究设计边界**：离线50% group-quota toy与在线pmax30%不相同；用户级独立性、作者历史重复、训练校准信息权限、不同full/S supervision合理但不平等的F-label优势、author-level memory与generic second expert正交negative control，必须X1严格预注册。有效corrected-S仍受NI-1g blocking gate约束。

## 4. X0-A当前完成矩阵

| Gate | 状态 | 理由和下一步实际要验证的数据 |
| --- | --- | --- |
| A0 原项目去重 | **PASS (AUDITED_SCOPE)** | 2026-09–10曝光/时序/关系/成本/NI相关旧资产已被明确排除 |
| A1 官方下载与字段存在 | **PARTIAL PASS** | KuaiRec timestamp+author+video反馈; KuaiRand time_ms+author+random logger; **未解压独立核对** |
| A2 近完整反馈评价对象 | **CONDITIONAL / RISK HIGH** | KuaiRec small matrix 99.6%但0.4% blocked author非随机missing；多时间戳的watch_ratio不等于同时刻全部反事实奖励 |
| A3 时序与对象泄漏 | **UNKNOWN/BLOCKED** | 需要实际small/big user交集、metadata upload_dt、creator coverage、可用候选、历史cutoff统计 |
| A4 KuaiRand随机支持 | **UNKNOWN/BLOCKED** | 官网约0.37%替换、random pool≈7583；需要真实propensity/ESS；Pure不适合完整序列 |
| A5 来源许可 | **PARTIAL, AUTHOR PENDING** | Github CC BY-SA 4.0; Zenodo数据再分发与派生许可/权利由人复核，当前不公开原始行 |
| A6 RecSys2025最强先例 | **KNOWN COLLISION** | “KuaiRec+曝光采样+模型ranking evaluation”已被覆盖，只有memory-specific policy estimand也许不同 |
| A7 可否证非平凡新命题 | **HOLD** | generic placebo/control、可部署Z和resource-constrained value需先证实可定义 |
| A8 X1先注册授权 | **NO-GO NOW** | A3/A4/A5/A7尚未解决，当前未批准拟合/路由训练/新政策 |

**X0-A结论：SOURCE_AND_NOVELTY_PRE-SCREEN COMPLETED；OVERALL X0 = HOLD_DATA_AND_NOVELTY_GATE。严格 NO X1, NO X2。** 这不是发现数据不可用，而是不能把官网schema和新命题设想冒充数据审计成功。

## 5. 后续X0-B：合法且读标签前的真实coverage-only核验合同

后续只有在实际下载、校验公开发行文件后才能开始。应先实现**不计算模型得分和政策绩效**的高效元数据审计：
1. 使用官方固定版本/文件hash并统计big/small真实user交集、\`video_id\`/author映射覆盖率、author出现频率、upload-before-event有效率；不得因前置筛选看完整反馈标签后调参数。
2. user cutoff实验：保留未来标签隔离，只计**历史user→author连接**的过去事件数、满足预先声明的history≥h请求率；记录same-day统计禁入Z规则、time ties、作者ID映射版本与small matrix评价候选size/time ratio分布。
3. 检查 99.6% small matrix missing类别中 blocked-video与其它缺失的可区分率；未知missing不能强制当negative。
4. 对 KuaiRand 选1K/Pure/27K前给出policy assignment、随机exposure概率、pool构造及可支持目标policy的ESS/coverage**可验证条件**；1K被抽样后并不必然代表总体。
5. 评估在new data上是否有**真正有用的 viewer→creator memory**而非一般popularity/short context；只可报告数据覆盖，不报告Memory scoring性能。
6. 任何新 X1 前明确数据许可证、允许的再分发/导出边界及作者责任；只有控制这些条件，才能对政策值问题作独立预注册。

**X0-B必要产物**：\`REV3_1_X0B_PUBLIC_DATA_SCHEMA_COVERAGE_ONLY_RESULTS.md\`、可复现的schema-only脚本与文件hash/字段权限表；无训练/DEV/TEST政策指标。必须由脚本真实执行与可信来源产物证明，否则仍 HOLD。X0-B通过后才讨论X1。

## 6. 目标论文/KBS的实际决策，不延误已完成Path A

Rev3.0 P0/P2/P4已完成，现稿39页＋47页且最邻近文献更全。当前论文创新性仍**HIGH-CONTESTABLE**：已知采样评估偏差与现成委托决策的组合风险、weak S、非严格预算、真实上线成本、新时期泛化均未被本X0文献审查解决。

**成功的新研究路线必须是**：合法独立数据 + 可信历史Memory模型 + 同候选与相同资源下的政策层full-feedback gain/regret + 与普通非Memory specialist的negative control + 能说明为何不同于Pereira2025与既有 deferral 的实证机制。若只能得到一般sampled-evaluation fidelity或数据schema上难以定义历史知识，则应执行 \`STOP_STANDALONE_EXTENSION\`，不改当前主稿；返回责任作者的 Path A / HOLD / REDIRECT 选择。

本轮不变：\`main.tex\`、\`kbs_references.bib\`、Supplement、冻结实验、GitHub Actions论文C7/C8V、NI-1g停止裁决、PR #6 Draft和责任作者声明。没有重新打开原 TEST，也没有宣称实际KuaiRec/KuaiRand训练或真实评测完成。
