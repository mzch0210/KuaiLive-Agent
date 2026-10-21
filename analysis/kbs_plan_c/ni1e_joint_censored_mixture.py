#!/usr/bin/env python3
"""NI-1e PUBLIC SYNTHETIC: shared-negative four-state censored rank mixture.

Latent rank-pair support is ASSUMED externally known; only its conditional
mixture weights are learned from sampled Base/Memory NDCG@10 and known N.
This is not a validated estimator for M3 and never reads DEV/TEST.
"""
from __future__ import annotations
import bisect
import json
import random
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction
from itertools import accumulate
from math import comb, log, log2

DRAW=574
K=10
# (label, full rank Base, full rank Memory, ahead-target overlap)
STATES=(("A",3,8,2),("B",14,5,3),("C",40,18,7),("D",12,11,6))
WRONG_STATES=(STATES[0],STATES[1],("C_wrong",40,9,7),STATES[3])
GROUPS=((14022,(.25,.10,.55,.10)),(53762,(.10,.55,.15,.20)))

def ndcg(rank:int)->float:
    return 1/log2(rank+1) if rank<=K else 0.

def full_delta(state:tuple)->float:
    return ndcg(state[2])-ndcg(state[1])

@lru_cache(maxsize=64)
def joint_emission(N:int,base_rank:int,memory_rank:int,overlap:int)->dict:
    """Combinatorial emission P((min(X_B,10),min(X_M,10)) | latent state).
    Both rankers use ONE sampled 574-negative set. 10 is censored >=10.
    """
    if not(N>DRAW and 1<=base_rank<=N and 1<=memory_rank<=N):
        raise ValueError("invalid N/ranks")
    a,b=base_rank-1,memory_rank-1
    if not max(0,a+b-(N-1))<=overlap<=min(a,b):
        raise ValueError("infeasible ahead-target overlap")
    cells=(overlap,a-overlap,b-overlap,N-1-a-b+overlap)
    denom=comb(N-1,DRAW)
    out=defaultdict(int)
    for both in range(min(cells[0],DRAW)+1):
        for bo in range(min(cells[1],DRAW-both)+1):
            for mo in range(min(cells[2],DRAW-both-bo)+1):
                tail=DRAW-both-bo-mo
                if 0<=tail<=cells[3]:
                    ways=comb(cells[0],both)*comb(cells[1],bo)*comb(cells[2],mo)*comb(cells[3],tail)
                    out[(min(K,both+bo),min(K,both+mo))]+=ways
    if sum(out.values())!=denom:
        raise ArithmeticError("joint pmf normalization failure")
    return {key:float(Fraction(val,denom)) for key,val in out.items()}

def state_emissions(N:int,states:tuple=STATES)->list:
    return [joint_emission(N,*s[1:]) for s in states]

def generate_sampled(N:int,prior:tuple,rows:int,seed:int)->Counter:
    """Synthetic generator knows full latent state; only labels leave it."""
    if len(prior)!=len(STATES) or any(p<0 for p in prior) or abs(sum(prior)-1)>1e-10 or rows<1:
        raise ValueError("invalid synthetic design")
    rng=random.Random(seed)
    emissions=state_emissions(N)
    categories=sorted(set().union(*(d.keys() for d in emissions)))
    cdfs=[list(accumulate(d.get(k,0.) for k in categories)) for d in emissions]
    state_cdf=list(accumulate(prior))
    counts=Counter()
    for _ in range(rows):
        s=min(bisect.bisect_left(state_cdf,rng.random()),len(prior)-1)
        y=min(bisect.bisect_left(cdfs[s],rng.random()),len(categories)-1)
        counts[categories[y]]+=1
    return counts

def raw_delta(counts:Counter)->float:
    return sum(c*(ndcg(y[1]+1)-ndcg(y[0]+1)) for y,c in counts.items())/sum(counts.values())

def fit_em(N:int,counts:Counter,states:tuple=STATES,maxiter:int=5000,tol:float=1e-8)->dict:
    """Observed-pair-label likelihood only; F labels NEVER passed to fitter."""
    emissions=state_emissions(N,states)
    observations=list(counts.items())
    probabilities=[[d.get(cat,0.) for d in emissions] for cat,_ in observations]
    weights=[1/len(states)]*len(states)
    total=sum(counts.values())
    for iteration in range(maxiter):
        expected=[0.]*len(states)
        for (_,amount),pr in zip(observations,probabilities):
            denom=sum(w*p for w,p in zip(weights,pr))
            if denom<=0:
                raise ArithmeticError("sampled observation impossible under support")
            for j,p in enumerate(pr):
                expected[j]+=amount*weights[j]*p/denom
        new=[v/total for v in expected]
        shift=max(abs(a-b) for a,b in zip(new,weights))
        weights=new
        if shift<tol:
            break
    return {"weights":weights,
            "eta_F_assumption_based":sum(w*full_delta(s) for w,s in zip(weights,states)),
            "iterations":iteration+1,"converged":shift<tol}

def heldout_sampled_logloss(N:int,counts:Counter,weights:list,states:tuple=STATES)->float:
    emissions=state_emissions(N,states)
    return -sum(num*log(max(sum(w*d.get(cat,0.) for w,d in zip(weights,emissions)),1e-300))
                for cat,num in counts.items())/sum(counts.values())

def trial(seed:int=20261020,train_per_group:int=20000,heldout_per_group:int=4000)->dict:
    groups=[]
    for i,(N,prior) in enumerate(GROUPS):
        train=generate_sampled(N,prior,train_per_group,seed+100*i)
        heldout=generate_sampled(N,prior,heldout_per_group,seed+100*i+17)
        fit=fit_em(N,train)
        wrong=fit_em(N,train,WRONG_STATES)
        groups.append({
            "N":N,
            "true_eta_generator_only":sum(p*full_delta(s) for p,s in zip(prior,STATES)),
            "raw_S_eta":raw_delta(train),
            "correct_family_eta":fit["eta_F_assumption_based"],
            "wrong_family_eta":wrong["eta_F_assumption_based"],
            "correct_heldout_sampled_logloss":heldout_sampled_logloss(N,heldout,fit["weights"]),
            "wrong_heldout_sampled_logloss":heldout_sampled_logloss(N,heldout,wrong["weights"],WRONG_STATES),
            "correct_family_weights":fit["weights"],
            "wrong_family_weights":wrong["weights"],
            "correct_converged":fit["converged"],
            "wrong_converged":wrong["converged"],
        })
    winner=max(range(2),key=lambda i:groups[i]["true_eta_generator_only"])
    allocations={}
    for name,key in (("raw_S","raw_S_eta"),("correct_family","correct_family_eta"),
                     ("wrong_family","wrong_family_eta"),("full_oracle","true_eta_generator_only")):
        chosen=max(range(2),key=lambda i:groups[i][key])
        allocations[name]={"chosen_group":chosen,"calls_per_two_requests":1,
                           "population_regret":(groups[winner]["true_eta_generator_only"]-
                                                 groups[chosen]["true_eta_generator_only"])/2}
    return {"seed":seed,"train_per_group":train_per_group,"heldout_per_group":heldout_per_group,
            "groups":groups,"equal_50pct_group_allocation":allocations}

def summary(repetitions:int=6,train_per_group:int=20000,heldout_per_group:int=4000)->dict:
    runs=[trial(seed=20261020+i,train_per_group=train_per_group,
                heldout_per_group=heldout_per_group) for i in range(repetitions)]
    counts={k:sum(r["equal_50pct_group_allocation"][k]["chosen_group"]==1 for r in runs)
            for k in runs[0]["equal_50pct_group_allocation"]}
    fields=("true_eta_generator_only","raw_S_eta","correct_family_eta",
            "wrong_family_eta","correct_heldout_sampled_logloss","wrong_heldout_sampled_logloss")
    averaged=[{k:sum(r["groups"][g][k] for r in runs)/len(runs) for k in fields} for g in range(2)]
    return {
        "scope":"PUBLIC_SYNTHETIC_ONLY_SHARED_NEGATIVE_CENSORED_SAMPLE",
        "assumptions":"Known FOUR latent full-rank B/M/overlap atoms; unknown conditional weights",
        "true_mixture_generator_only":GROUPS,
        "repetitions":repetitions,"train_per_group":train_per_group,
        "sampled_label_heldout_per_group":heldout_per_group,
        "group_mean":averaged,
        "times_chose_truly_best_group_B":counts,
        "first_run":runs[0],
        "warning":"Strong assumed support leaks structural rank knowledge; NO validation for actual M3."
    }

if __name__=="__main__":
    print(json.dumps(summary(),indent=2))
