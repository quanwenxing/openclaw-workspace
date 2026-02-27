# 設計書 v1.3: X API + Grok API 日次情報収集基盤（予測市場向け）

- 更新日: 2026-02-18 JST
- 対象: #poly-arb の情報収集・蓄積運用
- 目的: X投稿と手動共有情報を統合管理し、予測市場の収益化/開発に有用な知見を日次で蓄積する

---

## 1. 背景と目的

課題:
- 手動確認のため取りこぼしが発生
- 取得失敗時の再試行が手作業
- 分類品質にばらつき
- 手動投稿と自動収集の台帳連携が未定義

本設計は、**X APIで収集**、**Grok APIで要約/分類**、**手動投稿と同一台帳へ統合**を実現する。

---

## 2. スコープ

### 2.1 In Scope
- 監視対象Xアカウントの新規投稿取得（過去24h）
- Grok APIによる要約・分類・タグ付け
- 手動投稿（Discord共有）との統合管理
- 重複排除して市場別台帳に追記
- 日次サマリー通知（このチャネル）
- 実行ログ/結果JSON保存

### 2.2 Out of Scope
- 自動売買執行
- Xへの自動返信・投稿
- 秒単位リアルタイム監視

---

## 3. 決定済み前提

- 監視対象（初期）:
  - `@Polymarket`
  - `@Kalshi`
  - `@opinionlabsxyz`
- 実行時刻: 毎日 18:00 JST（仮置き）
- 通知先: このDiscordチャネル固定
- 通知粒度: 当日更新分サマリー
- 対象市場: Polymarket / Kalshi / Opinion
- 統合方針: `source_type` で手動/自動を識別して同一台帳に保存

---

## 4. 成果物（出力）

### 4.1 市場別台帳（市場ごとに同型）
- `markets/polymarket/ideas.md`
- `markets/polymarket/watchlist.md`
- `markets/polymarket/dev-tools.md`
- `markets/polymarket/other.md`
- `markets/polymarket/index.md`
- `markets/kalshi/ideas.md`
- `markets/kalshi/watchlist.md`
- `markets/kalshi/dev-tools.md`
- `markets/kalshi/other.md`
- `markets/kalshi/index.md`
- `markets/opinion/ideas.md`
- `markets/opinion/watchlist.md`
- `markets/opinion/dev-tools.md`
- `markets/opinion/other.md`
- `markets/opinion/index.md`
- `markets/multi-market/ideas.md`
- `markets/multi-market/watchlist.md`
- `markets/multi-market/dev-tools.md`
- `markets/multi-market/other.md`
- `markets/multi-market/index.md`
- `markets/other-market/ideas.md`
- `markets/other-market/watchlist.md`
- `markets/other-market/dev-tools.md`
- `markets/other-market/other.md`
- `markets/other-market/index.md`

### 4.2 実行管理
- `markets/runs/YYYY-MM-DD.json`
- `markets/logs/YYYY-MM-DD.log`
- `markets/state/collector-state.json`

### 4.3 戦略候補管理
- `markets/strategy-candidates/index.md`
- `markets/strategy-candidates/candidates.md`
- 収集情報から戦略化可能なトピックを `STRAT-xxxx` で管理

---

## 5. システム構成（論理）

1) Scheduler（OpenClaw cron）
2) ListSync（X Listメンバー同期）
3) Collector（X API取得）
4) Analyzer（Grok API要約/分類）
5) Ingestor（手動投稿取り込み）
6) Normalizer（市場判定/整形/重複排除）
7) Writer（台帳反映）
8) Reporter（日次サマリー通知）
9) Strategizer（戦略候補抽出・登録）

---

## 6. データフロー

1. cron が毎日18:00 JSTに起動
2. **ListSync** が最初に対象Xリストの更新有無を確認
3. リスト更新があれば監視対象（sources）をアップデート
4. Collector が更新後の対象アカウントから過去24h投稿を取得
5. Analyzer が投稿ごとに JSON（要約/分類/タグ）を生成
6. Ingestor が当日手動投稿分（Discord共有）を同スキーマ化
7. Normalizer が重複排除・市場振り分け
8. Writer がカテゴリ別にID採番して追記
9. Strategizer が戦略化可能トピックを抽出し `strategy-candidates` に登録
10. Reporter が当日追加分サマリーと戦略候補を通知

---

## 7. データ設計

### 7.1 設定ファイル
`markets/config/sources.yaml`

```yaml
accounts:
  - handle: Polymarket
    market: polymarket
  - handle: Kalshi
    market: kalshi
  - handle: opinionlabsxyz
    market: opinion

schedule:
  timezone: Asia/Tokyo
  daily_time: "18:00"

notification:
  channel: discord
  target: "#poly-arb"
  mode: daily_summary

lookback_hours: 24
```

### 7.2 実行状態（肥大化対策）
`markets/state/collector-state.json`

```json
{
  "last_run_at": "2026-02-18T18:00:00+09:00",
  "accounts": {
    "Polymarket": {"since_id": "0"},
    "Kalshi": {"since_id": "0"},
    "opinionlabsxyz": {"since_id": "0"}
  },
  "last_success": true
}
```

### 7.3 共通エントリ項目
- ID
- Title
- Summary
- Source
- Source Type (`manual_discord` | `auto_x_grok`)
- Tags
- Created At
- Event Time
- Updated

---

## 8. API連携設計

### 8.1 X API（収集）
- 取得項目: post_id, text, created_at, url, author_handle
- 方式: アカウント別 `since_id` 増分取得
- 制御: レート制御・ページネーション・最大3回リトライ

### 8.2 X List同期（事前更新）
- 対象: owner `@0xmonchan` / list_id `2011089054822187262`
- タイミング: 日次収集処理の**先頭**
- 手順:
  1. listメンバー取得
  2. 前回メンバーとの差分算出（追加/削除）
  3. `markets/config/sources.yaml` の監視対象に反映
- 反映ルール:
  - 追加メンバーは監視対象へ追加
  - 削除メンバーは監視対象から除外（履歴はrunログに保持）
- 失敗時: `list_sync_failed` として通知に明記し、前回監視対象で収集を継続

### 8.3 Grok API（解析）
- 目的: 要約/分類/タグ化
- 入力: `text + created_at + author + url`
- 出力（JSON固定）:
  - `summary_ja`
  - `category` (`ideas|watchlist|dev-tools|other`)
  - `tags[]`
  - `importance` (`high|medium|low`)
  - `watch_targets[]`（任意）
- 制御:
  - スキーマ検証失敗時は再試行1回
  - 失敗時は `other` + `needs_review=true`

---

## 9. 重複排除

キー優先順:
1. `post_id`
2. `canonical_url`
3. `normalized_text_hash`（空白/URL正規化後）

重複時:
- 新規追加しない
- 必要なら `Updated` のみ更新

---

## 10. 市場判定ロジック（確定）

判定優先順:
1. **アカウント起点判定**（公式アカウント等）
   - `@Polymarket` → `polymarket`
   - `@Kalshi` → `kalshi`
   - `@opinionlabsxyz` → `opinion`
2. **本文キーワード判定**（市場名の明示）
   - 例: `polymarket`, `kalshi`, `opinion`
3. 本文に**複数市場名**がある場合
   - 特定市場に振り分けず `multi-market` フォルダに保存
4. 本文から市場名を特定できない場合
   - `other-market` フォルダに保存

補足:
- アカウント判定できる場合はそれを優先する
- キーワード判定はアカウント不明/非公式ソース時に適用

---

## 11. カテゴリ分類ロジック

- `ideas`: 収益機会・戦略仮説
- `watchlist`: 人物/ウォレット/組織の監視価値
- `dev-tools`: bot開発/データ基盤/自動化手法
- `other`: 上記外

競合時優先順位:
`watchlist > dev-tools > ideas > other`

### 11.1 ルールベース再判定（分類ブレ対策）
Grok分類の後段で、以下の再判定を適用する。

- `0x...` アドレス / ENS / wallet文脈を検出 → `watchlist` 優先
- `API`, `SDK`, `bot`, `websocket`, `executor`, `pipeline` 等の開発語彙を検出 → `dev-tools` 優先
- `edge`, `mispricing`, `arb`, `entry`, `exit`, `odds` 等の戦略語彙を検出 → `ideas` 優先
- 短文・語彙不足・根拠なし等で信頼度が低い場合 → `other + needs_review=true`

### 11.2 ノイズ除去ルール（確定）
- 除外（台帳に入れない）:
  - giveaway / 紹介コード / 露骨な広告のみ
  - 同文テンプレ連投
  - 市場・手法・根拠の3要素がすべて欠落
- 低優先（保存はするが通知非掲載）:
  - 感想のみ
  - 価格実況のみ（戦略条件なし）
  - 追加情報のない単純リポスト
- 採用条件（ideas/dev-tools）:
  - 条件・数値・手順・ツール名のいずれかがある
  - 根拠リンクまたは観測対象がある

---

## 12. 手動投稿（Discord）統合仕様

- 取り込み対象は、このチャネルでの**`#インサイト分析` タグ付き投稿**のみ
- `#インサイト分析` の位置は本文先頭/末尾どちらでも可
- 手動投稿も同一スキーマに変換し台帳反映
- `source_type=manual_discord` を必須付与
- `tags` に `インサイト分析` を必須付与
- 既存自動投稿と重複判定を実施
- 同一メッセージの編集時は、既存エントリを更新（`Updated` 更新 + 差分反映）
- 添付画像のOCRは現時点で対象外（本文のみ取り込み）
- 手動投稿は必要に応じて優先レビュー対象に設定

---

## 13. エラー処理（縮退運転を含む）

- X API失敗: 3回リトライ（指数バックオフ）
- Grok API失敗: 暫定保存 + `needs_review`
- 全体失敗: 当チャネルに失敗通知 + ログ保存

### 13.1 縮退運転ルール（確定）
1. X API失敗時:
   - 当日ジョブで30分後に1回だけ自動再実行
   - 通知に「X取得失敗/再試行結果」を明記
2. X API成功・Grok失敗時:
   - 原文を保存
   - `category=other`, `needs_review=true` で仮登録
   - 翌日ジョブで再解析
3. 両系統失敗時:
   - 即時失敗通知
   - `run_status=failed` を保存
4. 0件取得時:
   - 正常0件（当日投稿なし）と異常0件（API障害疑い）を明示
5. 自動再実行上限:
   - 当日最大1回（無限リトライ禁止）

---

## 14. コスト/性能ガードレール

- 1実行あたり解析対象上限（例: 200投稿）
- Grok API日次トークン上限を設定
- 上限到達時は「未処理件数」をサマリー通知

### 14.1 品質KPI（運用開始指標）
- Precision@Top3
- Noise Rate
- Duplicate Escape Rate
- Strategy Conversion Rate
- Coverage（日次収集カバレッジ）

### 14.2 KPI見直し運用
- KPIは固定値ではなく、運用しながら定期見直しする
- **1週間ごとにユーザー（もんちゃん）と週間振り返り**を実施
- 振り返り結果でしきい値・定義・通知内容を更新する

---

## 15. 日次通知フォーマット（詳細版・確定）

```
[Daily Market Intel] YYYY-MM-DD (JST 18:00実行)
対象期間: YYYY-MM-DD 18:00 - YYYY-MM-DD 17:59 JST

取得投稿数: N
新規登録: N（manual_discord: x / auto_x_grok: y）
重複除外: N
失敗件数: N（X API: n / Grok: m）

市場別追加件数:
- polymarket: N
- kalshi: N
- opinion: N
- multi-market: N
- other-market: N

カテゴリ別追加件数:
- ideas: N
- watchlist: N
- dev-tools: N
- other: N

重要トピック TOP3:
1) [category] title / source
2) ...
3) ...

戦略候補（strategy-candidatesに登録推奨）:
- new: 最大3件まで掲載
- reviewing以上: 全件掲載
- STRAT候補タイトルA（根拠ID: IDEA-xxxx, TOOL-xxxx）
- STRAT候補タイトルB（根拠ID: ...）

運用メモ:
- needs_review: N
- 未処理件数: N
```

## 16. 戦略候補抽出ルール（追加）

`Strategizer` は当日追加データから、以下条件で `STRAT-xxxx` 候補を作成する。

作成条件（いずれか）:
- `ideas` に再現可能なエントリー/エグジット条件が含まれる
- `dev-tools` と `ideas` の組み合わせで自動化可能性が高い
- 同一テーマの根拠投稿が2件以上あり、実行仮説が立てられる

必須項目:
- Hypothesis
- Entry Signal / Exit Signal
- Risk
- Required Data/Tools
- Derived From IDs

`reviewing` 昇格条件（5要件）:
1. Hypothesisが明確
2. Entry / Exitが機械判定可能
3. リスク（最大損失または失敗条件）が明示
4. 必要データ/ツールが取得可能
5. 根拠IDが最低1件存在

除外条件:
- 根拠リンクがない
- 宣伝のみで検証可能性がない

## 17. スケジューリング

### 17.1 実行頻度
- 1日1回（18:00 JST）

### 17.2 OpenClaw cron
- `sessionTarget: isolated`
- `payload.kind: agentTurn`
- 処理: 収集→解析→台帳反映→サマリー通知

---

## 18. 受け入れ基準

- [ ] 7日連続で日次実行成功
- [ ] 同一投稿の重複登録率 0%
- [ ] 手動投稿/自動投稿が同一台帳で検索可能
- [ ] 失敗通知がこのチャネルに到達

---

## 19. 導入ステップ

1. APIキー設定（X/Grok）
2. `markets/config/sources.yaml` 確定（市場横断の単一設定）
3. 収集MVP実装（X取得→JSON保存）
4. 解析/分類実装（Grok→台帳反映）
5. 手動投稿統合ロジック追加
6. cron登録（18:00 JST）
7. 1週間試験運用

---

## 20. 拡張（Phase 2以降）

- Discovery（24hテーマ抽出: monetization_idea / bot_dev）を追加
- 市場横断インデックス（`markets/index.md`）追加
- 重要度スコアのチューニング
