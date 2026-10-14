#!/usr/bin/env python3
"""No-test-label checks for the B4-A preregistered A4/A5 statistical contract."""
import unittest
import numpy as np
from analysis.kbs_plan_c.n9_b4a_a4_weighted_stat_contract import (
    expected_cell_weights,h2_eventwise_difference,holm3,
    weighted_paired_user_cluster,
)


class A4FrozenStatistics(unittest.TestCase):
    def test_holm_exact_three_family(self):
        p=holm3([.04,.001,.02])
        self.assertTrue(np.allclose(p,[.04,.003,.04]))
        with self.assertRaises(ValueError):holm3([.1,.2])

    def test_weighted_event_ratio_and_user_clusters(self):
        delta=np.array([.2,.2,.5,.5,-.1,-.1,.3,.3],float)
        user=np.array([1,1,2,2,3,3,4,4])
        w=np.array([1,1,4,4,2,2,3,3],float)
        r=weighted_paired_user_cluster(delta,user,w)
        self.assertAlmostEqual(r["weighted_effect"],(.2*2+ .5*8-.1*4+.3*6)/20)
        self.assertEqual(r["n_events"],8)
        self.assertEqual(r["cluster_users"],4)
        self.assertEqual(r["bootstrap_and_null_draws"],5000)
        self.assertTrue(-1<=r["cluster_ci95"][0]<=r["cluster_ci95"][1]<=1)
        self.assertTrue(0<r["one_sided_cluster_signflip_p"]<=1)

    def test_h2_same_event_three_seeds(self):
        actual=np.array([.4,.3])
        null=np.array([[.1,.2,.3],[.1,.1,.4]])
        self.assertTrue(np.allclose(
            h2_eventwise_difference(actual,null),[.2,.1]))
        with self.assertRaises(ValueError):
            h2_eventwise_difference(actual,np.ones((2,4)))

    def test_original_20_cell_poststratification(self):
        cells=[f"d{k//4}_q{k%4+1}" for k in range(20)]
        pop={c:(1000+i) for i,c in enumerate(cells)}
        design={c:10 for c in cells}
        weights=expected_cell_weights(cells,pop,design)
        self.assertTrue(np.allclose(weights,np.array([100+i/10 for i in range(20)])))
        with self.assertRaises(ValueError):
            expected_cell_weights(cells,pop,dict(list(design.items())[:-1]))

    def test_all_nan_zero_weight_and_wrong_bootstrap_rejected(self):
        u=np.array([1,1,2,2])
        d=np.ones(4)
        with self.assertRaises(ValueError):
            weighted_paired_user_cluster(d,u,[1,0,1,1])
        with self.assertRaises(ValueError):
            weighted_paired_user_cluster(d,u,[1,1,1,1],reps=2000)
        with self.assertRaises(ValueError):
            weighted_paired_user_cluster([np.nan,0,0,0],u,[1,1,1,1])


if __name__=="__main__":unittest.main()
