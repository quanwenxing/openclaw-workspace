from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class CostAssumptions:
    taker_fee_buy: float
    taker_fee_sell: float
    maker_fee_buy: float = 0.0
    maker_fee_sell: float = 0.0
    withdrawal_fee_base: float = 0.0
    network_fee_quote: float = 0.0
    slippage_bps: float = 0.0
    latency_bps: float = 0.0


@dataclass
class MarketConstraints:
    min_notional: float
    amount_step: float
    price_step: float


OrderBookSide = List[Tuple[float, float]]  # (price, size)


@dataclass
class ExecutableQuote:
    avg_price: float
    filled_size: float
    gross_quote: float
