# REPORT_PROD.md

## 実施日時
- 2026-02-08 (JST)

## 実行コマンドと実出力

### 1) テスト

コマンド:
```bash
python3 -m pytest
```

出力:
```text
.........                                                                [100%]
9 passed in 0.01s
```

### 2) 短時間ペーパーシミュレーション

コマンド:
```bash
PYTHONPATH=. python3 scripts/paper_trade.py --loops 2
```

出力:
```text
mode=PAPER symbol=BTC/USD
{'exec': False, 'reason': 'max-inventory-skew', 'net': 0.0, 'rebalance': 'recommend: shift 1.000000 base from sell_ex to buy_ex (paper-only, no auto-transfer)'}
{'exec': False, 'reason': 'max-inventory-skew', 'net': 0.0, 'rebalance': 'recommend: shift 1.000000 base from sell_ex to buy_ex (paper-only, no auto-transfer)'}
```

### 3) メトリクス要約

コマンド:
```bash
PYTHONPATH=. python3 scripts/metrics_summary.py
```

出力:
```text
metrics_summary
decisions=8
rejects=8
reject_ratio=1.0000
fill_ratio=0.0000
pnl_estimate=0.000000
latency_note=decision_ts-recv_ts logged per entry; aggregate latency TODO
```

## 変更サマリ

- Data layer: `arb_bot/market_data.py` 追加（ws/rest abstraction + REST fallback + WS scaffold）
- Execution: `arb_bot/order_manager.py` 追加（IOC/FOK/POST_ONLY, partial対応）
- Inventory: `arb_bot/inventory.py` 追加（在庫偏りと再配分推奨）
- Risk: `arb_bot/risk.py` 拡張（inventory/order age/volatility/connection health）
- Engine: `arb_bot/engine.py` 拡張（timestamp skew / stale reject）
- Observability: `arb_bot/observability.py` + `reports/logs/*.jsonl`
- Metrics: `scripts/metrics_summary.py`
- Config/env: `config/default.yaml` 更新 + `.env.example` 追加
- Docs: `README.md` 更新 + `PROD_PLAN.md`
- Tests: `tests/test_production_guards.py` 追加

## 既知の制限 / ギャップ

1. WSは scaffold 段階（実購読未実装）
2. live注文執行は安全上デフォルト無効、詳細実装未完
3. latency集計は JSONL 記録済みだが、高度な統計は TODO
