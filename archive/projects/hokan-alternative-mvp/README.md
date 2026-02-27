# Insurance Agency MVP (hokan代替プロトタイプ)

保険代理店向けの最小実装（MVP）です。以下を実装しています。

- 顧客管理（Customers）
- 契約管理（Contracts）
- 更新リマインド（Reminders）
- 進捗パイプライン（Opportunities）
- 簡易ダッシュボード（件数・満期近接）
- 権限管理（viewer/agent/manager/admin）
- 監査ログ（Audit Logs）
- CSV入出力（customers/contracts）

---

## セットアップ

```bash
cd /Users/username/.openclaw/workspace/hokan-alternative-mvp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

起動後:
- http://127.0.0.1:5001/login
- 初期管理者: `admin / admin1234`

> 本番運用前に必ず `SECRET_KEY` と初期パスワードを変更してください。

---

## アーキテクチャ

- **Backend**: Flask
- **DB**: SQLite (`app.db`)
- **認証**: セッションベース
- **権限**: ロールベース（viewer < agent < manager < admin）
- **監査**: 主要操作（login/logout/create/update/delete/import/export）を `audit_logs` へ記録
- **CSV**: 
  - Export: `/csv/export/<entity>`
  - Import: `/csv/import/<entity>`

### データモデル（主要）
- `users`
- `customers`
- `contracts`
- `opportunities`
- `reminders`
- `audit_logs`

---

## 主要API

- `GET /customers` / `POST /customers` / `PUT /customers/<id>` / `DELETE /customers/<id>`
- `GET /contracts` / `POST /contracts`
- `GET /opportunities` / `POST /opportunities`
- `GET /reminders` / `POST /reminders/<id>/done`
- `GET /users` / `POST /users`（admin）
- `GET /audit-logs`（manager以上）
- `GET /csv/export/<entity>`（manager以上）
- `POST /csv/import/<entity>`（manager以上）

---

## 未実装・今後の拡張

1. UI強化（現状は最小画面 + API中心）
2. SSO/MFAの本格実装（現状はセッション + 任意の2段階認証未実装）
3. 詳細なワークフロー（意向把握・比較推奨のテンプレートエンジン）
4. 共同GW/APIの実接続
5. 通知チャネル（メール/SMS/Slack）
6. 論理削除・監査証跡の改ざん耐性（WORM等）
7. テスト自動化（unit/integration/e2e）
8. マルチテナント分離（現状は単一DB）

---

## 法令対応で注意すべき点（実運用前チェック）

本MVPは**業務検証用**です。実運用には以下を必須確認してください。

1. **個人情報保護法（APPI）**
   - 利用目的の特定、公表、第三者提供管理、開示等請求対応
   - 委託先管理・越境移転時の追加措置
2. **保険業法・監督指針**
   - 意向把握、比較推奨、高齢者募集、募集記録の保存/監査
3. **電子帳簿保存法・証憑管理**
   - 電子保存要件、検索性、真実性確保
4. **不正アクセス防止・情報セキュリティ**
   - ログ監視、アクセス制御、脆弱性対応、バックアップ/復旧訓練
5. **社内規程との整合**
   - 権限分掌、職務分離、内部監査プロセス

---

## ライセンス

検証用コード。商用利用時は法務・セキュリティ・監査部門のレビューを実施してください。
