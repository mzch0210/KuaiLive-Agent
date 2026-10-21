# Rev3.2 W0｜主张归属、段落迁移与冻结证据锁定

**2026-10-20｜W0 COMPLETE：只读审计；主稿/补充材料未改。W1可开始；W2须遵循此矩阵。**

## 0. 冻结对象与范围
- Repo / branch：\`mzch0210/KuaiLive-Agent\` / \`kbs-n12-single-thesis-restructure-plan-20261014\`；W0开始的 Git HEAD \`56d38cc0305a92ba273fa3ed1bf7c81993eeac7b\`，其中文件变动是 Rev3.2 计划。
- 唯一论文科学版：commit \`a686cd07ce80f8d4090aae720c0e583f39f73176\`；\`manuscript/kbs_latex/main.tex\` blob \`e5043a2fae305cfcdca49fefa3650732c927d1a4\`，**640行**，七章；\`SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md\` blob \`bb7d11074445988ecf637f895dad55084fc9577b\`，**1155行**。Rev3.0 final C7 #39398148734 / C8V #39398148731，主文39p＋Supplement47p，四jobs SUCCESS。
- 本文档的“原位置”统一指上述blob的 LaTeX **1-based 行号**，非PDF页码；W2以后行号改变，以LaTeX labels和本矩阵固定的anchor重新定位。不能凭行号覆盖后续新稿。
- N11/N12此前已完成七章、方法合并和重复表下沉，故**不再整章清空重写**。历史项目报告是证据溯源，不是需要原样放进期刊稿的编年史。

## 1. 一句话主张与证据强弱顺序

**中心**：在给定Base、已固定的历史关系Memory、排名候选与原始S/F监督协议下，候选制度影响相对知识价值标签和完整冻结知识调用政策的请求分配与排名效果。

**逻辑而非发现时间顺序**：研究动机=关系知识与Base的互补性（RQ1，Twitch与room）；最强新评价=**同采集期额外30k冻结F-vs-原uncorrected-S完整政策（H1）**；解释=50,049 DEV的G2调用集合差异（不等于H1因果机制）；有效性=嵌套4,096的H2真实历史对复合Null（与RQ2并行）；条件=外生quota和真实旧点式gate测时。

**保留的不利事实**：H1 calls SAS F 8,704 / S 9,105、GRU F 8,629 / S 9,168，实际差1.337/1.797pp，不可称严格同调用或单一标签效应；S是target-retained **uncorrected 575**；H2 原同队列 TRAIN-only Popularity prereveal门槛 **NOT VERIFIED**；H2复合干预≠单特征因果；Always Memory 更准、测得旧pointwise Utility更慢；额外H1不是未来期间独立外推；NI-1g V2b真实校正NO-GO不变。

## 2. 逐段现有→目标 owner 与动作（Results-first原则）

动作：**KEEP**保留；**MOVE**迁至指明小节；**MERGE**消除内容重复但保留唯一科学边界；**REFRAME**积极准确地解释；**S→**详细信息迁Supplement；**LEDGER**工程过程留GitHub审计。表中每一个范围都已由\`main.tex\`基准定位，最终W2–W7应在结果记录勾选。

| 原稿行号 / 标识 | 现有段落职责／问题 | 目标职责与动作 | 科学守卫 |
| --- | --- | --- | --- |
| 21，标题 | 历史Memory是否有用的提问在全文实际重心已转成监督→调用 | **W7 REASSESS**标题，允许保留原题或小幅强调candidate-aligned knowledge use | 不暗示新通用gate发明 |
| 25–27，Abstract | 背景＋三任务＋主H1＋多个limitations挤在一起 | **W7 REWRITE LAST**：问题/方法/完整政策主要结果/一条source check/含义；必要一处预算范围 | H1非等调用、原S未校正可发现，不能写部署节约 |
| 37–41，Intro P1–P3 | Base互补张力、先例并列、价值定义，逻辑尚可但主角不稳 | **W4 MERGE/REFRAME**：历史知识→Base-relative value→candidate-indexed target | Δ、F/S原义不变 |
| 43，Intro P4 | RQ2先行与RQ3并列已经正面表述但较抽象 | **W4 REFRAME** 一句话明确候选监督改变请求级使用与结果，RQ3是平行source check | 不画RQ2导致H2的因果箭头 |
| 45，Intro P5 | 三任务和实验证据形态密集罗列 | **W4 MOVE细节→§4**，前文仅解释为何三任务互补 | Twitch streamer/room/M3 author不能混 |
| 47–51，贡献三条 | 每条既给贡献又插“不能证明” | **W7/ W4 CONTRIBUTIONS** 主贡献RQ2在首、RQ1/RQ3各自附属；学术边界仅放必要位置 | H1和H2是不同估计量 |
| 55–81，Fig knowledge-value-chain | 单一val object，两条后果；与另一framework图表达局部重叠 | **W4 REVIEW**：仅留一张主框架图/若保留两张则一个研究问题图、一个信息权限图 | pretarget vs retrospective不得混 |
| 88–90，RW memory | 先例与本文区别部分反复 | **W4 KEEP+MERGE**，文献方法对象与固定source的真实gap | KBS SAMD/MHGFCL准确定位 |
| 94–96，RW deferral | 相对决策机制已知、decision-focused已知 | **W4 MERGE** 一次界定已有决策工具而非本稿发明 | 不产生firstness暗示 |
| 100–104，RW sampling/gap | 新五篇先例、candidate-dependence与通用评价偏差 | **W4 KEEP** 并把结尾gap收束至**knowledge-call policy consequences** | AAAI2021/2023、TORS2024、RecSys2025不能丢 |
| 110–126，Method ranking context | 单正例NDCG定义；context/candidate记号 | **W3 KEEP**，简洁一处说明single-positive ranking+target只在offline label | 公式\`eq:event-ndcg\`保留 |
| 132–142，fixed B/M | Twitch/room/M3不同ranker/Memory mixture | **W3 KEEP**，各协议区别首次说清后避免全文重复 | \`eq:memory-scoring\`原公式与0.45/0.45/0.10 |
| 148–169，Δ/η/SF | 中心建模与supervision-to-policy contrast，末段含重复式防御 | **W3 KEEP+MERGE**，以\`Δ→η→π\`正面过渡，必要完整政策估计目标保持 | \`eq:delta-memory\`, \`eq:eta\`, \`eq:candidate-supervision-transfer\` |
| 174–176，pretarget Z | 历史和Base-score的部署可见集 | **W3 KEEP**且与§4的训练权限对齐 | 历史/候选在决策前、target不能进入Z |
| 179–201，Fig framework | 执行决策图和后验source诊断混合 | **W3 REFRAME** online feature→label score→gate；后验states移结果诊断 | 不能让target-aware样本S成为线上输入 |
| 209–225，decision & quota | 标准效用恒等式后紧跟“不是新定理”句，阈值与quota定义 | **W3 KEEP+MERGE**，删除多余否定口吻，文献优先到RW | \`eq:expected-selective-gain\`, \`eq:utility-threshold\`，DEV限制不保证TEST calls |
| 227–250，posterior state/decomp | Twitch回顾性诊断内嵌决策规则，影响方法主线 | **W3 MOVE** 推至§4 RQ1诊断操作定义或Supplement S4，若保留方程需保持等价 | \`eq:diagnostic-states\`, \`eq:regime-decomposition\`现有九式不丢 |
| 255–277，Design intro & cohort list | 依历史实验先后列任务，段落与表重复 | **W3 REFRAME**先“主H1/支撑RQ1/并行H2”证据表，再介绍实际rank units和来源 | 同期额外IDs非独立future cohort |
| 279–289，\`tab:exp-datasets\` | TASK/evidence角色非常有用 | **W3 KEEP**，可调行顺序但不能更换排名对象 | Twitch streamer、room、M3 author准确 |
| 296–319，model/table | 回顾多个selection objective和任务，再列相同信息表 | **W3 MERGE**，主文一段对照意图，详细模型及差异至Supp | \`tab:exp-methods\`迁移须更新ref/fixture |
| 324–328，fitting/time | OOF/校准/历史更新协议被拆散 | **W3 KEEP**并放在各证据主体前一次性交代 | group folds/time lock不变 |
| 333–348，room paired formulas | C/R factorial与S/F客观效用分解 | **W3 KEEP**核心配对式，细节可由S5接管 | \`eq:paired-regime-shift\`,\`eq:factorial-allocations\`不删 |
| 350–354，DEV G2/B2 | post-G5解释性DEV与H2 pilot定义 | **W3 KEEP but subordinate**，不要抢H1/H2主协议位置 | DEV不是new TEST，20261014 seeds不是独立队列 |
| 358–362，additional H1/H2 | 当前最重要统计/信息设计后置 | **W3 MOVE FORWARD**在tasks/evidence table紧后说明H1政策与H2并行抽样 | same period，20cells，冻结评估，原S uncorrected |
| 368–376，stat/cost | CI、weights、3 Holm、模型和计时混在一起 | **W3 SPLIT**：数据/推断/硬件三段按Results证据位置展开 | 5000 cluster bootstrap、Kish不是独立用户 |
| 380，Results opening | 三个“successive” RQ措辞可能误读RQ3因果后续 | **W2 REFRAME**中心结果由RQ1动机导入，RQ3 parallel | 不声称中介 |
| 386–420，Twitch historical | recoverable/repeated context与状态图 | **W2 KEEP §5.1** 保持解释性铺垫，压掉表图数字重复 | 5,539 subgroup是hindsight defined |
| 423–442，room factorial | 10222 paired room候选反转 | **W2 KEEP §5.1**只留能导出候选监督的对照+一句图表结论 | room不能直接当M3训练效应 |
| 445–454，Twitch Utility & table | 在H1前先报策略选择，失去主次 | **W2 MOVE §5.4**，在5.2开头只用**一句**可信旧策略证据 | 44,221 TEST与M3区分 |
| 470–498，M3 original and six-fits tables | 核心决策能力支撑，但之前有多表遮住H1 | **W2 MOVE §5.4**，5.2开头一段简述完整M3 incumbent配置；六fit详细表可留S8 | 47,575 TEST六fits共享同TEST |
| 516–533，\`tab:results-m3-b4a-supervision\` | **最强政策后果结果**出现偏晚 | **W2 PROMOTE §5.2**（在5.1后即出现），保留S/F表、CI、real calls、同source时期 | H1+.005391/+.003585，calls非严格同配额；S uncorrected |
| 534–536，G2 DEV allocation | H1后简单补switch率，句子承担解释和限界两件事 | **W2 OWN §5.3**：明确F-only/S-only平均Δ、cohort 50,049 DEV、不是新独立确认 | SAS 10672 (21.32%), GRU11517 (23.01%) |
| 543–572，H2 source table | 真关系历史相对复合null + 控制说明，部分重复Methods/Discussion | **W2 KEEP §5.5**，真实缺失门槛在结果紧邻一处明说，其他限制Discussion集中 | +.031145 CI，H2 prereveal popularity condition unverified，4096 nested |
| 578–601，operating/cost table | A1旧quota路径、Always Memory真实更好与延迟旧路径更慢 | **W2 KEEP §5.6** 压掉反复“不节约”的同义句；表保留或下沉但真相可找到 | .348744>F .305446/.304530; 1.769>.692ms; new gate not measured |
| 608–610，Discussion 6.1 | 主结论真实但大段解释“不是new graph/deferral” | **W5 REFRAME**将context-dependent decision utility变成原则，文献定位一次 | 不能宣称first general theory |
| 615–619，Discussion 6.2 | 重新报H1+G2数字，与结果重合 | **W5 MERGE**提炼候选监督如何改变知识调用合同及对已有metrics/deferral理论的增量；统一限制段 | 有效corrected-S未比较，strict calls不相等 |
| 624–628，Discussion 6.3 | H2、评价、成本不同局限都挤在一起 | **W5 SPLIT** source meaning vs operational/validity; 避免仅再列失败清单 | composite intervention、H2 acceptance缺口、same period/成本均保留 |
| 633–635，Conclusion | 正面贡献后马上再重复密集限定 | **W5 REFRAME**以本稿建立的knowledge-use supervision contract与必要未来验证收尾 | 没有未来期/成本新结论 |

**主文图表迁移自检表（所有现有标签）**：
\`fig:knowledge-value-chain\` W4负责，与\`fig:framework\`审查功能冲突；\`fig:results-evidence-states\` §5.1保留或迁Supp只保留一套数字；\`tab:results-factorial\` §5.1；\`tab:results-twitch-policy\` §5.4；\`tab:results-m3-policy\` §5.4；\`tab:results-m3-robustness\` §5.4或S8；\`tab:results-m3-b4a-supervision\` §5.2首要；\`tab:results-m3-additional-relation-identity\` §5.5；\`tab:results-n10-cost\` §5.6；\`tab:exp-datasets\` §4；\`tab:exp-methods\` §4或Supplement。目标是适当突出主结果，**不是任意减少张数**。

## 3. Supplement科学原文责任及已确认遗留错位

| 原位置 | 问题 | W6必须处理 |
| --- | --- | --- |
| 首页L5 | date写13 October 2026，内容已经覆盖14日及其后冻结结果 | 时间元数据与真正最终科学版一致，文件名可不变 |
| S5.6 L375 | “Results Section 6.3”失效，现Results为§5 | 用标题/稳健xref替代裸章节编号 |
| S7.7 L584 | “final combined S1–S9”遗留，已有S10.19 | 改为不依赖旧版本号的科学表述 |
| S9.6 & S10.17 | 两次256 DEV测时方法不同并排且关键结果不同 | 简明条件对照；主文仅以counterbalanced来源为准 |
| S10.1–S10.19 L816–1155 | 按探索追加顺序列 B1/B2/G2/H1/H2/cost，S10.19倒回旧主结果 | 可移动并分组，但须 old/new S10迁移图；保留H1/H2的完整结果与预先未验证门槛 |
| S1.5 GitHub路径 | \`manuscript/kbs_latex/src/kuailive_agent/export_rechorus_room.py\` 实际不存在 | 更新成真实 \`src/kuailive_agent/export_rechorus_room.py\` |
| 多处 FAILED workflow / run IDs | 工程执行年表压入补充科学论证 | 期刊Supp留必要复现源链接与真实异常，详细重试历史保留GitHub audit |

## 4. 本次W0实际检查与历史重复的控制
- 原 \`KBS_ARGUMENT_DRIVEN_REVISION_PLAN_2026-10-10.md\`、\`KBS_THESIS_FIRST_REVISION_MASTERPLAN_2026-10-13.md\`、N11/ N12-C2/C3/C6/C8N 已做结构复审；本轮不同于旧计划：**为主文每段指定owner、动作、必须保留的科学事实，并以H1实际出现位置作为读者验收**，不是再发一份宏观“七章都优化”的口号。
- 冻结实验与 source-of-record：H1参见\`N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md\`与Supplement S10.15；G2见\`N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md\`及S10.9；H2见Supplement S10.16/S10.18；RQs其他数字见Supplement S10.13–S10.19。任何有冲突的叙述，以原结项科研结果和真实artifact为准，而不是选更好的措辞。
- Publisher写作来源：KBS官方目标 https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 ；Elsevier Results https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/how-to-write-the-results-section-of-a-research-paper/ ；Discussion https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/steps-to-write-excellent-discussion-in-manuscript/ 。结果优先、逻辑顺序、负结果不隐藏；这些是**编辑建议**而非专属期刊字数规定。
- 不新增 “related work firstness” 或新的采样校正/保守门控；KuaiRec X0-B真实历史适配 NO-GO，KBS学术原创性风险仍高；不重复跑私有TEST。

## 5. W0→W1 Gate（逐项已检查）

1. 源文件/历史run/主文七章归属与固定blob **VERIFIED**；W0新文件不修改科学源码。
2. 主结果H1能保持真实估计量与版式迁移；RQ1/RQ3并行，不作为H1因果中介。
3. 所有关键数字、样本角色、现有图表/公式label有归属，任何表迁Supplement需交叉引用更新。
4. H2 预先接受门槛NOT VERIFIED和其他不利事实保留在主文可发现位置。
5. W1可以**仅在新的单页storyboard中**编排论证；W2需等W1“首读测试”通过和源冻结核对完毕，不能因用户授权即可用改写冒称新的科研结论。

**W0 = PASS_FOR_W1.** 人类独立同行与投稿作者信息等工作仍PENDING，W0不是KBS审稿认可。
