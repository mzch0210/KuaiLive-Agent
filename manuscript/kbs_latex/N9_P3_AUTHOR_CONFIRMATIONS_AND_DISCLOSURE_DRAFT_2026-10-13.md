# N9-P3 — Author confirmations and publishing disclosures (NOT YET ATTESTED)

**Date:** 13 October 2026. **Submission status: HOLD.** This document is a preparation aid, **not** an author-signed declaration, IRB determination, copyright clearance or statement that particular human checks have already occurred. The corresponding authors must verify each field, document evidence and approve final wording.

## 1. Generative AI and research-code assistance

Elsevier's journal policy (updated 2026) requires a separate declaration immediately before references for substantive AI-assisted manuscript preparation. Its stated requirements are tool identity, purpose, author review and ultimate human responsibility. If generative AI helped write or edit **research code, methods or analyses**, its role must additionally be disclosed in the Methods section with reproducibility details. Spelling-only/grammar-only assistance is exempt; substantive drafting is not.

Relevant source: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals .

### Proposed disclosure for author review — do NOT paste into final paper without verification

> **Declaration of generative AI and AI-assisted technologies in the manuscript preparation process.**
>
> During preparation of this manuscript, the authors used ChatGPT (OpenAI; verify exact version and relevant dates) to assist with [describe actual use, e.g., structure editing, literature screening, English-language revision, and formatting]. [The authors must confirm which outputs were reviewed, what factual and bibliographic checks were completed, and what editorial changes they approved.] The authors remain fully responsible for the accuracy, originality and integrity of the submitted manuscript.

**Research methods/code sentence for review (only if factually accurate):**

> AI-assisted tools supported [specify actual scripts or aspects of experimental workflow/code drafting, test generation or analysis documentation]. All datasets, fixed event/candidate regimes, source manifests, code versions, trained model weights, numerical results and reproducibility checks were validated according to the reported experimental protocol by [identify actual human validators]; no model-generated data replaced measured event outcomes.

Do **not** use phrases such as "all results manually audited" or "all bibliographic entries verified" unless the responsible authors have performed and documented those actions. Keep a private use log, version IDs and verification trace.

## 2. Data license and privacy clearance

**Original KuaiLive repository:** https://github.com/imgkkk574/KuaiLive — advertises CC BY-NC-SA 4.0 for that work. The exact data release may have additional terms. Confirm Zenodo record's license and version.

**KuaiLive-M3:** https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3/tree/main — current dataset card advertises `cc-by-sa-4.0`. Confirm dataset card metadata and whether the particular versions of `live_interaction`, `live_room_meta`, authors and training files used in the paper fall under the same license.

**Twitch LiveRec:** https://github.com/JRappaz/liverec — official repository documents dataset source, anonymized users, and the research use. Confirm the precise redistribution rights of the derived Twitch working copy; do not assume public download means unlimited relicensing.

Before release/publication, review attribution, noncommercial/sharealike restrictions, dataset-specific privacy terms, derivative score/checkpoint redistribution, and whether the GitHub project contains or would contain prohibited user/event identifiers. Original public datasets, project analysis code, private run caches and human-generated manuscripts need not share one license.

## 3. Authors' accountable decisions

| Required item | Responsible person | Evidence / status |
| --- | --- | --- |
| Confirm complete list of actual human authors and affiliations | Authors | PENDING |
| CRediT contributions and approval of final version by each author | Authors | PENDING |
| Funding and conflict-of-interest statements | Authors | PENDING |
| Human-subjects / institution research-ethics status, if applicable | Institution / authors | PENDING |
| Exact dataset license(s), release versions and permitted outputs | Authors / data steward | PENDING |
| AI-assisted writing and code-method disclosure accuracy | Authors | PENDING |
| Numerical tables, statistical claims, references, supplementary coherence | Authors and independent checker | PENDING |
| Repository, code release, model checkpoint and private-data sharing plan | Authors | PENDING |
| KBS cover letter, highlights and publication declarations | Corresponding author | PENDING |
| Submission go/no-go and independent TEST eligibility | Authors | HOLD |

## 4. Scientific claim wording for cover letter after approval

The paper investigates the **relative ranking value of an explicit, fixed viewer–creator relationship knowledge source**, conditional on the incumbent and time-varying candidate regime. It connects paired candidate evaluation with development-only tests of how supervision mismatch changes downstream knowledge-use decisions, complementing independently frozen Twitch and M3 specialist-allocation TEST results. The method is a decision-support **valuation and assessment framework**, not a newly invented universal expert-routing algorithm. Its selective deployment implications are conditioned on actual specialist access constraints.

This paragraph is **draft language**, not a final statement that all experiments or journals have approved the method. It should not imply independently new confirmation of B1/B2/A1/A2.

## 5. What cannot be certified by the assistant

Human review, dataset redistribution permission, CRediT statements, actual AI-use completeness, final ethics determinations, missing full per-candidate score vectors for A2 fusion, and a new unexamined holdout cannot be inferred from GitHub Actions SUCCESS or current text. The manuscript remains on submission HOLD pending accountable author decisions.
