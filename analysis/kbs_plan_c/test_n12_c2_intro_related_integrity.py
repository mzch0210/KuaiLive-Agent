import unittest
from pathlib import Path
from n12_c2_intro_related_integrity import check,fnv32,MAIN,OLD_FRONT_UTF16_FNV,OLD_TAIL_UTF16_FNV

ROOT=Path(__file__).resolve().parents[2]
class C2JournalNarrative(unittest.TestCase):
    def test_single_thesis_and_all_prior_results_in_main(self):
        z=check(ROOT)
        self.assertEqual(z["status"],"N12_C2_INTRO_RELATED_WORK_INTEGRATED_PASS")
        self.assertEqual(z["prior_experiment_families_retained_in_main"],10)
        self.assertTrue(z["pre_c2_methods_results_discussion_and_conclusion_unchanged"])
    def test_original_prefix_suffix_are_sealed(self):
        s=(ROOT/MAIN).read_text()
        self.assertEqual(fnv32(s.split(r"\section{Introduction}")[0]),OLD_FRONT_UTF16_FNV)
        self.assertEqual(fnv32(r"\section{Problem Formulation}"+s.split(r"\section{Problem Formulation}",1)[1]),OLD_TAIL_UTF16_FNV)
    def test_branch_diagram_does_not_imply_causal_chain(self):
        s=(ROOT/MAIN).read_text()
        intro=s.split(r"\section{Introduction}",1)[1].split(r"\section{Related Work}",1)[0]
        self.assertEqual(intro.count(r"\draw[arr]"),2)
        self.assertNotIn("(decision.south) -- (source.north)",intro)
    def test_negative_scientific_findings_remain_visible(self):
        s=(ROOT/MAIN).read_text()
        for x in ("0.348744","0.005391","0.003585","0.031145","not verified","1.769","0.692"):
            self.assertIn(x.lower(),s.lower())
if __name__=="__main__":unittest.main()
