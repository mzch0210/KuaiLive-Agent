# KuaiLive-Agent — Post-P1.2 Experiment Plan

**Snapshot date:** 2026-09-22  
**Current phase:** P0 CLOSED; P1.0–P1.2 CLOSED/FROZEN; P1.3 untouched one-shot test NEXT.

---

# 1. Executive decision

No structural experiment-plan change is required after P1.2.

P1.2 produced the mechanism pattern the protocol was designed to test:

- Always Memory is globally worse than the frozen LiveRec base;
- Memory utility changes sign across relationship horizons;
- long-horizon-only relationships show strong positive marginal utility;
- matched-budget relative-utility routing exceeds generic difficulty routing.

Therefore stop dev tuning and proceed to the already specified one-shot P1.3 test.

A subsequent **DEV-only execution-platform compatibility audit** tested whether the frozen CUDA policy could be migrated to a standard GitHub-hosted CPU runner. The hosted CPU had ample compute capacity, but it did **not** reproduce the frozen CUDA policy exactly: 27 event-level Base NDCG@10 values and 19 H@10 values differed; six Utility-router invocation decisions and four matched-budget Difficulty-router decisions changed. The state features reproduced, but the LiveRec base-confidence features showed device-dependent numerical differences. Therefore the hosted-CPU fallback is **rejected**. This is an execution-environment decision only and does not modify P1.2 or P1.3 scientifically.

---

# 2. P1.2 — CLOSED / FROZEN

Frozen components that must not change:

- LiveRec epoch-74 base;
- transferred `MemoryFusion = 0.45 * short + 0.45 * long + 0.10 * popularity`;
- HGB utility gate family and features;
- event-level utility target `Memory NDCG@10 − Base NDCG@10`;
- frozen utility threshold;
- same-feature generic difficulty control;
- matched-budget comparison rule;
- relationship-horizon definitions;
- no routing directly from target-dependent horizon labels.

No dev result may be used to redesign the primary Memory specialist or utility gate.

---

# 3. P1.3 — Untouched one-shot test — UNCHANGED

Primary rows:

- frozen LiveRec Base;
- frozen transferred Always Memory;
- frozen Selective Utility Router;
- matched-budget Difficulty Router;
- exact-K Oracle as analysis-only headroom.

Primary metrics:

- NDCG@10;
- HR/Recall@10;
- realized Memory invocation rate;
- paired user bootstrap confidence intervals;
- repeat/novel breakdown;
- recent-visible / long-horizon-only / unseen breakdown;
- frozen utility strata.

Primary success rule:

`Selective Utility − LiveRec Base > 0` with paired-bootstrap 95% CI lower bound > 0.

Mechanism replication:

`Utility Router − Difficulty Router > 0`, preferably with positive paired CI.

A null or negative test result remains valid and must not trigger rescue tuning.

---

# 4. Execution-completeness requirements — IMPLEMENTATION ONLY

These requirements complete the frozen protocol; they do **not** modify the experiment design.

1. Fit the final difficulty HGB on all frozen dev examples using the already frozen target `1 − Base NDCG@10`, feature set, HGB family and hyperparameters.
2. Apply state-complexity percentiles on test using the frozen P1.2 **dev reference ECDF**, never test-distribution ranks.
3. The test Difficulty Router must select exactly `K` events, where `K` is the frozen utility-threshold router's realized invocation count on the test set.
4. Oracle uses the same realized test `K` and remains analysis-only.
5. Before opening test, replay the complete P1.3 export path on dev and require reproduction of frozen P1.2 Base, Memory, repeat fraction and relationship-horizon counts.
6. Enforce one-shot execution with both repository-artifact and persistent self-hosted-runner sentinels.
7. Final workflow validation must check protocol integrity only; it must **not** fail because effectiveness is null or negative.
8. The P1.3 ranking/feature export must run on the frozen CUDA/RTX3090 path. The standard GitHub-hosted CPU fallback is not protocol-compatible and must not be used for the one-shot test.

---

# 5. Efficiency requirements

P1.3 should not retrain LiveRec or recompute unnecessary splits.

Use:

- frozen checkpoint inference only;
- source/data/availability caches with SHA256 verification;
- test-only sequence materialization after the dev replay passes;
- batched GPU base inference with exact-equivalence guard;
- reusable Memory scratch buffers and train-only popularity cache semantics;
- hosted CPU policy fitting/evaluation so the self-hosted GPU environment remains minimal;
- chunked bootstrap computation to avoid excessive memory allocation.

Do not change batch size, precision, TF32, model architecture, optimizer, sequence length, Memory weights, gate family, features, or threshold for speed.

The DEV-only hosted-CPU audit remains diagnostic evidence only. Do not introduce CPU-to-GPU calibration, post-hoc feature rounding, threshold compensation, or any other device-specific rescue transformation after observing the compatibility result.

---

# 6. Updated stopping rule

> **P1.3 preflight freeze → full CUDA dev replay → arm one-shot guard → untouched CUDA test export once → frozen policy evaluation → manuscript freeze.**

No P2 expansion unless the frozen P1.3 result exposes a specific reviewer-risk question. No test-based rescue tuning under any outcome.
