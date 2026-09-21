from __future__ import annotations

import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--out-dir',type=Path,required=True)
    a=ap.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True)

    files=sorted(a.root.rglob('*_latency_replica_*.csv.gz'))
    if not files:
        raise SystemExit('no latency csv files found')
    frames=[pd.read_csv(p) for p in files]
    df=pd.concat(frames,ignore_index=True)
    df.to_csv(a.out_dir/'all_latency_samples.csv.gz',index=False,compression='gzip')

    pooled=[]
    for (system,budget),g in df.groupby(['system','budget'],dropna=False):
        x=g.latency_ms.to_numpy(float)
        pooled.append({
            'system':system,
            'budget':None if pd.isna(budget) else float(budget),
            'n':len(x),
            'replicas':int(g.replica.nunique()),
            'mean_ms':float(x.mean()),
            'p50_ms':float(np.quantile(x,.50)),
            'p95_ms':float(np.quantile(x,.95)),
            'p99_ms':float(np.quantile(x,.99)),
        })
    pooled_df=pd.DataFrame(pooled).sort_values(['system','budget'],na_position='first')
    pooled_df.to_csv(a.out_dir/'pooled_summary.csv',index=False)

    per=[]
    for (rep,system,budget),g in df.groupby(['replica','system','budget'],dropna=False):
        x=g.latency_ms.to_numpy(float)
        per.append({
            'replica':int(rep),'system':system,
            'budget':None if pd.isna(budget) else float(budget),
            'n':len(x),'mean_ms':float(x.mean()),
            'p50_ms':float(np.quantile(x,.50)),
            'p95_ms':float(np.quantile(x,.95)),
            'p99_ms':float(np.quantile(x,.99)),
        })
    pd.DataFrame(per).to_csv(a.out_dir/'replica_summary.csv',index=False)

    metas=[]
    for p in sorted(a.root.rglob('*_meta_replica_*.json')):
        metas.append(json.loads(p.read_text()))
    (a.out_dir/'environments.json').write_text(json.dumps(metas,indent=2)+'\n')

    # Derive an accuracy-latency-ready table for the selective-memory budgets.
    curve=pooled_df[pooled_df.system.str.startswith('selective_budget_')].copy()
    curve=curve.sort_values('budget')
    curve.to_csv(a.out_dir/'selective_latency_curve.csv',index=False)

    print('\n=== POOLED LATENCY SUMMARY ===')
    print(pooled_df.to_string(index=False))
    print('\n=== ENVIRONMENTS ===')
    for m in metas:
        print(m.get('replica'), m.get('cpu_model'), m.get('torch_threads'))

if __name__=='__main__': main()
