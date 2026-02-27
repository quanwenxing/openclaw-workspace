from __future__ import annotations

from dataclasses import dataclass
import uuid


@dataclass
class SimOrder:
    exchange: str
    symbol: str
    side: str
    order_type: str  # IOC/FOK/POST_ONLY
    price: float
    size: float


@dataclass
class SimFill:
    order_id: str
    requested_size: float
    filled_size: float
    avg_price: float
    status: str  # filled/partial/rejected
    reason: str = "ok"


class OrderManager:
    def __init__(self, paper_mode: bool = True, live_enabled: bool = False):
        self.paper_mode = paper_mode
        self.live_enabled = live_enabled

    def submit(self, order: SimOrder, book: dict) -> SimFill:
        if not self.paper_mode and not self.live_enabled:
            return SimFill("", order.size, 0.0, 0.0, "rejected", "live-disabled")
        if self.paper_mode:
            return self._simulate(order, book)
        return SimFill("", order.size, 0.0, 0.0, "rejected", "live-not-implemented")

    def _simulate(self, order: SimOrder, book: dict) -> SimFill:
        oid = str(uuid.uuid4())
        levels = book["asks"] if order.side == "buy" else book["bids"]
        remaining = order.size
        filled_quote = 0.0
        for px, sz in levels:
            if order.side == "buy" and px > order.price:
                break
            if order.side == "sell" and px < order.price:
                break
            take = min(remaining, sz)
            remaining -= take
            filled_quote += take * px
            if remaining <= 1e-12:
                break

        filled = order.size - remaining
        if order.order_type == "FOK" and filled + 1e-12 < order.size:
            return SimFill(oid, order.size, 0.0, 0.0, "rejected", "fok-unfilled")
        if order.order_type == "POST_ONLY":
            top_ask = levels[0][0] if order.side == "buy" and levels else None
            top_bid = levels[0][0] if order.side == "sell" and levels else None
            if (order.side == "buy" and top_ask is not None and order.price >= top_ask) or (
                order.side == "sell" and top_bid is not None and order.price <= top_bid
            ):
                return SimFill(oid, order.size, 0.0, 0.0, "rejected", "post-only-would-take")
            return SimFill(oid, order.size, 0.0, 0.0, "rejected", "post-only-resting-not-simulated")

        if filled <= 1e-12:
            return SimFill(oid, order.size, 0.0, 0.0, "rejected", "no-liquidity")
        avg = filled_quote / filled
        if order.order_type == "IOC" and filled < order.size:
            return SimFill(oid, order.size, filled, avg, "partial", "ioc-partial")
        return SimFill(oid, order.size, filled, avg, "filled", "ok")
