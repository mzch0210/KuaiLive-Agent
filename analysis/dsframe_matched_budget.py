from __future__ import annotations
import argparse, ast, json, math, re
from pathlib import Path
import numpy as np, pandas as pd, torch
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_predict

SEED=20260918; EPS=1e-12
BUDGETS=[.05,.10,.15,.20,.30]
USER_FEATURES=['log_history_len','repeat_rate','preference_entropy','preference_drift','time_regularity','state_complexity']
CONF_FEATURES=['sas_score_std','sas_score_range','sas_margin12','sas_margin15','sas_margin1011','sas_top1_z','sas_entropy','sas_top10_mass']


def parse_list(s):
    s=str(s).strip()
    if s.startswith('[') and s.endswith(']') and 'np.' not in s:
        return np.fromstring(s[1:-1],sep=',',dtype=float)
    s=re.sub(r"np\.(?:float(?:16|32|64)|int(?:8|16|32|64)|uint(?:8|16|32|64))\(([^()]*)\)",r"\1",s)
    return np.asarray(ast.literal_eval(s),dtype=float)

def confidence(path:Path):
    rows=[]; df=pd.read_csv(path,sep='\t',usecols=['user_id','rec_predictions'])
    for r in df.itertuples(index=False):
        x=parse_list(r.rec_predictions); ss=np.sort(x)[::-1]; mu=float(x.mean()); sd=float(x.std()); rg=float(x.max()-x.min())
        ex=np.exp(np.clip(x-x.max(),-60,0)); p=ex/ex.sum(); ps=np.sort(p)[::-1]
        rows.append({'user_id':int(r.user_id),'sas_score_std':sd,'sas_score_range':rg,'sas_margin12':float(ss[0]-ss[1]),
            'sas_margin15':float(ss[0]-ss[4]),'sas_margin1011':float(ss[9]-ss[10]),'sas_top1_z':float((ss[0]-mu)/max(sd,EPS)),
            'sas_entropy':float(-(p*np.log(np.maximum(p,EPS))).sum()/math.log(len(p))),'sas_top10_mass':float(ps[:10].sum())})
    return pd.DataFrame(rows)

def rate_threshold(x,rate):
    x=np.asarray(x,float); k=max(1,int(round(rate*len(x))))
    idx=np.argsort(-x,kind='mergesort'); cut=float(x[idx[k-1]])
    # continuous model scores make ties rare; use >= and report realized rate.
    return cut

def bootstrap(diff,n=2000,seed=SEED):
    x=np.asarray(diff,float); rng=np.random.default_rng(seed); N=len(x); vals=np.empty(n,float)
    for i in range(n): vals[i]=x[rng.integers(0,N,N)].mean()
    return float(x.mean()),float(np.quantile(vals,.025)),float(np.quantile(vals,.975))

class Selector(torch.nn.Module):
    def __init__(self,d):
        super().__init__(); self.net=torch.nn.Sequential(torch.nn.Linear(d,32),torch.nn.ReLU(),torch.nn.Linear(32,1))
    def forward(self,x): return self.net(x).squeeze(-1)

def fit_selector(X,label,budget,seed):
    torch.manual_seed(seed); X=np.asarray(X,np.float32); mu=X.mean(0); sd=X.std(0); sd[sd<1e-6]=1
    xt=torch.from_numpy((X-mu)/sd); yt=torch.from_numpy(np.asarray(label,np.float32)); m=Selector(X.shape[1]); opt=torch.optim.Adam(m.parameters(),lr=1e-3)
    for _ in range(400):
        opt.zero_grad(); logit=m(xt); prob=torch.sigmoid(logit); loss=torch.nn.functional.binary_cross_entropy_with_logits(logit,yt)+.01*torch.abs(prob.mean()-budget); loss.backward(); opt.step()
    with torch.no_grad(): p=torch.sigmoid(m(xt)).numpy()
    return m,mu,sd,p

def predict_selector(model,mu,sd,X):
    with torch.no_grad(): return torch.sigmoid(model(torch.from_numpy(((np.asarray(X,np.float32)-mu)/sd).astype(np.float32)))).numpy()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--recovered-dir',type=Path,required=True); ap.add_argument('--sasrec-dev',type=Path,required=True); ap.add_argument('--sasrec-test',type=Path,required=True); ap.add_argument('--ds-scores',type=Path,required=True); ap.add_argument('--out-dir',type=Path,required=True)
    a=ap.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True)
    def findone(root,name):
        q=list(root.rglob(name));
        if len(q)!=1: raise ValueError((name,[str(x) for x in q]))
        return q[0]
    dev=pd.read_csv(findone(a.recovered_dir,'per_user_dev.csv.gz')); test=pd.read_csv(findone(a.recovered_dir,'per_user_test.csv.gz'))
    dev=dev.merge(confidence(a.sasrec_dev),on='user_id',validate='one_to_one'); test=test.merge(confidence(a.sasrec_test),on='user_id',validate='one_to_one')
    dev=dev.sort_values('user_id').reset_index(drop=True); test=test.sort_values('user_id').reset_index(drop=True)
    assert np.array_equal(dev.user_id.to_numpy(),np.arange(1,len(dev)+1)); assert np.array_equal(test.user_id.to_numpy(),np.arange(1,len(test)+1))
    ds=np.load(a.ds_scores); assert len(ds['user_id'])==len(dev)==len(test)
    # Select one DS slow aggregation on dev only; this is the sole slow-output model selection.
    means={'mean':float(ds['dev_slow_mean_ndcg10'].mean()),'final':float(ds['dev_slow_final_ndcg10'].mean())}
    slow_variant=max(means,key=means.get); print('slow_variant',slow_variant,means,flush=True)
    ds_dev_fast=ds['dev_fast_ndcg10'].astype(float); ds_test_fast=ds['test_fast_ndcg10'].astype(float)
    ds_dev_slow=ds[f'dev_slow_{slow_variant}_ndcg10'].astype(float); ds_test_slow=ds[f'test_slow_{slow_variant}_ndcg10'].astype(float)
    ds_dev_fast_ce=ds['dev_fast_ce'].astype(float); ds_dev_slow_ce=ds[f'dev_slow_{slow_variant}_ce'].astype(float)
    oracle_label=(ds_dev_slow_ce < ds_dev_fast_ce).astype(np.float32)
    Xds_dev=ds['dev_fast_hidden'].astype(np.float32); Xds_test=ds['test_fast_hidden'].astype(np.float32)
    # Frozen v2 HGB structure; OOF dev scores define budget thresholds, full-dev fit predicts test.
    feats=USER_FEATURES+CONF_FEATURES; Xd=dev[feats].to_numpy(float); Xt=test[feats].to_numpy(float); yd=dev.MemoryFusion_delta.to_numpy(float)
    hgb=HistGradientBoostingRegressor(max_iter=200,learning_rate=.05,max_depth=3,min_samples_leaf=50,l2_regularization=1.0,random_state=SEED)
    cv=KFold(n_splits=5,shuffle=True,random_state=SEED); oof=cross_val_predict(hgb,Xd,yd,cv=cv,method='predict'); ptest=clone(hgb).fit(Xd,yd).predict(Xt)
    sas_dev=dev.sasrec_score10.to_numpy(float); sas_test=test.sasrec_score10.to_numpy(float); mem_dev=dev.MemoryFusion_score10.to_numpy(float); mem_test=test.MemoryFusion_score10.to_numpy(float)
    rows=[]
    for j,b in enumerate(BUDGETS):
        # Ours: target budget fixed from OOF dev score distribution; same threshold applied to test.
        thm=rate_threshold(oof,b); use_md=oof>=thm; use_mt=ptest>=thm; ours_dev=np.where(use_md,mem_dev,sas_dev); ours_test=np.where(use_mt,mem_test,sas_test)
        # DS-Frame selector reimplementation from paper: MLP on fast hidden, BCE oracle guidance + budget regularizer.
        selector,mu,sd,pdev=fit_selector(Xds_dev,oracle_label,b,SEED+j); thd=rate_threshold(pdev,b); use_dd=pdev>=thd; pte=predict_selector(selector,mu,sd,Xds_test); use_dt=pte>=thd
        ds_dev_sel=np.where(use_dd,ds_dev_slow,ds_dev_fast); ds_test_sel=np.where(use_dt,ds_test_slow,ds_test_fast)
        # Random routing expectation and test oracle upper bound are diagnostics, not trained models.
        rng=np.random.default_rng(SEED+100+j); rand=[]
        k=max(1,int(round(b*len(ds_test_fast))))
        for _ in range(200):
            mask=np.zeros(len(ds_test_fast),bool); mask[rng.choice(len(mask),k,replace=False)]=True; rand.append(float(np.where(mask,ds_test_slow,ds_test_fast).mean()))
        delta=ds_test_slow-ds_test_fast; oi=np.argsort(-delta,kind='mergesort')[:k]; om=np.zeros(len(delta),bool); om[oi]=True; oracle=float(np.where(om,ds_test_slow,ds_test_fast).mean())
        d_ds,lo_ds,hi_ds=bootstrap(ds_test_sel-ds_test_fast,seed=SEED+10+j); d_ours,lo_o,hi_o=bootstrap(ours_test-sas_test,seed=SEED+20+j); d_cross,lo_c,hi_c=bootstrap(ours_test-ds_test_sel,seed=SEED+30+j)
        rows.append({'target_budget':b,'slow_variant':slow_variant,'ds_dev_gate_rate':float(use_dd.mean()),'ds_test_gate_rate':float(use_dt.mean()),
            'ds_fast_test_ndcg10':float(ds_test_fast.mean()),'ds_slow_test_ndcg10':float(ds_test_slow.mean()),'ds_selective_test_ndcg10':float(ds_test_sel.mean()),
            'ds_delta_vs_fast':d_ds,'ds_delta_ci_low':lo_ds,'ds_delta_ci_high':hi_ds,'ds_random_test_ndcg10_mean':float(np.mean(rand)),'ds_oracle_test_ndcg10':oracle,
            'ours_dev_gate_rate':float(use_md.mean()),'ours_test_gate_rate':float(use_mt.mean()),'sasrec_test_ndcg10':float(sas_test.mean()),'memory_test_ndcg10':float(mem_test.mean()),
            'ours_selective_test_ndcg10':float(ours_test.mean()),'ours_delta_vs_sasrec':d_ours,'ours_delta_ci_low':lo_o,'ours_delta_ci_high':hi_o,
            'ours_minus_ds_selective':d_cross,'cross_ci_low':lo_c,'cross_ci_high':hi_c})
    out=pd.DataFrame(rows); out.to_csv(a.out_dir/'matched_budget.csv',index=False)
    report={'protocol':'KuaiLive shop streamer-level LOO; 574 active-at-time negatives; candidate seed 20260918','budgets':BUDGETS,
        'dsframe':'capacity-matched PRL slow path + paper-faithful MLP selector reimplementation; selector source is absent from public repo',
        'selector_oracle':'dev slow full-item CE < dev fast full-item CE; lambda_c=0 because computation is externally matched by routing budget; no test labels used',
        'selector_budget_loss_weight':.01,'ds_slow_variant_selected_on_dev':slow_variant,'ds_dev_slow_ndcg10_variants':means,
        'ours':'frozen Selective v2 HGB architecture/features; budget threshold from 5-fold OOF dev predictions; full dev fit then test once','results':rows}
    (a.out_dir/'report.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
if __name__=='__main__': main()
