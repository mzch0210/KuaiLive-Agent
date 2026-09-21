from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_val_predict

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from dual_id_room_baseline import conf_tuple
from room_level_selective_agent import (
    CONF_FEATURES,
    USER_FEATURES,
    EPS,
    SEED,
    bootstrap_delta,
    choose_threshold,
    hgb,
    histories,
    load_data,
    memory_scores,
    ndcg10,
    popularity_by_streamer,
    user_features,
)
from kuailive_agent.evaluate import IndexedCounterSet


RECHORUS_COMMIT = "c164ec4303cc20ddcfbd1b57de366a481811d1e5"
ALPHA_GRID = np.linspace(0.0, 1.0, 41)
FEATURES = USER_FEATURES + CONF_FEATURES


def load_rechorus(source: Path, data_root: Path, dataset: str, model_path: Path):
    src = str((source / "src").resolve())
    if src not in sys.path:
        sys.path.insert(0, src)
    from helpers.SeqReader import SeqReader
    from models.sequential.SASRec import SASRec

    args = SimpleNamespace(
        sep="\t",
        path=str(data_root.resolve()) + "/",
        dataset=dataset,
        device=torch.device("cpu"),
        model_path=str(model_path.resolve()),
        buffer=0,
        dropout=0.0,
        test_all=0,
        num_neg=1,
        history_max=50,
        emb_size=64,
        num_layers=1,
        num_heads=4,
    )
    corpus = SeqReader(args)
    model = SASRec(args, corpus).to(args.device)
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    return model, corpus


def user_histories(corpus, phase: str, history_max: int = 50) -> dict[int, np.ndarray]:
    df = corpus.data_df[phase]
    if df.user_id.duplicated().any():
        raise ValueError(f"{phase}: expected one target row per user")
    out: dict[int, np.ndarray] = {}
    for r in df.itertuples(index=False):
        uid = int(r.user_id)
        pos = int(r.position)
        seq = corpus.user_his[uid][:pos]
        ids = np.asarray([int(x[0]) for x in seq[-history_max:]], dtype=np.int64)
        if not len(ids):
            raise ValueError(f"{phase}: empty history for user {uid}")
        out[uid] = ids
    return out


def encode_user(model, history_items: np.ndarray) -> torch.Tensor:
    ids = torch.from_numpy(np.asarray(history_items, dtype=np.int64)).view(1, -1)
    length = ids.shape[1]
    valid = (ids > 0).long()
    hv = model.i_embeddings(ids)
    pos = (torch.tensor([[length]], dtype=torch.long) - model.len_range[None, :length]) * valid
    hv = hv + model.p_embeddings(pos)
    mask = torch.from_numpy(np.tril(np.ones((1, 1, length, length), dtype=np.int64)))
    for block in model.transformer_block:
        hv = block(hv, mask)
    hv = hv * valid[:, :, None].float()
    return hv[0, length - 1, :].detach()


def encode_phase_users(model, corpus, phase: str) -> dict[int, torch.Tensor]:
    hist = user_histories(corpus, phase, history_max=int(model.history_max))
    out = {}
    with torch.inference_mode():
        for uid, seq in hist.items():
            out[uid] = encode_user(model, seq)
    return out


def score_embedding_candidates(model, user_vec: torch.Tensor, item_ids: np.ndarray, chunk: int = 8192) -> np.ndarray:
    ids = np.asarray(item_ids, dtype=np.int64)
    out = np.empty(len(ids), dtype=np.float64)
    with torch.inference_mode():
        for lo in range(0, len(ids), chunk):
            hi = min(lo + chunk, len(ids))
            it = torch.from_numpy(ids[lo:hi]).long()
            emb = model.i_embeddings(it)
            out[lo:hi] = torch.mv(emb, user_vec).cpu().numpy().astype(np.float64, copy=False)
    return out


def zscore(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    sd = float(x.std())
    if sd <= EPS:
        return np.zeros_like(x)
    return (x - float(x.mean())) / sd


def rank_ge_at(scores: np.ndarray, target_index: int) -> int:
    ts = float(scores[int(target_index)])
    return int(np.sum(np.asarray(scores) >= ts - 1e-12))


def memory_rank(cands: np.ndarray, scores: np.ndarray, target_item: int) -> int:
    ts = float(scores[np.flatnonzero(cands == target_item)[0]])
    better = int(np.sum(scores > ts + EPS))
    ties_before = int(np.sum((np.abs(scores - ts) <= EPS) & (cands < int(target_item))))
    return 1 + better + ties_before


def ndcg_scalar(rank: int) -> float:
    return 0.0 if rank > 10 else 1.0 / math.log2(rank + 1.0)


def active_interval_arrays(rooms: pd.DataFrame, room_map: pd.DataFrame):
    rr = rooms[["live_id", "start_timestamp", "end_timestamp"]].dropna().drop_duplicates("live_id").copy()
    rr[["live_id", "start_timestamp", "end_timestamp"]] = rr[["live_id", "start_timestamp", "end_timestamp"]].astype("int64")
    rm = room_map[["item_id", "live_id"]].astype("int64")
    rr = rr.merge(rm, on="live_id", how="inner", validate="one_to_one")
    if len(rr) != len(rm):
        missing = len(rm) - len(rr)
        raise ValueError(f"room interval mapping incomplete: {missing} mapped rooms missing intervals")
    starts = rr.sort_values("start_timestamp", kind="mergesort")
    ends = rr.sort_values("end_timestamp", kind="mergesort")
    return (
        starts.start_timestamp.to_numpy(np.int64),
        starts.item_id.to_numpy(np.int64),
        ends.end_timestamp.to_numpy(np.int64),
        ends.item_id.to_numpy(np.int64),
    )


def phase_order(phase_df: pd.DataFrame):
    return phase_df.sort_values(["time", "user_id"], kind="mergesort").reset_index(drop=True)


def candidate_sweep(phase_df: pd.DataFrame, interval_arrays):
    s_t, s_id, e_t, e_id = interval_arrays
    active = IndexedCounterSet()
    i = j = 0
    for r in phase_order(phase_df).itertuples(index=False):
        t = int(r.time)
        while i < len(s_t) and int(s_t[i]) <= t:
            active.add(int(s_id[i])); i += 1
        # Match the frozen room exporter: active iff start <= t < end.
        while j < len(e_t) and int(e_t[j]) <= t:
            active.remove(int(e_id[j])); j += 1
        target = int(r.item_id)
        was_active = target in active.index
        cands = np.asarray(active.items, dtype=np.int64)
        if not was_active:
            # Preserve the frozen sampled protocol's positive-plus-active-negatives semantics
            # if metadata marks a clicked target inactive. This should be rare/zero and is reported.
            cands = np.concatenate(([target], cands))
        elif len(cands) == 0:
            cands = np.asarray([target], dtype=np.int64)
        yield int(r.user_id), t, target, cands, bool(was_active)


def room_to_streamer_item_array(room_map: pd.DataFrame, streamer_map: pd.DataFrame) -> np.ndarray:
    sid_to_item = dict(zip(streamer_map.streamer_id.astype(int), streamer_map.item_id.astype(int)))
    n = int(room_map.item_id.max()) + 1
    out = np.zeros(n, dtype=np.int64)
    for r in room_map.itertuples(index=False):
        out[int(r.item_id)] = int(sid_to_item[int(r.streamer_id)])
    if np.any(out[1:] <= 0):
        raise ValueError("some room items have no streamer-item mapping")
    return out


def evaluate_alpha_grid(
    phase_df,
    interval_arrays,
    room_model,
    streamer_model,
    room_vecs,
    streamer_vecs,
    room_to_sitem,
):
    sums = np.zeros(len(ALPHA_GRID), dtype=np.float64)
    counts = []
    target_active = 0
    n = 0
    start = time.perf_counter()
    for uid, _t, target, cands, was_active in candidate_sweep(phase_df, interval_arrays):
        n += 1; target_active += int(was_active); counts.append(len(cands))
        target_idx = int(np.flatnonzero(cands == target)[0])
        rz = zscore(score_embedding_candidates(room_model, room_vecs[uid], cands))
        sids = room_to_sitem[cands]
        sz = zscore(score_embedding_candidates(streamer_model, streamer_vecs[uid], sids))
        for ai, alpha in enumerate(ALPHA_GRID):
            dual = float(alpha) * rz + (1.0 - float(alpha)) * sz
            sums[ai] += ndcg_scalar(rank_ge_at(dual, target_idx))
    means = sums / max(n, 1)
    best_idx = max(range(len(ALPHA_GRID)), key=lambda k: (means[k], float(ALPHA_GRID[k])))
    tuning = pd.DataFrame({
        "alpha_room": ALPHA_GRID,
        "alpha_streamer": 1.0 - ALPHA_GRID,
        "dev_full_active_ndcg10": means,
    })
    meta = {
        "events": int(n),
        "target_active_rate": float(target_active / max(n, 1)),
        "candidate_counts": summarize_counts(counts),
        "wall_seconds": float(time.perf_counter() - start),
    }
    return float(ALPHA_GRID[best_idx]), tuning, meta


def summarize_counts(counts):
    x = np.asarray(counts, dtype=float)
    if not len(x):
        return {}
    return {
        "mean": float(x.mean()),
        "median": float(np.median(x)),
        "p10": float(np.quantile(x, .10)),
        "p90": float(np.quantile(x, .90)),
        "p95": float(np.quantile(x, .95)),
        "max": int(x.max()),
        "min": int(x.min()),
    }


def score_phase(
    phase_name: str,
    phase_df: pd.DataFrame,
    interval_arrays,
    room_model,
    streamer_model,
    room_vecs,
    streamer_vecs,
    room_to_sitem,
    alpha_native: float,
    alpha_transfer: float,
    memory_pop,
    memory_hist,
    item_to_streamer,
    state_df: pd.DataFrame,
):
    state = state_df.set_index("user_id")
    rows = []
    counts = []
    target_active = 0
    start = time.perf_counter()
    for uid, t, target, cands, was_active in candidate_sweep(phase_df, interval_arrays):
        counts.append(len(cands)); target_active += int(was_active)
        hit = np.flatnonzero(cands == target)
        if len(hit) != 1:
            raise ValueError(f"{phase_name} user={uid}: target match count={len(hit)}")
        target_idx = int(hit[0])
        room_raw = score_embedding_candidates(room_model, room_vecs[uid], cands)
        stream_items = room_to_sitem[cands]
        streamer_raw = score_embedding_candidates(streamer_model, streamer_vecs[uid], stream_items)
        rz = zscore(room_raw); sz = zscore(streamer_raw)

        native = alpha_native * rz + (1.0 - alpha_native) * sz
        transfer = alpha_transfer * rz + (1.0 - alpha_transfer) * sz
        native_rank = rank_ge_at(native, target_idx)
        transfer_rank = rank_ge_at(transfer, target_idx)

        ms = memory_scores(cands, uid, memory_pop, memory_hist, item_to_streamer)
        mrank = memory_rank(cands, ms, target)

        row = {
            "user_id": uid,
            "time": t,
            "target_item": target,
            "candidate_count": int(len(cands)),
            "target_metadata_active": bool(was_active),
            "native_base_rank": int(native_rank),
            "native_base_ndcg10": float(ndcg_scalar(native_rank)),
            "native_base_hr10": float(native_rank <= 10),
            "transfer_base_rank": int(transfer_rank),
            "transfer_base_ndcg10": float(ndcg_scalar(transfer_rank)),
            "transfer_base_hr10": float(transfer_rank <= 10),
            "memory_rank": int(mrank),
            "memory_ndcg10": float(ndcg_scalar(mrank)),
            "memory_hr10": float(mrank <= 10),
        }
        native_conf = conf_tuple(native)
        transfer_conf = conf_tuple(transfer)
        row.update({f"native_{k}": float(v) for k, v in zip(CONF_FEATURES, native_conf)})
        row.update({f"transfer_{k}": float(v) for k, v in zip(CONF_FEATURES, transfer_conf)})
        if uid not in state.index:
            raise KeyError(f"missing user state for uid={uid}")
        for k in USER_FEATURES:
            row[k] = float(state.loc[uid, k])
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("user_id").reset_index(drop=True)
    meta = {
        "phase": phase_name,
        "events": int(len(out)),
        "target_active_rate": float(target_active / max(len(out), 1)),
        "candidate_counts": summarize_counts(counts),
        "wall_seconds": float(time.perf_counter() - start),
    }
    return out, meta


def fit_native_gate(dev: pd.DataFrame):
    X = dev[[f"native_{k}" for k in CONF_FEATURES] + USER_FEATURES].copy()
    # Restore the frozen feature order: state, then confidence.
    X = np.column_stack([
        dev[USER_FEATURES].to_numpy(float),
        dev[[f"native_{k}" for k in CONF_FEATURES]].to_numpy(float),
    ])
    y = (dev.memory_ndcg10 - dev.native_base_ndcg10).to_numpy(float)
    base = dev.native_base_ndcg10.to_numpy(float)
    mem = dev.memory_ndcg10.to_numpy(float)
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    oof = cross_val_predict(hgb(), X, y, cv=cv, method="predict", n_jobs=1)
    threshold, use, dev_ndcg = choose_threshold(oof, base, mem)
    model = clone(hgb()).fit(X, y)
    return model, float(threshold), oof, use, float(dev_ndcg)


def apply_gate(model, threshold: float, df: pd.DataFrame, prefix: str):
    X = np.column_stack([
        df[USER_FEATURES].to_numpy(float),
        df[[f"{prefix}_{k}" for k in CONF_FEATURES]].to_numpy(float),
    ])
    pred = model.predict(X)
    use = pred > threshold
    return pred, use


def metric_block(base: np.ndarray, mem: np.ndarray, use: np.ndarray, seed: int):
    selected = np.where(use, mem, base)
    delta, lo, hi = bootstrap_delta(selected - base, seed=seed, n_boot=5000)
    return selected, {
        "base_ndcg10": float(base.mean()),
        "memory_ndcg10": float(mem.mean()),
        "selective_ndcg10": float(selected.mean()),
        "selective_minus_base": float(delta),
        "ci95": [float(lo), float(hi)],
        "invocation_rate": float(use.mean()),
        "selected_n": int(use.sum()),
    }


def hr_block(base_hr, mem_hr, use):
    sel = np.where(use, mem_hr, base_hr)
    return {
        "base_hr10": float(np.mean(base_hr)),
        "memory_hr10": float(np.mean(mem_hr)),
        "selective_hr10": float(np.mean(sel)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rechorus-source", type=Path, required=True)
    ap.add_argument("--data-root", type=Path, required=True)
    ap.add_argument("--prepared-dir", type=Path, required=True)
    ap.add_argument("--room-dataset", required=True)
    ap.add_argument("--streamer-dataset", required=True)
    ap.add_argument("--room-model", type=Path, required=True)
    ap.add_argument("--streamer-model", type=Path, required=True)
    ap.add_argument("--sampled-gate-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n-neg", type=int, default=574)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass

    t_all = time.perf_counter()
    room_dir = args.data_root / args.room_dataset
    streamer_dir = args.data_root / args.streamer_dataset
    train, dev, test, item_to_streamer = load_data(room_dir, args.n_neg)
    room_map = pd.read_csv(room_dir / "room_item_map.tsv", sep="\t")
    streamer_map = pd.read_csv(streamer_dir / "streamer_item_map.tsv", sep="\t")
    rooms = pd.read_pickle(args.prepared_dir / "rooms.pkl")
    interval_arrays = active_interval_arrays(rooms, room_map)
    room_to_sitem = room_to_streamer_item_array(room_map, streamer_map)

    room_model, room_corpus = load_rechorus(args.rechorus_source, args.data_root, args.room_dataset, args.room_model)
    streamer_model, streamer_corpus = load_rechorus(args.rechorus_source, args.data_root, args.streamer_dataset, args.streamer_model)

    # Precompute only 64-d user representations; candidate scores are streamed event by event.
    phase_vecs = {}
    for phase in ("dev", "test"):
        phase_vecs[("room", phase)] = encode_phase_users(room_model, room_corpus, phase)
        phase_vecs[("streamer", phase)] = encode_phase_users(streamer_model, streamer_corpus, phase)

    sampled_report = json.loads((args.sampled_gate_dir / "report.json").read_text())
    alpha_transfer = float(sampled_report["alpha_room"])
    transfer_gate = joblib.load(args.sampled_gate_dir / "hgb_gate.joblib")
    transfer_threshold = float(sampled_report["gates"]["hgb"]["threshold"])

    # A2 dev-native alpha is selected using only full-active dev rankings.
    alpha_native, tuning, alpha_meta = evaluate_alpha_grid(
        dev, interval_arrays,
        room_model, streamer_model,
        phase_vecs[("room", "dev")], phase_vecs[("streamer", "dev")],
        room_to_sitem,
    )
    tuning.to_csv(args.out_dir / "full_active_alpha_tuning.csv", index=False)

    pop = popularity_by_streamer(train, item_to_streamer)
    train_dev = pd.concat([train, dev[["user_id", "item_id", "time"]]], ignore_index=True)
    hist_dev = histories(train, item_to_streamer)
    hist_test = histories(train_dev, item_to_streamer)
    state_dev = user_features(train, item_to_streamer)
    state_test = user_features(train_dev, item_to_streamer)

    dev_scored, dev_meta = score_phase(
        "dev", dev, interval_arrays,
        room_model, streamer_model,
        phase_vecs[("room", "dev")], phase_vecs[("streamer", "dev")],
        room_to_sitem, alpha_native, alpha_transfer,
        pop, hist_dev, item_to_streamer, state_dev,
    )

    native_gate, native_threshold, native_oof, native_dev_use, native_dev_ndcg = fit_native_gate(dev_scored)
    dev_scored["native_oof_pred_delta"] = native_oof
    dev_scored["native_oof_use_memory"] = native_dev_use

    # A1 strict transfer on full-active dev is descriptive only; no full-active calibration.
    dev_transfer_pred, dev_transfer_use = apply_gate(transfer_gate, transfer_threshold, dev_scored, "transfer")
    dev_scored["transfer_pred_delta"] = dev_transfer_pred
    dev_scored["transfer_use_memory"] = dev_transfer_use

    # One full-active test scoring pass; both A1 and A2 are evaluated from the same frozen test scores.
    test_scored, test_meta = score_phase(
        "test", test, interval_arrays,
        room_model, streamer_model,
        phase_vecs[("room", "test")], phase_vecs[("streamer", "test")],
        room_to_sitem, alpha_native, alpha_transfer,
        pop, hist_test, item_to_streamer, state_test,
    )

    transfer_pred, transfer_use = apply_gate(transfer_gate, transfer_threshold, test_scored, "transfer")
    native_pred, native_use = apply_gate(native_gate, native_threshold, test_scored, "native")

    test_scored["transfer_pred_delta"] = transfer_pred
    test_scored["transfer_use_memory"] = transfer_use
    test_scored["native_pred_delta"] = native_pred
    test_scored["native_use_memory"] = native_use

    mem = test_scored.memory_ndcg10.to_numpy(float)
    a1_base = test_scored.transfer_base_ndcg10.to_numpy(float)
    a2_base = test_scored.native_base_ndcg10.to_numpy(float)
    a1_sel, a1 = metric_block(a1_base, mem, transfer_use, SEED + 1101)
    a2_sel, a2 = metric_block(a2_base, mem, native_use, SEED + 1102)
    a1.update(hr_block(test_scored.transfer_base_hr10.to_numpy(float), test_scored.memory_hr10.to_numpy(float), transfer_use))
    a2.update(hr_block(test_scored.native_base_hr10.to_numpy(float), test_scored.memory_hr10.to_numpy(float), native_use))
    test_scored["transfer_selective_ndcg10"] = a1_sel
    test_scored["native_selective_ndcg10"] = a2_sel

    # Always-Memory deltas against each base, useful to characterize the full-active regime.
    a1_mem = bootstrap_delta(mem - a1_base, seed=SEED + 1111, n_boot=5000)
    a2_mem = bootstrap_delta(mem - a2_base, seed=SEED + 1112, n_boot=5000)
    a1["memory_minus_base"] = {"mean": a1_mem[0], "ci95": [a1_mem[1], a1_mem[2]]}
    a2["memory_minus_base"] = {"mean": a2_mem[0], "ci95": [a2_mem[1], a2_mem[2]]}

    sampled_hgb = sampled_report["gates"]["hgb"]
    report = {
        "experiment": "full_active_dual_id_candidate_universe",
        "task": "next_live_room",
        "protocol": "all metadata-active rooms at each target timestamp; streamed per event",
        "legality": "start_timestamp <= t < end_timestamp; clicked target is added only if metadata marks it inactive, matching frozen positive-plus-active-negatives semantics",
        "users": int(len(test_scored)),
        "rechorus_commit": RECHORUS_COMMIT,
        "sampled_reference": {
            "candidate_count": int(sampled_report["candidate_count"]),
            "alpha_room": float(sampled_report["alpha_room"]),
            "dual_id_ndcg10": float(sampled_report["dual_id_test_ndcg10"]),
            "memory_ndcg10": float(sampled_report["memory_test_ndcg10"]),
            "selective_hgb_ndcg10": float(sampled_hgb["test_ndcg10"]),
            "selective_hgb_delta": float(sampled_hgb["test_delta_vs_dual"]),
            "selective_hgb_invocation": float(sampled_hgb["test_invocation_rate"]),
        },
        "A1_strict_transfer": {
            "purpose": "candidate-universe transfer stress test",
            "alpha_room": alpha_transfer,
            "gate_source": "sampled-regime HGB reconstructed/serialized by gate-compression workflow",
            "threshold": transfer_threshold,
            "feature_policy": "same feature definitions, mechanically recomputed over full-active candidates; no full-active calibration",
            **a1,
            "dev_full_active_invocation_rate_descriptive": float(dev_transfer_use.mean()),
        },
        "A2_full_active_native": {
            "purpose": "primary full-active scientific validity test",
            "alpha_room_dev_selected": alpha_native,
            "alpha_streamer_dev_selected": 1.0 - alpha_native,
            "gate": "HGB fit on full-active dev relative utility only",
            "threshold_dev_selected": native_threshold,
            "dev_oof_selective_ndcg10": native_dev_ndcg,
            "dev_oof_invocation_rate": float(native_dev_use.mean()),
            **a2,
            "pass_rule": "PASS iff Selective - Dual-ID mean > 0 and paired user-bootstrap 95% CI lower bound > 0",
            "pass": bool(a2["selective_minus_base"] > 0 and a2["ci95"][0] > 0),
        },
        "alpha_selection_meta": alpha_meta,
        "dev_meta": dev_meta,
        "test_meta": test_meta,
        "candidate_shift_guardrail": "A1 and A2 answer different questions because candidate-wise z-normalization and confidence features change with the candidate universe. A1 is transfer robustness; A2 is the primary validity result.",
        "wall_seconds_total": float(time.perf_counter() - t_all),
    }

    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    dev_scored.to_csv(args.out_dir / "per_user_dev_full_active.csv.gz", index=False, compression="gzip")
    test_scored.to_csv(args.out_dir / "per_user_test_full_active.csv.gz", index=False, compression="gzip")
    joblib.dump(native_gate, args.out_dir / "full_active_native_hgb.joblib")
    (args.out_dir / "full_active_native_gate.json").write_text(json.dumps({
        "features": FEATURES,
        "alpha_room": alpha_native,
        "threshold": native_threshold,
        "dev_oof_ndcg10": native_dev_ndcg,
        "dev_invocation_rate": float(native_dev_use.mean()),
    }, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
