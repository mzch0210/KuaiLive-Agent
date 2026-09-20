from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .evaluate import split_events


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepared-dir', type=Path, required=True)
    ap.add_argument('--raw-dir', type=Path, required=True)
    ap.add_argument('--base-room-dir', type=Path, required=True)
    ap.add_argument('--out-root', type=Path, required=True)
    ap.add_argument('--dataset', default='KuaiLiveShopRoomExposure')
    ap.add_argument('--k', type=int, default=9)
    ap.add_argument('--lookback-hours', type=float, default=24.0)
    ap.add_argument('--min-users', type=int, default=500)
    args = ap.parse_args()

    events = pd.read_pickle(args.prepared_dir / 'events.pkl')
    rooms = pd.read_pickle(args.prepared_dir / 'rooms.pkl')
    train, dev, test = split_events(events, 3)

    cleaned=[]
    for x in (train,dev,test):
        cleaned.append(x.drop_duplicates(['user_id','live_id','timestamp'], keep='last').copy())
    train,dev,test=cleaned
    common=set(dev.user_id.astype(int)) & set(test.user_id.astype(int))
    train=train[train.user_id.astype(int).isin(common)].copy()
    dev=dev[dev.user_id.astype(int).isin(common)].copy()
    test=test[test.user_id.astype(int).isin(common)].copy()
    users=sorted(common); uidmap={int(u):i+1 for i,u in enumerate(users)}

    base_train=pd.read_csv(args.base_room_dir/'train.csv', sep='\t')
    room_map=pd.read_csv(args.base_room_dir/'room_item_map.tsv', sep='\t')
    room_map[['item_id','live_id','streamer_id']]=room_map[['item_id','live_id','streamer_id']].astype('int64')
    live2item=dict(zip(room_map.live_id.astype(int), room_map.item_id.astype(int)))
    live2streamer=dict(zip(room_map.live_id.astype(int), room_map.streamer_id.astype(int)))

    # Official negative.csv: exposures presented to users but not clicked.
    neg=pd.read_csv(args.raw_dir/'negative.csv', usecols=['user_id','live_id','streamer_id','timestamp'])
    neg=neg[neg.user_id.astype(int).isin(common)].copy()
    neg=neg[neg.live_id.astype(int).isin(live2item)].copy()
    neg[['user_id','live_id','streamer_id','timestamp']]=neg[['user_id','live_id','streamer_id','timestamp']].astype('int64')
    neg.sort_values(['user_id','timestamp'], inplace=True)
    by_user={int(u):g for u,g in neg.groupby('user_id', sort=False)}

    rr=rooms[['live_id','start_timestamp','end_timestamp']].dropna().drop_duplicates('live_id').copy()
    rr[['live_id','start_timestamp','end_timestamp']]=rr[['live_id','start_timestamp','end_timestamp']].astype('int64')
    lifecycle={int(r.live_id):(int(r.start_timestamp),int(r.end_timestamp)) for r in rr.itertuples(index=False)}
    lookback_ms=int(args.lookback_hours*3600*1000)

    def build_pool(targets):
        pools={}; counts=[]
        for r in targets.itertuples(index=False):
            uid=int(r.user_id); target=int(r.live_id); t=int(r.timestamp)
            g=by_user.get(uid)
            vals=[]
            if g is not None:
                # strict: logged non-click exposure precedes target, is recent,
                # and the exposed room is still live at target time.
                z=g[(g.timestamp < t) & (g.timestamp >= t-lookback_ms)]
                seen={target}
                for q in z.iloc[::-1].itertuples(index=False):
                    live=int(q.live_id)
                    if live in seen: continue
                    life=lifecycle.get(live)
                    if life is None or not (life[0] <= t < life[1]): continue
                    vals.append(live); seen.add(live)
            pools[uid]=vals
            counts.append(len(vals))
        return pools, np.asarray(counts,dtype=int)

    dp,dc=build_pool(dev); tp,tc=build_pool(test)
    eligible=[u for u in users if len(dp.get(u,[]))>=args.k and len(tp.get(u,[]))>=args.k]
    elig=set(eligible)
    if len(eligible)<args.min_users:
        # Still write a coverage report before stopping so the protocol failure
        # is auditable instead of silently adding synthetic negatives.
        out=args.out_root/args.dataset; out.mkdir(parents=True,exist_ok=True)
        meta={'dataset':args.dataset,'protocol':'official_negative_strict_active','k':args.k,
              'lookback_hours':args.lookback_hours,'all_users':len(users),'eligible_users':len(eligible),
              'eligible_rate':len(eligible)/max(len(users),1),
              'dev_pool_quantiles':np.quantile(dc,[0,.25,.5,.75,.9,.95,.99,1]).tolist(),
              'test_pool_quantiles':np.quantile(tc,[0,.25,.5,.75,.9,.95,.99,1]).tolist(),
              'coverage_failure':True,'min_users':args.min_users}
        (out/'export_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
        print(json.dumps(meta,indent=2))
        raise SystemExit(2)

    def base_rows(x):
        x=x[x.user_id.astype(int).isin(elig)].copy()
        return pd.DataFrame({'user_id':x.user_id.astype(int).map(uidmap),
                             'item_id':x.live_id.astype(int).map(live2item),
                             'time':x.timestamp.astype('int64')}),x
    dv,dev_raw=base_rows(dev); te,test_raw=base_rows(test)
    def neg_items(x,pools):
        return [str([live2item[v] for v in pools[int(u)][:args.k]]) for u in x.user_id.astype(int)]
    dv['neg_items']=neg_items(dev_raw,dp); te['neg_items']=neg_items(test_raw,tp)

    out=args.out_root/args.dataset; out.mkdir(parents=True,exist_ok=True)
    # Keep full frozen training set; dev/test are the strict exposure-covered cohort.
    base_train.to_csv(out/'train.csv',sep='\t',index=False)
    dv.to_csv(out/'dev.csv',sep='\t',index=False); te.to_csv(out/'test.csv',sep='\t',index=False)
    room_map.to_csv(out/'room_item_map.tsv',sep='\t',index=False)

    # Familiar-streamer density among real exposure negatives: key diagnostic.
    train_hist=train.groupby('user_id').streamer_id.apply(lambda s:set(map(int,s))).to_dict()
    fam=[]
    for r in test_raw.itertuples(index=False):
        hist=train_hist.get(int(r.user_id),set())
        # Fair test history includes dev target as observed before test.
        drow=dev[dev.user_id.astype(int)==int(r.user_id)]
        if len(drow): hist=set(hist)|set(drow.streamer_id.astype(int))
        vals=tp[int(r.user_id)][:args.k]
        fam.append(sum(int(live2streamer[v]) in hist for v in vals))
    fam=np.asarray(fam,dtype=int)

    meta={'dataset':args.dataset,'protocol':'official_negative_strict_active',
          'definition':'negative.csv exposures shown-but-not-clicked; prior 24h (configurable) and still active at target',
          'k':args.k,'candidate_count':args.k+1,'lookback_hours':args.lookback_hours,
          'all_users':len(users),'eligible_users':len(eligible),'eligible_rate':len(eligible)/max(len(users),1),
          'train_rows':int(len(base_train)),'dev_rows':int(len(dv)),'test_rows':int(len(te)),
          'dev_pool_quantiles':np.quantile(dc,[0,.25,.5,.75,.9,.95,.99,1]).tolist(),
          'test_pool_quantiles':np.quantile(tc,[0,.25,.5,.75,.9,.95,.99,1]).tolist(),
          'test_familiar_negative_mean':float(fam.mean()),
          'test_zero_familiar_negative_rate':float((fam==0).mean()),
          'coverage_failure':False}
    (out/'export_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
    pd.DataFrame({'user_id':te.user_id.astype(int),'familiar_negative_count':fam}).to_csv(out/'test_candidate_diagnostics.csv',index=False)
    print(json.dumps(meta,indent=2))

if __name__=='__main__': main()
