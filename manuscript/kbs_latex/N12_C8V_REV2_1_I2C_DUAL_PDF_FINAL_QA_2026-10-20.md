# N12 Rev2.1 I2-C final scientific and dual-PDF QA (2026-10-20)

**MACHINE QA PASS, no new scientific TEST, no independent human scientific sign-off.**

## Rebuilt source identity

- Author-selected Path A, I2-A/B micro-revision commit: **7e4c5a6f616e22226f55e2396815d48cc838bf96**. It changed **three prose locations in main.tex**, added **one CIKM 2024 BibTeX entry**, and added I2 source regression tests to the C8V semantic dual-PDF workflow. The Supplement and Results source/figures/equations were not edited.
- Current branch's subsequent governance commit did not change manuscript science. Both CI runs below target **7e4c5a6f** and passed BOTH jobs:

| Contract | GitHub Actions run | MAIN job | SUPPLEMENT job | Final page numbers |
| --- | --- | --- | --- | --- |
| C8V scientific, source+semantic and I2 Path A regression | [#39351014765](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39351014765) | SUCCESS, job #118394921288 | SUCCESS, job #118394921039 | **38 main / 47 supplementary** |
| C7 frozen tables, source equations and supplement full-cell | [#39351014645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39351014645) | SUCCESS, job #118394920816 | SUCCESS, job #118394920649 | **38 main / 47 supplementary** |

- C8V artifacts: main **12232693237**, ZIP SHA256 **610346354b77c2e48df8a4a57d444b87bfcb7c8be951025b458d5d91aa91904c**; supplement **12233555700**, ZIP SHA256 **af4cf79a167c45b634c76eefaed51245dc05f04ae376dcbeb584affd22a71b8e**. Artifacts expire **2026-12-19 UTC** under current 60-day policy; preserve an authorized long-lived submission archive before that date.
- C7 artifacts: main **12232833497**, supplement **12233610531**, both successful. Independent duplicate PDF builds are CI redundancy, not independent datasets.

## Verified scope and limits

The C8V main job runs preexisting C6 bounded-results/equation scientific contract, C8V semantic audit and negative tests, C7 source-to-Supp full-row/cell regression and tests, then the newly introduced I2 Path A scientific claim test and 5 negative guard tests. It confirms Results frozen source blocks, major original counts/effect sizes, equation identities, original 7 retained and 4 relocated tables, whole migrated table-cell contract, weighted-vs-unweighted call distinctions, 21.32%/23.01% request denominators, 1.337/1.797pp unequal-call limit, RQ3 partial prereveal acceptance, negative legacy timing and original unchanged source evidence. LaTeX final logs passed both zero-overfull and fatal-error guards; final pass had resolved references. A first compilation pass emits expected provisional citation warnings until BibTeX runs; these are NOT evidence of unresolved final PDF bibliography, and later passes completed successfully.

Main PDF increased 37->**38** pages following editorial citation and paragraph updates. Supplement remains **47** pages. Do not write 37p after this point. No PDF content was manually signed or independently scientifically validated by a human.

The only added scholarly reference is Subbiah, Rendle & Aggarwal, *Improved Estimation of Ranks for Learning Item Recommenders with Negative Sampling*, CIKM 2024 pp. 4066–4070, DOI 10.1145/3627673.3679943. Source bibliographic comparison: https://dblp.org/rec/conf/cikm/SubbiahRA24 and Google Research https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ .

**I2-C final disposition: PASS. Next I2-D: internal adversarial contribution audit and independent HUMAN methods/routing expertise review, NOT yet signed. C8-A responsible-author submission signoff pending.**
