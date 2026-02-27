---
name: web-research
description: Web検索・調査を複合的に実行して、出典付きで要点をまとめる。Tavily/Braveなど複数の検索手段を使い分けたいとき、技術調査・市場調査・ニュース確認・一次情報確認（公式ページ）をしたいときに使う。
---

# Web Research

目的："検索"を単発ツールではなく、**目的に応じて手段を切り替える**ワークフローとして実行する。

## Quick workflow（基本）

1. **ゴールを確認**
   - 速報性が必要？（ニュース）
   - 網羅性が必要？（比較・まとめ）
   - 一次情報が必要？（公式発表・規約・論文）

2. **検索言語を決める（デフォルト：4言語で網羅）**
   - 入力が日本語/中国語/韓国語でも、**意図を保ったまま**以下を揃えて検索する
     - 日本語 / 英語 / 中国語 / 韓国語
   - 実装方針：クエリを4言語に言い換えて**複数回検索 → URLで重複排除して統合**

3. **手段を選ぶ（デフォルトの優先順位）**
   - まず俯瞰：`web_search`（OpenClaw標準：Brave Search）
   - 結果の追加収集・多様化：Tavily（このSkill同梱の `scripts/tavily_search.py` / `scripts/tavily_multilang.py`）
   - URLの本文抽出（APIキー不要で使えるが、ドメイン単位で一時ブロックが起きうる）：Jina Reader `r.jina.ai`（`scripts/jina_reader_fetch.py`）
     - 失敗時は **Tavilyのスニペットのみ** にフォールバック（`scripts/tavily_brief.py --enrich`）
   - 一次情報の確認：`browser` で公式/原典へアクセス（必要なら `web_fetch` で本文抽出）

4. **結果を統合して出力**
   - 重複URLは除外
   - 主要ポイントを3〜7個に要約
   - **出典（URL）を必ず付ける**

## Tavilyを使う（A: 検索結果の取得が主目的）

- APIキーは環境変数 `TAVILY_API_KEY` から読む（キーをチャットやログに出さない）
- 実行：
  - `python3 skills/public/web-research/scripts/tavily_search.py "<query>" --max-results 8`
- 返り値：標準出力にJSON（title/url/snippet等）

### 多言語（日本語/中国語/韓国語/英語）を混ぜたい場合

Tavily Search API自体に「言語固定」パラメータがない前提で、**クエリを言語ごとに作って複数回叩き、結果をマージ**するのが確実。

- まとめて回す場合：`scripts/tavily_multilang.py` を使う（4言語を並列実行してURL重複排除）

- 例：
  - 日本語：`"量子耐性 暗号 アップデート"`
  - 英語：`"post-quantum cryptography update"`
  - 中国語：`"后量子 密码 学术 进展"`
  - 韓国語：`"양자 내성 암호 동향"`

必要に応じてドメイン寄せも併用：
- 日本語：`--include-domains nikkei.com itmedia.co.jp` など
- 中国語：`--include-domains zhihu.com` など（用途次第）
- 韓国語：`--include-domains hankyung.com` など

詳細なオプションと例は `references/tavily.md` を読む。

## 出力テンプレ（推奨）

- 結論（1〜3行）
- 要点（箇条書き 3〜7）
- 参考（URL列挙）
- 補足（不明点・追加で調べるべき点）
