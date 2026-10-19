#!/usr/bin/env python3
"""V2a: read-only, DEV-scoped verification on original B1 self-hosted runner.

Never opens TEST/target user event values; logs only predeclared file-type
presence, checksum matches, total row counts and safe non-identifying summary.
Never modifies cache, retrains, rescoring, serializes checkpoints, or uploads
private rows, IDs, paths, credentials, or manifests.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

B1_SHA = "37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
F_SHA = "e144d9ed4c155b51a182a58150ea17d797b3eb4ee0dac0475ccba1d34f277e8f"
N_DEV = 50049
SAFE_SCHEMA = "N12_C8V_V2A_SELFHOST_DEV_READONLY_CHECK_v1"

def digest(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(8 << 20), b""):
            h.update(block)
    return h.hexdigest()

def main(root):
    dirs = {
        "g1": root / "klm3_plan_c_g1_v1",
        "index": root / "klm3_g2_train_index_v1",
        "dev": root / "klm3_g2_dev_checkpoint_screen_v1",
        "corrected_f": root / "klm3_g3_dev_fullactive_base_memory_corrected_v1",
        "models": root / "klm3_g2_seed20261012_epoch3_v1",
        "b1": root / "klm3_b1_full_dev_candidate_labels_seed20261012_v1",
    }
    files = {
        "g1_manifest": dirs["g1"] / "manifest.json",
        "index_manifest": dirs["index"] / "index_manifest.json",
        "dev_manifest": dirs["dev"] / "manifest.json",
        "selected_checkpoint_manifest": root / "klm3_g2_checkpoint_dev_selected_v1.json",
        "corrected_f_summary": dirs["corrected_f"] / "summary.json",
        "corrected_f_dev_csv": dirs["corrected_f"] / "dev_full_active_pairs.csv",
        "b1_summary": dirs["b1"] / "summary.json",
        "b1_dev_csv": dirs["b1"] / "dev_pair_candidate_labels.csv",
        "dev_event_snapshot": dirs["dev"] / "dev_source_event_ids.npy",
        "dev_positive_snapshot": dirs["dev"] / "dev_positive_author_tokens.npy",
        "dev_context_snapshot": dirs["dev"] / "dev_contexts.npy",
        "g1_dev_cohort": dirs["g1"] / "dev_cohort.parquet",
        "g1_causal_history": dirs["g1"] / "causal_stream_sealed.parquet",
        "g1_active_intervals": dirs["g1"] / "available_room_intervals.parquet",
        "training_known_authors": dirs["index"] / "authors.npy",
        "training_sequence_ids": dirs["index"] / "sequence_ids.npy",
    }
    checks = {name: p.is_file() and not p.is_symlink() for name, p in files.items()}
    report = {
        "schema": SAFE_SCHEMA,
        "scope": "DEV_FILES_ONLY_NO_TEST_PATHS",
        "read_only": True,
        "trained_or_scored_new_models": False,
        "event_level_export": False,
        "expected_dev_events": N_DEV,
        "file_present": checks,
        "published_b1_sha_match": False,
        "published_f_sha_match": False,
        "b1_manifest_accepted": False,
        "corrected_f_manifest_accepted": False,
        "provenance_manifests_chain_match": False,
        "dev_snapshot_hashes_match": False,
        "frozen_checkpoint_hashes_match": False,
        "b1_csv_rows_equal_50049": False,
        "b1_scalar_label_columns_present": False,
        "sampled_rank_and_vector_columns_persisted": False,
        "full_candidate_min": None,
        "full_candidate_max": None,
    }
    if checks["corrected_f_dev_csv"]:
        report["published_f_sha_match"] = digest(files["corrected_f_dev_csv"]) == F_SHA
    if checks["b1_dev_csv"]:
        report["published_b1_sha_match"] = digest(files["b1_dev_csv"]) == B1_SHA
        with files["b1_dev_csv"].open("r", newline="", encoding="utf-8") as f:
            rdr = csv.reader(f)
            header = next(rdr, [])
            wanted = {
                "sampled_memory_ndcg10",
                "sampled_sasrec_ndcg10",
                "sampled_gru4rec_ndcg10",
                "b1_sampled_candidate_count",
            }
            report["b1_scalar_label_columns_present"] = wanted.issubset(set(header))
            report["sampled_rank_and_vector_columns_persisted"] = any(
                k in set(header) for k in (
                    "sampled_sasrec_rank", "sampled_gru4rec_rank",
                    "sampled_memory_rank", "sampled_candidate_scores",
                    "sampled_candidate_ids",
                )
            )
            report["b1_csv_rows_equal_50049"] = sum(1 for _ in rdr) == N_DEV
    b1 = fsum = gm = im = dm = sel = None
    if checks["b1_summary"]:
        b1 = json.loads(files["b1_summary"].read_text())
        report["b1_manifest_accepted"] = (
            b1.get("schema") == "kbs-b1-full-dev-paired-candidate-labels-v1"
            and b1.get("status") == "PASS"
            and b1.get("scope") == "DEV_ONLY_POST_G5_EXPLORATORY"
            and b1.get("test_accessed") is False
            and b1.get("model_training") is False
            and b1.get("event_level_uploaded") is False
            and b1.get("n_dev_events") == N_DEV
            and b1.get("sampled_candidate_count") == 575
            and b1.get("private_event_source_csv_sha256") == B1_SHA
            and b1.get("corrected_F_source_sha256") == F_SHA
        )
        report["full_candidate_min"] = b1.get("full_candidate_count_min")
        report["full_candidate_max"] = b1.get("full_candidate_count_max")
    if checks["corrected_f_summary"]:
        fsum = json.loads(files["corrected_f_summary"].read_text())
        report["corrected_f_manifest_accepted"] = (
            fsum.get("schema") == "kbs-plan-c-full-active-dev-paired-v2"
            and fsum.get("scope") == "DEV_ONLY"
            and fsum.get("test_file_accessed") is False
            and fsum.get("memory_corrected_from_all_history") is True
            and fsum.get("n_scored") == N_DEV
            and fsum.get("event_csv_sha256") == F_SHA
        )
    for v,key in (
        ("g1_manifest", "gm"),
        ("index_manifest", "im"),
        ("dev_manifest", "dm"),
        ("selected_checkpoint_manifest", "sel"),
    ):
        if checks[v]:
            val = json.loads(files[v].read_text())
            if key == "gm": gm = val
            elif key == "im": im = val
            elif key == "dm": dm = val
            else: sel = val
    if gm is not None and im is not None and dm is not None and sel is not None:
        report["provenance_manifests_chain_match"] = (
            gm.get("protocol_sha256") == im.get("g1_protocol_sha256")
            == dm.get("g1_protocol_sha256")
            and isinstance(gm.get("protocol_sha256"), str)
            and sel.get("test_data_opened") is False
        )
        dev_files = ("dev_source_event_ids.npy", "dev_positive_author_tokens.npy", "dev_contexts.npy")
        if all(checks[k] for k in ("dev_event_snapshot", "dev_positive_snapshot", "dev_context_snapshot")):
            saved = dm.get("files_sha256", {})
            report["dev_snapshot_hashes_match"] = all(
                isinstance(saved.get(name), str)
                and digest(dirs["dev"] / name) == saved[name] for name in dev_files
            )
        family_results = sel.get("family_results", {})
        ck_checks = []
        for family in ("sasrec", "gru4rec"):
            fm = family_results.get(family, {}).get("selected", {})
            rel = fm.get("checkpoint")
            sha = fm.get("checkpoint_sha256")
            if not isinstance(rel, str) or not isinstance(sha, str):
                ck_checks.append(False)
                continue
            path_obj = Path(rel)
            if path_obj.is_absolute() or ".." in path_obj.parts:
                ck_checks.append(False)
                continue
            ck = dirs["models"] / family / path_obj
            ck_checks.append(ck.is_file() and not ck.is_symlink() and digest(ck) == sha)
        report["frozen_checkpoint_hashes_match"] = len(ck_checks) == 2 and all(ck_checks)
    core = (
        "g1_manifest", "index_manifest", "dev_manifest",
        "selected_checkpoint_manifest", "corrected_f_summary",
        "corrected_f_dev_csv", "b1_summary", "b1_dev_csv",
        "dev_event_snapshot", "dev_positive_snapshot", "dev_context_snapshot",
        "g1_dev_cohort", "g1_causal_history", "g1_active_intervals",
        "training_known_authors", "training_sequence_ids",
    )
    good = (
        all(checks[k] for k in core)
        and all(report[k] is True for k in (
            "published_b1_sha_match", "published_f_sha_match",
            "b1_manifest_accepted", "corrected_f_manifest_accepted",
            "provenance_manifests_chain_match", "dev_snapshot_hashes_match",
            "frozen_checkpoint_hashes_match", "b1_csv_rows_equal_50049",
            "b1_scalar_label_columns_present",
        ))
    )
    report["status"] = (
        "DEV_SOURCE_PRESENT_AND_ORIGINAL_SHA_MATCHED"
        if good else "HOLD_DEV_SOURCE_MISSING_OR_UNVERIFIED"
    )
    report["v2b_authorized"] = False
    report["corrected_s_estimator_validated"] = False
    return report

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--root", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    opts = a.parse_args()
    result = main(opts.root)
    opts.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    # Print only schema/status/check booleans; no private paths or manifests.
    print(json.dumps(result, sort_keys=True))
