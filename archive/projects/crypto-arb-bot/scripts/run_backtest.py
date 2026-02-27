#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import yaml
import pandas as pd

from arb_bot.backtest import synthetic_dataset, run_backtest, save_report

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    cfg = yaml.safe_load((ROOT / "config" / "default.yaml").read_text())
    data_path = ROOT / "data" / "sample_history.csv"
    df = synthetic_dataset(1200)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_path, index=False)

    transfer = run_backtest(cfg, df, transfer_mode=True)
    no_transfer = run_backtest(cfg, df, transfer_mode=False)

    save_report(transfer, ROOT / "reports" / "trades_transfer.csv")
    save_report(no_transfer, ROOT / "reports" / "trades_no_transfer.csv")
    pd.DataFrame([transfer.summary, no_transfer.summary]).to_csv(ROOT / "reports" / "summary.csv", index=False)

    print("=== Backtest Summary ===")
    for s in [transfer.summary, no_transfer.summary]:
        print(s)


if __name__ == "__main__":
    main()
