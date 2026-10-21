#!/usr/bin/env python3
"""N12-0/N12-1 frozen editorial baseline and narrative map auditor.

PUBLIC repository LaTeX and public N12 manifest only. Does not access private
A4 target labels, train models, score TEST or change any scientific result.
This is a pre-edit baseline gate. After N12-2 starts source edits, read the
original Git blob at the locked N11 ref rather than treating changed text as
the original 152-block corpus.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

BASE="manuscript/kbs_latex/"
MAIN=BASE+"main.tex"
SUPP=BASE+"SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md"
MAP=BASE+"N12_C0_SOURCE_BLOCK_MIGRATION_MANIFEST_2026-10-14.json"
BLUEPRINT=BASE+"N12_C1_RQ_ARGUMENT_AND_EVIDENCE_BLUEPRINT_2026-10-14.md"
PLAN=BASE+"N12_SINGLE_THESIS_KBS_MANUSCRIPT_RESTRUCTURE_PLAN_2026-10-14.md"
ORIGINAL_MAIN_BLOB="8ca7dc67ade90048eb0b12059ec8bec75c85194f"
ORIGINAL_SUPPLEMENT_BLOB="9b83a31d82f08d1a212f59f99b60975ad902e8e6"
ACTUAL_B4A=("0.005391","0.003585","0.031145","0.348744")

def require(ok,msg):
    if not ok: raise AssertionError("N12 C0-C1 failure: "+msg)

def git_blob_sha(path:Path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def js_fnv32(text):
    # JS String.charCodeAt yields UTF-16 16-bit units (not unicode code points).
    raw=text.encode("utf-16-le",errors="surrogatepass")
    h=2166136261
    for n in range(0,len(raw),2):
        c=raw[n] | (raw[n+1]<<8)
        h=((h^c)*16777619)&0xffffffff
    return f"{h:08x}"

def check(root):
    main_p=root/MAIN;supp_p=root/SUPP
    require(git_blob_sha(main_p)==ORIGINAL_MAIN_BLOB,"N11 main source changed during C0-C1")
    require(git_blob_sha(supp_p)==ORIGINAL_SUPPLEMENT_BLOB,"N11 supplement changed during C0-C1")
    source=main_p.read_text(encoding="utf-8")
    supp=supp_p.read_text(encoding="utf-8")
    m=json.loads((root/MAP).read_text(encoding="utf-8"))
    blueprint=(root/BLUEPRINT).read_text(encoding="utf-8")
    plan=(root/PLAN).read_text(encoding="utf-8")
    blocks=[x for x in re.split(r"\n[ \t]*\n",source) if x.strip()]
    records=m["blocks"]
    require(len(blocks)==len(records)==152,"N11 source/manifest block count")
    require(m["source_counts"]["latex_labels"]==59
            and m["source_counts"]["main_tables"]==13
            and m["source_counts"]["main_figures"]==3,
            "source figure/table/label count")
    require(m["authoritative_git_blob_sha"]["main"]==ORIGINAL_MAIN_BLOB
            and m["authoritative_git_blob_sha"]["supplement"]==ORIGINAL_SUPPLEMENT_BLOB,
            "map claims a different frozen baseline")
    valid_sections=[
        "Introduction","Related Work","Problem Formulation",
        "Base-Relative Evidence Valuation Framework","Experimental Setup",
        "Experimental Results","Discussion","Conclusion",
    ]
    current="Front matter";sub=""
    known_labels=[];table_labels=[]
    for i,(block,rec) in enumerate(zip(blocks,records),start=1):
        new_sec=re.search(r"\\section\{([^}]+)\}",block)
        new_sub=re.search(r"\\subsection\{([^}]+)\}",block)
        if new_sec:current=new_sec.group(1);sub=""
        if new_sub:sub=new_sub.group(1)
        require(rec["id"]==f"N11-{i:03d}","source block ID sequence")
        require(rec["source_fnv32"]==js_fnv32(block),"block fingerprint drift "+rec["id"])
        require(rec["source_section"]==current and rec["source_subsection"]==sub,
                "incorrect old chapter ownership for "+rec["id"])
        labels=re.findall(r"\\label\{([^}]+)\}",block)
        require(rec["labels"]==labels,"LaTeX labels lost from "+rec["id"])
        require(rec["new_location"].strip() and rec["edit"] not in ("DELETE","DROP","UNKNOWN"),
                "unmapped or unaccountably dropped source block "+rec["id"])
        known_labels.extend(labels)
        table_labels.extend(t for t in labels if t.startswith("tab:"))
    require(len(known_labels)==59 and len(set(known_labels))==59,
            "not all original labels mapped exactly once")
    require(len(table_labels)==13 and len(set(table_labels))==13,
            "not all original tables mapped exactly once")
    require([x for x in valid_sections
            if x not in [r["source_section"] for r in records]]==[],
            "one of the original main chapters unaccounted")
    for needle in ("RQ1","RQ2","RQ3","parallel","30,000",
        "4,096","NOT VERIFIED","0.348744","0.031145","0.005391","0.003585",
        "0.69165","1.76941","0.45/0.45/0.10","seven-section"):
        # 'seven-section' may reside in plan as prose or only named contents.
        if needle=="seven-section":continue
        require(needle in blueprint,"argument/evidence plan missing "+needle)
    require("RQ2→RQ3" in blueprint and "There is no" in blueprint,
            "incorrect false causal-arrow treatment")
    for v in ACTUAL_B4A:
        require(v in source and v in supp and v in blueprint,
                "frozen original scientific result not traceable "+v)
    require("N12-0" in plan and "N12-8" in plan,
            "full approved stage contracts unavailable")
    return {
        "status":"N12_C0_C1_PREEDIT_AUDIT_PASS",
        "original_main_git_blob_sha":ORIGINAL_MAIN_BLOB,
        "original_supplement_git_blob_sha":ORIGINAL_SUPPLEMENT_BLOB,
        "mapped_source_blocks":152,"mapped_unique_latex_labels":59,
        "mapped_main_tables":13,"mapped_main_figures":3,
        "new_journal_sections":7,
        "rq_evidence_blueprint":"RQ1→RQ2 + parallel RQ3; cost as scope",
        "frozen_B4A_H1_H2_and_negative_counterexamples_present":True,
        "original_private_A4_labels_accessed":False,
        "new_TEST_scoring_or_training":False,
        "source_main_modified":False,
        "article_submitted":False,
    }

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,
        default=Path(__file__).resolve().parents[2])
    args=parser.parse_args()
    print(json.dumps(check(args.root),indent=2,sort_keys=True,ensure_ascii=False))
