from __future__ import annotations

import argparse, math, random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader

from .evaluate import split_events, candidate_sets, ndcg, target_rank


def seed_all(seed:int):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)


def encode_ids(train, val, test):
    ids = pd.concat([train['streamer_id'], val['streamer_id'], test['streamer_id']]).astype(int).unique()
    sid2idx = {int(s): i+1 for i,s in enumerate(ids)}
    return sid2idx


def user_sequences(df, sid2idx):
    seqs={}; times={}
    for uid,g in df.sort_values(['user_id','timestamp','live_id']).groupby('user_id', sort=False):
        seqs[int(uid)] = [sid2idx[int(x)] for x in g.streamer_id.tolist() if int(x) in sid2idx]
        times[int(uid)] = [int(x) for x in g.timestamp.tolist()][-len(seqs[int(uid)]):]
    return seqs,times


class PairDataset(Dataset):
    def __init__(self, train, sid2idx, n_items, seed=0):
        self.rows=[(int(r.user_id), sid2idx[int(r.streamer_id)]) for r in train.itertuples(index=False)]
        self.users={u:i for i,u in enumerate(sorted({u for u,_ in self.rows}))}
        self.n_items=n_items; self.rng=np.random.default_rng(seed)
    def __len__(self): return len(self.rows)
    def __getitem__(self,i):
        u,pos=self.rows[i]; neg=int(self.rng.integers(1,self.n_items+1))
        while neg==pos: neg=int(self.rng.integers(1,self.n_items+1))
        return self.users[u],pos,neg


class BPRMF(nn.Module):
    def __init__(self,n_users,n_items,dim=48):
        super().__init__(); self.u=nn.Embedding(n_users,dim); self.i=nn.Embedding(n_items+1,dim,padding_idx=0)
        nn.init.normal_(self.u.weight,std=.02); nn.init.normal_(self.i.weight,std=.02)
    def forward(self,u,p,n):
        ue=self.u(u); return (ue*self.i(p)).sum(-1),(ue*self.i(n)).sum(-1)


class SeqDataset(Dataset):
    def __init__(self, seqs, times, n_items, max_len=30, max_samples_per_user=40, seed=0):
        self.examples=[]; self.n_items=n_items; self.max_len=max_len; self.rng=np.random.default_rng(seed)
        for uid,seq in seqs.items():
            ts=times[uid]; starts=list(range(1,len(seq)))
            if len(starts)>max_samples_per_user: starts=starts[-max_samples_per_user:]
            for j in starts:
                self.examples.append((seq[max(0,j-max_len):j], ts[max(0,j-max_len):j], seq[j]))
    def __len__(self): return len(self.examples)
    def __getitem__(self,i):
        seq,ts,pos=self.examples[i]; L=len(seq)
        x=np.zeros(self.max_len,np.int64); h=np.zeros(self.max_len,np.int64); x[-L:]=seq
        hours=pd.to_datetime(pd.Series(ts),unit='ms').dt.hour.to_numpy(np.int64)+1; h[-L:]=hours
        neg=int(self.rng.integers(1,self.n_items+1))
        while neg==pos: neg=int(self.rng.integers(1,self.n_items+1))
        return x,h,pos,neg


class SASRecLite(nn.Module):
    def __init__(self,n_items,dim=48,max_len=30,n_heads=2,time_aware=False):
        super().__init__(); self.max_len=max_len
        self.item=nn.Embedding(n_items+1,dim,padding_idx=0); self.pos=nn.Embedding(max_len,dim)
        self.hour=nn.Embedding(25,dim,padding_idx=0) if time_aware else None
        layer=nn.TransformerEncoderLayer(d_model=dim,nhead=n_heads,dim_feedforward=dim*2,dropout=.1,batch_first=True,norm_first=True)
        self.enc=nn.TransformerEncoder(layer,num_layers=1); self.norm=nn.LayerNorm(dim)
    def encode(self,x,hour=None):
        b,L=x.shape; pos=torch.arange(L,device=x.device).unsqueeze(0).expand(b,L)
        z=self.item(x)+self.pos(pos)
        if self.hour is not None and hour is not None: z=z+self.hour(hour)
        pad=x.eq(0); causal=torch.triu(torch.ones(L,L,device=x.device,dtype=torch.bool),1)
        z=self.enc(z,mask=causal,src_key_padding_mask=pad)
        return self.norm(z[:,-1,:])
    def pair_scores(self,x,h,pos,neg):
        z=self.encode(x,h); return (z*self.item(pos)).sum(-1),(z*self.item(neg)).sum(-1)


def bpr_loss(ps,ns): return -torch.log(torch.sigmoid(ps-ns)+1e-8).mean()


def train_bpr(train,sid2idx,n_items,device,seed,epochs=3):
    ds=PairDataset(train,sid2idx,n_items,seed); model=BPRMF(len(ds.users),n_items).to(device)
    dl=DataLoader(ds,batch_size=2048,shuffle=True,num_workers=0); opt=torch.optim.Adam(model.parameters(),lr=2e-3,weight_decay=1e-6)
    for ep in range(epochs):
        tot=0.0
        for u,p,n in dl:
            u,p,n=u.to(device),p.to(device),n.to(device); ps,ns=model(u,p,n); loss=bpr_loss(ps,ns)
            opt.zero_grad(); loss.backward(); opt.step(); tot+=loss.item()*len(u)
        print(f'BPRMF epoch {ep+1}/{epochs} loss={tot/len(ds):.4f}')
    return model,ds.users


def train_seq(seqs,times,n_items,device,seed,time_aware=False,epochs=2,max_len=30):
    ds=SeqDataset(seqs,times,n_items,max_len=max_len,seed=seed); model=SASRecLite(n_items,max_len=max_len,time_aware=time_aware).to(device)
    dl=DataLoader(ds,batch_size=512,shuffle=True,num_workers=0); opt=torch.optim.Adam(model.parameters(),lr=1e-3,weight_decay=1e-6)
    for ep in range(epochs):
        tot=0.0
        for x,h,p,n in dl:
            x,h,p,n=x.to(device),h.to(device),p.to(device),n.to(device); ps,ns=model.pair_scores(x,h,p,n); loss=bpr_loss(ps,ns)
            opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),5.0); opt.step(); tot+=loss.item()*len(x)
        print(f"{'TimeSASRec' if time_aware else 'SASRec'} epoch {ep+1}/{epochs} loss={tot/len(ds):.4f}")
    return model


def seq_context(seq,ts,max_len):
    L=min(len(seq),max_len); x=np.zeros(max_len,np.int64); h=np.zeros(max_len,np.int64)
    if L:
        x[-L:]=seq[-L:]; hours=pd.to_datetime(pd.Series(ts[-L:]),unit='ms').dt.hour.to_numpy(np.int64)+1; h[-L:]=hours
    return x,h


def evaluate_models(prepared_dir:Path,out_dir:Path,n_neg:int,seed:int,epochs_bpr:int,epochs_seq:int,max_len:int):
    seed_all(seed); device=torch.device('cpu'); torch.set_num_threads(max(1,min(4,torch.get_num_threads())))
    events=pd.read_pickle(prepared_dir/'events.pkl'); rooms=pd.read_pickle(prepared_dir/'rooms.pkl')
    train,val,test=split_events(events,3); sid2idx=encode_ids(train,val,test); n_items=len(sid2idx); seqs,times=user_sequences(train,sid2idx)
    print(f'train={len(train):,} test={len(test):,} users={test.user_id.nunique():,} items={n_items:,}')
    bpr,user_map=train_bpr(train,sid2idx,n_items,device,seed,epochs_bpr)
    sas=train_seq(seqs,times,n_items,device,seed,False,epochs_seq,max_len)
    tsa=train_seq(seqs,times,n_items,device,seed,True,epochs_seq,max_len)
    csets=candidate_sets(test,rooms,n_neg,seed); rows=[]; bpr.eval(); sas.eval(); tsa.eval()
    with torch.no_grad():
        for idx,r in test.iterrows():
            cands=csets[idx]; enc=np.array([sid2idx.get(int(s),0) for s in cands],dtype=np.int64); valid=enc>0; cand_t=torch.tensor(enc,device=device)
            uid=int(r.user_id); x,h=seq_context(seqs.get(uid,[]),times.get(uid,[]),max_len); xt=torch.tensor(x[None,:],device=device); ht=torch.tensor(h[None,:],device=device)
            scores={}
            if uid in user_map:
                ue=bpr.u(torch.tensor([user_map[uid]],device=device)); sc=(bpr.i(cand_t)*ue).sum(-1).cpu().numpy(); sc[~valid]=-1e9; scores['BPRMF']=sc
            z=sas.encode(xt,ht); sc=(sas.item(cand_t)*z).sum(-1).cpu().numpy(); sc[~valid]=-1e9; scores['SASRec']=sc
            z=tsa.encode(xt,ht); sc=(tsa.item(cand_t)*z).sum(-1).cpu().numpy(); sc[~valid]=-1e9; scores['TimeSASRec']=sc
            for name,sc in scores.items():
                rows.append({'user_id':uid,'model':name,'rank':target_rank(cands,sc),'long_view':bool(int(r.watch_live_time)>=30000),'candidate_count':len(cands)})
    raw=pd.DataFrame(rows); summaries=[]
    for m,g in raw.groupby('model'):
        lv=g[g.long_view]
        summaries.append({'model':m,'users':g.user_id.nunique(),'recall@10':(g['rank']<=10).mean(),'ndcg@10':g['rank'].map(lambda r:ndcg(int(r),10)).mean(),'mrr':(1/g['rank']).mean(),'longview_recall@10':(lv['rank']<=10).mean(),'longview_ndcg@10':lv['rank'].map(lambda r:ndcg(int(r),10)).mean()})
    summ=pd.DataFrame(summaries).sort_values('ndcg@10',ascending=False); out_dir.mkdir(parents=True,exist_ok=True)
    raw.to_csv(out_dir/f'deep_per_user_seed{seed}.csv.gz',index=False,compression='gzip'); summ.to_csv(out_dir/f'deep_summary_seed{seed}.csv',index=False); print(summ.to_string(index=False))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prepared-dir',type=Path,required=True); ap.add_argument('--out-dir',type=Path,required=True); ap.add_argument('--n-neg',type=int,default=999); ap.add_argument('--seed',type=int,default=20260918); ap.add_argument('--epochs-bpr',type=int,default=3); ap.add_argument('--epochs-seq',type=int,default=2); ap.add_argument('--max-len',type=int,default=30)
    a=ap.parse_args(); evaluate_models(a.prepared_dir,a.out_dir,a.n_neg,a.seed,a.epochs_bpr,a.epochs_seq,a.max_len)
if __name__=='__main__': main()
