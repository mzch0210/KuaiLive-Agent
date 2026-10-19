#!/usr/bin/env python3
"""N12 C8V-V0 manuscript semantic denominator and evidence-scope audit.

Source-level correctness checks on publication text; complements, not replaces,
C6 frozen-value/equation guards and C7 all-cell table migration audits.
No TEST-level data access; run entirely on public repository files.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MANUSCRIPT=Path("manuscript/kbs_latex/main.tex")
SUPPLEMENT=Path("manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md")
REFERENCES=Path("manuscript/kbs_latex/kbs_references.bib")
HIGHLIGHTS=Path("manuscript/kbs_latex/Highlights.txt")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError("C8V-V0 semantic verification: "+message)


def sections(main: str) -> dict[str, str]:
    marks=[
        ("abstract",r"\begin{abstract}"),
        ("introduction",r"\section{Introduction}"),
        ("related",r"\section{Related Work}"),
        ("methods",r"\section{Knowledge Valuation and Selective Use}"),
        ("design",r"\section{Experimental Design}"),
        ("results",r"\section{Results}"),
        ("discussion",r"\section{Discussion}"),
        ("conclusion",r"\section{Conclusion}"),
        ("bibliography",r"\bibliographystyle"),
    ]
    positions=[]
    for k,marker in marks:
        require(main.count(marker)==1,"section boundary not unique: "+k)
        positions.append((k,main.index(marker)))
    require(positions==sorted(positions,key=lambda kv:kv[1]),"section order changed")
    return {
        k:main[pos:positions[i+1][1] if i+1<len(positions) else len(main)]
        for i,(k,pos) in enumerate(positions)
    }


def audit_text(main: str, supp: str, bib: str, highlights: str) -> dict:
    parts=sections(main)
    abstract=parts["abstract"].split(r"\end{abstract}",1)[0]
    results=parts["results"]
    discussion=parts["discussion"]
    r2=results.split(r"\subsection{RQ2:",1)[1].split(r"\subsection{RQ3:",1)[0]
    r3=results.split(r"\subsection{RQ3:",1)[1].split(r"\subsection{Operational Conditions:",1)[0]
    require(bool(re.search(r"50,049\s+(?:DEV\s+)?requests",abstract,re.I)),
            "abstract does not state 50,049 DEV requests as policy disagreement denominator")
    require("development analyses of 50,049 requests" in abstract,
            "abstract DEV exploratory evidence no longer separately identifiable")
    require("21.32\\%" in abstract and "23.01\\%" in abstract,
            "abstract must show both precisely denominated policy disagreement percentages")
    for count,display in ((10672,21.32),(11517,23.01)):
        require(math.isclose(round(count/50049*100,2),display,abs_tol=1e-10),
                "frozen switch denominator arithmetic mismatch")
        require(f"{count:,}" in r2 and f"{display:.2f}\\%" in r2,
                f"RQ2 policy switches not tied to event denominator: {count}")
    # Previous erroneous prose passed source-cell QA: protect explicitly.
    for block in (abstract,results,discussion,parts["conclusion"],highlights):
        require(not re.search(r"(?:21--23|21\.32|23\.01)\\?%\s+of\s+Memory\s+invocations",
                              block,re.I),"wrong Memory-invocation denominator reintroduced")
    require("event decisions disagree" in r2,
            "RQ2 does not identify *event decisions* as the switch denominator")

    # Distinguish weighted outcome estimates from actual unweighted invocation counts.
    for val in ("0.005391","0.003585","0.003646","0.001599",
                "8,704","9,105","8,629","9,168","1.337","1.797"):
        require(val in r2,"H1 RQ2 source-locked comparison missing: "+val)
    require("weighted" in r2.lower() and "unweighted call counts" in r2,
            "weighted quality estimand confused with actual raw call counts")
    require("higher" in r2 and "fewer" in r2,
            "frozen F/S quality+invocation Pareto direction omitted")
    require("not an experimentally isolated equal-resource effect" in r2,
            "equal resource causal qualification missing")
    require("approximate 1pp" in r2,"predeclared one-percentage-point threshold omitted")
    for val in ("0.348744","0.69165","1.76941"):
        require(val in main or val in supp,"unfavorable Memory/legacy cost reference lost "+val)
    require("pointwise" in main and "vectorized F-aligned gate" in main,
            "legacy timing must not be attributed to newer F-aligned gate")
    require("not" in discussion and "deployment-savings" in discussion,
            "no-serving-savings qualification missing")

    # Source Null validity: bounded positive evidence, one incomplete original subgate.
    for val in ("0.334942","0.303797","0.031145","76.78--76.80",
                "1,903--1,913"):
        require(val in r3,"RQ3 null positive/nonfloor evidence missing: "+val)
    require("pass the reported nondegeneracy checks" in r3,
            "valid observed Null checks missing")
    require("not" in r3 and "TRAIN-only Popularity" in r3 and
            "not measured and sealed before target reveal" in r3,
            "missing original same-cohort prereveal TRAIN popularity subgate")
    require("partially completed" in discussion,
            "Discussion must distinguish partial control validity from complete failure")
    for invalid in ("all preregistered null checks passed","entire h2 invalid",
                    "all original acceptance checks passed"):
        require(invalid not in main.lower(),"invalid all-or-none Null conclusion: "+invalid)

    # Each independent evidence type is explicitly scoped.
    require("KuaiLive room-ranking" in main and "M3 author ranking" in main,
            "different candidate/ranking units not distinguished")
    require("50,049" in r2 and "30,000" in r2,
            "DEV explanatory requests and H1 held-out requests confused")
    require("same" in results.lower() and "recording period" in results.lower(),
            "additional same-period cohort described as new period")
    require("4,096" in r3 and "nested" in r3,
            "4096 historical Null sample not identified as nested")
    require("retrospectively" in main and "sampled" in main,
            "sampled retrospective-label construction must remain distinct from online use")
    require("not a causal decomposition of the separate 30,000-target H1 contrast" in r2,
            "DEV accounting must not impersonate confirmatory mechanism")

    for k in ("krichene2020kdd","mao2024regression","mandi2024decisionfocused"):
        require(k in bib and k in main,"key prior-art reference absent "+k)
    citekeys=set(re.findall(r"@\w+\s*\{\s*([^,\s}]+)\s*,",bib))
    refs={k.strip() for g in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",main)
          for k in g.split(",")}
    require(refs.issubset(citekeys),"undefined BibTeX references: "+repr(refs-citekeys))
    require("candidate-aligned supervision" in highlights.lower(),
            "Highlights does not use consistent primary contribution wording")
    require("NOT VERIFIED" in supp,"supplement original null prereveal gap lost")
    return {
        "status":"N12_C8V_V0_SEMANTIC_SOURCE_AUDIT_PASS",
        "DEV_policy_disagreement_denominator_requests":50049,
        "SASRec_changed_request_decisions":10672,
        "SASRec_disagreement_percent":round(10672/50049*100,2),
        "GRU4Rec_changed_request_decisions":11517,
        "GRU4Rec_disagreement_percent":round(11517/50049*100,2),
        "H1_raw_calls_SAS_F_S":[8704,9105],
        "H1_raw_calls_GRU_F_S":[8629,9168],
        "H1_raw_calls_not_equal_budget":True,
        "H2_null_other_diagnostics_present":True,
        "H2_cohort_popularity_subgate_not_verified":True,
        "DEV_switch_accounting_not_new_H1_test":True,
        "private_TEST_read":False,
    }


def check(root: Path=ROOT) -> dict:
    return audit_text(
        (root/MANUSCRIPT).read_text(encoding="utf-8"),
        (root/SUPPLEMENT).read_text(encoding="utf-8"),
        (root/REFERENCES).read_text(encoding="utf-8"),
        (root/HIGHLIGHTS).read_text(encoding="utf-8"),
    )


if __name__=="__main__":
    print(json.dumps(check(),indent=2,ensure_ascii=False))
