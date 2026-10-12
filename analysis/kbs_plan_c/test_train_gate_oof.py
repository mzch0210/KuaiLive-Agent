"""Synthetic end-to-end DEV OOF test, never downloads a dataset."""
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from train_gate_oof import fit_oof, predict_unlabeled

class TestOOF(unittest.TestCase):
    def test_user_grouped_oof_and_unlabeled_scoring(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            rng = np.random.default_rng(3)
            n=100
            dev = pd.DataFrame({
                "event_id": np.arange(n),
                "user_id": np.repeat(np.arange(n//2), 2),
                "split": ["DEV"] * n,
                "base_ndcg10": rng.uniform(.2, .7, n),
                "memory_ndcg10": rng.uniform(.2, .7, n),
                "x_base_margin": rng.uniform(0, 1, n),
                "x_hist_event_count": rng.integers(0, 10, n),
                "x_hist_recency": rng.uniform(0, 1, n),
            })
            f=p/"dev.csv";dev.to_csv(f,index=False)
            m=fit_oof(f,p/"models")
            self.assertTrue(m["user_disjoint_across_folds"])
            self.assertEqual(m["n_dev_events"],n)
            oof=pd.read_csv(p/"models/dev_oof.csv")
            self.assertEqual(len(oof),n)
            self.assertEqual(oof["score_utility"].notna().sum(),n)
            test=dev.drop(columns=["base_ndcg10","memory_ndcg10","user_id"]).iloc[:5].copy()
            test["split"]="TEST"
            t=p/"test.csv";test.to_csv(t,index=False)
            out=p/"pred.csv"
            self.assertEqual(predict_unlabeled(t,p/"models",out),5)
            self.assertEqual(len(pd.read_csv(out)),5)
            test["memory_ndcg10"]=0.5
            test.to_csv(t,index=False)
            with self.assertRaises(ValueError):
                predict_unlabeled(t,p/"models",out)
if __name__=="__main__":
    unittest.main()
