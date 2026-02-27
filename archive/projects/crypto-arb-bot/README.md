# crypto-arb-bot

安全側（デフォルトは **paper mode**）を維持したまま、プロトタイプから本番運用準備向けに拡張した CEX 裁定ボットです。

## 現在の実装ステータス（重要）

- ✅ RESTポーリングでの堅牢な板取得
- ✅ WebSocket対応の抽象化レイヤー（**scaffold**）
- ⚠️ WS実装は骨組みのみ（`WsMarketDataClient` は TODO / reconnect skeleton まで）
- ✅ ライブ実行はデフォルト無効（`runtime.live_enabled: false`）

## プロダクション向けアーキテクチャ（現実装）

- **Data Layer**
  - `arb_bot/market_data.py`
  - モード: `ws` / `rest`（現時点では安全に `rest` fallback 利用）
  - タイムスタンプ追跡: `exchange_ts`, `recv_ts`, `decision_ts`
  - `max_cross_exchange_skew_ms` と `stale_book_ms` で同期性・鮮度をチェック
- **Execution Layer**
  - `arb_bot/order_manager.py`
  - ペーパー注文タイプ: `IOC`, `FOK`, `POST_ONLY`
  - 部分約定（partial）を扱う
- **Inventory / Rebalancing**
  - `arb_bot/inventory.py`
  - 取引所ごとの `base/quote` 在庫を管理
  - 自動送金なし、**推奨のみ**（paper-only recommendation）
- **Risk Controls**
  - `arb_bot/risk.py`
  - kill-switch / circuit breaker 維持
  - 追加: 在庫偏り・注文滞留時間・ボラ急騰・接続健全性pause
- **Observability**
  - `reports/logs/*.jsonl`（decisions / orders / errors）
  - `scripts/metrics_summary.py` で reject率・fill率・PnL簡易集計

## セットアップ

```bash
cd crypto-arb-bot
python3 -m pip install -r requirements.txt || true
python3 -m pip install pyyaml ccxt numpy pandas pytest
```

### 環境変数

`.env.example` を参考に、必要なキーを設定してください。

```bash
cp .env.example .env
# 値を編集
```

例:

```dotenv
KRAKEN_API_KEY=your_kraken_api_key
KRAKEN_API_SECRET=your_kraken_api_secret
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_API_SECRET=your_coinbase_api_secret
```

`config/default.yaml` では `${...}` 形式で参照します（未設定でも paper 実行は可能）。

## 実行

### テスト

```bash
python3 -m pytest
```

### 短時間ペーパーシミュレーション

```bash
PYTHONPATH=. python3 scripts/paper_trade.py --loops 2
```

### メトリクス要約

```bash
PYTHONPATH=. python3 scripts/metrics_summary.py
```

## 安全なロールアウト手順（推奨）

1. **Phase 0: Unit tests + paper固定**
   - リスクガード・鮮度・skewテストを安定化
2. **Phase 1: 長時間paper運転**
   - JSONLログの監視、reject理由の分布確認
3. **Phase 2: 小サイズ / 監視付きlive準備**
   - ただし `live_enabled=true` を明示的に切り替えるまで実行不可
4. **Phase 3: 段階的拡大**
   - 取引サイズ・対象銘柄を徐々に増やす

## 既知の制限

- WSは抽象化のみで、実データ購読は未実装（reconnect骨組みあり）
- メトリクスは簡易集計（詳細なレイテンシ統計は今後拡張）
