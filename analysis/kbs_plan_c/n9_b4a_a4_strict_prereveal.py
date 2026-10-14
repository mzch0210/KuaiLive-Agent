#!/usr/bin/env python3
"""A4 stand-alone read-only pre-reveal verification: ZERO access to current authors."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
from n9_b4a_a4_one_shot_unseal import (
    verify_sealed_inputs,ndcg_from_top10,sha,PRIMARY,NULL_SEEDS
)

def main(a1,h1,h2_root,lock,weights,out):
    if out.exists():raise FileExistsError("Do not overwrite prereveal verification")
    (h1m,final,ids,users,top,calls,counts,mainmeta,
     mechanism_ids,subset,original,null,w,w2) = verify_sealed_inputs(
            a1,h1,h2_root,lock,weights)
    if not (len(ids)==30000 and len(mechanism_ids)==4096
            and top.shape==(30000,3,10)
            and null.shape==(4096,3,10)
            and calls.shape==(30000,2,2)):
        raise RuntimeError("A4 frozen input shape violation")
    if np.any(np.diff(np.sort(ids))==0) or np.any(np.diff(np.sort(mechanism_ids))==0):
        raise RuntimeError("duplicate frozen prediction identity")
    if (len(PRIMARY)!=3 or tuple(NULL_SEEDS)!=(20261014,20261015,20261016)):
        raise RuntimeError("A4 primary analysis family changed")
    # Synthetic-only boundary: no real target token is available to this script.
    fake_top=np.array([[2,5,6,7,8,9,10,11,12,13],
                       [3,4,5,6,7,8,9,10,11,12]],dtype=np.int32)
    fake=np.array([2,100],dtype=np.int32)
    if not np.allclose(ndcg_from_top10(fake_top,fake),[1,0]):
        raise RuntimeError("Top-10 metric synthetic sanity failed")
    report={"schema":"kbs-b4a-a4-strict-prereveal-input-verification-v1",
        "status":"PASS_ALL_A3_SHA_AND_FROZEN_PRIMARY_ESTIMANDS_NO_LABELS_READ",
        "A3_final_lock_SHA256":sha(lock/"manifest.json"),
        "A3_main_SHA256":h1m["source_sample_SHA256"],
        "main_events":len(ids),
        "H2_events":len(mechanism_ids),
        "null_seed_count":3,
        "Kish_n_eff_main":float(w.sum()**2/(w@w)),
        "Kish_n_eff_mechanism":float(w2.sum()**2/(w2@w2)),
        "A4_primary_comparisons":PRIMARY,
        "frozen_seed_nulls":NULL_SEEDS,
        "target_author_column_opened":False,
        "A4_NDCG_computed_from_real_targets":False,
        "A4_unseal_approved_by_technical_preflight":False}
    out.mkdir(parents=True,mode=0o700)
    (out/"summary.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps(report,sort_keys=True),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("a1","h1","h2-root","lock","weights","out"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    main(a.a1,a.h1,a.h2_root,a.lock,a.weights,a.out)
