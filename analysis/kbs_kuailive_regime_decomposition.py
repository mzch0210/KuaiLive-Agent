from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260923
EXPECTED_USERS = 10222
STATE_ORDER = ("represented", "recoverable-but-unrepresented", "unavailable")


def _bootstrap_mean(x: np.ndarray, seed: int, n_boot: int, chunk: int = 64) -> dict:
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1:
        raise ValueError("bootstrap input must be one-dimensional")
    if len(x) == 0:
        return {"mean": None, "ci95_low": None, "ci95_high": None, "n": 0}
    if not np.isfinite(x).all():
        raise ValueError("non-finite bootstrap input")
    rng = np.random.default_rng(seed)
    means = np.empty(int(n_boot), dtype=np.float64)
    p = 0
    while p < n_boot:
        b = min(int(chunk), int(n_boot) - p)
        idx = rng.integers(0, len(x), size=(b, len(x)), dtype=np.int32)
        means[p : p + b] = x[idx].mean(axis=1)
        p += b
    return {
        "mean": float(x.mean()),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "n": int(len(x)),
    }


def _read_phase(path: Path, cols: list[str]) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", usecols=cols)
    for c in ("user_id", "item_id", "time"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="raise").astype(np.int64)
    return df


def _build_test_states(data_dir: Path, history_max: int) -> pd.DataFrame:
    train = _read_phase(data_dir / "train.csv", ["user_id", "item_id", "time"])
    dev = _read_phase(data_dir / "dev.csv", ["user_id", "item_id", "time"])
    test = _read_phase(data_dir / "test.csv", ["user_id", "item_id", "time"])
    if test.user_id.duplicated().any():
        raise RuntimeError("expected one KuaiLive test target per user")

    room_map = pd.read_csv(data_dir / "room_item_map.tsv", sep="\t", usecols=["item_id", "streamer_id"])
    room_map["item_id"] = pd.to_numeric(room_map.item_id, errors="raise").astype(np.int64)
    room_map["streamer_id"] = pd.to_numeric(room_map.streamer_id, errors="raise").astype(np.int64)
    if room_map.item_id.duplicated().any():
        raise RuntimeError("room_item_map must have unique item_id")
    item_to_streamer = room_map.set_index("item_id").streamer_id

    history = pd.concat([train, dev], ignore_index=True)
    history["streamer_id"] = history.item_id.map(item_to_streamer)
    test["target_streamer"] = test.item_id.map(item_to_streamer)
    if history.streamer_id.isna().any() or test.target_streamer.isna().any():
        raise RuntimeError("missing room-to-streamer mapping")
    history["streamer_id"] = history.streamer_id.astype(np.int64)
    test["target_streamer"] = test.target_streamer.astype(np.int64)

    history["_row"] = np.arange(len(history), dtype=np.int64)
    history.sort_values(["user_id", "time", "_row"], kind="mergesort", inplace=True)
    grouped = {
        int(uid): g.streamer_id.to_numpy(np.int64, copy=True)
        for uid, g in history.groupby("user_id", sort=False)
    }

    rows: list[dict] = []
    for r in test.itertuples(index=False):
        uid = int(r.user_id)
        target = int(r.target_streamer)
        hist = grouped.get(uid, np.empty(0, dtype=np.int64))
        visible = hist[-int(history_max) :] if len(hist) else hist
        seen_visible = bool(np.any(visible == target))
        seen_full = bool(np.any(hist == target))
        if seen_visible:
            state = "represented"
        elif seen_full:
            state = "recoverable-but-unrepresented"
        else:
            state = "unavailable"
        rows.append(
            {
                "user_id": uid,
                "target_streamer": target,
                "history_len": int(len(hist)),
                "visible_history_len": int(min(len(hist), int(history_max))),
                "evidence_state": state,
            }
        )
    out = pd.DataFrame(rows)
    if len(out) != len(test) or out.user_id.duplicated().any():
        raise RuntimeError("KuaiLive state construction coverage mismatch")
    return out


def _load_sampled(path: Path) -> pd.DataFrame:
    header = pd.read_csv(path, nrows=0).columns.tolist()
    base_col = "dual_score10" if "dual_score10" in header else "dual_id_ndcg10" if "dual_id_ndcg10" in header else None
    memory_col = "MemoryFusion_score10" if "MemoryFusion_score10" in header else "memory_ndcg10" if "memory_ndcg10" in header else None
    if base_col is None or memory_col is None or "user_id" not in header:
        raise RuntimeError(f"unsupported sampled per-user schema: {header}")
    df = pd.read_csv(path, usecols=["user_id", base_col, memory_col]).rename(
        columns={base_col: "base_ndcg10", memory_col: "memory_ndcg10"}
    )
    df["regime"] = "sampled-active"
    return df


def _load_full(path: Path) -> pd.DataFrame:
    header = pd.read_csv(path, nrows=0).columns.tolist()
    required = {"user_id", "native_base_ndcg10", "memory_ndcg10"}
    if not required <= set(header):
        raise RuntimeError(f"unsupported full-active per-user schema: {header}")
    df = pd.read_csv(path, usecols=sorted(required)).rename(columns={"native_base_ndcg10": "base_ndcg10"})
    df["regime"] = "full-active"
    return df


def _summarize_regime(df: pd.DataFrame, regime: str, n_boot: int) -> tuple[pd.DataFrame, dict]:
    g0 = df.loc[df.regime == regime].copy()
    if g0.empty:
        raise RuntimeError(f"empty regime {regime}")
    g0["delta"] = g0.memory_ndcg10 - g0.base_ndcg10
    rows: list[dict] = []
    for j, state in enumerate(STATE_ORDER):
        g = g0.loc[g0.evidence_state == state]
        d = g.delta.to_numpy(np.float64)
        ci = _bootstrap_mean(d, SEED + 100 * (1 if regime == "sampled-active" else 2) + j, n_boot)
        rows.append(
            {
                "regime": regime,
                "evidence_state": state,
                "n": int(len(g)),
                "prevalence": float(len(g) / len(g0)),
                "base_ndcg10": float(g.base_ndcg10.mean()),
                "memory_ndcg10": float(g.memory_ndcg10.mean()),
                "memory_minus_base": ci["mean"],
                "ci95_low": ci["ci95_low"],
                "ci95_high": ci["ci95_high"],
                "positive_delta_fraction": float((d > 0).mean()),
                "weighted_contribution": float((len(g) / len(g0)) * ci["mean"]),
            }
        )
    out = pd.DataFrame(rows)
    if int(out.n.sum()) != len(g0) or not np.isclose(out.prevalence.sum(), 1.0, atol=1e-12):
        raise RuntimeError(f"state partition not exhaustive for {regime}")
    overall = float(g0.delta.mean())
    reconstructed = float(out.weighted_contribution.sum())
    if not np.isclose(overall, reconstructed, atol=1e-12, rtol=0.0):
        raise RuntimeError(f"decomposition identity failed for {regime}: {overall} vs {reconstructed}")
    return out, {
        "regime": regime,
        "n": int(len(g0)),
        "base_ndcg10": float(g0.base_ndcg10.mean()),
        "memory_ndcg10": float(g0.memory_ndcg10.mean()),
        "memory_minus_base": overall,
        "weighted_state_reconstruction": reconstructed,
        "reconstruction_abs_error": float(abs(overall - reconstructed)),
    }


def _state_delta_shift(merged: pd.DataFrame, n_boot: int) -> pd.DataFrame:
    rows: list[dict] = []
    sampled_delta = merged.sampled_memory_ndcg10 - merged.sampled_base_ndcg10
    full_delta = merged.full_memory_ndcg10 - merged.full_base_ndcg10
    merged = merged.assign(sampled_delta=sampled_delta, full_delta=full_delta, delta_shift=full_delta - sampled_delta)
    for j, state in enumerate(STATE_ORDER):
        g = merged.loc[merged.evidence_state == state]
        ci = _bootstrap_mean(g.delta_shift.to_numpy(np.float64), SEED + 500 + j, n_boot)
        rows.append(
            {
                "evidence_state": state,
                "n": int(len(g)),
                "sampled_delta_mean": float(g.sampled_delta.mean()),
                "full_active_delta_mean": float(g.full_delta.mean()),
                "full_minus_sampled_delta_shift": ci["mean"],
                "ci95_low": ci["ci95_low"],
                "ci95_high": ci["ci95_high"],
            }
        )
    return pd.DataFrame(rows)


def _self_test() -> None:
    x = np.asarray([-0.2, 0.1, 0.3])
    b = _bootstrap_mean(x, 3, 50, 8)
    assert b["n"] == 3 and np.isclose(b["mean"], x.mean())
    toy = pd.DataFrame(
        {
            "regime": ["sampled-active"] * 3,
            "evidence_state": list(STATE_ORDER),
            "base_ndcg10": [0.5, 0.5, 0.5],
            "memory_ndcg10": [0.4, 0.8, 0.3],
        }
    )
    s, r = _summarize_regime(toy, "sampled-active", 50)
    assert np.isclose(s.weighted_contribution.sum(), r["memory_minus_base"])
    print("self-test: PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--room-data-dir", type=Path)
    ap.add_argument("--sampled-per-user", type=Path)
    ap.add_argument("--full-active-per-user", type=Path)
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--history-max", type=int, default=50)
    ap.add_argument("--n-boot", type=int, default=3000)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        _self_test()
        return
    if any(x is None for x in (args.room_data_dir, args.sampled_per_user, args.full_active_per_user, args.out_dir)):
        ap.error("room data, sampled/full per-user files, and out-dir are required unless --self-test is used")
    if args.history_max <= 0:
        ap.error("--history-max must be positive")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    states = _build_test_states(args.room_data_dir, args.history_max)
    sampled = _load_sampled(args.sampled_per_user)
    full = _load_full(args.full_active_per_user)

    for name, df in (("states", states), ("sampled", sampled), ("full", full)):
        if df.user_id.duplicated().any():
            raise RuntimeError(f"duplicate users in {name}")
    users = set(states.user_id.astype(int))
    if set(sampled.user_id.astype(int)) != users or set(full.user_id.astype(int)) != users:
        raise RuntimeError("sampled/full/state user sets differ")
    if len(users) != EXPECTED_USERS:
        raise RuntimeError(f"unexpected KuaiLive user count: {len(users)}")

    stacked = pd.concat([sampled, full], ignore_index=True).merge(
        states[["user_id", "evidence_state", "history_len", "visible_history_len"]],
        on="user_id",
        how="left",
        validate="many_to_one",
    )
    if stacked[["base_ndcg10", "memory_ndcg10"]].isna().any().any():
        raise RuntimeError("missing per-user performance values after merge")
    if not np.isfinite(stacked[["base_ndcg10", "memory_ndcg10"]].to_numpy(np.float64)).all():
        raise RuntimeError("non-finite per-user performance values")

    summaries = []
    reports = []
    for regime in ("sampled-active", "full-active"):
        tab, rep = _summarize_regime(stacked, regime, args.n_boot)
        summaries.append(tab)
        reports.append(rep)
    decomposition = pd.concat(summaries, ignore_index=True)

    wide = sampled.rename(columns={"base_ndcg10": "sampled_base_ndcg10", "memory_ndcg10": "sampled_memory_ndcg10"}).drop(columns="regime")
    wide = wide.merge(
        full.rename(columns={"base_ndcg10": "full_base_ndcg10", "memory_ndcg10": "full_memory_ndcg10"}).drop(columns="regime"),
        on="user_id",
        validate="one_to_one",
    ).merge(states[["user_id", "evidence_state"]], on="user_id", validate="one_to_one")
    shifts = _state_delta_shift(wide, args.n_boot)

    p_sampled = decomposition.loc[decomposition.regime == "sampled-active"].set_index("evidence_state").prevalence
    p_full = decomposition.loc[decomposition.regime == "full-active"].set_index("evidence_state").prevalence
    prevalence_max_abs_diff = float((p_sampled - p_full).abs().max())
    if prevalence_max_abs_diff > 1e-15:
        raise RuntimeError("candidate-regime comparison unexpectedly changed evidence-state prevalence")

    decomposition.to_csv(args.out_dir / "candidate_regime_state_decomposition.csv", index=False)
    shifts.to_csv(args.out_dir / "candidate_regime_state_delta_shift.csv", index=False)
    states.to_csv(args.out_dir / "test_evidence_states.csv.gz", index=False, compression="gzip")

    report = {
        "experiment": "kbs_kuailive_candidate_regime_state_decomposition",
        "history_max": int(args.history_max),
        "users": int(len(users)),
        "relationship_unit": "target streamer",
        "base_relative_state_definition": {
            "represented": f"target streamer occurs in the most recent {args.history_max} pre-target relationship events visible to the streamer-ID Base branch",
            "recoverable-but-unrepresented": f"target streamer is absent from the most recent {args.history_max} events but present in older pre-target history",
            "unavailable": "target streamer is absent from all pre-target relationship history",
        },
        "regime_reports": reports,
        "candidate_regime_state_prevalence_max_abs_diff": prevalence_max_abs_diff,
        "state_delta_shift_rows": shifts.to_dict(orient="records"),
        "interpretation": "The sampled-active and full-active protocols evaluate the same frozen test events, so state composition is identical by construction; candidate-universe effects can therefore be localized to changes in state-specific Base-relative utility for this comparison.",
        "guardrails": [
            "No model or policy is refit by this analysis.",
            "The same event-level evidence-state labels are reused across the two candidate regimes.",
            "This candidate-regime result does not imply that temporal regime shifts preserve state composition.",
            "No result-sign criterion is used for workflow success.",
        ],
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
