from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from room_level_selective_agent import (  # noqa: E402
    CONF_FEATURES,
    USER_FEATURES,
    hgb,
    histories,
    load_data,
    memory_scores,
    parse_list,
    popularity_by_streamer,
)
from dual_id_room_baseline import conf_tuple  # noqa: E402

EPS = 1e-12
BUDGETS = [0.05, 0.10, 0.15, 0.20, 0.30]


def cpu_model() -> str:
    try:
        out = subprocess.check_output(["lscpu"], text=True)
        for line in out.splitlines():
            if line.lower().startswith("model name:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return platform.processor() or "unknown"


def torch_zscore(x: torch.Tensor) -> torch.Tensor:
    sd = x.std(unbiased=False)
    if float(sd) <= EPS:
        return torch.zeros_like(x)
    return (x - x.mean()) / sd


def top10_checksum_torch(x: torch.Tensor) -> float:
    return float(torch.topk(x, k=min(10, x.numel())).values.sum().item())


def top10_checksum_np(x: np.ndarray) -> float:
    k = min(10, len(x))
    idx = np.argpartition(-x, k - 1)[:k]
    return float(x[idx].sum())


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
        buffer=1,
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
    ds = SASRec.Dataset(model, corpus, "test")
    ds.prepare()
    return model, corpus, ds


def tensor_feed(ds, index: int) -> dict:
    b = ds.collate_batch([ds[index]])
    return {k: v for k, v in b.items() if torch.is_tensor(v)}


def benchmark(system: str, fn, queries, warmup: int, replica: int, budget=None):
    if not queries:
        return [], 0.0
    warm = queries[: min(warmup, len(queries))]
    checksum = 0.0
    with torch.inference_mode():
        for q in warm:
            checksum += float(fn(q))
    gc.collect()
    gc.disable()
    rows = []
    try:
        with torch.inference_mode():
            for q in queries:
                t0 = time.perf_counter_ns()
                val = float(fn(q))
                dt = (time.perf_counter_ns() - t0) / 1e6
                checksum += val
                rows.append({
                    "replica": replica,
                    "system": system,
                    "budget": budget,
                    "query_id": int(q),
                    "latency_ms": dt,
                })
    finally:
        gc.enable()
    return rows, checksum


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rechorus-source", type=Path, required=True)
    ap.add_argument("--data-root", type=Path, required=True)
    ap.add_argument("--room-dataset", default="KuaiLiveShopRoomDualID")
    ap.add_argument("--streamer-dataset", default="KuaiLiveShopStreamerParallel")
    ap.add_argument("--room-model", type=Path, required=True)
    ap.add_argument("--streamer-model", type=Path, required=True)
    ap.add_argument("--frozen-test", type=Path, required=True)
    ap.add_argument("--frozen-report", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--replica", type=int, required=True)
    ap.add_argument("--samples", type=int, default=1200)
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20260918)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass

    room_model, room_corpus, room_ds = load_rechorus(
        a.rechorus_source, a.data_root, a.room_dataset, a.room_model
    )
    # Purge ReChorus module names only after both models are loaded from the same source.
    streamer_model, streamer_corpus, streamer_ds = load_rechorus(
        a.rechorus_source, a.data_root, a.streamer_dataset, a.streamer_model
    )
    if len(room_ds) != len(streamer_ds):
        raise ValueError(("room/streamer test size mismatch", len(room_ds), len(streamer_ds)))

    room_data_dir = a.data_root / a.room_dataset
    train, dev, test, item_to_streamer = load_data(room_data_dir, 574)
    frozen = pd.read_csv(a.frozen_test).sort_values("user_id").reset_index(drop=True)
    report = json.loads(a.frozen_report.read_text())
    alpha_room = float(report["alpha_room"])
    alpha_streamer = 1.0 - alpha_room

    ds_uids = np.asarray(room_ds.data["user_id"], dtype=int)
    if not np.array_equal(ds_uids, np.asarray(streamer_ds.data["user_id"], dtype=int)):
        raise ValueError("room/streamer test user alignment mismatch")
    f_uids = frozen.user_id.to_numpy(dtype=int)
    if not np.array_equal(np.sort(ds_uids), f_uids):
        raise ValueError("frozen test user ids do not align with ReChorus test set")

    uid_to_frozen = frozen.set_index("user_id")
    user_state = {
        int(uid): uid_to_frozen.loc[int(uid), USER_FEATURES].to_numpy(dtype=float)
        for uid in f_uids
    }
    gate = hgb().fit(
        frozen[USER_FEATURES + CONF_FEATURES].to_numpy(float),
        frozen.primary_pred_delta.to_numpy(float),
    )

    pop = popularity_by_streamer(train, item_to_streamer)
    train_dev = pd.concat([train, dev[["user_id", "item_id", "time"]]], ignore_index=True)
    hist = histories(train_dev, item_to_streamer)
    t_by_uid = test.set_index("user_id")
    cand_by_uid = {}
    for uid in f_uids:
        r = t_by_uid.loc[int(uid)]
        cand_by_uid[int(uid)] = np.concatenate(
            ([int(r.item_id)], parse_list(r.neg_items, int))
        ).astype(np.int64)

    actual_mask = uid_to_frozen.primary_use_memory.astype(bool).to_dict()
    score_order = frozen.sort_values(
        ["primary_pred_delta", "user_id"], ascending=[False, True], kind="mergesort"
    ).user_id.to_numpy(dtype=int)
    budget_masks = {}
    for b in BUDGETS:
        k = int(round(b * len(frozen)))
        chosen = set(score_order[:k].tolist())
        budget_masks[b] = {int(uid): int(uid) in chosen for uid in f_uids}

    rng = np.random.default_rng(a.seed + a.replica)
    indices = rng.permutation(len(room_ds))[: min(a.samples, len(room_ds))].astype(int).tolist()
    room_feeds = {i: tensor_feed(room_ds, i) for i in indices}
    streamer_feeds = {i: tensor_feed(streamer_ds, i) for i in indices}
    uid_by_index = {i: int(room_ds.data["user_id"][i]) for i in indices}

    def room_query(i):
        s = room_model(room_feeds[i])["prediction"][0]
        return top10_checksum_torch(s)

    def streamer_query(i):
        s = streamer_model(streamer_feeds[i])["prediction"][0]
        return top10_checksum_torch(s)

    def dual_scores(i):
        rs = room_model(room_feeds[i])["prediction"][0]
        ss = streamer_model(streamer_feeds[i])["prediction"][0]
        return alpha_room * torch_zscore(rs) + alpha_streamer * torch_zscore(ss)

    def dual_query(i):
        return top10_checksum_torch(dual_scores(i))

    def mem_for_uid(uid: int):
        s = memory_scores(cand_by_uid[uid], uid, pop, hist, item_to_streamer)
        return top10_checksum_np(s)

    def memory_query(i):
        return mem_for_uid(uid_by_index[i])

    def gate_predict_from_scores(uid: int, scores: torch.Tensor):
        c = np.asarray(conf_tuple(scores.detach().numpy()), dtype=float)
        x = np.concatenate([user_state[uid], c]).reshape(1, -1)
        return float(gate.predict(x)[0])

    def gate_only_query(i):
        uid = uid_by_index[i]
        # Frozen confidence features avoid charging base inference twice; this isolates HGB traversal.
        x = uid_to_frozen.loc[uid, USER_FEATURES + CONF_FEATURES].to_numpy(dtype=float).reshape(1, -1)
        return float(gate.predict(x)[0])

    def selective_query(mask):
        def _q(i):
            uid = uid_by_index[i]
            ds = dual_scores(i)
            gate_predict_from_scores(uid, ds)  # execute real gate path; routing mask stays scientifically frozen
            if mask[uid]:
                return mem_for_uid(uid)
            return top10_checksum_torch(ds)
        return _q

    all_rows = []
    checksums = {}
    for system, fn, budget in [
        ("room_sasrec", room_query, None),
        ("streamer_sasrec", streamer_query, None),
        ("dual_id", dual_query, None),
        ("memory_fusion_cached", memory_query, None),
        ("gate_hgb_predict_only", gate_only_query, None),
        ("selective_frozen_14.25pct", selective_query(actual_mask), float(report["test_gate_rate"])),
    ]:
        rows, cs = benchmark(system, fn, indices, a.warmup, a.replica, budget)
        all_rows.extend(rows); checksums[system] = cs

    for b in BUDGETS:
        system = f"selective_budget_{int(round(100*b)):02d}pct"
        rows, cs = benchmark(system, selective_query(budget_masks[b]), indices, a.warmup, a.replica, b)
        all_rows.extend(rows); checksums[system] = cs

    out = pd.DataFrame(all_rows)
    out.to_csv(a.out_dir / f"ours_latency_replica_{a.replica}.csv.gz", index=False, compression="gzip")
    summary = []
    for (system, budget), g in out.groupby(["system", "budget"], dropna=False):
        x = g.latency_ms.to_numpy(float)
        summary.append({
            "replica": a.replica,
            "system": system,
            "budget": None if pd.isna(budget) else float(budget),
            "n": len(x),
            "mean_ms": float(x.mean()),
            "p50_ms": float(np.quantile(x, .50)),
            "p95_ms": float(np.quantile(x, .95)),
            "p99_ms": float(np.quantile(x, .99)),
        })
    pd.DataFrame(summary).to_csv(a.out_dir / f"ours_summary_replica_{a.replica}.csv", index=False)
    meta = {
        "replica": a.replica,
        "cpu_model": cpu_model(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_threads": torch.get_num_threads(),
        "candidate_count": 575,
        "history_max": 50,
        "batch_size": 1,
        "timing_scope": "warm steady-state online scoring through top-10; dataset parsing/model loading/state construction excluded",
        "memory_state": "cached short/long streamer history and popularity; candidate room->streamer mapping included",
        "gate": "same HistGradientBoostingRegressor configuration; fitted to frozen gate outputs for timing only; routing masks remain frozen from the scientific experiment",
        "alpha_room": alpha_room,
        "alpha_streamer": alpha_streamer,
        "frozen_gate_rate": float(report["test_gate_rate"]),
        "room_params": int(sum(p.numel() for p in room_model.parameters())),
        "streamer_params": int(sum(p.numel() for p in streamer_model.parameters())),
        "checksums": checksums,
    }
    (a.out_dir / f"ours_meta_replica_{a.replica}.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    print(pd.DataFrame(summary).to_string(index=False))


if __name__ == "__main__":
    main()
