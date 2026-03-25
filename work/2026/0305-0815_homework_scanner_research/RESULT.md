# 週末プロジェクト：PDF再構成型宿題スキャナー

## 1. 開発構成
- **言語**: Python 3.10+
- **モデル**: Gemini 1.5 Flash (OCR性能とコストのバランスが良い)
- **PDF生成**: [ReportLab](https://www.reportlab.com/) (PythonでPDFを生成する標準ライブラリ)
- **UI (オプション)**: Streamlit (ブラウザで操作) or CLI (ターミナルで実行)

## 2. ワークフロー
1. `input/` フォルダに写真を置く。
2. スクリプト実行。
3. Gemini APIが画像を読み取り、手書きを無視して問題だけをJSON抽出。
4. ReportLabがJSONを読み込み、A4サイズの綺麗なPDFファイルを `output/` に生成。

## 3. 必要なライブラリ
```bash
pip install google-generativeai pillow reportlab
```

## 4. 2日間のスケジュール
### Day 1: AI抽出とデータ構造化
- APIのプロンプト調整（手書きの除去、数式のLaTeX化など）。
- JSON形式での安定したデータ取得。

### Day 2: PDF自動生成と自動化
- ReportLabによるレイアウト定義（タイトル、問題番号、余白の配置）。
- 複数ファイルの一括処理。

## 5. 競合アプリの推定技術
- **手法**: **"EraseNet"** (筆跡除去に特化したGAN) や中国系教育AI（Zuoyebang/Baidu等）のSDK活用の可能性大。
- **調査テクニック**: 
    - **Acknowledgements**: アプリ内のライセンス表示をチェック（OpenCV, PaddleOCRなどの有無）。
    - **Proxyツール**: `Charles` や `Proxyman` で通信を見抜き、外部API（クラウド処理）かエッジAI（端末内処理）かを判別。
    - **論文検索**: "Handwriting Removal GAN paper" で検索。

