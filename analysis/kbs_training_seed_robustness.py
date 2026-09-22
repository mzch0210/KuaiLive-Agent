from __future__ import annotations

import argparse, ast, json, math, re
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_predict

SEED0=20260918
EPS=1e-12
STATE=["log_history_len","repeat_rate","preference_entropy","preference_drift","time_regularity","state_complexity"]
CONF=["sas_score_std","sas_score_range","sas_margin12","sas_margin15","sas_margin1011","sas_top1_z","sas_entropy","sas_top10_mass"]
FEATURES=STATE+CONF

def parse_list(s,dtype=float):
    s=str(s).strip()
    s=re.sub(r"np\.(?:float(?:16|32|64)|int(?:8|16|32|64)|uint(?:8|16|32|64))\(([^()]*)\)",r"\1",s)
    return np.asarray(ast.literal_eval(s),dtype=dtype)

def ndcg(rank,k=10):
    return 0.0 if int(rank)>k else 1.0/math.log2(int(rank)+1.0)

def rec_features(rec_path:Path, phase_path:Path):
    phase=pd.read_csv(phase_path,sep='\t',usecols=['user_id','item_id'])
    targets=phase.set_index('user_id').item_id.astype(int).to_dict()
    pred=pd.read_csv(rec_path,sep='\t')
    rows=[]
    for r in pred.itertuples(index=False):
        uid=int(r.user_id); items=parse_list(r.rec_items,int); s=parse_list(r.rec_predictions,float)
        if len(items)!=575 or len(s)!=575: raise ValueError((uid,len(items),len(s)))
        tgt=targets[uid]; hit=np.flatnonzero(items==tgt)
        if len(hit)!=1: raise ValueError((uid,tgt,len(hit)))
        rank=int(np.sum(s>=float(s[int(hit[0])]))); ss=np.sort(s)[::-1]
        mean=float(s.mean()); std=float(s.std()); rng=float(s.max()-s.min())
        ex=np.exp(np.clip(s-s.max(),-60,0)); p=ex/ex.sum(); ps=np.sort(p)[::-1]
        ent=float(-(p*np.log(np.maximum(p,EPS))).sum()/math.log(len(p)))
        rows.append({'user_id':uid,'base_ndcg10':ndcg(rank),
            'sas_score_std':std,'sas_score_range':rng,'sas_margin12':float(ss[0]-ss[1]),
            'sas_margin15':float(ss[0]-ss[4]),'sas_margin1011':float(ss[9]-ss[10]),
            'sas_top1_z':float((ss[0]-mean)/max(std,EPS)),'sas_entropy':ent,
            'sas_top10_mass':float(ps[:10].sum())})
    out=pd.DataFrame(rows)
    if out.user_id.duplicated().any(): raise ValueError('duplicate users')
    return out

def choose_threshold(pred,base,memory):
    ths=np.unique(np.r_[np.inf,np.quantile(pred,np.linspace(0,1,201)),-np.inf])
    best=None
    for th in ths:
        use=pred>th; score=float(np.where(use,memory,base).mean())
        key=(score,-float(use.mean()))
        if best is None or key>best[0]: best=(key,float(th),use)
    return best[1],best[2]

def bootstrap(x,seed,n=3000):
    x=np.asarray(x,float); rng=np.random.default_rng(seed); N=len(x)
    b=np.asarray([x[rng.integers(0,N,N)].mean() for _ in range(n)])
    return float(x.mean()),float(np.quantile(b,.025)),float(np.quantile(b,.975))

def run_seed(seed:int,recovered:Path,rechorus:Path,rec_dev:Path,rec_test:Path,n_boot:int):
    d0=pd.read_csv(recovered/'per_user_dev.csv.gz'); t0=pd.read_csv(recovered/'per_user_test.csv.gz')
    d=rec_features(rec_dev,rechorus/'dev.csv').merge(d0,on='user_id',validate='one_to_one')
    t=rec_features(rec_test,rechorus/'test.csv').merge(t0,on='user_id',validate='one_to_one')
    # MemoryFusion_score10 is independent of base training seed; recompute delta against this seed's base.
    d['memory_ndcg10']=d['MemoryFusion_score10']; t['memory_ndcg10']=t['MemoryFusion_score10']
    d['utility']=d.memory_ndcg10-d.base_ndcg10; t['utility']=t.memory_ndcg10-t.base_ndcg10
    X=d[FEATURES].to_numpy(float); Xt=t[FEATURES].to_numpy(float)
    hgb=lambda: HistGradientBoostingRegressor(max_iter=200,learning_rate=.05,max_depth=3,min_samples_leaf=50,l2_regularization=1.0,random_state=seed)
    cv=KFold(n_splits=5,shuffle=True,random_state=seed)
    u_oof=cross_val_predict(hgb(),X,d.utility.to_numpy(float),cv=cv,method='predict')
    th,use_dev=choose_threshold(u_oof,d.base_ndcg10.to_numpy(),d.memory_ndcg10.to_numpy())
    u_model=hgb().fit(X,d.utility.to_numpy(float)); u_test=u_model.predict(Xt); use_u=u_test>th
    sel=np.where(use_u,t.memory_ndcg10,t.base_ndcg10); K=int(use_u.sum())
    diff_model=hgb().fit(X,1-d.base_ndcg10.to_numpy(float)); diff_pred=diff_model.predict(Xt)
    order=np.argsort(-diff_pred,kind='mergesort'); use_d=np.zeros(len(t),bool); use_d[order[:K]]=True
    diff=np.where(use_d,t.memory_ndcg10,t.base_ndcg10)
    ds,lo,hi=bootstrap(sel-t.base_ndcg10.to_numpy(),seed+101,n_boot)
    ud,ulo,uhi=bootstrap(sel-diff,seed+202,n_boot)
    return {'training_seed':seed,'n_test':len(t),'base_ndcg10':float(t.base_ndcg10.mean()),
        'always_memory_ndcg10':float(t.memory_ndcg10.mean()),'selective_ndcg10':float(sel.mean()),
        'difficulty_exactk_ndcg10':float(diff.mean()),'invocation_k':K,'invocation_rate':float(K/len(t)),
        'selective_minus_base':ds,'selective_minus_base_ci95':[lo,hi],
        'utility_minus_difficulty':ud,'utility_minus_difficulty_ci95':[ulo,uhi]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--recovered-dir',type=Path,required=True); ap.add_argument('--rechorus-dir',type=Path,required=True)
    ap.add_argument('--seed-root',type=Path,required=True); ap.add_argument('--seeds',nargs='+',type=int,default=[20260918,20260919,20260920]); ap.add_argument('--out-dir',type=Path,required=True); ap.add_argument('--n-boot',type=int,default=3000)
    a=ap.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True); rows=[]
    for seed in a.seeds:
        root=a.seed_root/f'seed{seed}'/'SASRec_seed'
        rows.append(run_seed(seed,a.recovered_dir,a.rechorus_dir,root/'rec-SASRec-dev.csv',root/'rec-SASRec-test.csv',a.n_boot))
    df=pd.DataFrame(rows); df.to_csv(a.out_dir/'training_seed_results.csv',index=False)
    summary={'seeds':a.seeds,'n_seeds':len(rows),'all_selective_minus_base_positive':bool((df.selective_minus_base>0).all()),
        'all_utility_minus_difficulty_positive':bool((df.utility_minus_difficulty>0).all()),
        'selective_minus_base_mean':float(df.selective_minus_base.mean()),'selective_minus_base_std':float(df.selective_minus_base.std(ddof=1)),
        'utility_minus_difficulty_mean':float(df.utility_minus_difficulty.mean()),'utility_minus_difficulty_std':float(df.utility_minus_difficulty.std(ddof=1))}
    (a.out_dir/'training_seed_summary.json').write_text(json.dumps(summary,indent=2)); print(df.to_string(index=False)); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
