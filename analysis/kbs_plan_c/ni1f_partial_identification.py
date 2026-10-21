#!/usr/bin/env python3
"""Public NI-1f: finite-library partial identification for censored shared-S labels.

LP sharp only WITHIN declared artificial candidate-rank library and tolerance;
TV radii are sensitivity scenarios, NOT confidence intervals for M3.
Requires numpy==2.1.3 and scipy==1.14.1. Never reads private DEV/TEST.
"""
from __future__ import annotations
from functools import lru_cache
from math import comb, log2
import json
import numpy as np
from scipy.optimize import linprog

N_VALUES = (14022, 53762)
DRAW, K = 574, 10
LIBRARY = (
 ('A',3,8,2),('B',14,5,3),('C',40,18,7),('D',12,11,6),
 ('E',5,14,3),('F',14,7,4),('G',9,10,7),('H',10,9,7),
 ('I',11,12,8),('J',12,10,6),('K',20,12,8),('L',12,20,8),
 ('M',5,5,4),('N',18,18,12),('O',40,9,7),('P',30,30,20),
)
TRUE_MIXTURE = ((.25,.10,.55,.10),(.10,.55,.15,.20))

@lru_cache(maxsize=128)
def emission(N, rank_B, rank_M, overlap):
    """Joint sampled rank distribution; 10 means X>=10, and both experts
    use EXACTLY the same 574 negative candidates."""
    if N <= DRAW or not (1 <= rank_B <= N and 1 <= rank_M <= N):
        raise ValueError("Invalid roster or rank")
    a,b=rank_B-1,rank_M-1
    if not max(0,a+b-(N-1)) <= overlap <= min(a,b):
        raise ValueError("Invalid shared-ahead overlap")
    cells=(overlap,a-overlap,b-overlap,N-1-a-b+overlap)
    denom=comb(N-1,DRAW)
    counts={}
    for i in range(min(cells[0],DRAW)+1):
        for j in range(min(cells[1],DRAW-i)+1):
            for k in range(min(cells[2],DRAW-i-j)+1):
                t=DRAW-i-j-k
                if 0 <= t <= cells[3]:
                    ways=comb(cells[0],i)*comb(cells[1],j)*comb(cells[2],k)*comb(cells[3],t)
                    category=(min(K,i+j),min(K,i+k))
                    counts[category]=counts.get(category,0)+ways
    if sum(counts.values()) != denom:
        raise ArithmeticError("Joint hypergeometric emission not normalized")
    return {cat:value/denom for cat,value in counts.items()}

def full_delta(rB,rM):
    def u(r):return 1/log2(r+1) if r<=K else 0.0
    return u(rM)-u(rB)

def matrix(N):
    columns=[emission(N,*state[1:]) for state in LIBRARY]
    cats=sorted(set().union(*(set(d) for d in columns)))
    A=np.array([[col.get(cat,0.) for col in columns] for cat in cats])
    v=np.array([full_delta(s[1],s[2]) for s in LIBRARY])
    return cats,A,v

def bounds(A, observed, values, tv_radius):
    """Min/max full F delta over nonnegative mixture with sampled-label TV <= radius.
    L1 norm of Aw-observed represented with nonnegative slack.
    """
    L,J=A.shape
    upper=np.block([[A,-np.eye(L)],[-A,-np.eye(L)],
                    [np.zeros((1,J)),np.ones((1,L))]])
    limits=np.r_[observed,-observed,2*tv_radius]
    eq=np.r_[np.ones(J),np.zeros(L)].reshape(1,-1)
    kwargs={"A_ub":upper,"b_ub":limits,"A_eq":eq,"b_eq":np.array([1.]),
            "bounds":[(0,None)]*(J+L),"method":"highs"}
    lo=linprog(np.r_[values,np.zeros(L)],**kwargs)
    hi=linprog(np.r_[-values,np.zeros(L)],**kwargs)
    if not lo.success or not hi.success:
        raise RuntimeError(f"LP infeasible/unstable: {lo.message} | {hi.message}")
    out=[]
    for result in (lo,hi):
        weights=result.x[:J]
        out.append({"value":float(weights@values),
                    "actual_tv":float(np.abs(A@weights-observed).sum()/2),
                    "top_weights":[(LIBRARY[i][0],round(float(weights[i]),6))
                         for i in np.argsort(-weights)[:5] if weights[i]>1e-6]})
    return out

def evaluate(N, prior, tolerances=(1e-7,.001,.005,.01)):
    cats,A,v=matrix(N)
    w=np.zeros(len(LIBRARY));w[:4]=prior
    p=A@w
    spectrum=np.linalg.svd(A,compute_uv=False)
    data=[]
    for tol in tolerances:
        lo,hi=bounds(A,p,v,tol)
        data.append({"TV_radius":tol,"lower":lo["value"],"upper":hi["value"],
                     "width":hi["value"]-lo["value"],
                     "contains_zero":lo["value"]<=0<=hi["value"],
                     "lower_witness":lo,"upper_witness":hi})
    return {"N":N,"library_size":len(LIBRARY),"sampled_label_categories":len(cats),
            "matrix_rank_at_abs_1e_minus_12":int(np.linalg.matrix_rank(A,tol=1e-12)),
            "singular_min_max_ratio":float(spectrum[-1]/spectrum[0]),
            "generator_only_true_full_delta":float(w@v),"envelopes":data}

def sampled_noise(N, prior, sizes=(500,2000,20000,50000), reps=20):
    """Pure synthetic independent multinomial sampling: not statistical CI."""
    _,A,_=matrix(N)
    w=np.zeros(len(LIBRARY));w[:4]=prior
    p=A@w
    rng=np.random.default_rng(20261020+N)
    out=[]
    for n in sizes:
        scores=[float(np.abs(rng.multinomial(n,p)/n-p).sum()/2) for _ in range(reps)]
        out.append({"rows":n,"median_empirical_TV":float(np.median(scores)),
                    "max_empirical_TV":float(np.max(scores)),"repeats":reps})
    return out

def report():
    return {"scope":"PUBLIC_SYNTHETIC_ONLY_NO_PRIVATE_DEV_TEST",
            "warning":"Finite externally declared 16-atom library contains generator states; "
                      "tolerances are stress scenarios (1e-7 approximate numeric equality), "
                      "NOT confidence radii, and rank-support assumptions are unknown for real M3.",
            "cases":[dict(evaluate(N,prior),
                          **{"finite_sample_synthetic_noise":sampled_noise(N,prior)})
                     for N,prior in zip(N_VALUES,TRUE_MIXTURE)]}

if __name__=="__main__":
    print(json.dumps(report(),indent=2))
