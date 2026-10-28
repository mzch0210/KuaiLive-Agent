"""Public synthetic-only QA. Never reads original B1 DEV or TEST outcomes."""
import importlib.util
import pathlib
import unittest

import numpy as np

SCRIPT = pathlib.Path(__file__).with_name("n15_p1_matched_budget_dev.py")
spec = importlib.util.spec_from_file_location("n15_p1_matched_budget_dev", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ExactBatchTest(unittest.TestCase):
    def test_exact_calls_and_label_blind_permutation(self):
        scores = np.array([0.2, 0.9, 0.1, 0.7, 0.4, 0.3, 0.8, 0.6, 0.5, 0.0])
        ids = np.arange(len(scores))
        mask = m.exact_batch_topk(scores, ids, 0.3)
        self.assertEqual(mask.sum(), 3)
        self.assertEqual(set(ids[mask].tolist()), {1, 3, 6})
        permutation = np.array([9, 4, 8, 2, 7, 6, 0, 3, 1, 5])
        permuted = m.exact_batch_topk(scores[permutation], ids[permutation], .3)
        self.assertEqual(set(ids[permutation][permuted].tolist()), set(ids[mask].tolist()))

    def test_seeded_ties_repeatable_and_count(self):
        s = np.ones(19)
        rowids = np.arange(19) + 100
        a = m.exact_batch_topk(s, rowids, 0.3)
        b = m.exact_batch_topk(s[::-1], rowids[::-1], 0.3)
        self.assertEqual(int(a.sum()), 5)
        self.assertEqual(set(rowids[a].tolist()), set(rowids[::-1][b].tolist()))

    def test_invalid_and_empty_quota(self):
        for s, ids, q in [
            ([float("nan")], [0], .3),
            ([.1, .2], [1, 1], .5),
            ([.1], [1], -0.1),
            ([.1], [1], 1.1),
        ]:
            with self.assertRaises(ValueError):
                m.exact_batch_topk(np.array(s), np.array(ids), q)
        self.assertFalse(m.exact_batch_topk(np.array([.3,.2]), np.array([0,1]), 0).any())

    def test_matched_policy_utility_identity(self):
        fscore = np.array([.9, .8, .1, .0, .3, .2, .4, .5, .6, .7])
        sscore = np.array([.0, .8, .9, .7, .1, .2, .3, .4, .5, .6])
        indexes = np.arange(10)
        choosef = m.exact_batch_topk(fscore, indexes, .3)
        chooses = m.exact_batch_topk(sscore, indexes, .3)
        delta = np.array([.5,.2,-.4,.3,.2,-.1,.1,-.2,.3,.0])
        base = np.full(10, .4)
        diff = (base + choosef * delta) - (base + chooses * delta)
        self.assertEqual(choosef.sum(), chooses.sum())
        self.assertEqual((choosef & ~chooses).sum(), (chooses & ~choosef).sum())
        self.assertTrue(np.allclose(diff, (choosef.astype(int)-chooses.astype(int))*delta))

    def test_bootstrap_reproducible(self):
        a = m.user_cluster_ci(np.array([1.,0.,-1.,.5]),np.array(["u1","u1","u2","u3"]),30,123)
        b = m.user_cluster_ci(np.array([1.,0.,-1.,.5]),np.array(["u1","u1","u2","u3"]),30,123)
        self.assertEqual(a,b)
        self.assertEqual(len(a),2)


if __name__ == "__main__":
    unittest.main()
