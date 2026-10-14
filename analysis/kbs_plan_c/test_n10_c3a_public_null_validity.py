import ast,unittest
from pathlib import Path
from n10_c3a_public_null_validity import check,PUBLIC
class C3A(unittest.TestCase):
    def test_public_controls_are_not_silently_equated(self):
        x=check(Path(__file__).resolve().parents[2])
        self.assertEqual(x["status"],"PASS_C3A_PUBLIC_READ_ONLY")
        self.assertTrue(x["B2_DEV"]["popularity_floor_from_exact_same_DEV_cohort"])
        self.assertFalse(x["B4A_H2"]["predeclared_complete_nonfloor_family_verified"])
        self.assertFalse(x["B4A_H2"]["future_period_independent_TEST"])
        self.assertFalse(x["new_A4_author_or_event_labels_read"])
        self.assertEqual(len(x["B2_DEV"]["null_seeds"]),3)
    def test_only_frozen_public_docs_read(self):
        ast.parse(Path(__file__).with_name("n10_c3a_public_null_validity.py").read_text())
        for p,_ in PUBLIC.values():
            self.assertTrue(p.startswith(("experiments/","manuscript/")))
            self.assertNotIn("PRIVATE",p.upper())
if __name__=="__main__":unittest.main()
