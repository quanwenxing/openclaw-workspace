#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import time
from arb_bot.config import load_config
from arb_bot.connectors import make_exchange
from arb_bot.engine import evaluate_opportunity
from arb_bot.inventory import ExchangeBalance, InventoryState, inventory_skew_base, rebalancing_recommendation
from arb_bot.market_data import build_market_data_client
from arb_bot.observability import JsonlLogger
from arb_bot.order_manager import OrderManager, SimOrder
from arb_bot.risk import RiskState

ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--live", action="store_true", help="enable live orders (disabled by default)")
    p.add_argument("--loops", type=int, default=3)
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(ROOT / "config" / "default.yaml").raw
    if args.live and not cfg["runtime"].get("live_enabled", False):
        raise SystemExit("Live trading is disabled in config (runtime.live_enabled=false).")

    def _safe_cred(v):
        if not isinstance(v, str):
            return v
        return None if "${" in v else v

    ex_buy = make_exchange(
        cfg["exchanges"]["buy"]["id"],
        api_key=_safe_cred(cfg["exchanges"]["buy"].get("api_key")),
        secret=_safe_cred(cfg["exchanges"]["buy"].get("api_secret")),
    )
    ex_sell = make_exchange(
        cfg["exchanges"]["sell"]["id"],
        api_key=_safe_cred(cfg["exchanges"]["sell"].get("api_key")),
        secret=_safe_cred(cfg["exchanges"]["sell"].get("api_secret")),
    )

    buy_md = build_market_data_client(cfg["runtime"].get("market_data_mode", "rest"), ex_buy, cfg["exchanges"]["buy"]["id"])
    sell_md = build_market_data_client(cfg["runtime"].get("market_data_mode", "rest"), ex_sell, cfg["exchanges"]["sell"]["id"])

    symbol = cfg["market"]["symbol"]
    amount_base = cfg["market"]["trade_size_base"]

    state = RiskState()
    inventory = InventoryState(
        buy_ex=ExchangeBalance(base=cfg["sim"]["initial_base_buy_ex"], quote=cfg["sim"]["initial_quote_buy_ex"]),
        sell_ex=ExchangeBalance(base=cfg["sim"]["initial_base_sell_ex"], quote=cfg["sim"]["initial_quote_sell_ex"]),
    )

    om = OrderManager(paper_mode=cfg["runtime"].get("paper_mode", True), live_enabled=cfg["runtime"].get("live_enabled", False))
    decisions_log = JsonlLogger(ROOT / "reports" / "logs" / "decisions.jsonl")
    orders_log = JsonlLogger(ROOT / "reports" / "logs" / "orders.jsonl")
    errors_log = JsonlLogger(ROOT / "reports" / "logs" / "errors.jsonl")

    print(f"mode={'LIVE' if args.live else 'PAPER'} symbol={symbol}")
    for _ in range(args.loops):
        try:
            buy_book = buy_md.get_book(symbol, limit=20).__dict__
            sell_book = sell_md.get_book(symbol, limit=20).__dict__
            decision_ts = int(time.time() * 1000)

            state.inventory_skew_base = inventory_skew_base(inventory)
            state.connections_healthy = True

            res = evaluate_opportunity(
                cfg,
                buy_book,
                sell_book,
                amount_base,
                buy_balance_quote=inventory.buy_ex.quote,
                sell_balance_base=inventory.sell_ex.base,
                state=state,
                transfer_mode=False,
                now_ms=decision_ts,
            )

            decisions_log.log(
                "decision",
                {
                    "exec": res.executable,
                    "reason": res.reason,
                    "net": round(res.net_edge_quote, 6),
                    "decision_ts": decision_ts,
                    "buy_exchange_ts": buy_book.get("exchange_ts"),
                    "sell_exchange_ts": sell_book.get("exchange_ts"),
                },
            )

            if res.executable:
                buy_order = SimOrder(cfg["exchanges"]["buy"]["id"], symbol, "buy", "IOC", buy_book["asks"][0][0], amount_base)
                sell_order = SimOrder(cfg["exchanges"]["sell"]["id"], symbol, "sell", "IOC", sell_book["bids"][0][0], amount_base)
                buy_fill = om.submit(buy_order, buy_book)
                sell_fill = om.submit(sell_order, sell_book)
                orders_log.log("order", {"leg": "buy", **buy_fill.__dict__})
                orders_log.log("order", {"leg": "sell", **sell_fill.__dict__})

                filled = min(buy_fill.filled_size, sell_fill.filled_size)
                if filled > 0:
                    inventory.buy_ex.base += filled
                    inventory.buy_ex.quote -= buy_fill.avg_price * filled
                    inventory.sell_ex.base -= filled
                    inventory.sell_ex.quote += sell_fill.avg_price * filled
                    state.daily_pnl += (sell_fill.avg_price - buy_fill.avg_price) * filled
                if buy_fill.status == "rejected" or sell_fill.status == "rejected":
                    state.consecutive_failures += 1
            else:
                if res.reason in {"stale-book", "cross-exchange-skew", "connection-health-pause"}:
                    state.consecutive_failures += 1

            rec = rebalancing_recommendation(inventory, cfg["risk"]["max_inventory_skew_base"])
            print({"exec": res.executable, "reason": res.reason, "net": round(res.net_edge_quote, 4), "rebalance": rec})
        except Exception as e:  # noqa: BLE001
            errors_log.log("error", {"message": str(e)})
            state.connections_healthy = False
            print({"exec": False, "reason": "error", "error": str(e)})

        time.sleep(cfg["runtime"]["poll_sec"])


if __name__ == "__main__":
    main()
