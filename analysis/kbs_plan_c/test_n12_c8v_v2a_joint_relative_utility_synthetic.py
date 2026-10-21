import unittest
from n12_c8v_v2a_joint_relative_utility_synthetic import (
    DRAW, partition_counts, shared_outrank_counts, rank_loss_scenario,
    independent_vs_shared_negative_control, run
)
class V2aJointRelativeUtilityTest(unittest.TestCase):
    def test_partition_exact_ahead_marginals(self):
        for N,b,m,o in ((1000,2,8,0),(1000,2,8,1),(14022,12,7,0),
                         (53762,30,60,29)):
            z=partition_counts(N,b,m,o)
            self.assertEqual(sum(z),N-1)
            self.assertEqual(z[0]+z[1],b-1)
            self.assertEqual(z[0]+z[2],m-1)
    def test_invalid_overlap_fails(self):
        with self.assertRaises(ValueError):partition_counts(1000,2,8,2)
    def test_same_set_nested_rank_direction(self):
        p=partition_counts(1000,2,8,1)
        xb,xm=shared_outrank_counts(list(range(574)),p)
        self.assertLessEqual(xb,xm)
    def test_equal_identical_ranks_and_ahead_sets_produce_zero_delta(self):
        s=rank_loss_scenario(14022,8,8,7,repeats=128)
        for r in s["methods"].values():
            self.assertEqual(r["mse"],0)
            self.assertEqual(r["toy_allocation_regret"],0)
    def test_different_overlap_same_marginal_ranks(self):
        a=rank_loss_scenario(14022,8,8,0,repeats=256)
        b=rank_loss_scenario(14022,8,8,7,repeats=256)
        self.assertNotEqual(a["methods"]["original_s"]["mse"],b["methods"]["original_s"]["mse"])
    def test_shared_negative_control_cannot_reverse_nested_order(self):
        x=independent_vs_shared_negative_control(14022,512)
        self.assertEqual(x["shared_false_memory_preference"],0)
        self.assertGreater(x["independent_false_memory_preference"],0)
    def test_results_are_deterministic(self):
        a=rank_loss_scenario(14022,2,8,0,repeats=128)
        b=rank_loss_scenario(14022,2,8,0,repeats=128)
        self.assertEqual(a,b)
    def test_report_scope(self):
        x=run()
        self.assertEqual(x["scenario_count"],32)
        self.assertIn("PUBLIC_SYNTHETIC",x["scope"])
        self.assertIn("not authorized",x["limitations"].lower())
if __name__=="__main__":unittest.main()
