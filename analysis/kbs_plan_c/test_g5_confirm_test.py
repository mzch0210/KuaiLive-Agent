"""G5 one-shot CPU synthetic statistical inference and Holm sanity checks."""
import unittest
import numpy as np
from g5_confirm_test import holm3,group_clustering,ndcg10

class TestFrozenOutcomeScoring(unittest.TestCase):
    def test_ndcg_and_holm(self):
        self.assertTrue(np.allclose(ndcg10(np.array([1,2,10,11])),
          [1,1/np.log2(3),1/np.log2(11),0]))
        adjusted=holm3([.01,.03,.02])
        self.assertTrue(np.allclose(adjusted,[.03,.04,.04]))
        self.assertTrue(np.all(holm3([.7,.6,.5])<=1))
    def test_cluster_signflip_on_known_positive_utility(self):
        groups=np.repeat(np.arange(1050),2)
        draws=np.tile([.15,.20],1050)
        values=np.vstack([draws,np.zeros(len(groups))])
        n,means,lo,hi,p=group_clustering(values,groups,20261012,300)
        self.assertEqual(n,1050)
        self.assertAlmostEqual(means[0],.175)
        self.assertTrue(lo[0]>0 and hi[0]>0)
        self.assertLess(p[0],.05)
        self.assertGreaterEqual(p[1],0)
        self.assertEqual(means[1],0)
if __name__=="__main__":
    unittest.main()
