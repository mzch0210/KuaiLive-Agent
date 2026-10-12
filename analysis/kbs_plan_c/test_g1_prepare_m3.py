"""Synthetic G1 protocol test; no network or real/test outcomes."""
import csv
import json
import tempfile
import unittest
from pathlib import Path

import duckdb
from g1_prepare_m3 import prepare


class M3ForwardPrepTest(unittest.TestCase):
    def test_split_eligibility_and_sealed_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root/"source"
            source.mkdir()
            conn = duckdb.connect()
            conn.execute("""
              COPY (
                 SELECT i::BIGINT AS live_id, i::BIGINT AS author_id,
                    TIMESTAMP '2026-03-01 00:00:00' AS start_timestamp,
                    TIMESTAMP '2026-04-01 00:00:00' AS end_timestamp
                 FROM range(1,5) x(i)
              ) TO ? (FORMAT PARQUET)
            """, [str(source/"live_room_meta.parquet")])
            conn.close()
            csvfile = source/"live_interaction.csv"
            rows = []
            for user in range(1,5):
                for t in ("2026-03-20 12:00:00", "2026-03-21 12:00:00",
                          "2026-03-22 12:00:00", "2026-03-24 12:00:00",
                          "2026-03-28 12:00:00"):
                    rows.append([user,user,user,t])
            rows.reverse()  # input deliberately NOT chronologically ordered
            rows.append([9,9,999,"2026-03-28 12:00:00"])  # bad room excluded
            with csvfile.open("w",newline="") as out:
                w=csv.writer(out)
                w.writerow(["user_id","author_id","live_id","live_play_start_timestamp"])
                w.writerows(rows)
            protocol={
                "status":"SCIENTIFIC_DESIGN_PREREGISTERED_TEST_REMAINS_LOCKED",
                "source":{"revision":"synthetic", "inputs":{
                    "live_interaction.csv":"synthetic",
                    "live_room_meta.parquet":"synthetic"}},
                "split":{"dev_start":"2026-03-23T12:00:00",
                         "test_start":"2026-03-27T14:00:00"},
                "cohort":{"seed":20261012,
                          "dev_keep_if_mod_less_than":1000000,
                          "test_keep_if_mod_less_than":1000000},
                "unit":{"min_prior_history":2}
            }
            p=root/"protocol.json"
            p.write_text(json.dumps(protocol))
            out=root/"derived"
            report=prepare(source,p,out,synthetic=True)
            self.assertEqual(report["split_event_counts"],
                             {"TRAIN":12,"DEV":4,"TEST":4})
            self.assertEqual(report["selected_cohort_counts"],{"DEV":4,"TEST":4})
            self.assertEqual(report["known_train_author_count"],4)
            self.assertTrue(report["test_outcomes_inspected"] is False)
            self.assertTrue((out/"test_cohort_sealed.parquet").exists())
            with duckdb.connect() as db:
                chronology=db.execute("SELECT user_id,observed_at,prior_events FROM read_parquet(?)",
                    [str(out/"causal_stream_sealed.parquet")]).fetchall()
            self.assertEqual([x[2] for x in chronology[:5]],[0,1,2,3,4])
            with self.assertRaises(FileExistsError):
                prepare(source,p,out,synthetic=True)


if __name__=="__main__":
    unittest.main()
