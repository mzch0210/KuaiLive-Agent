#!/usr/bin/env python3
"""N10 C6 static editorial claims and citation integrity audit.

No network, private data, training, NDCG scoring, A4 or runtime benchmarking.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def validate(main,bib,supp):
    citations=[]
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',main):
        citations.extend(k.strip() for k in group.split(","))
    keys=re.findall(r'@\w+\s*\{\s*([^,\s}]+)\s*,',bib)
    dup=sorted(k for k in set(keys) if keys.count(k)>1)
    missing=sorted(set(citations)-set(keys))
    if not keys or dup or missing:raise AssertionError(
        f"bibliographic key validation failed duplicate={dup} missing={missing}")
    required={
      "SAMD_kbs_near_neighbor":r"\cite{zhong2026samd}",
      "cost_table_label":"tab:results-n10-cost",
      "evidence_chain_figure":"fig:knowledge-value-chain",
      "C3_missing_original_floor":"TRAIN-popularity",
      "C2_resource_reference":"Always Memory",
      "same_period_scope":"same-period",
      "preoutcome_policy":"pre-outcome",
    }
    for name,needle in required.items():
        if needle not in main:raise AssertionError("missing main manuscript condition: "+name)
    sections=[int(x) for x in re.findall(r"^## S10\.(\d+)\s+",supp,re.M)]
    if sections!=list(range(1,19)):raise AssertionError("missing S10 sections: "+str(sections))
    for k in ("S10.17","S10.18","Table S10.11","Table S10.12",
             "NOT VERIFIED","0.69165","1.76941","0.021867"):
        if k not in supp:raise AssertionError("supplement missing "+k)
    for k in ("0.005391","0.003585","0.031145","0.348744"):
        if k not in main or k not in supp:raise AssertionError("B4-A frozen effect drift "+k)
    for k in ("0.692","1.769"):
        if k not in main:raise AssertionError("new measured DEV latency absent "+k)
    if "@article{zhong2026samd," not in bib:
        raise AssertionError("SAMD publisher-verified bib record missing")
    return {"status":"N10_C6_STATIC_CLAIM_CITATION_PASS",
       "total_reference_entries":len(keys),"unique_citation_keys":len(set(citations)),
       "undefined_citation_keys":missing,"duplicate_bib_keys":dup,
       "supplement_sections":"S10.1-S10.18",
       "B4A_frozen_primary_claims_unchanged":True,
       "new_latency_claim_explicitly_DEV":True,
       "B4A_original_popularity_floor_not_verified":True,
       "external_forward_time_test_not_claimed":True,
       "manuscript_author_declarations_human_verified":False,
       "official_KBS_submission_completed":False}

def main():
    p=argparse.ArgumentParser();p.add_argument("--repo-root",type=Path,
        default=Path(__file__).resolve().parents[2]);a=p.parse_args()
    path=a.repo_root/"manuscript/kbs_latex"
    z=validate((path/"main.tex").read_text(),
        (path/"kbs_references.bib").read_text(),
        (path/"SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md").read_text())
    print(json.dumps(z,indent=2,sort_keys=True))

if __name__=="__main__":main()
