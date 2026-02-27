#!/usr/bin/env python3
import argparse
import datetime as dt
import email.utils
import html
import json
import re
import sys
import subprocess
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")
UTC = dt.timezone.utc


def clean_text(s: str) -> str:
    if not s:
        return ""
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_dt(value: str):
    if not value:
        return None
    value = value.strip()
    try:
        d = email.utils.parsedate_to_datetime(value)
        if d is not None:
            return d.astimezone(UTC) if d.tzinfo else d.replace(tzinfo=UTC)
    except Exception:
        pass
    v = value.replace("Z", "+00:00")
    try:
        d = dt.datetime.fromisoformat(v)
        return d.astimezone(UTC) if d.tzinfo else d.replace(tzinfo=UTC)
    except Exception:
        return None


def canonical_url(url: str) -> str:
    if not url:
        return ""
    u = url.strip()
    u = re.sub(r"#.*$", "", u)
    u = re.sub(r"\?.*$", "", u)
    return u.rstrip("/").lower()


def norm_title(t: str) -> str:
    t = clean_text(t).lower()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def text_of(elem, path):
    n = elem.find(path)
    return n.text.strip() if n is not None and n.text else ""


def parse_feed(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    tag = root.tag.lower()
    items = []

    if tag.endswith("rss") or tag.endswith("rdf"):
        channel = root.find("channel")
        if channel is None:
            channel = root
        title = text_of(channel, "title") or "(unknown)"
        for it in channel.findall("item"):
            entry = {
                "title": text_of(it, "title"),
                "url": text_of(it, "link"),
                "published": parse_dt(text_of(it, "pubDate") or text_of(it, "date")),
                "summary": clean_text(text_of(it, "description") or text_of(it, "content")),
            }
            items.append(entry)
        return title, items

    # Atom
    ns = "{http://www.w3.org/2005/Atom}"
    if root.tag.startswith(ns):
        title = text_of(root, f"{ns}title") or "(unknown)"
        for it in root.findall(f"{ns}entry"):
            link = ""
            for l in it.findall(f"{ns}link"):
                rel = l.attrib.get("rel", "alternate")
                if rel == "alternate" and l.attrib.get("href"):
                    link = l.attrib.get("href")
                    break
                if not link and l.attrib.get("href"):
                    link = l.attrib.get("href")
            entry = {
                "title": text_of(it, f"{ns}title"),
                "url": link,
                "published": parse_dt(text_of(it, f"{ns}published") or text_of(it, f"{ns}updated")),
                "summary": clean_text(text_of(it, f"{ns}summary") or text_of(it, f"{ns}content")),
            }
            items.append(entry)
        return title, items

    return "(unknown)", []


def load_sources(opml_path: Path):
    root = ET.parse(opml_path).getroot()
    sources = []
    for o in root.findall(".//outline"):
        xml_url = o.attrib.get("xmlUrl")
        if not xml_url:
            continue
        sources.append({
            "name": o.attrib.get("title") or o.attrib.get("text") or xml_url,
            "xmlUrl": xml_url,
            "htmlUrl": o.attrib.get("htmlUrl", ""),
        })
    return sources


def fetch(url: str, timeout=8):
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-RSS-Digest/1.0"})

    # First try urllib with a couple of retries for transient network timeouts.
    last_err = None
    for i in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout + i * 3) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            # Some feeds return 308 Permanent Redirect; Python's default handler can fail on this.
            if e.code != 308:
                raise
            last_err = e
            break
        except urllib.error.URLError as e:
            # TLS/protocol and timeout/network errors fallback to curl.
            last_err = e
            continue

    # Fallback: curl handles redirect/TLS edge-cases more robustly.
    cmd = [
        "curl",
        "-fsSL",
        "--retry",
        "2",
        "--retry-all-errors",
        "--connect-timeout",
        str(max(4, min(timeout, 12))),
        "--max-time",
        str(max(12, timeout * 3)),
        "--user-agent",
        "OpenClaw-RSS-Digest/1.0",
        url,
    ]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        err = p.stderr.decode("utf-8", errors="ignore").strip() or f"curl exit {p.returncode}"
        raise urllib.error.URLError(err if err else str(last_err) if last_err else "fetch failed")
    return p.stdout


def compute_window(mode: str, now_jst: dt.datetime, state: dict):
    if mode == "morning":
        yday = (now_jst - dt.timedelta(days=1)).date()
        start = dt.datetime.combine(yday, dt.time(0, 0, 0), JST)
        end = dt.datetime.combine(yday, dt.time(23, 59, 59), JST)
        return start.astimezone(UTC), end.astimezone(UTC), f"{yday} 前日分"

    # evening: from last run to now
    last = state.get("last_run_utc")
    if last:
        start = dt.datetime.fromisoformat(last).astimezone(UTC)
    else:
        today_8 = dt.datetime.combine(now_jst.date(), dt.time(8, 0, 0), JST)
        start = today_8.astimezone(UTC)
    end = now_jst.astimezone(UTC)
    return start, end, "前回実行以降の差分"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["morning", "evening"], required=True)
    p.add_argument("--opml", required=True)
    p.add_argument("--state", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-per-source", type=int, default=2)
    p.add_argument("--timeout", type=int, default=8)
    p.add_argument("--max-sources", type=int)
    p.add_argument("--now")
    args = p.parse_args()

    now_jst = dt.datetime.now(JST)
    if args.now:
        now_jst = dt.datetime.fromisoformat(args.now).astimezone(JST)

    state_path = Path(args.state)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    if state_path.exists():
        state = json.loads(state_path.read_text())
    else:
        state = {}

    start_utc, end_utc, window_label = compute_window(args.mode, now_jst, state)

    sources = load_sources(Path(args.opml))
    if args.max_sources:
        sources = sources[: args.max_sources]
    by_source = {}
    failures = []
    seen_urls = set()
    seen_titles = set()
    dup_count = 0

    for s in sources:
        name = s["name"]
        try:
            data = fetch(s["xmlUrl"], timeout=args.timeout)
            _, entries = parse_feed(data)
        except Exception as e:
            failures.append((name, str(e)))
            continue

        filtered = []
        for e in entries:
            pub = e.get("published")
            if not pub:
                continue
            if not (start_utc <= pub <= end_utc):
                continue

            cu = canonical_url(e.get("url", ""))
            nt = norm_title(e.get("title", ""))
            if cu and cu in seen_urls:
                dup_count += 1
                continue
            if nt and nt in seen_titles:
                dup_count += 1
                continue
            if cu:
                seen_urls.add(cu)
            if nt:
                seen_titles.add(nt)
            filtered.append(e)

        if filtered:
            filtered.sort(key=lambda x: x["published"], reverse=True)
            by_source[name] = filtered[: args.max_per_source]

    lines = []
    stamp = now_jst.strftime("%Y-%m-%d %H:%M")
    mode_label = "朝" if args.mode == "morning" else "夜"
    lines.append(f"【RSS更新サマリー】{mode_label} {stamp} JST")
    lines.append(f"対象: {window_label}")
    lines.append("")

    total_items = 0
    for source in sorted(by_source.keys()):
        lines.append(f"■ {source}")
        for it in by_source[source]:
            total_items += 1
            title = clean_text(it.get("title") or "(no title)")
            summary = clean_text(it.get("summary") or "")
            if summary:
                summary = summary[:120] + ("…" if len(summary) > 120 else "")
            else:
                summary = "要約なし"
            lines.append(f"・{title} — {summary}")
            lines.append(f"出典: {it.get('url') or ''}")
        lines.append("")

    if not by_source:
        lines.append("この時間帯の更新は検出されなかった。")
        lines.append("")

    lines.append(f"更新ソース数: {len(by_source)} / {len(sources)}")
    lines.append(f"採用記事数: {total_items}")
    lines.append(f"重複除外: {dup_count}")
    if failures:
        lines.append(f"取得失敗ソース: {len(failures)}")
        for name, err in failures[:10]:
            lines.append(f" - {name}: {clean_text(err)[:140]}")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")

    state["last_run_utc"] = now_jst.astimezone(UTC).isoformat()
    state["last_mode"] = args.mode
    state["last_output"] = str(out_path)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    print(str(out_path))


if __name__ == "__main__":
    main()
