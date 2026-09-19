from __future__ import annotations

import argparse
import ast
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_predict

SEED = 20260918
EPS = 1e-12
USER_FEATURES = [
    "log_history_len", "repeat_rate", "preference_entropy",
    "preference_drift", "time_regularity", "state_complexity",
]
CONF_FEATURES = [
    "sas_score_std", "sas_score_range", "sas_margin12", "sas_margin15",
    "sas_margin1011", "sas_top1_z", "sas_entropy", "sas_top10_mass",
]


def parse_list(text, dtype=float):
    s = str(text).strip()
    if s.startswith("[") and s.endswith("]") and "np." not in s:
        a = np.fromstring(s[1:-1], sep=",", dtype=float)
        return a.astype(dtype, copy=False)
    s = re.sub(
        r"np\.(?:float(?:16|32|64)|int(?:8|16|32|64)|uint(?:8|16|32|64))\(([^()]*)\)",
        r"\1", s,
    )
    return np.asarray(ast.literal_eval(s), dtype=dtype)


def ndcg10(rank):
    r = np.asarray(rank, dtype=int)
    out = np.zeros(len(r), dtype=float)
    m = r <= 10
    out[m] = 1.0 / np.log2(r[m] + 1.0)
    return out


def bootstrap_delta(diff, seed=SEED, n_boot=4000):
    x = np.asarray(diff, dtype=float)
    rng = np.random.default_rng(seed)
    n = len(x)
    b = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        b[i] = x[rng.integers(0, n, n)].mean()
    return float(x.mean()), float(np.quantile(b, .025)), float(np.quantile(b, .975))


def load_data(root: Path, n_neg: int):
    train = pd.read_csv(root / "train.csv", sep="\t")
    dev = pd.read_csv(root / "dev.csv", sep="\t")
    test = pd.read_csv(root / "test.csv", sep="\t")
    for name, df in [("train", train), ("dev", dev), ("test", test)]:
        df["user_id"] = df.user_id.astype(int)
        df["item_id"] = df.item_id.astype(int)
        df["time"] = df.time.astype("int64")
        if name != "train":
            if df.user_id.duplicated().any():
                raise ValueError(f"{name} must have one target row per user")
            lens = df.neg_items.map(lambda s: len(parse_list(s, int)))
            if not (lens == n_neg).all():
                raise ValueError(f"{name} negative counts differ from n_neg={n_neg}")
    if set(dev.user_id) != set(test.user_id):
        raise ValueError("dev/test user sets must match for dev-learned gating")
    return train, dev, test


def popularity(train):
    p = np.log1p(train.groupby("item_id").size().astype(float))
    if len(p):
        p = (p - p.min()) / max(float(p.max() - p.min()), EPS)
    return {int(k): float(v) for k, v in p.items()}


def histories(df, short_k=10):
    out = {}
    for uid, g in df.groupby("user_id", sort=False):
        items = g.item_id.astype(int).tolist()
        c = Counter(items)
        maxc = max(c.values()) if c else 1
        long = {i: n / maxc for i, n in c.items()}
        short = {}
        for dist, i in enumerate(reversed(items[-short_k:])):
            short[i] = max(short.get(i, 0.0), math.exp(-dist / 3.0))
        out[int(uid)] = (short, long)
    return out


def memory_scores(cands, uid, pop, hist):
    short, long = hist.get(uid, ({}, {}))
    p = np.fromiter((pop.get(int(i), 0.0) for i in cands), float, count=len(cands))
    s = np.fromiter((short.get(int(i), 0.0) for i in cands), float, count=len(cands))
    l = np.fromiter((long.get(int(i), 0.0) for i in cands), float, count=len(cands))
    return 0.45 * s + 0.45 * l + 0.10 * p


def target_rank(cands, scores):
    target = int(cands[0]); ts = float(scores[0])
    better = int(np.sum(scores > ts + EPS))
    ties = int(np.sum((np.abs(scores - ts) <= EPS) & (cands < target)))
    return 1 + better + ties


def score_memory(phase, history_df, pop, n_neg):
    hist = histories(history_df)
    rows = []
    for r in phase.itertuples(index=False):
        neg = parse_list(r.neg_items, int)
        if len(neg) != n_neg:
            raise ValueError("ragged candidate list")
        cands = np.concatenate(([int(r.item_id)], neg))
        rank = target_rank(cands, memory_scores(cands, int(r.user_id), pop, hist))
        rows.append((int(r.user_id), rank))
    out = pd.DataFrame(rows, columns=["user_id", "memory_rank"])
    out["MemoryFusion_score10"] = ndcg10(out.memory_rank)
    return out


def load_sasrec(rec_path, phase, n_neg):
    pred = pd.read_csv(rec_path, sep="\t")
    target = phase.set_index("user_id").item_id.astype(int).to_dict()
    rows = []
    conf = []
    for r in pred.itertuples(index=False):
        uid = int(r.user_id)
        items = parse_list(r.rec_items, int)
        scores = parse_list(r.rec_predictions, float)
        if len(items) != n_neg + 1 or len(scores) != n_neg + 1:
            raise ValueError(f"user {uid}: expected {n_neg+1} prediction candidates")
        hit = np.flatnonzero(items == int(target[uid]))
        if len(hit) != 1:
            raise ValueError(f"user {uid}: target match count {len(hit)}")
        ts = float(scores[int(hit[0])])
        rank = int(np.sum(scores >= ts))  # match ReChorus BaseRunner
        rows.append((uid, rank))

        ss = np.sort(scores)[::-1]
        mean = float(scores.mean()); std = float(scores.std()); rng = float(scores.max() - scores.min())
        ex = np.exp(np.clip(scores - scores.max(), -60, 0)); prob = ex / ex.sum(); ps = np.sort(prob)[::-1]
        ent = float(-(prob * np.log(np.maximum(prob, EPS))).sum() / math.log(len(prob)))
        conf.append((uid, std, rng, float(ss[0]-ss[1]), float(ss[0]-ss[4]),
                     float(ss[9]-ss[10]), float((ss[0]-mean)/max(std, EPS)), ent, float(ps[:10].sum())))
    a = pd.DataFrame(rows, columns=["user_id", "sasrec_rank"])
    a["sasrec_score10"] = ndcg10(a.sasrec_rank)
    c = pd.DataFrame(conf, columns=["user_id"] + CONF_FEATURES)
    out = a.merge(c, on="user_id", validate="one_to_one")
    if len(out) != len(phase) or out.user_id.duplicated().any():
        raise ValueError("SASRec prediction coverage mismatch")
    return out


def norm_entropy(items):
    c = Counter(items); n = sum(c.values())
    if n <= 1 or len(c) <= 1: return 0.0
    p = np.asarray(list(c.values()), float) / n
    return float(-(p * np.log(p)).sum() / math.log(len(c)))


def js_divergence(a, b):
    ca, cb = Counter(a), Counter(b); keys = sorted(set(ca) | set(cb))
    if not keys: return 0.0
    pa = np.asarray([ca[k] for k in keys], float); pb = np.asarray([cb[k] for k in keys], float)
    pa /= pa.sum(); pb /= pb.sum(); m = .5 * (pa + pb)
    def kl(p, q):
        z = p > 0
        return float((p[z] * np.log2(p[z] / q[z])).sum())
    return .5 * kl(pa, m) + .5 * kl(pb, m)


def circular_regularity(times):
    if not len(times): return 0.0
    hours = pd.to_datetime(pd.Series(times), unit="ms").dt.hour.to_numpy(float)
    a = 2 * np.pi * hours / 24.0
    return float(np.sqrt(np.mean(np.cos(a))**2 + np.mean(np.sin(a))**2))


def user_features(history_df):
    rows = []
    for uid, g in history_df.groupby("user_id", sort=False):
        items = g.item_id.astype(int).tolist(); times = g.time.astype("int64").tolist(); n = len(items)
        recent_n = min(10, max(2, n // 3)) if n >= 3 else max(1, n // 2)
        old = items[:-recent_n] if n > recent_n else items[:max(1, n // 2)]
        recent = items[-recent_n:] if recent_n else items
        uniq = len(set(items))
        rows.append({"user_id": int(uid), "history_len": n, "repeat_rate": 1 - uniq/max(n,1),
                     "preference_entropy": norm_entropy(items),
                     "preference_drift": js_divergence(old, recent) if old and recent else 0.0,
                     "time_regularity": circular_regularity(times)})
    f = pd.DataFrame(rows)
    f["entropy_pct"] = f.preference_entropy.rank(pct=True, method="average")
    f["drift_pct"] = f.preference_drift.rank(pct=True, method="average")
    f["history_pct"] = np.log1p(f.history_len).rank(pct=True, method="average")
    f["state_complexity"] = .4*f.entropy_pct + .4*f.drift_pct + .2*f.history_pct
    f["log_history_len"] = np.log1p(f.history_len.astype(float))
    return f


def choose_threshold(pred, sas, agent):
    qs = np.unique(np.quantile(pred, np.linspace(0, 1, 201)))
    best = None
    for th in np.r_[np.inf, qs, -np.inf]:
        use = pred > th
        score = float(np.where(use, agent, sas).mean())
        key = (score, -float(use.mean()))
        if best is None or key > best[0]: best = (key, float(th), use)
    return best[1], best[2], best[0][0]


def hgb():
    return HistGradientBoostingRegressor(max_iter=200, learning_rate=.05, max_depth=3,
                                         min_samples_leaf=50, l2_regularization=1.0,
                                         random_state=SEED)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--sasrec-dev", type=Path, required=True)
    ap.add_argument("--sasrec-test", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n-neg", type=int, required=True)
    ap.add_argument("--label", default="robustness")
    args = ap.parse_args(); args.out_dir.mkdir(parents=True, exist_ok=True)

    train, dev, test = load_data(args.data_dir, args.n_neg)
    pop = popularity(train)
    train_dev = pd.concat([train, dev[["user_id", "item_id", "time"]]], ignore_index=True)

    mem_dev = score_memory(dev, train, pop, args.n_neg)
    mem_test = score_memory(test, train_dev, pop, args.n_neg)
    sas_dev = load_sasrec(args.sasrec_dev, dev, args.n_neg)
    sas_test = load_sasrec(args.sasrec_test, test, args.n_neg)
    feat_dev = user_features(train)
    feat_test = user_features(train_dev)

    d = sas_dev.merge(mem_dev, on="user_id").merge(feat_dev, on="user_id")
    t = sas_test.merge(mem_test, on="user_id").merge(feat_test, on="user_id")
    d["MemoryFusion_delta"] = d.MemoryFusion_score10 - d.sasrec_score10
    t["MemoryFusion_delta"] = t.MemoryFusion_score10 - t.sasrec_score10

    feats = USER_FEATURES + CONF_FEATURES
    Xd = d[feats].to_numpy(float); Xt = t[feats].to_numpy(float)
    yd = d.MemoryFusion_delta.to_numpy(float)
    sas_d = d.sasrec_score10.to_numpy(float); ag_d = d.MemoryFusion_score10.to_numpy(float)
    sas_t = t.sasrec_score10.to_numpy(float); ag_t = t.MemoryFusion_score10.to_numpy(float)

    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    oof = cross_val_predict(hgb(), Xd, yd, cv=cv, method="predict")
    th, use_d, dev_sel = choose_threshold(oof, sas_d, ag_d)
    model = clone(hgb()).fit(Xd, yd)
    ptest = model.predict(Xt); use_t = ptest > th
    selected = np.where(use_t, ag_t, sas_t)
    delta, lo, hi = bootstrap_delta(selected - sas_t, SEED + 77)

    report = {
        "label": args.label,
        "users": int(len(t)),
        "n_neg": int(args.n_neg),
        "candidate_count": int(args.n_neg + 1),
        "sasrec_dev_ndcg10": float(sas_d.mean()),
        "memory_dev_ndcg10": float(ag_d.mean()),
        "selective_dev_oof_ndcg10": float(dev_sel),
        "sasrec_test_ndcg10": float(sas_t.mean()),
        "memory_test_ndcg10": float(ag_t.mean()),
        "selective_test_ndcg10": float(selected.mean()),
        "selective_absolute_delta": delta,
        "selective_relative_delta": float(delta / max(float(sas_t.mean()), EPS)),
        "ci95_low": lo,
        "ci95_high": hi,
        "dev_gate_rate": float(use_d.mean()),
        "test_gate_rate": float(use_t.mean()),
        "selected_n": int(use_t.sum()),
        "selected_history_mean": float(t.loc[use_t, "history_len"].mean()) if use_t.any() else None,
        "unselected_history_mean": float(t.loc[~use_t, "history_len"].mean()) if (~use_t).any() else None,
        "protocol": "Fixed Selective Agent v2 HGB; 5-fold OOF dev threshold; test evaluation only.",
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    t.assign(primary_pred_delta=ptest, primary_use_agent=use_t).to_csv(
        args.out_dir / "per_user_test.csv.gz", index=False, compression="gzip")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
