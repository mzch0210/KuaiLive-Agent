"""No external data or GPU needed for synthetic G0 unit tests."""
import tempfile
import unittest
from pathlib import Path
from g0_audit import CACHE_NAMES, audit, file_inventory

class TestG0(unittest.TestCase):
    def test_nonrecursive_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "live_interaction.csv").write_text("header\n")
            inv = file_inventory(root)
            self.assertTrue(inv["raw_live_present"])
            self.assertFalse(inv["room_meta_present"])
            self.assertEqual(inv["present_named_files"], ["live_interaction.csv"])

    def test_read_only_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / CACHE_NAMES[0]).mkdir()
            output = audit("hosted", root, root)
            self.assertTrue(output["original_kuailive_cache"]
                            [CACHE_NAMES[0]]["present"])
            self.assertFalse(output["test_accessed"])
            self.assertFalse(output["models_trained"])
            self.assertFalse(output["data_downloaded"])
            self.assertFalse(output["infrastructure_ready"])

if __name__ == "__main__":
    unittest.main()
