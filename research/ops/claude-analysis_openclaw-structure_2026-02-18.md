# Claude による `.openclaw` ディレクトリ構造分析

**分析日**: 2026-02-18
**分析者**: Claude (claude-sonnet-4-6)
**対象**: `/Users/username/.openclaw/`

---

## ディレクトリ全体像

```
~/.openclaw/
├── agents/                     # エージェント設定・セッション
├── browser/                    # Chrome拡張 + ブラウザユーザーデータ
├── canvas/                     # キャンバスUI (index.html)
├── completions/                # シェル補完スクリプト (bash/fish/ps1/zsh)
├── credentials/                # 認証情報 (telegram/discord の allowFrom, pairing)
├── cron/                       # cronジョブ定義 + 実行ログ (runs/)
├── delivery-queue/             # メッセージ配信キュー
├── devices/                    # ペアリング済みデバイス情報
├── identity/                   # デバイス認証情報
├── logs/                       # ゲートウェイ・コマンドログ
├── media/                      # 受信メディア (browser/, inbound/)
├── mlx-whisper/                # ★ Pythonプロジェクト (gitリポジトリ) — 要検討
├── subagents/                  # サブエージェント実行記録
├── telegram/                   # Telegram offset管理
├── workspace/                  # 主な作業スペース (55エントリ混在) — 要整理
├── openclaw.json               # メイン設定ファイル
├── openclaw.json.bak           # バックアップ
├── openclaw.json.bak.1         # ★ 削除候補
├── openclaw.json.bak.2         # ★ 削除候補
├── openclaw.json.bak.3         # ★ 削除候補
├── openclaw.json.bak.4         # ★ 削除候補
└── update-check.json           # アップデート確認用
```

---

## 問題点の詳細

### 問題1: `openclaw.json` バックアップの散乱

ルート直下に `.bak` 〜 `.bak.4` の計5ファイルが存在。
手動または自動で積み上がったもので、古い世代は不要と思われる。

### 問題2: `workspace/` の混在 (55エントリ)

性質の異なるものがフラットに混在している。

#### PDF 試行錯誤の残骸（削除候補多数）
| ファイル | 状況 |
|---|---|
| `AWSCertifiedGenerativeAIDeveloper_ja.pdf` | おそらく最終版 |
| `AWSCertifiedGenerativeAIDeveloper.pdf` | 英語版 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p1.pdf` | 分割・変換試行の残骸 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p1a.pdf` | 〃 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p1b.pdf` | 〃 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p2〜4.pdf` | 〃 |
| `AWSCertifiedGenerativeAIDeveloper_ja_part1〜2.pdf` | 〃 |
| `AWSCertifiedGenerativeAIDeveloper_ja_small.pdf` | 〃 |
| `AWSCertifiedGenerativeAIDeveloper_ja_split01〜06.pdf` | 〃 |
| `AWSCertifiedGenerativeAIDeveloper_ja_tg.pdf` | 〃 |
| `pqc-roadmap-slidev.pdf` | スライド最終版？ |
| `pqc-roadmap-slidev-styled.pdf` | 〃の別バージョン |
| `test_ja.pdf` | ★ テスト残骸 → 削除推奨 |
| `test_html_ja.pdf` | ★ テスト残骸 → 削除推奨 |

#### セキュリティ監査テキスト（整理・移動候補）
```
macmini_security_audit_20260204_135636.txt
macmini_security_audit_addendum_20260204_135650.txt
macmini_security_audit_ssh_20260204_135704.txt
macmini_security_audit_ssh_d_20260204_135710.txt
macmini_security_listeners_20260205_101355.txt
macmini_security_post_gui_disable_20260205_101350.txt
macmini_open_ports_full_20260205_101754.txt
```
→ `audits/` サブディレクトリに移動推奨

#### テスト・一時ファイル（削除候補）
- `test_ja.pdf`, `test_html_ja.pdf` — テスト用生成物
- `out_en.txt` — 用途不明の出力ファイル

#### HTMLスナップショット（`references/` への移動候補）
- `codex_gpt-5.3-codex_overview_2026-02-06.html`
- `dexter_guide_ja.html`

#### Node.js 残骸（要確認）
- `node_modules/`, `package.json`, `package-lock.json` — 親プロジェクト不明。`markets/` か別プロジェクトに属するはずが誤って workspace 直下に残っている可能性。

#### 実プロジェクト（`projects/` への移動候補）
- `crypto-arb-bot/`
- `hokan-alternative-mvp/`
- `markets/`
- `numerai-example-scripts/`

#### 管理ファイル（現状維持）
- `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `IDENTITY.md`, `HEARTBEAT.md`
- `memory/`, `skills/`, `reports/`
- `sources.yaml`, `.env`

### 問題3: `mlx-whisper/` の配置

独立したgitリポジトリ兼Pythonプロジェクト（`uv` 管理、`.venv` 含む）が
openclawのシステムディレクトリ直下に混在。
`workspace/projects/mlx-whisper/` への移動を推奨（ただし設定でパス参照がないか要確認）。

### 問題4: ログの肥大化

| ファイル | サイズ | 行数 |
|---|---|---|
| `logs/gateway.err.log` | 264KB | 3,739行 |
| `logs/gateway.log` | 77KB | 989行 |
| `logs/commands.log` | 1.6KB | 12行 |

`gateway.err.log` が自動ローテーションなしで肥大化している。

---

## 整理案

### 推奨ディレクトリ構造 (`workspace/`)

```
workspace/
├── projects/          # 実プロジェクト
│   ├── crypto-arb-bot/
│   ├── hokan-alternative-mvp/
│   ├── markets/
│   └── numerai-example-scripts/
├── study/             # 学習資料
│   ├── aws-certified-generative-ai/   # AWS PDF 最終版のみ
│   └── pqc-roadmap/                   # PQC関連
├── audits/            # セキュリティ監査レポート
│   └── macmini_2026-02/               # 監査テキスト群
├── references/        # 外部資料・HTMLスナップショット
├── memory/            # (現状維持)
├── skills/            # (現状維持)
├── reports/           # (現状維持)
├── AGENTS.md
├── MEMORY.md
├── SOUL.md
├── IDENTITY.md
├── HEARTBEAT.md
└── sources.yaml
```

### 優先順位別アクションリスト

| 優先度 | アクション | 内容 |
|---|---|---|
| 高 | PDF削除 | `test_*.pdf`, `out_en.txt` を削除。AWS PDF は最終版2個（ja + en）のみ残す |
| 高 | workspace 分類 | `projects/`, `study/`, `audits/`, `references/` 作成して移動 |
| 中 | バックアップ削除 | `openclaw.json.bak.1〜.4` を確認後削除（`.bak` 1世代は保持） |
| 低 | mlx-whisper 移動 | `workspace/projects/` または `~/projects/` へ移動 |
| 低 | ログローテーション | `gateway.err.log` の定期クリア/ローテーション設定 |
| 低 | node_modules 整理 | 親プロジェクト特定後、workspace直下から移動 or 削除 |
