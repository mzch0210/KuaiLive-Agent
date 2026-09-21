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


def cpu_model() -> str:
    try:
        out = subprocess.check_output(["lscpu"], text=True)
        for line in out.splitlines():
            if line.lower().startswith("model name:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return platform.processor() or "unknown"


def benchmark(system: str, fn, queries, warmup: int, replica: int):
    checksum = 0.0
    with torch.inference_mode():
        for q in queries[: min(warmup, len(queries))]:
            checksum += float(fn(q))
    gc.collect(); gc.disable()
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
                    "budget": None,
                    "query_id": int(q),
                    "latency_ms": dt,
                })
    finally:
        gc.enable()
    return rows, checksum


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds-source", type=Path, required=True)
    ap.add_argument("--data-root", type=Path, required=True)
    ap.add_argument("--dataset", default="KuaiLiveDSFull")
    ap.add_argument("--model-path", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--replica", type=int, required=True)
    ap.add_argument("--samples", type=int, default=1200)
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20260918)
    a = ap.parse_args(); a.out_dir.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass

    sys.path.insert(0, str(a.ds_source.resolve()))
    from helpers.BaseReader import BaseReader
    from models.PRL import PRL
    from utils.constants import ITEM_SEQ, ITEM_SEQ_LEN, MAX_ITEM_SEQ_LEN

    args = SimpleNamespace(
        sep=",", path=str(a.data_root.resolve()), dataset=a.dataset,
        device=torch.device("cpu"), model_path=str(a.model_path.resolve()), buffer=0,
        dropout=.2, test_all=1, emb_size=64, num_layers=1, num_heads=4,
        inner_size=128, hidden_act="gelu", layer_norm_eps=1e-12,
        initializer_range=.02, temperature=.07, reason_step=2, pl_weight=1.0,
        temp_scale=5.0, noise_factor=.01, cl_weight=1.0, warmup=2,
    )
    corpus = BaseReader(args)
    model = PRL(args, corpus).to(args.device)
    model.load_state_dict(torch.load(a.model_path, map_location="cpu"))
    model.eval()

    c = np.load(a.data_root / a.dataset / "eval_candidates.npz", allow_pickle=False)
    candidates = c["test"].astype(np.int64)
    data = corpus.data_dict["test"]
    if len(candidates) != len(data[ITEM_SEQ]):
        raise ValueError("candidate/test length mismatch")

    rng = np.random.default_rng(a.seed + a.replica)
    indices = rng.permutation(len(candidates))[: min(a.samples, len(candidates))].astype(int).tolist()
    cand_tensors = {i: torch.from_numpy(candidates[i]) for i in indices}

    W = model.item_emb.weight

    def hidden(i: int, reason_step: int):
        item_seq_ids = data[ITEM_SEQ][i:i+1]
        item_seq_len = data[ITEM_SEQ_LEN][i:i+1]
        padding_mask = item_seq_ids != (model.item_num - 1)
        valid_pos_ids = torch.cumsum(padding_mask.long(), dim=1) - 1
        pos_ids = torch.where(padding_mask, valid_pos_ids, MAX_ITEM_SEQ_LEN)
        input_embs = model.item_emb(item_seq_ids) + model.pos_emb(pos_ids)
        mo = model.model(input_embs, item_seq_len, noise_factor=0.0, reason_step=reason_step)
        return mo[:, -1, :]

    def score(i: int, reason_step: int):
        h = hidden(i, reason_step)
        emb = W[cand_tensors[i]]
        s = torch.einsum("bd,kd->bk", h, emb)[0] / model.temperature
        return float(torch.topk(s, k=10).values.sum().item())

    def fast_query(i):
        return score(i, 0)

    def slow_query(i):
        return score(i, 2)

    # The paper-faithful selector is a tiny 64->32->1 MLP. We isolate its traversal
    # cost using precomputed fast hidden states so fast model compute is not double-counted.
    torch.manual_seed(a.seed)
    selector = torch.nn.Sequential(torch.nn.Linear(64, 32), torch.nn.ReLU(), torch.nn.Linear(32, 1)).eval()
    fast_hidden = {}
    with torch.inference_mode():
        for i in indices:
            fast_hidden[i] = hidden(i, 0).detach()

    def selector_query(i):
        return float(torch.sigmoid(selector(fast_hidden[i])).item())

    all_rows = []; checksums = {}
    for system, fn in [
        ("ds_fast_candidate", fast_query),
        ("ds_slow_reason2_candidate", slow_query),
        ("ds_selector_mlp_only", selector_query),
    ]:
        rows, cs = benchmark(system, fn, indices, a.warmup, a.replica)
        all_rows.extend(rows); checksums[system] = cs

    out = pd.DataFrame(all_rows)
    out.to_csv(a.out_dir / f"ds_latency_replica_{a.replica}.csv.gz", index=False, compression="gzip")
    summary = []
    for system, g in out.groupby("system"):
        x = g.latency_ms.to_numpy(float)
        summary.append({
            "replica": a.replica,
            "system": system,
            "budget": None,
            "n": len(x),
            "mean_ms": float(x.mean()),
            "p50_ms": float(np.quantile(x, .50)),
            "p95_ms": float(np.quantile(x, .95)),
            "p99_ms": float(np.quantile(x, .99)),
        })
    pd.DataFrame(summary).to_csv(a.out_dir / f"ds_summary_replica_{a.replica}.csv", index=False)
    meta = {
        "replica": a.replica,
        "cpu_model": cpu_model(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_threads": torch.get_num_threads(),
        "candidate_count": int(candidates.shape[1]),
        "history_max": 50,
        "batch_size": 1,
        "timing_scope": "warm steady-state official PRL representation path plus scoring of the frozen 575 candidate streamers through top-10; full-item softmax intentionally excluded because online candidate ranking is the matched protocol",
        "fast": "reason_step=0",
        "slow": "reason_step=2",
        "selector": "64->32->1 MLP traversal isolated on precomputed fast hidden state",
        "params": int(sum(p.numel() for p in model.parameters())),
        "checksums": checksums,
    }
    (a.out_dir / f"ds_meta_replica_{a.replica}.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    print(pd.DataFrame(summary).to_string(index=False))


if __name__ == "__main__":
    main()
