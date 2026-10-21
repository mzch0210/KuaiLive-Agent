# N12-C8V Rev2.2-R1 | Path A 科学贡献增量审查与精准修订计划

**修订日期：2026-10-20｜性质：对原 Rev2.2 的原位修订，不创建平行科研路线｜本次提交：PLAN-ONLY。**

**执行状态：E0 已完成；E1 已完成；E2–E6 尚未完成；真实独立研究者审阅和责任作者最终 GO/NO-GO 均 PENDING；KBS 尚未投稿。** E0/E1 只读报告是当前阶段输入，不能因更新计划而重新标为未执行。本次计划修改本身不等于论文改稿、实验新增或 PDF CI 通过。

## 0. 事实基线、适用范围与不得重置的成果

- **仓库与分支**：mzch0210/KuaiLive-Agent；kbs-n12-single-thesis-restructure-plan-20261014；PR #6 仍为 Draft，不自动合并、改为 ready 或投稿。
- **现行论文源**：manuscript/kbs_latex/main.tex，E0 已核对 blob SHA **c713811acf5c6c47df3e5cb34ee8a7af5cc4ff5e**；Rev2.1 科学提交 **7e4c5a6f616e22226f55e2396815d48cc838bf96**。最近被真实 CI 验证的论文 PDF 为 **38 页主文、47 页完整 S1–S10**；对应 Actions **#39351014765 / #39351014645** 均 SUCCESS。后续纯治理/计划提交不产生新的科学 PDF QA。
- **E0 已完成**：N12_C8V_REV2_2_E0_CLAIM_TO_SOURCE_MATRIX_2026-10-20.md，结果为 PASS_SOURCE_MAPPING_WITH_ONE_WORDING_RISK_OPEN。源—论点与统计总体定位已经完成，无需再次执行原计划的 E0 数据核查。
- **E1 已完成**：N12_C8V_REV2_2_E1_PRIOR_ART_AND_ONE_THESIS_CONTRAST_2026-10-20.md，结果为 ANALYST_PASS_FOR_PRECISE_CONTRAST / NOVELTY_HIGH_CONTESTABLE。近邻研究对照已经形成，不以新一轮同内容文献综述冒充新进展。
- **Rev2.1 已完成**：Related Work 添加 CIKM 2024 sampled-rank 修正先例；RQ2 明确原 S 是 retrospectively target-retained、uncorrected 575-candidate 标签，Adapted 使用 F 标签；Discussion 承认有效 sampled-only corrected-S 尚未在训练后完整政策上比较。原 I2-D 仅是 AI 辅助的内部对抗审查，不能冒称真实人类独立同行评议。
- **原始结果和证据总账**：N12_C8V_REV2_EVIDENCE_LEDGER.json（14 个 estimands / 8 个 cohorts）、N9/N10/N11/N12 各阶段记录均继续有效。所有任务必须指明 cohort、ranking unit、estimand、source、pre/post outcome 权限，不得把不同人口或不同时间层级误称为独立复现。

**保持 Path A**：以已有经溯源的实验为核心，贡献清晰、边界诚实、审查可证伪；不追求新理论命名，不继续在已检查 DEV/TEST 上为显著性搜寻。当前稿件已有一条较完整的 candidate-regime supervision → request-level allocation → frozen policy result 证据链，不再把“再写一遍”作为默认提升工作。

### 已经写入现稿、不得当作新待办的论述

| 科学内容 | 当前 main.tex 位置（E0 审计时） | 新计划默认动作 |
| --- | --- | --- |
| 单一核心主张和三级贡献分工 | Introduction 37–52，Conclusion 631–633 | **L0 NO CHANGE** |
| KDD/CIKM/deferral/decision-focused 的已有与新增边界 | Related Work 90–102；Discussion 603–608 | **L0**，仅审查是否有真正缺漏 |
| 原 S/F/Adapted 的训练信息合同、H1 30k 两种模型政策表现 | RQ2 Results 513–534 | **L0**，不重写冻表 |
| G2 50,049 DEV、21.32%/23.01% 请求换位、F-only/S-only 价值解释 | RQ2 Results 529–534；Discussion 613–617 | **L0**，仅检查因果/同队列边界 |
| H1 中 F 质量较高、Memory calls 较少；natural call 差 1.337/1.797pp | RQ2 Results 513–528；Discussion 617 | **L0**，不制造等调用因果解释 |
| Always Memory 较准，旧 pointwise Utility 较慢，未证明服务成本节约 | Results 573–599；Discussion 626 | **L0**，仅跨章一致性检查 |
| corrected-S 未验证、额外同采集期 IDs 不是新时间段 | Related Work 100；RQ2 513；Discussion 624 | **L0**，不重复加入 limitation |
| RQ3 为复合历史来源敏感性；原 4096 预揭盲 TRAIN-only Popularity 条件 NOT VERIFIED | RQ3 Results 540–570；Discussion 622 | **L0**，保留负面原状 |
| Figure 1 历史 Null 文字 | Fig. 1 TikZ 原第 74 行：Authentic history versus valid historical nulls | **已知 L1 候选**：需精确弱化 |

行号是 E0 所核对的版本锚点；以之后的实际 Git diff / 文本锚点为准，不把行号漂移当成科学差异。

## 1. KBS 期刊目标与当前唯一可保留的中心贡献

KBS 官方说明包含 recommender systems、e-service personalization 和 intelligent decision support，并要求 original、innovative、creative 的 AI 研究，关注理论与应用之间的平衡。范围适配**不**等于创新性审核通过：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 。

**研究对象**：固定 Base、固定历史关系 Memory 专家与完整可用候选 F，考察相对效用标签 Δ_F(x)=u_10(M;x,F)-u_10(B;x,F) 的条件预测及受约束的专家使用。

**允许的唯一中心主张**：不同候选协议形成的离线增量效用监督，能够在所研究的历史关系专家—Base—候选制度合同下改变具体请求的 Memory 调用分配；已有探索性 DEV 中可观察到调用换位，额外冻结、但同采集期的 30,000 个事件 ID 中 F-supervised 完整政策优于**原未经校正** S-supervised 完整政策。

**证据分层而非三项互不相关的新发明**：
1. RQ1：Twitch 44,221 streamer TEST、KuaiLive 10,222 room 后验固定 checkpoint 对照负责定义和背景；room 与 M3 author task 不等价，不能识别候选数单独因果效应。
2. RQ2 主证据：M3 **50,049 DEV / 12,628 users** 的旧 B1/G2 探索性监督与调用换位，以及额外**30,000 同期 events / 10,387 users** 的 H1 完整政策结果；DEV 分解与 H1 **不是同样本因果中介识别**。
3. RQ3 平行支持：H2 嵌套 **4096 events** 三个历史 Null seeds（相同事件群体、复合干预），而非 RQ2 机制确认、独立三数据集或单一历史语义因果识别。

**必须保留的数值与负面结果**：
- H1 SAS F−S NDCG@10 +0.005391，95% CI [0.003646,0.007174]，F/S calls 8704/9105；GRU +0.003585，CI [0.001599,0.005576]，calls 8629/9168。前者 401、后者 539 次 Memory 调用减少，只是两个观测到的冻结 complete-policy operating points；unweighted calls 与 eligible-population-weighted NDCG 不可混算。
- F/S natural calls 差 1.337/1.797 个百分点，超过原 1pp near-equal tolerance；不能推断严格同调用或标签单因子因果效果、部署成本优化或全局 Pareto 优越性。
- B1/G2 DEV SAS 10672/50049=21.32%、GRU 11517/50049=23.01% **request decisions switch**；这是同 cohort 描述性分解，不是 30k H1 的独立解释性试验，更不是总体调用比例。
- RQ3 authentic−constrained-null +0.031145，CI [0.027389,0.035098]；4096 original TRAIN-only Popularity prereveal subgate **NOT VERIFIED**。三 seeds 共享样本，不能事后补签验收。
- H1 Always Memory 0.348744 > F gate SAS 0.305446；原 pointwise Utility DEV latency ~1.769ms > Always Memory ~0.692ms；新 vectorized F gate 未经实时计时。外部 quota 是明示假定，不是已测的经济瓶颈。
- V2a 只检查先前 128 DEV replay、已有 50,049 DEV joint labels、合成和两种 heuristic corrections；**V2b NOT_RUN_BY_DESIGN**，不代表合理 sampled-only corrected-S 已被排除。

**最近邻的科学边界**：Krichene & Rendle KDD 2020 已证明 sampled metric 不一致；Subbiah 等 CIKM 2024 已研究 sampled rank correction；Mao 等 ICML 2024/2025 已研究带成本的 expert deferral；decision-focused learning 是已有领域；2026 Active RAG 预印本还涉及知识调用效用和成本。N12 不主张这些一般原理或门控算法首创，仅主张限定任务中的监督—调用—结果实证联系。**独立贡献是否达到 KBS 发表强度仍为 HIGH / HUMAN REVIEW PENDING**，不能用写作与 CI 将 HIGH 自动改为 LOW。

## 2. 已完成 E0/E1：正式验收并保持不可回退的状态

### E0 — DONE / SOURCE_MAPPING_PASS_WITH_ONE_WORDING_RISK

源文、I0 14 估计对象、主要 CI、统计总体与现稿锚点已审查。文件：N12_C8V_REV2_2_E0_CLAIM_TO_SOURCE_MATRIX_2026-10-20.md。E0 的唯一已识别待检查措辞：Figure 1 中 valid historical nulls 过强；不要重跑原始数据或伪装成新的逐行复现。

### E1 — DONE / PRECISE_PRIOR_ART_CONTRAST_PASS; NOVELTY_HIGH_CONTESTABLE

文件：N12_C8V_REV2_2_E1_PRIOR_ART_AND_ONE_THESIS_CONTRAST_2026-10-20.md。保留一条核心贡献、最近邻研究对照与三项可证伪质疑。E1 完成并**没有**证明 KBS 新颖性已获审稿人认可。除确有新近、强相关先例或文献定位错误，不做另一轮相同内容综述，不重新加创新措辞。

## 3. 尚待执行的 E2–E6（修改后的工作内容与授权边界）

### E2-R1 — P0 现有核心贡献的科学增量审查（不是 RQ2 复述）

**输入**：E0/E1；现稿 Introduction 47–52、RQ2 513–534、Discussion 603–617、Conclusion 631–633；旧 B1/G2/H1/A1/A2 聚合证据。

**任务**：
1. 对“已观测监督差异→调用换位→冻结 policy 效果”作**论文已有信息审计**，准确指出现有文字已经回答、重复回答、没有回答的科学问题，避免重复表格/公式/段落。
2. 针对 KBS 审稿人“known sampling inconsistency + known deferral = trivial application”提出**可证伪的一条独立实证差异**，标注原始来源及当前文本；不得用增添形容词来宣称新颖性。
3. 核对同一 DEV 内 switched calls 的解释与另一个 30k H1 的整策略结果之间的桥梁。只能说一致性证据链，不能写成新识别的中介因果机制。
4. 核对已存在 A1 八预算、A2 Direct/Two-stage、B1 Adapted 等比较是否具有**被遗漏且实质重要**的解释；不得为了填任务再现同样的数字。
5. 对每个候选修改给出 CURRENT_TEXT_ANCHOR、EVIDENCE_SOURCE、NOVEL_INFORMATION_GAIN、RISKS、EDIT_LEVEL（L0/L1/L2），必须允许结论 **NO_MAIN_TEXT_CHANGE_REQUIRED**。

**交付**：N12_C8V_REV2_2_E2_EXISTING_CONTRIBUTION_INCREMENT_AUDIT.md；不是默认新增 Results 表或 Section。

**PASS 门槛**：能够解释当前唯一实证贡献及其反例边界；每一个建议修订都具有明确新信息增量，或明确判定现稿无需改动。若发现仅凭已有结果无法建立非平凡贡献，写 OPEN_HIGH_NOVELTY_RISK 而不是自拟理论结论。

### E3-R1 — P0 残余竞争解释与主张强度审查（不重复补 limitations）

**输入**：E2；现稿 Related Work 90–102、RQ2/RQ3、Results 573–599、Discussion 619–626；V2a 与 N9/N10 原报告。

**仅检验四类可能的跨段落矛盾**：
- C1 sampled-only corrected-S 未训练。现稿 Related Work 100、RQ2 513、Discussion 624 已承认；只找遗漏位置是否夸称所有 S 必败，未找到就 L0。
- C2 Always Memory 无约束更准、旧 pointwise Utility 慢、quota 只是外生约束。现稿 Results 573–599、Discussion 626 已充分阐述；只检查 Abstract、Highlights、Conclusion 有没有冲突，不能重复插入长篇限制。
- C3 RQ3 复合历史 Null 和预揭盲缺口。表注、Results 563、Discussion 622 已披露；**唯一已证实 L1 候选是 Figure 1 节点原句 Authentic history versus valid historical nulls → Authentic history versus constrained historical randomizations**。检查其与正文一致，不修复历史测试事前验收状态。
- C4 同期 30k、历史交叠、streamer/room/author unit、DEV/H1/H2 的独立性和 target exposure bias。现稿已有限定，仅作误述扫描，不添加未经验证的 IPS、线上或时间泛化主张。

**交付**：N12_C8V_REV2_2_E3_RESIDUAL_RISK_AND_CLAIM_SCOPE.md，统一分类 ALREADY_RESOLVED / WORDING_FIX_REQUIRED / SCIENTIFIC_GAP_OPEN / NO_CHANGE；逐一记录证据、原文锚点、是否需 E4 以及不能识别的对象。

**PASS 门槛**：至少保证上述 C1–C4 的强主张没有超出实际证据；没有必要的新修订时可明确 E3 PASS_WITH_NO_TEXT_CHANGE。开放科学缺口继续开放，不能因审核通过冒充解决。

### E4-R1 — P1 有条件的正文最小改动（NO-CHANGE 为合格结果）

**启动条件**：E2/E3 已给出明确、可核验、按优先级排序的差异清单，修改的是科学准确性、实际新信息、结论范围或可读性，不是为流程凑改稿数量。

**编辑权限分级**：
- **L0：NO CHANGE**。已准确表达且无新信息的段落（默认包括 Introduction 47–52、RQ2 513–534、Discussion 603–626、Conclusion 631–633）不得为了“增强”再堆砌结果或限制。
- **L1：SURGICAL EDIT**。证据支持的过强词、歧义、重复或小范围遗漏可以按句改动。已知候选：Figure 1 历史 Null 的 valid → constrained historical randomizations（准确最终英文以科学 QA 为准）。
- **L2：SCOPED PARAGRAPH RESTRUCTURE**。只有 E2 记录确凿论证缺口，允许重组受影响的少量段落并删减重复内容，不得重构章节、第四 RQ、方法命名或扩大因果结论。

**禁改与来源锁**：除确属误引并先停机核实，不能改变 11 个原 Results 表及 7 main/4 Supplement 迁移、17 行49单元格、原公式、效应/CIs/Holm p、call 数、cohort 单位和统计估计对象；不重开 G5/B4-A TEST、不拟合新 gate、不重做 B1/B2/A1/A2/G2/V2b、不伪造新 matched-call CI。Abstract、Highlights、BibTeX 只有在实际发现不一致或相关高可信 prior art 缺漏时才动。

**交付**：N12_C8V_REV2_2_E4_MINIMAL_SCIENTIFIC_DIFF_AND_RATIONALE.md；包含逐句前后差异、证据来源、E2/E3 issue ID、修改理由、保留/删除的重复内容。零正文改动允许 E4 NO_CHANGE_PASS。

### E5-R1 — P1 复用现有科学守卫与双 PDF 的差异化验收

**若 E4 存在 main.tex 或其他科学文件改动**：在确切新 head SHA 上运行当前 C8V Path A 语义/BibTeX 与 C7 表格/补充全文单元格守卫；两套真正完整 PDF 均成功，检查最终日志中引用、label、overfull/致命错误；视觉核对修改页和关键信息对应；记录两次 run IDs、head SHA、artifact IDs、PDF 页数、source hash。若旧守卫因合法措辞收紧而阻止构建，只能增补保护正确科学边界的断言，不关闭既有检查。

**若 E4 无正文/图表/补充源变化**：以已核实的原 I2-C 38p/47p 成功运行作为既有科学 PDF 基线，仅写明 no-new-source-change 和静态来源一致性；不得虚构新的 E5 CI PASS 或重新跑相同构建以充数量。作者最终投稿前仍须检查真正提交的精确 PDF 源版本。

**必须审查的语义**：claim-strength 与来源一致、不同 cohorts/ranking units 不混用、图注与文本对应、三条贡献与 Results/Discussion/Conclusion 同一中心主张、对 corrected-S/Always Memory/RQ3 负面边界不冲突。

**交付**：N12_C8V_REV2_2_E5_SCIENTIFIC_SOURCE_AND_DUAL_PDF_QA.md；PASS 或 NO_SOURCE_CHANGE_BASELINE_REUSED 或 HOLD；技术 CI PASS 不是学术创新性认证。

### E6-R1 — P0/P1 真实独立学术意见与责任作者 GO/NO-GO

**可前置征询，不新建平行流程**：E2/E3 后可复用 Rev2.1 I2-D 人审问题包和 E1 最近邻研究矩阵，请真实推荐/方法学学者优先判断 candidate-indexed knowledge-use supervision 与已有 sampled metrics/deferral 是否具有 KBS 需要的独立价值。该前置征询记录在 E6 的**同一台账**；如暂时不可获得，则标 PENDING，不把 AI 内部意见代签或让该项阻止 E4/E5 的科学整理。

**最终评审**：E5 后对修订稿完整检查：(i) 非平凡原创性；(ii) 原 S 未校正与 F 自然调用不等；(iii) H2 prereveal 子条件未验证；(iv) Always Memory 准确率与旧负面 cost；(v) corrected-S 缺位；(vi) 同期额外 ID 不等于后来时间泛化。真实学者姓名、学术身份、独立书面意见、日期、利益冲突、作者响应均由人类提供，不得伪造。

**责任作者独占门槛**：所有原始统计与数据权限逐项签认；现行 KBS Guide for Authors / title-page/Highlights/abstract/declarations 按实际投稿门户核实，别以 Elsevier 通用说明冒充 KBS 专项条款；真实作者身份、CRediT/COI/funding、伦理和数据可用性、与实际 AI 研究/写作使用相符的披露、合法来源及归档。期刊 AI 使用政策：https://www.elsevier.com/en-au/about/policies-and-standards/generative-ai-policies-for-journals 。

**交付**：N12_C8V_REV2_2_E6_REAL_EXTERNAL_REVIEW_AND_AUTHOR_DECISION.md（初始 PENDING）；作者书面 GO/REVISION/NO-GO 和与准备用于投稿的精确 PDF/源 SHA 匹配的存档。

**决策**：
- GO：真实人审认可 bounded empirical 主张在 KBS 的科研贡献充分，作者接受风险、数据/版权/声明/期刊专项要求已核实、最终版本完备。
- REVISION：若仅涉及证据遗漏或措辞，按 E2/E3→E4→E5 的最小路径处理，不作全篇重写。
- NO-GO / 独立新课题：若必需真实 corrected-S、严格同成本、完整重新预注册 Null、后来时段或线上外推证据，则当前 Path A 不应重开原 TEST；单独注册合法独立研究或重新考虑期刊定位。

## 4. 工作量控制、验收标准和停止规则

**实际剩余路线**：E0 DONE → E1 DONE → **E2-R1 → E3-R1 → 按可用性征询 E6 早期独立意见 → E4（可 NO CHANGE）→ E5 → E6 最终作者决定**。不重命名为 N13，不新增“创新性理论”“全局资源最优”等未经识别的 claim。

**唯一新增价值标准**：每个拟加入主文的科学句子，必须至少有 (a) 未被正确表达的已有证据、(b) 明确的最近邻差异、(c) 实质适用条件、(d) 对误导性表述的修复之一。没有增量则删除任务，不要求硬凑句子、表格或 p 值。

**完成 E2/E3 的合格结果可以是无改稿**，只要 source-to-claim audit 明确确认科学充分性并保留未解决风险。质量控制任务的通过不表示 novelty HIGH 变为 LOW。

**硬停止规则**：
- 任何引发新 DEV 选择偏差、重新开放 G5/B4-A TEST、事后补盖 H2 prereveal 验收、非法私有事件导出、伪造独立人审/作者签署，均 STOP。
- 任何新的严格同调用、成本节省、具体因果语义或后来时期外推 claim 必须先有独立、有效的数据和识别方案；当前 Path A 只记录 gap。
- 如果独立审阅认为“known sampled bias + learned defer”构成平凡组合且现有发现无足够独立价值，必须保留 HIGH/NO-GO 选项，不能用文学性叙述把创新性自动评为通过。

## 5. 残余科研风险总账（沿用原成果，不伪造关闭）

| 审稿风险 | 已写入论文的证据及位置 | 本轮处理 | 仍未解决 |
| --- | --- | --- | --- |
| 采样 bias + defer 的普通组合 | Intro 47–52 / Discussion 603–608 / B1-G2-H1 | E2 检查是否有**实质遗漏**，真实人审判断 | KBS 非平凡原创性：HIGH |
| F/S budget/calls 不等 | RQ2 513–534 / Discussion 617，401/539 更少自然 calls | 一致性核验，默认 L0 | 严格等调用标签单因子因果效应 |
| Always Memory 更准/旧 selector 更慢 | Results 573–599 / Discussion 626 | 不重复写，检查 Abstract/Highlights | 真实 quota 的成本/必要性、最新 gate 实测 |
| 合理 corrected-S 未比较 | Related Work 100 / Discussion 624 | 默认 L0，不重训 V2b | 合法 sampled-only conditional corrected policy |
| H2 Null prereveal 缺口和复合机制 | Results 540–570 / Discussion 622 | Figure 1 L1 候选修复 | 单一历史语义因果及缺失的事前验收 |
| 同期额外 TEST/离线曝光选择 | RQ2 513–528 / Discussion 624 | 样本口径巡检 | 未来期外推与在线效果 |

## 6. KBS/科研完整性与归档管理

- KBS 官方 journal scope：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051；具体 Guide for Authors 需责任作者从期刊官方当前投稿入口验证，不擅自声称已有权威 KBS abstract 字数、页数、Highlights 等限制。
- Elsevier **期刊** AI 政策：https://www.elsevier.com/en-au/about/policies-and-standards/generative-ai-policies-for-journals。不得引用“books and commissioned content”政策当作期刊专用规则；作者必须核实并透明披露实际生成式 AI 使用、研究与论文生成的参与范围；AI 不能代替作者、数据真实性与人工审稿。
- KuaiLive-M3 精确 release 数据权利/非商业条款与公开元数据差异、匿名事件/模型私有归档、受限制衍生品再分发仍由责任作者核定；不把 license 歧义直接等同论文不可投稿，也不得未经授权上传原始私人事件。
- 既有 Actions PDF artifacts 在先前 CI 中记录约 **2026-12-19 UTC** 到期；须在到期前由有权限者合法创建长久可复核的材料归档，记录源 SHA、分割 manifest、论文 PDF 和统计来源。
- PR #6 保持 Draft，直至作者决定；任何 Rev2.2-R1 文档提交不意味着正文变更、真实外部审稿、KBS submission 或 CI 已通过。

## 7. 最新状态与执行入口

**REV2.2-R1 PLAN REVISED / E0 DONE / E1 DONE / E2–E6 PENDING / MAIN SCIENTIFIC SOURCE UNCHANGED / NO NEW TEST / KBS AUTHOR GO PENDING.**

下一步唯一默认入口：**E2-R1**，先审查已完成论文的科学贡献增量，并允许明确作出 NO_MAIN_TEXT_CHANGE_REQUIRED；之后 E3-R1 才确认实际修改清单。除非明确新发现科学差错，否则不提前修改 main.tex、Supplement 或冻结结果。