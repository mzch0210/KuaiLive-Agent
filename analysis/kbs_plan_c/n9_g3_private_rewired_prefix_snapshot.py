#!/usr/bin/env python3
"""G3 pilot: cross-active temporal edge swap eligibility; no Memory score claims."""
from __future__ import annotations
import argparse,json,time,hashlib
from pathlib import Path
from collections import defaultdict
import numpy as np,pandas as pd,pyarrow.parquet as pq

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def ts(x):
 s=pd.Series(x)
 if pd.api.types.is_numeric_dtype(s):
  v=float(s.dropna().abs().median())
  unit=('ns' if v>1e17 else 'us' if v>1e14 else 'ms' if v>1e11 else 's')
  return pd.to_datetime(s,utc=True,unit=unit,errors='coerce')
 return pd.to_datetime(s,utc=True,errors='coerce')

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
 p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists():raise FileExistsError("Pilot output already exists")
 t=time.monotonic();g=a.root/'klm3_plan_c_g1_v1';v=a.root/'klm3_g2_dev_checkpoint_screen_v1'
 b=a.root/'klm3_b1_full_dev_candidate_labels_seed20261012_v1'
 mb=json.loads((b/'summary.json').read_text())
 if not(mb['scope']=='DEV_ONLY_POST_G5_EXPLORATORY'
   and mb['test_accessed'] is False
   and mb['private_event_source_csv_sha256']=='37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea'
   and sha(b/'dev_pair_candidate_labels.csv')==mb['private_event_source_csv_sha256']):
  raise RuntimeError("Frozen B1 source gate")
 source=pq.read_table(g/'dev_cohort.parquet',columns=['source_event_id','user_id','observed_at']).to_pandas()
 source['ts']=ts(source.observed_at)
 if source.ts.isna().any() or len(source)!=50049:raise RuntimeError("DEV clock invalid")
 seq=np.argsort(source.ts.to_numpy(),kind='stable')
 choose=seq[int(len(seq)*.75):]
 choose=choose[np.unique(np.linspace(0,len(choose)-1,128,dtype=int))]
 users=set(source.user_id.iloc[choose].tolist())
 cutoff=source.ts.iloc[choose].min()
 arrays=[]
 for batch in pq.ParquetFile(g/'causal_stream_sealed.parquet').iter_batches(
     batch_size=262144,columns=['source_event_id','user_id','author_id','observed_at','split']):
  df=batch.to_pandas()
  part=df.loc[df.user_id.isin(users)&df.split.ne('TEST'),['source_event_id','user_id','author_id','observed_at']].copy()
  if part.empty:continue
  part['ts']=ts(part.observed_at)
  part=part.loc[part.ts<cutoff,['source_event_id','user_id','author_id','ts']]
  if len(part):arrays.append(part)
 df=pd.concat(arrays,ignore_index=True)
 if len(df)<10000:raise RuntimeError("History pilot too small")
 active=set(df.author_id.unique().tolist())
 sets=[]
 for batch in pq.ParquetFile(g/'available_room_intervals.parquet').iter_batches(
      batch_size=262144,columns=['author_id','open_ts','close_ts']):
  arr=batch.to_pandas()
  arr=arr[arr.author_id.isin(active)]
  if len(arr):sets.append(arr)
 intervals=pd.concat(sets,ignore_index=True)
 intervals['start']=ts(intervals.open_ts)
 intervals['finish']=ts(intervals.close_ts)
 if intervals.start.isna().any() or intervals.finish.isna().any():
  raise RuntimeError("Availability timestamps unparseable")
 intervals=intervals[intervals.finish>=intervals.start]
 if len(intervals)==0:raise RuntimeError("No matched roster intervals")
 by_author={}
 for author,sub in intervals.groupby('author_id'):
  # Sort by starts and allow overlapping active intervals.
  starts=sub.start.dt.as_unit('ns').astype('int64').to_numpy()
  closes=sub.finish.dt.as_unit('ns').astype('int64').to_numpy()
  order=np.argsort(starts)
  ss=starts[order];max_end=np.maximum.accumulate(closes[order])
  by_author[author]=(ss,max_end)
 stamp=df.ts.dt.as_unit('ns').astype('int64').to_numpy()
 def available(author,at):
  u=by_author.get(author)
  if u is None:return False
  starts,ends=u
  k=int(np.searchsorted(starts,at,side='right'))-1
  return k>=0 and ends[k]>at
 hour=(stamp//(3600*10**9)).astype(np.int64)
 slots=defaultdict(list)
 for i,key in enumerate(hour):slots[int(key)].append(i)
 bins=[np.asarray(v,dtype=np.int64) for v in slots.values() if len(v)>=2]
 print(json.dumps({'timestamp_debug':True,
   'DEV_observed_dtype':str(source.observed_at.dtype),
   'history_timestamp_dtype':str(df.ts.dtype),
   'start_time_coarse':str(df.ts.min().date()),
   'end_time_coarse':str(df.ts.max().date()),
   'closed_prefix_history_rows':len(df),'unique_hour_slots':len(slots),
   'num_multirow_hour_bins':len(bins),
   'timestamp_null_count':int(df.ts.isna().sum())},sort_keys=True),flush=True)
 if len(bins)<2:raise RuntimeError("Insufficient time bins; see timestamp debug aggregate")
 weights=np.asarray([len(x) for x in bins],dtype=float);weights/=weights.sum()
 original=df.author_id.to_numpy(copy=True);after=original.copy()
 uid=df.user_id.to_numpy()
 rng=np.random.default_rng(20261013)
 used=np.zeros(len(df),dtype=bool)
 attempts=0;cross_active=0;proposed=0;swaps=0;original_valid=0
 # Both event authors must be active at both original event times.
 for _ in range(125000):
  pick=int(rng.choice(len(bins),p=weights))
  ids=bins[pick]
  ia,ib=rng.choice(ids,size=2,replace=False)
  ia=int(ia);ib=int(ib);attempts+=1
  if used[ia] or used[ib] or uid[ia]==uid[ib] or original[ia]==original[ib]:continue
  proposed+=1
  oa,ob=original[ia],original[ib];ta,tb=int(stamp[ia]),int(stamp[ib])
  if available(oa,ta) and available(ob,tb):original_valid+=1
  if not (available(ob,ta) and available(oa,tb)):continue
  cross_active+=1
  after[ia],after[ib]=ob,oa
  used[ia]=used[ib]=True
  swaps+=1
 # Invariants hold for every occupied 1-hour bin exactly.
 from collections import Counter
 before=Counter(zip(hour.tolist(),original.tolist()))
 changed=Counter(zip(hour.tolist(),after.tolist()))
 assert before==changed,"Per-hour author margins changed"
 assert np.all((after!=original)==used),"Swap identities not exact"
 assert np.array_equal(hour,(stamp//(3600*10**9)).astype(np.int64)),"Time slots changed"
 changed_users=len(set(uid[used].tolist()))
 result={'schema':'n9-g3-private-rewired-prefix-snapshot-v2','scope':'DEV_ONLY',
   'pilot_events':128,'pilot_users':len(users),'history_edges':len(df),
   'history_authors':len(active),'roster_intervals_for_history_authors':len(intervals),
   'hour_bins':len(bins),'proposed_cross_user_distinct_author_pairs':proposed,
   'original_pairs_both_active':original_valid,
   'counterfactual_cross_active_valid_pairs':cross_active,'attempts':attempts,
   'actual_disjoint_swaps':swaps,'changed_history_endpoints':int(used.sum()),
   'changed_fraction':float(used.mean()),'users_with_rewired_history':changed_users,
   'time_bin_author_degree_exact':True,
   'per_user_history_event_count_and_timestamp_exact':True,
   'both_swapped_authors_active_at_both_event_times':True,
   'all_swaps_before_earliest_target':True,
   'baseline_rank_parity':'NOT_EVALUATED',
   'memory_control_nonfloor':'NOT_EVALUATED',
   'full_E3b_evidence':False,'G5_TEST_read':False,'private_ids_exported':False,
   'wall_seconds':round(time.monotonic()-t,2)}
 a.out.mkdir(parents=True,mode=0o700)
 np.savez_compressed(a.out/'rewired_event_authors_PRIVATE.npz',source_event_ids=df.source_event_id.to_numpy()[used],rewired_author_ids=after[used])
 result['private_snapshot_filename']='rewired_event_authors_PRIVATE.npz'
 result['private_snapshot_rows']=int(used.sum())
 (a.out/'summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()
