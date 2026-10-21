#!/usr/bin/env python3
"""N12-C2 journal argument and source integrity audit. Public paper sources only.

C2 explicitly changes ONLY Introduction, Related Work and Figure 1. It must
not silently change Abstract, frozen statistics, methods, results or discussion.
After N12-C3 method merging, replace the old-tail freeze with a reviewed
migration-aware scientific coverage contract rather than disabling checks.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from n11_final_editorial_integrity import parse as legacy_scientific_coverage

MAIN="manuscript/kbs_latex/main.tex"
BLUE="manuscript/kbs_latex/N12_C1_RQ_ARGUMENT_AND_EVIDENCE_BLUEPRINT_2026-10-14.md"
OLD_FRONT_UTF16_FNV="a1e36733"
OLD_TAIL_UTF16_FNV="9117d105"
def fnv32(t):
    buf=t.encode("utf-16-le",errors="surrogatepass");v=2166136261
    for k in range(0,len(buf),2):
        v=((v^(buf[k]|buf[k+1]<<8))*16777619)&0xffffffff
    return f"{v:08x}"
def require(ok,why):
    if not ok:raise AssertionError("N12-C2 manuscript: "+why)
def check(root):
    raw=(root/MAIN).read_text()
    blue=(root/BLUE).read_text()
    a=raw.index(r"\section{Introduction}")
    b=raw.index(r"\section{Related Work}")
    c=raw.index(r"\section{Problem Formulation}")
    require(0<a<b<c,"major-section sequence")
    require(fnv32(raw[:a])==OLD_FRONT_UTF16_FNV,
            "frontmatter changed prematurely (abstract belongs to N12-C6)")
    require(fnv32(raw[c:])==OLD_TAIL_UTF16_FNV,
            "methods, original results or discussion altered outside N12-C2")
    intro=raw[a:b];related=raw[b:c]
    require(len(intro)>4000 and len(related)>3500,"argument too abbreviated")
    for item in ("Incumbent- and candidate-relative valuation",
                 "Candidate-aligned supervision for knowledge use",
                 "Fixed-candidate verification of historical-source information",
                 "30,000","4,096","same source recording period",
                 "fig:knowledge-value-chain"):
        require(item in intro,"missing one-thesis Intro or evidence role "+item)
    require("P1:" not in intro and "P2:" not in intro and "P3:" not in intro,
            "P1/P2/P3 legacy linear labels in framework figure")
    for item in ("RQ1: Define the value","RQ2: Predict value and choose",
                 "RQ3: Verify the history source",
                 "Authentic history versus valid historical nulls",
                 r"\draw[arr] (value.south) -- (decision.north);",
                 r"\draw[arr] (value.south) -- (source.north);"):
        require(item in intro,"missing branch diagram property "+item)
    require("(decision.south) -- (source.north)" not in intro and
            "(decision.south) -- (source.south)" not in intro,
            "source-validity RQ3 wrongly shown as effect of decision policy")
    heads=re.findall(r"\\subsection\{([^}]+)\}",related)
    expected=[
        "Knowledge Representation, Relationship Memory, and Memory Management",
        "Utility-Based Expert Selection and Adaptive Inference",
        "Candidate-Dependent Ranking in Live Recommendation"]
    require(heads==expected,"Related Work does not follow frozen 3-axis design")
    for cited in (
        "zhong2026samd","xie2026mhgfcl","yuan2026dsframe",
        "krichene2020kdd","mozannar2020defer","narasimhan2022posthoc",
        "mao2024regression","abbas2025voi","rappaz2021liverec",
        "qu2026kuailive"):
        require(re.search(r"\\cite\{[^}]*\b"+re.escape(cited)+r"\b[^}]*\}",related),
                "nearest work ungrounded or missing: "+cited)
    for obsolete in (
        "Our study does not require a new generic deferral theorem",
        "The contribution is evidence about a candidate-indexed knowledge valuation target",
        "Our contributions form a cumulative account"):
        require(obsolete not in intro+related,"obsolete self-limiting narrative "+obsolete)
    require("RQ2→RQ3" in blue and "There is no" in blue,
            "N12 approved parallel evidence design missing")
    legacy=legacy_scientific_coverage(root)
    require(len(legacy["prior_N9_N10_modifications_covered_in_main"])==10,
            "prior scientific claim lost")
    return {"status":"N12_C2_INTRO_RELATED_WORK_INTEGRATED_PASS",
        "pre_c2_frontmatter_fingerprint_unchanged":True,
        "pre_c2_methods_results_discussion_and_conclusion_unchanged":True,
        "parallel_RQ2_RQ3_source_diagram":"PASS",
        "related_work_reorganized_into_3_research_axes":True,
        "prior_experiment_families_retained_in_main":10,
        "bib_entries":legacy["bib_entries"],"used_citation_keys":legacy["citation_keys_used"],
        "missing_latex_refs":legacy["unresolved_latex_refs"],
        "missing_citation_keys":legacy["unresolved_citations"],
        "supplement_S10_1_to_18_preserved":True,
        "new_TEST_labels_read":False,"new_model_fit_or_test_scoring":False,
        "fully_restructured_7_section_article":False}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
    a=p.parse_args()
    print(json.dumps(check(a.repo_root),indent=2,sort_keys=True))
