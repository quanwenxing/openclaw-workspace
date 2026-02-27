#!/usr/bin/env python3
"""Fetch an URL via Jina Reader (r.jina.ai) and return LLM-friendly content.

No API key required for basic usage (rate-limited).

Examples:
  python3 jina_reader_fetch.py "https://example.com/article" --format markdown
  python3 jina_reader_fetch.py "https://example.com/article" --format json | jq .content

Notes:
- This is for *content extraction*, not web search.
- For dynamic pages, you may need --wait-for-selector.

Ref:
  https://jina.ai/reader/
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, Optional

import requests  # type: ignore


def build_reader_url(target_url: str) -> str:
    # Jina Reader works by prefixing r.jina.ai to the target URL.
    # If target_url already includes scheme, keep it.
    return f"https://r.jina.ai/{target_url}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("url", help="Target URL to read")
    p.add_argument("--format", choices=["markdown", "json"], default="json")
    p.add_argument("--soft-fail", action="store_true", help="Never raise on fetch errors; output JSON with error and exit 0")

    # Common Reader controls (best-effort; Reader interprets these headers)
    p.add_argument("--no-cache", action="store_true", help="Bypass cached content")
    p.add_argument("--cache-tolerance", type=int, default=None, help="Accept cached content if younger than N seconds")
    p.add_argument("--timeout", type=float, default=60.0)

    p.add_argument("--target-selector", default=None, help="Extract only matching CSS selector (e.g., article, #content)")
    p.add_argument("--wait-for-selector", default=None, help="Wait until selector appears (for dynamic pages)")
    p.add_argument("--exclude-selector", default=None, help="Remove matching elements before extraction")

    args = p.parse_args()

    headers: Dict[str, str] = {}

    # Response format
    if args.format == "json":
        headers["accept"] = "application/json"
    else:
        headers["accept"] = "text/markdown"

    # Cache controls (names based on Jina Reader docs UI; best-effort)
    if args.no_cache:
        headers["x-no-cache"] = "true"
    if args.cache_tolerance is not None:
        headers["x-cache-tolerance"] = str(args.cache_tolerance)

    # Selectors
    if args.target_selector:
        headers["x-target-selector"] = args.target_selector
    if args.wait_for_selector:
        headers["x-wait-for-selector"] = args.wait_for_selector
    if args.exclude_selector:
        headers["x-exclude-selector"] = args.exclude_selector

    reader_url = build_reader_url(args.url)
    r = requests.get(reader_url, headers=headers, timeout=args.timeout)

    def _soft_error(status: int, payload: Any, text: str | None = None) -> int:
        out: Dict[str, Any] = {
            "source": "jina-reader",
            "reader_url": reader_url,
            "url": args.url,
            "title": None,
            "content": None,
            "timestamp": None,
            "error": {
                "http_status": status,
                "payload": payload,
            },
        }
        if text is not None:
            out["error"]["text"] = text[:2000]
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    # Some failures return non-JSON even if accept json.
    if args.format == "json":
        try:
            data: Any = r.json()
        except Exception:
            if args.soft_fail:
                return _soft_error(r.status_code, payload=None, text=r.text)
            raise SystemExit(f"Reader returned non-JSON (status {r.status_code}):\n{r.text[:2000]}")

        if r.status_code >= 400:
            if args.soft_fail:
                return _soft_error(r.status_code, payload=data)
            raise SystemExit(f"Reader error ({r.status_code}): {json.dumps(data, ensure_ascii=False)[:2000]}")

        # Normalize to stable shape
        payload: Dict[str, Any]
        if isinstance(data, dict) and isinstance(data.get("data"), dict):
            payload = data["data"]
        elif isinstance(data, dict):
            payload = data
        else:
            payload = {}

        out: Dict[str, Any] = {
            "source": "jina-reader",
            "reader_url": reader_url,
            "url": payload.get("url") or args.url,
            "title": payload.get("title"),
            "content": payload.get("content"),
            "timestamp": payload.get("timestamp"),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    # markdown
    if r.status_code >= 400:
        raise SystemExit(f"Reader error ({r.status_code}):\n{r.text[:2000]}")
    sys.stdout.write(r.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
