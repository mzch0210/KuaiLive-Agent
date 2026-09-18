from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

EPS = 1e-12


class IndexedCounterSet:
    """Dynamic set with multiplicity and O(1) add/remove plus O(k) random sampling."""
    def __init__(self):
        self.items: list[int] = []
        self.index: dict[int, int] = {}
        self.count: Counter[int] = Counter()

    def add(self, x: int):
        self.count[x] += 1
        if self.count[x] == 1:
            self.index[x] = len(self.items)
            self.items.append(x)

    def remove(self, x: int):
        if self.count[x] <= 0:
            return
        self.count[x] -= 1
        if self.count[x] == 0:
            del self.count[x]
            idx = self.index.pop(x)
            last = self.items.pop()
            if idx < len(self.items):
                self.items[idx] = last
                self.index[last] = idx

    def sample(self, n: int, rng: np.random.Generator, exclude: int | None = None) -> np.ndarray:
        m = len(self.items)
        if m == 0:
            return np.empty(0, dtype=np.int64)
        if exclude is None or exclude not in self.index:
            if m <= n:
                return np.asarray(self.items, dtype=np.int64)
            idx = rng.choice(m, size=n, replace=False)
            return np.asarray([self.items[int(i)] for i in idx], dtype=np.int64)
        if m - 1 <= n:
            return np.asarray([x for x in self.items if x != exclude], dtype=np.int64)
        idx = rng.choice(m, size=min(m, n + 1), replace=False)
        vals = [self.items[int(i)] for i in idx if self.items[int(i)] != exclude]
        if len(vals) < n:
            chosen = set(vals)
            chosen.add(exclude)
            for x in self.items:
                if x not in chosen:
                    vals.append(x)
                    if len(vals) == n:
                        break
        return np.asarray(vals[:n], dtype=np.int64)


def ndcg(rank: int, k: int) -> float:
    return 0.0 if rank > k else 1.0 / math.log2(rank + 1.0)


def minmax(values: np.ndarray) -> np.ndarray:
    if values.size == 0:
        return values.astype(float)
    lo, hi = float(np.min(values)), float(np.max(values))
    if hi <= lo + EPS:
        return np.zeros_like(values, dtype=float)
    return (values.astype(float) - lo) / (hi - lo)


def split_events(events: pd.DataFrame, min_user_events: int = 3):
    events = events.sort_values(["user_id", "timestamp", "live_id"], kind="mergesort").reset_index(drop=True)
    size = events.groupby("user_id")["user_id"].transform("size")
    pos = events.groupby("user_id").cumcount()
    from_end = size - pos - 1
    eligible = size >= min_user_events
    train = events.loc[eligible & (from_end >= 2)].copy()
    val = events.loc[eligible & (from_end == 1)].copy()
    test = events.loc[eligible & (from_end == 0)].copy()
    return train, val, test


def build_global_stats(train: pd.DataFrame):
    pop = train.groupby("streamer_id").size().astype(float)
    pop = np.log1p(pop)
    if len(pop):
        pop = (pop - pop.min()) / max(float(pop.max() - pop.min()), EPS)
    engagement = train.groupby("streamer_id")["watch_live_time"].mean().astype(float)
    engagement = np.log1p(np.maximum(engagement, 0))
    if len(engagement):
        engagement = (engagement - engagement.min()) / max(float(engagement.max() - engagement.min()), EPS)
    hours = pd.to_datetime(train["timestamp"], unit="ms", errors="coerce").dt.hour.fillna(0).astype(int)
    hour_df = pd.DataFrame({"streamer_id": train["streamer_id"].to_numpy(), "hour": hours.to_numpy()})
    hour_ct = hour_df.groupby(["streamer_id", "hour"]).size()
    return pop.to_dict(), engagement.to_dict(), hour_ct.to_dict()


def make_user_histories(train: pd.DataFrame, short_k: int = 10):
    histories = {}
    for uid, g in train.groupby("user_id", sort=False):
        sids = g["streamer_id"].astype(int).tolist()
        counts = Counter(sids)
        maxc = max(counts.values()) if counts else 1
        long = {sid: c / maxc for sid, c in counts.items()}
        recent = sids[-short_k:]
        short = {}
        for dist, sid in enumerate(reversed(recent)):
            short[sid] = max(short.get(sid, 0.0), math.exp(-dist / 3.0))
        fat_ct = Counter(recent)
        fatigue = {sid: c / max(1, short_k) for sid, c in fat_ct.items()}
        histories[int(uid)] = (short, long, fatigue)
    return histories


def candidate_sets(test: pd.DataFrame, rooms: pd.DataFrame, n_neg: int, seed: int):
    starts = rooms[["start_timestamp", "end_timestamp", "streamer_id"]].dropna().copy()
    starts[["start_timestamp", "end_timestamp", "streamer_id"]] = starts[["start_timestamp", "end_timestamp", "streamer_id"]].astype("int64")
    starts = starts.sort_values("start_timestamp")
    ends = starts.sort_values("end_timestamp")
    s_start = starts["start_timestamp"].to_numpy()
    s_sid = starts["streamer_id"].to_numpy()
    e_end = ends["end_timestamp"].to_numpy()
    e_sid = ends["streamer_id"].to_numpy()
    ordered = test.reset_index().sort_values("timestamp")
    active = IndexedCounterSet()
    i = j = 0
    rng = np.random.default_rng(seed)
    out = {}
    for r in ordered.itertuples(index=False):
        t = int(r.timestamp)
        while i < len(s_start) and int(s_start[i]) <= t:
            active.add(int(s_sid[i])); i += 1
        while j < len(e_end) and int(e_end[j]) < t:
            active.remove(int(e_sid[j])); j += 1
        target = int(r.streamer_id)
        neg = active.sample(n_neg, rng, exclude=target)
        out[int(r.index)] = np.concatenate(([target], neg))
    return out


def score_candidates(cands: np.ndarray, uid: int, timestamp: int, pop, engagement, hour_ct, histories):
    short, long, fatigue = histories.get(uid, ({}, {}, {}))
    p = np.fromiter((pop.get(int(s), 0.0) for s in cands), dtype=float, count=len(cands))
    e = np.fromiter((engagement.get(int(s), 0.0) for s in cands), dtype=float, count=len(cands))
    s = np.fromiter((short.get(int(x), 0.0) for x in cands), dtype=float, count=len(cands))
    l = np.fromiter((long.get(int(x), 0.0) for x in cands), dtype=float, count=len(cands))
    f = np.fromiter((fatigue.get(int(x), 0.0) for x in cands), dtype=float, count=len(cands))
    hour = int(pd.to_datetime(timestamp, unit="ms").hour)
    t = np.fromiter((hour_ct.get((int(x), hour), 0.0) for x in cands), dtype=float, count=len(cands))
    t = minmax(np.log1p(t))
    return {
        "Popularity": p,
        "ShortMemory": 0.85*s + 0.15*p,
        "LongMemory": 0.75*l + 0.25*p,
        "MemoryFusion": 0.45*s + 0.45*l + 0.10*p,
        "MemoryPlanner": 0.30*s + 0.35*l + 0.15*e + 0.10*t + 0.10*p - 0.08*f,
        "Planner-NoShort": 0.55*l + 0.15*e + 0.10*t + 0.20*p - 0.08*f,
        "Planner-NoLong": 0.50*s + 0.15*e + 0.15*t + 0.20*p - 0.08*f,
        "Planner-NoTime": 0.33*s + 0.38*l + 0.16*e + 0.13*p - 0.08*f,
        "Planner-NoFatigue": 0.30*s + 0.35*l + 0.15*e + 0.10*t + 0.10*p,
    }


def target_rank(cands: np.ndarray, scores: np.ndarray) -> int:
    target_sid, target_score = int(cands[0]), float(scores[0])
    better = int(np.sum(scores > target_score + EPS))
    ties_before = int(np.sum((np.abs(scores - target_score) <= EPS) & (cands < target_sid)))
    return 1 + better + ties_before


def summarize(raw: pd.DataFrame, seed: int):
    rows = []
    for model, g in raw.groupby("model"):
        row = {
            "seed": seed,
            "model": model,
            "users": g["user_id"].nunique(),
            "recall@5": (g["rank"] <= 5).mean(),
            "recall@10": (g["rank"] <= 10).mean(),
            "recall@20": (g["rank"] <= 20).mean(),
            "ndcg@5": g["rank"].map(lambda r: ndcg(int(r), 5)).mean(),
            "ndcg@10": g["rank"].map(lambda r: ndcg(int(r), 10)).mean(),
            "ndcg@20": g["rank"].map(lambda r: ndcg(int(r), 20)).mean(),
            "mrr": (1.0 / g["rank"]).mean(),
            "mean_candidates": g["candidate_count"].mean(),
        }
        lv = g[g["long_view"]]
        row["longview_users"] = lv["user_id"].nunique()
        row["longview_recall@10"] = (lv["rank"] <= 10).mean() if len(lv) else np.nan
        row["longview_ndcg@10"] = lv["rank"].map(lambda r: ndcg(int(r), 10)).mean() if len(lv) else np.nan
        rows.append(row)
    return pd.DataFrame(rows).sort_values("ndcg@10", ascending=False)


def bootstrap_delta(raw: pd.DataFrame, challenger="MemoryPlanner", baseline="LongMemory", metric_k=10, n_boot=1000, seed=20260918):
    pivot = raw[raw["model"].isin([challenger, baseline])].copy()
    pivot["metric"] = pivot["rank"].map(lambda r: ndcg(int(r), metric_k))
    p = pivot.pivot(index="user_id", columns="model", values="metric").dropna()
    if challenger not in p or baseline not in p or p.empty:
        return None
    delta = (p[challenger] - p[baseline]).to_numpy()
    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot)
    n = len(delta)
    for i in range(n_boot):
        boots[i] = delta[rng.integers(0, n, n)].mean()
    return {
        "challenger": challenger,
        "baseline": baseline,
        "metric": f"ndcg@{metric_k}",
        "n_users": n,
        "mean_delta": float(delta.mean()),
        "ci95_low": float(np.quantile(boots, 0.025)),
        "ci95_high": float(np.quantile(boots, 0.975)),
    }


def evaluate(prepared_dir: Path, out_dir: Path, n_neg: int, seed: int, min_user_events: int = 3):
    events = pd.read_pickle(prepared_dir / "events.pkl")
    rooms = pd.read_pickle(prepared_dir / "rooms.pkl")
    train, val, test = split_events(events, min_user_events=min_user_events)
    print(f"train={len(train):,} val={len(val):,} test={len(test):,} users={test.user_id.nunique():,}")
    pop, engagement, hour_ct = build_global_stats(train)
    histories = make_user_histories(train)
    csets = candidate_sets(test, rooms, n_neg=n_neg, seed=seed)

    rows = []
    for idx, r in test.iterrows():
        cands = csets[idx]
        score_map = score_candidates(cands, int(r.user_id), int(r.timestamp), pop, engagement, hour_ct, histories)
        for model, scores in score_map.items():
            rows.append({
                "user_id": int(r.user_id),
                "model": model,
                "rank": target_rank(cands, scores),
                "candidate_count": len(cands),
                "long_view": bool(int(r.watch_live_time) >= 30_000),
            })
    raw = pd.DataFrame(rows)
    summary = summarize(raw, seed)
    delta = bootstrap_delta(raw, seed=seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw.to_csv(out_dir / f"per_user_seed{seed}.csv.gz", index=False, compression="gzip")
    summary.to_csv(out_dir / f"summary_seed{seed}.csv", index=False)
    if delta:
        (out_dir / f"bootstrap_seed{seed}.json").write_text(json.dumps(delta, indent=2) + "\n")
    print(summary.to_string(index=False))
    print("bootstrap:", delta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepared-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n-neg", type=int, default=999)
    ap.add_argument("--seed", type=int, default=20260918)
    ap.add_argument("--min-user-events", type=int, default=3)
    args = ap.parse_args()
    evaluate(args.prepared_dir, args.out_dir, args.n_neg, args.seed, args.min_user_events)


if __name__ == "__main__":
    main()
