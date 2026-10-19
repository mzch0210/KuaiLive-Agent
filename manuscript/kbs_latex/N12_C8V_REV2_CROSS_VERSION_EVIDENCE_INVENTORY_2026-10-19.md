# N12-C8V Rev2 | 跨版本研究证据总账与去重基线（2026-10-19）

**状态：研究报告和代码历史的只读核对已实施；这是“总账初版/方案输入”，不是重新独立运行全部实验或逐行核查全部 649 个仓库文件。** 后续正式的 `I0` 验收须再追踪关键原始 run、source SHA、私有数据字段充分性、当前 manuscript/Supplement 具体落点和人工抽查签署。工作分支：`kbs-n12-single-thesis-restructure-plan-20261014`，PR #6（Draft），`main.tex` 37页，Supplement 47页。不得把重复的同 cohort DEV 分析计成多次独立验证。

## 1. 版本谱系与研究历史（不是独立重复研究）

| 研究/写作时期 | 已完成内容和正文版本责任 | 科学结论、历史遗留问题 |
| --- | --- | --- |
| 2026-10-10/11：初稿论证驱动多轮修改 | Argument-driven Results；94段审计；第二轮投稿叙事、三个协议证据层级 | 已确立Base-relative知识价值、候选环境与选择决策的中心张力；没有解决通用L2D原创性 |
| 2026-10-12：Plan C / G0–G5 / R0–R8 | 数据冻结、六次Base fit、G5 47,575事件单次TEST，强Objective对照、DEV路由、原局部成本诊断；新R0–R8写作 | G5是首次冻结TEST；六训练fit同一TEST不是六独立TEST；Always Memory在M3无约束排名更好 |
| 2026-10-13：N0–N8；B0/B1/B2；N9-A/G | B1三臂完整DEV，B2五源×候选消融，N9-A1八档预算、A2 Direct/Two-stage和Difficulty/Quality，G1来源×候选配对、G2 request-switch分解，DEV时间控制null | 同一50,049 DEV既提供多个估计对象，也造成共享用户/事件依赖；Adapted arm使用F训练标签，不能冒称corrected-S |
| 2026-10-14：Route B/B4-A；N10；N11 | 九单元格zero-support、1,024 DEV历史Null、同期间30k的H1与嵌套4096 H2冻结评价、A5独立重构、旧点对点选择器真实计时；N10 42p/46p；N11 39p/45p | H1完整冻结策略F质量↑调用↓，但调用率差超预定近等预算阈值；H2部分nonfloor验收缺Popularity子门槛；旧Utility延迟逆向证据 |
| 2026-10-14至19：N12 C0–C7 / C8N / C8V | 单一命题与RQ1/RQ2/RQ3重构、11 Results表原块追踪、C7 17行49cell、C8N学术论证强化、V0修正分母/控制措辞；37p/47p CI | V0自动科学语义+双PDF PASS，V1先例分析已写但独立学者未签署；当前全文仍非KBS已投稿稿 |

真实PR继承顺序：`main` → [PR #3 B4-A](https://github.com/mzch0210/KuaiLive-Agent/pull/3) → [PR #4 N10](https://github.com/mzch0210/KuaiLive-Agent/pull/4) → [PR #5 N11](https://github.com/mzch0210/KuaiLive-Agent/pull/5) → [PR #6 N12](https://github.com/mzch0210/KuaiLive-Agent/pull/6)。#3–#6均开放Draft并相互作为后继base；不可误认为各自merged到`main`。

## 2. 原始科学估计对象／执行结果／证据类型／新方案决定

“源”仅列最有权威的初始/冻结报告文件，详细脚本和相关run可在对应报告查看。“已运行”指原仓库报告、脚本、成功工作流记录支持；不是本次重新跑过。

| ID | 研究对象、样本/实验等级 | 原始完成内容及最能支持的数字 | 可信起点（仓库相对路径） | 现稿位置和Rev2处理 |
| --- | --- | --- | --- | --- |
| P0 | Twitch streamer TEST 44,221 | Base .58211，Memory .53980，DEV-frozen Utility .58983/6650 calls；后验5,539 recoverable子群gain+.22045不可作pretarget gate输入 | `manuscript/kbs_latex/N12_C7_CLAIM_SOURCE_REPRODUCIBILITY_AND_RIGHTS_REGISTER_2026-10-19.md`；原TEST表冻结manifest | RQ1/RQ2主文；**复用** |
| P1 | 早期KuaiLive **room** paired 10,222已评价事件、回顾性 | Memory−Base sampled −.04120/full +.04631；room和M3 author不是相同任务 | `manuscript/kbs_latex/N12_C1_RQ_ARGUMENT_AND_EVIDENCE_BLUEPRINT_2026-10-14.md`；原冻结Results表 | RQ1诊断，**不得据此推断M3因果桥** |
| G5 | 原M3 author forward-time TEST 47,575/12,533用户、6 trained fits同TEST | Primary SAS Base .258004、Utility .302866、Always Memory .346792；6fits并非6个独立TEST；DEV阈值预冻结、TEST一次揭示 | `experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md` | RQ2原始独立冻结测试；**复用** |
| B1 | 原M3 DEV 50,049/12,628用户，5 outer×4 inner user-group；三臂**同DEV探索** | SAS S→F .296499、F→F .302658、Adapted→F .301847；GRU .298123/.303093/.303000。Adapted使用F训练和阈值标签，**不是corrected-S**；CI #38365477972 | `experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md` | 主文RQ2+Supp S10.19 S10.14；**取消重复三臂** |
| B2 | 同M3 DEV、五类历史源；12/6 pretarget特征；同队列探索 | Full迁移regret SAS .006159 GRU .004970；Long-only .010605/.010262更大；Short-only约.0207但call严重不等；Popularity/placebo近Base floor，不能作为nonknowledge优胜反例 | `experiments/kbs_plan_c/B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md` | Supp S10；**不重做五源消融** |
| G1/E3a | 同M3 DEV Full vs Long，候选S/F交互、用户bootstrap探索 | `[u_F(Full)-u_F(Long)]-[u_S(Full)-u_S(Long)]` +.115382，source×candidate不是严格关系身份因果 | `manuscript/kbs_latex/N9_G1_E3A_PAIRED_SOURCE_REGIME_INTERACTION_2026-10-13.md` | 主文支持/补充；**仅综合** |
| Route B B1A | 同M3 DEV，九单元格source-gap sign/zero分解 | 46,462/50,049（92.83%）至少一个source gap为0；66请求两制度下严格非零符号反转；87.44%为签名净贡献占比**不是绝对贡献比例** | `manuscript/kbs_latex/N9_B1_ZERO_STRUCTURE_AND_DECISION_FAIRNESS_AUDIT_2026-10-14.md` | Supp S10；**创新性竞争解释必须前置** |
| G2/E1 | 同M3 DEV S/F request decisions及F Δ accounting | SAS 10,672/50,049分歧，added/dropped 5350/5322，净+.006159；GRU 11,517分歧，5639/5878，净+.004970；代数分解**不是新机制因果实验** | `manuscript/kbs_latex/N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md` | RQ2/Discussion；**复用** |
| N9 A1 | 同M3 DEV下已校准inner 0/10/20/30/50/70/90/100%**八档**；非新TEST | 30% SAS .302658/15016 calls，GRU .303093/14762；100%学得门控近Always Memory but slightly worse;实际调用可漂移 | `manuscript/kbs_latex/N9_A1_UNCONSTRAINED_POLICY_FRONTIER_2026-10-13.md` | Supp S10；**取消默认额度扫描** |
| N9 A2 | 同M3 DEV 10/30/50%预算；Direct Δ/Two-stage/Difficulty/Quality | 30% SAS Direct .302658/Two-stage .301348，差+.001310**多318 calls**；GRU .303093/.302974，差+.000119 CI跨零且Direct少59 calls。两估计法同一条件Δ目标 | `manuscript/kbs_latex/N9_A2_DECISION_TARGET_CONTROLS_2026-10-13.md` | Supp S7.7/S10；**取消重复建模** |
| N9 G1/E2 | 同DEV A1现有frontier的 λ shadow-price上包络，忽略真实开销 | λ是**假设性每调用NDCG等价成本**，不能解释生产真实节省 | `manuscript/kbs_latex/N9_G1_E2_SHADOW_PRICE_DECISION_ENVELOPE_2026-10-13.md` | Supp；**仅解释边界** |
| B2/G3 | 同DEV中预选1024 / 992用户，历史时间/活动保留Null，3seed共享样本 | 真实历史 F .339348、3seed null .306491/.303804/.305321；同DEV TRAIN-only Popularity .021867曾验收PASS（不能借给4,096队列） | `manuscript/kbs_latex/N9_ROUTE_B_B2_1024_REAL_RELATION_IDENTITY_NULL_RESULTS_2026-10-14.md`; `N10_ROUTE_C_C3A_NULL_VALIDITY_AUDIT_2026-10-14.md` | Supp S10；**不得当新独立cohort** |
| B4-A H1 | 同采集期新评价30,000 M3 author目标/10,387用户、20cell weighted、DEV-frozen政策 | SAS F−S +.005391 CI [.003646,.007174] Calls F/S 8704/9105；GRU +.003585 CI [.001599,.005576] Calls 8629/9168；分别超预设1pp近同预算容忍；同期间并非未来时点 | `manuscript/kbs_latex/N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md`；A5重构 | RQ2主文**最高等级F/S结局**，不重调TEST阈值 |
| B4-A H2 | H1内嵌4096 /3059用户，同源期一次封存3 Null | True .334942/null mean .303797，差+.031145 CI [.027389,.035098] Holm p .000600；约76.8% history rewired+重复/高阶共同变化；原同队列TRAIN-only popularity预揭盲门槛**NOT VERIFIED** | 同B4-A A4/A5；`manuscript/kbs_latex/N10_ROUTE_C_C3A_NULL_VALIDITY_AUDIT_2026-10-14.md` | RQ3独立**平行**来源测试，不当作RQ2机制中介 |
| N10 C2B | 原256 M3 DEV请求×3 warmed重复，**旧pointwise Utility** vs Base/Memory | mean old Utility 1.76941ms、Always Memory .69165ms、Base .72759ms，不能推断新vectorized F策略计时；无真实生产成本论证 | `manuscript/kbs_latex/N10_ROUTE_C_C2B_MATCHED_DEV_COST_AND_R2_VERDICT_2026-10-14.md` | Operating conditions；**不重测同一旧实现** |
| N8/N9/N10/N11 | 多轮独立视角**模拟**审稿及写作修订（非真正外部审稿） | R1已有工作/新意，R2 Always Memory及无外生真实稀缺，R3机制独有性，H2控制验收等**早已被提出并部分缓解** | `N8_KBS_INDEPENDENT_REFEREE_REPORT_2026-10-13.md`；`N9_G4_THREE_RISK_EVIDENCE_VERDICT_2026-10-13.md`；`N10_ROUTE_C_C4_THREE_RISK_SCIENTIFIC_ADJUDICATION_2026-10-14.md`；`N11_FINAL_KBS_EDITORIAL_LANDING_AND_COHERENCE_AUDIT_2026-10-14.md` | Rev2独立审阅应**合并未决意见**，不再制造第三套模拟审稿 |
| N12/V0/V1 | C0–C7审计完成 + C8N强化和V0修正语义，V1分析近邻 | CI #39218602150 37p+47p、6语义tests+5表格tests、17行49cell全部PASS；V1 analyst matrix **完成**但未获外部研究者审阅 | `N12_C8V_V0_SEMANTIC_CORRECTION_EXECUTION_LOG_2026-10-19.md`；`N12_C8V_V1_PRIOR_ART_AND_NOVELTY_EVIDENCE_STRESS_TEST_2026-10-19.md` | **保留完成，不回滚；不将机器PASS视为科学原创性认证** |

## 3. 当前论文覆盖、读者仍可能误解的边界

1. 主文七节：Introduction、Related Work、Knowledge Valuation and Selective Use、Experimental Design、Results（RQ1/RQ2/RQ3/operating）、Discussion、Conclusion。36→37p是C8N学术文字强化，Supp 47p；原11张Results表：主文原7块与Supp迁4块17行49数值cell。**当前论文不等于原始八章 N11 的章节编号**。
2. **B1三臂已见于Supplement S10.19 S10.14和主文RQ2**；不能在计划写“首次提出三臂”。
3. **A2 Direct vs Two-stage**与**A1预算frontier**在Supp S7.7/S10有实证；主文着墨较少是**叙事选择/解释缺口**，不是实验未做。
4. G1/E3a + 九单元格zero-mass已在Supplement；**46,462 zero-support是Full vs Long source gap，不是Memory−Base Δ符号**。只读证据综合时不得跨估计对象偷换。
5. H1**质量与调用数量双重占优**相对于tested S是允许报告的完整冻结策略比较；严格等调用孤立监督效应未被识别。H2 null大幅重排、原Popularity预验收未验证是必须写出的限定，但不能抹去其他诊断PASS。
6. Primary novelty = 将已知采样评价不一致问题推进到**固定历史专家使用监督与request-level选择后果**的特定实证；不是新的sampled metric correction、通用deferral、DFL定理或已证实serving saving。
7. 当前脚本 `b1_dev_regime_pilot.py` 有确定性574-negative无放回target-retained抽样/完整秩次计算函数；`b1_full_dev_candidate_labels.py` 主要将sampled scalar NDCG写入私有DEV CSV。这说明**源代码可部分重建信息**，但不能声称私有缓存存在、correction有效或原完整排名已归档。术语 `corrected Memory` 主要为历史重放实现修正，**不是 statistically corrected-S**。
8. 原始实验经过N8–N12多轮文稿审核，但大多数新增DEV使用相同50,049 cohort；多报告、多seed、多CI工作流**不增加独立样本的证据数量**。

## 4. 审计字段与门槛（未来I0正式PASS必须补足）

对每条估计对象建立machine-readable记录，至少包含：`id`, `source_of_truth`, `execution_run`, `source_commit`, `cohort`, `rank_unit`, `original_label_access`, `candidate_F_S`, `policy_threshold_timing`, `evidence_class`, `estimand`, `effect`, `statistic`, `manuscript_anchor`, `supplement_anchor`, `independent_of`, `status`, `next_action`。人工核对同一估计对象的原表数字与正文叙述，区分控制变量与改变的机制；**不可只在后代报告中搜索数字存在**。对于早期失败/恢复的self-host runner（如B2标签生成workflow报告failure但计算/私有持久输出PASS），应分列job状态、private source真实状态以及可供第三方审核的公开证据。

**I0未核验完成时不得冒称“整个项目全部材料逐行看过、私有数据完整可用或独立重现所有置信区间”。** 源审核只是防止历史成果遗漏的基础设施。

## 5. 尚未执行、可由更高科学信息增益触发的项目（去重）

- Corrected-S validity：**NOT PERFORMED**, 且B1 Adapted→F含F training labels；先查条件期望估计对象、算法适用性和私有DEV可重建性，只有在确实能区分已知偏差解释时做DEV-only新对照。
- 非关系专家或来源身份的**独立因果隔离**：NOT ESTABLISHED；已有B2和B4-A composite null未识别唯一relation semantic机制。默认不新增，若作者希望提升科学主张才另定完整预注册设计。
- 严格same-call policy effect、实测新向量化F门控端到端成本、未来新时间窗口/新平台外推：NOT PERFORMED。不得为了报一个更好结果复用已揭盲30k调阈值。
- 真正外部学者独立审阅、责任作者审签、CRediT/AI/Funding/COI/Data Availability、KBS实际投稿：NOT COMPLETED。公开数据许可不同标签**本身不自动阻断投稿**，实际侵权、隐私或非法再分发除外。

**适用结论：** 先逐估计对象建档，再决定是否确有唯一尚未识别的问题；Rev2方案文件是下一步任务顺序的唯一规范。
