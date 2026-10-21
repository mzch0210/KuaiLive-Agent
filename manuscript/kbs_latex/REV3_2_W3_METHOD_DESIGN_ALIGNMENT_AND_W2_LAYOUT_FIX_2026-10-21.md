# Rev3.2 W3 — Framework / Experimental Design alignment and W2 typesetting fix

**2026-10-21 | W3 SOURCE EDITED / STATIC INVARIANTS PASS / FINAL C7-C8V IN PROGRESS / W4 NOT STARTED.**

## Root cause and fix
The previous W2 C7 #39429571240 and C8V #39429583687 were completed/FAILURE exclusively at the main PDF zero-overfull step. Both successfully compiled the 40-page main PDF and supplement. Extracted official main.log from C8V main artifact 12267137996 shows: **Overfull \\hbox (10.65091pt too wide) in paragraph at lines 549–550**, the moved Twitch DEV feature-ablation sentence. This is genuine typesetting and must not be solved by disabling the zero-overfull guard.

New science-edit commit `bf1329bd4cc1894a67f95a4487407c7a4ab1c058` rephrases that sentence into shorter, clearer sentences while retaining its three original gains (0.00838, 0.00372, 0.00160), common retrospective DEV-call setting and Supplement S10.16 pointer. W3 also rewrites framework and experimental-design introduction, locates the previously frozen additional-target protocol before retrospective candidate/source controls, and distinguishes online pretarget inputs from outcome-dependent diagnostics. The H2 original prereveal Popularity margin **not verified** remains explicit; LaTeX-visible \\emph{} replaces literal markdown bold markers, without changing the underlying admission.

## Static integrity
GitHub source read/edit comparison before update: **all nine table environment sources (including seven Results tables) byte-identical**, all **11 equation/align environments byte-identical**, **55 LaTeX labels preserved** (the order of existing formula blocks within their sections is unchanged); Results section was changed only in the paragraph causing layout failure. Bibliography, Highlights, Supplement, TEST and experiments untouched. New main.tex git blob: `cf63f19f7f8ec9e18eef0e9a91e13eabbc2092fe`.

## Workflow verification
New main-science commit triggers:
- C7 [#39521236360](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39521236360), IN_PROGRESS when recorded.
- C8V [#39521236359](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39521236359), IN_PROGRESS when recorded.

**Do not declare W2+W3 PDF PASS until both run success and the actual PDF/Overfull checks complete.** On failure inspect failing step and generated main.log, not only high-level workflow status; preserve numerical/semantic CI guards. Original W2 source `9e1e5d68...` and W3 `bf1329bd...` are separate from earlier Rev3.0 39-page verified PDF. W4 Intro/RW and later W6 Supplement work remain not started. KBS author-side issues, data rights, AI disclosure and journal Guide remain pending.
