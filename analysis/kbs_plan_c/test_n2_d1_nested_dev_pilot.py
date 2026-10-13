"""Synthetic guards for the N2-D1 nested DEV two-stage pilot."""
import unittest

import numpy as np
import pandas as pd

from n2_d1_nested_dev_pilot import cluster_ci, nested_compare, validate_frame, EXPECTED_N


class NestedPilotTests(unittest.TestCase):
    def synthetic(self):
        rng = np.random.default_rng(9)
        n_users = 24
        n = n_users * 6
        X = rng.normal(size=(n, 12))
        base = np.clip(0.27 + .07 * X[:, 0] + rng.normal(0, .02, n), 0, 1)
        mem = np.clip(0.31 + .08 * X[:, 1] + rng.normal(0, .03, n), 0, 1)
        data = {"user_id": np.repeat(np.arange(n_users), 6),
                "event_id": np.arange(n), "split": ["DEV"] * n,
                "base_ndcg10": base, "memory_ndcg10": mem}
        for j in range(12):
            data[f"x_{j:02d}"] = X[:, j]
        return pd.DataFrame(data)

    def test_fold_calibration_and_exploratory_scope(self):
        df = self.synthetic()
        result = nested_compare(df, "sasrec", n_outer=3, n_inner=2,
                                max_iter=8, min_leaf=3, n_boot=35)
        self.assertEqual(result["n_events"], len(df))
        self.assertFalse(result["test_accessed"])
        self.assertEqual(result["evidence_tier"], "POST_G5_EXPLORATORY_NESTED_DEV")
        self.assertEqual(set(result["methods"]), {"direct", "two_stage"})
        self.assertTrue(np.isfinite(result["direct_minus_two_stage_ndcg10"]))
        self.assertEqual(len(result["folds"]), 3)
        for fold in result["folds"]:
            for metric in fold["results"].values():
                self.assertLessEqual(metric["inner_oof_selection_rate"], .30 + 1e-12)

    def test_leaky_feature_rejected(self):
        df = self.synthetic()
        df = df.rename(columns={"x_00": "x_target_label"})
        with self.assertRaisesRegex(ValueError, "Outcome leakage"):
            nested_compare(df, "sasrec", n_outer=3, n_inner=2, max_iter=5,
                           min_leaf=3, n_boot=15)

    def test_reject_test_rows(self):
        df = self.synthetic()
        df.loc[0, "split"] = "TEST"
        with self.assertRaisesRegex(ValueError, "Only DEV"):
            validate_frame(df)

    def test_cluster_ci_finite(self):
        users = np.array(["a", "a", "b", "b", "c", "d"])
        ci = cluster_ci(np.array([1., -1., .5, -.2, .1, .2]), users, n_boot=30)
        self.assertEqual(len(ci), 2)
        self.assertTrue(np.isfinite(ci).all())


if __name__ == "__main__":
    unittest.main()
