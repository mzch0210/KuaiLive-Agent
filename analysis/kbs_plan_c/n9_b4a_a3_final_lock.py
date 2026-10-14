#!/usr/bin/env python3
"""A3 H1/H2 final private SHA-only, no-label sealing gate; does not unblind A4."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np

SEEDS=(20261014,20261015,20261016)
H1_SHA="be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
H2_SHA="40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059"

def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()

def checked(folder,filename,registered):
    p=folder/filename
    if digest(p)!=registered:
        raise RuntimeError("private predicted file SHA differs: "+str(p))
    return np.load(p,allow_pickle=False)

def main(h1,mechanism_root,out):
    if out.exists():raise FileExistsError("A3 final SHA seal immutable")
    a=json.loads((h1/"manifest.json").read_text())
    if not(a["status"]=="H1_30000_FROZEN_PREDICTIONS_A4_HARD_HOLD"
           and a["source_sample_SHA256"]==H1_SHA
           and a["nested_H2_SHA256"]==H2_SHA
           and a["n_events"]==30000
           and not a["test_rank_ndcg_hr_computed"]
           and not a["A4_unseal_authorized"]):
        raise RuntimeError("H1 is not an unblinded-safe 30k frozen ranking")
    h1_ids=checked(h1,"event_ids.npy",a["private_files_sha256"]["event_ids.npy"])
    h1_top=checked(h1,"top10_base_and_memory_author_tokens.npy",
                   a["private_files_sha256"]["top10_base_and_memory_author_tokens.npy"])
    h1_calls=checked(h1,"gate_calls.npy",a["private_files_sha256"]["gate_calls.npy"])
    if h1_ids.shape!=(30000,) or h1_top.shape!=(30000,3,10) or h1_calls.shape!=(30000,2,2):
        raise RuntimeError("H1 frozen array dimensions wrong")
    if len(set(h1_ids.tolist()))!=30000:
        raise RuntimeError("H1 repeated ID")
    reference_ids=None;reference_real=None;null_hashes={}
    for seed in SEEDS:
        folder=mechanism_root/f"null_seed_{seed}_frozen_top10_v1"
        b=json.loads((folder/"manifest.json").read_text())
        if not(b["status"]=="H2_SEED_FROZEN_4096_UNLABELED_TOP10"
               and b["seed"]==seed and b["n_events"]==4096
               and b["source_sample_SHA256"]==H2_SHA
               and b["H1_original_memory_top10_exact_match"]
               and b["original_and_null_rankings_same_F_roster"]
               and b["source_hour_rewire_applied_after_closed"]
               and not b["target_ndcg_rank_hr_computed"]
               and not b["A4_authorized"]):
            raise RuntimeError("H2 seed incomplete or not target blind")
        ids=checked(folder,"event_ids.npy",b["files_sha256"]["event_ids.npy"])
        original=checked(folder,"original_full_f_top10.npy",
                        b["files_sha256"]["original_full_f_top10.npy"])
        null=checked(folder,"null_full_f_top10.npy",
                     b["files_sha256"]["null_full_f_top10.npy"])
        if ids.shape!=(4096,) or original.shape!=(4096,10) or null.shape!=(4096,10):
            raise RuntimeError("H2 shape wrong")
        if reference_ids is None:
            reference_ids=ids.copy();reference_real=original.copy()
        elif not (np.array_equal(ids,reference_ids) and
                  np.array_equal(original,reference_real)):
            raise RuntimeError("H2 seed targets or original ranker differ")
        null_hashes[str(seed)]=b["files_sha256"]["null_full_f_top10.npy"]
    if not set(reference_ids.tolist()).issubset(set(h1_ids.tolist())):
        raise RuntimeError("H2 subset not contained in H1")
    # Locked A3 only; target labels remain inaccessible.
    manifest={"schema":"kbs-b4a-a3-complete-blind-prediction-lock-v1",
       "status":"A3_H1_H2_PREDICTIONS_SHA_LOCKED_A4_NOT_OPENED",
       "main_events":30000,"mechanism_events":4096,
       "frozen_H1_manifest_SHA256":digest(h1/"manifest.json"),
       "frozen_H2_manifests_SHA256":{
           str(seed):digest(mechanism_root/f"null_seed_{seed}_frozen_top10_v1"/"manifest.json")
           for seed in SEEDS},
       "frozen_H2_null_top10_SHA256":null_hashes,
       "H2_all_seed_ID_and_real_score_parity":True,
       "H2_nested_in_H1":True,"no_target_label_or_metric_read":True,
       "A4_authorized_by_A3_lock":False,
       "note":"A4 still requires an independent scientific protocol and no-current-target-access audit."}
    out.mkdir(parents=True,mode=0o700)
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":manifest["status"],"main":30000,
                      "mechanism":4096,"A4_authorized":False}),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--h1",type=Path,required=True)
    p.add_argument("--mechanism-root",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    main(a.h1,a.mechanism_root,a.out)
