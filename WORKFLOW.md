# WORKFLOW.md

## 目的
workspace直下の散乱を防ぎ、成果物を再利用しやすくする。

## 基本ルール
1. 新規作業は必ず `tmp/sessions/YYYY-MM-DD_<topic>/` で開始する。
2. 完了時に成果物だけを以下へ昇格する。
   - 開発成果: `projects/`
   - 調査/要約: `research/`
   - 参照資料: `docs/`
3. 中間生成物・旧版は `archive/` へ退避（即削除しない）。
4. 運用設定ファイルは `docs/ops/` に置く（例: `docs/ops/sources.yaml`）。
5. `workspace/` ルート直下には原則ファイルを新規作成しない。

## セッション開始
- `scripts/new-session.sh <topic>` を使う。

## セッション終了
- 成果物を昇格し、残りを `archive/` または削除。
- `scripts/close-session.sh <session-dir>` を使う。

## 命名規則
- セッション: `YYYY-MM-DD_<topic>`
- topicは英小文字・数字・ハイフン推奨（例: `openclaw-cleanup`）

## 運用メモ
- まずは非破壊（移動よりコピー優先）で定着させる。
- 定着後に既存ルート散乱物を段階整理する。
