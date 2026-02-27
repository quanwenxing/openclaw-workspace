from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskState:
    daily_pnl: float = 0.0
    open_orders: int = 0
    consecutive_failures: int = 0
    killed: bool = False
    inventory_skew_base: float = 0.0
    inventory_skew_ratio: float = 0.0
    oldest_order_age_ms: int = 0
    volatility_bps: float = 0.0
    connections_healthy: bool = True


def check_risk(state: RiskState, cfg: dict, requested_base: float, now_ms: int | None = None) -> tuple[bool, str]:
    guards = cfg["risk"]
    if state.killed or guards.get("kill_switch", False):
        return False, "kill-switch"
    if requested_base > guards["max_position_base"]:
        return False, "max-position"
    if state.daily_pnl <= -abs(guards["max_daily_loss_quote"]):
        return False, "max-daily-loss"
    if state.open_orders >= guards["max_open_orders"]:
        return False, "max-open-orders"
    if state.consecutive_failures >= guards["circuit_breaker_failures"]:
        return False, "circuit-breaker"

    ratio_limit = guards.get("max_inventory_skew_ratio")
    if ratio_limit is not None and state.inventory_skew_ratio > ratio_limit:
        return False, "inventory-skew"
    if state.inventory_skew_base > guards.get("max_inventory_skew_base", float("inf")):
        return False, "max-inventory-skew"
    if state.oldest_order_age_ms > guards.get("max_order_age_ms", float("inf")):
        return False, "max-order-age"
    if state.volatility_bps > guards.get("volatility_pause_bps", float("inf")):
        return False, "volatility-pause"
    if not state.connections_healthy and guards.get("pause_on_connection_unhealthy", True):
        return False, "connection-health-pause"
    return True, "ok"
