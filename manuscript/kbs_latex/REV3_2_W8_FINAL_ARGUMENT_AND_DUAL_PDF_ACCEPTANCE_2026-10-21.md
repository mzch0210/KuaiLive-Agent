# N12 Rev3.2 / W8 — Final Editorial Coherence and Dual-PDF Evidence Acceptance

**2026-10-21 | REV3.2 TECHNICAL FINAL PASS + INTERNAL EDITORIAL READABILITY PASS / EXTERNAL HUMAN ACADEMIC REVIEW PENDING / RESPONSIBLE-AUTHOR KBS SUBMISSION APPROVAL PENDING.**

## 1. Exact final source and independently retrieved build evidence

Repository \`mzch0210/KuaiLive-Agent\`, branch \`kbs-n12-single-thesis-restructure-plan-20261014\`, final audited HEAD **\`ffe204f376c4f1fd602f053e4a13223e775b15ed\`**. This is a test-fixture update after the last paper-science-edit commit **\`dc5f265c3b86081fcddfc49a3ab4a436061ac926\`**. The exact last Git blobs are:
- \`manuscript/kbs_latex/main.tex\`: **\`552586792cb80e0921a93c73868b4329d6e8b7ef\`**;
- \`SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md\`: **\`baa6f7c9d3ca1bff1403edeccda3bf97ed24da08\`**;
- \`Highlights.txt\`: **\`785ec3f63914d5fc4485f18338405038fef5e920\`**;
- \`kbs_references.bib\`: **\`a65ddd7eba40e24663891dc5d28cb83f65519fe1\`** (unchanged from Rev3.0).

Final runs:
- **C7 #39535398483**, head_sha \`dc5f265c3b86081fcddfc49a3ab4a436061ac926\`, main-paper SUCCESS, complete-supplement SUCCESS: https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39535398483 .
- **C8V #39535426937**, head_sha \`ffe204f376c4f1fd602f053e4a13223e775b15ed\`, main-paper SUCCESS, complete-supplement SUCCESS: https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39535426937 .
- C7's main source blob and C8V's main source blob are identical; the intermediate change affected only the C8V mutation-test text, not the paper or Supplement. Prior failed W7 runs #39534304945/#39534304944 are genuine historical failures (overfull and obsolete regression fixture), **not** the final validation status.

Official GitHub-generated C8V artifacts downloaded and ZIP-unpacked for direct local document verification:
- main artifact **12317183727**, GitHub ZIP digest \`sha256:b1a1ebd0ab504d93e9a8b9fab7ae4e06063f8890d6ac7dd269fe8b55dfe8fd05\`, ZIP expiry ~2026-12-20;
- Supplement artifact **12316969134**, GitHub ZIP digest \`sha256:d869cd6831b3b5ac5af3fa4619788342a351d19c78cc4e2447d711ccc9c6bf4f\`, ZIP expiry ~2026-12-20.
- **Extracted PDF file SHA256**: \`main.pdf\` **\`6abfb82d1406c6ee941d9e0613d6b50426c8e89c2da2eda633daca0effd4aaff\`** (547856 bytes, 36 pages); \`supplementary_information_n9.pdf\` **\`55cb7c52c27fb2e937a49395b3a3522d49f6dff1d7446a4a11262f526c10cfd8\`** (240430 bytes, 47 pages). Distinguish ZIP digest from inner-PDF SHA256.
- Main and supplement were rendered on selected representative pages; visual inspection covered main pages 1,2,3,6,19–26,32,35–36 and Supplement pages 1,2,17,33,34,42,44–47. No obvious clipped text, table cropping or layout break observed on those pages. **Not a claim that all 36+47 pages received page-by-page independent visual proofread.** Main \`main.log\` has no \`Overfull \hbox\`, fatal LaTeX errors or unresolved reference/citation messages; both PDFs have searchable text.

## 2. Scientific facts: source-of-record regression versus Rev3.0

Compared to frozen prior-science commit **\`a686cd07ce80f8d4090aae720c0e583f39f73176\`**:
- main manuscript **all 9 \`table\` source environments byte-identical**, including the seven Results tables;
- **all 11 \`equation\` / \`align\` mathematical environments byte-identical**;
- all **53 old \`\\label\` identifiers preserved**, plus just two new legitimate Result section labels \`sec:results-allocation\` and \`sec:results-selection-context\`; no duplicates;
- all **33 previously cited BibTeX keys retained**; no undefined \`\\ref\`/ \`\\eqref\` targets in main source.
- Supplement **all S10.1–S10.19 numbered headings preserved**, total Markdown table rows unchanged (**364**); 24 blob/main GitHub links found and all linked repository file paths exist in the audited current branch. Important: successful repository link resolution does not prove an expiring GitHub Action artifact remains available in the future.
- main paper 36 pages after editing (Rev3.0 was 39), Supplement still 47 pages. **Page reduction reflects editorial reflow; the rigorous evidence guarantee is exact source table/math preservation, not page count.**

Core truth anchors checked in source and/or final extracted PDF:
- RQ1 KuaiLive **room** paired 10,222: sampled-relative \`-0.04120\` vs full-active \`+0.04631\`; not same policy training.
- M3 DEV 50,049 with G2 policy disagreement SAS 10,672 (21.32%) and GRU 11,517 (23.01%). DEV retrospective description, not H1 mediator or new TEST.
- frozen H1 same-period 30,000 **author** targets: F over original uncorrected S SAS NDCG \`+0.005391\` CI [.003646,.007174] with F/S calls 8704/9105; GRU \`+0.003585\` CI [.001599,.005576] with F/S calls 8629/9168. F/S naturally realized calls **not strictly equal** (1.337/1.797 percentage points difference); no single-factor causal attribution to label.
- H2 nested 4096: authentic 0.334942 vs constrained-composite null mean 0.303797, difference +0.031145 CI [.027389,.035098]; original same-cohort TRAIN-only Popularity prereveal acceptability check **NOT VERIFIED**; no post-hoc validation replacement.
- Always Memory higher unconstrained ranking performance (0.348744) and prior warmed old-pointwise gate slower (1.76941 ms vs Always Memory 0.69165 ms); do not infer production cost savings or claim new vectorized gate was timed.
- NI-1g corrected-S real sampled-only method NO-GO and Rev3.1 Big→Small KuaiRec external historical Memory NO-GO remain intact; no new scientific experiment, re-estimation, or TEST reuse.

## 3. Internal first-read academic coherence check

**PASS, scoped to model-authored internal academic editorial review, not an independent human peer-review report.**

- Introduction now progresses bounded histories → complementary viewer–creator relationships → value relative to incumbent → candidate-dependent supervision → specific request-level gate consequences. It defines one question before discussing evidence.
- Related Work connects three established literatures with the additional observed empirical target; it does not claim invention of generic ranking sampling correction or deferral.
- Method and Design distinguish realized offline \`\\Delta_r\`, conditional pretarget \`\\eta_r(Z)\`, fixed sources, policy thresholds, and outcome-dependent diagnostic states. 30k frozen experiment is described before retrospective controls and H2 remains parallel.
- Results §§5.1–5.6 are readable in the order context → **primary H1 on main PDF page 21** → **G2 DEV allocation on page 22** → supporting frozen original selector evidence → **H2 on page 25** → measured operating conditions. The older six fits are still correctly based on shared original TEST.
- Discussion interprets candidate-relative supervision as a selective-knowledge-use design contract and places weak S / non-equal calls / incomplete H2 original acceptance / exposure / real-cost evidence in appropriately discoverable concentrated sections. Conclusion closes with a scoped positive claim and future discriminating tests.
- Supplement evidence map now locates S10.1–14 DEV, S10.15 H1, S10.16/18 H2, S10.17 timing, S10.19 full supporting tables. Obsolete S1–S9 and incorrect Results section cross-reference corrected. The 47-page Supplement still includes substantial detailed provenance; additional trimming is **not justified merely by page count**, and any submission-specific limit is a human KBS Guide question.
- Abstract simple whitespace-word count **211**, Highlights **5 entries of length 77/78/73/61/72**. Elsevier general guidance is 3–5 highlights each ≤85 characters, usually separately supplied in editable Word format unless Guide otherwise specifies: https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript . **KBS-specific current abstract and uploaded artifact format not yet verified**.

Residual editorial observations before actual submission:
- The title foregrounds relationship Memory as the question, while the final empirically discriminating result foregrounds candidate-aligned supervision. The introduction bridges the two; either title may be defensible. Any title change now must be deliberate, not a reflexive additional rewrite.
- \`Anonymous Authors\` remains the manuscript attribution and PDF metadata. Whether anonymity is permitted for this KBS submission type and final real author/Credit information must be decided by authors, not guessed.
- No verified independent external human field-review, actual author-approved contribution/affiliation/COI/funding/data-license/ethics/AI-research-methods disclosure, KBS current portal Guide checks, or author-signed final GO. These are **not** implied by W8 PASS.

## 4. Acceptance decision and remaining human-owned gate

- **W0–W7 editorial/source stages: DONE.**
- **W8 technical two-pipeline + artifact + science source QA: PASS.**
- **W8 internal read-through academic coherence QA: PASS, with scoped review and limited PDF page sampling.**
- **External human scholarly opinion + P5 legal/contributor/editorial author approval: PENDING.**
- **KBS status: NOT SUBMITTED**, PR #6 remains Draft.
- **Originality: HIGH-CONTESTABLE**, still relies on original uncorrected S comparison, not proven best corrected-S, and no future-period or actual resource savings. W8 improves accurate intelligibility; it does not create new science or a statistical KBS acceptance probability.

**Final disposition: REV3.2 EDITORIAL/C7/C8V TECHNICAL CLOSEOUT / READY FOR RESPONSIBLE-AUTHOR AND INDEPENDENT SCHOLARLY REVIEW / DO NOT SUBMIT AUTOMATICALLY.** Preserve the GitHub workflow archives before their expiration if legally permitted. Any subsequent actual scientific source edits must re-run the real C7/C8V and PDF evidence acceptance; test-fixture-only edits need relevant tests, not gratuitous full manuscript rewrites.
