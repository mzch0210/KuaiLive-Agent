#!/usr/bin/env python3
"""Independent A5 scientific/structural audit over SEALED A4 private paired metrics.

Never open the raw current target author column. Do not fit any model, choose a
new seed, change a threshold, delete an event, or revise the A4 primary tests.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np,pyarrow.parquet as pq

MAIN_SHA="be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
H2_SHA="40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059"
SEEDS=(20261014,20261015,20261016)
KEYS=("sasrec_F_minus_S","gru4rec_F_minus_S","original_Full_minus_mean_three_nulls")

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()

def require(cond,err):
    if not cond:raise RuntimeError("A5 independent audit failure: "+err)

def by_date(eids,user_ids,pair_diff,weight,a1file):
    table=pq.read_table(a1file,columns=["source_event_id","user_id","day"])
    ids=table.column("source_event_id").to_numpy()
    users=table.column("user_id").to_numpy()
    days=table.column("day").to_pylist()
    require(np.array_equal(ids,eids) and np.array_equal(users,user_ids),
            "A1 outcome-blind row identity differs from sealed A4")
    grouped={}
    for date in sorted(set(days)):
        ix=np.array([d==date for d in days],bool)
        require(ix.sum()>0,"day stratum empty")
        grouped[str(date)]={"events":int(ix.sum()),
           "weighted_paired_effect":float(np.average(pair_diff[ix],weights=weight[ix]))}
    return grouped

def main(a1,a4,h2_structure,out):
    if out.exists():raise FileExistsError("A5 audit result already exists")
    aggregate=json.loads((a4/"aggregate.json").read_text())
    require(aggregate["status"]=="A4_ONE_SHOT_FROZEN_TARGETS_EVALUATED_NEVER_REOPTIMIZED"
            and not aggregate["TEST_policies_recalibrated"],
            "A4 full immutable result missing")
    private=a4/"private_paired_event_metrics.npz"
    require(sha(private)==aggregate["private_audit_SHA256"],"A4 private data SHA mismatch")
    v=np.load(private,allow_pickle=False)
    eid=v["event_ids"];user=v["user_ids"];w=v["weights"]
    gate=v["H1_gate_ndcg"];calls=v["H1_gate_calls"]
    memory=v["memory_F"];base=v["base_F"]
    mech_eid=v["mechanism_ids"];w2=v["mechanism_weights"]
    real=v["mechanism_real_ndcg"];null=v["mechanism_null_ndcg"]
    require(len(eid)==30000 and len(mech_eid)==4096 and gate.shape==(30000,2,2)
            and null.shape==(4096,3) and calls.shape==(30000,2,2),
            "expected complete H1/H2 paired events")
    require(sha(a1/"B4A_MAIN_30000_PRIVATE.parquet")==MAIN_SHA
            and sha(a1/"B4A_IDENTITY_4096_PRIVATE.parquet")==H2_SHA,
            "original sealed samples changed")
    effects=[float(np.average(gate[:,i,1]-gate[:,i,0],weights=w)) for i in (0,1)]
    effects.append(float(np.average(real-null.mean(axis=1),weights=w2)))
    for name,value in zip(KEYS,effects):
        original=aggregate["frozen_primary_comparisons"][name]["weighted_effect"]
        require(math.isclose(original,value,rel_tol=1e-12,abs_tol=1e-12),
                "A4 frozen paired mean does not reconstruct: "+name)
    quality={}
    for k,base_name in enumerate(("sasrec","gru4rec")):
        reported=aggregate["main_calls_and_quality"][base_name]
        require(math.isclose(float(np.average(base[:,k],weights=w)),
                                  reported["base_F_weighted_NDCG10"],abs_tol=1e-12),
                "base ranking mismatch")
        require(math.isclose(float(np.average(memory,weights=w)),
                                  reported["always_memory_F_weighted_NDCG10"],abs_tol=1e-12),
                "memory ranking mismatch")
        for ai,name in enumerate(("S_aligned","F_aligned")):
            row=reported["frozen_arms"][name]
            require(math.isclose(float(np.average(gate[:,k,ai],weights=w)),
                                         row["F_weighted_NDCG10"],abs_tol=1e-12),
                    "gate ranking mismatch")
            require(math.isclose(float(np.average(calls[:,k,ai],weights=w)),
                                         row["realized_weighted_call_fraction"],abs_tol=1e-12),
                    "weighted realized calls mismatch")
        quality[base_name]={"F_minus_S":effects[k],
            "F_call_fraction":float(calls[:,k,1].mean()),
            "S_call_fraction":float(calls[:,k,0].mean()),
            "non_equal_call_budget":abs(float(calls[:,k,1].mean())-
                                         float(calls[:,k,0].mean()))>.01,
            "per_source_date":by_date(eid,user,gate[:,k,1]-gate[:,k,0],w,
                                      a1/"B4A_MAIN_30000_PRIVATE.parquet")}
    nullmeans=[float(np.average(null[:,k],weights=w2)) for k in range(3)]
    realm=float(np.average(real,weights=w2))
    struct=json.loads((h2_structure/"summary.json").read_text())
    require(struct["status"]=="THREE_SOURCE_VALID_NULL_MAPS_PRIVATE_NO_RANKS",
            "H2 source structure changed")
    require([x["seed"] for x in struct["seed_results"]]==list(SEEDS),
            "unregistered H2 randomization")
    h2_checks=[]
    for k,seed in enumerate(SEEDS):
        item=struct["seed_results"][k]
        n_positive=int(np.count_nonzero(null[:,k]>0))
        quality_floor=bool(nullmeans[k]>=max(.10,.30*realm))
        positive_floor=bool(n_positive>=10)
        structural_floor=bool(item["fraction_changed"]>=.10)
        h2_checks.append({"seed":seed,
            "null_F_weighted_NDCG10":nullmeans[k],
            "real_F_weighted_NDCG10":realm,
            "null_positive_top10_count":n_positive,
            "fraction_of_source_edges_rewired":item["fraction_changed"],
            "quality_nonfloor":quality_floor,
            "positive_top10_nonfloor":positive_floor,
            "structural_nonfloor":structural_floor,
            "TRAIN_popularity_relative_nonfloor":"NOT_EVALUATED_ON_B4A",
            "complete_predeclared_nonfloor_certification":False})
    # Be explicit: no retrospective popularity baseline top10 was sealed in
    # A3, so cannot truthfully certify that auxiliary reference on new targets.
    independent={
      "schema":"kbs-b4a-a5-independent-paired-sha-and-nonfloor-audit-v1",
      "state":"COMPLETED_AGGREGATE_AUDIT_NOT_A_NEW_TEST",
      "A4_private_metrics_SHA256":aggregate["private_audit_SHA256"],
      "n_main":30000,"n_H2":4096,
      "reconstructed_primary_weighted_paired_effects":{
          n:val for n,val in zip(KEYS,effects)},
      "H1_sup_alignment_call_fairness":quality,
      "H2_fixed_seed_nonfloor_diagnostics":h2_checks,
      "H2_real_per_date":by_date(mech_eid,
          pq.read_table(a1/"B4A_IDENTITY_4096_PRIVATE.parquet",
                   columns=["user_id"]).column("user_id").to_numpy(),
          real-null.mean(axis=1),w2,a1/"B4A_IDENTITY_4096_PRIVATE.parquet"),
      "H2_original_vs_null_seeds_are_same_requests":True,
      "H2_full_predeclared_nonfloor_fully_certified":False,
      "H2_popularity_gap_requires_cautious_report":True,
      "raw_author_ids_opened_from_original_source_by_A5":False,
      "new_model_selection_or_test_reveal":False}
    out.mkdir(parents=True,mode=0o700)
    (out/"aggregate.json").write_text(json.dumps(independent,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"A5":independent["state"],
       "reconstructed_effects":independent["reconstructed_primary_weighted_paired_effects"],
       "H2_seed_validity":h2_checks,
       "no_new_label_read":True},sort_keys=True),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("a1","a4","h2-structure","out"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    main(a.a1,a.a4,a.h2_structure,a.out)
