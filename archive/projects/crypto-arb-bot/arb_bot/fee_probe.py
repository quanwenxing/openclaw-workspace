from __future__ import annotations

import json
from pathlib import Path

import ccxt


def probe_exchange(exchange_id: str, symbol: str = "BTC/USDT") -> dict:
    ex_class = getattr(ccxt, exchange_id)
    ex = ex_class({"enableRateLimit": True})
    ex.load_markets()

    market = ex.market(symbol) if symbol in ex.markets else None
    trading = {
        "maker": market.get("maker") if market else None,
        "taker": market.get("taker") if market else None,
    }

    withdrawal = {}
    try:
        currencies = ex.fetch_currencies()
        btc = currencies.get("BTC", {})
        nets = btc.get("networks") or {}
        for net, info in nets.items():
            if info.get("withdraw") is not None:
                withdrawal[net] = {
                    "withdraw": info.get("withdraw"),
                    "fee": info.get("fee"),
                }
        if not withdrawal and btc:
            withdrawal["default"] = {
                "withdraw": btc.get("withdraw"),
                "fee": btc.get("fee"),
            }
    except Exception as e:
        withdrawal = {"error": str(e)}

    return {
        "exchange": exchange_id,
        "symbol": symbol,
        "trading_fee_market": trading,
        "withdrawal_btc": withdrawal,
    }


def main():
    out = []
    for ex in ["bybit", "okx", "kucoin"]:
        try:
            out.append(probe_exchange(ex))
        except Exception as e:
            out.append({"exchange": ex, "error": str(e)})

    Path("reports").mkdir(exist_ok=True)
    with Path("reports/fee_probe.json").open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
