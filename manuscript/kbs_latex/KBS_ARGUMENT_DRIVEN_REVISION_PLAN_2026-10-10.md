# KBS manuscript: argument-driven Results revision and Sections 1–6 editorial diagnosis

**Date:** 2026-10-10
**Canonical file:** [main.tex](main.tex), no change in formal C1–C3 novelty, fixed models, policy thresholds, evaluations, source estimates or statistical uncertainty.

## 1. Central scientific thesis and manuscript architecture

**One-sentence thesis:** *The value of relationship memory is the context-dependent incremental ranking utility a fixed evidence-based specialist provides over an existing Base, not the mere amount of available historical evidence.*

**Evidentiary argument:** (i) heterogeneity is measurable even when the specialist loses overall (C1 and conditional structure); (ii) a deployable pre-outcome feature set can recover part of the potential value by ranking requests for specialist invocation (C3); (iii) the operational value depends on candidate evaluation regime even for fixed users and model scores (C2). This is a deliberate **question → empirical finding → decision implication → operating boundary** progression; it retains the outline's *defined* contribution names C1–C3, even though Results sequence presents C3 before candidate-regime boundary C2.

Section roles:
- **1 Introduction:** why fixed Base-relative evidence value is the missing *decision quantity*; preview the two distinct empirical questions once, avoid process history.
- **2 Related Work:** distinguish evidence fusion, expert allocation, sampled evaluation; end with a succinct targeted research gap (not repetitive defensive comparisons).
- **3 Problem Formulation:** define event utility Δ and conditional expectation η, and prove the selection identity; history state is diagnostic not an observable selector input.
- **4 Framework:** implement the transparent fixed specialist and pre-outcome features; distinguish signal/protocol from claims about learned knowledge mechanisms.
- **5 Experimental Setup:** state model, events, candidates, freeze, comparator protocols, matched pairs and uncertainty; source hashes, special training budgets and detailed exercise history live in S1–S9.
- **6 Results:** structured empirical case from heterogeneity → realizable selection → context dependence → discriminating robustness → computation cost; quantify before qualification.
- **7 Discussion (not authorized in this phase):** interpret base- and regime-dependence, noncausal states and candidate confounding, bounded decision value, and deployment constraints in an integrated narrative.
- **8 Conclusion and Abstract:** write only after the full argument is stable.

## 2. All prior P1/P2 Results requests — implementation checklist

| ID | Source scope | Minimal evidence-safe change | Verification |
|---|---|---|---|
| P1-A | Start of 6 and links 6.1–6.3 | Add a 50–70-word Results roadmap and align subsection leads with the question, not experimental timeline | No reordering/retraction of experiments |
| P1-B | 6.2 | Reveal frozen Utility-selected and nonselected **conditional realized Δ**, plus equal-count Difficulty-selected Δ; values **+0.05136, −0.05890, +0.00855** derived algebraically from the *same* original frozen aggregate results. Show calculation in audit, no selection change or new significance claim | Exactly 6,650/44,221; full Base/Memory/Utility/Difficulty means reconcile |
| P1-C | 6.3 | Articulate distinction from existing sampled-metric model-order literature: fixed specialist versus designated Base, matched same-user and checkpoint and score-reference crossover | Keep descriptive/noncausal C2; no invented sampled theorem |
| P1-D | 6.4 | Explain original Full Memory was a **fixed study comparator**, not a post-subgroup optimized expert; report Long-only's recoverable advantage with contrast to overall DEV Base/memory | S4 observed original figures consistent; no retuning |
| P1-E | 6.4–6.5 | Distinguish auxiliary unequal-budget baseline checks from reference optimality and explain that **81 fitted trees** belong to the separate KuaiLive **benchmarked** HGB timing pipeline | No Twitch/KuaiLive model identity conflation |
| P2 | 6.3–6.5 and S1–S9 pointers | Cite precise **Tables S5.2 / S6.1–S6.4 / S7.1 / S9.1**, streamline repeat warnings, and keep full source tables in supplement | All cited tables exist in unified S1–S9; main no nine-row P2 duplicate |

## 3. Global rhetorical diagnosis and repair rule

**Diagnosis:** The paper has appropriate research content but its flow often foregrounds risk defenses (e.g., post-hoc status, not causal, not SOTA, not deployment) and experiment-management chronology. These are important *truth conditions*, but repeating them in every empirical sentence obscures the positive scientific finding. The research claim is therefore correct but under-signaled.

**Edit principle:** **Claim first → evidence/estimator second → one protocol boundary at the natural point**, often Methods/caption/short end-sentence; shift exhaustive checkpoint SHA, rerun chronology, file artifacts, selection comparisons and numerical grids to relevant S sections. **Do not remove necessary DEV/TEST labels, equal-count post-hoc nature, target-defined state restriction, confounded candidate size/composition, or controlled CPU mask-replay limitation.** Negative empirical evidence (e.g., Memory poorer in aggregate, measured latency 2.03×) is scientifically substantive and must remain prominent. Distinguish positive-but-not-causal from rhetorical hedging.

Targets for minimally invasive global cohesion: sharpen thesis and contribution order in Introduction, connect Related Work's research gap to the single decision quantity, and add one purpose-first sentence each at starts of sections 3, 4, 5, 6. Limit unrelated rewriting so a subsequent integrated editorial rewrite can proceed once Sections 7–8 and Abstract exist.

## 4. Source and presentation acceptance gates

1. Pin canonical pre-edit SHA and reproduce **only scoped** text changes in main.tex. No editing model code, TEST thresholds, labels, sampling dates or experiment outputs.
2. Every conditional event mean is an arithmetic consequence of the same released frozen TEST totals; **not a new independent experiment, bootstrap test, or trained predictor**.
3. Check all numeric literals and CIs from current sources; retain P0 matched 0.60709 vs full 0.38571, not auxiliary KuaiLive checkpoint 0.61714. Keep all six baseline/source roles distinct.
4. Check official source-guided writing practice: Results logical, focused; Methods reproducible; Discussion interprets implications and limits. Editorial repair avoids impression that research data supports broader causality.
5. Verify 25 BibTeX citation keys and LaTeX refs, exact Sx.y table labels and one build from exact edited source; inspect relevant PDF pages for placement and overflow. If formatting degrades, compress/reposition without changing findings.
6. Deliver an explicit list of remaining *whole-paper* structural changes to carry into Discussion / Abstract later, not an unrequested broad rewrite.
