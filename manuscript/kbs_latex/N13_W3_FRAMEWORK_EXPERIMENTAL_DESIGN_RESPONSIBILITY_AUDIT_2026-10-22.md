# N13 W3 — Framework / Experimental Design responsibility audit

Date: 2026-10-22  
Branch: kbs-n13-controlled-manuscript-revision-20261022  
Source before W3: main.tex blob 96c090b78de9d48331029def3c7ca52c4e5c4453  
Scope: Editorial responsibility and duplication only; no model, target, cohort, threshold, estimator, result or inferential changes.

## Responsibility contract

| Information | Sole conceptual owner | Experimental Design role | Disposition |
|---|---|---|---|
| Event \(\xi_r\), ranked candidates, event-level NDCG@10 | Framework, Ranking Events | Refer back to framework | Keep formal definition once |
| Fixed Base \(B\), fixed Memory \(M\), scoring formula and common candidates | Framework, Fixed Incumbent | Identify protocol-specific Base families only where needed | Avoid re-explaining Memory formula in Methods |
| \(\Delta_M\), \(\eta_r\), S/F labels and policy-transfer estimand | Framework, Incumbent-Relative Knowledge Value | Explain how S/F labels are generated and where they are evaluated | Keep equations in framework; keep protocol implementation in design |
| Pretarget feature contract \(Z\), target leakage boundary | Framework, Pretarget Estimation | Give task-specific feature counts/names and point to supplement | Remove repeated exclusion list from design |
| Threshold rule and development call constraint | Framework, Invocation-Constrained Use | Give OOF folds, threshold calibration design and exact cohort/fit protocol | Retain design-specific numbers |
| Retrospective evidence states \(S_L\) and decomposition | Framework, retrospective diagnostics | State that assignments are retrospective only where the cohort protocol needs it | Avoid repeating full definition |
| Ranked units, source intervals, eligibility, split boundaries and cohort counts | Experimental Design | Primary owner | Keep all reproducibility-critical details |
| Base families, seeds, checkpoint-screening and model-fit capacity | Experimental Design | Primary owner | Keep |
| Additional-target freeze, 20-cell weighting, nested null construction, inference families and device protocol | Experimental Design | Primary owner | Keep |
| NDCG endpoint, paired event/user-cluster inference | Experimental Design | Primary owner | Retain endpoint and all resampling/Holm details; remove duplicated target-state exclusion |

## Edits applied to main.tex

1. Framework “Pretarget Estimation and Observable Evidence”: removed duplicated task feature counts from the conceptual definition. It now defines what \(Z\) means and points to the operational schema; the explicit target-leakage contract remains in this section.
2. Experimental Design “Fixed Rankers and Selection Objectives”: removed repeated prose reintroducing the Base/Memory definition. Kept M3 model families, seeds and the fact that six fits share one TEST population.
3. Experimental Design feature schema: kept all twelve M3 and fourteen Twitch feature counts and names, but framed them as protocol-specific instantiations of the framework contract rather than repeating the entire leakage exclusion list.
4. Endpoints/inference: retained NDCG@10, HR@10, invocation fraction, paired comparisons and user-level resampling; removed a repeated sentence defining target-dependent states as retrospective because that contract is already formally defined in the framework.
5. H1 DEV switch denominator: restored the frozen audit phrase “event decisions disagree” while retaining 10,672 (21.32%) and 11,517 (23.01%) and the descriptive, non-causal interpretation.

## Scientific invariants explicitly unchanged

- H1 additional target effect: SASRec +0.005391 (95% CI [0.003646, 0.007174], Holm p=0.000600); GRU4Rec +0.003585 (CI [0.001599, 0.005576], Holm p=0.000800).
- Weighted calls: SASRec 29.203% versus 30.537%; GRU4Rec 29.008% versus 30.809%; realized calls differ and this is not an experimentally isolated equal-resource effect.
- H1 is a complete frozen-policy comparison against the original uncorrected sampled-label protocol; the 30,000 additional targets are from the same recording period, not a future-period replication.
- H2 uses 4,096 nested targets / 3,059 users; the cohort-specific pre-reveal TRAIN-only Popularity-margin acceptance check remains NOT VERIFIED.
- DEV allocation remains descriptive, not H1 mediation or a causal decomposition of the additional-target contrast.
- Always Memory NDCG 0.348744 exceeds the selective F-aligned scores 0.305446 / 0.304530; the legacy pointwise selector timing 1.769 ms versus 0.692 ms Always Memory remains an adverse cost result. No end-to-end/monetary savings claim.
- All seven frozen Results table blocks, core equations, cohort boundaries, confidence intervals, p-values and Holm family definitions remain untouched.

## W3 exit checks

- [x] Defined unique ownership for concepts versus protocol implementation.
- [x] Made only scoped prose edits to main.tex; no table/equation bodies were edited.
- [x] Preserved exact C8V phrase “event decisions disagree”.
- [ ] Rerun C7/C8V, cross-source consistency and both PDF builds on the final W3 source blob.
