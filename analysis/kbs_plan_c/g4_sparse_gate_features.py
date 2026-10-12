#!/usr/bin/env python3
"""Gate history-support feature with no Memory candidate scoring.

For any causal user prefix, positive long Memory support is equivalent to
membership in the TRAIN-known historical author keys. This exactly computes
the pretarget feature previously obtained by first evaluating all Memory
candidate scores and subtracting 0.10*TRAIN popularity, but does so sparsely.

Does not read labels, DEV outcomes or TEST. O(#history log #active authors).
"""
from __future__ import annotations
import numpy as np


def sparse_history_support_share(active_known_author_tokens, prior_warm_author_counts):
    """Fraction of time-eligible warm authors with strictly prior interactions.

    Candidate tokens are sorted ascending and unique. Raw histories include
    unknown TRAIN authors, but only known author tokens are in prior_warm counts.
    An author in short history necessarily occurs in the long history.
    """
    active=np.asarray(active_known_author_tokens,dtype=np.int64)
    if len(active)==0:
        raise ValueError("Empty eligible author candidate roster")
    if np.any(active[1:]<=active[:-1]):
        raise ValueError("Candidates must be distinct and sorted")
    if not prior_warm_author_counts:
        return 0.0
    previous=np.fromiter(prior_warm_author_counts.keys(),dtype=np.int64,
                          count=len(prior_warm_author_counts))
    if np.any(previous<=0):
        raise ValueError("History index 0 is padding and cannot be a known author")
    positions=np.searchsorted(active,previous)
    found=positions<len(active)
    found[found] &= active[positions[found]]==previous[found]
    return float(np.count_nonzero(found)/len(active))


def dense_reference_support_share(active,popularity,prior_warm,recent,all_author_max):
    """Unit-test-only reference to exactly evaluated Memory component support."""
    import math
    ids=np.asarray(active,dtype=np.int32)
    scores=0.10*popularity[ids].astype(np.float64).copy()
    rec=list(recent)[-10:]
    for j,token in enumerate(ids):
        if prior_warm:
            scores[j]+=0.45*prior_warm.get(int(token),0)/all_author_max
        short=max((math.exp(-distance/3.0)
                   for distance,item in enumerate(reversed(rec))
                   if int(item)==int(token)),default=0.0)
        scores[j]+=0.45*short
    signal=scores-0.10*popularity[ids]
    return float(np.mean(signal>1e-12))
