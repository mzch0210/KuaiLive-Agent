# N12 Rev2.2-R1 E5 | 最新论文科学来源与双 PDF 实际验收

**2026-10-20｜E5 VERIFIED: DUAL_WORKFLOW_SUCCESS / SOURCE_LEVEL_SCIENCE_GUARDS_PASS / MAIN_FIGURE_VISUAL_PASS / EXTERNAL_PEER_REVIEW_PENDING。**

本报告依据实际 GitHub Actions 最新源码提交、两条完整工作流状态/Jobs/Artifacts、构建日志及**下载的 PDF 原件**形成。不是新科研实验或真实人类独立学术审稿，亦非责任作者向 KBS 投稿授权。

## 1. 确切源码和改动范围

- 仓库 `mzch0210/KuaiLive-Agent`；分支 `kbs-n12-single-thesis-restructure-plan-20261014`。
- E2 `PASS_WITH_NO_MAIN_TEXT_CHANGE_REQUIRED`；E3 `PASS_WITH_ONE_L1_WORDING_FIX`；E4 最初提交 `8f6d7bd4756536c1e4079ba498bd1b6e92e6e98b`，随后针对 Figure 1 狭窄标签的 PDF 自动断词做**单一视觉排版跟进提交** `36d9c3f2daed116061f12722db56448f371de60e`。
- **最终实际 QA 科学源 SHA：`36d9c3f2daed116061f12722db56448f371de60e`**，不可用更早 `8f6d7bd` 的成功 CI 代替新版 QA。
- `main.tex` 最终图内 RQ3 节点为：`Authentic history\\` / `versus constrained\\` / `historical randomizations};`；`valid historical nulls` 从该图中移除。仅改变原 Figure 1 局部标签的措辞和强制换行；未更改数值/模型/数据/图结构、结果表、摘要、Discussion、Highlights、Supplement、BibTeX 或单一推断强度。
- Fig 1 的 bounded claim 意义：历史 Null 保持部分 specified rewiring constraints，但额外 H2 cohort 原 `TRAIN-only Popularity` prereveal acceptance condition **NOT VERIFIED**，不能通过图中 `valid` 宣布全部 original conditions 成功。

## 2. 真实双工作流 QA 状态（均对应精确科学源 SHA）

| 工作流 | Run | main-paper job | complete-supplement job | 总结论 |
| --- | --- | --- | --- | --- |
| C8V semantic + source-frozen dual PDF | [#39364334948](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39364334948) | SUCCESS | SUCCESS | **completed / success** |
| C7 bounded science + migrated cells dual PDF | [#39364334815](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39364334815) | SUCCESS | SUCCESS | **completed / success** |

全部四个 jobs 对应 `36d9c3f2...`，非审计文件更新后的 HEAD。C8V/C7 科学断言、C7 迁移单元格、引用与互相来源合同、PDF 生成及日志标准检查全部以对应 Actions SUCCESS 为判据。无任何 TEST、模型再评分或私有事件导出。

### 工作流工件（GitHub artifact ZIP digest，不等于 PDF 原文件 SHA256）

| 工作流 | 工件类型 | GitHub artifact ID | ZIP SHA256 digest | 预计到期 |
| --- | --- | --- | --- | --- |
| C8V | main | **12238387608** | a9dfbecb9ee1d01e9733f8a4b91f5b726911bb6b1c4b65a924ff1e945935aadd | 2026-12-19T03:28:33Z |
| C8V | supplement | **12238457305** | b74d523f560b509bdb91e73ebf61050cc406c9061da2bdc33797001398e63525 | 2026-12-19T03:28:46Z |
| C7 | main | **12238842375** | ddccde1a6521ed9ad57692aa8533f290ffbc2391f355d4203836274ec47443e8 | 2026-12-19T03:29:42Z |
| C7 | supplement | **12238607578** | c2ba12c486d69c9448a987bb067d1d7114cece5abc2835ead53f983bb380708c | 2026-12-19T03:28:55Z |

## 3. 实际 PDF 下载、文字与页面查看

- 首笔 E4 `8f6d7bd` 的 C8V [#39363725060](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39363725060) 和 C7 [#39363725079](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39363725079) 均已 SUCCESS，但**不能**认为视觉上自动没有问题。
- 在受控工作环境实际下载了初版 C8V 主论文 artifact `12238975800` 和原科学基线 `12232693237`，解压 `main.pdf` 并对比 `pdftotext -layout`。PDF 都 38p。图 1 原文 `valid historical nulls` 确已移除，但初版目标字符串在狭窄盒宽上产生 `ver-/sus constrained histor-/ical randomizations` 非理想断词。初版 PDF 的其他 text diff 包含跨页排版漂移而非科学结果变更。
- 因此随后 E4 采用同义的三行节点强制换行，科学源 commit `36d9c3f2...`，重新触发 C7/C8V 全部构建，**没有通过关闭旧检查绕过守卫**。
- 在最新 C8V [#39364334948](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39364334948) artifact `12238387608` 中实际解压 `main.pdf`，`pdfinfo` 为 **38 页**，`pdftotext -layout` 显示 Figure 1 节点的三行文字连续、语义正确；并实际渲染、查看了 **第 5 页**的 Figure 1，确认新 RQ3 语句位于图框内，清晰完整、未剪切、未异常重叠。其局部排版符合本次编辑的最终视觉要求。
- 从先前 C8V [#39363725060](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39363725060) supplement artifact `12238108396` 中**实际**解压了 Supplement PDF，用 `pdfinfo` 确认 **47 页**。最新版本只修改 `main.tex` 图文字，补充材料原文未改变；最新 C8V 和 C7 的 complete-supplement jobs **均 SUCCESS**，但没有逐页人工翻阅最新 Supplement，不得声称已完成 47 页人工视觉逐页检查。
- 旧编译 logs 中较早 LaTeX pass 可能出现临时的 natbib/reference unresolved 警告，不能误报为 final PDF 引用错误；最终 CI 的 log guard 完成后无 fatal/undefined refs/overfull 错误。若作者另行要求高精度视觉整稿审阅，应使用最终投稿 PDF 单独进行。

## 4. 事实保护与提交边界

- 本轮始终维持 RQ1 Twitch 44,221/room 10,222，RQ2 M3 DEV 50,049 的探索性 switch，与 H1 30,000 同采集期冻结 policies，RQ3 H2 4096 嵌套三 seeds 的证据等级差异。
- 冻结结果仍为 H1 SAS F−S +0.005391 (CI [.003646,.007174])、GRU +0.003585 (CI [.001599,.005576])；natural calls 不等 1.337/1.797pp；Always Memory 更准，旧 Utility timing 不利；原 RQ3 prereveal TRAIN-only Popularity subgate **NOT VERIFIED**。本报告只验收编辑准确性，不复制私有事件或新计算上述效应。
- PDF 技术与语义守卫的 PASS 不证明严谨 matched-call label-only 因果效应、不证明 valid corrected-S 必败、不证明服务成本节省，也不证明创新性达到 KBS 要求。KBS 官方研究范围：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051；范围适配非录用承诺。

## 5. 阶段决定与 E6 移交

**E5 = PASS_FOR_FINAL_SCIENCE_SOURCE_AND_DUAL_PDF_CI / FIG1_MANUAL_VISUAL_CHECKED / SUPPLEMENT_47P_AUTOMATED_VERIFIED。**

当前 E0–E5 全部已完成。仍须由真人研究者对论文的 KBS 原创性、合理 sampled-only corrected-S 缺失、自然 calls 不同、无真实外部 quota/最新门控服务成本和 H2 prereveal 条件缺口给出独立书面评审；责任作者完成身份、CRediT、COI、资助、数据许可及实际 AI 参与披露与现行期刊 Guide 核验，并本人签署 GO/NO-GO。**E6 HUMAN REVIEW / AUTHOR GO PENDING；PR #6 保持 Draft；未投稿 KBS。**

当前论文工件须由获授权者在 2026-12-19 GitHub artifact 过期前合法转存长久档案，记录完整科学源码 SHA、私人实验的受限权利和校验信息。
