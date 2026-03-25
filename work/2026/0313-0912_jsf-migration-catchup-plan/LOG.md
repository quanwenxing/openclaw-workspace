# LOG.md

## 2026-03-13
- ユーザー依頼: Java 8 / JSF 1.2 で動くシステムを Java 21 / JSF 4 へ移行するプロジェクト企画に向け、短期キャッチアップ用ロードマップ作成。
- まず運用ルール・作業分離ルールを確認。
- Perplexity検索APIは未設定で利用不可だったため、一次情報サイトを直接参照して構成。

## 参照した主な情報源
1. Jakarta Faces 4.0 release page
   - https://jakarta.ee/specifications/faces/4.0/
2. Jakarta Faces 4.0 specification (HTML)
   - https://jakarta.ee/specifications/faces/4.0/jakarta-faces-4.0
3. Jakarta EE Platform 10 release page
   - https://jakarta.ee/specifications/platform/10/
4. Eclipse Mojarra project page
   - https://eclipse-ee4j.github.io/mojarra/
5. OmniFaces homepage / showcase
   - https://omnifaces.org/
   - https://showcase.omnifaces.org/
6. Oracle JDK 21 migration guide
   - https://docs.oracle.com/en/java/javase/21/migrate/getting-started.html

## 抽出した重要論点
- Faces 4 では JSP サポート削除、`@ManagedBean` など旧Managed Bean機構削除、`MethodBinding` / `ValueBinding` 削除。
- Faces 4 は Jakarta EE 10 世代。最低 Java 11 だが、今回は Java 21 想定。
- パッケージ/名前空間は `javax.*` から `jakarta.*` へ移行前提。
- JSF理解の最短経路は「ライフサイクル」「Facelets」「CDI managed bean」「画面遷移」「変換/検証」「Ajax」「コンポーネントライブラリ依存の把握」。
- 実案件では学習と並行して、現行資産棚卸し（JSP/Facelets、カスタムタグ、PrimeFaces/RichFaces等、アプリサーバ、認証、セッション、ファイルアップロード）を進める必要あり。
