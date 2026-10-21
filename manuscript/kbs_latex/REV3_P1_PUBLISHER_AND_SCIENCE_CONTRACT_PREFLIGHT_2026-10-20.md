# Rev3.0 P1 — 出版合规与主张一致性预审（2026-10-20）

**状态：AI-ASSISTED PREFLIGHT COMPLETE; AUTHOR-EXCLUSIVE VERIFICATION PENDING; NOT READY TO SUBMIT.**

## 1. 已核实事实

- 最新科学源小改：P0 新增AAAI2021、AAAI2023、WI-IAT2023的Related Work引用和BibTeX，其他论文段落/所有结果没有重新计算。
- 现稿 Abstract／Introduction／RQ2／Discussion 已明确：F相对原未经校正S的 frozen complete-policy比较；H1自然calls不相同（1.337/1.797个百分点），不是strict matched-call纯标签因果；Always Memory无外部cap时更准确；旧计时未证线上节约；H2为constrained composite null且一项original prereveal acceptance NOT VERIFIED；同DEV G2分解非独立TEST。当前未见必须重复追加这些边界的科学内容缺口。
- PR #6为Draft，责任作者尚未批准投稿；Rev2.2 E0–E5已完成，旧科学源码为36d9c3f2daed116061f12722db56448f371de60e，主文38p／Supplement47p。新参考文献修订需新C7/C8V QA，不能借用旧成功run为新源码验收。
- Elsevier生成式AI使用政策：https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals ；作者应核实论文写作、代码、研究设计、数据分析中实际AI参与环节及需要何种声明。不得擅自填写“仅语言润色”。
- KBS官方Guide：https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors ，公开页面当前访问限制；任何具体abstract/highlights字符、匿名方式、图摘要及投稿格式要求仍必须由获授权的责任作者在portal核验。

## 2. 尚未完成，AI不得代签

| 项目 | 状态 | 责任方与必要证据 |
| --- | --- | --- |
| 实际作者、隶属、通讯联系、CRediT贡献 | PENDING | 责任作者提供可核实身份和各自真实贡献 |
| 原数据/模型许可、隐私、可复现资产披露 | PENDING | 数据权利持有人确认公开/受限内容，不能上传私有事件 |
| Funding/COI/Ethics与数据可用性 | PENDING | 责任作者核实，不得编造资助/批号 |
| AI辅助写作与研究/代码/分析披露 | PENDING | 责任作者根据具体工作流记录逐项申报，与Elsevier适用政策一致 |
| 期刊当前Guide逐条条款 | PENDING | 授权者浏览官方页面、对摘要/Highlights/附件/作者列表实际核验 |
| 真实独立学者审阅 | NOT OBTAINED | 项目自定质量目标，非已经证明的KBS投稿法律/强制前置条件 |
| 最终GO/REDIRECT/HOLD和实际投稿 | NOT APPROVED | 唯一由责任作者执行 |

## 3. 工作边界与下一步

本轮完成的是事实核查和待核验事项列示，不包含真实作者声明，也未实施任何真实源数据上的新研究。后续P2仅检验新增3条参考文献的BibTeX解析、论文与Supplement双PDF、原科学语义守卫及相关页面可读性。若P2通过，P4可把“提交准备度提高”和“原创性没有被新科学证据证实提高”分别陈述；P5真实作者作GO决定仍阻断。
