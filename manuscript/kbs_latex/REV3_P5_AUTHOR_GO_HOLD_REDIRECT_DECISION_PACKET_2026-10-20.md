# Rev3.0 P5 — KBS 责任作者决定书（仅预备资料，禁止 AI 代签）

**2026-10-20 | DECISION PACKET PREPARED / AUTHOR NOT APPROVED / NOT SUBMITTED / PR #6 DRAFT。**

> **2026-10-21 S3 verified update:** The 2026-10-20 snapshot below is retained as historical provenance; its former source SHA, 39-page figure and artifact expiry statements are **not** the current S1/S2 baseline. See section 4 for the latest verified status. External scholarly pre-review is **NOT REQUESTED**, not PASS. Responsible-author oversight and submission authorization remain PENDING.

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


## 4. S1–S3 去重续接与投稿准备增量记录（2026-10-21）

**状态：S1 源码修订 DONE；S2 当前 commit 双工作流 4 jobs SUCCESS；S3 客观核查及作者待办更新 DONE；投稿合规及责任作者 GO PENDING。** 此记录续接旧 P5，不设独立学者审稿、不新建 NI/DEV/TEST 科学路线、不替责任作者签字、不向投稿系统提交。该记录是科研及出版准备情况说明，不是期刊审稿或法律授权证明。

### 4.1 当前版本与真实 Actions 对应关系（旧 §1 快照已过期）

- Repo: `mzch0210/KuaiLive-Agent`; branch `kbs-n12-single-thesis-restructure-plan-20261014`; existing PR #6 remains **Draft** (not merged/not submitted).
- S1 commit **`c7678d347ed71aa8ea341d73f290a0eee8b16cdb`**, changes only `manuscript/kbs_latex/main.tex` in **seven narrative replacements**, with new title *Candidate-Regime Supervision for Selective Relationship Memory Use in Live-Streaming Recommendation*. Latest audited S1 LaTeX blob: **`98f045bb745341b7c6bae1b2da8f84defccf0e39`**. Rev3.2 W8 main-science blob `552586792cb80e0921a93c73868b4329d6e8b7ef` is the unchanged-before-S1 reference.
- Source-level old/new comparisons: **seven sections, nine main tables, eleven equation/align environments, fifty-five LaTeX label occurrences, and H1/H2 numerical source tokens remain unchanged**; S1 altered Title, abstract opening, Introduction bridge, three contribution headers and Conclusion opening only. No changes to Supplement, BibTeX, Highlights, trained models, frozen H1/H2 or private TEST.
- **C7 #39565629758** `https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39565629758` completed **SUCCESS**, main-paper and complete-supplement jobs both SUCCESS, `head_sha=c7678d3...`. Artifacts: `kbs-n12-c7-main` ID **12329323531**, `kbs-n12-c7-supplement` ID **12329419433**.
- **C8V #39565629809** `https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39565629809` completed **SUCCESS**, main-paper and complete-supplement jobs both SUCCESS, `head_sha=c7678d3...`. Artifacts: `kbs-n12-c8v-v0-main` ID **12329114474**, `kbs-n12-c8v-v0-supplement` ID **12330405274**. The artifacts were verified as **present and not expired in GitHub API metadata**, not binary-downloaded or visually page-by-page inspected in this S3 update.
- These **new** artifacts list expiry near **2026-12-20 07:58–08:00 UTC**. Archive through an authorized channel before expiry when legally permitted; neither the CI success nor metadata establishes rights to redistribute private training/TEST material. Rev3.2 W8's pre-S1 source was reported as 36-page main and 47-page Supplement; current S1 source rebuilt successfully, but **fresh page counts and per-page visual review have not been independently re-checked here**.
- Five unchanged Highlights have actual text character lengths **77, 78, 73, 61, 72** excluding Markdown/list markers; each meets the publicly documented general Elsevier 85-character convention. Confirm journal-specific upload form separately.

### 4.2 No external scholarly review by user choice; author responsibility remains distinct

- Original project-generated internal referee simulations and earlier source audits are not independent external peer review.
- **Independent outside scholarly pre-review: NOT REQUESTED BY USER; no review solicitation and no forged PASS.** This is a chosen optional project-quality activity, not an independently verified formal KBS submission prerequisite.
- **Responsible-author verification is still required** for originality judgment, scientific accuracy, authorship, permissions, declarations, data availability and actual approval. A decision not to seek external scholars cannot be used to assert the work is independently certified.

### 4.3 Official publishing guidance checked and outstanding KBS-specific information

- **Elsevier journal AI policy**, revised June 2026: `https://www.elsevier.com/en-au/about/policies-and-standards/generative-ai-policies-for-journals`. Substantive AI manuscript assistance should be documented in a separate declaration; AI used in study design, code/research methods or analysis requires reproducible Methods disclosure. Actual tool/provider/version, scope, verification and author acceptance must be factually confirmed. This project has records of substantial AI-assisted manuscript organization, argumentation, code/research planning and automated scientific auditing; it should **not** be described as spelling-only assistance.
- **Elsevier Highlights general guidance**, updated June 1, 2026: `https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript`: 3–5 bullets, each no more than 85 characters including spaces, usually a separate source file unless a journal Guide says otherwise. These are **generic**, not verified KBS-specific requirements.
- **Elsevier Data Statement guidance**: `https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-statement`: report actual access limits and check the target journal's policy; no blanket promise of raw data or checkpoint sharing.
- **KBS Guide for Authors**: `https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors`; the publicly queried Guide currently returns HTTP 403 in this access environment. Thus exact KBS abstract ceiling, anonymous review settings, highlights file requirements, declarations, and portal fields are **NOT VERIFIED**, and must be checked by the responsible author through a working official access path. The current `main.tex` still contains `\author{Anonymous Authors}`; no verified final author title page exists.
- Main LaTeX does **not** yet contain a separate `Declaration of generative AI ...` section, nor a verified completed data-availability, competing-interests or funding declaration. No such assertion should be inserted until factually approved.

### 4.4 Bounded author-owned submission items (do not auto-complete)

| Item | Exact outstanding action | State |
| --- | --- | --- |
| Scientific judgment | Confirm H1 is F versus original uncorrected S **complete fitted policies** with different observed call rates; NI1G corrected-S NO-GO, H2 original prereveal popularity gate NOT VERIFIED, Always Memory stronger and old gate slower; accept HIGH/CONTESTABLE originality risk or choose HOLD/REDIRECT | **AUTHOR PENDING** |
| AI manuscript declaration | Identify all AI services/models that actually contributed to drafting, reorganization, code and scientific audits; document human corrections and responsibility; supply final Elsevier-style declaration before references as applicable | **AUTHOR PENDING; NO AUTOMATIC INSERTION** |
| Research-method AI description | Identify AI involvement in research design, code development, statistical planning and evidence checks; confirm versions, reproducibility and proper methodological placement. AI-authored internal evaluation must not be labeled independent peer review | **AUTHOR PENDING** |
| Authorship and forms | True author names, affiliations, contributions/CRediT, correspondence, final author approval, COI, funding and required ethics statements | **AUTHOR PENDING** |
| Data and reproduction | Check KuaiLive/LiveRec/M3 original versions, license and privacy constraints, legal sharing/access procedures for restricted event data, checkpoints and derived artifacts; write truthful data/code availability | **AUTHOR PENDING** |
| Official KBS Guide | Access live Guide/portal to confirm anonymous/title page format, highlights upload, abstract limits, mandatory declarations and permissible files | **AUTHOR PENDING** |
| Archiving | Legally preserve new run artifacts, source commit, version details and accessible reproduction evidence before listed artifact expiry | **AUTHOR PENDING** |
| Formal submission | Authorized author selects conditional GO / HOLD / REDIRECT; keep PR #6 Draft and do not submit or change review state without explicit instruction | **AUTHOR PENDING** |

**Illustrative AI disclosure skeleton for verification only — NOT YET A SUBMISSION STATEMENT:**

> During the preparation of this work, the authors used [verified AI services and model versions] to assist with [verified literature synthesis, experimental planning, code development, source audits and substantive manuscript editing as actually applicable]. The authors [describe actually completed review, validation and revisions] and take full responsibility for the accuracy, originality and content of the submitted manuscript.

This skeleton must be edited to reflect the **true history**, with method-use details in Methods where applicable; do not automatically insert unsupported statements into `main.tex`.

### 4.5 Gate decisions

- **S1 PASS — precise editorial diff; S2 PASS — current commit/source-level checks and both PDF workflows SUCCESS.**
- **S3 CHECKLIST/EXTERNAL POLICY AUDIT COMPLETE, BUT HUMAN-OWNED SUBMISSION ITEMS STILL OPEN.**
- **No external independent scholarly review requested.** No extra NI/DEV/TEST experiments, method approvals, real-world cost claims, or new novelty certification.
- **Decision now: SUBMISSION HOLD_PENDING_AUTHOR**, while preserving pre-existing conditional GO/HOLD/REDIRECT options. This is administrative caution, **not** an automated rejection or a claim that the paper is scientifically invalid.



## 5. M1–M5 编辑评审建议的增量落实状态（2026-10-21）

- **M1 DONE** (commit `7628d07142dc6d802f75d2e1c49c586ede15931b`): the primary H1 Results now explicitly uses the previously frozen population-weighted realized specialist-call rates from Supplement Table S10.9: SASRec F/S 29.203%/30.537%, GRU4Rec 29.008%/30.809%; no frozen table, NDCG, CI, actual call count or TEST policy changed.
- **M2 DONE, scoped to documented facts** (commit `15e830166b0e45962cf9632f009f2fa45909eb3e`): distinguishes four user-disjoint DEV OOF threshold selection from the final full-DEV predictor fit and separate TEST realized invocation rates; original hypothetical invocation scarcity and negative old pointwise timing remain visible.
- **M1/M2 verified PASS** on same source SHA by C7 #39578302592 and C8V #39578302633, with both main and complete supplement jobs SUCCESS.
- **M3 focused editorial DONE** (commit `14cb33fa1edd8e90c2ea2a6f693d810c06ba203e`): abstract now refers to lower *population-weighted Memory-call fractions*, rather than using solely 401/539 raw sample call differences to summarize resource outcomes. The originally observed raw counts remain in Results and Supplement. Seven sections and primary scientific tables remain unchanged; no broad rewrite.
- **M4 public reproducibility index DONE** (commit `3b64437bc5b09b82f3b4239e2802933c597f4856`): see [REPRODUCIBILITY_MANIFEST.md](REPRODUCIBILITY_MANIFEST.md), linking existing claim-to-source and NI1G ledgers, precommitted population weights, score/replay scripts, original freeze and C7/C8V workflows, temporary artifacts, privacy and legal rights. All 27 relative documentation links were checked against the repository tree. This is an index, not a newly issued DOI or disclosure/rights signoff. Supplement was not shortened or stripped of scientific provenance.
- **M5 semantic guard updated** (commit `293d7e209fd45b1ca299748d1b9d7d8ea7170f46`): the existing C8V semantic checker now crosschecks four weighted percentages in main Results with Supplement S10.9 and checks the abstract, while retaining the prior frozen cohort, H1/H2 and negative-evidence guards. Associated CI must be checked for its actual outcome; a workflow dispatched for an earlier same-content source SHA must not be called final for a later changed audit script.
- **Final evidence verified:** C7 [#39579493919](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39579493919) on M3 abstract/source commit `14cb33fa1edd8e90c2ea2a6f693d810c06ba203e` and C8V [#39579562387](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39579562387) on updated scientific-audit commit `293d7e209fd45b1ca299748d1b9d7d8ea7170f46` each completed **SUCCESS** with main-paper and complete-supplement jobs both SUCCESS. The latter includes the former manuscript source plus the newer semantic audit; subsequent additions only concern the manifest and this P5 packet, which are outside the C7/C8V source triggers. A cancelled earlier C8V run is superseded, not a scientific failure.
- **M5 publication author tasks remain PENDING**: official KBS-specific Guide and anonymization rules, AI manuscript and methods declarations, real author/CRediT/COI/Funding/ethics, data owner rights, durable archiving, final author decision. Do not mark submission-ready or submit. External independent scholar pre-review stays NOT REQUESTED.
- **Scientific scope remains unchanged**: original uncorrected S comparator, natural unequal H1 calls, later-period replication absent, valid sampled-only corrected-S NO-GO, H2 original prereveal population subgate NOT VERIFIED, old pointwise gate slower than Always Memory and no evidenced production savings.

**Current decision: M1–M5 RELEVANT SCIENTIFIC CI SUCCESS; AUTHOR RIGHTS, DECLARATIONS AND GO/HOLD/REDIRECT PENDING; NO SUBMISSION.**
