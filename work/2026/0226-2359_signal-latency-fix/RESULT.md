# RESULT

## 実施内容（Todoist MCP）
- mcporter CLI を導入済み
- Todoist MCPサーバ定義を `~/.mcporter/mcporter.json` に追加済み
- APIキーは設定ファイルに平文保存せず、macOS Keychain参照ラッパー経由で注入する方式に設定済み

## 追加した実体
- `/Users/username/.openclaw/bin/todoist-mcp-keychain.sh`
  - Keychain項目: account=`todoist-api-token`, service=`openclaw/todoist`
  - 見つかれば `API_KEY` をexportして `npx -y todoist-mcp` を起動

## 現在の状態
- `mcporter list` で `todoist` サーバは認識
- ただし Keychain項目が未登録のため現在はoffline

## 残作業
1. KeychainへAPIキーを保存
2. `mcporter list todoist --schema` で疎通確認
3. 必要ならOpenClaw側の運用プロンプト（朝/夜のTODOルール）を追加
