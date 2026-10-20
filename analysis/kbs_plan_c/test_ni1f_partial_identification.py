"""NI-1f public finite-library partial identification QA."""
import unittest
from ni1f_partial_identification import N_VALUES, TRUE_MIXTURE, LIBRARY, emission, evaluate, sampled_noise

class NI1fTests(unittest.TestCase):
    def test_joint_shared_negative_mass(self):
        for N in N_VALUES:
            for s in LIBRARY:
                pmf=emission(N,*s[1:])
                self.assertAlmostEqual(sum(pmf.values()),1,places=11)
                self.assertTrue(all(0<=a<=10 and 0<=b<=10 for a,b in pmf))
    def test_generator_inside_lp_envelope(self):
        for N,p in zip(N_VALUES,TRUE_MIXTURE):
            r=evaluate(N,p)
            self.assertEqual(r['matrix_rank_at_abs_1e_minus_12'],len(LIBRARY))
            for v in r['envelopes']:
                self.assertLessEqual(v['lower'],r['generator_only_true_full_delta']+2e-5)
                self.assertGreaterEqual(v['upper'],r['generator_only_true_full_delta']-2e-5)
                self.assertLessEqual(v['lower_witness']['actual_tv'],v['TV_radius']+1e-6)
                self.assertLessEqual(v['upper_witness']['actual_tv'],v['TV_radius']+1e-6)
    def test_width_expands_under_more_tolerance(self):
        for N,p in zip(N_VALUES,TRUE_MIXTURE):
            a=evaluate(N,p)['envelopes']
            self.assertTrue(all(a[i]['width']<=a[i+1]['width']+1e-6 for i in range(len(a)-1)))
    def test_sampling_noise_declines_with_n(self):
        for N,p in zip(N_VALUES,TRUE_MIXTURE):
            a=sampled_noise(N,p)
            self.assertGreater(a[0]['median_empirical_TV'],a[-1]['median_empirical_TV'])
    def test_guards(self):
        with self.assertRaises(ValueError):emission(574,3,8,2)
        with self.assertRaises(ValueError):emission(14022,3,8,7)

if __name__=='__main__':unittest.main()
