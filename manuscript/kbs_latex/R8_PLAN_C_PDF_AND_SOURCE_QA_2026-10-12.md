# R8 technical PDF and manuscript QA

**Date:** 2026-10-12. **Gate:** manuscript technical PDF PASS; complete KBS submission **HOLD** until author facts, rights, publisher-specific instructions and author-approved final PDF are verified.

## Exact artifact and source

- Source [commit 0c2ea127d1a9e7a2030a2db2d67e4fdd7266c443](https://github.com/mzch0210/KuaiLive-Agent/commit/0c2ea127d1a9e7a2030a2db2d67e4fdd7266c443): `main.tex` blob `f46540dce8b076e08937e8f5912048eeff994ad1`; BibTeX blob `a33cb506fc2d08b422232a10e91a9d06c44044f5`. R6 supplementary S1–S9 blob `3f9413f8ffe2a2ff1ef70640a3820d81b281055f` remains unchanged.
- Original matching [GitHub Actions manuscript build #38271581420](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38271581420) **success**, artifact **11757690369**. The exact **artifact ZIP's** `main.pdf` is **37 pages**, **507,141 bytes**, letter format; PDF SHA256 `0177149bc5955ab17c76b99e660df7bb462a428ba143119b9aafecafceba69f1`. This is a temporary Actions artifact, not a permanent public archive.
- Original build `main.log`: no overfull hbox/vbox diagnostics, no fatal LaTeX errors or undefined citations/references. Three nonfatal underfull hbox cases and one float-position warning.
- Rendered all 37 pages for layout overview, visually inspected detailed pages 1, 4, 13–14, 20–24, 27–28, 30, 32–33 and 37. No observed clipped/overlapping tables; key Twitch and M3 rates/results (p.23) and adverse warm-path cost table (p.28) are legible. Automated PDF text-block coordinates stay inside page bounds.

## Static consistency gate

- Eight main sections, 28 subsections, 53 distinct labels; no missing `\\ref`/`\\eqref` targets.
- 30 unique cited keys resolve among 31 unique BibTeX entries, no duplicate citation keys.
- The **197-word** frontmatter Abstract reflects all three ranked units, Twitch 44,221 TEST with 15.04% selector calls and NDCG 0.58211 to 0.58983, original paired room 10,222 events and -0.04120 to +0.04631 sampled-to-full reversal, and M3 47,575 TEST with main seed 0.25800 to 0.30287 and Always Memory 0.34679.
- Main Results continue to disclose M3 30%-DEV policy cap (not fixed TEST cap), History 35.47% actual TEST calls, and warmed DEV Memory 0.803 ms versus Utility 1.802 ms. R0 and R6 frozen evidence remains the metric source of truth; no rerun of hidden TEST or claim of independent data release was performed.

## Residual R8 submission blockers

1. Human-verified ordered authors, affiliations, corresponding author and full CRediT contributions.
2. Human-confirmed funding, competing interests, permission/licence status and truthful AI-assisted manuscript-preparation declaration according to the current Elsevier policy.
3. Valid data/code availability statement, repository rights and persistent accessible sources where legally possible; no stable DOI is yet evidenced.
4. KBS-specific submission Guide for Authors/Highlights/abstract/declarations requirements; the journal guide currently returned HTTP 403 to automated retrieval.
5. Rebuild and re-inspect the final author-approved full PDF after these fields are completed. The current verified PDF still says `Anonymous Authors`.

**Verdict:** R7 literature + R8 current PDF engineering are checked. R8 complete submission **HOLD**. Do not mark all 12 R0 issues formally publication-closed before author signoff and final artifact verification.
