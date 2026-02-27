from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExchangeBalance:
    base: float
    quote: float


@dataclass
class InventoryState:
    buy_ex: ExchangeBalance
    sell_ex: ExchangeBalance


def inventory_skew_base(state: InventoryState) -> float:
    total = state.buy_ex.base + state.sell_ex.base
    if total <= 1e-12:
        return 0.0
    target = total / 2
    return abs(state.buy_ex.base - target)


def rebalancing_recommendation(state: InventoryState, max_skew_base: float) -> str:
    skew = inventory_skew_base(state)
    if skew <= max_skew_base:
        return "balanced"
    if state.buy_ex.base > state.sell_ex.base:
        amount = (state.buy_ex.base - state.sell_ex.base) / 2
        return f"recommend: shift {amount:.6f} base from buy_ex to sell_ex (paper-only, no auto-transfer)"
    amount = (state.sell_ex.base - state.buy_ex.base) / 2
    return f"recommend: shift {amount:.6f} base from sell_ex to buy_ex (paper-only, no auto-transfer)"
