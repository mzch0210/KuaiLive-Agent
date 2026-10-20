"""Exact-public NI-1b tests; no access to event data or models."""
import unittest
from fractions import Fraction
from math import comb
from ni1b_sampled_joint_identifiability import (K, NEGATIVES, RANK_SUPPORT,
    censored_emission_numerators,construct_worlds,solve_kernel_vector)

class IdentifiabilityTest(unittest.TestCase):
    def test_emission_normalizes_exactly(self):
        for N in (14022,53762):
            for rank in RANK_SUPPORT:
                x=censored_emission_numerators(N,rank)
                self.assertEqual(len(x), K+1)
                self.assertEqual(sum(x),comb(N-1,NEGATIVES))
                self.assertTrue(all(t>=0 for t in x))

    def test_exact_observational_equivalence(self):
        for N in (14022,53762):
            cols=[censored_emission_numerators(N,r) for r in RANK_SUPPORT]
            v=solve_kernel_vector(cols)
            self.assertTrue(any(x>0 for x in v) and any(x<0 for x in v))
            self.assertEqual(sum(v),Fraction(0))
            self.assertTrue(all(sum(v[j]*cols[j][i] for j in range(len(v)))==0 for i in range(K+1)))

    def test_full_value_gap(self):
        for N in (14022,53762):
            d=construct_worlds(N)
            self.assertGreater(d['full_utility_absolute_gap'],0.24)
            self.assertAlmostEqual(d['matched_50_percent_call_budget_minimax_regret_lower_bound'],d['full_utility_absolute_gap']/4,places=8)

    def test_guards(self):
        with self.assertRaises(ValueError):construct_worlds(575)
        with self.assertRaises(ValueError):censored_emission_numerators(575,576)

if __name__=='__main__':unittest.main()
