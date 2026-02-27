# PROD_PLAN.md

## 実装チェックリスト

- [x] 1) Data layer upgrade
  - [x] ws/rest 抽象化を追加
  - [x] REST fallback を実装
  - [x] WS scaffold + reconnect skeleton（TODO明記）
  - [x] `exchange_ts/recv_ts/decision_ts` を評価に反映
  - [x] stale / cross-exchange skew reject
- [x] 2) Execution layer
  - [x] OrderManager 抽象化
  - [x] IOC/FOK/POST_ONLY（paper）
  - [x] partial-fill 取り扱い
  - [x] liveは明示有効化なしで無効
- [x] 3) Inventory & rebalancing
  - [x] 取引所別 base/quote 在庫管理
  - [x] ドリフト判定と再配分推奨（自動送金なし）
- [x] 4) Risk controls
  - [x] max inventory skew
  - [x] max order age
  - [x] volatility spike pause
  - [x] connection health pause
  - [x] kill-switch / circuit breaker 維持
- [x] 5) Validation/testing
  - [x] skew reject テスト
  - [x] stale reject テスト
  - [x] risk guard テスト
  - [x] 既存テストの通過
- [x] 6) Observability
  - [x] JSONL logs（decisions/orders/errors）
  - [x] metrics summary スクリプト
- [x] 7) Config & env
  - [x] production params 追加
  - [x] `.env.example` 追加
- [x] 8) Docs
  - [x] README（日本語）更新
  - [x] 本ファイル作成
- [x] 9) Verification
  - [x] テスト実行
  - [x] 短時間paper simulation 実行
  - [x] `REPORT_PROD.md` 作成

## 現在のギャップ

1. WSは現状 scaffold のみ（本番購読未実装）
2. メトリクス集計は基本指標のみ（高度な時系列分析は未実装）
3. live注文実行の詳細ロジック（API毎の発注/約定照合/リトライ）は未実装
