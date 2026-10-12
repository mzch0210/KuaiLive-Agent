import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from frozen_gate import METHODS, apply_unlabeled, freeze_dev, select_threshold

def write_rows(path, rows, fields):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

class TestFrozenGate(unittest.TestCase):
    def test_threshold_ties_and_zero_calls(self):
        r = select_threshold([9., 9., 8., 4.], [1., 1., 1., -1.], 0.25)
        self.assertEqual(r["calls"], 0)
        self.assertIsNone(r["threshold"])
        s = select_threshold([9., 9., 8., 4.], [1., 1., 1., -1.], 0.5)
        self.assertEqual(s["calls"], 2)
        self.assertEqual(s["threshold"], 9.)

    def test_fit_apply_without_targets(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            dev = root / "dev.csv"
            fields = ["event_id", "split", "base_ndcg10", "memory_ndcg10"]
            fields += ["score_" + m for m in METHODS]
            rows = []
            for i in range(10):
                r = {"event_id": str(i), "split": "DEV",
                     "base_ndcg10": "0.4",
                     "memory_ndcg10": "0.6" if i < 3 else "0.2"}
                r.update({"score_" + m: str(10 - i) for m in METHODS})
                rows.append(r)
            write_rows(dev, rows, fields)
            oof = root / "oof.json"
            oof.write_text(json.dumps({"phase": "DEV", "predictions_are_oof": True,
                         "user_disjoint_across_folds": True,
                         "provenance_sha256": hashlib.sha256(dev.read_bytes()).hexdigest()}))
            policy = root / "policy.json"
            result = freeze_dev(dev, oof, policy, 0.3)
            self.assertEqual(result["methods"]["utility"]["calls"], 3)
            test = root / "test.csv"
            testfields = ["event_id", "split"] + ["score_" + m for m in METHODS]
            testrows = []
            for event, score in (("a", 10), ("b", 0)):
                r = {"event_id": event, "split": "TEST"}
                r.update({"score_" + m: str(score) for m in METHODS})
                testrows.append(r)
            write_rows(test, testrows, testfields)
            out = root / "masks.csv"
            self.assertEqual(apply_unlabeled(policy, test, out), 2)
            with out.open() as f:
                masks = list(csv.DictReader(f))
            self.assertEqual(masks[0]["call_utility"], "1")
            self.assertEqual(masks[1]["call_utility"], "0")
            write_rows(test, [{**r, "memory_ndcg10": "0.3"} for r in testrows],
                       testfields + ["memory_ndcg10"])
            with self.assertRaises(ValueError):
                apply_unlabeled(policy, test, out)

    def test_rejects_non_oof_and_test_fit(self):
        with tempfile.TemporaryDirectory() as d:
            a = Path(d)
            oof = a / "oof.json"
            oof.write_text(json.dumps({"phase": "TEST", "predictions_are_oof": True,
                         "user_disjoint_across_folds": True, "provenance_sha256": "e"*64}))
            with self.assertRaises(ValueError):
                freeze_dev(a / "irrelevant", oof, a / "out.json")

if __name__ == "__main__":
    unittest.main()
