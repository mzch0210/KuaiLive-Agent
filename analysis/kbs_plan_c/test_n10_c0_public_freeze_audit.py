import ast
import tempfile
import unittest
from pathlib import Path
from n10_c0_public_freeze_audit import git_blob_sha, check, FROZEN_GIT_BLOBS

class AuditSafety(unittest.TestCase):
    def test_frozen_public_baseline(self):
        root=Path(__file__).resolve().parents[2]
        x=check(root,False)
        self.assertEqual(x["status"],"C0_PUBLIC_READ_ONLY_PASS")
        self.assertFalse(x["privacy"]["reran_A4"])
        self.assertFalse(x["H2_popularity_floor_predeclared_verified"])
        self.assertFalse(x["strict_equal_budget_F_vs_S"])

    def test_git_blob_integrity_detects_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"sample.txt"
            p.write_text("original")
            digest=git_blob_sha(p)
            p.write_text("changed")
            self.assertNotEqual(digest,git_blob_sha(p))

    def test_no_private_reads_or_model_fit_in_audit_script(self):
        src=Path(__file__).with_name("n10_c0_public_freeze_audit.py").read_text()
        tree=ast.parse(src)
        calls=[]
        for item in ast.walk(tree):
            if isinstance(item,ast.Call):
                f=item.func
                calls.append(f.attr if isinstance(f,ast.Attribute) else (f.id if isinstance(f,ast.Name) else ""))
        banned={"load","read_parquet","joblib","torch","fit","predict","np","execute","subprocess","system","eval","exec"}
        self.assertFalse(banned.intersection(calls))
        self.assertFalse(any("PRIVATE" in p.upper() or "A4_PRIVATE" in p.upper() for p in FROZEN_GIT_BLOBS))

if __name__ == "__main__":
    unittest.main()
