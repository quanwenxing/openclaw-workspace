# REPORT.md

実装完了日時: 2026-02-08 JST

## 1. 実装内容

- クロス取引所スポット裁定Bot（安全デフォルト）
- transfer / no_transfer の2戦略モード
- コストモデル: 取引手数料、出金手数料、ネットワーク手数料、スリッページ、遅延ペナルティ
- 約定可能性チェック: 板厚、min notional、lot step、残高、stale book
- リスク制御: max position / max daily loss / max open orders / kill-switch / circuit breaker
- バックテスト + レポートCSV出力
- 手数料参照ドキュメントと取得スクリプト

## 2. 実行ログ（必須検証）

### テスト
コマンド:
```bash
source .venv313/bin/activate && pytest
```
結果:
- `3 passed in 0.00s`

### バックテスト
コマンド:
```bash
source .venv313/bin/activate && python scripts/run_backtest.py
```
結果:
- transfer: `trades=5, pnl=162.90, fee_ratio=0.7575`
- no_transfer: `trades=1114, pnl=65933.16, fee_ratio=0.2525`
- 出力: `reports/trades_transfer.csv`, `reports/trades_no_transfer.csv`, `reports/summary.csv`

### ペーパー判定ループ（実板取得）
コマンド:
```bash
source .venv313/bin/activate && python scripts/paper_trade.py --loops 3
```
結果:
- `mode=PAPER symbol=BTC/USD`
- `{'exec': True, 'reason': 'ok', 'net': -25.845}`
- `{'exec': True, 'reason': 'ok', 'net': -25.776}`
- `{'exec': True, 'reason': 'ok', 'net': -25.7404}`

### 手数料スナップショット
コマンド:
```bash
source .venv313/bin/activate && python scripts/fetch_fee_snapshot.py
```
結果:
- `reports/fee_snapshot.json` 生成
- 例: market fallback fees
  - binance BTC/USDT maker/taker: 0.001/0.001
  - kraken BTC/USDT maker/taker: 0.0025/0.004
  - coinbase BTC/USDT maker/taker: 0.006/0.012

## 3. 有効性検証（コスト込み）

- **バックテスト上**は no_transfer が有利（送金コストがないため）。
- transfer は出金・ネットワークコストの影響で成立機会が大幅に減少（5件）。
- **実板サンプル判定**では net がマイナスになり、現行設定では約定可能でも収益化できない局面を確認。

結論:
- 「約定可能性」と「コスト控除後の収益性」は別問題であり、**実運用前に最新手数料＋実測スリッページで再チューニング必須**。
- 特に transfer 型はコスト不利が強く、通常は no_transfer + 在庫再均衡設計の方が現実的。

## 4. 公式ソース

詳細は `docs/research_fees.md` を参照。
主要URL:
- Binance Spot Commission FAQ: https://developers.binance.com/docs/binance-spot-api-docs/faqs/commission_faq
- Kraken Get Trade Volume: https://docs.kraken.com/api/docs/rest-api/get-trade-volume/
- Coinbase Advanced Trade Fees: https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees
- mempool.space fees API: https://mempool.space/docs/api/rest#get-recommended-fees
- Etherscan Gas Tracker API: https://docs.etherscan.io/api-endpoints/gas-tracker
