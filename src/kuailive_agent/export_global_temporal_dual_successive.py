from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .evaluate import IndexedCounterSet


def _active_room_candidates(targets: pd.DataFrame, rooms: pd.DataFrame, max_n: int, seed: int):
    rr = rooms[['live_id','streamer_id','start_timestamp','end_timestamp']].dropna().drop_duplicates('live_id').copy()
    rr[['live_id','streamer_id','start_timestamp','end_timestamp']] = rr[['live_id','streamer_id','start_timestamp','end_timestamp']].astype('int64')
    starts = rr.sort_values('start_timestamp')
    ends = rr.sort_values('end_timestamp')
    s_t = starts.start_timestamp.to_numpy(); s_id = starts.live_id.to_numpy()
    e_t = ends.end_timestamp.to_numpy(); e_id = ends.live_id.to_numpy()
    ordered = targets.reset_index().sort_values(['timestamp','user_id','live_id'], kind='mergesort')
    active = IndexedCounterSet(); i = j = 0; rng = np.random.default_rng(seed); out = {}
    for r in ordered.itertuples(index=False):
        t = int(r.timestamp)
        while i < len(s_t) and int(s_t[i]) <= t:
            active.add(int(s_id[i])); i += 1
        while j < len(e_t) and int(e_t[j]) < t:
            active.remove(int(e_id[j])); j += 1
        target = int(r.live_id)
        neg = active.sample(max_n, rng, exclude=target)
        out[int(r.index)] = np.concatenate(([target], neg))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepared-dir', type=Path, required=True)
    ap.add_argument('--out-root', type=Path, required=True)
    ap.add_argument('--room-dataset', default='KuaiLiveShopGTSRoom')
    ap.add_argument('--streamer-dataset', default='KuaiLiveShopGTSStreamer')
    ap.add_argument('--train-q', type=float, default=.80)
    ap.add_argument('--dev-q', type=float, default=.90)
    ap.add_argument('--max-n-neg', type=int, default=574)
    ap.add_argument('--seed', type=int, default=20260918)
    ap.add_argument('--min-train-events', type=int, default=3)
    a = ap.parse_args()

    events = pd.read_pickle(a.prepared_dir/'events.pkl').sort_values(['timestamp','user_id','live_id'], kind='mergesort')
    rooms = pd.read_pickle(a.prepared_dir/'rooms.pkl')
    t1 = int(events.timestamp.quantile(a.train_q, interpolation='nearest'))
    t2 = int(events.timestamp.quantile(a.dev_q, interpolation='nearest'))
    early = events[events.timestamp <= t1].copy()
    devw = events[(events.timestamp > t1) & (events.timestamp <= t2)].copy()
    testw = events[events.timestamp > t2].copy()

    early_ct = early.groupby('user_id').size()
    eligible = set(early_ct[early_ct >= a.min_train_events].index.astype(int))
    eligible &= set(devw.user_id.astype(int)); eligible &= set(testw.user_id.astype(int))
    if not eligible:
        raise RuntimeError('No eligible users')

    train = early[early.user_id.isin(eligible)].copy()
    dev = devw[devw.user_id.isin(eligible)].copy()
    test = testw[testw.user_id.isin(eligible)].copy()
    # Avoid ambiguous SeqReader merge keys in the parallel streamer view.
    cleaned=[]; dup={}
    for name,x in [('train',train),('dev',dev),('test',test)]:
        before=len(x)
        x=(x.sort_values(['user_id','timestamp','live_id'], kind='mergesort')
             .drop_duplicates(['user_id','streamer_id','timestamp'], keep='last').copy())
        dup[name]=before-len(x); cleaned.append(x)
    train,dev,test=cleaned
    common=sorted(set(train.user_id.astype(int)) & set(dev.user_id.astype(int)) & set(test.user_id.astype(int)))
    train=train[train.user_id.isin(common)].copy(); dev=dev[dev.user_id.isin(common)].copy(); test=test[test.user_id.isin(common)].copy()

    # Generate once at max_n, then truncate to a single legal fixed count shared by dev/test.
    dcs=_active_room_candidates(dev, rooms, a.max_n_neg, a.seed)
    tcs=_active_room_candidates(test, rooms, a.max_n_neg, a.seed)
    dmin=min(len(v)-1 for v in dcs.values()); tmin=min(len(v)-1 for v in tcs.values())
    fixed_n=int(min(a.max_n_neg,dmin,tmin))
    if fixed_n < 100:
        raise RuntimeError(f'Too few active negatives: {fixed_n}')

    uidmap={u:i+1 for i,u in enumerate(common)}
    rr=rooms[['live_id','streamer_id']].dropna().drop_duplicates('live_id').copy()
    rr[['live_id','streamer_id']]=rr[['live_id','streamer_id']].astype('int64')
    live2streamer=dict(zip(rr.live_id.astype(int), rr.streamer_id.astype(int)))

    pos_rooms=set(pd.concat([train.live_id,dev.live_id,test.live_id]).astype(int))
    all_rooms=set(rr.live_id.astype(int)); room_order=sorted(all_rooms-pos_rooms)+sorted(pos_rooms)
    rmap={x:i+1 for i,x in enumerate(room_order)}
    pos_streamers=set(pd.concat([train.streamer_id,dev.streamer_id,test.streamer_id]).astype(int))
    all_streamers=set(rr.streamer_id.astype(int)); st_order=sorted(all_streamers-pos_streamers)+sorted(pos_streamers)
    smap={x:i+1 for i,x in enumerate(st_order)}

    def base(df, kind):
        item = df.live_id.astype(int).map(rmap) if kind=='room' else df.streamer_id.astype(int).map(smap)
        return pd.DataFrame({'user_id':df.user_id.astype(int).map(uidmap),'item_id':item.astype(int),'time':df.timestamp.astype('int64')})

    room_train=base(train,'room'); room_dev=base(dev,'room'); room_test=base(test,'room')
    st_train=base(train,'streamer'); st_dev=base(dev,'streamer'); st_test=base(test,'streamer')

    def add_negs(src, dst_room, dst_st, csets):
        rneg=[]; sneg=[]
        for idx,r in src.iterrows():
            vals=[int(x) for x in csets[idx][1:fixed_n+1]]
            if len(vals)!=fixed_n: raise ValueError('ragged candidates')
            rneg.append(str([rmap[x] for x in vals]))
            sneg.append(str([smap[live2streamer[x]] for x in vals]))
        dst_room['neg_items']=rneg; dst_st['neg_items']=sneg
    add_negs(dev,room_dev,st_dev,dcs); add_negs(test,room_test,st_test,tcs)

    room_out=a.out_root/a.room_dataset; st_out=a.out_root/a.streamer_dataset
    room_out.mkdir(parents=True,exist_ok=True); st_out.mkdir(parents=True,exist_ok=True)
    for name,df in [('train',room_train),('dev',room_dev),('test',room_test)]: df.to_csv(room_out/f'{name}.csv',sep='\t',index=False)
    for name,df in [('train',st_train),('dev',st_dev),('test',st_test)]: df.to_csv(st_out/f'{name}.csv',sep='\t',index=False)
    pd.DataFrame({'item_id':[rmap[x] for x in room_order],'live_id':room_order,'streamer_id':[live2streamer[x] for x in room_order]}).to_csv(room_out/'room_item_map.tsv',sep='\t',index=False)
    pd.DataFrame({'item_id':[smap[x] for x in st_order],'streamer_id':st_order}).to_csv(st_out/'streamer_item_map.tsv',sep='\t',index=False)

    def manifest(src, mapped):
        z=pd.DataFrame({'row_id':np.arange(len(src),dtype=int),'user_id':mapped.user_id.astype(int).to_numpy(),
                        'orig_user_id':src.user_id.astype(int).to_numpy(),'live_id':src.live_id.astype(int).to_numpy(),
                        'streamer_id':src.streamer_id.astype(int).to_numpy(),'time':src.timestamp.astype('int64').to_numpy()})
        z['is_last']=z.groupby('user_id').cumcount(ascending=False).eq(0)
        return z
    manifest(dev.reset_index(drop=True),room_dev).to_csv(room_out/'dev_manifest.csv',index=False)
    manifest(test.reset_index(drop=True),room_test).to_csv(room_out/'test_manifest.csv',index=False)

    meta={'protocol':'global_temporal_dual_successive','train_q':a.train_q,'dev_q':a.dev_q,
          'train_cut_timestamp':t1,'dev_cut_timestamp':t2,
          'train_cut_utc':str(pd.to_datetime(t1,unit='ms',utc=True)),'dev_cut_utc':str(pd.to_datetime(t2,unit='ms',utc=True)),
          'users':len(common),'train_rows':len(train),'dev_rows':len(dev),'test_rows':len(test),
          'dev_last_rows':int(len(common)),'test_last_rows':int(len(common)),'n_neg':fixed_n,'candidate_count':fixed_n+1,
          'target_rules':['last event per user in window','successive all events in chronological window order'],
          'history_rule':'ReChorus SeqReader chronological positions allow each successive target to see only prior train/dev/test events; no future event is in the sliced history.',
          'duplicates_dropped':dup,'seed':a.seed}
    (room_out/'export_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
    (st_out/'export_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta,indent=2))

if __name__=='__main__': main()
