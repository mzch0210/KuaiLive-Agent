from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_val_predict

from room_level_selective_agent import (
    CONF_FEATURES, USER_FEATURES, EPS, SEED, bootstrap_delta, choose_threshold,
    hgb, load_data, ndcg10, parse_list, popularity_by_streamer, score_memory,
    user_features,
)


def load_rec_score_maps(path: Path) -> dict[int, dict[int, float]]:
    df = pd.read_csv(path, sep='\t')
    out = {}
    for r in df.itertuples(index=False):
        items = parse_list(r.rec_items, int)
        scores = parse_list(r.rec_predictions, float)
        if len(items) != len(scores):
            raise ValueError('prediction item/score length mismatch')
        d: dict[int, list[float]] = {}
        for i, s in zip(items, scores):
            d.setdefault(int(i), []).append(float(s))
        out[int(r.user_id)] = {i: float(np.mean(v)) for i, v in d.items()}
    return out


def zscore(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, float)
    sd = float(x.std())
    if sd <= EPS:
        return np.zeros_like(x)
    return (x - float(x.mean())) / sd


def rank_ge(scores: np.ndarray) -> int:
    ts = float(scores[0])
    return int(np.sum(scores >= ts - 1e-12))


def conf_tuple(scores: np.ndarray):
    scores = np.asarray(scores, float)
    ss = np.sort(scores)[::-1]
    mean = float(scores.mean()); std = float(scores.std()); rng = float(scores.max() - scores.min())
    ex = np.exp(np.clip(scores - scores.max(), -60, 0)); prob = ex / ex.sum(); ps = np.sort(prob)[::-1]
    ent = float(-(prob * np.log(np.maximum(prob, EPS))).sum() / math.log(len(prob)))
    # candidate count is >= 21 in all intended protocols
    return (std, rng, float(ss[0]-ss[1]), float(ss[0]-ss[4]),
            float(ss[9]-ss[10]), float((ss[0]-mean)/max(std, EPS)), ent, float(ps[:10].sum()))


def aligned_vectors(phase: pd.DataFrame, room_rec: Path, streamer_rec: Path,
                    item_to_streamer: dict[int, int], streamer_to_item: dict[int, int], n_neg: int):
    rmap = load_rec_score_maps(room_rec)
    smap = load_rec_score_maps(streamer_rec)
    rows = []
    for r in phase.itertuples(index=False):
        uid = int(r.user_id)
        neg = parse_list(r.neg_items, int)
        if len(neg) != n_neg:
            raise ValueError('candidate count mismatch')
        rooms = np.concatenate(([int(r.item_id)], neg))
        try:
            room_scores = np.asarray([rmap[uid][int(i)] for i in rooms], float)
        except KeyError as e:
            raise KeyError(f'missing room prediction for user={uid}, item={e}')
        streamer_items = np.asarray([streamer_to_item[item_to_streamer[int(i)]] for i in rooms], int)
        try:
            streamer_scores = np.asarray([smap[uid][int(i)] for i in streamer_items], float)
        except KeyError as e:
            raise KeyError(f'missing streamer prediction for user={uid}, item={e}')
        rows.append((uid, zscore(room_scores), zscore(streamer_scores)))
    return rows


def evaluate_vectors(vectors, alpha: float, with_conf: bool):
    rows = []
    for uid, rz, sz in vectors:
        dual = alpha * rz + (1.0 - alpha) * sz
        rr = rank_ge(rz); sr = rank_ge(sz); dr = rank_ge(dual)
        row = {'user_id': uid, 'room_rank': rr, 'streamer_rank': sr, 'dual_rank': dr,
               'room_score10': float(ndcg10([rr])[0]),
               'streamer_score10': float(ndcg10([sr])[0]),
               'dual_score10': float(ndcg10([dr])[0])}
        if with_conf:
            row.update(dict(zip(CONF_FEATURES, conf_tuple(dual))))
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--room-data-dir', type=Path, required=True)
    ap.add_argument('--streamer-data-dir', type=Path, required=True)
    ap.add_argument('--room-dev', type=Path, required=True)
    ap.add_argument('--room-test', type=Path, required=True)
    ap.add_argument('--streamer-dev', type=Path, required=True)
    ap.add_argument('--streamer-test', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--n-neg', type=int, default=574)
    args = ap.parse_args(); args.out_dir.mkdir(parents=True, exist_ok=True)

    train, dev, test, item_to_streamer = load_data(args.room_data_dir, args.n_neg)
    streamer_map = pd.read_csv(args.streamer_data_dir / 'streamer_item_map.tsv', sep='\t')
    streamer_to_item = dict(zip(streamer_map.streamer_id.astype(int), streamer_map.item_id.astype(int)))

    dv = aligned_vectors(dev, args.room_dev, args.streamer_dev, item_to_streamer, streamer_to_item, args.n_neg)
    tv = aligned_vectors(test, args.room_test, args.streamer_test, item_to_streamer, streamer_to_item, args.n_neg)

    grid = np.linspace(0.0, 1.0, 41)
    tuning = []
    best = None
    for alpha in grid:
        z = evaluate_vectors(dv, float(alpha), False)
        score = float(z.dual_score10.mean())
        tuning.append({'alpha_room': float(alpha), 'alpha_streamer': float(1-alpha), 'dev_ndcg10': score})
        key = (score, float(alpha))  # ties prefer more room-ID weight (conservative identity control)
        if best is None or key > best[0]:
            best = (key, float(alpha))
    alpha = best[1]
    pd.DataFrame(tuning).to_csv(args.out_dir / 'alpha_tuning.csv', index=False)

    base_dev = evaluate_vectors(dv, alpha, True)
    base_test = evaluate_vectors(tv, alpha, True)

    pop = popularity_by_streamer(train, item_to_streamer)
    train_dev = pd.concat([train, dev[['user_id','item_id','time']]], ignore_index=True)
    mem_dev = score_memory(dev, train, pop, args.n_neg, item_to_streamer)
    mem_test = score_memory(test, train_dev, pop, args.n_neg, item_to_streamer)
    feat_dev = user_features(train, item_to_streamer)
    feat_test = user_features(train_dev, item_to_streamer)

    d = base_dev.merge(mem_dev, on='user_id').merge(feat_dev, on='user_id')
    t = base_test.merge(mem_test, on='user_id').merge(feat_test, on='user_id')
    d['MemoryFusion_delta'] = d.MemoryFusion_score10 - d.dual_score10
    t['MemoryFusion_delta'] = t.MemoryFusion_score10 - t.dual_score10

    feats = USER_FEATURES + CONF_FEATURES
    Xd = d[feats].to_numpy(float); Xt = t[feats].to_numpy(float)
    yd = d.MemoryFusion_delta.to_numpy(float)
    base_d = d.dual_score10.to_numpy(float); mem_d = d.MemoryFusion_score10.to_numpy(float)
    base_t = t.dual_score10.to_numpy(float); mem_t = t.MemoryFusion_score10.to_numpy(float)

    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    oof = cross_val_predict(hgb(), Xd, yd, cv=cv, method='predict')
    th, use_d, dev_sel = choose_threshold(oof, base_d, mem_d)
    model = clone(hgb()).fit(Xd, yd)
    ptest = model.predict(Xt); use_t = ptest > th
    selected = np.where(use_t, mem_t, base_t)

    sel_delta, sel_lo, sel_hi = bootstrap_delta(selected - base_t, SEED + 301)
    mem_delta, mem_lo, mem_hi = bootstrap_delta(mem_t - base_t, SEED + 302)
    dual_room_delta, dual_room_lo, dual_room_hi = bootstrap_delta(
        t.dual_score10.to_numpy(float) - t.room_score10.to_numpy(float), SEED + 303)

    report = {
        'experiment': 'dual_id_streamer_identity_control',
        'task': 'next_live_room',
        'users': int(len(t)),
        'candidate_count': int(args.n_neg + 1),
        'fusion': 'alpha*z(RoomSASRec)+(1-alpha)*z(StreamerSASRec), alpha chosen on dev only',
        'alpha_room': alpha,
        'alpha_streamer': 1.0-alpha,
        'room_sasrec_dev_ndcg10': float(d.room_score10.mean()),
        'streamer_sasrec_dev_ndcg10': float(d.streamer_score10.mean()),
        'dual_id_dev_ndcg10': float(base_d.mean()),
        'memory_dev_ndcg10': float(mem_d.mean()),
        'selective_dev_oof_ndcg10': float(dev_sel),
        'room_sasrec_test_ndcg10': float(t.room_score10.mean()),
        'streamer_sasrec_test_ndcg10': float(t.streamer_score10.mean()),
        'dual_id_test_ndcg10': float(base_t.mean()),
        'memory_test_ndcg10': float(mem_t.mean()),
        'selective_dual_memory_test_ndcg10': float(selected.mean()),
        'dual_minus_room_delta': dual_room_delta,
        'dual_minus_room_ci95': [dual_room_lo, dual_room_hi],
        'memory_minus_dual_delta': mem_delta,
        'memory_minus_dual_ci95': [mem_lo, mem_hi],
        'selective_minus_dual_delta': sel_delta,
        'selective_minus_dual_ci95': [sel_lo, sel_hi],
        'dev_gate_rate': float(use_d.mean()),
        'test_gate_rate': float(use_t.mean()),
        'selected_n': int(use_t.sum()),
        'identity_control_pass': bool(sel_delta > 0 and sel_lo > 0),
        'identity_control_rule': 'PASS iff dev-learned Selective(Memory vs DualID) improves DualID on test and paired-bootstrap 95% CI lower bound > 0.',
        'interpretation_guardrail': 'If DualID absorbs most MemoryFusion gain and Selective no longer improves it, the earlier room result is primarily persistent-identity representation rather than selective memory invocation.',
    }
    (args.out_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    t.assign(primary_pred_delta=ptest, primary_use_memory=use_t,
             selective_score10=selected).to_csv(args.out_dir / 'per_user_test.csv.gz', index=False, compression='gzip')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
