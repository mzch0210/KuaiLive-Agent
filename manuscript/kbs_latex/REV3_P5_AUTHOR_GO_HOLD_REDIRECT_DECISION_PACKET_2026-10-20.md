# Rev3.0 P5 — KBS 责任作者决定书（仅预备资料，禁止 AI 代签）

**2026-10-20 | DECISION PACKET PREPARED / AUTHOR NOT APPROVED / NOT SUBMITTED / PR #6 DRAFT。**

## 1. 目前可直接确认的技术与科学事实

- 现行科学源码 commit `a686cd07ce80f8d4090aae720c0e583f39f73176`；最终C7 #39398148734/C8V #39398148731四项主文+Supplement jobs SUCCESS。已下载C8V PDF原件、核实主稿39页、Supplement47页、引用和第6/33页视觉。
- P0新增AAA I 2021、AAA I 2023、WI-IAT 2023、ACM TORS 2024、RecSys 2025先例，仅对Related Work/Discussion作必要差异化修订。没有调整主贡献、实验、表格或预算推断。参见 `REV3_P2_FINAL_SOURCE_PDF_AND_CITATION_QA_2026-10-20.md` 和 `REV3_P2_AND_P4_VERIFICATION_ADVERSARIAL_DECISION_2026-10-20.md`。
- RQ2的冻结比较只涉及 **full-F vs 原未经校正 sampled-S**的各自 complete-policy；新同期H1 30k样本 F质量更好且Memory调用更少，但非strict matched-calls标签唯一因果比较；有效corrected-S没试，NI-1g将该研究设为当前 NO-GO，不得私自重启。
- H2为4096嵌套历史复合随机化而非单一历史语义机制；一个原prereveal子门槛NOT VERIFIED。Always Memory无quota时更准、旧门控延迟更差，尚无真实最新gate服务节约证明；旧G5/H1已揭盲不得复用于新模型确认。
- KBS范围匹配；但“已知sampled-metric偏差+已知deferral/decision-focused”的组合解释仍是 **HIGH-CONTESTABLE** 核心原创性风险。文献补齐改善评审防御，不构成新独立原创性证明。无外部人类同行审稿（项目理想质量门，不是已确认的Elsevier/KBS强制项）。

## 2. 责任作者必须亲自确认（当前全部PENDING）

1. [ ] 从可访问的官方KBS Guide/投稿系统核实摘要篇幅上限（当前简单空格计数约272）、Highlights数量/字符和上传文件格式（当前5条、分别77/81/72/76/72字符）、匿名制度、图摘/补充文件、投稿形式；不能从一般Elsevier规格替代KBS具体条文。
2. [ ] 真实作者姓名/单位/通信邮箱与每位作者CRediT，取得所有作者真实批准；当前main.tex仍为Anonymous Authors，请依据KBS允许的投稿形式处理。
3. [ ] 研究数据/代码/checkpoint的权属、隐私、伦理和传播许可；私有记录不得自动公开，提供合法可复现路径。
4. [ ] 实际AI参与写作、方法设计、代码和科研审查的逐项披露，符合最新Elsevier policy；不得把上述活动谎称成“只做语言润色”。
5. [ ] Funding、competing interests、伦理和真实 data availability 与软件可用性声明，有证据才填写。
6. [ ] 合法归档科学源、C7/C8V主稿/Supplement工件与checksum，GitHub Actions artifact预计2026-12-19到期。
7. [ ] 作者亲自评价核心HIGH originality风险、未知sampled-only corrected-S反例、真实成本/独立未来时期的开放风险；如不愿承担，选择REDIRECT或HOLD。

## 3. 决策，不由AI自动选择或操作投稿

- **CONDITIONAL_GO_KBS**：以上作者合规和当前KBS Guide全部核实，作者有意识接受HIGH novelty risk，以bounded empirical paper投稿，严禁在cover letter夸大新算法/等调用因果/实际节约。只有作者有权改变PR Draft/实际向Elsevier投稿。
- **HOLD_FOR_NEW_EVIDENCE**：已落实合法独立新时期数据或独立可审方法，并符合NI-1g等准入，预注册后再开展P3 B/C；保持原稿冻结，设置真实STOP条件。
- **REDIRECT**：作者不接受核心原创性风险，且没有可行新数据/方法，改选更适合期刊并核实其独立Guide及要求。
- **STOP_NI**：仅有更多人工toy/反复DEV选择、不具可验证先验和新信息时，不再开展NI新的策略训练。

**当前状态：PACKET_READY_FOR_HUMAN_VERIFICATION_ONLY / AUTHOR GO NOT SIGNED / NO SUBMISSION.**