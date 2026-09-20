from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from kuailive_agent.evaluate import split_events

NEG_COLS = ['user_id','live_id','streamer_id','timestamp']


def count_recent_unique(g: pd.DataFrame, t: int, target: int, window_ms: int, cap: int = 20) -> int:
    if g is None or g.empty:
        return 0
    times = g.timestamp.to_numpy(dtype=np.int64)
    rooms = g.live_id.to_numpy(dtype=np.int64)
    hi = int(np.searchsorted(times, t, side='left')) - 1
    lo_t = t - window_ms
    used = {int(target)}
    n = 0
    i = hi
    while i >= 0 and int(times[i]) >= lo_t and n < cap:
        room = int(rooms[i])
        if room not in used:
            used.add(room); n += 1
        i -= 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepared-dir', type=Path, required=True)
    ap.add_argument('--raw-data-dir', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--min-users', type=int, default=2000)
    ap.add_argument('--chunksize', type=int, default=500000)
    args = ap.parse_args(); args.out_dir.mkdir(parents=True, exist_ok=True)

    events = pd.read_pickle(args.prepared_dir/'events.pkl')
    rooms = pd.read_pickle(args.prepared_dir/'rooms.pkl')
    train, dev, test = split_events(events, 3)
    dev = dev.drop_duplicates(['user_id','live_id','timestamp'], keep='last')
    test = test.drop_duplicates(['user_id','live_id','timestamp'], keep='last')
    common = set(dev.user_id.astype(int)) & set(test.user_id.astype(int))
    dev = dev[dev.user_id.astype(int).isin(common)].copy()
    test = test[test.user_id.astype(int).isin(common)].copy()

    room_meta = rooms[['live_id','streamer_id']].dropna().drop_duplicates('live_id').copy()
    room_meta[['live_id','streamer_id']] = room_meta[['live_id','streamer_id']].astype('int64')
    valid_rooms = set(room_meta.live_id.astype(int))
    room_streamer = dict(zip(room_meta.live_id.astype(int), room_meta.streamer_id.astype(int)))

    parts=[]
    for chunk in pd.read_csv(args.raw_data_dir/'negative.csv', usecols=NEG_COLS, chunksize=args.chunksize):
        chunk = chunk[chunk.user_id.astype(int).isin(common) & chunk.live_id.astype(int).isin(valid_rooms)].copy()
        if chunk.empty: continue
        chunk[['user_id','live_id','streamer_id','timestamp']] = chunk[['user_id','live_id','streamer_id','timestamp']].astype('int64')
        expected = chunk.live_id.map(room_streamer)
        chunk = chunk[expected.astype('Int64').eq(chunk.streamer_id.astype('Int64')).fillna(False)]
        parts.append(chunk[['user_id','live_id','timestamp']])
    neg = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=['user_id','live_id','timestamp'])
    neg = neg.sort_values(['user_id','timestamp','live_id'], kind='mergesort').reset_index(drop=True)
    by_user = {int(u): g[['live_id','timestamp']].reset_index(drop=True) for u,g in neg.groupby('user_id', sort=False)}

    windows = [24,72,168,504]
    ns = [5,10,20]
    dev_counts = {w:{} for w in windows}; test_counts = {w:{} for w in windows}
    for w in windows:
        wm = int(w*3600*1000)
        for r in dev.itertuples(index=False):
            dev_counts[w][int(r.user_id)] = count_recent_unique(by_user.get(int(r.user_id)), int(r.timestamp), int(r.live_id), wm, 20)
        for r in test.itertuples(index=False):
            test_counts[w][int(r.user_id)] = count_recent_unique(by_user.get(int(r.user_id)), int(r.timestamp), int(r.live_id), wm, 20)

    rows=[]
    for n in ns:
        for w in windows:
            du={u for u,c in dev_counts[w].items() if c>=n}
            tu={u for u,c in test_counts[w].items() if c>=n}
            both=du & tu
            rows.append({'n_neg':n,'window_hours':w,'dev_users':len(du),'test_users':len(tu),
                         'both_users':len(both),'both_rate':len(both)/max(len(common),1)})
    grid=pd.DataFrame(rows).sort_values(['n_neg','window_hours'], ascending=[False,True])
    grid.to_csv(args.out_dir/'coverage_grid.csv', index=False)

    eligible=grid[grid.both_users>=args.min_users].copy()
    selected=None
    if len(eligible):
        eligible=eligible.sort_values(['n_neg','window_hours'], ascending=[False,True])
        selected=eligible.iloc[0].to_dict()
        selected={k:(int(v) if k in ['n_neg','window_hours','dev_users','test_users','both_users'] else float(v)) for k,v in selected.items()}
    report={'common_users':len(common),'shop_negative_rows':int(len(neg)),'min_users_rule':args.min_users,
            'selection_rule':'among protocols with both_users >= min_users, maximize n_neg then minimize window_hours',
            'selected_protocol':selected}
    (args.out_dir/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(grid.to_string(index=False)); print(json.dumps(report, indent=2))


if __name__=='__main__':
    main()
