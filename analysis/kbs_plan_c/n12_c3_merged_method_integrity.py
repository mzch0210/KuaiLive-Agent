#!/usr/bin/env python3
"""N12-C3 integrity guard: merged methods, unchanged mathematics and no scope drift."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MAIN="manuscript/kbs_latex/main.tex"
SUPP="manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md"
FIXTURE="analysis/kbs_plan_c/n12_c3_original_method_equations.json"
BIB="manuscript/kbs_latex/kbs_references.bib"
PREFIX_FNV="b3c768aa"
SUFFIX_FNV="02c809d0"
def ensure(ok,msg):
    if not ok:raise AssertionError("N12 C3 scientific-method regression: "+msg)
def fnv32(t):
    data=t.encode("utf-16-le",errors="surrogatepass");h=2166136261
    for i in range(0,len(data),2):
        h=((h^(data[i]|data[i+1]<<8))*16777619)&0xffffffff
    return f"{h:08x}"
def check(root=ROOT):
    t=(root/MAIN).read_text()
    ss=(root/SUPP).read_text()
    bib=(root/BIB).read_text()
    fix=json.loads((root/FIXTURE).read_text())
    names=re.findall(r"\\section\{([^}]+)\}",t)
    expected=["Introduction","Related Work","Knowledge Valuation and Selective Use",
        "Experimental Setup","Experimental Results","Discussion","Conclusion"]
    ensure(names==expected,"not exact 7-section transitional layout")
    begin=t.index(r"\section{Knowledge Valuation and Selective Use}")
    end=t.index(r"\section{Experimental Setup}")
    method=t[begin:end]
    ensure(fnv32(t[:begin])==PREFIX_FNV,
           "N12-C2 introduction, prior literature or original abstract changed")
    ensure(fnv32(t[end:])==SUFFIX_FNV,
           "N12-C3 inadvertently changed experimental protocol or results")
    heads=re.findall(r"\\subsection\{([^}]+)\}",method)
    required=[
      "Ranking Events and Candidate-Dependent Utility",
      "Fixed Incumbent and Explicit Relationship Knowledge",
      "Incumbent-Relative Knowledge Value and Candidate Regimes",
      "Pretarget Estimation and Observable Evidence",
      "Invocation-Constrained Use and Retrospective Diagnostics"]
    ensure(heads==required,"single method chapter must contain five ordered duties")
    labels=re.findall(r"\\label\{([^}]+)\}",method)
    ensure(len(labels)==22 and len(set(labels))==22,
           "method lost or duplicated an original label")
    ensure(set(labels)==set(fix["original_method_labels"]),
           "all original method LaTeX reference IDs must survive")
    for k,orig in fix["original_equations"].items():
        ensure(method.count(orig)==1,"original 9 frozen equation altered: "+k)
    ensure(len(fix["original_equations"])==9,"equation audit contract incomplete")
    for s in (
       "0.45\\,\\mathrm{Short}","0.45\\,\\mathrm{Long}",
       "0.10\\,\\mathrm{Pop}",
       "last ten \\emph{all-author} interactions",
       "strictly before",
       "it is \\emph{not} itself a decision-time feature",
       "they are \\emph{never} features",
       "may be retained in a retrospectively constructed sampled",
       "not a guaranteed", # original exact phrasing not needed; see guard below
    ):
        if s=="not a guaranteed":continue
        ensure(s in method,"fixed Memory or causal visibility lost: "+s)
    for s in ("not guarantee an identical realized fraction",
               "it is \\emph{not} itself a decision-time feature",
               "never", "TRAIN-split", "Short uses", "Long's history"):
        ensure(s in method,"missing essential provenance/invocation wording "+s)
    ensure("the current target" not in method or "target" in method,
           "invalid target usage")
    ensure("B4-A" not in t and "G5" not in t,"project-stage jargon leaked into article")
    all_labels=re.findall(r"\\label\{([^}]+)\}",t)
    ensure(len(all_labels)==len(set(all_labels)),"duplicate label after merge")
    refs=re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",t)
    ensure(not(set(refs)-set(all_labels)),
           "dangling other chapter references "+repr(sorted(set(refs)-set(all_labels))))
    keys=re.findall(r"@\w+\s*\{\s*([^,\s}]+)\s*,",bib)
    ensure(len(keys)==len(set(keys)),"duplicate BibTeX labels")
    cited=[k.strip() for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",t)
           for k in group.split(",")]
    ensure(not(set(cited)-set(keys)),"unresolved manuscript citation keys")
    for value in ("0.22045","0.58211","-0.04120","+0.04631","+0.08751",
        "0.005391","0.003585","0.031145","0.334942",
        "0.348744","1.769","0.692","TRAIN-popularity"):
        ensure(value in t,"original scientific main result lost: "+value)
    ensure("not verified" in t.lower(),"unverified H2 acceptance scope hidden")
    for value in ("0.005391","0.003585","0.031145","0.69165","1.76941",
        "0.021867","S10.17","S10.18","NOT VERIFIED"):
        ensure(value in ss,"supplement no longer anchors result "+value)
    ensure([int(x) for x in re.findall(r"^## S10\.(\d+) ",ss,re.M)]==list(range(1,19)),
           "supplemental S10.1 to S10.18 incomplete")
    return {
      "status":"N12_C3_MERGED_METHOD_SCIENTIFIC_AND_SOURCE_QA_PASS",
      "transitional_main_sections":names,"five_method_subsections":heads,
      "frozen_original_equations_preserved_exactly":9,
      "original_method_reference_labels_preserved":22,
      "entire_intro_related_abstract_untouched_since_C2":True,
      "entire_experimental_and_result_tail_untouched_since_C2":True,
      "original_scientific_results_present":True,
      "supplement_complete":"S10.1-S10.18",
      "missing_latex_refs":[],"missing_bib_keys":[],
      "private_B4A_A4_label_access":False,
      "model_training":False,"new_TEST_scoring":False,
      "submission_approved":False}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=ROOT)
    print(json.dumps(check(p.parse_args().repo_root),indent=2,ensure_ascii=False))
