from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .evaluate import split_events

NEG_COLS = ['user_id', 'live_id', 'streamer_id', 'timestamp']


def recent_unique_exposures(g: pd.DataFrame, t: int, target: int, n_neg: int, window_ms: int) -> list[int]:
    if g is None or g.empty:
        return []
    times = g.timestamp.to_numpy(dtype=np.int64)
    rooms = g.live_id.to_numpy(dtype=np.int64)
    hi = int(np.searchsorted(times, t, side='left')) - 1
    lo_t = t - window_ms
    out = []
    used = {int(target)}
    i = hi
    while i >= 0 and int(times[i]) >= lo_t and len(out) < n_neg:
        room = int(rooms[i])
        if room not in used:
            out.append(room); used.add(room)
        i -= 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepared-dir', type=Path, required=True)
    ap.add_argument('--raw-data-dir', type=Path, required=True)
    ap.add_argument('--out-root', type=Path, required=True)
    ap.add_argument('--dataset', default='KuaiLiveShopRoomExposure')
    ap.add_argument('--n-neg', type=int, default=20)
    ap.add_argument('--window-hours', type=float, default=24.0)
    ap.add_argument('--chunksize', type=int, default=500_000)
    args = ap.parse_args()
    window_ms = int(args.window_hours * 3600 * 1000)

    events = pd.read_pickle(args.prepared_dir / 'events.pkl')
    rooms = pd.read_pickle(args.prepared_dir / 'rooms.pkl')
    train, dev, test = split_events(events, 3)
    cleaned = []
    dup = {}
    for name, x in [('train', train), ('dev', dev), ('test', test)]:
        before = len(x)
        x = x.drop_duplicates(['user_id','live_id','timestamp'], keep='last').copy()
        dup[name] = before - len(x)
        cleaned.append(x)
    train, dev, test = cleaned
    common = set(dev.user_id.astype(int)) & set(test.user_id.astype(int))
    train = train[train.user_id.astype(int).isin(common)].copy()
    dev = dev[dev.user_id.astype(int).isin(common)].copy()
    test = test[test.user_id.astype(int).isin(common)].copy()

    room_meta = rooms[['live_id','streamer_id']].dropna().drop_duplicates('live_id').copy()
    room_meta[['live_id','streamer_id']] = room_meta[['live_id','streamer_id']].astype('int64')
    valid_rooms = set(room_meta.live_id.astype(int))
    room_streamer = dict(zip(room_meta.live_id.astype(int), room_meta.streamer_id.astype(int)))

    neg_path = args.raw_data_dir / 'negative.csv'
    if not neg_path.exists():
        raise FileNotFoundError(neg_path)
    parts = []
    raw_neg = kept_neg = 0
    common_arr = common
    for chunk in pd.read_csv(neg_path, usecols=NEG_COLS, chunksize=args.chunksize):
        raw_neg += len(chunk)
        chunk = chunk[chunk.user_id.astype(int).isin(common_arr) & chunk.live_id.astype(int).isin(valid_rooms)].copy()
        if chunk.empty:
            continue
        chunk[['user_id','live_id','streamer_id','timestamp']] = chunk[['user_id','live_id','streamer_id','timestamp']].astype('int64')
        # Trust room metadata for identity and drop any inconsistent exposure row.
        expected = chunk.live_id.map(room_streamer)
        chunk = chunk[expected.astype('Int64').eq(chunk.streamer_id.astype('Int64')).fillna(False)]
        kept_neg += len(chunk)
        parts.append(chunk)
    neg = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=NEG_COLS)
    neg = neg.sort_values(['user_id','timestamp','live_id'], kind='mergesort').reset_index(drop=True)
    neg_by_user = {int(uid): g[['live_id','timestamp']].reset_index(drop=True) for uid, g in neg.groupby('user_id', sort=False)}

    def build_candidates(df: pd.DataFrame):
        out = {}
        counts = []
        for idx, r in df.iterrows():
            uid = int(r.user_id); t = int(r.timestamp); target = int(r.live_id)
            c = recent_unique_exposures(neg_by_user.get(uid), t, target, args.n_neg, window_ms)
            out[int(uid)] = c
            counts.append(len(c))
        return out, np.asarray(counts, int)

    dev_cs, dev_counts = build_candidates(dev)
    test_cs, test_counts = build_candidates(test)
    eligible = {u for u in common if len(dev_cs.get(int(u), [])) >= args.n_neg and len(test_cs.get(int(u), [])) >= args.n_neg}
    train = train[train.user_id.astype(int).isin(eligible)].copy()
    dev = dev[dev.user_id.astype(int).isin(eligible)].copy()
    test = test[test.user_id.astype(int).isin(eligible)].copy()
    if not len(eligible):
        raise RuntimeError('No users have enough causal official exposure negatives in both dev and test')

    users = sorted(int(u) for u in eligible)
    uidmap = {u: i+1 for i, u in enumerate(users)}

    positive = set(pd.concat([train.live_id, dev.live_id, test.live_id]).astype(int))
    selected_neg_rooms = set()
    for u in users:
        selected_neg_rooms.update(dev_cs[u][:args.n_neg]); selected_neg_rooms.update(test_cs[u][:args.n_neg])
    universe = positive | selected_neg_rooms
    candidate_only = sorted(universe - positive)
    seen = sorted(positive)
    ordered_rooms = candidate_only + seen
    imap = {room: i+1 for i, room in enumerate(ordered_rooms)}
    assert max(imap[r] for r in positive) == len(imap)

    def base(x: pd.DataFrame):
        return pd.DataFrame({'user_id': x.user_id.astype(int).map(uidmap),
                             'item_id': x.live_id.astype(int).map(imap),
                             'time': x.timestamp.astype('int64')})
    tr = base(train); dv = base(dev); te = base(test)
    dv['neg_items'] = [str([imap[x] for x in dev_cs[int(u)][:args.n_neg]]) for u in dev.user_id.astype(int)]
    te['neg_items'] = [str([imap[x] for x in test_cs[int(u)][:args.n_neg]]) for u in test.user_id.astype(int)]

    out = args.out_root / args.dataset
    out.mkdir(parents=True, exist_ok=True)
    tr.to_csv(out/'train.csv', sep='\t', index=False)
    dv.to_csv(out/'dev.csv', sep='\t', index=False)
    te.to_csv(out/'test.csv', sep='\t', index=False)
    pd.DataFrame({'item_id':[imap[r] for r in ordered_rooms], 'live_id':ordered_rooms,
                  'streamer_id':[room_streamer[r] for r in ordered_rooms]}).to_csv(out/'room_item_map.tsv', sep='\t', index=False)

    train_hist = {int(u): set(g.streamer_id.astype(int)) for u,g in train.groupby('user_id', sort=False)}
    pretest_events = pd.concat([train, dev[['user_id','live_id','streamer_id','timestamp','watch_live_time']]], ignore_index=True)
    test_hist = {int(u): set(g.streamer_id.astype(int)) for u,g in pretest_events.groupby('user_id', sort=False)}
    def fam_stats(df, cs, hist):
        target_fam=[]; neg_fam=[]
        for r in df.itertuples(index=False):
            uid=int(r.user_id); h=hist.get(uid,set()); ts=int(r.streamer_id)
            target_fam.append(ts in h)
            negs=cs[uid][:args.n_neg]
            neg_fam.append(np.mean([room_streamer[int(x)] in h for x in negs]))
        return float(np.mean(target_fam)), float(np.mean(neg_fam)), float(np.mean(np.asarray(neg_fam)>0))
    dev_tf, dev_nf, dev_any = fam_stats(dev, dev_cs, train_hist)
    test_tf, test_nf, test_any = fam_stats(test, test_cs, test_hist)

    meta = {
        'dataset': args.dataset,
        'task': 'next_live_room_with_recent_official_unclicked_exposures',
        'negative_source': 'KuaiLive negative.csv: exposures presented to users but not clicked',
        'causal_rule': f'most recent {args.n_neg} distinct shop live_id exposures with exposure_timestamp < target_timestamp and within previous {args.window_hours:g} hours',
        'n_neg': args.n_neg,
        'candidate_count': args.n_neg + 1,
        'window_hours': args.window_hours,
        'original_common_users': len(common),
        'eligible_users': len(users),
        'eligible_rate': len(users)/max(len(common),1),
        'train_rows': len(tr), 'dev_rows': len(dv), 'test_rows': len(te),
        'room_universe': len(imap), 'positive_rooms': len(positive),
        'raw_negative_rows': raw_neg, 'shop_common_user_negative_rows': kept_neg,
        'dev_users_with_at_least_n': int(np.sum(dev_counts >= args.n_neg)),
        'test_users_with_at_least_n': int(np.sum(test_counts >= args.n_neg)),
        'dev_negative_count_median_before_filter': float(np.median(dev_counts)),
        'test_negative_count_median_before_filter': float(np.median(test_counts)),
        'dev_target_familiar_streamer_rate': dev_tf,
        'test_target_familiar_streamer_rate': test_tf,
        'dev_mean_negative_familiar_streamer_rate': dev_nf,
        'test_mean_negative_familiar_streamer_rate': test_nf,
        'dev_any_familiar_streamer_negative_rate': dev_any,
        'test_any_familiar_streamer_negative_rate': test_any,
        'duplicates_dropped': dup,
        'guardrail': 'This is exposure-aware ranking robustness, not IPS/SNIPS or causal estimation; no propensity scores are available.',
    }
    (out/'export_meta.json').write_text(json.dumps(meta, indent=2)+'\n')
    print(json.dumps(meta, indent=2))


if __name__ == '__main__':
    main()
