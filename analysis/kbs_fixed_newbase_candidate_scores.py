"""Post-hoc fixed-new-Base, paired KuaiLive candidate-regime scorer.

Identical newly trained Room/Streamer model weights and fixed Dual-ID alpha are
used for both candidate sets. This is NOT reconstruction of a lost checkpoint.
No gate is fitted, no test-dependent hyperparameter is selected. A user
representation is encoded once per phase/model, in GPU batches of equal length.
Candidate dot products are vectorized on cached CPU item matrices per user.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from full_active_dual_id import (
    active_interval_arrays, candidate_sweep, load_rechorus,
    memory_rank, ndcg_scalar, rank_ge_at, room_to_streamer_item_array,
    user_histories, zscore,
)
from room_level_selective_agent import (
    histories, load_data, memory_scores, parse_list, popularity_by_streamer,
)

ALPHA_ROOM = 0.10
DATA_SEED = 20260918


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _encode(model, seqs: np.ndarray) -> torch.Tensor:
    """Match original full_active_dual_id.encode_user math, batched by length."""
    ids = torch.as_tensor(seqs, dtype=torch.long, device=model.i_embeddings.weight.device)
    batch, length = ids.shape
    valid = (ids > 0).long()
    hidden = model.i_embeddings(ids)
    rng = model.len_range[:length].to(ids.device)
    positions = (torch.full((batch, 1), length, dtype=torch.long, device=ids.device)
                 - rng.unsqueeze(0)) * valid
    hidden = hidden + model.p_embeddings(positions)
    mask = torch.tril(torch.ones((1, 1, length, length),
                                 dtype=torch.long, device=ids.device))
    for block in model.transformer_block:
        hidden = block(hidden, mask)
    hidden = hidden * valid[:, :, None].float()
    return hidden[:, length - 1, :]


def encode_phase_batched(model, corpus, phase: str, batch_size: int = 96):
    history = user_histories(corpus, phase, history_max=int(model.history_max))
    # Group exact lengths, preserving original position indices and causal masks.
    grouped = {}
    for user, seq in history.items():
        grouped.setdefault(len(seq), []).append((user, seq))
    encoded = {}
    start = time.perf_counter()
    with torch.inference_mode():
        model.eval()
        for length, records in sorted(grouped.items()):
            for i in range(0, len(records), batch_size):
                chunk = records[i:i + batch_size]
                batch = np.stack([seq for _, seq in chunk])
                output = _encode(model, batch).cpu().numpy()
                for (uid, _seq), vec in zip(chunk, output):
                    encoded[int(uid)] = np.asarray(vec, dtype=np.float64)

        # Correctness check: grouped encoding must agree with scalar encoding.
        users = list(history)[:min(8, len(history))]
        for uid in users:
            single = _encode(model, history[uid][None, :]).cpu().numpy()[0]
            if not np.allclose(single, encoded[uid], atol=2e-5, rtol=1e-5):
                raise ValueError(f"GPU batched-vs-scalar disagreement, phase={phase} uid={uid}")
    if len(encoded) != len(history):
        raise AssertionError("Lost users during GPU batching")
    return encoded, history, {"users": len(encoded), "groups": len(grouped),
                              "seconds": time.perf_counter() - start}


def rank_event(candidates, target, uid, room_vectors, streamer_vectors, room_weight,
               streamer_weight, to_streamer, memory_pop, memory_hist):
    cands = np.asarray(candidates, dtype=np.int64)
    if not len(cands) or len(set(cands.tolist())) != len(cands):
        raise ValueError(f"Invalid candidate list uid={uid}")
    hits = np.flatnonzero(cands == target)
    if len(hits) != 1 or np.any(cands <= 0):
        raise ValueError(f"Invalid target or candidate IDs uid={uid}")
    if cands.max() >= len(to_streamer):
        raise ValueError(f"room ID beyond streamer mapping uid={uid}")
    room_score = room_weight[cands] @ room_vectors[uid]
    sitems = to_streamer[cands]
    streamer_score = streamer_weight[sitems] @ streamer_vectors[uid]
    combined = ALPHA_ROOM * zscore(room_score) + (1 - ALPHA_ROOM) * zscore(streamer_score)
    brank = rank_ge_at(combined, int(hits[0]))
    mscore = memory_scores(cands, uid, memory_pop, memory_hist, to_streamer)
    # The memory scorer expects a dict room->actual streamer IDs, while
    # to_streamer above maps room->ReChorus streamer item. Hand in the
    # original room->streamer mapping, not the model-internal item mapping.
    mrank = memory_rank(cands, mscore, target)
    return brank, mrank


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rechorus-source", type=Path, required=True)
    ap.add_argument("--data-root", type=Path, required=True)
    ap.add_argument("--prepared-dir", type=Path, required=True)
    ap.add_argument("--room-model", type=Path, required=True)
    ap.add_argument("--streamer-model", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--phase", choices=["dev", "test"], default="dev")
    ap.add_argument("--batch-size", type=int, default=96)
    args = ap.parse_args()
    if args.batch_size < 1 or args.batch_size > 256:
        raise ValueError("batch-size must be 1..256")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rds = "KuaiLiveShopRoomDualID"
    sds = "KuaiLiveShopStreamerParallel"
    roomdir = args.data_root / rds
    streamerdir = args.data_root / sds
    train, dev, test, item_to_streamer = load_data(roomdir, 574)
    phase = dev if args.phase == "dev" else test
    if phase.user_id.duplicated().any():
        raise ValueError("Expected exactly one target per user")
    room_map = pd.read_csv(roomdir / "room_item_map.tsv", sep="\t")
    streamer_map = pd.read_csv(streamerdir / "streamer_item_map.tsv", sep="\t")
    intervals = active_interval_arrays(pd.read_pickle(args.prepared_dir / "rooms.pkl"), room_map)
    room_to_sitem = room_to_streamer_item_array(room_map, streamer_map)
    room_model, room_corpus = load_rechorus(args.rechorus_source, args.data_root, rds, args.room_model)
    streamer_model, streamer_corpus = load_rechorus(args.rechorus_source, args.data_root, sds, args.streamer_model)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required for batched representation encoding")
    room_model = room_model.to("cuda").eval()
    streamer_model = streamer_model.to("cuda").eval()
    rv, _, rm = encode_phase_batched(room_model, room_corpus, args.phase, args.batch_size)
    sv, visible_history, sm = encode_phase_batched(streamer_model, streamer_corpus, args.phase, args.batch_size)
    if set(rv) != set(sv) or set(rv) != set(phase.user_id.tolist()):
        raise AssertionError("Base and event users are not aligned")
    room_weights = room_model.i_embeddings.weight.detach().cpu().numpy().astype(np.float64)
    streamer_weights = streamer_model.i_embeddings.weight.detach().cpu().numpy().astype(np.float64)

    pop = popularity_by_streamer(train, item_to_streamer)
    hist_df = train if args.phase == "dev" else pd.concat(
        [train, dev[["user_id", "item_id", "time"]]], ignore_index=True)
    hist = histories(hist_df, item_to_streamer)
    rows = []
    phase_by_user = phase.set_index("user_id")
    phase_started = time.perf_counter()
    for uid, timestamp, target, fcands, was_active in candidate_sweep(phase, intervals):
        src = phase_by_user.loc[uid]
        if int(src.item_id) != target or int(src.time) != timestamp:
            raise ValueError(f"Event pairing failure uid={uid}")
        negatives = parse_list(src.neg_items, int)
        if len(negatives) != 574:
            raise AssertionError("Frozen negative count differs from 574")
        scands = np.concatenate(([target], negatives))
        if target not in fcands:
            raise AssertionError("Full candidates missing target")
        sampled_memory = memory_scores(scands, uid, pop, hist, item_to_streamer)
        full_memory = memory_scores(fcands, uid, pop, hist, item_to_streamer)
        # Shared cached item matrices and user vectors; candidates are evaluated
        # separately because each legal set defines its own z-score.
        sampled_room = room_weights[scands] @ rv[uid]
        sampled_stream = streamer_weights[room_to_sitem[scands]] @ sv[uid]
        full_room = room_weights[fcands] @ rv[uid]
        full_stream = streamer_weights[room_to_sitem[fcands]] @ sv[uid]
        samp_score = ALPHA_ROOM * zscore(sampled_room) + (1 - ALPHA_ROOM) * zscore(sampled_stream)
        full_score = ALPHA_ROOM * zscore(full_room) + (1 - ALPHA_ROOM) * zscore(full_stream)
        bs = rank_ge_at(samp_score, 0)
        bf = rank_ge_at(full_score, int(np.flatnonzero(fcands == target)[0]))
        ms = memory_rank(scands, sampled_memory, target)
        mf = memory_rank(fcands, full_memory, target)
        target_streamer = item_to_streamer[target]
        target_sitem = int(room_to_sitem[target])
        if target_sitem in visible_history[uid]:
            state = "represented"
        elif target_streamer in hist.get(uid, ({}, {}))[1]:
            state = "recoverable"
        else:
            state = "unavailable"
        rows.append({
            "user_id": uid, "time": timestamp, "target_item": target,
            "state": state, "sampled_candidates": len(scands),
            "full_candidates": len(fcands), "target_metadata_active": was_active,
            "sampled_base_rank": bs, "full_base_rank": bf,
            "sampled_memory_rank": ms, "full_memory_rank": mf,
            "sampled_base_ndcg10": ndcg_scalar(bs), "full_base_ndcg10": ndcg_scalar(bf),
            "sampled_memory_ndcg10": ndcg_scalar(ms), "full_memory_ndcg10": ndcg_scalar(mf),
            "sampled_base_hr10": float(bs <= 10), "full_base_hr10": float(bf <= 10),
            "sampled_memory_hr10": float(ms <= 10), "full_memory_hr10": float(mf <= 10),
        })
    out = pd.DataFrame(rows).sort_values("user_id").reset_index(drop=True)
    if len(out) != len(phase) or out.user_id.duplicated().any():
        raise AssertionError("Output size / duplicate-user violation")
    output_path = args.out_dir / f"paired_{args.phase}.csv.gz"
    out.to_csv(output_path, index=False, compression="gzip")
    meta = {
        "experiment": "NEW_DIAGNOSTIC_FIXED_BASE_NOT_ORIGINAL",
        "phase": args.phase, "n": len(out),
        "alpha_room": ALPHA_ROOM,
        "room_checkpoint_sha256": sha256(args.room_model),
        "streamer_checkpoint_sha256": sha256(args.streamer_model),
        "frozen_data_sampled_negatives": 574,
        "room_vectors": rm, "streamer_vectors": sm,
        "paired_scoring_seconds": time.perf_counter() - phase_started,
        "candidate_count_sampled_unique": sorted(out.sampled_candidates.unique().tolist()),
        "full_candidate_count": {"mean": float(out.full_candidates.mean()),
                                 "min": int(out.full_candidates.min()),
                                 "max": int(out.full_candidates.max())},
        "target_fallback_count": int((~out.target_metadata_active).sum()),
        "posthoc_no_gate_or_test_tuning": True,
    }
    (args.out_dir / f"paired_{args.phase}_meta.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
