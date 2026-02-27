# Jina Reader（r.jina.ai）メモ

## 何ができる？

- URLを **LLM向けのMarkdown/JSON** に変換（本文抽出/整形）
- APIキー不要でも使える（ただしレート制限あり）

公式：
- https://jina.ai/reader/
- https://github.com/jina-ai/reader

## 使い方

- もっとも簡単：
  - `https://r.jina.ai/https://example.com/...`

- JSONで取りたい（ツール連携向き）：
  - `Accept: application/json` を付ける

## よく使うヘッダ（ベストエフォート）

※Jina側が解釈するヘッダ。挙動は変更されうる。

- `x-target-selector`: 指定CSSセレクタのみ抽出（例：`article`）
- `x-wait-for-selector`: 指定セレクタが現れるまで待機（動的ページ）
- `x-exclude-selector`: 指定セレクタを除外（例：`nav, footer`）
- `x-no-cache: true`: キャッシュを無視
- `x-cache-tolerance: <seconds>`: 何秒以内のキャッシュなら許容

## OpenClawスキル内スクリプト

- `scripts/jina_reader_fetch.py` : URL→JSON/Markdown

例：

```bash
python3 skills/public/web-research/scripts/jina_reader_fetch.py \
  "https://example.com/article" \
  --format json \
  --target-selector article
```
