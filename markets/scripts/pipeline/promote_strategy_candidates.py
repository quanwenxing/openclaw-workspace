#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List

JST = timezone(timedelta(hours=9))


def now_jst() -> str:
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")


def parse_blocks(text: str) -> List[Dict[str, str]]:
    blocks = []
    parts = re.split(r"\n(?=- ID:\s*STRAT-\d+)", text)
    for part in parts:
        if "- ID: STRAT-" not in part:
            continue
        b = {}
        for line in part.splitlines():
            m = re.match(r"-\s*([^:]+):\s*(.*)", line)
            if m:
                b[m.group(1).strip()] = m.group(2).strip()
        b["_raw"] = part
        blocks.append(b)
    return blocks


def has_text(v: str) -> bool:
    return bool(v and v.strip() and v.strip().lower() not in {"", "n/a", "none", "未設定"})


def evaluate_gate(block: Dict[str, str]) -> Dict[str, bool]:
    return {
        "hypothesis": has_text(block.get("Hypothesis", "")),
        "entry_exit": has_text(block.get("Entry Signal", "")) and has_text(block.get("Exit Signal", "")),
        "risk": has_text(block.get("Risk", "")),
        "tools": has_text(block.get("Required Data/Tools", "")),
        "derived": has_text(block.get("Derived From IDs", "")),
    }


def rewrite_block(block: Dict[str, str], new_status: str, reason: str) -> str:
    lines = block["_raw"].splitlines()
    out = []
    updated_set = False
    status_set = False
    reason_set = False
    for line in lines:
        if line.startswith("- Status:"):
            out.append(f"- Status: {new_status}")
            status_set = True
            continue
        if line.startswith("- Updated:"):
            out.append(f"- Updated: {now_jst()}")
            updated_set = True
            continue
        if line.startswith("- Review Gate:"):
            out.append(f"- Review Gate: {reason}")
            reason_set = True
            continue
        out.append(line)

    if not status_set:
        out.append(f"- Status: {new_status}")
    if not reason_set:
        out.append(f"- Review Gate: {reason}")
    if not updated_set:
        out.append(f"- Updated: {now_jst()}")
    return "\n".join(out)


def update_index(idx_path: Path, strat_id: str, new_status: str) -> None:
    if not idx_path.exists():
        return
    lines = idx_path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if line.startswith(f"| {strat_id} "):
            cols = [c.strip() for c in line.strip("|").split("|")]
            # ID,Title,Market,Type,Priority,Status,Sources,Updated
            if len(cols) >= 8:
                cols[5] = new_status
                cols[7] = now_jst()
                lines[i] = "| " + " | ".join(cols) + " |"
            break
    idx_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Promote strategy candidates by review gate")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cand = root / "markets/strategy-candidates/candidates.md"
    idx = root / "markets/strategy-candidates/index.md"

    if not cand.exists():
        print("no_candidates_file")
        return 0

    text = cand.read_text(encoding="utf-8")
    blocks = parse_blocks(text)
    promoted = 0
    reviewed = 0

    new_text = text
    for b in blocks:
        strat_id = b.get("ID", "")
        status = b.get("Status", "new").strip().lower()
        if not strat_id or status not in {"new", "reviewing"}:
            continue

        gate = evaluate_gate(b)
        ok = all(gate.values())
        reason = ",".join([k for k, v in gate.items() if v]) + " / missing:" + ",".join([k for k, v in gate.items() if not v])
        target_status = "reviewing" if ok else "new"

        replaced = rewrite_block(b, target_status, reason)
        new_text = new_text.replace(b["_raw"], replaced)
        reviewed += 1
        if ok and status != "reviewing":
            promoted += 1
            update_index(idx, strat_id, "reviewing")

    cand.write_text(new_text, encoding="utf-8")
    print(f"reviewed={reviewed} promoted={promoted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
