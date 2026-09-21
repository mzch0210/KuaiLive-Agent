from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

from dual_id_room_baseline import aligned_vectors, evaluate_vectors
from room_level_selective_agent import (
    CONF_FEATURES,
    USER_FEATURES,
    SEED,
    bootstrap_delta,
    choose_threshold,
    hgb,
    load_data,
    popularity_by_streamer,
    score_memory,
    user_features,
)

FEATURES = USER_FEATURES + CONF_FEATURES


class TinyGate(torch.nn.Module):
    def __init__(self, d: int, hidden: int = 16):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(d, hidden),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


def fit_tiny_mlp(X: np.ndarray, y: np.ndarray, seed: int, hidden: int = 16,
                 epochs: int = 200, lr: float = 1e-2, weight_decay: float = 1e-4):
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X).astype(np.float32)
    ys = np.asarray(y, dtype=np.float32)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    model = TinyGate(X.shape[1], hidden=hidden)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    loss_fn = torch.nn.MSELoss()
    xt = torch.from_numpy(Xs)
    yt = torch.from_numpy(ys)
    model.train()
    for _ in range(epochs):
        opt.zero_grad(set_to_none=True)
        pred = model(xt)
        loss = loss_fn(pred, yt)
        loss.backward()
        opt.step()
    model.eval()
    return scaler, model


def predict_tiny(scaler, model, X: np.ndarray) -> np.ndarray:
    Xs = scaler.transform(X).astype(np.float32)
    with torch.inference_mode():
        return model(torch.from_numpy(Xs)).cpu().numpy().astype(float)


def oof_hgb(X, y, cv):
    out = np.empty(len(y), dtype=float)
    for tr, va in cv.split(X):
        m = hgb().fit(X[tr], y[tr])
        out[va] = m.predict(X[va])
    return out


def oof_ridge(X, y, cv):
    out = np.empty(len(y), dtype=float)
    for tr, va in cv.split(X):
        sc = StandardScaler().fit(X[tr])
        m = Ridge(alpha=1.0).fit(sc.transform(X[tr]), y[tr])
        out[va] = m.predict(sc.transform(X[va]))
    return out


def oof_mlp(X, y, cv):
    out = np.empty(len(y), dtype=float)
    for fold, (tr, va) in enumerate(cv.split(X)):
        sc, m = fit_tiny_mlp(X[tr], y[tr], seed=SEED + 1000 + fold)
        out[va] = predict_tiny(sc, m, X[va])
    return out


def eval_gate(name, oof_pred, test_pred, base_d, mem_d, base_t, mem_t):
    threshold, dev_use, dev_ndcg = choose_threshold(oof_pred, base_d, mem_d)
    test_use = test_pred > threshold
    selected = np.where(test_use, mem_t, base_t)
    delta, lo, hi = bootstrap_delta(selected - base_t, SEED + 700 + len(name), n_boot=5000)
    return {
        'name': name,
        'threshold': float(threshold),
        'dev_oof_ndcg10': float(dev_ndcg),
        'dev_invocation_rate': float(dev_use.mean()),
        'test_ndcg10': float(selected.mean()),
        'test_delta_vs_dual': float(delta),
        'ci95_low': float(lo),
        'ci95_high': float(hi),
        'test_invocation_rate': float(test_use.mean()),
        'selected_n': int(test_use.sum()),
        'test_use': test_use,
        'selected': selected,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--room-data-dir', type=Path, required=True)
    ap.add_argument('--streamer-data-dir', type=Path, required=True)
    ap.add_argument('--room-dev', type=Path, required=True)
    ap.add_argument('--streamer-dev', type=Path, required=True)
    ap.add_argument('--reference-report', type=Path, required=True)
    ap.add_argument('--reference-test', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--n-neg', type=int, default=574)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    train, dev, _test, item_to_streamer = load_data(args.room_data_dir, args.n_neg)
    streamer_map = pd.read_csv(args.streamer_data_dir / 'streamer_item_map.tsv', sep='\t')
    streamer_to_item = dict(zip(streamer_map.streamer_id.astype(int), streamer_map.item_id.astype(int)))

    dv = aligned_vectors(dev, args.room_dev, args.streamer_dev, item_to_streamer, streamer_to_item, args.n_neg)

    grid = np.linspace(0.0, 1.0, 41)
    best = None
    for alpha in grid:
        z = evaluate_vectors(dv, float(alpha), False)
        score = float(z.dual_score10.mean())
        key = (score, float(alpha))
        if best is None or key > best[0]:
            best = (key, float(alpha))
    alpha = best[1]
    base_dev = evaluate_vectors(dv, alpha, True)

    pop = popularity_by_streamer(train, item_to_streamer)
    mem_dev = score_memory(dev, train, pop, args.n_neg, item_to_streamer)
    feat_dev = user_features(train, item_to_streamer)
    d = base_dev.merge(mem_dev, on='user_id').merge(feat_dev, on='user_id')
    d['MemoryFusion_delta'] = d.MemoryFusion_score10 - d.dual_score10

    # Test is reused verbatim from the locked identity-control artifact.
    t = pd.read_csv(args.reference_test).sort_values('user_id').reset_index(drop=True)
    needed = set(['user_id', 'dual_score10', 'MemoryFusion_score10'] + FEATURES)
    missing = sorted(needed - set(t.columns))
    if missing:
        raise ValueError(f'reference test missing columns: {missing}')

    Xd = d[FEATURES].to_numpy(float)
    Xt = t[FEATURES].to_numpy(float)
    yd = d.MemoryFusion_delta.to_numpy(float)
    base_d = d.dual_score10.to_numpy(float)
    mem_d = d.MemoryFusion_score10.to_numpy(float)
    base_t = t.dual_score10.to_numpy(float)
    mem_t = t.MemoryFusion_score10.to_numpy(float)

    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)

    hgb_oof = oof_hgb(Xd, yd, cv)
    hgb_full = clone(hgb()).fit(Xd, yd)
    hgb_test_pred = hgb_full.predict(Xt)
    gh = eval_gate('hgb', hgb_oof, hgb_test_pred, base_d, mem_d, base_t, mem_t)

    ridge_oof = oof_ridge(Xd, yd, cv)
    ridge_scaler = StandardScaler().fit(Xd)
    ridge_full = Ridge(alpha=1.0).fit(ridge_scaler.transform(Xd), yd)
    ridge_test_pred = ridge_full.predict(ridge_scaler.transform(Xt))
    gr = eval_gate('ridge', ridge_oof, ridge_test_pred, base_d, mem_d, base_t, mem_t)

    mlp_oof = oof_mlp(Xd, yd, cv)
    mlp_scaler, mlp_full = fit_tiny_mlp(Xd, yd, seed=SEED + 2000)
    mlp_test_pred = predict_tiny(mlp_scaler, mlp_full, Xt)
    gm = eval_gate('tiny_mlp', mlp_oof, mlp_test_pred, base_d, mem_d, base_t, mem_t)

    ref = json.loads(args.reference_report.read_text())
    reproduction = {
        'alpha_room_expected': float(ref['alpha_room']),
        'alpha_room_observed': float(alpha),
        'hgb_test_ndcg_expected': float(ref['selective_dual_memory_test_ndcg10']),
        'hgb_test_ndcg_observed': float(gh['test_ndcg10']),
        'hgb_rate_expected': float(ref['test_gate_rate']),
        'hgb_rate_observed': float(gh['test_invocation_rate']),
    }
    tol = 1e-10
    reproduction_pass = (
        abs(reproduction['alpha_room_expected'] - reproduction['alpha_room_observed']) <= tol
        and abs(reproduction['hgb_test_ndcg_expected'] - reproduction['hgb_test_ndcg_observed']) <= tol
        and abs(reproduction['hgb_rate_expected'] - reproduction['hgb_rate_observed']) <= tol
    )
    if not reproduction_pass:
        raise SystemExit('HGB reproduction gate failed: ' + json.dumps(reproduction, indent=2))

    joblib.dump(hgb_full, args.out_dir / 'hgb_gate.joblib')
    np.savez(
        args.out_dir / 'light_gate_params.npz',
        feature_names=np.asarray(FEATURES, dtype='U64'),
        ridge_mean=ridge_scaler.mean_.astype(np.float64),
        ridge_scale=ridge_scaler.scale_.astype(np.float64),
        ridge_coef=ridge_full.coef_.astype(np.float64),
        ridge_intercept=np.asarray([ridge_full.intercept_], dtype=np.float64),
        mlp_mean=mlp_scaler.mean_.astype(np.float64),
        mlp_scale=mlp_scaler.scale_.astype(np.float64),
        mlp_w1=mlp_full.net[0].weight.detach().cpu().numpy().astype(np.float64),
        mlp_b1=mlp_full.net[0].bias.detach().cpu().numpy().astype(np.float64),
        mlp_w2=mlp_full.net[2].weight.detach().cpu().numpy().astype(np.float64),
        mlp_b2=mlp_full.net[2].bias.detach().cpu().numpy().astype(np.float64),
    )

    gates = {}
    for g in (gh, gr, gm):
        gates[g['name']] = {k: v for k, v in g.items() if k not in ('test_use', 'selected')}

    report = {
        'experiment': 'dual_id_gate_compression',
        'hypothesis': 'Current Selective Memory latency disadvantage is primarily selector overhead rather than intrinsic memory-specialist cost.',
        'protocol': 'Same frozen Dual-ID base, MemoryFusion expert, 575 candidates, 5-fold OOF dev threshold, one-shot frozen test.',
        'users': int(len(t)),
        'candidate_count': int(args.n_neg + 1),
        'alpha_room': float(alpha),
        'alpha_streamer': float(1.0 - alpha),
        'dual_id_test_ndcg10': float(base_t.mean()),
        'memory_test_ndcg10': float(mem_t.mean()),
        'features': FEATURES,
        'ridge': {'alpha': 1.0, 'parameter_count': int(len(FEATURES) + 1)},
        'tiny_mlp': {
            'architecture': f'{len(FEATURES)}-16-1',
            'activation': 'ReLU',
            'epochs': 200,
            'optimizer': 'AdamW',
            'lr': 1e-2,
            'weight_decay': 1e-4,
            'parameter_count': int(len(FEATURES) * 16 + 16 + 16 + 1),
        },
        'reproduction': reproduction,
        'reproduction_pass': bool(reproduction_pass),
        'gates': gates,
    }
    (args.out_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')

    out = t.copy()
    out['hgb_pred_delta'] = hgb_test_pred
    out['hgb_use_memory'] = gh['test_use']
    out['hgb_selective_score10'] = gh['selected']
    out['ridge_pred_delta'] = ridge_test_pred
    out['ridge_use_memory'] = gr['test_use']
    out['ridge_selective_score10'] = gr['selected']
    out['tiny_mlp_pred_delta'] = mlp_test_pred
    out['tiny_mlp_use_memory'] = gm['test_use']
    out['tiny_mlp_selective_score10'] = gm['selected']
    out.to_csv(args.out_dir / 'per_user_test.csv.gz', index=False, compression='gzip')

    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
