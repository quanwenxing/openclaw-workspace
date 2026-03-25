# 結果報告：Jupyter Docker + Host Tailscale Serve 構成

## 最終的な成果物
- **Docker Compose環境**: `work/2026/0308-1225_jupyter-docker-setup/`
- **Jupyter Notebook**: `jupyter/datascience-notebook`イメージを単独コンテナで使用。
- **外部アクセス**: ホストMacの Tailscale アプリ経由で `8888` ポートをHTTPS公開。
- **セキュリティ**: Tailnet内限定アクセス ＋ HTTPS ＋ トークン認証の三重ガード。

## アクセスURL
- **外部（Tailnet経由）**: `https://<Macのホスト名>.tail53f1d7.ts.net`
- **ホストMac（ローカル）**: `http://localhost:8888`
- **認証トークン**: `secure-jupyter-token-2026`

## セキュリティに関する結論
`tailscale serve` は自分のTailnet内（同一アカウントのデバイス間）のみにアクセスを制限するため、インターネット全体に公開されるリスクはなく、かつHTTPSによる経路暗号化が行われるため安全である。

## 完了日
2026-03-08
