# 投資ネタ蓄積システム v1（先に蓄積を回す版）

## 1. 目的
- 不定期に投げられる投資/投機ネタを、粒度がバラバラでも取りこぼさず保存する。
- 後で棚卸し・定量評価できるように、最低限の構造化を強制する。

## 2. データ保存先
- ネタ本体: `memory/investment_ideas.jsonl`
- 棚卸し履歴: `memory/investment_reviews.jsonl`（未作成なら初回棚卸し時に作成）

## 3. ネタ1件の標準レコード（JSONL）
必須項目:
- `idea_id` 例: `idea-20260301-004`
- `captured_at` ISO日時
- `source_type` (`user_thesis` / `article` / `official_release` / `social` / `other`)
- `source_title`
- `source_url`（なければ null）
- `hypothesis`（一文で仮説）
- `markets`（配列）
- `time_horizon`（短期/中期/長期/任意表現）
- `quant_assessment`（下記5軸+overall）
- `status`（`inbox`/`testing`/`keep`/`archive`/`drop`）
- `next_actions`（配列）

任意項目:
- `candidate_strategies` / `unknowns` / `constraints` / `notes`

## 4. 暫定スコアリング（0-100）
- `feasibility`: 実装可能性
- `data_availability`: データ取得容易性
- `testability`: 検証容易性
- `evidence_strength`: 根拠の強さ
- `risk_penalty` またはカテゴリ別リスク（例: crowding/volatility）
- `overall`: 総合（単純平均で開始。後で重み付けへ移行）

## 5. 運用フロー（v1）
1) ユーザー入力受領
2) 必須項目が欠ける場合は最小補完（不足は `unknowns` へ）
3) JSONL 1行で `investment_ideas.jsonl` に追記
4) 返信で `idea_id` / 暫定スコア / 次アクションを返す

## 6. 棚卸し（v1）
- 頻度: 隔週（後でcron化）
- 判定: `keep` / `refine` / `archive` / `drop`
- 判定理由を `investment_reviews.jsonl` に記録

## 7. 重要ルール
- 推測で事実断定しない。出典付きで保管。
- 生データ/外部情報は原文URLを保存。
- 捨てる判断（drop）は、理由と再開条件を残す。
