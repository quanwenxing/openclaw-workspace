# hokanシリーズ調査レポート（一次情報優先）

作成日: 2026-02-10  
方針: 公式サイト・公式プロダクトページ・公式導入事例・公式方針ページを優先。  
制約: 非公開情報は「不明」と明記。

---

## 1) hokanシリーズの整理

## 1-1. 製品ラインナップ（確認できた範囲）

### A. hokan®（基盤CRM）
- 顧客・契約の一元管理
- 意向把握/比較推奨
- 満期更改・アフターフォロー
- テンプレート、ファイル管理、モバイル対応、CSV出力
- 共同ゲートウェイ/API/マジックインポート/外部サービス連携（DECHI, AS-BOX, Eight, Moneytree LINK）

出典:  
- https://hkn.jp/  
- https://hkn.jp/function/

### B. hokan CRM + 意向把握
- 意向把握・比較推奨・意向確認のデジタル化
- 高齢者募集確認、電子署名、永年保管、上長承認

出典:  
- https://hkn.jp/product/ikouhaaku/

### C. hokan CRM + 案件管理
- 見込客/満期更改等の進捗可視化
- 代理店独自プロセスのカスタマイズ
- アラートで記録漏れ防止

出典:  
- https://hkn.jp/product/ankenkanri/

### D. hokan CRM + レポート
- 業務・顧客属性・収益データの可視化/分析
- 毎日集計更新
- 監査ログオプション

出典:  
- https://hkn.jp/product/dashboard/

### E. hokan CRM + 出納
- 請求書発行、入出金照合、収支明細、精算照合
- 銀行API連携、帳票出力、CSV出力

出典:  
- https://hkn.jp/product/suitou/

### F. hokan CRM + ATOIKURA
- 成績証明書処理/集計の効率化を狙う領域（LP本文で課題提示を確認）
- 詳細機能は取得情報が限定的で一部不明

出典:  
- https://hkn.jp/product/atoikura/

### G. hokan CRM + People
- 従業員管理課題向け領域（取得テキストは限定）
- 詳細機能は不明

出典:  
- https://hkn.jp/product/people/

---

## 1-2. 機能

公式で確認できた主要機能（重複統合）:
- 顧客管理（個人/法人/世帯）
- 契約管理、保有契約一覧、契約検索
- 対応履歴（モバイル入力）
- 意向把握・比較推奨・意向確認
- 高齢者募集確認、上長承認
- 満期更改管理、アフターフォロー管理（苦情・事故等）
- カンバン型タスク管理
- 添付ファイル管理
- 分析/集計/収益系レポート
- 監査ログ（オプション）
- 請求/入出金/精算（出納）
- CSV export/import（文脈上、importはマジックインポート）

出典:  
- https://hkn.jp/function/  
- https://hkn.jp/product/suitou/  
- https://hkn.jp/product/ikouhaaku/  
- https://hkn.jp/product/ankenkanri/  
- https://hkn.jp/product/dashboard/

---

## 1-3. 対象ユーザー

- 保険代理店（乗合/企業内代理店を含む）
- 事例では、代理店に加え保険会社直販チャネルでの導入事例あり

出典:  
- https://hkn.jp/  
- https://hkn.jp/case/orixlife/

---

## 1-4. 価格

- hokan公式ページ上で定価表は確認できず（問い合わせ/資料請求導線中心）
- よって **公開価格は不明**

出典:  
- https://hkn.jp/  
- https://hkn.jp/contact/

---

## 1-5. 導入事例（抜粋）

- インターグ: API連携、自動同期、メモテンプレート活用、監査対応
  - https://hkn.jp/case/interg/
- オリックス生命: 直販チャネル初導入、営業可視化・育成支援
  - https://hkn.jp/case/orixlife/
- 三井物産インシュアランス: 情報一元化、プロジェクト機能、メンション連携
  - https://hkn.jp/case/mih/

---

## 1-6. 連携

- 共同ゲートウェイ連携（契約情報一括取込・メンテ）
- API連携（自社Web等）
- マジックインポート（Excel取込）
- 他社サービス連携（DECHI, AS-BOX, Eight, Moneytree LINK）

出典:  
- https://hkn.jp/function/  
- https://hkn.jp/

---

## 1-7. セキュリティ

corpサイトで明示されている事項:
- SSL通信
- 日次バックアップ
- Pマーク取得済み
- ISMS認証取得済み
- 二段階認証・画面ロック（生体認証含む）
- 情報セキュリティ基本方針（2019制定、2025/5/1最終改定）

出典:  
- https://www.corp.hkn.jp/security  
- https://www.corp.hkn.jp/info-security

補足: 認証番号・適用範囲（SoA範囲）の詳細は取得情報では確認できず **不明**。

---

## 1-8. 法規制観点

公式記載で確認できるポイント:
- 改正保険業法、監督指針への対応を訴求
- 意向把握・比較推奨・高齢者募集確認・証跡管理
- 個人情報保護法に沿うポリシー・開示請求対応手続きの明示

出典:  
- https://hkn.jp/function/  
- https://dairiten-system.com/（業界側比較の参考）  
- https://www.corp.hkn.jp/privacy-policy

---

## 2) 競合比較（3社以上）

| 観点 | hokan | i-Fit（ISネットワーク） | WiseOffice（NTTデータ） | YouWill-CRM |
|---|---|---|---|---|
| 主対象 | 保険代理店、企業代理店、事例上は直販にも展開 | 保険代理店 | 乗合代理店 | 保険代理店 |
| 基本機能 | 顧客/契約、意向把握、比較推奨、満期更改、案件、レポート、出納 | CRM + 事務機能（売上、チェックオフ等） | 顧客/契約一元化、態勢整備、権限、検索、履歴 | 顧客/契約、意向把握、比較推奨、満期、権限、手数料集計 |
| 連携 | 共同GW、API、Excel取込、他社連携 | 共同GW経由契約取込 | 保険会社データをNTTデータ共同GW経由で直接連携 | 共同GW/TNET/ISSファイル取込 |
| セキュリティ訴求 | SSL、日次バックアップ、Pマーク、ISMS、2段階認証 | 「各種リスク対策」記載（詳細は要問い合わせ） | NTTデータ運営・高度セキュリティ訴求 | ISMS取得、2段階認証 |
| 価格公開 | 不明（要問合せ） | 不明（要問合せ） | 不明（要問合せ） | Standard 3,000円/人、Core 2,000円/人（条件あり） |

出典:
- hokan: https://hkn.jp/ , https://hkn.jp/function/ , https://www.corp.hkn.jp/security
- i-Fit: https://www.isnetwork.co.jp/i-fit-lp/ , https://www.isnetwork.co.jp/service/
- WiseOffice: https://dairiten-system.com/
- YouWill-CRM: https://youwill-crm.com/

---

## 3) 調査結果をもとにした代替製品設計（ゼロベース）

## 3-1. 製品コンセプト

**製品名（試作）: AgencyCore**  
「代理店の顧客・契約・募集進捗・満期・内部統制を一気通貫で管理する軽量クラウド」

## 3-2. MVP要件（今回実装）

- 顧客管理
- 契約管理
- 満期リマインド（契約満期-60日デフォルト）
- 進捗パイプライン（opportunities）
- ダッシュボード
- 権限管理（RBAC）
- 監査ログ
- CSV入出力

## 3-3. 設計方針

- 代理店現場で使える最小コアに絞る
- 後続で共同GW/API接続可能な拡張余地を残す
- 「入力負荷の軽さ」と「監査追跡」の両立を優先

---

## 4) 実装サマリ（作成コード）

実装先:  
`/Users/username/.openclaw/workspace/hokan-alternative-mvp`

主ファイル:
- `app.py`（Flask + SQLite）
- `templates/login.html`
- `templates/dashboard.html`
- `requirements.txt`
- `README.md`

実装済み機能:
- ログイン/ログアウト
- ロール制御（viewer/agent/manager/admin）
- 顧客CRUD
- 契約登録・更新リマインダ生成
- 案件（パイプライン）
- リマインダ完了処理
- 監査ログ閲覧
- CSV export/import（customers/contracts）
- ダッシュボード（件数・60日以内満期）

動作確認:
- `/health` が `{"status":"ok"}` を返すことを確認

---

## 5) 不明点（推測回避）

- hokan公式の標準価格表（プラン単価、初期費用）: **不明**
- hokanの認証登録番号/適用範囲の詳細（Pマーク、ISMS）: **不明**
- hokan People/ATOIKURAの詳細機能一覧（取得テキスト上の詳細）: **一部不明**

---

## 6) 参考URL一覧

- https://hkn.jp/
- https://hkn.jp/function/
- https://hkn.jp/product/suitou/
- https://hkn.jp/product/ikouhaaku/
- https://hkn.jp/product/ankenkanri/
- https://hkn.jp/product/dashboard/
- https://hkn.jp/product/atoikura/
- https://hkn.jp/product/people/
- https://hkn.jp/case/interg/
- https://hkn.jp/case/orixlife/
- https://hkn.jp/case/mih/
- https://www.corp.hkn.jp/security
- https://www.corp.hkn.jp/info-security
- https://www.corp.hkn.jp/privacy-policy
- https://www.isnetwork.co.jp/i-fit-lp/
- https://www.isnetwork.co.jp/service/
- https://dairiten-system.com/
- https://youwill-crm.com/
