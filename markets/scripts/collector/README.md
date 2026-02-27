# X Collector (Day1 MVP)

## 目的
- `markets/config/sources.yaml` の監視アカウントからX投稿を収集
- （有効時）日次実行の先頭でXリストメンバーを同期し、収集対象へ追加
- `markets/runs/YYYY-MM-DD.json` / `markets/state/collector-state.json` / `markets/state/active-sources.json` / `markets/logs/YYYY-MM-DD.log` を更新

## 必要環境変数
- `X_BEARER_TOKEN`: X API Bearer Token

## 実行
```bash
# 疎通（APIを叩かない）
python3 markets/scripts/collector/collect_x_posts.py --root /Users/username/.openclaw/workspace --dry-run

# 本番収集
python3 markets/scripts/collector/collect_x_posts.py --root /Users/username/.openclaw/workspace
```

## 依存
- requests
- pyyaml
