import math
import unittest
import numpy as np
from g4_sparse_gate_features import sparse_history_support_share,dense_reference_support_share


class SparseParity(unittest.TestCase):
    def test_exact_parity_to_corrected_original_memory(self):
        rng=np.random.default_rng(20261012)
        for n in (3,100,1000,33759):
            author_pool=10*n+50
            eligible=np.sort(rng.choice(np.arange(1,author_pool),size=n,replace=False))
            seen=rng.choice(np.arange(1,author_pool),size=max(1,n//5),replace=False)
            counts={int(t):int(rng.integers(1,12)) for t in seen}
            latest=tuple(int(t) for t in rng.choice(
                        list(counts)+[0]*15,size=10,replace=True))
            p=np.zeros(author_pool,dtype=np.float64)
            p[1:]=rng.random(author_pool-1)
            all_max=max(counts.values())+19
            fast=sparse_history_support_share(eligible,counts)
            slow=dense_reference_support_share(eligible,p,counts,latest,all_max)
            self.assertEqual(fast,slow)

    def test_unknown_authors_consume_slots_but_never_make_extra_warm_candidates(self):
        eligible=np.array([1,2,5,7],dtype=np.int32)
        counts={1:1,2:3,3:8,9:1}
        p=np.zeros(12)
        self.assertEqual(sparse_history_support_share(eligible,counts),.5)
        self.assertEqual(sparse_history_support_share(eligible,{}),0.0)
        with self.assertRaises(ValueError):
            sparse_history_support_share(np.array([2,1]),counts)


if __name__=="__main__":
    unittest.main()
