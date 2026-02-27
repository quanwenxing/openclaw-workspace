#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

JST = timezone(timedelta(hours=9))


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def to_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=JST)


def safe_rate(n: float, d: float) -> float:
    return 0.0 if d == 0 else round(n / d, 4)


def load_daily_stats(root: Path, date_str: str) -> Dict[str, Any]:
    run = read_json(root / f"markets/runs/{date_str}.json", {})
    summary_path = root / f"markets/runs/{date_str}-summary.txt"
    summary_exists = summary_path.exists()

    total_posts = int(run.get("stats", {}).get("total_posts", 0))
    account_failed = int(run.get("stats", {}).get("account_failed", 0))
    account_success = int(run.get("stats", {}).get("account_success", 0))
    duplicates = int(run.get("dedupe", {}).get("duplicates", 0))
    excluded_noise = int(run.get("dedupe", {}).get("excluded_noise", 0))

    accounts = run.get("accounts", {})
    processed = sum(int((a or {}).get("count", 0)) for a in accounts.values())
    # new entries estimated from summary text first match
    new_entries = 0
    if summary_exists:
        txt = summary_path.read_text(encoding="utf-8")
        import re
        m = re.search(r"新規登録:\s*(\d+)", txt)
        if m:
            new_entries = int(m.group(1))

    return {
        "date": date_str,
        "total_posts": total_posts,
        "processed_posts": processed,
        "new_entries": new_entries,
        "duplicates": duplicates,
        "excluded_noise": excluded_noise,
        "account_success": account_success,
        "account_failed": account_failed,
    }


def compute_kpi(day: Dict[str, Any]) -> Dict[str, float]:
    # proxy metrics (operational until manual labeling added)
    new_entries = day.get("new_entries", 0)
    duplicates = day.get("duplicates", 0)
    excluded_noise = day.get("excluded_noise", 0)
    total_posts = day.get("total_posts", 0)

    precision_top3 = 1.0 if new_entries > 0 else 0.0
    noise_rate = safe_rate(excluded_noise, max(total_posts, 1))
    duplicate_escape_rate = safe_rate(duplicates, max(total_posts + duplicates, 1))
    strategy_conversion_rate = 0.0  # to be updated with state transitions
    coverage = safe_rate(day.get("account_success", 0), max(day.get("account_success", 0) + day.get("account_failed", 0), 1))

    return {
        "precision_top3": precision_top3,
        "noise_rate": noise_rate,
        "duplicate_escape_rate": duplicate_escape_rate,
        "strategy_conversion_rate": strategy_conversion_rate,
        "coverage": coverage,
    }


def build_weekly_report(root: Path, end_date: str, history: List[Dict[str, Any]]) -> str:
    end = to_date(end_date)
    start = end - timedelta(days=6)
    week = [h for h in history if start.date() <= to_date(h["date"]).date() <= end.date()]

    def avg(key: str) -> float:
        vals = [float((w.get("kpi", {}) or {}).get(key, 0.0)) for w in week]
        return round(sum(vals) / len(vals), 4) if vals else 0.0

    total_new = sum(int((w.get("daily") or {}).get("new_entries", 0)) for w in week)
    total_posts = sum(int((w.get("daily") or {}).get("total_posts", 0)) for w in week)
    total_dup = sum(int((w.get("daily") or {}).get("duplicates", 0)) for w in week)

    lines = [
        f"# KPI Weekly Review Draft ({start.strftime('%Y-%m-%d')} - {end.strftime('%Y-%m-%d')})",
        "",
        f"- 対象日数: {len(week)}",
        f"- 総取得投稿: {total_posts}",
        f"- 総新規登録: {total_new}",
        f"- 総重複: {total_dup}",
        "",
        "## KPI平均",
        f"- Precision@Top3: {avg('precision_top3')}",
        f"- Noise Rate: {avg('noise_rate')}",
        f"- Duplicate Escape Rate: {avg('duplicate_escape_rate')}",
        f"- Strategy Conversion Rate: {avg('strategy_conversion_rate')}",
        f"- Coverage: {avg('coverage')}",
        "",
        "## 週間所感（下書き）",
        "- 良かった点: Coverageと自動実行安定性",
        "- 要改善: Precision@Top3 / Strategy conversion の手動評価導入",
        "- 次週アクション: 閾値見直し、ノイズ除去ルールの微調整",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Update KPI metrics and weekly review draft")
    ap.add_argument("--root", default=".")
    ap.add_argument("--date", default=datetime.now(JST).strftime("%Y-%m-%d"))
    args = ap.parse_args()

    root = Path(args.root).resolve()
    date_str = args.date

    daily = load_daily_stats(root, date_str)
    kpi = compute_kpi(daily)

    kpi_store_path = root / "markets/state/kpi-history.json"
    store = read_json(kpi_store_path, {"history": []})
    history = store.setdefault("history", [])

    # upsert date
    history = [h for h in history if h.get("date") != date_str]
    history.append({"date": date_str, "daily": daily, "kpi": kpi, "updated_at": datetime.now(JST).isoformat()})
    history = sorted(history, key=lambda x: x.get("date", ""))[-120:]
    store["history"] = history
    write_json(kpi_store_path, store)

    # weekly draft (always refresh)
    weekly_text = build_weekly_report(root, date_str, history)
    weekly_path = root / "markets/reviews/weekly-latest.md"
    weekly_path.parent.mkdir(parents=True, exist_ok=True)
    weekly_path.write_text(weekly_text, encoding="utf-8")

    print(json.dumps({
        "date": date_str,
        "daily": daily,
        "kpi": kpi,
        "kpi_store": str(kpi_store_path),
        "weekly_draft": str(weekly_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
