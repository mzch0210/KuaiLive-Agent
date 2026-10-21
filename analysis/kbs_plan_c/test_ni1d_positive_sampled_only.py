"""Tests of a STRONGLY ASSUMED S-only correction on synthetic data.

NI-1d must not be interpreted as an approved real-data corrected-S method.
"""
import unittest
from math import isclose
from ni1d_positive_sampled_only import (
    N_SMALL, N_LARGE, DRAW, PI, FULL_GAP,
    analytic_raw_sampled_mean, conditional_common_ahead_probabilities,
    decisions, run_experiment, synthetic_training, u,
)


class PositiveSampledOnlyTest(unittest.TestCase):
    def test_shared_sample_emission_normalizes(self):
        for n in (N_SMALL, N_LARGE):
            self.assertTrue(isclose(
                sum(conditional_common_ahead_probabilities(n)), 1.0, abs_tol=1e-12
            ))
            self.assertGreater(DRAW / (n - 1), 0)
            self.assertLess(DRAW / (n - 1), 1)

    def test_analytic_raw_reversal_vs_full(self):
        self.assertGreater(
            analytic_raw_sampled_mean(N_SMALL, PI[0]),
            analytic_raw_sampled_mean(N_LARGE, PI[1]),
        )
        self.assertGreater((2 * PI[1] - 1) * FULL_GAP,
                           (2 * PI[0] - 1) * FULL_GAP)

    def test_s_only_fitted_correction_and_matched_budget(self):
        result = run_experiment(replicates=12, events=50000)
        self.assertEqual(result["times_chose_true_best_group"]["raw_s"], 0)
        self.assertEqual(result["times_chose_true_best_group"]["corrected_s"], 12)
        self.assertEqual(result["times_chose_true_best_group"]["full_oracle"], 12)
        policies = result["example_first_rep"]["policies"]
        self.assertEqual(policies["raw_s"]["calls_per_2events"], 1)
        self.assertEqual(policies["corrected_s"]["calls_per_2events"], 1)
        self.assertGreater(policies["raw_s"]["regret_vs_full_oracle"], 0.05)
        self.assertEqual(policies["corrected_s"]["regret_vs_full_oracle"], 0)

    def test_corrected_assumption_fails_under_rank_misspecification(self):
        # 9/10 rank pair has a far smaller full effect than assumed 10/11.
        self.assertGreater(FULL_GAP / (u(9) - u(10)), 20)

    def test_equal_roster_negative_control(self):
        self.assertGreater(
            analytic_raw_sampled_mean(N_SMALL, PI[1]),
            analytic_raw_sampled_mean(N_SMALL, PI[0]),
        )

    def test_inputs(self):
        for args in ((575, 0.5, 100, 1), (N_SMALL, 1.2, 100, 1),
                     (N_SMALL, 0.5, 0, 1)):
            with self.assertRaises(ValueError):
                synthetic_training(*args)
        with self.assertRaises(ValueError):
            decisions(numbers=(N_SMALL,))


if __name__ == "__main__":
    unittest.main()
