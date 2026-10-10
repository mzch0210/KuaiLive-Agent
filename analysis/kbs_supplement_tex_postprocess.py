"""Deterministic academic typesetting corrections for Pandoc-created S1--S9 TeX.

No numeric/word content is changed: long cryptographic hashes are line-breakable,
wide evidence tables use landscape pages, and paired interval commas permit
typographic wrapping. This file is used by the source-controlled PDF build.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


def polish(path: Path) -> dict:
    source = path.read_text(encoding="utf-8")
    if source.count(r"\begin{document}") != 1:
        raise ValueError("Input must be a Pandoc standalone LaTeX document")
    source = source.replace(
        r"\begin{document}",
        "\\usepackage{seqsplit}\n\\usepackage{pdflscape}\n"
        "\\setlength{\\tabcolsep}{2pt}\n\\begin{document}",
        1,
    )
    source, n_hash = re.subn(
        r"\\texttt\{([a-f0-9]{64})\}",
        lambda m: "\\texttt{\\seqsplit{" + m.group(1) + "}}",
        source,
    )
    # The source PDF displays exact SHA256 values, including their intact bytes,
    # but permits a line break between individual characters.
    if n_hash < 14:
        raise ValueError(f"Expected archived SHA256 representation count >=14, got {n_hash}")
    source = re.sub(
        r"(?<=\d),(?=[+−-]\d)",
        lambda _: ",\\allowbreak ",
        source,
    )
    rotations = 0
    tables = 0

    def convert_table(m: re.Match[str]) -> str:
        nonlocal rotations, tables
        block = m.group()
        tables += 1
        header = block.split(r"\midrule", 1)[0]
        n_col = header.count(r"\begin{minipage}")
        if n_col >= 7 or (n_col == 5 and "Fit/selection information" in header):
            rotations += 1
            return "\\begin{landscape}\n{\\footnotesize\n" + block + "\n}\\end{landscape}"
        if n_col >= 5:
            return "{\\footnotesize\n" + block + "\n}"
        return block

    source = re.sub(
        r"\\begin\{longtable\}.*?\\end\{longtable\}",
        convert_table, source, flags=re.S,
    )
    if tables != 23:
        raise ValueError(f"Supplement must have exactly 23 source tables; found {tables}")
    if rotations < 3:
        raise ValueError(f"Expected several publication-width tables; found {rotations}")
    path.write_text(source, encoding="utf-8")
    return {"breakable_sha256": n_hash, "tables": tables, "landscape_tables": rotations}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: kbs_supplement_tex_postprocess.py path/to/supplementary_information.tex")
    print(polish(Path(sys.argv[1])))
