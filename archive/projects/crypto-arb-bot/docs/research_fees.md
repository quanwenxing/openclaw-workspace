# 手数料・ネットワークコスト調査メモ（公式ソース）

最終更新: 2026-02-08 (JST)

このプロジェクトでは、**固定値を盲信せず、設定ファイルで明示して毎回見直す**方針です。実運用前に必ず最新値を再取得してください。

## 1) 取引手数料（公式情報）

- Binance Spot API Commission FAQ（公式開発者ドキュメント）
  - https://developers.binance.com/docs/binance-spot-api-docs/faqs/commission_faq
  - 注: `/api/v3/account/commission` 等でアカウント別レート確認が可能と記載。

- Kraken REST API: Get Trade Volume（公式APIドキュメント）
  - https://docs.kraken.com/api/docs/rest-api/get-trade-volume/
  - 注: 30日取引高に応じた fee schedule を返すと明記。

- Coinbase Advanced Trade Fees（公式ヘルプ）
  - https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees

## 2) 出金/ネットワーク手数料 参照先

- Binance 資産情報 API（公式、ネットワーク/出金情報系）
  - https://developers.binance.com/docs/wallet/capital

- Kraken 資金系 API（出金可否/メソッド関連）
  - https://docs.kraken.com/api/docs/rest-api/get-withdrawal-methods/
  - https://docs.kraken.com/api/docs/rest-api/get-withdrawal-information/

- Bitcoin 推奨手数料（mempool.space API）
  - https://mempool.space/docs/api/rest#get-recommended-fees

- Ethereum Gas Tracker（Etherscan API Docs）
  - https://docs.etherscan.io/api-endpoints/gas-tracker

## 3) 実装での扱い

- 実際のバックテストでは `config/default.yaml` に明示された値を使用。
- `scripts/fetch_fee_snapshot.py` で ccxt 経由の取得スナップショットを保存 (`reports/fee_snapshot.json`)。
- 取得不可な場合は API 制限/認証要件の可能性があるため、公式画面/APIで再確認して値を更新する。

## 4) 注意

- 手数料はティア、プロモーション、通貨、チェーン、時刻で変化。
- 転送型アービトラージは、出金＋ネットワーク＋待ち時間の不確実性で期待値が崩れやすい。
- 無転送型（両取引所に事前在庫）でも、在庫偏りと再均衡コストが必要。
