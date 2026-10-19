#!/usr/bin/env python3
"""N12-C6 source-level scientific coverage and RQ-driven Results verifier.

Uses only publication LaTeX, Supplement S1-S10.19 and frozen prior source fixtures.
No new TRAIN, DEV, TEST scoring, A4 label re-unsealing or performance tuning.
"""
from __future__ import annotations
import re,json,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=Path("manuscript/kbs_latex")
FIX=Path("analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json")
C3=Path("analysis/kbs_plan_c/n12_c3_original_method_equations.json")
C4=Path("analysis/kbs_plan_c/n12_c4_original_experimental_section_freeze.json")
def assert_ok(v,msg):
    if not v: raise AssertionError("N12-C6: "+msg)
def fnv32(t):
    buf=t.encode("utf-16-le",errors="surrogatepass");h=2166136261
    for i in range(0,len(buf),2):
        h=((h^(buf[i]|(buf[i+1]<<8)))*16777619)&0xffffffff
    return f"{h:08x}"
def check(root=ROOT):
    main=(root/BASE/"main.tex").read_text()
    supp=(root/BASE/"SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md").read_text()
    bib=(root/BASE/"kbs_references.bib").read_text()
    fix=json.loads((root/FIX).read_text())
    c3=json.loads((root/C3).read_text())
    c4=json.loads((root/C4).read_text())
    a=main.index(r"\section{Results}")
    b=main.index(r"\section{Discussion}")
    result=main[a:b]
    # C6 is permitted to edit frontmatter, selected Intro explanation, Discussion and Conclusion.
    # Never fingerprint sections deliberately edited in C6. Original method/results stay controlled below.
    chapters=re.findall(r"\\section\{([^}]+)\}",main)
    assert_ok(chapters==["Introduction","Related Work","Knowledge Valuation and Selective Use",
        "Experimental Design","Results","Discussion","Conclusion"],"chapter contract")
    subs=re.findall(r"\\subsection\{([^}]+)\}",result)
    assert_ok(subs==[
        "RQ1: When Is Relationship Knowledge Incrementally Valuable?",
        "RQ2: Does Candidate-Aligned Value Supervision Improve Knowledge Use?",
        "RQ3: Does Authentic Relationship History Matter with Fixed Candidates?",
        "Operational Conditions: Invocation Limits and Measured Scoring Cost",
    ],"exact four RQ-driven Results roles")
    retained=[
        "tab:results-factorial","tab:results-twitch-policy",
        "tab:results-m3-policy","tab:results-m3-robustness",
        "tab:results-m3-b4a-supervision",
        "tab:results-m3-additional-relation-identity",
        "tab:results-n10-cost"]
    moved=[
        "tab:results-evidence-states",
        "tab:results-m3-dev-regime-transfer",
        "tab:results-m3-dev-source",
        "tab:results-feature-ablation"]
    labels=re.findall(r"\\label\{([^}]+)\}",result)
    tables=[x for x in labels if x.startswith("tab:")]
    assert_ok(len(tables)==7 and set(tables)==set(retained),"retain seven key main Results tables")
    assert_ok(not(set(moved)&set(labels)),"moved DEV tables remain duplicated in main")
    assert_ok("fig:results-evidence-states" in labels,"original empirical diagnostic figure lost")
    for name in retained:
        assert_ok(result.count(fix["original_latex_tables"][name])==1,
                  "original full main frozen table altered: "+name)
    oldfig=fix["original_latex_figures"]["fig:results-evidence-states"]
    newfig=re.search(r"\\begin\{figure\}(?:\[[^\]]*\])?[\s\S]*?\\label\{fig:results-evidence-states\}[\s\S]*?\\end\{figure\}",result)
    assert_ok(bool(newfig) and "Supplementary Table S10.13" in newfig.group(0),
              "Twitch figure not present or hanging citation")
    # All migrated tables have their entire source still stored under version-controlled fixture
    # and a full table of literal original numbers rendered in Supplement S10.19.
    assert_ok("## S10.19 " in supp,"missing explicit source-preserving supplement extension")
    s19=supp.split("## S10.19 ",1)[1]
    assert_ok("N12-C6" not in s19 and "relocated" not in s19 and "original main table" not in s19,
              "internal revision chronology must not enter journal supplement")
    for title in ("Table S10.13.","Table S10.14.","Table S10.15.","Table S10.16."):
        assert_ok(s19.count(title)==1,"full relocated table missing/duplicate "+title)
    for label,numbers in {
      moved[0]:["24,285","5,539","14,397","0.86102","0.52225",
                "0.22045","0.23001","0.18681"],
      moved[1]:["14,988","15,016","14,954","15,001","14,762","14,989",
                "0.296499","0.302658","0.303093"],
      moved[2]:["0.343509","0.333231","0.773602","0.668498","0.407506",
                "0.022215","0.197796","0.007576","0.189571"],
      moved[3]:["6,563","0.00372","0.00160","0.00838",
                "0.14791","0.09109","0.18990","0.00963"],
    }.items():
        assert_ok(all(v in s19 for v in numbers),"transferred numeric row missing in S10.19 "+label)
        assert_ok(label in fix["original_latex_tables"],"not sourced from original frozen table "+label)
    for s in ("Supplementary Table S10.13","Supplementary Table S10.14",
              "Supplementary Table S10.15","Supplementary Table S10.16"):
        assert_ok(s in result,"main does not link relocated source "+s)
    # RQ2 primary H1 + RQ3 primary H2 and adverse decision/cost all visible, with
    # original true scientific denominators and no falsely equal call or period.
    for role,v in {
      "first_M3_TEST":"47,575",
      "original_test_seed":"20261012",
      "SAS_H1":"0.005391",
      "GRU_H1":"0.003585",
      "SAS_calls":"8,704",
      "S_calls":"9,105",
      "GRU_calls":"8,629",
      "GRU_S_calls":"9,168",
      "H1_SAS_CI":"0.003646",
      "H1_GRU_CI":"0.001599",
      "H2_nested":"4,096",
      "H2_authentic":"0.334942",
      "H2_mean_null":"0.303797",
      "H2_gap":"0.031145",
      "H2_CI":"0.027389",
      "H2_p":"0.000600",
      "Always_Memory":"0.348744",
      "measured_Utility":"1.769",
      "measured_Memory":"0.692",
      "non_preunseal_floor":"not measured and sealed before target reveal",
      "call_nonnequality":"not an experimentally isolated equal-resource",
      "same_source":"original recording period",
    }.items():
        assert_ok(v in result,"lost mandatory frozen science "+role+":"+v)
    method=main[main.index(r"\section{Knowledge Valuation and Selective Use}"):main.index(r"\section{Experimental Design}")]
    ex=main[main.index(r"\section{Experimental Design}"):a]
    for name,text in c3["original_equations"].items():
        assert_ok(method.count(text)==1,"method original equation changed "+name)
    for name,text in c4["original_experimental_formulas"].items():
        assert_ok(ex.count(text)==1,"experimental original equation changed "+name)
    all_labels=re.findall(r"\\label\{([^}]+)\}",main)
    assert_ok(len(all_labels)==len(set(all_labels)),"duplicate paper labels")
    refs=re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",main)
    assert_ok(not(set(refs)-set(all_labels)),"unresolved LaTeX references "+
              repr(sorted(set(refs)-set(all_labels))))
    bib_keys=re.findall(r"@\w+\s*\{\s*([^,\s}]+)\s*,",bib)
    cited=[k.strip() for g in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",main) for k in g.split(",")]
    assert_ok(not(set(cited)-set(bib_keys)),"unresolved BibTeX citations")
    assert_ok([int(k) for k in re.findall(r"^## S10\.(\d+) ",supp,re.M)]==list(range(1,20)),
             "supplement not continuous S10.1-S10.19")
    for n in ["0.005391","0.003585","0.031145","0.334942",
              "0.69165","1.76941","0.021867","NOT VERIFIED"]:
        assert_ok(n in supp,"primary supplement frozen verification missing "+n)
    assert_ok("B4-A" not in main and "G5" not in main,"research execution jargon in main paper")
    # Ensure the revised journal-facing claim is bounded and the parallel source check remains explicit.
    front=main.split(r"\\end{abstract}",1)[0]
    discussion=main[b:]
    assert_ok("candidate-aligned" in front and "supervision" in front,"abstract lacks C6 contribution")
    for z in ("strictly equal", "not verified", "unconditional", "historical"):
        assert_ok(z.lower() in discussion.lower(),"missing C6 Discussion/Conclusion caution: "+z)
    highlights=(root/BASE/"Highlights.txt").read_text()
    assert_ok("candidate-aligned supervision" in highlights.lower(),"Highlights lag primary contribution")
    return {
        "status":"N12_C6_FROZEN_SCIENCE_CONTRACT_PASS",
        "one_thesis_four_results_roles":subs,
        "original_results_tables":11,"retained_main_tables":7,"migrated_full_supplement_tables":4,
        "old_source_figures_kept":1,"C6_editorial_regions_permitted":True,
        "original_9_plus_2_math_blocks_unchanged":True,
        "H1_H2_call_budget_and_negative_cost_evidence_present":True,
        "no_dangling_LaTex_or_Bibtex_refs":True,
        "private_A4_access_or_rescoring":False}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=ROOT)
    print(json.dumps(check(p.parse_args().repo_root),indent=2,ensure_ascii=False))
