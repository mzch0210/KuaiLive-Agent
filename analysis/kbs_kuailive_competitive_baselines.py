from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


def parse_list(text: str) -> np.ndarray:
    return np.asarray(ast.literal_eval(str(text)), dtype=np.int64)


def ndcg10(rank: int) -> float:
    return 0.0 if rank > 10 else float(1.0 / np.log2(rank + 1.0))


def deterministic_rank(items: np.ndarray, scores: np.ndarray) -> int:
    target_item = int(items[0])
    target_score = float(scores[0])
    better = int(np.sum(scores > target_score))
    ties = int(np.sum((scores == target_score) & (items < target_item)))
    return 1 + better + ties


def popularity_metrics(data_dir: Path) -> dict:
    train = pd.read_csv(data_dir / "train.csv", sep="\t")
    dev = pd.read_csv(data_dir / "dev.csv", sep="\t")
    test = pd.read_csv(data_dir / "test.csv", sep="\t")
    counts = train.item_id.astype(int).value_counts().to_dict()

    def evaluate(df: pd.DataFrame) -> tuple[float, float]:
        ndcgs, hits = [], []
        for r in df.itertuples(index=False):
            neg = parse_list(r.neg_items)
            items = np.concatenate(([int(r.item_id)], neg))
            scores = np.asarray([counts.get(int(i), 0) for i in items], dtype=np.float64)
            rank = deterministic_rank(items, scores)
            ndcgs.append(ndcg10(rank))
            hits.append(float(rank <= 10))
        return float(np.mean(ndcgs)), float(np.mean(hits))

    d_ndcg, d_hr = evaluate(dev)
    t_ndcg, t_hr = evaluate(test)
    return {
        "model": "Popularity",
        "source": "same_protocol_recomputed",
        "dev_ndcg10": d_ndcg,
        "dev_hr10": d_hr,
        "test_ndcg10": t_ndcg,
        "test_hr10": t_hr,
    }


def metric(text: str, name: str) -> float | None:
    # ReChorus releases/logging paths use both `NDCG@10:0.x` and
    # `NDCG@10=0.x`; accept either delimiter without changing metrics.
    m = re.search(rf"{re.escape(name)}@10\s*[:=]\s*([0-9.]+)", text or "")
    return float(m.group(1)) if m else None


def parse_rechorus_log(path: Path, model: str, config: str) -> dict:
    txt = path.read_text(errors="ignore")
    dev = re.findall(r"Dev\s+After Training:\s*\((.*?)\)", txt)
    test = re.findall(r"Test After Training:\s*\((.*?)\)", txt)
    best = re.findall(r"Best Iter\(dev\)=\s*(\d+).*?dev=\((.*?)\)", txt)
    d = dev[-1] if dev else (best[-1][1] if best else "")
    t = test[-1] if test else ""
    row = {
        "model": model,
        "config": config,
        "source": "same_protocol_gpu_training",
        "best_epoch": int(best[-1][0]) if best else None,
        "dev_ndcg10": metric(d, "NDCG"),
        "dev_hr10": metric(d, "HR"),
        "test_ndcg10": metric(t, "NDCG"),
        "test_hr10": metric(t, "HR"),
        "log": str(path),
    }
    if row["dev_ndcg10"] is None or row["test_ndcg10"] is None:
        raise RuntimeError(f"Could not parse dev/test NDCG@10 from {path}")
    return row


def best_by_dev(rows: list[dict]) -> dict:
    return max(rows, key=lambda r: float(r["dev_ndcg10"]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--dual-report", type=Path, required=True)
    ap.add_argument("--gru-log", type=Path, action="append", default=[])
    ap.add_argument("--tisas-log", type=Path, action="append", default=[])
    ap.add_argument("--contra-log", type=Path, action="append", default=[])
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    report = json.loads(args.dual_report.read_text())
    rows: list[dict] = [popularity_metrics(args.data_dir)]

    families = [
        ("GRU4Rec", args.gru_log),
        ("TiSASRec", args.tisas_log),
        ("ContraRec-BERT4Rec", args.contra_log),
    ]
    for model, paths in families:
        parsed = [parse_rechorus_log(p, model, p.stem) for p in paths]
        if parsed:
            rows.append(best_by_dev(parsed))

    rows.extend([
        {
            "model": "Room-SASRec",
            "source": "frozen_DualID_component",
            "dev_ndcg10": float(report["room_sasrec_dev_ndcg10"]),
            "test_ndcg10": float(report["room_sasrec_test_ndcg10"]),
            "dev_hr10": None,
            "test_hr10": None,
        },
        {
            "model": "Streamer-SASRec",
            "source": "frozen_DualID_component",
            "dev_ndcg10": float(report["streamer_sasrec_dev_ndcg10"]),
            "test_ndcg10": float(report["streamer_sasrec_test_ndcg10"]),
            "dev_hr10": None,
            "test_hr10": None,
        },
        {
            "model": "Dual-ID Base",
            "source": "frozen_primary_base",
            "dev_ndcg10": float(report["dual_id_dev_ndcg10"]),
            "test_ndcg10": float(report["dual_id_test_ndcg10"]),
            "dev_hr10": None,
            "test_hr10": None,
        },
    ])

    table = pd.DataFrame(rows)
    table = table.sort_values("test_ndcg10", ascending=False, kind="mergesort").reset_index(drop=True)
    table.insert(0, "test_rank", np.arange(1, len(table) + 1))
    table.to_csv(args.out_dir / "kuailive_strong_base_benchmark.csv", index=False)

    dual_row = table[table.model == "Dual-ID Base"].iloc[0]
    non_dual = table[table.model != "Dual-ID Base"]
    best_non_dual = non_dual.iloc[0] if len(non_dual) else None
    summary = {
        "experiment": "kbs_strong_base_competitiveness_kuailive",
        "selection_rule": "For newly trained model families, choose configuration by DEV NDCG@10 only; TEST is reporting-only.",
        "candidate_protocol": "same frozen legal active-room 575-candidate protocol",
        "new_model_families": [m for m, p in families if p],
        "dual_id_test_ndcg10": float(dual_row.test_ndcg10),
        "dual_id_rank": int(dual_row.test_rank),
        "n_compared_models": int(len(table)),
        "best_non_dual_model": None if best_non_dual is None else str(best_non_dual.model),
        "best_non_dual_test_ndcg10": None if best_non_dual is None else float(best_non_dual.test_ndcg10),
        "dual_minus_best_non_dual": None if best_non_dual is None else float(dual_row.test_ndcg10 - best_non_dual.test_ndcg10),
        "claim_guardrail": "This benchmark establishes that the scientific Base is a competitive reference, not that it is state of the art.",
    }
    (args.out_dir / "kuailive_strong_base_benchmark.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(table.to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
