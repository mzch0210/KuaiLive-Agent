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

import joblib
import numpy as np
import pandas as pd
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from dual_id_room_baseline import conf_tuple
from room_level_selective_agent import (
    CONF_FEATURES,
    USER_FEATURES,
    histories,
    load_data,
    memory_scores,
    parse_list,
    popularity_by_streamer,
    user_features,
)

EPS = 1e-12


def cpu_model() -> str:
    try:
        out = subprocess.check_output(['lscpu'], text=True)
        for line in out.splitlines():
            if line.lower().startswith('model name:'):
                return line.split(':', 1)[1].strip()
    except Exception:
        pass
    return platform.processor() or 'unknown'


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
    src = str((source / 'src').resolve())
    if src not in sys.path:
        sys.path.insert(0, src)
    from helpers.SeqReader import SeqReader
    from models.sequential.SASRec import SASRec

    args = SimpleNamespace(
        sep='\t', path=str(data_root.resolve()) + '/', dataset=dataset,
        device=torch.device('cpu'), model_path=str(model_path.resolve()), buffer=1,
        dropout=0.0, test_all=0, num_neg=1, history_max=50,
        emb_size=64, num_layers=1, num_heads=4,
    )
    corpus = SeqReader(args)
    model = SASRec(args, corpus).to(args.device)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    ds = SASRec.Dataset(model, corpus, 'test')
    ds.prepare()
    return model, ds


def tensor_feed(ds, index: int) -> dict:
    b = ds.collate_batch([ds[index]])
    return {k: v for k, v in b.items() if torch.is_tensor(v)}


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
                rows.append({'replica': replica, 'system': system, 'budget': None,
                             'query_id': int(q), 'latency_ms': dt})
    finally:
        gc.enable()
    return rows, checksum


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rechorus-source', type=Path, required=True)
    ap.add_argument('--data-root', type=Path, required=True)
    ap.add_argument('--room-dataset', required=True)
    ap.add_argument('--streamer-dataset', required=True)
    ap.add_argument('--room-model', type=Path, required=True)
    ap.add_argument('--streamer-model', type=Path, required=True)
    ap.add_argument('--gate-dir', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--replica', type=int, required=True)
    ap.add_argument('--samples', type=int, default=1200)
    ap.add_argument('--warmup', type=int, default=100)
    ap.add_argument('--seed', type=int, default=20260918)
    a = ap.parse_args(); a.out_dir.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault('OMP_NUM_THREADS', '1')
    os.environ.setdefault('MKL_NUM_THREADS', '1')
    torch.set_num_threads(1)
    try: torch.set_num_interop_threads(1)
    except RuntimeError: pass

    report = json.loads((a.gate_dir / 'report.json').read_text())
    params = np.load(a.gate_dir / 'light_gate_params.npz', allow_pickle=False)
    hgb_gate = joblib.load(a.gate_dir / 'hgb_gate.joblib')
    thresholds = {k: float(v['threshold']) for k, v in report['gates'].items()}
    scientific = pd.read_csv(a.gate_dir / 'per_user_test.csv.gz').set_index('user_id')
    route_masks = {
        'hgb': scientific.hgb_use_memory.astype(bool).to_dict(),
        'ridge': scientific.ridge_use_memory.astype(bool).to_dict(),
        'tiny_mlp': scientific.tiny_mlp_use_memory.astype(bool).to_dict(),
    }

    room_model, room_ds = load_rechorus(a.rechorus_source, a.data_root, a.room_dataset, a.room_model)
    streamer_model, streamer_ds = load_rechorus(a.rechorus_source, a.data_root, a.streamer_dataset, a.streamer_model)
    if len(room_ds) != len(streamer_ds):
        raise ValueError('room/streamer test size mismatch')

    room_data_dir = a.data_root / a.room_dataset
    train, dev, test, item_to_streamer = load_data(room_data_dir, 574)
    train_dev = pd.concat([train, dev[['user_id', 'item_id', 'time']]], ignore_index=True)
    pop = popularity_by_streamer(train, item_to_streamer)
    hist = histories(train_dev, item_to_streamer)
    feats = user_features(train_dev, item_to_streamer).set_index('user_id')
    user_state = {int(uid): feats.loc[int(uid), USER_FEATURES].to_numpy(float) for uid in feats.index}
    t_by_uid = test.set_index('user_id')
    cand_by_uid = {}
    for uid in t_by_uid.index.astype(int):
        r = t_by_uid.loc[uid]
        cand_by_uid[uid] = np.concatenate(([int(r.item_id)], parse_list(r.neg_items, int))).astype(np.int64)

    room_uids = np.asarray(room_ds.data['user_id'], dtype=int)
    streamer_uids = np.asarray(streamer_ds.data['user_id'], dtype=int)
    if not np.array_equal(room_uids, streamer_uids):
        raise ValueError('room/streamer user alignment mismatch')

    rng = np.random.default_rng(a.seed + a.replica)
    indices = rng.permutation(len(room_ds))[: min(a.samples, len(room_ds))].astype(int).tolist()
    room_feeds = {i: tensor_feed(room_ds, i) for i in indices}
    streamer_feeds = {i: tensor_feed(streamer_ds, i) for i in indices}
    uid_by_index = {i: int(room_uids[i]) for i in indices}

    alpha_room = float(report['alpha_room']); alpha_streamer = 1.0 - alpha_room

    def dual_scores(i):
        rs = room_model(room_feeds[i])['prediction'][0]
        ss = streamer_model(streamer_feeds[i])['prediction'][0]
        return alpha_room * torch_zscore(rs) + alpha_streamer * torch_zscore(ss)

    def x_from_dual(i, ds):
        uid = uid_by_index[i]
        c = np.asarray(conf_tuple(ds.detach().numpy()), dtype=float)
        return np.concatenate([user_state[uid], c])

    def memory_for_uid(uid):
        s = memory_scores(cand_by_uid[uid], uid, pop, hist, item_to_streamer)
        return top10_checksum_np(s)

    rmean=params['ridge_mean']; rscale=params['ridge_scale']; rcoef=params['ridge_coef']; rint=float(params['ridge_intercept'][0])
    mmean=params['mlp_mean']; mscale=params['mlp_scale']; w1=params['mlp_w1']; b1=params['mlp_b1']; w2=params['mlp_w2']; b2=float(params['mlp_b2'][0])

    def pred_hgb(x): return float(hgb_gate.predict(np.asarray(x, float).reshape(1, -1))[0])
    def pred_ridge(x):
        z=(np.asarray(x,float)-rmean)/rscale
        return float(np.dot(rcoef,z)+rint)
    def pred_mlp(x):
        z=(np.asarray(x,float)-mmean)/mscale
        h=np.maximum(w1 @ z + b1, 0.0)
        return float((w2 @ h).reshape(-1)[0] + b2)

    def dual_query(i): return top10_checksum_torch(dual_scores(i))
    def memory_query(i): return memory_for_uid(uid_by_index[i])

    frozen_x = {}
    with torch.inference_mode():
        for i in indices:
            frozen_x[i]=x_from_dual(i, dual_scores(i))

    def gate_hgb(i): return pred_hgb(frozen_x[i])
    def gate_ridge(i): return pred_ridge(frozen_x[i])
    def gate_mlp(i): return pred_mlp(frozen_x[i])

    def selective(gate_name, pred_fn, threshold):
        mask = route_masks[gate_name]
        def _q(i):
            uid=uid_by_index[i]
            ds=dual_scores(i)
            x=x_from_dual(i, ds)
            pred_fn(x)
            if bool(mask[uid]):
                return memory_for_uid(uid)
            return top10_checksum_torch(ds)
        return _q

    systems = [
        ('dual_id', dual_query),
        ('memory_fusion_cached', memory_query),
        ('gate_hgb_predict_only', gate_hgb),
        ('gate_ridge_numpy_only', gate_ridge),
        ('gate_tiny_mlp_numpy_only', gate_mlp),
        ('selective_hgb', selective('hgb', pred_hgb, thresholds['hgb'])),
        ('selective_ridge', selective('ridge', pred_ridge, thresholds['ridge'])),
        ('selective_tiny_mlp', selective('tiny_mlp', pred_mlp, thresholds['tiny_mlp'])),
    ]

    rows=[]; checksums={}
    for name,fn in systems:
        r,cs=benchmark(name,fn,indices,a.warmup,a.replica)
        rows.extend(r); checksums[name]=cs
    out=pd.DataFrame(rows)
    out.to_csv(a.out_dir / f'gate_latency_replica_{a.replica}.csv.gz', index=False, compression='gzip')

    summary=[]
    for system,g in out.groupby('system'):
        x=g.latency_ms.to_numpy(float)
        summary.append({'replica':a.replica,'system':system,'n':len(x),'mean_ms':float(x.mean()),
                        'p50_ms':float(np.quantile(x,.5)),'p95_ms':float(np.quantile(x,.95)),
                        'p99_ms':float(np.quantile(x,.99))})
    pd.DataFrame(summary).to_csv(a.out_dir / f'gate_summary_replica_{a.replica}.csv', index=False)
    meta={'replica':a.replica,'cpu_model':cpu_model(),'python':platform.python_version(),'torch':torch.__version__,
          'torch_threads':torch.get_num_threads(),'candidate_count':575,'history_max':50,'batch_size':1,
          'timing_scope':'warm steady-state batch-1 scoring through top-10; cached user/memory state; real gate traversal is executed; routing masks are frozen from the scientific gate-compression experiment',
          'checksums':checksums}
    (a.out_dir / f'gate_meta_replica_{a.replica}.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta,indent=2)); print(pd.DataFrame(summary).to_string(index=False))

if __name__=='__main__': main()
