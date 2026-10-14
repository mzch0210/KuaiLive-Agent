#!/usr/bin/env python3
"""B4-A A2: prespecified natural-population poststratification from pretarget metadata.

The frozen A1 outcomes are NEVER read; only A1 summary stratum counts are used.
"""
from pathlib import Path
import argparse,hashlib,json
import duckdb

SHA_MAIN="be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
SHA_SUB="40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059"

def q(v):return "'"+str(v).replace("'","''")+"'"

def main(root,a1,out):
    if out.exists():raise FileExistsError("A2 weights already frozen")
    m=json.loads((a1/"summary.json").read_text())
    if not(m["schema"]=="kbs-n9-route-b-b4a-a1-blind-freeze-v1"
           and m["main_private_SHA256"]==SHA_MAIN
           and m["mechanism_private_SHA256"]==SHA_SUB
           and m["target_ranking_scores_read"] is False
           and m["target_author_labels_in_frozen_files"] is False
           and m["main_events"]==30000 and m["mechanism_events"]==4096):
        raise RuntimeError("A1 manifest source invalid")
    db=duckdb.connect()
    db.execute("SET threads=4")
    db.execute("SET memory_limit='12GB'")
    db.execute("CREATE VIEW old AS SELECT source_event_id FROM read_parquet("+q(root/"test_cohort_sealed.parquet")+")")
    db.execute("CREATE VIEW warm AS SELECT author_id FROM read_parquet("+q(root/"train_known_authors.parquet")+")")
    db.execute("CREATE VIEW test AS SELECT source_event_id,author_id,observed_at,prior_events FROM read_parquet("+q(root/"causal_stream_sealed.parquet")+") WHERE split='TEST'")
    db.execute("""CREATE TEMP VIEW eligible AS SELECT t.source_event_id,
             CAST(t.observed_at AS DATE) AS day,t.prior_events
             FROM test t JOIN warm w USING(author_id)
             WHERE t.prior_events>=2 AND NOT EXISTS (
                SELECT 1 FROM old o WHERE o.source_event_id=t.source_event_id)""")
    db.execute("""CREATE TEMP TABLE basecells AS SELECT day,
             'q'||CAST(NTILE(4) OVER(
                PARTITION BY day ORDER BY prior_events,source_event_id) AS VARCHAR) AS history_group
             FROM eligible""")
    pop={(str(d),g):int(n) for d,g,n in db.execute(
         "SELECT day,history_group,count(*) FROM basecells GROUP BY 1,2").fetchall()}
    if len(pop)!=20 or sum(pop.values())!=4723652:
        raise RuntimeError("Population cell count source integrity failed")
    obs={}
    for key,counts,tot in [("main",m["main_strata"],30000),
                           ("mechanism",m["mechanism_strata"],4096)]:
        x={(v["date"],v["history_group"]):int(v["events"]) for v in counts}
        if set(x)!=set(pop) or sum(x.values())!=tot or any(n<=0 for n in x.values()):
            raise RuntimeError("A1 20-cell sample proportions invalid")
        w={k:pop[k]/x[k] for k in sorted(pop)}
        neff=sum(pop.values())**2/sum(x[k]*w[k]**2 for k in pop)
        obs[key]={"N":tot,"N_effective_kish_for_population_weights":neff,
                  "min_weight":min(w.values()),"max_weight":max(w.values()),
                  "strata":[{"date":k[0],"history_q":k[1],
                             "population_n":pop[k],"sample_n":x[k],
                             "base_poststratification_weight":w[k]}
                            for k in sorted(pop)]}
    result={"schema":"kbs-n9-b4a-a2-population-weight-freeze-v1",
            "state":"FROZEN_BEFORE_TARGET_OUTCOME_REVEAL",
            "population_total":sum(pop.values()),
            "sample_main_SHA256":SHA_MAIN,"sample_mechanism_SHA256":SHA_SUB,
            "main":obs["main"],"mechanism":obs["mechanism"],
            "estimand":"eligible_population_date_by_history_quartile_ratio_weighted_NDCG",
            "balanced_cell_secondary":True,
            "cluster_bootstrap":"5000 paired users, weighted ratio per draw",
            "all_B4A_target_labels_read":False,
            "new_test_ranking_scores_computed":False,
            "raw_event_or_author_ids_public":False}
    out.mkdir(parents=True,mode=0o700)
    (out/"summary.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True),flush=True)
    db.close()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--g1",type=Path,required=True)
    p.add_argument("--a1",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    main(a.g1,a.a1,a.out)
