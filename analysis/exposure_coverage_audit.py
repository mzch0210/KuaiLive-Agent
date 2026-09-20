from __future__ import annotations

import argparse
import json
from bisect import bisect_left
from pathlib import Path

import numpy as np
import pandas as pd

from kuailive_agent.evaluate import split_events


def parse_ints(s: str) -> list[int]:
    return [int(x.strip()) for x in s.split(',') if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepared-dir', type=Path, required=True)
    ap.add_argument('--raw-dir', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--windows-hours', default='1,6,24,72,168,336')
    ap.add_argument('--ks', default='5,10,20')
    ap.add_argument('--min-users', type=int, default=2000)
    args = ap.parse_args()

    windows = sorted(parse_ints(args.windows_hours))
    ks = sorted(parse_ints(args.ks))
    if not windows or not ks:
        raise ValueError('windows and ks must be non-empty')

    events = pd.read_pickle(args.prepared_dir / 'events.pkl')
    rooms = pd.read_pickle(args.prepared_dir / 'rooms.pkl')
    train, dev, test = split_events(events, 3)
    cleaned = []
    for x in (train, dev, test):
        cleaned.append(x.drop_duplicates(['user_id', 'live_id', 'timestamp'], keep='last').copy())
    train, dev, test = cleaned

    common = set(dev.user_id.astype(int)) & set(test.user_id.astype(int))
    dev = dev[dev.user_id.astype(int).isin(common)].copy()
    test = test[test.user_id.astype(int).isin(common)].copy()
    users = sorted(common)

    shop_live = set(rooms.live_id.dropna().astype('int64').unique().tolist())
    neg = pd.read_csv(
        args.raw_dir / 'negative.csv',
        usecols=['user_id', 'live_id', 'streamer_id', 'timestamp'],
    )
    raw_negative_rows = int(len(neg))
    neg = neg[neg.user_id.astype(int).isin(common)].copy()
    user_filtered_rows = int(len(neg))
    neg = neg[neg.live_id.astype(int).isin(shop_live)].copy()
    shop_filtered_rows = int(len(neg))
    neg[['user_id', 'live_id', 'streamer_id', 'timestamp']] = neg[
        ['user_id', 'live_id', 'streamer_id', 'timestamp']
    ].astype('int64')
    neg.sort_values(['user_id', 'timestamp'], inplace=True)

    by_user: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    for uid, g in neg.groupby('user_id', sort=False):
        by_user[int(uid)] = (
            g.timestamp.to_numpy(dtype=np.int64),
            g.live_id.to_numpy(dtype=np.int64),
        )

    targets = {'dev': dev, 'test': test}
    pool_records: list[dict] = []
    one_hour = 3600 * 1000
    for split, frame in targets.items():
        for r in frame.itertuples(index=False):
            uid = int(r.user_id)
            target = int(r.live_id)
            t = int(r.timestamp)
            arr = by_user.get(uid)
            if arr is None:
                for w in windows:
                    pool_records.append({'split': split, 'user_id': uid, 'window_hours': w, 'pool_size': 0})
                continue
            times, lives = arr
            hi = bisect_left(times, t)
            for w in windows:
                lo = bisect_left(times, t - w * one_hour, 0, hi)
                # Real logged non-click exposures strictly before the target.
                # Deduplicate repeated impressions of the same room and exclude target room.
                vals = lives[lo:hi]
                if vals.size:
                    vals = vals[vals != target]
                    n = int(np.unique(vals).size)
                else:
                    n = 0
                pool_records.append({'split': split, 'user_id': uid, 'window_hours': w, 'pool_size': n})

    pools = pd.DataFrame(pool_records)
    dev_p = pools[pools.split == 'dev'].pivot(index='user_id', columns='window_hours', values='pool_size')
    test_p = pools[pools.split == 'test'].pivot(index='user_id', columns='window_hours', values='pool_size')

    rows = []
    for w in windows:
        d = dev_p[w].reindex(users, fill_value=0).to_numpy(dtype=int)
        t = test_p[w].reindex(users, fill_value=0).to_numpy(dtype=int)
        for k in ks:
            d_ok = d >= k
            t_ok = t >= k
            both = d_ok & t_ok
            rows.append({
                'window_hours': w,
                'k': k,
                'dev_eligible_users': int(d_ok.sum()),
                'dev_eligible_rate': float(d_ok.mean()),
                'test_eligible_users': int(t_ok.sum()),
                'test_eligible_rate': float(t_ok.mean()),
                'both_eligible_users': int(both.sum()),
                'both_eligible_rate': float(both.mean()),
                'dev_pool_p50': float(np.quantile(d, 0.50)),
                'dev_pool_p90': float(np.quantile(d, 0.90)),
                'dev_pool_p99': float(np.quantile(d, 0.99)),
                'test_pool_p50': float(np.quantile(t, 0.50)),
                'test_pool_p90': float(np.quantile(t, 0.90)),
                'test_pool_p99': float(np.quantile(t, 0.99)),
            })
    grid = pd.DataFrame(rows).sort_values(['k', 'window_hours']).reset_index(drop=True)

    # Frozen selection rule: preserve k=10 if at least min_users have sufficient
    # official exposures in BOTH dev and test; among qualifying protocols choose
    # the shortest lookback. If impossible, fall back to k=5 under the same rule.
    selected = None
    for preferred_k in (10, 5):
        if preferred_k not in ks:
            continue
        z = grid[(grid.k == preferred_k) & (grid.both_eligible_users >= args.min_users)]
        if len(z):
            selected = z.sort_values('window_hours').iloc[0].to_dict()
            break
    coverage_failure = selected is None
    if selected is None:
        selected = grid.sort_values(
            ['both_eligible_users', 'k', 'window_hours'],
            ascending=[False, False, True],
        ).iloc[0].to_dict()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    grid.to_csv(args.out_dir / 'coverage_grid.csv', index=False)
    pools.to_csv(args.out_dir / 'pool_sizes_by_user.csv', index=False)

    audit = {
        'protocol_family': 'official_negative_recent_preclick_exposure',
        'negative_definition': 'KuaiLive negative.csv: exposure presented to user but not clicked',
        'future_exposures_used': False,
        'target_time_active_filter': False,
        'deduplicate_live_id_within_window': True,
        'all_users': len(users),
        'raw_negative_rows': raw_negative_rows,
        'negative_rows_for_eval_users': user_filtered_rows,
        'shop_negative_rows_for_eval_users': shop_filtered_rows,
        'users_with_shop_negative': int(neg.user_id.nunique()),
        'windows_hours': windows,
        'ks': ks,
        'min_users': args.min_users,
        'selection_rule': 'prefer k=10, then k=5; require >= min_users eligible in both dev/test; choose shortest lookback; coverage only, no model metrics',
        'coverage_failure': coverage_failure,
        'selected': {k: (int(v) if k in {'window_hours','k','dev_eligible_users','test_eligible_users','both_eligible_users'} else float(v)) for k, v in selected.items()},
    }
    (args.out_dir / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(grid.to_string(index=False))
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
