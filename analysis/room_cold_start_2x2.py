from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260918


def boot(x, seed, n_boot=5000):
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed)
    vals = np.empty(n_boot)
    n = len(x)
    for i in range(n_boot):
        vals[i] = x[rng.integers(0, n, n)].mean()
    return float(x.mean()), float(np.quantile(vals, .025)), float(np.quantile(vals, .975))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--per-user', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    d = pd.read_csv(args.per_user)
    d['selective_score10'] = np.where(d.primary_use_agent, d.MemoryFusion_score10, d.sasrec_score10)
    d['selective_rank'] = np.where(d.primary_use_agent, d.memory_rank, d.sasrec_rank).astype(int)
    total_gain = float((d.selective_score10 - d.sasrec_score10).sum())

    rows = []
    specs = [
        (True, True, 'seen_room__familiar_streamer'),
        (True, False, 'seen_room__novel_streamer'),
        (False, True, 'new_room__familiar_streamer'),
        (False, False, 'new_room__novel_streamer'),
    ]
    for i, (room_seen, familiar, name) in enumerate(specs):
        g = d[(d.target_room_seen_train == room_seen) &
              (d.target_streamer_user_familiar_pre_event == familiar)].copy()
        diff = g.selective_score10 - g.sasrec_score10
        delta, lo, hi = boot(diff, SEED + i * 17)
        rows.append({
            'group': name,
            'room_seen_train': room_seen,
            'user_familiar_streamer': familiar,
            'n': int(len(g)),
            'share': float(len(g) / len(d)),
            'sasrec_ndcg10': float(g.sasrec_score10.mean()),
            'memory_ndcg10': float(g.MemoryFusion_score10.mean()),
            'selective_ndcg10': float(g.selective_score10.mean()),
            'selective_minus_sasrec': delta,
            'ci95_low': lo,
            'ci95_high': hi,
            'sasrec_hr10': float((g.sasrec_rank <= 10).mean()),
            'memory_hr10': float((g.memory_rank <= 10).mean()),
            'selective_hr10': float((g.selective_rank <= 10).mean()),
            'gate_rate': float(g.primary_use_agent.mean()),
            'gain_contribution_share': float(diff.sum() / total_gain),
        })
    out = pd.DataFrame(rows)
    out.to_csv(args.out_dir / 'room_streamer_2x2.csv', index=False)

    q = out.set_index('group')
    seen_novel = q.loc['seen_room__novel_streamer']
    seen_fam = q.loc['seen_room__familiar_streamer']
    new_fam = q.loc['new_room__familiar_streamer']
    if seen_novel.ci95_high < 0 and seen_fam.ci95_low > 0 and new_fam.ci95_low > 0:
        conclusion = 'gain_is_driven_by_persistent_user_streamer_familiarity_not_room_cold_start_alone'
    else:
        conclusion = 'mixed_mechanism_requires_more_diagnostics'

    report = {
        'source_run': 35481681725,
        'users': int(len(d)),
        'conclusion': conclusion,
        'key_test': {
            'seen_room_novel_streamer_delta': float(seen_novel.selective_minus_sasrec),
            'seen_room_novel_streamer_ci95': [float(seen_novel.ci95_low), float(seen_novel.ci95_high)],
            'seen_room_familiar_streamer_delta': float(seen_fam.selective_minus_sasrec),
            'new_room_familiar_streamer_delta': float(new_fam.selective_minus_sasrec),
        },
        'interpretation': 'If Selective loses on seen-room/novel-streamer but wins strongly whenever the target streamer is in user history, the dominant mechanism is persistent streamer relationship transfer rather than generic selective agentic reasoning.',
    }
    (args.out_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    print(out.to_string(index=False))


if __name__ == '__main__':
    main()
