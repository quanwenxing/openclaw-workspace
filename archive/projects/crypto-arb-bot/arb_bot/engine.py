from __future__ import annotations

from dataclasses import dataclass
import time

from .execution import executable_price
from .costs import CostInputs, calc_total_cost_quote
from .risk import RiskState, check_risk


@dataclass
class OpportunityResult:
    executable: bool
    reason: str
    gross_edge_quote: float
    total_cost_quote: float
    net_edge_quote: float


def _book_ts(book: dict, fallback: int) -> int:
    return int(book.get("exchange_ts") or book.get("timestamp") or fallback)


def validate_constraints(
    cfg: dict,
    amount_base: float,
    buy_px: float,
    buy_depth_ok: bool,
    sell_depth_ok: bool,
    buy_balance_quote: float,
    sell_balance_base: float,
    buy_book: dict,
    sell_book: dict,
    decision_ts: int,
) -> tuple[bool, str]:
    market = cfg["market"]
    min_notional = market["min_notional_quote"]
    if amount_base * buy_px < min_notional:
        return False, "min-notional"
    step = market["lot_size_step"]
    if abs((amount_base / step) - round(amount_base / step)) > 1e-9:
        return False, "lot-size"
    if not buy_depth_ok or not sell_depth_ok:
        return False, "depth"
    if buy_balance_quote < amount_base * buy_px:
        return False, "buy-balance"
    if sell_balance_base < amount_base:
        return False, "sell-balance"

    runtime = cfg["runtime"]
    stale_ms = runtime["stale_book_ms"]
    buy_recv_ts = int(buy_book.get("recv_ts") or decision_ts)
    sell_recv_ts = int(sell_book.get("recv_ts") or decision_ts)
    if decision_ts - buy_recv_ts > stale_ms or decision_ts - sell_recv_ts > stale_ms:
        return False, "stale-book"

    buy_exchange_ts = _book_ts(buy_book, buy_recv_ts)
    sell_exchange_ts = _book_ts(sell_book, sell_recv_ts)
    skew = abs(buy_exchange_ts - sell_exchange_ts)
    if skew > runtime.get("max_cross_exchange_skew_ms", 500):
        return False, "cross-exchange-skew"

    return True, "ok"


def evaluate_opportunity(
    cfg: dict,
    buy_book: dict,
    sell_book: dict,
    amount_base: float,
    buy_balance_quote: float,
    sell_balance_base: float,
    state: RiskState,
    transfer_mode: bool,
    ts_ms: int | None = None,
    now_ms: int | None = None,
) -> OpportunityResult:
    decision_ts = now_ms or int(time.time() * 1000)
    _ = ts_ms  # kept for compatibility with previous API

    allowed, risk_reason = check_risk(state, cfg, amount_base)
    if not allowed:
        return OpportunityResult(False, risk_reason, 0.0, 0.0, 0.0)

    buy_exec = executable_price(buy_book, "buy", amount_base)
    sell_exec = executable_price(sell_book, "sell", amount_base)

    ok, reason = validate_constraints(
        cfg,
        amount_base,
        buy_exec.avg_price,
        buy_exec.depth_ok,
        sell_exec.depth_ok,
        buy_balance_quote,
        sell_balance_base,
        buy_book,
        sell_book,
        decision_ts,
    )
    if not ok:
        return OpportunityResult(False, reason, 0.0, 0.0, 0.0)

    buy_notional = buy_exec.filled_quote
    sell_notional = sell_exec.filled_quote
    gross = sell_notional - buy_notional

    costs_cfg = cfg["costs"]
    c = CostInputs(
        buy_notional=buy_notional,
        sell_notional=sell_notional,
        taker_fee_buy=costs_cfg["taker_fee_buy"],
        taker_fee_sell=costs_cfg["taker_fee_sell"],
        withdrawal_fee_quote=costs_cfg["withdrawal_fee_quote"],
        network_fee_quote=costs_cfg["network_fee_quote"],
        slippage_bps=costs_cfg["slippage_bps"],
        latency_bps=costs_cfg["latency_penalty_bps"],
        transfer_mode=transfer_mode,
    )
    total = calc_total_cost_quote(c)
    net = gross - total
    return OpportunityResult(True, "ok", gross, total, net)
