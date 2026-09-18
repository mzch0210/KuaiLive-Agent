from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

CLICK_COLS = ["user_id", "live_id", "streamer_id", "timestamp", "watch_live_time"]
ROOM_COLS = ["p_date", "live_id", "streamer_id", "live_type", "start_timestamp", "end_timestamp", "live_content_category", "live_name_id"]


def normalize_category(s: pd.Series) -> pd.Series:
    return s.astype("string").str.strip().str.lower()


def prepare(data_dir: Path, out_dir: Path, scope: str = "shop", chunksize: int = 500_000):
    click_path = data_dir / "click.csv"
    room_path = data_dir / "room.csv"
    if not click_path.exists() or not room_path.exists():
        raise FileNotFoundError(f"Expected click.csv and room.csv under {data_dir}")

    rooms = pd.read_csv(room_path, usecols=ROOM_COLS)
    rooms = rooms.drop_duplicates(subset=["live_id"], keep="first")
    rooms["live_content_category"] = normalize_category(rooms["live_content_category"])
    if scope == "shop":
        rooms = rooms.loc[rooms["live_content_category"].eq("shop")].copy()
    elif scope != "all":
        raise ValueError("scope must be 'shop' or 'all'")

    room_ids = set(rooms["live_id"].astype("int64").tolist())
    room_streamer = rooms.set_index("live_id")["streamer_id"].astype("int64")
    event_parts = []
    total_in = total_keep = mismatch = 0
    for chunk in pd.read_csv(click_path, usecols=CLICK_COLS, chunksize=chunksize):
        total_in += len(chunk)
        chunk = chunk[chunk["live_id"].isin(room_ids)].copy()
        if chunk.empty:
            continue
        expected = chunk["live_id"].map(room_streamer)
        same = expected.astype("Int64").eq(chunk["streamer_id"].astype("Int64"))
        mismatch += int((~same.fillna(False)).sum())
        chunk = chunk.loc[same.fillna(False)].copy()
        total_keep += len(chunk)
        event_parts.append(chunk)

    if not event_parts:
        raise RuntimeError(f"No click events retained for scope={scope}")
    events = pd.concat(event_parts, ignore_index=True)
    for c in ["user_id", "live_id", "streamer_id", "timestamp", "watch_live_time"]:
        events[c] = pd.to_numeric(events[c], errors="coerce")
    events = events.dropna(subset=["user_id", "live_id", "streamer_id", "timestamp"])
    events[["user_id", "live_id", "streamer_id", "timestamp", "watch_live_time"]] = events[["user_id", "live_id", "streamer_id", "timestamp", "watch_live_time"]].fillna(0).astype("int64")
    events = events.sort_values(["user_id", "timestamp", "live_id"], kind="mergesort").reset_index(drop=True)

    out_dir.mkdir(parents=True, exist_ok=True)
    events.to_pickle(out_dir / "events.pkl")
    rooms.to_pickle(out_dir / "rooms.pkl")

    stats = pd.DataFrame([{
        "scope": scope,
        "raw_click_rows": total_in,
        "retained_click_rows": len(events),
        "retained_users": events["user_id"].nunique(),
        "retained_streamers": events["streamer_id"].nunique(),
        "retained_live_rooms": events["live_id"].nunique(),
        "room_rows": len(rooms),
        "streamer_mismatch_rows_dropped": mismatch,
    }])
    stats.to_csv(out_dir / "dataset_stats.csv", index=False)
    print(stats.to_string(index=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--scope", choices=["shop", "all"], default="shop")
    ap.add_argument("--chunksize", type=int, default=500_000)
    args = ap.parse_args()
    prepare(args.data_dir, args.out_dir, args.scope, args.chunksize)


if __name__ == "__main__":
    main()
