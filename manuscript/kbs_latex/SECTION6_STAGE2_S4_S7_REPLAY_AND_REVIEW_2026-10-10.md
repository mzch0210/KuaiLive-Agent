# KBS Section 6 — Phase 2 DEV evidence integration, replication, and reviewer audit

**Date:** 2026-10-10  
**Canonical paper source:** [main.tex](main.tex), Section 6.4.  
**Original evidence run:** [Twitch DEV-only 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454), job 106700833375, artifact 10688746451.  
**Reproducibility re-execution:** [DEV replay run 37959745609](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37959745609), same-repo archived artifact download and checksum guard, [hosted artifact 11629932688](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37959745609/artifacts/11629932688). The hosted replay completed successfully.  
**Source code:** [analysis/kbs_section6_stage2_dev_replay.py](../../analysis/kbs_section6_stage2_dev_replay.py); [workflow](../../.github/workflows/kbs-stage2-dev-replay.yml).  
**Draft supplements:** [S4 Memory components](SUPPLEMENTARY_S4_MEMORY_COMPONENTS_DRAFT_2026-10-10.md), [S7 feature budget sensitivity](SUPPLEMENTARY_S7_GATE_BUDGET_DRAFT_2026-10-10.md).  
**Status:** Completed Stage-2 scientific replay and reviewer-style tightening of main Section 6.4; source/CI integrity verified. Journal supplement typesetting, final manuscript PDF page verification and coauthor approval are separate gates. **This is not a new held-out TEST or model training.**

## 1. Scope and non-leakage assurance

This phase used the previously archived **46,878 unique Twitch DEV events** and their previously fitted five-fold OOF predictions, plus archived deterministic rank outcomes for fixed Memory score variants. It never loaded Twitch TEST labels; it did not refit Utility, Difficulty, LiveRec, any Memory variant, or choose a new frozen threshold. The one-shot Twitch TEST (n=44,221), exact Difficulty count of 6,650, KuaiLive candidate factorial and associated bootstrap are unchanged. No new scientific novelty claim is introduced: C1–C3 are exactly the current approved outline.

The archived outputs were checked against SHA256 digests stored in the original run:
- Gate OOF gz: 25b5e560ce67d16221e483e9c18cad679eb28525ce0a8279ae91555726547627
- Original feature summary: 58d835e0ae53c43fe1ae522fdefee83374ba4ae58900968ea741780cffe92e48
- Memory variant user-event gz: b84e187290a7df2918e3bd050c4ab0a6a2baac611f72eb72f8616c7634c0644b
- Original Memory component summary: cc97794c49431c547ccf08a29da96bc275a900ed78a9ae71674b748b05e0750a

The exact archived 6,563-call Utility/Difficulty top-K masks were replayed for **all three feature families**, with **zero selection mismatches**; the original Utility−Base improvements were reproduced to **1e−12**. All 20 original Memory-variant × history-state mean results also reproduced to **1e−12**. The GitHub Actions job explicitly asserts selected legacy and newly computed metrics.

## 2. Output inventory and independent agreement

The hosted Action emits **budget_profile.csv** (36 records: five new exact budgets plus one original checkpoint × three feature families × Utility/Difficulty), **budget_contrasts.csv** (18 directly paired difference records), **component_pairwise.csv** (20 records: four groups × five direct variant comparisons), and **replay_provenance.json**. A completely independent local script generated the same values from the same archived input and separate vectorized user-bootstrap implementation; the two runs' gain differences were **exactly zero**, and pairwise bootstrap interval differences were below 1e−15.

Reproducibility parameters: identical candidate/event cohort, one target per user, standard fixed row-order tie-breaking, exact K = floor(n×fraction + 0.5), budget fractions 5%, 10%, 15%, 20% and 30%, **3,000 paired user-bootstrap replicates** for gate curves and **5,000** for component pairwise differences, seed 20261010 (or seed + group index). Resampling always occurs at the **user-event**, and a given user carries the same Base, Memory and all selector/variant values across contrasted policies.

## 3. Main statistical findings and boundaries

**S7—Feature families:** The history-only / Base-score-only / combined predicted-Utility gains versus the same DEV Base are:

| Equal invocation fraction | Number of calls | History features | Base-score features | Combined |
|---|---:|---:|---:|---:|
| 5% | 2,344 | +0.00221 | +0.00220 | **+0.00598** |
| 10% | 4,688 | +0.00349 | +0.00232 | **+0.00774** |
| 15% | 7,032 | +0.00371 | +0.00137 | **+0.00832** |
| 20% | 9,376 | +0.00406 | +0.00045 | **+0.00792** |
| 30% | 14,063 | +0.00311 | **−0.00282** | **+0.00736** |
| Original K = 6,563 | 6,563 | +0.00372 | +0.00160 | **+0.00838** |

At each inspected budget, direct within-user combined-versus-restricted feature comparisons are positive; their **pointwise, unadjusted, conditional** bootstrap intervals are in S7 and original hosted output. Combined Utility exceeds combined Base-Difficulty OOF score selection at the same counts, but **this is a development-only batch-top-count diagnostic, not a new one-shot frozen TEST result or a pointwise deployable hard-budget policy**. Gains are nonmonotonic; the Base-score-only series becomes negative at 30%.

**S4—Memory components:** In the recoverable-but-unrepresented DEV subgroup n=5,879, Base NDCG@10 is **0.30201**, fixed Full Memory **0.53298**, Long-only **0.63890**, Short+Long **0.58673**. The newly bootstrapped **paired Long-only−Full Memory** mean is **+0.105915**, 95% percentile CI **[+0.100957, +0.110610]**. The Short+Long−Full Memory difference is **+0.053744**, CI **[+0.049556,+0.057919]**. All scores come from fixed specialist ranking variants of the *same* events; that differences are positive does not identify causal information content, and no Memory weights or frozen policy were changed. The Long-only−Full contrast has the opposite sign (approximately −0.03208) on the unavailable group, further limiting universality.

**Sampling/inference:** Bootstrap resamples the observed DEV users while **holding score vectors, trained models, retrospectively assigned state labels, selected event sets, and fixed budgets constant**. It does not incorporate model training, OOF/cross-validation choice, threshold-selection uncertainty, multiple-testing adjustment, or truly new data. No simultaneous confidence band is reported. These are important design constraints for the KBS manuscript, not optional footnotes.

## 4. Manuscript Results changes and editorial review

- Only canonical **Section 6.4** was modified, not 6.1–6.3 or 6.5, nor the C1–C3 contribution definitions in Sections 1–4.
- Added a concise scientific result that combined features retain the greatest **observed** DEV OOF Utility gain at the five inspected equal-call budgets, with pointwise and model-selection caveats; no new full-size figure/table was forced into main Results.
- Added one direct paired effect estimate for Long-only versus the original fixed Full Memory, with exact subgroup n, effect size, confidence interval and strict causal boundary.
- Preserved the existing one-count feature-family table, seven-setting Memory sensitivity, L8/L16/L32 Base retraining caveat, nonmonotonic recency and limited baseline-competitiveness check.
- Independently reviewer-tightened 6.4 from **896 whitespace-delimited words to 610** (including unchanged table source) to reduce repeated caveats and keep the journal-facing Results scientifically dense. Full panels belong in S4, S6 and S7; only the most material effects remain in Results. The section ordering and related framework remain unchanged.
- The first revised source commit [fe78ed69](https://github.com/mzch0210/KuaiLive-Agent/commit/fe78ed69c6b869b6969c226067d93ba46165f651) passed a matching [LaTeX build 37959035191](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37959035191) but the extra prose crowded the efficiency subsection over a page break. A scoped layout reviewer-tightening commit [008e4704](https://github.com/mzch0210/KuaiLive-Agent/commit/008e47043d017ab8492cdc232d9b2f1260c4075c) compressed Section 6.4 only, without changing any effect, CI or policy.

**Additional PDF gate:** Check final commit 008e4704 (not just the earlier 28-page intermediate) against a successful, exact-SHA GitHub Actions build and visually inspect pages containing §6.4–6.5 and References. This status must be updated with actual evidence before declaring full layout approval.

## 5. Reviewer-style acceptance checklist

| KBS-facing requirement | Result |
|---|---|
| Work addresses C1 and C3 without inventing new method novelty | PASS |
| No frozen Twitch TEST leakage/recalibration | PASS by source SHA and DEV-only workflow |
| Original K=6,563 and original component replay identity | PASS |
| Same-user exact-count policy comparisons and paired CIs | PASS |
| Full component matrix and all budgets accessible | PASS in S4/S7 draft + independent Actions artifact |
| Clear causal/multiple-comparison/OOF uncertainty limits | PASS |
| No new main-text figure density or additional table creep | PASS |
| No false production budget/latency or online treatment-effect promise | PASS |
| Final matching-PDF render of compact 6.4 | PENDING current source-specific final check |
| Formal S4/S7 supplementary PDF/coauthor sign-off | OPEN |

**No additional new experiment is required to substantiate these *development robustness* results.** The next authorized work outside this phase is submission-ready S1–S9 assembly and optional, separately approved candidate-sampling P2; neither should be silently described as completed.
