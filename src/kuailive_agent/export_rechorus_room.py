from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .evaluate import IndexedCounterSet, split_events


def room_candidate_sets(targets: pd.DataFrame, rooms: pd.DataFrame, n_neg: int, seed: int):
    """Sample legal live-room negatives active at each target timestamp.

    The positive room is always placed first. Active negatives satisfy
    start_timestamp <= t < end_timestamp and are distinct live_id values.
    """
    rr = rooms[["live_id", "start_timestamp", "end_timestamp"]].dropna().drop_duplicates("live_id").copy()
    rr[["live_id", "start_timestamp", "end_timestamp"]] = rr[["live_id", "start_timestamp", "end_timestamp"]].astype("int64")
    starts = rr.sort_values("start_timestamp")
    ends = rr.sort_values("end_timestamp")
    s_t = starts.start_timestamp.to_numpy()
    s_id = starts.live_id.to_numpy()
    e_t = ends.end_timestamp.to_numpy()
    e_id = ends.live_id.to_numpy()

    ordered = targets.reset_index().sort_values("timestamp")
    active = IndexedCounterSet()
    i = j = 0
    rng = np.random.default_rng(seed)
    out = {}
    lengths = []
    target_active = 0
    for r in ordered.itertuples(index=False):
        t = int(r.timestamp)
        while i < len(s_t) and int(s_t[i]) <= t:
            active.add(int(s_id[i])); i += 1
        # Official KuaiLive author->room mapping uses timestamp < end_timestamp.
        while j < len(e_t) and int(e_t[j]) <= t:
            active.remove(int(e_id[j])); j += 1
        target = int(r.live_id)
        if target in active.index:
            target_active += 1
        neg = active.sample(n_neg, rng, exclude=target)
        out[int(r.index)] = np.concatenate(([target], neg))
        lengths.append(len(neg))
    return out, np.asarray(lengths, dtype=int), target_active


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepared-dir", type=Path, required=True)
    ap.add_argument("--out-root", type=Path, required=True)
    ap.add_argument("--dataset", default="KuaiLiveShopRoom")
    ap.add_argument("--n-neg", type=int, default=574)
    ap.add_argument("--seed", type=int, default=20260918)
    args = ap.parse_args()

    events = pd.read_pickle(args.prepared_dir / "events.pkl")
    rooms = pd.read_pickle(args.prepared_dir / "rooms.pkl")
    train, dev, test = split_events(events, 3)

    # ReChorus SeqReader merges on (user,item,time), so exact duplicate room events
    # must be removed before export.
    cleaned = []
    dup = {}
    for name, x in [("train", train), ("dev", dev), ("test", test)]:
        before = len(x)
        x = x.drop_duplicates(["user_id", "live_id", "timestamp"], keep="last").copy()
        dup[name] = before - len(x)
        cleaned.append(x)
    train, dev, test = cleaned

    # Keep only users represented in both dev and test after duplicate removal.
    common = set(dev.user_id.astype(int)) & set(test.user_id.astype(int))
    train = train[train.user_id.astype(int).isin(common)].copy()
    dev = dev[dev.user_id.astype(int).isin(common)].copy()
    test = test[test.user_id.astype(int).isin(common)].copy()
    if dev.user_id.duplicated().any() or test.user_id.duplicated().any():
        raise ValueError("room-level dev/test must contain one target per user")

    users = sorted(common)
    uidmap = {int(u): i + 1 for i, u in enumerate(users)}

    room_meta = rooms[["live_id", "streamer_id"]].dropna().drop_duplicates("live_id").copy()
    room_meta[["live_id", "streamer_id"]] = room_meta[["live_id", "streamer_id"]].astype("int64")
    room_streamer = dict(zip(room_meta.live_id.astype(int), room_meta.streamer_id.astype(int)))

    positive = set(pd.concat([train.live_id, dev.live_id, test.live_id]).astype(int))
    universe = set(room_meta.live_id.astype(int))
    missing = positive - universe
    if missing:
        raise ValueError(f"positive live_ids absent from room metadata: {len(missing)}")
    unseen = sorted(universe - positive)
    seen = sorted(positive)
    ordered_rooms = unseen + seen
    imap = {room: i + 1 for i, room in enumerate(ordered_rooms)}
    # ReChorus infers n_items from positive rows; place seen rooms last so max
    # positive item id spans the full active-room candidate universe.
    assert max(imap[r] for r in positive) == len(imap)

    dev_cs, dev_len, dev_target_active = room_candidate_sets(dev, rooms, args.n_neg, args.seed)
    test_cs, test_len, test_target_active = room_candidate_sets(test, rooms, args.n_neg, args.seed)
    if not (np.all(dev_len == args.n_neg) and np.all(test_len == args.n_neg)):
        raise ValueError(
            f"Fixed room candidate requirement failed for n_neg={args.n_neg}: "
            f"dev min/max={dev_len.min()}/{dev_len.max()}, "
            f"test min/max={test_len.min()}/{test_len.max()}"
        )

    def base(x):
        return pd.DataFrame({
            "user_id": x.user_id.astype(int).map(uidmap),
            "item_id": x.live_id.astype(int).map(imap),
            "time": x.timestamp.astype("int64"),
        })

    tr = base(train)
    dv = base(dev)
    te = base(test)

    def negcol(x, csets):
        vals = []
        for idx, r in x.iterrows():
            target = int(r.live_id)
            c = csets[idx][1:]
            out = []
            used = {target}
            for room in c:
                room = int(room)
                if room in imap and room not in used:
                    out.append(imap[room]); used.add(room)
            if len(out) != args.n_neg:
                raise ValueError(f"room candidate mapping became ragged: {len(out)}")
            vals.append(str(out))
        return vals

    dv["neg_items"] = negcol(dev, dev_cs)
    te["neg_items"] = negcol(test, test_cs)

    out = args.out_root / args.dataset
    out.mkdir(parents=True, exist_ok=True)
    tr.to_csv(out / "train.csv", sep="\t", index=False)
    dv.to_csv(out / "dev.csv", sep="\t", index=False)
    te.to_csv(out / "test.csv", sep="\t", index=False)

    map_df = pd.DataFrame({
        "item_id": [imap[r] for r in ordered_rooms],
        "live_id": ordered_rooms,
        "streamer_id": [room_streamer[r] for r in ordered_rooms],
    })
    map_df.to_csv(out / "room_item_map.tsv", sep="\t", index=False)

    meta = {
        "dataset": args.dataset,
        "task": "next_live_room",
        "memory_identity": "streamer_relationship_projected_to_active_room",
        "seed": args.seed,
        "n_neg": args.n_neg,
        "candidate_count": args.n_neg + 1,
        "train_rows": len(tr),
        "dev_rows": len(dv),
        "test_rows": len(te),
        "users": len(users),
        "room_universe": len(imap),
        "positive_rooms": len(positive),
        "duplicates_dropped": dup,
        "dev_target_active_rate": dev_target_active / max(len(dev), 1),
        "test_target_active_rate": test_target_active / max(len(test), 1),
        "dev_neg_min": int(dev_len.min()),
        "dev_neg_max": int(dev_len.max()),
        "test_neg_min": int(test_len.min()),
        "test_neg_max": int(test_len.max()),
    }
    (out / "export_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
