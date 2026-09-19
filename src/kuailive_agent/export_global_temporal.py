from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .evaluate import candidate_sets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepared-dir", type=Path, required=True)
    ap.add_argument("--out-root", type=Path, required=True)
    ap.add_argument("--dataset", default="KuaiLiveShopGlobalTemporal")
    ap.add_argument("--train-q", type=float, default=0.80)
    ap.add_argument("--dev-q", type=float, default=0.90)
    ap.add_argument("--max-n-neg", type=int, default=574)
    ap.add_argument("--seed", type=int, default=20260918)
    ap.add_argument("--min-train-events", type=int, default=3)
    a = ap.parse_args()
    if not (0 < a.train_q < a.dev_q < 1):
        raise ValueError("Require 0 < train_q < dev_q < 1")

    events = pd.read_pickle(a.prepared_dir / "events.pkl").sort_values("timestamp", kind="mergesort")
    rooms = pd.read_pickle(a.prepared_dir / "rooms.pkl")
    t1 = int(events.timestamp.quantile(a.train_q, interpolation="nearest"))
    t2 = int(events.timestamp.quantile(a.dev_q, interpolation="nearest"))

    early = events[events.timestamp <= t1].copy()
    devw = events[(events.timestamp > t1) & (events.timestamp <= t2)].copy()
    testw = events[events.timestamp > t2].copy()

    early_ct = early.groupby("user_id").size()
    eligible = set(early_ct[early_ct >= a.min_train_events].index.astype(int))
    eligible &= set(devw.user_id.astype(int))
    eligible &= set(testw.user_id.astype(int))
    if not eligible:
        raise RuntimeError("No users satisfy global temporal landmark eligibility")

    train = early[early.user_id.isin(eligible)].copy()
    dev = (devw[devw.user_id.isin(eligible)]
           .sort_values(["user_id", "timestamp", "live_id"], kind="mergesort")
           .groupby("user_id", as_index=False, sort=False).first())
    test = (testw[testw.user_id.isin(eligible)]
            .sort_values(["user_id", "timestamp", "live_id"], kind="mergesort")
            .groupby("user_id", as_index=False, sort=False).first())

    # Keep identical user sets and enforce chronological landmarks per user.
    common = sorted(set(dev.user_id.astype(int)) & set(test.user_id.astype(int)))
    train = train[train.user_id.isin(common)].copy()
    dev = dev[dev.user_id.isin(common)].copy()
    test = test[test.user_id.isin(common)].copy()
    chk = dev[["user_id", "timestamp"]].merge(test[["user_id", "timestamp"]], on="user_id", suffixes=("_dev", "_test"))
    if not (chk.timestamp_dev < chk.timestamp_test).all():
        raise AssertionError("Temporal ordering violated")

    # De-duplicate exact ReChorus merge keys.
    dup = {}
    cleaned = []
    for name, x in [("train", train), ("dev", dev), ("test", test)]:
        before = len(x)
        x = x.drop_duplicates(["user_id", "streamer_id", "timestamp"], keep="last").copy()
        dup[name] = before - len(x)
        cleaned.append(x)
    train, dev, test = cleaned

    # Probe legal active-at-time candidate counts, then choose one fixed count for all rows.
    probe_n = max(a.max_n_neg, 2000)
    dev_probe = candidate_sets(dev, rooms, probe_n, a.seed)
    test_probe = candidate_sets(test, rooms, probe_n, a.seed)
    dev_min = min(len(v) - 1 for v in dev_probe.values())
    test_min = min(len(v) - 1 for v in test_probe.values())
    fixed_n = int(min(a.max_n_neg, dev_min, test_min))
    if fixed_n < 100:
        raise RuntimeError(f"Too few legal active negatives for robust evaluation: {fixed_n}")
    dev_cs = candidate_sets(dev, rooms, fixed_n, a.seed)
    test_cs = candidate_sets(test, rooms, fixed_n, a.seed)

    users = sorted(set(train.user_id) | set(dev.user_id) | set(test.user_id))
    uidmap = {int(u): i + 1 for i, u in enumerate(users)}
    positive = set(pd.concat([train.streamer_id, dev.streamer_id, test.streamer_id]).astype(int))
    room_items = set(rooms.streamer_id.dropna().astype(int))
    ordered = sorted(room_items - positive) + sorted(positive)
    imap = {s: i + 1 for i, s in enumerate(ordered)}
    assert max(imap[s] for s in positive) == len(imap)

    def base(x):
        return pd.DataFrame({
            "user_id": x.user_id.astype(int).map(uidmap),
            "item_id": x.streamer_id.astype(int).map(imap),
            "time": x.timestamp.astype("int64"),
        })

    tr, dv, te = base(train), base(dev), base(test)

    def negcol(x, csets):
        vals = []
        for idx, r in x.iterrows():
            target = int(r.streamer_id); used = {target}; out = []
            for s in csets[idx][1:]:
                s = int(s)
                if s in imap and s not in used:
                    out.append(imap[s]); used.add(s)
            if len(out) != fixed_n:
                raise ValueError(f"fixed negative export failed: {len(out)} != {fixed_n}")
            vals.append(str(out))
        return vals

    dv["neg_items"] = negcol(dev, dev_cs)
    te["neg_items"] = negcol(test, test_cs)

    out = a.out_root / a.dataset
    out.mkdir(parents=True, exist_ok=True)
    tr.to_csv(out / "train.csv", sep="\t", index=False)
    dv.to_csv(out / "dev.csv", sep="\t", index=False)
    te.to_csv(out / "test.csv", sep="\t", index=False)
    meta = {
        "dataset": a.dataset,
        "seed": a.seed,
        "split": "global_temporal_landmark",
        "train_quantile": a.train_q,
        "dev_quantile": a.dev_q,
        "train_cut_timestamp": t1,
        "dev_cut_timestamp": t2,
        "train_cut_utc": str(pd.to_datetime(t1, unit="ms", utc=True)),
        "dev_cut_utc": str(pd.to_datetime(t2, unit="ms", utc=True)),
        "eligibility": f">={a.min_train_events} train-period events plus >=1 dev-window and >=1 test-window event",
        "target_rule": "first event per eligible user in each future window",
        "history_rule": "dev sees train history; test sees train plus selected dev landmark only; unused within-window events are excluded to prevent leakage",
        "users": len(common),
        "train_rows": len(tr),
        "dev_rows": len(dv),
        "test_rows": len(te),
        "n_neg": fixed_n,
        "candidate_count": fixed_n + 1,
        "probe_dev_min": int(dev_min),
        "probe_test_min": int(test_min),
        "duplicates_dropped": dup,
        "item_universe": len(imap),
    }
    (out / "export_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
