#!/usr/bin/env python3
"""N12 I2 Path A claim and prior-art guard, preserving original C6/C7/V0 controls."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=Path("manuscript/kbs_latex")


def check_text(main: str, bib: str) -> dict:
    def need(condition: bool, message: str):
        if not condition:
            raise AssertionError("I2 Path A: "+message)
    related=main.split(r"\subsection{Candidate-Dependent Ranking in Live Recommendation}",1)[1].split(r"\section{Knowledge Valuation and Selective Use}",1)[0]
    rq2=main.split(r"\paragraph{Actual-candidate labels improve frozen policy outcomes.}",1)[1].split(r"\subsection{RQ3:",1)[0]
    valid=main.split(r"\subsection{Source Validity, Evaluation Limits and Actual Operating Conditions}",1)[1].split(r"\section{Conclusion}",1)[0]
    need(r"\cite{krichene2020kdd}" in related and r"\cite{subbiah2024rankestimation}" in related,
         "sampled metric and rank-training correction prior art both required")
    need("WARP and LambdaRank" in related and "conditional utility relative to an incumbent" in related,
         "CIKM training rank correction must be distinguished from paired specialist value")
    need("original, uncorrected 575-candidate labels" in rq2,
         "S comparison must explicitly be with uncorrected target-retained labels")
    need("retrospectively retaining the observed target" in rq2,
         "target retention used for retrospective labeling only")
    need("regime-adapted DEV control" in rq2 and
         "uses full-candidate training labels" in rq2 and
         "not a sampled-only statistical correction" in rq2,
         "old B1 adapted arm must not masquerade as corrected-S")
    need("did not train or evaluate a selector using such corrected labels" in valid,
         "no corrected-S trained policy was evaluated")
    need("could narrow the observed F-versus-S policy difference" in valid and
         "cannot rule out that alternative" in valid,
         "untested valid correction must be an open competitor")
    need("not causal online user outcomes" in valid,
         "retain offline-only claim boundary")
    need(re.search(r"@inproceedings\s*\{\s*subbiah2024rankestimation,",bib)!=None,
         "reference absent")
    need("10.1145/3627673.3679943" in bib and "4066--4070" in bib,
         "verified CIKM 2024 DOI and proceedings pages required")
    for v in ("0.005391","0.003585","0.031145","0.334942",
              "8,704","9,105","8,629","9,168","1.337","1.797"):
        need(v in main,"frozen H1/H2 scientific evidence lost: "+v)
    need("not an experimentally isolated equal-resource effect" in rq2,
         "strict equal-call limitation missing")
    all_cites={k.strip() for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",main)
               for k in group.split(",")}
    all_keys=set(re.findall(r"@\w+\s*\{\s*([^,\s}]+)\s*,",bib))
    need(not (all_cites-all_keys),"undefined BibTeX citation: "+repr(all_cites-all_keys))
    need(len(all_keys)==len(re.findall(r"@\w+\s*\{\s*([^,\s}]+)\s*,",bib)),
         "duplicate bibliography keys")
    return {"status":"I2_PATH_A_PRIOR_CORRECTION_AND_SCOPED_CLAIMS_PASS",
            "CIKM_2024_reference":True,
            "original_S_uncorrected_label_contract":True,
            "adapted_F_assisted_not_corrected_S":True,
            "corrected_S_policy_unverified":True,
            "frozen_H1_H2_and_call_limit_guard":True,
            "no_TEST_or_model_scoring":True}


def check(root: Path=ROOT):
    return check_text((root/BASE/"main.tex").read_text(),
                      (root/BASE/"kbs_references.bib").read_text())


if __name__=="__main__":
    print(json.dumps(check(),indent=2))
