# 実装タスク分解（Day1〜Day3）

作成: 2026-02-18 13:23:51 JST
対象設計: `markets/x-grok-daily-collector-design.md` v1.3

---

## Day1: 収集MVP（X API → 保存）

### 目的
日次実行の先頭でXリスト同期を行い、その結果を使って24h投稿を取得し、run/state/log を更新できる状態にする。

### タスク
1. プロジェクト雛形作成
   - `markets/scripts/collector/` 作成
   - `collect_x_posts.py`（または同等）作成
2. 設定読込
   - `markets/config/sources.yaml` を読込
3. X API取得実装
   - 対象: `@Polymarket @Kalshi @opinionlabsxyz`
   - 方式: account別 `since_id` 増分
   - 失敗時: 3回リトライ（指数バックオフ）
4. 生データ保存
   - `markets/runs/YYYY-MM-DD.json` に raw_posts セクション追加
5. 状態更新
   - `markets/state/collector-state.json` の since_id 更新
6. ログ出力
   - `markets/logs/YYYY-MM-DD.log`

### 完了条件
- 手動実行で投稿がJSON保存される
- since_id が更新される
- 失敗時リトライが動作する

---

## Day2: 解析/分類/統合（Grok + 台帳反映）

### 目的
収集データを台帳へ自動反映し、ノイズ除去・分類ブレ補正まで動かす。

### タスク
1. Analyzer実装（Grok API）
   - 出力: `summary_ja, category, tags, importance, watch_targets`
   - JSON schema検証 + 失敗時再試行1回
2. Normalizer実装
   - 重複排除: `post_id -> canonical_url -> normalized_text_hash`
   - 市場判定: アカウント優先 / キーワード / multi-market / other-market
3. ノイズ除去実装
   - 除外/低優先/採用条件を反映
4. ルールベース再判定実装
   - watchlist/dev-tools/ideas上書きルール
5. Writer実装
   - `markets/<market>/*.md` にID採番追記
   - `source_type=auto_x_grok`

### 完了条件
- 1回実行で各市場台帳に追記される
- 重複登録が発生しない
- needs_review運用が効く

---

## Day3: 手動統合・戦略候補・通知・cron

### 目的
日次運用に必要な通知と定期実行を完成させる。

### タスク
1. 手動投稿取り込み
   - 条件: このチャネルの `#インサイト分析` 投稿のみ
   - `source_type=manual_discord`, tag=`インサイト分析`
   - メッセージ編集時は差分更新
2. Strategizer実装
   - `STRAT-xxxx` 候補生成
   - reviewing昇格5要件チェック
3. 日次通知生成
   - 詳細版テンプレ固定
   - `new最大3件 + reviewing以上全件`
4. 縮退運転実装
   - X失敗時30分後1回再実行
   - 0件取得の正常/異常区別
5. cron登録
   - 毎日18:00 JST
   - 失敗通知/成功通知をこのチャネルへ
6. ドライラン
   - 連続2回実行で重複なし確認

### 完了条件
- 18:00定期ジョブが実行される
- 日次詳細通知が届く
- 戦略候補が生成される

---

## 運用開始後（初週）

- 7日連続稼働確認
- KPI計測開始:
  - Precision@Top3
  - Noise Rate
  - Duplicate Escape Rate
  - Strategy Conversion Rate
  - Coverage
- 1週間後にユーザーと週間振り返り（KPI見直し）
