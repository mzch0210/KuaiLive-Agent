# Room-level Cold-Start Audit Results

Date: 2026-09-20

Source room-level kill-gate run: 35455075346  
Cold-start audit run: 35481681725  
Room × streamer 2×2 audit run: 35481886222

## Status

**Cold-start-only explanation rejected.** The large room-level improvement is not driven only by unseen `live_id`s. However, the dominant mechanism is **persistent user–streamer familiarity**, not a generally effective selective router.

## Overall frozen room-level result

| Model | Test NDCG@10 |
|---|---:|
| SASRec (room ID) | 0.315093 |
| Always MemoryFusion | 0.565887 |
| Selective Memory v2 | 0.567991 |

Selective vs SASRec: +0.252899 (+80.26%), with the frozen paired-bootstrap CI from the kill gate fully above zero. Test gate rate: 96.21%.

## Exposure audit

- Test targets with room seen in train: 65.35%.
- Test targets with streamer seen in train: 93.16%.
- Test targets with room seen before test (train+dev): 69.55%.
- Test targets with streamer seen before test globally: 94.22%.
- Test targets whose streamer is familiar in that user's fair pre-test history: 46.91%.
- Across all 575 candidates, only 17.39% of room IDs are seen in train, while 94.99% of streamers are seen in train.

This confirms that room IDs are much more ephemeral than streamer identities, but unseen-room targets are not the majority of test cases.

## Global train-exposure strata

| Stratum | n | Share | SASRec | MemoryFusion | Selective | Selective − SASRec | 95% CI | Gate |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| Seen room | 6,680 | 65.35% | 0.481441 | 0.620638 | 0.623857 | +0.142416 | [0.130823, 0.152804] | 94.34% |
| New room, seen streamer | 2,843 | 27.81% | 0.001464 | 0.552107 | 0.552107 | +0.550643 | [0.533136, 0.568103] | 99.79% |
| New room, new streamer | 699 | 6.84% | 0.000984 | 0.098712 | 0.098712 | +0.097728 | [0.075392, 0.120514] | 99.57% |

Because the benefit remains strongly positive on seen-room targets, the overall room-level gain cannot be dismissed as a pure target-room cold-start artifact.

## Room × personal-streamer-familiarity 2×2 audit

| Stratum | n | Share | SASRec | MemoryFusion | Selective | Selective − SASRec | 95% CI | Gate |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| Seen room + familiar streamer | 3,069 | 30.02% | 0.577511 | 0.972505 | 0.969472 | +0.391961 | [0.376652, 0.407020] | 93.26% |
| Seen room + novel streamer | 3,611 | 35.33% | 0.399791 | 0.321585 | 0.330119 | **−0.069672** | **[−0.081706, −0.057941]** | 95.26% |
| New room + familiar streamer | 1,726 | 16.89% | 0.002453 | 0.943710 | 0.943710 | +0.941257 | [0.931798, 0.950178] | 100% |
| New room + novel streamer | 1,816 | 17.77% | 0.000339 | 0.005394 | 0.005394 | +0.005055 | [0.002836, 0.007486] | 99.50% |

The two familiar-streamer strata account for about 109% of the net Selective-vs-SASRec gain; the seen-room/novel-streamer stratum offsets about 9.7% of that gain.

## Candidate-sampling diagnostic

The average candidate set contains only 0.30 familiar-streamer negatives out of 574 negatives. In 84.69% of test cases there are zero familiar-streamer negatives, and in 93.95% there is at most one.

For the 4,795 target-familiar cases, the target streamer is familiar but 83.07% of candidate sets contain **no other familiar-streamer negative**. Consequently, personal streamer familiarity is often almost a unique marker of the positive target under the active-at-time random-negative protocol. This does not constitute label leakage—the familiarity comes only from fair pre-event history—but it can substantially amplify MemoryFusion under synthetic negative sampling.

## Scientific diagnosis

1. **Room cold-start alone is not the explanation.** Selective Memory remains better than SASRec on seen-room targets.
2. **Persistent streamer relationship is the dominant mechanism.** Memory is extremely strong when the target streamer has appeared in the user's prior history and can be harmful when that relationship is absent.
3. **The current v2 router is not genuinely selective in the room task.** It invokes Memory for 93–100% of users in every 2×2 stratum, including the seen-room/novel-streamer group where Memory significantly hurts.
4. **The +80% headline should not be used as evidence that the router learned 'when to think'.** It is better interpreted as evidence that persistent streamer identity is a powerful transferable representation for ephemeral live rooms under this candidate protocol.
5. **Random active-room negatives likely magnify the relationship signal.** Exposure-aware / official negative robustness is required before using the room-level magnitude as a main result.

## Decision

**Do not proceed directly to Full-active + GTS-Successive on the basis of the +80% room-level result.**

The next reviewer-facing experiment should use a stronger room baseline that can transfer through persistent streamer identity (for example a dual room+streamer sequential model or equivalent streamer-aware SASRec) and should test exposure-aware negatives. The scientific comparison should then ask whether MemoryFusion / selective memory adds value beyond that fairer base.
