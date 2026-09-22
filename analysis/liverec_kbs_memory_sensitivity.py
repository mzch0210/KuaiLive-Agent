from __future__ import annotations

import argparse, json, math, time
from pathlib import Path
import numpy as np
import pandas as pd

EPS=1e-12
EXPECTED_N=46878
SEED=20260922
ORIG=(0.45,0.45,0.10,10,3.0) # short,long,pop,K,decay


def ndcg(rank): return 0.0 if rank>=10 else 1.0/math.log2(rank+2.0)
def h10(rank): return float(rank<10)

def rank_score(cand, score, target):
    idx=np.flatnonzero(cand==target)
    if idx.size!=1: raise RuntimeError(f'target multiplicity={idx.size}')
    s=float(score[int(idx[0])])
    return int(np.count_nonzero(score>s+EPS)+np.count_nonzero((np.abs(score-s)<=EPS)&(cand<target)))

def bootstrap(x, seed, n_boot=3000, chunk=64):
    x=np.asarray(x,float); n=len(x); rng=np.random.default_rng(seed); out=np.empty(n_boot)
    p=0
    while p<n_boot:
        b=min(chunk,n_boot-p); idx=rng.integers(0,n,size=(b,n),dtype=np.int32)
        out[p:p+b]=x[idx].mean(1); p+=b
    return {'mean':float(x.mean()),'ci95_low':float(np.quantile(out,.025)),'ci95_high':float(np.quantile(out,.975)),'n':n}

def active_matrix(starts,stops,sids,target_steps,max_sid):
    t=len(target_steps); diff=np.zeros((max_sid+1,t+1),np.int32)
    left=np.searchsorted(target_steps,starts,'left'); right=np.searchsorted(target_steps,stops,'left')
    m=(left<right)&(left<t); np.add.at(diff,(sids[m],left[m]),1)
    mr=m&(right<t); np.add.at(diff,(sids[mr],right[mr]),-1)
    np.cumsum(diff[:,:t],axis=1,out=diff[:,:t]); return diff[:,:t]

def configs():
    out=[]
    for wl in (0.30,0.45,0.60):
        rem=1-wl; out.append((f'long_weight_{wl:.2f}',rem*0.45/0.55,wl,rem*0.10/0.55,10,3.0))
    for k in (5,10,20): out.append((f'short_k_{k}',.45,.45,.10,k,3.0))
    for d in (2.0,3.0,5.0): out.append((f'decay_{d:g}',.45,.45,.10,10,d))
    # de-duplicate original configuration while retaining one canonical label
    seen=set(); z=[]
    for row in out:
        key=tuple(round(x,12) if isinstance(x,float) else x for x in row[1:])
        if key not in seen: seen.add(key); z.append(row)
    return z

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dev-oof',type=Path,required=True); ap.add_argument('--twitch-csv',type=Path,required=True); ap.add_argument('--out-dir',type=Path,required=True); ap.add_argument('--n-boot',type=int,default=3000); a=ap.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True); t0=time.perf_counter()
    dev=pd.read_csv(a.dev_oof)
    req={'user_id','target_step','target_streamer','candidate_count','relationship_horizon','base_ndcg10','memory_rank0','memory_ndcg10','history_len'}
    miss=req-set(dev.columns)
    if miss or len(dev)!=EXPECTED_N or dev.user_id.duplicated().any(): raise RuntimeError(f'bad frozen DEV: missing={miss}, n={len(dev)}')
    raw=pd.read_csv(a.twitch_csv,header=None,names=['user','stream','streamer','start','stop']); raw['row']=np.arange(len(raw)); raw['uid']=pd.factorize(raw.user)[0]+1; raw['sid']=pd.factorize(raw.streamer)[0]+1
    starts=raw.start.to_numpy(np.int64); stops=raw.stop.to_numpy(np.int64); users=raw.uid.to_numpy(np.int64); sids=raw.sid.to_numpy(np.int64); rows=raw.row.to_numpy(np.int64); max_sid=int(sids.max()); max_step=int(max(starts.max(),stops.max())); pivot=max_step-500
    cnt=np.bincount(sids[stops<pivot],minlength=max_sid+1).astype(float); lg=np.log1p(cnt); pop=np.zeros_like(lg); m=cnt>0
    if m.any():
        lo,hi=lg[m].min(),lg[m].max(); pop[m]=(lg[m]-lo)/max(hi-lo,EPS)
    steps=np.sort(dev.target_step.unique().astype(np.int64)); act=active_matrix(starts,stops,sids,steps,max_sid); smap={int(s):i for i,s in enumerate(steps)}
    order=np.lexsort((rows,starts,users)); su=users[order]; ss=starts[order]; si=sids[order]; uu,first,counts=np.unique(su,return_index=True,return_counts=True); bounds={int(u):(int(f),int(f+c)) for u,f,c in zip(uu,first,counts)}
    cfg=configs(); ranks={name:np.empty(len(dev),np.int64) for name,*_ in cfg}; cand_bad=hist_bad=0
    long=np.zeros(max_sid+1,float); short=np.zeros(max_sid+1,float)
    for i,r in enumerate(dev.itertuples(index=False)):
        cand=np.flatnonzero(act[:,smap[int(r.target_step)]]>0).astype(np.int64)
        cand_bad += len(cand)!=int(r.candidate_count)
        lo,hi=bounds[int(r.user_id)]; n=int(np.searchsorted(ss[lo:hi],int(r.target_step),'left')); hist=si[lo:lo+n]; hist_bad += n!=int(r.history_len)
        if n:
            lids,lcnt=np.unique(hist,return_counts=True); long[lids]=lcnt/lcnt.max()
        else: lids=np.empty(0,np.int64)
        for name,ws,wl,wp,k,dec in cfg:
            touched=list(lids); sm={}
            for dist,sid in enumerate(reversed(hist[-k:].tolist())):
                sm[int(sid)]=max(sm.get(int(sid),0.0),math.exp(-dist/dec))
            if sm:
                ids=np.fromiter(sm.keys(),dtype=np.int64); vals=np.fromiter(sm.values(),dtype=float); short[ids]=vals; touched.extend(ids.tolist())
            score=wp*pop[cand]+wl*long[cand]+ws*short[cand]; ranks[name][i]=rank_score(cand,score,int(r.target_streamer))
            if sm: short[ids]=0
        if lids.size: long[lids]=0
    if cand_bad or hist_bad: raise RuntimeError(f'reconstruction mismatch candidate={cand_bad} history={hist_bad}')
    base=dev.base_ndcg10.to_numpy(float); rows_out=[]; original_replay=None
    for j,(name,ws,wl,wp,k,dec) in enumerate(cfg):
        nd=np.array([ndcg(x) for x in ranks[name]],float); hh=(ranks[name]<10).astype(float)
        if abs(ws-.45)<1e-12 and abs(wl-.45)<1e-12 and abs(wp-.10)<1e-12 and k==10 and abs(dec-3)<1e-12:
            original_replay={'rank_mismatches':int(np.sum(ranks[name]!=dev.memory_rank0.to_numpy(int))),'ndcg_max_abs_diff':float(np.max(np.abs(nd-dev.memory_ndcg10.to_numpy(float))))}
        for horizon,g in dev.groupby('relationship_horizon',sort=False).groups.items():
            idx=np.asarray(list(g),int); ci=bootstrap(nd[idx]-base[idx],SEED+100*j+len(rows_out),a.n_boot)
            rows_out.append({'config':name,'short_weight':ws,'long_weight':wl,'pop_weight':wp,'short_k':k,'decay':dec,'horizon':str(horizon),'ndcg10':float(nd[idx].mean()),'h10':float(hh[idx].mean()),'delta_vs_base':ci['mean'],'ci95_low':ci['ci95_low'],'ci95_high':ci['ci95_high'],'n':len(idx)})
        ci=bootstrap(nd-base,SEED+9000+j,a.n_boot); rows_out.append({'config':name,'short_weight':ws,'long_weight':wl,'pop_weight':wp,'short_k':k,'decay':dec,'horizon':'ALL','ndcg10':float(nd.mean()),'h10':float(hh.mean()),'delta_vs_base':ci['mean'],'ci95_low':ci['ci95_low'],'ci95_high':ci['ci95_high'],'n':len(dev)})
    if not original_replay or original_replay['rank_mismatches'] or original_replay['ndcg_max_abs_diff']>1e-12: raise RuntimeError(f'original replay failed: {original_replay}')
    tab=pd.DataFrame(rows_out); tab.to_csv(a.out_dir/'memory_sensitivity.csv',index=False)
    sign=tab[tab.horizon.isin(['recent_visible','long_horizon_only','unseen'])].assign(sign=lambda x:np.sign(x.delta_vs_base)).pivot(index='config',columns='horizon',values='sign')
    report={'experiment':'KBS post-P1.3 DEV-only Memory sensitivity','test_ranking_inspected':False,'n_dev':len(dev),'original_replay_guard':original_replay,'candidate_mismatches':cand_bad,'history_mismatches':hist_bad,'configs':[x[0] for x in cfg],'all_configs_preserve_expected_horizon_signs':bool(((sign.get('long_horizon_only')>0)&(sign.get('recent_visible')<0)&(sign.get('unseen')<0)).all()),'runtime_seconds':time.perf_counter()-t0}
    (a.out_dir/'memory_sensitivity_report.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
if __name__=='__main__': main()
