# R3 — Experimental Results revision and source-backed acceptance

**Date:** 2026-10-12. **Decision:** R3 PASS for Section 6; paper-wide submission remains HOLD until R4–R8. No frozen experiments, model checkpoints, DEV thresholds, or TEST outcomes were modified.

## Source and PDF

- Canonical source: [main.tex](main.tex), GitHub blob SHA 10c7bdf2b89795c747c8d2db8dc885e2eb94050c. Results integrated at commit c4a82e3277cad90faac80f2765f0333ea94f81f8; final numerical rounding corrected at commit 0e3789a023e2ca7b9c51f5d35f621f272f6c9cf5.
- Final [GitHub Actions LaTeX build #38237393777](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38237393777) **SUCCESS**. Artifact ID 11741412494 contains PDF and logs; original PDF 34 pages, 489,109 bytes. No overfull boxes, undefined LaTeX references or missing citations in final log. Earlier 31-page R2 manuscript has grown by three pages; further display density/float management is an explicit R7/R8 editorial item.
- PDF pages 17–25 and the three new M3 tables on pages 21, 23 and 25 were visually inspected in the R3 audit; no visible table clipping. Existing Twitch state figure/table, Twitch policy table, original KuaiLive paired regime table and DEV feature ablation all survive.

## Source numeric verification: original artifacts downloaded and inspected

Independent R3 source check **unpacked the actual aggregate.json** from the [G5-B one-shot TEST action #38226690320](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38226690320), artifact 11735868084, and the [G4 DEV warmed-cost action #38223495966](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38223495966), artifact 11734923392. The accepted summary report alone was **not** treated as proof of all values. Private event-level TEST outcomes were not reopened or recomputed.

### M3 frozen TEST: same 47,575 events and 12,533 users

| Base fit | Base NDCG | Utility NDCG | Utility minus Base | Utility minus Uncertainty | Utility TEST calls |
|---|---:|---:|---:|---:|---:|
| SASRec 20261012 | 0.258004 | 0.302866 | +0.04486 | +0.01349 | 29.21% |
| SASRec 20261013 | 0.258811 | 0.301766 | +0.04296 | +0.01363 | 27.72% |
| SASRec 20261014 | 0.258673 | 0.303058 | +0.04439 | +0.01368 | 28.21% |
| GRU4Rec 20261012 | 0.260033 | 0.304004 | +0.04397 | +0.01311 | 28.87% |
| GRU4Rec 20261013 | 0.260649 | 0.303016 | +0.04237 | +0.01301 | 28.65% |
| GRU4Rec 20261014 | 0.258400 | 0.303549 | +0.04515 | +0.01431 | 29.10% |

Source verified two final 5-decimal rounding corrections, SASRec 20261013 +0.04296 and SASRec 20261014 +0.04439. All six models have Utility above Base and above the four M3 competitor gate objectives, but six independently fitted checkpoints evaluated on the same event cohort are **not six independent population samples**.

For primary seed SASRec 20261012: Always Base **0.258004**; fixed Always Memory **0.346792**; Utility **0.302866** (29.2149% TEST calls); Difficulty **0.282479** (29.9044%); Specialist **0.279558** (29.5681%); Uncertainty **0.289373** (30.1797%); History **0.279789** (35.4724%). M3 policies used a **DEV** at-most-30% threshold-selection constraint and were then pointwise frozen; they did **not** receive equal or capped actual TEST call counts. Strongest secondary alternative is the specified Base-margin Uncertainty proxy, **not** a reimplementation of the GUIDER algorithm.

Primary seed Utility-minus-Base paired gain is **+0.044862**, 95% user-cluster CI [0.042805,0.046915]; minus Difficulty **+0.020387**, CI [0.018370,0.022442]; minus Specialist **+0.023308**, CI [0.021177,0.025508]. Each six-model-seed condition has **three predeclared one-sided tests**, 5000 paired user-cluster bootstraps, 5000 cluster sign randomizations and its own **three-test Holm correction**; adjusted p is 0.00059988 (simulation floor) for each of 18 individual results. This does not establish globally protected familywise significance across all 18 tests, and relies on a sign-symmetry assumption. Utility-minus-Uncertainty is a **secondary** comparison. Full intervals await S8 during R6.

Unconditional Memory **0.346792 NDCG@10** beats all Utility methods on absolute quality; main text reports this prominently. Oracle@30 **0.388135** is a hindsight nondeployable reference, Random@30 **0.284640** is a conditional random expectation, not a tested frozen policy.

### Cost source and adverse evidence

G4 original RTX3090 warmed offline DEV replay on **256** already-prepared M3 events: Always Base mean/median **1.4245 / 0.8317 ms**, Always Memory **0.8033 / 0.7744 ms**, Utility selective **1.8018 / 1.6778 ms**, with 80/256 = **31.25%** Memory calls. Memory is both more accurate on the full M3 TEST and cheaper on this limited warmed DEV benchmark. Missing from benchmark: historical state maintenance, candidate interval construction, IO/network, batch serving and contention; execution order/warm-up affects path means. **No demonstrated production end-to-end speedup or actual external budget necessity.**

Original KuaiLive room 575-candidate warmed **CPU** replay is a separate setting: Base 0.991 ms and selective HGB 2.007 ms, 14.25% Memory calls. Do not merge or pool the two hardware settings or Twitch 15.04% selection rates into an imaginary common deployment.

### Old conclusions retained accurately

- Twitch streamer frozen TEST n=44,221: Base 0.58211, Memory 0.53980, Utility 0.58983 at 6,650 Memory calls (15.04%), retrospectively TEST-count-matched Difficulty 0.58340 and hindsight Oracle 0.64806. Primary paired Utility-minus-Base 95% CI [0.00641,0.00903], Utility-minus-Difficulty [0.00528,0.00762].
- Old KuaiLive **room** n=10,222 paired targets, sampled 575 rooms Memory-minus-Base −0.04120 versus full-active +0.04631, paired shift +0.08751, CI [0.08210,0.09326]. Candidate/reference four-cell allocation preserved and presented only as retrospective ranking-regime diagnostics.
- Twitch 14-feature fivefold OOF DEV ablation and Memory component/context length checks remain descriptive, not independent M3 TEST replication.

## Section 6 revision details

- **6.1:** Twitch fixed Memory negative aggregate plus recoverable-target benefit; M3 fixed Memory positive aggregate versus six fitted author Bases; different tasks/incumbents/candidates prevent a single-factor causal explanation.
- **6.2:** Two different frozen TEST selection settings; new M3 primary-seed five-gate + Always Base/Memory full-active table with **realized TEST call percentages**, three registered paired contrasts/Holm and descriptive hindsight upper bound.
- **6.3:** Unchanged original paired KuaiLive room candidate-regime and crossed-reference analysis, explicitly distinct from M3 author task and its 575-author DEV checkpoint screening.
- **6.4:** New six-fit M3 heldout results table plus old Twitch DEV feature-family and Memory-component diagnostics; same-cohort fitted-model dependence and primary/secondary inference status explicit.
- **6.5:** Separate CPU and 3090 warmed replay paths, negative observed overhead and strong unconditional Memory comparisons; no 70% real hardware cost-savings claim.

Scientific prose remains results-oriented and does not chronicle GitHub jobs, patch operations or experiment debugging inside the manuscript.

## R0 P0/P1 issue state

The [updated R3 twelve-issue tracker](R3_R0_P0_P1_ISSUE_CLOSURE_TRACKER_2026-10-12.json) documents each source conflict and its next closure stage. None is falsely marked closed paper-wide:

- **P0-01/02:** R2–R3 now distinguish all three protocols and the two frozen selection tests; R5 and R6 still need to update introduction/discussion/conclusion and supplement.
- **P0-03:** R2–R3 correct DEV budget versus actual M3 TEST rate; R4 must align problem formulation; R6 S7 all rates.
- **P0-04:** R3 formally includes Always Memory and measured cost counterevidence; R5 §7 discussion and R6 S9 are still pending.
- **P0-05:** R2–R3 distinguish ranked units/features; R4 §4 must align implementation and R6 S1–S3.
- **P0-06:** R2–R3 specify per-fit three-Holm and cluster tests; R6 S8 full CI provenance.
- **P1-01/02:** hash/tie rules appear in R2 §5 but need R6 S1–S2 full details.
- **P1-03:** stale S1–S9 frozen-policy scope awaits R6.
- **P1-04:** novelty versus established Learning-to-Defer and KBS gating awaits R5/R7.
- **P1-05:** superseded DEV/TEST status text awaits R6.
- **P1-06:** stable privacy-respecting artifact persistence awaits R6/R8.

**R3 status = PASS. Whole manuscript submission status = HOLD. NEXT: R4 targeted §3–4 formalism/implementation bridge**, then R5 §1–2/§7–8, R6 S1–S9, R7 originality referee audit, R8 final PDF and authors' declarations.
