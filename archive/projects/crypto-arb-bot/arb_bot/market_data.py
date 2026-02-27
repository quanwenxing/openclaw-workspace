from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Protocol


@dataclass
class BookSnapshot:
    exchange: str
    symbol: str
    book: dict
    exchange_ts: int
    recv_ts: int


@dataclass
class MarketBook:
    exchange: str
    symbol: str
    bids: list[list[float]]
    asks: list[list[float]]
    exchange_ts: int
    recv_ts: int
    source: str = "rest"


class MarketDataClient(Protocol):
    def get_book(self, symbol: str, limit: int = 20) -> MarketBook: ...


class RestMarketDataClient:
    def __init__(self, exchange, exchange_name: str):
        self.exchange = exchange
        self.exchange_name = exchange_name

    def get_book(self, symbol: str, limit: int = 20) -> MarketBook:
        recv_ts = int(time.time() * 1000)
        raw = self.exchange.fetch_order_book(symbol, limit=limit)
        exchange_ts = int(raw.get("timestamp") or recv_ts)
        return MarketBook(
            exchange=self.exchange_name,
            symbol=symbol,
            bids=raw.get("bids", []),
            asks=raw.get("asks", []),
            exchange_ts=exchange_ts,
            recv_ts=recv_ts,
            source="rest",
        )


class WsMarketDataClient:
    """WebSocket market data scaffold.

    TODO:
      - implement exchange-specific subscribe/connect via ccxt.pro or native ws clients.
      - fill live cache from ws updates and serve best-effort synchronized books.
      - add heartbeat/ping and real reconnect with backoff.
    """

    def __init__(self, exchange_name: str, reconnect_base_ms: int = 500):
        self.exchange_name = exchange_name
        self.reconnect_base_ms = reconnect_base_ms
        self.connected = False
        self.last_error: str | None = None
        self.reconnect_attempts = 0

    def connect(self) -> None:
        self.connected = True
        self.reconnect_attempts = 0

    def on_disconnect(self, reason: str) -> None:
        self.connected = False
        self.last_error = reason

    def reconnect_delay_ms(self) -> int:
        self.reconnect_attempts += 1
        return min(self.reconnect_base_ms * (2 ** self.reconnect_attempts), 10_000)

    def get_book(self, symbol: str, limit: int = 20) -> MarketBook:
        raise NotImplementedError("WS client scaffold only. Use REST fallback for now.")


def validate_snapshot_pair(cfg: dict, buy: BookSnapshot, sell: BookSnapshot, decision_ts_ms: int) -> tuple[bool, str]:
    runtime = cfg["runtime"]
    stale_ms = runtime["stale_book_ms"]
    if decision_ts_ms - buy.recv_ts > stale_ms or decision_ts_ms - sell.recv_ts > stale_ms:
        return False, "stale-book"
    if abs(buy.exchange_ts - sell.exchange_ts) > runtime.get("max_cross_exchange_skew_ms", 500):
        return False, "cross-exchange-skew"
    return True, "ok"


def build_market_data_client(mode: str, rest_exchange, exchange_name: str):
    mode = (mode or "rest").lower()
    if mode == "ws":
        return RestMarketDataClient(rest_exchange, exchange_name)
    return RestMarketDataClient(rest_exchange, exchange_name)
