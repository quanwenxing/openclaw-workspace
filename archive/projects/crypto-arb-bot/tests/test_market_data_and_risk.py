from arb_bot.market_data import BookSnapshot, validate_snapshot_pair
from arb_bot.risk import RiskState, check_risk


def cfg():
    return {
        "runtime": {"stale_book_ms": 1000, "max_cross_exchange_skew_ms": 200},
        "risk": {
            "max_position_base": 1.0,
            "max_daily_loss_quote": 100,
            "max_open_orders": 3,
            "circuit_breaker_failures": 2,
            "max_inventory_skew_ratio": 0.3,
            "max_order_age_ms": 5000,
            "volatility_pause_bps": 50,
            "kill_switch": False,
        },
    }


def test_skew_rejection():
    c = cfg()
    b = BookSnapshot("a", "BTC/USD", {"bids": [], "asks": []}, 10000, 10010)
    s = BookSnapshot("b", "BTC/USD", {"bids": [], "asks": []}, 10350, 10010)
    ok, reason = validate_snapshot_pair(c, b, s, decision_ts_ms=10020)
    assert not ok
    assert reason == "cross-exchange-skew"


def test_stale_rejection():
    c = cfg()
    b = BookSnapshot("a", "BTC/USD", {"bids": [], "asks": []}, 10000, 10000)
    s = BookSnapshot("b", "BTC/USD", {"bids": [], "asks": []}, 10020, 10000)
    ok, reason = validate_snapshot_pair(c, b, s, decision_ts_ms=12050)
    assert not ok
    assert reason in {"stale-book", "stale-exchange-ts"}


def test_risk_guard_inventory_skew():
    c = cfg()
    st = RiskState(inventory_skew_ratio=0.5)
    ok, reason = check_risk(st, c, requested_base=0.1, now_ms=1000)
    assert not ok
    assert reason == "inventory-skew"
