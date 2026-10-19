# N12-C8V V0 | 论文语义错误修复及防回归检查执行记录

日期 2026-10-19。此文件是**已实施改动的过程记录，V0完成与否以独立新CI为准**。受控工作分支 `kbs-n12-single-thesis-restructure-plan-20261014`；不触碰冻结G5、A4/B4-A TEST、模型和阈值。

## 1. 主稿已经实施的四处精准修订

- **Abstract** 将错误的 “the policies disagree on 21--23% of Memory invocations” 改为明确请求分母 “development analyses of 50,049 requests ... 21.32% of SASRec requests and 23.01% of GRU4Rec requests”；分子仍是10,672、11,517个DEV事件。
- **RQ2 Results** 明确F冻结政策对比受检S冻结政策具有更高20-cell加权F NDCG与更少**未加权实际**Memory calls：SAS 8704/9105；GRU 8629/9168；1.337/1.797pp调用率差超旧1pp同调用解释阈值。这不是严格等额度的isolated label effect。
- **RQ3 Results** 明确三Null还具有每seed 1903–1913 Top-10 positives及76.78–76.80% historical rewiring，并通过现有的ranking/support/rewiring nondegeneracy checks。原同cohort TRAIN-only Popularity prereveal subgate没有按承诺验收，不能追认PASS；也不能称整个H2无效。
- **Discussion** 改用 “control checks partially completed” 的准确语义，不用“所有控制条件失败”的暗示。
- 以上均为**陈述修订**，未改变主文Results冻结表格、原模型、数据、p值、CI、阈值与统计估计。

## 2. 工程质量：为何旧绿色CI不足

- C7旧成功run **#39217601692** 已在论文修改commit `f22e5251fa18f1f73e45ae1cf185c44221d0a74a` 上确认此前冻结科学检查和双PDF构建，**但不具备语义分母错误的可判别单元测试**。
- 新增 `analysis/kbs_plan_c/n12_c8v_scientific_semantics_audit.py`，检查DEV 50,049分母及准确百分比、H1实际调用对比及weighted/raw单位、H2通过与缺失的子验收、rank unit/DEV/H1分层、旧Utility时间对象与核心引用。
- 新增 `analysis/kbs_plan_c/test_n12_c8v_scientific_semantics_audit.py`：对真实论文验收，并**故意篡改**摘要分母、DEV分母、H1调用数、H2验收条件、DEV accounting的因果级别，测试必须拒绝错误。
- 新建 `.github/workflows/kbs-n12-c8v-v0-semantic-pdf-qa.yml`，继承C6/C7冻结表格、9+2公式、主文+完整补充PDF、交叉引用与零overfull检查。旧C6/C7 PASS不被覆盖或回填新验收。
- 新工作流初次run **#39218342607** 报告1个 mutation test失败：原审计器只检查数值在整个RQ2章节存在，导致正文调用数被篡改时可由冻结表格内的正确数值掩盖；**这是审计器的假阴性，不是论文实验错误**。已在后续commit `26525af9e218081f988872c3e78f9e285f79e92a` 将原调用配对检查固定到比较表之前的解释性段落，继续以新CI判定。
- 若新CI未完成或失败，V0必须维持 **IN_PROGRESS**；不得声称科学审稿已经确认了所有自然语言论断。人工独立科研审读还未签署，后续不得用自动PASS冒充人工认证。

## 3. 当前研究状态

V0：正文纠错提交+语义审计与反例测试实现，**新CI验收待确认**。V1：公开先例页面初步核查（KDD2020/ICML2024/JAIR2024/2026 Active RAG）已启动，完整证据矩阵未完成。V2 corrected-S：未开始私有DEV信息充分性核验，更无corrected-S实验。V3/V4、V5/V6：未开始。C8作者最终Go/No-go：未签署，PR仍Draft，未投稿。

该状态必须随真实GitHub Actions更新；当前只承诺提交已实施的文本和代码，不预测CI结论。
