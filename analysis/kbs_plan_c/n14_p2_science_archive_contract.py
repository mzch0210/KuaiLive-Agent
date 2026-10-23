#!/usr/bin/env python3
"""N14 P2: placement-independent frozen Results and one-question scope QA.

Reads only committed public manuscript/appendix/source-fixture files.
No original row-level TEST access, training, model tuning or re-estimation.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

from n12_c7_full_table_cell_audit import TABLES, latex_rows, markdown_rows, tokens

ROOT=Path(__file__).resolve().parents[2]
LATEX=ROOT/"manuscript/kbs_latex"
ORIGINAL_RESULTS=ROOT/"analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json"
ARCHIVE=LATEX/"N14_N13_COMPLETE_RESULTS_RESEARCH_ARCHIVE_2026-10-23.tex"
MAIN=LATEX/"main.tex"
SUPP=LATEX/"SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md"
TABLE_PRESERVE=("tab:results-factorial","tab:results-m3-b4a-supervision")
OLD_MAIN=("tab:results-twitch-policy","tab:results-m3-policy",
          "tab:results-m3-robustness","tab:results-m3-additional-relation-identity",
          "tab:results-n10-cost")
S10_LABELS=("S10.13","S10.14","S10.15","S10.16")


def require(ok, why):
    if not ok:
        raise AssertionError("N14 P2 science contract: "+why)


def check():
    main=MAIN.read_text(encoding="utf-8")
    supp=SUPP.read_text(encoding="utf-8")
    archive=ARCHIVE.read_text(encoding="utf-8")
    fixture=json.loads(ORIGINAL_RESULTS.read_text(encoding="utf-8"))
    original=fixture["original_latex_tables"]
    require(len(original)==11,"original frozen eleven-table inventory altered")
    require(main.count(r"\section{Results}")==1 and main.count(r"\section{Discussion}")==1,
            "results/discussion boundaries")
    res=main.split(r"\section{Results}",1)[1].split(r"\section{Discussion}",1)[0]
    require(res.count(r"\begin{table}") == 2, "focused Results must have exactly two tables")
    expected_headers=[
      "Candidate-Regime Sensitivity of the Supervision Target",
      "Primary Frozen Full-Candidate Policy Comparison",
      "DEV Allocation: Which Requests Change Specialist Use?",
      "Quality, Comparator and Operating Boundaries",
    ]
    got=re.findall(r"\subsection\{([^}]+)\}",res)
    require(got==expected_headers, "Results must follow the one-question evidence sequence")
    require(not re.search(r"\bRQ[123]\b",res), "parallel RQ labels reintroduced")
    require("Twitch" not in res,"cross-task Twitch selection results reintroduced")
    require("NOT VERIFIED" in supp,"H2 pre-reveal disclosure missing from full source supplement")
    require("S10.19" in supp,"original supporting result archive missing")
    for label in TABLE_PRESERVE:
        require(res.count(original[label])==1,"main frozen table body altered "+label)
        require(archive.count(original[label])==1,"research archive original table not intact "+label)
    for label in OLD_MAIN:
        require(original[label] not in res,"parallel Results table still in main "+label)
        require(archive.count(original[label])==1,"archived table source not intact "+label)
    require(archive.count(r"\begin{table}")==7,"research archive must retain all seven full tables")
    require("fig:results-evidence-states" in archive,"original historical diagnostic figure missing")
    require("fig:results-evidence-states" not in res,"legacy independent mechanism figure remains main")
    # Verify the FOUR relocated original source tables by each cell, as in old C7,
    # but no longer require the seven retained tables to sit in main.
    checked=[]
    for name in S10_LABELS:
        cfg=TABLES[name]
        src=latex_rows(original[cfg["original"]])
        head,dst=markdown_rows(supp,name)
        require(len(src)==len(dst)==len(cfg["labels"]),"S10 source row counts "+name)
        require(len(head)==len(src[0]),"S10 source column widths "+name)
        for rowno,(left,right) in enumerate(zip(src,dst),1):
            require(len(left)==len(right)==len(head),"S10 source cell row width "+name)
            identities=cfg["labels"][rowno-1]
            if name=="S10.14":
                require("|".join(left[:2])==identities[0] and "|".join(right[:2])==identities[1],
                        "S10 double-identity changed "+name)
            else:
                require(left[0]==identities[0] and right[0]==identities[1],
                        "S10 row identity changed "+name)
            for col in cfg["numeric_columns"]:
                a,b=tokens(left[col]),tokens(right[col])
                require(bool(a) and a==b,"S10 source numeric cell changed "+name+" row "+str(rowno))
                checked.append((name,rowno,col))
    require(len(checked)==49, "expected 49 exact numeric migrated source cells")
    # Do not reinterpret the original 3-comparison Holm family as a two-test family.
    for t in ("0.005391","0.003585","0.000600","0.000800",
              "0.348744","29.203","30.537","29.008","30.809",
              "1.337","1.797","50,049","10,672","11,517","21.32","23.01",
              "0.133417","0.076194","0.126600","0.079135"):
        require(t in res,"frozen primary-policy result lost "+t)
    require("three-comparison prereveal Holm family" in res,"original Holm family was redefined")
    require("nested historical-source contrast" in res,"excluded H2 original multiplicity member undisclosed")
    require("not a causal decomposition" in res,"DEV accounting falsely elevated to causal claim")
    require("uncorrected" in res and "retrospective target retention" in res,
            "original sampled comparator has lost information-contract limits")
    require("not an experimentally isolated equal-resource effect" in res,
            "resource/label-only inference caveat missing")
    require("Always Memory" in res and "0.348744" in res and "1.76941" in res,
            "adverse full-specialist / gate-timing evidence hidden")
    require("was not measured end to end" in res,"unmeasured vectorized F gate cost not acknowledged")
    return {
        "status":"N14_P2_SINGLE_QUESTION_SCIENCE_AND_ARCHIVE_PASS",
        "main_frozen_tables":2,
        "archived_full_original_tables":7,
        "original_result_tables_total":11,
        "relocated_supplement_tables":4,
        "original_migrated_numeric_cells_checked":len(checked),
        "results_subsections":got,
        "main_sha256":hashlib.sha256(main.encode()).hexdigest(),
        "archive_sha256":hashlib.sha256(archive.encode()).hexdigest(),
        "supplement_sha256":hashlib.sha256(supp.encode()).hexdigest(),
    }


if __name__=="__main__":
    print(json.dumps(check(),indent=2,ensure_ascii=False))
