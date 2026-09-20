from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import torch
import torch.nn.functional as F


def ndcg10_from_scores(scores: torch.Tensor) -> torch.Tensor:
    # candidate 0 is the positive; strict greater plus deterministic candidate-order tie break
    tgt=scores[:,0:1]
    rank=1+(scores[:,1:]>tgt).sum(1)
    out=torch.zeros_like(tgt[:,0])
    m=rank<=10
    out[m]=1.0/torch.log2(rank[m].float()+1.0)
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--ds-source',type=Path,required=True); ap.add_argument('--data-root',type=Path,required=True)
    ap.add_argument('--dataset',required=True); ap.add_argument('--model-path',type=Path,required=True)
    ap.add_argument('--candidates',type=Path,required=True); ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--batch-size',type=int,default=128)
    a=ap.parse_args(); sys.path.insert(0,str(a.ds_source.resolve()))
    from helpers.BaseReader import BaseReader
    from models.PRL import PRL
    from utils.constants import ITEM_SEQ, ITEM_SEQ_LEN, ITEM_ID

    args=SimpleNamespace(sep=',',path=str(a.data_root.resolve()),dataset=a.dataset,device=torch.device('cpu'),
        model_path=str(a.model_path.resolve()),buffer=0,dropout=.2,test_all=1,emb_size=64,num_layers=1,
        num_heads=4,inner_size=128,hidden_act='gelu',layer_norm_eps=1e-12,initializer_range=.02,
        temperature=.07,reason_step=2,pl_weight=1.0,temp_scale=5.0,noise_factor=.01,cl_weight=1.0,warmup=2)
    corpus=BaseReader(args); model=PRL(args,corpus).to(args.device); model.load_state_dict(torch.load(a.model_path,map_location='cpu')); model.eval()
    cand=np.load(a.candidates,allow_pickle=False); user_ids=cand['user_ids'].astype(np.int64)
    W=model.item_emb.weight.detach()
    result={'user_id':user_ids}
    meta={'dataset':a.dataset,'slow_variants':['mean','final'],'primary_selection':'choose slow variant by dev all-slow NDCG only; then freeze for test','model_path':str(a.model_path)}
    for phase,key in [('dev','valid'),('test','test')]:
        C=torch.from_numpy(cand[phase].astype(np.int64)); data=corpus.data_dict[key]
        assert len(C)==len(data[ITEM_ID])==len(user_ids),(phase,len(C),len(data[ITEM_ID]),len(user_ids))
        hidden=[]; fast_nd=[]; mean_nd=[]; final_nd=[]; fast_ce=[]; mean_ce=[]; final_ce=[]
        for st in range(0,len(C),a.batch_size):
            en=min(len(C),st+a.batch_size)
            seq=data[ITEM_SEQ][st:en]; slen=data[ITEM_SEQ_LEN][st:en]; labels=data[ITEM_ID][st:en]
            feed={ITEM_SEQ:seq,ITEM_SEQ_LEN:slen,ITEM_ID:labels}
            with torch.no_grad():
                out=model(feed,stage='infer'); mo=out['model_output']
                fast=mo[:,0,:]; mean=mo.mean(1); final=mo[:,-1,:]
                cc=C[st:en]; emb=W[cc]
                sf=torch.einsum('bd,bkd->bk',fast,emb)/model.temperature
                sm=torch.einsum('bd,bkd->bk',mean,emb)/model.temperature
                sl=torch.einsum('bd,bkd->bk',final,emb)/model.temperature
                # paper-faithful selector supervision: full-item predictive loss, computed batchwise.
                lf=torch.matmul(fast,W.T)/model.temperature
                lm=torch.matmul(mean,W.T)/model.temperature
                ll=torch.matmul(final,W.T)/model.temperature
                fast_ce.append(F.cross_entropy(lf,labels,reduction='none').cpu().numpy())
                mean_ce.append(F.cross_entropy(lm,labels,reduction='none').cpu().numpy())
                final_ce.append(F.cross_entropy(ll,labels,reduction='none').cpu().numpy())
                hidden.append(fast.cpu().numpy()); fast_nd.append(ndcg10_from_scores(sf).cpu().numpy())
                mean_nd.append(ndcg10_from_scores(sm).cpu().numpy()); final_nd.append(ndcg10_from_scores(sl).cpu().numpy())
        result[f'{phase}_fast_hidden']=np.concatenate(hidden).astype(np.float32)
        result[f'{phase}_fast_ndcg10']=np.concatenate(fast_nd).astype(np.float32)
        result[f'{phase}_slow_mean_ndcg10']=np.concatenate(mean_nd).astype(np.float32)
        result[f'{phase}_slow_final_ndcg10']=np.concatenate(final_nd).astype(np.float32)
        result[f'{phase}_fast_ce']=np.concatenate(fast_ce).astype(np.float32)
        result[f'{phase}_slow_mean_ce']=np.concatenate(mean_ce).astype(np.float32)
        result[f'{phase}_slow_final_ce']=np.concatenate(final_ce).astype(np.float32)
        meta[f'{phase}_fast_ndcg10']=float(result[f'{phase}_fast_ndcg10'].mean())
        meta[f'{phase}_slow_mean_ndcg10']=float(result[f'{phase}_slow_mean_ndcg10'].mean())
        meta[f'{phase}_slow_final_ndcg10']=float(result[f'{phase}_slow_final_ndcg10'].mean())
    a.out.parent.mkdir(parents=True,exist_ok=True); np.savez_compressed(a.out,**result)
    a.out.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n'); print(json.dumps(meta,indent=2))

if __name__=='__main__': main()
