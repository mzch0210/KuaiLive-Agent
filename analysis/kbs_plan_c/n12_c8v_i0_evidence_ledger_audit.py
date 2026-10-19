#!/usr/bin/env python3
"""I0: public-source provenance integrity, independence and study deduplication."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LEDGER=ROOT/"manuscript/kbs_latex/N12_C8V_REV2_EVIDENCE_LEDGER.json"
VALID_TIERS={"ORIGINAL_TEST","ORIGINAL_RETROSPECTIVE_PAIRED","FROZEN_ONE_SHOT_TEST","FROZEN_ADDITIONAL_SAME_PERIOD_TEST","FROZEN_NESTED_SAME_PERIOD_TEST","POST_G5_EXPLORATORY_DEV","POST_G5_DEV_TIMING"}
def check(root=ROOT):
    obj=json.loads((root/"manuscript/kbs_latex/N12_C8V_REV2_EVIDENCE_LEDGER.json").read_text())
    records=obj["entries"]
    assert len(records)>=14 and len(set(e["id"] for e in records))==len(records)
    groups={x["group"]:x for x in obj["cohort_relationships"]}
    assert len(groups)>=8
    actual=[]
    for row in records:
        assert row["cohort_group"] in groups, row["id"]
        assert row["evidence_tier"] in VALID_TIERS, row["id"]
        assert row["events"]==groups[row["cohort_group"]]["events"], row["id"]
        p=root/row["source_of_truth"]["path"]
        assert p.is_file(),f"missing source: {p}"
        raw=p.read_bytes()
        sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        assert sha==row["source_of_truth"]["git_blob_sha1"],f"blob mismatch {row['id']} {sha}"
        text=raw.decode("utf-8")
        for marker in row["source_of_truth"]["required_text"]:
            assert marker in text,f"source anchor missing {row['id']}: {marker}"
        assert row["next_action"] and row["scientific_result"] and row["interpretation_limits"]
        for run in row["execution_runs"]:
            assert run["conclusion"] in ("success","failure"),row["id"]
            assert re.fullmatch(r"[0-9a-f]{12}",run["head_sha_prefix"])
        actual.append({"id":row["id"],"blob":sha,"run_ids":[r["id"] for r in row["execution_runs"]]})
    for grp,info in groups.items():
        if "parent" in info:assert info["parent"] in groups
    byid={x["id"]:x for x in records}
    assert byid["B1_THREE_ARM_DEV"]["cohort_group"]==byid["B2_FIVE_SOURCE_COMPOSITION"]["cohort_group"]
    assert byid["B4A_H2_NESTED_HISTORY_NULL"]["parent_cohort"]==byid["B4A_H1_NEW_EVENT_ID_SUPERVISION"]["cohort_group"]
    assert byid["B1_THREE_ARM_DEV"]["next_action"]=="REUSE_NO_REPEAT_THREE_ARM"
    assert byid["N9_A1_EIGHT_BUDGET_FRONTIER"]["next_action"]=="DO_NOT_REPEAT_BUDGET_SCAN"
    assert byid["B4A_H2_NESTED_HISTORY_NULL"]["evidence_tier"]=="FROZEN_NESTED_SAME_PERIOD_TEST"
    assert byid["B2_FIVE_SOURCE_COMPOSITION"]["execution_runs"][0]["conclusion"]=="failure"
    assert byid["B2_FIVE_SOURCE_COMPOSITION"]["execution_runs"][1]["conclusion"]=="success"
    return {"status":"I0_PUBLIC_SOURCE_BLOB_AND_COHORT_CONTRACT_PASS","records":len(records),
            "cohort_groups":len(groups),"checked_blobs":len(actual),
            "run_records":sum(len(x["execution_runs"]) for x in records),
            "private_event_recalculation":False,"items":actual}
if __name__=="__main__":
    out=check()
    print(json.dumps({k:v for k,v in out.items() if k!="items"},indent=2))
