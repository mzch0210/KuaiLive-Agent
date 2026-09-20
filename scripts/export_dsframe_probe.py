from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np, pandas as pd
from kuailive_agent.evaluate import split_events


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prepared-dir',type=Path,required=True); ap.add_argument('--out-root',type=Path,required=True)
    ap.add_argument('--dataset',default='KuaiLiveDSProbe'); ap.add_argument('--train-fraction',type=float,default=.02); ap.add_argument('--eval-users',type=int,default=512); ap.add_argument('--seed',type=int,default=20260918); ap.add_argument('--history-max',type=int,default=50)
    a=ap.parse_args(); rng=np.random.default_rng(a.seed)
    ev=pd.read_pickle(a.prepared_dir/'events.pkl').sort_values(['user_id','timestamp','streamer_id'],kind='mergesort')
    tr,dv,te=split_events(ev,3); common=sorted(set(dv.user_id.astype(int)) & set(te.user_id.astype(int)))
    tr=tr[tr.user_id.isin(common)].copy(); dv=dv[dv.user_id.isin(common)].copy(); te=te[te.user_id.isin(common)].copy()
    umap={u:i for i,u in enumerate(common)}
    streamers=sorted(set(pd.concat([tr.streamer_id,dv.streamer_id,te.streamer_id]).astype(int))); imap={s:i for i,s in enumerate(streamers)}
    train_rows=[]; total_full=0
    for uid,g in tr.groupby('user_id',sort=False):
        seq=[imap[int(x)] for x in g.streamer_id.astype(int)]; u=umap[int(uid)]
        for j in range(1,len(seq)):
            total_full+=1
            if rng.random() <= a.train_fraction:
                train_rows.append({'user_id':u,'item_id':seq[j],'item_seq':str(seq[max(0,j-a.history_max):j])})
    eval_users=set(rng.choice(common,size=min(a.eval_users,len(common)),replace=False).tolist())
    valid=[]; test=[]
    train_hist={int(u):[imap[int(x)] for x in g.streamer_id.astype(int)] for u,g in tr.groupby('user_id',sort=False)}
    dev_target={int(r.user_id):imap[int(r.streamer_id)] for r in dv.itertuples(index=False)}
    test_target={int(r.user_id):imap[int(r.streamer_id)] for r in te.itertuples(index=False)}
    for uid in sorted(eval_users):
        h=train_hist[int(uid)][-a.history_max:]; u=umap[int(uid)]; d=dev_target[int(uid)]; t=test_target[int(uid)]
        valid.append({'user_id':u,'item_id':d,'item_seq':str(h)})
        test.append({'user_id':u,'item_id':t,'item_seq':str((h+[d])[-a.history_max:])})
    out=a.out_root/a.dataset; out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(train_rows).to_csv(out/f'{a.dataset}.train.remap.csv',index=False)
    pd.DataFrame(valid).to_csv(out/f'{a.dataset}.valid.remap.csv',index=False)
    pd.DataFrame(test).to_csv(out/f'{a.dataset}.test.remap.csv',index=False)
    meta={'dataset':a.dataset,'train_fraction':a.train_fraction,'probe_train_rows':len(train_rows),'estimated_full_train_rows':total_full,'eval_users':len(eval_users),'item_universe':len(imap),'history_max':a.history_max,'seed':a.seed}
    (out/'probe_meta.json').write_text(json.dumps(meta,indent=2)+'\n'); print(json.dumps(meta,indent=2))
if __name__=='__main__': main()
