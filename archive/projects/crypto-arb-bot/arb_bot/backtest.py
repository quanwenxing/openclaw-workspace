from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd

from .engine import evaluate_opportunity
from .risk import RiskState


@dataclass
class BacktestResult:
    summary: dict
    trades: pd.DataFrame


def synthetic_dataset(n: int = 800, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    px = 50000 + np.cumsum(rng.normal(0, 20, n))
    spread_a = np.abs(rng.normal(3, 1.0, n))
    spread_b = np.abs(rng.normal(3.5, 1.2, n))
    edge = rng.normal(0.03, 0.015, n)
    a_bid = px - spread_a / 2
    a_ask = px + spread_a / 2
    b_bid = px * (1 + edge) - spread_b / 2
    b_ask = px * (1 + edge) + spread_b / 2
    depth_a = rng.uniform(0.03, 0.9, n)
    depth_b = rng.uniform(0.03, 0.9, n)
    return pd.DataFrame({
        "ts_ms": 1_700_000_000_000 + t * 500,
        "a_bid": a_bid,
        "a_ask": a_ask,
        "b_bid": b_bid,
        "b_ask": b_ask,
        "depth_a": depth_a,
        "depth_b": depth_b,
    })


def _book(bid: float, ask: float, depth: float) -> dict:
    return {
        "bids": [[bid, depth], [bid * 0.9998, depth * 1.2]],
        "asks": [[ask, depth], [ask * 1.0002, depth * 1.2]],
    }


def run_backtest(cfg: dict, df: pd.DataFrame, transfer_mode: bool) -> BacktestResult:
    amount_base = cfg["market"]["trade_size_base"]
    state = RiskState()
    balance_buy_quote = cfg["sim"]["initial_quote_buy_ex"]
    balance_sell_base = cfg["sim"]["initial_base_sell_ex"]

    rows = []
    for r in df.itertuples(index=False):
        buy_book = _book(r.a_bid, r.a_ask, r.depth_a)
        sell_book = _book(r.b_bid, r.b_ask, r.depth_b)
        res = evaluate_opportunity(
            cfg=cfg,
            buy_book=buy_book,
            sell_book=sell_book,
            amount_base=amount_base,
            buy_balance_quote=balance_buy_quote,
            sell_balance_base=balance_sell_base,
            state=state,
            transfer_mode=transfer_mode,
            ts_ms=int(r.ts_ms),
            now_ms=int(r.ts_ms),
        )
        traded = res.executable and res.net_edge_quote > 0
        pnl = res.net_edge_quote if traded else 0.0

        if traded:
            state.daily_pnl += pnl
            if transfer_mode:
                state.open_orders = min(state.open_orders + 1, cfg["risk"]["max_open_orders"])
                balance_sell_base -= amount_base
            else:
                # rebalancing assumed internal using pre-funded inventories
                pass
        rows.append({
            "ts_ms": r.ts_ms,
            "executable": res.executable,
            "reason": res.reason,
            "gross": res.gross_edge_quote,
            "cost": res.total_cost_quote,
            "net": res.net_edge_quote,
            "traded": traded,
            "pnl": pnl,
        })

    trades = pd.DataFrame(rows)
    rets = trades["pnl"].values
    turnover = float(trades.loc[trades["traded"], "gross"].abs().sum())
    fee_ratio = float(trades["cost"].sum() / (turnover + 1e-9)) if turnover > 0 else 0.0
    eq = trades["pnl"].cumsum()
    dd = eq - eq.cummax()
    sharpe = float(np.mean(rets) / (np.std(rets) + 1e-12) * np.sqrt(365 * 24 * 60))

    summary = {
        "mode": "transfer" if transfer_mode else "no_transfer",
        "trades": int(trades["traded"].sum()),
        "hit_rate": float((trades.loc[trades["traded"], "pnl"] > 0).mean() if trades["traded"].any() else 0.0),
        "pnl": float(trades["pnl"].sum()),
        "avg_edge": float(trades.loc[trades["traded"], "net"].mean() if trades["traded"].any() else 0.0),
        "max_drawdown": float(dd.min()),
        "turnover": turnover,
        "fee_ratio": fee_ratio,
        "sharpe": sharpe,
    }
    return BacktestResult(summary=summary, trades=trades)


def save_report(result: BacktestResult, out_csv: str | Path) -> None:
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    result.trades.to_csv(out_csv, index=False)
