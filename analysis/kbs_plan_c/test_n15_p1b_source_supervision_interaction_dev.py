"""Public synthetic-only tests for N15 P1-B; never loads private B1/B2 files."""
import importlib.util
import pathlib
import unittest
import numpy as np

SCRIPT = pathlib.Path(__file__).with_name("n15_p1b_source_supervision_interaction_dev.py")
spec = importlib.util.spec_from_file_location("n15_p1b_source_supervision_interaction_dev", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ExactQuotaAndInteractionTests(unittest.TestCase):
    def test_exact_quota_and_permutation_invariance(self):
        scores = np.array([.3, .8, .1, .9, .5, .4, .2, .7, .6, 0.])
        ids = np.arange(10)
        mask = m.exact_batch_topk(scores, ids, .3)
        self.assertEqual(int(mask.sum()), 3)
        perm = np.array([9, 2, 5, 0, 8, 3, 1, 7, 4, 6])
        m2 = m.exact_batch_topk(scores[perm], ids[perm], .3)
        self.assertEqual(set(ids[mask]), set(ids[perm][m2]))

    def test_ties_repeatable_and_exact_count(self):
        ids = np.arange(17) + 100
        a = m.exact_batch_topk(np.ones(17), ids, .3)
        b = m.exact_batch_topk(np.ones(17)[::-1], ids[::-1], .3)
        self.assertEqual(a.sum(), 5)
        self.assertEqual(set(ids[a]), set(ids[::-1][b]))

    def test_rejects_invalid_inputs(self):
        bad = [
            (np.array([np.nan]), np.array([0]), .5),
            (np.array([.2, .4]), np.array([1, 1]), .5),
            (np.array([.2]), np.array([1]), -0.1),
            (np.array([.2]), np.array([1]), 1.1),
        ]
        for s, i, q in bad:
            with self.assertRaises(ValueError):
                m.exact_batch_topk(s, i, q)

    def test_allocation_identity_and_source_interaction_identity(self):
        n = 20
        f = np.array([.4, .3, -.2, .5, .1, -.1, .2, .3, -.3, .1,
                      .2, -.1, .4, .2, -.2, .1, .3, -.1, .2, .1])
        l = f * .6 + np.linspace(-.05, .05, n)
        pf = m.exact_batch_topk(np.arange(n, dtype=float), np.arange(n), .3)
        ps = m.exact_batch_topk(np.arange(n, dtype=float)[::-1], np.arange(n), .3)
        def d(delta):
            return float(((pf.astype(float)-ps.astype(float))*delta).mean())
        d_full, d_long = d(f), d(l)
        i = ((pf.astype(float)-ps.astype(float))*(f-l)).mean()
        self.assertAlmostEqual(i, d_full-d_long, places=14)
        self.assertEqual(pf.sum(), ps.sum())
        self.assertEqual((pf & ~ps).sum(), (ps & ~pf).sum())

    def test_user_cluster_ci_is_reproducible(self):
        values = np.array([.1, .2, -.1, .4, .2])
        users = np.array(["a", "a", "b", "c", "c"])
        self.assertEqual(
            m.user_cluster_ci(values, users, 40, 7),
            m.user_cluster_ci(values, users, 40, 7),
        )


if __name__ == "__main__":
    unittest.main()

# Trigger the branch-scoped CI after the workflow definition was added.
