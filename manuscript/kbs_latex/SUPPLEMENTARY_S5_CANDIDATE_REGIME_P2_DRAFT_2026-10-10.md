# Supplementary S5 — Paired candidate-regime factorization and fixed-checkpoint negative-draw sensitivity

**Status:** KBS scholarly supplement **draft**; scientific values independently rechecked from completed original artifacts, but not yet author-approved or journal-typeset.  
**Scientific contribution:** C2, operational candidate-regime dependence of a fixed specialist's *Base-relative NDCG@10*, not a new generic sampled-metric theorem.  
**Source of original paired 2×2:** [20260918 P0/P1 run 37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645), result artifact 11538678848.  
**Source of additional sensitivity:** [precommitted P2 protocol](SECTION6_STAGE3_P2_PREDECLARED_PROTOCOL_2026-10-10.md), [hosted-CPU run 38014145900](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900), immutable code version d88222e924e6c66bdaf27cb1700fad8309284a05, [four-file result artifact 11655273833](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900/artifacts/11655273833).  
**Inference status:** Retrospective analysis of the **previously inspected** KuaiLive TEST population, not independent held-out testing. No policies, model weights, fusion parameters or thresholds were trained or retuned for P2.

## S5.1 Matched experiment identity and safeguard checks

We preserve **n=10,222** one-target-per-user KuaiLive evaluation events, the original Room- and Streamer-SASRec checkpoints from seed 20260918, eligible history, target timestamps, candidate availability logic, Memory rule and fusion coefficient (room 0.125; streamer 0.875). The complete full-active candidate set is defined at each event time; metadata reports that every observed target was active. The full-active set has **575–13,266 eligible rooms per event** (mean **8,269.11**, median **8,131.5**), with each positive target included exactly once.

The original fixed 575 protocol and full-active protocol are first reproduced **user by user**, comparing six archived event-level scores: sampled/full Base, sampled/full Memory, and their two differences. The original-data equality guard passes at absolute tolerance 1e−11; these results **must be replicated before** new sampling. Original model hashes: Room \`b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7\`, Streamer \`82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945\`; train, DEV and TEST dataset SHA256s are in the original P2 provenance manifest.

The negative-sampling pool follows the original exporter: **active eligible rooms except the current positive target**. It does not exclude all earlier user interactions; the original 575 lists contain prior-history negative intersections for 433 unique users. Changing this definition would alter the original tested protocol. New samples are uniform without replacement from this time-specific pool; the observed positive is always added. P2 samples only from the frozen **full-active score vectors** and does not retrain or re-encode any user per draw.

## S5.2 Original P0 matched factorial benchmark

For fixed original sampled candidates S (575 items including the target) nested in full-active F, the original paired contrast is:

| Ranked candidate set | S z-score reference | F z-score reference |
|---|---:|---:|
| S | −0.04120411 | −0.04141760 |
| F | +0.04761085 | +0.04630669 |

Entries are mean **Memory−Base NDCG@10**. Native S/S uses Base 0.60709158 and Memory 0.56588746; native F/F uses Base 0.38571242 and Memory 0.43201911. The within-event F/F minus S/S difference is **+0.08751080** (original paired bootstrap 95% CI **[+0.08210,+0.09326]**, 3,000 user resamples). The two-order algebraic allocation is ranked-candidate membership **+0.08826963** and branch z-score normalization reference **−0.00075883**, summing exactly to the native shift. The crossed S/F and F/S configurations are **analytical**, not independent operational policies or causal interventions.

## S5.3 Prespecified new candidate-draw protocol

The P2 sizes and RNGs were committed before the first scored outcome: **128, 256, 575 candidate rooms including one positive**, with **three independent prespecified RNG streams** 20261010, 20261011 and 20261012 for each size. The **original 575 negative list** is separately preserved as a reference; full-active is the same fixed reference under all new draws. A total of nine new full-cohort candidate conditions were computed. Original checkpoints, Base/Memory logits, historical events, active-room eligibility, preprocessing and alpha remain unchanged. No seed, user or condition was selected based on its result.

A 3,000-resample user-paired percentile bootstrap (same user indices across compared policies) gives **pointwise conditional CIs** for each draw's Memory−Base mean and full-minus-sampled shift. These intervals condition on original models and observed users; they do not incorporate the choice of candidate sizes/draw seeds, hypothetical independent negative-draw distributions, model fitting or TEST selection. There is **no familywise multiplicity adjustment**.

## S5.4 All nine P2 outcomes

| Sample size (positive included) | Draw seed | Base NDCG@10 | Memory NDCG@10 | Memory−Base | 95% CI for Memory−Base | F/F − sampled | 95% CI for F/F−sampled |
|---|---:|---:|---:|---:|---|---:|---|
| **128** | 20261010 | 0.726025 | 0.645648 | **−0.080377** | [−0.086764, −0.073864] | **+0.126683** | [+0.119936,+0.133530] |
| 128 | 20261011 | 0.726010 | 0.646158 | −0.079852 | [−0.086162, −0.073125] | +0.126159 | [+0.119471,+0.133256] |
| 128 | 20261012 | 0.726867 | 0.647608 | −0.079260 | [−0.085593, −0.072616] | +0.125566 | [+0.118770,+0.132659] |
| **256** | 20261010 | 0.675502 | 0.607702 | **−0.067800** | [−0.074253, −0.060869] | **+0.114107** | [+0.107907,+0.120613] |
| 256 | 20261011 | 0.676118 | 0.607526 | −0.068593 | [−0.075296, −0.061703] | +0.114899 | [+0.108514,+0.121534] |
| 256 | 20261012 | 0.674257 | 0.606676 | −0.067581 | [−0.074182, −0.060755] | +0.113888 | [+0.107533,+0.120214] |
| **575** | 20261010 | 0.607331 | 0.565142 | **−0.042189** | [−0.048747, −0.035141] | **+0.088495** | [+0.082897,+0.094078] |
| 575 | 20261011 | 0.607060 | 0.566137 | −0.040922 | [−0.047656, −0.033802] | +0.087229 | [+0.081500,+0.092836] |
| 575 | 20261012 | 0.606207 | 0.564586 | −0.041621 | [−0.048239, −0.034708] | +0.087927 | [+0.082273,+0.093542] |
| Original **575** | Original historical list | 0.607092 | 0.565887 | **−0.041204** | [−0.047850, −0.034175] | **+0.087511** | original P0 bootstrap: [+0.08210,+0.09326] |
| **Full-active** | Original complete population | 0.385712 | 0.432019 | **+0.046307** | [+0.039990,+0.053289] | 0 | — |

The original-575 and full-active CIs above are P2's **conditional resample** estimates except where the original P0 interval is expressly identified; the original-575 shift CI is from the original P0 rather than implying an independently fixed rerun confidence band. All signed P2 means have been recomputed directly from the archived **10,222 × 65** per-user outcome matrix, with no missing or duplicated events.

All **nine** prespecified sampled candidate means are negative and all F/F minus sampled means positive. Within each size, the between-draw mean (and min–max over just three draws) is:

| Sampled size | Mean sampled Memory−Base across draws | Observed three-draw range | Mean F/F−sampled | Range of F/F−sampled |
|---|---:|---|---:|---|
| 128 | −0.079829 | [−0.080377,−0.079260] | +0.126136 | [+0.125566,+0.126683] |
| 256 | −0.067991 | [−0.068593,−0.067581] | +0.114298 | [+0.113888,+0.114899] |
| 575 | −0.041577 | [−0.042189,−0.040922] | +0.087884 | [+0.087229,+0.088495] |

These ranges are **descriptive**, not empirical 95% sampling-distribution CIs or independent dataset replicates; all runs reuse the same checkpoint and TEST users.

## S5.5 Scoring-reference allocation under independent draws

For each sample size and draw, the crossed 2×2 design yields an event-level algebraic identity:

\[
\Delta_{FF}-\Delta_{SS}
= A_{\mathrm{membership}}+A_{\mathrm{normalization}} .
\]

Across the three fixed draws per size, the means of these **descriptive path-averaged terms** are:

| Sampled size | Candidate-membership allocation | Score-normalization-reference allocation | Net full-minus-sampled shift |
|---|---:|---:|---:|
| 128 | +0.129023 | −0.002887 | +0.126136 |
| 256 | +0.115923 | −0.001625 | +0.114298 |
| 575 | +0.088562 | −0.000678 | +0.087884 |

The allocation algebra is checked on **every original user and every new draw**, maximum numerical identity discrepancy on the order of machine epsilon. "Membership" encompasses count, which negative items are included, the available rank competition and consequent scoring task difficulty; this table **cannot causally separate** those mechanisms. Likewise, z-score-reference terms should not be conflated with a controlled rank-normalization intervention in the live system.

## S5.6 Interpretation for C2 and relation to related literature

This controlled fixed-checkpoint replay strengthens the **bounded** original C2 finding: the sign reversal between the specified sampled-active and full-active candidate regimes persists over the nine inspected negative lists across three positive-inclusive sample sizes. The result **does not** establish universality over all draws, user populations, models or platforms; repeated negative draws on the *same* events are not independent TEST replications. The shared full-active reference makes the sign check transparent, not an independent benchmark.

The known general fact that sampled ranking metrics can invert model orderings is due to prior work (Krichene and Rendle, *On Sampled Metrics for Item Recommendation*, CACM 65(7):75–83, 2022, DOI 10.1145/3535335; original KDD 2020). Our result is about the **observed Base-relative utility of a fixed interpretably scored relationship specialist on KuaiLive rooms**, not a new sampled-metric theorem, new gate training method, or causal attribution to sample count.

**Submission organization:** One concise robustness paragraph appears in Results Section 6.3; all per-draw outcomes, confidence intervals, original rank reproduction and factorization belong here. The three alternative *training*-seed model realizations are reported separately in S8, not as nine new independent checkpoint seeds. This supplement is prepared for later unified S1–S9 submission formatting; coauthor verification and publisher-ready cross-reference packaging are still open.

## S5.7 Archive manifest and exact source protocol

- Original factorial run/artifact: 37751814645 / 11538678848.
- P2 source commit and run: d88222e924e6c66bdaf27cb1700fad8309284a05 / 38014145900.
- P2 archived artifact: **11655273833**, \`kuailive-p2-frozen-candidates-38014145900\`.
- \`p2_predeclared_draws.csv\`: all nine sample-size/seed condition means.
- \`p2_user_bootstrap.csv\`: fixed-draw 3,000-user-bootstrap conditional per-draw CIs and crossed-factor allocation intervals.
- \`p2_per_user_fixed_checkpoint.csv.gz\`: complete 10,222-user/65-column score matrix, actual archived Base/Memory values and paired contrasts.
- \`p2_protocol_and_provenance.json\`: model/data checksums, source run IDs, eligibility, sample sizes, RNG streams and whether original P0 replay passed.
- [Predeclared design](SECTION6_STAGE3_P2_PREDECLARED_PROTOCOL_2026-10-10.md), [scientific audit](SECTION6_STAGE3_P2_RESULTS_2026-10-10.md), [source code](../../analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py).

The first two GitHub-hosted workflow attempts failed **before model scoring** because of incorrect cross-run artifact selection/extraction options; the third run performed all hard guards. This execution history is fully retained to prevent conflating code/infrastructure retries with scientific draw retries.
