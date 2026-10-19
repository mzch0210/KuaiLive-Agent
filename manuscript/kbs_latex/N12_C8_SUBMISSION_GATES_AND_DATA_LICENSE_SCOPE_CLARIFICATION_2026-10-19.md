# N12-C8 | Submission readiness inventory and dataset-license scope correction

**2026-10-19, plan clarification following author feedback.** This note **supersedes the automatic dataset-license/owner-written-permission submission blocker** stated in older C7/C8 audit reports and the original 2026-10-19 amendment. It does not retrospectively rewrite historical audit findings, confer rights that are not held, or record author signoff. The research and submission state remains C0–C7 PASS, C8 referee simulation COMPLETE, C8 final signoff INCOMPLETE.

## A. 修正的政策：区分“公开数据集上开展研究并报告汇总结果”和“再分发数据”

- **DO NOT BLOCK submission merely because** the original KuaiLive and KuaiLive-M3 public metadata name different Creative Commons licenses, or because no additional dataset-owner written permission letter has been requested. Using properly accessed, publicly released datasets for research and publishing one's own aggregate analysis does not by itself entail republishing or redistributing the raw dataset. Record exact source, dataset release/version, link and attribution in the article/data statement to the extent known.
- **DO NOT automatically require public release** of private raw events, user identifiers, historical features, TEST targets, processed files or model checkpoints. Existing public scientific summaries/source checks and an accurate Data/Code Availability Statement can explain restricted access without inventing public end-to-end reproduction. The specific journal's live data policy must still be checked; Elsevier has multiple research-data options.
- **DO assess actual restrictions when relevant**, not treat every license as legally irrelevant. For example, a noncommercial license can limit commercial uses, ShareAlike constrains sharing covered adaptations, and private/confidential/user rights can be independent of copyright license. If concrete facts indicate the *research use itself* is unauthorized, violates access terms, or reveals protected personal data, escalate to the responsible author and institution instead of papering it over. This is a real rights/ethics exception, not an automatic gate triggered by competing license labels.
- **Publication-license metadata task: NONBLOCKING DOCUMENTATION** in the ordinary case of research results only, no prohibited redistribution and no identified rights/privacy breach. Written owner clearance for redistribution is needed only if authors choose to upload data/material for which their permission is insufficient; decline such upload rather than holding the paper indefinitely.

Official context:
- Elsevier research data journal-option policy: https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-guidelines
- Elsevier data license distinctions: https://www.elsevier.support/publishing/answer/which-license-should-i-select-when-posting-my-research-data
- Creative Commons BY-NC-SA 4.0 rights and conditions: https://creativecommons.org/licenses/by-nc-sa/4.0/
- Elsevier AI policy: https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals

## B. Latest C8 unfinished work, grouped by whether author action is necessary

| Priority | Unfinished deliverable | Current recorded state / required completion | Dependency |
| --- | --- | --- | --- |
| P0 | **Scientific manuscript Go/No-go** | C8 three-role referee simulation/major-comment matrix complete, but owner has not accepted residual originality risk (sampled metric + deferral combination), strict unequal-call H1 boundary, unverified prereveal H2 popularity floor and adverse Always-Memory cost evidence. Choose bounded empirical submission vs scientifically narrow/revise vs independently authorized new study; new experiments are **not required for a bounded submission**. | Human scientific judgment |
| P0 | **Author identity and approval** | `main.tex` still contains `\author{Anonymous Authors}`; author list/order, corresponding author, CRediT, final version approval not recorded. Use actual journal-required blinded or unblinded route; never invent names. | Human |
| P0 | **Mandatory declarations** | No verified journal-facing standalone AI manuscript-assistance declaration before bibliography; substantial ChatGPT-assisted organization and scientific text revision must be disclosed in language author validates. Funding, COI and data/code availability wording pending. AI used as part of actual research methods, if any, needs accurate Methods-level description; do not conflate with manuscript preparation. | Drafting can be prepared; human validation |
| P1 | **Submission package and live KBS guide** | Final guide-for-authors-specific requirements, cover letter, highlights format, mandatory submission files, reviewer/research ethics fields and supplementary file linkage are not recorded as fully checked. No evidence of actual KBS portal upload. | Check official instructions and create files; human submit |
| P1 | **Human PDF/source final read** | C7 36p/47p automatic science/table/citation/overfull tests PASS (49 numeric cells). Final 36p/47p author science, figure/table visual read and accurate declarations still need recorded review. | Human |
| NONBLOCKING | **Dataset license provenance** | Record which public data release/version was used and cite its landing page; optional metadata reconciliation. Neither mismatched labels nor absence of a separate owner letter alone should set NO-GO. Maintain actual user privacy and no impermissible raw/derivative redistribution. | Documentation only unless actual violation |
| OPTIONAL FUTURE WORK | **New independent equal-call/future-period/production-cost evidence** | Not performed, nor necessary to claim bounded frozen-policy evidence. Required only **if** author elects stronger causal, temporal-transfer or deployment-savings claims. | New separately sealed protocol if chosen |

## C. What is already complete (must not be reopened gratuitously)

- C0–C7 manuscript restructure, frozen source/equation/table mapping and dual-PDF science QA.
- C7 official CI #39205375045, both jobs SUCCESS, **36p main +47p full supplement**, 11 original Results tables accounted for, 7 main literal source tables retained, 4 supporting tables audited at 17 rows/49 numeric cells with negative mutation tests.
- C8 independent-role simulated editor, methodological and knowledge/deployment criticisms plus Major-comment response/location matrix **COMPLETE** (this is not actual external peer review).
- Frozen H1/H2 outcomes, no new TEST/training, same-period qualification, original H2 prereveal incomplete acceptance, higher Always-Memory rank accuracy and old pointwise timing disadvantage all remain visible.

## D. Decision rule

**C8 must not be marked PASS by an automated workflow**. A bounded empirical paper may proceed to actual journal submission once all required author declarations, real authorship/ethical accountability, verified submission-package fields and explicit author scientific Go decision are documented. A mismatch between public dataset license metadata, *without evidence of a violation in the actual research/publication use*, is **not independently a blocker**. No direct paper submission/PR merge is authorized by this clarification.

Current project state: **C8 reviewer simulation DONE; author approval and journal-facing submission materials PENDING; dataset metadata differences NONBLOCKING.**
