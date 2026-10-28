# N12-C7 | Bidirectional Claim-to-Source Ledger, Reproducibility Tiers and Rights Register

日期：2026-10-19。**C7审计文档，尚非伦理/授权完成证明**。主稿源：`main.tex`；来源冻结：`analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json`、N12-C0 source map、N12-C6审计。禁止新TEST开封/重训练/暗改统计。

## 1. 主文主张—样本—结果—来源映射

| ID | 主文落点 / 主张 | 推断总体与评价环境 | 结果或计算 | 可信来源 / 层级 | 不可提升为 |
| --- | --- | --- | --- | --- | --- |
| RQ1-Twitch | §5.1 historical complementarity; §5.2 Utility | Twitch streamer TEST 44,221 | Base .58211; Memory .53980; Utility .58983 / 6650 calls; outcome-defined recoverable subgroup 5539 gain +.22045 | 原冻结Results `tab:results-twitch-policy`; S10.19 Table S10.13; original manuscript fixture | 子群体当作pretarget feature、等调用Difficulty为在线冻结策略 |
| RQ1-KuaiLive | §5.1 candidate regime | 原KuaiLive room paired retrospective 10,222 | Memory−Base S −.04120 / F +.04631; shift +.08751 | 原表 `tab:results-factorial` 与冻结C4 Eq | isolated candidate-count cause、与M3 author同任务 |
| RQ2-M3-orig | §5.2 incumbent-relative choice | M3 original TEST 47,575 author targets/12,533 users; six SAS/GRU model fits **同一TEST总体** | Primary SAS Base .25800, Utility .30287, Always Memory .34679, calls 29.21%; robustness six fits | 原表 `tab:results-m3-policy`, `tab:results-m3-robustness`, S8 | 六个独立TEST/cohort、无约束超过Always Memory |
| RQ2-DEV | §5.2 / §6.2 switch mechanism | M3 DEV 50,049/12,628 users, five outer x four inner user-disjoint, primary Base fits; *exploratory* | SAS/GRU F−S +.006159/+ .004970; 10672/11517 decision switches; new selected gains > dropped gains | S10.19 Table S10.14, N9 G2/E1 report and public aggregate | independent new TEST, 53.8%纯正负翻转、new theorem |
| RQ2-H1 | §5.2 `tab:results-m3-b4a-supervision` | 30,000 additional **same-period** author-target IDs / 10,387 users; 20-cell eligible-pop weighted F NDCG, user-cluster CI, Holm three-H family | SAS F−S+.005391 CI [.003646,.007174] p .000600, calls 8704/9105; GRU +.003585 CI [.001599,.005576] p .000800, calls 8629/9168 | 原冻结H1表、B4-A A4/A5 signed aggregate reports; original scientific contract | strict equal calls, future-time independent replication |
| RQ3-H2 | §5.3 `tab:results-m3-additional-relation-identity` | 4,096 **nested within H1**/3,059 users; fixed F current candidates; three null seeds same cohort | authentic .334942, null mean .303797, gap +.031145 CI [.027389,.035098], Holm p .000600 | frozen H2 table; S10.15–S10.18 | isolate one relation mechanism, H2 original prereveal popularity floor PASS (**NOT VERIFIED**) |
| Cost/operate | §5.4 `tab:results-n10-cost` | 256 DEV requests ×3, original pointwise Utility, matched RTX3090 warmed replay | Utility 1.769ms vs Always Memory .692ms; additional H1 unconditional Always Memory .348744 > F policies | frozen cost table / S10.17–S10.18 | new vectorized gate measured, production savings |

七张保留主文原Results表以完整LaTeX原始块匹配；四张迁Supplement S10.19的表由 `n12_c7_full_table_cell_audit.py` 基于11表冻结源实施**17行/49数值单元格**逐一校验，包括符号、精度、CI边界和行语义映射；只是选定数值字符串存在不足以说明每格相同。

## 2. 全部样本层级与统计解释核对

- Twitch streamer原TEST、KuaiLive room paired回顾性、M3 persistent-author TEST是三种不同rank unit，没有因果跨平台复现。
- 额外30k来自相同2026-03-27—03-31采集期；只与原已评价TEST事件ID互斥，不保证user/history独立；nested 4096共享30k母样本，不能增加独立证据次数。
- F/S gate在内层DEV依据上限阈值冻结；TEST真实call比例有漂移，H1自然calls差超原1pp容忍，不能宣称等调用因果隔离。
- Null约76.8%历史边重排同时改变重复配对和高阶拓扑；三个seed是共同cohort的技术扰动而非样本独立重现；原同队列训练Popularity门槛未于揭盲前确证。
- 检验三项预承诺Holm H族及每种CI的用户聚类级别，不可把原六fit TEST的统计检验与30k三项新H族混成一个群体。
- 单观察正反馈的离线NDCG@10受记录曝光机制影响，不是在线因果用户福利。
- 主文与Supplement旧S10中DEV探索及原TEST结果必须标明不同等级；无原始可公开event rows则不得宣称第三方可完全复核全部置信区间。

## 3. 可复现性等级矩阵

| 层级 | 可做的工作 | 当前判断 / 缺口 |
| --- | --- | --- |
| A：公共source可重复审计 | GitHub LaTeX、冻结结果块hash/比较、原始表迁移逐cell检查、公开汇总、Actions双PDF | **可审计**；scripts/fixtures已公开。成功CI只证明来源一致，不证明私有原始事件评分可由外人独立从零再算 |
| B：有条件的端到端复现 | 配置正确公开数据版本、许可与合规访问、数据预处理、原训练与官方划分、models、hashes | **待完成**：目前不能认定整套原始TRAIN/DEV/TEST事件与权重都具备公开可用分发权限 |
| C：私有或受限原始数据 | 私有M3事件、对象ID、私有TEST/cache、pre-reveal artifacts / model weights | **不应为追求复现而上传公开**；维护代码、摘要hash、执行参数与授权受控访问说明 |
| D：尚未做的科学扩展 | 真实未来期TEST、严格等调用预先冻结政策、在线/真实成本负载、完整source×gate设计 | **NOT PERFORMED**；只能标注待研究，不能填进现有结果 |

C7必须将代码commit、配置/版本、公开汇总、PDF工件manifest长存；GitHub artifact会到期，且ZIP digest不等于内部PDF digest。

## 4. 数据来源、权属和隐私（待作者复核，**NOT CLEARED**）

- 原始KuaiLive项目仓库（需确认研究实际使用的确切release）：https://github.com/imgkkk574/KuaiLive 。原始release/仓库的非商业共享条款或其他具体权限需通过该版本的license文件与data owner核查。
- Hugging Face数据集`imgkkk2004/KuaiLive-M3`页当前标`cc-by-sa-4.0`：https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3 。该元数据**不能自动证明**作者原库、M3全部实体或本研究私有衍生物拥有相同再分发许可。该数据卡README目前空白，实际研究下载commit、许可来源和联系人书面确认都应列为提交前阻断项。
- 对Twitch/LiveRec及自制拆分也要确认官方数据条款、是否允许公开模型权重/派生特征与标识符，以及小样本/用户级结果的再识别风险。
- **许可状态：OPEN / REQUIRES HUMAN VERIFICATION**；未做直接授权联系人确认。不得在Data Availability声明写成“所有数据已公开，可自由再分发”。

## 5. Elsevier/KBS合规准备（非作者最终签署）

Elsevier在2026-06更新的生成式AI期刊政策：https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals 。人类作者必须核验内容；实质性AI文稿组织/句子改写应在投稿稿件中提供独立Declaration，说明工具名、用途与作者审核；如果AI被用于研究设计或方法/分析，应在Methods提供可复现描述。任何未确认的工具使用范围、作者责任与伦理事项均不得由自动化助手代替作者签字。KBS最新投稿清单、ORCID/CRediT、funding/COI、Data/code availability、授权及隐私须以实际提交时的期刊要求为准。

**C7后续验收**：先以自动审计通过证实17行/49数值cell及双PDF未变，再完成人工审阅PDF关键图表与数据来源权利记录。未确认的原始许可和作者声明必须留给C8且视为投稿阻断，不得把C7代码审计写成法律授权PASS。


## 6. 2026-10-28 project-use confirmation and restricted P1-D scope

**User confirmation:** On 2026-10-28, the user explicitly confirmed in the project conversation: “确认数据可以使用” (the data may be used). This confirmation is recorded as permission to proceed with the narrowly scoped internal P1-D diagnostic described in the N15 gate record. It is not represented as an independently obtained source-owner letter or legal opinion.

**Public-source cross-check:** The original [KuaiLive repository](https://github.com/imgkkk574/KuaiLive) states CC BY-NC-SA 4.0; the [KuaiLive-M3 Hugging Face page](https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3) labels the dataset CC BY-SA 4.0 while its README/data card is empty. These public declarations differ. They do not by themselves establish identical terms for the exact downloaded M3 release, private B1/B2 derived artifacts, model weights, or user-level features. The exact source release/commit and applicable terms should remain part of author-side verification before any public redistribution.

**Permitted narrow action under the user's confirmation:** one q=0.30 P1-D exploratory diagnostic, on the already-existing restricted B1/B2 DEV artifacts and approved self-hosted runner only; exact frozen six-feature panel; Full versus Long-only; five existing user-disjoint folds; aggregate-only JSON. No raw rows, identifiers, per-event scores, checkpoints, model weights or private cache files may be exported to GitHub. No TEST/G5/B4-A access, retraining of Base/Memory models, source expansion, quota sweep or public data/model release is authorized by this entry.

**Rights status split:**
- Internal, narrow P1-D computation: **USER-CONFIRMED TO PROCEED**, subject to the protocol/hash/compute/output gates in the dated N15 P1-D record.
- Independent legal verification of upstream licensing, and public redistribution of source data or derived private artifacts: **OPEN / NOT CLEARED**.

This distinction prevents the user's project-level confirmation from being misreported as a verified license grant for every upstream or derived artifact.
