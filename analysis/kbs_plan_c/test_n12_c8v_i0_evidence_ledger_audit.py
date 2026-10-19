import json, tempfile, unittest
from pathlib import Path
from n12_c8v_i0_evidence_ledger_audit import ROOT,check
class I0EvidenceLedgerTests(unittest.TestCase):
    def test_public_record_ledger(self):
        r=check(ROOT)
        self.assertGreaterEqual(r["records"],14)
        self.assertEqual(r["checked_blobs"],r["records"])
    def test_detects_corrupt_source_hash(self):
        obj=json.loads((ROOT/"manuscript/kbs_latex/N12_C8V_REV2_EVIDENCE_LEDGER.json").read_text())
        obj["entries"][0]["source_of_truth"]["git_blob_sha1"]="0"*40
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            dest=root/"manuscript/kbs_latex"
            dest.mkdir(parents=True)
            (dest/"N12_C8V_REV2_EVIDENCE_LEDGER.json").write_text(json.dumps(obj))
            with self.assertRaises(AssertionError):check(root)
    def test_shared_dev_is_not_independent_replication(self):
        obj=json.loads((ROOT/"manuscript/kbs_latex/N12_C8V_REV2_EVIDENCE_LEDGER.json").read_text())
        lookup={x["id"]:x for x in obj["entries"]}
        self.assertEqual(lookup["B1_THREE_ARM_DEV"]["cohort_group"],lookup["G2_E1_SWITCH_ACCOUNTING"]["cohort_group"])
        self.assertEqual(lookup["B4A_H2_NESTED_HISTORY_NULL"]["parent_cohort"],lookup["B4A_H1_NEW_EVENT_ID_SUPERVISION"]["cohort_group"])
    def test_rejects_relabelled_confirmatory_dev(self):
        src=(ROOT/"analysis/kbs_plan_c/n12_c8v_i0_evidence_ledger_audit.py").read_text()
        self.assertIn('assert row["evidence_tier"] in VALID_TIERS',src)
        obj=json.loads((ROOT/"manuscript/kbs_latex/N12_C8V_REV2_EVIDENCE_LEDGER.json").read_text())
        self.assertEqual({x["evidence_tier"] for x in obj["entries"] if x["cohort_group"]=="M3_SHARED_DEV"},{"POST_G5_EXPLORATORY_DEV"})
if __name__=="__main__": unittest.main()
