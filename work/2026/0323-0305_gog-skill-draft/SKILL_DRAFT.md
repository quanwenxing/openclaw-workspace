# gog (gogcli) スキル定義案（下書き）

このスキルは、AIエージェントが `gog` (gogcli) を通じて Google Workspace (Gmail, Calendar, Drive, etc.) を正確かつ安全に操作するための定義です。

## スキル名
`gog-workspace-agent`

## 目的
ターミナルから Google サービスのデータを取得・加工・連携し、ユーザーの生産性を向上させる。

## コマンド構成 (引数の定義)

### 1. Gmail
*   `gog gmail search "query" --limit 10 --json`: 指定条件でメールを検索しJSONで出力。
*   `gog gmail send --to "address" --subject "subject" --body-file -`: 標準入力からメールを送信。

### 2. Calendar
*   `gog calendar events --today --json`: 本日の予定をリストアップ。
*   `gog calendar events --start "YYYY-MM-DD" --end "YYYY-MM-DD" --json`: 期間指定でカレンダーを取得。
*   `gog calendar create --summary "Title" --start "Time" --duration 1h`: 予定を新規作成。

### 3. Drive / Sheets
*   `gog drive search "name contains 'query'" --json`: ファイルを検索。
*   `gog drive download <fileId>`: ファイルを取得。
*   `gog sheets read <spreadsheetId> <range> --json`: シートを読み取る。

## 安全性ガイドライン (AIへの指示)

1.  **破壊的操作の禁止:** `delete` や `clear` などのコマンド、および `update` による大幅な書き換えを行う際は、必ず実行前に具体的な内容をユーザーに提示し、承認（AskUserQuestion / Approve）を得ること。
2.  **大量送信の警告:** 一度に 5 件以上の宛先へメールを送信する場合、または 20 件以上のタスクを一括操作する場合は、ユーザーに確認を求める。
3.  **JSONパース:** AIは常に `--json` オプションを使用し、結果をパースして次のアクションを決定すること。表形式の出力を読み取ることは避ける。
4.  **プライバシー:** 取得した個人情報（メールアドレスや住所など）を、不必要に外部に送信したり、コンテキスト外で利用しない。

## 使用例 (Prompt Examples)

*   「今日のカレンダーの空き枠を調べて、TODOリストの優先タスクを埋めておいて」
*   「最新の請求書メールから情報を抜き取って、スプレッドシートの集計表に追記して」
*   「来週の予定を要約して、Slackに送る下書きを作って」
