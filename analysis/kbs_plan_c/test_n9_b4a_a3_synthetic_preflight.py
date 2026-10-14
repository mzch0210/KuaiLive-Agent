#!/usr/bin/env python3
"""Synthetic-only B4-A A3 contract regression tests; never read private TEST."""
import unittest
from pathlib import Path

from analysis.kbs_plan_c.n9_b4a_a3_synthetic_preflight import (
    BlindRequest, Observation, blind_synthetic_replay,
    run_synthetic_probe, verify_public_freeze,
)


ROOT = Path(__file__).resolve().parents[2]


def dummy_score(request, history):
    assert isinstance(request, BlindRequest)
    assert not hasattr(request, "author_token")
    return {"top10": list(range(1, 11)), "memory_call": bool(history)}


class SyntheticA3Tests(unittest.TestCase):
    def test_published_sha_and_weights_are_consistent(self):
        result = verify_public_freeze(ROOT)
        self.assertEqual(result["frozen_DEV_gate_models"], 4)
        self.assertEqual(result["population_cells"], 20)
        self.assertEqual(result["frozen_main_events"], 30_000)
        self.assertEqual(result["frozen_mechanism_events"], 4_096)
        self.assertFalse(result["A3_authorized"])
        self.assertFalse(result["A4_authorized"])

    def test_all_synthetic_invariance_checks_pass(self):
        checks = run_synthetic_probe()
        self.assertTrue(all(value == "PASS" for value in checks.values()))

    def test_current_target_label_not_passed_to_callback(self):
        seen = []
        def capture(request, history):
            seen.append((request, history))
            return dummy_score(request, history)
        rows = [
            Observation(1, 20, 100, 1, 3),
            Observation(2, 20, 200, 2, 5),
            Observation(3, 20, 300, 3, 9),
        ]
        result = blind_synthetic_replay(rows, {1, 2, 3}, capture)
        self.assertEqual(set(result), {1, 2, 3})
        self.assertEqual([len(h) for _, h in seen], [0, 1, 2])
        self.assertEqual(seen[2][1][-1].author_token, 5)
        self.assertFalse(hasattr(seen[2][0], "author_token"))

    def test_reject_label_or_utility_in_prediction_payload(self):
        def improper(request, history):
            return {"top10": list(range(1, 11)),
                    "memory_call": False, "target_rank": 1}
        with self.assertRaises(ValueError):
            blind_synthetic_replay([Observation(1, 1, 1, 1, 7)], {1}, improper)

    def test_reject_wrong_target_set_and_duplicates(self):
        rows = [Observation(1, 1, 1, 1, 7)]
        with self.assertRaises(ValueError):
            blind_synthetic_replay(rows, {2}, dummy_score)
        with self.assertRaises(ValueError):
            blind_synthetic_replay(rows + rows, {1}, dummy_score)

    def test_same_clock_stable_source_order_not_future(self):
        rows = [
            Observation(7, 2, 40, 1, 3),
            Observation(8, 2, 40, 2, 4),
        ]
        seen = []
        def inspect(request, history):
            seen.append([x.event_id for x in history])
            return dummy_score(request, history)
        blind_synthetic_replay(rows, {7, 8}, inspect)
        self.assertEqual(seen, [[], [7]])
        with self.assertRaises(ValueError):
            blind_synthetic_replay(rows[::-1], {7, 8}, inspect)

    def test_reject_incomplete_and_invalid_top10(self):
        def malformed(request, history):
            return {"top10": [1] * 10, "memory_call": False}
        with self.assertRaises(ValueError):
            blind_synthetic_replay([Observation(1, 1, 1, 1, 9)], {1}, malformed)


if __name__ == "__main__":
    unittest.main()
