import json
import unittest
from pathlib import Path
from n12_c5_rq_results_evidence_audit import ROOT,check,BASE,FIX

class N12C5ResultsScience(unittest.TestCase):
    def test_single_thesis_four_question_results(self):
        x=check(ROOT)
        self.assertEqual(x["status"],"N12_C5_RQ_RESULTS_FROZEN_EVIDENCE_AUDIT_PASS")
        self.assertEqual(x["retained_main_tables"],7)
        self.assertEqual(x["migrated_full_supplement_tables"],4)
        self.assertEqual(len(x["one_thesis_four_results_roles"]),4)
    def test_h1_h2_and_adverse_cost_not_deleted(self):
        m=(ROOT/BASE/"main.tex").read_text()
        r=m.split(r"\section{Results}",1)[1].split(r"\section{Discussion}",1)[0]
        for v in ("0.305446","0.304530","0.348744","0.031145",
                  "0.027389","0.035098","1.769","0.692","8,704","9,105"):
            self.assertIn(v,r)
        self.assertIn("not measured and sealed before target reveal",r)
    def test_all_four_prior_exploratory_tables_full_and_traceable(self):
        fx=json.loads((ROOT/FIX).read_text())
        supp=(ROOT/BASE/"SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md").read_text()
        for label in ("tab:results-evidence-states","tab:results-m3-dev-regime-transfer",
                      "tab:results-m3-dev-source","tab:results-feature-ablation"):
            self.assertIn(label,fx["original_latex_tables"])
            self.assertIn(label,supp)
    def test_no_abstract_or_discussion_early_rewrite(self):
        z=check(ROOT)
        self.assertTrue(z["unchanged_N12_C2_C4_prefix"])
        self.assertTrue(z["unchanged_original_discussion_conclusion"])
if __name__=="__main__":
    unittest.main()
