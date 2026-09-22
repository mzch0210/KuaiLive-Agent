from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


class NextItemDataset(Dataset):
    def __init__(self, sequences: dict[int, list[int]], n_items: int, max_len: int, seed: int, max_samples_per_user: int = 50):
        self.examples: list[tuple[list[int], int]] = []
        self.n_items = int(n_items)
        self.max_len = int(max_len)
        self.rng = np.random.default_rng(seed)
        for seq in sequences.values():
            starts = list(range(1, len(seq)))
            if len(starts) > max_samples_per_user:
                starts = starts[-max_samples_per_user:]
            for j in starts:
                self.examples.append((seq[max(0, j - max_len):j], int(seq[j])))

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        hist, pos = self.examples[idx]
        x = np.zeros(self.max_len, dtype=np.int64)
        L = min(len(hist), self.max_len)
        x[:L] = np.asarray(hist[-L:], dtype=np.int64)
        neg = int(self.rng.integers(1, self.n_items + 1))
        while neg == pos:
            neg = int(self.rng.integers(1, self.n_items + 1))
        return x, L, pos, neg


class SASRecSmall(nn.Module):
    def __init__(self, n_items: int, max_len: int, dim: int = 64, heads: int = 4):
        super().__init__()
        self.item = nn.Embedding(n_items + 1, dim, padding_idx=0)
        self.pos = nn.Embedding(max_len, dim)
        layer = nn.TransformerEncoderLayer(d_model=dim, nhead=heads, dim_feedforward=dim * 2, dropout=0.1, batch_first=True, norm_first=True)
        self.enc = nn.TransformerEncoder(layer, num_layers=1)
        self.norm = nn.LayerNorm(dim)

    def encode(self, x: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        B, L = x.shape
        p = torch.arange(L, device=x.device).unsqueeze(0).expand(B, L)
        z = self.item(x) + self.pos(p)
        pad = x.eq(0)
        causal = torch.triu(torch.ones(L, L, device=x.device, dtype=torch.bool), 1)
        z = self.enc(z, mask=causal, src_key_padding_mask=pad)
        idx = (lengths.clamp_min(1) - 1).view(-1, 1, 1).expand(-1, 1, z.shape[-1])
        return self.norm(z.gather(1, idx).squeeze(1))


class GRU4RecSmall(nn.Module):
    def __init__(self, n_items: int, dim: int = 64):
        super().__init__()
        self.item = nn.Embedding(n_items + 1, dim, padding_idx=0)
        self.gru = nn.GRU(dim, dim, num_layers=1, batch_first=True)
        self.norm = nn.LayerNorm(dim)

    def encode(self, x: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        z, _ = self.gru(self.item(x))
        idx = (lengths.clamp_min(1) - 1).view(-1, 1, 1).expand(-1, 1, z.shape[-1])
        return self.norm(z.gather(1, idx).squeeze(1))


def seed_all(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def bpr_loss(pos: torch.Tensor, neg: torch.Tensor) -> torch.Tensor:
    return -torch.log(torch.sigmoid(pos - neg) + 1e-8).mean()


def train_model(model, ds: Dataset, device: torch.device, epochs: int, lr: float, batch_size: int = 1024):
    model.to(device)
    loader = DataLoader(ds, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=(device.type == "cuda"))
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-6)
    for ep in range(epochs):
        model.train()
        total = 0.0
        n = 0
        for x, lengths, pos, neg in loader:
            x = x.to(device, non_blocking=True)
            lengths = lengths.to(device, non_blocking=True)
            pos = pos.to(device, non_blocking=True)
            neg = neg.to(device, non_blocking=True)
            rep = model.encode(x, lengths)
            ps = (rep * model.item(pos)).sum(-1)
            ns = (rep * model.item(neg)).sum(-1)
            loss = bpr_loss(ps, ns)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
            total += float(loss.detach()) * len(x)
            n += len(x)
        print(f"epoch={ep+1}/{epochs} loss={total/max(n,1):.6f}")
    model.eval()
    return model


def load_twitch(path: Path) -> tuple[pd.DataFrame, int, int, int]:
    cols = ["user", "stream", "streamer", "start", "stop"]
    d = pd.read_csv(path, header=None, names=cols)
    d.user = pd.factorize(d.user)[0] + 1
    d.streamer = pd.factorize(d.streamer)[0] + 1
    max_step = int(max(d.start.max(), d.stop.max()))
    return d, max_step - 500, max_step - 250, max_step


def train_sequences(d: pd.DataFrame, pivot1: int) -> dict[int, list[int]]:
    out = {}
    tr = d[d.stop < pivot1]
    for uid, g in tr.sort_values(["user", "start"], kind="mergesort").groupby("user", sort=False):
        seq = g.streamer.astype(int).tolist()
        if len(seq) >= 2:
            out[int(uid)] = seq
    return out


def dev_events(d: pd.DataFrame, p1: int, p2: int, seq_len: int) -> list[dict]:
    rows = []
    eligible = d[d.stop < p2]
    for uid, g in eligible.groupby("user", sort=False):
        g = g.sort_values("start", kind="mergesort").tail(seq_len + 1).reset_index(drop=True)
        if len(g) < 2:
            continue
        target = g.iloc[-1]
        yt = int(target.start)
        if yt < p1 or yt >= p2:
            continue
        hist = g.iloc[:-1].streamer.astype(int).tolist()
        rows.append({
            "user_id": int(uid),
            "target_streamer": int(target.streamer),
            "target_step": yt,
            "history": hist[-seq_len:],
        })
    return rows


def availability_for_steps(d: pd.DataFrame, steps: set[int], max_step: int) -> dict[int, np.ndarray]:
    starts: dict[int, list[int]] = defaultdict(list)
    stops: dict[int, list[int]] = defaultdict(list)
    for r in d[["streamer", "start", "stop"]].itertuples(index=False):
        starts[int(r.start)].append(int(r.streamer))
        stops[int(r.stop)].append(int(r.streamer))
    active = Counter()
    out = {}
    for s in range(max_step + 1):
        for sid in stops.get(s, ()):
            active[sid] -= 1
            if active[sid] <= 0:
                del active[sid]
        for sid in starts.get(s, ()):
            active[sid] += 1
        if s in steps:
            out[s] = np.asarray(sorted(active.keys()), dtype=np.int64)
    missing = steps - set(out)
    if missing:
        raise RuntimeError(f"availability missing {len(missing)} target steps")
    return out


def attach_candidates(events: list[dict], availability: dict[int, np.ndarray]) -> list[dict]:
    for e in events:
        av = availability[e["target_step"]]
        target = e["target_streamer"]
        if target not in set(av.tolist()):
            raise RuntimeError(f"target not active: user={e['user_id']} step={e['target_step']}")
        e["candidates"] = np.concatenate(([target], av[av != target]))
    return events


def metrics_from_ranks(ranks: np.ndarray) -> tuple[float, float]:
    hit = ranks <= 10
    ndcg = np.zeros(len(ranks), dtype=np.float64)
    ndcg[hit] = 1.0 / np.log2(ranks[hit] + 1.0)
    return float(ndcg.mean()), float(hit.mean())


def popularity_eval(events: list[dict], pop: dict[int, int]) -> tuple[float, float]:
    ranks = []
    for e in events:
        c = e["candidates"]
        s = np.asarray([pop.get(int(i), 0) for i in c], dtype=np.float64)
        ts = s[0]
        rank = 1 + int(np.sum(s > ts)) + int(np.sum((s == ts) & (c < c[0])))
        ranks.append(rank)
    return metrics_from_ranks(np.asarray(ranks, dtype=np.int64))


def neural_eval(model, events: list[dict], device: torch.device, seq_len: int, batch_size: int = 512) -> tuple[float, float]:
    ranks = []
    model.eval()
    with torch.inference_mode():
        for i in range(0, len(events), batch_size):
            batch = events[i:i + batch_size]
            B = len(batch)
            max_c = max(len(e["candidates"]) for e in batch)
            x = np.zeros((B, seq_len), dtype=np.int64)
            lengths = np.zeros(B, dtype=np.int64)
            cands = np.zeros((B, max_c), dtype=np.int64)
            mask = np.zeros((B, max_c), dtype=bool)
            for j, e in enumerate(batch):
                h = e["history"][-seq_len:]
                x[j, :len(h)] = h
                lengths[j] = len(h)
                c = e["candidates"]
                cands[j, :len(c)] = c
                mask[j, :len(c)] = True
            xt = torch.from_numpy(x).to(device)
            lt = torch.from_numpy(lengths).to(device)
            ct = torch.from_numpy(cands).to(device)
            rep = model.encode(xt, lt)
            emb = model.item(ct)
            scores = (emb * rep.unsqueeze(1)).sum(-1)
            scores = scores.masked_fill(~torch.from_numpy(mask).to(device), float("-inf"))
            target_score = scores[:, 0:1]
            better = (scores > target_score).sum(1)
            ids = ct
            ties = ((scores == target_score) & (ids < ids[:, 0:1]) & torch.from_numpy(mask).to(device)).sum(1)
            r = (1 + better + ties).detach().cpu().numpy().astype(np.int64)
            ranks.extend(r.tolist())
    return metrics_from_ranks(np.asarray(ranks, dtype=np.int64))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--twitch-csv", type=Path, required=True)
    ap.add_argument("--official-oof", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--seq-len", type=int, default=16)
    ap.add_argument("--epochs", type=int, default=5)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    seed_all(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        raise RuntimeError("Strong-base benchmark is assigned to the self-hosted GPU runner; CUDA is required")

    d, p1, p2, max_step = load_twitch(args.twitch_csv)
    n_items = int(d.streamer.max())
    seqs = train_sequences(d, p1)
    events = dev_events(d, p1, p2, args.seq_len)
    availability = availability_for_steps(d, {e["target_step"] for e in events}, max_step)
    attach_candidates(events, availability)

    oof = pd.read_csv(args.official_oof)
    expected = oof[["user_id", "target_streamer", "target_step"]].astype(int).sort_values("user_id").reset_index(drop=True)
    got = pd.DataFrame([{k: e[k] for k in ["user_id", "target_streamer", "target_step"]} for e in events]).sort_values("user_id").reset_index(drop=True)
    if len(got) != len(expected) or not got.equals(expected):
        raise RuntimeError(f"DEV event reconstruction mismatch: got={len(got)} expected={len(expected)}")

    pop_counts = d[d.stop < p1].streamer.astype(int).value_counts().to_dict()
    pop_ndcg, pop_hr = popularity_eval(events, pop_counts)

    ds_sas = NextItemDataset(seqs, n_items=n_items, max_len=args.seq_len, seed=args.seed)
    sas = train_model(SASRecSmall(n_items, args.seq_len, dim=64, heads=4), ds_sas, device, args.epochs, 5e-4)
    sas_ndcg, sas_hr = neural_eval(sas, events, device, args.seq_len)
    del sas
    torch.cuda.empty_cache()

    ds_gru = NextItemDataset(seqs, n_items=n_items, max_len=args.seq_len, seed=args.seed + 1)
    gru = train_model(GRU4RecSmall(n_items, dim=64), ds_gru, device, args.epochs, 1e-3)
    gru_ndcg, gru_hr = neural_eval(gru, events, device, args.seq_len)

    if "base_rank0" in oof.columns:
        official_hr = float((oof.base_rank0.astype(int) < 10).mean())
    else:
        official_hr = float((oof.base_ndcg10.astype(float) > 0).mean())
    official_ndcg = float(oof.base_ndcg10.astype(float).mean())

    table = pd.DataFrame([
        {"model": "Popularity", "dev_ndcg10": pop_ndcg, "dev_hr10": pop_hr, "source": "same LiveRec DEV protocol"},
        {"model": "GRU4Rec-small", "dev_ndcg10": gru_ndcg, "dev_hr10": gru_hr, "source": "same LiveRec DEV events/candidates; standard BPR training"},
        {"model": "SASRec-small", "dev_ndcg10": sas_ndcg, "dev_hr10": sas_hr, "source": "same LiveRec DEV events/candidates; standard BPR training"},
        {"model": "Official LiveRec Base", "dev_ndcg10": official_ndcg, "dev_hr10": official_hr, "source": "frozen P1.2 official reproduction"},
    ]).sort_values("dev_ndcg10", ascending=False, kind="mergesort").reset_index(drop=True)
    table.insert(0, "dev_rank", np.arange(1, len(table) + 1))
    table.to_csv(args.out_dir / "twitch_dev_strong_base_benchmark.csv", index=False)

    base = table[table.model == "Official LiveRec Base"].iloc[0]
    summary = {
        "experiment": "kbs_strong_base_competitiveness_twitch_dev",
        "test_ranking_inspected": False,
        "n_dev": int(len(events)),
        "seq_len": int(args.seq_len),
        "training_epochs": int(args.epochs),
        "device": str(device),
        "official_liverec_dev_ndcg10": float(base.dev_ndcg10),
        "official_liverec_rank": int(base.dev_rank),
        "event_reconstruction_exact_match": True,
        "claim_guardrail": "The auxiliary GRU4Rec/SASRec implementations provide same-event protocol context; they are not claimed as exhaustive tuned reproductions. The frozen official LiveRec model remains the scientific external Base.",
    }
    (args.out_dir / "twitch_dev_strong_base_benchmark.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(table.to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
