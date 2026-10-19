# N12 C8V Rev2 V2a | Single-sample target-retained top-10 label: identification and synthetic contract

Date 2026-10-19. **Standalone theoretical/synthetic audit; not observed M3 DEV labels or a corrected-S experiment.** Freeze original B1 source code and original TEST. This report adds a defensible estimate-level distinction; it does not claim to prove no useful correction exists.

## Verified source design

Original B1 `deterministic_sample` draws exactly **574 non-target candidates without replacement** from the `N-1` other eligible authors and retains observed target offline, then computes single-positive NDCG@10 from the sampled rank. The B1-2 private event label CSV includes *sampled scalar* NDCG for fixed Memory and each of SASRec/GRU4Rec; it does not store the complete sampled rank or sampled candidate-score vectors. Stable full-candidate data and replays MAY be reconstructible on authorized private DEV host, but this session has not verified that those bytes survive. Original B1-3 3-arm DEV **already exists**; Adapted is F-assisted.

## Exact probabilistic design identity

Fix one request, its pre-outcome full roster size `N`, one scoring expert `A`, a positive target's *full rank* `R`, and sampled-negative count `n=574`. Under the specified uniform-without-replacement design, the number `X` of full-rank-ahead negatives drawn among the 574 is

```
X | N,R ~ Hypergeometric(population=N−1, success=R−1, draws=n).
Pr[X=k | N,R] = C(R−1,k) C(N−R,n−k) / C(N−1,n).
sample_rank = 1 + X;
sampled_ndcg10 = 1/log2(2+X) if X <=9, else 0.
full_ndcg10 = 1/log2(1+R) if R <=10, else 0.
```

The target is always included, unlike generic candidate sampling; hence this conditional law is the actual B1 protocol. The Base and Memory share the same sampled negatives but rank them differently: their sampled label errors are **correlated**, and Delta_S is not the difference of independently sampled rank noises.

**One-sided rank fact:** `sample_rank <= full_rank` for a fixed scorer, so a target with full rank 12 (thus full NDCG@10=0) may still achieve a *positive* sampled NDCG@10.

### Public synthetic sanity case (not empirical M3)

With **synthetic N=1000, n=574, true R=12**,
- true full NDCG@10 = **0**;
- Pr(sampled rank <=10) = **0.9799134943**;
- expected sampled NDCG@10 = **0.3284950525**.

For N=575 with all N−1 alternatives sampled, sampled and full NDCG@10 coincide identically. For a full-rank-12 positive, observing positive sampled top10 utility does **not** establish positive full top10 utility.

### Narrow impossibility lemma: no *universal exact design-unbiased per-request* estimator from ONE sampled rank

Consider any numeric mapping `g(X,N)` of the ONE sampled rank only (and known N), with no external feature/prior/full-score information. The expectation `E[g(X,N)|R]` is a polynomial in `R` of degree at most `n` under the hypergeometric design (it has a finite-polynomial binomial/falling-factorial form). The desired full truncated-NDCG@K function vanishes on every full rank `R=K+1,...,N` but is positive at `R=1`. When `N-K >= n+1`, the expectation polynomial would have more roots than its degree unless identically zero, which cannot also agree at rank 1. **Therefore exact universal design unbiasedness for every R is impossible under these assumptions.**

For B1 `n=574, K=10`, this sufficient impossibility condition holds when `N>=585`. The published M3 author full-active TEST average is ~32,166 candidates, but that TEST summary must **not** be used to assert every B1 DEV request `N>=585` without checking original DEV candidate minima; the theorem is conditional on each fixed request's N. Note that sampled NDCG itself is a deterministic recoding of `X` for ranks 1–10 and an all-zero code for ranks 11–575, so `g(sampled_NDCG,N)` is **no more informative** than `g(X,N)`; impossibility for full sampled rank implies impossibility for the censored NDCG scalar.

**Scope limit:** This does NOT disprove a population-averaged bias/MSE correction, a Bayesian/prior-assisted conditional predictor, multi-sample repeated S randomization, consistent estimation across pooled users, or downstream policy improvement. It only refutes claims that one sampled NDCG scalar, even with exact N, universally recovers an exactly design-unbiased full NDCG label for every arbitrary rank when N>=585. The KDD 2020 corrections were expressly offered as **quality-improving estimators**, not necessarily unbiased per-event reconstruction: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ ; complementary treatment: https://ojs.aaai.org/index.php/AAAI/article/view/16537 .

## Synthetic code, validation contract and status

- [Source](../../analysis/kbs_plan_c/n12_c8v_v2a_sampled_rank_identifiability.py) and [tests](../../analysis/kbs_plan_c/test_n12_c8v_v2a_sampled_rank_identifiability.py) contain only math, synthetic N=1000 and no private/user data.
- [CI #39228504534](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39228504534) independently runs probability normalization, toy top10 censoring, full-sample parity, sufficient impossibility threshold and invalid-input guards. **CI outcome verified: SUCCESS (one job; synthetic tests PASS), distinct from prior V0/I0 CI.**
- **Current interpretation:** corrected-S V2a is STILL `HOLD_PRIVATE_DEV_AND_ESTIMATOR_SPEC`, because a correct per-event estimator and existing private data availability are unverified. Scientific V2b remains **NOT AUTHORIZED**. Avoid filling the missing private input with frozen 30k H1 data, and do not claim this mathematical check supplies a new independent dataset.

## Residual V2a decision requirements

1. An authorized self-host researcher must confirm whether original B1 `klm3_g3_dev_fullactive_base_memory_corrected_v1`, `klm3_plan_c_g1_v1`, `klm3_g2_seed20261012_epoch3_v1`, original F DEV CSV and B1-2 SHA `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea` exist **without opening TEST**. Verify manifests/columns and exact sampled-label parity under original deterministic sampler, only in DEV.
2. Independently define corrected-S as aggregate metric estimator, conditional Base-relative utility label estimator or policy optimization, and state admissible prior information. In particular an F-label-assisted mixture is not sampled-only.
3. Only if a legitimate corrective method is both identifiable under declared information and scientifically tests a still-open alternative, preregister new DEV-only synthetic+three-arm protocol separately. Otherwise mark V2b `NOT_RUN_BY_DESIGN` with reason.

**I0 update:** Original Twitch one-shot P1.3 TEST #35708072303 and room primary 10,222 #37746520476 + factorial #37751814645 have been verified and placed in the public-source ledger. No original TEST was reopened in this turn.
