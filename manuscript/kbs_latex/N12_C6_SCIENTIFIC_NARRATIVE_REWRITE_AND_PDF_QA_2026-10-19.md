# N12-C6 | Scientific-contribution gate, evidence-chain integration and dual-PDF editorial QA

Date: **2026-10-19**. **Stage verdict: C6 COMPLETE / scientific-source and dual-PDF CI PASS**, with explicit unresolved *KBS novelty, identification and human-review risks*. This report documents completed actions on Draft PR #6 only; no submission, independent referee approval or author signature.

## 1. Scientific starting point and C6.0–C6.1 completion

- Input: existing N12 C5 seven-section / four-Results-role manuscript, last frozen science CI #38864362019 (36p main / 47p supplement). C0–C5 remain unchanged and successful.
- [C6.0 claim/prior-art stress test](N12_C6_CLAIM_EVIDENCE_PRIOR_ART_STRESS_TEST_2026-10-19.md): **PASS_TO_EDIT_WITH_BOUNDED_EMPIRICAL_CLAIMS**. A defensible empirical decision-target contribution is possible; the P0 risk of seeming a straightforward combination of sampled-metric inconsistency (Krichene/Rendle) and established learning-to-defer (Mao/Mohri/Zhong) **remains**. No new novelty theorem or journal acceptance is claimed.
- [C6.1 supervision-to-decision trace](N12_C6_RQ2_SUPERVISION_TO_DECISION_EVIDENCE_CHAIN_2026-10-19.md): documented DEV switch decomposition (50,049 events; SAS 10,672 = 21.32%, GRU 11,517 = 23.01%; new-vs-displaced call gains SAS .133417/.076194, GRU .126600/.079135), frozen 30k same-period H1 (SAS +.005391; GRU +.003585), and 4096 nested, parallel RQ3 history check (+.031145). Kept scientific cohort identities separate; no private event-level rescoring.
- C6 authorship of text was informed by primary source/public abstract evidence and exact existing GitHub public DEV aggregates, not by opening new private TEST labels.

## 2. Exact manuscript edit scope (C6.2)

- `manuscript/kbs_latex/main.tex` **Abstract**: now leads with candidate-regime-conditioned relative-utility supervision, reports 30k H1 as the principal frozen policy result, paired room reversal and RQ3 as supporting, and names unequal calls, incomplete original H2 prereveal floor, adverse Always Memory comparison and offline evidence limitations.
- `Introduction`: revised exactly the three contribution bullets (main RQ2 decision effect; RQ1 valuation diagnostic; RQ3 independent history check). The existing RQ1→RQ2 and parallel RQ3 concept figure remains unchanged.
- `Discussion`: restructured into three science-led subsections: (1) candidate-indexed knowledge value versus prior metrics/deferral/knowledge-representation work; (2) supervised policy allocation and its evidence limits, including switch-on/off gains and B2 non-monotonic counterexamples; (3) composite historical source null, unverified same-cohort popularity floor, same-period samples, offline exposure and adverse system costs.
- `Conclusion`: transfer-worthy candidate-aligned knowledge value *supervision contract*, without generic gating firstness, strictly equal-call causality, source-specific semantic causality, unmeasured future validation or production savings.
- `Highlights.txt`: aligned to candidate-supervision and decision allocation, with adverse resource bounds.
- No Results table cells, experimental cohorts, 9 method equations, 2 experimental formulas, frozen H1/H2 statistics or additional TEST outcomes altered. Original Results table disposition remains seven literal original LaTeX blocks in main + four full supporting tables in S10.19.

## 3. Stage-correct scientific CI replacement (C6.3)

The archival C5 auditor `analysis/kbs_plan_c/n12_c5_rq_results_evidence_audit.py` fingerprints both **main[:Results] (including Abstract)** and **main[Discussion:]** and would falsely fail on required C6 editorial edits. C5 push workflow `.github/workflows/kbs-n12-c5-rq-results-pdf-qa.yml` was switched to manual-only, keeping its historical successful run intact.

New `analysis/kbs_plan_c/n12_c6_scientific_contract.py` preserves scientific portions of the C5 contract (seven-section/4-Results role structure, all 7 frozen main scientific result table blocks, figure, 4 moved supplement tables, 9+2 frozen equations, H1/H2/realized call counts and negative accuracy/timing, 3 RQ references, all LaTeX/BibTeX citations) **without freezing Abstract/Discussion/Conclusion bytes**. Additional C6 checks require the refocused Abstract and Highlights and reporting of equal-resource, historical, unconditional and unverified control cautions.

New `.github/workflows/kbs-n12-c6-scientific-pdf-qa.yml` builds main paper and full S1–S10.19 supplement, verifies human-visible text/citations/statistics and absence of overfull boxes in both outputs. No old C5 preservation theorem is overwritten in place; its archival success is separately inspectable.

## 4. Failure triage and final verified successful CI

- First new run [#39200571393](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39200571393) successfully compiled the **36-page main PDF** and passed scientific source and cross-document checks, but **failed strict main-PDF overfull QA** owing to a ~2.86324 pt wide Discussion sentence at source lines 624–625. This is an actual C6 editorial layout failure, not a frozen scientific-result mismatch. No decision to weaken the QA threshold was made.
- Fixed by shortening only the nonquantitative sentence describing the three distinct ranking units, in commit `788c71dc48391639f8bf6fdaf9792239939b75b1`.
- **Final successful run:** [#39200835455](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39200835455) on source SHA **`788c71dc48391639f8bf6fdaf9792239939b75b1`**. **Both `main-paper` and `complete-supplement` jobs SUCCESS.** Source science verifier and main–S10 cross consistency PASS. Main compiled **36 pages**, supplement XeLaTeX XDV/PDF **47 pages**; zero overfull and no fatal/undefined label/citation QA issues in checked logs. Journal-facing RQ1/RQ2/RQ3 primary figures, 30k H1, 4096 H2 and adverse cost numbers remained discoverable in PDF text.
- **Workflow archive artifacts** (digest denotes GitHub artifact ZIP, not embedded PDF SHA256):
  - main artifact ID **12162784746**, `kbs-n12-c6-main`, GitHub ZIP digest `sha256:73b8c65d9c7340a48e5840bf9dd7b7251dde04c6ab50247a8326d8612e8abdf9`;
  - supplement artifact ID **12164145955**, `kbs-n12-c6-supplement`, ZIP digest `sha256:01e1c3d5c949c1918321b79abb5d1c1a56273514082ac5e07e77bc7184ffaf26`.
  - Both Actions artifacts currently expire **2026-12-18**. Long-term paper reproducibility manifest belongs to C7. The source PDF SHA256 has not separately been computed and must **not** be inferred from ZIP digests.

## 5. Precise scientific gate verdict

**C6 editorial/science QA: PASS, with bounded contribution language.** This means the approved *internal scientific source editorial process and two final PDF builds* passed. It does **not** close these independent research risks:

1. Original F/S H1 natural Memory-call differences 1.337/1.797 percentage points exceed the old 1pp near-equal gate, so the comparison remains **complete frozen policies**, not strict equal-budget supervision-only causal identification.
2. The new 30k targets are same-period (not independent future-time cohorts); 4096 H2 targets are nested, and three history-null seeds share a cohort.
3. Original B4-A cohort-specific TRAIN-only Popularity prereveal acceptance requirement was **NOT VERIFIED**; DEV parity cannot replace it.
4. Real historical permuting is a strong composite intervention, not isolation of one semantic user–creator mechanism.
5. Always Memory remains better in unconstrained M3 ranking quality; original pointwise Utility slower in measured DEV replay; new vectorized F gate has no workload-matched production cost measurement or demonstrated external knowledge scarcity.
6. Original KBS contribution's originality relative to KDD sampled-metric and ICML learning-to-defer work is **not settled by editorial QA**. C8 must generate adversarial referee memos and an author go/no-go decision.

**Next stage: C7**, per [2026-10-19 amendment](N12_C6_C8_SCIENTIFIC_CONTRIBUTION_AND_REVIEW_GATE_AMENDMENT_2026-10-19.md): exact four migrated table full-cell source matching, dual-direction claim→source ledger, dataset rights and reproducibility tiers, full manuscript/supplement coherence. C8 remains NOT STARTED. PR #6 stays DRAFT; nothing submitted.
