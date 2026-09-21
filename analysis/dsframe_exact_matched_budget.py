from __future__ import annotations

import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingRegressor

from analysis.dsframe_matched_budget import (
    BUDGETS, CONF_FEATURES, EPS, SEED, USER_FEATURES,
    bootstrap, confidence, fit_selector, predict_selector,
)


def findone(root: Path, name: str) -> Path:
    matches = list(root.rglob(name))
    if len(matches) != 1:
        raise ValueError((name, [str(x) for x in matches]))
    return matches[0]


def topk_mask(scores, k: int):
    idx = np.argsort(-np.asarray(scores, float), kind='mergesort')[:k]
    mask = np.zeros(len(scores), bool)
    mask[idx] = True
    return mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recovered-dir', type=Path, required=True)
    ap.add_argument('--sasrec-dev', type=Path, required=True)
    ap.add_argument('--sasrec-test', type=Path, required=True)
    ap.add_argument('--ds-scores', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    dev = pd.read_csv(findone(args.recovered_dir, 'per_user_dev.csv.gz'))
    test = pd.read_csv(findone(args.recovered_dir, 'per_user_test.csv.gz'))
    dev = dev.merge(confidence(args.sasrec_dev), on='user_id', validate='one_to_one')
    test = test.merge(confidence(args.sasrec_test), on='user_id', validate='one_to_one')
    dev = dev.sort_values('user_id').reset_index(drop=True)
    test = test.sort_values('user_id').reset_index(drop=True)

    ds = np.load(args.ds_scores)
    assert len(ds['user_id']) == len(dev) == len(test)
    assert np.array_equal(dev.user_id.to_numpy(), np.arange(1, len(dev) + 1))
    assert np.array_equal(test.user_id.to_numpy(), np.arange(1, len(test) + 1))

    means = {
        'mean': float(ds['dev_slow_mean_ndcg10'].mean()),
        'final': float(ds['dev_slow_final_ndcg10'].mean()),
    }
    slow_variant = max(means, key=means.get)
    ds_test_fast = ds['test_fast_ndcg10'].astype(float)
    ds_test_slow = ds[f'test_slow_{slow_variant}_ndcg10'].astype(float)
    oracle_label = (
        ds[f'dev_slow_{slow_variant}_ce'].astype(float)
        < ds['dev_fast_ce'].astype(float)
    ).astype(np.float32)
    xds_dev = ds['dev_fast_hidden'].astype(np.float32)
    xds_test = ds['test_fast_hidden'].astype(np.float32)

    feats = USER_FEATURES + CONF_FEATURES
    xd = dev[feats].to_numpy(float)
    xt = test[feats].to_numpy(float)
    yd = dev.MemoryFusion_delta.to_numpy(float)
    hgb = HistGradientBoostingRegressor(
        max_iter=200, learning_rate=.05, max_depth=3, min_samples_leaf=50,
        l2_regularization=1.0, random_state=SEED,
    )
    ptest = clone(hgb).fit(xd, yd).predict(xt)
    sas_test = test.sasrec_score10.to_numpy(float)
    mem_test = test.MemoryFusion_score10.to_numpy(float)

    rows = []
    n = len(test)
    for j, budget in enumerate(BUDGETS):
        k = max(1, int(round(budget * n)))
        rate = k / n

        use_ours = topk_mask(ptest, k)
        ours = np.where(use_ours, mem_test, sas_test)

        selector, mu, sd, _ = fit_selector(xds_dev, oracle_label, budget, SEED + j)
        pte = predict_selector(selector, mu, sd, xds_test)
        use_ds = topk_mask(pte, k)
        ds_sel = np.where(use_ds, ds_test_slow, ds_test_fast)

        rng = np.random.default_rng(SEED + 100 + j)
        random_scores = []
        for _ in range(500):
            mask = np.zeros(n, bool)
            mask[rng.choice(n, k, replace=False)] = True
            random_scores.append(float(np.where(mask, ds_test_slow, ds_test_fast).mean()))

        utility = ds_test_slow - ds_test_fast
        oracle_idx = np.argsort(-utility, kind='mergesort')[:k]
        oracle_mask = np.zeros(n, bool)
        oracle_mask[oracle_idx] = True
        oracle = float(np.where(oracle_mask, ds_test_slow, ds_test_fast).mean())

        d_ds, lo_ds, hi_ds = bootstrap(ds_sel - ds_test_fast, n=5000, seed=SEED + 10 + j)
        d_ours, lo_ours, hi_ours = bootstrap(ours - sas_test, n=5000, seed=SEED + 20 + j)
        d_cross, lo_cross, hi_cross = bootstrap(ours - ds_sel, n=5000, seed=SEED + 30 + j)
        ds_fast_mean = float(ds_test_fast.mean())

        rows.append({
            'target_budget': budget, 'k': k, 'exact_rate': rate,
            'ds_fast_test_ndcg10': ds_fast_mean,
            'ds_slow_test_ndcg10': float(ds_test_slow.mean()),
            'ds_selective_test_ndcg10': float(ds_sel.mean()),
            'ds_delta_vs_fast': d_ds, 'ds_delta_ci_low': lo_ds, 'ds_delta_ci_high': hi_ds,
            'ds_random_test_ndcg10_mean': float(np.mean(random_scores)),
            'ds_oracle_test_ndcg10': oracle,
            'sasrec_test_ndcg10': float(sas_test.mean()),
            'memory_test_ndcg10': float(mem_test.mean()),
            'ours_selective_test_ndcg10': float(ours.mean()),
            'ours_delta_vs_sasrec': d_ours, 'ours_delta_ci_low': lo_ours, 'ours_delta_ci_high': hi_ours,
            'ours_minus_ds_selective': d_cross, 'cross_ci_low': lo_cross, 'cross_ci_high': hi_cross,
            'ds_gain_per_invocation': d_ds / rate,
            'ours_gain_per_invocation': d_ours / rate,
            'ds_oracle_fraction': d_ds / max(oracle - ds_fast_mean, EPS),
            'ours_selected_positive_fraction': float(((mem_test[use_ours] - sas_test[use_ours]) > 0).mean()),
            'ds_selected_positive_fraction': float(((ds_test_slow[use_ds] - ds_test_fast[use_ds]) > 0).mean()),
        })

    out = pd.DataFrame(rows)
    out.to_csv(args.out_dir / 'exact_matched_budget.csv', index=False)
    report = {
        'protocol': 'Exact test invocation count: identical K per budget, top-K by each frozen gate score; no test relevance labels used for routing.',
        'task': 'KuaiLive shop streamer-level LOO; 574 active-at-time negatives; candidate seed 20260918',
        'n_test': n,
        'budgets': BUDGETS,
        'dsframe': 'capacity-matched PRL slow path + paper-faithful MLP selector reimplementation; selector source is absent from public repo',
        'ours': 'frozen Selective v2 HGB architecture/features; full-dev fit predicts test; exact K externally imposed for budget fairness',
        'ds_slow_variant_selected_on_dev': slow_variant,
        'ds_dev_slow_ndcg10_variants': means,
        'results': rows,
    }
    (args.out_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(out.to_string(index=False))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
