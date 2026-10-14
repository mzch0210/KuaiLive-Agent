#!/usr/bin/env python3
"""N12-C4 source-only KBS experimental-design evidence and provenance guard."""
from __future__ import annotations
import re,json,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PATH="manuscript/kbs_latex/"
def require(ok,s):
    if not ok:raise AssertionError("N12-C4 evidence-integrity: "+s)
def fnv32(t):
    z=t.encode("utf-16-le",errors="surrogatepass");v=2166136261
    for k in range(0,len(z),2):v=((v^(z[k]|(z[k+1]<<8)))*16777619)&0xffffffff
    return f"{v:08x}"
def check(root=ROOT):
    m=(root/PATH/"main.tex").read_text()
    sup=(root/PATH/"SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md").read_text()
    bib=(root/PATH/"kbs_references.bib").read_text()
    original=json.loads((root/"analysis/kbs_plan_c/n12_c4_original_experimental_section_freeze.json").read_text())
    method=json.loads((root/"analysis/kbs_plan_c/n12_c3_original_method_equations.json").read_text())
    b=m.index(r"\section{Experimental Design}")
    e=m.index(r"\section{Experimental Results}")
    chapter=m[b:e]
    require(fnv32(m[:b])==original["pre_exp_prefix_fnv32"],"Intro and N12-C3 method changed")
    require(fnv32(m[e:])==original["post_exp_suffix_fnv32"],"Results, Discussion or conclusion changed")
    sections=re.findall(r"\\section\{([^}]+)\}",m)
    require(sections==["Introduction","Related Work","Knowledge Valuation and Selective Use",
        "Experimental Design","Experimental Results","Discussion","Conclusion"],"seven-section transition changed")
    subsections=re.findall(r"\\subsection\{([^}]+)\}",chapter)
    expected=["Ranking Tasks and Evidence Hierarchy","Fixed Rankers and Selection Objectives",
        "Development Calibration and Pre-Outcome Information",
        "Candidate-Regime and Historical-Source Controls",
        "Additional-Target Freeze and Prespecified Comparisons",
        "Endpoints, Statistical Inference, and System Measurements"]
    require(subsections==expected,"design lacks question-first evidence tiers")
    labels=re.findall(r"\\label\{([^}]+)\}",chapter)
    require(set(labels)==set(original["original_experimental_labels"]) and len(labels)==len(set(labels))==11,
            "original 11 experimental references drift")
    for key,latex in original["original_experimental_formulas"].items():
        require(chapter.count(latex)==1,"original candidate equation drift "+key)
    newmethod=m[m.index(r"\section{Knowledge Valuation and Selective Use}"):b]
    for key,latex in method["original_equations"].items():
        require(newmethod.count(latex)==1,"N12-C3 mathematical source altered "+key)
    # Evidence levels and pretarget/no target leakage are mandatory study identities.
    contracts={
      "Twitch_main":["46,878","44,221","streamers","16"],
      "KuaiLive_original":["10,222","574","575 total","retrospective"],
      "M3_original":["24,995,148","50,049","47,575","12,533","31,065",
        "23 March 2026","27 March 2026"],
      "M3_additional":["30,000","10,387","4,096","3,059","twenty",
        "1,500","five recorded source dates","pretarget-history","same"],
      "DEV_exploration":["12,628","five-outer/four-inner","120","2,000"],
      "historical_null":["992","1,024","128","one","20261014","20261016",
        "after its source hour fully closes","TRAIN-only Popularity"],
      "statistical_frozen":["5,000","Holm","twenty-cell","three precommitted",
        "SASRec","GRU4Rec","one-sided","sign"],
      "hardware_scope":["256","three times","RTX 3090","original",
        "not","vectorized","production"],
      "negative_boundary":["not scored and sealed before the outcome revelation",
        "not retrospectively certified","not retrospectively equalized","Neither sample is a newly collected later-period TEST"],
    }
    for role,needles in contracts.items():
        absent=[x for x in needles if x.lower() not in chapter.lower()]
        require(not absent,role+" missing "+str(absent))
    # Original extra targets are from same source period, not new chronological data.
    require("Neither sample is a newly collected later-period TEST" in chapter and
            "not a guaranteed" not in chapter and
            "not make users disjoint across time" in chapter,
            "temporal and sampling identities inconsistent")
    all_labels=re.findall(r"\\label\{([^}]+)\}",m)
    require(len(all_labels)==len(set(all_labels)),"duplicate manuscript label")
    refs=re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",m)
    require(not (set(refs)-set(all_labels)),"dangling cross-chapter references "+
           repr(sorted(set(refs)-set(all_labels))))
    keys=re.findall(r"@\w+\s*\{\s*([^,\s}]+)\s*,",bib)
    require(len(keys)==len(set(keys)),"duplicate BibTeX keys")
    cited=[v.strip() for a in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",m) for v in a.split(",")]
    require(not (set(cited)-set(keys)),"undefined citations "+str(set(cited)-set(keys)))
    for v in ["0.005391","0.003585","0.031145","0.348744","0.334942",
              "0.692","1.769","0.22045","0.08751"]:
        require(v in m,"frozen evidence missing in main "+v)
    for v in ["0.005391","0.003585","0.031145","0.69165","1.76941",
              "0.021867","S10.15","S10.16","S10.17","S10.18","NOT VERIFIED"]:
        require(v in sup,"supporting evidence missing "+v)
    require([int(x) for x in re.findall(r"^## S10\.(\d+) ",sup,re.M)]==list(range(1,19)),
            "supplement structural coverage changed")
    require("not verified" in m.lower() and "B4-A" not in m and "G5" not in m,
            "post-unseal control incorrectly stated or project jargon leaked")
    return {"status":"N12_C4_EXPERIMENTAL_DESIGN_AUDIT_PASS",
      "sections":len(sections),"design_subsections":subsections,
      "two_original_candidate_equations_unchanged":True,
      "all_nine_N12_C3_equations_unchanged":True,
      "old_experimental_labels_preserved":11,
      "cohorts_provenance_and_statistics":list(contracts),
      "unresolved_latex_references":0,"unresolved_citation_keys":0,
      "previous_chapters_and_future_results_byte_text_untouched":True,
      "new_TEST_or_A4_reveal":False}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--repo-root",type=Path,default=ROOT)
    print(json.dumps(check(p.parse_args().repo_root),indent=2,ensure_ascii=False))
