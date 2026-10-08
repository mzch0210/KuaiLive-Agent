"""Read-only provenance and artifact-availability preflight for KBS paired-candidate diagnostics.

No model inference, training, TEST-label inspection or parameter selection takes place here.
Stdlib only, suitable for GitHub-hosted ubuntu runners. Results are emitted even when
original checkpoints are no longer downloadable.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

SOURCE_RUNS = {
    "room_collision_data": 35554842873,
    "latency_checkpoints": 35559499838,
    "full_active_results": 35580324870,
    "seed_robustness": 35729896175,
    "evidence_decomposition": 35829433706,
    "sampled_gate": 35571827672,
}
CRITICAL_ARTIFACTS = {
    "room_collision_data": ["room-collision-data-35554842873"],
    "latency_checkpoints": [
        "latency-room-checkpoint-35559499838",
        "latency-streamer-checkpoint-35559499838",
    ],
    "full_active_results": ["full-active-dual-id-35580324870"],
    "seed_robustness": ["seed-20260918"],
    "evidence_decomposition": ["kbs-kuailive-regime-decomposition-35829433706"],
    "sampled_gate": ["gate-compression-accuracy-35571827672"],
}

def github_json(path: str, token: str, repo: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "KBS-fixed-checkpoint-audit/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"GitHub API {exc.code} for {path}") from exc

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=pathlib.Path, default=pathlib.Path("diagnostic_preflight"))
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "mzch0210/KuaiLive-Agent"))
    args = ap.parse_args()
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Set GH_TOKEN/GITHUB_TOKEN with read access to Actions metadata.", file=sys.stderr)
        return 2
    args.out_dir.mkdir(parents=True, exist_ok=True)
    sources = {}
    errors = {}
    for label, run_id in SOURCE_RUNS.items():
        try:
            run = github_json(f"actions/runs/{run_id}", token, args.repo)
            # Two requests per run; metadata only, no large download.
            meta = github_json(f"actions/runs/{run_id}/artifacts?per_page=100", token, args.repo)
            artifacts = [
                {
                    "id": a["id"], "name": a["name"], "size_in_bytes": a.get("size_in_bytes"),
                    "expired": a.get("expired"), "created_at": a.get("created_at"),
                    "expires_at": a.get("expires_at"), "digest": a.get("digest"),
                    "archive_download_url": a.get("archive_download_url"),
                }
                for a in meta.get("artifacts", [])
            ]
            names = {a["name"] for a in artifacts if a.get("expired") is False}
            want = CRITICAL_ARTIFACTS[label]
            sources[label] = {
                "run_id": run_id, "run_status": run.get("status"),
                "conclusion": run.get("conclusion"), "head_sha": run.get("head_sha"),
                "run_created_at": run.get("created_at"),
                "available_expected_artifacts": [x for x in want if x in names],
                "missing_or_expired_expected_artifacts": [x for x in want if x not in names],
                "artifacts": artifacts,
            }
        except Exception as exc:
            errors[label] = str(exc)
            sources[label] = {"run_id": run_id, "error": str(exc)}
    ck = sources["latency_checkpoints"]
    pairs_available = (
        len(ck.get("available_expected_artifacts", [])) == 2
        and ck.get("conclusion") in ("success", "failure")
    )
    report = {
        "protocol": "KBS_FIXED_CHECKPOINT_CANDIDATE_DIAGNOSTIC_2026-10-08",
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repo": args.repo,
        "source_runs": sources,
        "errors": errors,
        "checkpoint_pair_from_original_latency_run_available": pairs_available,
        "stage_b_policy": (
            "Eligible for checksum and checkpoint compatibility verification; NOT auto-authorized to run TEST"
            if pairs_available else
            "BLOCKED: original room+streamer checkpoint pair not both visible in named latency run."
            " Search immutable cache elsewhere; do not substitute per-user scores for model weights."
        ),
        "frozen_test_status": "UNCHANGED — this preflight does not download ranking results or inspect TEST targets",
    }
    (args.out_dir / "preflight.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# KBS fixed-checkpoint diagnostic — Stage A preflight",
        "",
        f"Repository: `{args.repo}`",
        f"Audit UTC: {report['created_utc']}",
        "",
        "| Evidence source | Run | Run conclusion | Expected artifacts available | Missing / expired |",
        "|---|---:|---|---|---|",
    ]
    for k, v in sources.items():
        lines.append(
            f"| {k} | {v['run_id']} | {v.get('conclusion', 'ERROR')} | "
            f"{', '.join(v.get('available_expected_artifacts', [])) or 'none'} | "
            f"{', '.join(v.get('missing_or_expired_expected_artifacts', [])) or 'none'} |"
        )
    lines += [
        "",
        "**Original fixed checkpoint pair accessible by Actions metadata:** "
        + ("yes" if pairs_available else "no"),
        "",
        "**Decision:** " + report["stage_b_policy"],
        "",
        "This is an artifact-availability audit only; no ranking scores were recomputed.",
        "Artifacts absent here may be present in a local self-hosted cache, which must be separately verified.",
        "",
    ]
    (args.out_dir / "preflight.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
