#!/usr/bin/env python3
"""Synthetic-only causal timeline and structural-null tests for Route B B2."""
import unittest
from collections import Counter

from n9_route_b_temporal_null_engine import (
    HOUR_NS, HistoricalEdge, time_bin_end, frozen_closed_hour_swaps,
    visible_pretarget_history, check_request_causal_consistency,
)


class TemporalNullTests(unittest.TestCase):
    def fixture(self):
        # Two users, two mutually available authors, three complete hour bins.
        # Each bin contains exactly two source interactions to ensure pairing.
        return [
            HistoricalEdge(1, 10, 101, 5 * 60 * 10**9),
            HistoricalEdge(2, 20, 202, 10 * 60 * 10**9),
            HistoricalEdge(3, 10, 101, HOUR_NS + 5 * 60 * 10**9),
            HistoricalEdge(4, 20, 202, HOUR_NS + 10 * 60 * 10**9),
            HistoricalEdge(5, 10, 101, 2 * HOUR_NS + 5 * 60 * 10**9),
            HistoricalEdge(6, 20, 202, 2 * HOUR_NS + 10 * 60 * 10**9),
        ]

    def test_closed_hour_blocks_same_hour_future_leakage(self):
        events = self.fixture()
        swaps, summary = frozen_closed_hour_swaps(
            events, lambda author, t: True, seed=20261014)
        self.assertEqual(summary["disjoint_swaps"], 3)
        self.assertEqual(len(swaps), 6)
        user_history = [x for x in events if x.user_id == 10]
        req_inside_first_hour = 7 * 60 * 10**9
        a = visible_pretarget_history(events, swaps, requesting_user_id=10,
                                      request_at_ns=req_inside_first_hour)
        self.assertEqual([x.author_id for x in a], [101])
        check_request_causal_consistency(
            [x for x in user_history if x.observed_at_ns < req_inside_first_hour],
            a, request_at_ns=req_inside_first_hour)

        req_after_first_hour = HOUR_NS
        b = visible_pretarget_history(events, swaps, requesting_user_id=10,
                                      request_at_ns=req_after_first_hour)
        self.assertEqual([x.author_id for x in b], [202])
        check_request_causal_consistency(
            [x for x in user_history if x.observed_at_ns < req_after_first_hour],
            b, request_at_ns=req_after_first_hour)

        # At the boundary of hour 2: only first hour can be rewired.
        halfway_second_hour = HOUR_NS + 7 * 60 * 10**9
        c = visible_pretarget_history(events, swaps, requesting_user_id=10,
                                      request_at_ns=halfway_second_hour)
        self.assertEqual([x.author_id for x in c], [202, 101])
        check_request_causal_consistency(
            [x for x in user_history if x.observed_at_ns < halfway_second_hour],
            c, request_at_ns=halfway_second_hour)

    def test_original_degree_and_timestamp_margins(self):
        events = self.fixture()
        swap, summary = frozen_closed_hour_swaps(events, lambda a, t: True, seed=1)
        self.assertTrue(summary["author_hour_degree_exact"])
        self.assertTrue(summary["user_count_and_timestamps_unchanged"])
        before = Counter((x.observed_at_ns // HOUR_NS, x.author_id) for x in events)
        after = Counter((x.observed_at_ns // HOUR_NS,
                         swap.get(x.source_event_id, x.author_id)) for x in events)
        self.assertEqual(before, after)
        for x in events:
            self.assertGreaterEqual(time_bin_end(x.observed_at_ns), x.observed_at_ns)

    def test_future_bins_cannot_change_past_randomization(self):
        events = self.fixture()
        first_bin = events[:2]
        swaps1, _ = frozen_closed_hour_swaps(first_bin, lambda a, t: True, seed=9)
        swaps2, _ = frozen_closed_hour_swaps(events, lambda a, t: True, seed=9)
        self.assertEqual({k: v for k, v in swaps2.items() if k in (1, 2)}, swaps1)

    def test_activity_failures_prohibit_cross_swap(self):
        events = self.fixture()[:2]
        # Original authors available only at their own source timestamps.
        own_times = {(x.author_id, x.observed_at_ns) for x in events}
        changes, stats = frozen_closed_hour_swaps(events, lambda a, t: (a, t) in own_times,
                                                  seed=20261014)
        self.assertEqual(changes, {})
        self.assertEqual(stats["disjoint_swaps"], 0)

    def test_invalid_timeline_violations_are_rejected(self):
        events = self.fixture()
        with self.assertRaises(ValueError):
            frozen_closed_hour_swaps(events + events[:1], lambda a, t: True, seed=1)
        with self.assertRaises(ValueError):
            frozen_closed_hour_swaps(
                [HistoricalEdge(9, 10, 101, -1)], lambda a, t: True, seed=1)
        with self.assertRaises(AssertionError):
            check_request_causal_consistency([events[0]],
                                             [HistoricalEdge(1, 10, 202, events[0].observed_at_ns)],
                                             request_at_ns=30 * 60 * 10**9)
        with self.assertRaises(AssertionError):
            check_request_causal_consistency([events[0]],
                                             [events[0]],
                                             request_at_ns=events[0].observed_at_ns)

    def test_deterministic_independent_of_batch_order(self):
        events = self.fixture()
        rng_seed = 12
        a, _ = frozen_closed_hour_swaps(events, lambda author, t: True, seed=rng_seed)
        b, _ = frozen_closed_hour_swaps(events[::-1], lambda author, t: True, seed=rng_seed)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main(verbosity=2)
