# N12-C8V Rev2 I0 | 跨版本证据台账执行及公开来源自动验收（2026-10-19）

**本轮判定：PUBLIC_SOURCE_MACHINE_PASS / HUMAN_SCIENTIFIC_REVIEW_PENDING。** 此文档不是全部私有原始数据重跑、所有历史文件逐行审核、主文已编辑或责任作者签名。

## 已提交成果与实际成功运行

1. `N12_C8V_REV2_EVIDENCE_LEDGER.json`：14个具不同估计对象的记录、8个样本/父子关系，15条原始GitHub Actions运行凭证，字段包括：来源文件及真实Git blob SHA、科学估计对象与代表统计量、使用的同/不同cohort、证据等级、原工作流结果、当前主文/Supplement位置、限制和下一动作。旧 `N9_P0_B1B2_CLAIM_SOURCE_COHORT_REGISTER_2026-10-13.csv` 是B1/B2更细的先存源表；正式I0总账**复用**，不宣称取代旧22KB逐条claim CSV。
2. `analysis/kbs_plan_c/n12_c8v_i0_evidence_ledger_audit.py`：对每个引用公开文件按真实Git blob `SHA1(blob size\\0raw)`核对、检查核心值/原文关键词与证据类型，并明确定义50,049共享DEV、1024/256 DEV子样本、同期间30,000额外目标、4096嵌套H2、原47,575 TEST的层级。
3. `analysis/kbs_plan_c/test_n12_c8v_i0_evidence_ledger_audit.py`：通过4项测试，包括故意把源SHA变错、共享DEV依赖和DEV证据等级检查。
4. [**Actions #39224636666**](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39224636666)：`public-ledger-integrity`作业**SUCCESS**，日志 `I0_PUBLIC_SOURCE_BLOB_AND_COHORT_CONTRACT_PASS`：**14 records、8 cohort groups、14 checked blobs、15 recorded runs、4 tests OK**。公开运行凭证此前经GitHub API查询，包括B2原上传故障Run #38367721633 **FAILURE**和补恢复Run #38369503457 **SUCCESS**；不能将第一次失败当成整个私有计算无效，也不能说原workflow完全成功。

## 典型去重发现

- B1三臂DEV、B2五来源、G1来源候选交互、G2调用切换、A1八档预算、A2 Direct/Two-stage共享**原50,049请求/12,628用户**；分析和报告数目不等于独立数据集数目。
- B1 Adapted→F**包含F监督标签**，不等价于不使用F训练值的corrected-S。B1原三臂无需重做。
- B4-A额外30,000为同录制期、事件ID与已评分G5不同，H2 4,096为其中的嵌套子集；不能视为真正新日历期独立复现。
- B1A 92.83%零支持是Full-vs-Long来源差，不是Memory−Base标签零支持；需要防止跨估计对象换义。
- A1八额度、A2 Direct/two-stage和N10已做旧pointwise timing，默认不得安排重复实验。
- 1,024 DEV Null验证过其自身TRAIN-only Popularity，对B4-A 4,096队列原预揭盲Popularity子门槛仍NOT VERIFIED。两个样本不能相互补充预先验收。
- H1 F监督配置在额外30,000上相对所测S具有更好加权NDCG及更少**原始调用次数**，但不支持强同调用标签因果分解。

## 公开QA通过不能取代的I0余项

- 当前14条优先估计对象的**执行run API身份与报告内容**已经抽查确认，但个别早期Twitch和原KuaiLive room实验只有冻结主稿原始表作为来源起点（ledger标注 `FROZEN_MANUSCRIPT_BLOCK_ONLY`）；需继续追溯最早执行脚本/run，不能认为已覆盖全部项目实验。
- 自动契约仅保证源文件blob完全一致及关键原文存在，不保证每一个新增解释都逻辑正确。原CSV中的每一条B1/B2细粒度claim尚未全部转为长期审计检查。
- 还需做至少一次跨研究者的人工抽样：正文/Supp原估计对象、CI/p和加权率与调用次数是否对应，核对G5、B4-A前置锁定和H2例外；填写签署人/日期/争议项，不得由助手冒充外部审核者。
- 私有self-host DEV/TEST逐事件记录及模型权重未读取，也未独立复算置信区间；禁止称“全项目结果从零复现”。
- 近期最后一版主文的科学/双PDF QA沿用此前 [#39218602150](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39218602150) 37p+47p SUCCESS。本轮**没有改动主文/补充材料，因此没有再次构建PDF的必要**。

## 下一执行关口

**I0 SOURCE MACHINE CHECK PASS，I0 HUMAN REVIEW PENDING。** 新版次序仍是I0→I1（旧B1/B2/A1/A2/G1/zero-support/Null证据综合）→V2a（corrected-S适用性核验）→仅有科学新意才V2b→I2→责任作者C8。禁止把I0代码质量验收当成学术创新性认可；未获得真实科研作者审阅不得声称最终Go。
