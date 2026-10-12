"""G4 synthetic alignment and model rank-score tests, no M3/TEST read."""
import unittest
import numpy as np
import torch
from g2_train_base import Encoder
from g4_extra_seed_full_dev import score_block,SEEDS,FAMILIES

class ExtraSeedScoreTests(unittest.TestCase):
    def test_candidate_identity_and_memory_preservation(self):
        self.assertTrue(torch.cuda.is_available(),"Runs only in guarded 3090 User-host workflow")
        models={}
        reps={}
        for seed in SEEDS:
            for family in FAMILIES:
                m=Encoder(25,family).cuda().eval()
                models[(seed,family)]=m
                with torch.inference_mode():
                    reps[(seed,family)]=m(torch.tensor([[0]*14+[1,2]],device="cuda")).cpu().numpy()
        candidate=np.arange(1,21,dtype=np.int32)
        state={
            "models":models,"reps":reps,
            "id":np.array([55]),"pos":np.array([2]),
            "users":np.array([19]),
            "old_rows":{55:{"event_id":"55","user_id":"19",
                            "candidate_count":"20",
                            "memory_ndcg10":"0.8"}}}
        results=score_block([(0,candidate)],state)
        self.assertEqual(set(results),set(SEEDS))
        for seed in SEEDS:
            self.assertEqual(set(results[seed][0]),set(FAMILIES))
            for family in FAMILIES:
                r=results[seed][0][family]
                self.assertGreaterEqual(r["rank"],1)
                self.assertLessEqual(r["rank"],20)
                self.assertTrue(np.isfinite(r["base_std"]))
        self.assertEqual(state["old_rows"][55]["memory_ndcg10"],"0.8")
    def test_candidate_set_mismatch_is_error(self):
        model=Encoder(25,"gru4rec").cuda().eval()
        state={"models":{(SEEDS[0],"gru4rec"):model},
               "reps":{(SEEDS[0],"gru4rec"):np.ones((1,64),np.float32)},
               "id":np.array([55]),"pos":np.array([2]),"users":np.array([19]),
               "old_rows":{55:{"event_id":"55","user_id":"19",
                                "candidate_count":"19"}}}
        with self.assertRaises(ValueError):
            score_block([(0,np.arange(1,21,dtype=np.int32))],state)

if __name__=="__main__":
    unittest.main()
