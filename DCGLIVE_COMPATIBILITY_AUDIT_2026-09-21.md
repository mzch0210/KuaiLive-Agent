# DCGLive Compatibility Audit — 2026-09-21

**Target paper:** KuaiLive-Agent / selective explicit relationship memory  
**External method:** DCGLive, *Room Matters: Dynamic Room-level Collaboration Information Modeling for Live Streaming Recommendation*, WWW 2026  
**Official repository:** https://github.com/imgkkk574/DCGLive  
**Decision:** **Do not place the official DCGLive number in the primary effectiveness table. The official protocol is materially different from our frozen next-live-room protocol.**

---

## 1. Why this audit was run

DCGLive is the closest 2026 room-level live-stream recommendation competitor. Its public repository explicitly supports `--network kuailive`, so the first question is not whether code exists, but whether the official result can be compared scientifically to our frozen task without redefining either side.

This audit checks target, split, candidate universe, evaluation state update, data representation, and metric semantics.

---

## 2. What matches

### Target family

The official evaluation script states that its task is **next room prediction**. This is conceptually close to our primary `next live_id` target.

### Room / streamer / user dynamics

DCGLive explicitly models the evolving tripartite relationships among room, streamer, and user, including initialization for newly created rooms from existing rooms/streamer information. This makes it highly relevant related work for our identity-control discussion.

### KuaiLive lineage

The official repository provides a transformed `data/kuailive.csv` and launch commands with `--network kuailive`.

These similarities make DCGLive a required related-work reference, but they are not sufficient for a numeric head-to-head comparison.

---

## 3. Material protocol mismatches

| Dimension | Our frozen primary protocol | Official DCGLive protocol | Compatibility |
|---|---|---|---|
| Target | next live room (`live_id`) | next room | conceptually aligned |
| Dataset slice | KuaiLive `shop` subset | repository-provided transformed `kuailive.csv` event stream | **not identical** |
| Split | per-user LOO: history / dev / test | global chronological interaction indices, default train 80%, validation 10%, test 10% | **material mismatch** |
| Candidate universe | rooms legally active at target time; sampled-active 575 and full-active robustness | rank true item against **all item IDs** in model item universe | **material mismatch** |
| Availability semantics | explicit `start <= t < end` legal candidate mask | room end/start time enters dynamic modeling, but ranking code does not mask to currently active items | **material mismatch** |
| Test-state evolution | ordinary LOO has one test target per user; dev-only tuning and frozen test evaluation | validation/test are processed sequentially and dynamic embeddings/adjacency are updated after interactions | **material mismatch** |
| Main metric | NDCG@10 / HR@10 under legal active candidates | rank of true room among all rooms; downstream metric computation follows official script | not directly comparable |
| Identity control | explicit room-SASRec + streamer-SASRec Dual-ID baseline | dynamic graph representations jointly model rooms/users/streamers | different mechanism |

---

## 4. Code evidence behind the decision

The official evaluation script:

1. defines the task as `next room prediction`;
2. uses `train_proportion=0.8` by default;
3. sets boundaries by global interaction index:
   - train end = 80%;
   - validation = next 10%;
   - test = next 10%;
4. computes distances from the predicted room embedding to **all items** and ranks the true room among all items;
5. continues a chronological forward pass through validation and test, updating user/room/streamer dynamic embeddings and adjacency information after observed interactions.

The official data loader consumes a transformed event stream containing user, streamer, room, timestamps/end time, state-change labels, room features, and streamer features. It is not our frozen shop-only LOO export.

---

## 5. Why an adapted DCGLive would no longer be an official baseline

To force DCGLive onto our final protocol we would need to change at least:

- the data slice and user eligibility rules;
- split construction from global 80/10/10 to our LOO/GTS semantics;
- ranking from all rooms to legal active rooms at each target timestamp;
- validation/test update semantics;
- likely data/event feature construction.

That would be a substantial adapter/new experimental implementation rather than an official reproduction. A number produced after these changes should not be labeled simply “DCGLive official” and would introduce another large implementation-validation burden late in the paper-closing phase.

---

## 6. Decision for the manuscript

### Main paper

- Cite DCGLive as the strongest direct room-dynamics related work.
- Explain that it addresses a different evaluation regime: global chronological online dynamic-graph prediction over the room universe rather than our legal-active LOO selective-memory setting.
- Do **not** put its published/official score in the same numeric effectiveness table as Dual-ID / Memory / Selective.

### Optional appendix only

An adapted DCGLive experiment is justified only if a reviewer explicitly requests a common-protocol graph baseline and the paper schedule allows an independently validated adapter. If run, label it **DCGLive-adapted**, enumerate every protocol modification, and do not claim equivalence to the official reported result.

---

## 7. Scientific implication

The absence of a direct official numeric comparison is not a missing generic-baseline problem. DCGLive primarily tests **dynamic room representation / collaboration modeling**, whereas the present paper asks whether an **explicit relationship-memory specialist has positive marginal ranking utility beyond a strong identity-aware base and when that relative utility changes across regimes**.

The correct defense is protocol transparency plus a strong Dual-ID identity control, full-active candidate robustness, and conditional-utility analysis—not an invalid cross-protocol score comparison.

---

## 8. P0-D status

**CLOSED by compatibility audit.**

No expensive DCGLive retraining should be launched before submission under the current protocol. Keep the official implementation as required related work and document this task mismatch in the experimental-comparison limitations.
