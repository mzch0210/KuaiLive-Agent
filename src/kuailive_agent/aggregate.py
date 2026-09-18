from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", type=Path, required=True)
    args = ap.parse_args()
    files = sorted(args.results_dir.glob("summary_seed*.csv"))
    if not files:
        raise FileNotFoundError("No summary_seed*.csv files")
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    metrics = [c for c in df.columns if c not in {"seed", "model", "users", "longview_users"}]
    agg = df.groupby("model", as_index=False).agg({**{m:["mean","std"] for m in metrics}, "users":"mean", "longview_users":"mean"})
    agg.columns = ["model" if c[0]=="model" else (c[0] if c[1]=="" else f"{c[0]}_{c[1]}") for c in agg.columns]
    agg = agg.sort_values("ndcg@10_mean", ascending=False)
    agg.to_csv(args.results_dir / "summary_across_seeds.csv", index=False)
    print(agg.to_string(index=False))

if __name__ == "__main__":
    main()
