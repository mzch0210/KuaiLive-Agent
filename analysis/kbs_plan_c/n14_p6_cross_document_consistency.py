#!/usr/bin/env python3
"""N14 P6 consistency contract: main/focused supplement/highlights, no science rewriting."""
from pathlib import Path
import re
from n14_p2_science_archive_contract import check as original_science_check, require, LATEX
main=(LATEX/"main.tex").read_text()
supp=(LATEX/"SUPPLEMENTARY_INFORMATION_N14_FOCUSED_2026-10-27.md").read_text()
hist=(LATEX/"SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md").read_text()
high=(LATEX/"Highlights.txt").read_text().splitlines()
original_science_check()
require(len(high)==5 and all(x.startswith("- ") and len(x)<=85 for x in high),"exactly five <=85-character Highlights")
require(not any("authentic histories outperform" in x.lower() for x in high),"old H2 independent Highlight still present")
require(all(not re.search(r"\bRQ[123]\b",area) for area in (main,supp)),"obsolete parallel RQs")
for text in ("0.005391","0.003585","0.348744","50,049","10,672","11,517","29.203","30.537","29.008","30.809","0.000600","0.000800"):
    require(text in main and text in supp,"main/focused mismatch: "+text)
for text in ("0.031145","0.334942","0.303797","NOT VERIFIED","0.027389","0.035098"):
    require(text in supp and text in hist,"Holm third-member archived disclosure lost: "+text)
for text in ("Table N14-S1","Table N14-S2","original Table S10.9","original Table S10.14"):
    require(text in supp,"traceable table caption missing: "+text)
for text in ("focused Supplement Table N14-S1","focused Supplement Table N14-S2"):
    require(text in main,"main-to-journal supplement crossref missing: "+text)
require(not re.search(r"\bSupplementary (?:S\d+|Table S10\.)",main),"legacy journal supplement reference in main")
require("candidate regime" in main.lower() and "candidate regime" in supp.lower(),"one-question topic missing")
require("corrected" in main and "corrected" in supp,"uncorrected sampled competing explanation hidden")
print("N14 P6 MAIN-FOCUSED-HIGHLIGHTS SOURCE CONSISTENCY PASS")
