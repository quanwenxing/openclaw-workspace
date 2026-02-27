from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExecutableResult:
    avg_price: float
    filled_base: float
    filled_quote: float
    depth_ok: bool


def executable_price(orderbook: dict, side: str, amount_base: float) -> ExecutableResult:
    if amount_base <= 0:
        raise ValueError("amount_base must be positive")
    levels = orderbook["asks"] if side == "buy" else orderbook["bids"]
    remaining = amount_base
    filled_quote = 0.0
    filled_base = 0.0

    for level in levels:
        price, size = level[0], level[1]
        take = min(size, remaining)
        filled_quote += take * price
        filled_base += take
        remaining -= take
        if remaining <= 1e-12:
            break

    if filled_base <= 0:
        return ExecutableResult(0.0, 0.0, 0.0, False)

    return ExecutableResult(
        avg_price=filled_quote / filled_base,
        filled_base=filled_base,
        filled_quote=filled_quote,
        depth_ok=remaining <= 1e-12,
    )
