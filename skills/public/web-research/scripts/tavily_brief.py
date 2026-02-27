#!/usr/bin/env python3
"""Create a research-friendly brief from Tavily results.

Policy:
- Base layer is Tavily multilang results (title/url/snippet).
- Optionally enrich each URL via Jina Reader.
- If Jina fails (e.g., 451 blocked), fall back to Tavily snippet only.

Input:
- A Tavily multilang JSON file (output of tavily_multilang.py)

Output:
- JSON to stdout with a compact list of items ready for LLM summarization.

Usage:
  python3 tavily_brief.py /tmp/crypto_tavily.json --top 15

Enrich (best-effort):
  python3 tavily_brief.py /tmp/crypto_tavily.json --top 15 --enrich

Notes:
- This does NOT do any LLM summarization; it just prepares sources.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any, Dict, List


def _load(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _run_jina(url: str, *, timeout: float) -> Dict[str, Any]:
    # Use sibling script
    cmd = [
        sys.executable,
        "skills/public/web-research/scripts/jina_reader_fetch.py",
        url,
        "--format",
        "json",
        "--soft-fail",
        "--timeout",
        str(timeout),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    # soft-fail guarantees JSON on stdout.
    try:
        return json.loads(p.stdout)
    except Exception:
        return {
            "source": "jina-reader",
            "url": url,
            "error": {"http_status": None, "payload": None, "text": (p.stdout + "\n" + p.stderr)[:2000]},
            "title": None,
            "content": None,
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Path to tavily_multilang JSON")
    ap.add_argument("--top", type=int, default=12, help="How many URLs to include")
    ap.add_argument("--enrich", action="store_true", help="Try to enrich using Jina Reader; fallback to snippet on failure")
    ap.add_argument("--jina-timeout", type=float, default=45.0)
    args = ap.parse_args()

    tav = _load(args.input)
    results = tav.get("results")
    if not isinstance(results, list):
        raise SystemExit("Invalid input: missing results[]")

    items: List[Dict[str, Any]] = []
    for r in results:
        if not isinstance(r, dict):
            continue
        if len(items) >= args.top:
            break
        url = r.get("url")
        if not isinstance(url, str) or not url:
            continue
        item: Dict[str, Any] = {
            "url": url,
            "title": r.get("title"),
            "snippet": r.get("content"),
            "score": r.get("score"),
            "published_date": r.get("published_date"),
            "languages": r.get("languages"),
            "content": None,
            "content_source": "tavily-snippet",
            "errors": [],
        }

        if args.enrich:
            jr = _run_jina(url, timeout=args.jina_timeout)
            if jr.get("content"):
                item["content"] = jr.get("content")
                item["content_source"] = "jina-reader"
            else:
                # keep snippet only
                if jr.get("error"):
                    item["errors"].append({"jina_reader": jr.get("error")})

        items.append(item)

    out = {
        "source": "tavily",
        "queries": tav.get("queries"),
        "generated_from": args.input,
        "enriched": bool(args.enrich),
        "items": items,
    }
    try:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    except BrokenPipeError:
        # e.g., when piped to `head`
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
