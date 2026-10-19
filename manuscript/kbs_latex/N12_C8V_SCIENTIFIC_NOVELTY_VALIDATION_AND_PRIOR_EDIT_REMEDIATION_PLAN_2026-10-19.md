# N12-C8V | 科学创新性独立验证与上一轮遗留问题修复方案（2026-10-19）

**文档性质：PLAN ONLY，尚未执行；不是论文已修复、验证已通过或实验已发生的证明。** 对象为 N12 Draft PR #6，分支 kbs-n12-single-thesis-restructure-plan-20261014；计划起点 HEAD c3e25fddae6668c1297108a3c9020aa4756a0af1，最近完成的论文科学/双PDF CI #39209043536（37页主文 + 47页补充材料，C7源表17行/49数值cell审核通过）。C0–C7历史通过记录不可倒改，C8三角色模拟审稿与C8N文字强化已完成；C8作者最终Go/No-go仍未完成。本计划新增 **C8V 验证门槛**，应先执行完验证再考虑大范围叙事重写。执行本计划本身不要求重新TRAIN、揭封原TEST、向KBS投稿或合并PR。

## A. 唯一要验证的科学命题，以及三种不同强度

**基本命题：** 对固定外部历史关系Memory专家 M、既有Base B及目标完整候选 F，候选抽样不仅影响 NDCG 报告，还影响用来监督请求级Memory调用策略的增量效用标签。F-和原始S监督训练的冻结完整策略在F下表现不同；DEV的请求级switch解释这些策略如何重新分配Memory调用。RQ3的真实历史对照是平行来源有效性，不是这一选择机制的因果中介。

- **层级 L1（现有结果已经支持）**：特定同期间 M3 30,000 targets上，F-监督完整冻结策略的加权 F NDCG 优于原始 S-监督策略，且实际Memory调用更少；SAS +0.005391、calls F/S 8704/9105，GRU +0.003585、calls 8629/9168。冻结用户聚类CI/Holm不变。只允许称“上述已冻结策略比较”。
- **层级 L2（部分由现有DEV提供解释，但待替代解释审查）**：后G5、50,049 M3 DEV事件上的请求分歧与switch accounting解释候选监督目标不同如何改变受限知识分配；它是代数分解与探索性观察，不能冒充30k TEST的独立机制实验。
- **层级 L3（当前没有证据充分成立）**：所有采样校正监督均劣于F；纯监督标签在严格等调用条件下的因果效应；该规律是历史关系知识独有；任何新方法定理、独立未来时间外推或真实系统节约。不得因为L1显著就提升为L3。
- **RQ3平行**：原4096嵌套TEST真实历史0.334942 vs三Null逐事件均值0.303797，差+0.031145；其NDCG/top10/有效扰动的多项Null诊断已通过，但原同队列TRAIN-only Popularity prereveal非退化检查未按预承诺流程完成；“控制验收不完整”不是“全部Null失败”，同样不能追认原预验收全部PASS。

## B. 先修复上一轮修改遗留的确定性问题：C8V-0（必须独立小PR/commit范围审阅）

**B0-1 摘要分母语义错误（P0，已由原E1报告证实）**
- 当前Abstract写作 “the policies disagree on 21--23% of Memory invocations”。原N9-G2/E1为：SAS 10672/50049=21.32%、GRU 11517/50049=23.01%，分母是**全部DEV事件/请求**，不是Memory调用次数。
- 建议英文精确替换为：“On 50,049 exploratory DEV requests, full- and sampled-supervised policies disagree on the Memory-invocation decision for 21.32% of SASRec requests and 23.01% of GRU4Rec requests.”
- 通过标准：摘要、Results、Discussion、Highlights、图题、S10均不得写作“of Memory invocations”；文内每一个%须标明分子、分母、总体、DEV/TEST和是否weighted。审计不应仅检查存在21--23字符串。

**B0-2 已冻结策略的质量与调用关系（P0，避免负面过度解释）**
- 在30k上F在NDCG和**实际调用次数**两维均优于所比较的S冻结策略。不能把超出旧1pp解释阈值写成“结果失败/不公平致使优势不成立”；也不能把它写成严格等调用的纯监督效应。
- 建议正文“F-aligned frozen configurations show a favorable observed quality–invocation comparison relative to the tested S configurations; the natural call differences exceed the prespecified approximate equal-call range.” 同时区分**20-cell weighted NDCG/加权调用比例**与报告里的**unweighted调用次数**。
- 通过标准：核对SAS F/S 8704/9105、GRU 8629/9168、1.337/1.797pp、H1 CI/p、Always Memory 0.348744且确实更高；不以新文句改计算。

**B0-3 RQ3非退化控制解释（P0，避免把部分缺失说成整体失败）**
- 清楚区分已完成的3seed fixed F、null NDCG 0.302796–0.304689、约1903–1913 Top-10 positives、76.78–76.80% rewiring，与**未按预揭盲流程建立的同队列 TRAIN-only Popularity 对比门槛**。
- 一句话“Original prereveal acceptance was only partially established: the cohort-specific TRAIN-popularity comparison was not verified, although separate outcome-independent sealing, null-ranking nondegeneracy and rewiring checks passed.”
- 通过标准：不能写“all preregistered null checks passed”，也不能写“entire H2 invalid”；不能通过事后看真实目标、新换seed或重新校准补签此前验收。

**B0-4 独立性、数据可见性与指标语言（P0）**
- 再核对：RQ1原KuaiLive 10222为**room** paired，RQ2 30k为**author** same-period，最初M3 47575及六fit同一TEST总体，4096嵌套30k；DEV 50049不等于H1 confirmatory TEST；S为保留已观察target并抽574 negatives 的**离线监督标签**，不能构造成target-aware的部署路径。
- 约53.8%的DEV类别转移含zero与非zero，**真正非零正负反向仅SAS 157/GRU 145**；不得错称“半数事件正负反转”。DEV on/off收益均为正，不称“主要避免负收益Memory调用”。
- 通过标准：完成一份 all-numeric-prose ledger，至少扫描Abstract、贡献bullet、Results解释、Discussion、Conclusion、Highlights、所有图表标题/脚注；每数值均给原source+分母/单位+证据等级。仅机器查表不够。

**B0-5 上次CI盲区修复（P0）**
- 原C6/C7检查保证7张主文原Results表和4张Supp迁移表17行/49数字不变、公式/引用/PDF完整，但不会从句子理解分母或不当因果。新增 **语义合同测试**（建议文件 analysis/kbs_plan_c/n12_c8v_scientific_semantics_audit.py 和 unittest），最少含：
  ① Abstract不含 “% of Memory invocations”/相同歧义；
  ② DEV分歧按 10672、11517 / 50049 计算，检查四舍五入；
  ③ 30k F/S counts、差值、30k weighted vs raw quantities、old 1pp解释相容；
  ④ 原H2 popularity subgate明确 NOT VERIFIED、其它3项有证据；
  ⑤ Always Memory/负面legacy timing、非新gate计时；
  ⑥ RQ1 room vs M3 author，DEV探索与B4-A冻结互不误称独立；
  ⑦ 相关引用keys解析、主要新先例BibTeX元信息/引用、双PDF可见；
  ⑧ 测试故意篡改Abstract分母、H2验收表述、原H1调用计数时**必须失败**。
- 验收依然需要一名与修订者不同的科研审阅者人工读Abstract/Discussion/PDF；自动审计通过不是科学审稿。原C6/C7历史PASS保持；本轮新CI用新文件名/run/hash与页数。

**C8V-0 EXIT**：仅文本/审计修复；所有错误有old→new、source line、test name和真实修复CI记录。未得到新CI不标PASS；如发现实质性统计冲突，停止文本编辑、单独转源追溯审查。

## C. 现有文献的原创性威胁：C8V-1（先案文献审查门槛）

至少逐一精读或核查方法/实验对象，而非仅罗列标题：
1. Krichene & Rendle, KDD2020 sampled metric inconsistency及其bias/MSE corrections：https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
2. Mao, Mohri & Zhong, ICML2024 Regression with Multi-Expert Deferral：https://proceedings.mlr.press/v235/mao24d.html
3. Mandi et al., JAIR2024 Decision-Focused Learning survey DOI 10.1613/JAIR.1.15320：https://mlanthology.org/jair/2024/mandi2024jair-decisionfocused/
4. Qian et al., **2026-07-27 arXiv PREPRINT** *When Should Active RAG Retrieve? A Budget-Aware Evaluation of Utility, Calibration, and Cost*（真实且近邻；是QA/RAG，不是推荐）：https://arxiv.org/abs/2607.24010 。对比其增量效用、exact vs deployable frontier、阈值迁移、实际使用率与路由开销：**不可再宣称首次提出Base-relative external-knowledge utility和预算门控**。
5. DS-Frame fast/slow recommender（https://arxiv.org/abs/2609.02671）、SAMD记忆保留/MHGFCL知识融合仅做精确边界比较，不能强制将推荐记忆计数包装成KG语义推理。
6. 搜索截至本轮日期2026-10-19更直接的 “sampled candidate regime + routing/deferral supervision” 先例；区分正式发表与预印本。每篇填：研究任务、已存在的理论或结果、N12真正不同的估计对象、**能支撑此差异的现有数据**、仍未排除的相似性。

**评分规则**：主创新点必须在剔除“采样指标不一致”“选择高收益专家”“面向决策学习”“按预算选择外部知识”四类先例后，仍留下至少一个能用**实际policy-switch行为、同候选冻结policy结局**检验的非平凡经验发现。若剩余只是“train/test candidate matches better”，标 **NOVELTY_GATE_NARROW**，不靠“首次”“独特”等字眼补救。

**C8V-1 EXIT**：近邻文献6列表 + 独立编辑反驳稿，并由未参与主要改稿的科研审阅者签署“可防守/需收缩/需新证据”，不等于真实KBS审稿意见。

## D. corrected-S 是否可用：C8V-2（先检查可行性，绝不能先宣称结果）

**最直接的竞争性解释**：已知原样本S用 target-retained、574个无放回均匀随机负样本组成575候选，其sampled NDCG可能是未经校正的不一致标签。F优于**原始未经校正S**，不自动意味着F优于任意合法校正S。

### D2-0 数据充足性与估计对象冻结（不读取任何封存TEST）
- 在私有 DEV 或公共schema/受限元数据范围确认：每请求完整F候选人数 N、S抽样法/seed及inclusion probabilities、true target仅用于DEV离线label、**正例的完整采样rank（包括top10以外的censored情形）**、是否有全部F与S候选scores和原始排序/tie处理。当前公开B1摘要包含 sampled top10 NDCG scalar，**未证明**完整sampled排序或每个候选的分数都存在；不能把Krichene的correction直接套到只给top10 NDCG的缓存上。
- 若部分必要字段缺失，可仅从既存合法 **DEV** 原始请求在权限内重建/重新评分：先独立审计无未来数据、可重建全rank与sampling law、与冻结原始B1的S/F对照逐行达到定义一致。**不得访问A4目标标签或原G5已评价TEST以筛选方案**。
- 方法学规格必须写清corrected-S实际上估计什么（全候选单正例 NDCG@10 的哪个量，是否逐event有偏/仅总体近似）、哪些分数/先验用于校正、是否引入F真实标签。如果方法需要用F标签校正，则成为**F-assisted hybrid**，不得叫不含F信息的S-only监督。

### D2-1 只有可行才开展DEV限定性实验
- 冻结 correction方法/参数/验证协议后，用无标签泄露的独立synthetic known-full-ranking样本检验统计性质，包括 varying candidate N、正例rank>10、ties/全候选多样性、574无放回采样；不事后挑最好一版。
- 严格对照三臂：original S / validated corrected-S / actual F，**同B、M、Z、模型容量、outer user folds、内层预算与候选F评价**；B和M分别校正后取差值，必要时报告校正后的预测值error和决策损失，不能仅报告训练拟合误差。
- 输出：完整DEV用户分组的 full-F NDCG、调用率、switch、value estimation error、校准迁移；DEV-only探索性效应/区间标记，不独立确认，不移植旧B4-A Holm p。
- 不可行时明确 **CORRECTED_S_INFEASIBLE_WITH_AVAILABLE_SOURCE**：报告缺什么信息/现有理论无法准确用于该S采样，文稿claim收缩为“full F vs tested uncorrected target-retained S”；不是偷偷以另一个不正确估计器充数。

**C8V-2 EXIT**：产出 data sufficiency decision、verified estimator contract、synthetic unit tests、若可行再DEV aggregate；否则完整negative feasibility report。**禁止**回头使用已经揭示的30k TEST训练/调参/equalize来追认新confirmatory效果。

## E. 识别和知识来源特异性：C8V-3（优先复用证据）

### E3-0 来源×候选×使用的受控证据矩阵
- 只读归档B2 Full/Long/Short/Popularity/history-placement placebo，分别分解：source-only F/S NDCG、Base-relative gain、selector S/F政策质量、actual call counts、features 6/12信息合同与floor。
- 重点检验反例：Long-only十二特征迁移损失 SAS .010605 / GRU .010262 均高于Full (.006159/.004970)；Short-only约.0207而自然calls严重不匹配；Popularity/placebo回归到Base地板，接近零“迁移损失”**不是**候选不敏感的一般定理。
- 输出一页claim-strength matrix： (i) under this historical source, supervision mismatch observed (**supported**); (ii) historical-source component moderates the phenomenon (**exploratory mixed evidence**); (iii) historical relation semantics uniquely cause it (**not established**)。
- 若有DEV上现成的质量匹配、非关系专家、固定same-B same-F score供应，可先核对可比性/合法信息合同，再设计**单独exploratory**的非关系专家对照；不得为凑“知识特异性”构造质量悬殊或不按相同预算的弱基线。

### E3-1 跨协议桥接和对照边界
- 把原KuaiLive room 10,222 S−.04120/F+.04631定位为不同rank unit的 paired diagnostic；M3 author DEV 50,049 S/F+policy switch 和 frozen 30k author H1作为**主证据链**；Twitch 44,221只作历史互补性和另一个既有协议上的支持。不能从room flip推断M3决策增益的直接因果机制。
- RQ3原4096 Null仅是parallel source information test，缺Popularity子验收及强扰动复合性，不能被写成“RQ2由关系身份因果驱动”。

**C8V-3 EXIT**：给出支持、部分支持、不支持三等级；若只剩一般ranking/candidate效应，稿件定位为 knowledge-use evaluation application，而非“relationship-specific mechanism”。

## F. 预算公平性、候选监督及实际成本：C8V-4

- 对30k已揭盲H1仅复述冻结数字、原权重与调用数，不重调TEST阈值；SAS F calls8704<S9105，GRU F8629<S9168，**观察到的是更高质量且较少调用的完整政策比较**，不是equal-call isolating effect。
- 在原50,049 user-disjoint DEV内部可以**事先锁定** 10%、20%、30%三个额度做两种诊断，必须分开：
  1. **hindsight matched top-k quota**：TEST不可部署的固定请求数比较，仅解释score对高收益事件的排序；
  2. **deployable inner-DEV calibrated threshold**：在inner用户上定阈值、在outer用户上不动阈值评价，报告实际calls/超标/效用/用户聚类区间。
- 参考Qian2026区分ranking frontier、threshold transfer、pre-decision gate overhead；任何拟合目标选择以当前DEV为准，不冒充独立新TEST，且不得根据H1观察性能挑选额度。
- Always Memory在同30k上的0.348744、旧pointwise warmed 256 DEV×3均值Utility1.76941ms vs Always Memory0.69165ms保留；后者**不是**新B4-A向量化F gate，因此不说新gate已被测慢，也不把较少Memory calls写成实际生产节约。真实外生知识额度存在性目前只是设计条件，非观测经济事实。

**C8V-4 EXIT**：区分ranking、deployable、call parity、cost四条结论；如新预算frontier不支持强结论，科学主张按现有冻结结果降级，不能选最有利子区间报稿。

## G. 执行时序、交付物、决策门槛（不得一轮内全部宣告PASS）

| 门槛 | 任务/可交付文件（建议路径位于manuscript/kbs_latex或analysis/kbs_plan_c） | 验收/失败行动 |
| --- | --- | --- |
| V0 | prior-edit defect register + old/new text diff + semantic-contract unit tests + stage-named main/supp CI/PDF | **优先执行**。分母/证据等级/引用/统计总体全部修好才进入V1；不变更科研结果 |
| V1 | SCIENTIFIC_PRIOR_ART_CLAIM_MATRIX.md；2026 RAG及修正采样估计来源方法审查 | 产生可辩护差异或“贡献需收缩”裁决，不用措辞弥补缺方法 |
| V2a | CORRECTED_S_INFORMATION_AUDIT.md；DEV metadata/schema/无泄露可行性报告 | 判FEASIBLE/INFEASIBLE/HOLD；未证明能做就停，不自行制造假校正 |
| V2b（条件式） | CORRECTED_S_DEV_PILOT_PROTOCOL.md；synthetic tests；DEV-only 3-arm aggregate | 仅在V2a可行且预先定规则后；不得触碰冻结G5/30k H1/H2 TEST |
| V3 | SOURCE_CANDIDATE_SUPERVISION_EVIDENCE_MATRIX.md | 复用B2并准确报告Long-only等反例，不能假装关系知识独有因果定理 |
| V4（可选） | DEV_ONLY_INVOCATION_FRONTIERS.md + real/weighted-call contract | 必须区分理想等调用与可部署阈值；若无资源/必要性可报告已有数据的边界，不强制额外训练 |
| V5 | INDEPENDENT_KBS_EDITOR_METHODS_SYSTEMS_REVIEW.md + point-by-point response | 针对每条contribution留下证据与未排除解释；独立审阅，不把CI当peer review |
| V6（仅在V0–V5确定后） | 仅需要的最小稿件/Highlights/BibTeX修订、source-level CI、双PDF、版本/哈希、作者人工终审 | 如修订超出既有冻结范围则重新启动审计；C8作者Go/No-go另行判定 |

### 三个科学决策结局（V5必须二选一/三选一作出明确理由）
- **A / VALIDATED_BOUNDED_EMPIRICAL_CLAIM**：原始S/F policy结局与DEV switch解释稳健，替代解释有界，明确没有与已有采样/deferral/DFL完全相同的实证对象。允许准备一篇限缩的empirical KBS稿，不承诺接收。
- **B / CONTRIBUTION_REFRAME_REQUIRED**：正确校正后的S在DEV接近F或关系知识特异性不可支持，仍可报告“候选监督目标与已测试S构造的影响”，但不可抬高为普遍更优或独特机制；投稿定位谨慎。
- **C / INDEPENDENT_NEW_EVIDENCE_REQUIRED**：若作者确实希望主张等调用因果效应、关系身份机制独特性、未来时间推广或真实成本优势，另外设计新的独立时间窗/真实预算或来源交互试验，并事前封存，不能复用已揭盲30k当新确认。

### 技术与伦理边界
- 纯写作缺陷V0无需新标签。V1仅公开文献。V2–V4如需受限DEV只在已有可授权私有环境运行，公开仅不可逆聚合和源hash，不发表用户/author ID、原始事件或私有TEST行。**不因公共KuaiLive/M3不同许可标签本身自动阻断科学论文投稿**；如确有使用/隐私/再分发限制，按已有C8 licencing-scope修订处理。
- 当前声明不能从37p/47p CI推断“全部科学语义正确”；不能从新计划文件推断任何V0–V6任务已执行。
- 整个V系列执行完成前PR #6仍为Draft；作者个人的科学风险接受、CRediT/AI/Funding/COI/Data/Code声明、KBS现行指南和提交动作属于另一个**不可被助手代签**的C8人类审批门槛。

## H. 直接来源与材料索引

当前正文 main.tex（37p）、Highlights.txt、kbs_references.bib；状态 N12_C0_C1_EXECUTION_STATUS_2026-10-14.json（v11）；C8N核查 N12_C8N_DECISION_ALLOCATION_NOVELTY_REWRITE_QA_2026-10-19.md；原始 N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md（21.32%分母及corrected-S可行性）；B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md；N9_ROUTE_B_B4A_A2_FROZEN_ESTIMANDS_AND_DEV_GATE_SPEC_2026-10-14.md；N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md；N10_ROUTE_C_C2B_MATCHED_DEV_COST_AND_R2_VERDICT_2026-10-14.md；原冻结11表manifest与C7 17行/49cell验证器。

**最后声明**：本文件本身仅新增科学验证顺序和阻断标准；不得借创建此文件把任何验证阶段标记完成，不得修改冻结论文结果、模型/阈值或原始H1/H2记录。
