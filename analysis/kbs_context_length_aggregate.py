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


def _canonical_state(x: object) -> str:
    s = str(x).strip().lower().replace("_", "-")
    if s not in STATE_ORDER:
        raise ValueError(f"unknown relationship state {x!r}")
    return s


def _bootstrap_mean(x: np.ndarray, seed: int, n_boot: int, chunk: int = 64) -> dict:
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1 or len(x) == 0 or not np.isfinite(x).all():
        raise ValueError("bootstrap input must be non-empty, finite, one-dimensional")
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


def _load(path: Path, length: int) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "user_id", "relationship_horizon", "base_ndcg10", "memory_ndcg10",
        "memory_delta_ndcg10", "history_len",
    }
    missing = sorted(required - set(df.columns))
    if missing or len(df) != EXPECTED_N or df.user_id.duplicated().any():
        raise RuntimeError(
            f"bad L={length} events: missing={missing}, n={len(df)}, duplicate_users={df.user_id.duplicated().any()}"
        )
    df = df[list(required)].copy()
    df["relationship_state"] = df.relationship_horizon.map(_canonical_state)
    df["seq_len"] = int(length)
    numeric = ["base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10", "history_len"]
    if not np.isfinite(df[numeric].to_numpy(np.float64)).all():
        raise RuntimeError(f"non-finite values for L={length}")
    check = df.memory_ndcg10.to_numpy(np.float64) - df.base_ndcg10.to_numpy(np.float64)
    if not np.allclose(check, df.memory_delta_ndcg10.to_numpy(np.float64), rtol=0.0, atol=1e-12):
        raise RuntimeError(f"memory delta identity failed for L={length}")
    return df


def _state_summary(df: pd.DataFrame, length: int, n_boot: int) -> pd.DataFrame:
    rows: list[dict] = []
    for j, state in enumerate(STATE_ORDER):
        g = df.loc[df.relationship_state == state]
        if g.empty:
            raise RuntimeError(f"empty state {state} at L={length}")
        delta = g.memory_delta_ndcg10.to_numpy(np.float64)
        ci = _bootstrap_mean(delta, SEED + 100 * length + j, n_boot)
        rows.append(
            {
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
            }
        )
    out = pd.DataFrame(rows)
    if int(out.n.sum()) != len(df) or not np.isclose(out.prevalence.sum(), 1.0, atol=1e-12):
        raise RuntimeError(f"state partition failed for L={length}")
    return out


def _pair_by_user(a: pd.DataFrame, b: pd.DataFrame, la: int, lb: int) -> pd.DataFrame:
    ca = a[["user_id", "relationship_state", "base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10"]].rename(
        columns={
            "relationship_state": f"state_{la}",
            "base_ndcg10": f"base_{la}",
            "memory_ndcg10": f"memory_{la}",
            "memory_delta_ndcg10": f"delta_{la}",
        }
    )
    cb = b[["user_id", "relationship_state", "base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10"]].rename(
        columns={
            "relationship_state": f"state_{lb}",
            "base_ndcg10": f"base_{lb}",
            "memory_ndcg10": f"memory_{lb}",
            "memory_delta_ndcg10": f"delta_{lb}",
        }
    )
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
            rows.append(
                {
                    "from_len": la, "to_len": lb, "transition": name, "n": 0,
                    "delta_from": None, "delta_to": None, "delta_change": None,
                    "ci95_low": None, "ci95_high": None,
                }
            )
            continue
        change = g[f"delta_{lb}"].to_numpy(np.float64) - g[f"delta_{la}"].to_numpy(np.float64)
        ci = _bootstrap_mean(change, SEED + 10000 + 100 * la + 10 * lb + j, n_boot)
        rows.append(
            {
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
            }
        )
    return pd.DataFrame(rows)


def _self_test() -> None:
    x = np.array([1.0, 2.0, 3.0])
    b = _bootstrap_mean(x, 1, 50, 8)
    assert b["n"] == 3 and np.isclose(b["mean"], 2.0)
    assert _canonical_state("long_horizon_only") == "long-horizon-only"
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

    dfs = {
        8: _load(args.l8_events, 8),
        16: _load(args.l16_events, 16),
        32: _load(args.l32_events, 32),
    }
    user_sets = {L: set(df.user_id.astype(int)) for L, df in dfs.items()}
    if not (user_sets[8] == user_sets[16] == user_sets[32]):
        raise RuntimeError("user sets differ across context lengths")

    # Memory uses the same pre-target evidence definition and must therefore be invariant to Base seq_len.
    base = dfs[8].set_index("user_id").sort_index()
    for L in (16, 32):
        cur = dfs[L].set_index("user_id").sort_index()
        if not np.allclose(base.memory_ndcg10.to_numpy(), cur.memory_ndcg10.to_numpy(), rtol=0.0, atol=1e-12):
            raise RuntimeError(f"Memory ranking changed unexpectedly between L=8 and L={L}")
        if not np.array_equal(base.history_len.to_numpy(), cur.history_len.to_numpy()):
            raise RuntimeError(f"history_len changed unexpectedly between L=8 and L={L}")

    represented = {L: set(df.loc[df.relationship_state == "recent-visible", "user_id"].astype(int)) for L, df in dfs.items()}
    unseen = {L: set(df.loc[df.relationship_state == "unseen", "user_id"].astype(int)) for L, df in dfs.items()}
    if not (represented[8] <= represented[16] <= represented[32]):
        raise RuntimeError("represented state is not nested as context expands")
    if not (unseen[8] == unseen[16] == unseen[32]):
        raise RuntimeError("unseen user set changed with Base context length")

    state_tabs = [_state_summary(dfs[L], L, args.n_boot) for L in LENGTHS]
    state_summary = pd.concat(state_tabs, ignore_index=True)
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

    report = {
        "experiment": "kbs_context_length_intervention_aggregate",
        "scope": "DEV-only L=8/16/32 mechanism intervention",
        "test_ranking_inspected": False,
        "n_users": EXPECTED_N,
        "state_summary": state_summary.to_dict(orient="records"),
        "transition_summary": transitions.to_dict(orient="records"),
        "guards": {
            "same_user_set": True,
            "memory_invariant_across_context_lengths": True,
            "history_invariant_across_context_lengths": True,
            "represented_nested": True,
            "unseen_invariant": True,
        },
        "interpretation_guardrail": "Changing seq_len retrains the Base and changes its visible representation capacity. Results support a Base-relative visibility interpretation but are not a causal theorem and are not used for frozen TEST model selection.",
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
