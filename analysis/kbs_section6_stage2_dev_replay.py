"""KBS Section 6 Phase-2 reproducibility: no-refit Twitch DEV OOF replay.

Get archived artifact 10688746451 from successful GitHub Actions run 35713931454,
extract it, and pass its root directory as --source-dir. This reads only DEV
events and frozen DEV OOF predictions, not Twitch TEST or checkpoints.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

EXPECTED = {
    "results/gate_features/kbs_gate_feature_family_oof.csv.gz":
        "25b5e560ce67d16221e483e9c18cad679eb28525ce0a8279ae91555726547627",
    "results/gate_features/kbs_gate_feature_family_ablation.csv":
        "58d835e0ae53c43fe1ae522fdefee83374ba4ae58900968ea741780cffe92e48",
    "results/memory_components/kbs_memory_component_dev_events.csv.gz":
        "b84e187290a7df2918e3bd050c4ab0a6a2baac611f72eb72f8616c7634c0644b",
    "results/memory_components/kbs_memory_component_horizon_ablation.csv":
        "cc97794c49431c547ccf08a29da96bc275a900ed78a9ae71674b748b05e0750a",
}
FAMILIES = ("state_only", "confidence_only", "full")
FRACTIONS = (0.05, 0.10, 0.15, 0.20, 0.30)
GROUPS = ("all", "recent_visible", "long_horizon_only", "unseen")
VARIANTS = ("popularity_only", "short_only", "long_only", "short_long", "full_memory")
ORIGINAL_K = 6563
N = 46878


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sample_intervals(x, replicates, seed):
    """Same-bootstrap-user resampling across *all* paired score contrasts."""
    n, d = x.shape
    rng = np.random.default_rng(seed)
    means = np.empty((replicates, d), dtype=np.float64)
    with threadpool_limits(limits=2):
        for pos in range(0, replicates, 64):
            b = min(64, replicates-pos)
            idx = rng.integers(0, n, size=(b,n), dtype=np.int32)
            local = (idx + np.arange(b,dtype=np.int32)[:,None]*n).ravel()
            counts = np.bincount(local, minlength=b*n).reshape(b,n)
            means[pos:pos+b] = counts.astype(np.float64) @ x / n
    return np.quantile(means, 0.025, axis=0), np.quantile(means, 0.975, axis=0)


def score_order(pred):
    if not np.isfinite(pred).all():
        raise RuntimeError("Nonfinite OOF scores")
    return np.lexsort((np.arange(len(pred)), -pred))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--budget-boot", type=int, default=3000)
    ap.add_argument("--component-boot", type=int, default=5000)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for rel, expected in EXPECTED.items():
        observed = digest(args.source_dir / rel)
        if observed != expected:
            raise RuntimeError(f"Archived source SHA mismatch for {rel}: {observed}")

    gate = pd.read_csv(args.source_dir / "results/gate_features/kbs_gate_feature_family_oof.csv.gz")
    orig = pd.read_csv(args.source_dir / "results/gate_features/kbs_gate_feature_family_ablation.csv").set_index("feature_family")
    if len(gate) != N or gate.user_id.duplicated().any():
        raise RuntimeError("Incorrect OOF user identity")
    base = gate.base_ndcg10.to_numpy(float)
    memory = gate.memory_ndcg10.to_numpy(float)
    delta = gate.memory_delta_ndcg10.to_numpy(float)
    if not np.isfinite(np.column_stack([base, memory, delta])).all() or np.max(np.abs(delta - (memory-base))) > 1e-12:
        raise RuntimeError("Original event ranking utility identity mismatch")

    order = {}
    for f in FAMILIES:
        order[f] = {}
        for target in ("utility", "difficulty"):
            p = gate[f"{f}_{target}_oof_pred"].to_numpy(float)
            o = score_order(p)
            original_mask = gate[f"{f}_{target}_exact_k"].to_numpy(bool)
            replay_mask = np.zeros(N,dtype=bool)
            replay_mask[o[:ORIGINAL_K]] = True
            if not np.array_equal(original_mask, replay_mask):
                raise RuntimeError(f"Original 6563-choice mask mismatch {f} {target}")
            order[f][target] = o
        replay_gain = np.where(gate[f"{f}_utility_exact_k"].to_numpy(bool),delta,0).mean()
        if abs(replay_gain-float(orig.loc[f,"utility_exact_k_gain_vs_base"])) > 1e-12:
            raise RuntimeError(f"Original family utility gain mismatch: {f}")

    budget_rows = []
    contrast_rows = []
    for budget in [*FRACTIONS, ORIGINAL_K/N]:
        k = ORIGINAL_K if abs(budget-ORIGINAL_K/N)<1e-15 else int(math.floor(budget*N+0.5))
        label = "historical_6563" if k==ORIGINAL_K else f"{round(100*budget)}pct"
        score_vectors = []
        names = []
        for fam in FAMILIES:
            for target in ("utility", "difficulty"):
                values=np.zeros(N,float)
                values[order[fam][target][:k]] = delta[order[fam][target][:k]]
                score_vectors.append(values)
                names.append((fam,target))
        matrix=np.column_stack(score_vectors)
        extras=np.column_stack([matrix[:,4]-matrix[:,0], matrix[:,4]-matrix[:,2], matrix[:,4]-matrix[:,5]])
        combined=np.column_stack([matrix,extras])
        low, high=sample_intervals(combined,args.budget_boot,20261010)
        for j,(fam,target) in enumerate(names):
            gain=float(matrix[:,j].mean())
            budget_rows.append({"budget":label,"k":k,"rate":k/N,"family":fam,
                "decision_target":target,"base_ndcg10":float(base.mean()),
                "selected_ndcg10":float(base.mean()+gain),"gain_vs_base":gain,
                "ci95_low":float(low[j]),"ci95_high":float(high[j]),
                "n_boot":args.budget_boot})
        for j,name in enumerate(("full_utility_minus_state_only_utility",
                                  "full_utility_minus_confidence_only_utility",
                                  "full_utility_minus_full_difficulty")):
            contrast_rows.append({"budget":label,"contrast":name,"mean":float(extras[:,j].mean()),
                "ci95_low":float(low[6+j]),"ci95_high":float(high[6+j]),
                "n_boot":args.budget_boot})
    pd.DataFrame(budget_rows).to_csv(args.out_dir/"budget_profile.csv",index=False)
    pd.DataFrame(contrast_rows).to_csv(args.out_dir/"budget_contrasts.csv",index=False)

    events=pd.read_csv(args.source_dir/"results/memory_components/kbs_memory_component_dev_events.csv.gz")
    component=pd.read_csv(args.source_dir/"results/memory_components/kbs_memory_component_horizon_ablation.csv")
    if len(events)!=N or events.user_id.duplicated().any():
        raise RuntimeError("Component-level events not uniquely paired")
    for row in component.itertuples(index=False):
        state=(np.ones(N,bool) if row.group=="all" else
               events.relationship_horizon.eq(row.group).to_numpy(bool))
        src=events[f"{row.variant}_ndcg10"].to_numpy(float)[state]
        base_values=events.base_ndcg10.to_numpy(float)[state]
        if int(state.sum()) != row.n or abs(src.mean()-row.ndcg10)>1e-12 or abs((src-base_values).mean()-row.delta_ndcg10)>1e-12:
            raise RuntimeError("Original 20-row component replay mismatch")
    pairs=[("long_only","full_memory"),("short_long","full_memory"),
           ("long_only","short_long"),("short_only","full_memory"),
           ("popularity_only","full_memory")]
    component_rows=[]
    for gi,g in enumerate(GROUPS):
        sel=np.ones(N,bool) if g=="all" else events.relationship_horizon.eq(g).to_numpy(bool)
        diff=np.column_stack([events[f"{a}_ndcg10"].to_numpy(float)[sel]
                              -events[f"{b}_ndcg10"].to_numpy(float)[sel] for a,b in pairs])
        low,high=sample_intervals(diff,args.component_boot,20261010+gi)
        for k,(a,b) in enumerate(pairs):
            component_rows.append({"group":g,"n_users":int(sel.sum()),"variant_a":a,"variant_b":b,
                "mean_ndcg10_a_minus_b":float(diff[:,k].mean()),
                "ci95_low":float(low[k]),"ci95_high":float(high[k]),"n_boot":args.component_boot})
    pd.DataFrame(component_rows).to_csv(args.out_dir/"component_pairwise.csv",index=False)
    report={"source_run":35713931454,"source_artifact":10688746451,
        "source_sha256":EXPECTED,"n_dev":N,"original_6563_masks":"all six exact replay",
        "original_20_component_means":"all exact to 1e-12","new_training":False,
        "new_TEST_access":False,"changed_frozen_policy":False,
        "budgets":list(FRACTIONS),"budget_bootstrap_replicates":args.budget_boot,
        "component_bootstrap_replicates":args.component_boot,
        "bootstrap_unit":"one DEV user-event; paired fixed masks/predictions",
        "bootstrap_scope":"pointwise exploratory CIs, no refitting or familywise adjustment",
        "tie_breaking":"descending OOF prediction, ascending original row index",
        "inferential_boundary":"DEV-only batch top-count diagnostics, not serving-policy or causal effects"}
    (args.out_dir/"replay_provenance.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PASS: 6 historical masks and 20 historical component means reproduced.")
    print(pd.DataFrame(budget_rows).query("decision_target=='utility'")[["budget","family","gain_vs_base"]].to_string(index=False))


if __name__=="__main__":
    main()
