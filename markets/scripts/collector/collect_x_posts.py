#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import yaml

JST = timezone(timedelta(hours=9))
UTC = timezone.utc


@dataclass
class AccountCfg:
    handle: str
    market: str
    source: str = "static"


class CollectorError(Exception):
    pass


def now_jst() -> datetime:
    return datetime.now(JST)


def setup_logger(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("x_collector")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise CollectorError(f"config not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )


def load_state(path: Path, accounts: List[AccountCfg]) -> Dict[str, Any]:
    if path.exists():
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    else:
        state = {}

    state.setdefault("last_run_at", None)
    state.setdefault("last_success", False)
    state.setdefault("accounts", {})
    for a in accounts:
        state["accounts"].setdefault(a.handle, {"since_id": "0"})
    return state


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    *,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None,
    retries: int = 3,
    backoff_base: float = 1.5,
    timeout: int = 20,
) -> requests.Response:
    last_err: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            r = session.request(method, url, headers=headers, params=params, timeout=timeout)
            if 200 <= r.status_code < 300:
                return r
            if r.status_code in (429, 500, 502, 503, 504):
                raise CollectorError(f"retryable status={r.status_code} body={r.text[:300]}")
            raise CollectorError(f"status={r.status_code} body={r.text[:500]}")
        except Exception as e:
            last_err = e
            if attempt >= retries:
                break
            sleep_s = backoff_base ** attempt
            time.sleep(sleep_s)
    raise CollectorError(str(last_err) if last_err else "request failed")


def get_user_id(session: requests.Session, headers: Dict[str, str], handle: str) -> str:
    url = f"https://api.x.com/2/users/by/username/{handle}"
    r = request_with_retry(session, "GET", url, headers=headers)
    data = r.json()
    uid = data.get("data", {}).get("id")
    if not uid:
        raise CollectorError(f"user id not found for @{handle}: {data}")
    return uid


def collect_user_posts(
    session: requests.Session,
    headers: Dict[str, str],
    user_id: str,
    since_id: str,
    lookback_hours: int,
    max_results: int = 100,
) -> List[Dict[str, Any]]:
    url = f"https://api.x.com/2/users/{user_id}/tweets"
    start_time = (datetime.now(UTC) - timedelta(hours=lookback_hours)).isoformat(timespec="seconds").replace("+00:00", "Z")
    params = {
        "max_results": str(max_results),
        "tweet.fields": "created_at,entities,public_metrics,referenced_tweets,lang",
        "exclude": "replies,retweets",
        "start_time": start_time,
    }
    if since_id and since_id != "0":
        params["since_id"] = since_id

    all_posts: List[Dict[str, Any]] = []
    next_token: Optional[str] = None

    while True:
        q = dict(params)
        if next_token:
            q["pagination_token"] = next_token
        r = request_with_retry(session, "GET", url, headers=headers, params=q)
        payload = r.json()
        all_posts.extend(payload.get("data", []))
        meta = payload.get("meta", {})
        next_token = meta.get("next_token")
        if not next_token:
            break

    return all_posts


def collect_list_members(
    session: requests.Session,
    headers: Dict[str, str],
    list_id: str,
) -> List[str]:
    url = f"https://api.x.com/2/lists/{list_id}/members"
    params = {"max_results": "100", "user.fields": "username"}
    members: List[str] = []
    next_token: Optional[str] = None

    while True:
        q = dict(params)
        if next_token:
            q["pagination_token"] = next_token
        r = request_with_retry(session, "GET", url, headers=headers, params=q)
        payload = r.json()
        for u in payload.get("data", []):
            un = u.get("username")
            if un:
                members.append(un)
        next_token = payload.get("meta", {}).get("next_token")
        if not next_token:
            break

    # unique preserve order
    seen = set()
    out: List[str] = []
    for m in members:
        if m.lower() in seen:
            continue
        seen.add(m.lower())
        out.append(m)
    return out


def canonical_url(handle: str, post_id: str) -> str:
    return f"https://x.com/{handle}/status/{post_id}"


def run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg_path = root / "markets/config/sources.yaml"

    now = now_jst()
    date_str = now.strftime("%Y-%m-%d")
    run_ts = now.isoformat()

    log_path = root / f"markets/logs/{date_str}.log"
    logger = setup_logger(log_path)

    logger.info("collector start")
    cfg = load_yaml(cfg_path)

    accounts: List[AccountCfg] = []
    for a in cfg.get("accounts", []):
        handle = a.get("handle") or a.get("x_handle")
        market = a.get("market")
        source = a.get("source", "static")
        if not handle or not market:
            raise CollectorError(f"invalid account config: {a}")
        accounts.append(AccountCfg(handle=handle, market=market, source=source))
    if not accounts:
        raise CollectorError("accounts is empty in config")

    lookback_hours = int(cfg.get("lookback_hours", 24))
    state_path = root / "markets/state/collector-state.json"
    state = load_state(state_path, accounts)

    token = os.getenv("X_BEARER_TOKEN", "")
    if not token and not args.dry_run:
        raise CollectorError("X_BEARER_TOKEN is not set")

    run_result: Dict[str, Any] = {
        "run_at": run_ts,
        "lookback_hours": lookback_hours,
        "dry_run": args.dry_run,
        "accounts": {},
        "stats": {
            "total_posts": 0,
            "account_success": 0,
            "account_failed": 0,
        },
        "errors": [],
    }

    session = requests.Session()
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # Optional list sync (before collection)
    list_sync_cfg = cfg.get("list_sync", {}) or {}
    list_sync_info: Dict[str, Any] = {
        "enabled": bool(list_sync_cfg.get("enabled", False)),
        "status": "skipped",
        "owner_handle": list_sync_cfg.get("owner_handle"),
        "list_ids": list_sync_cfg.get("list_ids", []),
        "added_accounts": [],
        "removed_accounts": [],
        "error": None,
    }
    if list_sync_info["enabled"] and not args.dry_run:
        try:
            dynamic_market = list_sync_cfg.get("default_market", "other-market")
            list_ids = list_sync_cfg.get("list_ids", []) or []
            refresh_before = bool(list_sync_cfg.get("refresh_before_collect", True))
            if refresh_before and list_ids:
                synced_members: List[str] = []
                for lid in list_ids:
                    synced_members.extend(collect_list_members(session, headers, str(lid)))
                synced_set = {m.lower() for m in synced_members}

                # current config map
                cfg_accounts = cfg.get("accounts", []) or []
                cfg_map = {}
                for item in cfg_accounts:
                    h = (item.get("handle") or item.get("x_handle") or "").strip()
                    if not h:
                        continue
                    cfg_map[h.lower()] = item

                # add new list_sync members
                for m in synced_members:
                    key = m.lower()
                    if key in cfg_map:
                        continue
                    new_item = {
                        "name": f"list_{m}",
                        "x_handle": m,
                        "market": dynamic_market,
                        "source": "list_sync",
                    }
                    cfg_accounts.append(new_item)
                    cfg_map[key] = new_item
                    list_sync_info["added_accounts"].append(m)

                # remove stale list_sync members (keep static)
                keep_accounts = []
                for item in cfg_accounts:
                    h = (item.get("handle") or item.get("x_handle") or "").strip()
                    src = item.get("source", "static")
                    if src == "list_sync" and h and h.lower() not in synced_set:
                        list_sync_info["removed_accounts"].append(h)
                        continue
                    keep_accounts.append(item)
                cfg["accounts"] = keep_accounts

                # persist config when changed
                if list_sync_info["added_accounts"] or list_sync_info["removed_accounts"]:
                    save_yaml(cfg_path, cfg)
                    logger.info("list sync updated config added=%s removed=%s",
                                len(list_sync_info["added_accounts"]),
                                len(list_sync_info["removed_accounts"]))

                # rebuild accounts from updated cfg
                accounts = []
                for a in cfg.get("accounts", []):
                    handle = a.get("handle") or a.get("x_handle")
                    market = a.get("market")
                    source = a.get("source", "static")
                    if handle and market:
                        accounts.append(AccountCfg(handle=handle, market=market, source=source))

                list_sync_info["status"] = "ok"
            else:
                list_sync_info["status"] = "skipped"
        except Exception as e:
            list_sync_info["status"] = "error"
            list_sync_info["error"] = str(e)
            logger.error("list sync failed: %s", e)

    run_result["list_sync"] = list_sync_info

    for a in accounts:
        state["accounts"].setdefault(a.handle, {"since_id": "0"})
        since_id = state["accounts"][a.handle].get("since_id", "0")
        logger.info("collecting @%s market=%s since_id=%s", a.handle, a.market, since_id)
        acct = {
            "handle": a.handle,
            "market": a.market,
            "source": a.source,
            "since_id_before": since_id,
            "since_id_after": since_id,
            "posts": [],
            "count": 0,
            "status": "ok",
            "error": None,
        }

        try:
            if args.dry_run:
                posts: List[Dict[str, Any]] = []
            else:
                uid = get_user_id(session, headers, a.handle)
                raw = collect_user_posts(session, headers, uid, since_id, lookback_hours)
                posts = []
                for p in raw:
                    pid = p["id"]
                    posts.append(
                        {
                            "post_id": pid,
                            "author_handle": a.handle,
                            "market": a.market,
                            "text": p.get("text", ""),
                            "created_at": p.get("created_at"),
                            "url": canonical_url(a.handle, pid),
                            "lang": p.get("lang"),
                            "public_metrics": p.get("public_metrics", {}),
                        }
                    )

            acct["posts"] = posts
            acct["count"] = len(posts)
            if posts:
                max_id = max(int(p["post_id"]) for p in posts)
                acct["since_id_after"] = str(max_id)
                state["accounts"][a.handle]["since_id"] = str(max_id)

            run_result["stats"]["total_posts"] += acct["count"]
            run_result["stats"]["account_success"] += 1
        except Exception as e:
            acct["status"] = "error"
            acct["error"] = str(e)
            run_result["stats"]["account_failed"] += 1
            run_result["errors"].append({"handle": a.handle, "error": str(e)})
            logger.error("failed @%s: %s", a.handle, e)

        run_result["accounts"][a.handle] = acct

    run_path = root / f"markets/runs/{date_str}.json"
    save_json(run_path, run_result)

    active_sources = {
        "updated_at": run_ts,
        "accounts": [
            {"handle": a.handle, "market": a.market, "source": a.source}
            for a in accounts
        ],
    }
    save_json(root / "markets/state/active-sources.json", active_sources)

    state["last_run_at"] = run_ts
    state["last_success"] = run_result["stats"]["account_failed"] == 0
    save_json(state_path, state)

    logger.info("collector done total_posts=%s success=%s failed=%s dry_run=%s",
                run_result["stats"]["total_posts"],
                run_result["stats"]["account_success"],
                run_result["stats"]["account_failed"],
                args.dry_run)

    return 0 if state["last_success"] else 1


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Collect posts from configured X accounts")
    p.add_argument("--root", default=".", help="workspace root")
    p.add_argument("--dry-run", action="store_true", help="run without external API calls")
    return p.parse_args()


if __name__ == "__main__":
    try:
        sys.exit(run(parse_args()))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
