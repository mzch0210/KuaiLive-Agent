#!/usr/bin/env python3
"""B0 only: inspect fixed M3 DEV sources and availability; no model training/TEST reads."""
import argparse
import csv
import hashlib
import json
from pathlib import Path


EXPECTED = {
    "G1": "klm3_plan_c_g1_v1",
    "TRAIN_INDEX": "klm3_g2_train_index_v1",
    "DEV_SCREEN": "klm3_g2_dev_checkpoint_screen_v1",
    "DEV_CORRECTED_PAIRS": "klm3_g3_dev_fullactive_base_memory_corrected_v1",
    "TRAINED_BASE": "klm3_g2_seed20261012_epoch3_v1",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def get_json(p, expected):
    if not p.is_file():
        raise RuntimeError("missing required DEV manifest")
    x = json.loads(p.read_text())
    if x.get("schema") != expected:
        raise RuntimeError("unexpected DEV manifest schema")
    return x


def check(root, roster_probe=False):
    # Every path below is a hardcoded TRAIN/DEV source; NEVER recurse over root,
    # discover files by a broad glob, inspect any TEST path, or upload row data.
    folder = {k: root / name for k, name in EXPECTED.items()}
    report = {
        "schema": "kbs-b0-candidate-regime-dev-source-gate-v1",
        "evidence_tier": "POST_G5_DEV_ONLY_FEASIBILITY",
        "test_labels_accessed": False,
        "new_training_executed": False,
        "raw_event_or_candidate_ids_exported": False,
        "per_candidate_base_scores_stored_in_canonical_dev_csv": False,
        "full_candidate_scores_require_frozen_base_inference": True,
        "knowledge_memory_requires_corrected_all_prior_history": True,
        "sampled_checkpoint_candidates_are_4096_dev_screen_only": True,
        "sources": {},
        "checkpoints": {},
    }
    mandatory = {
        "G1": ["manifest.json", "dev_cohort.parquet", "causal_stream_sealed.parquet",
               "available_room_intervals.parquet"],
        "TRAIN_INDEX": ["index_manifest.json", "authors.npy", "sequence_ids.npy"],
        "DEV_SCREEN": ["manifest.json", "dev_contexts.npy",
                       "dev_positive_author_tokens.npy",
                       "dev_source_event_ids.npy", "checkpoint_candidate_tokens.npy"],
        "DEV_CORRECTED_PAIRS": ["summary.json", "dev_full_active_pairs.csv"],
    }
    for k, files in mandatory.items():
        missing = [f for f in files if not (folder[k] / f).is_file()]
        report["sources"][k] = {"complete": not bool(missing),
                                 "required_files_checked": len(files),
                                 "missing_file_types": missing}
        if missing:
            raise RuntimeError("Missing required TRAIN/DEV cache files in " + k)

    g1 = get_json(folder["G1"] / "manifest.json", "kbs-plan-c-g1-derived-v1")
    idx = json.loads((folder["TRAIN_INDEX"] / "index_manifest.json").read_text())
    ds = get_json(folder["DEV_SCREEN"] / "manifest.json",
                  "kbs-plan-c-g2-dev-screen-v1")
    paired = get_json(folder["DEV_CORRECTED_PAIRS"] / "summary.json",
                      "kbs-plan-c-full-active-dev-paired-v2")
    if not (g1["protocol_sha256"] == idx["g1_protocol_sha256"]
            == ds["g1_protocol_sha256"]):
        raise RuntimeError("G1/INDEX/DEV provenance mismatch")
    if not (paired.get("scope") == "DEV_ONLY"
            and paired.get("n_scored") == 50049
            and paired.get("all_dev_scored") is True
            and paired.get("memory_corrected_from_all_history") is True
            and paired.get("test_file_accessed") is False):
        raise RuntimeError("Corrected full-active DEV cache not proven clean")
    for fname in ("dev_contexts.npy", "dev_positive_author_tokens.npy",
                  "dev_source_event_ids.npy", "checkpoint_candidate_tokens.npy"):
        wanted = ds["files_sha256"].get(fname)
        if not wanted or sha256(folder["DEV_SCREEN"] / fname) != wanted:
            raise RuntimeError("DEV snapshot digest mismatch")
    csvpath = folder["DEV_CORRECTED_PAIRS"] / "dev_full_active_pairs.csv"
    if sha256(csvpath) != paired["event_csv_sha256"]:
        raise RuntimeError("Corrected DEV paired source digest mismatch")
    report["sources"]["DEV_CORRECTED_PAIRS"]["byte_verified"] = True
    with csvpath.open(newline="") as file:
        rdr = csv.DictReader(file)
        cols = rdr.fieldnames or []
        required = ("event_id", "user_id", "split", "candidate_count",
                    "memory_ndcg10", "sasrec_ndcg10", "gru4rec_ndcg10")
        if any(x not in cols for x in required):
            raise RuntimeError("DEV paired schema incomplete")
        n, min_c, max_c, users = 0, 10**12, 0, set()
        for row in rdr:
            if row["split"] != "DEV":
                raise RuntimeError("non-DEV row in paired file")
            n += 1
            users.add(row["user_id"])  # host-local only
            cc = int(row["candidate_count"])
            min_c, max_c = min(min_c, cc), max(max_c, cc)
        if n != 50049:
            raise RuntimeError("DEV event count mismatch")
    report["corrected_paired"] = {
        "n_dev_events": n, "n_dev_users": len(users),
        "candidate_count_min": min_c, "candidate_count_max": max_c,
        "contains_event_level_features_and_rank_metrics": True,
        "contains_full_candidate_score_vectors": False,
    }

    selected = root / "klm3_g2_checkpoint_dev_selected_v1.json"
    if not selected.is_file():
        raise RuntimeError("DEV-only checkpoint selection registry missing")
    sel = get_json(selected, "kbs-plan-c-g2-checkpoint-selection-dev-only-v1")
    if sel.get("test_data_opened") is not False:
        raise RuntimeError("Invalid DEV checkpoint freeze")
    for family in ("sasrec", "gru4rec"):
        chosen = sel["family_results"][family]["selected"]
        ckpt = folder["TRAINED_BASE"] / family / chosen["checkpoint"]
        if not ckpt.is_file() or sha256(ckpt) != chosen["checkpoint_sha256"]:
            raise RuntimeError("Missing or altered frozen " + family + " Base")
        report["checkpoints"][family] = {
            "frozen_train_weights_present_and_sha_verified": True,
            "seed": 20261012,
            "checkpoint_bytes": ckpt.stat().st_size,
        }

    if roster_probe:
        # Small, deterministic, DEV-only live roster probe. Identities never leave host.
        import numpy as np
        import pyarrow.parquet as pq
        from g3_dev_full_active import author_availability

        index = np.load(folder["TRAIN_INDEX"] / "authors.npy", mmap_mode="r")
        known = {int(author): i + 1 for i, author in enumerate(index)}
        tokens = np.load(folder["DEV_SCREEN"] / "dev_positive_author_tokens.npy",
                         mmap_mode="r")
        times = pq.read_table(folder["G1"] / "dev_cohort.parquet",
                              columns=["observed_at"]).column("observed_at").to_pylist()
        samples = np.unique(np.linspace(0, n-1, 8, dtype=np.int64))
        seen = list(author_availability(
            folder["G1"] / "available_room_intervals.parquet",
            [times[i] for i in samples],
            np.asarray(tokens[samples], dtype=np.int32), known))
        sizes = [len(candidates) for _, candidates, _ in seen]
        if len(sizes) != 8 or min(sizes) <= 575:
            raise RuntimeError("DEV-only full roster reconstruction failed")
        report["availability_reconstruction"] = {
            "status": "PASS", "sampled_dev_time_points": len(sizes),
            "candidate_count_min": min(sizes),
            "candidate_count_max": max(sizes),
            "all_targets_in_active_roster": True,
            "pretarget_time_order": True,
        }
    else:
        report["availability_reconstruction"] = {
            "status": "NOT_EXECUTED", "source_code_available": True,
        }
    report["B0_source_gate"] = "PASS_RECONSTRUCTIBLE_REQUIRES_FROZEN_BASE_RESCORING"
    report["B1_preconditions"] = [
        "Reconstruct full-active and sampled candidates without future outcomes in gate features",
        "Recompute full and sampled ranks from identical frozen Base and corrected Memory",
        "Keep sampled target-retention separate from prospective candidate generation",
        "Use user-disjoint DEV nested validation, no G5 TEST",
        "Evaluate all policies on the same outer full-active DEV events",
    ]
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--roster-probe", action="store_true")
    a = ap.parse_args()
    result = check(a.root, roster_probe=a.roster_probe)
    if a.out.exists():
        raise SystemExit("Refuse to overwrite existing B0 result")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"B0": result["B0_source_gate"],
                      "n_dev": result["corrected_paired"]["n_dev_events"],
                      "roster": result["availability_reconstruction"]["status"],
                      "test_opened": result["test_labels_accessed"]}, sort_keys=True))


if __name__ == "__main__":
    main()
