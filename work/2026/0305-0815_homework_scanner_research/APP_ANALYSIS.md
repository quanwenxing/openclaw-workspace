# 競合アプリ「宿題スキャナー / GradeUp」の技術分析

## 1. 運営元
- **社名**: PIXELCELL PTE. LIMITED (シンガポール)
- **インフラ**: AWS (Amazon Web Services)
- **API**: `app-service.homeworkhelperai.com`

## 2. 推定コード構成
- **フロントエンド**: Swift (iOS) / Kotlin (Android)
- **バックエンド**: Python (FastAPI/Django) がAWS LambdaやEC2上で稼働。
- **コアエンジン**: 
    - サードパーティ製教育AI SDKの統合。
    - クラウド型OCR + 数式認識 (LaTeX) + 検索エンジン。

## 3. 独自開発への示唆
- 競合は複数の特化型APIを組み合わせているが、最新のマルチモーダルLLM (Gemini 1.5等) はこれらをシングルパスで処理可能。
- 週末プロジェクトとしては、**「AIに完璧なJSONを吐かせる」**ことが成功の9割を握る。
