"""Paired candidate-regime diagnostic using exactly one frozen Dual-ID checkpoint pair.

This is an exploratory diagnostic, not a re-run or tuning of frozen P1.3 TEST.
Models are trained once upstream and scored once over full-active candidates,
with sampled scores extracted by subsetting the SAME raw candidate scores.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "src"))

from full_active_dual_id import (
    ALPHA_GRID, active_interval_arrays, candidate_sweep, encode_phase_users,
    load_rechorus, memory_rank, ndcg_scalar, popularity_by_streamer,
    room_to_streamer_item_array, score_embedding_candidates, user_histories, zscore,
)
from room_level_selective_agent import histories, load_data, memory_scores, parse_list
from kbs_kuailive_regime_decomposition import _build_test_states

SEED = 20260918


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def subset_indices(all_items: np.ndarray, sampled_items: np.ndarray) -> np.ndarray:
    """Map each sampled room into full-active items, fail closed on membership/duplicates."""
    if len(np.unique(all_items)) != len(all_items):
        raise ValueError("duplicate full-active room items")
    if len(np.unique(sampled_items)) != len(sampled_items):
        raise ValueError("duplicate sampled room items")
    pos = {int(v): i for i, v in enumerate(all_items)}
    try:
        idx = np.fromiter((pos[int(v)] for v in sampled_items), dtype=int, count=len(sampled_items))
    except KeyError as e:
        raise ValueError(f"sampled item absent from full active: {e}") from e
    if not np.array_equal(all_items[idx], sampled_items):
        raise AssertionError("candidate subset reconstruction failed")
    return idx


def boot(values: np.ndarray, seed: int, reps: int = 3000) -> dict:
    v = np.asarray(values, dtype=float)
    if not len(v) or not np.isfinite(v).all():
        raise ValueError("empty or non-finite bootstrap values")
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(0, reps, 64):
        count = min(64, reps - len(means))
        means.extend(np.mean(v[rng.integers(0, len(v), (count, len(v)))], axis=1))
    return {"mean": float(v.mean()), "ci95": [float(x) for x in np.quantile(means, [.025, .975])], "n": int(len(v))}


def score_pair(phase: pd.DataFrame, room_model, stream_model,
               room_vecs, stream_vecs, intervals, room_to_sitem,
               sample_neg: int, alpha: float | None, pop, hist, item_to_streamer):
    sampled = phase.set_index("user_id", verify_integrity=True)
    rows = []
    grid_sum = np.zeros(len(ALPHA_GRID), dtype=float)
    for uid, t, target, full_items, metadata_active in candidate_sweep(phase, intervals):
        row = sampled.loc[uid]
        if int(row.item_id) != target or int(row.time) != t:
            raise ValueError("sampled/full event identity mismatch")
        sample_items = np.concatenate(([target], parse_list(row.neg_items, int)))
        if len(sample_items) != sample_neg + 1:
            raise ValueError("unexpected sampled candidate count")
        index = subset_indices(full_items, sample_items)
        if np.count_nonzero(full_items == target) != 1:
            raise ValueError("full target cardinality must equal 1")
        if not np.array_equal(sample_items[0:1], np.array([target])):
            raise ValueError("sampled target not in position zero")
        # SAME checkpoint and SAME raw full-candidate scores for both regimes.
        room_raw = score_embedding_candidates(room_model, room_vecs[uid], full_items)
        stream_raw = score_embedding_candidates(stream_model, stream_vecs[uid], room_to_sitem[full_items])
        room_sample = zscore(room_raw[index])
        stream_sample = zscore(stream_raw[index])
        if alpha is None:
            for j, a in enumerate(ALPHA_GRID):
                s = a * room_sample + (1.0 - a) * stream_sample
                grid_sum[j] += ndcg_scalar(int(np.sum(s >= s[0] - 1e-12)))
            continue
        full_tidx = int(np.flatnonzero(full_items == target)[0])
        sample_s = alpha * room_sample + (1.0 - alpha) * stream_sample
        full_s = alpha * zscore(room_raw) + (1.0 - alpha) * zscore(stream_raw)
        sampled_rank = int(np.sum(sample_s >= sample_s[0] - 1e-12))
        full_rank = int(np.sum(full_s >= full_s[full_tidx] - 1e-12))
        mem_sample = memory_rank(sample_items, memory_scores(sample_items, uid, pop, hist, item_to_streamer), target)
        mem_full = memory_rank(full_items, memory_scores(full_items, uid, pop, hist, item_to_streamer), target)
        rows.append({
            "user_id": int(uid), "time": int(t), "target_item": int(target),
            "sampled_candidates": int(len(sample_items)),
            "full_candidates": int(len(full_items)),
            "target_metadata_active": bool(metadata_active),
            "sampled_base_rank": sampled_rank, "full_base_rank": full_rank,
            "sampled_memory_rank": int(mem_sample), "full_memory_rank": int(mem_full),
            "sampled_base_ndcg10": ndcg_scalar(sampled_rank),
            "full_base_ndcg10": ndcg_scalar(full_rank),
            "sampled_memory_ndcg10": ndcg_scalar(mem_sample),
            "full_memory_ndcg10": ndcg_scalar(mem_full),
        })
    if alpha is None:
        best_idx = max(range(len(ALPHA_GRID)), key=lambda j: (grid_sum[j], float(ALPHA_GRID[j])))
        return float(ALPHA_GRID[best_idx]), pd.DataFrame({
            "alpha_room": ALPHA_GRID, "dev_sampled_ndcg10": grid_sum / len(phase)
        })
    result = pd.DataFrame(rows).sort_values("user_id").reset_index(drop=True)
    if len(result) != len(phase) or result.user_id.duplicated().any():
        raise RuntimeError("scored test coverage mismatch")
    return result


def summarize(result: pd.DataFrame, states: pd.DataFrame, reps: int) -> dict:
    if result.user_id.duplicated().any() or states.user_id.duplicated().any():
        raise ValueError("duplicate user identity")
    d = result.merge(states[["user_id", "evidence_state"]], on="user_id", how="inner", validate="one_to_one")
    if len(d) != len(result) or d.evidence_state.isna().any():
        raise ValueError("missing/mismatched evidence-state labels")
    out = {"n": int(len(d)), "regimes": {}, "state_rows": []}
    for regime in ("sampled", "full"):
        base = d[f"{regime}_base_ndcg10"].to_numpy()
        mem = d[f"{regime}_memory_ndcg10"].to_numpy()
        out["regimes"][regime] = {
            "base": float(base.mean()), "memory": float(mem.mean()),
            "memory_minus_base": boot(mem - base, SEED + (1 if regime == "sampled" else 2), reps),
        }
    shift = ((d.full_memory_ndcg10 - d.full_base_ndcg10) -
             (d.sampled_memory_ndcg10 - d.sampled_base_ndcg10)).to_numpy()
    out["paired_full_minus_sampled_delta"] = boot(shift, SEED + 3, reps)
    for j, state in enumerate(("represented", "recoverable-but-unrepresented", "unavailable")):
        g = d[d.evidence_state == state]
        if len(g) == 0:
            raise RuntimeError(f"missing state {state}")
        delta_s = (g.sampled_memory_ndcg10 - g.sampled_base_ndcg10).to_numpy()
        delta_f = (g.full_memory_ndcg10 - g.full_base_ndcg10).to_numpy()
        out["state_rows"].append({
            "state": state, "n": int(len(g)), "prevalence": float(len(g) / len(d)),
            "sampled_delta": float(delta_s.mean()), "full_delta": float(delta_f.mean()),
            "paired_shift": boot(delta_f - delta_s, SEED + 10 + j, reps),
        })
    weighted = sum(row["prevalence"] * row["sampled_delta"] for row in out["state_rows"])
    if not np.isclose(weighted, out["regimes"]["sampled"]["memory_minus_base"]["mean"], atol=1e-12):
        raise AssertionError("sampled state decomposition identity violated")
    weighted = sum(row["prevalence"] * row["full_delta"] for row in out["state_rows"])
    if not np.isclose(weighted, out["regimes"]["full"]["memory_minus_base"]["mean"], atol=1e-12):
        raise AssertionError("full state decomposition identity violated")
    # Scientific outcome is never used as a CI pass/fail condition.
    out["guards"] = {
        "same_event_identities": True, "same_model_checkpoints": True,
        "same_alpha_room": True, "sampled_subset_of_full_active": True,
        "same_memory_definition": True, "paired_user_bootstrap": True,
        "sign_neutral_evaluation": True,
    }
    return out


def self_test():
    assert np.array_equal(subset_indices(np.array([4, 8, 7]), np.array([7, 4])), [2, 0])
    try:
        subset_indices(np.array([2, 3]), np.array([2, 5]))
    except ValueError:
        pass
    else:
        raise AssertionError("subset fail-closed test failed")
    toy = pd.DataFrame({
        "user_id": [1, 2, 3], "sampled_base_ndcg10": [.5, .1, .3],
        "full_base_ndcg10": [.3, .2, .6], "sampled_memory_ndcg10": [.1, .3, .2],
        "full_memory_ndcg10": [.2, .5, .4],
    })
    states = pd.DataFrame({"user_id": [1, 2, 3], "evidence_state": [
        "represented", "recoverable-but-unrepresented", "unavailable"]})
    r = summarize(toy, states, 100)
    assert r["n"] == 3 and np.isfinite(r["paired_full_minus_sampled_delta"]["mean"])
    print("same-checkpoint paired diagnostic self-test PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    for key in ("rechorus-source", "data-root", "prepared-dir", "room-model",
                "streamer-model", "out-dir"):
        ap.add_argument("--" + key, type=Path)
    ap.add_argument("--room-dataset", default="KuaiLiveShopRoomDualID")
    ap.add_argument("--streamer-dataset", default="KuaiLiveShopStreamerParallel")
    ap.add_argument("--n-neg", type=int, default=574)
    ap.add_argument("--n-boot", type=int, default=3000)
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    for key in ("rechorus_source", "data_root", "prepared_dir", "room_model", "streamer_model", "out_dir"):
        if getattr(args, key) is None:
            ap.error(f"--{key.replace('_', '-')} is required")
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass
    args.out_dir.mkdir(parents=True, exist_ok=True)
    room_dir = args.data_root / args.room_dataset
    streamer_dir = args.data_root / args.streamer_dataset
    train, dev, test, item_to_streamer = load_data(room_dir, args.n_neg)
    room_map = pd.read_csv(room_dir / "room_item_map.tsv", sep="\t")
    streamer_map = pd.read_csv(streamer_dir / "streamer_item_map.tsv", sep="\t")
    rooms = pd.read_pickle(args.prepared_dir / "rooms.pkl")
    intervals = active_interval_arrays(rooms, room_map)
    room_to_sitem = room_to_streamer_item_array(room_map, streamer_map)
    room_model, room_corpus = load_rechorus(args.rechorus_source, args.data_root, args.room_dataset, args.room_model)
    stream_model, stream_corpus = load_rechorus(args.rechorus_source, args.data_root, args.streamer_dataset, args.streamer_model)
    pop = popularity_by_streamer(train, item_to_streamer)
    vecs = {}
    for phase in ("dev", "test"):
        vecs[("room", phase)] = encode_phase_users(room_model, room_corpus, phase)
        vecs[("streamer", phase)] = encode_phase_users(stream_model, stream_corpus, phase)
    alpha, alpha_grid = score_pair(dev, room_model, stream_model,
                                    vecs[("room", "dev")], vecs[("streamer", "dev")],
                                    intervals, room_to_sitem, args.n_neg, None, pop,
                                    histories(train, item_to_streamer), item_to_streamer)
    result = score_pair(test, room_model, stream_model,
                        vecs[("room", "test")], vecs[("streamer", "test")],
                        intervals, room_to_sitem, args.n_neg, alpha, pop,
                        histories(pd.concat([train, dev[["user_id", "item_id", "time"]]], ignore_index=True),
                                  item_to_streamer), item_to_streamer)
    states = _build_test_states(room_dir, 50)
    report = summarize(result, states, args.n_boot)
    report["design"] = "single frozen Room/Streamer model pair, DEV-selected sampled alpha, paired TEST candidate swap; no TEST fitting"
    report["alpha_room_selected_on_sampled_dev"] = float(alpha)
    report["model_sha256"] = {"room": sha256(args.room_model), "streamer": sha256(args.streamer_model)}
    report["event_fingerprint_sha256"] = sha256(room_dir / "test.csv")
    report["input_sha256"] = {x: sha256(room_dir / x) for x in
                                ("train.csv", "dev.csv", "test.csv", "room_item_map.tsv")}
    report["secondary_diagnostic_not_frozen_confirmation"] = True
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    result.to_csv(args.out_dir / "per_user_paired_test.csv.gz", index=False, compression="gzip")
    alpha_grid.to_csv(args.out_dir / "sampled_dev_alpha_grid.csv", index=False)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
