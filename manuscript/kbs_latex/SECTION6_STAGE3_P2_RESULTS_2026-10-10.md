# KBS Section 6 Stage 3B — Fixed-checkpoint KuaiLive P2 candidate-draw results

**Date:** 2026-10-10  
**Status:** **COMPLETED**, with exact archived P0 replication and all nine predeclared candidate-draw conditions.  
**Executed original-model workflow:** [GitHub Actions run 38014145900](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900), status **success**, git SHA \`d88222e924e6c66bdaf27cb1700fad8309284a05\`, artifact [11655273833](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900/artifacts/11655273833) (\`kuailive-p2-frozen-candidates-38014145900\`).  
**Predeclared protocol filed before scoring:** [P2 protocol](SECTION6_STAGE3_P2_PREDECLARED_PROTOCOL_2026-10-10.md); scientific feasibility audit: [3A](SECTION6_STAGE3_3A_FEASIBILITY_AND_SCIENTIFIC_BOUNDARIES_2026-10-10.md).  
**Code:** [analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py](../../analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py), [hosted CPU workflow](../../.github/workflows/kbs-kuailive-p2-fixed-candidate-draws.yml).  
**Evidence status:** RETROSPECTIVE sensitivity on **previously inspected KuaiLive TEST**, not a new independently untouched confirmation. Models, alpha, Memory, user events, observed targets and original 575/full candidates were never reselected or retrained.

## 1. Scientific validation gates passed

1. Full same-user cohort exactly **10,222 unique TEST users**, no missing numeric values in the archived **10,222 × 65** paired per-event outcome table.
2. The two original Room/Streamer SASRec model files were loaded with exact original SHA256 identities, and train/DEV/TEST data byte hashes matched historical frozen inputs.
3. Every original P0 user-level Base-SS, Base-FF, Memory-S, Memory-F, delta-SS and delta-FF **exactly reproduced within the preregistered 1e−11 tolerance**, before calculating new P2 conditions. Original 575 Base **0.6070915752**, Memory **0.5658874643**, Memory−Base **−0.0412041108**; full-active Base **0.3857124230**, Memory **0.4320191095**, Memory−Base **+0.0463066865**; paired full-minus-original sampled **+0.0875107973**.
4. **Nine of nine** prespecified conditions (three total positive-inclusive candidate sizes × three fixed draw RNGs) scored and archived; no favorable seed selection, repeated training, post hoc alpha changes or exclusion of unfavorable draws.
5. All per-user 2×2 allocation identities hold; each reported difference is a paired fixed-checkpoint *scoring-protocol allocation*, not a causal candidate-count effect.
6. Original source negatives allow previously interacted rooms as long as they are at-time eligible and not the current positive. New uniform draws use exactly this eligibility definition. Historical 575 negatives overlapped earlier room histories in **433 of 10,222 users**; these are not silently excluded.

## 2. Every prespecified candidate condition

All values are mean **Memory−Base NDCG@10**, scored on the SAME 10,222 original users. Full-active serves as the *same fixed* reference for all sampled draws.

| Candidate total, including target | Draw seed | Sampled Memory−Base | Full Memory−Base | Paired Full−Sampled |
|---|---:|---:|---:|---:|
| **128** | 20261010 | −0.080377 | +0.046307 | **+0.126683** |
| 128 | 20261011 | −0.079852 | +0.046307 | **+0.126159** |
| 128 | 20261012 | −0.079260 | +0.046307 | **+0.125566** |
| **256** | 20261010 | −0.067800 | +0.046307 | **+0.114107** |
| 256 | 20261011 | −0.068593 | +0.046307 | **+0.114899** |
| 256 | 20261012 | −0.067581 | +0.046307 | **+0.113888** |
| **575** | 20261010 | −0.042189 | +0.046307 | **+0.088495** |
| 575 | 20261011 | −0.040922 | +0.046307 | **+0.087229** |
| 575 | 20261012 | −0.041621 | +0.046307 | **+0.087927** |
| Original frozen **575** | historical set | **−0.041204** | **+0.046307** | **+0.087511** |
| **Full-active** | original full set | **+0.046307** | **+0.046307** | 0 |

**Qualitative result:** **All 9/9 new sampled draw means are negative**, whereas the shared full-active Memory−Base mean is **positive**. Thus **all nine full-minus-sampled contrasts are positive**. This extends the original paired inversion from its single frozen sampled-negative draw to the **three predeclared draws for each of the three sample sizes** under the *same frozen checkpoint pair*. It does **not** prove a distribution-free statement about every possible negative-sampling list or other ranking models.

### Between-draw descriptive summaries

| Candidate total | Mean sampled Memory−Base across the three fixed draws | Min to max sampled Memory−Base | Mean full−sampled across draws | Full−sampled range |
|---|---:|---:|---:|---|
| 128 | **−0.079829** | [−0.080377,−0.079260] | **+0.126136** | [+0.125566,+0.126683] |
| 256 | **−0.067991** | [−0.068593,−0.067581] | **+0.114298** | [+0.113888,+0.114899] |
| 575 | **−0.041577** | [−0.042189,−0.040922] | **+0.087884** | [+0.087229,+0.088495] |

Across these **three fixed draws per size**, the smaller sampled set is associated with a more negative Memory−Base contrast. However, changing size also changes candidate membership, difficulty and normalization reference; this numerical trend is **not causal evidence of candidate count in isolation**. The 3 draws share users and checkpoints and must not be misrepresented as independent dataset replications.

## 3. Conditional paired user-bootstrap uncertainty

The original P2 protocol uses **3,000 paired user resamples**, sharing each resampled-user index across all ranking variants. Pointwise 95% percentile intervals conditional on original models/users/draws exclude zero for all new sampled Memory−Base contrasts and their corresponding full−sampled shifts. Illustrative full run values:

- 128, seed 20261010: sampled Δ = **−0.080377**, 95% user-paired CI **[−0.086764,−0.073864]**; full−sampled = **+0.126683**, CI **[+0.119936,+0.133530]**.
- 256, seed 20261010: sampled Δ = **−0.067800**, CI **[−0.074253,−0.060869]**; shift **+0.114107**, CI **[+0.107907,+0.120613]**.
- 575, seed 20261010: sampled Δ = **−0.042189**, CI **[−0.048747,−0.035141]**; shift **+0.088495**, CI **[+0.082897,+0.094078]**.
- Original 575: sampled Δ **−0.041204**, conditional original-data CI **[−0.047850,−0.034175]** from this particular replay's bootstrap RNG. The mean is identical to P0; confidence interval draws are not required to be identical across historical bootstrap RNGs.
- Shared full-active: Δ **+0.046307**, conditional CI **[+0.039990,+0.053289]**.

Full pointwise intervals for **each of the nine exact draws**, and each per-draw two-factor allocation, are in the attached **p2_user_bootstrap.csv**. They **do not cover** independent new checkpoints, unseen sampled-negative populations, choice of the three seeds/sizes, refitting or multiplicity. Between-draw min/max in Section 2 is descriptive, not a confidence interval.

## 4. Decomposition diagnostics

Each full−sampled shift is algebraically allocated to ranked-candidate membership versus branch z-score reference using the established 2×2 protocol. Averaged across the three predetermined draws, these are approximately:
- **128:** membership +0.1290, normalization −0.0029;
- **256:** membership +0.1159, normalization −0.0016;
- **575:** membership +0.0886, normalization −0.0007.

The reference-only normalization term remains much smaller in magnitude than the ranked-membership allocation for this design, but does not justify a causal interpretation. All 2×2 per-user identities were rechecked and no mismatches found.

## 5. KBS acceptance-oriented interpretation and next steps

**Contributes bounded robustness to C2.** This experiment closes the exact fixed-checkpoint P2 gap identified in the first six-issue audit: three independent **candidate draw RNG streams at each of three positive-inclusive sample sizes**, while preserving exact original P0 model/data/cohort identities. A useful manuscript-compatible statement is:

> On the previously inspected KuaiLive TEST users, a fixed-checkpoint negative-candidate sensitivity replay preserved the sign of the sampled-versus-full Memory−Base inversion for all nine prespecified sampled sets (128, 256 and 575 candidates; three draws per size). The result remains a descriptive evaluation-protocol finding rather than a new independent held-out test, a causal attribution to candidate-set size, or a general sampled-ranking theorem.

**Recommended placement:** one concise robustness sentence in §6.3 *after independent KBS reviewer-style tightening*; a complete per-draw table and sampling/protocol explanation in Supplementary S5 with archived run/artifact links. Keep S8's three trained-model seed analysis distinct from the three sampled-negative RNG streams here. Do not modify C1/C3, any frozen Twitch TEST policy, expert weighting, thresholds, or causal statements. An author/reviewer can choose to keep all P2 details in S5 and simply cross-refer from §6.3.

**Provenance files in original artifact 11655273833:**
- \`p2_predeclared_draws.csv\`: all 9 prespecified mean observations.
- \`p2_user_bootstrap.csv\`: 3,000-user-replicate conditional mean/CI for full, original sampled, nine sampled configurations, 2×2 membership and normalization allocations.
- \`p2_per_user_fixed_checkpoint.csv.gz\`: complete 10,222-user paired outcome matrix (65 columns, no missing values, all candidate-score 2×2 identities passed).
- \`p2_protocol_and_provenance.json\`: pinned model/data SHA256, original P0 exact replay, negative eligibility, fixed counts/seeds and limitations.

**Execution history:** Two preliminary hosted workflow attempts failed **before model scoring** due to cross-run artifact and extraction-directory configuration. Their run records are preserved as [38013914045](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38013914045) and [38014023961](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014023961); neither supplied exploratory scientific results or informed seed/size selection. The third run **38014145900** completed all predeclared scientific checks without any post-result modification.
