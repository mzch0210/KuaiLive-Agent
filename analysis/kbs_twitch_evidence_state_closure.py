from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

EXPECTED_N = 46878
EXPECTED_K = 6563
SEED = 20260923
STATE_ORDER = ("recent-visible", "long-horizon-only", "unseen")
STATE_LABEL = {
    "recent-visible": "represented",
    "long-horizon-only": "recoverable-but-unrepresented",
    "unseen": "unavailable",
}
ROUTERS = ("utility", "difficulty", "oracle")


def _canonical_state(x: object) -> str:
    s = str(x).strip().lower().replace("_", "-")
    aliases = {
        "recent-visible": "recent-visible",
        "long-horizon-only": "long-horizon-only",
        "unseen": "unseen",
    }
    if s not in aliases:
        raise ValueError(f"unknown relationship state: {x!r}")
    return aliases[s]


def _as_bool_array(s: pd.Series) -> np.ndarray:
    if pd.api.types.is_bool_dtype(s.dtype):
        return s.to_numpy(dtype=bool, copy=False)
    if pd.api.types.is_numeric_dtype(s.dtype):
        x = s.to_numpy()
        if not np.isin(x, [0, 1]).all():
            raise ValueError(f"non-binary numeric values in {s.name}")
        return x.astype(bool, copy=False)
    norm = s.astype(str).str.strip().str.lower()
    mapping = {"true": True, "false": False, "1": True, "0": False}
    bad = sorted(set(norm) - set(mapping))
    if bad:
        raise ValueError(f"unrecognized boolean values in {s.name}: {bad[:5]}")
    return norm.map(mapping).to_numpy(dtype=bool)


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


def _state_summary(dev: pd.DataFrame, n_boot: int) -> pd.DataFrame:
    rows: list[dict] = []
    n = len(dev)
    for j, state in enumerate(STATE_ORDER):
        g = dev.loc[dev.relationship_state == state]
        if g.empty:
            raise RuntimeError(f"empty relationship state: {state}")
        delta = g.memory_delta_ndcg10.to_numpy(np.float64)
        ci = _bootstrap_mean(delta, SEED + 10 + j, n_boot)
        rows.append(
            {
                "relationship_state": state,
                "evidence_state": STATE_LABEL[state],
                "n": int(len(g)),
                "prevalence": float(len(g) / n),
                "base_ndcg10": float(g.base_ndcg10.mean()),
                "memory_ndcg10": float(g.memory_ndcg10.mean()),
                "memory_minus_base": ci["mean"],
                "ci95_low": ci["ci95_low"],
                "ci95_high": ci["ci95_high"],
                "positive_delta_fraction": float((delta > 0).mean()),
            }
        )
    out = pd.DataFrame(rows)
    if int(out.n.sum()) != n or not np.isclose(out.prevalence.sum(), 1.0, atol=1e-12):
        raise RuntimeError("relationship-state partition is not exhaustive")
    weighted = float((out.prevalence * out.memory_minus_base).sum())
    overall = float(dev.memory_delta_ndcg10.mean())
    if not np.isclose(weighted, overall, atol=1e-12, rtol=0.0):
        raise RuntimeError(f"state decomposition mismatch: weighted={weighted} overall={overall}")
    return out


def _selection_composition(dev: pd.DataFrame, state_summary: pd.DataFrame) -> pd.DataFrame:
    prevalence = state_summary.set_index("relationship_state").prevalence.to_dict()
    use_cols = {
        "utility": "use_utility",
        "difficulty": "use_difficulty",
        "oracle": "use_oracle_exact_k",
    }
    masks = {name: _as_bool_array(dev[col]) for name, col in use_cols.items()}
    k_u = int(masks["utility"].sum())
    k_d = int(masks["difficulty"].sum())
    k_o = int(masks["oracle"].sum())
    if k_u != k_d or k_u != k_o:
        raise RuntimeError(f"exact-budget guard failed: utility={k_u}, difficulty={k_d}, oracle={k_o}")
    if k_u != EXPECTED_K:
        raise RuntimeError(f"frozen DEV invocation budget changed: got={k_u}, expected={EXPECTED_K}")

    rows: list[dict] = []
    for router in ROUTERS:
        mask = masks[router]
        selected_n = int(mask.sum())
        selected = dev.loc[mask]
        for state in STATE_ORDER:
            g = selected.loc[selected.relationship_state == state]
            share = float(len(g) / selected_n)
            prev = float(prevalence[state])
            rows.append(
                {
                    "router": router,
                    "selected_n": selected_n,
                    "invocation_rate": float(selected_n / len(dev)),
                    "relationship_state": state,
                    "evidence_state": STATE_LABEL[state],
                    "state_n_selected": int(len(g)),
                    "selection_share": share,
                    "overall_state_prevalence": prev,
                    "enrichment_ratio": float(share / prev) if prev > 0 else None,
                    "realized_delta_mean": float(g.memory_delta_ndcg10.mean()) if len(g) else None,
                    "positive_delta_fraction": float((g.memory_delta_ndcg10 > 0).mean()) if len(g) else None,
                }
            )
    return pd.DataFrame(rows)


def _reconstruct_twitch_features(dev: pd.DataFrame, twitch_csv: Path) -> tuple[np.ndarray, np.ndarray, dict]:
    raw = pd.read_csv(
        twitch_csv,
        header=None,
        names=["user", "stream", "streamer", "start", "stop"],
        usecols=[0, 2, 3, 4],
    )
    raw["row"] = np.arange(len(raw), dtype=np.int64)
    raw["uid"] = pd.factorize(raw.user, sort=False)[0].astype(np.int64) + 1
    raw["sid"] = pd.factorize(raw.streamer, sort=False)[0].astype(np.int64) + 1

    users = raw.uid.to_numpy(np.int64, copy=False)
    starts = raw.start.to_numpy(np.int64, copy=False)
    sids = raw.sid.to_numpy(np.int64, copy=False)
    rows = raw.row.to_numpy(np.int64, copy=False)

    # User histories: one global stable sort, then O(log n) cutoff per frozen DEV event.
    uorder = np.lexsort((rows, starts, users))
    su, ss = users[uorder], starts[uorder]
    uu, first, counts = np.unique(su, return_index=True, return_counts=True)
    ubounds = {int(u): (int(f), int(f + c)) for u, f, c in zip(uu, first, counts)}

    # Time-safe creator exposure proxy: interactions with the target creator strictly before target time.
    sorder = np.lexsort((rows, starts, sids))
    cs, ct = sids[sorder], starts[sorder]
    creators, cfirst, ccounts = np.unique(cs, return_index=True, return_counts=True)
    cbounds = {int(s): (int(f), int(f + c)) for s, f, c in zip(creators, cfirst, ccounts)}

    history_len = np.empty(len(dev), dtype=np.int64)
    creator_prior_exposure = np.empty(len(dev), dtype=np.int64)
    missing_users = 0
    missing_creators = 0
    for i, r in enumerate(dev.itertuples(index=False)):
        uid = int(r.user_id)
        sid = int(r.target_streamer)
        t = int(r.target_step)
        if uid not in ubounds:
            missing_users += 1
            history_len[i] = -1
        else:
            lo, hi = ubounds[uid]
            history_len[i] = int(np.searchsorted(ss[lo:hi], t, side="left"))
        if sid not in cbounds:
            missing_creators += 1
            creator_prior_exposure[i] = -1
        else:
            lo, hi = cbounds[sid]
            creator_prior_exposure[i] = int(np.searchsorted(ct[lo:hi], t, side="left"))

    mismatch = int(np.sum(history_len != dev.history_len.to_numpy(np.int64)))
    meta = {
        "raw_rows": int(len(raw)),
        "missing_users": int(missing_users),
        "missing_creators": int(missing_creators),
        "history_len_mismatches": mismatch,
    }
    if missing_users or missing_creators or mismatch:
        raise RuntimeError(f"Twitch reconstruction mismatch: {meta}")
    return history_len, creator_prior_exposure, meta


def _quantile_groups(s: pd.Series, max_bins: int = 4) -> pd.Series:
    x = pd.to_numeric(s, errors="raise")
    if x.isna().any():
        raise ValueError(f"NaN in stratification variable {s.name}")
    nunique = int(x.nunique(dropna=True))
    if nunique <= 1:
        return pd.Series(pd.Categorical(["all"] * len(x), categories=["all"]), index=x.index)
    q = min(int(max_bins), nunique)
    try:
        bins = pd.qcut(x, q=q, duplicates="drop")
        return bins.astype(str)
    except ValueError:
        return pd.Series(["all"] * len(x), index=x.index, dtype="object")


def _alternative_explanations(dev: pd.DataFrame, n_boot: int) -> pd.DataFrame:
    long = dev.loc[dev.relationship_state == "long-horizon-only"].copy()
    if long.empty:
        raise RuntimeError("no long-horizon-only events")
    specs = (
        "history_len",
        "creator_prior_exposure_count",
        "candidate_count",
        "repeat_rate",
    )
    rows: list[dict] = []
    for vi, var in enumerate(specs):
        group = _quantile_groups(long[var], max_bins=4)
        tmp = long.assign(_stratum=group.to_numpy())
        for gi, (label, g) in enumerate(tmp.groupby("_stratum", sort=True, observed=True)):
            delta = g.memory_delta_ndcg10.to_numpy(np.float64)
            ci = _bootstrap_mean(delta, SEED + 1000 + 100 * vi + gi, n_boot)
            v = g[var].to_numpy(np.float64)
            rows.append(
                {
                    "variable": var,
                    "stratum": str(label),
                    "n": int(len(g)),
                    "variable_min": float(np.min(v)),
                    "variable_median": float(np.median(v)),
                    "variable_max": float(np.max(v)),
                    "memory_minus_base": ci["mean"],
                    "ci95_low": ci["ci95_low"],
                    "ci95_high": ci["ci95_high"],
                    "positive_delta_fraction": float((delta > 0).mean()),
                }
            )
    return pd.DataFrame(rows)


def _self_test() -> None:
    x = np.asarray([-1.0, 0.0, 1.0, 2.0])
    b = _bootstrap_mean(x, seed=7, n_boot=50, chunk=8)
    assert b["n"] == 4 and np.isclose(b["mean"], 0.5)
    assert _canonical_state("long_horizon_only") == "long-horizon-only"
    assert _as_bool_array(pd.Series(["True", "False", "1", "0"])).tolist() == [True, False, True, False]
    q = _quantile_groups(pd.Series([1, 1, 2, 3, 4, 5], name="x"))
    assert len(q) == 6
    toy = pd.DataFrame(
        {
            "relationship_state": ["recent-visible", "long-horizon-only", "unseen"] * 2,
            "base_ndcg10": [0.1] * 6,
            "memory_ndcg10": [0.0, 0.3, 0.0] * 2,
            "memory_delta_ndcg10": [-0.1, 0.2, -0.1] * 2,
        }
    )
    st = _state_summary(toy, n_boot=50)
    assert np.isclose((st.prevalence * st.memory_minus_base).sum(), toy.memory_delta_ndcg10.mean())
    print("self-test: PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-oof", type=Path)
    ap.add_argument("--twitch-csv", type=Path)
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--n-boot", type=int, default=3000)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        _self_test()
        return
    if args.dev_oof is None or args.twitch_csv is None or args.out_dir is None:
        ap.error("--dev-oof, --twitch-csv, and --out-dir are required unless --self-test is used")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    dev = pd.read_csv(args.dev_oof)
    required = {
        "user_id", "target_step", "target_streamer", "relationship_horizon",
        "history_len", "candidate_count", "repeat_rate",
        "base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10",
        "use_utility", "use_difficulty", "use_oracle_exact_k",
    }
    missing = sorted(required - set(dev.columns))
    if missing or len(dev) != EXPECTED_N or dev.user_id.duplicated().any():
        raise RuntimeError(f"bad frozen DEV: missing={missing}, n={len(dev)}, duplicate_users={dev.user_id.duplicated().any()}")
    numeric = [
        "history_len", "candidate_count", "repeat_rate", "base_ndcg10",
        "memory_ndcg10", "memory_delta_ndcg10",
    ]
    if not np.isfinite(dev[numeric].to_numpy(np.float64)).all():
        raise RuntimeError("non-finite frozen DEV values")

    dev["relationship_state"] = dev.relationship_horizon.map(_canonical_state)
    reconstructed_history, creator_exposure, reconstruction = _reconstruct_twitch_features(dev, args.twitch_csv)
    dev["reconstructed_history_len"] = reconstructed_history
    dev["creator_prior_exposure_count"] = creator_exposure

    state = _state_summary(dev, args.n_boot)
    selection = _selection_composition(dev, state)
    alternatives = _alternative_explanations(dev, args.n_boot)

    state.to_csv(args.out_dir / "state_summary.csv", index=False)
    selection.to_csv(args.out_dir / "selection_composition.csv", index=False)
    alternatives.to_csv(args.out_dir / "alternative_explanations.csv", index=False)

    k = int(_as_bool_array(dev.use_utility).sum())
    report = {
        "experiment": "kbs_twitch_evidence_state_closure",
        "scope": "frozen P1.2 DEV OOF only",
        "test_ranking_inspected": False,
        "n_dev": int(len(dev)),
        "exact_matched_budget_k": k,
        "exact_matched_budget_rate": float(k / len(dev)),
        "history_reconstruction": reconstruction,
        "overall_memory_minus_base": float(dev.memory_delta_ndcg10.mean()),
        "state_weighted_reconstruction": float((state.prevalence * state.memory_minus_base).sum()),
        "state_rows": state.to_dict(orient="records"),
        "selection_rows": selection.to_dict(orient="records"),
        "alternative_explanation_rows": alternatives.to_dict(orient="records"),
        "guardrails": [
            "No P1.3 TEST artifact is read or required.",
            "Relationship-state labels are analysis-only and are not selector features.",
            "Utility, Difficulty, and Oracle composition use the frozen exact matched budget.",
            "No result-sign criterion is used for workflow success.",
        ],
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
