from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260923
EXPECTED_N = 46878
LENGTHS = (8, 16, 32)
STATE_ORDER = ("recent-visible", "long-horizon-only", "unseen")
IDENTITY_COLS = ("target_streamer", "target_step", "candidate_count")


def _strict_bool(s: pd.Series, name: str) -> pd.Series:
    if s.dtype == bool:
        return s.astype(bool)
    text = s.astype(str).str.strip().str.lower()
    mapping = {"true": True, "false": False, "1": True, "0": False}
    bad = ~text.isin(mapping)
    if bad.any():
        vals = sorted(text.loc[bad].unique().tolist())[:10]
        raise RuntimeError(f"invalid boolean values in {name}: {vals}")
    return text.map(mapping).astype(bool)


def _canonical_state_name(x: object) -> str:
    s = str(x).strip().lower().replace("_", "-")
    if s not in STATE_ORDER:
        raise ValueError(f"unknown relationship state {x!r}")
    return s


def _ndcg10_from_rank0(rank: np.ndarray) -> np.ndarray:
    r = np.asarray(rank, dtype=np.int64)
    out = np.zeros(len(r), dtype=np.float64)
    m = r < 10
    out[m] = 1.0 / np.log2(r[m].astype(np.float64) + 2.0)
    return out


def _bootstrap_mean(x: np.ndarray, seed: int, n_boot: int, chunk: int = 64) -> dict:
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1 or len(x) == 0 or not np.isfinite(x).all():
        raise ValueError("bootstrap input must be non-empty, finite, one-dimensional")
    if n_boot <= 0:
        raise ValueError("n_boot must be positive")
    rng = np.random.default_rng(seed)
    means = np.empty(int(n_boot), dtype=np.float64)
    pos = 0
    while pos < n_boot:
        b = min(int(chunk), int(n_boot) - pos)
        idx = rng.integers(0, len(x), size=(b, len(x)), dtype=np.int32)
        means[pos : pos + b] = x[idx].mean(axis=1)
        pos += b
    return {
        "mean": float(x.mean()),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "n": int(len(x)),
    }


def _load_frozen_l16(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "user_id", "target_streamer", "target_step", "candidate_count",
        "relationship_horizon", "seen_before",
        "base_rank0", "base_ndcg10", "memory_rank0", "memory_ndcg10",
        "memory_delta_ndcg10", "history_len",
    }
    missing = sorted(required - set(df.columns))
    if missing or len(df) != EXPECTED_N or df.user_id.duplicated().any():
        raise RuntimeError(
            f"bad frozen L16 events: missing={missing}, n={len(df)}, "
            f"duplicate_users={df.user_id.duplicated().any()}"
        )
    out = df[list(required)].copy()
    out["relationship_state"] = out.relationship_horizon.map(_canonical_state_name)
    out["seen_before"] = _strict_bool(out.seen_before, "L16.seen_before")
    out["recent_visible"] = out.relationship_state.eq("recent-visible")
    if (out.recent_visible & ~out.seen_before).any():
        raise RuntimeError("frozen L16 has recent-visible events not present in pre-target history")
    expected_state = np.full(len(out), "unseen", dtype=object)
    expected_state[out.seen_before.to_numpy(bool)] = "long-horizon-only"
    expected_state[out.recent_visible.to_numpy(bool)] = "recent-visible"
    if not np.array_equal(expected_state, out.relationship_state.to_numpy(object)):
        raise RuntimeError("frozen L16 relationship state is inconsistent with seen_before/visibility semantics")
    numeric = [
        "user_id", "target_streamer", "target_step", "candidate_count",
        "base_rank0", "base_ndcg10", "memory_rank0", "memory_ndcg10",
        "memory_delta_ndcg10", "history_len",
    ]
    if not np.isfinite(out[numeric].to_numpy(np.float64)).all():
        raise RuntimeError("non-finite values in frozen L16")
    expected_ndcg = _ndcg10_from_rank0(out.memory_rank0.to_numpy(np.int64))
    if not np.allclose(expected_ndcg, out.memory_ndcg10.to_numpy(np.float64), rtol=0.0, atol=1e-12):
        raise RuntimeError("frozen L16 memory rank/NDCG identity failed")
    delta = out.memory_ndcg10.to_numpy(np.float64) - out.base_ndcg10.to_numpy(np.float64)
    if not np.allclose(delta, out.memory_delta_ndcg10.to_numpy(np.float64), rtol=0.0, atol=1e-12):
        raise RuntimeError("frozen L16 memory delta identity failed")
    return out


def _load_intervention(path: Path, length: int) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "user_id", "target_streamer", "target_step", "candidate_count",
        "recent_visible", "base_rank0", "base_ndcg10",
        "memory_rank0", "memory_ndcg10", "memory_delta_ndcg10", "history_len",
    }
    missing = sorted(required - set(df.columns))
    if missing or len(df) != EXPECTED_N or df.user_id.duplicated().any():
        raise RuntimeError(
            f"bad L={length} intervention events: missing={missing}, n={len(df)}, "
            f"duplicate_users={df.user_id.duplicated().any()}"
        )
    out = df[list(required)].copy()
    out["recent_visible"] = _strict_bool(out.recent_visible, f"L{length}.recent_visible")
    numeric = [
        "user_id", "target_streamer", "target_step", "candidate_count",
        "base_rank0", "base_ndcg10", "memory_rank0", "memory_ndcg10",
        "memory_delta_ndcg10", "history_len",
    ]
    if not np.isfinite(out[numeric].to_numpy(np.float64)).all():
        raise RuntimeError(f"non-finite values in L={length}")
    base_ndcg = _ndcg10_from_rank0(out.base_rank0.to_numpy(np.int64))
    if not np.allclose(base_ndcg, out.base_ndcg10.to_numpy(np.float64), rtol=0.0, atol=1e-12):
        raise RuntimeError(f"L={length} base rank/NDCG identity failed")
    return out


def _align_and_check_identity(reference: pd.DataFrame, other: pd.DataFrame, label: str) -> pd.DataFrame:
    ref = reference.set_index("user_id").sort_index()
    cur = other.set_index("user_id").sort_index()
    if not ref.index.equals(cur.index):
        raise RuntimeError(f"user set/order mismatch for {label}")
    for col in IDENTITY_COLS:
        if not np.array_equal(ref[col].to_numpy(), cur[col].to_numpy()):
            n = int(np.sum(ref[col].to_numpy() != cur[col].to_numpy()))
            raise RuntimeError(f"event identity mismatch {label}/{col}: n={n}")
    return cur


def _drift_summary(raw: pd.DataFrame, frozen: pd.DataFrame, length: int) -> dict:
    r = _align_and_check_identity(frozen, raw, f"L{length}-vs-frozen")
    f = frozen.set_index("user_id").sort_index()
    rank_diff = r.memory_rank0.to_numpy(np.int64) - f.memory_rank0.to_numpy(np.int64)
    hist_diff = r.history_len.to_numpy(np.int64) - f.history_len.to_numpy(np.int64)
    ndcg_diff = r.memory_ndcg10.to_numpy(np.float64) - f.memory_ndcg10.to_numpy(np.float64)
    return {
        "seq_len": int(length),
        "history_len_mismatch_users": int(np.count_nonzero(hist_diff)),
        "history_len_total_difference": int(hist_diff.sum()),
        "history_len_min_difference": int(hist_diff.min()),
        "history_len_max_difference": int(hist_diff.max()),
        "memory_rank_mismatch_users": int(np.count_nonzero(rank_diff)),
        "memory_rank_max_abs_difference": int(np.max(np.abs(rank_diff))),
        "memory_ndcg_mismatch_users": int(np.count_nonzero(np.abs(ndcg_diff) > 1e-15)),
        "memory_ndcg_mean_difference_raw_minus_frozen": float(ndcg_diff.mean()),
        "memory_ndcg_max_abs_difference": float(np.max(np.abs(ndcg_diff))),
    }


def _canonicalize(
    frozen: pd.DataFrame,
    raw: pd.DataFrame | None,
    length: int,
) -> pd.DataFrame:
    f = frozen.set_index("user_id").sort_index()
    if length == 16:
        base = f
        recent_visible = f.recent_visible.to_numpy(bool)
    else:
        if raw is None:
            raise RuntimeError(f"raw intervention missing for L={length}")
        base = _align_and_check_identity(frozen, raw, f"L{length}")
        recent_visible = base.recent_visible.to_numpy(bool)

    seen_before = f.seen_before.to_numpy(bool)
    if np.any(recent_visible & ~seen_before):
        raise RuntimeError(f"L={length} has recent-visible event absent from canonical pre-target history")

    state = np.full(EXPECTED_N, "unseen", dtype=object)
    state[seen_before] = "long-horizon-only"
    state[recent_visible] = "recent-visible"

    out = pd.DataFrame({
        "user_id": f.index.to_numpy(np.int64),
        "target_streamer": f.target_streamer.to_numpy(np.int64),
        "target_step": f.target_step.to_numpy(np.int64),
        "candidate_count": f.candidate_count.to_numpy(np.int64),
        "seq_len": int(length),
        "recent_visible": recent_visible,
        "seen_before": seen_before,
        "relationship_state": state,
        "base_rank0": base.base_rank0.to_numpy(np.int64),
        "base_ndcg10": base.base_ndcg10.to_numpy(np.float64),
        "memory_rank0": f.memory_rank0.to_numpy(np.int64),
        "memory_ndcg10": f.memory_ndcg10.to_numpy(np.float64),
        "history_len": f.history_len.to_numpy(np.int64),
    })
    out["memory_delta_ndcg10"] = out.memory_ndcg10 - out.base_ndcg10
    if out.user_id.duplicated().any() or len(out) != EXPECTED_N:
        raise RuntimeError(f"canonical L={length} coverage failure")
    return out


def _state_summary(df: pd.DataFrame, length: int, n_boot: int) -> pd.DataFrame:
    rows: list[dict] = []
    for j, state in enumerate(STATE_ORDER):
        g = df.loc[df.relationship_state == state]
        if g.empty:
            raise RuntimeError(f"empty state {state} at L={length}")
        delta = g.memory_delta_ndcg10.to_numpy(np.float64)
        ci = _bootstrap_mean(delta, SEED + 100 * length + j, n_boot)
        rows.append({
            "seq_len": int(length),
            "relationship_state": state,
            "n": int(len(g)),
            "prevalence": float(len(g) / len(df)),
            "base_ndcg10": float(g.base_ndcg10.mean()),
            "memory_ndcg10": float(g.memory_ndcg10.mean()),
            "memory_minus_base": ci["mean"],
            "ci95_low": ci["ci95_low"],
            "ci95_high": ci["ci95_high"],
            "positive_delta_fraction": float((delta > 0).mean()),
        })
    out = pd.DataFrame(rows)
    if int(out.n.sum()) != len(df) or not np.isclose(out.prevalence.sum(), 1.0, atol=1e-12):
        raise RuntimeError(f"state partition failed for L={length}")
    return out


def _overall_summary(df: pd.DataFrame, length: int, n_boot: int) -> dict:
    delta = df.memory_delta_ndcg10.to_numpy(np.float64)
    ci = _bootstrap_mean(delta, SEED + 50000 + length, n_boot)
    return {
        "seq_len": int(length),
        "n": int(len(df)),
        "base_ndcg10": float(df.base_ndcg10.mean()),
        "memory_ndcg10": float(df.memory_ndcg10.mean()),
        "memory_minus_base": ci["mean"],
        "ci95_low": ci["ci95_low"],
        "ci95_high": ci["ci95_high"],
    }


def _pair_by_user(a: pd.DataFrame, b: pd.DataFrame, la: int, lb: int) -> pd.DataFrame:
    cols = ["user_id", "relationship_state", "base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10"]
    ca = a[cols].rename(columns={
        "relationship_state": f"state_{la}",
        "base_ndcg10": f"base_{la}",
        "memory_ndcg10": f"memory_{la}",
        "memory_delta_ndcg10": f"delta_{la}",
    })
    cb = b[cols].rename(columns={
        "relationship_state": f"state_{lb}",
        "base_ndcg10": f"base_{lb}",
        "memory_ndcg10": f"memory_{lb}",
        "memory_delta_ndcg10": f"delta_{lb}",
    })
    out = ca.merge(cb, on="user_id", validate="one_to_one")
    if len(out) != EXPECTED_N:
        raise RuntimeError(f"paired user coverage failed L={la}->{lb}")
    return out


def _transition_summary(a: pd.DataFrame, b: pd.DataFrame, la: int, lb: int, n_boot: int) -> pd.DataFrame:
    m = _pair_by_user(a, b, la, lb)
    pairs = [
        ("long-horizon-only", "recent-visible", "recoverable_to_represented"),
        ("long-horizon-only", "long-horizon-only", "remains_recoverable"),
        ("recent-visible", "recent-visible", "remains_represented"),
        ("unseen", "unseen", "remains_unavailable"),
    ]
    rows: list[dict] = []
    for j, (sa, sb, name) in enumerate(pairs):
        g = m.loc[(m[f"state_{la}"] == sa) & (m[f"state_{lb}"] == sb)].copy()
        if g.empty:
            rows.append({
                "from_len": la, "to_len": lb, "transition": name, "n": 0,
                "delta_from": None, "delta_to": None, "delta_change": None,
                "ci95_low": None, "ci95_high": None, "base_change": None,
                "memory_change": None,
            })
            continue
        change = g[f"delta_{lb}"].to_numpy(np.float64) - g[f"delta_{la}"].to_numpy(np.float64)
        ci = _bootstrap_mean(change, SEED + 10000 + 100 * la + 10 * lb + j, n_boot)
        rows.append({
            "from_len": la,
            "to_len": lb,
            "transition": name,
            "n": int(len(g)),
            "delta_from": float(g[f"delta_{la}"].mean()),
            "delta_to": float(g[f"delta_{lb}"].mean()),
            "delta_change": ci["mean"],
            "ci95_low": ci["ci95_low"],
            "ci95_high": ci["ci95_high"],
            "base_change": float((g[f"base_{lb}"] - g[f"base_{la}"]).mean()),
            "memory_change": float((g[f"memory_{lb}"] - g[f"memory_{la}"]).mean()),
            "positive_fraction_from": float((g[f"delta_{la}"] > 0).mean()),
            "positive_fraction_to": float((g[f"delta_{lb}"] > 0).mean()),
        })
    return pd.DataFrame(rows)


def _self_test() -> None:
    s = pd.Series(["true", "FALSE", "1", "0"])
    assert _strict_bool(s, "test").tolist() == [True, False, True, False]
    assert _canonical_state_name("long_horizon_only") == "long-horizon-only"
    b = _bootstrap_mean(np.array([1.0, 2.0, 3.0]), 1, 50, 8)
    assert b["n"] == 3 and np.isclose(b["mean"], 2.0)
    ranks = np.array([0, 1, 9, 10])
    vals = _ndcg10_from_rank0(ranks)
    assert np.isclose(vals[0], 1.0) and vals[-1] == 0.0
    print("self-test: PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--l8-events", type=Path)
    ap.add_argument("--l16-events", type=Path)
    ap.add_argument("--l32-events", type=Path)
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--n-boot", type=int, default=3000)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        _self_test()
        return
    if any(x is None for x in (args.l8_events, args.l16_events, args.l32_events, args.out_dir)):
        ap.error("L8/L16/L32 event files and out-dir are required unless --self-test is used")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    frozen = _load_frozen_l16(args.l16_events)
    raw8 = _load_intervention(args.l8_events, 8)
    raw32 = _load_intervention(args.l32_events, 32)

    drift = [
        _drift_summary(raw8, frozen, 8),
        _drift_summary(raw32, frozen, 32),
    ]

    dfs = {
        8: _canonicalize(frozen, raw8, 8),
        16: _canonicalize(frozen, None, 16),
        32: _canonicalize(frozen, raw32, 32),
    }

    base = dfs[16].set_index("user_id").sort_index()
    for L in (8, 32):
        cur = dfs[L].set_index("user_id").sort_index()
        if not np.array_equal(base.memory_rank0.to_numpy(), cur.memory_rank0.to_numpy()):
            raise RuntimeError(f"canonical Memory rank changed between L16 and L{L}")
        if not np.allclose(base.memory_ndcg10.to_numpy(), cur.memory_ndcg10.to_numpy(), rtol=0.0, atol=0.0):
            raise RuntimeError(f"canonical Memory NDCG changed between L16 and L{L}")
        if not np.array_equal(base.history_len.to_numpy(), cur.history_len.to_numpy()):
            raise RuntimeError(f"canonical history_len changed between L16 and L{L}")

    represented = {
        L: set(df.loc[df.relationship_state == "recent-visible", "user_id"].astype(int))
        for L, df in dfs.items()
    }
    unseen = {
        L: set(df.loc[df.relationship_state == "unseen", "user_id"].astype(int))
        for L, df in dfs.items()
    }
    if not (represented[8] <= represented[16] <= represented[32]):
        raise RuntimeError("represented state is not nested as context expands")
    if not (unseen[8] == unseen[16] == unseen[32]):
        raise RuntimeError("unseen state changed with Base context length")

    state_summary = pd.concat(
        [_state_summary(dfs[L], L, args.n_boot) for L in LENGTHS],
        ignore_index=True,
    )
    overall = [_overall_summary(dfs[L], L, args.n_boot) for L in LENGTHS]
    transitions = pd.concat(
        [
            _transition_summary(dfs[8], dfs[16], 8, 16, args.n_boot),
            _transition_summary(dfs[16], dfs[32], 16, 32, args.n_boot),
            _transition_summary(dfs[8], dfs[32], 8, 32, args.n_boot),
        ],
        ignore_index=True,
    )

    state_summary.to_csv(args.out_dir / "context_length_state_summary.csv", index=False)
    transitions.to_csv(args.out_dir / "context_length_transitions.csv", index=False)
    pd.DataFrame(overall).to_csv(args.out_dir / "context_length_overall.csv", index=False)
    pd.DataFrame(drift).to_csv(args.out_dir / "memory_implementation_drift_diagnostic.csv", index=False)

    report = {
        "experiment": "kbs_context_length_intervention_aggregate_repaired",
        "scope": "DEV-only L=8/16/32 mechanism intervention; no GPU retraining",
        "test_ranking_inspected": False,
        "n_users": EXPECTED_N,
        "canonical_memory_source": "immutable frozen P1.2 L16 event-level artifact",
        "only_intervention_variable_for_scientific_comparison": "Base seq_len",
        "overall_summary": overall,
        "state_summary": state_summary.to_dict(orient="records"),
        "transition_summary": transitions.to_dict(orient="records"),
        "memory_implementation_drift_diagnostic": drift,
        "guards": {
            "same_event_identity_across_lengths": True,
            "canonical_memory_rank_invariant": True,
            "canonical_memory_ndcg_invariant": True,
            "canonical_history_invariant": True,
            "represented_nested": True,
            "unseen_invariant": True,
            "test_ranking_not_inspected": True,
        },
        "provenance_note": (
            "The first aggregation attempt failed closed because L8/L32 used a later Memory-history "
            "helper whose eligibility rule differed slightly from the frozen P1.2 exporter. "
            "This repair does not relax invariance checks and does not retrain any Base. "
            "It anchors Memory/history to the immutable frozen P1.2 event-level artifact and uses "
            "L8/L32 artifacts only for their independently trained Base outputs and visibility state."
        ),
        "interpretation_guardrail": (
            "Changing seq_len retrains the Base and changes its visible representation capacity. "
            "The repaired analysis supports a Base-relative visibility interpretation but is not a "
            "causal theorem and is not used for frozen P1.3 TEST model selection."
        ),
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
