"""Scientific Memory-component invariance tests against all historical events."""
import unittest
import math
import tempfile
from pathlib import Path
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from g3_replay_correct_memory import corrected_memory_score,replay_all_history,rank


class TestMemoryCorrected(unittest.TestCase):
    def test_unknown_author_consumes_recency_slot(self):
        # Source sequence: known author 1, unknown, then target known 1.
        # Last known occurrence is at distance ONE (not ZERO).
        pop=np.array([0.,0.,0.])
        s=corrected_memory_score(np.array([1,2],dtype=np.int32),pop,
               {1:1},(1,0),1)
        self.assertAlmostEqual(float(s[0]),.45*.5+.45*math.exp(-1/3))
        self.assertAlmostEqual(float(s[1]),0.)
        self.assertEqual(rank(np.array([1,2],dtype=np.int32),s,1),1)

    def test_unknown_author_counts_in_long_normalizer(self):
        pop=np.array([0.,0.,0.])
        a=corrected_memory_score(np.array([1,2],dtype=np.int32),pop,
                                  {1:1},(),5)
        self.assertAlmostEqual(float(a[0]),.45/5.)

    def test_read_only_replay_excludes_test_and_target_from_memory(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'all.parquet'
            pq.write_table(pa.table({
              'source_event_id':[1,2,3,4,5],
              'user_id':[10,10,10,10,10],
              'author_id':[101,999,999,101,101],
              'split':['TRAIN','TRAIN','DEV','DEV','TEST']}),path)
            snap,processed=replay_all_history(path,np.array([4]),{101:1})
            self.assertEqual(processed,4)
            counts,recent,maximum=snap[0]
            self.assertEqual(counts,{1:1})
            self.assertEqual(recent,(1,0,0))
            self.assertEqual(maximum,2)


if __name__=="__main__":
    unittest.main()
