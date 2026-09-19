from __future__ import annotations

import argparse
import ast
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 20260918
N_NEG = 574
EPS = 1e-12
PRIMARY_AGENT = "MemoryFusion"
AGENTS = ["MemoryFusion", "LongMemory", "ShortMemory"]
GATE_FEATURES = [
    "log_history_len",
    "repeat_rate",
    "preference_entropy",
    "preference_drift",
    "time_regularity",
    "state_complexity",
]
EXPECTED_OLD_FUSION_NDCG10 = 0.5240614245440782


def ndcg(rank: int, k: int = 10) -> float:
    return 0.0 if rank > k else 1.0 / math.log2(rank + 1.0)


def parse_list(text: str, dtype=float) -> np.ndarray:
    value = ast.literal_eval(str(text))
    return np.asarray(value, dtype=dtype)


def minmax(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if not len(values):
        return values
    lo, hi = float(values.min()), float(values.max())
    if hi <= lo + EPS:
        return np.zeros_like(values)
    return (values - lo) / (hi - lo)


def load_data(root: Path):
    train = pd.read_csv(root / "train.csv", sep="\t")
    dev = pd.read_csv(root / "dev.csv", sep="\t")
    test = pd.read_csv(root / "test.csv", sep="\t")
    for name, x in [("train", train), ("dev", dev), ("test", test)]:
        x["user_id"] = x.user_id.astype(int)
        x["item_id"] = x.item_id.astype(int)
        x["time"] = x.time.astype("int64")
        if name != "train":
            if x.user_id.duplicated().any():
                raise ValueError(f"Expected one {name} row per user")
            lens = x.neg_items.map(lambda s: len(parse_list(s, int)))
            if not (lens == N_NEG).all():
                raise ValueError(f"{name} candidate lengths are not all {N_NEG}")
    return train, dev, test


def popularity(train: pd.DataFrame) -> dict[int, float]:
    p = np.log1p(train.groupby("item_id").size().astype(float))
    if len(p):
        p = (p - p.min()) / max(float(p.max() - p.min()), EPS)
    return {int(k): float(v) for k, v in p.items()}


def histories(df: pd.DataFrame, short_k: int = 10):
    out = {}
    for uid, g in df.groupby("user_id", sort=False):
        items = g.item_id.astype(int).tolist()
        counts = Counter(items)
        maxc = max(counts.values()) if counts else 1
        long = {iid: c / maxc for iid, c in counts.items()}
        recent = items[-short_k:]
        short = {}
        for dist, iid in enumerate(reversed(recent)):
            short[iid] = max(short.get(iid, 0.0), math.exp(-dist / 3.0))
        out[int(uid)] = (short, long)
    return out


def candidate_vector(row) -> np.ndarray:
    neg = parse_list(row.neg_items, int)
    return np.concatenate(([int(row.item_id)], neg.astype(np.int64)))


def agent_scores(cands: np.ndarray, uid: int, pop: dict[int, float], hist):
    short, long = hist.get(uid, ({}, {}))
    p = np.fromiter((pop.get(int(i), 0.0) for i in cands), dtype=float, count=len(cands))
    s = np.fromiter((short.get(int(i), 0.0) for i in cands), dtype=float, count=len(cands))
    l = np.fromiter((long.get(int(i), 0.0) for i in cands), dtype=float, count=len(cands))
    return {
        "ShortMemory": 0.85 * s + 0.15 * p,
        "LongMemory": 0.75 * l + 0.25 * p,
        "MemoryFusion": 0.45 * s + 0.45 * l + 0.10 * p,
    }


def target_rank(cands: np.ndarray, scores: np.ndarray) -> int:
    target_item, target_score = int(cands[0]), float(scores[0])
    better = int(np.sum(scores > target_score + EPS))
    ties_before = int(np.sum((np.abs(scores - target_score) <= EPS) & (cands < target_item)))
    return 1 + better + ties_before


def score_agents(phase_df: pd.DataFrame, history_df: pd.DataFrame, pop, phase: str, history_mode: str) -> pd.DataFrame:
    hist = histories(history_df)
    rows = []
    for r in phase_df.itertuples(index=False):
        cands = candidate_vector(r)
        score_map = agent_scores(cands, int(r.user_id), pop, hist)
        for model in AGENTS:
            rows.append({
                "user_id": int(r.user_id),
                "phase": phase,
                "history_mode": history_mode,
                "model": model,
                "rank": target_rank(cands, score_map[model]),
                "candidate_count": len(cands),
            })
    return pd.DataFrame(rows)


def load_sasrec_ranks(rec_path: Path, phase_df: pd.DataFrame, phase: str) -> pd.DataFrame:
    pred = pd.read_csv(rec_path, sep="\t")
    target = phase_df.set_index("user_id")["item_id"].astype(int).to_dict()
    rows = []
    for r in pred.itertuples(index=False):
        uid = int(r.user_id)
        items = parse_list(r.rec_items, int)
        scores = parse_list(r.rec_predictions, float)
        if len(items) != N_NEG + 1 or len(scores) != N_NEG + 1:
            raise ValueError(f"{phase}: user {uid} does not have full {N_NEG+1}-candidate export")
        tgt = int(target[uid])
        hit = np.flatnonzero(items == tgt)
        if len(hit) != 1:
            raise ValueError(f"{phase}: target {tgt} appears {len(hit)} times for user {uid}")
        target_score = float(scores[int(hit[0])])
        # Match ReChorus BaseRunner exactly: gt_rank = count(prediction >= target prediction).
        rank = int(np.sum(scores >= target_score))
        rows.append({"user_id": uid, "sasrec_rank": rank, "sasrec_candidate_count": len(items)})
    out = pd.DataFrame(rows)
    if out.user_id.duplicated().any() or len(out) != len(phase_df):
        raise ValueError(f"SASRec {phase} user coverage mismatch: {len(out)} vs {len(phase_df)}")
    return out


def norm_entropy(items) -> float:
    c = Counter(items); n = sum(c.values())
    if n <= 1 or len(c) <= 1:
        return 0.0
    p = np.asarray(list(c.values()), dtype=float) / n
    return float(-(p * np.log(p)).sum() / math.log(len(c)))


def js_divergence(a, b) -> float:
    ca, cb = Counter(a), Counter(b); keys = sorted(set(ca) | set(cb))
    if not keys:
        return 0.0
    pa = np.asarray([ca[k] for k in keys], float); pb = np.asarray([cb[k] for k in keys], float)
    pa /= max(pa.sum(), 1); pb /= max(pb.sum(), 1); m = 0.5 * (pa + pb)
    def kl(p, q):
        z = p > 0
        return float((p[z] * np.log2(p[z] / q[z])).sum())
    return 0.5 * kl(pa, m) + 0.5 * kl(pb, m)


def circular_regularity(times) -> float:
    if not len(times):
        return 0.0
    hours = pd.to_datetime(pd.Series(times), unit="ms").dt.hour.to_numpy(float)
    ang = 2 * np.pi * hours / 24.0
    return float(np.sqrt(np.mean(np.cos(ang)) ** 2 + np.mean(np.sin(ang)) ** 2))


def user_features(history_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for uid, g in history_df.groupby("user_id", sort=False):
        items = g.item_id.astype(int).tolist(); times = g.time.astype("int64").tolist(); n = len(items)
        recent_n = min(10, max(2, n // 3)) if n >= 3 else max(1, n // 2)
        old = items[:-recent_n] if n > recent_n else items[:max(1, n // 2)]
        recent = items[-recent_n:] if recent_n else items
        uniq = len(set(items))
        rows.append({
            "user_id": int(uid),
            "history_len": n,
            "unique_items": uniq,
            "repeat_rate": 1 - uniq / max(n, 1),
            "preference_entropy": norm_entropy(items),
            "preference_drift": js_divergence(old, recent) if old and recent else 0.0,
            "time_regularity": circular_regularity(times),
        })
    f = pd.DataFrame(rows)
    f["entropy_pct"] = f.preference_entropy.rank(pct=True, method="average")
    f["drift_pct"] = f.preference_drift.rank(pct=True, method="average")
    f["history_pct"] = np.log1p(f.history_len).rank(pct=True, method="average")
    f["state_complexity"] = 0.4 * f.entropy_pct + 0.4 * f.drift_pct + 0.2 * f.history_pct
    f["log_history_len"] = np.log1p(f.history_len.astype(float))
    return f


def metrics(rank: pd.Series) -> dict:
    r = rank.astype(int)
    return {
        "users": int(len(r)),
        "hr@5": float((r <= 5).mean()),
        "hr@10": float((r <= 10).mean()),
        "hr@20": float((r <= 20).mean()),
        "ndcg@5": float(r.map(lambda x: ndcg(int(x), 5)).mean()),
        "ndcg@10": float(r.map(lambda x: ndcg(int(x), 10)).mean()),
        "ndcg@20": float(r.map(lambda x: ndcg(int(x), 20)).mean()),
        "mrr": float((1.0 / r).mean()),
    }


def bootstrap_mean(x, seed=SEED, n_boot=2000):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    rng = np.random.default_rng(seed); n = len(x)
    boots = np.asarray([x[rng.integers(0, n, n)].mean() for _ in range(n_boot)])
    return float(x.mean()), float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))


def phase_table(sas: pd.DataFrame, agents: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    a = agents.pivot(index="user_id", columns="model", values="rank").reset_index()
    z = sas.merge(a, on="user_id", how="inner").merge(features, on="user_id", how="inner")
    z["sasrec_score10"] = z.sasrec_rank.map(lambda r: ndcg(int(r), 10))
    for model in AGENTS:
        z[f"{model}_score10"] = z[model].map(lambda r: ndcg(int(r), 10))
        z[f"{model}_delta"] = z[f"{model}_score10"] - z.sasrec_score10
    return z


def summarize(sas_dev, sas_test, agent_frames) -> pd.DataFrame:
    rows = []
    for phase, sas in [("dev", sas_dev), ("test", sas_test)]:
        row = {"phase": phase, "history_mode": "ReChorus sequential", "model": "SASRec"}
        row.update(metrics(sas.sasrec_rank)); rows.append(row)
    all_agents = pd.concat(agent_frames, ignore_index=True)
    for (phase, hm, model), g in all_agents.groupby(["phase", "history_mode", "model"]):
        row = {"phase": phase, "history_mode": hm, "model": model}
        row.update(metrics(g["rank"])); rows.append(row)
    return pd.DataFrame(rows).sort_values(["phase", "history_mode", "ndcg@10"], ascending=[True, True, False])


def residual_stability(dev: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model in AGENTS:
        d = dev[["user_id", f"{model}_delta"]].rename(columns={f"{model}_delta": "dev_delta"})
        t = test[["user_id", f"{model}_delta"]].rename(columns={f"{model}_delta": "test_delta"})
        z = d.merge(t, on="user_id")
        rows.append({
            "model": model,
            "users": len(z),
            "dev_mean_delta": z.dev_delta.mean(),
            "test_mean_delta": z.test_delta.mean(),
            "dev_agent_win_rate": (z.dev_delta > 0).mean(),
            "test_agent_win_rate": (z.test_delta > 0).mean(),
            "pearson_dev_test": z.dev_delta.corr(z.test_delta, method="pearson"),
            "spearman_dev_test": z.dev_delta.corr(z.test_delta, method="spearman"),
            "sign_agreement": (np.sign(z.dev_delta) == np.sign(z.test_delta)).mean(),
        })
    return pd.DataFrame(rows)


def residual_quartiles(test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    features = ["history_len", "repeat_rate", "preference_entropy", "preference_drift", "time_regularity", "state_complexity"]
    delta_col = f"{PRIMARY_AGENT}_delta"
    for feat in features:
        tmp = test[["user_id", feat, delta_col]].dropna().copy()
        try:
            tmp["quartile"] = pd.qcut(tmp[feat], 4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
        except ValueError:
            continue
        for qi, (q, g) in enumerate(tmp.groupby("quartile", observed=True)):
            mean, lo, hi = bootstrap_mean(g[delta_col], seed=SEED + qi, n_boot=1000)
            rows.append({
                "model": PRIMARY_AGENT,
                "feature": feat,
                "quartile": str(q),
                "n": len(g),
                "feature_mean": g[feat].mean(),
                "delta_ndcg10": mean,
                "ci95_low": lo,
                "ci95_high": hi,
                "agent_win_rate": (g[delta_col] > 0).mean(),
                "tie_rate": (g[delta_col] == 0).mean(),
                "sasrec_win_rate": (g[delta_col] < 0).mean(),
            })
    return pd.DataFrame(rows)


def choose_threshold(predicted_delta, sas_score, agent_score):
    qs = np.quantile(predicted_delta, np.linspace(0, 1, 101))
    thresholds = np.unique(np.r_[np.inf, qs, -np.inf])
    best = None
    for th in thresholds:
        use_agent = predicted_delta > th
        score = float(np.where(use_agent, agent_score, sas_score).mean())
        candidate = (score, -float(use_agent.mean()))
        if best is None or candidate > best[0]:
            best = (candidate, float(th), use_agent)
    return best[1], best[2]


def feature_gate(dev: pd.DataFrame, test: pd.DataFrame) -> dict:
    model = PRIMARY_AGENT
    xdev = dev[GATE_FEATURES].astype(float).to_numpy()
    xtest = test[GATE_FEATURES].astype(float).to_numpy()
    ydev = dev[f"{model}_delta"].to_numpy(float)
    sas_dev = dev.sasrec_score10.to_numpy(float); ag_dev = dev[f"{model}_score10"].to_numpy(float)
    sas_test = test.sasrec_score10.to_numpy(float); ag_test = test[f"{model}_score10"].to_numpy(float)

    pipe = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    oof = cross_val_predict(pipe, xdev, ydev, cv=cv, method="predict")
    threshold, use_agent_oof = choose_threshold(oof, sas_dev, ag_dev)
    oof_selective = np.where(use_agent_oof, ag_dev, sas_dev)

    pipe.fit(xdev, ydev)
    ptest = pipe.predict(xtest)
    use_agent_test = ptest > threshold
    test_selective = np.where(use_agent_test, ag_test, sas_test)
    delta, lo, hi = bootstrap_mean(test_selective - sas_test, seed=SEED + 77, n_boot=2000)
    oracle = np.maximum(ag_test, sas_test)
    return {
        "gate": "feature_ridge_5fold_oof_threshold",
        "agent": model,
        "threshold": threshold,
        "dev_oof_gate_rate": float(use_agent_oof.mean()),
        "dev_sasrec_ndcg10": float(sas_dev.mean()),
        "dev_agent_ndcg10": float(ag_dev.mean()),
        "dev_oof_selective_ndcg10": float(oof_selective.mean()),
        "test_gate_rate": float(use_agent_test.mean()),
        "test_sasrec_ndcg10": float(sas_test.mean()),
        "test_agent_ndcg10": float(ag_test.mean()),
        "test_selective_ndcg10": float(test_selective.mean()),
        "test_selective_delta": delta,
        "test_selective_ci95_low": lo,
        "test_selective_ci95_high": hi,
        "test_oracle_ndcg10": float(oracle.mean()),
        "test_oracle_delta": float((oracle - sas_test).mean()),
    }


def prior_outcome_gate(dev: pd.DataFrame, test: pd.DataFrame) -> dict:
    model = PRIMARY_AGENT
    d = dev[["user_id", f"{model}_delta"]].copy()
    z = test.merge(d, on="user_id", suffixes=("", "_dev"))
    use_agent = z[f"{model}_delta_dev"].to_numpy(float) > 0
    sas = z.sasrec_score10.to_numpy(float); agent = z[f"{model}_score10"].to_numpy(float)
    selective = np.where(use_agent, agent, sas)
    delta, lo, hi = bootstrap_mean(selective - sas, seed=SEED + 88, n_boot=2000)
    return {
        "gate": "previous_dev_winner",
        "agent": model,
        "test_gate_rate": float(use_agent.mean()),
        "test_sasrec_ndcg10": float(sas.mean()),
        "test_agent_ndcg10": float(agent.mean()),
        "test_selective_ndcg10": float(selective.mean()),
        "test_selective_delta": delta,
        "test_selective_ci95_low": lo,
        "test_selective_ci95_high": hi,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rechorus-dir", type=Path, required=True)
    ap.add_argument("--sasrec-dev", type=Path, required=True)
    ap.add_argument("--sasrec-test", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args(); args.out_dir.mkdir(parents=True, exist_ok=True)

    train, dev, test = load_data(args.rechorus_dir)
    pop = popularity(train)
    train_dev = pd.concat([train, dev[["user_id", "item_id", "time"]]], ignore_index=True)

    sas_dev = load_sasrec_ranks(args.sasrec_dev, dev, "dev")
    sas_test = load_sasrec_ranks(args.sasrec_test, test, "test")
    agent_dev = score_agents(dev, train, pop, "dev", "train")
    agent_test_fair = score_agents(test, train_dev, pop, "test", "train+dev")
    agent_test_old = score_agents(test, train, pop, "test", "train_only_audit")

    feat_dev = user_features(train)
    feat_test = user_features(train_dev)
    dev_table = phase_table(sas_dev, agent_dev, feat_dev)
    test_table = phase_table(sas_test, agent_test_fair, feat_test)

    summary = summarize(sas_dev, sas_test, [agent_dev, agent_test_fair, agent_test_old])
    old_p = agent_test_old.pivot(index="user_id", columns="model", values="rank")
    new_p = agent_test_fair.pivot(index="user_id", columns="model", values="rank")
    audit_rows = []
    for model in AGENTS:
        old_s = old_p[model].map(lambda r: ndcg(int(r), 10)).to_numpy(float)
        new_s = new_p[model].map(lambda r: ndcg(int(r), 10)).to_numpy(float)
        delta, lo, hi = bootstrap_mean(new_s - old_s, seed=SEED + 123, n_boot=2000)
        audit_rows.append({
            "model": model,
            "train_only_ndcg10": float(old_s.mean()),
            "train_plus_dev_ndcg10": float(new_s.mean()),
            "history_update_delta": delta,
            "ci95_low": lo,
            "ci95_high": hi,
        })
    audit = pd.DataFrame(audit_rows)
    old_fusion = float(audit.loc[audit.model == PRIMARY_AGENT, "train_only_ndcg10"].iloc[0])
    if abs(old_fusion - EXPECTED_OLD_FUSION_NDCG10) > 1e-10:
        raise AssertionError(f"Frozen-artifact reproduction failed: {old_fusion} != {EXPECTED_OLD_FUSION_NDCG10}")

    stability = residual_stability(dev_table, test_table)
    quartiles = residual_quartiles(test_table)
    gates = pd.DataFrame([feature_gate(dev_table, test_table), prior_outcome_gate(dev_table, test_table)])

    summary.to_csv(args.out_dir / "metric_summary.csv", index=False)
    audit.to_csv(args.out_dir / "history_fairness_audit.csv", index=False)
    stability.to_csv(args.out_dir / "residual_stability.csv", index=False)
    quartiles.to_csv(args.out_dir / "residual_quartiles.csv", index=False)
    gates.to_csv(args.out_dir / "selective_gate.csv", index=False)
    dev_table.to_csv(args.out_dir / "per_user_dev.csv.gz", index=False, compression="gzip")
    test_table.to_csv(args.out_dir / "per_user_test.csv.gz", index=False, compression="gzip")

    fair_fusion = float(audit.loc[audit.model == PRIMARY_AGENT, "train_plus_dev_ndcg10"].iloc[0])
    sas_test_ndcg = float(test_table.sasrec_score10.mean())
    report = {
        "seed": SEED,
        "n_neg": N_NEG,
        "candidate_count": N_NEG + 1,
        "users": int(len(test_table)),
        "primary_agent": PRIMARY_AGENT,
        "frozen_artifact_reproduction": old_fusion,
        "fair_history_agent_ndcg10": fair_fusion,
        "sasrec_ndcg10_from_full_predictions": sas_test_ndcg,
        "fair_gap_sasrec_minus_agent": sas_test_ndcg - fair_fusion,
        "method_note": "Dev Agent uses train history; test Agent uses train+dev history, matching information available to ReChorus sequential test input. Popularity remains train-only. Feature gate threshold is selected from 5-fold OOF dev predictions and evaluated once on test.",
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")

    print("\n=== Metric summary ===\n", summary.to_string(index=False))
    print("\n=== History fairness audit ===\n", audit.to_string(index=False))
    print("\n=== Residual stability ===\n", stability.to_string(index=False))
    print("\n=== Selective gates ===\n", gates.to_string(index=False))
    print("\n=== Report ===\n", json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
