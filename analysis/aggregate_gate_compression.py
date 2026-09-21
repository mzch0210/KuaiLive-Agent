from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--accuracy-report', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(a.root.rglob('gate_latency_replica_*.csv.gz'))
    if len(files) != 3:
        raise SystemExit(f'expected 3 latency replica files, found {len(files)}')
    df = pd.concat([pd.read_csv(p) for p in files], ignore_index=True)
    df.to_csv(a.out_dir / 'all_latency_samples.csv.gz', index=False, compression='gzip')

    pooled = []
    for system, g in df.groupby('system'):
        x = g.latency_ms.to_numpy(float)
        pooled.append({
            'system': system,
            'n': len(x),
            'replicas': int(g.replica.nunique()),
            'mean_ms': float(x.mean()),
            'p50_ms': float(np.quantile(x, .5)),
            'p95_ms': float(np.quantile(x, .95)),
            'p99_ms': float(np.quantile(x, .99)),
        })
    p = pd.DataFrame(pooled).sort_values('system')
    p.to_csv(a.out_dir / 'pooled_latency.csv', index=False)

    per = []
    for (rep, system), g in df.groupby(['replica', 'system']):
        x = g.latency_ms.to_numpy(float)
        per.append({
            'replica': int(rep), 'system': system, 'n': len(x),
            'mean_ms': float(x.mean()), 'p50_ms': float(np.quantile(x, .5)),
            'p95_ms': float(np.quantile(x, .95)), 'p99_ms': float(np.quantile(x, .99)),
        })
    pd.DataFrame(per).to_csv(a.out_dir / 'replica_latency.csv', index=False)

    report = json.loads(a.accuracy_report.read_text())
    lmap = p.set_index('system').to_dict('index')
    dual = lmap['dual_id']
    mem = lmap['memory_fusion_cached']
    rows = []
    for gate, sysname, gatename in [
        ('hgb', 'selective_hgb', 'gate_hgb_predict_only'),
        ('ridge', 'selective_ridge', 'gate_ridge_numpy_only'),
        ('tiny_mlp', 'selective_tiny_mlp', 'gate_tiny_mlp_numpy_only'),
    ]:
        g = report['gates'][gate]
        sl = lmap[sysname]
        gl = lmap[gatename]
        inc = sl['mean_ms'] - dual['mean_ms']
        expected_mem = g['test_invocation_rate'] * mem['mean_ms']
        rows.append({
            'gate': gate,
            'test_ndcg10': g['test_ndcg10'],
            'delta_vs_dual': g['test_delta_vs_dual'],
            'ci95_low': g['ci95_low'],
            'ci95_high': g['ci95_high'],
            'invocation_rate': g['test_invocation_rate'],
            'selective_mean_ms': sl['mean_ms'],
            'selective_p50_ms': sl['p50_ms'],
            'selective_p95_ms': sl['p95_ms'],
            'gate_only_mean_ms': gl['mean_ms'],
            'dual_mean_ms': dual['mean_ms'],
            'memory_mean_ms': mem['mean_ms'],
            'incremental_mean_ms': inc,
            'latency_ratio_vs_dual': sl['mean_ms'] / dual['mean_ms'],
            'expected_memory_component_ms': expected_mem,
            'gate_share_of_increment': gl['mean_ms'] / inc if inc > 0 else np.nan,
        })
    curve = pd.DataFrame(rows)
    curve.to_csv(a.out_dir / 'accuracy_latency_summary.csv', index=False)

    metas = []
    for f in sorted(a.root.rglob('gate_meta_replica_*.json')):
        metas.append(json.loads(f.read_text()))
    (a.out_dir / 'environments.json').write_text(json.dumps(metas, indent=2) + '\n')
    (a.out_dir / 'accuracy_report.json').write_text(json.dumps(report, indent=2) + '\n')

    print('=== ACCURACY-LATENCY SUMMARY ===')
    print(curve.to_string(index=False))
    print('\n=== POOLED LATENCY ===')
    print(p.to_string(index=False))


if __name__ == '__main__':
    main()
