from __future__ import annotations

import argparse
import time
from pathlib import Path

import yaml

from .strategy import evaluate_opportunity, from_config, risk_allows_trade


def load_config(path: str):
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/default.yaml")
    parser.add_argument("--live", action="store_true", help="live execution (dangerous)")
    parser.add_argument("--paper", action="store_true", default=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.live and not cfg.get("allow_live", False):
        raise SystemExit("allow_live=false のため live 実行をブロックしました")

    costs, constraints, limits = from_config(cfg)

    current_position = 0.0
    day_realized = 0.0
    open_orders = 0
    failed_fills = 0

    print("paper mode start" if not args.live else "LIVE mode start")
    print("このサンプルは取引所接続を省略し、戦略判定とリスク制御を示します。")

    for _ in range(5):
        buy_asks = [(100.0, 2.0), (100.3, 3.0)]
        sell_bids = [(100.4, 2.0), (100.1, 3.0)]
        order_size = cfg["strategy"]["trade_size_base"]

        ok, reason = risk_allows_trade(
            limits, current_position, day_realized, open_orders, failed_fills, order_size
        )
        if not ok:
            print(f"[SKIP] risk guard: {reason}")
            time.sleep(1)
            continue

        opp = evaluate_opportunity(
            buy_asks,
            sell_bids,
            target_size=order_size,
            constraints=constraints,
            costs=costs,
            transfer_based=cfg["strategy"]["transfer_based"],
            stale_seconds=0.2,
            max_stale_seconds=cfg["strategy"]["max_stale_seconds"],
        )
        if opp.executable:
            day_realized += opp.net_pnl_quote
            print(f"[TRADE] net_pnl={opp.net_pnl_quote:.4f} edge_bps={opp.edge_bps:.2f}")
        else:
            print(f"[SKIP] {opp.reason} net={opp.net_pnl_quote:.4f}")
            if opp.reason in {"insufficient_depth", "stale_orderbook"}:
                failed_fills += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
