from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from arguments import arg_parse
from data import load_data
from models import get_model_type

import liverec_p12_dev_memory as p12

ALLOWED_SEQ_LEN = {8, 32}
EXPECTED_DEV_TARGETS = 46878


def _validate_base_config(args, frozen: dict) -> None:
    if frozen.get("test_ranking_inspected") is not False:
        raise RuntimeError("context intervention requires a DEV-only base report")
    if frozen.get("official_commit") != os.environ.get("LIVEREC_OFFICIAL_COMMIT"):
        raise RuntimeError("official LiveRec commit mismatch")

    cfg = frozen.get("config", {})
    expected = {
        "seed": int(args.seed),
        "model": str(args.model),
        "fr_ctx": bool(args.fr_ctx),
        "fr_rep": bool(args.fr_rep),
        "lr": float(args.lr),
        "l2": float(args.l2),
        "batch_size": int(args.batch_size),
        "seq_len": int(args.seq_len),
        "dim": int(args.K),
        "num_att": int(args.num_att),
        "num_att_ctx": int(args.num_att_ctx),
        "num_heads": int(args.num_heads),
        "num_heads_ctx": int(args.num_heads_ctx),
        "topk_att": int(args.topk_att),
        "early_stop": int(args.early_stop),
        "num_epochs_cap": int(args.num_epochs),
    }
    for key, value in expected.items():
        got = cfg.get(key)
        if isinstance(value, float):
            if got is None or not np.isclose(float(got), value, rtol=0.0, atol=1e-15):
                raise RuntimeError(f"base config mismatch {key}: {got!r} != {value!r}")
        elif got != value:
            raise RuntimeError(f"base config mismatch {key}: {got!r} != {value!r}")


def _validate_data(data_fu: pd.DataFrame, args, frozen: dict) -> dict:
    observed = {
        "users": int(data_fu.user.nunique()),
        "streamers": int(data_fu.streamer.nunique()),
        "rows": int(len(data_fu)),
        "max_step": int(args.max_step),
        "pivot_1": int(args.pivot_1),
        "pivot_2": int(args.pivot_2),
    }
    expected = frozen.get("data", {})
    for key, value in observed.items():
        if int(expected.get(key, -1)) != value:
            raise RuntimeError(f"data mismatch {key}: {expected.get(key)!r} != {value!r}")
    return observed


def main() -> None:
    args = arg_parse()
    args.device = torch.device(args.device)
    if args.device.type != "cuda" or not torch.cuda.is_available():
        raise RuntimeError("context-length intervention evaluation requires CUDA")
    if not args.fr_ctx or not args.fr_rep:
        raise RuntimeError("context-length intervention must preserve fr_ctx+fr_rep")
    if int(args.seq_len) not in ALLOWED_SEQ_LEN:
        raise RuntimeError(f"only DEV-only intervention lengths {sorted(ALLOWED_SEQ_LEN)} are allowed")

    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    base_report_path = Path(os.environ["LIVEREC_BASE_REPORT"])
    checkpoint_path = Path(os.environ["LIVEREC_BASE_CHECKPOINT"])
    out_dir = Path(os.environ.get("LIVEREC_CONTEXT_OUT", f"context_len_{args.seq_len}"))
    out_dir.mkdir(parents=True, exist_ok=True)

    frozen = json.loads(base_report_path.read_text())
    _validate_base_config(args, frozen)

    data_fu = load_data(args)
    data_meta = _validate_data(data_fu, args, frozen)
    workers = int(os.environ.get("LIVEREC_NUM_WORKERS", "4"))
    val_loader = p12._make_val_loader(data_fu, args, workers)

    _model_path, model_cls = get_model_type(args)
    model = model_cls(args).to(args.device)
    state = torch.load(checkpoint_path, map_location=args.device, weights_only=True)
    model.load_state_dict(state, strict=True)
    model.eval()

    sparse_guard = p12._assert_sparse_equivalence(model, val_loader, args, probe_batches=2)
    events = p12._score_frozen_base(model, val_loader, args)
    base_guard = p12._assert_frozen_base_metrics(events, frozen)
    events, history_meta = p12._add_state_and_memory(events, data_fu, args)

    if len(events) != EXPECTED_DEV_TARGETS or events.user_id.duplicated().any():
        raise RuntimeError(
            f"unexpected DEV event coverage: n={len(events)}, duplicate_users={events.user_id.duplicated().any()}"
        )
    horizon_counts = events.relationship_horizon.value_counts().to_dict()
    expected_states = {"recent-visible", "long-horizon-only", "unseen"}
    if set(horizon_counts) != expected_states or sum(horizon_counts.values()) != len(events):
        raise RuntimeError(f"relationship-state partition mismatch: {horizon_counts}")

    feature_cols = list(dict.fromkeys(p12.STATE_FEATURES + p12.CONF_FEATURES))
    if events[feature_cols].isna().any().any():
        raise RuntimeError("NaN in DEV intervention features")
    if np.isinf(events[feature_cols].to_numpy(np.float64)).any():
        raise RuntimeError("infinite value in DEV intervention features")

    summary = p12._summarize(events)
    cols = [
        "user_id",
        "target_streamer",
        "target_step",
        "candidate_count",
        "official_repeat",
        "recent_visible",
        "relationship_horizon",
        "base_rank0",
        "memory_rank0",
        "base_ndcg10",
        "memory_ndcg10",
        "memory_delta_ndcg10",
        "history_len",
    ] + feature_cols
    cols = list(dict.fromkeys(cols))
    events[cols].to_csv(out_dir / "dev_events.csv.gz", index=False, compression="gzip")

    report = {
        "experiment": "kbs_liverec_context_length_intervention_dev_only",
        "official_commit": os.environ.get("LIVEREC_OFFICIAL_COMMIT"),
        "controller_sha": os.environ.get("GITHUB_SHA"),
        "test_ranking_inspected": False,
        "seq_len": int(args.seq_len),
        "base_best_epoch": int(frozen["best_epoch"]),
        "base_best_dev_h1": float(frozen["best_dev_h1"]),
        "data": data_meta,
        "relationship_state_definition": {
            "recent-visible": f"target streamer occurs in the exact LiveRec {args.seq_len}-step input context",
            "long-horizon-only": f"target absent from the {args.seq_len}-step Base context but present in chronological pre-target relationship history",
            "unseen": "target absent from both Base context and chronological pre-target relationship history",
        },
        "relationship_state_counts": {str(k): int(v) for k, v in horizon_counts.items()},
        "summary": summary,
        "history_meta": history_meta,
        "guards": {
            "dev_targets": int(len(events)),
            "test_sequence_materialized": False,
            "frozen_base_exact_metric_match": base_guard,
            "sparse_scoring_exact_match": sparse_guard,
            "only_intervention_variable": "seq_len",
            "allowed_seq_len": sorted(ALLOWED_SEQ_LEN),
        },
        "interpretation_guardrail": "This is a DEV-only intervention. It must not be used to select a new policy for the frozen P1.3 TEST.",
    }
    (out_dir / "report.json").write_text(json.dumps(p12._py(report), indent=2) + "\n")
    print(json.dumps(p12._py(report), indent=2))


if __name__ == "__main__":
    main()
