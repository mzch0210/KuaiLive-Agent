from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np, pandas as pd
from kuailive_agent.evaluate import split_events
from kuailive_agent.export_rechorus_room import room_candidate_sets


def _hist(seq):
    return " ".join(str(int(x)) for x in seq)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prepared-dir',type=Path,required=True)
    ap.add_argument('--out-root',type=Path,required=True)
    ap.add_argument('--dataset',default='KuaiLiveDSRoom')
    ap.add_argument('--n-neg',type=int,default=574)
    ap.add_argument('--seed',type=int,default=20260918)
    ap.add_argument('--history-max',type=int,default=50)
    a=ap.parse_args()

    ev=pd.read_pickle(a.prepared_dir/'events.pkl').sort_values(['user_id','timestamp','live_id'],kind='mergesort')
    rooms=pd.read_pickle(a.prepared_dir/'rooms.pkl')
    tr,dv,te=split_events(ev,3)

    cleaned=[]; dup={}
    for name,x in [('train',tr),('dev',dv),('test',te)]:
        before=len(x)
        x=x.drop_duplicates(['user_id','live_id','timestamp'],keep='last').copy()
        dup[name]=before-len(x); cleaned.append(x)
    tr,dv,te=cleaned
    common=sorted(set(dv.user_id.astype(int)) & set(te.user_id.astype(int)))
    tr=tr[tr.user_id.astype(int).isin(common)].copy()
    dv=dv[dv.user_id.astype(int).isin(common)].copy()
    te=te[te.user_id.astype(int).isin(common)].copy()
    if dv.user_id.duplicated().any() or te.user_id.duplicated().any():
        raise ValueError('room-level dev/test must contain one target per user')

    room_meta=rooms[['live_id']].dropna().drop_duplicates('live_id').copy()
    universe=set(room_meta.live_id.astype(int))
    positive=set(pd.concat([tr.live_id,dv.live_id,te.live_id]).astype(int))
    missing=positive-universe
    if missing: raise ValueError(f'positive live_ids absent from metadata: {len(missing)}')
    ordered=sorted(universe-positive)+sorted(positive)
    imap={r:i for i,r in enumerate(ordered)}
    inv=np.asarray(ordered,dtype=np.int64)
    umap={u:i for i,u in enumerate(common)}

    rows=[]
    for uid,g in tr.groupby('user_id',sort=False):
        seq=[imap[int(x)] for x in g.sort_values(['timestamp','live_id'],kind='mergesort').live_id.astype(int)]
        u=umap[int(uid)]
        for j in range(1,len(seq)):
            rows.append({'user_id':u,'item_id':seq[j],'history_id':_hist(seq[max(0,j-a.history_max):j])})

    train_hist={int(uid):[imap[int(x)] for x in g.sort_values(['timestamp','live_id'],kind='mergesort').live_id.astype(int)] for uid,g in tr.groupby('user_id',sort=False)}
    dev_target={int(r.user_id):imap[int(r.live_id)] for r in dv.itertuples(index=False)}
    test_target={int(r.user_id):imap[int(r.live_id)] for r in te.itertuples(index=False)}
    valid=[]; test=[]
    for uid in common:
        h=train_hist[int(uid)][-a.history_max:]; u=umap[int(uid)]; d=dev_target[int(uid)]; t=test_target[int(uid)]
        valid.append({'user_id':u,'item_id':d,'history_id':_hist(h)})
        test.append({'user_id':u,'item_id':t,'history_id':_hist((h+[d])[-a.history_max:])})

    dev_cs,dev_len,dev_active=room_candidate_sets(dv,rooms,a.n_neg,a.seed)
    test_cs,test_len,test_active=room_candidate_sets(te,rooms,a.n_neg,a.seed)
    if not (np.all(dev_len==a.n_neg) and np.all(test_len==a.n_neg)):
        raise ValueError('fixed room candidate requirement failed')

    def mapped(frame,csets):
        out=[]
        for idx,r in frame.iterrows():
            vals=[]; used=set()
            for rid in csets[idx]:
                rid=int(rid)
                if rid in imap and rid not in used:
                    vals.append(imap[rid]); used.add(rid)
            if len(vals)!=a.n_neg+1:
                raise ValueError(f'candidate length {len(vals)} != {a.n_neg+1} at row {idx}')
            out.append(vals)
        return np.asarray(out,dtype=np.int64)

    dev_c=mapped(dv,dev_cs); test_c=mapped(te,test_cs)
    out=a.out_root/a.dataset; out.mkdir(parents=True,exist_ok=True); cols=['user_id','item_id','history_id']
    pd.DataFrame(rows,columns=cols).to_csv(out/f'{a.dataset}.train.remap.csv',index=False)
    pd.DataFrame(valid,columns=cols).to_csv(out/f'{a.dataset}.valid.remap.csv',index=False)
    pd.DataFrame(test,columns=cols).to_csv(out/f'{a.dataset}.test.remap.csv',index=False)
    np.savez_compressed(out/'eval_candidates.npz',dev=dev_c,test=test_c,user_ids=np.arange(1,len(common)+1,dtype=np.int64),item_inverse=inv)
    meta={'dataset':a.dataset,'task':'next_live_room','seed':a.seed,'n_neg':a.n_neg,'candidate_count':a.n_neg+1,
          'train_rows':len(rows),'dev_rows':len(valid),'test_rows':len(test),'users':len(common),'item_universe':len(imap),
          'history_max':a.history_max,'duplicates_dropped':dup,'dev_target_active_rate':dev_active/max(len(dv),1),
          'test_target_active_rate':test_active/max(len(te),1),'candidate_protocol':'active live-room IDs; positive first; frozen seed 20260918'}
    (out/'export_meta.json').write_text(json.dumps(meta,indent=2)+'\n'); print(json.dumps(meta,indent=2))

if __name__=='__main__': main()
