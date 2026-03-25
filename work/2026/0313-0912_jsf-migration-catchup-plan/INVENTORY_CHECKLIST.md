# 現行システム棚卸しチェックリスト

## 目的
Java 8 / JSF 1.2 システムを Java 21 / Jakarta Faces 4 へ移行するにあたり、技術的な難所を早期に把握するためのチェックリスト。

---

## 1. 基本情報
- [ ] システム名
- [ ] 業務概要
- [ ] 利用ユーザー数 / 同時接続規模
- [ ] 主要業務フロー
- [ ] 画面数 / バッチ数 / 外部IF数
- [ ] 本番 / 検証 / 開発環境の構成

## 2. ビルド・配布形態
- [ ] Maven / Gradle / Ant / 独自
- [ ] WAR 単体 / EAR / 複数モジュール
- [ ] CI/CD 有無
- [ ] テスト自動化有無
- [ ] 依存ライブラリ一覧取得済み

## 3. 実行基盤
- [ ] 現行JDKバージョン
- [ ] 現行アプリサーバ名・バージョン
- [ ] Servlet / EL / CDI / JSTL の利用実態
- [ ] OS / ミドルウェア依存
- [ ] コンテナ利用有無

## 4. View層（最重要）
- [ ] `.jsp` / `.jspx` / `.xhtml` の比率確認
- [ ] Facelets 利用有無
- [ ] テンプレート構成有無
- [ ] include / tag file / composite component 利用有無
- [ ] `faces-config.xml` 利用有無
- [ ] `web.xml` の FacesServlet mapping 確認
- [ ] `http://xmlns.jcp.org/jsf/` など旧namespace利用確認

## 5. JSF管理Bean / CDI
- [ ] `@ManagedBean` 使用箇所
- [ ] `@ManagedProperty` 使用箇所
- [ ] `javax.faces.bean.*` 使用箇所
- [ ] `@Named` / CDI 利用有無
- [ ] Request/View/Session/Application scope の利用分布
- [ ] Beanサイズ肥大化有無

## 6. バリデーション / コンバータ
- [ ] 独自 `Converter` の数
- [ ] 独自 `Validator` の数
- [ ] Bean Validation 利用有無
- [ ] メッセージリソース管理方法
- [ ] 画面エラーメッセージ仕様確認

## 7. 画面部品 / UIライブラリ
- [ ] PrimeFaces 利用有無・バージョン
- [ ] RichFaces 利用有無
- [ ] ICEfaces / Tomahawk / Trinidad / その他利用有無
- [ ] OmniFaces 利用有無
- [ ] 独自タグ / 独自コンポーネント利用有無
- [ ] `MethodBinding` / `ValueBinding` 利用有無

## 8. Ajax / JavaScript
- [ ] `f:ajax` 利用有無
- [ ] a4j など旧Ajaxタグ利用有無
- [ ] JavaScript直書き依存有無
- [ ] jQuery等のフロント依存有無
- [ ] 部分更新 / モーダル / DataTable の難所把握

## 9. セッション / 認証 / 権限
- [ ] ログイン方式
- [ ] SSO連携有無
- [ ] コンテナ認証依存有無
- [ ] セッションタイムアウト仕様
- [ ] 権限制御の実装箇所

## 10. ファイル / 帳票 / 外部連携
- [ ] ファイルアップロード有無
- [ ] ファイルダウンロード有無
- [ ] PDF/帳票出力有無
- [ ] メール送信有無
- [ ] SOAP / REST / DB連携有無

## 11. Java / Jakarta移行影響
- [ ] `javax.*` 利用範囲
- [ ] JAXB / JAX-WS 利用有無
- [ ] JDK内部API依存有無
- [ ] 反射利用箇所
- [ ] 文字コード / 日付API / Security設定影響確認

## 12. テスト / 品質保証
- [ ] 単体テスト有無
- [ ] 結合テスト手順有無
- [ ] 回帰テスト観点一覧有無
- [ ] 自動UIテスト有無
- [ ] 性能テスト有無

## 13. 代表画面選定
- [ ] 入力中心画面
- [ ] 一覧検索画面
- [ ] Ajax多用画面
- [ ] ファイル処理画面
- [ ] 権限制御が複雑な画面

## 14. 初期判定
### 高リスク条件
- [ ] JSP中心
- [ ] `@ManagedBean` 多数
- [ ] RichFaces等の旧ライブラリ依存
- [ ] 独自コンポーネント多数
- [ ] テスト資産不足

### 中リスク条件
- [ ] Facelets化済だが `javax.*` 依存が広い
- [ ] PrimeFaces等のバージョン差が大きい
- [ ] アプリサーバ依存が強い

### 低リスク条件
- [ ] XHTML / Facelets中心
- [ ] CDI化が進んでいる
- [ ] UI依存が軽い
- [ ] テスト資産がある

---

## grepで先に当てる候補
- `@ManagedBean`
- `@ManagedProperty`
- `javax.faces.bean`
- `MethodBinding`
- `ValueBinding`
- `\.jsp$`
- `\.jspx$`
- `faces-config.xml`
- `rich:`
- `a4j:`
- `ice:`
- `t:`
- `p:`
- `xmlns.jcp.org/jsf`
- `javax.`
