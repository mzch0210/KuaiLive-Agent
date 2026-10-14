#!/usr/bin/env python3
"""Audit aggregate residual source cohort counts without computing any ranking metrics."""
import argparse, hashlib, json, time
from pathlib import Path
import duckdb

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for x in iter(lambda:f.read(8388608),b""):h.update(x)
    return h.hexdigest()

def q(path):
    return "'"+str(path).replace("'","''")+"'"

def main(root,out):
    if out.exists():raise FileExistsError(str(out))
    meta=json.loads((root/"manifest.json").read_text())
    if meta.get("schema")!="kbs-plan-c-g1-derived-v1" or meta.get("source_revision")!="138d213a23e261ed3094d27ed8a4b867fb9143fe":
        raise RuntimeError("source identity")
    names=("causal_stream_sealed.parquet","test_cohort_sealed.parquet","train_known_authors.parquet")
    for name in names:
        if digest(root/name)!=meta["generated_files_sha256"][name]:
            raise RuntimeError("file identity "+name)
    db=duckdb.connect()
    db.execute("SET threads=4")
    db.execute("SET memory_limit='12GB'")
    db.execute("CREATE VIEW hist AS SELECT source_event_id,user_id,author_id,observed_at,prior_events FROM read_parquet("+q(root/"causal_stream_sealed.parquet")+") WHERE split='TEST'")
    db.execute("CREATE VIEW warm AS SELECT author_id FROM read_parquet("+q(root/"train_known_authors.parquet")+")")
    db.execute("CREATE VIEW old AS SELECT source_event_id,user_id FROM read_parquet("+q(root/"test_cohort_sealed.parquet")+")")
    db.execute("""CREATE TEMP TABLE pool AS SELECT h.source_event_id,h.user_id,h.observed_at,h.prior_events
         FROM hist h JOIN warm w USING(author_id)
         WHERE h.prior_events>=2 AND NOT EXISTS(SELECT 1 FROM old o WHERE o.source_event_id=h.source_event_id)""")
    all_test=db.execute("SELECT COUNT(*) FROM hist").fetchone()[0]
    old_n=db.execute("SELECT COUNT(*) FROM old").fetchone()[0]
    pool_n=db.execute("SELECT COUNT(*) FROM pool").fetchone()[0]
    users=db.execute("SELECT COUNT(DISTINCT user_id) FROM pool").fetchone()[0]
    overlaps=db.execute("SELECT COUNT(*) FROM pool p JOIN old o USING(source_event_id)").fetchone()[0]
    disjoint=db.execute("SELECT COUNT(*),COUNT(DISTINCT p.user_id) FROM pool p WHERE NOT EXISTS(SELECT 1 FROM old o WHERE o.user_id=p.user_id)").fetchone()
    days=[{"date":str(d),"events":n,"users":u} for d,n,u in db.execute(
        "SELECT CAST(observed_at AS DATE),COUNT(*),COUNT(DISTINCT user_id) FROM pool GROUP BY 1 ORDER BY 1").fetchall()]
    if all_test!=5124893 or old_n!=47575 or overlaps:
        raise RuntimeError("source or exclusion mismatch")
    summary={"schema":"route-b-b4a-a0-v1","technical_status":"PASS" if pool_n>=30000 and users>=3000 else "HOLD",
        "source_sha256_verified":True,"test_eligible_source":all_test,"g5_excluded":old_n,
        "residual_warm_history_eligible_events":pool_n,"residual_users":users,
        "G5_event_overlap":overlaps,"G5_user_disjoint_events":disjoint[0],
        "G5_user_disjoint_users":disjoint[1],"days":days,
        "unseen_future_time_period":False,"new_target_sample_frozen":False,
        "target_ranking_metrics_computed":False,"data_license_confirmed":False}
    out.mkdir(parents=True,mode=0o700)
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary),flush=True)
    db.close()

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--g1",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    x=a.parse_args()
    main(x.g1,x.out)
