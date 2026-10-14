import json
import unittest
from pathlib import Path
from n12_c4_experimental_design_audit import ROOT,check

class C4DesignIntegrity(unittest.TestCase):
    def test_complete_cohort_and_statistical_protocol(self):
        result=check(ROOT)
        self.assertEqual(result["status"],"N12_C4_EXPERIMENTAL_DESIGN_AUDIT_PASS")
        self.assertEqual(result["old_experimental_labels_preserved"],11)
        self.assertTrue(result["two_original_candidate_equations_unchanged"])
    def test_original_c3_method_math_unchanged(self):
        a=check(ROOT)
        self.assertTrue(a["all_nine_N12_C3_equations_unchanged"])
        self.assertTrue(a["previous_chapters_and_future_results_byte_text_untouched"])
    def test_new_target_not_misrepresented_as_independent_future_test(self):
        src=(ROOT/"manuscript/kbs_latex/main.tex").read_text()
        b=src.split(r"\section{Experimental Design}",1)[1].split(r"\section{Experimental Results}",1)[0]
        self.assertIn("original March 2026 TEST-source collection interval",b)
        self.assertIn("Neither sample is a newly collected later-period TEST",b)
        self.assertIn("was not scored and sealed before the outcome revelation",b)
    def test_older_scientific_controls_retained_in_supplement(self):
        supp=(ROOT/"manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md").read_text()
        self.assertIn("0.021867",supp)
        self.assertIn("NOT VERIFIED",supp)
        self.assertIn("0.69165",supp)
if __name__=="__main__": unittest.main()
