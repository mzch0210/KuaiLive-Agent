from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


def official_target_rows(df: pd.DataFrame, p1: int, p2: int, seq_len: int):
    eligible = df[df.stop < p2].copy()
    out = []
    for uid, g in eligible.groupby("user", sort=False):
        g = g.sort_values("start", kind="mergesort").tail(seq_len + 1)
        if len(g) < 2:
            continue
        target = g.tail(1).iloc[0]
        yt = int(target.start)
        if yt < p1 or yt >= p2:
            continue
        hist = g.iloc[:-1]
        out.append({
            "user": int(uid),
            "target_streamer": int(target.streamer),
            "target_start": yt,
            "target_stop": int(target.stop),
            "history_len": int(len(hist)),
            "target_repeated_in_seq": bool(int(target.streamer) in set(hist.streamer.astype(int))),
        })
    return pd.DataFrame(out)


def availability_counts(df: pd.DataFrame, target_steps: set[int], max_step: int):
    starts = defaultdict(list)
    stops = defaultdict(list)
    # Arrays of integer ids keep the sweep compact enough for the 100k benchmark.
    for s, e, sid in zip(df.start.astype(int), df.stop.astype(int), df.streamer.astype(int)):
        starts[int(s)].append(int(sid))
        stops[int(e)].append(int(sid))

    active_counts = Counter()
    active_unique = 0
    out = {}
    for step in range(max_step + 1):
        # Official availability is start <= step and stop > step.
        for sid in stops.get(step, ()):
            prev = active_counts[sid]
            if prev <= 0:
                raise ValueError("availability counter underflow")
            if prev == 1:
                del active_counts[sid]
                active_unique -= 1
            else:
                active_counts[sid] = prev - 1
        for sid in starts.get(step, ()):
            prev = active_counts.get(sid, 0)
            if prev == 0:
                active_unique += 1
            active_counts[sid] = prev + 1
        if step in target_steps:
            out[step] = {
                "candidate_count": int(active_unique),
                "active_streamers": set(active_counts.keys()),
            }
    return out


def summarize_targets(name: str, targets: pd.DataFrame, availability: dict):
    if targets.empty:
        return {"split": name, "n": 0}
    counts = np.asarray([availability[int(t)].get("candidate_count", 0) for t in targets.target_start], float)
    target_active = np.asarray([
        int(sid) in availability[int(t)]["active_streamers"]
        for sid, t in zip(targets.target_streamer, targets.target_start)
    ], bool)
    return {
        "split": name,
        "n": int(len(targets)),
        "unique_users": int(targets.user.nunique()),
        "repeat_target_fraction": float(targets.target_repeated_in_seq.mean()),
        "history_len_mean": float(targets.history_len.mean()),
        "history_len_median": float(targets.history_len.median()),
        "target_active_rate": float(target_active.mean()),
        "candidate_count": {
            "mean": float(counts.mean()),
            "median": float(np.median(counts)),
            "p10": float(np.quantile(counts, .10)),
            "p90": float(np.quantile(counts, .90)),
            "p95": float(np.quantile(counts, .95)),
            "min": int(counts.min()),
            "max": int(counts.max()),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--seq-len", type=int, default=16)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    cols = ["user_raw", "stream_raw", "streamer_raw", "start", "stop"]
    df = pd.read_csv(args.csv, header=None, names=cols)
    # Match official factorization order (+1 for padding).
    df["user"] = pd.factorize(df.user_raw)[0].astype(np.int64) + 1
    df["streamer"] = pd.factorize(df.streamer_raw)[0].astype(np.int64) + 1
    df["start"] = df.start.astype(np.int64)
    df["stop"] = df.stop.astype(np.int64)

    max_step = int(max(df.start.max(), df.stop.max()))
    pivot_1 = max_step - 500
    pivot_2 = max_step - 250

    train = official_target_rows(df, 0, pivot_1, args.seq_len)
    dev = official_target_rows(df, pivot_1, pivot_2, args.seq_len)
    test = official_target_rows(df, pivot_2, max_step, args.seq_len)

    target_steps = set(train.target_start.astype(int)) | set(dev.target_start.astype(int)) | set(test.target_start.astype(int))
    availability = availability_counts(df, target_steps, max_step)

    train.to_csv(args.out_dir / "official_train_targets.csv.gz", index=False, compression="gzip")
    dev.to_csv(args.out_dir / "official_dev_targets.csv.gz", index=False, compression="gzip")
    test.to_csv(args.out_dir / "official_test_targets.csv.gz", index=False, compression="gzip")

    report = {
        "experiment": "liverec_twitch100k_p1_data_audit",
        "source_file": args.csv.name,
        "rows": int(len(df)),
        "users": int(df.user.nunique()),
        "streamers": int(df.streamer.nunique()),
        "max_step": max_step,
        "official_pivot_1": pivot_1,
        "official_pivot_2": pivot_2,
        "official_seq_len": int(args.seq_len),
        "official_availability": "streamer is candidate at step s iff at least one row satisfies start <= s < stop",
        "splits": {
            "train": summarize_targets("train", train, availability),
            "dev": summarize_targets("dev", dev, availability),
            "test": summarize_targets("test", test, availability),
        },
        "guardrail": "This audit reproduces official split/availability semantics before any P1 test-model selection. It does not inspect recommender predictions or tune on test.",
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
