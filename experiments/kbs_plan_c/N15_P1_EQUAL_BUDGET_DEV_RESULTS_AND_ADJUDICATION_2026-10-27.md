# N15 P1 — Strict equal-call DEV outcome and scientific adjudication

**2026-10-27. STATUS: EXPLORATORY_DEV_MATCHED_CALLS_PASS; NOT INDEPENDENT TEST AND NOT SUBMISSION GO.**

## 1. Execution provenance

- Branch: `kbs-n15-scientific-strengthening-20261027`.
- Source commit: `164b60f6a06efb19942077c12383e56f2a6d1b68`.
- GitHub Actions: [#40510033361](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40510033361), hosted preflight **SUCCESS**, self-hosted private DEV **SUCCESS**, result export **SUCCESS**.
- Aggregate-only artifact: `n15-p1-exploratory-dev-matched-aggregate`, artifact ID `12737320332`, SHA256 ZIP digest `2c70a2e5a7e357629e9357f6993c6ee2db20d8f7e2002a6bc5bcdfab57b7cc8d`. Expiry shown as 2026-11-26; retain permanent checked aggregate or reproducible regeneration contract separately.
- Frozen private B1 DEV candidate label CSV SHA256: `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`; metadata and actual hash validated on selfhost. **50,049** original DEV Author events, **12,628** users, no G5/B4-A TEST input.
- Initial workflow #40509775700 stopped before reading data because `sklearn` not importable. Second #40509926112 passed private source hash but was stopped before fitting because per-step `PYTHONPATH` was not propagated. Both errors were fixed in workflow only; neither is a negative scientific result.

## 2. Predeclared question and exact offline batch allocation

At q=.30, evaluate both F-supervised and original S-supervised HGB predicted conditional Memory-minus-Base utility on the same full-active Author DEV candidate rosters. Five outer **user-disjoint** GroupKFold validation folds; separate train-fold F and S regressors, identical 12 pretarget input variables; on each outer evaluation fold both policies select exactly floor(.30 * fold size) top-scored requests. Score ties use deterministic, label-blind SHA256 of protected original CSV row index. Thus exact *raw* Memory calls match within fold and globally.

**This is offline fold-batch top-k allocation**, not the original threshold-based naturally realized B4-A policies, not an online policy and not an isolated label-only causal effect. Existing original DEV has been extensively reanalyzed after G5, making these analyses exploratory even with user-disjoint predictions.

## 3. Grounded q=.30 results (source: Actions #40510033361 successful verified job log)

| Base | F-supervised full-F NDCG@10 | S-supervised full-F NDCG@10 | F−S | Equal Memory calls F/S | F-only=S-only requests | Descriptive paired user 95% CI |
|---|---:|---:|---:|---:|---:|---|
| SASRec | 0.302635782570 | 0.296502457148 | **+0.006133325422** | **15,014 / 15,014** | **5,338 / 5,338** | [0.004722260564, 0.007495203212] |
| GRU4Rec | 0.303569955822 | 0.298172145024 | **+0.005397810798** | **15,014 / 15,014** | **5,786 / 5,786** | [0.003931550706, 0.006732675038] |

Observed raw call fraction is exactly 15,014/50,049 (~30.0%) for each policy and architecture. No B4-A twenty-cell weighting was imposed on the unweighted DEV population. The script validated `F_minus_S_full_F_ndcg == mean((pi_F-pi_S)*Delta_F)` within 1e-12, and the both/F-only/S-only/neither categories account for all requests at each predeclared budget q∈{.1,.2,.3,.4}.

**Scientific read:** the direction and practical scale of the previously reported exploratory DEV policy difference do **not** collapse when both F/S selectors are permitted exactly the same number of Memory calls. Matched-call allocation removes the simplest net-call-count imbalance explanation for this *new offline batching estimand*. It does NOT establish the previous B4-A TEST comparison as a strictly equal-call causal result, since that was a different frozen threshold policy and its call counts stay immutable.

The two bootstrap intervals are **descriptive reused-DEV uncertainty**, not fresh confirmatory inference. There is no new Holm test or new external replication.

## 4. Scientific verdict and qualification

- **P1-A scientific feasibility: PASS_FOR_EXPLORATORY_MECHANISM_EXTENSION.** This directly answers an important reviewer objection at the DEV sensitivity-analysis level.
- **Novelty remains HIGH-CONTESTABLE.** Sampled metric inconsistency (Krichene/Rendle KDD20) and learned expert deferral (Mao/Mohri/Zhong ICML24) are not original here. New work must still demonstrate knowledge-source/competition dependence or independently confirmed decision policy guidance.
- **P1-B source specificity: NOT RUN.** Full-vs-Long source×supervision decision-loss interaction requires own score/model and paired labels, with old B2 showing Long-only can have greater regret than Full; no monotone relationship presupposed.
- **Corrected-S: STILL OPEN COMPETITOR.** Existing NI1g NO-GO for prior candidate corrected-S estimators stays in force; sampled-only valid correction not ruled out.
- **Practical deployment: NOT SUPPORTED.** Offline fold-batch top-k looks ahead at the evaluation fold's request score list and does not show real-time latency/cost savings; Always Memory remains better for unconstrained accuracy.
- **Temporal confirmation: STILL OPEN.** Same extensively analyzed DEV; 30k B4-A already unsealed and same recording period. The next valid P3 requires independently authorized, previously unseen future targets and pre-frozen rules.

## 5. Next research decision

Proceed with a **gated, small Full-versus-Long-only knowledge-source-interaction feasibility** using original B2 DEV source parity, exact same q and independent source-specific models. Before any new selfhost scoring, verify candidate labels, source-specific feature contract and competence/floor diagnostics. Run only if it can answer a genuinely new source×supervision allocation question; else stop.

Do not alter N14 paper or original B4-A quantitative conclusions merely on the basis of this same-DEV exploratory result. Retain as a sensitivity result and as the basis for a prospective evaluation design.

**GO:** P1-A exploration completed. **HOLD:** P1-B source admission, P3 fresh test, KBS author submission.
