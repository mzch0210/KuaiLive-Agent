# N12-C6.1 | Candidate-supervision → knowledge-allocation → F-ranking: frozen-evidence chain

日期：2026-10-19。**C6.1现有证据梳理完成（文档层）；非新实验或独立TEST验证。** 依赖：`N12_C6_CLAIM_EVIDENCE_PRIOR_ART_STRESS_TEST_2026-10-19.md` 的有条件进入编辑裁决。

## 1. 比较对象与估计边界

固定Base B（SASRec/GRU4Rec分别比较）、显式历史关系Memory M、预目标特征合同Z、最终full-active候选F、HGB预测器容量和已封存的原始协议。训练标签为不同候选环境下的 `Δ_S=u_10(M,S)-u_10(B,S)` 与 `Δ_F=u_10(M,F)-u_10(B,F)`；部署决策条件下没有看到真实目标。S在DEV的575名候选包含**事后保留的已观察目标**以计算**离线监督标签**，不是线上candidate generator。两种监督还分别进行内层校准、产生不同冻结门槛；故研究比较对象是**完整冻结政策**，而非只交换一个标签的严格孤立干预。

价值分解为：在相同评价F和同一Base/M下，`V_F(π_F)-V_F(π_S)=E[(π_F−π_S)Δ_F]`。这是代数恒等式，不是新的selection theorem。实际部署调用额度在DEV内层受不超过30%阈值校准约束，外层/TEST执行调用并非事后强制精确等量。

## 2. 首先看标签是否改变了政策所选事件（仅探索性DEV）

来源：50,049 M3 DEV事件、12,628位用户，同一批用户分组5 outer×4 inner，两个Base primary seed。原始报告 `N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md` 与 `N9_G2_E1_SUPERVISION_DECISION_SWITCHES_PUBLIC_AGGREGATE_2026-10-13.json`，工作流 #38389150075。

| Base | S→F NDCG@10 | F→F NDCG@10 | F−S | F/S calls | 不同选择事件 | F新增调用 / F停止调用 |
| --- | ---: | ---: | ---: | --- | --- | --- |
| SASRec | 0.296499 | 0.302658 | +0.006159 [0.004835, 0.007543] | 15,016 / 14,988 | 10,672 (21.32%) | 5,350 / 5,322 |
| GRU4Rec | 0.298123 | 0.303093 | +0.004970 [0.003550, 0.006369] | 14,762 / 15,001 | 11,517 (23.01%) | 5,639 / 5,878 |

注意上表F/S calls第一项为**F策略**第二项为**S策略**；不能与新增/停止调用两个类别混淆。自然调用SAS相差28次，GRU相差239次，依旧不是严格相同调用。数字与冻结源逐项比对，不是本次重新生成的统计。

### Switch accounting（可解释的知识调用分配，绝非新定理）

| Base | F新增调用事件上的平均`Δ_F` | F停止调用事件上的平均`Δ_F` | 新增对整队列的贡献 | 停止对整队列的贡献 | 净差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| SASRec | +0.133417 | +0.076194 | +0.014262 | −0.008102 | +0.006159 |
| GRU4Rec | +0.126600 | +0.079135 | +0.014264 | −0.009294 | +0.004970 |

**科研解释**：两个被替换集合的`Δ_F`平均值都为正；F监督不是简单避免Memory负效用，而是在限制调用下把有限调用倾向分配给增量收益更高的事件。不能声称该分解发生在30,000冻结H1上；没有从现有public aggregate重算任何目标标签。

### 其他辅助但不能夸大的DEV证据

- 同队列三类`Δ`标签sign category（负/零/正）差异约53.8%，大部分是零与非零变化；**真正双非零正负相反**仅SAS 157、GRU 145事件。禁止把53.8%写成“严格正负翻转率”。
- DEV B1同一模型/特征/outer groups，full-sup优于sampled-sup；regime-adapted含有F训练标签，因此不代表未见F标签的成功迁移。
- DEV B2 Long-only在十二特征下的supervision regret **大于Full**（SAS 0.010605 vs 0.006159；GRU 0.010262 vs 0.004970）。Short-only巨大regret同时伴随S policy近零calls/F约15k calls。Popularity及history-placement placebo近零regret至少部分因性能地板和极少调用。不存在经识别的“越强真实关系→越大F-supervision效应”单调因果结论。六特征panel与12特征panel也改变预测信息，不能当唯一isolated source causal test。

## 3. 独立于原已评价TEST事件ID的30,000同期间冻结验证（主证据）

来源：M3额外 **30,000 targets /10,387 users**，20-cell eligible-population加权，原始2026-03-27—03-31采集期，与原47575已评分事件ID不同，但可能用户/历史重合；不存在跨新时期独立验证。两族Base共享同一30k cohort。

| Base | S-policy weighted F NDCG | F-policy weighted F NDCG | F−S user-cluster 95% CI | Holm p | calls F/S |
| --- | ---: | ---: | --- | ---: | --- |
| SASRec | 0.300055 | 0.305446 | +0.005391 [0.003646, 0.007174] | 0.000600 | 8704/9105 |
| GRU4Rec | 0.300945 | 0.304530 | +0.003585 [0.001599, 0.005576] | 0.000800 | 8629/9168 |

自然realized Memory调用率差分别1.337pp、1.797pp，**违反原约1pp near-equal gate**；原H1只能支持不同完整冻结策略的总体表现差异，不支持严格等调用预算隔离的纯监督标签因果效应。额外的样本数无法自行修复识别缺口。不可用已揭盲30k事件后验重新挑阈值来假装达成原要求。

30k Always Memory weighted F NDCG 0.348744高于所测试F选择策略；因此H1的价值是在外生调用额度存在时的配置研究，而不是unconstrained quality domination。

## 4. 知识来源平行支撑与困难反证

RQ3嵌套4096并非独立于30k的另一次样本：真实历史F 0.334942，对3个historical-null per-event mean 0.303797，差+0.031145，95% CI[0.027389,0.035098], Holm p=0.000600，三seed共一cohort。扰动约76.8%边，改变用户重复配对和高阶结构；**原B4-A same-cohort TRAIN-only Popularity floor在reveal前NOT VERIFIED**。这只能作为并行历史信息来源检验，不能声称来源×选择机制被单一因果设计完全识别。

此外原旧pointwise Utility设备计时平均约1.769ms，高于Always Memory约0.692ms；这不是对新vectorized F gate的计时。本论文没有实测新gate端到端部署经济性。

## 5. 适用于C6.2的英文科学叙事合同（不自动修改现有主稿）

**Claim A (primary):** “Training the knowledge-use selector on candidate-aligned relative utility is associated with better frozen-policy ranking decisions on the evaluated full-active M3 cohort than sampled-label supervision, under the observed DEV-calibrated call allocations.”

**Claim B (mechanistic exploratory):** “On the user-separated development folds, aligning the label with full candidates changed 21–23% of specialist-invocation decisions and favored requests with larger realized full-candidate incremental utility; this event-level decomposition is descriptive and does not establish a new deferral theorem.”

**Claim C (source parallel):** “With current candidates and scoring fixed, authentic historical arrangements outperform constrained historical nulls; the comparison is composite and the original same-cohort prereveal popularity acceptance check was not verified.”

**Transferable insight:** “For decision-time use of an external knowledge source, the incumbent and intended candidate evaluation regime are part of the value-supervision contract. This can alter which requests are assigned the source, but fewer calls alone are not evidence of lower end-to-end serving cost.”

**Forbidden:** “same-budget causal” / “unique relationship semantic mechanism” / “future out-of-time replication” / “new generic gating algorithm” / “deployment savings” / “H2 all original prereveal conditions fulfilled”.

## 6. C6.1审计决策与后续工程入口

- **C6.1 evidence-chain document: COMPLETE**, source-level cross-checked against original public DEV report/aggregate and present RQ2 table;无重训练、无TEST再评。
- **C6.2 manuscript editing: NOT STARTED**。必须把上述primary contribution作为Abstract/Intro/Discussion/Conclusion/Highlights的统一内容，同时保留原始11个结果表的完整源追溯、并行RQ3和不利成本证据。
- **C6.3 science guard/PDF: NOT STARTED**。旧C5脚本的prefix/suffix全段指纹不能直接用于C6 planned edit，需以科学事实/数值/公式合同取代，并归档旧C5阶段审计。

**相关源码**：`manuscript/kbs_latex/main.tex`、`manuscript/kbs_latex/N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md`、`experiments/kbs_plan_c/N9_G2_E1_SUPERVISION_DECISION_SWITCHES_PUBLIC_AGGREGATE_2026-10-13.json`、`experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md`、`experiments/kbs_plan_c/B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md`、`manuscript/kbs_latex/N12_C6_CLAIM_EVIDENCE_PRIOR_ART_STRESS_TEST_2026-10-19.md`。
