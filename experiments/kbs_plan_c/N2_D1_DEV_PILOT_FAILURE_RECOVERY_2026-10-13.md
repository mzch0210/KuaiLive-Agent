# N2-D1 failed-run root-cause and corrected restart record

**Date:** 2026-10-13. **Failure:** [GitHub run #38336227770](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38336227770), commit `a97414890e78709c8d43fc9c121d37e4953b0e8d`. Hosted synthetic job **PASS** (4 tests); self-host job `115096934376` failed **before data validation/model training** in the `Verify private corrected 50,049-event DEV source and Python packages` step.

## Verified root cause (full GitHub job logs)

```
ModuleNotFoundError: No module named 'sklearn'
Process completed with exit code 1.
```

The job had executed repo checkout and filesystem existence checks, then attempted `import pandas,numpy,sklearn` from `$HOME/venvs/kuailive-gpu/bin/python`. Its default Python import path omits the prior working scikit-learn bundle. The same self-host runner `kuailive-3090-01` ran [G4 successful extra-seed DEV gates #38223562473](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38223562473) using:

```bash
export PYTHONPATH="$PWD/e2-bundle:$HOME/.cache/kuailive-agent-kbs/e2-py312-sklearn-v1:$HOME/.cache/kuailive-agent-kbs/audit-py312-tools-v1"
```

The successful G4 job verified `sklearn.__version__ == '1.5.2'` in that environment. N2-D1 corrects every private-host `run` step to use the same offline cached scientific-package roots, while the script remains in `$PWD/analysis/kbs_plan_c`. No `pip install` is run on the self-host, avoiding untracked dependency/version changes. The pipeline explicitly checks the cache directory before attempting DEV training.

**Scientific interpretation:** This run has **no actual DEV model fits, no DEV comparison, and no evidence about whether Direct beats TwoStage**. No G5 TEST label access or frozen G5 policy edits. The former N3 paper PASS is unaffected.

## Fix acceptance and stop rules

1. Hosted synthetic test must PASS.
2. Self-host import must find exactly cached scikit-learn 1.5.x and maintain source DEV-only checksum, 50,049 rows, corrected Memory rule.
3. Group-disjoint nested fit must PASS on the existing private DEV rows without TEST access.
4. Only aggregate DEV pilot metrics are exported; no event records, user IDs or fitted private model files.
5. Any new error must be diagnosed from the failed step and logs before further action; **do not falsely report the experiment completed**.

A new source-controlled commit changes only the test workflow and this postmortem; original `main.tex`, N3 Results and G5 policy/result files remain unchanged.
