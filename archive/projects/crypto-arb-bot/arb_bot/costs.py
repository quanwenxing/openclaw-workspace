from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CostInputs:
    buy_notional: float
    sell_notional: float
    taker_fee_buy: float
    taker_fee_sell: float
    withdrawal_fee_quote: float
    network_fee_quote: float
    slippage_bps: float
    latency_bps: float
    transfer_mode: bool


def calc_total_cost_quote(c: CostInputs) -> float:
    trade_fees = c.buy_notional * c.taker_fee_buy + c.sell_notional * c.taker_fee_sell
    slippage = (c.buy_notional + c.sell_notional) * (c.slippage_bps / 10_000)
    latency = (c.buy_notional + c.sell_notional) * (c.latency_bps / 10_000)
    transfer_cost = (c.withdrawal_fee_quote + c.network_fee_quote) if c.transfer_mode else 0.0
    return trade_fees + slippage + latency + transfer_cost


def net_edge_quote(gross_edge_quote: float, c: CostInputs) -> float:
    return gross_edge_quote - calc_total_cost_quote(c)
