#!/usr/bin/env python3
"""B4-A A4 single outcome reveal, AFTER A3 H1/H2 SHA lock and independent audit.

The data stem is the SAME March-2026 collection period, newly sealed target IDs.
No model fit, threshold update, outcome-driven exclusion or second unseal allowed.
Only publish anonymized aggregates; raw identifiers / event utilities stay private.
"""
from __future__ import annotations
import argparse,hashlib,json,math,time
from pathlib import Path
import numpy as np,pyarrow.parquet as pq
from g5_unlabeled_test_score import active_rosters
from n9_b4a_a4_weighted_stat_contract import (
    weighted_paired_user_cluster, h2_eventwise_difference, holm3,
    expected_cell_weights, PRIMARY, BOOTSTRAPS, NULL_SEEDS,
)

A1_MAIN_SHA="be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
A1_H2_SHA="40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059"
N=30000;N_H2=4096;FAMILIES=("sasrec","gru4rec")
ARMS=("S_aligned","F_aligned")

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for part in iter(lambda:f.read(8<<20),b""):h.update(part)
    return h.hexdigest()

def require(cond,why):
    if not cond:raise RuntimeError(why)

def checked_array(root,filename,registered):
    path=root/filename
    require(sha(path)==registered,"frozen A3 output byte SHA changed: "+filename)
    return np.load(path,allow_pickle=False)

def ndcg_from_top10(top,truth):
    """Top-10 metric is zero outside first ten; no rank-11 inference."""
    top=np.asarray(top)
    truth=np.asarray(truth)
    require(top.ndim==2 and top.shape[1]==10 and truth.shape==(top.shape[0],),
            "Top-10/label shape mismatch")
    match=top==truth[:,None]
    require(np.all(match.sum(axis=1)<=1),"duplicate target in one fixed Top-10")
    rank=match.argmax(axis=1)+1
    return np.where(match.any(axis=1),1.0/np.log2(rank+1),0.0)

def verify_sealed_inputs(a1,h1,h2_root,lock,weights):
    """EVERY input and comparison must be verified before calling label vault."""
    final=json.loads((lock/"manifest.json").read_text())
    require(final["status"]=="A3_H1_H2_PREDICTIONS_SHA_LOCKED_A4_NOT_OPENED"
            and final["main_events"]==N and final["mechanism_events"]==N_H2
            and final["H2_all_seed_ID_and_real_score_parity"]
            and not final["A4_authorized_by_A3_lock"]
            and final["no_target_label_or_metric_read"],
            "A3 final lock not blind/complete")
    h1m=json.loads((h1/"manifest.json").read_text())
    require(sha(h1/"manifest.json")==final["frozen_H1_manifest_SHA256"]
            and h1m["status"]=="H1_30000_FROZEN_PREDICTIONS_A4_HARD_HOLD"
            and not h1m["test_rank_ndcg_hr_computed"]
            and not h1m["A4_unseal_authorized"]
            and not h1m["retrospective_target_retained_S_candidate_used"]
            and not h1m["thresholds_recalibrated_on_TEST"],
            "H1 not eligible for frozen A4")
    require(sha(a1/"B4A_MAIN_30000_PRIVATE.parquet")==A1_MAIN_SHA
            and sha(a1/"B4A_IDENTITY_4096_PRIVATE.parquet")==A1_H2_SHA,
            "A1 source samples unexpectedly changed")
    obj=json.loads(weights.read_text())
    require(obj["sample_main_SHA256"]==A1_MAIN_SHA
            and obj["sample_mechanism_SHA256"]==A1_H2_SHA
            and obj["population_total"]==4723652
            and obj["all_B4A_target_labels_read"] is False,
            "A2 original population weights not still frozen")
    h1_ids=checked_array(h1,"event_ids.npy",h1m["private_files_sha256"]["event_ids.npy"])
    h1_users=checked_array(h1,"user_ids.npy",h1m["private_files_sha256"]["user_ids.npy"])
    h1_top=checked_array(h1,"top10_base_and_memory_author_tokens.npy",
                         h1m["private_files_sha256"]["top10_base_and_memory_author_tokens.npy"])
    calls=checked_array(h1,"gate_calls.npy",h1m["private_files_sha256"]["gate_calls.npy"])
    counts=checked_array(h1,"candidate_counts.npy",h1m["private_files_sha256"]["candidate_counts.npy"])
    require(h1_ids.shape==(N,) and h1_top.shape==(N,3,10)
            and calls.shape==(N,2,2) and counts.shape==(N,)
            and np.all(counts>=10),"frozen H1 dimensions/candidates invalid")
    require(len(set(h1_ids.tolist()))==N,"repeated H1 event IDs")
    for family in FAMILIES:
        require(family in h1m["frozen_gate_model_SHA256"] and
                set(h1m["frozen_gate_model_SHA256"][family])==set(ARMS),
                "H1 original F/S frozen gate source missing")
    h2_arrays=[];reference=None;original_top=None
    for seed in NULL_SEEDS:
        folder=h2_root/f"null_seed_{seed}_frozen_top10_v1"
        m=json.loads((folder/"manifest.json").read_text())
        require(sha(folder/"manifest.json")==final["frozen_H2_manifests_SHA256"][str(seed)]
                and m["status"]=="H2_SEED_FROZEN_4096_UNLABELED_TOP10"
                and m["seed"]==seed and m["n_events"]==N_H2
                and m["H1_original_memory_top10_exact_match"]
                and not m["target_ndcg_rank_hr_computed"]
                and not m["A4_authorized"],
                "H2 sealed null invalid")
        ids=checked_array(folder,"event_ids.npy",m["files_sha256"]["event_ids.npy"])
        orig=checked_array(folder,"original_full_f_top10.npy",
                           m["files_sha256"]["original_full_f_top10.npy"])
        null=checked_array(folder,"null_full_f_top10.npy",
                           m["files_sha256"]["null_full_f_top10.npy"])
        require(ids.shape==(N_H2,) and orig.shape==(N_H2,10) and null.shape==(N_H2,10),
                "H2 Top-10 shape changed")
        if reference is None:reference=ids;original_top=orig
        else:require(np.array_equal(ids,reference) and
                     np.array_equal(orig,original_top),"H2 arms don't share requests")
        h2_arrays.append(null)
    require(set(reference.tolist()).issubset(set(h1_ids.tolist())),
            "H2 target ID not nested in main H1 targets")
    # A1 metadata only, never read target author yet.
    mainmeta=pq.read_table(a1/"B4A_MAIN_30000_PRIVATE.parquet",
             columns=["source_event_id","user_id","observed_at","day","history_group"])
    subset=pq.read_table(a1/"B4A_IDENTITY_4096_PRIVATE.parquet",
             columns=["source_event_id","user_id","observed_at","day","history_group"])
    require(np.array_equal(mainmeta.column("source_event_id").to_numpy(),h1_ids)
            and np.array_equal(mainmeta.column("user_id").to_numpy(),h1_users)
            and np.array_equal(subset.column("source_event_id").to_numpy(),reference),
            "A3/A1 metadata row ordering mismatch")
    def cell_weights(table,kind):
        rows=obj[kind]["strata"]
        population={(x["date"],x["history_q"]):int(x["population_n"]) for x in rows}
        sample={(x["date"],x["history_q"]):int(x["sample_n"]) for x in rows}
        labels=[(str(d),str(q)) for d,q in zip(
            table.column("day").to_pylist(),table.column("history_group").to_pylist())]
        w=expected_cell_weights(labels,population,sample)
        require(math.isclose(float(w.sum()),4723652.,rel_tol=1e-10),
                "original population weights not recovered")
        return w
    w_main=cell_weights(mainmeta,"main")
    w_h2=cell_weights(subset,"mechanism")
    return (h1m,final,h1_ids,h1_users,h1_top,calls,counts,
            mainmeta,reference,subset,original_top,np.stack(h2_arrays,axis=1),
            w_main,w_h2)


def main(cache,g1,index,a1,h1,h2_root,lock,weights,out):
    # Fresh lock artifact may NOT preexist. Once first unseal begins, preserve
    # an attempt marker, and refuse reruns even after technical exceptions.
    if out.exists() or out.with_name(out.name+".unseal_in_progress").exists():
        raise FileExistsError("B4-A A4 can only unseal ONCE")
    start=time.monotonic()
    (h1m,final,ids,users,top,calls,counts,mainmeta,
     mechanism_ids,subset,real_top,null_top,w,w2)=verify_sealed_inputs(
         a1,h1,h2_root,lock,weights)
    # Up to this line all data were TARGET-BLIND. Seal A4 attempt before
    # the first current author label from causal source can be accessed.
    pending=out.with_name(out.name+".unseal_in_progress")
    pending.mkdir(parents=True,mode=0o700,exist_ok=False)
    attempt={"state":"A4_STARTED_EXACT_ONCE_UNSEAL_ATTEMPT",
             "frozen_A3_manifest_SHA256":sha(lock/"manifest.json"),
             "A1_main_SHA256":A1_MAIN_SHA,"A1_nested_SHA256":A1_H2_SHA,
             "statistical_test_family":PRIMARY,"null_seeds":NULL_SEEDS,
             "bootstrap_draws":BOOTSTRAPS,"raw_labels_logged_or_published":False}
    (pending/"attempt.json").write_text(json.dumps(attempt,sort_keys=True,indent=2)+"\n")
    # SINGLE authorized projection containing selected current authors.
    requested={int(e):i for i,e in enumerate(ids)}
    target_raw=np.full(N,-1,dtype=np.int64)
    expected_users=users
    expected_clocks=mainmeta.column("observed_at").to_pylist()
    seen=0
    for block in pq.ParquetFile(g1/"causal_stream_sealed.parquet").iter_batches(
        batch_size=262144,
        columns=["source_event_id","user_id","author_id","observed_at","split"]):
        d=block.to_pydict()
        for eid,user,author,clock,split in zip(d["source_event_id"],
                                                d["user_id"],d["author_id"],
                                                d["observed_at"],d["split"]):
            i=requested.get(int(eid))
            if i is None:continue
            require(target_raw[i]==-1,"duplicate target author or source event in unseal")
            require(split=="TEST" and int(user)==int(expected_users[i])
                    and clock==expected_clocks[i],
                    "A4 label source did not align with the original blind request")
            target_raw[i]=int(author);seen+=1
    require(seen==N and np.all(target_raw>=0),"incomplete one-shot TEST target author reveal")
    warm=np.load(index/"authors.npy",mmap_mode="r")
    token_pos=np.searchsorted(warm,target_raw)
    require(np.all(token_pos<len(warm)),"unsealed target not TRAIN-known")
    require(np.all(warm[token_pos]==target_raw),"unsealed author not in TRAIN-known fixed universe")
    truth=token_pos.astype(np.int32)+1
    # Explicitly validate each target is in the original Full-F eligible roster,
    # not merely absent from a Top-10 ranking. Never outcome-selectively exclude.
    known={int(a):i+1 for i,a in enumerate(warm)}
    for i,roster in active_rosters(g1/"available_room_intervals.parquet",
                                   expected_clocks,known):
        require(len(roster)==int(counts[i]),"A4 active author roster differs from A3")
        p=int(np.searchsorted(roster,int(truth[i])))
        require(p<len(roster) and roster[p]==int(truth[i]),
                "A4 author not eligible in precommitted Full-F roster")
    # The target was never passed to the A3 scorer. At this point the reveal
    # is irrevocable; no ML fitting or policy calibration is permitted.
    base=np.column_stack([ndcg_from_top10(top[:,j,:],truth) for j in (0,1)])
    mem=ndcg_from_top10(top[:,2,:],truth)
    policy=np.empty((N,2,2),dtype=np.float64)
    quality={}
    delta=[]
    for j,family in enumerate(FAMILIES):
        arms={}
        for k,arm in enumerate(ARMS):
            policy[:,j,k]=base[:,j]+calls[:,j,k]*(mem-base[:,j])
            arms[arm]={"F_weighted_NDCG10":float(np.average(policy[:,j,k],weights=w)),
                       "realized_weighted_call_fraction":float(np.average(calls[:,j,k],weights=w)),
                       "realized_unweighted_call_fraction":float(calls[:,j,k].mean()),
                       "n_calls":int(calls[:,j,k].sum())}
        quality[family]={"base_F_weighted_NDCG10":float(np.average(base[:,j],weights=w)),
            "always_memory_F_weighted_NDCG10":float(np.average(mem,weights=w)),
            "frozen_arms":arms,
            "raw_call_rate_gap":abs(arms["F_aligned"]["realized_unweighted_call_fraction"]-
                                    arms["S_aligned"]["realized_unweighted_call_fraction"]),
            "not_strict_equal_budget":abs(arms["F_aligned"]["realized_unweighted_call_fraction"]-
                                          arms["S_aligned"]["realized_unweighted_call_fraction"])>0.01}
        delta.append(policy[:,j,1]-policy[:,j,0])
    subset_index={int(e):i for i,e in enumerate(ids)}
    selection=np.asarray([subset_index[int(e)] for e in mechanism_ids],dtype=np.int64)
    require(len(np.unique(selection))==N_H2,"H2 repeated index")
    truth2=truth[selection]
    users2=users[selection]
    real_ndcg=ndcg_from_top10(real_top,truth2)
    three_null=np.column_stack([
        ndcg_from_top10(null_top[:,k,:],truth2) for k in range(3)])
    diffs=h2_eventwise_difference(real_ndcg,three_null)
    delta.append(diffs)
    results=[
        weighted_paired_user_cluster(delta[0],users,w,seed=20261014),
        weighted_paired_user_cluster(delta[1],users,w,seed=20261014),
        weighted_paired_user_cluster(delta[2],users2,w2,seed=20261014),
    ]
    raw_p=[x["one_sided_cluster_signflip_p"] for x in results]
    adjusted=holm3(raw_p)
    primaries={}
    for i,k in enumerate(PRIMARY):
        primaries[k]={**results[i],"holm3_adjusted_one_sided_p":float(adjusted[i]),
                      "directional_reject_at_0_05":bool(adjusted[i]<.05)}
    manifest={"schema":"kbs-b4a-a4-first-and-only-same-period-target-heldout-v1",
        "status":"A4_ONE_SHOT_FROZEN_TARGETS_EVALUATED_NEVER_REOPTIMIZED",
        "A3_complete_lock_SHA256":sha(lock/"manifest.json"),
        "A1_main_and_H2_sample_SHA256":[A1_MAIN_SHA,A1_H2_SHA],
        "n_main_requests":N,"n_main_users":int(len(np.unique(users))),
        "n_mechanism_requests":N_H2,"n_mechanism_users":int(len(np.unique(users2))),
        "source_period":"MARCH_2026_SAME_COLLECTION_AS_G5_NOT_NEW_CHRONOLOGICAL_PERIOD",
        "statistical_design":"20_CELL_NATURAL_ELIGIBLE_SOURCE_POPULATION_WEIGHTED_RATIO",
        "main_Kish_n_eff":float(w.sum()**2/np.square(w).sum()),
        "h2_Kish_n_eff":float(w2.sum()**2/np.square(w2).sum()),
        "main_calls_and_quality":quality,"H2_full_real_vs_null":{
          "real_weighted_NDCG10":float(np.average(real_ndcg,weights=w2)),
          "seed_null_weighted_NDCG10":{
             str(seed):float(np.average(three_null[:,k],weights=w2))
             for k,seed in enumerate(NULL_SEEDS)},
          "mean_three_null_weighted_NDCG10":float(np.average(three_null.mean(axis=1),weights=w2))},
        "frozen_primary_comparisons":primaries,
        "one_sided_familywise_method":"HOLM_3",
        "bootstrap_and_signflip_user_cluster_draws":5000,
        "signflip_reliance":"USER_CLUSTER_SIGN_SYMMETRY_ASSUMPTION",
        "TEST_policies_recalibrated":False,
        "true_same_candidate_control":True,
        "three_seed_nulls_not_three_independent_TESTS":True,
        "any_success_claim_prior_to_this_A4":False,
        "author_IDs_or_private_edge_data_public":False,
        "unfavorable_effects_also_reported":True,
        "wall_seconds":round(time.monotonic()-start,2)}
    # Preserve full paired result for author-only audit; not exported to public repo.
    np.savez_compressed(pending/"private_paired_event_metrics.npz",
        event_ids=ids,user_ids=users,weights=w,
        base_F=base,memory_F=mem,H1_gate_calls=calls,H1_gate_ndcg=policy,
        mechanism_ids=mechanism_ids,mechanism_weights=w2,
        mechanism_real_ndcg=real_ndcg,mechanism_null_ndcg=three_null)
    manifest["private_audit_SHA256"]=sha(pending/"private_paired_event_metrics.npz")
    (pending/"aggregate.json").write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
    pending.rename(out)
    # Print only safe aggregates, never event/user/author IDs or private metrics rows.
    print(json.dumps({"status":manifest["status"],"n_main":N,
        "n_mechanism":N_H2,
        "primary_effects":{k:{"effect":v["weighted_effect"],
            "ci95":v["cluster_ci95"],"Holm_p":v["holm3_adjusted_one_sided_p"]}
            for k,v in primaries.items()},
        "TEST_model_or_threshold_updates":False},sort_keys=True),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("cache","g1","index","a1","h1","h2-root","lock","weights","out"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    main(a.cache,a.g1,a.index,a.a1,a.h1,a.h2_root,a.lock,a.weights,a.out)
