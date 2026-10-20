import unittest
from pathlib import Path
from n12_c8v_i2_path_a_claim_audit import check, check_text, ROOT, BASE

class PathAPaperContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main=(ROOT/BASE/"main.tex").read_text()
        cls.bib=(ROOT/BASE/"kbs_references.bib").read_text()

    def test_claim_bibliography_contract(self):
        self.assertEqual(check()["status"],
                         "I2_PATH_A_PRIOR_CORRECTION_AND_SCOPED_CLAIMS_PASS")

    def test_missing_prior_art_detected(self):
        with self.assertRaises(AssertionError):
            check_text(self.main.replace(r"\cite{subbiah2024rankestimation}","",1),self.bib)

    def test_false_corrected_s_claim_detected(self):
        with self.assertRaises(AssertionError):
            check_text(self.main.replace("not a sampled-only statistical correction",
                                         "a sampled-only statistical correction",1),self.bib)

    def test_missing_remaining_alternative_detected(self):
        with self.assertRaises(AssertionError):
            check_text(self.main.replace("cannot rule out that alternative",
                                         "have ruled out that alternative",1),self.bib)

    def test_reference_corruption_detected(self):
        with self.assertRaises(AssertionError):
            check_text(self.main,self.bib.replace("10.1145/3627673.3679943",
                                                 "10.1145/not-correct"))

if __name__=="__main__":
    unittest.main()
