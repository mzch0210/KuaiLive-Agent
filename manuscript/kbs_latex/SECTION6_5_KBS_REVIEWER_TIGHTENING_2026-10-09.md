# Section 6.5 — KBS reviewer-style tightening and source audit

**Date:** 2026-10-09  
**Canonical text:** [main.tex](main.tex), `\subsection{Computational Considerations}`, `sec:results-efficiency`.  
**Independent scope:** only Section 6.5 of canonical `main.tex` was rewritten. Chapters 1–5, previously reviewed 6.1–6.4, frozen policy comparisons, model artifacts and bibliography were not modified. Sections 7–8 and Abstract remain unwritten.  
**First draft:** [86aa425b](https://github.com/mzch0210/KuaiLive-Agent/commit/86aa425ba8dd032c13d34106a6c723907e33b43d).  
**Reviewer-tightened source:** [6ed0a42e](https://github.com/mzch0210/KuaiLive-Agent/commit/6ed0a42eca653e1709e62db8e38c60d77105b14d).  
**Nature of review:** Simulated KBS reviewer/editor check of claim accuracy and publication-oriented writing, not real journal referee feedback or a guarantee of acceptance.

## Overall decision

The efficiency evidence belongs in the experimental results because it tests the operational implication of selective specialist use: reducing expert calls **does not** entail a Base-relative deployment speedup. The central result is unambiguously adverse to a net-efficiency assertion in the measured KuaiLive implementation: Base mean **0.990585 ms**, selective HGB **2.006624 ms**, difference **+1.016039 ms**, ratio **2.025696**, with distinct pooled P95 values **1.275783 / 2.904929 ms**. The benchmark does not time the Twitch policy; its frozen 15.04% invocation rate cannot be converted into milliseconds.

The pre-revision Section 6.5 had an unnecessarily wide comparison with multiple distinct gates, serialized file sizes and process RSS in the primary Results text. It also did not explicitly disclose that the timed selective pipeline **executes** gate predictions but **replays frozen route masks** when taking branches. Those features could invite fairness and serving-realism objections. The revision retains the main numerical contrast in prose and stages the full audit as [Supplementary S9 draft](SUPPLEMENTARY_S9_RESOURCE_EFFICIENCY_DRAFT_2026-10-09.md).

## Reviewer objections and targeted corrections

| ID | Priority | Before / reviewer concern | Revision | Remaining qualification |
|---|---|---|---|---|
| E1 | P0 | A small Memory invocation fraction could be mistaken for latency reduction. | Opens by distinguishing frozen Twitch 6,650/44,221 (15.04%) from cost; Base and Base-derived features are computed for each event. | Twitch serving latency is **unmeasured**. |
| E2 | P0 | HGB vs Ridge/Tiny-MLP timings appear to benchmark three interchangeable equal-budget policies. | Removes Ridge/MLP rows from main, moves all alternatives and their differing route fractions to S9. | Equal-utility or fixed-decision matched cost comparison is **not** established. |
| E3 | P0 | The initial wording suggests timed predictions decide which branch to run. | Explicitly states the timing executes the trained predictor but **replays previously frozen routing decisions** for specialist selection. | Not a live policy correctness, rethresholding, or deployable online service benchmark. |
| E4 | P1 | Generic complexity descriptions risk omitting precomputation and cache updates. | Describes Base scoring, 14 feature preparation, shallow-tree traversal and optional candidate-level cached Memory; qualifies assumptions rather than claiming a total universal Big-O. | Full architecture-conditional schematic Big-O and gate comparisons go to S9; no formal end-to-end complexity theorem. |
| E5 | P1 | Means, P95, gate-only latency and file/RSS footprints compete for primary-table space and could imply metric additivity. | Main reports only paired Base/HGB means, P95, excess and ratio, under one timing panel; moves other measurements to S9. | Pooled latency percentiles are **descriptive**, not inferential confidence intervals or performance SLAs. |
| E6 | P1 | Mixing Base 0.761/HGB 2.337 ms from the older replicated benchmark with the later 0.991/2.007 ms panel would yield an incoherent ratio. | Keeps the entire main result on the gate-compression panel; documents older measurements separately in S9. | Different runner workloads/path implementations may explain differences; not an experimental replication of the same estimand. |
| E7 | P1 | Process peak RSS could be misread as gate footprint; serialized data sizes as active memory. | Moves checkpoint file, fitted HGB file, cache serialization and process RSS to an S9 table with separate semantics. | Memory loading/reconstruction costs and production concurrency remain unmeasured. |
| E8 | P1 | Claims of throughput or production latency could go beyond data. | Ends with explicit no-deployment-throughput, no-tail-SLA, no-online-engagement boundary. | Empirical portability requires new same-platform deployment study. |
| E9 | P1 | A two-row timing table has little incremental information beyond one paired sentence. | Removes primary 6.5 table in favor of prose; preserves full multi-row table with original precision and context in S9. | Main Results now better prioritizes selection value in 6.2 and contextual boundaries in 6.3–6.4. |

## Exact checks on the benchmark

- **Official source:** successful [formal CPU run 35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758), incorporating successful [gate-compression run 35571827672](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35571827672); executable: [`analysis/gate_compression_latency.py`](../../analysis/gate_compression_latency.py).
- **Protocol:** 575 candidate rooms, KuaiLive sampled-active, two SASRec branches, length 50, 14 gate descriptors, three heterogeneous GitHub-hosted CPU replicas, 1,200 warmed batch-size-one timed events per replica, cached history/input feeds.
- **Panel identity:** same gate-compression benchmark for Base and selective HGB. No mixing with older aggregate `dual_id=0.760783555` and `selective_frozen_14.25pct=2.336902394` ms from a separate latency benchmark.
- **Measured main values:** `dual_id.mean_ms=0.9905847453`, `dual_id.p95_ms=1.275783`; `selective_hgb.mean_ms=2.0066239936`, `selective_hgb.p95_ms=2.904929`; KuaiLive HGB specialist invocation frequency `p=0.142536`.
- **Other gates:** `selective_ridge.mean_ms=1.387248` at `p=0.309920`, `selective_tiny_mlp.mean_ms=1.271907` at `p=0.103698`. These are different learned routes; they are **not** a Pareto frontier at the same utility and budget.
- **HGB complexity:** 14 features; fitted `n_iter_=81`, maximum depth 3, not the configured `max_iter=200` as a claim about the resulting number of boosting iterations. Basic `O(TD)` traversal is conditional on features ready, one tree per iteration and ordinary single-output regression.
- **Cache/memory details:** two checkpoint files 303.851841 MiB, HGB estimator file 0.104691 MiB, serialized cached history 4.307323 MiB and separate 875.625 MiB process RSS; never sum file sizes to infer runtime peak.
- **Validation boundary:** frozen Twitch HGB gate on a different LiveRec candidate environment is `6,650/44,221=15.04%`; the current KuaiLive benchmark is **not a frozen Twitch TEST policy timing run**. No new accuracy model, threshold, or test-ranking analysis was carried out for this reviewer-style textual edit.

## Main-versus-S9 information policy

**Section 6.5 main text:** one lean finding sequence: frozen Twitch invocation frequency is not a cost metric → matched KuaiLive Base/HGB mean/P95 and 2.03× observation → cost structure/cached assumptions → routing-mask/fairness/deployment boundaries. No additional table is required for the isolated Base/HGB contrast.

**Staged Supplementary S9:** full 4-pipeline + component comparison, three host/benchmark settings, difference between frozen route masks and live decision making, older benchmark data, explicit complexity assumptions, Ridge/Tiny-MLP accuracy-route comparability, all memory/serialized sizes, artifacts, IDs and scripts. Draft at [S9 resource audit](SUPPLEMENTARY_S9_RESOURCE_EFFICIENCY_DRAFT_2026-10-09.md); formal submission supplementary package not yet assembled.

## Follow-up experimental gate, not required for this scoped text edit

If journal referees demand a deployment cost claim, a new **same-platform, matched-budget or fixed-decisions**, truly online gate-driven microbenchmark is needed, accounting for input construction, history/cache updates, queuing and tail latency under concurrency. Add a cost--utility Pareto comparison only after policies and tuning budgets are specified, and report uncertainty across hardware/user sampling. None of this was executed or implied by the present revision.

## Build and document-status gates

Source-only revision commit: [6ed0a42e](https://github.com/mzch0210/KuaiLive-Agent/commit/6ed0a42eca653e1709e62db8e38c60d77105b14d). [Corresponding LaTeX workflow run 37950210098](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37950210098) is the matching source to check for compilation, PDF/log upload and visual layout; its status must be verified independently before declaring typography closed. The original first-draft PDF from run 37948687922 is not a valid post-revision visual proof. Reviewer-style source tightening is complete; formal S9 document assembly, visual verification and coauthor approval remain distinct outstanding steps.
