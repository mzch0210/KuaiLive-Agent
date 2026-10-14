import unittest
from pathlib import Path
from n10_c6_claim_citation_audit import validate
class C6Claims(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=Path(__file__).resolve().parents[2]/"manuscript/kbs_latex"
        cls.main=(p/"main.tex").read_text()
        cls.bib=(p/"kbs_references.bib").read_text()
        cls.supp=(p/"SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md").read_text()
    def test_full_citation_claims_pass(self):
        x=validate(self.main,self.bib,self.supp)
        self.assertEqual(x["status"],"N10_C6_STATIC_CLAIM_CITATION_PASS")
        self.assertFalse(x["manuscript_author_declarations_human_verified"])
    def test_missing_reference_fails(self):
        with self.assertRaises(AssertionError):
            validate(self.main.replace(r"\cite{zhong2026samd}",r"\cite{not_a_real_2026_kbs_work}"),self.bib,self.supp)
    def test_missing_unverified_r3_floor_fails(self):
        with self.assertRaises(AssertionError):
            validate(self.main,self.bib,self.supp.replace("NOT VERIFIED","COMPLETELY PASSED"))
if __name__=="__main__":unittest.main()
