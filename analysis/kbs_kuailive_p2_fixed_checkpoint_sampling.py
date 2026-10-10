"""KBS P2: retrospective KuaiLive candidate-draw sensitivity, frozen P0 model.

The completed historical 20260918 P0 per-user scores MUST reproduce before
any new sampling results are released. Do not change checkpoint, TEST cohort,
target, Memory scoring, alpha, timestamp/availability, or model selection.
This is an exploratory sensitivity analysis of already inspected TEST events.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import torch

from kbs_kuailive_factorial import (
    BASELINE_MODEL_HASHES, EXPECTED_INPUT_HASHES, EXPECTED_SEED0,
    four_cell_ranks,
)
from kbs_kuailive_same_checkpoint import sha256, subset_indices
from full_active_dual_id import (
    active_interval_arrays, candidate_sweep, encode_phase_users, load_rechorus,
    memory_rank, ndcg_scalar, popularity_by_streamer,
    room_to_streamer_item_array, score_embedding_candidates,
)
from room_level_selective_agent import (
    histories, load_data, memory_scores, parse_list,
)

N = 10222
ALPHA = 0.125
SIZES = (128, 256, 575)
DRAW_SEEDS = (20261010, 20261011, 20261012)
SOURCE_RUN = 37751814645
SOURCE_RESULTS_ARTIFACT = 11538678848
SOURCE_MODEL_ARTIFACT = 11536890439
SOURCE_INPUT_ARTIFACT = 11534262601
UPSTREAM_RECHORUS = "c164ec4303cc20ddcfbd1b57de366a481811d1e5"


def n_boot_ci(mat: np.ndarray, n_boot: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    # Fixed-score conditional paired user bootstrap, same user indices for every
    # draw/size contrast; no training/model-choice or draw-population CI claimed.
    x = np.asarray(mat, dtype=np.float64)
    n, p = x.shape
    rng = np.random.default_rng(seed)
    means = np.empty((n_boot, p), dtype=np.float64)
    for k in range(0, n_boot, 16):
        b = min(16, n_boot - k)
        ids = rng.integers(0, n, size=(b, n), dtype=np.int32)
        means[k:k+b] = x[ids].mean(axis=1)
    return np.quantile(means, .025, axis=0), np.quantile(means, .975, axis=0)


def check_seed_protocol():
    assert SIZES == (128, 256, 575)
    assert DRAW_SEEDS == (20261010, 20261011, 20261012)
    assert ALPHA == .125
    assert N == 10222
    assert SOURCE_RUN == 37751814645


def self_test():
    check_seed_protocol()
    rng = np.random.default_rng(20261010)
    candidates = np.array([17, 8, 2, 9, 10, 33, 4])
    target = 17
    pool = np.flatnonzero(candidates != target)
    idx = np.r_[0, rng.choice(pool, size=3, replace=False)]
    assert len(idx) == 4 and len(set(idx)) == 4 and idx[0] == 0
    assert set(candidates[idx]).issubset(set(candidates))
    trial = np.array([[-.1, .2], [.3, .5], [.1, -.3], [.2, .1]])
    lo, hi = n_boot_ci(trial, 50, 22)
    assert np.all(lo <= hi)
    print("P2 synthetic score-mask and paired-bootstrap preflight PASS")


def main(args):
    check_seed_protocol()
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass

    root = args.data_root / "KuaiLiveShopRoomDualID"
    stream_root = args.data_root / "KuaiLiveShopStreamerParallel"
    input_sha = {name: sha256(root / name) for name in EXPECTED_INPUT_HASHES}
    model_sha = {"room": sha256(args.room_model),
                 "streamer": sha256(args.streamer_model)}
    if input_sha != EXPECTED_INPUT_HASHES:
        raise RuntimeError("Frozen P0 input SHA mismatch: " + str(input_sha))
    if model_sha != BASELINE_MODEL_HASHES:
        raise RuntimeError("Frozen P0 checkpoint SHA mismatch: " + str(model_sha))

    reference = pd.read_csv(args.reference_per_user)
    if len(reference) != N or reference.user_id.duplicated().any():
        raise RuntimeError("Invalid original P0 per-user reference")
    ref = reference.set_index("user_id", verify_integrity=True)
    if not {"base_SS", "base_FF", "delta_SS", "delta_FF",
            "sampled_memory", "full_memory"}.issubset(ref.columns):
        raise RuntimeError("Original P0 reference is missing required columns")

    train, dev, test, item_to_streamer = load_data(root, 574)
    if len(test) != N or test.user_id.duplicated().any():
        raise RuntimeError("Frozen 10,222-user cohort identity mismatch")
    room_map = pd.read_csv(root / "room_item_map.tsv", sep="\t")
    streamer_map = pd.read_csv(stream_root / "streamer_item_map.tsv", sep="\t")
    intervals = active_interval_arrays(
        pd.read_pickle(args.prepared_dir / "rooms.pkl"), room_map)
    item_to_streamer_id = room_to_streamer_item_array(room_map, streamer_map)

    room_model, room_corpus = load_rechorus(
        args.rechorus_source, args.data_root,
        "KuaiLiveShopRoomDualID", args.room_model)
    streamer_model, streamer_corpus = load_rechorus(
        args.rechorus_source, args.data_root,
        "KuaiLiveShopStreamerParallel", args.streamer_model)
    room_vec = encode_phase_users(room_model, room_corpus, "test")
    streamer_vec = encode_phase_users(streamer_model, streamer_corpus, "test")
    pop = popularity_by_streamer(train, item_to_streamer)
    hist = histories(
        pd.concat([train, dev[["user_id", "item_id", "time"]]],
                  ignore_index=True), item_to_streamer)
    by_user = test.set_index("user_id", verify_integrity=True)

    # Independent prespecified RNG streams, each consumed in the SAME event order.
    randomizers = {seed: np.random.default_rng(seed) for seed in DRAW_SEEDS}
    records = []
    min_full_n = 10**12
    metadata_inactive = 0
    history_negative_users = 0
    # Original sampled candidates may include *previously clicked* rooms. The
    # original "unobserved negative" means not currently the positive target;
    # do not silently exclude historical room interactions in new lists.
    prior_rooms = pd.concat([train, dev[["user_id", "item_id", "time"]]],
                            ignore_index=True).groupby("user_id").item_id.apply(set).to_dict()

    for j, (uid, t, target, full_items, was_active) in enumerate(
        candidate_sweep(test, intervals)
    ):
        event = by_user.loc[uid]
        if int(event.item_id) != target or int(event.time) != t:
            raise RuntimeError("Event user/timestamp/target identity mismatch")
        if not was_active:
            metadata_inactive += 1
        original = np.r_[target, parse_list(event.neg_items, int)]
        if len(original) != 575 or len(set(original)) != 575:
            raise RuntimeError("Original candidate list corrupted")
        if len(set(original[1:]) & prior_rooms[uid]) > 0:
            history_negative_users += 1
        original_idx = subset_indices(full_items, original)
        target_ids = np.flatnonzero(full_items == target)
        if len(target_ids) != 1 or int(original_idx[0]) != int(target_ids[0]):
            raise RuntimeError("Target is not uniquely nested in full candidates")
        if len(full_items) < max(SIZES):
            raise RuntimeError("Full candidate list smaller than frozen sampled protocol")
        min_full_n = min(min_full_n, len(full_items))

        # ONE encoder pass per user and ONE full-candidate embedding scoring.
        room_score = score_embedding_candidates(room_model, room_vec[uid], full_items)
        stream_score = score_embedding_candidates(
            streamer_model, streamer_vec[uid], item_to_streamer_id[full_items])
        all_memory_score = memory_scores(
            full_items, uid, pop, hist, item_to_streamer)
        if not (np.isfinite(room_score).all() and
                np.isfinite(stream_score).all() and
                np.isfinite(all_memory_score).all()):
            raise RuntimeError("Non-finite full score vector")

        def evaluate_selection(idx: np.ndarray):
            sample = full_items[idx]
            r = four_cell_ranks(
                room_score, stream_score, idx, int(target_ids[0]), ALPHA)
            m = ndcg_scalar(memory_rank(sample, all_memory_score[idx], target))
            b = {c: ndcg_scalar(rank) for c, rank in r.items()}
            return m, b

        # Fail closed: reproduce ALL six historical P0 event-level scores,
        # not only their aggregate means.
        original_memory, original_b = evaluate_selection(original_idx)
        full_memory = ndcg_scalar(memory_rank(
            full_items, all_memory_score, target))
        base_full = original_b["FF"]
        uref = ref.loc[uid]
        for k, v in {
            "base_SS": original_b["SS"],
            "base_FF": base_full,
            "delta_SS": original_memory - original_b["SS"],
            "delta_FF": full_memory - base_full,
            "sampled_memory": original_memory,
            "full_memory": full_memory,
        }.items():
            if abs(float(uref[k]) - float(v)) > 1e-11:
                raise RuntimeError(
                    f"Frozen P0 per-user score mismatch uid={uid} {k}: "
                    f"archived={uref[k]} re-scored={v}")
        fixed = {"user_id": uid, "time": t, "target_item": target,
                 "full_candidates": len(full_items),
                 "target_metadata_active": bool(was_active),
                 "base_full": base_full,
                 "memory_full": full_memory,
                 "delta_full": full_memory-base_full,
                 "base_original_575": original_b["SS"],
                 "memory_original_575": original_memory,
                 "delta_original_575": original_memory-original_b["SS"]}

        candidate_pool = np.flatnonzero(full_items != target)
        if len(candidate_pool) < 574:
            raise RuntimeError("Not enough eligible full-active non-target rooms")

        for seed in DRAW_SEEDS:
            rng = randomizers[seed]
            for size in SIZES:
                draw_idx = np.r_[int(target_ids[0]),
                                 rng.choice(candidate_pool, size=size-1,
                                            replace=False)]
                assert len(set(draw_idx)) == size
                mem, b = evaluate_selection(draw_idx)
                prefix = f"s{size}_d{seed}"
                fixed[f"base_{prefix}"] = b["SS"]
                fixed[f"memory_{prefix}"] = mem
                fixed[f"delta_{prefix}"] = mem-b["SS"]
                fixed[f"shift_{prefix}"] = (full_memory-base_full) - (mem-b["SS"])
                # 2x2 path-average allocation is descriptive, not causal.
                delta_ss = mem-b["SS"]
                delta_sf = mem-b["SF"]
                delta_fs = full_memory-b["FS"]
                delta_ff = full_memory-b["FF"]
                mem_alloc = .5*((delta_fs-delta_ss)+(delta_ff-delta_sf))
                norm_alloc = .5*((delta_sf-delta_ss)+(delta_ff-delta_fs))
                if abs(mem_alloc + norm_alloc - fixed[f"shift_{prefix}"]) > 1e-12:
                    raise RuntimeError("Candidate 2x2 allocation identity failed")
                fixed[f"membership_{prefix}"] = mem_alloc
                fixed[f"normalization_{prefix}"] = norm_alloc
        records.append(fixed)
        if (j+1) % 2500 == 0:
            print(f"Scored {j+1} original P0-matched users", flush=True)

    df = pd.DataFrame(records).sort_values("user_id").reset_index(drop=True)
    if len(df) != N or df.user_id.duplicated().any():
        raise RuntimeError("Missing or duplicate user outcomes")
    assert (df.full_candidates >= 575).all()
    report_expected = {
        "SS": float(df.delta_original_575.mean()),
        "FF": float(df.delta_full.mean()),
        "shift": float((df.delta_full-df.delta_original_575).mean()),
        "sampled_base": float(df.base_original_575.mean()),
        "full_base": float(df.base_full.mean()),
        "sampled_memory": float(df.memory_original_575.mean()),
        "full_memory": float(df.memory_full.mean()),
    }
    for name, expected in EXPECTED_SEED0.items():
        if abs(report_expected[name] - expected) > 1e-10:
            raise RuntimeError(f"Original P0 global replay mismatch: {name}")

    draws = [(size, seed) for size in SIZES for seed in DRAW_SEEDS]
    cols = ["delta_full", "delta_original_575"]
    cols += [f"delta_s{size}_d{seed}" for size,seed in draws]
    cols += [f"shift_s{size}_d{seed}" for size,seed in draws]
    cols += [f"membership_s{size}_d{seed}" for size,seed in draws]
    cols += [f"normalization_s{size}_d{seed}" for size,seed in draws]
    matrix = df[cols].to_numpy(np.float64)
    lo, hi = n_boot_ci(matrix, args.n_boot, 20261010+333)

    rows = []
    for i, name in enumerate(cols):
        rows.append({"measure":name, "mean":float(matrix[:,i].mean()),
                     "ci95_low":float(lo[i]), "ci95_high":float(hi[i]),
                     "n_users":N, "n_boot":args.n_boot})
    summary = pd.DataFrame(rows)
    per_draw = []
    for size in SIZES:
        subset = []
        for seed in DRAW_SEEDS:
            delta = float(df[f"delta_s{size}_d{seed}"].mean())
            shift = float(df[f"shift_s{size}_d{seed}"].mean())
            subset.append(delta)
            per_draw.append({"size":size, "seed":seed, "sampled_delta":delta,
                             "full_delta":float(df.delta_full.mean()),
                             "full_minus_sampled":shift,
                             "sampled_is_negative":delta < 0,
                             "shift_is_positive":shift > 0,
                             "n_users":N})
        print(f"candidate_size={size}; delta across predeclared draws={subset}", flush=True)
    per_draw_df = pd.DataFrame(per_draw)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out_dir/"p2_per_user_fixed_checkpoint.csv.gz",
              index=False, compression="gzip")
    summary.to_csv(args.out_dir/"p2_user_bootstrap.csv", index=False)
    per_draw_df.to_csv(args.out_dir/"p2_predeclared_draws.csv", index=False)
    manifest = {
        "kind":"POSTHOC_FIXED_CHECKPOINT_CANDIDATE_DRAW_SENSITIVITY",
        "not_an_independent_heldout_TEST":True,
        "not_new_model_training":True,
        "not_new_gate_selection":True,
        "n_users":N, "candidate_sizes":list(SIZES),
        "negative_draw_seeds":list(DRAW_SEEDS),
        "original_575_reference_reproduced_per_user":True,
        "original_global_reference":report_expected,
        "original_source_run":SOURCE_RUN,
        "original_reference_artifact":SOURCE_RESULTS_ARTIFACT,
        "original_model_artifact":SOURCE_MODEL_ARTIFACT,
        "original_input_artifact":SOURCE_INPUT_ARTIFACT,
        "upstream_rechorus_commit":UPSTREAM_RECHORUS,
        "model_sha256":model_sha, "frozen_input_sha256":input_sha,
        "room_fusion_alpha":ALPHA, "all_sampling_without_replacement":True,
        "sampled_pool":"all full-active eligible candidate rooms except current target; prior-user-room interactions NOT excluded, consistent with original 575 protocol",
        "one_encoder_and_full_raw_score_pass_per_user":True,
        "min_full_candidates":int(min_full_n),
        "target_metadata_inactive_n":metadata_inactive,
        "original_575_users_with_previously_observed_negative_rooms":history_negative_users,
        "all_nine_draws_reported":True,
        "bootstrap_replicates":args.n_boot,
        "ci_target":"conditional user-resampling only for each prespecified draw",
        "between_draw_sd_is_descriptive":True,
        "design_boundary":"candidate count and composition change together; no causal intervention, no untouched TEST, no selector retuning",
    }
    (args.out_dir/"p2_protocol_and_provenance.json").write_text(
        json.dumps(manifest, indent=2)+"\n")
    print("P2 historical per-user identities and all new draw analyses PASS")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    for name in ("rechorus-source","data-root","prepared-dir","room-model",
                 "streamer-model","reference-per-user","out-dir"):
        p.add_argument("--"+name, type=Path)
    p.add_argument("--n-boot", type=int, default=3000)
    args = p.parse_args()
    if args.self_test:
        self_test()
    else:
        for name in ("rechorus_source","data_root","prepared_dir",
                     "room_model","streamer_model","reference_per_user","out_dir"):
            if getattr(args,name) is None:
                p.error("--"+name.replace("_","-")+" required")
        if args.n_boot != 3000:
            raise RuntimeError("P2 protocol prespecified n_boot=3000")
        main(args)
