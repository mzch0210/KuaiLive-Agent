# Rev3.0 P2/P4 验证与原创性风险裁决（2026-10-20）

## 状态与证据等级

**第一轮 P2 已完成双工作流 SUCCESS + 下载 PDF 实物检查；随后 P4 两条引文修订需新科学源的二次 CI 复核。作者合规及 KBS 最终投稿仍 PENDING。**

P0 首次文献修订科学提交 `1b0fbe83686ab289dd350cd5a49e5868447e142a`：AAAI 2021 Jin 等、AAAI 2023 Li 等、WI-IAT 2023 Ihemelandu/Ekstrand已加入正文和BibTeX；当时 HEAD 的其他报告提交不改变这三篇科学引用。对应 Actions：C7 [#39396116259](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39396116259) 与 C8V [#39396116261](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39396116261)，均 completed/success，四个 main/supplement jobs 成功。C8V main artifact 12251863045、supplement artifact 12251956482，预计2026-12-19失效。

**实际下载并检查**上述 C8V ZIP 中 `main.pdf`、`supplementary_information_n9.pdf`：主稿从原 38页→**39页**（新增文献后的分页变化），Supplement仍**47页**。主文第6页新增文字连续，参考文献页包含Jin2021、Li2023、Ihemelandu2023的作者、页码和DOI；PDF可提取文本，未发现编译致命错误或 unresolved references。Github source检查31个被引用bib key均存在、Highlights五条长度72–81字符、abstract约272空格词（两者均非KBS已核准的投稿规格）。检查主文Related Work页面，不声称39页逐页人审；Supplement 47页通过CI且抽取确认，不声称逐页视觉审核。

## P4 新发现的 2024/2025 最近邻

新增对抗审查发现两篇有必要披露的直接近邻：
- Li, Jin, Liu, Ren, Gao, Liu，*On Item-Sampling Evaluation for Recommender System*, ACM Transactions on Recommender Systems 2(1), Article 7, 36p, 2024, DOI 10.1145/3629171。这是AAAI2021/2023系列的较新、完整系统处理，不能称rank-distribution/采样纠偏为本文算法新意。
- Pereira, Said, Santos，*On the Reliability of Sampling Strategies in Offline Recommender Evaluation*, RecSys 2025:360–369, DOI 10.1145/3705328.3748086；结合曝光偏差和采样策略研究离线模型比较的可靠性，提示单正例观测不能等同用户真实偏好/福利。

第二轮最小科学修改：`kbs_references.bib` commit `9a97f38985de4949830c623ea07d2ce287eecfa9`，`main.tex` commit `a686cd07ce80f8d4090aae720c0e583f39f73176`；新增两条BibTeX和**各一句**现有Related Work/Discussion语义边界，不改变 Abstract、Contributions、冻结结果、统计权重、Calls、Methods、Figures、Supplement或Highlights。**这些commit之后的新版 PDF 需要单独成功CI，不得用首次1b0fbe8的P2成功run代替。**

## P4 对抗审稿裁决

| 最强反方 | 现稿允许的回应 | 严重度和剩余事实 |
| --- | --- | --- |
| KDD2020+AAAI2021/2023+TORS2024 已知sampled偏差，ICML2024已知deferral；只是组合 | N12的限定经验对象是固定历史Memory相对固定Base的candidate-regime训练标签，DEV具体调用换位和额外同期冻结完整政策表现；不发明采样估计或deferral理论 | **NOVELTY HIGH-CONTESTABLE**，表述修复不消除方法缺口 |
| 原 S 575是未校正弱对照 | 已明确S为事后target-retained、Adapted需F监督；NI-1g不批准当前真实 corrected-S训练 | **OPEN HIGH**，不能推论合理sampled-only correction失败 |
| H1 natural call差 1.337/1.797pp >1pp预设容差 | 仅比较冻结complete policies，F两组观察点质量较高且Memory调用较少；不是严格同调用或标签单因子效应 | **OPEN HIGH**，不得将质量加权量与未加权calls直接推成经济证明 |
| 六fits/G2/H1/H2都“独立重复” | 六fits共享G5 TEST；G2是同DEV描述；H1新ID同采集期可能用户重叠；H2嵌套4096+3seed同群体 | **ALREADY DISCLOSED** |
| H2是关系语义因果机制 | composite rewiring改变重复/高阶结构，一项TRAIN-only Popularity prereveal子门槛NOT VERIFIED，已修Figure 1 | **OPEN DISCLOSED** |
| Conditional access真的节省生产算力？ | Always Memory未受cap下更准，旧pointwise gate更慢，新gate未测；现稿仅考虑外部quota可能性 | **OPEN HIGH REAL-WORLD** |
| 论文原创性/发布合规已经成功了吗？ | 文献引用更全、源可复现、双 CI验收只能提高科学表述准确性；Elsevier AI政策/许可/作者身份/Guide核验未完成 | **SUBMISSION BLOCKED UNTIL HUMAN AUTHORIZATION** |

## P4决策与下一步

**P4 SCIENTIFIC AUDIT COMPLETE / CONTRIBUTION DELTA = precise novel-prior-art boundary and explicit logging bias only; NEW INDEPENDENT SCIENTIFIC EVIDENCE = NONE.** 无新增同预算估计、合法 corrected-S 比较、时期外推或服务收益证明。Novelty风险仍HIGH；此前NI-1g V2b NO-GO、NI-2/3未授权，绝不触碰G5/H1已揭盲TEST。

**P2两阶段状态**：首次科学sha 1b0fbe8已有C7/C8V及实物PASS；最终科学sha a686cd07尚须其自身C7/C8V真实SUCCESS/工件及PDF验证。新的后续CI报告需以这个准确SHA为准。

**P5** 仅由责任作者决定：完成KBS官方Guide、本人的真实身份/CRediT/COI/funding、数据许可证和AI研究/写作参与披露后，可选择有边界KBS投稿并接受较高风险，或若有新合法数据/方法再预注册科学验证，或REDIRECT。真实独立学者预审仍PENDING但并非已证KBS强制要求。PR #6保持Draft；绝不自动投稿。
