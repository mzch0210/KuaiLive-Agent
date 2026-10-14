#!/usr/bin/env python3
"""B4-A A3 PRE-FLIGHT ONLY: audit public freeze and synthetic prediction-before-label.

No private cache, real TEST event, target label, ranking metric, or GPU is read.
A passing result is never permission to launch A3 or A4.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Callable

EXPECTED_POOL = 4_723_652
EXPECTED_MAIN = 30_000
EXPECTED_MECHANISM = 4_096
EXPECTED_MAIN_SHA = "be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
EXPECTED_MECHANISM_SHA = "40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059"
EXPECTED_DEV_SHA = "37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
FAMILIES = ("sasrec", "gru4rec")
ARMS = ("S_aligned", "F_aligned")
FORBIDDEN_OUTPUT_KEYS = frozenset({
    "author_id", "target_author", "target", "label", "ndcg",
    "ndcg10", "hr10", "target_rank", "realized_gain",
})


def _read(root: Path, name: str) -> dict:
    folder = root / "experiments" / "kbs_plan_c"
    return json.loads((folder / name).read_text(encoding="utf-8"))


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError("A3 synthetic preflight failed: " + reason)


def _cells(rows: list[dict], group_key: str) -> dict:
    cells = {}
    for row in rows:
        key = (row["date"], row[group_key])
        _require(key not in cells, "duplicate cell " + str(key))
        cells[key] = row
    _require(len(cells) == 20, "expected exactly 20 frozen design cells")
    return cells


def verify_public_freeze(repo_root: Path) -> dict:
    """Cross-check four already-public, outcome-free registered sources."""
    a0 = _read(repo_root, "N9_ROUTE_B_B4A_A0_AGGREGATE_ELIGIBILITY_2026-10-14.json")
    a1 = _read(repo_root, "N9_ROUTE_B_B4A_A1_SEALED_SAMPLE_PUBLIC_2026-10-14.json")
    a2 = _read(repo_root, "N9_ROUTE_B_B4A_A2_DEV_FINAL_GATE_AGGREGATE_2026-10-14.json")
    w = _read(repo_root, "N9_ROUTE_B_B4A_A2_POPULATION_WEIGHTS_2026-10-14.json")
    contract = _read(repo_root, "N9_ROUTE_B_B4A_A2_MODEL_CONTRACT_PUBLIC_2026-10-14.json")

    _require(a0["technical_status"] == "PASS"
             and a0["source_sha256_verified"] is True
             and a0["G5_event_overlap"] == 0
             and a0["residual_warm_history_eligible_events"] == EXPECTED_POOL,
             "A0 eligibility/lineage changed")
    _require(a1["main_events"] == EXPECTED_MAIN
             and a1["mechanism_events"] == EXPECTED_MECHANISM
             and a1["old_G5_target_id_overlap"] == 0
             and a1["source_A0_pool_count"] == EXPECTED_POOL
             and a1["main_private_SHA256"] == EXPECTED_MAIN_SHA
             and a1["mechanism_private_SHA256"] == EXPECTED_MECHANISM_SHA,
             "A1 sample freeze changed")
    _require(a1["target_author_in_sampling_hash"] is False
             and a1["target_author_labels_in_frozen_files"] is False
             and a1["target_ranking_scores_read"] is False
             and a1["A2_A3_A4_authorized"] is False,
             "A1 label separation or approval state inconsistent")
    _require(a2["status"] == "DEV_ONLY_GATE_MODELS_AND_THRESHOLDS_FROZEN"
             and a2["dev_source_SHA256"] == EXPECTED_DEV_SHA
             and a2["n_dev_events"] == 50049
             and a2["B4A_sample_read"] is False
             and a2["test_labels_or_ranking_metrics_opened"] is False,
             "A2 training or DEV source changed")
    _require(contract["status"] == "FOUR_MODELS_DEV_SHA_FEATURE_AND_PREDICTION_CONTRACT_PASS"
             and contract["source_DEV_SHA256"] == EXPECTED_DEV_SHA
             and contract["TEST_rows_read"] == 0
             and contract["B4A_labels_read"] is False
             and contract["A3_A4_authorized"] is False,
             "A2 model contract changed")
    for family in FAMILIES:
        for arm in ARMS:
            m = a2["models"][family][arm]
            qc = contract["results"][family][arm]
            _require(len(m["features"]) == 12 and len(set(m["features"])) == 12
                     and m["oof_user_disjoint"] is True
                     and m["oof_budget"]["dev_oof_call_rate"] <= 0.3 + 1e-12
                     and len(m["model_private_SHA256"]) == 64,
                     "A2 model/fold/budget/hash invalid " + family + arm)
            _require(qc["model_SHA256_pass"] is True
                     and qc["feature_contract_pass"] is True
                     and qc["pointwise_threshold_frozen"] is True
                     and qc["A3_execution_allowed"] is False,
                     "A2 feature preflight or authorization changed " + family + arm)

    _require(w["population_total"] == EXPECTED_POOL
             and w["sample_main_SHA256"] == EXPECTED_MAIN_SHA
             and w["sample_mechanism_SHA256"] == EXPECTED_MECHANISM_SHA
             and w["all_B4A_target_labels_read"] is False
             and w["new_test_ranking_scores_computed"] is False,
             "A2 population-weight registration changed")
    main_cells = _cells(a1["main_strata"], "history_group")
    mech_cells = _cells(a1["mechanism_strata"], "history_group")
    population = None
    kish = {}
    for name, n, design in (
        ("main", EXPECTED_MAIN, main_cells),
        ("mechanism", EXPECTED_MECHANISM, mech_cells),
    ):
        rows = _cells(w[name]["strata"], "history_q")
        _require(set(rows) == set(design), "strata keys not aligned: " + name)
        _require(sum(r["sample_n"] for r in rows.values()) == n, "sample count mismatch")
        _require(sum(r["population_n"] for r in rows.values()) == EXPECTED_POOL,
                 "population cell count mismatch")
        squared = 0.0
        total = 0.0
        for cell, row in rows.items():
            sample_n = row["sample_n"]
            expected = row["population_n"] / sample_n
            _require(design[cell]["events"] == sample_n and sample_n > 0
                     and math.isclose(row["base_poststratification_weight"], expected,
                                      rel_tol=1e-12), "stratum weight mismatch")
            total += expected * sample_n
            squared += expected ** 2 * sample_n
        effective = total ** 2 / squared
        _require(math.isclose(effective, w[name]["N_effective_kish_for_population_weights"],
                              abs_tol=1e-6), "effective weighted sample size mismatch")
        kish[name] = round(effective, 3)
        if population is None:
            population = {cell: row["population_n"] for cell, row in rows.items()}
        else:
            _require(population == {cell: row["population_n"] for cell, row in rows.items()},
                     "main/mechanism population definitions differ")

    return {
        "public_source_freezes": "PASS",
        "frozen_main_events": EXPECTED_MAIN,
        "frozen_mechanism_events": EXPECTED_MECHANISM,
        "frozen_DEV_gate_models": 4,
        "population_cells": 20,
        "Kish_effective_sample_size": kish,
        "license_human_attestation": "PENDING",
        "new_TEST_rows_read": 0,
        "A3_authorized": False,
        "A4_authorized": False,
    }


@dataclass(frozen=True)
class Observation:
    event_id: int
    user_id: int
    timestamp: int
    source_order: int
    author_token: int


@dataclass(frozen=True)
class BlindRequest:
    event_id: int
    user_id: int
    timestamp: int
    source_order: int


def blind_synthetic_replay(
    events: list[Observation],
    chosen_ids: set[int],
    callback: Callable[[BlindRequest, tuple[Observation, ...]], dict],
) -> dict[int, dict]:
    """Model the allowed information boundary; NEVER call on real TEST data.

    An event's author is passed only to the state update that follows its own
    callback. Equal timestamps follow an explicit stable source-order field.
    """
    _require(len(set(e.event_id for e in events)) == len(events),
             "duplicate source event IDs")
    seen = set()
    prior_by_user: dict[int, list[Observation]] = defaultdict(list)
    responses = {}
    last_sort = None
    for e in events:
        order = (e.user_id, e.timestamp, e.source_order)
        _require(last_sort is None or order > last_sort,
                 "stream not ordered by user, timestamp and stable source index")
        last_sort = order
        if e.event_id in chosen_ids:
            req = BlindRequest(e.event_id, e.user_id, e.timestamp, e.source_order)
            history = tuple(prior_by_user[e.user_id])
            _require(all(
                (h.timestamp, h.source_order) < (req.timestamp, req.source_order)
                for h in history
            ), "future or current history exposed")
            outcome_free = callback(req, history)
            _require(type(outcome_free) is dict, "callback contract is not dict")
            keys = set(outcome_free)
            _require(keys == {"top10", "memory_call"}, "unregistered prediction fields")
            _require(not keys.intersection(FORBIDDEN_OUTPUT_KEYS), "label or metric emitted")
            _require(isinstance(outcome_free["memory_call"], bool), "invalid call mask")
            top = outcome_free["top10"]
            _require(isinstance(top, (list, tuple)) and len(top) == 10
                     and len(set(top)) == 10, "invalid top-10 candidate IDs")
            responses[e.event_id] = outcome_free
            seen.add(e.event_id)
        prior_by_user[e.user_id].append(e)
    _require(seen == chosen_ids, "requested target set missing or altered")
    return responses


def run_synthetic_probe() -> dict:
    """Change only an event's synthetic current author: same-event output must not change."""
    def score(req: BlindRequest, previous: tuple[Observation, ...]) -> dict:
        counts = Counter(o.author_token for o in previous)
        roster = tuple(range(1, 13))
        top = sorted(roster, key=lambda candidate: (-counts[candidate], candidate))[:10]
        return {"top10": top, "memory_call": len(previous) >= 2}

    base = [
        Observation(101, 7, 1, 1, 3),
        Observation(102, 7, 2, 2, 4),
        Observation(103, 7, 3, 3, 5),
        Observation(104, 7, 3, 4, 6),
        Observation(105, 8, 4, 5, 7),
        Observation(106, 8, 5, 6, 8),
    ]
    altered = list(base)
    altered[2] = Observation(103, 7, 3, 3, 11)
    before = blind_synthetic_replay(base, {103, 104}, score)
    after = blind_synthetic_replay(altered, {103, 104}, score)
    _require(before[103] == after[103],
             "same-request prediction depends on current target token")
    _require(before[104]["top10"] != after[104]["top10"],
             "later request failed to observe the now-past synthetic target")

    failed_future = False
    try:
        blind_synthetic_replay([base[1], base[0]], {101}, score)
    except ValueError:
        failed_future = True
    _require(failed_future, "chronological order violation was not rejected")

    from analysis.kbs_plan_c.n9_route_b_temporal_null_engine import (
        HistoricalEdge, HOUR_NS, visible_pretarget_history
    )
    older = [HistoricalEdge(1, 11, 2, HOUR_NS + 10)]
    changed = {1: 9}
    current_hour = visible_pretarget_history(
        older, changed, requesting_user_id=11, request_at_ns=HOUR_NS + 20
    )
    closed_hour = visible_pretarget_history(
        older, changed, requesting_user_id=11, request_at_ns=2 * HOUR_NS + 20
    )
    _require(current_hour[0].author_id == 2 and closed_hour[0].author_id == 9,
             "closed-hour null activation leakage")
    return {
        "synthetic_target_identity_invariance": "PASS",
        "synthetic_prequential_history": "PASS",
        "synthetic_same_timestamp_source_order": "PASS",
        "synthetic_future_order_rejection": "PASS",
        "synthetic_closed_hour_null_activation": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    report = {
        "schema": "kbs-b4a-a3-synthetic-preflight-v1",
        "status": "PASS_SYNTHETIC_PROTOCOL_ONLY_A3_AND_A4_HOLD",
        "freeze": verify_public_freeze(args.repo_root),
        "synthetic": run_synthetic_probe(),
        "real_PRIVATE_source_events_read": 0,
        "real_TEST_labels_read": 0,
        "real_TEST_predictions_created": 0,
        "A3_and_A4_execution_permitted": False,
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
