#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import ccxt

ROOT = Path(__file__).resolve().parents[1]


def snap(exchange_id: str, symbol: str = "BTC/USDT") -> dict:
    ex = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    ex.load_markets()
    out = {"exchange": exchange_id, "symbol": symbol}

    try:
        out["trading_fee"] = ex.fetch_trading_fee(symbol)
    except Exception as e:
        out["trading_fee_error"] = str(e)
        m = ex.markets.get(symbol, {})
        out["market_fallback_fees"] = {"maker": m.get("maker"), "taker": m.get("taker")}

    try:
        c = ex.fetch_currencies()
        btc = c.get("BTC", {})
        out["btc_networks"] = btc.get("networks", {})
        out["btc_withdraw_fee"] = btc.get("fee")
    except Exception as e:
        out["currency_fee_error"] = str(e)

    return out


def main() -> None:
    rows = [snap("binance"), snap("kraken"), snap("coinbase")]
    out_path = ROOT / "reports" / "fee_snapshot.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"saved: {out_path}")
    print(json.dumps(rows, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main()
