#!/usr/bin/env python3
"""Assemble N7 S7.7 into the frozen S1-S9 supplement; refuse unexpected sources."""
from pathlib import Path
import subprocess

ROOT = Path("manuscript/kbs_latex")
combined = ROOT / "SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md"
addendum = ROOT / "SUPPLEMENTARY_S7_7_DEV_ESTIMATOR_EXPLORATORY_2026-10-13.md"
expected_git_blob = "3f9413f8ffe2a2ff1ef70640a3820d81b281055f"
marker = "\n\n---\n\n# S8. Distinct KuaiLive room-seed diagnostics and M3 frozen author-ranking robustness"

def main():
    original = combined.read_text()
    if "## S7.7 Nested-DEV" in original:
        if 'date: "12 October 2026"' in original:
            original = original.replace('date: "12 October 2026"', 'date: "13 October 2026"')
            combined.write_text(original)
            print("Updated supplement publication date after S7.7 integration")
        stale = "and is intended for incorporation into the final combined S1–S9 submission supplement during N8."
        if stale in original:
            combined.write_text(original.replace(stale, "within the final combined S1–S9 submission supplement."))
            print("Updated assembled supplement status to current final-package wording")
        else:
            print("S7.7 already assembled; no changes")
        return
    blob = subprocess.check_output(["git", "hash-object", str(combined)], text=True).strip()
    if blob != expected_git_blob:
        raise SystemExit("Refuse merge: original combined supplement is not the frozen approved source")
    if original.count(marker) != 1:
        raise SystemExit("Refuse merge: S7/S8 exact insertion boundary is missing")
    extra = addendum.read_text()
    if "Table S7.5." not in extra or "post-G5" not in extra:
        raise SystemExit("Addendum evidence-tier guard failed")
    paragraphs = extra.split("\n", 1)
    if not paragraphs[0].startswith("# Supplementary S7.7"):
        raise SystemExit("Unexpected addendum header")
    new_section = "## S7.7 Nested-DEV direct versus two-stage estimator sensitivity (exploratory)\n" + paragraphs[1].lstrip()
    merged = original.replace(marker, "\n\n" + new_section.rstrip() + marker)
    if merged.count("## S7.7 ") != 1 or merged.count("Table S7.5.") != 1:
        raise SystemExit("Merged section/table numbering not unique")
    if sum(line.startswith("# S") and line[3:4].isdigit() for line in merged.splitlines()) != 9:
        raise SystemExit("S1-S9 top-level section count changed")
    combined.write_text(merged)
    print("S7.7 inserted; original S1-S7.6 and S8-S9 preserved byte-for-byte")

if __name__ == "__main__":
    main()
