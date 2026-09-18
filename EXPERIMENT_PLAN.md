# Experiment gates

## Gate A — engineering validity
- full Zenodo file downloaded and checksum/size verified
- `click.csv` and `room.csv` located after extraction
- click-to-room streamer identity checked during scope filtering
- smoke test passes before full job begins

## Gate B — data validity
Report:
- raw click rows
- retained shop click rows
- users, streamers, rooms
- number of click/room streamer mismatches dropped
- users eligible for chronological leave-one-out
- active-candidate count distribution

## Gate C — main empirical claim
Primary comparison: `MemoryPlanner` vs `LongMemory` and `MemoryFusion`.

A direction is worth continuing only if the planner's NDCG@10 increment is:
1. positive across seeds;
2. positive for the >=30s watched subset;
3. not entirely explained by the long-memory component;
4. robust to removing individual planner modules in ablation.

## Gate D — strong recommender baseline
Only after Gate C passes, add BPRMF/SASRec/TiSASRec using ReChorus and preserve the same shop-only time split/candidate semantics. A publishable Agent claim should survive comparison with TiSASRec/SASRec, not merely Popularity.
