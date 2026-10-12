# R4 — Problem Formulation and Framework Acceptance

**Date:** 2026-10-12. **Decision: R4 PASS for Sections 3–4.** Overall paper remains HOLD pending R5–R8. The frozen G0F and G5 protocols, models, TEST evidence, original Twitch and KuaiLive tests, and S1–S9 were not altered.

## Accepted source and engineering evidence

- Canonical [main.tex](main.tex) GitHub blob SHA **df1aa8c9781188e714cff0df51abc2008c33dac3**.
- R4 text commits: **11ed966b660ec29a03e357b8ec32c05e54974250** (Section 3) and **9069fc150f2bb936761d8cf07849496a52686912** (Section 4).
- [Final R4 GitHub Actions LaTeX build #38238654424](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38238654424): **SUCCESS**, artifact **11742520029**, complete **36-page PDF**, **502,062 bytes** in Letter-format working preprint.
- Inspected rendered PDF pages **5–12**, including new §3 threshold formula and §4 framework graphic. **No overfull box warnings, undefined references/citations or duplicated labels.** Three underfull line-break warnings exist but do not represent clipping. Section 3/4 math and diagram were visually verified. Compared with the 34-page R3 PDF, R4 added two pages, so R5–R8 must improve information density and float layout.
- R4 did not change Sections 1–2, 5–8, or supplemental S1–S9.

## §3: coherent comparative valuation and exact budget protocol

- Retained event NDCG@K, candidate-conditioned specialist-minus-incumbent utility Δ_M, conditional η_r and the expected routing-gain identity. Explicitly distinguished the conditional decision-quality estimand from proved real-world cost savings.
- Clarified M3 prequential history: only events strictly earlier than the current prediction may enter historical features; previously observed earlier TEST events are allowed, while present/future labels are excluded. This is not an identified disjoint-person generalization test.
- Linked generic relative-expert deferral to existing ICML 2020 and NeurIPS 2022 theory instead of presenting a new generic theorem.
- Reworked invocation subsection: the mathematical decision uses the frozen protocol-specific strict/inclusive threshold convention. **M3 is inclusive at threshold ties**, with all tied events assigned together.
- The **max 30% call fraction applies to DEV OOF threshold selection**, not a rigid realized TEST quota or equal-call TEST comparison. Twitch's Difficulty and Oracle retain their historical **retrospective TEST count matching**, unlike M3's independently DEV-frozen pointwise objectives.
- Neither a reduced expert-call frequency nor the expected selective ranking-utility equation establishes lower hardware latency or an economically optimal deployment.

## §4: align fixed knowledge and competing Bases with verified source code

- Distinguished three ranked targets and their designated incumbents: Twitch LiveRec streamers (context 16), original KuaiLive Dual-ID SASRec live rooms, and KuaiLive-M3 persistent active TRAIN-known authors with separately trained SASRec or GRU4Rec (three training seeds each, input 16). M3 checkpoint selection on 4,096 × 575-author DEV screen is not full-active TEST.
- Preserved the transparent **Memory = 0.45 Short + 0.45 Long + 0.10 TRAIN-popularity** and short horizon 10 with exp(−distance/3) decay.
- **Critical frozen M3 code match:** TRAIN-unseen authors in prior interactions **consume Short recency positions** and **contribute to the maximum creator count used in Long normalization**, though they cannot be current TRAIN-known candidate authors. The Base has its own known-author context-16 sequence; thus the two scoring paths do not necessarily use identical historical visibility windows.
- Kept represented/recoverable/unavailable states **target-dependent retrospective diagnostics**; they cannot enter the decision-time selector.
- Specified **Twitch 14 observable features** separately from **M3 12 features** (5 Base score descriptors, 7 history/candidate descriptors). The support fraction for history-observed eligible candidates is computable without executing a full Memory ranking. There is no claimed zero-shot transfer of the Twitch gate to M3.
- Clarified the five M3 routing objectives: supervised Utility, Difficulty and Specialist Quality, plus observable deterministic Uncertainty and History scores. Their thresholds remain independently DEV-frozen; Twitch's retrospective equal-count control is not reclassified as a frozen pointwise policy.
- Framework diagram now says **apply DEV-frozen selection rule** instead of asserting a universally strict score-greater-than-threshold rule.

### Source-of-truth implementation files

- [Corrected M3 all-history Memory replay](../../analysis/kbs_plan_c/g3_replay_correct_memory.py) — exact Short/Long history.
- [M3 frozen label-blind TEST scoring](../../analysis/kbs_plan_c/g5_unlabeled_test_score.py) — prequential history and inclusive gate masks.
- [Grouped DEV OOF gate implementation](../../analysis/kbs_plan_c/train_gate_oof.py) and [DEV-frozen gate comparison](../../analysis/kbs_plan_c/g3_fit_dev_gates.py).
- [R0 source claim matrix](R0_PLAN_C_CLAIM_PROTOCOL_EVIDENCE_MATRIX_2026-10-12.json), [R3 source-backed results acceptance](R3_PLAN_C_RESULTS_ACCEPTANCE_2026-10-12.md).

## R0/P0/P1 responsibilities after R4

Full machine-readable updated [R4 twelve-issue closure tracker](R4_R0_P0_P1_ISSUE_CLOSURE_TRACKER_2026-10-12.json) records each of 6 P0 and 6 P1 items. **No item is marked fully closed at the article level before downstream revisions.**

| R0 issue | R4 first or continued correction | Remaining accountable work |
|---|---|---|
| P0-01 | Value formulation and framework now explicitly conditioned on Base, task and regime | R5 intro/discussion/conclusion; R6 supplement; R8 |
| P0-02 | Twitch retrospective and M3 five DEV-frozen pointwise policies distinguished | R6, R8 |
| P0-03 | DEV max 30% call cap, actual TEST drift and threshold ties formalized | R6 S7, R8 |
| P0-04 | Count constraint not equated to real latency; §6 already contains negative M3 cost evidence | **R5 §7**, R6 S9, R8 |
| P0-05 | Twitch 14-vs-M3 12, room-vs-author, Base-vs-Memory historical windows specified | R6 S1–S3, R8 |
| P0-06 | No unsupported six-dataset or global 18-test inferential claim | R6 S8 complete intervals, R8 |
| P1-01 | No change to original G0F/G1 sampling hash implementation identity | R6 S1 details; R8 |
| P1-02 | Platform-specific frozen deterministic tie behavior preserved | R6 S2; R8 |
| P1-03 | Methods no longer imply a sole Twitch heldout confirmation | R6 old S1–S9 introduction |
| P1-04 | Learning-to-Defer theory acknowledged and cited explicitly | R5 §2/§7; R7 |
| P1-05 | No superseded pre-G5 status in framework | R6 latest report/legacy index |
| P1-06 | G5 SHA provenance retained, public Actions retention still a risk | R6/R8 archival plan |

## Reviewer risk and next step

Two substantive limitations remain **scientific**, not method-text defects. First, fixed relationship-memory relative utility is not a new deferral theorem; R5/R7 must distinguish knowledge-specific full-candidate ranking valuation from established post-hoc expert routing and knowledge-fusion gates. Second, on M3 unconditional Memory produces **higher TEST NDCG@10** and **lower mean warm DEV replay time** than the Utility routing path; R5 Discussion must directly address the absence of a demonstrated practical need for selective deployment under the observed cost model. Further limitations concern M3's author task differing from old room ranking, candidate eligibility and strict per-request call fraction drift.

The 36-page draft must be condensed without deleting scientifically essential evidence or hiding adverse cost. The source is now aligned through §6, but §1–2/§7–8 and S1–S9 are not. **R4 PASS; next R5: integrated academic revision of Introduction, Related Work, Discussion and Conclusion, then R6 supplementary synchronization.**
