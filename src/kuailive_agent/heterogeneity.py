from __future__ import annotations

import argparse, math
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd

from .evaluate import split_events, ndcg


def norm_entropy(xs):
    c=Counter(xs); n=sum(c.values())
    if n<=1 or len(c)<=1: return 0.0
    p=np.array(list(c.values()),dtype=float)/n
    return float(-(p*np.log(p)).sum()/math.log(len(c)))

def js_divergence(a,b):
    ca,cb=Counter(a),Counter(b); keys=sorted(set(ca)|set(cb))
    if not keys: return 0.0
    pa=np.array([ca[k] for k in keys],float); pb=np.array([cb[k] for k in keys],float)
    pa/=max(pa.sum(),1); pb/=max(pb.sum(),1); m=.5*(pa+pb)
    def kl(p,q):
        z=p>0
        return float((p[z]*np.log2(p[z]/q[z])).sum())
    return .5*kl(pa,m)+.5*kl(pb,m)

def circular_regularity(ts):
    if not len(ts): return 0.0
    h=pd.to_datetime(pd.Series(ts),unit='ms').dt.hour.to_numpy(float)
    ang=2*np.pi*h/24.0
    return float(np.sqrt(np.mean(np.cos(ang))**2+np.mean(np.sin(ang))**2))

def user_features(train):
    rows=[]
    for uid,g in train.sort_values(['user_id','timestamp','live_id']).groupby('user_id'):
        s=g.streamer_id.astype(int).tolist(); t=g.timestamp.astype('int64').tolist(); n=len(s)
        recent_n=min(10,max(2,n//3)) if n>=3 else max(1,n//2)
        old=s[:-recent_n] if n>recent_n else s[:max(1,n//2)]
        recent=s[-recent_n:] if recent_n else s
        uniq=len(set(s))
        rows.append({
            'user_id':int(uid),'history_len':n,'unique_streamers':uniq,
            'repeat_rate':1-uniq/max(n,1),'preference_entropy':norm_entropy(s),
            'preference_drift':js_divergence(old,recent) if old and recent else 0.0,
            'time_regularity':circular_regularity(t),
        })
    f=pd.DataFrame(rows)
    # preregistered composite: complexity rises with entropy, drift and available history.
    for c in ['preference_entropy','preference_drift']:
        f[c+'_pct']=f[c].rank(pct=True,method='average')
    f['history_pct']=np.log1p(f.history_len).rank(pct=True,method='average')
    f['state_complexity']=.4*f.preference_entropy_pct+.4*f.preference_drift_pct+.2*f.history_pct
    return f

def load_per_user(result_dir):
    frames=[]
    for p in sorted(Path(result_dir).glob('per_user_seed*.csv.gz')):
        x=pd.read_csv(p); x['seed']=p.stem.replace('.csv','').split('seed')[-1]; frames.append(x)
    if not frames: raise FileNotFoundError('No per_user_seed*.csv.gz')
    r=pd.concat(frames,ignore_index=True)
    r['score10']=r['rank'].map(lambda x:ndcg(int(x),10))
    # average over negative-sampling seeds before subgroup analysis
    return r.groupby(['user_id','model'],as_index=False).agg(score10=('score10','mean'),rank=('rank','mean'),long_view=('long_view','max'))

def bootstrap_mean(x,seed=20260918,n_boot=2000):
    x=np.asarray(x,float); x=x[np.isfinite(x)]
    if not len(x): return np.nan,np.nan,np.nan
    rng=np.random.default_rng(seed); n=len(x)
    b=np.array([x[rng.integers(0,n,n)].mean() for _ in range(n_boot)])
    return float(x.mean()),float(np.quantile(b,.025)),float(np.quantile(b,.975))

def make_deltas(r):
    p=r.pivot(index='user_id',columns='model',values='score10')
    pairs={
      'planning_vs_fusion':('MemoryPlanner','MemoryFusion'),
      'time_component':('MemoryPlanner','Planner-NoTime'),
      'long_memory_component':('MemoryPlanner','Planner-NoLong'),
      'short_memory_component':('MemoryPlanner','Planner-NoShort'),
      'planning_vs_long':('MemoryPlanner','LongMemory'),
    }
    out=pd.DataFrame(index=p.index)
    for name,(a,b) in pairs.items(): out[name]=p[a]-p[b]
    return out.reset_index()

def quartile_table(df,feature,delta):
    tmp=df[['user_id',feature,delta]].dropna().copy()
    try: tmp['quartile']=pd.qcut(tmp[feature],4,labels=['Q1','Q2','Q3','Q4'],duplicates='drop')
    except ValueError: return pd.DataFrame()
    rows=[]
    for q,g in tmp.groupby('quartile',observed=True):
        m,lo,hi=bootstrap_mean(g[delta].to_numpy(),seed=20260918+len(rows))
        rows.append({'feature':feature,'delta':delta,'quartile':str(q),'n':len(g),'feature_mean':g[feature].mean(),'delta_ndcg10':m,'ci95_low':lo,'ci95_high':hi})
    return pd.DataFrame(rows)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prepared-dir',type=Path,required=True); ap.add_argument('--result-dir',type=Path,required=True); ap.add_argument('--out-dir',type=Path,required=True)
    a=ap.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True)
    events=pd.read_pickle(a.prepared_dir/'events.pkl'); train,_,_=split_events(events,3)
    f=user_features(train); r=load_per_user(a.result_dir); d=make_deltas(r); z=f.merge(d,on='user_id',how='inner')
    z.to_csv(a.out_dir/'user_features_and_deltas.csv.gz',index=False,compression='gzip')
    tests=[
      ('preference_entropy','planning_vs_fusion','H1: planning benefit increases with preference entropy'),
      ('preference_drift','planning_vs_fusion','H2: planning benefit increases with preference drift'),
      ('state_complexity','planning_vs_fusion','H3: planning benefit increases with state complexity'),
      ('time_regularity','time_component','H4: explicit time component benefits temporally regular users'),
      ('repeat_rate','long_memory_component','H5a: long-memory contribution increases with repeat rate'),
      ('history_len','long_memory_component','H5b: long-memory contribution increases with history length'),
      ('preference_drift','short_memory_component','H6: short-memory contribution increases with preference drift'),
    ]
    tabs=[]; trend=[]
    for feat,delta,hyp in tests:
        t=quartile_table(z,feat,delta)
        if len(t):
            t['hypothesis']=hyp; tabs.append(t)
            q1=t.iloc[0].delta_ndcg10; q4=t.iloc[-1].delta_ndcg10
            trend.append({'hypothesis':hyp,'feature':feat,'delta':delta,'Q1':q1,'Q4':q4,'Q4_minus_Q1':q4-q1,'direction_supported':bool(q4>q1)})
    alltab=pd.concat(tabs,ignore_index=True); alltab.to_csv(a.out_dir/'heterogeneity_quartiles.csv',index=False)
    pd.DataFrame(trend).to_csv(a.out_dir/'hypothesis_trends.csv',index=False)
    print(pd.DataFrame(trend).to_string(index=False)); print('\nQuartiles:\n',alltab.to_string(index=False))

if __name__=='__main__': main()
