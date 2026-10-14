#!/usr/bin/env python3
"""N11 independent source-only KBS editorial integrity / amendment coverage audit.

Reads public manuscript, supplement, references and frozen public reports ONLY.
Does not read raw interactions or private author IDs, retrain, use B4-A A4 or
evaluate NDCG. A revised journal narrative is assessed on traceable evidence.
"""
import argparse, json, re
from pathlib import Path

PAPER="manuscript/kbs_latex/main.tex"
SUP="manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md"
BIB="manuscript/kbs_latex/kbs_references.bib"
FROZEN="manuscript/kbs_latex/N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md"
def ensure(ok,msg):
    if not ok:raise AssertionError("N11 academic integrity: "+msg)
def parse(root):
    paper=(root/PAPER).read_text(encoding="utf-8")
    supp=(root/SUP).read_text(encoding="utf-8")
    bib=(root/BIB).read_text(encoding="utf-8")
    frozen=(root/FROZEN).read_text(encoding="utf-8")
    sections=re.findall(r"\\section\{([^}]+)\}",paper)
    expected=[
        "Introduction","Related Work","Problem Formulation",
        "Base-Relative Evidence Valuation Framework","Experimental Setup",
        "Experimental Results","Discussion","Conclusion"]
    ensure(sections==expected,"missing/reordered eight research-paper sections")
    rs=paper.split(r"\section{Experimental Results}",1)[1].split(r"\section{Discussion}",1)[0]
    ordered=[
        "Heterogeneous Utility of Relationship Memory",
        "Candidate-Regime Dependence of Relative Utility",
        "Decision Value of Predicting Relative Utility",
        "Relationship Sources and Observable Signals",
        "Invocation Constraints and Measured Scoring Cost"]
    ensure(re.findall(r"\\subsection\{([^}]+)\}",rs)==ordered,
           "Results not ordered knowledge→candidate→decision→source→cost")
    ensure("B4-A" not in paper and "G5" not in paper and
           "post-G5" not in paper and "B2 DEV and" not in paper,
           "internal project labels remain in journal narrative")
    # Primary vs exploratory evidence and previous changes, in main—not only S10.
    claims=[
       ("P1_history_complementarity",["0.22045","0.53980","0.58211",
            r"\label{eq:delta-memory}",r"\label{sec:results-heterogeneity}"]),
       ("P2_candidate_reversal",["-0.04120","+0.04631","+0.08751",
            r"\label{tab:results-factorial}"]),
       ("P2_exploratory_DEV_supervision",["0.296499","0.302658",
            "0.298123","0.303093","10,672","11,517"]),
       ("P2_frozen_new_target_H1",["30,000","0.005391","0.003585",
            "8,704","9,105","8,629","9,168",
            r"\label{tab:results-m3-b4a-supervision}"]),
       ("P3_source_interaction",["0.115382","0.100885","46,462","66"]),
       ("P3_frozen_4096_H2",["4,096","0.334942","0.303905",
            "0.304689","0.302796","0.303797","0.031145",
            r"\label{tab:results-m3-additional-relation-identity}"]),
       ("R2_original_unconditional_Memory_counterexample",
            ["0.34679","0.348744","Always Memory","0.803"]),
       ("R2_measured_negative_cost",["0.692","1.769","31.25",
             r"\label{tab:results-n10-cost}"]),
       ("R1_nearest_KBS_SAMD", [r"\cite{zhong2026samd}",
            r"\cite{yuan2026dsframe}","fig:knowledge-value-chain"]),
       ("R3_unverified_population_floor",["TRAIN-popularity","not verified",
              "S10.18"]),
    ]
    normalized=paper.lower()
    covered={}
    for name,tokens in claims:
        missing=[v for v in tokens if v.lower() not in normalized]
        ensure(not missing,"main missing prior research changes "+name+": "+str(missing))
        covered[name]="MAIN_AND_FROZEN_EVIDENCE"
    # Check the frozen comparison values have not drifted in both sources.
    for v in ("0.005391","0.003585","0.031145","0.334942","0.348744"):
        ensure(v in paper and v in supp and v in frozen,
               "original B4A confirmation absent/drift: "+v)
    for v in ("0.69165","1.76941","0.021867","S10.17","S10.18",
               "NOT VERIFIED","Table S10.11","Table S10.12"):
        ensure(v in supp,"newer C2/C3 not incorporated in Supplement: "+v)
    # Old standalone G4 cost table is in supplement; only one current cost
    # table in manuscript prevents presentation of two adjacent near-duplicate tables.
    ensure(r"tab:results-m3-cost" not in paper and
           r"tab:results-n10-cost" in paper,"duplicated old system cost table")
    ensure(r"tab:results-m3-dev-relation-identity" not in paper and
           "0.306491" in supp,
           "older B2 DEV seed-by-seed table must be supplemental, frozen H2 main")
    labels=re.findall(r"\\label\{([^}]+)\}",paper)
    dups=sorted(x for x in set(labels) if labels.count(x)>1)
    ensure(not dups,"duplicate LaTeX labels: "+repr(dups))
    refs=re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",paper)
    missing_labels=sorted(set(refs)-set(labels))
    ensure(not missing_labels,"dangling section/figure/table/equation refs "+repr(missing_labels))
    citekeys=re.findall(r"@\w+\s*\{\s*([^,\s}]+)\s*,",bib)
    ensure(len(set(citekeys))==len(citekeys),"duplicate BibTeX keys")
    cite=[]
    for grp in re.findall(r"\\cite(?:\[[^\]]+\])?\{([^}]+)\}",paper):
        cite.extend(x.strip() for x in grp.split(","))
    missing_cites=sorted(set(cite)-set(citekeys))
    ensure(not missing_cites,"unresolved citations "+str(missing_cites))
    s10=[int(x) for x in re.findall(r"^## S10\.(\d+) ",supp,re.M)]
    ensure(s10==list(range(1,19)),"S10 1-18 incomplete")
    ensure("same recording period" in normalized and "invocation" in normalized,
           "sample boundaries or invocation constraint missing")
    return {"status":"N11_FINAL_EDITORIAL_SOURCE_AUDIT_PASS",
       "main_sections":sections,
       "results_evidence_order":ordered,
       "prior_N9_N10_modifications_covered_in_main":covered,
       "citation_keys_used":len(set(cite)),"bib_entries":len(citekeys),
       "latex_labels":len(labels),"unresolved_latex_refs":missing_labels,
       "unresolved_citations":missing_cites,"main_source_chars":len(paper),
       "supplement_S10_sections":"S10.1--S10.18",
       "B4A_original_target_outcomes_reopened":False,
       "additional_future_period_test_claimed":False,
       "human_author_submittal_approved":False}
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2])
    cfg=a.parse_args()
    print(json.dumps(parse(cfg.root),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
