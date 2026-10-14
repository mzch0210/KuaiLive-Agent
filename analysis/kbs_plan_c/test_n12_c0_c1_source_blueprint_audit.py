import ast
import json
import unittest
from pathlib import Path
from n12_c0_c1_source_blueprint_audit import check,js_fnv32,MAP

ROOT=Path(__file__).resolve().parents[2]
class N12C0C1PreEditTests(unittest.TestCase):
    def test_frozen_baseline_and_full_mapping(self):
        result=check(ROOT)
        self.assertEqual(result["status"],"N12_C0_C1_PREEDIT_AUDIT_PASS")
        self.assertEqual(result["mapped_source_blocks"],152)
        self.assertEqual(result["mapped_unique_latex_labels"],59)
        self.assertEqual(result["mapped_main_tables"],13)
        self.assertFalse(result["original_private_A4_labels_accessed"])
        self.assertFalse(result["source_main_modified"])
    def test_robust_utf16_fingerprint(self):
        self.assertEqual(js_fnv32("abc"),"1a47e90b")
        self.assertEqual(js_fnv32("abc"),js_fnv32("abc"))
        self.assertNotEqual(js_fnv32("abc"),js_fnv32("abd"))
    def test_all_thirteen_table_fates_covered(self):
        manifest=json.loads((ROOT/MAP).read_text())
        table=[b for b in manifest["blocks"] if any(x.startswith("tab:") for x in b["labels"])]
        self.assertEqual(len(table),13)
        self.assertTrue(all(b["new_location"].strip() for b in table))
        self.assertTrue(any(b["edit"]=="MOVE_TO_SUPPLEMENT" for b in table))
    def test_no_private_label_or_scoring_imports(self):
        code=Path(__file__).with_name("n12_c0_c1_source_blueprint_audit.py").read_text()
        tree=ast.parse(code);imports=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(z.name.split(".")[0] for z in n.names)
            if isinstance(n,ast.ImportFrom):imports.add((n.module or "").split(".")[0])
        self.assertEqual(imports,{"__future__","argparse","hashlib","json","re","pathlib"})
if __name__=="__main__":
    unittest.main()
