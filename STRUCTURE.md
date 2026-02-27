# STRUCTURE.md

## 公式ディレクトリ構造

```text
workspace/
├── projects/        # 開発プロジェクト（継続運用）
├── docs/            # 参照資料（PDF/HTML/一次情報）
├── research/        # 調査・分析レポート
├── tmp/
│   └── sessions/    # 作業中フォルダ（セッション単位）
├── archive/         # 旧版・中間生成物・退避物
├── scripts/         # 運用スクリプト
└── [core files]     # AGENTS.md / MEMORY.md / SOUL.md など
```

## 配置基準
- **projects/**: 実行可能コード、継続更新する成果
- **docs/**: 読み物、配布物、固定参照
  - 運用設定ファイル（例: RSSソース定義）: `docs/ops/`
- **research/**: 要約、比較、検証結果、提案書
- **tmp/sessions/**: 作業途中のみ
- **archive/**: もう現行ではないが保管したいもの

## 禁止事項
- ルート直下へのテスト出力常設
- 「final」「latest」など曖昧命名の乱立
