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
    # Preserve other SHA256 displays (bold provenance and plain wide-table cells).
    source = re.sub(
        r"\\textbf\{([a-f0-9]{64})\}",
        lambda m: "\\textbf{\\seqsplit{" + m.group(1) + "}}",
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
        block = re.sub(
            r"(?<!\\seqsplit\{)(?<![a-f0-9])([a-f0-9]{64})(?![a-f0-9])",
            lambda token: "\\seqsplit{" + token.group(1) + "}",
            block,
        )
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
    markdown_path = path.with_name("SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md")
    markdown = markdown_path.read_text(encoding="utf-8")
    expected_tables = len(re.findall(r"\*\*Table S[1-9]\.\d+\.", markdown))
    if tables != expected_tables or expected_tables < 23:
        raise ValueError(
            f"Source/TeX supplementary table-count mismatch: markdown {expected_tables}, TeX {tables}"
        )
    if rotations < 3:
        raise ValueError(f"Expected several publication-width tables; found {rotations}")
    # Pandoc emits the supplementary caption as a bold paragraph preceding
    # its longtable. Move this caption *inside* the landscape page so the
    # caption cannot be stranded on the preceding portrait page.
    source, n_captions = re.subn(
        r"(\\textbf\{Table S\d+\.\d+\.[^\n]*\})\s+(\\begin\{landscape\}\n)",
        lambda m: m.group(2) + m.group(1) + "\n\n",
        source,
    )
    if n_captions != rotations:
        raise ValueError(
            f"Each landscape table needs a caption on its own page: "
            f"{n_captions} of {rotations}"
        )
    path.write_text(source, encoding="utf-8")
    return {"breakable_sha256": n_hash, "tables": tables, "landscape_tables": rotations}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: kbs_supplement_tex_postprocess.py path/to/supplementary_information.tex")
    print(polish(Path(sys.argv[1])))
