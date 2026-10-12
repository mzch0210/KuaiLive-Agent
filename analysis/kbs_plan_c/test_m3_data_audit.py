import csv
import tempfile
import unittest
from pathlib import Path
from m3_data_audit import audit_interaction_header

class M3DataAuditTest(unittest.TestCase):
    def test_header_and_sample(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"live_interaction.csv"
            with f.open("w",newline="") as p:
                w=csv.writer(p)
                w.writerow(["user_id","author_id","live_id","live_play_start_timestamp"])
                w.writerow([1,2,3,12345])
                w.writerow([4,5,6,12347])
            a=audit_interaction_header(f)
            self.assertEqual(a["audited_sample_rows"],2)
            self.assertEqual(a["required_values_missing_in_sample"],0)
            self.assertFalse(a["full_file_scan"])
    def test_missing_required_field(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bad.csv";p.write_text("user_id,live_id\n1,2\n")
            with self.assertRaises(ValueError):
                audit_interaction_header(p)
if __name__=="__main__":
    unittest.main()
