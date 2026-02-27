#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

JST = timezone(timedelta(hours=9))

CATEGORY_PRIORITY = {"watchlist": 4, "dev-tools": 3, "ideas": 2, "other": 1}
DEV_KEYWORDS = {"api", "sdk", "bot", "websocket", "executor", "pipeline", "automation", "agent", "script"}
IDEA_KEYWORDS = {"edge", "mispricing", "arb", "entry", "exit", "odds", "probability", "liquidity", "spread"}
WATCH_PATTERNS = [re.compile(r"0x[a-fA-F0-9]{8,}"), re.compile(r"\.[a-z]{2,10}\b", re.IGNORECASE)]
NOISE_PATTERNS = [
    re.compile(r"\bgiveaway\b", re.IGNORECASE),
    re.compile(r"\bref(erral)?\b", re.IGNORECASE),
    re.compile(r"promo code|coupon|airdrop", re.IGNORECASE),
]
MARKET_KEYWORDS = {
    "polymarket": ["polymarket"],
    "kalshi": ["kalshi"],
    "opinion": ["opinion", "opinionlabs"],
}


@dataclass
class Entry:
    market: str
    category: str
    entry_id: str
    title: str
    summary: str
    source: str
    source_type: str
    tags: List[str]
    created_at: str
    event_time: str
    updated: str
    importance: str = "medium"
    watch_target: str = ""
    why_track: str = ""


def now_jst_str() -> str:
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_text(text: str) -> str:
    t = re.sub(r"https?://\S+", "", text)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def text_hash(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()[:16]


def detect_market(post: Dict[str, Any]) -> str:
    text = (post.get("text") or "").lower()
    source_market = post.get("market")
    mentioned = []
    for m, kws in MARKET_KEYWORDS.items():
        if any(k in text for k in kws):
            mentioned.append(m)
    if len(set(mentioned)) >= 2:
        return "multi-market"
    if source_market in {"polymarket", "kalshi", "opinion"}:
        return source_market
    if len(mentioned) == 1:
        return mentioned[0]
    return "other-market"


def rule_based_category(text: str, base_category: str) -> str:
    lo = text.lower()
    if any(p.search(text) for p in WATCH_PATTERNS):
        return "watchlist"
    if any(k in lo for k in DEV_KEYWORDS):
        return "dev-tools"
    if any(k in lo for k in IDEA_KEYWORDS):
        return "ideas"
    return base_category


def is_noise(text: str) -> Tuple[bool, bool]:
    lo = text.lower()
    for p in NOISE_PATTERNS:
        if p.search(lo):
            return True, False
    low_priority = False
    if len(lo.split()) < 6:
        low_priority = True
    if "rt @" in lo:
        low_priority = True
    return False, low_priority


def heuristic_analyze(post: Dict[str, Any]) -> Dict[str, Any]:
    text = post.get("text", "")
    lo = text.lower()
    category = "other"
    if any(k in lo for k in DEV_KEYWORDS):
        category = "dev-tools"
    if any(k in lo for k in IDEA_KEYWORDS):
        category = "ideas"
    if any(p.search(text) for p in WATCH_PATTERNS):
        category = "watchlist"

    tags = []
    for m, kws in MARKET_KEYWORDS.items():
        if any(k in lo for k in kws):
            tags.append(m)
    for k in ["bot", "api", "alpha", "arb", "liquidity", "odds", "market maker"]:
        if k in lo:
            tags.append(k.replace(" ", "-"))

    importance = "medium"
    if any(k in lo for k in ["alpha", "arb", "mispricing", "edge"]):
        importance = "high"
    if len(text) < 40:
        importance = "low"

    summary = text.strip().replace("\n", " ")
    if len(summary) > 200:
        summary = summary[:200] + "..."

    return {
        "summary_ja": summary,
        "category": category,
        "tags": sorted(set(tags)),
        "importance": importance,
        "watch_targets": [],
        "confidence": 0.6,
    }


def grok_analyze(post: Dict[str, Any], api_key: str, model: str) -> Optional[Dict[str, Any]]:
    prompt = {
        "role": "user",
        "content": (
            "次のX投稿を日本語で要約し、JSONのみで返してください。"
            "keys: summary_ja, category(ideas|watchlist|dev-tools|other), tags(array), importance(high|medium|low), watch_targets(array).\n"
            f"text: {post.get('text','')}\n"
            f"author: @{post.get('author_handle','')}\n"
            f"url: {post.get('url','')}"
        ),
    }
    payload = {"model": model, "messages": [prompt], "temperature": 0.1}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        r = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload, timeout=40)
        if r.status_code >= 300:
            return None
        data = r.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        m = re.search(r"\{[\s\S]*\}", content)
        if not m:
            return None
        obj = json.loads(m.group(0))
        if obj.get("category") not in {"ideas", "watchlist", "dev-tools", "other"}:
            return None
        return obj
    except Exception:
        return None


def next_id(path: Path, prefix: str) -> str:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    nums = [int(n) for n in re.findall(rf"{re.escape(prefix)}-(\d+)", text)]
    n = (max(nums) + 1) if nums else 1
    return f"{prefix}-{n:04d}"


def append_entry_file(path: Path, entry: Entry) -> None:
    block = (
        f"\n- ID: {entry.entry_id}\n"
        f"- Title: {entry.title}\n"
        f"- Summary: {entry.summary}\n"
        f"- Source: {entry.source}\n"
        f"- Source Type: {entry.source_type}\n"
        f"- Tags: {', '.join(entry.tags)}\n"
        f"- Created At: {entry.created_at}\n"
        f"- Event Time: {entry.event_time}\n"
        f"- Updated: {entry.updated}\n"
    )
    if entry.category == "watchlist":
        block = (
            f"\n- ID: {entry.entry_id}\n"
            f"- Name/Address: {entry.watch_target or entry.title}\n"
            f"- Type: person\n"
            f"- Chain/Platform: x\n"
            f"- Why Track: {entry.why_track or entry.summary}\n"
            f"- Signals: {entry.summary}\n"
            f"- Source: {entry.source}\n"
            f"- Source Type: {entry.source_type}\n"
            f"- Tags: {', '.join(entry.tags)}\n"
            f"- First Seen At: {entry.created_at}\n"
            f"- Event Time: {entry.event_time}\n"
            f"- Updated: {entry.updated}\n"
        )
    elif entry.category == "dev-tools":
        block = (
            f"\n- ID: {entry.entry_id}\n"
            f"- Tool/Method: {entry.title}\n"
            f"- Category: monitoring\n"
            f"- Use Case: {entry.summary}\n"
            f"- Setup Notes: Auto-collected from X\n"
            f"- Source: {entry.source}\n"
            f"- Source Type: {entry.source_type}\n"
            f"- Tags: {', '.join(entry.tags)}\n"
            f"- Created At: {entry.created_at}\n"
            f"- Event Time: {entry.event_time}\n"
            f"- Updated: {entry.updated}\n"
        )
    p = path
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(f"# {entry.category}\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write(block)


def insert_index_row(index_path: Path, section: str, row: str) -> None:
    text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    marker = f"## {section}"
    if marker not in text:
        return
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == marker)
    insert_at = start + 1
    # skip header rows
    while insert_at < len(lines) and lines[insert_at].startswith("|"):
        insert_at += 1
    lines.insert(insert_at, row)
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ensure_market_dir(root: Path, market: str) -> Path:
    mdir = root / f"markets/{market}"
    mdir.mkdir(parents=True, exist_ok=True)
    return mdir


def add_strategy_candidates(root: Path, entries: List[Entry]) -> List[Dict[str, Any]]:
    out = []
    cand_path = root / "markets/strategy-candidates/candidates.md"
    idx_path = root / "markets/strategy-candidates/index.md"
    now = now_jst_str()

    cand_text = cand_path.read_text(encoding="utf-8") if cand_path.exists() else ""
    nums = [int(n) for n in re.findall(r"STRAT-(\d+)", cand_text)]
    next_num = (max(nums) + 1) if nums else 1

    # select high-signal ideas/dev-tools
    picked = [e for e in entries if e.category in {"ideas", "dev-tools"} and e.importance in {"high", "medium"}][:3]
    for e in picked:
        sid = f"STRAT-{next_num:04d}"
        next_num += 1
        title = f"{e.market}: {e.title[:60]}"
        block = (
            f"\n- ID: {sid}\n"
            f"- Title: {title}\n"
            f"- Market: {e.market}\n"
            f"- Type: event-driven\n"
            f"- Hypothesis: {e.summary}\n"
            f"- Entry Signal: Related post signal appears with momentum shift\n"
            f"- Exit Signal: Odds normalize or catalyst invalidated\n"
            f"- Risk: False signal / low liquidity / slippage\n"
            f"- Required Data/Tools: X feed, market odds feed\n"
            f"- Source Links: {e.source}\n"
            f"- Derived From IDs: {e.entry_id}\n"
            f"- Priority: {e.importance}\n"
            f"- Status: new\n"
            f"- Created At: {now}\n"
            f"- Updated: {now}\n"
        )
        with cand_path.open("a", encoding="utf-8") as f:
            f.write(block)

        row = f"| {sid} | {title} | {e.market} | event-driven | {e.importance} | new | {e.entry_id} | {now} |"
        with idx_path.open("a", encoding="utf-8") as f:
            f.write(row + "\n")
        out.append({"id": sid, "title": title, "derived_from": e.entry_id})
    return out


def build_summary(run: Dict[str, Any], entries: List[Entry], strat_new: List[Dict[str, Any]]) -> str:
    today = datetime.now(JST).strftime("%Y-%m-%d")
    n_manual = len([e for e in entries if e.source_type == "manual_discord"])
    n_auto = len([e for e in entries if e.source_type == "auto_x_grok"])
    by_market: Dict[str, int] = {}
    by_cat: Dict[str, int] = {}
    for e in entries:
        by_market[e.market] = by_market.get(e.market, 0) + 1
        by_cat[e.category] = by_cat.get(e.category, 0) + 1

    top = [e for e in entries if e.importance == "high"][:3]
    if not top:
        top = entries[:3]

    top1 = top[0] if top else None

    lines = [
        f"[Daily Market Intel] {today} (JST 18:00実行)",
        f"Summary-1: 取得投稿 {run.get('stats',{}).get('total_posts',0)}件 / 新規登録 {len(entries)}件",
        f"Summary-2: ソース内訳 manual_discord={n_manual} / auto_x_grok={n_auto}",
        f"Summary-3: 重要TOP1 {f'[{top1.category}] {top1.title}' if top1 else 'なし'}",
        "",
        f"取得投稿数: {run.get('stats',{}).get('total_posts',0)}",
        f"新規登録: {len(entries)}（manual_discord: {n_manual} / auto_x_grok: {n_auto}）",
        f"重複除外: {run.get('dedupe',{}).get('duplicates',0)}",
        f"失敗件数: {run.get('stats',{}).get('account_failed',0)}",
        "",
        "市場別追加件数:",
        f"- polymarket: {by_market.get('polymarket',0)}",
        f"- kalshi: {by_market.get('kalshi',0)}",
        f"- opinion: {by_market.get('opinion',0)}",
        f"- multi-market: {by_market.get('multi-market',0)}",
        f"- other-market: {by_market.get('other-market',0)}",
        "",
        "カテゴリ別追加件数:",
        f"- ideas: {by_cat.get('ideas',0)}",
        f"- watchlist: {by_cat.get('watchlist',0)}",
        f"- dev-tools: {by_cat.get('dev-tools',0)}",
        f"- other: {by_cat.get('other',0)}",
        "",
        "重要トピック TOP3:",
    ]
    for i, e in enumerate(top, 1):
        lines.append(f"{i}) [{e.category}] {e.title} / {e.source}")

    lines += ["", "戦略候補（strategy-candidates）:"]
    if strat_new:
        for s in strat_new[:3]:
            lines.append(f"- {s['id']} {s['title']}（根拠ID: {s['derived_from']}）")
    else:
        lines.append("- なし")

    return "\n".join(lines)


def process(root: Path, run_date: str, dry_run: bool = False) -> Dict[str, Any]:
    run_path = root / f"markets/runs/{run_date}.json"
    run = read_json(run_path, {})
    if not run:
        raise SystemExit(f"run file not found: {run_path}")

    dedupe_path = root / "markets/state/processed-posts.json"
    dedupe = read_json(dedupe_path, {"seen": {}})
    seen: Dict[str, Any] = dedupe.setdefault("seen", {})

    grok_key = os.getenv("GROK_API_KEY", "")
    grok_model = os.getenv("GROK_MODEL", "grok-3-mini")

    now = now_jst_str()
    new_entries: List[Entry] = []
    duplicates = 0
    excluded_noise = 0

    for _, acct in run.get("accounts", {}).items():
        for post in acct.get("posts", []):
            pid = str(post.get("post_id"))
            source = post.get("url") or ""
            h = text_hash(post.get("text", ""))
            dedupe_key = pid or source or h
            if dedupe_key in seen:
                duplicates += 1
                continue

            noise, low_priority = is_noise(post.get("text", ""))
            if noise:
                excluded_noise += 1
                seen[dedupe_key] = {"skipped": "noise", "at": now}
                continue

            analysis = None
            if grok_key:
                analysis = grok_analyze(post, grok_key, grok_model)
            if not analysis:
                analysis = heuristic_analyze(post)

            category = analysis.get("category", "other")
            category = rule_based_category(post.get("text", ""), category)
            if category not in {"ideas", "watchlist", "dev-tools", "other"}:
                category = "other"

            market = detect_market(post)
            title = normalize_text(post.get("text", ""))[:72]
            if not title:
                title = f"post-{pid}"

            mdir = ensure_market_dir(root, market)
            if category == "ideas":
                prefix, file_name, section = "IDEA", "ideas.md", "Ideas"
            elif category == "watchlist":
                prefix, file_name, section = "WATCH", "watchlist.md", "Watchlist"
            elif category == "dev-tools":
                prefix, file_name, section = "TOOL", "dev-tools.md", "Dev Tools / Methods"
            else:
                prefix, file_name, section = "MISC", "other.md", "Other"

            entry_id = next_id(mdir / file_name, prefix)
            tags = analysis.get("tags", []) or []
            if low_priority:
                tags.append("low-priority")
            tags = sorted(set(tags))

            entry = Entry(
                market=market,
                category=category,
                entry_id=entry_id,
                title=title,
                summary=analysis.get("summary_ja", ""),
                source=source,
                source_type="auto_x_grok",
                tags=tags,
                created_at=now,
                event_time=post.get("created_at") or now,
                updated=now,
                importance=analysis.get("importance", "medium"),
                why_track=analysis.get("summary_ja", ""),
            )

            if not dry_run:
                append_entry_file(mdir / file_name, entry)
                idx = mdir / "index.md"
                if idx.exists():
                    if category == "watchlist":
                        row = f"| {entry.entry_id} | {entry.title} | person | {entry.summary[:40]} | {entry.source} | {entry.created_at} | {entry.updated} |"
                    elif category == "dev-tools":
                        row = f"| {entry.entry_id} | {entry.title} | monitoring | auto-collected | {entry.source} | {entry.created_at} | {entry.updated} |"
                    elif category == "ideas":
                        row = f"| {entry.entry_id} | {entry.title} | {', '.join(entry.tags)} | {entry.source} | {entry.created_at} | {entry.updated} |"
                    else:
                        row = f"| {entry.entry_id} | {entry.title} | x-post | auto-collected | {entry.source} | {entry.created_at} | {entry.updated} |"
                    insert_index_row(idx, section, row)

            seen[dedupe_key] = {
                "post_id": pid,
                "source": source,
                "hash": h,
                "entry_id": entry_id,
                "market": market,
                "category": category,
                "at": now,
            }
            new_entries.append(entry)

    run.setdefault("dedupe", {})
    run["dedupe"]["duplicates"] = duplicates
    run["dedupe"]["excluded_noise"] = excluded_noise

    # Keep seen map bounded
    if len(seen) > 10000:
        keys = sorted(seen.keys(), key=lambda k: seen[k].get("at", ""))
        for k in keys[:-8000]:
            seen.pop(k, None)

    if not dry_run:
        save_json(run_path, run)
        save_json(dedupe_path, dedupe)

    strat_new = []
    if not dry_run:
        strat_new = add_strategy_candidates(root, new_entries)

    summary = build_summary(run, new_entries, strat_new)
    summary_path = root / f"markets/runs/{run_date}-summary.txt"
    if not dry_run:
        summary_path.write_text(summary + "\n", encoding="utf-8")

    return {
        "new_entries": len(new_entries),
        "duplicates": duplicates,
        "excluded_noise": excluded_noise,
        "strategy_new": len(strat_new),
        "summary_path": str(summary_path),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Process collected run into ledgers + summary")
    ap.add_argument("--root", default=".")
    ap.add_argument("--date", default=datetime.now(JST).strftime("%Y-%m-%d"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    result = process(Path(args.root).resolve(), args.date, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
