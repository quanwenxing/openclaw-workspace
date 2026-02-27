# Workspace Migration Status (2026-02-18)

## 実施内容（安全優先）

### 1) 参照影響が低いファイルの移動（完了）
- `docs/security/macmini_2026-02/` へ監査TXT 7件
- `docs/references/` へHTML 2件
- `research/ops/` へ分析メモ 3件
- `archive/misc/` へ `out_en.txt`
- `archive/delete-candidate/` へ `test_ja.pdf`, `test_html_ja.pdf`

### 2) AWS PDF群の移動（完了）
- `AWSCertifiedGenerativeAIDeveloper*.pdf` を `docs/aws/` へ移動

### 3) `translate_pdf_ja.py` のパス安全化（完了）
- 絶対パス固定を廃止
- デフォルトを `docs/aws/` に変更
- 旧配置（workspace直下）へのフォールバックを残した
- `SRC_PDF`, `OUT_PDF` 環境変数で明示指定可能

### 4) PQC資料の移動（完了）
- `research/pqc-roadmap/` へ `pqc-roadmap-slidev.*` 3件

## HOLD（未実施）
- `sources.yaml`（運用参照の確認が必要）
- `translate_pdf_ja.py` 本体の配置移動（現状は互換性優先でルート残置）

## 現在のルート直下（主要）
- コア運用ファイル + 主要プロジェクト + `sources.yaml` + `translate_pdf_ja.py`
- 一時・重複・監査・参考資料はサブディレクトリへ整理済み
