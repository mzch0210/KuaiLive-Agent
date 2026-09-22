from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path

import numpy as np
import torch
import torch.optim as optim

# This script is executed from a pinned checkout of the official JRappaz/liverec
# repository, with this file copied into that checkout. It intentionally reuses
# the official arguments/data/model/eval modules and changes only the terminal
# control flow: model selection is dev-only and test ranking is not executed.
from arguments import arg_parse, print_args
from data import get_dataloaders, load_data
from eval import compute_recall, print_scores
from models import get_model_type


def _py(v):
    if isinstance(v, dict):
        return {str(k): _py(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_py(x) for x in v]
    if isinstance(v, (np.floating, np.integer)):
        return v.item()
    if torch.is_tensor(v):
        return v.detach().cpu().item() if v.numel() == 1 else v.detach().cpu().tolist()
    return v


def _runtime_info(device: torch.device) -> dict:
    info = {
        "torch_version": torch.__version__,
        "cuda_build": torch.version.cuda,
        "cuda_available": bool(torch.cuda.is_available()),
        "cudnn_version": torch.backends.cudnn.version(),
        "device": str(device),
    }
    if device.type == "cuda":
        idx = device.index if device.index is not None else torch.cuda.current_device()
        props = torch.cuda.get_device_properties(idx)
        info.update(
            {
                "gpu_name": torch.cuda.get_device_name(idx),
                "gpu_capability": [int(props.major), int(props.minor)],
                "gpu_total_memory_bytes": int(props.total_memory),
                "gpu_index": int(idx),
            }
        )
    return info


def main() -> None:
    args = arg_parse()
    print_args(args)

    # Reproducibility controls missing from the original main.py but consistent
    # with its exposed --seed argument. They do not change task/model semantics.
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    args.device = torch.device(args.device)
    if args.device.type == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA execution requested but torch.cuda.is_available() is False")
        torch.cuda.manual_seed_all(args.seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    Path(args.model_path).mkdir(parents=True, exist_ok=True)
    Path(args.cache_dir).mkdir(parents=True, exist_ok=True)

    model_path, model_cls = get_model_type(args)
    data_fu = load_data(args)
    train_loader, val_loader, _test_loader = get_dataloaders(data_fu, args)

    model = model_cls(args).to(args.device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.l2)

    best_val_h1 = -math.inf
    best_epoch = -1
    best_scores = None
    remaining = args.early_stop

    print("training (dev-only freeze; test ranking intentionally disabled)...")
    print(json.dumps({"runtime": _runtime_info(args.device)}, indent=2))
    for epoch in range(args.num_epochs):
        loss_all = 0.0
        loss_cnt = 0
        model.train()

        for data in train_loader:
            data = data.to(args.device)
            optimizer.zero_grad()
            loss = model.train_step(data)
            if torch.isnan(loss):
                raise RuntimeError(f"NaN loss at epoch {epoch}")
            loss.backward()
            optimizer.step()
            loss_all += float(loss.detach().cpu().item())
            loss_cnt += int((data[:, :, 5] != 0).sum().detach().cpu().item())

        scores = compute_recall(model, val_loader, args, maxit=500)
        mean_loss = loss_all / max(loss_cnt, 1)
        print(f"Epoch: {epoch:03d}, Loss: {mean_loss:.8f}")
        print_scores(scores)

        h1 = float(scores["all"]["h01"])
        if h1 > best_val_h1:
            best_val_h1 = h1
            best_epoch = epoch
            best_scores = _py(scores)
            torch.save(model.state_dict(), model_path)
            remaining = args.early_stop
        else:
            remaining -= 1
            if remaining == 0:
                break

    if best_scores is None or best_epoch < 0:
        raise RuntimeError("No valid dev checkpoint was selected")

    report = {
        "experiment": "liverec_twitch100k_p1_official_base_dev_freeze",
        "official_commit": os.environ.get("LIVEREC_OFFICIAL_COMMIT"),
        "test_ranking_inspected": False,
        "selection_metric": "dev all h@1, matching official main.py",
        "best_epoch": int(best_epoch),
        "best_dev_h1": float(best_val_h1),
        "best_dev_scores": best_scores,
        "checkpoint": str(model_path),
        "runtime": _runtime_info(args.device),
        "config": {
            "seed": args.seed,
            "model": args.model,
            "fr_ctx": bool(args.fr_ctx),
            "fr_rep": bool(args.fr_rep),
            "lr": args.lr,
            "l2": args.l2,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "dim": args.K,
            "num_att": args.num_att,
            "num_att_ctx": args.num_att_ctx,
            "num_heads": args.num_heads,
            "num_heads_ctx": args.num_heads_ctx,
            "topk_att": args.topk_att,
            "early_stop": args.early_stop,
            "num_epochs_cap": args.num_epochs,
            "device": str(args.device),
        },
        "data": {
            "users": int(data_fu.user.nunique()),
            "streamers": int(data_fu.streamer.nunique()),
            "rows": int(len(data_fu)),
            "max_step": int(args.max_step),
            "pivot_1": int(args.pivot_1),
            "pivot_2": int(args.pivot_2),
            "max_available": int(args.max_avail),
        },
        "guardrail": "The official architecture/loss/data modules are reused. This stage selects a checkpoint from validation only and deliberately does not compute test ranking metrics.",
    }

    out = Path(os.environ.get("LIVEREC_REPORT", "p1_base_dev_freeze.json"))
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
