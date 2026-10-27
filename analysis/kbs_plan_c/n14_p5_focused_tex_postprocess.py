"""N14 focused-only Pandoc TeX postprocessor, separate from frozen full S1--S10 audit.

Keeps exact 64-character SHA representations and every focused-source table.
The legacy S1--S10 postprocessor's >=14-hash, >=23-table and 3-landscape-table
assumptions are intentionally inapplicable to the narrower journal supplement.
"""
from pathlib import Path
import re
import sys


def polish(tex_path: Path, markdown_path: Path) -> dict:
    source=tex_path.read_text(encoding="utf-8")
    if source.count(r"\begin{document}")!=1:
        raise ValueError("Expected one standalone LaTeX document")
    original=markdown_path.read_text(encoding="utf-8")
    if "NOT VERIFIED" not in original or "0.031145" not in original:
        raise ValueError("Original H2 acceptance/multiplicity disclosure missing")
    source=source.replace(r"\begin{document}",
         "\\usepackage{seqsplit}\n\\usepackage{pdflscape}\n"
         "\\setlength{\\tabcolsep}{3pt}\n\\begin{document}",1)
    source,n_hash=re.subn(r"\\texttt\{([a-f0-9]{64})\}",
      lambda m: "\\texttt{\\seqsplit{"+m.group(1)+"}}",source)
    # Exact code-hash characters are preserved, but line wrapping is permitted.
    source=re.sub(r"(?<=\d),(?=[+−-]\d)",lambda _:r",\allowbreak ",source)
    expected=len(re.findall(r"^\*\*Table S10\.(?:9|14)\.", original,flags=re.M))
    actual=len(re.findall(r"\\begin\{longtable\}",source))
    if expected!=2 or actual!=expected:
        raise ValueError(f"Two copied S10 aggregate result tables required: {expected}, generated {actual}")
    # Do not silently relocate, delete or alter any table or numeric content.
    tex_path.write_text(source,encoding="utf-8")
    return {"breakable_sha256":n_hash,"focused_source_tables":expected,"generated_longtables":actual}


if __name__=="__main__":
    if len(sys.argv)!=3:
        raise SystemExit("Usage: n14_p5_focused_tex_postprocess.py generated.tex focused.md")
    print(polish(Path(sys.argv[1]),Path(sys.argv[2])))
