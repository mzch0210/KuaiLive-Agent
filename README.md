# KuaiLive-Agent

Reproducible public-data validation for **memory- and planning-augmented agents in livestream commerce recommendation**.

## Primary question
On the complete public KuaiLive release, restricted *after loading the full raw dataset* to `live_content_category == shop`, does an agentic policy with explicit short-term memory, long-term memory, temporal state, expected engagement and an anti-fatigue term improve next-streamer ranking over non-agentic and memory-only policies?

This repository is intentionally API-free: the first validation isolates the value of agent components rather than conflating it with access to a proprietary LLM.

## Data
The workflow downloads the complete `KuaiLive.zip` from the official Zenodo record `16565801`, verifies the file against Zenodo metadata, extracts it, then filters the commerce domain from `room.csv`. No dataset binary is committed to GitHub.

Primary public fields used:
- `room.csv`: `live_id`, `streamer_id`, start/end timestamps, `live_content_category`.
- `click.csv`: `user_id`, `live_id`, `streamer_id`, timestamp, `watch_live_time`.

## Evaluation protocol
- Unit: **streamer recommendation**.
- Eligibility: >=3 retained clicks per user.
- Chronological leave-one-out: last event=test, second-last=validation, earlier events=train.
- Candidate negatives: **streamers with an active room at the test timestamp**, sampled without replacement.
- Default candidate set: logged target + up to 999 active negatives.
- Primary metrics: Recall@5/10/20, NDCG@5/10/20, MRR.
- Engagement diagnostic: ranking metrics on logged test events watched >=30 seconds.
- Statistical diagnostic: paired user-level bootstrap delta in NDCG@10, `MemoryPlanner` vs `LongMemory`.

## Policies
1. Popularity
2. ShortMemory
3. LongMemory
4. MemoryFusion
5. **MemoryPlanner** = short + long + engagement + temporal affinity + popularity − recent-repeat fatigue
6. Ablations: no-short, no-long, no-time, no-fatigue

These are transparent agentic policies with the loop `perception → memory → utility planning → recommendation action`.

## GitHub Actions
`full-validation.yml` runs:
1. engineering smoke test;
2. full official KuaiLive download and verification;
3. complete data preprocessing;
4. shop-only primary experiment across three seeds;
5. result aggregation;
6. upload of all result tables as a GitHub Actions artifact.

Manual workflow inputs let you change `scope`, number of active negatives, and seeds. `robustness-all.yml` is a separate, intentionally lighter all-domain robustness check because processing every live-room interval is substantially more expensive on a CPU-only GitHub runner.

## Local run
```bash
python -m pip install -r requirements.txt
export PYTHONPATH=$PWD/src
python scripts/download_kuailive.py --data-root data
SCOPE=shop N_NEG=999 SEEDS="20260918 20260919 20260920" bash scripts/run_full.sh
```

Smoke test:
```bash
export PYTHONPATH=$PWD/src
python tests/smoke_test.py
```

## Interpretation
This is an **offline predictive validation**, not a randomized estimate of GMV uplift. Improvements support the claim that explicit memory/planning can better reconstruct logged user choices under the stated candidate protocol. Causal sales claims require randomized deployment or stronger off-policy identification assumptions.

## Next benchmark layer
The next experiment layer should add BPRMF/SASRec/TiSASRec under the *same shop-only split and candidate protocol*. ReChorus already provides those model implementations; this repository keeps the transparent Agent-vs-memory experiment independent so that failures in a deep baseline environment cannot invalidate the public-data pipeline.
