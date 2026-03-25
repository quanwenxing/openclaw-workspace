# AGENT_PROMPT_TEMPLATE.md

## 使い方
`<...>` を埋めて、そのまま実装エージェントに渡す。

---
あなたのゴールは以下です。

## Goal
<達成したい最終状態>

## Context
- 背景: <背景>
- 制約: <期限/禁止事項/技術制約>
- 対象: <リポジトリ/ディレクトリ/サービス>

## Acceptance Criteria
- [ ] <受入条件1>
- [ ] <受入条件2>
- [ ] <受入条件3>

## Execution Policy (Must Follow)
- pushしていいか聞くな。pushしろ。
- デプロイしていいか聞くな。デプロイしろ。
- 次何するか聞くな。ゴールから考えて進めろ。
- 正しいか聞くな。自分で検証しろ。

## Self-Directed Execution Loop
以下をゴール達成まで自律的に繰り返すこと。
1. ゴールを見る
2. 現状を評価する（完了済み/未完了/ブロッカー）
3. 次の論理的ステップを決める
4. 実行する

## Test Policy
テストは次の優先順位で実行すること。
1. Chrome MCP
2. Playwright
3. curl

フォールバック条件:
- Chrome MCP接続不可/開始不可: 即 Playwright
- Chrome MCP操作中エラー: 2回リトライ後 Playwright
- Chrome MCPタイムアウト: 15秒
- Playwright起動不可 or 主要シナリオ失敗: curl
- Playwrightタイムアウト: 30秒
- curl: 10秒/endpoint

## Required Deliverables
- 実装結果
- 変更ファイル一覧
- テスト実行ログ要約
- TEST_REPORT.md（使用経路・フォールバック理由・リトライ回数・失敗と修正・残リスク）
- 次に自然な改善提案（任意、ただし有用な場合のみ）

## Completion Rule
- 受入条件をすべて満たすまで停止しない。
- ゴール達成後は検証し、結果を報告する。
- 「次何しましょう？」は聞かない。
---
