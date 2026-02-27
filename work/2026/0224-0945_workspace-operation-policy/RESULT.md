# RESULT

## 要約（2〜4行）
workspace直下での直接作業を避けるため、`work/` 配下での標準運用を構築した。
人間向け `WORK_INDEX.md` と機械向け `work/index.json` を用意し、検索導線を統一した。
テンプレートとルール追記により、次回以降の作業を同一フォーマットで継続可能にした。

## 実施内容
- `work/templates` に標準テンプレート作成
- `WORK_INDEX.md` と `work/index.json` 初期化
- `AGENTS.md` へ作業分離ルール追記
- `MEMORY.md` へ運用希望を記録

## 生成・変更ファイル
- ../../../../WORK_INDEX.md
- ../../index.json
- ../../templates/README.template.md
- ../../templates/LOG.template.md
- ../../templates/RESULT.template.md
- ../../templates/META.template.json
- ../../../../AGENTS.md
- ../../../../MEMORY.md

## 判断メモ
- 大規模化に備え、`work/index/` に月次jsonl分割の導線を用意。

## 次アクション
- 次の依頼から同フォーマットで新規フォルダを作成して運用開始。
