#!/usr/bin/env python3
"""B4-A A4/A5 pre-reveal statistical contract functions.

Pure numerical routines only. Never reads datasets or reveals TARGET labels.
Do not import this in the A3 pipeline, and do not use it to reoptimize gates.
"""
from __future__ import annotations
import numpy as np

BOOTSTRAPS = 5000
PRIMARY = ("sasrec_F_minus_S", "gru4rec_F_minus_S", "original_Full_minus_mean_three_nulls")
NULL_SEEDS = (20261014, 20261015, 20261016)


def holm3(raw):
    """Return Holm-adjusted p-values in original three-contrast order."""
    p=np.asarray(raw,dtype=np.float64)
    if p.shape!=(3,) or not np.isfinite(p).all() or np.any((p<0)|(p>1)):
        raise ValueError("Exactly three frozen primary directional p-values required")
    ranked=np.argsort(p,kind="stable")
    out=np.empty(3,dtype=np.float64)
    running=0.
    for k,i in enumerate(ranked):
        running=max(running,min(1.0,(3-k)*p[i]))
        out[i]=running
    return out


def weighted_paired_user_cluster(delta, user, weight, *, seed=20261014, reps=BOOTSTRAPS):
    """User-cluster paired 95% percentile CI plus user-level signflip p.

    The null signflip test assumes symmetric user-cluster weighted outcome
    contributions; Holm correction across the three primary contrasts happens
    OUTSIDE this routine. Weighted event means target the pre-frozen eligible
    source event population, not 20 equally frequent sample design cells.
    """
    delta=np.asarray(delta,dtype=np.float64)
    user=np.asarray(user)
    weight=np.asarray(weight,dtype=np.float64)
    if delta.ndim!=1 or user.ndim!=1 or weight.ndim!=1:
        raise ValueError("Expected one event column per argument")
    n=len(delta)
    if n==0 or len(user)!=n or len(weight)!=n:
        raise ValueError("Paired arrays must have same positive number of events")
    if not np.isfinite(delta).all() or not np.isfinite(weight).all() or np.any(weight<=0):
        raise ValueError("Finite positive pretarget weights required")
    if reps!=5000:raise ValueError("A2 preregistered exactly 5000 resamples")
    ids,inv=np.unique(user,return_inverse=True)
    if len(ids)<2:raise ValueError("At least two independent user clusters needed")
    numerator=np.bincount(inv,weights=weight*delta,minlength=len(ids))
    denom=np.bincount(inv,weights=weight,minlength=len(ids))
    if np.any(denom<=0):raise ValueError("empty user cluster")
    point=float(numerator.sum()/denom.sum())
    samples=np.empty(reps,dtype=np.float64)
    signs=np.empty(reps,dtype=np.float64)
    rng=np.random.default_rng(seed)
    # Chunked resampling bounds temporary RAM for >10,000 users.
    m=len(ids)
    for offset in range(0,reps,24):
        k=min(24,reps-offset)
        chosen=rng.integers(m,size=(k,m),dtype=np.int32)
        samples[offset:offset+k]=numerator[chosen].sum(axis=1)/denom[chosen].sum(axis=1)
        flip=2*rng.integers(0,2,size=(k,m),dtype=np.int8).astype(np.float64)-1
        signs[offset:offset+k]=(flip*numerator).sum(axis=1)/denom.sum()
    lo,hi=np.quantile(samples,[.025,.975])
    # Strictly one-sided: positive effect is the predeclared direction.
    p=float((1+np.sum(signs>=point))/(reps+1))
    return {"weighted_effect":point,"cluster_ci95":[float(lo),float(hi)],
            "one_sided_cluster_signflip_p":p,"cluster_users":int(m),
            "n_events":int(n),"bootstrap_and_null_draws":reps,
            "null_sign_symmetry_required":True}


def h2_eventwise_difference(real_ndcg, three_null_ndcg):
    """Average the three predeclared nulls WITHIN event, before any cluster CI."""
    r=np.asarray(real_ndcg,dtype=np.float64)
    null=np.asarray(three_null_ndcg,dtype=np.float64)
    if r.ndim!=1 or null.shape!=(len(r),3):
        raise ValueError("H2 must be events x exactly three fixed null arms")
    if not np.isfinite(r).all() or not np.isfinite(null).all():
        raise ValueError("nonfinite H2 NDCG")
    if np.any((r<0)|(r>1)) or np.any((null<0)|(null>1)):
        raise ValueError("NDCG not in [0,1]")
    return r-null.mean(axis=1)


def expected_cell_weights(cell_labels, frozen_cell_population, frozen_sample_count):
    """Look up PRETARGET registered post-stratification weights only."""
    labels=list(cell_labels)
    if set(frozen_cell_population)!=set(frozen_sample_count):
        raise ValueError("Unmatched original 20 design-cell population counts")
    if len(frozen_cell_population)!=20:
        raise ValueError("Original 20-cell design must be frozen")
    for key in frozen_cell_population:
        if not (frozen_cell_population[key]>0 and frozen_sample_count[key]>0):
            raise ValueError("Invalid frozen cell counts")
    if any(label not in frozen_cell_population for label in labels):
        raise ValueError("Test record not in frozen cell registry")
    return np.asarray(
        [frozen_cell_population[c]/frozen_sample_count[c] for c in labels],
        dtype=np.float64)
