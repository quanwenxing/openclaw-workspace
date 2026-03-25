---
name: investment-idea-capture
description: 投資・投機ネタの継続蓄積と棚卸し判定を行う。ユーザーが「蓄積して」「ネタとして残して」「棚卸しして」「使えない案を整理して」などを依頼したときに使う。入力が雑でも構造化して `memory/investment_ideas.jsonl` に追記し、評価時は `memory/investment_reviews.jsonl` に判定ログを残す。
---

# Investment Idea Capture

目的: 不定期・粒度バラバラの投資ネタを、後で定量評価できる形で保存する。

## 保存先
- ネタ本体: `memory/investment_ideas.jsonl`
- 棚卸しログ: `memory/investment_reviews.jsonl`

## 実行ルール（蓄積）
1. 入力から以下の必須項目を埋める（不足は `unknowns` に回す）。
   - `idea_id`（`idea-YYYYMMDD-XXX`）
   - `captured_at`
   - `source_type`
   - `source_title`
   - `source_url`（なければ null）
   - `hypothesis`
   - `markets`（配列）
   - `time_horizon`
   - `quant_assessment`
   - `status`（初期値 `inbox`）
   - `next_actions`（最低1件）
2. 外部ソースがある場合は `web_fetch` / `web_search` で最低限の補足確認を行い、出典URLを保存する。
3. 1レコードをJSONLで `memory/investment_ideas.jsonl` に追記する。
4. 返信では `idea_id`・暫定スコア・次アクションを短く返す。

## 暫定スコア（0-100）
最低5軸を含める。
- `feasibility`
- `data_availability`
- `testability`
- `evidence_strength`
- リスク軸（`crowding_risk` か `volatility_risk` など）
- `overall`（初期は単純平均でよい）

## 棚卸しルール
- 判定: `keep` / `refine` / `archive` / `drop`
- `drop` 時は理由と「再開条件」を必ず残す。
- 棚卸し結果は `memory/investment_reviews.jsonl` に1行追記する。

## 禁止事項
- 推測を事実として書かない。
- 出典なしで断定しない。
- 元データURLを消さない。

## 返信テンプレ（簡潔）
- `idea_id`
- 判定（例: inbox / keep）
- 暫定スコア（overall）
- 次アクション（1〜3件）

必要なら詳細仕様は `references/schema.md` を読む。
