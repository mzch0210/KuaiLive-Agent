from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np, pandas as pd, torch

SEED=20260918
BUDGETS=[.05,.10,.15,.20,.30]

class Selector(torch.nn.Module):
    def __init__(self,d):
        super().__init__(); self.net=torch.nn.Sequential(torch.nn.Linear(d,32),torch.nn.ReLU(),torch.nn.Linear(32,1))
    def forward(self,x): return self.net(x).squeeze(-1)

def fit_selector(X,label,budget,seed):
    torch.manual_seed(seed); X=np.asarray(X,np.float32); mu=X.mean(0); sd=X.std(0); sd[sd<1e-6]=1
    xt=torch.from_numpy((X-mu)/sd); yt=torch.from_numpy(np.asarray(label,np.float32))
    m=Selector(X.shape[1]); opt=torch.optim.Adam(m.parameters(),lr=1e-3)
    for _ in range(400):
        opt.zero_grad(); logit=m(xt); prob=torch.sigmoid(logit)
        loss=torch.nn.functional.binary_cross_entropy_with_logits(logit,yt)+.01*torch.abs(prob.mean()-budget)
        loss.backward(); opt.step()
    return m,mu,sd

def predict_selector(m,mu,sd,X):
    z=((np.asarray(X,np.float32)-mu)/sd).astype(np.float32)
    with torch.no_grad(): return torch.sigmoid(m(torch.from_numpy(z))).numpy()

def topk_mask(score,rate):
    score=np.asarray(score,float); k=max(1,int(round(rate*len(score))))
    idx=np.argsort(-score,kind='mergesort')[:k]; m=np.zeros(len(score),bool); m[idx]=True
    return m,k

def bootstrap(x,n=5000,seed=SEED):
    x=np.asarray(x,float); rng=np.random.default_rng(seed); N=len(x); vals=np.empty(n,float)
    for i in range(n): vals[i]=x[rng.integers(0,N,N)].mean()
    return float(x.mean()),float(np.quantile(vals,.025)),float(np.quantile(vals,.975))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dual-test',type=Path,required=True)
    ap.add_argument('--ds-scores',type=Path,required=True)
    ap.add_argument('--out-dir',type=Path,required=True)
    a=ap.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True)

    ours=pd.read_csv(a.dual_test).sort_values('user_id').reset_index(drop=True)
    ds=np.load(a.ds_scores)
    if len(ours)!=len(ds['user_id']): raise ValueError((len(ours),len(ds['user_id'])))
    if not np.array_equal(ours.user_id.astype(int).to_numpy(),ds['user_id'].astype(int)):
        raise ValueError('user alignment mismatch')

    means={'mean':float(ds['dev_slow_mean_ndcg10'].mean()),'final':float(ds['dev_slow_final_ndcg10'].mean())}
    slow=max(means,key=means.get)
    dfast=ds['dev_fast_ce'].astype(float); dslow=ds[f'dev_slow_{slow}_ce'].astype(float)
    label=(dslow<dfast).astype(np.float32)
    Xd=ds['dev_fast_hidden'].astype(np.float32); Xt=ds['test_fast_hidden'].astype(np.float32)
    tf=ds['test_fast_ndcg10'].astype(float); ts=ds[f'test_slow_{slow}_ndcg10'].astype(float)

    ob=ours.dual_score10.to_numpy(float); om=ours.MemoryFusion_score10.to_numpy(float)
    gate=ours.primary_pred_delta.to_numpy(float)
    rows=[]
    for j,b in enumerate(BUDGETS):
        use_o,k=topk_mask(gate,b); os=np.where(use_o,om,ob)
        sel,mu,sd=fit_selector(Xd,label,b,SEED+j); pte=predict_selector(sel,mu,sd,Xt); use_d,k2=topk_mask(pte,b)
        if k!=k2: raise ValueError('budget mismatch')
        ds_sel=np.where(use_d,ts,tf)
        dd,dl,dh=bootstrap(ds_sel-tf,seed=SEED+10+j)
        od,ol,oh=bootstrap(os-ob,seed=SEED+20+j)
        cr,cl,ch=bootstrap(os-ds_sel,seed=SEED+30+j)
        rows.append({'target_budget':b,'k':k,'realized_rate':k/len(ours),
                     'ds_fast_test_ndcg10':float(tf.mean()),'ds_slow_test_ndcg10':float(ts.mean()),
                     'ds_selective_test_ndcg10':float(ds_sel.mean()),'ds_delta_vs_fast':dd,'ds_delta_ci_low':dl,'ds_delta_ci_high':dh,
                     'ours_dualid_test_ndcg10':float(ob.mean()),'ours_memory_test_ndcg10':float(om.mean()),
                     'ours_selective_test_ndcg10':float(os.mean()),'ours_delta_vs_dualid':od,'ours_delta_ci_low':ol,'ours_delta_ci_high':oh,
                     'ours_minus_ds_selective':cr,'cross_ci_low':cl,'cross_ci_high':ch,
                     'ds_gain_per_invocation':dd/(k/len(ours)),'ours_gain_per_invocation':od/(k/len(ours))})
    out=pd.DataFrame(rows); out.to_csv(a.out_dir/'matched_budget_room.csv',index=False)
    report={'protocol':'KuaiLive next-live-room; 574 legal active-room negatives; exact same K on test by unlabeled gate-score ranking',
            'ours':'frozen Dual-ID base + frozen Selective-v2 room gate predictions from dual_id_room_baseline.py',
            'dsframe':'capacity-matched PRL slow path + paper-faithful MLP selector reimplementation; selector trained on dev only',
            'slow_variant_selected_on_dev':slow,'dev_slow_ndcg_variants':means,'results':rows}
    (a.out_dir/'report.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))

if __name__=='__main__': main()
