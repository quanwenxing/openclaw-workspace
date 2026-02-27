from arb_bot.engine import evaluate_opportunity
from arb_bot.risk import RiskState, check_risk


def _cfg():
    return {
        "runtime": {"stale_book_ms": 1000, "max_cross_exchange_skew_ms": 200},
        "market": {"min_notional_quote": 10.0, "lot_size_step": 0.0001},
        "costs": {
            "taker_fee_buy": 0.001,
            "taker_fee_sell": 0.001,
            "withdrawal_fee_quote": 0.0,
            "network_fee_quote": 0.0,
            "slippage_bps": 0.0,
            "latency_penalty_bps": 0.0,
        },
        "risk": {
            "max_position_base": 10,
            "max_daily_loss_quote": 1000,
            "max_open_orders": 10,
            "kill_switch": False,
            "circuit_breaker_failures": 5,
            "max_inventory_skew_base": 0.5,
            "max_order_age_ms": 1000,
            "volatility_pause_bps": 50,
            "pause_on_connection_unhealthy": True,
        },
    }


def _book(ts, recv):
    return {
        "bids": [[100.0, 1.0]],
        "asks": [[100.1, 1.0]],
        "exchange_ts": ts,
        "recv_ts": recv,
    }


def test_reject_cross_exchange_skew():
    cfg = _cfg()
    now = 10_000
    b1 = _book(9_000, 9_800)
    b2 = _book(9_400, 9_800)  # 400ms skew > 200
    res = evaluate_opportunity(cfg, b1, b2, 0.1, 10000, 10, RiskState(), False, now_ms=now)
    assert not res.executable
    assert res.reason == "cross-exchange-skew"


def test_reject_stale_book():
    cfg = _cfg()
    now = 10_000
    b1 = _book(9_900, 8_000)  # stale by recv_ts
    b2 = _book(9_900, 9_900)
    res = evaluate_opportunity(cfg, b1, b2, 0.1, 10000, 10, RiskState(), False, now_ms=now)
    assert not res.executable
    assert res.reason == "stale-book"


def test_risk_guard_inventory_skew_and_volatility_pause():
    cfg = _cfg()
    s = RiskState(inventory_skew_base=0.8)
    ok, reason = check_risk(s, cfg, requested_base=0.1)
    assert not ok
    assert reason == "max-inventory-skew"

    s2 = RiskState(volatility_bps=120)
    ok2, reason2 = check_risk(s2, cfg, requested_base=0.1)
    assert not ok2
    assert reason2 == "volatility-pause"
