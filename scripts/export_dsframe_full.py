from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np, pandas as pd
from kuailive_agent.evaluate import split_events, candidate_sets


def _hist(seq):
    return " ".join(str(int(x)) for x in seq)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prepared-dir',type=Path,required=True); ap.add_argument('--out-root',type=Path,required=True)
    ap.add_argument('--dataset',default='KuaiLiveDSFull'); ap.add_argument('--n-neg',type=int,default=574)
    ap.add_argument('--seed',type=int,default=20260918); ap.add_argument('--history-max',type=int,default=50)
    a=ap.parse_args()
    ev=pd.read_pickle(a.prepared_dir/'events.pkl').sort_values(['user_id','timestamp','live_id'],kind='mergesort')
    rooms=pd.read_pickle(a.prepared_dir/'rooms.pkl')
    tr,dv,te=split_events(ev,3)
    common=sorted(set(dv.user_id.astype(int)) & set(te.user_id.astype(int)))
    tr=tr[tr.user_id.isin(common)].copy(); dv=dv[dv.user_id.isin(common)].copy(); te=te[te.user_id.isin(common)].copy()
    # Include every streamer that can occur in active-at-time candidates. Put positive items last so
    # the largest observed target id spans the full real item universe; BaseReader then adds padding.
    positive=set(pd.concat([tr.streamer_id,dv.streamer_id,te.streamer_id]).astype(int))
    all_items=set(rooms.streamer_id.dropna().astype(int)); ordered=sorted(all_items-positive)+sorted(positive)
    imap={s:i for i,s in enumerate(ordered)}; inv=np.asarray(ordered,dtype=np.int64)
    umap={u:i for i,u in enumerate(common)}
    rows=[]
    for uid,g in tr.groupby('user_id',sort=False):
        seq=[imap[int(x)] for x in g.streamer_id.astype(int)]; u=umap[int(uid)]
        for j in range(1,len(seq)):
            rows.append({'user_id':u,'item_id':seq[j],'history_id':_hist(seq[max(0,j-a.history_max):j])})
    train_hist={int(u):[imap[int(x)] for x in g.streamer_id.astype(int)] for u,g in tr.groupby('user_id',sort=False)}
    dev_target={int(r.user_id):imap[int(r.streamer_id)] for r in dv.itertuples(index=False)}
    test_target={int(r.user_id):imap[int(r.streamer_id)] for r in te.itertuples(index=False)}
    valid=[]; test=[]
    for uid in common:
        h=train_hist[int(uid)][-a.history_max:]; u=umap[int(uid)]; d=dev_target[int(uid)]; t=test_target[int(uid)]
        valid.append({'user_id':u,'item_id':d,'history_id':_hist(h)})
        test.append({'user_id':u,'item_id':t,'history_id':_hist((h+[d])[-a.history_max:])})
    dev_cs=candidate_sets(dv,rooms,a.n_neg,a.seed); test_cs=candidate_sets(te,rooms,a.n_neg,a.seed)
    def mapped_candidates(frame,csets):
        out=[]
        for idx,r in frame.iterrows():
            vals=[]; used=set()
            for sid in csets[idx]:
                sid=int(sid)
                if sid in imap and sid not in used:
                    vals.append(imap[sid]); used.add(sid)
            if len(vals)!=a.n_neg+1:
                raise ValueError(f'candidate length {len(vals)} != {a.n_neg+1} at row {idx}')
            out.append(vals)
        return np.asarray(out,dtype=np.int64)
    dev_c=mapped_candidates(dv,dev_cs); test_c=mapped_candidates(te,test_cs)
    out=a.out_root/a.dataset; out.mkdir(parents=True,exist_ok=True); cols=['user_id','item_id','history_id']
    pd.DataFrame(rows,columns=cols).to_csv(out/f'{a.dataset}.train.remap.csv',index=False)
    pd.DataFrame(valid,columns=cols).to_csv(out/f'{a.dataset}.valid.remap.csv',index=False)
    pd.DataFrame(test,columns=cols).to_csv(out/f'{a.dataset}.test.remap.csv',index=False)
    np.savez_compressed(out/'eval_candidates.npz',dev=dev_c,test=test_c,user_ids=np.asarray(common,dtype=np.int64),item_inverse=inv)
    meta={'dataset':a.dataset,'seed':a.seed,'n_neg':a.n_neg,'candidate_count':a.n_neg+1,'train_rows':len(rows),'dev_rows':len(valid),'test_rows':len(test),'users':len(common),'item_universe':len(imap),'history_max':a.history_max,'schema':cols,'candidate_protocol':'active-at-time fixed candidates; positive first; same frozen seed as main streamer-level experiment'}
    (out/'export_meta.json').write_text(json.dumps(meta,indent=2)+'\n'); print(json.dumps(meta,indent=2))
if __name__=='__main__': main()
