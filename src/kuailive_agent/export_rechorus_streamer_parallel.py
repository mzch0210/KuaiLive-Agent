from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd


def parse_ids(text: str) -> list[int]:
    x = ast.literal_eval(str(text))
    return [int(v) for v in x]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--room-data-dir', type=Path, required=True)
    ap.add_argument('--out-root', type=Path, required=True)
    ap.add_argument('--dataset', default='KuaiLiveShopStreamerParallel')
    args = ap.parse_args()

    train = pd.read_csv(args.room_data_dir / 'train.csv', sep='\t')
    dev = pd.read_csv(args.room_data_dir / 'dev.csv', sep='\t')
    test = pd.read_csv(args.room_data_dir / 'test.csv', sep='\t')
    room_map = pd.read_csv(args.room_data_dir / 'room_item_map.tsv', sep='\t')
    room_map[['item_id', 'live_id', 'streamer_id']] = room_map[['item_id', 'live_id', 'streamer_id']].astype('int64')
    item_to_streamer = dict(zip(room_map.item_id.astype(int), room_map.streamer_id.astype(int)))

    positive_streamers = set()
    for df in (train, dev, test):
        positive_streamers.update(item_to_streamer[int(i)] for i in df.item_id.astype(int))
    universe = set(room_map.streamer_id.astype(int))
    unseen = sorted(universe - positive_streamers)
    seen = sorted(positive_streamers)
    ordered = unseen + seen
    smap = {sid: i + 1 for i, sid in enumerate(ordered)}
    assert max(smap[s] for s in positive_streamers) == len(smap)

    def convert_base(df: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame({
            'user_id': df.user_id.astype(int),
            'item_id': [smap[item_to_streamer[int(i)]] for i in df.item_id.astype(int)],
            'time': df.time.astype('int64'),
        })

    tr = convert_base(train)
    dv = convert_base(dev)
    te = convert_base(test)

    duplicate_rates = {}
    target_duplicate_rates = {}
    for name, src, dst in [('dev', dev, dv), ('test', test, te)]:
        neg_out = []
        dup = []
        target_dup = []
        for r in src.itertuples(index=False):
            neg_rooms = parse_ids(r.neg_items)
            neg_streamers = [smap[item_to_streamer[int(room_item)]] for room_item in neg_rooms]
            target_streamer = smap[item_to_streamer[int(r.item_id)]]
            neg_out.append(str(neg_streamers))
            all_ids = [target_streamer] + neg_streamers
            dup.append(1.0 - len(set(all_ids)) / max(len(all_ids), 1))
            target_dup.append(float(sum(x == target_streamer for x in neg_streamers) > 0))
        dst['neg_items'] = neg_out
        duplicate_rates[name] = float(np.mean(dup))
        target_duplicate_rates[name] = float(np.mean(target_dup))

    out = args.out_root / args.dataset
    out.mkdir(parents=True, exist_ok=True)
    tr.to_csv(out / 'train.csv', sep='\t', index=False)
    dv.to_csv(out / 'dev.csv', sep='\t', index=False)
    te.to_csv(out / 'test.csv', sep='\t', index=False)
    pd.DataFrame({'item_id': [smap[s] for s in ordered], 'streamer_id': ordered}).to_csv(
        out / 'streamer_item_map.tsv', sep='\t', index=False
    )

    meta = {
        'dataset': args.dataset,
        'task': 'parallel_streamer_sequence_for_same_room_candidates',
        'users': int(test.user_id.nunique()),
        'train_rows': int(len(tr)),
        'dev_rows': int(len(dv)),
        'test_rows': int(len(te)),
        'streamer_universe': int(len(smap)),
        'positive_streamers': int(len(positive_streamers)),
        'candidate_duplicate_streamer_rate': duplicate_rates,
        'target_streamer_repeated_among_negative_rooms_rate': target_duplicate_rates,
        'note': 'Negative positions preserve the exact room-candidate list; multiple rooms from one streamer intentionally map to repeated streamer IDs.',
    }
    (out / 'export_meta.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(json.dumps(meta, indent=2))


if __name__ == '__main__':
    main()
