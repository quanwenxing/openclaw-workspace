# MCP部内ミニ勉強会
## Model Context Protocol の仕組みと活用

---

## 今日のアジェンダ

1. MCPとは何か（5分）
2. 仕組み・構成（10分）
3. ユースケース紹介（10分）
4. ライブデモ（10分）
5. まとめ・QA（5分）

---

## 1. MCPとは何か

### Model Context Protocol

**一言で言うと：**
> AIアシスタントと外部システムを繋ぐ**オープン標準**

---

### MCPの背景

| 項目 | 内容 |
|------|------|
| **正式名称** | Model Context Protocol |
| **発表** | 2024年11月 Anthropic |
| **目的** | AIとデータのあるシステムを接続 |

---

### 例え：USB-Cポート

**従来：**
- ツールA → 専用ケーブルA
- ツールB → 専用ケーブルB
- ツールC → 専用ケーブルC

**MCP：**
- どんなツールも **USB-C一本** で接続

---

### なぜMCPが必要か

**従来の問題：**
- ツールごとに独自の連携方法
- 実装の重複
- メンテナンス大変

**MCPの解決：**
- 統一的なプロトコル
- 一度実装すればどこでも使える
- コミュニティによる共通化

---

## 2. 仕組み・構成

### アーキテクチャ（3層構造）

```
┌─────────────────────────────────┐
│        Host（AIアプリ）          │
│   Claude Desktop / Cursor etc   │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│     MCP Client（クライアント）    │
│   Host ↔ MCP Server の仲介       │
└──────────────┬──────────────────┘
               │ JSON-RPC 2.0
┌──────────────▼──────────────────┐
│     MCP Server（サーバー）        │
│  GitHub / Slack / DB / File etc │
└─────────────────────────────────┘
```

---

### 各層の役割

| 層 | 役割 | 例 |
|----|------|-----|
| **Host** | AIアシスタント本体 | Claude Desktop, Cursor |
| **Client** | 接続クライアント | Host内蔵のMCP Client |
| **Server** | 外部ツール接続 | 各種MCP Server |

---

### MCP Serverの種類

**公式提供：**
- `@anthropics/mcp-server-fetch` - Web検索
- `@anthropics/mcp-server-filesystem` - ファイル操作
- `@modelcontextprotocol/server-github` - GitHub連携

**コミュニティ製：**
- 300+ のServerが公開されている
- <https://github.com/modelcontextprotocol/servers>

---

### 通信プロトコル

**JSON-RPC 2.0**
- 軽量なRPCプロトコル
- リクエスト/レスポンス形式
- 標準的で実装しやすい

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": { "name": "search", "arguments": {...} },
  "id": 1
}
```

---

## 3. ユースケース紹介

### 開発支援

**GitHub連携**
- Issue/PRの確認
- コードレビュー支援
- ブランチ操作

```
「このリポジトリのopenなissueを一覧して」
→ AIがGitHub API経由で取得・要約
```

---

### 情報検索

**Web検索連携**
- 最新情報のリアルタイム取得
- 複数ソースの横断検索

**社内Wiki連携**
- ナレッジベースへのアクセス
- 社内用語・手順の即時参照

---

### 業務自動化

| ツール | できること |
|--------|-----------|
| Slack | 通知送信、チャンネル検索 |
| Email | メール作成・送信 |
| Calendar | 予定確認・調整 |
| Todoist | タスク管理 |

---

### データ分析

**データベース連携**
- SQLクエリの自然言語実行
- 結果の可視化

**ファイル解析**
- CSV/Excelの分析
- レポート自動生成

---

### 導入事例

**大手フィンテック企業**
- 社内ツール統合
- 開発者生産性向上

**国内スタートアップ**
- 顧客対応自動化
- 情報収集効率化

---

## 4. ライブデモ

### デモ1：既存MCP Serverを使う

**Fetch Server（Web検索）**
```bash
npx -y @anthropics/mcp-server-fetch
```

**Filesystem Server（ファイル操作）**
```bash
npx -y @anthropics/mcp-server-filesystem ~/docs
```

---

### デモ2：Claude Desktopで試す

**Claude Desktop設定**
```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropics/mcp-server-fetch"]
    }
  }
}
```

**実際の利用**
```
ユーザー：「MCPの最新ニュースを調べて」
AI：→ Fetch Serverで検索 → 結果を要約
```

---

### デモ3：シンプルなMCP Server作成

**最小構成（Python）**
```python
from mcp.server import Server
from mcp.types import TextContent

app = Server("my-server")

@app.call_tool()
async def get_weather(city: str) -> list:
    # 天気APIを呼び出し
    result = await fetch_weather(city)
    return [TextContent(text=result)]

if __name__ == "__main__":
    app.run()
```

---

## 5. まとめ

### キーテイクアウェイ

✅ **MCPはAIツール連携の「共通言語」**
- 標準化により実装コスト削減

✅ **USB-Cのような存在**
- 同じ接続方法で様々なツールが使える

✅ **既存APIのラッピングでOK**
- 既存システムも簡単にMCP対応可能

---

### 次のステップ

1. **試してみる**
   - Claude DesktopにMCP Serverを追加

2. **カスタムServer作成**
   - 社内ツールをMCP化

3. **コミュニティ参加**
   - GitHubで事例を共有

---

### 参考リソース

| リソース | URL |
|----------|-----|
| 公式ドキュメント | <https://modelcontextprotocol.io> |
| GitHub | <https://github.com/modelcontextprotocol> |
| Server一覧 | <https://github.com/modelcontextprotocol/servers> |

---

## QA

**質問をお待ちしています！**

---

## ご清聴ありがとうございました

### Model Context Protocol

🌐 <https://modelcontextprotocol.io>

