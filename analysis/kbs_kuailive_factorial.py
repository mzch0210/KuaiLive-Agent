"""Post-hoc 2x2 candidate-set versus normalization-reference diagnostic.

One fixed Dual-ID checkpoint pair, one frozen fusion alpha, one TEST scoring pass.
Four cells rank C in {sampled, full} using per-branch z-score statistics from
R in {sampled, full}. The mixed cells are counterfactual diagnostics, not
deployable ranking rules or causal interventions.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import torch

from kbs_kuailive_same_checkpoint import sha256, subset_indices, SEED
from kbs_kuailive_regime_decomposition import _build_test_states
from full_active_dual_id import (
    active_interval_arrays, candidate_sweep, encode_phase_users, load_rechorus,
    memory_rank, ndcg_scalar, popularity_by_streamer, room_to_streamer_item_array,
    score_embedding_candidates, zscore,
)
from room_level_selective_agent import histories, load_data, memory_scores, parse_list

EXPECTED_INPUT_HASHES = {
    "train.csv": "ad91413537175b9f6e9013c525a552b6004cc00e029b41360f08519e0735b5b4",
    "dev.csv": "46dd3081688468c89acf6366d36d87c122fa45850ddb69320c05da9de94a9f54",
    "test.csv": "3491862df4de5cfb487fbd21c2f62c2d1d62acac110f852cc83c019dfcc6e956",
}
BASELINE_MODEL_HASHES = {
    "room": "b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7",
    "streamer": "82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945",
}
EXPECTED_SEED0 = {
    "SS": -0.041204110825603886,
    "FF": 0.04630668646082395,
    "shift": 0.08751079728642783,
    "sampled_base": 0.60709157516216,
    "full_base": 0.38571242304278636,
    "sampled_memory": 0.5658874643365561,
    "full_memory": 0.4320191095036103,
}


def norm_to_reference(values: np.ndarray, reference: np.ndarray) -> np.ndarray:
    """Match original population-STD fallback; a different ref changes scale."""
    sd = float(np.std(reference))
    if not np.isfinite(sd):
        raise ValueError("nonfinite reference std")
    if sd <= 1e-12:
        return np.zeros_like(values, dtype=np.float64)
    return (np.asarray(values, dtype=np.float64) - float(np.mean(reference))) / sd


def base_rank(room: np.ndarray, stream: np.ndarray, target_index: int, alpha: float) -> int:
    values = alpha * room + (1.0-alpha) * stream
    return int(np.sum(values >= values[target_index] - 1e-12))


def four_cell_ranks(room: np.ndarray, stream: np.ndarray,
                    sample_idx: np.ndarray, target_full_idx: int, alpha: float) -> dict:
    sample_r, sample_s = room[sample_idx], stream[sample_idx]
    target_sample = int(np.flatnonzero(sample_idx == target_full_idx)[0])
    rz_s, sz_s = zscore(sample_r), zscore(sample_s)
    rz_f, sz_f = zscore(room), zscore(stream)
    # SS, FF are literally the pre-existing scorer; mixed cells use external moments.
    return {
        "SS": base_rank(rz_s, sz_s, target_sample, alpha),
        "SF": base_rank(norm_to_reference(sample_r, room),
                        norm_to_reference(sample_s, stream), target_sample, alpha),
        "FS": base_rank(norm_to_reference(room, sample_r),
                        norm_to_reference(stream, sample_s), target_full_idx, alpha),
        "FF": base_rank(rz_f, sz_f, target_full_idx, alpha),
    }


def per_event_factorial(raw: dict) -> dict:
    # g(C,R): Memory on C minus Base ranked on C with reference moments R.
    ss, sf, fs, ff = (float(raw[k]) for k in ("SS","SF","FS","FF"))
    member = 0.5 * ((fs-ss) + (ff-sf))
    normalize = 0.5 * ((sf-ss) + (ff-fs))
    shift = ff-ss
    if not np.isclose(member+normalize,shift,rtol=0,atol=1e-14):
        raise AssertionError("Shapley identity violated")
    return {"membership":member, "normalization":normalize, "shift":shift}


def paired_ci(arrays: dict[str,np.ndarray], reps: int, seed: int) -> dict:
    """Use exactly the same user-resample index matrix for every variable."""
    n = len(next(iter(arrays.values())))
    vals = {k:np.asarray(v,dtype=np.float64) for k,v in arrays.items()}
    if any(len(v)!=n or not np.isfinite(v).all() for v in vals.values()):
        raise ValueError("invalid bootstrap input")
    rng = np.random.default_rng(seed)
    dist = {k:[] for k in vals}
    for low in range(0,reps,32):
        k = min(32,reps-low)
        draw = rng.integers(0,n,size=(k,n))
        for name,v in vals.items():
            dist[name].extend(v[draw].mean(axis=1).tolist())
    return {name: {"mean":float(v.mean()),
                   "ci95":[float(q) for q in np.quantile(dist[name], [.025,.975])],
                   "n":int(n)} for name,v in vals.items()}


def self_test():
    # Nonzero and zero-variance reference; exact original cells and Shapley identity.
    r=np.asarray([1.2, 1.2, -0.5, 0.9, 2.0])
    s=np.asarray([0.2, 0.9, -1.1, 0.5, 0.2])
    idx=np.asarray([4,1,0],dtype=int)
    a=0.125
    got=four_cell_ranks(r,s,idx,4,a)
    assert got["SS"]==base_rank(zscore(r[idx]),zscore(s[idx]),0,a)
    assert got["FF"]==base_rank(zscore(r),zscore(s),4,a)
    deg=norm_to_reference(np.asarray([1.,2.]),np.asarray([3.,3.]))
    assert np.array_equal(deg,np.zeros(2))
    for example in ({"SS":0.1,"SF":0.3,"FS":0.2,"FF":0.8},
                    {"SS":-0.4,"SF":0.1,"FS":-0.3,"FF":-0.2}):
        terms=per_event_factorial(example)
        assert abs(terms["shift"]-terms["membership"]-terms["normalization"])<1e-14
    ci=paired_ci({"shift":np.array([0.3,-0.1,0.5]),"membership":np.array([0.1,0.0,0.4])},30,SEED)
    assert ci["shift"]["n"]==3
    try:
        subset_indices(np.array([1,2]),np.array([3]))
        raise AssertionError("subset must fail closed")
    except ValueError:
        pass
    print("P0/P1 factorial synthetic self-test PASS")


def evaluate(args):
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass
    room_dir=args.data_root/"KuaiLiveShopRoomDualID"
    stream_dir=args.data_root/"KuaiLiveShopStreamerParallel"
    input_sha={name:sha256(room_dir/name) for name in EXPECTED_INPUT_HASHES}
    if input_sha!=EXPECTED_INPUT_HASHES:
        raise RuntimeError("frozen input SHA256 mismatch")
    model_sha={"room":sha256(args.room_model),"streamer":sha256(args.streamer_model)}
    if args.seed==20260918 and model_sha!=BASELINE_MODEL_HASHES:
        raise RuntimeError("baseline seed checkpoint SHA256 mismatch")
    if model_sha["room"]==model_sha["streamer"]:
        raise RuntimeError("same weights presented for both branches")
    train,dev,test,item_to_streamer=load_data(room_dir,574)
    if len(test)!=10222 or test.user_id.duplicated().any():
        raise RuntimeError("unexpected matched TEST coverage")
    room_map=pd.read_csv(room_dir/"room_item_map.tsv",sep="\t")
    streamer_map=pd.read_csv(stream_dir/"streamer_item_map.tsv",sep="\t")
    intervals=active_interval_arrays(pd.read_pickle(args.prepared_dir/"rooms.pkl"),room_map)
    room_to_sitem=room_to_streamer_item_array(room_map,streamer_map)
    rm,rc=load_rechorus(args.rechorus_source,args.data_root,"KuaiLiveShopRoomDualID",args.room_model)
    sm,sc=load_rechorus(args.rechorus_source,args.data_root,"KuaiLiveShopStreamerParallel",args.streamer_model)
    rvec=encode_phase_users(rm,rc,"test")
    svec=encode_phase_users(sm,sc,"test")
    pop=popularity_by_streamer(train,item_to_streamer)
    history=histories(pd.concat([train,dev[["user_id","item_id","time"]]],ignore_index=True),
                      item_to_streamer)
    by_user=test.set_index("user_id",verify_integrity=True)
    rows=[]
    for uid,t,target,full_items,active in candidate_sweep(test,intervals):
        event=by_user.loc[uid]
        if int(event.item_id)!=target or int(event.time)!=t:
            raise RuntimeError("paired target membership mismatch")
        sample=np.concatenate(([target],parse_list(event.neg_items,int)))
        if len(sample)!=575:
            raise RuntimeError("sample count mismatch")
        idx=subset_indices(full_items,sample)
        target_full=np.flatnonzero(full_items==target)
        if len(target_full)!=1 or int(idx[0])!=int(target_full[0]):
            raise RuntimeError("positive membership mismatch")
        rr=score_embedding_candidates(rm,rvec[uid],full_items)
        sr=score_embedding_candidates(sm,svec[uid],room_to_sitem[full_items])
        if not np.isfinite(rr).all() or not np.isfinite(sr).all():
            raise RuntimeError("invalid raw scores")
        ranks=four_cell_ranks(rr,sr,idx,int(target_full[0]),args.alpha)
        mem_s=ndcg_scalar(memory_rank(sample,memory_scores(sample,uid,pop,history,item_to_streamer),target))
        mem_f=ndcg_scalar(memory_rank(full_items,memory_scores(full_items,uid,pop,history,item_to_streamer),target))
        base={k:ndcg_scalar(v) for k,v in ranks.items()}
        delta={k:(mem_s if k[0]=="S" else mem_f)-value for k,value in base.items()}
        decomposition=per_event_factorial(delta)
        rows.append({"user_id":uid,"time":t,"target_item":target,"full_candidates":len(full_items),
                     "target_metadata_active":bool(active),
                     "sampled_memory":mem_s,"full_memory":mem_f,
                     **{"base_"+k:base[k] for k in ("SS","SF","FS","FF")},
                     **{"delta_"+k:delta[k] for k in ("SS","SF","FS","FF")},
                     **decomposition})
    d=pd.DataFrame(rows).sort_values("user_id").reset_index(drop=True)
    if len(d)!=10222 or d.user_id.duplicated().any():
        raise RuntimeError("missing/duplicate scored users")
    states=_build_test_states(room_dir,50)[["user_id","evidence_state"]]
    d=d.merge(states,on="user_id",validate="one_to_one")
    if d.evidence_state.isna().any():
        raise RuntimeError("missing state")
    components=["delta_SS","delta_SF","delta_FS","delta_FF","membership","normalization","shift"]
    arrays={k:d[k].to_numpy(dtype=float) for k in components}
    overall=paired_ci(arrays,args.n_boot,SEED+100+args.seed)
    groups={}
    for j,group in enumerate(("represented","recoverable-but-unrepresented","unavailable")):
        sub=d.loc[d.evidence_state==group]
        groups[group]=paired_ci({k:sub[k].to_numpy(dtype=float) for k in components},args.n_boot,SEED+300+j+args.seed)
        groups[group]["count"]=int(len(sub))
        groups[group]["prevalence"]=float(len(sub)/len(d))
    for key in components:
        weighted=sum(v["prevalence"]*v[key]["mean"] for v in groups.values())
        if not np.isclose(weighted,overall[key]["mean"],atol=1e-12,rtol=0):
            raise RuntimeError("group weighted decomposition mismatch")
    if not np.allclose(d.membership+d.normalization,d["shift"],atol=1e-13,rtol=0):
        raise RuntimeError("per-event decomposition mismatch")
    if args.seed==20260918:
        replay={
            "SS":overall["delta_SS"]["mean"],"FF":overall["delta_FF"]["mean"],
            "shift":overall["shift"]["mean"],
            "sampled_base":float(d.base_SS.mean()),"full_base":float(d.base_FF.mean()),
            "sampled_memory":float(d.sampled_memory.mean()),"full_memory":float(d.full_memory.mean())}
        for key,expected in EXPECTED_SEED0.items():
            if abs(replay[key]-expected)>1e-10:
                raise RuntimeError(f"original run replay mismatch: {key}, {replay[key]}, expected {expected}")
    report={"status":"completed","design":"posthoc factorial candidate membership x z reference",
            "seed":args.seed,"alpha_room":args.alpha,"n":len(d),
            "cells":{"SS":"sampled items/sampled z ref","SF":"sampled items/full z ref",
                     "FS":"full items/sampled z ref","FF":"full items/full z ref"},
            "bootstrap_replicates":args.n_boot,"overall":overall,"states":groups,
            "model_sha256":model_sha,"input_sha256":input_sha,
            "original_run_replayed":args.seed==20260918,
            "guards":{"one_target_per_user":True,"sampled_subset_full":True,
                      "fixed_alpha":True,"same_raw_scores":True,"identity":True,
                      "exact_shapley_per_event":True,"state_weighted_identity":True},
            "interpretation":"algebraic normalization/member attribution, noncausal; already inspected TEST"}
    args.out_dir.mkdir(parents=True,exist_ok=True)
    d.to_csv(args.out_dir/"factorial_per_user.csv.gz",index=False,compression="gzip")
    (args.out_dir/"factorial_report.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"seed":args.seed,"n":len(d),"overall":overall,
                      "original_run_replayed":report["original_run_replayed"]},indent=2))
    return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    for key in ("rechorus-source","data-root","prepared-dir","room-model","streamer-model","out-dir"):
        p.add_argument("--"+key,type=Path)
    p.add_argument("--alpha",type=float,default=0.125)
    p.add_argument("--seed",type=int,default=20260918)
    p.add_argument("--n-boot",type=int,default=3000)
    args=p.parse_args()
    if args.self_test:
        self_test()
        return
    for name in ("rechorus_source","data_root","prepared_dir","room_model","streamer_model","out_dir"):
        if getattr(args,name) is None:
            p.error("--"+name.replace("_","-")+" required")
    if args.seed not in (20260918,20260919,20260920):
        raise ValueError("only predeclared seeds supported")
    if args.alpha != 0.125 or args.n_boot!=3000:
        raise ValueError("primary protocol requires frozen alpha=0.125 and 3000 replicates")
    evaluate(args)


if __name__=="__main__":
    main()
