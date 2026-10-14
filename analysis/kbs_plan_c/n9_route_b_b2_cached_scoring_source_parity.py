#!/usr/bin/env python3
"""Read-only Route B B2 original scalar-label parity on the frozen 1024 DEV requests.

This is CACHE-TO-CACHE parity, not a reconstructed scorer parity or causal null
result. No private identifiers are included in exported logs or reports.
"""
from __future__ import annotations
import argparse,hashlib,json,time
from pathlib import Path
import numpy as np
import pandas as pd

B1_EXPECTED = "37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
MEDIUM_EXPECTED = "6ad1a0753e181ac638636c278d226832b08d90d7d4867019910c61b96d7507da"
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<23),b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cache-root',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():
        raise FileExistsError('B2 read-only report cannot overwrite another run')
    started=time.monotonic()
    cache=a.cache_root
    sample=cache/'klm3_n9_route_b_b2_pretarget_sample_v1'
    b1=cache/'klm3_b1_full_dev_candidate_labels_seed20261012_v1'
    b2=cache/'klm3_b2_full_dev_memory_source_ablation_seed20261013_v1'
    sm=json.loads((sample/'summary.json').read_text())
    m1=json.loads((b1/'summary.json').read_text())
    m2=json.loads((b2/'summary.json').read_text())
    sample_file=sample/'B2_MEDIUM_EVENTS_PRIVATE.npz'
    f1=b1/'dev_pair_candidate_labels.csv'
    f2=b2/'dev_memory_source_ablation_pairs.csv'
    if not (sm['schema']=='kbs-route-b-b2-medium-preoutcome-sample-v1'
            and sm['n_events']==1024 and sm['old_128_late_DEV_pilot_excluded'] is True
            and sm['no_target_or_outcome_columns_loaded'] is True
            and digest(sample_file)==sm['sample_private_SHA256']==MEDIUM_EXPECTED):
        raise RuntimeError('pretarget sample hash/provenance invalid')
    if not (m1.get('test_accessed') is False and m2.get('new_TEST_opened') is False
            and m2.get('full_memory_nDCG_mismatches')=={'F':0,'S':0}
            and digest(f1)==m1.get('private_event_source_csv_sha256')==B1_EXPECTED
            and digest(f2)==m2.get('private_event_source_csv_sha256')):
        raise RuntimeError('B1/B2 original cache hash parity invalid')
    data=np.load(sample_file,allow_pickle=False)
    ids=np.asarray(data['source_event_ids'],dtype=np.int64)
    if len(ids)!=1024 or len(np.unique(ids))!=1024:
        raise RuntimeError('nonunique B2 request IDs')
    left=pd.read_csv(f1,usecols=[
        'event_id','user_id','split','memory_ndcg10','sampled_memory_ndcg10'])
    right=pd.read_csv(f2,usecols=[
        'event_id','user_id','split','memory_ndcg10','sampled_memory_ndcg10',
        'b2_long_only_F_ndcg10','b2_long_only_S_ndcg10'])
    if not (len(left)==50049 and len(right)==50049
            and left.event_id.is_unique and right.event_id.is_unique):
        raise RuntimeError('cohort cardinality invalid')
    sel=pd.DataFrame({'event_id':ids})
    merged=(sel.merge(left,on='event_id',validate='one_to_one')
            .merge(right,on='event_id',validate='one_to_one',suffixes=('_B1','_B2')))
    if len(merged)!=1024 or not(merged.split_B1.eq('DEV').all()
                                and merged.split_B2.eq('DEV').all()):
        raise RuntimeError('DEV target eligibility mismatch')
    if not(merged.user_id_B1.astype(str)==merged.user_id_B2.astype(str)).all():
        raise RuntimeError('B1/B2 user mismatch')
    distinct=merged.user_id_B1.nunique()
    if distinct!=sm['n_users']:
        raise RuntimeError('medium cohort unique user mismatch')
    for v in ('memory_ndcg10','sampled_memory_ndcg10'):
        a1=merged[v+'_B1'].to_numpy(float)
        a2=merged[v+'_B2'].to_numpy(float)
        if not (np.isfinite(a1).all() and np.isfinite(a2).all()
                and np.allclose(a1,a2,rtol=0,atol=1e-12)):
            raise RuntimeError('cached original fixed Memory result inconsistent')
    ff=merged.memory_ndcg10_B2.to_numpy(float)
    ss=merged.sampled_memory_ndcg10_B2.to_numpy(float)
    fl=merged.b2_long_only_F_ndcg10.to_numpy(float)
    sl=merged.b2_long_only_S_ndcg10.to_numpy(float)
    if not all(np.isfinite(x).all() for x in (ff,ss,fl,sl)):
        raise RuntimeError('invalid rank source cache')
    z={
        'schema':'kbs-route-b-b2-cached-label-parity-v1',
        'evidence':'PREEXISTING_POST_G5_M3_DEV_CACHE_ONLY',
        'sample_events':1024,'sample_users':int(distinct),
        'private_sample_hash':MEDIUM_EXPECTED,
        'private_B1_hash':B1_EXPECTED,
        'private_B2_hash':m2['private_event_source_csv_sha256'],
        'B1_B2_full_memory_original_F_S_scalar_parity':True,
        'new_base_or_memory_models_run':False,
        'original_memory_rank_rescored':False,
        'medium_historical_edges_rewired':False,
        'mean_original_full_F':float(ff.mean()),'mean_original_full_S':float(ss.mean()),
        'mean_original_long_F':float(fl.mean()),'mean_original_long_S':float(sl.mean()),
        'mean_full_minus_long_F':float((ff-fl).mean()),
        'mean_full_minus_long_S':float((ss-sl).mean()),
        'descriptive_source_candidate_interaction':float(((ff-fl)-(ss-sl)).mean()),
        'top10_positive_full_F':int(np.count_nonzero(ff)),
        'top10_positive_full_S':int(np.count_nonzero(ss)),
        'no_G5_TEST_opened':True,
        'interpretation':'Cached scalar labels agree across source files, NOT independent frozen scoring-path parity or a new causal experiment',
        'wall_seconds':round(time.monotonic()-started,2)}
    a.out.mkdir(parents=True,mode=0o700)
    (a.out/'summary.json').write_text(json.dumps(z,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'B2_CACHED_PARITY':'PASS','safe_summary':z},sort_keys=True),flush=True)

if __name__=='__main__':
    main()
