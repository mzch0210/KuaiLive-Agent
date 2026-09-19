from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from kuailive_agent.evaluate import (
    build_global_stats,
    candidate_sets,
    make_user_histories,
    ndcg,
    score_candidates,
    split_events,
    target_rank,
)
from kuailive_agent.heterogeneity import bootstrap_mean, user_features

SEED = 20260918
N_NEG = 574
GATE_FEATURES = [
    "log_history_len",
    "repeat_rate",
    "preference_entropy",
    "preference_drift",
    "time_regularity",
    "state_complexity",
]
AGENTS = ["MemoryFusion", "MemoryPlanner", "LongMemory"]


def _parse_ranked_items(text: str) -> np.ndarray:
    text = str(text).strip()
    if not text or text == "[]":
        return np.empty(0, dtype=np.int64)
    text = text.replace("np.int64(", "").replace(")", "")
    body = text[1:-1] if text.startswith("[") and text.endswith("]") else text
    return np.fromstring(body, sep=",", dtype=np.int64)


def load_sasrec_ranks(rec_path: Path, phase_path: Path, uid_to_original: dict[int, int], phase: str) -> pd.DataFrame:
    pred = pd.read_csv(rec_path, sep="\t")
    phase_df = pd.read_csv(phase_path, sep="\t", usecols=["user_id", "item_id"])
    target = phase_df.set_index("user_id")["item_id"].astype(int).to_dict()
    if phase_df["user_id"].duplicated().any():
        raise ValueError(f"Expected one {phase} row per ReChorus user")
    rows = []
    for r in pred.itertuples(index=False):
        uid = int(r.user_id)
        ranked = _parse_ranked_items(r.rec_items)
        tgt = int(target[uid])
        hit = np.flatnonzero(ranked == tgt)
        if len(hit) != 1:
            raise ValueError(f"{phase}: target item {tgt} appears {len(hit)} times for user {uid}")
        rows.append({
            "user_id": int(uid_to_original[uid]),
            "sasrec_rank": int(hit[0]) + 1,
            "sasrec_candidate_count": int(len(ranked)),
        })
    out = pd.DataFrame(rows)
    if out.user_id.duplicated().any():
        raise ValueError(f"Duplicate original users in SASRec {phase} predictions")
    if len(out) == 0 or out.sasrec_candidate_count.min() != N_NEG + 1 or out.sasrec_candidate_count.max() != N_NEG + 1:
        raise ValueError(
            f"Expected full {N_NEG+1}-candidate rankings for {phase}; got "
            f"min={out.sasrec_candidate_count.min() if len(out) else 'NA'} "
            f"max={out.sasrec_candidate_count.max() if len(out) else 'NA'}"
        )
    return out


def score_agent_phase(phase_df, rooms, history_df, global_train, phase: str, history_mode: str) -> pd.DataFrame:
    pop, engagement, hour_ct = build_global_stats(global_train)
    histories = make_user_histories(history_df.sort_values(["user_id", "timestamp", "live_id"], kind="mergesort"))
    csets = candidate_sets(phase_df, rooms, n_neg=N_NEG, seed=SEED)
    rows = []
    for idx, r in phase_df.iterrows():
        cands = csets[idx]
        scores = score_candidates(cands, int(r.user_id), int(r.timestamp), pop, engagement, hour_ct, histories)
        for model in AGENTS:
            rows.append({
                "user_id": int(r.user_id), "phase": phase, "history_mode": history_mode,
                "model": model, "rank": target_rank(cands, scores[model]), "candidate_count": int(len(cands)),
            })
    return pd.DataFrame(rows)


def rank_metrics(rank: pd.Series) -> dict[str, float]:
    r = rank.astype(int)
    return {
        "users": int(len(r)),
        "hr@5": float((r <= 5).mean()), "hr@10": float((r <= 10).mean()), "hr@20": float((r <= 20).mean()),
        "ndcg@5": float(r.map(lambda x: ndcg(int(x), 5)).mean()),
        "ndcg@10": float(r.map(lambda x: ndcg(int(x), 10)).mean()),
        "ndcg@20": float(r.map(lambda x: ndcg(int(x), 20)).mean()),
        "mrr": float((1.0 / r).mean()),
    }


def summarize_ranks(sas_dev, sas_test, agent_frames) -> pd.DataFrame:
    rows = []
    for phase, sas in [("dev", sas_dev), ("test", sas_test)]:
        row = {"phase": phase, "history_mode": "ReChorus sequential", "model": "SASRec"}
        row.update(rank_metrics(sas.sasrec_rank)); rows.append(row)
    agents = pd.concat(agent_frames, ignore_index=True)
    for (phase, hm, model), g in agents.groupby(["phase", "history_mode", "model"]):
        row = {"phase": phase, "history_mode": hm, "model": model}; row.update(rank_metrics(g["rank"])); rows.append(row)
    return pd.DataFrame(rows).sort_values(["phase", "history_mode", "ndcg@10"], ascending=[True, True, False])


def make_phase_table(sas, agents, features) -> pd.DataFrame:
    a = agents.pivot(index="user_id", columns="model", values="rank").reset_index()
    z = sas.merge(a, on="user_id", how="inner").merge(features, on="user_id", how="inner")
    z["log_history_len"] = np.log1p(z["history_len"].astype(float))
    z["sasrec_score10"] = z["sasrec_rank"].map(lambda r: ndcg(int(r), 10))
    for model in AGENTS:
        z[f"{model}_score10"] = z[model].map(lambda r: ndcg(int(r), 10))
        z[f"{model}_delta"] = z[f"{model}_score10"] - z["sasrec_score10"]
    return z


def residual_stability(dev, test) -> pd.DataFrame:
    rows = []
    for model in AGENTS:
        d = dev[["user_id", f"{model}_delta"]].rename(columns={f"{model}_delta": "dev_delta"})
        t = test[["user_id", f"{model}_delta"]].rename(columns={f"{model}_delta": "test_delta"})
        z = d.merge(t, on="user_id", how="inner")
        rows.append({
            "model": model, "users": len(z), "dev_mean_delta": z.dev_delta.mean(), "test_mean_delta": z.test_delta.mean(),
            "dev_win_rate": (z.dev_delta > 0).mean(), "test_win_rate": (z.test_delta > 0).mean(),
            "dev_loss_rate": (z.dev_delta < 0).mean(), "test_loss_rate": (z.test_delta < 0).mean(),
            "pearson_dev_test": z.dev_delta.corr(z.test_delta, method="pearson"),
            "spearman_dev_test": z.dev_delta.corr(z.test_delta, method="spearman"),
            "sign_agreement": (np.sign(z.dev_delta) == np.sign(z.test_delta)).mean(),
        })
    return pd.DataFrame(rows)


def quartile_residuals(test) -> pd.DataFrame:
    rows = []
    features = ["history_len", "repeat_rate", "preference_entropy", "preference_drift", "time_regularity", "state_complexity"]
    for model in AGENTS:
        delta_col = f"{model}_delta"
        for feat in features:
            tmp = test[["user_id", feat, delta_col]].dropna().copy()
            try:
                tmp["quartile"] = pd.qcut(tmp[feat], 4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
            except ValueError:
                continue
            for qi, (q, g) in enumerate(tmp.groupby("quartile", observed=True)):
                mean, lo, hi = bootstrap_mean(g[delta_col].to_numpy(), seed=SEED + qi, n_boot=1000)
                rows.append({
                    "model": model, "feature": feat, "quartile": str(q), "n": len(g), "feature_mean": g[feat].mean(),
                    "delta_ndcg10": mean, "ci95_low": lo, "ci95_high": hi,
                    "agent_win_rate": (g[delta_col] > 0).mean(), "tie_rate": (g[delta_col] == 0).mean(),
                    "sasrec_win_rate": (g[delta_col] < 0).mean(),
                })
    return pd.DataFrame(rows)


def fit_gate(dev, test, model: str) -> dict:
    xdev = dev[GATE_FEATURES].astype(float).to_numpy(); xtest = test[GATE_FEATURES].astype(float).to_numpy()
    ydev = dev[f"{model}_delta"].astype(float).to_numpy()
    reg = make_pipeline(StandardScaler(), Ridge(alpha=1.0)); reg.fit(xdev, ydev)
    pdev = reg.predict(xdev); ptest = reg.predict(xtest)
    sas_dev = dev["sasrec_score10"].to_numpy(float); ag_dev = dev[f"{model}_score10"].to_numpy(float)
    sas_test = test["sasrec_score10"].to_numpy(float); ag_test = test[f"{model}_score10"].to_numpy(float)
    thresholds = np.unique(np.r_[0.0, np.quantile(pdev, np.linspace(0, 1, 101))])
    best = None
    for th in thresholds:
        use_agent = pdev > th
        score = np.where(use_agent, ag_dev, sas_dev).mean()
        cand = (float(score), -float(use_agent.mean()), float(th))
        if best is None or cand > best[0]: best = (cand, float(th), use_agent)
    _, threshold, use_agent_dev = best
    use_agent_test = ptest > threshold
    selective_dev = np.where(use_agent_dev, ag_dev, sas_dev); selective_test = np.where(use_agent_test, ag_test, sas_test)
    mean_delta, lo, hi = bootstrap_mean(selective_test - sas_test, seed=SEED + 77, n_boot=2000)
    oracle_test = np.maximum(ag_test, sas_test); oracle_dev = np.maximum(ag_dev, sas_dev)
    return {
        "agent": model, "threshold": threshold, "dev_gate_rate": float(use_agent_dev.mean()), "test_gate_rate": float(use_agent_test.mean()),
        "dev_sasrec_ndcg10": float(sas_dev.mean()), "dev_agent_ndcg10": float(ag_dev.mean()),
        "dev_selective_ndcg10": float(selective_dev.mean()), "dev_oracle_ndcg10": float(oracle_dev.mean()),
        "test_sasrec_ndcg10": float(sas_test.mean()), "test_agent_ndcg10": float(ag_test.mean()),
        "test_selective_ndcg10": float(selective_test.mean()), "test_selective_delta": mean_delta,
        "test_selective_ci95_low": lo, "test_selective_ci95_high": hi,
        "test_oracle_ndcg10": float(oracle_test.mean()), "test_oracle_delta": float((oracle_test - sas_test).mean()),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepared-dir", type=Path, required=True); ap.add_argument("--rechorus-dir", type=Path, required=True)
    ap.add_argument("--sasrec-dev", type=Path, required=True); ap.add_argument("--sasrec-test", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True); args = ap.parse_args(); args.out_dir.mkdir(parents=True, exist_ok=True)

    events = pd.read_pickle(args.prepared_dir / "events.pkl"); rooms = pd.read_pickle(args.prepared_dir / "rooms.pkl")
    train, dev, test = split_events(events, 3)
    users = sorted(set(train.user_id) | set(dev.user_id) | set(test.user_id)); uid_to_original = {i + 1: int(u) for i, u in enumerate(users)}
    sas_dev = load_sasrec_ranks(args.sasrec_dev, args.rechorus_dir / "dev.csv", uid_to_original, "dev")
    sas_test = load_sasrec_ranks(args.sasrec_test, args.rechorus_dir / "test.csv", uid_to_original, "test")

    agent_dev = score_agent_phase(dev, rooms, train, train, "dev", "train")
    train_dev = pd.concat([train, dev], ignore_index=True)
    agent_test_online = score_agent_phase(test, rooms, train_dev, train, "test", "train+dev")
    agent_test_train_only = score_agent_phase(test, rooms, train, train, "test", "train_only_audit")

    feat_dev = user_features(train); feat_test = user_features(train_dev.sort_values(["user_id", "timestamp", "live_id"], kind="mergesort"))
    dev_table = make_phase_table(sas_dev, agent_dev, feat_dev); test_table = make_phase_table(sas_test, agent_test_online, feat_test)
    summary = summarize_ranks(sas_dev, sas_test, [agent_dev, agent_test_online, agent_test_train_only])
    stability = residual_stability(dev_table, test_table); quartiles = quartile_residuals(test_table)
    gates = pd.DataFrame([fit_gate(dev_table, test_table, m) for m in AGENTS]).sort_values("dev_selective_ndcg10", ascending=False).reset_index(drop=True)
    gates["selected_on_dev"] = False
    if len(gates): gates.loc[0, "selected_on_dev"] = True

    audit = []
    old = agent_test_train_only.pivot(index="user_id", columns="model", values="rank"); new = agent_test_online.pivot(index="user_id", columns="model", values="rank")
    for model in AGENTS:
        old_score = old[model].map(lambda r: ndcg(int(r), 10)).to_numpy(float); new_score = new[model].map(lambda r: ndcg(int(r), 10)).to_numpy(float)
        m, lo, hi = bootstrap_mean(new_score - old_score, seed=SEED + 123, n_boot=2000)
        audit.append({"model": model, "train_only_ndcg10": float(old_score.mean()), "train_plus_dev_ndcg10": float(new_score.mean()), "history_update_delta": m, "ci95_low": lo, "ci95_high": hi})
    audit = pd.DataFrame(audit)

    summary.to_csv(args.out_dir / "metric_summary.csv", index=False); stability.to_csv(args.out_dir / "residual_stability.csv", index=False)
    quartiles.to_csv(args.out_dir / "residual_quartiles.csv", index=False); gates.to_csv(args.out_dir / "selective_gate.csv", index=False)
    audit.to_csv(args.out_dir / "history_fairness_audit.csv", index=False)
    dev_table.to_csv(args.out_dir / "per_user_dev.csv.gz", index=False, compression="gzip"); test_table.to_csv(args.out_dir / "per_user_test.csv.gz", index=False, compression="gzip")
    selected = gates.iloc[0].to_dict() if len(gates) else {}
    (args.out_dir / "report.json").write_text(json.dumps({"seed": SEED, "n_neg": N_NEG, "users": len(users), "fairness_change": "test Agent user history updated from train-only to train+dev; global statistics remain train-only", "best_gate_selected_on_dev": selected}, indent=2) + "\n")

    print("\n=== Metric summary ==="); print(summary.to_string(index=False))
    print("\n=== History fairness audit ==="); print(audit.to_string(index=False))
    print("\n=== Residual stability ==="); print(stability.to_string(index=False))
    print("\n=== Selective gates (chosen only by dev) ==="); print(gates.to_string(index=False))


if __name__ == "__main__": main()
