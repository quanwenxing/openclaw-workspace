from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from .execution import executable_price
from .costs import evaluate_cross_exchange_trade
from .models import CostAssumptions, MarketConstraints


@dataclass
class RiskLimits:
    max_position_base: float
    max_daily_loss_quote: float
    max_open_orders: int
    max_failed_fills: int


@dataclass
class OpportunityResult:
    executable: bool
    reason: str
    net_pnl_quote: float
    edge_bps: float


def _round_down(value: float, step: float) -> float:
    if step <= 0:
        return value
    units = int(value / step)
    return units * step


def evaluate_opportunity(
    buy_asks,
    sell_bids,
    target_size,
    constraints: MarketConstraints,
    costs: CostAssumptions,
    transfer_based: bool,
    stale_seconds: float,
    max_stale_seconds: float = 1.5,
) -> OpportunityResult:
    if stale_seconds > max_stale_seconds:
        return OpportunityResult(False, "stale_orderbook", 0.0, 0.0)

    size = _round_down(target_size, constraints.amount_step)
    if size <= 0:
        return OpportunityResult(False, "size_too_small", 0.0, 0.0)

    buy = executable_price(buy_asks, size)
    sell = executable_price(sell_bids, size)
    if buy.filled_size < size or sell.filled_size < size:
        return OpportunityResult(False, "insufficient_depth", 0.0, 0.0)

    if buy.gross_quote < constraints.min_notional or sell.gross_quote < constraints.min_notional:
        return OpportunityResult(False, "min_notional", 0.0, 0.0)

    eval_res = evaluate_cross_exchange_trade(
        buy_avg_price=buy.avg_price,
        sell_avg_price=sell.avg_price,
        size_base=size,
        costs=costs,
        transfer_based=transfer_based,
    )
    edge_bps = (eval_res.net_pnl_quote / buy.gross_quote) * 10_000 if buy.gross_quote else 0.0
    if eval_res.net_pnl_quote <= 0:
        return OpportunityResult(False, "negative_after_cost", eval_res.net_pnl_quote, edge_bps)

    return OpportunityResult(True, "ok", eval_res.net_pnl_quote, edge_bps)


def risk_allows_trade(
    limits: RiskLimits,
    current_position_base: float,
    day_realized_pnl_quote: float,
    open_orders: int,
    failed_fills: int,
    order_size_base: float,
) -> tuple[bool, str]:
    if abs(current_position_base + order_size_base) > limits.max_position_base:
        return False, "max_position"
    if day_realized_pnl_quote <= -abs(limits.max_daily_loss_quote):
        return False, "max_daily_loss"
    if open_orders >= limits.max_open_orders:
        return False, "max_open_orders"
    if failed_fills >= limits.max_failed_fills:
        return False, "circuit_breaker_failed_fills"
    return True, "ok"


def from_config(cfg: Dict[str, Any]):
    c = cfg["costs"]
    m = cfg["market_constraints"]
    r = cfg["risk_limits"]
    costs = CostAssumptions(**c)
    constraints = MarketConstraints(**m)
    limits = RiskLimits(**r)
    return costs, constraints, limits
