from __future__ import annotations

import argparse
import ast
import json
import math
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import torch

from dsframe_matched_budget import BUDGETS, EPS, SEED, bootstrap, fit_selector, predict_selector


def parse_list(value, dtype=float):
    s = str(value).strip()
    s = re.sub(r"np\.(?:float(?:16|32|64)|int(?:8|16|32|64)|uint(?:8|16|32|64))\(([^()]*)\)", r"\1", s)
    if s.startswith('[') and s.endswith(']') and dtype in (float, int):
        arr = np.fromstring(s[1:-1], sep=',', dtype=np.float64 if dtype is float else np.int64)
        return arr.astype(dtype, copy=False)
    return np.asarray(ast.literal_eval(s), dtype=dtype)


def zscore_rows(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, np.float32)
    mu = x.mean(axis=1, keepdims=True)
    sd = x.std(axis=1, keepdims=True)
    sd[sd <= EPS] = 1.0
    return (x - mu) / sd


def ndcg10(scores: np.ndarray) -> np.ndarray:
    scores = np.asarray(scores, float)
    tgt = scores[:, :1]
    # Match the frozen Dual-ID evaluator: tied candidates are conservatively counted with the target.
    rank = (scores >= (tgt - 1e-12)).sum(axis=1)
    out = np.zeros(len(scores), float)
    m = rank <= 10
    out[m] = 1.0 / np.log2(rank[m] + 1.0)
    return out


def topk_mask(scores: np.ndarray, k: int) -> np.ndarray:
    idx = np.argsort(-np.asarray(scores, float), kind='mergesort')[:k]
    out = np.zeros(len(scores), bool)
    out[idx] = True
    return out


def load_room_candidate_scores(phase_path: Path, rec_path: Path, room_to_ds_streamer: np.ndarray, n_neg: int):
    phase = pd.read_csv(phase_path, sep='\t').sort_values('user_id').reset_index(drop=True)
    pred = pd.read_csv(rec_path, sep='\t', usecols=['user_id', 'rec_items', 'rec_predictions']).sort_values('user_id').reset_index(drop=True)
    if not np.array_equal(phase.user_id.to_numpy(), pred.user_id.to_numpy()):
        raise ValueError('room phase/prediction user alignment mismatch')

    n = len(phase); k = n_neg + 1
    room_scores = np.empty((n, k), np.float32)
    streamer_idx = np.empty((n, k), np.int64)
    users = phase.user_id.to_numpy(np.int64)

    for j, (r, p) in enumerate(zip(phase.itertuples(index=False), pred.itertuples(index=False))):
        neg = parse_list(r.neg_items, int)
        if len(neg) != n_neg:
            raise ValueError(f'candidate count mismatch user={r.user_id}: {len(neg)}')
        rooms = np.concatenate(([int(r.item_id)], neg)).astype(np.int64)
        if rooms.max() >= len(room_to_ds_streamer):
            raise ValueError(f'room item id outside map user={r.user_id}')
        si = room_to_ds_streamer[rooms]
        if (si < 0).any():
            raise ValueError(f'unmapped room->streamer user={r.user_id}')
        streamer_idx[j] = si

        items = parse_list(p.rec_items, int)
        vals = parse_list(p.rec_predictions, float)
        if len(items) != len(vals):
            raise ValueError(f'frozen room prediction length mismatch user={r.user_id}')
        smap = {int(i): float(v) for i, v in zip(items, vals)}
        try:
            room_scores[j] = [smap[int(i)] for i in rooms]
        except KeyError as exc:
            raise KeyError(f'frozen room prediction missing candidate user={r.user_id}, item={exc}')

    return users, zscore_rows(room_scores), streamer_idx


def model_hidden(ds_source: Path, ds_root: Path, dataset: str, model_path: Path, batch_size: int):
    sys.path.insert(0, str(ds_source.resolve()))
    from helpers.BaseReader import BaseReader
    from models.PRL import PRL
    from utils.constants import ITEM_ID, ITEM_SEQ, ITEM_SEQ_LEN

    args = SimpleNamespace(
        sep=',', path=str(ds_root.resolve()), dataset=dataset, device=torch.device('cpu'),
        model_path=str(model_path.resolve()), buffer=0, dropout=.2, test_all=1, emb_size=64,
        num_layers=1, num_heads=4, inner_size=128, hidden_act='gelu', layer_norm_eps=1e-12,
        initializer_range=.02, temperature=.07, reason_step=2, pl_weight=1.0, temp_scale=5.0,
        noise_factor=.01, cl_weight=1.0, warmup=2,
    )
    corpus = BaseReader(args)
    model = PRL(args, corpus).to(args.device)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()

    outputs = {}
    with torch.no_grad():
        for phase, key in [('dev', 'valid'), ('test', 'test')]:
            data = corpus.data_dict[key]
            fast, mean, final = [], [], []
            for st in range(0, len(data[ITEM_ID]), batch_size):
                en = min(len(data[ITEM_ID]), st + batch_size)
                feed = {
                    ITEM_SEQ: data[ITEM_SEQ][st:en],
                    ITEM_SEQ_LEN: data[ITEM_SEQ_LEN][st:en],
                    ITEM_ID: data[ITEM_ID][st:en],
                }
                mo = model(feed, stage='infer')['model_output']
                fast.append(mo[:, 0, :].cpu().numpy())
                mean.append(mo.mean(1).cpu().numpy())
                final.append(mo[:, -1, :].cpu().numpy())
            outputs[phase] = {
                'fast': np.concatenate(fast).astype(np.float32),
                'mean': np.concatenate(mean).astype(np.float32),
                'final': np.concatenate(final).astype(np.float32),
            }
    return model, outputs


def candidate_scores(hidden: np.ndarray, streamer_idx: np.ndarray, item_weight: torch.Tensor, temperature: float, batch_size: int):
    result = []
    with torch.no_grad():
        for st in range(0, len(hidden), batch_size):
            en = min(len(hidden), st + batch_size)
            h = torch.from_numpy(hidden[st:en])
            idx = torch.from_numpy(streamer_idx[st:en])
            emb = item_weight[idx]
            score = torch.einsum('bd,bkd->bk', h, emb) / temperature
            result.append(score.cpu().numpy())
    return np.concatenate(result).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ds-source', type=Path, required=True)
    ap.add_argument('--ds-root', type=Path, required=True)
    ap.add_argument('--ds-dataset', required=True)
    ap.add_argument('--ds-model', type=Path, required=True)
    ap.add_argument('--ds-candidates', type=Path, required=True)
    ap.add_argument('--ds-scores', type=Path, required=True)
    ap.add_argument('--room-data-dir', type=Path, required=True)
    ap.add_argument('--room-dev-rec', type=Path, required=True)
    ap.add_argument('--room-test-rec', type=Path, required=True)
    ap.add_argument('--dual-test', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--n-neg', type=int, default=574)
    ap.add_argument('--alpha-room', type=float, default=.1)
    ap.add_argument('--batch-size', type=int, default=128)
    args = ap.parse_args(); args.out_dir.mkdir(parents=True, exist_ok=True)

    cand = np.load(args.ds_candidates, allow_pickle=False)
    item_inverse = cand['item_inverse'].astype(np.int64)
    ds_user_ids = cand['user_ids'].astype(np.int64)
    streamer_to_ds = {int(s): i for i, s in enumerate(item_inverse)}

    room_map = pd.read_csv(args.room_data_dir / 'room_item_map.tsv', sep='\t')
    max_room = int(room_map.item_id.max())
    room_to_ds_streamer = np.full(max_room + 1, -1, np.int64)
    missing = []
    for r in room_map.itertuples(index=False):
        idx = streamer_to_ds.get(int(r.streamer_id))
        if idx is None:
            missing.append(int(r.streamer_id))
        else:
            room_to_ds_streamer[int(r.item_id)] = idx
    if missing:
        raise ValueError(f'{len(set(missing))} room streamers absent from frozen DS streamer universe')

    dev_users, room_dev_z, dev_streamer_idx = load_room_candidate_scores(
        args.room_data_dir / 'dev.csv', args.room_dev_rec, room_to_ds_streamer, args.n_neg)
    test_users, room_test_z, test_streamer_idx = load_room_candidate_scores(
        args.room_data_dir / 'test.csv', args.room_test_rec, room_to_ds_streamer, args.n_neg)
    if not np.array_equal(dev_users, test_users):
        raise ValueError('room dev/test user ordering mismatch')
    if not np.array_equal(dev_users, ds_user_ids):
        raise ValueError(f'DS/room user alignment mismatch: ds[:5]={ds_user_ids[:5]}, room[:5]={dev_users[:5]}')

    model, hidden = model_hidden(args.ds_source, args.ds_root, args.ds_dataset, args.ds_model, args.batch_size)
    W = model.item_emb.weight.detach().cpu()
    if len(item_inverse) > W.shape[0]:
        raise ValueError('item inverse larger than PRL embedding table')

    projected = {}
    alpha = float(args.alpha_room)
    for phase, room_z, sidx in [('dev', room_dev_z, dev_streamer_idx), ('test', room_test_z, test_streamer_idx)]:
        projected[phase] = {}
        for variant in ['fast', 'mean', 'final']:
            raw = candidate_scores(hidden[phase][variant], sidx, W, model.temperature, args.batch_size)
            stream_z = zscore_rows(raw)
            fused = alpha * room_z + (1.0 - alpha) * stream_z
            projected[phase][variant] = ndcg10(fused)

    slow_dev_means = {v: float(projected['dev'][v].mean()) for v in ['mean', 'final']}
    slow_variant = max(slow_dev_means, key=slow_dev_means.get)
    ds_fast = projected['test']['fast']
    ds_slow = projected['test'][slow_variant]

    score_npz = np.load(args.ds_scores, allow_pickle=False)
    if not np.array_equal(score_npz['user_id'].astype(np.int64), test_users):
        raise ValueError('frozen DS selector feature/user alignment mismatch')
    xds_dev = score_npz['dev_fast_hidden'].astype(np.float32)
    xds_test = score_npz['test_fast_hidden'].astype(np.float32)
    oracle_label = (
        score_npz[f'dev_slow_{slow_variant}_ce'].astype(float)
        < score_npz['dev_fast_ce'].astype(float)
    ).astype(np.float32)

    ours = pd.read_csv(args.dual_test).sort_values('user_id').reset_index(drop=True)
    if not np.array_equal(ours.user_id.to_numpy(np.int64), test_users):
        raise ValueError('Dual-ID frozen per-user table does not align with room users')
    ours_base = ours.dual_score10.to_numpy(float)
    ours_mem = ours.MemoryFusion_score10.to_numpy(float)
    ours_gate = ours.primary_pred_delta.to_numpy(float)

    rows = []
    n = len(test_users)
    for j, budget in enumerate(BUDGETS):
        k = max(1, int(round(float(budget) * n)))
        rate = k / n

        selector, mu, sd, _ = fit_selector(xds_dev, oracle_label, float(budget), SEED + j)
        ptest = predict_selector(selector, mu, sd, xds_test)
        use_ds = topk_mask(ptest, k)
        ds_sel = np.where(use_ds, ds_slow, ds_fast)

        use_ours = topk_mask(ours_gate, k)
        ours_sel = np.where(use_ours, ours_mem, ours_base)

        rng = np.random.default_rng(SEED + 100 + j)
        rand = []
        for _ in range(500):
            m = np.zeros(n, bool); m[rng.choice(n, k, replace=False)] = True
            rand.append(float(np.where(m, ds_slow, ds_fast).mean()))
        utility = ds_slow - ds_fast
        oracle_mask = topk_mask(utility, k)
        ds_oracle = float(np.where(oracle_mask, ds_slow, ds_fast).mean())

        d_ds, lo_ds, hi_ds = bootstrap(ds_sel - ds_fast, n=5000, seed=SEED + 10 + j)
        d_ours, lo_ours, hi_ours = bootstrap(ours_sel - ours_base, n=5000, seed=SEED + 20 + j)
        d_cross, lo_cross, hi_cross = bootstrap(ours_sel - ds_sel, n=5000, seed=SEED + 30 + j)

        rows.append({
            'target_budget': float(budget), 'k': k, 'exact_rate': rate,
            'ds_room_fast_ndcg10': float(ds_fast.mean()),
            'ds_room_allslow_ndcg10': float(ds_slow.mean()),
            'ds_room_selective_ndcg10': float(ds_sel.mean()),
            'ds_delta_vs_fast': d_ds, 'ds_delta_ci_low': lo_ds, 'ds_delta_ci_high': hi_ds,
            'ds_random_ndcg10_mean': float(np.mean(rand)), 'ds_oracle_ndcg10': ds_oracle,
            'dual_id_base_ndcg10': float(ours_base.mean()), 'memory_ndcg10': float(ours_mem.mean()),
            'ours_selective_ndcg10': float(ours_sel.mean()),
            'ours_delta_vs_dual': d_ours, 'ours_delta_ci_low': lo_ours, 'ours_delta_ci_high': hi_ours,
            'ours_minus_ds_selective': d_cross, 'cross_ci_low': lo_cross, 'cross_ci_high': hi_cross,
            'ds_gain_per_invocation': d_ds / rate, 'ours_gain_per_invocation': d_ours / rate,
            'ds_selected_positive_fraction': float((utility[use_ds] > 0).mean()),
            'ours_selected_positive_fraction': float(((ours_mem - ours_base)[use_ours] > 0).mean()),
        })

    pd.DataFrame(rows).to_csv(args.out_dir / 'room_projected_exact_budget.csv', index=False)
    np.savez_compressed(
        args.out_dir / 'room_projected_per_user.npz', user_id=test_users,
        ds_fast_ndcg10=ds_fast.astype(np.float32), ds_slow_ndcg10=ds_slow.astype(np.float32),
        ours_base_ndcg10=ours_base.astype(np.float32), ours_memory_ndcg10=ours_mem.astype(np.float32),
        ours_gate_score=ours_gate.astype(np.float32),
    )
    report = {
        'task': 'next_live_room',
        'candidate_protocol': f'{args.n_neg} legal active-at-time negatives + positive; seed 20260918; identical frozen room candidates',
        'n_users': n,
        'projection': 'alpha*z(frozen RoomSASRec)+(1-alpha)*z(official PRL streamer path), evaluated on each live-room candidate via room->streamer identity',
        'alpha_room': alpha, 'alpha_streamer_reasoning': 1.0 - alpha,
        'alpha_source': 'frozen Dual-ID representation weight; not retuned for DS-Frame',
        'dsframe_model': 'official pinned PRL from streamer-level collision experiment; no retraining or loss modification',
        'selector': 'paper-faithful MLP on frozen PRL fast hidden; dev full-item CE oracle; exact test K imposed by gate score only',
        'slow_variant_selected_on_room_dev': slow_variant,
        'room_dev_allslow_ndcg10_variants': slow_dev_means,
        'ds_room_fast_test_ndcg10': float(ds_fast.mean()),
        'ds_room_allslow_test_ndcg10': float(ds_slow.mean()),
        'dual_id_frozen_test_ndcg10': float(ours_base.mean()),
        'memory_frozen_test_ndcg10': float(ours_mem.mean()),
        'native_room_prl_guardrail': 'A native PRL over 1,179,779 room IDs would require official full-softmax/progressive losses over the entire room universe. We do not replace those losses with sampled-softmax because that would change DS-Frame; instead we project the unchanged official streamer PRL path through the frozen Dual-ID room representation.',
        'comparison_guardrail': 'Absolute DS-vs-ours NDCG mixes different fast bases; matched-budget marginal gains versus each method own fast/base are the collision-defense quantity.',
        'results': rows,
    }
    (args.out_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
