from arb_bot.execution import executable_price


def test_executable_price_depth_and_average():
    ob = {
        "asks": [[100, 0.3], [101, 0.5]],
        "bids": [[99, 0.2], [98.5, 0.6]],
    }
    res = executable_price(ob, "buy", 0.5)
    assert res.depth_ok
    assert abs(res.avg_price - ((0.3 * 100 + 0.2 * 101) / 0.5)) < 1e-9


def test_executable_price_insufficient_depth():
    ob = {"asks": [[100, 0.1]], "bids": [[99, 0.1]]}
    res = executable_price(ob, "sell", 0.5)
    assert not res.depth_ok
    assert res.filled_base == 0.1
