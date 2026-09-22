from __future__ import annotations

import json
import math
import os
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

# Executed from the pinned official JRappaz/liverec checkout.
from arguments import arg_parse
from data import get_sequences, load_data
from models import get_model_type

EPS = 1e-12
SHORT_K = 10
SHORT_DECAY = 3.0
MEM_W_SHORT = 0.45
MEM_W_LONG = 0.45
MEM_W_POP = 0.10

CONF_FEATURES = [
    "base_score_std",
    "base_score_range",
    "base_margin12",
    "base_margin15",
    "base_margin1011",
    "base_top1_z",
    "base_entropy",
    "base_top10_mass",
]
STATE_FEATURES = [
    "log_history_len",
    "repeat_rate",
    "preference_entropy",
    "preference_drift",
    "time_regularity",
    "state_complexity",
]


def _py(v):
    if isinstance(v, dict):
        return {str(k): _py(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_py(x) for x in v]
    if isinstance(v, (np.integer, np.floating)):
        return v.item()
    if torch.is_tensor(v):
        return v.detach().cpu().item() if v.numel() == 1 else v.detach().cpu().tolist()
    return v


def _official_collate(batch, seq_len: int):
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


def _make_val_loader(data_fu, args, workers: int) -> DataLoader:
    """Materialize validation only; never construct test sequences in P1.2."""
    mu = 1000 if args.debug else int(10e9)
    val_ds = get_sequences(data_fu, args.pivot_1, args.pivot_2, args, mu)
    kwargs = dict(
        dataset=val_ds,
        batch_size=args.batch_size,
        shuffle=False,
        collate_fn=_Collator(args.seq_len),
        num_workers=max(0, int(workers)),
        pin_memory=(args.device.type == "cuda"),
        drop_last=False,
    )
    if kwargs["num_workers"] > 0:
        kwargs.update(persistent_workers=True, prefetch_factor=2)
    return DataLoader(**kwargs)


def _ndcg10_from_rank0(rank0):
    r = np.asarray(rank0, dtype=np.int64)
    out = np.zeros(r.shape[0], dtype=np.float64)
    m = r < 10
    out[m] = 1.0 / np.log2(r[m].astype(np.float64) + 2.0)
    return out


def _metrics_rank0(rank0):
    r = np.asarray(rank0, dtype=np.int64)
    if r.size == 0:
        return {k: None for k in ["h01", "h05", "h10", "ndcg01", "ndcg05", "ndcg10"]}
    return {
        "h01": float(np.mean(r < 1)),
        "h05": float(np.mean(r < 5)),
        "h10": float(np.mean(r < 10)),
        "ndcg01": float(np.mean(np.where(r < 1, 1.0 / np.log2(r + 2.0), 0.0))),
        "ndcg05": float(np.mean(np.where(r < 5, 1.0 / np.log2(r + 2.0), 0.0))),
        "ndcg10": float(np.mean(np.where(r < 10, 1.0 / np.log2(r + 2.0), 0.0))),
    }


def _sparse_scores(model, data, feats, ctx, batch_inds, args):
    """Exact algebraic equivalent of LiveRec's ctx_expand scoring without BxAxK allocation."""
    selected = (ctx[:, -1, :, :] * feats[:, -1, :].unsqueeze(1)).sum(-1)
    scores = torch.zeros(
        data.shape[0], args.av_tens.shape[1], device=args.device, dtype=selected.dtype
    )
    scores.scatter_(1, batch_inds[:, -1, :], selected)
    return scores


def _assert_sparse_equivalence(model, loader, args, probe_batches: int = 2):
    model.eval()
    checked_users = 0
    checked_batches = 0
    with torch.no_grad():
        for data_cpu in loader:
            data = data_cpu.to(args.device, non_blocking=bool(getattr(loader, "pin_memory", False)))
            inputs = data[:, :, 3]
            feats = model(inputs)
            ctx, batch_inds = model.get_ctx_att(data, feats)
            new_scores = _sparse_scores(model, data, feats, ctx, batch_inds, args)
            steps = data_cpu[:, -1, 6].tolist()
            for b, step in enumerate(steps):
                av_len = len(args.ts[int(step)])
                old_ctx = torch.zeros(args.av_tens.shape[1], args.K, device=args.device)
                old_ctx[batch_inds[b, -1, :], :] = ctx[b, -1, :, :]
                old_scores = (feats[b, -1, :] * old_ctx).sum(-1)[:av_len]
                ns = new_scores[b, :av_len]
                if not torch.equal(old_scores, ns):
                    raise RuntimeError(f"Sparse base scoring is not bit-exact at probe user {checked_users}")
                target = data[b, -1, 5]
                av = args.av_tens[int(step), :av_len]
                idx = torch.where(av == target)[0]
                if idx.numel() != 1:
                    raise RuntimeError("Target must occur exactly once in active candidates")
                r_old = torch.where(torch.argsort(old_scores, descending=True) == idx)[0]
                r_new = torch.where(torch.argsort(ns, descending=True) == idx)[0]
                if not torch.equal(r_old, r_new):
                    raise RuntimeError("Sparse base rank mismatch in equivalence probe")
                checked_users += 1
            checked_batches += 1
            if checked_batches >= probe_batches:
                break
    if checked_batches == 0:
        raise RuntimeError("Empty validation loader")
    return {"exact_match": True, "probe_batches": checked_batches, "probe_users": checked_users}


def _confidence_batch(scores_full, lengths):
    """Vectorized confidence features over ragged legal-active candidate sets."""
    bsz, width = scores_full.shape
    ar = torch.arange(width, device=scores_full.device).unsqueeze(0)
    valid = ar < lengths.unsqueeze(1)
    n = lengths.to(scores_full.dtype).clamp_min(1)

    z = scores_full * valid
    mean = z.sum(1) / n
    sq = (scores_full.square() * valid).sum(1) / n
    var = torch.clamp(sq - mean.square(), min=0.0)
    std = torch.sqrt(var)

    neg_inf = torch.tensor(float("-inf"), device=scores_full.device, dtype=scores_full.dtype)
    pos_inf = torch.tensor(float("inf"), device=scores_full.device, dtype=scores_full.dtype)
    vmax = scores_full.masked_fill(~valid, neg_inf).max(1).values
    vmin = scores_full.masked_fill(~valid, pos_inf).min(1).values
    vrange = vmax - vmin

    top = scores_full.masked_fill(~valid, neg_inf).topk(k=11, dim=1).values
    m12 = top[:, 0] - top[:, 1]
    m15 = top[:, 0] - top[:, 4]
    m1011 = top[:, 9] - top[:, 10]
    top1z = (top[:, 0] - mean) / std.clamp_min(EPS)

    shifted = scores_full - vmax.unsqueeze(1)
    ex = torch.exp(shifted).masked_fill(~valid, 0.0)
    denom = ex.sum(1, keepdim=True).clamp_min(EPS)
    prob = ex / denom
    entropy = -(prob * torch.log(prob.clamp_min(EPS))).sum(1)
    entropy = entropy / torch.log(n).clamp_min(EPS)
    top10_mass = prob.topk(k=10, dim=1).values.sum(1)

    return torch.stack([std, vrange, m12, m15, m1011, top1z, entropy, top10_mass], dim=1)


def _score_frozen_base(model, loader, args):
    rows = []
    model.eval()
    non_blocking = bool(args.device.type == "cuda" and getattr(loader, "pin_memory", False))
    with torch.no_grad():
        for data_cpu in loader:
            users = data_cpu[:, -1, 4].numpy().astype(np.int64, copy=False)
            targets = data_cpu[:, -1, 5].numpy().astype(np.int64, copy=False)
            steps = data_cpu[:, -1, 6].numpy().astype(np.int64, copy=False)
            inputs_cpu = data_cpu[:, :, 3].numpy()
            pos_cpu = data_cpu[:, :, 5].numpy()

            if np.any(steps < args.pivot_1) or np.any(steps >= args.pivot_2):
                raise RuntimeError("Validation scorer encountered a target outside the frozen dev window")

            official_repeat = []
            recent_visible = []
            for b in range(data_cpu.shape[0]):
                p = pos_cpu[b, :-1]
                official_repeat.append(bool(np.any(p[p != 0] == targets[b])))
                x = inputs_cpu[b]
                recent_visible.append(bool(np.any(x[x != 0] == targets[b])))

            data = data_cpu.to(args.device, non_blocking=non_blocking)
            inputs = data[:, :, 3]
            feats = model(inputs)
            ctx, batch_inds = model.get_ctx_att(data, feats)
            scores_full = _sparse_scores(model, data, feats, ctx, batch_inds, args)

            lengths_cpu = np.fromiter((len(args.ts[int(s)]) for s in steps), dtype=np.int64, count=len(steps))
            lengths = torch.as_tensor(lengths_cpu, device=args.device, dtype=torch.long)
            if torch.any(lengths < 11):
                raise RuntimeError("Confidence feature definition requires >=11 active candidates")
            conf = _confidence_batch(scores_full, lengths)

            rank_t = []
            for b in range(data_cpu.shape[0]):
                av_len = int(lengths_cpu[b])
                av = args.av_tens[int(steps[b]), :av_len]
                idx = torch.where(av == data[b, -1, 5])[0]
                if idx.numel() != 1:
                    raise RuntimeError(
                        f"Target availability mismatch user={int(users[b])} step={int(steps[b])} matches={idx.numel()}"
                    )
                rank = torch.where(
                    torch.argsort(scores_full[b, :av_len], descending=True) == idx
                )[0]
                if rank.numel() != 1:
                    raise RuntimeError("Expected exactly one base rank")
                rank_t.append(rank[0])

            packed = torch.cat(
                [torch.stack(rank_t).to(conf.dtype).unsqueeze(1), conf], dim=1
            ).detach().cpu().numpy()

            for b in range(data_cpu.shape[0]):
                rec = {
                    "user_id": int(users[b]),
                    "target_streamer": int(targets[b]),
                    "target_step": int(steps[b]),
                    "official_repeat": bool(official_repeat[b]),
                    "recent_visible": bool(recent_visible[b]),
                    "base_rank0": int(packed[b, 0]),
                }
                for j, name in enumerate(CONF_FEATURES, start=1):
                    rec[name] = float(packed[b, j])
                rows.append(rec)

    out = pd.DataFrame(rows)
    if out.empty or out.user_id.duplicated().any():
        raise RuntimeError("Expected exactly one dev target per user")
    out["base_ndcg10"] = _ndcg10_from_rank0(out.base_rank0.to_numpy())
    return out


def _assert_frozen_base_metrics(events: pd.DataFrame, frozen_report: dict):
    masks = {
        "all": np.ones(len(events), dtype=bool),
        "rep": events.official_repeat.to_numpy(bool),
        "new": ~events.official_repeat.to_numpy(bool),
    }
    got = {k: _metrics_rank0(events.loc[m, "base_rank0"].to_numpy()) for k, m in masks.items()}
    expected = frozen_report["best_dev_scores"]
    for split in ["all", "rep", "new"]:
        for metric in ["h01", "h05", "h10", "ndcg01", "ndcg05", "ndcg10"]:
            a = got[split][metric]
            b = float(expected[split][metric])
            if not math.isclose(a, b, rel_tol=0.0, abs_tol=1e-12):
                raise RuntimeError(
                    f"Frozen base reproduction mismatch {split}/{metric}: got={a} expected={b}"
                )
    ratio = float(events.official_repeat.mean())
    if not math.isclose(ratio, float(expected["ratio"]), rel_tol=0.0, abs_tol=1e-12):
        raise RuntimeError(f"Repeat ratio mismatch: got={ratio}, expected={expected['ratio']}")
    return {"exact_metric_match": True, "metrics": got, "repeat_ratio": ratio}


def _norm_entropy(items):
    n = len(items)
    if n <= 1:
        return 0.0
    _, counts = np.unique(items, return_counts=True)
    if counts.size <= 1:
        return 0.0
    p = counts.astype(np.float64) / counts.sum()
    return float(-(p * np.log(p)).sum() / math.log(counts.size))


def _js_divergence(a, b):
    if len(a) == 0 or len(b) == 0:
        return 0.0
    ca, cb = Counter(map(int, a)), Counter(map(int, b))
    keys = sorted(set(ca) | set(cb))
    pa = np.asarray([ca[k] for k in keys], dtype=np.float64)
    pb = np.asarray([cb[k] for k in keys], dtype=np.float64)
    pa /= pa.sum(); pb /= pb.sum(); m = 0.5 * (pa + pb)
    def kl(p, q):
        z = p > 0
        return float((p[z] * np.log2(p[z] / q[z])).sum())
    return 0.5 * kl(pa, m) + 0.5 * kl(pb, m)


def _timestep_regularity(starts):
    if len(starts) == 0:
        return 0.0
    phase = np.asarray(starts, dtype=np.float64) % 144.0  # 144 ten-minute bins/day
    ang = 2.0 * np.pi * phase / 144.0
    return float(np.hypot(np.cos(ang).mean(), np.sin(ang).mean()))


def _build_strict_histories(data_fu: pd.DataFrame, events: pd.DataFrame):
    """History rows must have completed strictly before the target starts."""
    target_step = events.set_index("user_id")["target_step"]
    cutoff = data_fu["user"].map(target_step)
    mask = cutoff.notna().to_numpy() & (data_fu["stop"].to_numpy() < cutoff.fillna(-1).to_numpy())
    hist = data_fu.loc[mask, ["user", "streamer", "start", "stop"]].copy()
    hist["_row"] = np.flatnonzero(mask)
    hist.sort_values(["user", "start", "_row"], kind="mergesort", inplace=True)

    info = {}
    for uid, g in hist.groupby("user", sort=False):
        items = g.streamer.to_numpy(dtype=np.int64, copy=False)
        starts = g.start.to_numpy(dtype=np.int64, copy=False)
        n = len(items)
        uniq, counts = np.unique(items, return_counts=True)
        maxc = int(counts.max()) if counts.size else 1
        long_vals = counts.astype(np.float64) / float(maxc)

        short_map = {}
        for dist, item in enumerate(items[-SHORT_K:][::-1]):
            val = math.exp(-dist / SHORT_DECAY)
            item = int(item)
            if val > short_map.get(item, 0.0):
                short_map[item] = val
        short_items = np.fromiter(short_map.keys(), dtype=np.int64, count=len(short_map))
        short_vals = np.fromiter(short_map.values(), dtype=np.float64, count=len(short_map))

        recent_n = min(10, max(2, n // 3)) if n >= 3 else max(1, n // 2)
        old = items[:-recent_n] if n > recent_n else items[:max(1, n // 2)]
        recent = items[-recent_n:] if recent_n else items

        info[int(uid)] = {
            "items": uniq.astype(np.int64, copy=False),
            "long_vals": long_vals,
            "short_items": short_items,
            "short_vals": short_vals,
            "history_len": int(n),
            "repeat_rate": float(1.0 - len(uniq) / max(n, 1)),
            "preference_entropy": _norm_entropy(items),
            "preference_drift": _js_divergence(old, recent) if len(old) and len(recent) else 0.0,
            "time_regularity": _timestep_regularity(starts),
        }
    return info, int(len(hist))


def _train_popularity(data_fu: pd.DataFrame, args):
    """Train-only popularity: rows completed before pivot_1, matching the frozen transfer rule."""
    tr = data_fu.loc[data_fu.stop < args.pivot_1, "streamer"].to_numpy(dtype=np.int64, copy=False)
    counts = np.bincount(tr, minlength=int(args.N) + 1).astype(np.float64)
    pop = np.zeros_like(counts)
    nz = counts > 0
    if np.any(nz):
        vals = np.log1p(counts[nz])
        lo, hi = float(vals.min()), float(vals.max())
        if hi > lo:
            pop[nz] = (vals - lo) / (hi - lo)
    return pop, int(len(tr))


def _add_state_and_memory(events: pd.DataFrame, data_fu: pd.DataFrame, args):
    hist_info, strict_hist_rows = _build_strict_histories(data_fu, events)
    pop, train_pop_rows = _train_popularity(data_fu, args)

    short_dense = np.zeros_like(pop, dtype=np.float64)
    long_dense = np.zeros_like(pop, dtype=np.float64)
    mem_rank = np.empty(len(events), dtype=np.int64)
    horizon = np.empty(len(events), dtype=object)
    state_rows = []

    for j, r in enumerate(events.itertuples(index=False)):
        uid = int(r.user_id); target = int(r.target_streamer); step = int(r.target_step)
        h = hist_info.get(uid)
        if h is None:
            hist_items = np.empty(0, dtype=np.int64)
            state = {
                "history_len": 0,
                "repeat_rate": 0.0,
                "preference_entropy": 0.0,
                "preference_drift": 0.0,
                "time_regularity": 0.0,
            }
            touched = np.empty(0, dtype=np.int64)
        else:
            hist_items = h["items"]
            long_dense[hist_items] = h["long_vals"]
            short_dense[h["short_items"]] = h["short_vals"]
            touched = hist_items
            state = {k: h[k] for k in ["history_len", "repeat_rate", "preference_entropy", "preference_drift", "time_regularity"]}

        cands = np.asarray(args.ts[step], dtype=np.int64)
        hit = np.flatnonzero(cands == target)
        if hit.size != 1:
            raise RuntimeError(f"Memory target availability mismatch user={uid} step={step} matches={hit.size}")
        scores = (
            MEM_W_SHORT * short_dense[cands]
            + MEM_W_LONG * long_dense[cands]
            + MEM_W_POP * pop[cands]
        )
        ts = float(scores[int(hit[0])])
        better = int(np.sum(scores > ts + EPS))
        ties = int(np.sum((np.abs(scores - ts) <= EPS) & (cands < target)))
        mem_rank[j] = better + ties

        if bool(r.recent_visible):
            horizon[j] = "recent-visible"
        elif h is not None and bool(np.any(hist_items == target)):
            horizon[j] = "long-horizon-only"
        else:
            horizon[j] = "unseen"

        state_rows.append(state)
        if touched.size:
            long_dense[touched] = 0.0
        if h is not None and h["short_items"].size:
            short_dense[h["short_items"]] = 0.0

    st = pd.DataFrame(state_rows)
    out = pd.concat([events.reset_index(drop=True), st], axis=1)
    out["relationship_horizon"] = horizon
    out["memory_rank0"] = mem_rank
    out["memory_ndcg10"] = _ndcg10_from_rank0(mem_rank)
    out["memory_delta_ndcg10"] = out.memory_ndcg10 - out.base_ndcg10
    out["log_history_len"] = np.log1p(out.history_len.astype(np.float64))

    out["entropy_pct"] = out.preference_entropy.rank(pct=True, method="average")
    out["drift_pct"] = out.preference_drift.rank(pct=True, method="average")
    out["history_pct"] = out.log_history_len.rank(pct=True, method="average")
    out["state_complexity"] = 0.4 * out.entropy_pct + 0.4 * out.drift_pct + 0.2 * out.history_pct
    out.drop(columns=["entropy_pct", "drift_pct", "history_pct"], inplace=True)

    return out, {"strict_history_rows": strict_hist_rows, "train_popularity_rows": train_pop_rows}


def _slice_summary(df: pd.DataFrame):
    if len(df) == 0:
        return {"n": 0}
    delta = df.memory_delta_ndcg10.to_numpy(np.float64)
    return {
        "n": int(len(df)),
        "base": _metrics_rank0(df.base_rank0.to_numpy()),
        "memory": _metrics_rank0(df.memory_rank0.to_numpy()),
        "memory_minus_base_ndcg10": float(delta.mean()),
        "positive_delta_fraction": float(np.mean(delta > 0)),
        "negative_delta_fraction": float(np.mean(delta < 0)),
    }


def _summarize(events: pd.DataFrame):
    return {
        "overall": _slice_summary(events),
        "repeat": _slice_summary(events[events.official_repeat]),
        "novel": _slice_summary(events[~events.official_repeat]),
        "relationship_horizon": {
            k: _slice_summary(events[events.relationship_horizon == k])
            for k in ["recent-visible", "long-horizon-only", "unseen"]
        },
    }


def main():
    args = arg_parse()
    args.device = torch.device(args.device)
    if args.device.type != "cuda" or not torch.cuda.is_available():
        raise RuntimeError("P1.2 workflow requires the frozen CUDA execution environment")
    if not (args.fr_ctx and args.fr_rep and args.seq_len == 16):
        raise RuntimeError("P1.2 must use the frozen LiveRec fr_ctx+fr_rep, seq_len=16 configuration")

    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    base_report_path = Path(os.environ["LIVEREC_BASE_REPORT"])
    checkpoint_path = Path(os.environ["LIVEREC_BASE_CHECKPOINT"])
    out_dir = Path(os.environ.get("LIVEREC_P12_OUT", "p12_dev"))
    out_dir.mkdir(parents=True, exist_ok=True)
    frozen = json.loads(base_report_path.read_text())
    if frozen.get("test_ranking_inspected") is not False:
        raise RuntimeError("Frozen base artifact does not certify untouched test ranking")
    if frozen.get("official_commit") != os.environ.get("LIVEREC_OFFICIAL_COMMIT"):
        raise RuntimeError("Frozen base official commit does not match P1.2 source pin")
    if int(frozen["best_epoch"]) != 74:
        raise RuntimeError(f"Unexpected frozen base epoch: {frozen['best_epoch']}")
    fc = frozen["config"]
    expected_cfg = {
        "seed": 42, "model": "LiveRec", "fr_ctx": True, "fr_rep": True,
        "batch_size": 100, "seq_len": 16, "dim": 64, "num_att": 2,
        "num_att_ctx": 2, "num_heads": 4, "num_heads_ctx": 4, "topk_att": 64,
    }
    for k, v in expected_cfg.items():
        if fc.get(k) != v:
            raise RuntimeError(f"Frozen base config mismatch {k}: {fc.get(k)!r} != {v!r}")

    data_fu = load_data(args)
    fd = frozen["data"]
    observed_data = {
        "users": int(data_fu.user.nunique()), "streamers": int(data_fu.streamer.nunique()),
        "rows": int(len(data_fu)), "max_step": int(args.max_step),
        "pivot_1": int(args.pivot_1), "pivot_2": int(args.pivot_2),
    }
    for k, v in observed_data.items():
        if int(fd[k]) != v:
            raise RuntimeError(f"Frozen base data mismatch {k}: {fd[k]} != {v}")
    workers = int(os.environ.get("LIVEREC_NUM_WORKERS", "4"))
    val_loader = _make_val_loader(data_fu, args, workers)

    model_path, model_cls = get_model_type(args)
    del model_path
    model = model_cls(args).to(args.device)
    state = torch.load(checkpoint_path, map_location=args.device, weights_only=True)
    model.load_state_dict(state, strict=True)
    model.eval()

    sparse_guard = _assert_sparse_equivalence(model, val_loader, args, probe_batches=2)
    events = _score_frozen_base(model, val_loader, args)
    base_guard = _assert_frozen_base_metrics(events, frozen)

    events, history_meta = _add_state_and_memory(events, data_fu, args)
    if len(events) != 46878:
        raise RuntimeError(f"Unexpected dev target count: {len(events)}")
    horizon_counts = events.relationship_horizon.value_counts().to_dict()
    if sum(horizon_counts.values()) != len(events):
        raise RuntimeError("Relationship-horizon partition is not exhaustive")
    if events[STATE_FEATURES + CONF_FEATURES].isna().any().any():
        raise RuntimeError("NaN detected in exported gate features")
    if np.isinf(events[STATE_FEATURES + CONF_FEATURES].to_numpy(np.float64)).any():
        raise RuntimeError("Infinite value detected in exported gate features")

    summary = _summarize(events)
    report = {
        "experiment": "liverec_twitch100k_p12_dev_memory_horizon",
        "official_commit": os.environ.get("LIVEREC_OFFICIAL_COMMIT"),
        "base_run_id": int(os.environ.get("LIVEREC_BASE_RUN_ID", "35679482824")),
        "base_best_epoch": int(frozen["best_epoch"]),
        "test_ranking_inspected": False,
        "dev_targets": int(len(events)),
        "memory": {
            "short_k": SHORT_K,
            "short_decay": SHORT_DECAY,
            "weights": {"short": MEM_W_SHORT, "long": MEM_W_LONG, "popularity": MEM_W_POP},
            "popularity": "train-only rows with stop < pivot_1; log1p count; min-max over observed streamers",
            "history": "rows for the same user with stop < target_start; sorted by start then original row order",
            "tie_break": "higher MemoryFusion score first; exact score ties by smaller factorized streamer id",
        },
        "relationship_horizon": {
            "recent-visible": "target streamer occurs in the exact LiveRec 16-step input context",
            "long-horizon-only": "target absent from LiveRec context but present in strict completed pre-target history",
            "unseen": "target absent from both LiveRec context and strict completed pre-target history",
            "counts": {str(k): int(v) for k, v in horizon_counts.items()},
        },
        "execution": {
            "validation_only_sequence_materialization": True,
            "test_sequence_materialized": False,
            "single_frozen_base_forward_pass": True,
            "sparse_context_scoring": sparse_guard,
            "batched_gpu_to_cpu_feature_transfer": True,
            "num_workers": int(getattr(val_loader, "num_workers", 0)),
            "pin_memory": bool(getattr(val_loader, "pin_memory", False)),
        },
        "guards": {
            "frozen_base_exact_metric_match": base_guard,
            "feature_finite": True,
            "dev_window_only": True,
        },
        "history_meta": history_meta,
        "summary": summary,
        "gate_feature_columns": STATE_FEATURES + CONF_FEATURES,
    }

    cols = [
        "user_id", "target_streamer", "target_step", "official_repeat", "recent_visible",
        "relationship_horizon", "base_rank0", "memory_rank0", "base_ndcg10", "memory_ndcg10",
        "memory_delta_ndcg10", "history_len",
    ] + STATE_FEATURES + CONF_FEATURES
    cols = list(dict.fromkeys(cols))
    events[cols].to_csv(out_dir / "p12_dev_events.csv.gz", index=False, compression="gzip")
    (out_dir / "p12_dev_memory_report.json").write_text(json.dumps(_py(report), indent=2) + "\n")
    print(json.dumps(_py(report), indent=2))


if __name__ == "__main__":
    main()
