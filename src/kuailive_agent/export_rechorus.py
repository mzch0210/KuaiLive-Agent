from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from .evaluate import split_events, candidate_sets


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prepared-dir',type=Path,required=True); ap.add_argument('--out-root',type=Path,required=True); ap.add_argument('--dataset',default='KuaiLiveShop'); ap.add_argument('--n-neg',type=int,default=574); ap.add_argument('--seed',type=int,default=20260918)
    a=ap.parse_args(); events=pd.read_pickle(a.prepared_dir/'events.pkl'); rooms=pd.read_pickle(a.prepared_dir/'rooms.pkl')
    train,dev,test=split_events(events,3)
    # ReChorus SeqReader merges on (user,item,time); remove exact duplicate triples to avoid merge multiplication.
    splits=[]; dup={}
    for name,x in [('train',train),('dev',dev),('test',test)]:
        before=len(x); x=x.drop_duplicates(['user_id','streamer_id','timestamp'],keep='last').copy(); dup[name]=before-len(x); splits.append(x)
    train,dev,test=splits
    users=sorted(set(train.user_id)|set(dev.user_id)|set(test.user_id)); uidmap={int(u):i+1 for i,u in enumerate(users)}
    positive=set(pd.concat([train.streamer_id,dev.streamer_id,test.streamer_id]).astype(int))
    room_items=set(rooms.streamer_id.dropna().astype(int)); unseen=sorted(room_items-positive); seen=sorted(positive)
    # Put positive-seen items last so max positive id equals the total item universe; ReChorus infers n_items from positive rows.
    ordered=unseen+seen; imap={s:i+1 for i,s in enumerate(ordered)}
    assert max(imap[s] for s in positive)==len(imap)
    dev_cs=candidate_sets(dev,rooms,a.n_neg,a.seed); test_cs=candidate_sets(test,rooms,a.n_neg,a.seed)
    def base(x):
        return pd.DataFrame({'user_id':x.user_id.astype(int).map(uidmap),'item_id':x.streamer_id.astype(int).map(imap),'time':x.timestamp.astype('int64')})
    tr=base(train); dv=base(dev); te=base(test)
    def negcol(x,csets):
        vals=[]; lens=[]
        for idx,r in x.iterrows():
            target=int(r.streamer_id); c=csets[idx][1:]
            # active-at-time negatives from the same room universe; exclude target and de-duplicate stably.
            out=[]; used={target}
            for s in c:
                s=int(s)
                if s in imap and s not in used:
                    out.append(imap[s]); used.add(s)
            vals.append(str(out)); lens.append(len(out))
        return vals, np.asarray(lens,dtype=int)
    dv_neg,dv_len=negcol(dev,dev_cs); te_neg,te_len=negcol(test,test_cs)
    # ReChorus BaseReader materializes neg_items as a dense 2-D ndarray; ragged candidate lists are invalid.
    # Fail here with a useful diagnostic rather than later inside ReChorus.
    if not (np.all(dv_len==a.n_neg) and np.all(te_len==a.n_neg)):
        raise ValueError(
            f'Fixed candidate requirement failed for n_neg={a.n_neg}: '
            f'dev min/max={dv_len.min()}/{dv_len.max()}, test min/max={te_len.min()}/{te_len.max()}, '
            f'dev short={(dv_len<a.n_neg).sum()}, test short={(te_len<a.n_neg).sum()}. '
            'Choose n_neg no larger than the minimum legal active-at-time candidate count.'
        )
    dv['neg_items']=dv_neg; te['neg_items']=te_neg
    out=a.out_root/a.dataset; out.mkdir(parents=True,exist_ok=True)
    tr.to_csv(out/'train.csv',sep='\t',index=False); dv.to_csv(out/'dev.csv',sep='\t',index=False); te.to_csv(out/'test.csv',sep='\t',index=False)
    meta={'dataset':a.dataset,'seed':a.seed,'n_neg':a.n_neg,'train_rows':len(tr),'dev_rows':len(dv),'test_rows':len(te),'users':len(uidmap),'item_universe':len(imap),'positive_items':len(positive),'duplicates_dropped':dup,'dev_neg_min':int(dv_len.min()),'dev_neg_max':int(dv_len.max()),'test_neg_min':int(te_len.min()),'test_neg_max':int(te_len.max())}
    (out/'export_meta.json').write_text(json.dumps(meta,indent=2)+'\n'); print(json.dumps(meta,indent=2))

if __name__=='__main__': main()
