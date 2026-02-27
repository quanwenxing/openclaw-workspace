# `.openclaw/` ディレクトリ構造分析レポート

> 分析日: 2026-02-18
> 分析者: Claude (claude-sonnet-4-6)

---

## 1. `.openclaw/` ルート構造

```
.openclaw/
├── agents/
├── browser/
├── canvas/
├── completions/        # シェル補完スクリプト (bash/fish/ps1/zsh)
├── credentials/
├── cron/
├── delivery-queue/
├── devices/
├── identity/
├── logs/
├── media/
├── mlx-whisper/
├── subagents/
├── telegram/
├── workspace/
├── openclaw.json           ← メイン設定
├── openclaw.json.bak       ← バックアップ (5個散乱 ⚠️)
├── openclaw.json.bak.1
├── openclaw.json.bak.2
├── openclaw.json.bak.3
├── openclaw.json.bak.4
└── update-check.json
```

### 問題点
- `openclaw.json.bak.*` が5個ルートに散乱している
- 整理方針: `backups/` フォルダにまとめるか、最新1〜2個を残して削除

---

## 2. `workspace/` 内の問題

### 2-1. PDFファイルの大量重複・断片化 ⚠️

`AWSCertifiedGenerativeAIDeveloper` 関連のPDFが **13個以上** 存在。
これはPDF分割・変換の試行錯誤の残骸と推察される。

| ファイル | サイズ | 状態 |
|---|---|---|
| `AWSCertifiedGenerativeAIDeveloper.pdf` | 24.7 MB | 英語原本 |
| `AWSCertifiedGenerativeAIDeveloper_ja.pdf` | 106 MB | 日本語翻訳版（元） |
| `AWSCertifiedGenerativeAIDeveloper_ja_part1.pdf` | 93.2 MB | 分割版 |
| `AWSCertifiedGenerativeAIDeveloper_ja_part2.pdf` | 10.4 MB | 分割版 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p1.pdf` | 87.1 MB | 別分割 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p1a.pdf` | 83.1 MB | 別分割 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p1b.pdf` | 4.4 MB | 別分割 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p2.pdf` | 6.5 MB | 別分割 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p3.pdf` | 5.6 MB | 別分割 |
| `AWSCertifiedGenerativeAIDeveloper_ja_p4.pdf` | 5.5 MB | 別分割 |
| `AWSCertifiedGenerativeAIDeveloper_ja_split01.pdf` | 32.6 MB | さらに別分割 |
| `AWSCertifiedGenerativeAIDeveloper_ja_split02〜06.pdf` | 各数〜47 MB | さらに別分割 |
| `AWSCertifiedGenerativeAIDeveloper_ja_small.pdf` | **0 bytes** | 空ファイル ❌ |
| `AWSCertifiedGenerativeAIDeveloper_ja_tg.pdf` | **0 bytes** | 空ファイル ❌ |
| `test_ja.pdf` | 26.6 MB | 変換テスト産物 |
| `test_html_ja.pdf` | 30.2 MB | 変換テスト産物 |

**削除候補**: `_small.pdf`、`_tg.pdf`（0バイト）、`test_*.pdf`、重複分割ファイル群

---

### 2-2. ルートへの散乱ファイル ⚠️

プロジェクト・ドキュメント・ログ・スクリプトが `workspace/` ルートに混在:

**セキュリティ監査レポート群** (2026-02-04〜05):
- `macmini_security_audit_20260204_135636.txt`
- `macmini_security_audit_addendum_20260204_135650.txt`
- `macmini_security_audit_ssh_20260204_135704.txt`
- `macmini_security_audit_ssh_d_20260204_135710.txt`
- `macmini_security_listeners_20260205_101355.txt`
- `macmini_security_post_gui_disable_20260205_101350.txt`
- `macmini_open_ports_full_20260205_101754.txt`

**その他の散乱ファイル**:
- `codex_gpt-5.3-codex_overview_2026-02-06.html`
- `dexter_guide_ja.html`
- `translate_pdf_ja.py` / `translate_pdf_ja.log`
- `pqc-roadmap-slidev.md` / `pqc-roadmap-slidev.pdf` / `pqc-roadmap-slidev-styled.pdf`
- `sources.yaml`
- `out_en.txt`
- `棚卸し_2026-02-03.md`
- `package.json` / `package-lock.json` / `node_modules/`（どのプロジェクトに属するか不明）

---

### 2-3. プロジェクト間の分類なし

以下のプロジェクトが同列に並んでいる（カテゴリ分けなし）:

| ディレクトリ | 内容推察 |
|---|---|
| `crypto-arb-bot/` | 暗号資産アービトラージBot |
| `hokan-alternative-mvp/` | 保管系サービスのMVP |
| `markets/` | マーケットデータ関連 |
| `numerai-example-scripts/` | Numerai ML スクリプト |
| `udemy-mock/` | Udemy風モック試験 |
| `memory/` | メモリ管理ファイル |
| `skills/` | スキル定義 |
| `reports/` | レポート出力 |

---

## 3. 整理案

### 案A: `workspace/` を目的別に再編成

```
workspace/
├── projects/               # 開発プロジェクト
│   ├── crypto-arb-bot/
│   ├── hokan-alternative-mvp/
│   ├── markets/
│   ├── numerai-example-scripts/
│   └── udemy-mock/
│
├── docs/                   # 参考資料（読み取り専用）
│   ├── aws/                # AWSのPDF → 元ファイル1〜2本に集約
│   └── security/           # macmini_security_*.txt をまとめる
│
├── research/               # 調査・分析アウトプット
│   ├── pqc-roadmap.*
│   └── codex_*.html
│
├── tmp/                    # 一時作業ファイル（定期削除対象）
│   └── translate_pdf_ja.*
│
└── [コアファイル]           # AGENTS.md, MEMORY.md, SOUL.md 等はルートに残す
```

### 案B: `.openclaw/` バックアップの整理

```
.openclaw/
└── backups/
    └── openclaw.json.bak.* ← 一箇所にまとめる（または最新2個残し削除）
```

---

## 4. 削除候補リスト（要確認）

| ファイル | 削除理由 |
|---|---|
| `AWSCertifiedGenerativeAIDeveloper_ja_small.pdf` | 0バイト |
| `AWSCertifiedGenerativeAIDeveloper_ja_tg.pdf` | 0バイト |
| `test_ja.pdf` | 変換テストの産物 |
| `test_html_ja.pdf` | 変換テストの産物 |
| 分割PDF群 (`_p1a`, `_p1b`, `_split01〜06` 等) | 元PDF + 必要な分割版で代替可能 |
| `translate_pdf_ja.log` | 作業ログ、不要なら削除 |
| `openclaw.json.bak.2〜4` | 古いバックアップ |

---

## 5. 優先度まとめ

| 優先度 | アクション |
|---|---|
| 高 | AWS PDF重複ファイルの整理・削除 (ディスク容量 ~500MB相当) |
| 高 | 0バイトPDFの削除 |
| 中 | セキュリティレポートを `docs/security/` にまとめる |
| 中 | `openclaw.json.bak.*` を `backups/` にまとめる |
| 低 | プロジェクトを `projects/` 配下に再編成 |
| 低 | `package.json` / `node_modules` の帰属整理 |
