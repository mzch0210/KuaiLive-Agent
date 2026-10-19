import math
import unittest
from n12_c8v_v2a_corrected_s_rank_mapping_stress import (
    DRAW,K,N_RANGE,METHODS,score,decode_observed_sampled_scalar,
    sampled_scalar_from_outrank,corrected_s_rank_expand_from_scalar,
    uniform_prior_posterior_from_scalar,hypergeom_pmf,expanded_rank,
    conditional_quality,synthetic_mixture,RANK_MIXTURES,run
)

class CorrectedSSyntheticStress(unittest.TestCase):
    def test_sampled_scalar_preserves_necessary_top10_information(self):
        for x in range(K):
            self.assertEqual(decode_observed_sampled_scalar(sampled_scalar_from_outrank(x)),x)
        for x in (K,K+1,574):
            self.assertIsNone(decode_observed_sampled_scalar(sampled_scalar_from_outrank(x)))
            for N in N_RANGE:
                self.assertEqual(corrected_s_rank_expand_from_scalar(0.0,N),0.0)
                self.assertEqual(uniform_prior_posterior_from_scalar(0.0,N),0.0)
    def test_bad_ndcg_rejected(self):
        for val in (-.01,.12345,1.2,float("nan")):
            with self.assertRaises(ValueError):
                decode_observed_sampled_scalar(val)
    def test_hypergeom_marginals(self):
        for N in (575,585,14022,53762):
            for R in (1,2,10,12,200):
                if R>N:continue
                s=sum(hypergeom_pmf(N,R,DRAW,k) for k in range(DRAW+1))
                self.assertAlmostEqual(s,1.,places=7)
    def test_full_roster_parity(self):
        N=575
        for R in (1,2,5,10,11,50,575):
            observed=sampled_scalar_from_outrank(R-1)
            self.assertAlmostEqual(corrected_s_rank_expand_from_scalar(observed,N),score(R),places=10)
            self.assertAlmostEqual(uniform_prior_posterior_from_scalar(observed,N),score(R),places=8)
    def test_rank_expansion_is_mean_unbiased_but_not_ndcg(self):
        N=14022
        R=12
        expected=(1+(N-1)*(DRAW*(R-1)/(N-1))/DRAW)
        self.assertAlmostEqual(expected,R)
        mapped=conditional_quality(N,R)
        self.assertEqual(score(R),0.0)
        self.assertGreater(mapped["original_s"]["mean"],0.0)
        self.assertGreater(mapped["rank_expansion"]["mean"],0.0)
        self.assertGreater(mapped["rank_expansion"]["mse"],0.0)
    def test_two_prior_regimes_are_not_identical(self):
        a=synthetic_mixture(14022,RANK_MIXTURES["synthetic_top_heavy"])
        b=synthetic_mixture(14022,RANK_MIXTURES["synthetic_tail_heavy"])
        self.assertNotEqual(a["true_mean"],b["true_mean"])
        for scenario in (a,b):
            for m in METHODS:
                self.assertGreaterEqual(scenario["methods"][m]["mse"],0.)
    def test_posterior_bayes_identity_uniform_rank_prior(self):
        # Marginal rank of one uniformly random catalog target in an n+1
        # sampled roster is exactly uniform: P(X=k)=1/(n+1).
        N=575
        for x in (0,1,9):
            target=(DRAW+1)/N * sum(score(r)*hypergeom_pmf(N,r,DRAW,x) for r in range(1,K+1))
            self.assertAlmostEqual(uniform_prior_posterior_from_scalar(sampled_scalar_from_outrank(x),N),
                                   target,places=10)
    def test_public_report_scope(self):
        d=run()
        self.assertTrue("synthetic" in d["selection"].lower())
        self.assertEqual(set(d["experiments"]),set(str(n) for n in N_RANGE))
        self.assertIn("not authorized",d["limitations"].lower())
if __name__=="__main__":
    unittest.main()
