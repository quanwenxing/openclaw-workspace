#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Tuple

JST = timezone(timedelta(hours=9))


def now_jst() -> str:
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def next_id(path: Path, prefix: str) -> str:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    nums = [int(n) for n in re.findall(rf"{re.escape(prefix)}-(\d+)", text)]
    n = (max(nums) + 1) if nums else 1
    return f"{prefix}-{n:04d}"


def classify_category(text: str) -> str:
    lo = text.lower()
    if any(k in lo for k in ["0x", "wallet", "address", "watch"]):
        return "watchlist"
    if any(k in lo for k in ["api", "bot", "script", "sdk", "automation", "websocket"]):
        return "dev-tools"
    if any(k in lo for k in ["arb", "edge", "mispricing", "entry", "exit", "odds", "strategy"]):
        return "ideas"
    return "other"


def market_from_text(text: str) -> str:
    lo = text.lower()
    hit = []
    if "polymarket" in lo:
        hit.append("polymarket")
    if "kalshi" in lo:
        hit.append("kalshi")
    if "opinion" in lo or "opinionlabs" in lo:
        hit.append("opinion")
    if len(set(hit)) >= 2:
        return "multi-market"
    if len(hit) == 1:
        return hit[0]
    return "other-market"


def ensure_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"entries": {}}


def block_for(category: str, entry_id: str, title: str, summary: str, source: str, message_id: str, content_hash: str, created_at: str, updated: str) -> str:
    return (
        f"\n<!-- MANUAL_ENTRY_START:{message_id} -->\n"
        f"- ID: {entry_id}\n"
        f"- Title: {title}\n"
        f"- Summary: {summary}\n"
        f"- Source: {source}\n"
        f"- Source Type: manual_discord\n"
        f"- Tags: インサイト分析\n"
        f"- Message ID: {message_id}\n"
        f"- Content Hash: {content_hash}\n"
        f"- Created At: {created_at}\n"
        f"- Event Time: {updated}\n"
        f"- Updated: {updated}\n"
        f"<!-- MANUAL_ENTRY_END:{message_id} -->\n"
    )


def locate_file_and_id(root: Path, message_id: str) -> Tuple[Path, str] | Tuple[None, None]:
    for p in (root / "markets").glob("*/**/*.md"):
        if p.name not in {"ideas.md", "watchlist.md", "dev-tools.md", "other.md"}:
            continue
        text = p.read_text(encoding="utf-8")
        if f"MANUAL_ENTRY_START:{message_id}" in text:
            m = re.search(rf"MANUAL_ENTRY_START:{re.escape(message_id)}[\s\S]*?- ID:\s*([A-Z]+-\d+)", text)
            return p, (m.group(1) if m else "")
    return None, None


def update_existing_block(path: Path, message_id: str, new_block: str) -> bool:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"\n<!-- MANUAL_ENTRY_START:{re.escape(message_id)} -->[\s\S]*?<!-- MANUAL_ENTRY_END:{re.escape(message_id)} -->\n",
        re.MULTILINE,
    )
    if not pattern.search(text):
        return False
    text = pattern.sub(new_block, text)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest #インサイト分析 discord message")
    ap.add_argument("--root", default=".")
    ap.add_argument("--message-id", required=True)
    ap.add_argument("--author", default="unknown")
    ap.add_argument("--text", required=True)
    ap.add_argument("--source-url", default="")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    state_path = root / "markets/state/manual-discord-state.json"
    state = ensure_state(state_path)

    # Strict trigger: only when user explicitly asks Claw to do insight analysis
    trigger_ok = bool(re.search(r"クロウ.*インサイト分析して", args.text))
    if not trigger_ok:
        print("skip_no_explicit_request")
        return 0

    if "#インサイト分析" not in args.text:
        print("skip_no_tag")
        return 0

    body = args.text.replace("#インサイト分析", "").strip()
    if not body:
        print("skip_empty")
        return 0

    category = classify_category(body)
    market = market_from_text(body)
    content_hash = sha(body)
    source = args.source_url or f"discord://{args.message_id}"
    ts = now_jst()
    title = body.splitlines()[0][:100]

    if category == "ideas":
        file_name, prefix = "ideas.md", "IDEA"
    elif category == "watchlist":
        file_name, prefix = "watchlist.md", "WATCH"
    elif category == "dev-tools":
        file_name, prefix = "dev-tools.md", "TOOL"
    else:
        file_name, prefix = "other.md", "MISC"

    entries: Dict[str, Dict] = state.setdefault("entries", {})

    # Update path: existing message id
    existing = entries.get(args.message_id)
    if existing and existing.get("content_hash") == content_hash:
        print("already_ingested")
        return 0

    if existing:
        existing_path = Path(existing["path"])
        eid = existing.get("entry_id", "")
        created = existing.get("created_at", ts)
        block = block_for(category, eid, title, body, source, args.message_id, content_hash, created, ts)
        ok = update_existing_block(existing_path, args.message_id, block)
        if ok:
            existing.update({
                "content_hash": content_hash,
                "updated_at": ts,
                "market": market,
                "category": category,
                "source": source,
            })
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"updated {eid} -> {existing_path}")
            return 0

    # If not tracked in state, try find in files (migration)
    fpath, fid = locate_file_and_id(root, args.message_id)
    if fpath and fid:
        created = ts
        block = block_for(category, fid, title, body, source, args.message_id, content_hash, created, ts)
        if update_existing_block(fpath, args.message_id, block):
            entries[args.message_id] = {
                "entry_id": fid,
                "path": str(fpath),
                "content_hash": content_hash,
                "created_at": created,
                "updated_at": ts,
                "market": market,
                "category": category,
                "source": source,
            }
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"updated {fid} -> {fpath}")
            return 0

    # Create new
    market_dir = root / f"markets/{market}"
    market_dir.mkdir(parents=True, exist_ok=True)
    path = market_dir / file_name
    eid = next_id(path, prefix)
    block = block_for(category, eid, title, body, source, args.message_id, content_hash, ts, ts)

    with path.open("a", encoding="utf-8") as f:
        f.write(block)

    entries[args.message_id] = {
        "entry_id": eid,
        "path": str(path),
        "content_hash": content_hash,
        "created_at": ts,
        "updated_at": ts,
        "market": market,
        "category": category,
        "source": source,
    }
    if len(entries) > 5000:
        # keep latest by updated_at
        ordered = sorted(entries.items(), key=lambda kv: kv[1].get("updated_at", ""))
        entries = dict(ordered[-4000:])
        state["entries"] = entries

    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ingested {eid} market={market} category={category}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
