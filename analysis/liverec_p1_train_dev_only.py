from __future__ import annotations

import json
import math
import os
import random
import time
from itertools import islice
from pathlib import Path

import numpy as np
import torch
import torch.optim as optim
from torch.utils.data import DataLoader

# This script is executed from a pinned checkout of the official JRappaz/liverec
# repository, with this file copied into that checkout. It intentionally reuses
# the official arguments/data/model modules and preserves official ranking
# semantics, with exact-equivalence-guarded execution optimizations only.
from arguments import arg_parse, print_args
from data import get_dataloaders, load_data
from eval import compute_recall, metrics, print_scores
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


def _official_collate(batch, seq_len: int):
    """Same tensor layout and assignments as pinned LiveRec custom_collate."""
    bs = len(batch)
    feat_len = len(batch[0])
    batch_seq = torch.zeros(bs, seq_len, feat_len, dtype=torch.long)
    for ib, b in enumerate(batch):
        for ifeat, feat in enumerate(b):
            batch_seq[ib, b[0], ifeat] = feat
    return batch_seq


class _Collator:
    def __init__(self, seq_len: int):
        self.seq_len = int(seq_len)

    def __call__(self, batch):
        return _official_collate(batch, self.seq_len)


def _accelerate_loader(loader, args, workers: int):
    """Preserve dataset/order/batch/collate semantics; tune host-to-GPU feeding."""
    if args.device.type != "cuda":
        return loader

    workers = max(0, int(workers))
    kwargs = {
        "dataset": loader.dataset,
        "batch_size": loader.batch_size,
        "shuffle": False,
        "collate_fn": _Collator(args.seq_len),
        "num_workers": workers,
        "pin_memory": True,
        "drop_last": bool(loader.drop_last),
    }
    if workers > 0:
        kwargs.update({"persistent_workers": True, "prefetch_factor": 2})
    return DataLoader(**kwargs)


def _cuda_sync(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def _compute_recall_low_sync(model, loader, args, maxit=100000):
    """Exact official fr_ctx ranking with one rank transfer per batch.

    The pinned official evaluator synchronizes CUDA multiple times per user via
    Tensor.item() and Python tensor membership. Here repeat labels and timestamps
    are read from the still-CPU batch, while each user's candidate score vector
    and torch.argsort are kept identical to model.compute_rank. Ranks are copied
    to CPU once per batch. For non-fr_ctx configurations we fall back to the
    official evaluator.
    """
    if not args.fr_ctx:
        return compute_recall(model, loader, args, maxit=maxit)

    store = {"rrep": [], "rnew": [], "rall": [], "ratio": []}
    model.eval()

    with torch.no_grad():
        for i, data_cpu in enumerate(loader):
            # Repeat/new labels and target timestamps do not require CUDA.
            pos_cpu = data_cpu[:, :, 5]
            steps_cpu = data_cpu[:, -1, 6].tolist()
            repeat_flags = []
            for b in range(pos_cpu.shape[0]):
                avt = pos_cpu[b, :-1]
                avt = avt[avt != 0]
                is_rep = bool((avt == pos_cpu[b, -1]).any().item())
                repeat_flags.append(is_rep)

            data = data_cpu.to(args.device, non_blocking=bool(getattr(loader, "pin_memory", False)))
            inputs = data[:, :, 3]
            pos = data[:, :, 5]

            feats = model(inputs)
            ctx, batch_inds = model.get_ctx_att(data, feats)

            rank_tensors = []
            for b in range(inputs.shape[0]):
                step = int(steps_cpu[b])
                av_len = len(args.ts[step])

                # args.av_tens was built directly from args.ts in pinned data.py;
                # slicing its row avoids a per-user CPU->GPU tensor construction.
                av = args.av_tens[step, :av_len]

                # This is the exact fr_ctx scoring branch from LiveRec.compute_rank.
                ctx_expand = torch.zeros(
                    args.av_tens.shape[1], args.K, device=args.device
                )
                ctx_expand[batch_inds[b, -1, :], :] = ctx[b, -1, :, :]
                scores = (feats[b, -1, :] * ctx_expand).sum(-1)
                scores = scores[:av_len]

                iseq = pos[b, -1] == av
                idx = torch.where(iseq)[0]
                rank_t = torch.where(torch.argsort(scores, descending=True) == idx)[0]
                if rank_t.numel() != 1:
                    raise RuntimeError(
                        f"Expected exactly one target rank, got {rank_t.numel()} at batch {i}, row {b}"
                    )
                rank_tensors.append(rank_t[0])

            # One device->host synchronization for the whole batch, rather than
            # one .item() per user as in the pinned official evaluator.
            ranks = torch.stack(rank_tensors).detach().cpu().tolist()
            for rank, is_rep in zip(ranks, repeat_flags):
                store["ratio"].append(float(is_rep))
                if is_rep:
                    store["rrep"].append(int(rank))
                else:
                    store["rnew"].append(int(rank))
                store["rall"].append(int(rank))

            # Preserve the official evaluator's break placement/semantics.
            if i > maxit:
                break

    return {
        "rep": metrics(store["rrep"]),
        "new": metrics(store["rnew"]),
        "all": metrics(store["rall"]),
        "ratio": np.mean(store["ratio"]),
    }


def _assert_eval_equivalence(model, val_loader, args, probe_batches: int = 2) -> dict:
    """Fail closed unless optimized ranking exactly matches official ranking."""
    batches = list(islice(iter(val_loader), probe_batches))
    if not batches:
        raise RuntimeError("Validation loader is empty; cannot verify evaluator equivalence")

    official = _py(compute_recall(model, batches, args, maxit=100000))
    optimized = _py(_compute_recall_low_sync(model, batches, args, maxit=100000))

    # Exact equality is intentional: both paths execute the same score expression
    # and per-user torch.argsort. No tolerance-based semantic drift is accepted.
    if official != optimized:
        raise RuntimeError(
            "Optimized evaluator failed exact equivalence guard:\n"
            + json.dumps({"official": official, "optimized": optimized}, indent=2)
        )
    return {
        "probe_batches": len(batches),
        "probe_examples": int(sum(batch.shape[0] for batch in batches)),
        "exact_match": True,
    }


def main() -> None:
    args = arg_parse()
    print_args(args)

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    args.device = torch.device(args.device)
    if args.device.type == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA execution requested but torch.cuda.is_available() is False")
        torch.cuda.manual_seed_all(args.seed)
        # Deliberately preserve deterministic numerical settings. No AMP, TF32,
        # cudnn autotuning, torch.compile, batch-size or optimizer changes.
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    Path(args.model_path).mkdir(parents=True, exist_ok=True)
    Path(args.cache_dir).mkdir(parents=True, exist_ok=True)

    model_path, model_cls = get_model_type(args)
    data_fu = load_data(args)
    train_loader, val_loader, _test_loader = get_dataloaders(data_fu, args)

    requested_workers = int(os.environ.get("LIVEREC_NUM_WORKERS", "0"))
    train_loader = _accelerate_loader(train_loader, args, requested_workers)
    val_loader = _accelerate_loader(val_loader, args, requested_workers)
    non_blocking = bool(args.device.type == "cuda" and getattr(train_loader, "pin_memory", False))

    model = model_cls(args).to(args.device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.l2)

    execution = {
        "num_workers": int(getattr(train_loader, "num_workers", 0)),
        "pin_memory": bool(getattr(train_loader, "pin_memory", False)),
        "persistent_workers": bool(getattr(train_loader, "persistent_workers", False)),
        "prefetch_factor": getattr(train_loader, "prefetch_factor", None),
        "non_blocking_h2d": non_blocking,
        "per_batch_train_gpu_cpu_sync_removed": True,
        "batched_validation_rank_transfer": bool(args.fr_ctx),
        "amp": False,
        "tf32_override": False,
        "torch_compile": False,
        "batch_size_changed": False,
    }

    print("training (dev-only freeze; test ranking intentionally disabled)...")
    print(json.dumps({"runtime": _runtime_info(args.device), "execution": execution}, indent=2))

    # Verify optimized evaluator before it is allowed to influence checkpoint
    # selection. This uses the untrained model in eval mode and does not consume
    # randomness because dropout is disabled.
    eval_guard = _assert_eval_equivalence(model, val_loader, args, probe_batches=2)
    print(json.dumps({"evaluation_equivalence_guard": eval_guard}, indent=2))

    best_val_h1 = -math.inf
    best_epoch = -1
    best_scores = None
    remaining = args.early_stop
    epoch_timings = []

    for epoch in range(args.num_epochs):
        if args.device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(args.device)
        _cuda_sync(args.device)
        train_t0 = time.perf_counter()

        # Device-side reporting accumulators eliminate successful-run host syncs
        # inside the batch loop. They never participate in gradient computation.
        loss_sum = torch.zeros((), device=args.device, dtype=torch.float64)
        nan_seen = torch.zeros((), device=args.device, dtype=torch.bool)
        loss_cnt = 0
        model.train()

        for data in train_loader:
            # Same target count as before, performed while tensor remains on CPU.
            loss_cnt += int((data[:, :, 5] != 0).sum().item())
            data = data.to(args.device, non_blocking=non_blocking)

            optimizer.zero_grad()
            loss = model.train_step(data)
            nan_seen = nan_seen | torch.isnan(loss.detach())
            loss.backward()
            optimizer.step()
            loss_sum = loss_sum + loss.detach().to(torch.float64)

        _cuda_sync(args.device)
        train_seconds = time.perf_counter() - train_t0

        if bool(nan_seen.item()):
            raise RuntimeError(f"NaN loss observed during epoch {epoch}")

        val_t0 = time.perf_counter()
        scores = _compute_recall_low_sync(model, val_loader, args, maxit=500)
        _cuda_sync(args.device)
        val_seconds = time.perf_counter() - val_t0

        mean_loss = float(loss_sum.item()) / max(loss_cnt, 1)
        peak_mem = None
        if args.device.type == "cuda":
            peak_mem = int(torch.cuda.max_memory_allocated(args.device))

        epoch_record = {
            "epoch": int(epoch),
            "train_seconds": float(train_seconds),
            "val_seconds": float(val_seconds),
            "peak_cuda_memory_bytes": peak_mem,
            "dev_h1": float(scores["all"]["h01"]),
            "dev_ndcg10": float(scores["all"]["ndcg10"]),
        }
        epoch_timings.append(epoch_record)

        print(f"Epoch: {epoch:03d}, Loss: {mean_loss:.8f}")
        print_scores(scores)
        print(json.dumps({"timing": epoch_record}))

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
        "execution": execution,
        "evaluation_equivalence_guard": eval_guard,
        "epoch_timings": epoch_timings,
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
        "guardrail": "Official architecture, loss, data split, candidate order, per-user torch.argsort ranking, batch size, optimizer and dev-H@1 checkpoint selection are unchanged. The optimized evaluator must exactly match the official evaluator on a pre-training probe before use. Test ranking remains deliberately disabled.",
    }

    out = Path(os.environ.get("LIVEREC_REPORT", "p1_base_dev_freeze.json"))
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
