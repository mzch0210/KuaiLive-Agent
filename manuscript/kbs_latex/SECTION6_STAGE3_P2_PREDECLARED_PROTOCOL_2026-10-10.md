# Section 6 Stage 3 — P2 prespecified fixed-checkpoint candidate sampling protocol

**Registration status:** Recorded **before the first new P2 scoring run**. This is a retrospective diagnostic on previously inspected KuaiLive TEST data, **not** a new untouched held-out experiment, a preregistered prospective clinical-style analysis, or a new training policy. No results were observed when fixing these sizes/seeds/criteria.

**Scientific claim:** C2 in the approved KBS outline, subject to the already demonstrated matched sampled-575 versus full-active fixed-checkpoint contrast. Supplementary S5/S8 is the intended reporting destination; main Section 6.3 will be revisited only after the *complete* set of signs and protocol deviations is examined.

## 1. Feasibility evidence, verified at preparation

- Preserved **original seed 20260918 Room checkpoint** in [same-checkpoint run 37746520476](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476), artifact **11536890439**, SHA256 **b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7**.
- Preserved **original Streamer checkpoint**, same artifact, SHA256 **82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945**.
- Preserved data artifact **11534262601**, source P0 and original 3-seed results archive **11538678848**; input train, DEV, TEST SHA256 respectively **ad91413537175b9f6e9013c525a552b6004cc00e029b41360f08519e0735b5b4**, **46dd3081688468c89acf6366d36d87c122fa45850ddb69320c05da9de94a9f54**, **3491862df4de5cfb487fbd21c2f62c2d1d62acac110f852cc83c019dfcc6e956**.
- Hash verification of **both original model files and all three original input files PASSED**, using the actual downloaded archive bytes. The previously completed [fixed-checkpoint factorial run 37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645) is the scientific P0/P1 baseline.
- Historical results archives contain **event-level utility** and all four paired factorial cells, **not** raw full-candidate logits. The P2 evaluator must score each original full-active candidate set **once per event**, verify archived historical per-user scores **exactly**, and only then generate new candidate draws.

## 2. Frozen scientific estimand, models, candidate population

- Cohort: exactly **10,222** KuaiLive TEST user–time–target events; original chronology and target unchanged.
- Ranking unit: live **room**, relationship Memory indexed by the room's streamer; no model training; same 0.45/0.45/0.10 fixed expert and original P0 checkpoint pair.
- Fusion: **room alpha 0.125**, streamer 0.875, unchanged; per-branch sample-specific z-score as the original SS protocol. The full-active FF Base is unchanged.
- Candidate pool for each event: rooms active at the event step, half-open session availability, with target included if metadata flags it inactive. Draw candidates uniformly **without replacement** from this exact original full-active set *excluding only the current target*. The positive remains included and the original full-active population is not redefined.
- **Important data finding:** In the original 575-list, sampled negative room IDs sometimes also occur in that user's **prior interaction history** (601 repeated negative–prior-room intersections over 433/10,222 users). Hence it would change the historical scientific protocol to exclude *all* previously clicked room IDs from the newly generated candidates. "Unobserved negatives" means not the observed target in that event; do not silently substitute a never-previously-interacted restriction.
- Conditions: sampled candidate totals **128, 256, 575** (including one observed target); **original archived 575** retained as a separate fixed reference; full-active is an unchanged benchmark, not an additional random draw.
- Three independent, prespecified negative-list RNG streams: **20261010, 20261011, 20261012**. Use NumPy Generator sampling for each event in chronological event order and candidate-size order **128, 256, 575**, without selecting, replacing or pruning seeds by outcome. Total **nine** new full-cohort sampled conditions plus original 575 and full-active.

## 3. Hard reproducibility and abort guards

1. All original model/data SHA256s, cohort uniqueness, original 575 candidate inclusion/nested-in-full and target membership MUST pass.
2. Reconstructed Base-SS, Base-FF, Memory-sampled, Memory-full, delta-SS and delta-FF MUST reproduce **the entire 10,222-user original P0 report** at absolute tolerance 1e−11, not merely the group means. Group means must also reproduce P0 expected NDCGs/shift to 1e−10.
3. For each event, compute the full Base branch logits and Memory scores once, and use exact indexed subsets for all new candidate draws. Keep the same scoring, target-rank conventions and room-ID tie behavior.
4. Every random sample must contain the target exactly once and exactly \(k-1\) unique eligible active negatives; full candidate availability must support the original 575-set.
5. Evaluate sampled SS and the reference-crossed 2x2 if feasible; the membership and normalization allocations must sum to FF−SS **for each event**.
6. **Fail closed**, with original training/TEST left untouched, on any missing artifact, hash mismatch, per-user rank mismatch, candidate eligibility failure, non-finite scores or ID collision. Do not present a partial successful-looking subset as a full result.

## 4. Primary summary and statistical design

The **primary descriptive quantities** for each of the nine predeclared conditions are (i) mean Memory−Base NDCG@10 on identical users and (ii) paired FF−sampled shift; compare separately with the *original historical 575* reference. Report both signed mean and the count of draws yielding negative sampled delta / positive shift. Do not collapse across sizes into one "confidence" test.

The paired user-level percentile bootstrap has **3,000 resamples**, seed **20261343**, reusing the same row-resample indices across all new policies; intervals condition on the already trained and fixed model, original TEST event set, exact sample draw and decisions. Provide additional between-draw range/SD by candidate size as **descriptive sampling heterogeneity**, explicitly separate from user-bootstrap uncertainty and the prior P1 between-trained-checkpoint SD.

The crossed candidate membership vs score-normalization decomposition is a **descriptive algebraic allocation**, not independent randomized causal effects. Even at fixed model parameters, candidate count, individual negative membership, ranking difficulty, and score-reference moments may vary together. The results test sensitivity of **this fixed KuaiLive evaluation protocol**, not an external general sampled-metric law. No multiple-testing-adjusted simultaneous intervals will be claimed; all intervals are pointwise exploratory.

**All nine results must be reported**, including non-reversing or null conditions. If any sample size or RNG draw changes the original sign pattern, narrow the conclusion rather than discarding the draw. Do not select a new alpha, Memory mixture or selector threshold using already examined TEST.

## 5. Safety and resource constraints

Existing self-hosted GPU runner in the project has explicit owner-only, manually confirmed execution guards. **Do not bypass those guards.** If automated execution is desired, use only an ephemeral GitHub-hosted **CPU** runner with actions read-only permission; no owner private GPU or secret tokens are needed and no checkpoints are published in results artifacts. Keep the original archived binary checkpoints in their existing artifacts; outputs should contain **only reports/derived per-user numerical data**.

**Planned source:** [analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py](../../analysis/kbs_kuailive_p2_fixed_checkpoint_sampling.py). The original benchmark is an inspected historical TEST population. A completed hosted run is required before labeling P2 "executed"; archival feasibility alone is not a result.

**External methods:** Krichene and Rendle, *On Sampled Metrics for Item Recommendation*, *Communications of the ACM* 65(7), 75–83 (2022), DOI 10.1145/3535335. This established sampled-metric ordering issue is prior literature, **not** claimed as the paper's contribution.
