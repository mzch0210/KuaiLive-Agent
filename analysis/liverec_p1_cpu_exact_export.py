from __future__ import annotations

"""CPU-only compatibility wrapper for the frozen P1.3 exporter.

The frozen GPU path uses a batched 2-D argsort after batched score construction.
On CPU, PyTorch may order exact score ties differently for a 2-D argsort than for
the pinned LiveRec per-event 1-D argsort.  This wrapper keeps the efficient single
batched model forward and confidence-feature computation, but computes each rank
with the exact per-event 1-D argsort semantics used by the pinned official path.
It is DEV-only in the hosted CPU compatibility workflow; the base exporter still
refuses CPU execution for the P1.3 test split.
"""

import numpy as np
import torch

import p1_test_export as export_mod
from p1_dev_memory_export import EPS


def cpu_official_rank_batched_outputs(model, data_cpu, args):
    if args.device.type != "cpu":
        raise RuntimeError("CPU exact-rank wrapper may only run on CPU")

    data = data_cpu.to(args.device)
    inputs = data[:, :, 3]
    pos = data[:, :, 5]
    xtsy = data[:, :, 6]
    feats = model(inputs)
    ctx, batch_inds = model.get_ctx_att(data, feats)

    final_feat = feats[:, -1, :]
    final_ctx = ctx[:, -1, :, :]
    final_inds = batch_inds[:, -1, :]
    top_scores = (final_ctx * final_feat[:, None, :]).sum(-1)

    bsz = inputs.shape[0]
    max_av = args.av_tens.shape[1]
    scores = torch.zeros((bsz, max_av), dtype=top_scores.dtype, device=args.device)
    scores.scatter_(1, final_inds, top_scores)

    steps = xtsy[:, -1]
    step_list = steps.detach().cpu().tolist()
    lengths = torch.as_tensor([len(args.ts[int(x)]) for x in step_list], device=args.device)
    ar = torch.arange(max_av, device=args.device).unsqueeze(0)
    valid = ar < lengths.unsqueeze(1)
    masked_scores = scores.masked_fill(~valid, -torch.inf)

    av_rows = args.av_tens[steps, :]
    target_mask = av_rows == pos[:, -1].unsqueeze(1)
    if not bool(target_mask.any(dim=1).all().item()):
        raise RuntimeError("At least one dev target is not in the legal active candidate set")
    target_pos = target_mask.to(torch.int64).argmax(dim=1)

    # Critical CPU compatibility detail: rank each real candidate vector with the
    # same 1-D torch.argsort call shape used by the pinned official evaluator.
    # This avoids CPU 2-D-vs-1-D tie-order differences while retaining one model
    # forward per batch.
    rank_list: list[int] = []
    for b in range(bsz):
        length = int(lengths[b].item())
        order_b = torch.argsort(scores[b, :length], descending=True)
        rank_b = torch.where(order_b == target_pos[b])[0]
        if rank_b.numel() != 1:
            raise RuntimeError("CPU exact-rank path found non-unique target rank")
        rank_list.append(int(rank_b.item()))
    ranks = np.asarray(rank_list, dtype=np.int64)

    # Confidence features intentionally retain the frozen P1.2 batched score
    # semantics.  Only the raw rank tie-order path differs on CPU.
    n = lengths.to(scores.dtype)
    s1 = scores.masked_fill(~valid, 0.0).sum(dim=1)
    s2 = scores.square().masked_fill(~valid, 0.0).sum(dim=1)
    mean = s1 / n
    var = torch.clamp(s2 / n - mean.square(), min=0.0)
    std = torch.sqrt(var)
    maxv = masked_scores.max(dim=1).values
    minv = scores.masked_fill(~valid, torch.inf).min(dim=1).values
    rng = maxv - minv
    top11 = torch.topk(masked_scores, k=11, dim=1).values

    shifted = masked_scores - maxv.unsqueeze(1)
    ex = torch.exp(torch.clamp(shifted, min=-60.0, max=0.0)).masked_fill(~valid, 0.0)
    z = ex.sum(dim=1, keepdim=True)
    prob = ex / z
    entropy = -(prob * torch.log(torch.clamp(prob, min=EPS))).sum(dim=1) / torch.log(n)
    top10_mass = torch.topk(prob, k=10, dim=1).values.sum(dim=1)

    conf = torch.stack(
        [
            std,
            rng,
            top11[:, 0] - top11[:, 1],
            top11[:, 0] - top11[:, 4],
            top11[:, 9] - top11[:, 10],
            (top11[:, 0] - mean) / torch.clamp(std, min=EPS),
            entropy,
            top10_mass,
        ],
        dim=1,
    )

    return (
        ranks,
        conf.detach().cpu().numpy(),
        steps.detach().cpu().numpy(),
        pos[:, -1].detach().cpu().numpy(),
        data_cpu[:, :, 3].numpy(),
        data_cpu[:, :, 5].numpy(),
    )


# Monkeypatch only the exporter module used in this process.  The CUDA P1.2/P1.3
# code remains unchanged on disk and retains its frozen implementation.
export_mod.batched_base_outputs = cpu_official_rank_batched_outputs


if __name__ == "__main__":
    export_mod.main()
