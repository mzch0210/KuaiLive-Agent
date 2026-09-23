from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

import kbs_twitch_competitive_baselines as base


def _parse_wrapper_args(argv: list[str]) -> tuple[Path, Path]:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--official-oof", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    known, _ = ap.parse_known_args(argv[1:])
    return known.official_oof, known.out_dir


def make_oof_aligned_dev_events(official_oof: Path):
    frozen = pd.read_csv(
        official_oof,
        usecols=["user_id", "target_streamer", "target_step"],
    ).astype(int)
    if frozen.user_id.duplicated().any():
        raise RuntimeError("Frozen P1.2 OOF must contain exactly one DEV event per user")

    def dev_events_oof_aligned(
        d: pd.DataFrame,
        p1: int,
        p2: int,
        seq_len: int,
    ) -> list[dict]:
        eligible = d[d.stop < p2]
        grouped = eligible.groupby("user", sort=False)
        rows: list[dict] = []

        for r in frozen.itertuples(index=False):
            uid = int(r.user_id)
            target = int(r.target_streamer)
            step = int(r.target_step)
            if step < p1 or step >= p2:
                raise RuntimeError(f"Frozen OOF target outside DEV interval: user={uid} step={step}")
            try:
                g = grouped.get_group(uid)
            except KeyError as exc:
                raise RuntimeError(f"Frozen OOF user missing from eligible Twitch rows: user={uid}") from exc

            target_rows = g[(g.start == step) & (g.streamer == target)]
            if target_rows.empty:
                raise RuntimeError(
                    f"Frozen OOF target not found in raw Twitch data: user={uid} streamer={target} step={step}"
                )

            # Same-timestamp ordering in the original LiveRec helper depended on the
            # pandas sorting implementation. Anchor the target to the frozen P1.2 OOF
            # and use only strictly earlier interactions for the auxiliary context.
            # This is deterministic, leakage-free, and preserves the exact frozen
            # DEV target/candidate protocol across pandas versions.
            hist = (
                g[g.start < step]
                .sort_values("start", kind="mergesort")
                .tail(seq_len)
                .streamer.astype(int)
                .tolist()
            )
            rows.append(
                {
                    "user_id": uid,
                    "target_streamer": target,
                    "target_step": step,
                    "history": hist,
                }
            )

        return rows

    return dev_events_oof_aligned


def main() -> None:
    official_oof, out_dir = _parse_wrapper_args(sys.argv)
    base.dev_events = make_oof_aligned_dev_events(official_oof)
    base.main()

    report_path = out_dir / "twitch_dev_strong_base_benchmark.json"
    report = json.loads(report_path.read_text())
    report["event_alignment"] = (
        "DEV user/target/step triplets are anchored to the frozen P1.2 OOF; "
        "auxiliary histories use only raw interactions strictly before the frozen target step."
    )
    report["same_timestamp_policy"] = (
        "Strict-before-target context removes pandas-version-dependent ordering among interactions sharing a timestamp."
    )
    report_path.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
