# N12-C3 — Knowledge Valuation and Selective Use: Scientific Editorial Audit

Date: 2026-10-14. Stage: method merger, with frozen TEST and outcome labels untouched. This review concerns source-level academic integrity; final PDF validation belongs to N12-C3 dual PDF CI.

## Revised conceptual order

The formerly separate Problem Formulation and Base-Relative Evidence Valuation Framework have been merged into **Knowledge Valuation and Selective Use**, with five subsections:

1. **Ranking Events and Candidate-Dependent Utility** — define the pre-outcome context, candidate regime, observed target (offline only) and NDCG@10.
2. **Fixed Incumbent and Explicit Relationship Knowledge** — protocol-specific trained Base and unchanged auditable Memory combining Short/Long/Popularity at 0.45/0.45/0.10. Training-only Pop normalization and M3 all-author past-history rules remain.
3. **Incumbent-Relative Knowledge Value and Candidate Regimes** — define event delta, conditional eta and S-vs-F label/decision transfer. Retrospectively target-retained sampled labels are not serving-time inputs.
4. **Pretarget Estimation and Observable Evidence** — define user-history and Base-score feature summaries; train from realized DEV targets, predict from pretarget observable features; retain original online/offline framework figure.
5. **Invocation-Constrained Use and Retrospective Diagnostics** — same frozen invocation threshold with development-only call fraction; same standard expected gain identity; posterior target-evidence states and state-value decomposition explicitly reserved for offline interpretation.

The resulting chapter follows the paper's fixed-knowledge-source → candidate-relative value → pre-outcome prediction → selection logic. RQ3 remains a parallel source-validity study rather than a new causal proof.

## Strict mathematical and reference provenance

An independent locked fixture at analysis/kbs_plan_c/n12_c3_original_method_equations.json retains the exact nine original environments and equations by label: eq:event-ndcg, eq:memory-scoring, eq:delta-memory, eq:eta, eq:candidate-supervision-transfer, eq:expected-selective-gain, eq:utility-threshold, eq:diagnostic-states and eq:regime-decomposition.

All nine equation/align LaTeX bodies are byte-equivalent at text level to the frozen premerge file; all 22 original method reference labels remain unique and resolvable. Old section identifiers sec:problem and sec:framework both point to the same new parent section to avoid breaking later chapters. This compatibility should be simplified only after the N12-C4/C5 prose references are rewritten.

The entire pre-method document prefix (original abstract and N12-C2 Introduction/Related Work) remains identical under original source UTF-16 FNV32 b3c768aa. The subsequent Experimental Setup/Results/Discussion/Conclusion suffix retains UTF-16 FNV32 02c809d0. Bibliography and S1–S10.18 supplemental manuscript have not changed.

## Mandatory scientific boundaries

Memory history uses only observations before target decision time. The target identity, target-specific recoverable-state indicator, per-event true gain and hindsight Oracle never enter actual selection features. Candidate regime participates in defining the utility label and is not required as a categorical online feature. The DEV invocation cap is not a guaranteed future budget nor an established monetary or serving-speed benefit.

All original frozen TEST/30k H1/4096 H2 effects and comparisons remain unchanged. Unequal H1 realized F/S Memory calls, higher unconditional Always Memory accuracy, slower original pointwise Utility hardware timings, same-source-period additional targets, composite H2 historical permutation and the incomplete original H2 popularity-floor acceptance remain transparently reported in their original Results/Discussion locations.

## Reviewer-style method check and next stage

This form improves scholarly coherence by consolidating definitions rather than presenting existing math identities as novel theory. A KBS methodology reviewer can locate rank utility, fixed specialist, relative value, pre-outcome features and the decision rule in a single progressively defined sequence.

N12-C4 remains responsible for evidence hierarchy, chronology, sampling weights and hypothesis testing. N12-C5 will reorganize Results, and N12-C6 will finish Abstract/Discussion/Conclusion when evidence presentation is stable. No author approval, final submission or new experiment is implied.


## Final dual-PDF quality assurance (post-float and overfull corrections)

**Full Actions run #38549828504: BOTH JOBS SUCCESS.**
https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38549828504

- Main manuscript **38 pages** (N12-C2 predecessor 39), GitHub artifact **11885972844**, PDF SHA-256 **773ecfe60b0d1410728e29575deb88075315dab1438ee662b8ddb702c83a1038**.
- Supplement S1–S10.18 **45 pages**, artifact **11886356772**, PDF SHA-256 **032b1c96353029294bd3d2bc9768c15e34247d53144d313dc1ae9f8237f33448**.
- Both logs have zero overfull boxes or unresolved citation warnings. Main PDF scientific text extraction passed; 9 original equation environments and 22 labels compared to frozen source fixture.
- A small 3.13pt methods paragraph overflow was removed by shortening explanatory prose only. An online/offline framework figure floated between parts of an expected-value sentence in the first compiled version; adding a FloatBarrier now places it **before** Section 3.5. Final PDF text check confirms Figure 2 precedes Section 3.5, and selection utility/expected gain read continuously.
- This is the N12-C3 interim method draft. Experimental Setup (future Experimental Design), Results, Abstract, Discussion and Conclusion still await their individually scheduled N12 stages. No complete seven-section submission manuscript is asserted.

**C3 result:** academically coherent single methods section accepted for the next N12-C4 writing stage, subject to later cross-section editorial pass. This is not independent peer review or author signoff.
