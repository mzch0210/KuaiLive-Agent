"""NI-1e deterministic PUBLIC test suite. No private events, F labels or TEST."""
import unittest
from math import isclose
from ni1e_joint_censored_mixture import (
    STATES, WRONG_STATES, GROUPS, joint_emission, generate_sampled,
    fit_em, summary
)

class NI1eTests(unittest.TestCase):
    def test_shared_negative_joint_emission(self):
        for n,_ in GROUPS:
            for state in STATES+WRONG_STATES:
                prob=joint_emission(n,*state[1:])
                self.assertTrue(isclose(sum(prob.values()),1,abs_tol=1e-12))
                self.assertTrue(all(0<=a<=10 and 0<=b<=10 for a,b in prob))

    def test_probability_input_guards(self):
        with self.assertRaises(ValueError):joint_emission(14022,7,8,30)
        with self.assertRaises(ValueError):joint_emission(14022,0,8,0)
        with self.assertRaises(ValueError):generate_sampled(14022,(.3,.3,.3,.3),100,1)

    def test_sampled_only_fit_valid_weights(self):
        n,w=GROUPS[0]
        label_counts=generate_sampled(n,w,3000,20261020)
        fitted=fit_em(n,label_counts)
        self.assertAlmostEqual(sum(fitted["weights"]),1,places=9)
        self.assertTrue(all(0<=v<=1 for v in fitted["weights"]))

    def test_policy_and_misspecification(self):
        result=summary(repetitions=6,train_per_group=20000,heldout_per_group=4000)
        counts=result["times_chose_truly_best_group_B"]
        self.assertEqual(counts["full_oracle"],6)
        self.assertLessEqual(counts["raw_S"],1)
        self.assertGreaterEqual(counts["correct_family"],5)
        b=result["group_mean"][1]
        self.assertGreater(b["wrong_heldout_sampled_logloss"]-
                           b["correct_heldout_sampled_logloss"],0)
        self.assertGreater(abs(b["wrong_family_eta"]-
                               b["true_eta_generator_only"]),0.025)
        self.assertEqual(result["first_run"]["equal_50pct_group_allocation"]["correct_family"]["calls_per_two_requests"],1)

if __name__=="__main__":
    unittest.main()
