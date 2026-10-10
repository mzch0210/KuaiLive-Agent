# KBS reviewer-style tightening — Discussion §7.3 (2026-10-10)

**Manuscript:** *When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation*  
**Section:** §7.3, *From Relative Utility to Selective Decisions*  
**Accepted manuscript source:** [main.tex](main.tex)  
**Scoped tightening commit:** [e8bec689](https://github.com/mzch0210/KuaiLive-Agent/commit/e8bec68935b63b8f6c15814cf73ae9fe911ddc52)  
**Pre-tightening first draft:** [3615a0a](https://github.com/mzch0210/KuaiLive-Agent/commit/3615a0a2542bfe497013efb2cb83ed20296b0caa)  
**Authority:** [independently optimized §7 plan](SECTION7_KBS_DISCUSSION_WRITING_PLAN_2026-10-10.md); §3 conditional-gain identity; frozen §6.2 Twitch selector evidence; DEV-only §6.4 feature-family ablation; [prior source-provenance audit](SECTION7_3_FIRST_DRAFT_SOURCE_AUDIT_2026-10-10.md).

## Independent referee verdict

**Accept subject to scoped wording and cross-subsection tightening; no new experiment, method or hypothesis is necessary for the approved C1–C3 claims.** The first draft was numerically correct and appropriately bounded, but its argument could be read as rediscovering a known deferral objective and repeating the preceding Results. The revision changes the *scientific exposition*, not the empirical estimands, evidence or claims.

| Priority | Independent referee issue | Concrete source revision and criterion |
|---|---|---|
| P1 | **7.1/7.2 → 7.3 bridge:** the first paragraph reintroduced the relative-utility equation but did not explicitly connect the history- and candidate-dependence findings to the proposed choice rule | Open with direct cross-references to §7.1 and §7.2 and emphasize that selection evaluates the *alternative ranking within the current candidate regime*, not incumbent difficulty alone; Eq. (expected selective gain) now serves as the concise inference link, not new theory |
| P1 | **Nearest-neighbor novelty:** the first draft risked implying that prediction of Base-relative advantage for expert choice was entirely new | State explicitly that Learning-to-Defer already studies allocating requests to existing predictors and experts; cite the *final published versions* of Mozannar and Sontag (ICML 2020) and Narasimhan et al. (NeurIPS 2022); differentiate from GUIDER (AAAI 2026), whose uncertainty-based LLM reranking adjusts a different adaptation signal |
| P1 | **Comparator information structure:** a matched call count is not equal deployment access: Difficulty used top-m ranking of the examined TEST batch and obtained m from Utility’s realized count | Attribute the result to superior **which-events** selection at the observed m=6,650; distinguish the DEV-frozen Utility pointwise threshold from the retrospectively matched Difficulty batch control |
| P2 | **RESULTS duplication / independent evidence:** §6.2 already contains the full result table and selected-mask figures | Retain just two signed gain estimates (+0.00772, +0.00644) and two descriptive mask means (+0.05136, −0.05890), and make the latter explanatory rather than a separate confirmation |
| P2 | **Mechanistic DEV evidence:** the first draft did not use the complementary feature-family evidence for why the predictor can differentiate relative utility | Add a single reference to §6.4’s DEV-only ablation: combined history + Base-score descriptors outperform either family individually at the original matched DEV count; no TEST ablation or new statistical independence is asserted |
| P2 | **Prediction vs policy value:** positive NDCG gain with modest per-event rank correlation can be misread as calibrated or near-Oracle routing | Keep TEST Spearman 0.173 and only 11.7% of the *same-count hindsight Oracle over Base* gain; explicitly limit the policy finding to the frozen Twitch regime |
| P2 | **Academic rhetoric:** avoid a process audit, serial negations, future-tense promises or new broad algorithm claims in published prose | Three linked paragraphs, no new table, no first/only novelty rhetoric, no retuning; scientific assertion followed by source-grounded evidence and bounded interpretation |

## Evidence and formal-publication audit

1. **Decision identity:** §3 Eq. \`eq:expected-selective-gain\` exactly states \(\mathbb{E}[a(Z)\eta_r(Z)\mid R=r]\) for pre-outcome \(Z\) and fixed \(r\). §7.3 does not promote this identity to a novel theorem, assert optimality for the DEV-frozen \(\tau_r\), or use target-conditioned states as features.
2. **Frozen Twitch TEST:** \(n=44{,}221\) events, \(m=6{,}650\); Utility–Base NDCG@10 **+0.00772** (95% paired CI **[+0.00641,+0.00903]**) and Utility–Difficulty **+0.00644** (95% paired CI **[+0.00528,+0.00762]**). The confidence intervals and TEST table remain in §6.2 rather than being repeated here.
3. **Realized Utility-selected masks:** Memory–Base average **+0.05136** in selected requests and **−0.05890** in unselected; conditional descriptive means from the same frozen TEST sample, not post-selection causal estimates. A different Difficulty selection at the same retrospective count produces +0.00855; §6.2 carries full comparison.
4. **Independent DEV evidence within study:** §6.4 reports five-fold OOF DEV-only gains +0.00372 (history 6 features), +0.00160 (Base 8 features) and +0.00838 (combined 14). These are in-sample development diagnostics with finite-grid/OOF qualification, not newly acquired TEST.
5. **Known prior art — verified publisher records:** Mozannar & Sontag, [*Consistent Estimators for Learning to Defer to an Expert*, ICML 2020 (PMLR 119:7076–7087)](https://proceedings.mlr.press/v119/mozannar20b.html); Narasimhan et al., [*Post-hoc estimators for learning to defer to an expert*, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html); Xu et al., [*GUIDER: Uncertainty Guided Dynamic Re-ranking for Large Language Models Based Recommender Systems*, AAAI 2026, 40(19):16049–16057](https://doi.org/10.1609/aaai.v40i19.38639). These records are formal proceedings, not arXiv versions.
6. **Prediction boundary:** TEST Spearman **0.173** is rank concordance of predicted and realized relative utility, not per-event gain calibration; approximately **11.7%** of the same-count hindsight Oracle headroom is recovered by Utility. No KuaiLive or cross-regime frozen gate policy is inferred.
7. **Numerical inference boundary:** A user-paired TEST bootstrap quantifies observed Utility-vs-Base and Utility-vs-matched-Difficulty mean differences, not external-dataset transfer or zero-shot adaptation. No inference is made from DEV subgroup labels to serving labels.

## Exact-source quality gates

- **Source-scope check passed:** only the §7.3 span between its subsection heading and the bibliography marker was replaced. Previously accepted §§7.1–7.2, all numbered sections, the formal equations, table numbers and figures remain byte-identical.
- **Static manuscript checks passed:** all 28 unique manuscript citation keys exist in the same 29-record BibTeX database; no duplicate LaTeX labels or undefined \`ref\`/\`eqref\` keys detected in source.
- **Rendered PDF / workflow:** the push to \`main.tex\` automatically triggers the repository’s KBS LaTeX GitHub Action. Record final job conclusion and artifact ID here only after checking the workflow for commit \`e8bec689\`.
- **Accepted claim:** the KBS contribution is *evidence-specific specialist-relative ranking valuation and held-out selection*, not a new universal deferral algorithm, generic uncertainty-control strategy, candidate-count causal intervention or deployable speed-up.
- **Next independent gate:** §7.4 should organize evidence validity (frozen Twitch vs post-hoc KuaiLive; retrospective vs pre-outcome; actual CPU overhead/transfer), without reopening settled §7.3 claims or moving additional TEST exploratory findings into the original frozen policy.
