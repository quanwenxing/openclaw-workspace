# Session: 2026-03-12 23:58:57 UTC

- **Session Key**: agent:main:main
- **Session ID**: 92f8a35c-9175-4f15-8c0d-06946784e363
- **Source**: signal

## Conversation Summary

assistant: [[reply_to_current]] おはよう、クロウだよ。今朝も短く実務でいこう。今日は何を進める？
user: [Queued messages while agent was busy]

---
Queued #1
Conversation info (untrusted metadata):
```json
{
  "message_id": "1773268744562",
  "sender_id": "uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282",
  "sender": "太郎 田中",
  "timestamp": "Thu 2026-03-12 07:39 GMT+9"
}
```

Sender (untrusted metadata):
```json
{
  "label": "太郎 田中 (uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282)",
  "id": "uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282",
  "name": "太郎 田中"
}
```

Firecrawl CLIにツアで調べて
assistant: [[reply_to_current]] 了解。Firecrawl CLIを使って調べる方向でいける。  
何を調べたい？対象URL・キーワード・知りたい観点（使い方 / 導入方法 / 料金 / scrape方法 / crawl例 など）を1行でくれれば、そのまま調査する。
assistant: 了解。Firecrawl CLIを使って調べる方向でいける。
何を調べたい？対象URL・キーワード・知りたい観点（使い方 / 導入方法 / 料金 / scrape方法 / crawl例 など）を1行でくれれば、そのまま調査する。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "1773268787001",
  "sender_id": "uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282",
  "sender": "太郎 田中",
  "timestamp": "Thu 2026-03-12 07:39 GMT+9"
}
```

Sender (untrusted metadata):
```json
{
  "label": "太郎 田中 (uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282)",
  "id": "uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282",
  "name": "太郎 田中"
}
```

何ができるか、例えばクロウがこれ使って何ができるか、できないことは何かなど
assistant: ざっくり確認する。Firecrawl公式ドキュメントから拾う。
assistant: [[reply_to_current]] ざっくり言うと、**Firecrawl CLI は「WebサイトをAI向けデータとして取ってくるための入口」**。  
クロウ視点だと、**調査・収集・整形**はかなり強いけど、**万能ブラウザ自動化**や**何でも突破**ではない。

**クロウがこれでできること**
- **URLをそのまま取得して Markdown/HTML/links などで抽出**
  - 例: ドキュメント、LP、ヘルプページ、ブログをLLM向けに整理
- **Web検索**
  - 検索結果だけでなく、結果ページの本文取得までつなげられる
- **複数ページのクロール**
  - サイト配下をたどって情報収集しやすい
- **構造化データ抽出**
  - ページ本文をそのまま読むだけでなく、必要な項目をJSONっぽく抜く用途に向く
- **動的ページ対応が比較的強い**
  - JavaScript描画サイト向けの設計が前提
- **Browser Sandbox 連携**
  - フォーム入力、クリック、待機などの「操作してから取得」ができる
- **AIエージェント用の取り込み**
  - 公式が CLI / Skill / MCP 経由でエージェント連携を前提にしている

**クロウが Firecrawl CLI でやると強い仕事**
- 競合サイト・料金ページ・FAQの収集
- 公式ドキュメントの要点抽出
- 特定テーマのリサーチ素材集め
- サイト全体をざっとクロールして「どこに何があるか」を把握
- AIに渡しやすい Markdown 化
- 「このページから価格・会社情報・機能一覧だけ抜く」みたいな整理

**できない / 苦手なこと**
- **SNS系は基本向いていない**
  - 公式FAQで「social media platforms は現在サポート外」と明記
- **ログイン必須・強い認証・厳しいBot対策を必ず突破できるわけではない**
  - Browser機能はあるけど、何でも通る保証はない
- **サイト内の全ページ取得を常に保証できない**
  - rate limit、anti-scraping、サイト構造次第で漏れる
- **Web上の操作全般を完全代替する万能RPAではない**
  - 主目的は「Webデータ取得」。業務UI自動化専用ツールではない
- **ローカルファイル操作やアプリ連携そのものは別**
  - Firecrawlは基本Webデータ層。取得後の整形・保存・連携は別途組む
- **結果の正しさを100%保証しない**
  - ページ構造変更、レンダリング差分、取得タイミングでブレることはある

**向いてる用途**
- 調査
- 要約前の素材収集
- ドキュメント収集
- 価格/機能比較
- RAG用データ作成
- AIエージェントへのWeb読解能力追加

**向いてない用途**
- SNS監視メイン
- 厳格な業務RPA
- 完全再現性が必要なUIテスト
- 強認証サイトの安定巡回
- 「絶対に全ページ漏れなく」前提の収集

**一言でいうと**
- **得意:** 「Webを読める形にする」
- **微妙:** 「Webサービスを人間みたいに何でも操作する」
- **苦手:** 「SNSや強く閉じた環境を安定突破する」

必要なら次に  
**「Firecrawl CLIでクロウが実際にやれる具体例10個」** か  
**「OpenClaw + Firecrawl CLI の実運用パターン」**  
まで落として整理する。

**出典**
- Firecrawl Docs Quickstart / Introduction: https://docs.firecrawl.dev/introduction.md
- Firecrawl 公式サイト FAQ・機能説明: https://www.firecrawl.dev/
assistant: [[reply_to_current]] 今朝のメモ、1件ある。

- **claude公式のplugin skillを試す**（**3/12**, **P1**）

必要なら、このまま今日やる順に軽く並べ替えるよ。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "1773274372385",
  "sender_id": "uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282",
  "sender": "太郎 田中",
  "timestamp": "Thu 2026-03-12 09:12 GMT+9"
}
```

Sender (untrusted metadata):
```json
{
  "label": "太郎 田中 (uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282)",
  "id": "uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282",
  "name": "太郎 田中"
}
```

使い方を公式ドキュメント確認してわかりやすくまとめて
assistant: 公式のCLIドキュメントを見て、使い方だけわかりやすく噛み砕いてまとめる。
assistant: [[reply_to_current]] 公式ドキュメント確認して、**Firecrawl CLIの使い方**を実務目線でまとめる。

## まず何者か
Firecrawl CLI は、**Webページの取得・検索・URL一覧化・ブラウザ操作**をコマンドで使うための公式CLI。  
主な軸はこの4つ。

- **scrape**: 1ページを取得してMarkdown/HTML/linksなどにする
- **search**: Web検索して結果を返す。必要なら本文も取れる
- **map**: サイト内URLを一覧化する
- **browser**: クラウド上のブラウザを起動してクリックや取得を行う

---

## 1. インストール

### AIエージェント向けの推奨導入
```bash
npx -y firecrawl-cli@latest init --all --browser
```

意味:
- `--all`: 検出したAIコーディングエージェント全部にFirecrawl skillを入れる
- `--browser`: 認証用ブラウザを自動で開く

### 普通にCLIだけ入れる
```bash
npm install -g firecrawl-cli
```

---

## 2. 認証

### いちばん普通
```bash
firecrawl login
```

### ブラウザ認証
```bash
firecrawl login --browser
```

### APIキー直指定
```bash
firecrawl login --api-key fc-YOUR-API-KEY
```

### 環境変数
```bash
export FIRECRAWL_API_KEY=fc-YOUR-API-KEY
```

### 状態確認
```bash
firecrawl --status
firecrawl view-config
```

### ログアウト
```bash
firecrawl logout
```

---

## 3. まずはこれだけ覚えれば使える

## A. 1ページ取得: scrape
### 最小形
```bash
firecrawl https://example.com
```

または
```bash
firecrawl scrape https://example.com
```

### 実務でまずおすすめ
```bash
firecrawl https://example.com --only-main-content
```

`--only-main-content` は、**ヘッダ・フッタ・ナビを減らして本文中心で取る**ので、要約やRAG向き。

### よく使う例
```bash
# HTMLで取得
firecrawl https://example.com --html

# Markdown + links をJSONで取得
firecrawl https://example.com --format markdown,links --pretty

# JS描画待ち
firecrawl https://example.com --wait-for 3000

# スクリーンショット付き
firecrawl https://example.com --screenshot

# ファイル保存
firecrawl https://example.com -o output.md
```

### 取れる主な format
- `markdown`
- `html`
- `rawHtml`
- `links`
- `screenshot`
- `json`
- `images`
- `summary`
- `changeTracking`
- `attributes`
- `branding`

---

## B. Web検索: search
```bash
firecrawl search "web scraping tutorials"
```

### よく使う例
```bash
# 件数指定
firecrawl search "AI news" --limit 10

# news / images も含める
firecrawl search "OpenAI" --sources web,news,images

# GitHub寄りに絞る
firecrawl search "react hooks" --categories github

# 期間指定
firecrawl search "tech news" --tbs qdr:d   # 直近1日
firecrawl search "tech news" --tbs qdr:w   # 直近1週間

# 検索結果の本文も取る
firecrawl search "documentation" --scrape --scrape-formats markdown
```

**用途**
- 最新情報の候補集め
- 検索→本文取得まで一気にやる
- 「まず広く探す」フェーズ

---

## C. サイトURL一覧化: map
```bash
firecrawl map https://example.com
```

### よく使う例
```bash
# JSONで出す
firecrawl map https://example.com --json

# 最大件数
firecrawl map https://example.com --limit 500

# blogを含むURLだけ探す
firecrawl map https://example.com --search "blog"

# サブドメイン込み
firecrawl map https://example.com --include-subdomains

# sitemapだけ使う
firecrawl map https://example.com --sitemap only
```

**用途**
- docsサイトの全体把握
- クロール前のURL棚卸し
- 対象ページ候補の洗い出し

---

## D. ブラウザ操作: browser
CLIの中では少し強めの機能。  
**クラウド上のChromiumセッション**を立てて、操作や取得ができる。

### セッション開始
```bash
firecrawl browser launch-session
```

### 自然言語っぽく操作
```bash
firecrawl browser execute "open https://example.com"
firecrawl browser execute "snapshot"
firecrawl browser execute "click @e5"
firecrawl browser execute "scrape"
```

### Playwright Python
```bash
firecrawl browser execute --python 'await page.goto("https://example.com")
print(await page.title())'
```

### Playwright JavaScript
```bash
firecrawl browser execute --node 'await page.goto("https://example.com"); console.log(await page.title());'
```

### セッション一覧・終了
```bash
firecrawl browser list
firecrawl browser close
```

**用途**
- クリックしてから本文取得
- JSサイトの確認
- 軽いブラウザ自動化
- 人間操作に近いフロー確認

---

## 4. クロウが使うなら、実際こう使う

## パターン1: 1ページだけ要約したい
```bash
firecrawl https://example.com --only-main-content -o page.md
```
→ そのまま要約や抽出に回す。

## パターン2: 公式ドキュメントを調べたい
```bash
firecrawl map https://docs.example.com --search "api" --json
```
→ URL候補を出して、必要ページだけ `scrape`

## パターン3: 最新情報を探して本文まで欲しい
```bash
firecrawl search "OpenClaw Firecrawl update" --limit 5 --scrape --scrape-formats markdown --pretty
```

## パターン4: 普通の取得で足りないページ
```bash
firecrawl browser launch-session
firecrawl browser execute "open https://example.com"
firecrawl browser execute "snapshot"
firecrawl browser execute "scrape"
```

---

## 5. まず覚えるべきおすすめ最小セット
最初はこの5つだけで十分。

```bash
firecrawl login
firecrawl --status
firecrawl https://example.com --only-main-content
firecrawl search "keyword" --limit 5
firecrawl map https://example.com --json
```

---

## 6. 注意点
- **APIキー認証が基本必要**
- **custom API URL / self-hosted の場合は `--api-url` が使える**
- `--status` で **認証状態 / credits / concurrency** を見られる
- `search` は「検索」、`scrape` は「1ページ取得」、`map` は「URL発見」、`browser` は「操作付き」
- **本文だけ欲しいなら `--only-main-content` がかなり重要**

---

## 7. もんちゃん向けの一言まとめ
**Firecrawl CLI = “WebをAI向けの読みやすいデータにするための公式CLI”**。  
まずは:

1. `login`
2. `scrape`
3. `search`
4. `map`
5. 必要なら `browser`

この順で覚えるのが一番ラク。

**出典**
- Firecrawl公式CLIドキュメント: https://docs.firecrawl.dev/sdks/cli
- Firecrawl公式ドキュメント索引: https://docs.firecrawl.dev/llms.txt

必要なら次に  
**「Firecrawl CLI チートシート」**  
か  
**「OpenClawでクロウが使う前提の実践コマンド集」**  
にして渡せる。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "1773275553973",
  "sender_id": "uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282",
  "sender": "太郎 田中",
  "timestamp": "Thu 2026-03-12 09:32 GMT+9"
}
```

Sender (untrusted metadata):
```json
{
  "label": "太郎 田中 (uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282)",
  "id": "uuid:39c73231-2cd0-41c4-b7b2-7ce6580e6282",
  "name": "太郎 田中"
}
```

エージェント向けの情報収集はこういうのいっぱいあって何をどう使うのが一番良いか検討したい。全ての使えるツール、サービスを有料無料関係なく網羅的に調べてまとめて。
assistant: 網羅寄りでやる。主要カテゴリごとに公式情報を拾って、エージェント用途で比較できる形に整理する。
assistant: [[reply_to_current]] 了解。  
**「エージェント向け情報収集」の主要ツール/サービスを、有料無料を分けずにカテゴリ横断で整理**して、**何をどう使うのが一番いいか**まで踏み込んでまとめる。  
結論から言うと、**1個で全部やるより、`検索層 + 取得層 + ブラウザ層 + オーケストレーション層` の4層で組むのが一番強い**。

---

# 先に結論

## いま一番バランスがいい考え方
エージェント向け情報収集は、だいたい次の4層で考えると整理しやすい。

1. **検索層**  
   「どこを読むべきか探す」  
   例: Tavily, Exa, SerpApi

2. **取得/抽出層**  
   「そのURLから本文や構造化データを取る」  
   例: Firecrawl, Tavily Extract, Jina Reader, Scrapy, Apify

3. **ブラウザ操作層**  
   「クリック・待機・ログイン後ページ・JS描画」  
   例: Browserbase, Stagehand, Playwright, Puppeteer, browser-use, Cloudflare Browser Rendering

4. **エージェント実行/統合層**  
   「LLMにどう渡して、どう再試行・監視・HITLするか」  
   例: LangChain/LangGraph, MCP, OpenClaw, Claude Code系連携

---

# まず、用途別の最適解

## A. 調査・要約・競合比較が主目的
**最有力**
- **Tavily**
- **Exa**
- **Firecrawl**

### 理由
- **Tavily**: 「検索→抽出→クロール」までエージェント向けにまとまっていて早い
- **Exa**: 「AI向け検索エンジン」として優秀。類似ページ探索やResearch系が強い
- **Firecrawl**: 取得後の本文/Markdown/JSON化がかなり使いやすい

### 実務での組み方
- **Exa or Tavilyで候補URL発見**
- **Firecrawlで本文取得**
- 必要なら **Browserbase / Playwright** で操作込み収集

---

## B. docs / help center / ブログ / FAQ の収集が主目的
**最有力**
- **Firecrawl**
- **Apify**
- **Scrapy**（自前運用なら）

### 理由
- **Firecrawl**: LLM-readyな本文化が速い
- **Apify**: Actor資産と運用基盤が強い
- **Scrapy**: OSSで自由度高いが、エージェント向け即戦力というより開発者向け

---

## C. ログイン後画面やJSサイト、クリック前提
**最有力**
- **Browserbase + Stagehand**
- **Playwright**
- **browser-use**
- **Cloudflare Browser Rendering**

### 理由
- **Browserbase**: ブラウザ基盤を持たなくて済む
- **Stagehand**: AIを使った「壊れにくいブラウザ操作」に向く
- **Playwright**: 汎用性最強
- **browser-use**: AIブラウザエージェント寄り
- **Cloudflare Browser Rendering**: REST/Workers経由の実行に向く

---

# 網羅マップ

---

## 1. 検索特化系

## 1-1. Tavily
**何が強いか**
- エージェント向けWeb検索をかなり明確に意識
- **search / extract / crawl** を持つ
- 検索結果に本文取得をつなげやすい
- SDK/HTTPがシンプル

**向く用途**
- 調査エージェント
- 最新情報収集
- 「まず探して、そのまま読む」

**弱み**
- 検索・抽出中心で、複雑ブラウザ操作の主役ではない
- 深いサイト攻略は別レイヤーが必要

**総評**
- **“エージェント向け検索の第一候補” のひとつ**

**出典**
- Tavily Docs Welcome: https://docs.tavily.com/welcome

---

## 1-2. Exa
**何が強いか**
- 公式で **“search engine made for AIs”**
- `search`, `contents`, `findsimilar`, `answer`, `research` がある
- 「類似ページ発見」「リサーチタスク」まで見えている

**向く用途**
- 深掘り調査
- 類似文書探索
- トピック拡張
- リサーチワークフロー

**弱み**
- ブラウザ自動化そのものは主戦場ではない
- 実ページ取得/操作は別ツールと組みたくなる

**総評**
- **“調査の上流” に強い**
- 特に「何を読むべきか探す」の精度設計で候補

**出典**
- Exa Docs Getting Started: https://exa.ai/docs/reference/getting-started

---

## 1-3. SerpApi
**何が強いか**
- Google系SERP取得の定番
- location / gl / uule など、検索条件の細かさが強い
- 検索結果JSON取得が安定

**向く用途**
- SERP監視
- 地域別検索結果比較
- SEO/競合観測
- 「検索結果そのもの」が重要な業務

**弱み**
- 本文取得・構造化抽出は別ツール前提
- 「エージェント向け検索統合体験」はTavily/Exaほど前面ではない

**総評**
- **“検索結果を正確に取りたい” なら依然強い**
- ただしエージェント向けには単体では足りないことが多い

**出典**
- SerpApi Google Search API: https://serpapi.com/search-api

---

## 1-4. Jina AI Reader / Search Foundation
**何が強いか**
- 既知URLをLLM向けに読む `r.reader`
- 検索して読ませる `s.reader`
- Embeddings / Reranker まで同じ系統にある

**向く用途**
- URLをそのまま読ませる
- RAG前処理
- 軽い検索＋整形

**弱み**
- 今回見た docs の見せ方が特殊で、導線が少し癖あり
- ブラウザ操作層としては弱い

**総評**
- **“軽量な取得・検索基盤” としては魅力**
- ただし全体基盤に据えるより、補助レイヤー向き

**出典**
- Jina AI Search Foundation Docs: https://docs.jina.ai/

---

# 2. 取得・抽出・クロール特化系

## 2-1. Firecrawl
**何が強いか**
- `scrape`, `search`, `agent`, `browser` を持つ
- **Markdown / HTML / structured JSON / screenshot**
- JS対応、動的ページ、MCP、CLI、Browser Sandbox
- LLM向け出力をかなり前提にしている

**向く用途**
- docs/ブログ/FAQ/LP収集
- RAG用データ化
- URLから本文抽出
- 検索→本文化→要約

**弱み**
- SNSや閉じた環境には向かない
- 複雑業務フローの自動化専用ではない
- “検索専業” の精度競争は Tavily/Exa と比較検討が必要

**総評**
- **“取得/整形の主軸” として非常に強い**
- いまの候補群の中では、**エージェント向け取得レイヤーの本命級**

**出典**
- Firecrawl Quickstart / Intro: https://docs.firecrawl.dev/introduction
- Firecrawl CLI Docs: https://docs.firecrawl.dev/sdks/cli

---

## 2-2. Tavily Extract / Crawl
**何が強いか**
- 検索だけでなく `extract`, `crawl` も持つ
- 1サービスで流れを完結しやすい

**向く用途**
- リサーチエージェントを素早く作る
- 検索→URL→本文取得までまとめる

**弱み**
- ブラウザ操作や複雑ページ攻略は別レイヤーが必要
- 深いサイト攻略は Firecrawl / Browserbase / Playwright 側が欲しくなる

**総評**
- **“少ない部品で始めたい” 人向け**
- Firecrawl とかなり比較対象になる

**出典**
- Tavily Docs Welcome: https://docs.tavily.com/welcome

---

## 2-3. Apify
**何が強いか**
- Cloud platform + marketplace + Actors
- Proxy / Storage / Scheduling / Monitoring まである
- 「既製スクレイパー資産」が非常に大きい

**向く用途**
- 大量収集
- 定期運用
- 特定サイト向け専用Actor活用
- 社内基盤化

**弱み**
- “AIエージェント用に即使える自然な取得体験” という意味では Firecrawl/Tavily の方が分かりやすいこともある
- 柔軟だが、サービス理解コストは少しある

**総評**
- **“運用基盤・マーケットプレイス込みの現実解”**
- 特定サイトに強い既存Actorがあるならかなり有力

**出典**
- Apify Platform Docs: https://docs.apify.com/platform

---

## 2-4. Scrapy
**何が強いか**
- 老舗OSS
- 非同期クロール
- 大規模収集で強い
- 抽出/出力/パイプライン設計が自由

**向く用途**
- 自前で本格クローラ構築
- 長期運用
- 高度なカスタム収集

**弱み**
- AIエージェント向け即戦力ではない
- JS対応・ブラウザ操作は別物
- 実務では Playwright 等との併用が必要になりやすい

**総評**
- **“開発者が自分で作るなら強い”**
- でも **“今すぐエージェント情報収集” の主役ではない**

**出典**
- Scrapy Overview: https://docs.scrapy.org/en/latest/intro/overview.html

---

## 2-5. Oxylabs / Bright Data 系
**何が強いか**
- Proxy / Web Scraper API / Unblocker / Headless Browser など
- 対bot対策が強い領域に寄っている
- 大規模・商用・取得難サイトで候補になる

**向く用途**
- 難サイト
- 収集規模が大きい案件
- 安定的な商用スクレイピング

**弱み**
- エージェント向けUXとしてはややインフラ寄り
- 「自然言語で調査」より「堅牢な取得基盤」向け

**総評**
- **“難しいサイトを落とすための取得インフラ”**
- 研究エージェント単体より、収集基盤の裏方向き

**出典**
- Oxylabs Developers Overview: https://developers.oxylabs.io/
- Bright Data Browser/Scraping docs home: https://docs.brightdata.com/home

---

# 3. ブラウザ自動化・操作系

## 3-1. Browserbase
**何が強いか**
- headless browser 実行基盤をマネージドで提供
- Playwright / Puppeteer / Selenium / Stagehand と親和性
- session visibility, replay, logs, captcha solving, residential proxies

**向く用途**
- エージェントにブラウザを持たせる
- ログイン後収集
- JSサイト操作
- 運用時の可観測性

**弱み**
- 検索そのものは主戦場でない
- 取得後の整形/検索は別と組み合わせたくなる

**総評**
- **“ブラウザ層の本命”**
- Browserbase 単体というより **Stagehand/Playwright の実行基盤** として強い

**出典**
- Browserbase What is Browserbase: https://docs.browserbase.com/introduction/what-is-browserbase

---

## 3-2. Stagehand
**何が強いか**
- Browserbase製のAIブラウザ自動化フレームワーク
- `act`, `extract`, `observe`, `agent`
- 「セレクタ壊れやすい問題」と「AI任せで不安定問題」の間を狙っている

**向く用途**
- エージェントにクリックさせる
- UI変更に多少強いブラウザ操作
- 自然言語+コードの混合運用

**弱み**
- 完全に決定的な挙動を求めると Playwright の方が読みやすい場面もある
- AIコスト/不確実性はゼロではない

**総評**
- **“AI時代のブラウザ操作” としてかなり有望**
- ただし **重要フローは deterministic code と混ぜる** 前提がいい

**出典**
- Stagehand Introduction: https://docs.stagehand.dev/

---

## 3-3. Playwright
**何が強いか**
- 汎用ブラウザ自動化の定番
- Chromium / Firefox / WebKit
- テストだけでなく、収集にも使える
- assertions, tracing, report など成熟

**向く用途**
- 複雑UI操作
- ログイン・ページ遷移
- 安定したブラウザスクリプト
- 独自ワークフロー実装

**弱み**
- セレクタ保守コスト
- “探索的なエージェント行動” は上位レイヤーが必要

**総評**
- **“最終的に帰ってくる土台”**
- なんだかんだ一番信頼できる

**出典**
- Playwright Intro: https://playwright.dev/docs/intro

---

## 3-4. Puppeteer
**何が強いか**
- Chrome系中心でシンプル
- Node周りで使いやすい
- MCPサーバ連携も見える

**向く用途**
- 軽量なChrome自動化
- Nodeベースの既存資産活用

**弱み**
- 近年のエージェント用途だと Playwright に寄ることが多い
- クロスブラウザ/テスト体験では Playwright 優勢

**総評**
- **まだ現役**だが、新規で選ぶなら Playwright 優先になりがち

**出典**
- Puppeteer: https://pptr.dev/

---

## 3-5. browser-use
**何が強いか**
- AI browser automation をかなり前面に出している
- stealth / CAPTCHA / residential proxies / managed infra
- coding agent quickstart もある

**向く用途**
- ブラウザエージェント
- 操作込みタスク
- 目的指向のWebタスク実行

**弱み**
- 強いが、再現性/保守性は設計次第
- “調査の上流検索” ではない

**総評**
- **“操作させるAIエージェント” には有力**
- ただし情報収集全体の主軸というよりブラウザ層

**出典**
- Browser Use Cloud Intro: https://docs.browser-use.com/introduction

---

## 3-6. Cloudflare Browser Rendering
**何が強いか**
- BrowserをCloudflare上で実行
- REST API で screenshot / pdf / markdown / links / structured data / crawl
- Workers Bindings で Playwright / Puppeteer / Stagehand 接続
- Free/Paid plans の導線あり

**向く用途**
- Cloudflare中心の基盤
- エッジ実行
- 軽量API化
- 大量 stateless 実行

**弱み**
- Browserbaseほど“ブラウザ開発専業UX”ではない
- エージェント用途は少し設計力が必要

**総評**
- **Cloudflare民ならかなり魅力**
- 既存インフラにハマるなら強い

**出典**
- Cloudflare Browser Rendering: https://developers.cloudflare.com/browser-rendering/

---

# 4. エージェント統合・オーケストレーション系

## 4-1. LangChain / LangGraph
**何が強いか**
- モデル・ツール統合
- エージェント構築
- durable execution, persistence, human-in-the-loop
- LangSmith で可観測性

**向く用途**
- 自前エージェント基盤
- ツール呼び出し設計
- 長期ワークフロー

**弱み**
- 検索/取得そのものは別途必要
- レイヤーが増えると複雑化しやすい

**総評**
- **“集める道具” ではなく “まとめて動かす骨格”**
- 情報収集エージェントではかなり有力

**出典**
- LangChain Overview: https://docs.langchain.com/oss/javascript/langchain/overview

---

## 4-2. MCP
**何が強いか**
- Claude / Cursor / 各種エージェントとの接続標準として広がっている
- ツールの“接続方法”を揃えやすい

**向く用途**
- 各収集ツールをLLMから使わせる
- CLI/SDK/BrowserをMCPに載せる
- ツールの再利用

**弱み**
- それ自体が検索・取得するわけではない
- うまく使うにはツール選定が本体

**総評**
- **“道具箱の配線規格”**
- 今後ほぼ必須に近い

---

# 実務での比較表

## ざっくり比較
- **検索精度・AI向け探索**
  - 強い: **Exa, Tavily**
- **本文抽出・Markdown化**
  - 強い: **Firecrawl, Tavily Extract, Jina Reader**
- **大規模運用・既製スクレイパー**
  - 強い: **Apify**
- **難サイト攻略・取得インフラ**
  - 強い: **Bright Data, Oxylabs**
- **ブラウザ実行基盤**
  - 強い: **Browserbase, Cloudflare Browser Rendering**
- **ブラウザ操作フレームワーク**
  - 強い: **Playwright, Stagehand, browser-use**
- **OSS自前構築**
  - 強い: **Scrapy, Playwright, Puppeteer**
- **エージェント統合**
  - 強い: **LangChain/LangGraph, MCP**

---

# で、「一番良い使い方」は何か

## パターン1: いちばん実用的で失敗しにくい構成
### おすすめ構成
- **検索**: Tavily or Exa
- **取得**: Firecrawl
- **ブラウザ操作**: Browserbase + Playwright or Stagehand
- **統合**: MCP / OpenClaw / LangChain系

### これが強い理由
- 検索と取得を分離できる
- Firecrawlを「本文化マシン」として使いやすい
- ブラウザ操作が必要な時だけ Browserbase/Playwright を足せる
- 一番柔軟

### いまの俺の評価
**これが総合1位候補。**

---

## パターン2: 部品数を減らして早く作る
### おすすめ構成
- **Tavily 単体を主軸**
- 足りないとこだけ Firecrawl / Playwright

### 向く人
- まず早く動かしたい
- deep browser automation はまだ少ない
- リサーチ主体

### 評価
**PoC最速。**

---

## パターン3: 収集規模が大きい / 定期運用 / 難サイトあり
### おすすめ構成
- **Apify or Bright Data or Oxylabs**
- ブラウザは Browserbase / Playwright
- 調査系だけ Tavily/Exa追加

### 向く人
- 事業化前提
- 毎日大量取得
- 特定サイトを安定運用

### 評価
**商用収集基盤向け。**

---

## パターン4: すべてOSS中心で自前
### おすすめ構成
- **Scrapy + Playwright**
- 必要なら Puppeteer
- 検索は別API

### 向く人
- かなり作り込みたい
- コスト最適化したい
- ベンダーロックを避けたい

### 評価
**自由度最強、でも開発負荷も最強。**

---

# もんちゃんにおすすめの現実解

会話の流れ的に、もんちゃんが検討したいのは  
**「エージェント向け情報収集の標準スタックをどうするか」** だと思う。  
その前提で、俺のおすすめ順はこう。

## 推奨案A: まずこれ
- **Tavily**
- **Firecrawl**
- **Playwright**
- 必要なら **Browserbase**
- 接続は **MCP**

### 理由
- 情報収集エージェントとしてバランスがいい
- 検索 / 本文取得 / JS操作 をきれいに分けられる
- 過不足が少ない

---

## 推奨案B: Firecrawl中心でまとめたい
- **Firecrawl**
- **Playwright**
- 必要なら **Exa**

### 理由
- Firecrawlは取得と整形が強い
- searchもある
- 足りない探索力を Exa で補える

---

## 推奨案C: 将来の商用運用まで見据える
- **Exa or Tavily**
- **Firecrawl**
- **Browserbase + Stagehand**
- **Apify**（定期運用・特定サイト用）
- **LangGraph / MCP**

### 理由
- 収集・操作・運用まで伸ばしやすい

---

# 「何を捨てるか」も大事

## 最初から全部は要らない
最初に全部入れると、だいたい失敗する。  
まずは以下で十分。

### 最小セット
- **検索**: Tavily か Exa のどちらか1つ
- **取得**: Firecrawl
- **ブラウザ**: Playwright
- **接続**: MCP

この4つで、かなり広い範囲をカバーできる。

---

# クロウの率直な評価

## かなり良い
- **Firecrawl**: 取得層としてかなり優秀
- **Tavily**: 調査エージェント向けに使いやすい
- **Exa**: 探索・類似発見・research寄りで良い
- **Browserbase**: ブラウザ基盤として強い
- **Stagehand**: “AIで壊れにくいブラウザ操作” の筋が良い
- **Playwright**: 土台として外しにくい

## 強いけど役割が違う
- **Apify**: 運用・Actor資産が強い
- **SerpApi**: SERP取得専業として強い
- **Oxylabs / Bright Data**: 難サイト・商用収集インフラ向け
- **Scrapy**: OSS本格構築向け

## 最初の主役にしなくていい
- **Puppeteer**: 悪くないけど新規主役はPlaywright寄り
- **Jina Reader系**: 補助としては面白いが主軸は再検討余地あり

---

# 結論を一文で
**「検索は Tavily / Exa、取得は Firecrawl、操作は Playwright or Browserbase+Stagehand、全体接続は MCP」**  
この構成が、いま一番“失敗しにくくて強い”と思う。

---

# 出典
- Firecrawl Introduction / Quickstart: https://docs.firecrawl.dev/introduction
- Firecrawl CLI: https://docs.firecrawl.dev/sdks/cli
- Tavily Docs Welcome: https://docs.tavily.com/welcome
- Exa Docs Getting Started: https://exa.ai/docs/reference/getting-started
- Browserbase Intro: https://docs.browserbase.com/introduction/what-is-browserbase
- Stagehand Intro: https://docs.stagehand.dev/
- Playwright Intro: https://playwright.dev/docs/intro
- Apify Platform Docs: https://docs.apify.com/platform
- SerpApi Google Search API: https://serpapi.com/search-api
- Cloudflare Browser Rendering: https://developers.cloudflare.com/browser-rendering/
- Oxylabs Developers Overview: https://developers.oxylabs.io/
- Browser Use Cloud Intro: https://docs.browser-use.com/introduction
- Scrapy Overview: https://docs.scrapy.org/en/latest/intro/overview.html
- Jina AI Search Foundation Docs: https://docs.jina.ai/
- LangChain Overview: https://docs.langchain.com/oss/javascript/langchain/overview

必要なら次にそのまま続けて、
**1. 比較表（機能 / 料金感 / 向く用途 / 向かない用途）**
または
**2. もんちゃん向け推奨スタックを3案に絞って設計**
までやる。
assistant: [[reply_to_current]] 今のところ、今日のタスクは入ってないよ。
