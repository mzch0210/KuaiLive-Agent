import unittest
from n12_c8v_v2a_sampled_rank_identifiability import (
    hypergeom_sample_outrank_pmf as pmf, full_ndcg, sampled_topk_probability as ptop,
    expected_sampled_ndcg as es, no_universal_design_unbiased_from_sampled_rank as impossible)
class SampledRankV2a(unittest.TestCase):
    def test_hypergeom_normalizes(self):
        for r in (1,5,11,12,20,50,100,500):
            self.assertAlmostEqual(sum(pmf(1000,r,574,k) for k in range(575)),1.,places=12)
    def test_full_rank_12_can_look_relevant_in_sample(self):
        self.assertEqual(full_ndcg(12),0)
        self.assertAlmostEqual(ptop(1000,12),.9799134942781722,places=10)
        self.assertAlmostEqual(es(1000,12),.32849505251347333,places=10)
    def test_exact_sample_matches_all_candidates(self):
        for r in (1,5,10,11,99,575):
            self.assertAlmostEqual(es(575,r,574),full_ndcg(r),places=10)
    def test_root_count_boundaries(self):
        self.assertFalse(impossible(584))
        self.assertTrue(impossible(585))
        self.assertTrue(impossible(1000))
    def test_invalid_source(self):
        with self.assertRaises(ValueError):pmf(100,101,50,1)
if __name__=="__main__":unittest.main()
