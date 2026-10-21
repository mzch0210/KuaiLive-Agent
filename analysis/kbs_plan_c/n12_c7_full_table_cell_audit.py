#!/usr/bin/env python3
"""N12-C7 strict original Results table -> Supplement S10.19 cell-preservation audit.

Reads only publication sources and previously frozen C5 original-Results fixture.
Does not read private TEST rows, retrain models, change estimates or open protected data.
Cell numeric tokens (sign, precision and number) must match exactly, in original order.
The explicit row-name map permits reader-facing wording improvements, never value changes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FIXTURE=Path("analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json")
MAIN=Path("manuscript/kbs_latex/main.tex")
SUPPLEMENT=Path("manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md")
TABLES={
    "S10.13":{
        "original":"tab:results-evidence-states", "numeric_columns":[1,2,3,4,5],
        "labels":[("Represented","Represented"),
            ("Recoverable","Recoverable outside Base input"),
            ("Unavailable","Unavailable in prior history")]},
    "S10.14":{
        "original":"tab:results-m3-dev-regime-transfer","numeric_columns":[2,3],
        "labels":[("SASRec|$S\\rightarrow F$","SASRec|Sampled S → full F"),
            ("SASRec|$F\\rightarrow F$","SASRec|Full F → full F"),
            ("SASRec|Adapted $\\rightarrow F$","SASRec|Full-label adapted → full F"),
            ("GRU4Rec|$S\\rightarrow F$","GRU4Rec|Sampled S → full F"),
            ("GRU4Rec|$F\\rightarrow F$","GRU4Rec|Full F → full F"),
            ("GRU4Rec|Adapted $\\rightarrow F$","GRU4Rec|Full-label adapted → full F")]},
    "S10.15":{
        "original":"tab:results-m3-dev-source","numeric_columns":[1,2],
        "labels":[("Full Memory","Full Memory (unchanged mixture)"),
            ("Long-only","Long-only"),("Short-only","Short-only"),
            ("Training popularity","TRAIN-only author popularity"),
            ("History placement control","History-score-placement control")]},
    "S10.16":{
        "original":"tab:results-feature-ablation","numeric_columns":[1,2,3,4],
        "labels":[("History descriptors","History descriptors"),
            ("Base-score descriptors","Base-score descriptors"),
            ("Combined","History + Base scores")]},
}
NUMBER=re.compile(r"(?<![A-Za-z0-9])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?")
def require(test,message):
    if not test: raise AssertionError("N12-C7 table-cell mismatch: "+message)
def sha(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
def latex_rows(table):
    require(table.count(r"\midrule")==1 and table.count(r"\bottomrule")==1,"source table bounds")
    body=table.split(r"\midrule",1)[1].split(r"\bottomrule",1)[0]
    rows=[]
    for line in body.splitlines():
        if " & " not in line: continue
        require(line.rstrip().endswith("\\\\"),"source row missing LaTeX terminator: "+line)
        rows.append([x.strip() for x in line.rstrip()[:-2].split("&")])
    return rows
def markdown_rows(supp,key):
    marker="**Table "+key+"."
    require(supp.count(marker)==1,"missing or duplicate supplement heading "+key)
    tail=supp.split(marker,1)[1].splitlines()
    lines=[];started=False
    for line in tail:
        if line.startswith("|"):
            lines.append(line);started=True
        elif started: break
    require(len(lines)>=4,"missing Markdown table "+key)
    cols=lambda line:[v.strip() for v in line.strip().strip("|").split("|")]
    sep=cols(lines[1])
    require(all(re.fullmatch(r":?-{3,}:?",v) for v in sep),"malformed Markdown rule "+key)
    return cols(lines[0]), [cols(v) for v in lines[2:]]
def tokens(cell):
    # Formatting is permitted; signs, comma thousands, decimal precision and row order are not.
    t=(cell.replace("−","-").replace("–","-").replace("\N{NON-BREAKING HYPHEN}","-")
       .replace("\\,",","))
    for mark in ("**","$",r"\textbf",r"\mathbf","{","}"):
        t=t.replace(mark,"")
    return NUMBER.findall(t)
def check_content(fixture,main,supp):
    original=fixture["original_latex_tables"]
    require(len(original)==11,"original results table inventory changed")
    kept=["tab:results-factorial","tab:results-twitch-policy","tab:results-m3-policy",
          "tab:results-m3-robustness","tab:results-m3-b4a-supervision",
          "tab:results-m3-additional-relation-identity","tab:results-n10-cost"]
    res=main.split(r"\section{Results}",1)[1].split(r"\section{Discussion}",1)[0]
    for label in kept:
        require(res.count(original[label])==1,"frozen main LaTeX table altered "+label)
    summary=[]
    for name,config in TABLES.items():
        label=config["original"]
        require(label in original,"source label absent "+label)
        require(original[label] not in main,"relocated source LaTeX duplicated in main "+label)
        old=latex_rows(original[label]); headers,new=markdown_rows(supp,name)
        require(len(old)==len(new)==len(config["labels"]),
                f"{name} original/new row mismatch {len(old)}/{len(new)}")
        require(len(headers)==len(old[0]),f"{name} header column count")
        for i,(src,dst) in enumerate(zip(old,new)):
            require(len(src)==len(dst)==len(headers),f"{name} row {i+1} column width")
            names=config["labels"][i]
            if name=="S10.14":
                require("|".join(src[:2])==names[0],f"{name} row {i+1} changed source identity")
                require("|".join(dst[:2])==names[1],f"{name} row {i+1} changed destination identity")
            else:
                require(src[0]==names[0] and dst[0]==names[1],
                        f"{name} row {i+1} changed label semantic identity")
            for col in config["numeric_columns"]:
                x,y=tokens(src[col]),tokens(dst[col])
                require(bool(x),f"{name} row {i+1} col {col+1} source numeric cell empty")
                require(x==y,
                        f"{name} row {i+1} col {col+1} source={x} supplement={y}")
                summary.append({"table":name,"source":label,"row":i+1,"column":col+1,
                                "source_tokens":x,"supplement_tokens":y,"pass":True})
    return {"status":"N12_C7_ALL_RELOCATED_TABLE_NUMERIC_CELLS_EXACT",
            "original_result_tables":11,"unchanged_main_original_result_tables":7,
            "relocated_tables":len(TABLES),"relocated_rows":sum(len(x["labels"]) for x in TABLES.values()),
            "verified_numeric_cells":len(summary),
            "source_fixture_sha256":sha(json.dumps(fixture,sort_keys=True,ensure_ascii=False)),
            "main_sha256":sha(main),"supplement_sha256":sha(supp),
            "row_column_cells":summary}
def check(root=ROOT):
    fixture=json.loads((root/FIXTURE).read_text(encoding="utf-8"))
    main=(root/MAIN).read_text(encoding="utf-8")
    supp=(root/SUPPLEMENT).read_text(encoding="utf-8")
    return check_content(fixture,main,supp)
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,default=ROOT)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    output=check(args.root)
    data=json.dumps(output,indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k!="row_column_cells"},indent=2,ensure_ascii=False))
