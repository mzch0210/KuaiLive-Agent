# Rev3.1 X0-B: KuaiRec 真实元数据审计与实验适配性裁决

**2026-10-20 | REAL DATA AUDIT SUCCESS / PRIMARY BIG→SMALL HISTORICAL MEMORY PATH NO-GO / X1-X2 HOLD / SCIENTIFIC PAPER UNCHANGED**

## 一、实证来源与真实工件

运行 [#39410776300](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39410776300) 完成 **SUCCESS**（科学脚本 commit `517f12a2a69653b8198bba5fd6d6f1cdeef954cb`），包括官方 Zenodo API checksum、数据 ZIP 下载、MD5 验证、元数据覆盖审计和聚合 artifact 上传。聚合 artifact ID `12259272122`，GitHub ZIP digest `sha256:4e0087b1d0f4dca4d00ff5b01ff644490717e9a1c9eed50d02a728e6cc50d0b6`，官方文件 MD5 `261550d472c48eff4990fb13c0e5bcf7`，预计 2026-11-19 过期。仓库只保存公开**聚合结果** `experiments/kbs_plan_c/REV31_X0B_KUAIREC_REAL_METADATA_PUBLIC_AGGREGATE_2026-10-20.json`，没有上传原始用户—视频或历史关系记录。

实际解析数据：Small 4,676,570 行 / 1,411 用户 / 3,327 视频，唯一配对 4,676,570，密度 99.6202494%；缺失/无效时间戳 181,992（3.89157%），1,411 人至少一个有效时间戳。Big 12,530,806 行、7,176 用户 / 10,728 视频，时间戳缺失 0；small用户与big重合 1,411。daily metadata 343,341 行；10,728 个视频具有作者和upload_dt，作者冲突与映射缺失 0。

**严格历史定义**：Big 的事件时间 **严格小于用户 Small 最早*有效*时间戳**，而不是依赖结果标签；这个近似只应视为**潜在历史的乐观上界**，因为Small缺失时间戳的行可能存在更早事件，且尚未核实Big来源事件的实际曝光有效性。

严格Big→Small prehistory：269/1411用户至少有一个过去作者（19.06%）；16/1411有≥5位不同历史作者（1.13%）；1/1411有≥10位（0.071%）；仅7/1411用户具有作者重复记录（0.50%）；≤492个潜在pre-first-small Big历史事件（不能把这个数据等价于合法、重复、可决策的关系）。**数据设计与真正长期关系Memory使用的问题不匹配。**

上传时间核查：0行 Small date < video upload date；363,557 Small事件与上传同日，不能证明同日具体时间已发布；4,131,021行在上传日期之后；181,992 行时间/日期或upload日期无法核对。daily stat存在当日后见信息泄漏风险，因此不允许作为早期决策时预可见 Z。

## 二、为什么成功运行≠科研可行性通过

**Primary design GO/NO-GO: NO-GO**。原X0目标是独立公开数据中可因果时间排序的user→creator历史Memory，再与几乎完整Small多反馈比较受预算调用policy的质量。观察到不足1%的用户具有重复历史作者，严重限制历史知识的作用、有效样本量、分层方差和可检验效果；3.89% Small时间缺失会使“最早有效”历史的资格偏乐观，故不能把 7 当作可靠的严格有重复历史用户总体。只有一个用户≥10位历史作者也无法支持丰富历史知识机制。不得因为另一个样本切分更多行就称该估计目标仍成立。

**Small内部时间切分**：可以在原则上获取更多历史，但会使Small将不再作为同一时刻同一catalog的99.6%几乎完整后验评价矩阵。历史时间与观测反馈时间混杂；时序标签缺失和上传可用候选均须重新定新目标。这不是原X0科学命题的“直接修复”，属于新的研究设定，需独立先例对照、作者批准、预注册和合法新确认数据；**不直接授权 X1/X2，也不调用训练资源。**

**KuaiRand**：为不同的随机曝光日志研究对象，未运行官方真实文件 MD5/propensity/support/ESS审查。不可用KuaiRec的本次成功替它判PASS；不未经核查宣称可做unbiased online OPE，若另行研究应先独立数据准入，而非自动启动训练。

## 三、KBS和新颖性门槛不变

RecSys2025 Pereira/Said/Santos 已在 KuaiRec上做近完整偏好、曝光和采样条件下的**模型排名可靠性**；本轮数据结果不建立独立的“relationship Memory policy value”研究对象，不能向现有N12主文虚增第三数据集或新的因果结果。KBS需要实质原创性，已有sampled metric bias + deferral的组合风险仍高；Rev3.0论文科学sha `a686cd07ce80f8d4090aae720c0e583f39f73176`、C7/C8V (#39398148734/#39398148731)，39p+47p，PR #6 Draft，NI-1g V2b NO-GO不变。作者AI与数据权利、期刊专属Guide与最终提交 P5 仍待真实作者确认。

## 四、执行决定与可选方向

1. **X0-B 数据文件审计完成**；具体初始设定 `KuaiRec Big prehistory → near-complete Small heldout` 正式 **NO-GO**，不要进行X1模型预注册、X2训练或本稿S11外部实验。
2. **不自动切换到 small 内部时间切分、KuaiRand 或旧M3 TEST**，因为它们改变estimand或存在另外的支持/许可前提。
3. 保留两种由作者选择的独立未来动作：a) 返回已通过科研技术验收的N12 Path A，解决人类作者声明与KBS指南并决定投稿；b) 另行注册KuaiRand随机化支持/propensity或全新未来时段直播数据的独立可行性项目，先审计数据与已有先例，在未准入前不影响N12。
4. 禁止把本轮结果描述为“Kuairec没有历史”或“外部验证一般不可能”：仅是**明确的先前Big→首次有效Small设计**历史稀薄。研究主线可独立推进，但需不同可辩护的数据合同。

**最终状态：X0-B TRUE RESULTS RECORDED / SELECTED DATA PATH NO-GO / X1-X2 NOT STARTED / MAIN/SUPPLEMENT UNTOUCHED / NO NEW CONFIRMATORY NDCG OR CAUSAL RESULTS.**
