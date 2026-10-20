# N12 Rev3.1 — 全历史去重后的公开反馈／知识调用决策可靠性研究修改计划

**2026-10-20 | PLAN_ONLY / SCIENTIFIC FEASIBILITY HOLD / MANUSCRIPT NOT MODIFIED / ORIGINAL TEST NOT REOPENED。**

## 0. 为什么修订 Rev3.0？

这不是第五轮“补写实验”，而是对 2026-10-20 Rev3.0 P0–P5 的条件性**科研扩展决策**。截至本计划前仓库 HEAD `aa414fa2edb12f3f61dd8905c76e727448c2d80f`；现稿科学源 `a686cd07ce80f8d4090aae720c0e583f39f73176`，对应 C7 #39398148734/C8V #39398148731 **SUCCESS**；主稿39页、Supplement47页，PR #6 Draft、责任作者P5未签署。P0/P2/P4已完成的最近邻引用和质量核验继续有效，NI-1g V2b NO-GO 继续有效。

KBS官方 https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 指明推荐系统、知识工程和智能决策支持、需要 original/innovative 结果；“更换数据集”、“加入sampling bias图”和“添加已知deferral”均不足以单独作为 KBS 新颖性。当前N12的核心是固定Base/关系Memory的全候选相对效用监督及请求级调用。Rev3.1只能新增**确有证据的外部决策可靠性**；不得改写核心主张来迁就新的短视频任务。

## 1. 项目历史真正已做什么／没有找到什么

本次核查当前分支 **722个受控文件，Git树未truncated**；对9月与10月重点报告、脚本/工作流路径及当前提交历史中KuaiRec/KuaiRand关键词做了定向检查。**结论仅限当前可访问仓库/分支，不证明私人未提交实验或其它分支绝对不存在。**

| 新建议主题 | 已完成或已探索的资产（严格区别原任务） | 新意裁决 |
| --- | --- | --- |
| 真实历史未点击曝光稳健性 | `EXPOSURE_EPISODE_PROTOCOL.md`：官方`negative.csv`约1270万条，前168小时未点击10例protocol，原“同时刻仍活跃”严约束仅1/10,222达标；工作流`exposure-episode-dual-id.yml`及coverage、robustness辅助代码。没有已知propensity；历史暴露不是同一target即时slate | **已探索，不能重新称首次曝光偏差研究** |
| 候选制度、score normalization | `FULL_ACTIVE_DUAL_ID_RESULTS_2026-09-21.md`, `KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md`：同旧room 10,222、相同checkpoint 2×2候选membership与标准化对照、三seed。 | **已做，不能重测旧room为新确认** |
| 真实关系×候选来源交互 | `N9_G1_E3A_PAIRED_SOURCE_REGIME_INTERACTION_2026-10-13.md`：Full-vs-Long F−S交互 +.115382，同50,049DEV、92.83%至少一个zero；`N9_ROUTE_B_B2_1024_REAL_RELATION_IDENTITY_NULL_RESULTS_2026-10-14.md`：3 seed时间/活跃结构保留randomization，1024DEV；H2嵌套4096也已做composite rewiring，pre-unseal部分未验证 | **机制路线已经探索；只在新独立数据、真正正交且弱扰动等前提下再注册，非本计划默认** |
| 成本、预算、选择 | 旧latency代码`analysis/inference_latency_ours.py`, `analysis/gate_compression_latency.py`, G4 256DEV warmed memory-vs-gate; A1八档、A2目标、G1 shadow price已做；Always Memory无quota更准、旧门控更慢 | **新vectorized F gate未全路径测时是有限缺口，沿用 Rev3.0 P3-A，不另建重复课题** |
| 监督、校正、识别 | B1/G2/H1三臂、原S/F call changes，V2a、NI-1b–f，NI-1g sampled-only real model NO-GO; 旧 TEST 已揭盲 | **不得新训练V2b；不能把新toy当原稿核心Results** |
| 完整反馈/随机曝光驱动的知识调用政策可靠性 | 本次当前分支文件路径、定向报告及提交/代码检索未找到**KuaiRec/KuaiRand独立实验、代码或冻结政策结果** | **现有项目的未覆盖候选；外部文献创新性与数据协议尚需更强审查** |

## 2. 关键外部文献：候选方向此前已被谁做到哪一步？

**已知直接竞争者不能忽略：**
- Gao et al., *KuaiRec: A Fully-Observed Dataset and Insights for Evaluating Recommender Systems*, CIKM2022, DOI 10.1145/3511808.3557220, https://github.com/chongminggao/KuaiRec 。小矩阵1,411 users×3,327 videos、4,676,570 interactions、99.6% density；原作者提供时间戳、watch_ratio和item_daily_features的author_id。**大量反馈不等于无曝光偏差的因果真偏好、也不等于直播author候选快照**。
- Gao et al., *KuaiRand: An Unbiased Sequential Recommendation Dataset with Randomly Exposed Videos*, CIKM2022, DOI 10.1145/3511808.3557624, https://github.com/chongminggao/KuaiRand 。从随机干预pool选择、原日志仅约0.37%是替换干预；完整政策价值识别仍需实际propensity、overlap/支持、时序和有效样本量。绝不自动称“unbiased full preference matrix”。
- **Pereira, Said & Santos, RecSys2025, DOI 10.1145/3705328.3748086, https://doi.org/10.1145/3705328.3748086**。已经**使用KuaiRec近完整矩阵**，设置uniform/popularity/positivity模拟logger和多种候选sampler，评估四类模型级sampling reliability。**因此KuaiRec + exposure + sampling + model ranking Fidelity既有先例；这是 Rev3.1 最大 originality kill gate。**
- TRACE-Memory (2026)已有相对public-only记忆增量效用的个人化文本生成预印本 https://arxiv.org/abs/2608.08446 ；KDD2020/AAAI2021/AAAI2023/CIKM2024与ICML2024已覆盖通用sampled evaluation correction/deferral。项目也已纳入近邻BibTeX，新增研究不能宣称这些原则首次提出。

**剩余有条件区别**：Pereira等研究的是“sampling是否忠实比较不同推荐模型”，Rev3.1尝试研究“既定历史关系Memory相对Base的**请求级知识调用政策**，会不会在模拟曝光/采样监督与几乎完整用户反馈评价间发生资源受控的策略regret”，包括candidate-indexed paired gain、预目标可见特征、分配集合、历史知识source null以及任务迁移约束。**区别对象≠证明非平凡新意**；正式方案仍需一篇篇阅读全文核对是否已有决策层相同控制。

## 3. Rev3.1 唯一候选新增研究命题（未经证实）

**X1 / cross-task decision-reliability**：在新公开数据上，固定同一Base/Memory、候选宇宙和事前决策特征，如果部分曝光／负采样监督导致的**知识调用政策**与近完整反馈下较优调用决策发生系统差异，该差异能否在相同*预注册资源预算*下表现为真实full-feedback ranking utility loss，而不只是两模型全局好坏的指标波动？

严格分清 3 个不同估计目标：
1. 现稿 M3：单真实target在author F上 single-positive NDCG@10；
2. KuaiRec：全部观测用户-视频反馈定义的**multi-relevance**视频ranking效用，可能另有日志式single-positive proxy，两者不能混为同一个 `Delta_F`；
3. KuaiRand：随机暴露支持条件下的观察反馈，非complete preference truth，且其最优政策/IPS/OPE必须有真实propensity与正支持，否则只报告描述性对照。

**最小新增贡献只有在满足“已有sampling评估错误 → 特定固定关系历史专家的额外调用分配错误 → 预注册资源条件下可信独立评价下降”完整链条后才考虑作为新证据**。允许零效应或反例：若真实多反馈下Memory无帮助或original S与F调用近似，则不强行移入N12。

## 4. 执行阶段及停止条件（全部需要逐次授权）

### X0（立即执行：READ-ONLY 科研与数据权利适配审查，不能跳过）

**任务**：
- 完整阅读2025 RecSys的方法与代码，判定是否已经实现直接可用于知识调用政策的结果；与其它2024–2026 personalized memory/defer工作做逐命题重合矩阵，给 novelty score **LOW/HIGH-CONTESTABLE** 但不捏造KBS接收概率。
- KuaiRec核验 `big_matrix/small_matrix` user_id overlap、时间字段缺失、同user过去关系是否可从`big_matrix`合法恢复、视频`author_id`覆盖和是否与回传式反馈一致、items upload_dt 是否在请求时间有效、3,327 video场景是否有真正的可用F。要预先确定哪些离线“almost full”响应在evaluation才读取，不得进入pretarget Z/history/model checkpoint/threshold。
- 版权/数据许可分别检查公开GitHub源代码和Zenodo数据文件的许可版本（仓库CC BY-SA 4.0不自动证明所有派生发布方式合规）。不能私有导出KuaiLive用户或身份映射加入KuaiRec。
- KuaiRand审查哪些policy产生真实random logs、随机pool=7583、约0.37%替换及是否有**用于该policy estimand**的conditioned propensity；对有效样本量ESS/overlap做先验可行性范围，不能把各user/author IDs跨KuaiRec/KuaiRand/KuaiLive相互对应。
- 当前文件路径/提交/执行资料没有出现专门KuaiRec/KuaiRand实验：作为**候选新增研究**，非“已验证可用”。

**X0交付**：`REV3_1_X0_PUBLIC_DATA_COMPATIBILITY_AND_PRIOR_ART_GATE.md`，逐条 VERIFIED / BLOCKED / UNKNOWN；包含“可用字段—时间风险—反馈对象—权利—计算成本—novelty先例—可能的反例”。不得在X0读公开矩阵标签后调后续研究方法；可做小规模schema/coverage仅无模型质量分数，留审计哈希。

**X0 STOP**：没有有效的时间防泄漏历史、creator或candidate对象无法对应、反馈稀疏/随机暴露支持太弱、许可不清楚、或RecSys2025已覆盖唯一声称的创新结果，则 STOP_STANDALONE_EXTENSION。恢复P5责任作者决策，不向原稿加“外部验证”。

### X1（X0通过后：预注册协议，不运行TEST）

**事先冻结**：目标任务粒度（video还是creator）、固定Base与同一Short-Long-Pop样式Memory是否语义有效、时间与train/validation/test user拆分、近完整矩阵仅评估用的multi-relevance指标、日志proxy指标、按用户聚类CI、统一的candidate/抽样事件池、有效的历史零假设和至少一个控制知识专家（no-history/popularity）以区分memory effect和generic sampled evaluation。若选择用KuaiRec全部反馈当truth，应标记其是事后测得的用户视频偏好proxy，不是online causal welfare。

**策略公平**：固定两个专家checkpoint和部署时可见Z，原uncorrected S、full-F supervision的标签信息差别预先披露；相同适当部署约束下比较policy full-feedback quality、actual calls和switch patterns。严格区别外部fixed call budget（在线经DEV threshold的realized-test calls未必正好相同）与TEST批次offline TopK/Oracle。现NI-1g阻断的有效sampled-only corrected-S不能凭外部新数据自动放行；如果缺少有力对照，不得声称排除修正后的S。

**最强阴性对照**：同样候选/监督机制下不含relationship Memory的fixed generic second ranker；若政策可靠性损失并非关系知识特异，应降低“relationship-specific novelty”，只能形成generic decision robustness事实。

**终点注册**：主estimand(一个)和次要量、预算值、纠错准则、最小有意义效应阈值与不确定性区间、误差/多重比较族、负结果、提前STOP规则；绝不能把以前已揭盲的G5/H1 TEST用于模型选择。

**X1交付**：`REV3_1_X1_PREREGISTERED_EXTERNAL_POLICY_PROTOCOL.md`及仅用于schema/leakage的QA脚本，用户/事件ID分配SHA与数据许可表。未经作者审批不得开始任何训练或score。

### X2（可选：仅X1和数据权利准入均通过，真正一次新实验）

仅对冻结公开数据cohort执行合法的train-only拟合、CV OOF校准、一次独立heldout policy validation，保持项目已确立的Base/Memory/candidate identity parity。报出主指标、paired user uncertainty、policy calls、conditional realized Full value/decision regret、source null和full-feedbackvslogged-proxy分歧，同时诚实报出Always Memory与成本。实验可失败，不多次挑更好seed/pool/threshold。KuaiRec新数据不等于对KuaiLive-M3直播任务“独立未来时期”验证；如果研究目标从直播换为一般短视频推荐，稿件正文不得隐瞒任务变更。

**X2交付**：独立工作流、实验冻结注册、公开汇总和分层结果、私有/许可保护、阴性结果、复现命令。X2仅在X0/X1真批准后执行。

### X3（有新科学证据才修改论文，不破坏Rev3.0验收）

- 若X2强且经独立确认能证明与RecSys2025不同的policy-level/knowledge-source机制，首先判断 **附录S11紧凑外部验证** 与**独立后续论文**哪个更符合KBS的一条主论点；主文最多新一小节 external decision reliability，加短段 Discussion解释 video vs author、multi-feedback vs single-target、显式日志 vs simulated exposure 的 estimand变化，不能改原H1、RQ3的冻表。
- 若X0不合格或X2阴性/仅模型排序层面已有结论：**NO_MAIN_TEXT_CHANGE**。可保留内部负结果报告，不强行加入39页主文或47页Supplement；E6继续可独立做稿件决策。
- 任何真正改变论文科学源的更新都需 C7/C8V 两条真实成功、PDF页码/引文/内容实物核验、具体SHA；不能用旧 `a686cd07...`的success冒充新CI。

## 5. 沿用而不重复建立的两条路线

**成本**：Rev3.0 P3-A已有细致合同；若有真实quota/权限/算力瓶颈，才更新“**最新版向量化 F**”全路径同硬件p50/p95/吞吐等，和Always Memory公平比较。不能将G4旧点测重复提交为创新性新试验；若new gate仍慢且不更准，则公开放弃部署节约主张。

**关系机制**：N9 Full–Long×F/S、1024 DEV three-null、H2 4096都已有。下一轮只有**新独立样本与弱干预真正可隔离关系身份**才具可信科学增量，不得把先前`Gamma`旧聚合重新标为新发现。

## 6. 期刊创新性、执行优先级和终态选择

| Gate | 客观通过条件 | 决定 |
| --- | --- | --- |
| C0 历史去重 | 当前主分支旧曝光、B2/G1、H2、成本和NI已逐项核实 | DONE_FOR_AUDITED_ASSETS |
| C1 新任务适配/数据权利 | 合法时序、关系专家、同候选、近完整或随机反馈、无target泄漏、许可与作者确认 | PENDING |
| C2 与RecSys2025及deferral的非平凡区别 | 有预注册policy-level + memory-source-specific estimand，不能只是复制ranking fidelity/EM | PENDING / HIGH_RISK |
| C3 科学预注册和独立确认 | 真实训练/估计和user-split frozen holdout，负面分支，统计权重与预算清楚 | BLOCKED_UNTIL_C1_C2 |
| C4 论文集成 | 新结论与live-streaming主线、估计量/时间任务一致，科学源与CI正确 | BLOCKED_UNTIL_C3 |
| C5 投稿 | 责任作者真实作者/贡献/许可/AI披露/KBS Guide核验及本人GO | PENDING |

**建议优先级**：先X0，只做一次read-only外部数据和方法适配核查；X0失败则绝不开启X1/X2，也不推迟原稿无限等待。若X0通过且真的发现独立的knowledge-call policy科学问题，由责任作者选择“本篇新增外部验证”或“保留原39p+47p Path A，另开独立研究”。不假定进一步新研究一定能使KBS录用；新的公开数据无法自动解决原H1严格同预算比较、有效corrected-S缺失、真实服务成本或KBS journal originality门槛。

**当前终态**：REV3.1 PLAN_ONLY / X0-X3 NOT STARTED / EXISTING PAPER SCIENCE FROZEN / REV3.0 P0,P2,P4 DONE / P1 AUTHOR ITEMS PENDING / NI-1g NO-GO / ORIGINAL TEST SEALED-AS-REVEALED / PR #6 DRAFT / KBS NOT SUBMITTED。