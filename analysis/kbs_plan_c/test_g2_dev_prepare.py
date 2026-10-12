"""DEV-only causal context and active author candidate guards, synthetic."""
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
from g2_dev_prepare import extract_dev_contexts, sample_active_author_sets


class G2DevPrepareTest(unittest.TestCase):
    def test_prior_only_context_excludes_same_target_and_test(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            stream=root/"stream.parquet"
            cohort=root/"dev.parquet"
            data={
                "source_event_id":[1,2,3,4,5,6],
                "user_id":[1,1,1,1,2,2],
                "author_id":[10,11,12,13,10,12],
                "split":["TRAIN","TRAIN","DEV","TEST","TRAIN","DEV"]
            }
            pq.write_table(pa.table(data),stream)
            pq.write_table(pa.table({"source_event_id":[3,6]}),cohort)
            contexts,report=extract_dev_contexts(stream,cohort,{10:1,11:2,12:3})
            self.assertEqual(contexts.shape,(2,16))
            self.assertEqual(contexts[0,-2:].tolist(),[1,2])
            self.assertEqual(contexts[1,-1],1)
            self.assertEqual(report["test_split_events_used_for_history"],0)
            self.assertEqual(report["target_contexts_found"],2)

    def test_active_author_half_open_and_reproducible(self):
        t=datetime(2026,3,24,12)
        room=[(t-timedelta(hours=1),t+timedelta(hours=1),id)
               for id in range(1,600)]
        times=[t,t+timedelta(minutes=2)]
        ids=[1,2]
        events=[100,101]
        kwargs=dict(known_to_index={i:i for i in range(1,600)},seed=20261012)
        one,m=sample_active_author_sets(iter(room),times,ids,events,**kwargs)
        two,_=sample_active_author_sets(iter(room),times,ids,events,**kwargs)
        self.assertTrue(np.array_equal(one,two))
        self.assertEqual(one.shape,(2,575))
        self.assertEqual(one[:,0].tolist(),ids)
        self.assertEqual(m["DEV_roster_n_min"],599)
        self.assertTrue(np.all([len(np.unique(row))==575 for row in one]))


if __name__=="__main__":
    unittest.main()
