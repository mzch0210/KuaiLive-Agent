#!/usr/bin/env python3
"""Plan C G1: freeze forward-time, author-level M3 event bundles.

Never fit a ranking model or compute TEST NDCG. All raw/derived per-event rows
stay on the User-host. This stage must be rerunnable from pinned source bytes.
"""
import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path

import duckdb


def quoted(x):
    return "'" + str(x).replace("'", "''") + "'"


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prepare(source, protocol_path, destination, synthetic=False):
    spec = json.loads(protocol_path.read_text())
    if spec["status"] != "SCIENTIFIC_DESIGN_PREREGISTERED_TEST_REMAINS_LOCKED":
        raise ValueError("Pretest protocol not locked")
    for name, expected in spec["source"]["inputs"].items():
        file = source / name
        if not file.is_file() or (not synthetic and sha(file) != expected):
            raise ValueError("M3 raw source unavailable or SHA256 mismatch: " + name)
    if destination.exists():
        raise FileExistsError("Existing G1 output never overwritten: " + str(destination))
    stage = destination.with_name(destination.name + ".incomplete")
    if stage.exists():
        raise FileExistsError("Inspect interrupted G1 stage before retry: " + str(stage))
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage.mkdir(mode=0o700)
    (stage / "spill").mkdir()
    start = time.monotonic()
    db = duckdb.connect(str(stage / "build.duckdb"))
    try:
        db.execute("SET preserve_insertion_order=true")
        db.execute("SET threads=1")  # stable sequential CSV identity on fixed source
        db.execute("SET memory_limit='12GB'")
        db.execute("SET temp_directory=" + quoted(stage / "spill"))
        meta = quoted(source / "live_room_meta.parquet")
        events = quoted(source / "live_interaction.csv")
        db.execute(f"""
        CREATE TABLE rooms AS SELECT CAST(live_id AS BIGINT) AS live_id,
          CAST(author_id AS BIGINT) AS author_id,
          CAST(start_timestamp AS TIMESTAMP) AS open_ts,
          CAST(end_timestamp AS TIMESTAMP) AS close_ts
        FROM read_parquet({meta})
        WHERE live_id IS NOT NULL AND author_id IS NOT NULL
          AND start_timestamp IS NOT NULL AND end_timestamp IS NOT NULL
          AND end_timestamp > start_timestamp
        QUALIFY ROW_NUMBER() OVER
          (PARTITION BY live_id ORDER BY start_timestamp,end_timestamp,author_id)=1
        """)
        print("G1 validated rooms:", db.sql("SELECT COUNT(*) FROM rooms").fetchone()[0], flush=True)
        db.execute(f"""
        CREATE TABLE eligible AS
        WITH observed AS (
          SELECT ROW_NUMBER() OVER () AS source_event_id,
             TRY_CAST(user_id AS BIGINT) AS user_id,
             TRY_CAST(author_id AS BIGINT) AS author_id,
             TRY_CAST(live_id AS BIGINT) AS live_id,
             TRY_CAST(live_play_start_timestamp AS TIMESTAMP) AS observed_at
          FROM read_csv({events}, all_varchar=true, header=true)
        )
        SELECT e.source_event_id,e.user_id,e.author_id,e.live_id,e.observed_at
        FROM observed e INNER JOIN rooms r
          ON e.live_id=r.live_id AND e.author_id=r.author_id
        WHERE e.user_id IS NOT NULL AND e.observed_at IS NOT NULL
          AND r.open_ts <= e.observed_at AND e.observed_at < r.close_ts
        """)
        print("G1 eligible interactions:",
              db.sql("SELECT COUNT(*) FROM eligible").fetchone()[0], flush=True)
        dev = quoted(spec["split"]["dev_start"])
        test = quoted(spec["split"]["test_start"])
        if spec["split"]["dev_start"] >= spec["split"]["test_start"]:
            raise ValueError("Nonmonotonic global split boundary")
        db.execute("SET threads=4")
        db.execute(f"""
        CREATE TABLE chronological AS SELECT *,
          ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY observed_at,source_event_id)-1
               AS prior_events,
          CASE WHEN observed_at < CAST({dev} AS TIMESTAMP) THEN 'TRAIN'
               WHEN observed_at < CAST({test} AS TIMESTAMP) THEN 'DEV'
               ELSE 'TEST' END AS split
        FROM eligible
        """)
        split_counts = dict(db.sql("SELECT split,COUNT(*) FROM chronological GROUP BY split").fetchall())
        db.execute("CREATE TABLE known_authors AS SELECT DISTINCT author_id FROM chronological WHERE split='TRAIN'")
        seed=int(spec["cohort"]["seed"])
        mod_dev=int(spec["cohort"]["dev_keep_if_mod_less_than"])
        mod_test=int(spec["cohort"]["test_keep_if_mod_less_than"])
        min_hist=int(spec["unit"]["min_prior_history"])
        if not 0 < mod_dev <= 1000000 or not 0 < mod_test <= 1000000:
            raise ValueError("Sample fraction out of range")
        db.execute(f"""
        CREATE TABLE sampled AS SELECT c.*
        FROM chronological c INNER JOIN known_authors k ON c.author_id=k.author_id
        WHERE c.prior_events >= {min_hist} AND
          ((c.split='DEV' AND hash(c.user_id,c.author_id,c.live_id,c.observed_at,
                                   c.source_event_id,{seed}) % 1000000 < {mod_dev})
          OR
           (c.split='TEST' AND hash(c.user_id,c.author_id,c.live_id,c.observed_at,
                                    c.source_event_id,{seed}) % 1000000 < {mod_test}))
        """)
        sampled_counts = dict(db.sql("SELECT split,COUNT(*) FROM sampled GROUP BY split").fetchall())
        print("G1 chronology counts", split_counts, "selected", sampled_counts, flush=True)
        if not synthetic and (
            min(split_counts.get(s,0) for s in ("TRAIN","DEV","TEST")) < 10000
            or min(sampled_counts.get(s,0) for s in ("DEV","TEST")) < 1000):
            raise ValueError("Unexpectedly small required split or DEV/TEST cohort")
        export = {
            "train_author_events.parquet":
                "SELECT source_event_id,user_id,author_id,live_id,observed_at,prior_events "
                "FROM chronological WHERE split='TRAIN' "
                "ORDER BY user_id,observed_at,source_event_id",
            "causal_stream_sealed.parquet":
                "SELECT source_event_id,user_id,author_id,live_id,observed_at,prior_events,split "
                "FROM chronological ORDER BY user_id,observed_at,source_event_id",
            "dev_cohort.parquet":
                "SELECT source_event_id,user_id,author_id,live_id,observed_at,prior_events "
                "FROM sampled WHERE split='DEV' ORDER BY user_id,observed_at,source_event_id",
            "test_cohort_sealed.parquet":
                "SELECT source_event_id,user_id,author_id,live_id,observed_at,prior_events "
                "FROM sampled WHERE split='TEST' ORDER BY user_id,observed_at,source_event_id",
            "train_known_authors.parquet": "SELECT author_id FROM known_authors ORDER BY author_id",
            "available_room_intervals.parquet":
                "SELECT live_id,author_id,open_ts,close_ts FROM rooms ORDER BY open_ts,live_id"
        }
        fingerprints={}
        for name,sql in export.items():
            print("G1 writing",name,flush=True)
            db.execute(f"COPY ({sql}) TO {quoted(stage/name)} (FORMAT PARQUET,COMPRESSION ZSTD)")
            fingerprints[name]=sha(stage/name)
        summary={
            "schema":"kbs-plan-c-g1-derived-v1",
            "source_sha256":spec["source"]["inputs"],
            "protocol_sha256":sha(protocol_path),
            "source_revision":spec["source"]["revision"],
            "duckdb_version":duckdb.__version__,
            "split_event_counts":split_counts,
            "selected_cohort_counts":sampled_counts,
            "valid_room_count":db.sql("SELECT COUNT(*) FROM rooms").fetchone()[0],
            "known_train_author_count":db.sql("SELECT COUNT(*) FROM known_authors").fetchone()[0],
            "generated_files_sha256":fingerprints,
            "test_outcomes_inspected":False,
            "test_ranking_metrics_computed":False,
            "models_trained":False,
            "full_event_stream_sorted_per_user_by_time":True,
            "elapsed_seconds":round(time.monotonic()-start,1)
        }
        (stage/"manifest.json").write_text(json.dumps(summary,indent=2)+"\n")
        db.close()
        shutil.rmtree(stage/"spill",ignore_errors=True)
        (stage/"build.duckdb").unlink(missing_ok=True)
        (stage/"build.duckdb.wal").unlink(missing_ok=True)
        stage.rename(destination)
        print(json.dumps(summary),flush=True)
        return summary
    except BaseException:
        db.close()
        raise


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,required=True)
    parser.add_argument("--protocol",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--synthetic",action="store_true")
    args=parser.parse_args()
    prepare(args.source,args.protocol,args.output,args.synthetic)
