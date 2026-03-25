# Java 8 / JSF 1.2 → Java 21 / Jakarta Faces 4
# 企画書向け要約版（A4 1〜2枚想定）

## 1. 企画の背景
現行システムは **Java 8 + JSF 1.2** で稼働しており、保守性・将来互換性・実行基盤更新の観点から、**Java 21 + Jakarta Faces 4** への移行を検討する。

本件は単なるJDK更新ではなく、以下を同時に含む複合移行である。
- Java 8 → Java 21
- Java EE / `javax.*` → Jakarta EE / `jakarta.*`
- JSF 1.2 → Jakarta Faces 4
- アプリサーバ / 周辺ライブラリ / ビルド・運用基盤更新

## 2. 重要ポイント
### 最優先で確認すべき3点
1. **現行ViewがJSPかXHTMLか**
   - Faces 4ではJSPサポートが削除されているため、JSPベースの場合は単純移行不可。
2. **旧 managed bean 機構への依存**
   - `@ManagedBean` / `@ManagedProperty` 等は Faces 4 では削除済み。
   - CDI (`@Named`, `@RequestScoped`, `@ViewScoped` 等) へ移行が必要。
3. **UIコンポーネントライブラリ依存**
   - RichFaces / ICEfaces / Tomahawk / 旧PrimeFaces / 独自タグ依存は高リスク。

## 3. 想定リスク
- JSP → Facelets(XHTML) 再構成が必要
- `MethodBinding` / `ValueBinding` 依存コードが存在
- `javax.*` → `jakarta.*` の変更が広範囲
- 実行基盤（Tomcat/WebLogic/JBoss等）とライブラリの整合性確保が必要
- 画面回帰テスト不足により、移行後不具合検出が遅れる可能性

## 4. 進め方（推奨）
### Phase 1: 事前調査 / キャッチアップ（7週間）
- JSF/Faces基礎理解
- 非互換ポイント調査
- 現行資産棚卸し
- 代表画面PoC
- リスク・移行方式・概算WBS整理

### Phase 2: 技術検証
- 代表画面移植
- 実行基盤候補比較
- ライブラリ置換可否確認
- テスト方針策定

### Phase 3: 本格移行
- 共通基盤更新
- 画面群単位の移行
- 総合試験 / 性能確認 / 本番切替

## 5. 7週間キャッチアップのゴール
7週間終了時点で以下を揃える。
- JSF/Faces 4 基礎理解
- 非互換一覧
- 現行資産棚卸し結果
- 代表画面PoC結果
- 移行方式案比較
- リスク一覧
- 初期WBS / 次アクション

## 6. 推奨判断
本件は **学習だけ先行** より、**学習と現行資産棚卸しを並行** する方が妥当。  
理由は、移行難易度の大半が JSF文法ではなく、**現行資産の作られ方（JSP/managed bean/ライブラリ/サーバ依存）** で決まるため。

## 7. 直近アクション
1. 現行資産の技術棚卸し
2. 代表画面3〜5本選定
3. 非互換ポイント初期評価
4. Java 21 / Jakarta Faces 4 のPoC実施
5. 概算スケジュールと体制案作成

## 出典
- Jakarta Faces 4.0 Release Page: https://jakarta.ee/specifications/faces/4.0/
- Jakarta Faces 4.0 Specification: https://jakarta.ee/specifications/faces/4.0/jakarta-faces-4.0
- Jakarta EE 10 Platform: https://jakarta.ee/specifications/platform/10/
- Eclipse Mojarra: https://eclipse-ee4j.github.io/mojarra/
- OmniFaces: https://omnifaces.org/
- Oracle JDK 21 Migration Guide: https://docs.oracle.com/en/java/javase/21/migrate/getting-started.html
