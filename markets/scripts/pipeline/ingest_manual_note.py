#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))


def now_jst() -> str:
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")


def next_id(path: Path, prefix: str) -> str:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    nums = [int(n) for n in re.findall(rf"{re.escape(prefix)}-(\d+)", text)]
    n = (max(nums) + 1) if nums else 1
    return f"{prefix}-{n:04d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest manual Discord insight post")
    ap.add_argument("--root", default=".")
    ap.add_argument("--market", default="other-market")
    ap.add_argument("--category", choices=["ideas", "watchlist", "dev-tools", "other"], default="ideas")
    ap.add_argument("--title", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--source", default="discord:#poly-arb")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    market_dir = root / f"markets/{args.market}"
    market_dir.mkdir(parents=True, exist_ok=True)

    if args.category == "ideas":
        file_name, prefix = "ideas.md", "IDEA"
    elif args.category == "watchlist":
        file_name, prefix = "watchlist.md", "WATCH"
    elif args.category == "dev-tools":
        file_name, prefix = "dev-tools.md", "TOOL"
    else:
        file_name, prefix = "other.md", "MISC"

    path = market_dir / file_name
    eid = next_id(path, prefix)
    ts = now_jst()

    block = (
        f"\n- ID: {eid}\n"
        f"- Title: {args.title}\n"
        f"- Summary: {args.summary}\n"
        f"- Source: {args.source}\n"
        f"- Source Type: manual_discord\n"
        f"- Tags: インサイト分析\n"
        f"- Created At: {ts}\n"
        f"- Event Time: {ts}\n"
        f"- Updated: {ts}\n"
    )

    with path.open("a", encoding="utf-8") as f:
        f.write(block)

    print(f"ingested {eid} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
