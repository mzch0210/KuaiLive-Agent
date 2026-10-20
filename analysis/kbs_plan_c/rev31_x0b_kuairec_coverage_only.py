#!/usr/bin/env python3
"""Rev3.1 X0-B: KuaiRec official ZIP *metadata only*; no model/utility labels.

Output contains aggregated counts only; no user IDs, raw rows, scores or
private project data. A verified official ZIP MD5 is a required precondition.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

OFFICIAL_ZIP_MD5 = None  # Must come from verified Zenodo API in workflow
COLUMN_ALLOW = {"user_id", "video_id", "author_id", "upload_dt",
                "timestamp", "date", "time"}
CHUNK = 300_000


def digest_md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def locate(zf, suffix):
    matches = [n for n in zf.namelist()
               if n.lower().endswith(suffix) and not n.startswith("__MACOSX/")]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one " + suffix +
                           " file; found " + repr(matches))
    return matches[0]


def chunks(zf, name, cols):
    with zf.open(name) as f:
        for df in pd.read_csv(f, chunksize=CHUNK, low_memory=False,
                              usecols=lambda x: x in cols):
            missing = cols.difference(df.columns)
            if missing:
                raise ValueError(f"{name} missing mandatory columns {missing}")
            yield df


def analyze_zip(path, expected_md5):
    path = Path(path)
    md5 = digest_md5(path)
    if not expected_md5 or len(expected_md5) != 32:
        raise RuntimeError('Must supply a verified Zenodo MD5 from the official record')
    if md5 != expected_md5.lower():
        raise RuntimeError(f'Official ZIP MD5 mismatch: computed {md5}, expected {expected_md5}')
    with zipfile.ZipFile(path) as z:
        needed = {n: locate(z, n) for n in
                  ("big_matrix.csv", "small_matrix.csv",
                   "item_daily_features.csv")}
        members = sorted(z.namelist())

        # Detect author-id instability across daily metadata revisions.
        author = {}
        uploads = {}
        author_conflicts = set()
        author_missing_rows = 0
        upload_distinct = defaultdict(set)
        daily_rows = 0
        upload_names = []
        for chunk in chunks(z, needed["item_daily_features.csv"],
                            {"video_id", "author_id", "upload_dt"}):
            daily_rows += len(chunk)
            if not upload_names:
                upload_names = list(chunk.columns)
            for video, auth, dt in chunk[["video_id", "author_id", "upload_dt"]].itertuples(index=False, name=None):
                if pd.isna(video):
                    continue
                v = int(video)
                if pd.isna(auth):
                    author_missing_rows += 1
                else:
                    a = int(auth)
                    if v in author and author[v] != a:
                        author_conflicts.add(v)
                    author.setdefault(v, a)
                if pd.notna(dt):
                    text = str(dt).strip()
                    if text:
                        upload_distinct[v].add(text)
                        uploads.setdefault(v, text)
        upload_conflicts = sum(len(v) > 1 for v in upload_distinct.values())

        # Do not inspect watch_ratio / play_duration / relevance labels.
        small_n = 0
        small_timestamp_missing_rows = 0
        small_users = set()
        small_video_ids = set()
        small_first = {}
        small_last = {}
        small_missing_author = 0
        small_missing_upload = 0
        small_video_after_upload = 0
        small_video_before_upload = 0
        same_day_upload = 0
        date_unparseable = 0
        small_events_user = Counter()
        observations = []
        for chunk in chunks(z, needed["small_matrix.csv"],
                            {"user_id", "video_id", "timestamp", "date"}):
            small_n += len(chunk)
            uvals = chunk["user_id"].to_numpy(dtype=np.int64)
            vvals = chunk["video_id"].to_numpy(dtype=np.int64)
            tsvals = pd.to_numeric(chunk["timestamp"], errors="coerce").to_numpy(dtype=float)
            valid_time = np.isfinite(tsvals)
            # Timestamp is optional in some real KuaiRec rows: count missing
            # rather than manufacture temporal ordering. Never use undated
            # observations to establish pre-target histories.
            small_timestamp_missing_rows += int((~valid_time).sum())
            small_users.update(np.unique(uvals).tolist())
            small_video_ids.update(np.unique(vvals).tolist())
            if valid_time.any():
                tmp = pd.DataFrame({"u":uvals[valid_time], "ts":tsvals[valid_time]}).groupby("u")["ts"].agg(["min","max"])
                for u, row in tmp.iterrows():
                    i = int(u)
                    small_first[i] = min(small_first.get(i, float("inf")), float(row["min"]))
                    small_last[i] = max(small_last.get(i, float("-inf")), float(row["max"]))
            small_events_user.update(Counter(uvals.tolist()))
            vids = pd.Series(vvals)
            small_missing_author += int((~vids.isin(author)).sum())
            small_missing_upload += int((~vids.isin(uploads)).sum())
            # Day-granularity only; same-day membership is not proven timestamp-valid.
            if "date" in chunk:
                days = pd.to_numeric(chunk["date"], errors="coerce").to_numpy()
                # Upload_date may be "2020-07-05" or "20200705".
                v_upload = vids.map(uploads).astype("string").str.replace(r"[^0-9]", "",regex=True)
                d_up = pd.to_numeric(v_upload.str.slice(0,8),errors="coerce").to_numpy()
                valid = np.isfinite(days) & np.isfinite(d_up)
                small_video_before_upload += int((valid & (days < d_up)).sum())
                same_day_upload += int((valid & (days == d_up)).sum())
                small_video_after_upload += int((valid & (days > d_up)).sum())
                date_unparseable += int((~valid).sum())
            # Pair density/missingness: hashed pairs, no identifiers released.
            observations.append(pd.util.hash_pandas_object(
                chunk[["user_id", "video_id"]], index=False).to_numpy(dtype=np.uint64))
        pair_hashes = np.concatenate(observations)
        observed_pairs = int(len(np.unique(pair_hashes)))
        del pair_hashes, observations
        possible_pairs = len(small_users) * len(small_video_ids)
        small_rows_duplicates = small_n - observed_pairs

        # Build an author/history audit using ONLY big events earlier than
        # each user's first small observation; never use small labels as history.
        big_n = 0
        big_timestamp_missing_rows = 0
        big_users = set()
        big_video_ids = set()
        big_first = float("inf")
        big_last = float("-inf")
        big_missing_author = 0
        valid_pretarget_rows = 0
        before_cutoff_user = Counter()
        pretarget_author_sets = defaultdict(set)
        for chunk in chunks(z, needed["big_matrix.csv"],
                            {"user_id", "video_id", "timestamp"}):
            big_n += len(chunk)
            uvals = chunk["user_id"].to_numpy(dtype=np.int64)
            vvals = chunk["video_id"].to_numpy(dtype=np.int64)
            tsvals = pd.to_numeric(chunk["timestamp"], errors="coerce").to_numpy(dtype=float)
            valid_big_time = np.isfinite(tsvals)
            big_timestamp_missing_rows += int((~valid_big_time).sum())
            big_users.update(np.unique(uvals).tolist())
            big_video_ids.update(np.unique(vvals).tolist())
            if valid_big_time.any():
                big_first = min(big_first, float(tsvals[valid_big_time].min()))
                big_last = max(big_last, float(tsvals[valid_big_time].max()))
            big_missing_author += int((~pd.Series(vvals).isin(author)).sum())
            cutoffs = pd.Series(uvals).map(small_first).to_numpy(dtype=float)
            mask = valid_big_time & np.isfinite(cutoffs) & (tsvals < cutoffs)
            valid_pretarget_rows += int(mask.sum())
            if mask.any():
                for u, v in zip(uvals[mask].tolist(), vvals[mask].tolist()):
                    if v in author:
                        before_cutoff_user[int(u)] += 1
                        pretarget_author_sets[int(u)].add(author[v])
        overlap = small_users & big_users
        eligible = lambda threshold: sum(
            len(pretarget_author_sets.get(u, set())) >= threshold for u in small_users)
        repeat_history = sum(
            before_cutoff_user[u] > len(pretarget_author_sets.get(u, ()))
            for u in small_users)
        output = {
            "scope": "OFFICIAL_KUAIREC_ZIP_METADATA_ONLY_NO_LABELS_OR_MODEL_RESULTS",
            "source": "https://zenodo.org/records/18164998/files/KuaiRec.zip",
            "file_version": "2026-01-06 Zenodo record 18164998",
            "verified_zip_md5": md5,
            "zip_member_count": len(members),
            "located_member_paths": needed,
            "daily_features": {
                "rows": daily_rows, "mapped_videos": len(author),
                "author_conflicting_video_count": len(author_conflicts),
                "author_missing_rows": author_missing_rows,
                "upload_dt_distinct_for_one_video_multiple": upload_conflicts,
                "video_upload_dt_available": len(uploads),
            },
            "small": {
                "rows": small_n, "users": len(small_users), "videos": len(small_video_ids),
                "unique_user_video_pairs": observed_pairs,
                "duplicate_user_video_rows": small_rows_duplicates,
                "pair_density": observed_pairs / possible_pairs,
                "earliest_unix_ts": min(small_first.values(), default=None),
                "latest_unix_ts": max(small_last.values(), default=None),
                "missing_or_invalid_timestamp_rows": small_timestamp_missing_rows,
                "users_with_a_valid_timestamp": len(small_first),
                "users_without_any_valid_timestamp": len(small_users - set(small_first)),
                "rows_without_author_metadata": small_missing_author,
                "rows_without_upload_metadata": small_missing_upload,
                "row_date_before_upload_date": small_video_before_upload,
                "row_date_equal_upload_date_ambiguous": same_day_upload,
                "row_date_after_upload_date": small_video_after_upload,
                "row_date_or_upload_unparseable": date_unparseable,
                "per_user_row_min": min(small_events_user.values()),
                "per_user_row_max": max(small_events_user.values()),
            },
            "big": {
                "rows": big_n, "users": len(big_users), "videos": len(big_video_ids),
                "earliest_unix_ts": big_first if np.isfinite(big_first) else None,
                "latest_unix_ts": big_last if np.isfinite(big_last) else None,
                "missing_or_invalid_timestamp_rows": big_timestamp_missing_rows,
                "rows_without_author_metadata": big_missing_author,
                "small_users_in_big": len(overlap),
                "small_users_with_any_pre_first_small_big_author_history": eligible(1),
                "small_users_with_5_distinct_pre_first_small_authors": eligible(5),
                "small_users_with_10_distinct_pre_first_small_authors": eligible(10),
                "small_users_with_20_distinct_pre_first_small_authors": eligible(20),
                "small_users_with_pre_first_small_author_repeat": repeat_history,
                "pre_first_small_big_rows_matching_a_known_author": valid_pretarget_rows,
                "historical_condition": "big.timestamp < earliest VALID small.timestamp; users with no dated small observations excluded from time-based history checks; historical upload/exposure validity still unproven"
            },
            "method_warnings": [
                "Nearly complete small_matrix is repeated logged feedback, not a simultaneous choice set.",
                "Metadata timestamp and upload date timezone/time resolution are not yet proven comparable.",
                "Undated small/big rows are excluded from chronology, but retained in total row counts; missingness can cause severe selection bias.",
                "Daily aggregate features forbidden as pretarget Z unless lagged with defensible availability.",
                "Only known metadata columns read: NO watch_ratio or other relevance labels, NO model scoring.",
                "Full label/policy work X1/X2 remains blocked pending human licenses, temporal compatibility and novelty."
            ]
        }
        return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--expected-md5",required=True,help="Zenodo record-API checksum after source verification")
    args = parser.parse_args()
    result = analyze_zip(args.zip,args.expected_md5)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(result,indent=2),encoding="utf-8")
    print("AUDIT_SUMMARY",json.dumps(result,ensure_ascii=False))
if __name__ == "__main__":
    main()
