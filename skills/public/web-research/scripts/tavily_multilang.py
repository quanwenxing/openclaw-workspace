#!/usr/bin/env python3
"""Run Tavily search across multiple languages and merge results.

Design goal:
- One command that performs 4 searches (JA/EN/ZH/KO) and merges by URL.
- Does NOT attempt machine translation (no external deps/services).
  Instead, accept per-language query overrides.

Usage:
  python3 tavily_multilang.py "<seed query>" --max-results 8

Better (recommended):
  python3 tavily_multilang.py --ja "..." --en "..." --zh "..." --ko "..." --max-results 8

Env:
  TAVILY_API_KEY

Output:
  JSON to stdout:
    {
      source: "tavily",
      queries: {ja,en,zh,ko},
      results: [ {url,title,content,score,published_date,languages:[...]} ... ]
    }
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

from _env import require_env

try:
    import requests  # type: ignore
except Exception:
    print("ERROR: requests is required. Try: python3 -m pip install requests", file=sys.stderr)
    raise

API_URL = "https://api.tavily.com/search"
LANGS = ["ja", "en", "zh", "ko"]


def _env(key: str) -> str:
    # Back-compat wrapper
    return require_env(key)


def _call_tavily(api_key: str, query: str, *, max_results: int, search_depth: str,
                include_domains: Optional[List[str]], exclude_domains: Optional[List[str]],
                timeout: float) -> Dict[str, Any]:
    payload: dict[str, Any] = {
        "api_key": api_key,
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        # A運用：検索結果のみ
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
    }
    if include_domains:
        payload["include_domains"] = include_domains
    if exclude_domains:
        payload["exclude_domains"] = exclude_domains

    r = requests.post(API_URL, json=payload, timeout=timeout)
    data = r.json()
    if r.status_code >= 400:
        msg = data.get("message") if isinstance(data, dict) else None
        raise RuntimeError(f"Tavily API error ({r.status_code}): {msg or 'see response'}")
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected Tavily response")
    return data


def main() -> int:
    p = argparse.ArgumentParser()

    # Either provide a seed query (positional) OR per-language overrides.
    p.add_argument("seed", nargs="?", help="Seed query (used for any language query not explicitly provided)")
    p.add_argument("--ja", dest="q_ja", help="Japanese query")
    p.add_argument("--en", dest="q_en", help="English query")
    p.add_argument("--zh", dest="q_zh", help="Chinese query")
    p.add_argument("--ko", dest="q_ko", help="Korean query")

    p.add_argument("--max-results", type=int, default=8)
    p.add_argument("--search-depth", choices=["basic", "advanced"], default="basic")
    p.add_argument("--include-domains", nargs="*", default=None)
    p.add_argument("--exclude-domains", nargs="*", default=None)
    p.add_argument("--timeout", type=float, default=30.0)
    p.add_argument("--workers", type=int, default=4)

    args = p.parse_args()

    if not (args.seed or args.q_ja or args.q_en or args.q_zh or args.q_ko):
        p.error("Provide a seed query or at least one of --ja/--en/--zh/--ko")

    seed = args.seed
    queries = {
        "ja": args.q_ja or seed,
        "en": args.q_en or seed,
        "zh": args.q_zh or seed,
        "ko": args.q_ko or seed,
    }

    # Drop None queries (shouldn't happen if seed set), but keep output shape.
    for k in list(queries.keys()):
        if queries[k] is None:
            queries[k] = ""

    api_key = _env("TAVILY_API_KEY")

    per_lang_results: Dict[str, List[Dict[str, Any]]] = {l: [] for l in LANGS}

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {}
        for lang in LANGS:
            q = queries[lang]
            if not q:
                continue
            futs[ex.submit(
                _call_tavily,
                api_key,
                q,
                max_results=args.max_results,
                search_depth=args.search_depth,
                include_domains=args.include_domains,
                exclude_domains=args.exclude_domains,
                timeout=args.timeout,
            )] = lang

        for fut in as_completed(futs):
            lang = futs[fut]
            data = fut.result()
            results = data.get("results")
            if isinstance(results, list):
                for item in results:
                    if isinstance(item, dict):
                        per_lang_results[lang].append(item)

    # Merge by URL
    merged: Dict[str, Dict[str, Any]] = {}
    for lang, items in per_lang_results.items():
        for item in items:
            url = item.get("url")
            if not isinstance(url, str) or not url:
                continue
            cur = merged.get(url)
            if not cur:
                merged[url] = {
                    "url": url,
                    "title": item.get("title"),
                    "content": item.get("content"),
                    "score": item.get("score"),
                    "published_date": item.get("published_date"),
                    "languages": [lang],
                }
            else:
                if lang not in cur["languages"]:
                    cur["languages"].append(lang)
                # Prefer keeping a title/content if missing
                if not cur.get("title") and item.get("title"):
                    cur["title"] = item.get("title")
                if not cur.get("content") and item.get("content"):
                    cur["content"] = item.get("content")
                # Prefer higher score if numeric
                try:
                    s_new = float(item.get("score")) if item.get("score") is not None else None
                    s_old = float(cur.get("score")) if cur.get("score") is not None else None
                    if s_new is not None and (s_old is None or s_new > s_old):
                        cur["score"] = item.get("score")
                except Exception:
                    pass

    # Sort by score desc when possible
    def sort_key(x: Dict[str, Any]):
        try:
            s = x.get("score")
            return float(s) if s is not None else -1.0
        except Exception:
            return -1.0

    merged_list = sorted(merged.values(), key=sort_key, reverse=True)

    out = {
        "source": "tavily",
        "mode": "multilang",
        "queries": queries,
        "note": "This script does not translate. Provide per-language queries for best coverage.",
        "results": merged_list,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
