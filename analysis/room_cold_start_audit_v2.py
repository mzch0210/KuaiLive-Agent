from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260918
EPS = 1e-12


def parse_ids(text: str) -> np.ndarray:
    s = str(text).strip()
    if not (s.startswith("[") and s.endswith("]")):
        raise ValueError(f"bad candidate list: {s[:80]}")
    if len(s) <= 2:
        return np.empty(0, dtype=np.int64)
    return np.fromstring(s[1:-1], sep=",", dtype=np.int64)


def boot(x, seed, n_boot=4000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (None, None, None)
    if len(x) == 1:
        v = float(x[0]); return (v, v, v)
    rng = np.random.default_rng(seed)
    n = len(x)
    vals = np.empty(n_boot)
    for i in range(n_boot):
        vals[i] = x[rng.integers(0, n, n)].mean()
    return float(x.mean()), float(np.quantile(vals, .025)), float(np.quantile(vals, .975))


def group_row(taxonomy, group, g, n_total, total_gain, seed):
    ds = (g.selective_score10 - g.sasrec_score10).to_numpy(float)
    dm = (g.MemoryFusion_score10 - g.sasrec_score10).to_numpy(float)
    dsm, dslo, dshi = boot(ds, seed)
    dmm, dmlo, dmhi = boot(dm, seed + 1)
    return {
        "taxonomy": taxonomy,
        "group": group,
        "n": int(len(g)),
        "share": float(len(g) / max(n_total, 1)),
        "sasrec_ndcg10": float(g.sasrec_score10.mean()) if len(g) else None,
        "memory_ndcg10": float(g.MemoryFusion_score10.mean()) if len(g) else None,
        "selective_ndcg10": float(g.selective_score10.mean()) if len(g) else None,
        "sasrec_hr10": float((g.sasrec_rank <= 10).mean()) if len(g) else None,
        "memory_hr10": float((g.memory_rank <= 10).mean()) if len(g) else None,
        "selective_hr10": float((g.selective_rank <= 10).mean()) if len(g) else None,
        "selective_minus_sasrec": dsm,
        "selective_ci95_low": dslo,
        "selective_ci95_high": dshi,
        "memory_minus_sasrec": dmm,
        "memory_ci95_low": dmlo,
        "memory_ci95_high": dmhi,
        "gate_rate": float(g.primary_use_agent.mean()) if len(g) else None,
        "gain_contribution_share": float(ds.sum() / total_gain) if abs(total_gain) > EPS else None,
        "candidate_room_seen_train_rate": float(g.candidate_room_seen_train_rate.mean()) if len(g) else None,
        "candidate_streamer_seen_train_rate": float(g.candidate_streamer_seen_train_rate.mean()) if len(g) else None,
        "candidate_user_streamer_familiar_rate": float(g.candidate_user_streamer_familiar_rate.mean()) if len(g) else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--frozen-dir", type=Path, required=True)
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

    for df in (train, dev, test):
        df["user_id"] = df.user_id.astype(int)
        df["item_id"] = df.item_id.astype(int)
    room_map[["item_id", "live_id", "streamer_id"]] = room_map[["item_id", "live_id", "streamer_id"]].astype("int64")
    item2streamer = dict(zip(room_map.item_id.astype(int), room_map.streamer_id.astype(int)))

    if len(test) != len(frozen) or set(test.user_id) != set(frozen.user_id):
        raise ValueError("frozen per-user rows do not align with regenerated test")
    neg_lens = test.neg_items.map(lambda s: len(parse_ids(s)))
    if not (neg_lens == args.n_neg).all():
        raise ValueError("candidate count mismatch")

    train_rooms = set(train.item_id.astype(int))
    train_streamers = {item2streamer[i] for i in train_rooms}
    pretest = pd.concat([train[["user_id", "item_id"]], dev[["user_id", "item_id"]]], ignore_index=True)
    pre_rooms = set(pretest.item_id.astype(int))
    pre_streamers = {item2streamer[i] for i in pre_rooms}
    user_train_streamers = {
        int(uid): {item2streamer[int(i)] for i in g.item_id}
        for uid, g in train.groupby("user_id", sort=False)
    }
    user_pre_streamers = {
        int(uid): {item2streamer[int(i)] for i in g.item_id}
        for uid, g in pretest.groupby("user_id", sort=False)
    }

    def flag_targets(df, pre_r, pre_s, user_hist):
        x = df[["user_id", "item_id"]].copy()
        x["target_streamer_id"] = x.item_id.map(item2streamer).astype("int64")
        x["target_room_seen_train"] = x.item_id.isin(train_rooms)
        x["target_streamer_seen_train"] = x.target_streamer_id.isin(train_streamers)
        x["target_room_seen_pre_event"] = x.item_id.isin(pre_r)
        x["target_streamer_seen_pre_event_global"] = x.target_streamer_id.isin(pre_s)
        x["target_streamer_user_familiar_pre_event"] = [
            int(sid) in user_hist.get(int(uid), set())
            for uid, sid in zip(x.user_id, x.target_streamer_id)
        ]
        return x

    devf = flag_targets(dev, train_rooms, train_streamers, user_train_streamers)
    testf = flag_targets(test, pre_rooms, pre_streamers, user_pre_streamers)

    t = testf.merge(frozen, on="user_id", validate="one_to_one")
    t["selective_score10"] = np.where(t.primary_use_agent, t.MemoryFusion_score10, t.sasrec_score10)
    t["selective_rank"] = np.where(t.primary_use_agent, t.memory_rank, t.sasrec_rank).astype(int)

    frozen_checks = {
        "sasrec_test_ndcg10": float(t.sasrec_score10.mean()),
        "memory_test_ndcg10": float(t.MemoryFusion_score10.mean()),
        "selective_test_ndcg10": float(t.selective_score10.mean()),
        "test_gate_rate": float(t.primary_use_agent.mean()),
    }
    for k, v in frozen_checks.items():
        if abs(v - float(frozen_report[k])) > 1e-10:
            raise ValueError(f"frozen metric mismatch {k}: {v} != {frozen_report[k]}")

    # O(number of candidates): positive train exposure and personal-streamer familiarity.
    cand_rows = []
    for r in test.itertuples(index=False):
        neg = parse_ids(r.neg_items)
        cands = np.concatenate(([int(r.item_id)], neg))
        familiar = user_pre_streamers.get(int(r.user_id), set())
        room_seen = 0; streamer_seen = 0; user_familiar = 0
        for item in cands:
            item = int(item); sid = int(item2streamer[item])
            room_seen += item in train_rooms
            streamer_seen += sid in train_streamers
            user_familiar += sid in familiar
        n = len(cands)
        cand_rows.append((int(r.user_id), room_seen/n, streamer_seen/n, user_familiar/n))
    cdf = pd.DataFrame(cand_rows, columns=[
        "user_id", "candidate_room_seen_train_rate", "candidate_streamer_seen_train_rate",
        "candidate_user_streamer_familiar_rate"])
    t = t.merge(cdf, on="user_id", validate="one_to_one")

    t["cold_start_group"] = np.select(
        [t.target_room_seen_train,
         (~t.target_room_seen_train) & t.target_streamer_seen_train],
        ["seen_room_train", "new_room_seen_streamer_train"],
        default="new_room_new_streamer_train")
    t["personal_memory_group"] = np.select(
        [t.target_room_seen_train,
         (~t.target_room_seen_train) & t.target_streamer_user_familiar_pre_event],
        ["seen_room_train", "new_room_user_familiar_streamer"],
        default="new_room_user_novel_streamer")

    total_gain = float((t.selective_score10 - t.sasrec_score10).sum())
    rows = []
    specs = [
        ("global_train_exposure", "cold_start_group", [
            "seen_room_train", "new_room_seen_streamer_train", "new_room_new_streamer_train"]),
        ("user_memory_exposure", "personal_memory_group", [
            "seen_room_train", "new_room_user_familiar_streamer", "new_room_user_novel_streamer"]),
    ]
    seed = SEED
    for taxonomy, col, order in specs:
        for group in order:
            seed += 13
            rows.append(group_row(taxonomy, group, t[t[col] == group], len(t), total_gain, seed))
    groups = pd.DataFrame(rows)

    exposure_rows = []
    for phase, x in [("dev", devf), ("test", testf)]:
        for col in ["target_room_seen_train", "target_streamer_seen_train",
                    "target_room_seen_pre_event", "target_streamer_seen_pre_event_global",
                    "target_streamer_user_familiar_pre_event"]:
            exposure_rows.append({"phase": phase, "flag": col, "rate": float(x[col].mean()), "n": int(len(x))})
    exposure = pd.DataFrame(exposure_rows)

    primary = groups[groups.taxonomy == "global_train_exposure"].set_index("group")
    seen = primary.loc["seen_room_train"]
    new_seen = primary.loc["new_room_seen_streamer_train"]
    if seen.n >= 100 and pd.notna(seen.selective_ci95_low) and seen.selective_ci95_low > 0:
        diagnosis = "benefit_persists_on_seen_rooms"
    elif new_seen.n >= 100 and pd.notna(new_seen.selective_ci95_low) and new_seen.selective_ci95_low > 0:
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
        "overall": frozen_checks,
        "candidate_summary": {
            "mean_candidate_room_seen_train_rate": float(t.candidate_room_seen_train_rate.mean()),
            "mean_candidate_streamer_seen_train_rate": float(t.candidate_streamer_seen_train_rate.mean()),
            "mean_candidate_user_streamer_familiar_rate": float(t.candidate_user_streamer_familiar_rate.mean()),
            "median_candidate_room_seen_train_rate": float(t.candidate_room_seen_train_rate.median()),
            "median_candidate_streamer_seen_train_rate": float(t.candidate_streamer_seen_train_rate.median()),
        },
        "diagnosis": diagnosis,
        "definitions": {
            "seen_room_train": "target live_id occurs as a positive interaction in train.csv",
            "new_room_seen_streamer_train": "target live_id is absent from train positives but its streamer_id occurs in train positives",
            "new_room_new_streamer_train": "neither target live_id nor its streamer_id occurs in train positives",
            "user_familiar_streamer": "target streamer_id occurs in that user's fair pre-event history; for test this is train+dev",
            "semantic_exposure_note": "Exposure is defined by positive interactions, not possible negative-sampler touches.",
        },
    }

    t.to_csv(args.out_dir / "per_user_cold_start.csv.gz", index=False, compression="gzip")
    groups.to_csv(args.out_dir / "group_metrics.csv", index=False)
    exposure.to_csv(args.out_dir / "target_exposure_rates.csv", index=False)
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")

    print(json.dumps(report, indent=2))
    print("\n=== GROUP METRICS ===")
    print(groups.to_string(index=False))
    print("\n=== TARGET EXPOSURE ===")
    print(exposure.to_string(index=False))


if __name__ == "__main__":
    main()
