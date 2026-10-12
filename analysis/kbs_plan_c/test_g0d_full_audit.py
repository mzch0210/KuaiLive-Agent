"""Synthetic stream unit tests; no KLM3 file is required."""
import csv
import tempfile
import unittest
from pathlib import Path
from g0d_full_audit import audit_events, time_quantiles

class Tests(unittest.TestCase):
    def test_event_matching_and_repeat_indicators(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"interactions.csv"
            with p.open("w",newline="") as f:
                w=csv.writer(f)
                w.writerow(["user_id","author_id","live_id","live_play_start_timestamp",
                            "live_play_end_timestamp"])
                w.writerow([1,10,100,1772582400000,1772582401000])
                w.writerow([1,10,101,1772582402000,1772582404000])
                w.writerow([2,11,200,1772582403000,1772582405000])
            rooms={100:(10,1772582000000,1772582600000),
                   101:(10,1772582000000,1772582600000),
                   200:(11,1772582000000,1772582600000)}
            x=audit_events(p,rooms,sorted(a for _,a,_ in rooms.values()),
                           sorted(c for _,_,c in rooms.values()),
                           report_stride=0,sample_stride=1)
            self.assertEqual(x["events"]["rows"],3)
            self.assertEqual(x["events"]["room_id_matched"],3)
            self.assertEqual(x["unique_users"],2)
            self.assertEqual(x["unique_user_author_pairs"],2)
            self.assertEqual(x["events"]["pair_repeat_ever"],1)
            self.assertEqual(x["events"].get("entry_outside_room_lifecycle",0),0)
            self.assertEqual(x["sampled_exact_live_room_candidates"]["n"],3)
    def test_global_hour_cutoff_descriptive(self):
        x=time_quantiles({100:2,101:3,102:5})
        self.assertEqual(len(x),2)
        self.assertGreaterEqual(x["q85"]["cumulative_event_fraction"],.85)

if __name__=="__main__":
    unittest.main()
