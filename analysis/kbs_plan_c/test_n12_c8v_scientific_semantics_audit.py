import unittest
from pathlib import Path
from n12_c8v_scientific_semantics_audit import ROOT, MANUSCRIPT, SUPPLEMENT, REFERENCES, HIGHLIGHTS, audit_text

class ScientificSemanticsV0Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main=(ROOT/MANUSCRIPT).read_text()
        cls.supp=(ROOT/SUPPLEMENT).read_text()
        cls.bib=(ROOT/REFERENCES).read_text()
        cls.highlights=(ROOT/HIGHLIGHTS).read_text()

    def check(self,main):
        return audit_text(main,self.supp,self.bib,self.highlights)

    def test_real_manuscript(self):
        self.assertEqual(self.check(self.main)["status"],
                         "N12_C8V_V0_SEMANTIC_SOURCE_AUDIT_PASS")

    def test_reject_wrong_abstract_denominator(self):
        s=self.main.replace("21.32\\% (SASRec) and 23.01\\% (GRU4Rec) of requests",
                            "21--23\\% of Memory invocations",1)
        self.assertNotEqual(s,self.main)
        with self.assertRaises(AssertionError):self.check(s)

    def test_reject_wrong_dev_denominator_count(self):
        s=self.main.replace("50,049 requests find different Memory-use decisions",
                            "15,016 requests trace this consequence",1)
        self.assertNotEqual(s,self.main)
        with self.assertRaises(AssertionError):self.check(s)

    def test_reject_changed_h1_call_count(self):
        s=self.main.replace("SASRec 8,704 versus 9,105",
                            "SASRec 8,705 versus 9,105",1)
        self.assertNotEqual(s,self.main)
        with self.assertRaises(AssertionError):self.check(s)

    def test_reject_h2_unverified_control_disappearing(self):
        s=self.main.replace(
            "was \\emph{not measured and sealed before target reveal}",
            "was fully verified before target reveal",1)
        self.assertNotEqual(s,self.main)
        with self.assertRaises(AssertionError):self.check(s)

    def test_reject_dev_as_h1_mechanism(self):
        s=self.main.replace(
            "not a causal decomposition of the separate additional 30,000-target policy contrast",
            "a causal decomposition of the separate additional 30,000-target policy contrast",1)
        self.assertNotEqual(s,self.main)
        with self.assertRaises(AssertionError):self.check(s)

if __name__=="__main__": unittest.main()
