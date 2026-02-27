from arb_bot.costs import CostInputs, calc_total_cost_quote


def test_cost_model_transfer_vs_no_transfer():
    c_transfer = CostInputs(
        buy_notional=1000,
        sell_notional=1015,
        taker_fee_buy=0.001,
        taker_fee_sell=0.001,
        withdrawal_fee_quote=3,
        network_fee_quote=2,
        slippage_bps=5,
        latency_bps=2,
        transfer_mode=True,
    )
    c_no_transfer = CostInputs(**{**c_transfer.__dict__, "transfer_mode": False})

    t = calc_total_cost_quote(c_transfer)
    n = calc_total_cost_quote(c_no_transfer)
    assert t > n
    assert round(t - n, 8) == 5.0
