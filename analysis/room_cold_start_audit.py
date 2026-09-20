from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260918
EPS = 1e-12


def parse_int_list(text: str) -> np.ndarray:
    s = str(text).strip()
    if not (s.startswith("[") and s.endswith("]")):
        raise ValueError(f"bad list: {s[:80]}")
    if len(s) <= 2:
        return np.empty(0, dtype=np.int64)
    return np.fromstring(s[1:-1], sep=",", dtype=np.int64)


def ndcg10(rank) -> np.ndarray:
    r = np.asarray(rank, dtype=int)
    out = np.zeros(len(r), dtype=float)
    m = r <= 10
    out[m] = 1.0 / np.log2(r[m] + 1.0)
    return out


def bootstrap_mean(diff, seed: int, n_boot: int = 4000):
    x = np.asarray(diff, dtype=float)
    if len(x) == 0:
        return None, None, None
    if len(x) == 1:
        v = float(x[0])
        return v, v, v
    rng = np.random.default_rng(seed)
    b = np.empty(n_boot, dtype=float)
    n = len(x)
    for i in range(n_boot):
        b[i] = x[rng.integers(0, n, n)].mean()
    return float(x.mean()), float(np.quantile(b, .025)), float(np.quantile(b, .975))


def metrics_row(name: str, g: pd.DataFrame, total_gain: float, seed: int):
    ds = g.selective_score10.to_numpy() - g.sasrec_score10.to_numpy()
    dm = g.MemoryFusion_score10.to_numpy() - g.sasrec_score10.to_numpy()
    sel, slo, shi = bootstrap_mean(ds, seed)
    mem, mlo, mhi = bootstrap_mean(dm, seed + 1)
    gain_sum = float(ds.sum())
    return {
        "group": name,
        "n": int(len(g)),
        "share": float(len(g) / max(len(TEST_FRAME), 1)),
        "sasrec_ndcg10": float(g.sasrec_score10.mean()) if len(g) else None,
        "memory_ndcg10": float(g.MemoryFusion_score10.mean()) if len(g) else None,
        "selective_ndcg10": float(g.selective_score10.mean()) if len(g) else None,
        "sasrec_hr10": float((g.sasrec_rank <= 10).mean()) if len(g) else None,
        "memory_hr10": float((g.memory_rank <= 10).mean()) if len(g) else None,
        "selective_hr10": float((g.selective_rank <= 10).mean()) if len(g) else None,
        "selective_minus_sasrec": sel,
        "selective_ci95_low": slo,
        "selective_ci95_high": shi,
        "memory_minus_sasrec": mem,
        "memory_ci95_low": mlo,
        "memory_ci95_high": mhi,
        "gate_rate": float(g.primary_use_agent.mean()) if len(g) else None,
        "gain_contribution_share": float(gain_sum / total_gain) if abs(total_gain) > EPS else None,
        "candidate_room_seen_train_rate": float(g.candidate_room_seen_train_rate.mean()) if len(g) else None,
        "candidate_streamer_seen_train_rate": float(g.candidate_streamer_seen_train_rate.mean()) if len(g) else None,
        "candidate_user_streamer_familiar_rate": float(g.candidate_user_streamer_familiar_rate.mean()) if len(g) else None,
    }


def add_target_flags(df, item_to_streamer, train_rooms, train_streamers, pre_rooms, pre_streamers, user_pre_streamers):
    out = df.copy()
    out["target_streamer_id"] = out.item_id.astype(int).map(item_to_streamer).astype("int64")
    out["target_room_seen_train"] = out.item_id.astype(int).isin(train_rooms)
    out["target_streamer_seen_train"] = out.target_streamer_id.astype(int).isin(train_streamers)
    out["target_room_seen_pretest"] = out.item_id.astype(int).isin(pre_rooms)
    out["target_streamer_seen_pretest_global"] = out.target_streamer_id.astype(int).isin(pre_streamers)
    out["target_streamer_user_familiar_pretest"] = [
        int(sid) in user_pre_streamers.get(int(uid), set())
        for uid, sid in zip(out.user_id, out.target_streamer_id)
    ]
    return out


def target_rate_table(dev, test):
    rows = []
    for phase, df in [("dev", dev), ("test", test)]:
        for col in [
            "target_room_seen_train", "target_streamer_seen_train",
            "target_room_seen_pretest", "target_streamer_seen_pretest_global",
            "target_streamer_user_familiar_pretest",
        ]:
            if col in df:
                rows.append({"phase": phase, "flag": col, "rate": float(df[col].mean()), "n": int(len(df))})
    return pd.DataFrame(rows)


def candidate_rates(row, item_to_streamer, train_rooms, train_streamers, user_pre_streamers):
    neg = parse_int_list(row.neg_items)
    cands = np.concatenate(([int(row.item_id)], neg))
    sids = np.fromiter((int(item_to_streamer[int(i)]) for i in cands), dtype=np.int64, count=len(cands))
    familiar = user_pre_streamers.get(int(row.user_id), set())
    return (
        float(np.mean(np.isin(cands, list(train_rooms)))),
        float(np.mean(np.isin(sids, list(train_streamers)))),
        float(np.mean([int(s) in familiar for s in sids])),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--frozen-dir", type=Path, required=True,
                    help="Directory containing room_kill_gate/per_user_test.csv.gz and report.json")
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n-neg", type=int, default=574)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv(args.data_dir / "train.csv", sep="\t")
    dev = pd.read_csv(args.data_dir / "dev.csv", sep="\t")
    test = pd.read_csv(args.data_dir / "test.csv", sep="\t")
    room_map = pd.read_csv(args.data_dir / "room_item_map.tsv", sep="\t")
    frozen = pd.read_csv(args.frozen_dir / "room_kill_gate" / "per_user_test.csv.gz")
    frozen_report = json.load(open(args.frozen_dir / "room_kill_gate" / "report.json"))

    for df in [train, dev, test]:
        df["user_id"] = df.user_id.astype(int)
        df["item_id"] = df.item_id.astype(int)
    room_map[["item_id", "live_id", "streamer_id"]] = room_map[["item_id", "live_id", "streamer_id"]].astype("int64")
    item_to_streamer = dict(zip(room_map.item_id.astype(int), room_map.streamer_id.astype(int)))

    if len(test) != len(frozen) or set(test.user_id) != set(frozen.user_id):
        raise ValueError("Frozen per-user test results do not align with regenerated test set")
    lens = test.neg_items.map(lambda x: len(parse_int_list(x)))
    if not (lens == args.n_neg).all():
        raise ValueError("Regenerated candidate count mismatch")

    train_rooms = set(train.item_id.astype(int))
    train_streamers = {int(item_to_streamer[i]) for i in train_rooms}
    pretest = pd.concat([train[["user_id", "item_id"]], dev[["user_id", "item_id"]]], ignore_index=True)
    pre_rooms = set(pretest.item_id.astype(int))
    pre_streamers = {int(item_to_streamer[i]) for i in pre_rooms}
    user_pre_streamers = {
        int(uid): {int(item_to_streamer[int(i)]) for i in g.item_id.astype(int)}
        for uid, g in pretest.groupby("user_id", sort=False)
    }

    # Dev has train as its pre-event history; use train-only personal streamer familiarity there.
    user_train_streamers = {
        int(uid): {int(item_to_streamer[int(i)]) for i in g.item_id.astype(int)}
        for uid, g in train.groupby("user_id", sort=False)
    }
    dev_flags = add_target_flags(dev, item_to_streamer, train_rooms, train_streamers,
                                 train_rooms, train_streamers, user_train_streamers)
    test_flags = add_target_flags(test, item_to_streamer, train_rooms, train_streamers,
                                  pre_rooms, pre_streamers, user_pre_streamers)

    t = test_flags.merge(frozen, on="user_id", validate="one_to_one")
    t["selective_score10"] = np.where(t.primary_use_agent, t.MemoryFusion_score10, t.sasrec_score10)
    t["selective_rank"] = np.where(t.primary_use_agent, t.memory_rank, t.sasrec_rank).astype(int)

    # Frozen-result integrity checks.
    checks = {
        "sasrec_test_ndcg10": float(t.sasrec_score10.mean()),
        "memory_test_ndcg10": float(t.MemoryFusion_score10.mean()),
        "selective_test_ndcg10": float(t.selective_score10.mean()),
        "test_gate_rate": float(t.primary_use_agent.mean()),
    }
    for k, v in checks.items():
        if abs(v - float(frozen_report[k])) > 1e-10:
            raise ValueError(f"Frozen result mismatch for {k}: {v} vs {frozen_report[k]}")

    # Candidate cold-start load per user.
    crows = []
    for r in test.itertuples(index=False):
        rr, ss, uu = candidate_rates(r, item_to_streamer, train_rooms, train_streamers, user_pre_streamers)
        crows.append((int(r.user_id), rr, ss, uu))
    cdf = pd.DataFrame(crows, columns=[
        "user_id", "candidate_room_seen_train_rate", "candidate_streamer_seen_train_rate",
        "candidate_user_streamer_familiar_rate",
    ])
    t = t.merge(cdf, on="user_id", validate="one_to_one")

    # Primary global cold-start taxonomy.
    t["cold_start_group"] = np.select(
        [
            t.target_room_seen_train,
            (~t.target_room_seen_train) & t.target_streamer_seen_train,
        ],
        ["seen_room_train", "new_room_seen_streamer_train"],
        default="new_room_new_streamer_train",
    )
    # Secondary, memory-specific taxonomy: can this user's prior history identify the target streamer?
    t["personal_memory_group"] = np.select(
        [
            t.target_room_seen_train,
            (~t.target_room_seen_train) & t.target_streamer_user_familiar_pretest,
        ],
        ["seen_room_train", "new_room_user_familiar_streamer"],
        default="new_room_user_novel_streamer",
    )

    global TEST_FRAME
    TEST_FRAME = t
    total_gain = float((t.selective_score10 - t.sasrec_score10).sum())
    rows = []
    for taxonomy, col, order in [
        ("global_train_exposure", "cold_start_group", [
            "seen_room_train", "new_room_seen_streamer_train", "new_room_new_streamer_train"]),
        ("user_memory_exposure", "personal_memory_group", [
            "seen_room_train", "new_room_user_familiar_streamer", "new_room_user_novel_streamer"]),
    ]:
        for j, name in enumerate(order):
            r = metrics_row(name, t[t[col] == name], total_gain, SEED + 100 * (j + 1))
            r["taxonomy"] = taxonomy
            rows.append(r)
    groups = pd.DataFrame(rows)

    target_rates = target_rate_table(dev_flags, test_flags)
    candidate_summary = {
        "mean_candidate_room_seen_train_rate": float(t.candidate_room_seen_train_rate.mean()),
        "mean_candidate_streamer_seen_train_rate": float(t.candidate_streamer_seen_train_rate.mean()),
        "mean_candidate_user_streamer_familiar_rate": float(t.candidate_user_streamer_familiar_rate.mean()),
        "median_candidate_room_seen_train_rate": float(t.candidate_room_seen_train_rate.median()),
        "median_candidate_streamer_seen_train_rate": float(t.candidate_streamer_seen_train_rate.median()),
    }

    seen = groups[(groups.taxonomy == "global_train_exposure") & (groups.group == "seen_room_train")]
    new_seen_s = groups[(groups.taxonomy == "global_train_exposure") & (groups.group == "new_room_seen_streamer_train")]
    if len(seen) and int(seen.iloc[0].n) >= 100 and float(seen.iloc[0].selective_ci95_low) > 0:
        diagnosis = "benefit_persists_on_seen_rooms"
    elif len(new_seen_s) and int(new_seen_s.iloc[0].n) >= 100 and float(new_seen_s.iloc[0].selective_ci95_low) > 0:
        diagnosis = "benefit_concentrated_in_new_rooms_with_seen_streamers"
    else:
        diagnosis = "no_stable_positive_seen_room_or_seen_streamer_stratum"

    report = {
        "audit": "room_cold_start",
        "frozen_source_run": 35455075346,
        "users": int(len(t)),
        "train_unique_rooms": int(len(train_rooms)),
        "train_unique_streamers": int(len(train_streamers)),
        "pretest_unique_rooms_train_plus_dev": int(len(pre_rooms)),
        "pretest_unique_streamers_train_plus_dev": int(len(pre_streamers)),
        "overall": checks,
        "candidate_summary": candidate_summary,
        "diagnosis": diagnosis,
        "definitions": {
            "seen_room_train": "target live_id occurs as a positive interaction in train.csv",
            "new_room_seen_streamer_train": "target live_id is absent from train positives but its streamer_id occurs in train positives",
            "new_room_new_streamer_train": "neither target live_id nor its streamer_id occurs in train positives",
            "user_familiar_streamer": "target streamer_id occurs in that user's fair pre-test history (train+dev)",
            "note": "ReChorus may sample future-unseen item IDs as training negatives because its item universe spans the corpus; this audit therefore defines semantic exposure using positive interactions, not negative-sampler touches.",
        },
    }

    t.to_csv(args.out_dir / "per_user_cold_start.csv.gz", index=False, compression="gzip")
    groups.to_csv(args.out_dir / "group_metrics.csv", index=False)
    target_rates.to_csv(args.out_dir / "target_exposure_rates.csv", index=False)
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")

    print(json.dumps(report, indent=2))
    print("\n=== GROUP METRICS ===")
    print(groups.to_string(index=False))
    print("\n=== TARGET EXPOSURE RATES ===")
    print(target_rates.to_string(index=False))


if __name__ == "__main__":
    TEST_FRAME = pd.DataFrame()
    main()
