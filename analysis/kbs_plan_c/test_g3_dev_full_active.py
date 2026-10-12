"""G3 DEV-only fixed Memory and causal availability regression tests."""
import math
import tempfile
import unittest
from pathlib import Path
from datetime import datetime,timedelta

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from g3_dev_full_active import score_history,memory_rank,author_availability,build_dev_histories,ndcg


class TestFixedMemory(unittest.TestCase):
    def test_component_weights_and_ties(self):
        pop=np.array([0.0,.2,.5,.1,.8])
        roster=np.array([1,2,3,4],dtype=np.int32)
        score=score_history(roster,pop,{2:4,4:2},(2,4,2))
        self.assertAlmostEqual(score[1],.10*.5+.45*1+.45*1,places=10)
        self.assertAlmostEqual(score[3],
          .10*.8+.45*math.exp(-1/3)+.45*(2/4),places=10)
        self.assertEqual(memory_rank(roster,score,2),1)
        self.assertEqual(memory_rank(np.array([1,2,3]),
                                    np.array([.5,.5,.3]),2),2)
        self.assertEqual(ndcg(1),1.0)
        self.assertEqual(ndcg(11),0.0)

    def test_causal_dev_history_no_current_label_or_test(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"chronology.parquet"
            pq.write_table(pa.table({
                "source_event_id":[1,2,3,4,5,6],
                "user_id":[1,1,1,1,2,2],
                "author_id":[10,11,10,13,11,11],
                "split":["TRAIN","TRAIN","DEV","TEST","TRAIN","DEV"]}),path)
            hist,features,count=build_dev_histories(path,np.array([3,6]),
                                                   {10:1,11:2,13:3},stride=0)
            self.assertEqual(hist[0][0],{1:1,2:1})
            self.assertEqual(hist[0][1],(1,2))
            self.assertEqual(features[0]["hist_events_all"],2)
            self.assertEqual(hist[1][0],{2:1})
            self.assertEqual(count,5)

    def test_room_candidate_eligibility_half_open_and_author_dedup(self):
        with tempfile.TemporaryDirectory() as tmp:
            t=datetime(2026,3,24,12)
            path=Path(tmp)/"rooms.parquet"
            pq.write_table(pa.table({
                "open_ts":[t-timedelta(hours=1),t-timedelta(hours=2),
                           t-timedelta(hours=1),t+timedelta(hours=1)],
                "close_ts":[t+timedelta(hours=1),t+timedelta(hours=2),
                            t,t+timedelta(hours=2)],
                "author_id":[10,10,11,12]}),path)
            values=list(author_availability(path,[t],
                   np.array([1]),{10:1,11:2,12:3}))
            self.assertEqual(len(values),1)
            self.assertEqual(values[0][1].tolist(),[1])

if __name__=="__main__":
    unittest.main()
