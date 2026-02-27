# MEMORY.md

## 運用ルール（ユーザー明示）
- モデル変更時は、モデル名を必ず公式ドキュメントで確認してから実施する。
- 未確認のモデル名で変更・案内をしない。
- 同種ミス防止のため、モデル関連の操作前に確認を必須化する。
- 2026-02-18: タスク完了時の「この内容をスキル化するか？」確認は不要（ユーザー明示）。
- 2026-02-15: Discord/Telegramで音声メッセージ受信時は、Whisper(MLX)で文字起こししてから内容確認・応答する運用を希望。
- 2026-02-24: 依頼作業は workspace直下で行わず、必ず `work/YYYY/MMDD-HHMM_<task-slug>/` で実施。作業履歴は `WORK_INDEX.md` と `work/index.json` で一元管理する運用を希望。
- 2026-02-24: 新セッションでは過去チャネル表示の混在を避け、現在セッションの実チャネル情報（inbound metadata）を優先して案内する。
- 2026-02-27: Todoist操作（「todo追加」「todoist確認」等）は `todoist`/`todoist-cli` の有無だけで不可判定しない。まず `mcporter list` でTodoist MCP可用性を確認し、利用可能なら `mcporter call todoist.*` で実行する。
