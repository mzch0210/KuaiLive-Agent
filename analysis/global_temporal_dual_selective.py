from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import GroupKFold, cross_val_predict

from room_level_selective_agent import CONF_FEATURES, USER_FEATURES, EPS, SEED, choose_threshold, hgb, ndcg10, parse_list


def zscore(x):
    x=np.asarray(x,float); sd=float(x.std())
    return np.zeros_like(x) if sd<=EPS else (x-float(x.mean()))/sd

def rank_ge(scores):
    s=np.asarray(scores,float); return int(np.sum(s>=float(s[0])-1e-12))

def conf_tuple(scores):
    scores=np.asarray(scores,float); ss=np.sort(scores)[::-1]
    mean=float(scores.mean()); std=float(scores.std()); rng=float(scores.max()-scores.min())
    ex=np.exp(np.clip(scores-scores.max(),-60,0)); p=ex/ex.sum(); ps=np.sort(p)[::-1]
    ent=float(-(p*np.log(np.maximum(p,EPS))).sum()/math.log(len(p)))
    return (std,rng,float(ss[0]-ss[1]),float(ss[0]-ss[4]),float(ss[9]-ss[10]),float((ss[0]-mean)/max(std,EPS)),ent,float(ps[:10].sum()))

def _scoremap(items,scores):
    d={}
    for i,s in zip(items,scores): d.setdefault(int(i),[]).append(float(s))
    return {k:float(np.mean(v)) for k,v in d.items()}

def load_vectors(phase_room, phase_streamer, room_pred_path, streamer_pred_path):
    rp=pd.read_csv(room_pred_path,sep='\t'); sp=pd.read_csv(streamer_pred_path,sep='\t')
    if not (len(rp)==len(sp)==len(phase_room)==len(phase_streamer)): raise ValueError('prediction length mismatch')
    out=[]
    for k,((_,rr),(_,sr)) in enumerate(zip(phase_room.iterrows(),phase_streamer.iterrows())):
        pr=rp.iloc[k]; ps=sp.iloc[k]
        if int(pr.user_id)!=int(rr.user_id) or int(ps.user_id)!=int(sr.user_id): raise ValueError(f'prediction row order mismatch at {k}')
        rc=np.concatenate(([int(rr.item_id)],parse_list(rr.neg_items,int)))
        sc=np.concatenate(([int(sr.item_id)],parse_list(sr.neg_items,int)))
        rm=_scoremap(parse_list(pr.rec_items,int),parse_list(pr.rec_predictions,float))
        sm=_scoremap(parse_list(ps.rec_items,int),parse_list(ps.rec_predictions,float))
        try:
            rz=np.asarray([rm[int(i)] for i in rc],float); sz=np.asarray([sm[int(i)] for i in sc],float)
        except KeyError as e: raise KeyError(f'missing candidate score row={k} item={e}')
        out.append((int(rr.user_id),zscore(rz),zscore(sz)))
    return out

def eval_vectors(vectors, alpha, with_conf=True):
    rows=[]
    for row_id,(uid,rz,sz) in enumerate(vectors):
        dual=alpha*rz+(1-alpha)*sz
        rr=rank_ge(rz); sr=rank_ge(sz); dr=rank_ge(dual)
        x={'row_id':row_id,'user_id':uid,'room_score10':float(ndcg10([rr])[0]),'streamer_score10':float(ndcg10([sr])[0]),'dual_score10':float(ndcg10([dr])[0])}
        if with_conf: x.update(dict(zip(CONF_FEATURES,conf_tuple(dual))))
        rows.append(x)
    return pd.DataFrame(rows)

def norm_entropy(items):
    c=Counter(items); n=sum(c.values())
    if n<=1 or len(c)<=1:return 0.0
    p=np.asarray(list(c.values()),float)/n; return float(-(p*np.log(p)).sum()/math.log(len(c)))
def js_div(a,b):
    ca,cb=Counter(a),Counter(b); keys=sorted(set(ca)|set(cb))
    if not keys:return 0.0
    pa=np.asarray([ca[k] for k in keys],float); pb=np.asarray([cb[k] for k in keys],float); pa/=pa.sum(); pb/=pb.sum(); m=.5*(pa+pb)
    def kl(p,q):
        z=p>0; return float((p[z]*np.log2(p[z]/q[z])).sum())
    return .5*kl(pa,m)+.5*kl(pb,m)
def regularity(times):
    if not times:return 0.0
    h=pd.to_datetime(pd.Series(times),unit='ms').dt.hour.to_numpy(float); a=2*np.pi*h/24
    return float(np.sqrt(np.mean(np.cos(a))**2+np.mean(np.sin(a))**2))
def hist_stats(sids,times):
    n=len(sids); recent_n=min(10,max(2,n//3)) if n>=3 else max(1,n//2)
    old=sids[:-recent_n] if n>recent_n else sids[:max(1,n//2)]; recent=sids[-recent_n:] if recent_n else sids
    return {'history_len':n,'repeat_rate':1-len(set(sids))/max(n,1),'preference_entropy':norm_entropy(sids),
            'preference_drift':js_div(old,recent) if old and recent else 0.0,'time_regularity':regularity(times)}
def memory_score(cand_room_items,sids,pop,item_to_streamer):
    cnt=Counter(sids); mx=max(cnt.values()) if cnt else 1; long={k:v/mx for k,v in cnt.items()}
    short={}
    for dist,sid in enumerate(reversed(sids[-10:])): short[sid]=max(short.get(sid,0.0),math.exp(-dist/3.0))
    cs=[item_to_streamer[int(i)] for i in cand_room_items]
    return np.asarray([.45*short.get(s,0)+.45*long.get(s,0)+.10*pop.get(s,0) for s in cs],float)

def dynamic_memory_features(train, phase, item_to_streamer, seed_hist=None):
    pop_s=pd.Series([item_to_streamer[int(i)] for i in train.item_id.astype(int)]).value_counts().astype(float); pop_s=np.log1p(pop_s)
    if len(pop_s): pop_s=(pop_s-pop_s.min())/max(float(pop_s.max()-pop_s.min()),EPS)
    pop={int(k):float(v) for k,v in pop_s.items()}
    hist={}
    if seed_hist is not None:
        for uid,(s,t) in seed_hist.items(): hist[int(uid)]=(list(s),list(t))
    else:
        for uid,g in train.groupby('user_id',sort=False): hist[int(uid)]=([item_to_streamer[int(i)] for i in g.item_id.astype(int)],g.time.astype('int64').tolist())
    rows=[]
    for row_id,r in enumerate(phase.itertuples(index=False)):
        uid=int(r.user_id); sids,times=hist.get(uid,([],[])); sids=list(sids); times=list(times)
        cands=np.concatenate(([int(r.item_id)],parse_list(r.neg_items,int)))
        ms=memory_score(cands,sids,pop,item_to_streamer); mr=rank_ge(ms); st=hist_stats(sids,times)
        rows.append({'row_id':row_id,'user_id':uid,'MemoryFusion_score10':float(ndcg10([mr])[0]),**st})
        sids.append(item_to_streamer[int(r.item_id)]); times.append(int(r.time)); hist[uid]=(sids,times)
    f=pd.DataFrame(rows)
    f['entropy_pct']=f.preference_entropy.rank(pct=True,method='average'); f['drift_pct']=f.preference_drift.rank(pct=True,method='average')
    f['history_pct']=np.log1p(f.history_len).rank(pct=True,method='average')
    f['state_complexity']=.4*f.entropy_pct+.4*f.drift_pct+.2*f.history_pct; f['log_history_len']=np.log1p(f.history_len.astype(float))
    return f,hist

def cluster_boot(diff,users,seed,n_boot=5000):
    z=pd.DataFrame({'u':np.asarray(users,int),'d':np.asarray(diff,float)}).groupby('u').d.agg(['sum','count']).reset_index()
    rng=np.random.default_rng(seed); b=np.empty(n_boot); n=len(z)
    sums=z['sum'].to_numpy(); cnt=z['count'].to_numpy()
    for i in range(n_boot):
        q=rng.integers(0,n,n); b[i]=sums[q].sum()/cnt[q].sum()
    return float(np.mean(diff)),float(np.quantile(b,.025)),float(np.quantile(b,.975))

def protocol_eval(label,mask_d,mask_t,dev_base,test_base,dev_mem,test_mem,seed):
    d=dev_base.loc[mask_d].merge(dev_mem.loc[mask_d],on=['row_id','user_id'],validate='one_to_one')
    t=test_base.loc[mask_t].merge(test_mem.loc[mask_t],on=['row_id','user_id'],validate='one_to_one')
    d['MemoryFusion_delta']=d.MemoryFusion_score10-d.dual_score10; t['MemoryFusion_delta']=t.MemoryFusion_score10-t.dual_score10
    feats=USER_FEATURES+CONF_FEATURES; Xd=d[feats].to_numpy(float); Xt=t[feats].to_numpy(float); yd=d.MemoryFusion_delta.to_numpy(float)
    cv=GroupKFold(n_splits=5); oof=cross_val_predict(hgb(),Xd,yd,groups=d.user_id.to_numpy(),cv=cv,method='predict')
    th,use_d,dev_sel=choose_threshold(oof,d.dual_score10.to_numpy(),d.MemoryFusion_score10.to_numpy())
    model=clone(hgb()).fit(Xd,yd); pred=model.predict(Xt); use_t=pred>th
    base=t.dual_score10.to_numpy(float); mem=t.MemoryFusion_score10.to_numpy(float); sel=np.where(use_t,mem,base)
    delta,lo,hi=cluster_boot(sel-base,t.user_id.to_numpy(),seed)
    md,mlo,mhi=cluster_boot(mem-base,t.user_id.to_numpy(),seed+1)
    macro=pd.DataFrame({'u':t.user_id,'b':base,'m':mem,'s':sel}).groupby('u').mean()
    report={'protocol':label,'dev_events':len(d),'test_events':len(t),'test_users':int(t.user_id.nunique()),
            'dual_id_test_ndcg10':float(base.mean()),'memory_test_ndcg10':float(mem.mean()),'selective_test_ndcg10':float(sel.mean()),
            'macro_user_dual_ndcg10':float(macro.b.mean()),'macro_user_selective_ndcg10':float(macro.s.mean()),
            'memory_minus_dual_delta':md,'memory_minus_dual_ci95':[mlo,mhi],
            'selective_minus_dual_delta':delta,'selective_minus_dual_ci95':[lo,hi],
            'dev_gate_rate':float(use_d.mean()),'test_gate_rate':float(use_t.mean()),'selected_events':int(use_t.sum()),
            'pass':bool(delta>0 and lo>0),'pass_rule':'event-level mean delta > 0 and user-cluster bootstrap 95% CI lower bound > 0'}
    return report,t.assign(predicted_memory_delta=pred,use_memory=use_t,selective_score10=sel)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--room-data-dir',type=Path,required=True); ap.add_argument('--streamer-data-dir',type=Path,required=True)
    ap.add_argument('--room-dev',type=Path,required=True); ap.add_argument('--room-test',type=Path,required=True); ap.add_argument('--streamer-dev',type=Path,required=True); ap.add_argument('--streamer-test',type=Path,required=True); ap.add_argument('--out-dir',type=Path,required=True)
    a=ap.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True)
    tr=pd.read_csv(a.room_data_dir/'train.csv',sep='\t'); dv=pd.read_csv(a.room_data_dir/'dev.csv',sep='\t'); te=pd.read_csv(a.room_data_dir/'test.csv',sep='\t')
    sdv=pd.read_csv(a.streamer_data_dir/'dev.csv',sep='\t'); ste=pd.read_csv(a.streamer_data_dir/'test.csv',sep='\t')
    rm=pd.read_csv(a.room_data_dir/'room_item_map.tsv',sep='\t'); item_to_streamer=dict(zip(rm.item_id.astype(int),rm.streamer_id.astype(int)))
    md=pd.read_csv(a.room_data_dir/'dev_manifest.csv'); mt=pd.read_csv(a.room_data_dir/'test_manifest.csv')
    dvectors=load_vectors(dv,sdv,a.room_dev,a.streamer_dev); tvectors=load_vectors(te,ste,a.room_test,a.streamer_test)
    dev_mem,dev_hist=dynamic_memory_features(tr,dv,item_to_streamer)
    test_mem,_=dynamic_memory_features(tr,te,item_to_streamer,seed_hist=dev_hist)
    reports={}
    for label,dm,tm in [('last',md.is_last.to_numpy(bool),mt.is_last.to_numpy(bool)),('successive',np.ones(len(dv),bool),np.ones(len(te),bool))]:
        # Tune Dual-ID alpha using this protocol's dev targets only.
        best=None
        for alpha in np.linspace(0,1,41):
            q=eval_vectors(dvectors,float(alpha),False).loc[dm,'dual_score10'].mean(); key=(float(q),float(alpha))
            if best is None or key>best[0]: best=(key,float(alpha))
        alpha=best[1]; db=eval_vectors(dvectors,alpha,True); tb=eval_vectors(tvectors,alpha,True)
        rep,per=protocol_eval(label,dm,tm,db,tb,dev_mem,test_mem,SEED+(401 if label=='last' else 501)); rep['alpha_room']=alpha; rep['alpha_streamer']=1-alpha
        reports[label]=rep; per.to_csv(a.out_dir/f'per_event_{label}.csv.gz',index=False,compression='gzip')
    meta=json.loads((a.room_data_dir/'export_meta.json').read_text()); out={'experiment':'GTS-Last_and_Successive_DualID_SelectiveMemory','split_meta':meta,'results':reports}
    (a.out_dir/'report.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))

if __name__=='__main__': main()
