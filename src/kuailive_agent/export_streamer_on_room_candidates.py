from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

import pandas as pd


def parse_ids(text):
    s = str(text).strip()
    return [int(x) for x in ast.literal_eval(s)] if s else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--room-data-dir', type=Path, required=True)
    ap.add_argument('--out-root', type=Path, required=True)
    ap.add_argument('--dataset', default='KuaiLiveShopStreamerOnRoom')
    args = ap.parse_args()

    train = pd.read_csv(args.room_data_dir / 'train.csv', sep='\t')
    dev = pd.read_csv(args.room_data_dir / 'dev.csv', sep='\t')
    test = pd.read_csv(args.room_data_dir / 'test.csv', sep='\t')
    room_map = pd.read_csv(args.room_data_dir / 'room_item_map.tsv', sep='\t')
    room_map[['item_id','streamer_id']] = room_map[['item_id','streamer_id']].astype('int64')
    item2streamer = dict(zip(room_map.item_id.astype(int), room_map.streamer_id.astype(int)))

    # The room export already fixes user IDs and split membership.  We only
    # change the item identity from ephemeral room ID to persistent streamer ID.
    positive_streamers = set()
    for df in (train, dev, test):
        positive_streamers.update(df.item_id.astype(int).map(item2streamer).astype(int))
    all_streamers = sorted(set(room_map.streamer_id.astype(int)))
    unseen = [s for s in all_streamers if s not in positive_streamers]
    seen = sorted(positive_streamers)
    ordered = unseen + seen
    smap = {s: i + 1 for i, s in enumerate(ordered)}
    assert max(smap[s] for s in positive_streamers) == len(smap)

    def convert(df, phase):
        x = pd.DataFrame({
            'user_id': df.user_id.astype(int),
            'item_id': df.item_id.astype(int).map(item2streamer).map(smap).astype(int),
            'time': df.time.astype('int64'),
        })
        if phase != 'train':
            negs = []
            for txt in df.neg_items:
                room_items = parse_ids(txt)
                negs.append(str([smap[int(item2streamer[int(i)])] for i in room_items]))
            x['neg_items'] = negs
        return x

    tr = convert(train, 'train').drop_duplicates(['user_id','item_id','time'], keep='last')
    dv = convert(dev, 'dev')
    te = convert(test, 'test')

    out = args.out_root / args.dataset
    out.mkdir(parents=True, exist_ok=True)
    tr.to_csv(out / 'train.csv', sep='\t', index=False)
    dv.to_csv(out / 'dev.csv', sep='\t', index=False)
    te.to_csv(out / 'test.csv', sep='\t', index=False)
    pd.DataFrame({'streamer_item_id':[smap[s] for s in ordered], 'streamer_id':ordered}).to_csv(
        out / 'streamer_item_map.tsv', sep='\t', index=False)

    # Duplicate streamer IDs among different room candidates are intentional.
    # A streamer model assigns them the same persistent-identity score; room
    # SASRec can still break ties after score fusion.
    meta = {
        'dataset': args.dataset,
        'train_rows': int(len(tr)), 'dev_rows': int(len(dv)), 'test_rows': int(len(te)),
        'streamer_universe': int(len(smap)),
        'room_candidate_protocol': str(args.room_data_dir),
    }
    (out / 'export_meta.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(json.dumps(meta, indent=2))


if __name__ == '__main__':
    main()
