#!/usr/bin/env python3
"""B4-A A1: technical sample seal. No current-target author is exported or scored."""
import argparse, hashlib, json, time
from pathlib import Path
import duckdb

SEED = "20261014"
EXPECTED_POOL = 4723652
EXPECTED_USERS = 21565

def hashfile(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(8388608),b""):h.update(c)
    return h.hexdigest()

def q(p):
    return "'"+str(p).replace("'","''")+"'"

def main(root,a0,out):
    if out.exists():raise FileExistsError("Do not overwrite B4-A A1")
    audit=json.loads((a0/"summary.json").read_text())
    if not(audit["schema"]=="route-b-b4a-a0-v1"
           and audit["technical_status"]=="PASS"
           and audit["source_sha256_verified"] is True
           and audit["residual_warm_history_eligible_events"]==EXPECTED_POOL
           and audit["residual_users"]==EXPECTED_USERS):
        raise RuntimeError("A0 identity eligibility failed")
    manifest=json.loads((root/"manifest.json").read_text())
    for f in ("causal_stream_sealed.parquet","test_cohort_sealed.parquet","train_known_authors.parquet"):
        if hashfile(root/f)!=manifest["generated_files_sha256"][f]:
            raise RuntimeError("G1 input hash mismatch "+f)
    db=duckdb.connect()
    db.execute("SET threads=4")
    db.execute("SET memory_limit='12GB'")
    db.execute("CREATE VIEW old AS SELECT source_event_id FROM read_parquet("+q(root/"test_cohort_sealed.parquet")+")")
    db.execute("CREATE VIEW warm AS SELECT author_id FROM read_parquet("+q(root/"train_known_authors.parquet")+")")
    db.execute("CREATE VIEW test AS SELECT source_event_id,user_id,author_id,observed_at,prior_events FROM read_parquet("+q(root/"causal_stream_sealed.parquet")+") WHERE split='TEST'")
    db.execute("""
      CREATE TEMP TABLE pool AS
      SELECT base.*,
        'q' || CAST(NTILE(4) OVER (
          PARTITION BY day ORDER BY prior_events,source_event_id
        ) AS VARCHAR) AS history_group
      FROM (
        SELECT t.source_event_id,t.user_id,t.observed_at,t.prior_events,
               CAST(t.observed_at AS DATE) AS day
        FROM test t JOIN warm w USING(author_id)
        WHERE t.prior_events>=2
          AND NOT EXISTS(SELECT 1 FROM old o WHERE o.source_event_id=t.source_event_id)
      ) base
    """)
    counts=db.execute("SELECT day,history_group,count(*) AS n FROM pool GROUP BY 1,2 ORDER BY 1,2").fetchall()
    if db.execute("SELECT COUNT(*) FROM pool").fetchone()[0]!=EXPECTED_POOL:
        raise RuntimeError("Pool count changed since A0")
    if len(counts)!=20 or any(n<1500 for _,_,n in counts):
        print(json.dumps({"A1_PREOUTCOME_STRATUM_COUNTS":[{"day":str(d),"group":g,"eligible":n} for d,g,n in counts],"status":"HOLD_NOT_ENOUGH_FOR_EQUAL_QUOTA"}),flush=True)
        raise RuntimeError("Insufficient 5-day by 4 within-day history-activity rank quartiles")
    # Candidate qualification previously checked author, but ranking is determined
    # solely by SOURCE EVENT ID and two frozen public purpose/seed strings.
    db.execute("""
      CREATE TEMP TABLE main AS
      SELECT source_event_id,user_id,observed_at,prior_events,day,history_group
      FROM (
        SELECT *,ROW_NUMBER() OVER(
          PARTITION BY day,history_group
          ORDER BY sha256('B4A-MAIN-V1-20261014:' || CAST(source_event_id AS VARCHAR)),
                   source_event_id) AS selection_rank
        FROM pool
      )
      WHERE selection_rank<=1500
    """)
    n,users=db.execute("SELECT count(*),count(DISTINCT user_id) FROM main").fetchone()
    if n!=30000 or users<3000:raise RuntimeError("Main sample size/user count")
    db.execute("""
      CREATE TEMP TABLE mechanism AS
      SELECT source_event_id,user_id,observed_at,prior_events,day,history_group
      FROM (
         SELECT *,ROW_NUMBER() OVER(
          ORDER BY sha256('B4A-IDENTITY-V1-20261014:'||CAST(source_event_id AS VARCHAR)),
                   source_event_id) AS selection_rank
         FROM main
      ) WHERE selection_rank<=4096
    """)
    m,mu=db.execute("SELECT count(*),count(DISTINCT user_id) FROM mechanism").fetchone()
    overlap=db.execute("SELECT COUNT(*) FROM main m JOIN old o USING(source_event_id)").fetchone()[0]
    if m!=4096 or mu<400 or overlap:
        raise RuntimeError("Mechanism sample or G5 overlap invalid")
    out.mkdir(parents=True,mode=0o700)
    def write(table,filename):
        file=out/filename
        db.execute("COPY (SELECT source_event_id,user_id,observed_at,prior_events,day,history_group FROM "
                   +table+" ORDER BY user_id,observed_at,source_event_id) TO "
                   +q(file)+" (FORMAT PARQUET,COMPRESSION ZSTD)")
        return hashfile(file)
    main_hash=write("main","B4A_MAIN_30000_PRIVATE.parquet")
    mech_hash=write("mechanism","B4A_IDENTITY_4096_PRIVATE.parquet")
    main_days=[{"date":str(d),"history_group":g,"events":int(c)}
        for d,g,c in db.execute("SELECT day,history_group,count(*) FROM main GROUP BY 1,2 ORDER BY 1,2").fetchall()]
    subset_days=[{"date":str(d),"history_group":g,"events":int(c)}
        for d,g,c in db.execute("SELECT day,history_group,count(*) FROM mechanism GROUP BY 1,2 ORDER BY 1,2").fetchall()]
    result={"schema":"kbs-n9-route-b-b4a-a1-blind-freeze-v1",
        "technical_status":"SEALED_SAMPLES_PASS_HUMAN_RIGHTS_AND_MODEL_GATES_PENDING",
        "source_A0_pool_count":EXPECTED_POOL,"main_events":n,"main_users":users,
        "mechanism_events":m,"mechanism_users":mu,
        "strata":"5 source dates x 4 within-day pretarget history rank quartiles",
        "main_per_stratum":1500,"main_strata":main_days,
        "mechanism_strata":subset_days,
        "old_G5_target_id_overlap":overlap,
        "main_private_SHA256":main_hash,"mechanism_private_SHA256":mech_hash,
        "sample_seed":SEED,
        "hash_input_fields":["source_event_id","fixed purpose and seed"],
        "target_author_in_sampling_hash":False,
        "target_author_labels_in_frozen_files":False,
        "target_ranking_scores_read":False,
        "model_predictions_computed":False,
        "no_new_independent_collection_period":True,
        "right_to_publish_derived_private_data":"PENDING_HUMAN_CLEARANCE",
        "A2_A3_A4_authorized":False}
    (out/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result),flush=True)
    db.close()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--g1",type=Path,required=True)
    p.add_argument("--a0",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    x=p.parse_args()
    main(x.g1,x.a0,x.out)
