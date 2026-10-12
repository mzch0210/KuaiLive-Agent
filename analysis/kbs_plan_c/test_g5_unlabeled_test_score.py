"""Synthetic-only G5-A causal chronology, author roster and stable top-k tests."""
import unittest,tempfile
from datetime import datetime,timedelta
from pathlib import Path
import numpy as np,pyarrow as pa,pyarrow.parquet as pq
from g5_unlabeled_test_score import histories,active_rosters,stable_top10

class PretestControls(unittest.TestCase):
    def test_strictly_prior_current_target_and_later_test_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"stream.parquet"
            pq.write_table(pa.table({
                "source_event_id":[1,2,3,4,5,6,7],
                "user_id":[7]*5+[8]*2,
                "author_id":[101,999,102,103,104,101,105],
                "split":["TRAIN","DEV","TEST","TEST","TEST","TRAIN","TEST"]}),p)
            snaps,processed=histories(p,np.array([3,4,7],dtype=np.int64),
                                     {101:1,102:2,103:3,104:4,105:5})
            self.assertEqual(processed,7)
            self.assertEqual(snaps[0][0][-1],1)
            self.assertEqual(snaps[0][1],{1:1})
            self.assertEqual(snaps[0][2],(1,0))
            self.assertEqual(snaps[0][3],1)
            self.assertEqual(snaps[1][0][-2:].tolist(),[1,2])
            self.assertEqual(snaps[1][2],(1,0,2))
            self.assertEqual(snaps[1][3],1)
            self.assertEqual(snaps[1][4]["x_hist_event_count"],3)
            with self.assertRaises(ValueError):
                histories(p,np.array([2]),{101:1})
    def test_half_open_roster_dedup_without_current_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"room.parquet"
            t=datetime(2026,3,30,12)
            pq.write_table(pa.table({
                "open_ts":[t-timedelta(hours=2),t-timedelta(hours=1),t-timedelta(hours=1)],
                "close_ts":[t+timedelta(hours=1),t+timedelta(hours=1),t],
                "author_id":[101,101,102]}),p)
            times=[t,t+timedelta(hours=2)]
            out=list(active_rosters(p,times,{101:1,102:2}))
            self.assertEqual(out[0][1].tolist(),[1])
            self.assertEqual(len(out[1][1]),0)
    def test_stable_top10_boundary_ties(self):
        toks=np.arange(1,20,dtype=np.int32)
        sc=np.zeros(19,dtype=np.float64)
        sc[:11]=0.7
        top=stable_top10(toks,sc)
        self.assertEqual(top.tolist(),list(range(1,11)))
        for i in range(10):
            self.assertEqual(top[i],i+1)
        sc[15]=1.0
        top=stable_top10(toks,sc)
        self.assertEqual(top[0],16)
        self.assertEqual(top[-1],9)

if __name__=="__main__":
    unittest.main()
