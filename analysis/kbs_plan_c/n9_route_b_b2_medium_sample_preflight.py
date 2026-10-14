#!/usr/bin/env python3
"""B2.0: deterministic PRE-OUTCOME DEV-only medium cohort selection. No target/outcome reads."""
from __future__ import annotations
import argparse,hashlib,json,time
from pathlib import Path
import numpy as np,pandas as pd,pyarrow.parquet as pq
N=50049;USERS=12628;SEED=20261014
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--root',type=Path,required=True)
 p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists():raise FileExistsError('Do not overwrite sealed sample')
 t=time.monotonic()
 root=a.root;g=root/'klm3_plan_c_g1_v1'
 b=root/'klm3_b1_full_dev_candidate_labels_seed20261012_v1'
 c=root/'klm3_g2_dev_checkpoint_screen_v1'
 met=json.loads((b/'summary.json').read_text())
 source=b/'dev_pair_candidate_labels.csv'
 if not(met.get('scope')=='DEV_ONLY_POST_G5_EXPLORATORY' and met.get('test_accessed') is False
  and sha(source)==met.get('private_event_source_csv_sha256')
  and met['private_event_source_csv_sha256']=='37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea'):
  raise RuntimeError('B1 locked DEV source check failed')
 idx=np.load(c/'dev_source_event_ids.npy',mmap_mode='r')
 clocks=pq.read_table(g/'dev_cohort.parquet',
    columns=['source_event_id','user_id','observed_at']).to_pandas()
 if len(idx)!=N or len(clocks)!=N or not np.array_equal(idx,clocks.source_event_id.to_numpy()):
  raise RuntimeError('B2 DEV chronological event source mismatch')
 dat=pd.read_csv(source,usecols=['event_id','user_id','split','x_hist_event_count'])
 if not(len(dat)==N and dat.event_id.is_unique and dat.user_id.nunique()==USERS
  and dat.split.eq('DEV').all()):raise RuntimeError('B2 B1 source identity invalid')
 frame=clocks.merge(dat,left_on='source_event_id',right_on='event_id',
     validate='one_to_one',suffixes=('_clock','_B1'))
 if len(frame)!=N or not np.array_equal(frame.source_event_id.to_numpy(),clocks.source_event_id.to_numpy()) or not(frame.user_id_clock.astype(str)==frame.user_id_B1.astype(str)).all():
  raise RuntimeError('B2 user ID mismatch')
 frame['ts']=pd.to_datetime(frame.observed_at,utc=True)
 if frame.ts.isna().any() or frame.x_hist_event_count.isna().any():
  raise RuntimeError('invalid pretarget clock/history')
 chronological=np.argsort(frame.ts.to_numpy(),kind='stable')
 old=chronological[int(N*.75):]
 old=old[np.unique(np.linspace(0,len(old)-1,128,dtype=int))]
 old_idx=set(old.tolist())
 frame['time_q']=np.zeros(N,dtype=np.int8)
 for q,indices in enumerate(np.array_split(chronological,4)):
  frame.loc[indices,'time_q']=q
 # Historical activity binning fixed before inspecting any outcomes.
 # Reuse empirical distribution within temporal quartiles, ties via stable ranks.
 frame['history_q']=np.zeros(N,dtype=np.int8)
 for q in range(4):
  pick=np.where(frame.time_q.to_numpy()==q)[0]
  sub=frame.x_hist_event_count.to_numpy()[pick]
  order=np.argsort(sub,kind='stable')
  for h,ix in enumerate(np.array_split(pick[order],4)):
   frame.loc[ix,'history_q']=h
 rnd=np.random.default_rng(SEED)
 chosen=[];chosen_users=set();counts=[]
 for q in range(4):
  for h in range(4):
   indices=np.flatnonzero((frame.time_q.to_numpy()==q)&(frame.history_q.to_numpy()==h))
   indices=np.array([i for i in indices if i not in old_idx],dtype=int)
   rnd.shuffle(indices)
   unique=[int(i) for i in indices if str(frame.user_id_clock.iloc[int(i)]) not in chosen_users]
   take=unique[:64]
   if len(take)<64:
    for i in indices:
     if int(i) not in take:take.append(int(i))
     if len(take)==64:break
   if len(take)!=64:raise RuntimeError('B2 insufficient pretarget stratum capacity')
   chosen+=take
   chosen_users.update(map(str,frame.user_id_clock.iloc[take]))
   counts.append({'time_quartile':q+1,'history_quartile':h+1,'selected':len(take),
     'eligible_preoutcome_DEV_events':int(len(indices)),
     'selected_unique_users':int(frame.user_id_clock.iloc[take].nunique())})
 if len(chosen)!=1024 or len(set(chosen))!=1024 or set(chosen)&old_idx:
  raise RuntimeError('B2 stratification/old pilot exclusion violated')
 saved=frame.iloc[chosen].sort_values('ts')
 event_ids=saved.source_event_id.to_numpy()
 users=saved.user_id_clock.to_numpy()
 a.out.mkdir(parents=True,mode=0o700)
 np.savez_compressed(a.out/'B2_MEDIUM_EVENTS_PRIVATE.npz',
    source_event_ids=event_ids,user_ids=users,observed_at_ns=saved.ts.astype('int64').to_numpy(),
    preoutcome_history_event_count=saved.x_hist_event_count.to_numpy())
 h=sha(a.out/'B2_MEDIUM_EVENTS_PRIVATE.npz')
 summary={'schema':'kbs-route-b-b2-medium-preoutcome-sample-v1',
    'selection':'1024 DEV event IDs with exactly 64 events in each of 16 chronological/history quartile strata',
    'n_events':1024,'n_users':int(len(np.unique(users))),
    'seed':SEED,'old_128_late_DEV_pilot_excluded':True,
    'by_strata':counts,'sample_private_SHA256':h,
    'source_B1_SHA256':met['private_event_source_csv_sha256'],
    'source_test_accessed':False,'no_target_or_outcome_columns_loaded':True,
    'relation_edges_rewired':False,'Memory_scoring_performed':False,
    'study_status':'METADATA_SOURCE_PREP_PASS_RIGHTS_AND_CAUSAL_SCORING_GATES_PENDING',
    'wall_seconds':round(time.monotonic()-t,2)}
 (a.out/'summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'B2_PREFLIGHT':'PASS','n_events':1024,'n_users':summary['n_users'],
  'source_B1_SHA256_PASS':True,'sample_manifest_SHA256':h,
  'strata':counts,'excluded_128_pilot':True,'outcome_columns_read':False,
  'no_G5_TEST':True,'no_scoring_or_rewiring':True},sort_keys=True),flush=True)
if __name__=='__main__':main()
