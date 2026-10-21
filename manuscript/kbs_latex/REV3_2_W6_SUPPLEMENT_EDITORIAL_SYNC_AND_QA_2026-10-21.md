# Rev3.2 W6 — Supplement editorial synchronization, source integrity, and pending dual-PDF audit

**2026-10-21 | W6 TEXT SYNCHRONIZATION APPLIED / SCIENCE FIXTURES PRESERVED / C7+C8V FINAL PENDING / W7 NOT STARTED**

## 1. Prior W5 scientific-guard issue
Previous W5 source commit `cbcacf65563c3c6b083060b1568590cddc94ede5` failed its C7/C8V main audit for fixed wording **"strictly equal"** absent from the professionally rewritten Discussion; actual H1 natural-call inequality and strict matched-call limit remain explicitly present. Old C8V also demanded the historical phrase "WARP and LambdaRank" even though the current Related Work still identifies CIKM negative-sampling corrections for training ranking losses, as distinct from incremental specialist value. Updated the C6 *semantic scientific-boundary* guard (commit `19f89d1d85ee427c185e74680921c10050effefb`) to test "strict matched-call" + explicit H1 call inequality, unverified H2 prereveal, uncorrected sampled comparator, Always Memory, and no deployment savings; updated I2 guard (commit `38ade95b8e8821ef89dc0781294af0dce1edc29e`) to test actual training-ranking-loss versus specialist-use contrast. No primary stats checks disabled. The previous C7/C8V failures are not evidence of scientific data change; **new workflow PASS not yet confirmed**.

## 2. W6 first pass: six deliberately limited publication-facing fixes
Source `SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md`, commit `7827cfc1d988cf710b9991dc767c4c0141b98b5c`:
1. Align front-matter date to 21 October 2026; retain unchanged filename because build workflows point to it.
2. Fix the broken KuaiLive exporter GitHub path from nested `manuscript/kbs_latex/src` to real `src/kuailive_agent/export_rechorus_room.py` on the project branch.
3. Replace an invalid "Results Section 6.3" with a topic-based RQ1 cross-reference that survives Results rearrangement.
4. Remove an obsolete “final combined S1–S9” statement after S10 was incorporated, while preserving exploratory DEV evidence status.
5. Rewrite S10 introduction as a map of **S10.1–14 DEV**, **S10.15 frozen same-period H1**, **S10.16/18 nested H2**, **S10.17 DEV timing**, and **S10.19 migrated supporting tables**. Do not call the entire S10 exploratory or independent TEST.
6. Explain why S10.19 stores full supporting tables after the main-text evidence and avoid project-version wording.

## 3. Scientific source preservation
- Original S1–S10.19 numeric values, H1 H2 effects, CI, calls, all S10 headings and all four source-preserving relocated tables S10.13–S10.16 unchanged.
- 1,155 Markdown source lines before/after; existing Section S10.1–S10.19 serial identifiers exactly preserved; no figures/scores/models/test reopened.
- Existing **two distinct timing protocols** S9.6 and S10.17 remain as separate measured reports and are *not* averaged or described as latest production measurements. The newer counterbalanced values remain 0.69165 and 1.76941; actual speed advantage for selective use remains unproven.
- H2 same-cohort TRAIN-only Popularity prereveal condition remains **NOT VERIFIED**; no artificial replacement with earlier DEV acceptance.

## 4. Remaining editorial backlog and limitations of W6
The full historical reproducibility archive remains lengthy and some older raw-run IDs remain in the supplement. They are retained pending a separate link-by-link evidence replacement review because deleting artifact provenance could impair reproducibility; this round did not assert a full S1–S10 thematic rewrite or remove complete results. The KBS Guide for Authors remains subject to responsibility-author verification. An optional future reorganization of S10 subsections needs a full old→new cross-reference map and fresh C6/C7/C8V science guards, not casual renumbering.

## 5. True QA status and next gate
New C7 [#39533633863](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39533633863) / C8V [#39533633988](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39533633988) for exact latest W6 supplement commit were *pending at last checked*. **Do not claim W6 PDF PASS before both completed/success, actual artifact availability and preview of changed pages.** Earlier workflow cancellation due to concurrency is neither a PASS nor data failure.

W7 front matter must be updated only after W6 factual/technical gate and re-read of rewritten whole paper; author approval and journal-specific formats remain pending. Rev3.1 KuaiRec X0-B rejected primary Big→Small experiment; NI-1g corrective-S remains NO-GO; PR #6 remains Draft; KBS not submitted.
