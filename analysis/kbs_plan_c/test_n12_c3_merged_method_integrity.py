import unittest
from pathlib import Path
from n12_c3_merged_method_integrity import check,ROOT,MAIN,FIXTURE

class N12C3(unittest.TestCase):
    def test_merged_method_preserves_every_scientific_equation_and_old_labels(self):
        a=check(ROOT)
        self.assertEqual(a["status"],"N12_C3_MERGED_METHOD_SCIENTIFIC_AND_SOURCE_QA_PASS")
        self.assertEqual(a["frozen_original_equations_preserved_exactly"],9)
        self.assertEqual(a["original_method_reference_labels_preserved"],22)
    def test_outcome_blind_pretarget_and_memory_weights(self):
        p=(ROOT/MAIN).read_text()
        m=p.split(r"\section{Knowledge Valuation and Selective Use}",1)[1].split(r"\section{Experimental Setup}",1)[0]
        self.assertIn("0.45",m)
        self.assertIn("0.10",m)
        self.assertIn("never",m)
        self.assertIn("not guarantee an identical realized fraction",m)
        self.assertIn("retrospectively constructed sampled",m)
    def test_old_two_method_sections_absent(self):
        p=(ROOT/MAIN).read_text()
        self.assertNotIn(r"\section{Problem Formulation}",p)
        self.assertNotIn(r"\section{Base-Relative Evidence Valuation Framework}",p)
        self.assertIn(r"\section{Knowledge Valuation and Selective Use}",p)
    def test_immutable_fixture_has_nine_exact_equations(self):
        import json
        f=json.loads((ROOT/FIXTURE).read_text())
        self.assertEqual(len(f["original_equations"]),9)
        self.assertEqual(len(f["original_method_labels"]),22)
if __name__=="__main__": unittest.main()
