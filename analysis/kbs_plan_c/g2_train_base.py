#!/usr/bin/env python3
"""KBS Plan C G2: train-only GPU baselines and reusable author sequence index.

No TEST file is opened. Training is not DEV model selection. This module only
produces TRAIN checkpoints and pilot throughput/memory observations. Models
must be evaluated/selected on a frozen DEV protocol before TEST.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import random
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

L = 16
D = 64


def digest(file: Path):
    h = hashlib.sha256()
    with file.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class Encoder(nn.Module):
    def __init__(self, items, kind):
        super().__init__()
        if kind not in ("sasrec", "gru4rec"):
            raise ValueError("unknown Base family")
        self.kind = kind
        self.item = nn.Embedding(items + 1, D, padding_idx=0)
        nn.init.normal_(self.item.weight, 0, .02)
        with torch.no_grad():
            self.item.weight[0].zero_()
        if kind == "sasrec":
            self.pos = nn.Embedding(L, D)
            self.norm = nn.LayerNorm(D)
            block = nn.TransformerEncoderLayer(
                D, nhead=4, dim_feedforward=D * 4, dropout=.1,
                activation="gelu", batch_first=True, norm_first=True)
            self.encoder = nn.TransformerEncoder(block, num_layers=1, enable_nested_tensor=False)
            self.dropout = nn.Dropout(.1)
            self.register_buffer(
                "causal", torch.triu(torch.ones(L, L, dtype=torch.bool), 1),
                persistent=False)
        else:
            self.encoder = nn.GRU(D, D, num_layers=1, batch_first=True)
            self.norm = nn.LayerNorm(D)

    def forward(self, history):
        # Histories are left-padded and nonempty; latest event is rightmost.
        x = self.item(history)
        if self.kind == "sasrec":
            x = self.dropout(x + self.pos(torch.arange(
                history.shape[1], device=history.device)))
            x = self.encoder(x, mask=self.causal[:history.shape[1], :history.shape[1]],
                             src_key_padding_mask=history.eq(0))
            return self.norm(x[:, -1])
        # Right-aligned sequences; a single GRU applied to all positions
        # handles left padding consistently across train and DEV.
        x, _ = self.encoder(x)
        return self.norm(x[:, -1])

    def score(self, history, candidate_ids):
        rep = self(history)
        return (rep.unsqueeze(-2) * self.item(candidate_ids)).sum(-1)


def load_or_prepare_train_index(g1: Path, cache: Path, synthetic=False):
    import pyarrow.parquet as pq
    manifest = json.loads((g1/"manifest.json").read_text())
    if (manifest["schema"] != "kbs-plan-c-g1-derived-v1"
            or manifest["test_outcomes_inspected"] is not False):
        raise ValueError("wrong G1 source: expected TEST-unseen TRAIN bundle")
    authors_path = g1 / "train_known_authors.parquet"
    events_path = g1 / "train_author_events.parquet"
    for path in (authors_path, events_path):
        if not path.is_file():
            raise FileNotFoundError(path)
        if not synthetic and digest(path) != manifest["generated_files_sha256"][path.name]:
            raise ValueError("train input digest mismatch " + path.name)
    expected = {"g1_protocol_sha256": manifest["protocol_sha256"],
                "train_author_sha256": manifest["generated_files_sha256"][authors_path.name],
                "train_events_sha256": manifest["generated_files_sha256"][events_path.name],
                "item_index_zero_reserved": True}
    idx_manifest = cache / "index_manifest.json"
    if idx_manifest.exists():
        record = json.loads(idx_manifest.read_text())
        if any(record.get(k) != v for k, v in expected.items()):
            raise ValueError("TRAIN index manifest does not match source/protocol")
        for name in ("authors.npy", "sequence_ids.npy", "user_offsets.npy", "popularity_cdf.npy"):
            if digest(cache/name) != record["files_sha256"][name]:
                raise ValueError("TRAIN index was modified " + name)
        return record
    if cache.exists():
        raise FileExistsError("Incomplete existing TRAIN index; inspect, never overwrite")
    stage = cache.with_name(cache.name+".partial")
    if stage.exists():
        raise FileExistsError("Interrupted stage exists; do not overwrite")
    stage.mkdir(parents=True, mode=0o700)
    author_arr = pq.read_table(authors_path, columns=["author_id"]).column("author_id").to_numpy()
    author_arr = np.asarray(author_arr, dtype=np.int64)
    if not np.all(author_arr[1:] > author_arr[:-1]):
        raise ValueError("TRAIN author IDs must be strictly ascending")
    table = pq.read_table(events_path, columns=["user_id", "author_id"])
    users = np.asarray(table.column("user_id").to_numpy(), dtype=np.int64)
    raw_items = np.asarray(table.column("author_id").to_numpy(), dtype=np.int64)
    if len(users) < 100 or len(author_arr) < 3:
        if not synthetic:
            raise ValueError("Unexpectedly small TRAIN")
    if np.any(users[1:] < users[:-1]):
        raise ValueError("TRAIN must be sorted by user and causal event time")
    mapped = np.searchsorted(author_arr, raw_items)
    if np.any(mapped >= len(author_arr)) or np.any(author_arr[mapped] != raw_items):
        raise ValueError("TRAIN event contains unknown author")
    ids = (mapped + 1).astype(np.int32)
    starts = np.concatenate(([0], np.flatnonzero(users[1:] != users[:-1])+1,
                             [len(users)])).astype(np.int64)
    counts = np.bincount(ids, minlength=len(author_arr)+1).astype(np.float64)
    weights = np.power(counts[1:], .75)
    cdf = np.cumsum(weights)
    cdf /= cdf[-1]
    for name,array in (
        ("authors.npy", author_arr),
        ("sequence_ids.npy", ids),
        ("user_offsets.npy", starts),
        ("popularity_cdf.npy", cdf)
    ):
        np.save(stage/name, array, allow_pickle=False)
    record = dict(expected)
    record.update({"schema":"kbs-plan-c-g2-train-index-v1",
                   "total_training_events":int(len(ids)),
                   "unique_train_users":int(len(starts)-1),
                   "unique_train_authors":int(len(author_arr)),
                   "training_only":True,"dev_labels_used":False,
                   "test_files_opened":False,
                   "files_sha256":{n:digest(stage/n) for n in
                       ("authors.npy","sequence_ids.npy","user_offsets.npy","popularity_cdf.npy")}})
    (stage/"index_manifest.json").write_text(json.dumps(record,indent=2)+"\n")
    stage.rename(cache)
    return record


def draw_contexts(ids, offsets, rng, batch, context=L):
    # Unbiased random TRAIN event positions conditioned on >=2 prior user events.
    batchpos = rng.integers(0, len(ids), size=batch*2, dtype=np.int64)
    out=[]
    while len(out) < batch:
        block=np.asarray(batchpos)
        uid=np.searchsorted(offsets,block,side="right")-1
        start=offsets[uid]
        valid=block >= start+2
        out.extend(block[valid].tolist())
        if len(out)<batch:
            batchpos=rng.integers(0,len(ids),size=batch,dtype=np.int64)
    positions=np.asarray(out[:batch],dtype=np.int64)
    groups=np.searchsorted(offsets,positions,side="right")-1
    first=offsets[groups]
    indices=positions[:,None]-np.arange(context,0,-1)[None,:]
    valid=indices >= first[:,None]
    padded=np.zeros((batch,context),dtype=np.int64)
    padded[valid]=ids[indices[valid]]
    return padded, ids[positions].astype(np.int64)


def sample_negatives(cdf, rng, positives, contexts, n_neg=32):
    batch=len(positives)
    half=n_neg//2
    uniform=rng.integers(1,len(cdf)+1,size=(batch,n_neg-half),dtype=np.int64)
    pop=np.searchsorted(cdf,rng.random((batch,half)))+1
    neg=np.concatenate((uniform,pop),axis=1).astype(np.int64)
    invalid=(neg==positives[:,None]) | (neg[:,:,None]==contexts[:,None,:]).any(axis=2)
    # Bounded deterministic repair; extremely rare for million-item vocabulary.
    for _ in range(3):
        if not invalid.any():
            break
        neg[invalid]=rng.integers(1,len(cdf)+1,size=int(invalid.sum()))
        invalid=(neg==positives[:,None]) | (neg[:,:,None]==contexts[:,None,:]).any(axis=2)
    if invalid.any():
        neg[invalid]=((positives[:,None]+np.arange(n_neg)[None,:])%len(cdf)+1)[invalid]
    return neg


def train(args):
    seed=int(args.seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if not args.synthetic and not torch.cuda.is_available():
        raise RuntimeError("G2 real pilot/fit needs CUDA GPU")
    device="cuda" if torch.cuda.is_available() and not args.cpu else "cpu"
    if not args.synthetic and device!="cuda":
        raise RuntimeError("Real G2 must not silently train on CPU")
    src_manifest=load_or_prepare_train_index(args.g1,args.index,args.synthetic)
    ids=np.load(args.index/"sequence_ids.npy",mmap_mode="r")
    offsets=np.load(args.index/"user_offsets.npy",mmap_mode="r")
    cdf=np.load(args.index/"popularity_cdf.npy",mmap_mode="r")
    count=src_manifest["unique_train_authors"]
    model=Encoder(count,args.model).to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=args.learning_rate,weight_decay=1e-4)
    rng=np.random.default_rng(seed)
    stats=[]
    t0=time.monotonic()
    maxsteps=args.steps_per_epoch
    if args.mode=="smoke":
        maxsteps=min(maxsteps,3)
    for ep in range(args.epochs):
        model.train()
        total=0.
        for step in range(maxsteps):
            seq,pos=draw_contexts(ids,offsets,rng,args.batch,L)
            neg=sample_negatives(cdf,rng,pos,seq,args.negatives)
            candidates=np.column_stack([pos,neg])
            h=torch.as_tensor(seq,device=device,dtype=torch.long)
            c=torch.as_tensor(candidates,device=device,dtype=torch.long)
            optimizer.zero_grad(set_to_none=True)
            logits=model.score(h,c)
            loss=F.cross_entropy(logits,torch.zeros(len(seq),device=device,dtype=torch.long))
            if not torch.isfinite(loss):
                raise FloatingPointError("nonfinite TRAIN loss")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(),max_norm=1.0)
            optimizer.step()
            total+=float(loss.detach().item())
            if (step+1)%max(1,args.log_interval)==0:
                print(json.dumps({"model":args.model,"epoch":ep+1,"steps":step+1,
                                  "TRAIN_loss":round(total/(step+1),6),
                                  "time_s":round(time.monotonic()-t0,1)}),flush=True)
        record={"epoch":ep+1,"TRAIN_cross_entropy":total/maxsteps,
                "elapsed_s":round(time.monotonic()-t0,2)}
        stats.append(record)
        if args.mode=="train":
            args.out.mkdir(parents=True,exist_ok=True)
            target=args.out/f"{args.model}_seed{seed}_epoch{ep+1}.pt"
            tmp=target.with_suffix(".pt.partial")
            torch.save({"model_family":args.model,"model_state":model.state_dict(),
                        "optimizer_state":optimizer.state_dict(),"epoch":ep+1,
                        "input_manifest":src_manifest,"seed":seed,
                        "config":vars(args),"test_used":False,
                        "dev_selected":False},tmp)
            tmp.rename(target)
            record["checkpoint"]=target.name
            record["checkpoint_sha256"]=digest(target)
    device_info={"device":device,"torch":torch.__version__,
                 "cuda":torch.version.cuda}
    if device=="cuda":
        device_info.update({"gpu":torch.cuda.get_device_name(0),
                            "peak_vram_gib":round(
                                torch.cuda.max_memory_allocated()/1024**3,3)})
    result={"schema":"kbs-plan-c-g2-train-only-v1",
            "model_family":args.model,"mode":args.mode,
            "seed":seed,"index_manifest":src_manifest,
            "n_epochs":args.epochs,"steps_per_epoch":maxsteps,
            "batch_size":args.batch,"negative_count":args.negatives,
            "learning_rate":args.learning_rate,
            "train_records":stats,"runtime":device_info,
            "elapsed_s":round(time.monotonic()-t0,2),
            "status":"TRAIN_CHECKPOINTS_NOT_DEV_SELECTED" if args.mode=="train" else "GPU_PILOT_ONLY",
            "dev_outcomes_read":False,"test_outcomes_read":False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/f"{args.model}_{args.mode}_report.json").write_text(
        json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({"model_family":args.model,"status":result["status"],
                      "elapsed_s":result["elapsed_s"],
                      "peak_vram_gib":device_info.get("peak_vram_gib"),
                      "last_train_loss":stats[-1]["TRAIN_cross_entropy"]}),flush=True)
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--g1",type=Path,required=True)
    p.add_argument("--index",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--mode",choices=["smoke","pilot","train"],default="pilot")
    p.add_argument("--model",choices=["sasrec","gru4rec"],required=True)
    p.add_argument("--seed",type=int,default=20261012)
    p.add_argument("--batch",type=int,default=512)
    p.add_argument("--negatives",type=int,default=32)
    p.add_argument("--steps-per-epoch",type=int,default=160)
    p.add_argument("--epochs",type=int,default=1)
    p.add_argument("--learning-rate",type=float,default=.001)
    p.add_argument("--log-interval",type=int,default=40)
    p.add_argument("--synthetic",action="store_true")
    p.add_argument("--cpu",action="store_true")
    args=p.parse_args()
    if args.batch<1 or args.negatives<2 or args.steps_per_epoch<1 or args.epochs<1:
        p.error("Invalid model size/step settings")
    train(args)
if __name__=="__main__":
    main()
