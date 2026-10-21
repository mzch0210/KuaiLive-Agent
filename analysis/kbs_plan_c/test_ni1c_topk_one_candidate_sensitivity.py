"""PUBLIC NI-1c tests: structured near-indistinguishability, no private M3 data."""
import unittest
from fractions import Fraction
from math import log2
from ni1c_topk_one_candidate_sensitivity import model

class TestTopKBoundary(unittest.TestCase):
    def test_detection_exact(self):
        for N in (14022,53762):
            r=model(N)
            self.assertEqual(r['exact_TV_joint_sample_observations'],float(Fraction(574,N-1)))
            self.assertAlmostEqual(r['probability_of_sampled_agreement']+r['probability_of_observable_sampled_disagreement'],1)
    def test_value_flip(self):
        for N in (14022,53762):
            r=model(N)
            self.assertAlmostEqual(r['world_plus_full_delta'],1/log2(11))
            self.assertAlmostEqual(r['world_minus_full_delta'],-1/log2(11))
            self.assertGreater(r['expected_sampled_delta_in_positive_world'],0)
            self.assertLess(r['expected_sampled_delta_in_negative_world'],0)
    def test_repeated_detection(self):
        for N in (14022,53762):
            r=model(N,repeats=50)
            self.assertAlmostEqual(r['two_world_equal_prior_minimax_sign_error_lower_bound'],r['probability_no_disagreement_in_independent_repeats']/2)
    def test_input_guards(self):
        for kwargs in ({'N':575,'n':574,'repeats':0},{'N':100,'n':101},{'N':9}):
            with self.assertRaises(ValueError):model(**kwargs)

if __name__ == '__main__':unittest.main()
