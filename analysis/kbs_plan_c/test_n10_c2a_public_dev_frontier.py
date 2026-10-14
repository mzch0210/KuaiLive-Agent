import ast
import unittest
from pathlib import Path
from n10_c2a_public_dev_frontier import calc

ROOT=Path(__file__).resolve().parents[2]
class TestC2APublic(unittest.TestCase):
    def test_exact_frozen_frontier_and_negative_reference(self):
        r=calc(ROOT)
        self.assertEqual(r["status"],"C2A_PUBLIC_DEV_FRONTIER_READ_ONLY_PASS")
        self.assertTrue(r["gate_overhead_assumed_zero_in_source"])
        self.assertFalse(r["production_latency_or_cost_measured"])
        self.assertFalse(r["B4A_reopened"])
        for family in ("sasrec","gru4rec"):
            p=r["families"][family]
            self.assertLess(p["fixed_30_inner_DEV_F_NDCG"],p["always_memory_DEV_F_NDCG"])
            self.assertGreater(p["full_memory_minus_30_quality"],.03)
            self.assertGreater(p["break_even_lambda_ndcg_per_memory_call"],.05)
            self.assertIn("Always Memory",
                [item["policy"] for item in p["quality_vs_calls_pareto_archived_policies"]])
    def test_only_public_read_only_python_imports(self):
        src=Path(__file__).with_name("n10_c2a_public_dev_frontier.py").read_text()
        tree=ast.parse(src)
        imports=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            if isinstance(node,ast.ImportFrom):
                imports.add((node.module or "").split(".")[0])
        self.assertEqual(imports,{"__future__","argparse","hashlib","json","pathlib"})
if __name__=="__main__":unittest.main()
