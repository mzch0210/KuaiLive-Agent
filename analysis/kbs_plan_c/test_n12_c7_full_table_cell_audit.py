import copy
import json
import unittest
from pathlib import Path
from n12_c7_full_table_cell_audit import ROOT, FIXTURE, MAIN, SUPPLEMENT, check, check_content, TABLES

class C7TableCellTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fx=json.loads((ROOT/FIXTURE).read_text(encoding="utf-8"))
        cls.main=(ROOT/MAIN).read_text(encoding="utf-8")
        cls.supp=(ROOT/SUPPLEMENT).read_text(encoding="utf-8")
    def test_every_source_table_row_and_numeric_cell_matches(self):
        report=check()
        self.assertEqual(report["relocated_tables"],4)
        self.assertEqual(report["original_result_tables"],11)
        self.assertEqual(report["unchanged_main_original_result_tables"],7)
        self.assertEqual(report["relocated_rows"],17)
        self.assertGreaterEqual(report["verified_numeric_cells"],60)
        self.assertTrue(all(x["pass"] for x in report["row_column_cells"]))
    def test_reject_changed_source_numeric_cell(self):
        dirty=self.supp.replace("| Represented | 24,285 | 0.86102 |",
                                     "| Represented | 24,286 | 0.86102 |",1)
        self.assertNotEqual(dirty,self.supp)
        with self.assertRaisesRegex(AssertionError,"cell"):
            check_content(self.fx,self.main,dirty)
    def test_reject_changed_ci_sign(self):
        dirty=self.supp.replace("[−0.02234, −0.01633]","[+0.02234, −0.01633]",1)
        self.assertNotEqual(dirty,self.supp)
        with self.assertRaisesRegex(AssertionError,"cell"):
            check_content(self.fx,self.main,dirty)
    def test_reject_deleted_or_duplicated_rows(self):
        orig="| Long-only | 0.333231 | **0.773602** |"
        self.assertIn(orig,self.supp)
        with self.assertRaises(AssertionError):
            check_content(self.fx,self.main,self.supp.replace(orig,"",1))
        with self.assertRaises(AssertionError):
            check_content(self.fx,self.main,self.supp.replace(orig,orig+"\n"+orig,1))
    def test_reject_label_semantic_change(self):
        dirty=self.supp.replace("| Unavailable in prior history |","| New users |",1)
        self.assertNotEqual(dirty,self.supp)
        with self.assertRaises(AssertionError):
            check_content(self.fx,self.main,dirty)

if __name__=="__main__":
    unittest.main()
