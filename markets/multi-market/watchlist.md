# Watchlist

フォーマット:
- ID: WATCH-0001
- Name/Address:
- Type: address | person | org
- Chain/Platform:
- Why Track:
- Signals:
- Source:
- Source Type: manual_discord | auto_x_grok
- Tags:
- First Seen At:
- Event Time:
- Updated:

- ID: WATCH-0002
- Title: 進めた。**残タスク2（``の自動取り込み）** を実装した。
- Summary: 進めた。**残タスク2（``の自動取り込み）** を実装した。

### 追加したもの
- `markets/scripts/pipeline/ingest_manual_discord_event.py`
- ``付きメッセージを自動取り込み
- 市場判定（polymarket/kalshi/opinion/multi/other）
- カテゴリ判定（ideas/watchlist/dev-tools/other）
- `manual_discord` + `インサイト分析`タグ付与
- メッセージID重複防止（state管理）

### 自動化ジョブも追加
- cron: `markets-manual-insight-sync-15m`
- 15分ごとにこのチャネルを確認し、``投稿を台帳へ反映
- 新規があれば簡潔に通知、なければ何もしない

---
- Source: discord://1473508792929882142/1473571891926274133
- Source Type: manual_discord
- Tags: インサイト分析
- Created At: 2026-02-18 16:00:24 JST
- Event Time: 2026-02-18 16:00:24 JST
- Updated: 2026-02-18 16:00:24 JST

