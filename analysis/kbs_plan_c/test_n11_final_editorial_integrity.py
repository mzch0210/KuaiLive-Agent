import unittest
from pathlib import Path
from n11_final_editorial_integrity import parse,PAPER

ROOT=Path(__file__).resolve().parents[2]
class N11Editorial(unittest.TestCase):
    def test_paper_has_all_frozen_and_prior_changes(self):
        x=parse(ROOT)
        self.assertEqual(x["status"],"N11_FINAL_EDITORIAL_SOURCE_AUDIT_PASS")
        self.assertEqual(len(x["prior_N9_N10_modifications_covered_in_main"]),10)
        self.assertFalse(x["unresolved_latex_refs"])
    def test_source_only_cannot_read_private_rows(self):
        x=Path(__file__).with_name("n11_final_editorial_integrity.py").read_text()
        self.assertNotIn("read_parquet(",x)
        self.assertNotIn("private_models/",x)
        self.assertNotIn("A4_PRIVATE",x)
        self.assertNotIn("joblib.load(",x)
    def test_no_project_phase_labels_in_article(self):
        paper=(ROOT/PAPER).read_text()
        for x in ("B4-A","G5","B2 DEV and","post-G5"):
            self.assertNotIn(x,paper)
if __name__=="__main__":unittest.main()
