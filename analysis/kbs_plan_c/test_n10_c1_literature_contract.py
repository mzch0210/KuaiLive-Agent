import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BIB=ROOT/"manuscript/kbs_latex/kbs_references.bib"
MATRIX=ROOT/"manuscript/kbs_latex/N10_C1_KBS_NOVELTY_BOUNDARY_MATRIX_2026-10-14.md"

class C1LiteratureContract(unittest.TestCase):
    def test_publisher_verified_samd_metadata(self):
        text=BIB.read_text()
        record=re.search(r'@article\{zhong2026samd,.*?^\}',text,re.S|re.M)
        self.assertIsNotNone(record)
        r=record.group()
        for token in (
            'Zhong, Yijie','Guo, Mengying','Wang, Zewei','Li, Zhongyang',
            'Tu, Dandan','Wang, Haofen',
            'Scene-aware memory discrimination: Deciding which personal knowledge stays',
            'Knowledge-Based Systems','338','115496','2026',
            '10.1016/j.knosys.2026.115496'
        ):
            self.assertIn(token,r)
        self.assertEqual(len(re.findall(r'@article\{zhong2026samd',text)),1)

    def test_five_near_neighbor_research_boundaries(self):
        x=MATRIX.read_text()
        for name in ("SAMD","MHGFCL","DS-Frame","Krichene","learning-to-defer","P1","P2","P3"):
            self.assertIn(name,x)
        for bounded in ("0.005391","0.003585","0.031145",
                        "0.348744","NOT VERIFIED","1.337","1.797"):
            self.assertIn(bounded,x)

    def test_c1_is_positioning_not_premature_main_rewrite(self):
        x=MATRIX.read_text()
        self.assertIn("draft for C5",x)
        self.assertIn("not yet inserted",x)
        self.assertIn("not additional experiments",x)

if __name__=="__main__":
    unittest.main()
