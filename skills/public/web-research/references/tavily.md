# Tavily（検索結果取得）

## 環境変数

- `TAVILY_API_KEY` を使う（.envに保存し、起動時に読み込む）

## エンドポイント（スクリプト実装の前提）

- `POST https://api.tavily.com/search`

## 代表パラメータ

- `query` (string)
- `max_results` (int)
- `search_depth` (`basic`|`advanced`) ※必要時のみ
- `include_answer` (bool) → **A運用ではfalse推奨**
- `include_raw_content` (bool) → たいていfalse（必要なら browser/web_fetch）
- `include_domains` / `exclude_domains`（必要なときだけ）

## 多言語検索のコツ

- TavilyのSearchは**クエリ言語に強く依存**するため、多言語で拾いたいときは
  - 同じ意図のクエリを **日本語/英語/中国語/韓国語で作って複数回検索**
  - 結果をURLで重複排除して統合
が堅い。

- ドメイン寄せ（必要なときだけ）
  - `include_domains` で特定の言語圏・媒体に寄せる（例：`.co.jp`系、韓国紙、中国語圏サイト等）

## 例

```bash
python3 skills/public/web-research/scripts/tavily_search.py "openclaw web_search brave" --max-results 8
python3 skills/public/web-research/scripts/tavily_search.py "Tavily API search parameters" --max-results 5 --search-depth advanced

# 多言語を一括（推奨：言語別クエリを明示）
python3 skills/public/web-research/scripts/tavily_multilang.py \
  --ja "量子耐性 暗号 動向" \
  --en "post-quantum cryptography trends" \
  --zh "后量子 密码 进展" \
  --ko "양자 내성 암호 동향" \
  --max-results 8
```

## 注意

- APIキーは出力しない（ログ/履歴に残さない）
- Tavily結果は誤りや古い情報が混ざることがあるので、重要事項は一次情報（公式）を browser で確認する
