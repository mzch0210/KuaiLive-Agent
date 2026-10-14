#!/usr/bin/env python3
"""Route B B2: purely structural, time-respecting relation null.

No private dataset is loaded by this module. A separate gated runner must supply
pretarget, non-TEST interaction events and an observed-at author availability
predicate. Source event ids are opaque and never exported by this module.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import random
from typing import Callable, Iterable, Sequence

HOUR_NS = 3_600_000_000_000


@dataclass(frozen=True)
class HistoricalEdge:
    source_event_id: int
    user_id: int
    author_id: int
    observed_at_ns: int


def time_bin_end(timestamp_ns: int) -> int:
    """The first timestamp at which the hour containing an edge is closed."""
    return (timestamp_ns // HOUR_NS + 1) * HOUR_NS


def _stable_bin_seed(seed: int, time_bin: int) -> int:
    raw = f"n9-route-b-null-v1:{seed}:{time_bin}".encode("ascii")
    return int.from_bytes(hashlib.blake2b(raw, digest_size=8).digest(), "little")


def frozen_closed_hour_swaps(
    historical: Sequence[HistoricalEdge],
    is_author_active: Callable[[int, int], bool],
    *,
    seed: int,
    attempts_per_edge: int = 18,
) -> tuple[dict[int, int], dict]:
    """Construct activity-valid cross-user author substitutions within *individual hours*.

    Critical design: swaps for each hour use a seed derived from only seed and
    that hour's timestamp. Changes in later hours cannot affect earlier bins.
    The returned map is not yet a causal history: a request may consume a
    substitution only AFTER its whole source hour has closed.
    """
    if attempts_per_edge < 0:
        raise ValueError("attempts_per_edge must be nonnegative")
    ids = [int(x.source_event_id) for x in historical]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate historical event ID")
    if any(x.observed_at_ns < 0 for x in historical):
        raise ValueError("negative historical timestamp")
    original = {x.source_event_id: x.author_id for x in historical}
    group: dict[int, list[HistoricalEdge]] = defaultdict(list)
    for edge in historical:
        group[edge.observed_at_ns // HOUR_NS].append(edge)

    mapping: dict[int, int] = {}
    considered = 0
    swaps = 0
    valid_pairs = 0
    for hour in sorted(group):
        # Sorted IDs make results independent of how batches were delivered.
        edges = sorted(group[hour], key=lambda x: x.source_event_id)
        n = len(edges)
        if n < 2:
            continue
        rng = random.Random(_stable_bin_seed(seed, hour))
        occupied: set[int] = set()
        for _ in range(min(n * attempts_per_edge, 200_000)):
            if len(occupied) >= n - 1:
                break
            i = rng.randrange(n)
            j = rng.randrange(n - 1)
            if j >= i:
                j += 1
            a, b = edges[i], edges[j]
            considered += 1
            if (i in occupied or j in occupied
                    or a.user_id == b.user_id
                    or a.author_id == b.author_id):
                continue
            ta, tb = a.observed_at_ns, b.observed_at_ns
            if not (is_author_active(a.author_id, ta)
                    and is_author_active(b.author_id, tb)
                    and is_author_active(b.author_id, ta)
                    and is_author_active(a.author_id, tb)):
                continue
            valid_pairs += 1
            mapping[a.source_event_id] = b.author_id
            mapping[b.source_event_id] = a.author_id
            occupied.add(i)
            occupied.add(j)
            swaps += 1

    # All past timestamps, user IDs, source event IDs are untouched.
    before = Counter((x.observed_at_ns // HOUR_NS, x.author_id) for x in historical)
    after = Counter((x.observed_at_ns // HOUR_NS,
                     mapping.get(x.source_event_id, x.author_id)) for x in historical)
    if before != after:
        raise AssertionError("hourly author margins changed")
    if len(mapping) != 2 * swaps:
        raise AssertionError("non-disjoint swap or swap accounting failure")
    summary = {
        "schema": "route-b-temporal-null-structural-v1",
        "source_event_count": len(historical),
        "source_hours": len(group),
        "proposals_attempted": considered,
        "cross_active_distinct_user_pairs": valid_pairs,
        "disjoint_swaps": swaps,
        "changed_historical_endpoints": len(mapping),
        "author_hour_degree_exact": True,
        "user_count_and_timestamps_unchanged": True,
        "source_hour_seed_independent_of_future_hours": True,
        "null_activation_rule": "source-hour-end <= target-request-time",
    }
    return mapping, summary


def visible_pretarget_history(
    history: Iterable[HistoricalEdge],
    mapping: dict[int, int],
    *,
    requesting_user_id: int,
    request_at_ns: int,
) -> list[HistoricalEdge]:
    """Use rewired history only after the source hour is fully closed.

    In the request's currently open hour, original edges remain unchanged.
    The history excludes all events with timestamp >= the request timestamp.
    """
    out = []
    for edge in history:
        if edge.user_id != requesting_user_id:
            continue
        if edge.observed_at_ns >= request_at_ns:
            continue
        can_use_null = time_bin_end(edge.observed_at_ns) <= request_at_ns
        author = mapping.get(edge.source_event_id, edge.author_id) if can_use_null else edge.author_id
        out.append(HistoricalEdge(edge.source_event_id, edge.user_id,
                                  author, edge.observed_at_ns))
    out.sort(key=lambda x: (x.observed_at_ns, x.source_event_id))
    return out


def check_request_causal_consistency(original: Iterable[HistoricalEdge],
                                     altered: Iterable[HistoricalEdge],
                                     *,
                                     request_at_ns: int) -> None:
    old = {e.source_event_id: e for e in original}
    new = {e.source_event_id: e for e in altered}
    if old.keys() != new.keys():
        raise AssertionError("changed request history membership")
    for id_, a in old.items():
        b = new[id_]
        if (a.user_id != b.user_id or a.observed_at_ns != b.observed_at_ns
                or a.observed_at_ns >= request_at_ns):
            raise AssertionError("changed timestamp, user or used future event")
        if time_bin_end(a.observed_at_ns) > request_at_ns and a.author_id != b.author_id:
            raise AssertionError("same-bin future edge leakage")
