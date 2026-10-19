#!/usr/bin/env python3
"""N12 V2a: verify old B1 F ranks AND old B1 sampled DEV labels on fixed requests.

Frozen Base weights only. DEV-only sources, no TRAIN fitting or TEST access.
All event, author, user and per-candidate score vectors stay on private host.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import time

import numpy as np
import torch
import pyarrow.parquet as pq

from g3_dev_full_active import author_availability, load_models, representations
from g3_replay_correct_memory import corrected_memory_score, replay_all_history, rank as memory_rank

SEED = 20261012
SAMPLED = 575
EXPECTED_N = 50049
B1_SOURCE_SHA = '37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea'


def sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def true_rank(candidates, scores, target):
    pos = int(np.searchsorted(candidates, target))
    if pos >= len(candidates) or int(candidates[pos]) != int(target):
        raise ValueError("target not in sorted pre-outcome roster")
    v = float(scores[pos])
    # Exact original G3 Base tie convention (do not mix with Memory epsilon).
    return int(1 + np.count_nonzero((scores > v) | ((scores == v) & (candidates < target))))


def ndcg(rank):
    return float(1.0 / math.log2(rank + 1)) if rank <= 10 else 0.0


def deterministic_sample(full, target, source_event_id):
    # Target-retained sampled metric is OFFLINE supervision, never gate input.
    pool = full[full != target]
    if len(pool) < SAMPLED - 1:
        raise RuntimeError("Insufficient DEV negative candidates")
    rng = np.random.default_rng(SEED + int(source_event_id))
    sampled = rng.choice(pool, size=SAMPLED - 1, replace=False)
    result = np.sort(np.concatenate((sampled, np.array([target], dtype=np.int32))))
    if len(np.unique(result)) != SAMPLED:
        raise RuntimeError("Sampled candidate duplicates")
    return result


@torch.inference_mode()
def dense_scores(representations_by_model, models, selection, device, batch):
    """One GEMM over frozen vocabulary, no per-event GPU launches."""
    result = {}
    for family, model in models.items():
        rep = torch.as_tensor(np.asarray(representations_by_model[family]),
                              dtype=torch.float32, device=device)
        weights = model.item.weight.detach()
        tensors = []
        for start in range(0, len(selection), batch):
            # Fixed all-author output permits one large GEMM instead of
            # dynamic per-event embedding lookup + small kernel launches.
            out = rep[start:start + batch] @ weights.T
            tensors.append(out.cpu().numpy().copy())
        result[family] = np.concatenate(tensors, axis=0)
    return result


@torch.inference_mode()
def gpu_batch_benchmark(model, representations_by_model, device, n_vocab):
    """Warm, synchronized GPU-only kernel throughput; no claim of overall utilization."""
    batch_trials = (12, 32, 64, 128, 256)
    weights = model.item.weight.detach()
    rep = torch.as_tensor(np.asarray(representations_by_model, dtype=np.float32),
                          dtype=torch.float32, device=device)
    rows = []
    for batch in batch_trials:
        if batch > 512:
            continue
        inpt = rep[:min(len(rep), batch)]
        if len(inpt) < batch:
            inpt = inpt.repeat((batch + len(inpt) - 1) // len(inpt), 1)[:batch]
        for _ in range(3):
            _ = inpt @ weights.T
        torch.cuda.synchronize()
        before = torch.cuda.Event(enable_timing=True)
        after = torch.cuda.Event(enable_timing=True)
        before.record()
        for _ in range(24):
            _ = inpt @ weights.T
        after.record()
        torch.cuda.synchronize()
        ms = float(before.elapsed_time(after)) / 24.0
        rows.append({"batch": batch, "gpu_gemm_ms": round(ms, 4),
                     "event_throughput_per_gpu_second": int(batch * 1000 / max(ms, 1e-6))})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=128)
    parser.add_argument("--score-batch", type=int, default=128)
    args = parser.parse_args()
    if not 16 <= args.limit <= 512 or not 16 <= args.score_batch <= 256:
        raise ValueError("Stage-one DEV pilot bounds exceeded")
    if args.out.exists():
        raise FileExistsError("B1 must never overwrite a prior result")
    if not torch.cuda.is_available() or "3090" not in torch.cuda.get_device_name(0):
        raise RuntimeError("B1 controlled GPU pilot requires frozen self-host RTX3090")
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.set_float32_matmul_precision("highest")
    started = time.monotonic()
    root = args.root
    g1 = root / "klm3_plan_c_g1_v1"
    index = root / "klm3_g2_train_index_v1"
    dev = root / "klm3_g2_dev_checkpoint_screen_v1"
    corrected = root / "klm3_g3_dev_fullactive_base_memory_corrected_v1"
    b1_original = root / "klm3_b1_full_dev_candidate_labels_seed20261012_v1"
    training = root / "klm3_g2_seed20261012_epoch3_v1"
    select = root / "klm3_g2_checkpoint_dev_selected_v1.json"
    # Fixed, explicit source paths. Never open/test/discover a TEST file.
    source_manifest = json.loads((corrected / "summary.json").read_text())
    if not (source_manifest["schema"] == "kbs-plan-c-full-active-dev-paired-v2"
            and source_manifest["scope"] == "DEV_ONLY"
            and source_manifest["memory_corrected_from_all_history"] is True
            and source_manifest["test_file_accessed"] is False
            and source_manifest["n_scored"] == EXPECTED_N):
        raise RuntimeError("Invalid corrected DEV source provenance")
    source_csv = corrected / "dev_full_active_pairs.csv"
    if sha(source_csv) != source_manifest["event_csv_sha256"]:
        raise RuntimeError("DEV reference source SHA mismatch")
    with source_csv.open(newline="") as file:
        rows = list(csv.DictReader(file))
    if len(rows) != EXPECTED_N:
        raise RuntimeError("DEV source size mismatch")
    b1_manifest = json.loads((b1_original / "summary.json").read_text())
    b1_csv = b1_original / "dev_pair_candidate_labels.csv"
    if not (b1_manifest.get("schema") == "kbs-b1-full-dev-paired-candidate-labels-v1"
            and b1_manifest.get("scope") == "DEV_ONLY_POST_G5_EXPLORATORY"
            and b1_manifest.get("status") == "PASS"
            and b1_manifest.get("test_accessed") is False
            and b1_manifest.get("model_training") is False
            and b1_manifest.get("n_dev_events") == EXPECTED_N
            and b1_manifest.get("sampled_candidate_count") == SAMPLED
            and b1_manifest.get("private_event_source_csv_sha256") == B1_SOURCE_SHA
            and b1_manifest.get("corrected_F_source_sha256") == source_manifest["event_csv_sha256"]
            and sha(b1_csv) == B1_SOURCE_SHA):
        raise RuntimeError("B1 frozen original S-label source checksum or manifest mismatch")
    with b1_csv.open(newline="") as f:
        b1_rows = {int(r["event_id"]):r for r in csv.DictReader(f)}
    if len(b1_rows) != EXPECTED_N:
        raise RuntimeError("Original B1 DEV sampled event coverage mismatch")
    g1_manifest = json.loads((g1 / "manifest.json").read_text())
    index_manifest = json.loads((index / "index_manifest.json").read_text())
    dev_manifest = json.loads((dev / "manifest.json").read_text())
    selection = json.loads(select.read_text())
    if not (g1_manifest["protocol_sha256"] == index_manifest["g1_protocol_sha256"]
            == dev_manifest["g1_protocol_sha256"]
            and selection["test_data_opened"] is False):
        raise RuntimeError("G1/G2 DEV provenance mismatch")
    for name in ("dev_contexts.npy", "dev_positive_author_tokens.npy",
                 "dev_source_event_ids.npy"):
        if sha(dev / name) != dev_manifest["files_sha256"][name]:
            raise RuntimeError("DEV cached input digest mismatch")
    events = np.load(dev / "dev_source_event_ids.npy", mmap_mode="r")
    positives = np.load(dev / "dev_positive_author_tokens.npy", mmap_mode="r")
    contexts = np.load(dev / "dev_contexts.npy", mmap_mode="r")
    authors = np.load(index / "authors.npy", mmap_mode="r")
    known = {int(a): i + 1 for i, a in enumerate(authors)}
    devtable = pq.read_table(g1 / "dev_cohort.parquet",
                             columns=["source_event_id", "observed_at"])
    if not np.array_equal(devtable.column("source_event_id").to_numpy(), events):
        raise RuntimeError("DEV cohort event-order mismatch")
    times = devtable.column("observed_at").to_pylist()
    ids = np.unique(np.linspace(0, EXPECTED_N-1, args.limit, dtype=np.int64))
    selected_events = np.asarray(events[ids], dtype=np.int64)
    if len(ids) != args.limit:
        raise RuntimeError("Pilot event selection not exact")
    baseline = {int(row["event_id"]): row for row in rows}
    if any(int(e) not in baseline or int(e) not in b1_rows for e in selected_events):
        raise RuntimeError("Missing corrected baseline event")
    checkpoint_start = time.monotonic()
    models = load_models(training, index_manifest, selection, "cuda")
    reprs = representations(models, np.asarray(contexts[ids]), "cuda", batch=256)
    checkpoint_seconds = time.monotonic() - checkpoint_start
    # CPU history and live-roster replay only once for both Base families.
    replay_start = time.monotonic()
    snapshots, scanned = replay_all_history(g1 / "causal_stream_sealed.parquet",
                                              selected_events, known)
    replay_seconds = time.monotonic() - replay_start
    count = np.bincount(np.load(index / "sequence_ids.npy", mmap_mode="r"),
                        minlength=len(authors) + 1).astype(np.float64)
    logp = np.log1p(count)
    pop = np.zeros(len(count), dtype=np.float64)
    pop[1:] = (logp[1:] - logp[1:].min()) / (logp[1:].max() - logp[1:].min())
    roster_start = time.monotonic()
    rosters = [None] * args.limit
    for j, candidate, _ in author_availability(
            g1 / "available_room_intervals.parquet",
            [times[i] for i in ids], np.asarray(positives[ids]), known):
        rosters[j] = candidate
    if any(c is None for c in rosters):
        raise RuntimeError("Incomplete DEV roster replay")
    roster_seconds = time.monotonic() - roster_start
    torch.cuda.synchronize()
    benchmark = {k: gpu_batch_benchmark(v, reprs[k], "cuda", len(authors)+1)
                 for k, v in models.items()}
    torch.cuda.reset_peak_memory_stats()
    gpu_started = time.monotonic()
    all_scores = dense_scores(reprs, models, ids, "cuda", args.score_batch)
    torch.cuda.synchronize()
    gpu_wall_seconds = time.monotonic() - gpu_started
    peak_gpu_allocated_mib = torch.cuda.max_memory_allocated() / 2**20
    scores_start = time.monotonic()
    errors = {k: 0 for k in ("sasrec", "gru4rec", "memory")}
    sampled_label_errors = {k: 0 for k in errors}
    sum_full = {k: [] for k in errors}
    sum_sample = {k: [] for k in errors}
    sampled_count = []
    for j, index_position in enumerate(ids):
        event = int(events[index_position])
        target = int(positives[index_position])
        cand = rosters[j]
        if not np.all(cand[1:] > cand[:-1]):
            raise RuntimeError("Live roster unsorted or has duplicates")
        recorded = baseline[event]
        if len(cand) != int(recorded["candidate_count"]):
            raise RuntimeError("Full candidate universe does not match corrected DEV")
        sampled = deterministic_sample(cand, target, event)
        sampled_count.append(len(sampled))
        positions = np.searchsorted(cand, sampled)
        if not np.array_equal(cand[positions], sampled):
            raise RuntimeError("Sampled is not exact full roster subset")
        warm, recent, denominator = snapshots[j]
        mem = corrected_memory_score(cand, pop, warm, recent, denominator)
        for family in ("sasrec", "gru4rec", "memory"):
            scores = all_scores[family][j, cand] if family != "memory" else mem
            rank_f = (true_rank(cand, scores, target) if family != "memory"
                      else memory_rank(cand, scores, target))
            rank_s = (true_rank(sampled, scores[positions], target) if family != "memory"
                      else memory_rank(sampled, scores[positions], target))
            if rank_f != int(recorded[family + "_rank"]):
                errors[family] += 1
            old_sample = float(b1_rows[event]["sampled_" + family + "_ndcg10"])
            if abs(ndcg(rank_s) - old_sample) > 1e-12:
                sampled_label_errors[family] += 1
            sum_full[family].append(ndcg(rank_f))
            sum_sample[family].append(ndcg(rank_s))
    cpu_post_seconds = time.monotonic() - scores_start
    output = {
        "schema": "n12-c8v-v2a-original-b1-frozen-dev-full-s-parity-v1",
        "status": "PASS" if not any(errors.values()) and not any(sampled_label_errors.values()) else "HOLD_PARITY",
        "evidence_tier": "POST_G5_DEV_ONLY_EXPLORATORY",
        "test_opened": False,
        "new_training_performed": False,
        "ids_exported": False,
        "n_events": args.limit,
        "full_candidates_min": int(min(len(x) for x in rosters)),
        "full_candidates_max": int(max(len(x) for x in rosters)),
        "sampled_candidates": int(min(sampled_count)),
        "candidate_sample_retains_revealed_target_offline_only": True,
        "gate_features_from_target_informed_samples": False,
        "full_rank_disagreements_with_original_corrected_DEV": errors,
        "sampled_ndcg10_disagreements_with_original_b1_dev": sampled_label_errors,
        "original_B1_source_sha256_verified": True,
        "full_and_sampled_event_level_label_parity_verified": True,
        "means_full": {k: float(np.mean(v)) for k, v in sum_full.items()},
        "means_sampled": {k: float(np.mean(v)) for k, v in sum_sample.items()},
        "mean_base_relative_Memory": {k: {
            "full": float(np.mean(np.asarray(sum_full["memory"]) - np.asarray(sum_full[k]))),
            "sampled": float(np.mean(np.asarray(sum_sample["memory"]) - np.asarray(sum_sample[k])))}
            for k in ("sasrec", "gru4rec")},
        "gpu_benchmark": benchmark,
        "gpu_peak_allocated_MiB": round(float(peak_gpu_allocated_mib), 1),
        "timings_seconds": {
            "weights_and_encoder_representations": round(checkpoint_seconds, 3),
            "all_prior_history_cpu": round(replay_seconds, 3),
            "active_roster_cpu": round(roster_seconds, 3),
            "batched_dense_gpu_full_vocab": round(gpu_wall_seconds, 3),
            "event_ranks_and_memory_cpu": round(cpu_post_seconds, 3),
            "overall": round(time.monotonic() - started, 3)},
        "gpu_batches_evaluated": [12, 32, 64, 128, 256],
        "chosen_gpu_scoring_batch": args.score_batch,
        "causal_prior_events_scanned": int(scanned),
        "reference_sha256_verified": True,
        "checkpoint_family_count": 2,
        "B1_nested_policy_fit_executed": False,
        "B1_full_cohort_scoring_executed": False,
    }
    if args.out.exists():
        raise FileExistsError("Cannot overwrite result")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": output["status"], "events": args.limit,
                      "rank_errors": errors, "sampled_label_errors": sampled_label_errors,
                      "seconds": output["timings_seconds"],
                      "gpu_peak_MiB": output["gpu_peak_allocated_MiB"]}), flush=True)
    if any(errors.values()) or any(sampled_label_errors.values()):
        raise RuntimeError("B1 frozen-score parity failure; do not run full nested DEV")


if __name__ == "__main__":
    main()
