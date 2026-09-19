from __future__ import annotations
import argparse, ast, json, math, re, zipfile, zlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

SEED=20260918
EPS=1e-12
USER_FEATURES=["log_history_len","repeat_rate","preference_entropy","preference_drift","time_regularity","state_complexity"]
CONF_FEATURES=["sas_score_std","sas_score_range","sas_margin12","sas_margin15","sas_margin1011","sas_top1_z","sas_entropy","sas_top10_mass"]
AGENTS=["MemoryFusion","LongMemory","ShortMemory"]

def parse_list(s):
    s=str(s).strip()
    if s.startswith("[") and s.endswith("]") and "np." not in s:
        return np.fromstring(s[1:-1], sep=",", dtype=float)
    s=re.sub(r"np\.(?:float(?:16|32|64)|int(?:8|16|32|64)|uint(?:8|16|32|64))\(([^()]*)\)",r"\1",s)
    return np.asarray(ast.literal_eval(s),dtype=float)

def confidence_features_from_zip(zip_path:Path, member:str)->pd.DataFrame:
    rows=[]
    with zipfile.ZipFile(zip_path) as z, z.open(member) as f:
        df=pd.read_csv(f,sep='\t',usecols=['user_id','rec_predictions'])
    for r in df.itertuples(index=False):
        s=parse_list(r.rec_predictions)
        if len(s)!=575: raise ValueError((r.user_id,len(s)))
        if np.any(s[:-1] < s[1:] - 1e-7):
            ss=np.sort(s)[::-1]
        else:
            ss=s
        mean=float(s.mean()); std=float(s.std()); rng=float(s.max()-s.min())
        top1z=float((ss[0]-mean)/max(std,EPS))
        ex=np.exp(np.clip(s-s.max(),-60,0)); p=ex/ex.sum()
        ent=float(-(p*np.log(np.maximum(p,EPS))).sum()/math.log(len(p)))
        ps=np.sort(p)[::-1]
        rows.append({'user_id':int(r.user_id),'sas_score_std':std,'sas_score_range':rng,
                     'sas_margin12':float(ss[0]-ss[1]),'sas_margin15':float(ss[0]-ss[4]),
                     'sas_margin1011':float(ss[9]-ss[10]),'sas_top1_z':top1z,
                     'sas_entropy':ent,'sas_top10_mass':float(ps[:10].sum())})
    return pd.DataFrame(rows)

def ndcg_array_from_rank(r):
    r=np.asarray(r,int)
    out=np.zeros(len(r),float); m=r<=10
    out[m]=1/np.log2(r[m]+1)
    return out

def bootstrap_delta(diff,seed=SEED,n_boot=4000):
    x=np.asarray(diff,float); n=len(x); rng=np.random.default_rng(seed)
    means=[]
    for _ in range(n_boot): means.append(float(x[rng.integers(0,n,n)].mean()))
    b=np.asarray(means)
    return float(x.mean()),float(np.quantile(b,.025)),float(np.quantile(b,.975))

def choose_threshold(pred, sas, agent):
    pred=np.asarray(pred,float); sas=np.asarray(sas,float); agent=np.asarray(agent,float)
    qs=np.unique(np.quantile(pred,np.linspace(0,1,201)))
    ths=np.r_[np.inf,qs,-np.inf]
    best=None
    for th in ths:
        use=pred>th; score=float(np.where(use,agent,sas).mean())
        key=(score,-float(use.mean()),float(th) if np.isfinite(th) else (1e99 if th>0 else -1e99))
        if best is None or key>best[0]: best=(key,float(th),use)
    return best[1],best[2],best[0][0]

def eval_binary_gate(name, model, features, dev, test):
    Xd=dev[features].to_numpy(float); Xt=test[features].to_numpy(float)
    yd=dev['MemoryFusion_delta'].to_numpy(float)
    sas_d=dev.sasrec_score10.to_numpy(float); ag_d=dev.MemoryFusion_score10.to_numpy(float)
    sas_t=test.sasrec_score10.to_numpy(float); ag_t=test.MemoryFusion_score10.to_numpy(float)
    cv=KFold(n_splits=5,shuffle=True,random_state=SEED)
    oof=cross_val_predict(model,Xd,yd,cv=cv,n_jobs=None,method='predict')
    th,use_d,dev_score=choose_threshold(oof,sas_d,ag_d)
    m=clone(model).fit(Xd,yd); pred=m.predict(Xt); use_t=pred>th
    sel=np.where(use_t,ag_t,sas_t)
    delta,lo,hi=bootstrap_delta(sel-sas_t,SEED+zlib.crc32(name.encode())%10000)
    return {'gate':name,'feature_set':'+'.join(features),'threshold':th,
            'dev_gate_rate':float(use_d.mean()),'dev_selective_ndcg10':float(dev_score),
            'test_gate_rate':float(use_t.mean()),'test_selective_ndcg10':float(sel.mean()),
            'test_delta':delta,'ci95_low':lo,'ci95_high':hi,'selected_n':int(use_t.sum()),
            'selected_history_mean':float(test.loc[use_t,'history_len'].mean()) if use_t.any() else np.nan,
            'unselected_history_mean':float(test.loc[~use_t,'history_len'].mean()) if (~use_t).any() else np.nan}, pred, use_t

def eval_history_threshold(dev,test):
    sas_d=dev.sasrec_score10.to_numpy(float); ag_d=dev.MemoryFusion_score10.to_numpy(float)
    vals=np.unique(dev.history_len.to_numpy(int)); best=None
    for th in np.r_[np.inf, vals, -np.inf]:
        use=dev.history_len.to_numpy(float)>=th
        score=float(np.where(use,ag_d,sas_d).mean())
        key=(score,-float(use.mean()),float(th) if np.isfinite(th) else (1e99 if th>0 else -1e99))
        if best is None or key>best[0]: best=(key,float(th),use)
    th=best[1]; use_t=test.history_len.to_numpy(float)>=th
    sas_t=test.sasrec_score10.to_numpy(float); ag_t=test.MemoryFusion_score10.to_numpy(float)
    sel=np.where(use_t,ag_t,sas_t); d,lo,hi=bootstrap_delta(sel-sas_t,SEED+900)
    return {'gate':'history_threshold','feature_set':'history_len','threshold':th,
            'dev_gate_rate':float(best[2].mean()),'dev_selective_ndcg10':float(best[0][0]),
            'test_gate_rate':float(use_t.mean()),'test_selective_ndcg10':float(sel.mean()),
            'test_delta':d,'ci95_low':lo,'ci95_high':hi,'selected_n':int(use_t.sum()),
            'selected_history_mean':float(test.loc[use_t,'history_len'].mean()) if use_t.any() else np.nan,
            'unselected_history_mean':float(test.loc[~use_t,'history_len'].mean()) if (~use_t).any() else np.nan}

def eval_multi_router(name, model, features, dev, test):
    Xd=dev[features].to_numpy(float); Xt=test[features].to_numpy(float)
    cv=KFold(n_splits=5,shuffle=True,random_state=SEED)
    oof_pred={}; test_pred={}
    for a in AGENTS:
        y=dev[f'{a}_delta'].to_numpy(float)
        oof_pred[a]=cross_val_predict(model,Xd,y,cv=cv,method='predict')
        test_pred[a]=clone(model).fit(Xd,y).predict(Xt)
    oof_mat=np.column_stack([oof_pred[a] for a in AGENTS]); test_mat=np.column_stack([test_pred[a] for a in AGENTS])
    max_oof=oof_mat.max(axis=1); max_test=test_mat.max(axis=1)
    idx_oof=oof_mat.argmax(axis=1); idx_test=test_mat.argmax(axis=1)
    sas_d=dev.sasrec_score10.to_numpy(float); sas_t=test.sasrec_score10.to_numpy(float)
    agent_dev=np.column_stack([dev[f'{a}_score10'].to_numpy(float) for a in AGENTS])
    agent_test=np.column_stack([test[f'{a}_score10'].to_numpy(float) for a in AGENTS])
    chosen_d=agent_dev[np.arange(len(dev)),idx_oof]; chosen_t=agent_test[np.arange(len(test)),idx_test]
    th,use_d,dev_score=choose_threshold(max_oof,sas_d,chosen_d)
    use_t=max_test>th; sel=np.where(use_t,chosen_t,sas_t)
    d,lo,hi=bootstrap_delta(sel-sas_t,SEED+1200+zlib.crc32(name.encode())%10000)
    action=np.array(['SASRec']*len(test),dtype=object); cand=np.array(AGENTS,dtype=object)[idx_test]; action[use_t]=cand[use_t]
    counts=pd.Series(action).value_counts().to_dict()
    return {'gate':name,'feature_set':'+'.join(features),'threshold':th,
            'dev_gate_rate':float(use_d.mean()),'dev_selective_ndcg10':float(dev_score),
            'test_gate_rate':float(use_t.mean()),'test_selective_ndcg10':float(sel.mean()),
            'test_delta':d,'ci95_low':lo,'ci95_high':hi,'selected_n':int(use_t.sum()),
            **{f'action_{k}':int(counts.get(k,0)) for k in ['SASRec']+AGENTS}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--recovered-dir',type=Path,required=True)
    ap.add_argument('--sasrec-dev',type=Path,required=True)
    ap.add_argument('--sasrec-test',type=Path,required=True)
    ap.add_argument('--out-dir',type=Path,required=True)
    args=ap.parse_args(); args.out_dir.mkdir(parents=True,exist_ok=True)
    dev=pd.read_csv(args.recovered_dir/'per_user_dev.csv.gz'); test=pd.read_csv(args.recovered_dir/'per_user_test.csv.gz')
    def confidence_features_from_file(path: Path) -> pd.DataFrame:
        rows=[]; df=pd.read_csv(path,sep='\t',usecols=['user_id','rec_predictions'])
        for r in df.itertuples(index=False):
            scores=parse_list(r.rec_predictions)
            if len(scores)!=575: raise ValueError((r.user_id,len(scores)))
            ss=np.sort(scores)[::-1]; mean=float(scores.mean()); std=float(scores.std()); rng=float(scores.max()-scores.min())
            ex=np.exp(np.clip(scores-scores.max(),-60,0)); prob=ex/ex.sum(); ps=np.sort(prob)[::-1]
            ent=float(-(prob*np.log(np.maximum(prob,EPS))).sum()/math.log(len(prob)))
            rows.append({'user_id':int(r.user_id),'sas_score_std':std,'sas_score_range':rng,
                         'sas_margin12':float(ss[0]-ss[1]),'sas_margin15':float(ss[0]-ss[4]),
                         'sas_margin1011':float(ss[9]-ss[10]),'sas_top1_z':float((ss[0]-mean)/max(std,EPS)),
                         'sas_entropy':ent,'sas_top10_mass':float(ps[:10].sum())})
        return pd.DataFrame(rows)
    conf_d=confidence_features_from_file(args.sasrec_dev); conf_t=confidence_features_from_file(args.sasrec_test)
    dev=dev.merge(conf_d,on='user_id',validate='one_to_one'); test=test.merge(conf_t,on='user_id',validate='one_to_one')
    assert len(dev)==10222 and len(test)==10222
    assert abs(dev.sasrec_score10.mean()-0.6114767450679792)<1e-10
    assert abs(test.sasrec_score10.mean()-0.6100980120259171)<1e-10

    ridge=lambda: make_pipeline(StandardScaler(),Ridge(alpha=1.0))
    tree=lambda: DecisionTreeRegressor(max_depth=3,min_samples_leaf=100,random_state=SEED)
    hgb=lambda: HistGradientBoostingRegressor(max_iter=200,learning_rate=0.05,max_depth=3,min_samples_leaf=50,l2_regularization=1.0,random_state=SEED)
    extra=lambda: ExtraTreesRegressor(n_estimators=300,max_depth=7,min_samples_leaf=20,max_features=0.8,n_jobs=-1,random_state=SEED)
    specs=[('ridge_state',ridge(),USER_FEATURES),('ridge_combined',ridge(),USER_FEATURES+CONF_FEATURES),
           ('tree3_state',tree(),USER_FEATURES),('tree3_combined',tree(),USER_FEATURES+CONF_FEATURES),
           ('hgb_state',hgb(),USER_FEATURES),('hgb_combined_PRIMARY',hgb(),USER_FEATURES+CONF_FEATURES),
           ('extra_combined',extra(),USER_FEATURES+CONF_FEATURES)]
    rows=[eval_history_threshold(dev,test)]; aux={}
    for name,model,features in specs:
        print('binary',name,flush=True)
        row,pred,use=eval_binary_gate(name,model,features,dev,test); rows.append(row); aux[name]=(pred,use)
    gates=pd.DataFrame(rows).sort_values('test_selective_ndcg10',ascending=False); gates.to_csv(args.out_dir/'binary_gates.csv',index=False)

    multi=[eval_multi_router('multi_hgb_state',hgb(),USER_FEATURES,dev,test),
           eval_multi_router('multi_hgb_combined',hgb(),USER_FEATURES+CONF_FEATURES,dev,test)]
    mult=pd.DataFrame(multi).sort_values('test_selective_ndcg10',ascending=False); mult.to_csv(args.out_dir/'multi_router.csv',index=False)

    pred,use=aux['hgb_combined_PRIMARY']; pt=test.copy(); pt['primary_pred_delta']=pred; pt['primary_use_agent']=use
    diag=[]
    for feat in ['history_len','repeat_rate','preference_entropy','preference_drift','time_regularity','sas_entropy','sas_margin12','sas_top1_z']:
        q=pd.qcut(pt[feat],4,labels=['Q1','Q2','Q3','Q4'],duplicates='drop')
        for lab,g in pt.groupby(q,observed=True):
            diag.append({'feature':feat,'quartile':str(lab),'n':len(g),'feature_mean':float(g[feat].mean()),
                         'gate_rate':float(g.primary_use_agent.mean()),'fusion_delta_mean':float(g.MemoryFusion_delta.mean())})
    pd.DataFrame(diag).to_csv(args.out_dir/'primary_subgroups.csv',index=False)
    pt[['user_id','history_len','sasrec_score10','MemoryFusion_score10','MemoryFusion_delta','primary_pred_delta','primary_use_agent']+CONF_FEATURES].to_csv(args.out_dir/'primary_per_user_test.csv.gz',index=False,compression='gzip')

    ex=extra().fit(dev[USER_FEATURES+CONF_FEATURES],dev.MemoryFusion_delta)
    imp=pd.DataFrame({'feature':USER_FEATURES+CONF_FEATURES,'extra_importance':ex.feature_importances_}).sort_values('extra_importance',ascending=False)
    imp.to_csv(args.out_dir/'feature_importance_descriptive.csv',index=False)

    Xd=dev[USER_FEATURES+CONF_FEATURES].to_numpy(float); Xt=test[USER_FEATURES+CONF_FEATURES].to_numpy(float)
    yd=dev.MemoryFusion_delta.to_numpy(float); sas_d=dev.sasrec_score10.to_numpy(float); ag_d=dev.MemoryFusion_score10.to_numpy(float)
    sas_t=test.sasrec_score10.to_numpy(float); ag_t=test.MemoryFusion_score10.to_numpy(float)
    full_primary=hgb().fit(Xd,yd); ptest=full_primary.predict(Xt); sens=[]
    for cv_seed in [20260918,20260919,20260920,20260921,20260922]:
        cv=KFold(n_splits=5,shuffle=True,random_state=cv_seed)
        oof=cross_val_predict(hgb(),Xd,yd,cv=cv,method='predict',n_jobs=-1)
        th,use_d,dev_score=choose_threshold(oof,sas_d,ag_d)
        use_t=ptest>th; selected=np.where(use_t,ag_t,sas_t)
        delta,lo,hi=bootstrap_delta(selected-sas_t,seed=cv_seed+100,n_boot=2000)
        sens.append({'cv_seed':cv_seed,'threshold':th,'dev_gate_rate':float(use_d.mean()),'dev_selective':dev_score,
                     'test_gate_rate':float(use_t.mean()),'test_selective':float(selected.mean()),'delta':delta,
                     'ci_low':lo,'ci_high':hi,'selected_n':int(use_t.sum())})
    sensitivity=pd.DataFrame(sens); sensitivity.to_csv(args.out_dir/'primary_cv_seed_sensitivity.csv',index=False)

    report={'protocol':'Analysis-locked primary before v2 test evaluation. All gate fitting and threshold selection use dev only; test is evaluation-only. Primary v2 = hgb_combined_PRIMARY.',
            'users':len(test),'sasrec_test_ndcg10':float(test.sasrec_score10.mean()),
            'memoryfusion_test_ndcg10':float(test.MemoryFusion_score10.mean()),
            'primary':gates[gates.gate=='hgb_combined_PRIMARY'].iloc[0].to_dict(),
            'best_binary_by_test_descriptive':gates.iloc[0].to_dict(),
            'best_multi_by_test_descriptive':mult.iloc[0].to_dict(),
            'primary_cv_seed_sensitivity':{'min_test_selective':float(sensitivity.test_selective.min()),
                                           'max_test_selective':float(sensitivity.test_selective.max()),
                                           'min_delta':float(sensitivity.delta.min()),'min_ci_low':float(sensitivity.ci_low.min())}}
    (args.out_dir/'report.json').write_text(json.dumps(report,indent=2,default=lambda x: float(x) if hasattr(x,'item') else str(x))+'\n')
    primary=gates.loc[gates.gate=='hgb_combined_PRIMARY'].iloc[0]
    assert primary.test_selective_ndcg10 > 0.620
    assert primary.ci95_low > 0.005
    assert sensitivity.delta.min() > 0.009
    assert sensitivity.ci_low.min() > 0.005
    print('\nBINARY\n',gates.to_string(index=False)); print('\nMULTI\n',mult.to_string(index=False)); print('\nIMPORTANCE\n',imp.to_string(index=False)); print('\nREPORT\n',json.dumps(report,indent=2,default=str))

if __name__=='__main__': main()
