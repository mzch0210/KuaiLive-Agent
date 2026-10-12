"""E2 comparator manifest and family-isolation invariants."""
import unittest

import numpy as np
import pandas as pd

from g3_fit_dev_gates import (FAMILY_BASE_FEATURES, SHARED_FEATURES,
                              prepare_family_data, evaluate_oof)
from frozen_gate import METHODS


class Tests(unittest.TestCase):
    def test_family_specific_features_only(self):
        n=50049
        d={"event_id":np.arange(n),"user_id":np.arange(n)%137,
           "split":["DEV"]*n,"memory_ndcg10":np.ones(n)*.2,
           "sasrec_ndcg10":np.ones(n)*.4,
           "gru4rec_ndcg10":np.ones(n)*.5}
        d.update({"x_"+x:np.full(n,2.) for x in SHARED_FEATURES})
        for model in ("sasrec","gru4rec"):
            d.update({"x_"+model+"_"+x:np.full(n,1.) for x in FAMILY_BASE_FEATURES})
        src=pd.DataFrame(d)
        a=prepare_family_data(src,"sasrec")
        b=prepare_family_data(src,"gru4rec")
        self.assertEqual(len(a),n)
        self.assertEqual(len(b),n)
        self.assertEqual(a.base_ndcg10.iloc[0],.4)
        self.assertEqual(b.base_ndcg10.iloc[0],.5)
        self.assertTrue("x_base_margin" in a)
        self.assertFalse(any("gru4rec" in k for k in a))

    def test_threshold_ranking_and_zero_call(self):
        d=pd.DataFrame({"base_ndcg10":[.2,.3,.4],
              "memory_ndcg10":[.4,.1,.5],
              **{"score_"+m:[.9,.5,.2] for m in METHODS}})
        methods={m:{"threshold":None,"dev_oof_gain":0.}
                 for m in METHODS}
        methods["utility"]={"threshold":.9,"dev_oof_gain":(.4-.2)/3}
        result=evaluate_oof(d,{"methods":methods},"sasrec")
        self.assertAlmostEqual(result["methods"]["utility"]["dev_oof_gain_over_base"],.2/3)
        self.assertEqual(result["methods"]["history"]["dev_oof_selected_events"],0)

if __name__=="__main__":
    unittest.main()
