#!/usr/bin/env python3
"""Minimal Tavily search client.

Goal: fetch search results (URLs/snippets) for later synthesis.

Usage:
  python3 tavily_search.py "query" --max-results 8

Reads:
  TAVILY_API_KEY from environment

Outputs:
  JSON to stdout
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from _env import require_env

try:
    import requests  # type: ignore
except Exception as e:
    print("ERROR: requests is required. Try: python3 -m pip install requests", file=sys.stderr)
    raise


API_URL = "https://api.tavily.com/search"


def _env(key: str) -> str:
    # Back-compat wrapper
    return require_env(key)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("query", help="Search query")
    p.add_argument("--max-results", type=int, default=8)
    p.add_argument("--search-depth", choices=["basic", "advanced"], default="basic")
    p.add_argument("--include-domains", nargs="*", default=None)
    p.add_argument("--exclude-domains", nargs="*", default=None)
    p.add_argument("--timeout", type=float, default=30.0)
    args = p.parse_args()

    api_key = _env("TAVILY_API_KEY")

    payload: dict[str, Any] = {
        "api_key": api_key,
        "query": args.query,
        "max_results": args.max_results,
        "search_depth": args.search_depth,
        # A運用：検索結果のみ
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
    }
    if args.include_domains:
        payload["include_domains"] = args.include_domains
    if args.exclude_domains:
        payload["exclude_domains"] = args.exclude_domains

    r = requests.post(API_URL, json=payload, timeout=args.timeout)
    try:
        data = r.json()
    except Exception:
        print(r.text, file=sys.stderr)
        raise

    if r.status_code >= 400:
        # Avoid printing api_key; Tavily errors shouldn't contain it, but keep it safe.
        msg = data.get("message") if isinstance(data, dict) else None
        raise SystemExit(f"Tavily API error ({r.status_code}): {msg or 'see output'}")

    # Normalize to a compact shape for downstream use.
    out = {
        "query": args.query,
        "source": "tavily",
        "results": [],
    }

    results = data.get("results") if isinstance(data, dict) else None
    if isinstance(results, list):
        for item in results:
            if not isinstance(item, dict):
                continue
            out["results"].append(
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content"),
                    "score": item.get("score"),
                    "published_date": item.get("published_date"),
                }
            )

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
