# N12 Rev3.0 P2 最终引文版科研源、PDF 与引用验收

**2026-10-20 | P2 FINAL PASS: C7/C8V BOTH SUCCESS / FINAL-PDF DOWNLOADED / SPECIFIC PAGES VISUALLY CHECKED / SOURCE-STATS-UNCHANGED / KBS NOVELTY STILL HIGH-CONTESTABLE.**

## 1. 严格匹配的科学源与执行层级

- Repo: `mzch0210/KuaiLive-Agent`; branch `kbs-n12-single-thesis-restructure-plan-20261014`。Rev3.0 FINAL SCIENCE COMMIT **`a686cd07ce80f8d4090aae720c0e583f39f73176`**，后续 P4 内部报告等治理提交不产生新PDF科学源。当前 `main.tex` Git blob `e5043a2fae305cfcdca49fefa3650732c927d1a4`；`kbs_references.bib` blob `a65ddd7eba40e24663891dc5d28cb83f65519fe1`。
- 和此前E5 `36d9c3f2...`的区别仅为新增五篇已核验出版先例、最小Related Work/Discussion辅助说明。**不改变**Abstract、Introduction三项贡献、方法/模型、DEV/TEST排名结果、置信区间、call counts、H2历史Null、Figures、Highlights或Supplement。原E0–E5保持DONE；NI-1g METHOD NO-GO、V2b NOT_RUN_BY_DESIGN、NI-2/3 NOT_AUTHORIZED保持。
- 原首轮P0引文版 `1b0fbe83...` 的CI #39396116259/#39396116261曾成功；**不得**把它误当最终版QA。最终版两条Actions分别为 **C7 [#39398148734](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39398148734)**、**C8V [#39398148731](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39398148731)**，均 completed/success，且各自main-paper和complete-supplement两个jobs均SUCCESS，执行的科学源SHA皆是 `a686cd07...`。早期 `9a97f389...` 仅bib修订的C8V #39398094055后来被cancelled；最终版SUCCESS已覆盖，不把已cancelled误记为FAIL。

## 2. 最终实际工件（ZIP DIGEST与原PDF SHA必须区分）

| Workflow | Artifact | Artifact ID | ZIP SHA256 digest（GitHub） | 截止 |
| --- | --- | ---: | --- | --- |
| C8V | main PDF archive | 12253306410 | `89c54a993c561af03a026e560a851d3b38dca8b8c00fedfb26b63528d8946437` | 2026-12-19 09:08:26 UTC |
| C8V | Supplement archive | 12253496119 | `723b6e9c761ac54ba2014f70bf6cd4fb40eaccf3237c2ccca2639e0305eca3f7` | 2026-12-19 09:09:29 UTC |
| C7 | main PDF archive | 12252732237 | `b9699025bf84c5fb6e42558f15f564b579e7755c3549013a7093a237ae32ec04` | 2026-12-19 09:07:25 UTC |
| C7 | Supplement archive | 12252762287 | `c0d3c036d3d590fe77cbe86384a6e7526a1422414406a7fdc0721b6fccfaa877` | 2026-12-19 09:07:50 UTC |

实际使用GitHub连接下载并解压C8V主文 ZIP 与 Supplement ZIP，检查 `main.pdf` **39页**（555,658 bytes）及 `supplementary_information_n9.pdf` **47页**（239,815 bytes）。两份PDF原件的本地文件 SHA256：

- `main.pdf`: `6e4cc4c13ed807f8806357461293e11c50af026ad8e8bc224fe27e3464c30fdc`
- `supplementary_information_n9.pdf`: `9b87587f0fea03258b91cc8da2d0c1645da71d0d83676e0827d3ec5449dca82a`

即当前主文由旧38p自然扩展至39p（文献增加的分页变化），Supplement保持47p；无根据声称KBS已经核准39页长度。主文pdftotext包含 2021/2023 AAAI、2023 WI-IAT、2024 TORS、2025 RecSys新增先例，已对**第6页 Related Work**与**第33页 Discussion/Conclusion边界**分别渲染并人工目视确认文字清晰、无明显框外溢出/剪切；本地编译日志搜索未发现 undefined citations/references、fatal或 overfull hbox。**没有**逐页人工复核全部39+47页，不可夸称完成全页视觉检查。

## 3. 静态文献、前端与缺口检查

- GitHub `main.tex`含33个去重 `\cite` keys；`kbs_references.bib`有42个条目且不存在重复key；33个被引用的key均存在，五项新增 `jin2021sampledeval`、`li2023reliable`、`ihemelandu2023candidatesampling`、`li2024itemsampling`、`pereira2025samplingreliability` 都同时存在于源与PDF。确保“引用已列”不等于已经全文复核了每篇相关数学定理。
- `Highlights.txt`共5条，长度77/81/72/76/72字符，符合Elsevier**通用**3–5条/每条<=85字符说明，https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript 。是否KBS专属要求、是否需单独Word格式仍以当前KBS portal为准；项目当前是纯文本文件，作者需核准上传格式。
- `main.tex` Abstract用简单空格分词约272词，**不是当前KBS官方已核准上限**。通用Elsevier材料不能用于宣称KBS要求250词；投稿前应核准专属Guide，如上限低于该字数，应进行保留所有核心负面边界的最小缩写并再次构建。当前暂不主动改。
- 当前没有自动生成/签署真实作者、许可证、AI使用声明、COI、CRediT或数据访问方式；真实性属于 P1 作者审批。Elsevier June 2026官方AI政策要求实质性AI写作披露、方法研究中的AI参与Methods披露：https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals 。不能由于CI SUCCESS将P1作者项改为完成。

## 4. 科学与投稿结论

**P2 FINAL SCIENTIFIC QA = PASS**，唯一完成的是“最近邻先例补全后主稿可构建、引用/PDF准确、冻结统计没被修改”；没有新增独立科学证据，也没有纠正S的合格现实训练方法，故核心KBS原创性仍是HIGH-CONTESTABLE。

**P4 ADVERSARIAL NOVELTY AUDIT = ALREADY DONE**，参见 `REV3_P2_AND_P4_VERIFICATION_ADVERSARIAL_DECISION_2026-10-20.md`。不再重复改写段落或反复添同义文献；下一阶段交接P5为有条件的人类责任作者GO/REDIRECT/HOLD选择，PR #6仍Draft，未真实投稿；P3-A/B/C研究都须实际权限、信息/资源合同和相应准入，不自动启动。所有暂存于Actions的C7/C8V工件在预计2026-12-19到期前须由有权人员合法长期保存。
