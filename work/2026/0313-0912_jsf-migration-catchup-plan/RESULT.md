# Java 8 / JSF 1.2 → Java 21 / Jakarta Faces 4
# 7週間キャッチアップ計画

作成日: 2026-03-13  
対象: **JSF未経験の担当者が、短期間で移行プロジェクト企画を主導できるレベルへ到達するための計画**

---

## 0. 結論：7週間で目指す到達点

7週間で目指すのは、**JSFの達人になることではなく、移行プロジェクトを安全に企画・分解・説明できること**。

到達目標は以下。

1. **JSF/Jakarta Faces の基本動作を説明できる**  
   - リクエストライフサイクル
   - managed bean / CDI
   - Facelets
   - バリデーション / コンバータ / Ajax / ナビゲーション

2. **JSF 1.2 → Faces 4 の非互換ポイントを把握している**  
   - `javax.*` → `jakarta.*`
   - JSP削除
   - `@ManagedBean` 系削除
   - `MethodBinding` / `ValueBinding` 削除
   - XML namespace / 設定差分

3. **実システム棚卸しと移行難所の仮説を立てられる**  
   - JSPかFaceletsか
   - 画面部品ライブラリ（PrimeFaces / RichFaces / ICEfaces / 独自タグ）
   - アプリサーバ依存
   - セッション / 認証 / 例外処理 / ファイルUpload / バッチ連携

4. **PoC計画・工数感・リスク一覧を作れる**

---

## 1. 大前提：この案件で本当に危険な論点

今回の移行は、単なるJDK更新ではなく、**実質4本の移行が同時に走る** タイプ。

1. **Java 8 → Java 21**
2. **Java EE / javax 系 → Jakarta EE / jakarta 系**
3. **JSF 1.2 → Jakarta Faces 4**
4. **周辺ライブラリ・アプリサーバ更新**

つまり、学習計画も「JSFの勉強」だけでは足りない。  
**企画上は、JSFそのもの 4割 / 周辺依存 4割 / PoCと棚卸し 2割** くらいで考えるのが現実的。

特に危険なのは次の3つ。

### 危険1: 現行が JSP ベースの可能性
Faces 4 では **JSPサポートが削除** されている。  
もし現行画面が `.jsp` / `.jspx` ベースなら、**単純移行ではなく View 層の作り直しに近い**。

### 危険2: `@ManagedBean` / 旧JSF管理Bean依存
Faces 4 では **native managed bean 機構が削除**。  
CDI (`@Named`, `@RequestScoped`, `@ViewScoped`, など) への置換が必要。

### 危険3: コンポーネントライブラリ依存
古い JSF 1.2 世代では、PrimeFaces 以前/初期版、RichFaces、ICEfaces、Tomahawk、独自タグなどが混在しやすい。  
この依存が強いと、**ライブラリ選定からやり直し** になる可能性がある。

---

## 2. 7週間の進め方

- **Week 1-2:** JSF/Faces の仕組みを短期間で把握
- **Week 3:** 旧JSF 1.2 と Faces 4 の差分理解
- **Week 4:** 実システム棚卸しと移行論点整理
- **Week 5:** Java 21 / Jakarta EE 10 / アプリサーバ観点の整理
- **Week 6:** 小さな PoC と移行方式の比較
- **Week 7:** 企画書・リスク・概算WBS化

学習時間の目安は、**平日1.5〜2時間 + 週末4〜6時間**。  
7週間で **合計90〜110時間** 程度を想定。

---

# 3. 週次詳細計画

## Week 1: JSFの全体像を最短で掴む

### 目的
「JSFって何をしているのか」を説明できるようになる。

### 学習テーマ
- JSF / Jakarta Faces の役割
- MVCの中での位置づけ
- リクエスト処理ライフサイクル
- コンポーネントツリー
- Backing Bean の役割
- Facelets の基本構文

### この週で最低限理解すべきこと
- 画面は単なるHTMLテンプレートではなく、**サーバ側コンポーネントツリー** として扱われる
- フォーム送信時に **Restore View → Apply Request Values → Process Validations → Update Model Values → Invoke Application → Render Response** の流れで動く
- 変換/検証エラー時にどのフェーズで止まるか
- `h:form`, `h:inputText`, `h:commandButton`, `h:messages`, `f:ajax` の役割

### やること
1. Jakarta Faces 4.0 spec の **Overview** と **Request Processing Lifecycle** を読む
2. Mojarra の Hello World 相当を読む
3. Hello World の画面と Bean の対応を自分の言葉で説明できるようにする
4. A4 1枚で「JSFの処理の流れ」メモを作る

### アウトプット
- 「JSFライフサイクル6フェーズ」説明メモ
- `input -> validation -> model update -> action` の因果関係メモ

### 理解確認チェック
- `immediate="true"` が何に効くかをざっくり説明できるか
- バリデーション失敗時に action が呼ばれない理由を説明できるか
- なぜ JSF は“状態を持つフレームワーク”と呼ばれるか説明できるか

---

## Week 2: Facelets / Bean / Scope / Navigation を掴む

### 目的
画面・Bean・スコープ・画面遷移の基礎を理解する。

### 学習テーマ
- Facelets の構文
- EL式 `#{...}`
- CDI bean と scope
- 画面遷移（action / outcome / redirect）
- 画面テンプレート / includes / composite components の概念

### 優先度高
- `@Named`
- `@RequestScoped`
- `@ViewScoped`
- `@SessionScoped`
- `faces-config.xml` の役割縮小
- `web.xml` / FacesServlet mapping の考え方

### やること
1. Facelets でフォーム画面を読む
2. CDI スコープの違いを整理する
3. 画面遷移方法（戻り値文字列、redirect、GETパラメータ）を整理する
4. テンプレート / include / composite component の違いを調べる

### 実務で重要な理解
- JSFでは **ViewScoped の寿命理解** が事故防止に直結する
- SessionScoped の濫用はメモリ・不具合の温床
- 旧 managed bean と CDI managed bean は移行時の重要論点

### アウトプット
- scope比較表
- navigationパターン一覧
- Faceletsタグの基本チートシート

---

## Week 3: JSF 1.2 と Faces 4 の差分を集中把握する

### 目的
「どこが壊れるか」を先に知る。

### 学習テーマ
- JSF 1.2 時代の典型実装
- JSF 2.x で追加された主要概念（Facelets標準化、Ajax、CDI寄り設計、ViewScoped など）
- Faces 4 で消えたもの / 変わったもの
- `javax` → `jakarta`

### 重点差分
1. **JSP廃止**  
   現行が JSP なら大きな改修前提。

2. **`@ManagedBean` 系削除**  
   CDIへ置換が必要。

3. **`MethodBinding`, `ValueBinding` 削除**  
   古いカスタムコンポーネントやライブラリ依存コードは危険。

4. **XML namespace 変更**  
   `http://xmlns.jcp.org/jsf/...` から新しい Jakarta Faces 向け記法へ寄る必要あり。

5. **周辺ライブラリの世代断絶**  
   旧ライブラリが Jakarta 対応していないと置換が必要。

### やること
1. Faces 4 release notes を読む
2. 現行システムのソースから以下を grep する
   - `@ManagedBean`
   - `javax.faces.bean`
   - `MethodBinding`
   - `ValueBinding`
   - `.jsp`, `.jspx`
   - `faces-config.xml`
   - `rich:`, `a4j:`, `ice:`, `t:`, `p:` 等のタグプレフィックス
3. 「そのまま移せる/そのままは無理」を分類する

### アウトプット
- 非互換一覧表
- 旧資産の危険度マップ（高/中/低）

---

## Week 4: 実システム棚卸しをする

### 目的
学習から企画へ移る。実案件の論点を洗い出す。

### 棚卸し観点

#### A. View 層
- JSP / JSPX / XHTML の比率
- Facelets化済みか
- テンプレート利用有無
- カスタムタグ / composite component / tag file

#### B. Managed Bean / Controller 層
- `@ManagedBean` / `@ManagedProperty` 使用有無
- scope の分布
- Beanサイズの肥大化
- actionメソッドの責務肥大化

#### C. Validation / Converter
- 独自 `Converter` / `Validator`
- メッセージ資源
- Bean Validation 利用状況

#### D. Ajax / UI ライブラリ
- PrimeFaces / RichFaces / ICEfaces / Tomahawk / OmniFaces
- JavaScript 直書き依存
- ファイルアップロード / ダイアログ / DataTable

#### E. インフラ / ランタイム
- 現行アプリサーバ（Tomcat / WebLogic / JBoss / WebSphere 等）
- JNDI / Security / SSO
- JSTL / Servlet / CDI / EL の依存関係
- WAR / EAR 構成

### やること
1. アーキ図を作る
2. ライブラリ一覧を作る
3. 画面数 / 主要ユースケース / 難画面を特定する
4. 代表画面 3〜5本を選ぶ
5. 移行難度の仮説を立てる

### 代表画面の選定基準
- 入力多い画面
- Ajax多い画面
- 一覧/検索/ページング画面
- ファイルアップロード画面
- 権限制御やセッション依存が強い画面

### アウトプット
- 現行棚卸しシート
- 代表画面一覧
- 技術的リスクトップ10

---

## Week 5: Java 21 / Jakarta EE 10 / 実行基盤の理解

### 目的
JSF以外の移行論点を押さえる。

### 学習テーマ
- Java 8 → 21 の主要変更点
- deprecated / removed APIs
- default charset, module, reflection 周りの影響
- Jakarta EE 10 の全体像
- Faces 4 を動かす実行基盤（GlassFish/Payara/WildFly/Tomcat+実装など）

### やること
1. Oracle の JDK 21 migration guide を読む
2. Java 8時代のコードで危ない論点を洗う
   - 内部API依存
   - JAXB / JAX-WS の扱い
   - 古いログ / XML / Security 設定
3. ターゲット実行基盤候補を決める
   - フル Jakarta EE サーバに載せるか
   - Tomcat + Mojarra/MyFaces + CDI の構成にするか
4. `javax.*` → `jakarta.*` の変換範囲を見積もる

### 実務判断ポイント
- **アプリサーバを何にするか** で移行難度がかなり変わる
- Java 21 へ上げるだけでなく、**ビルド・テスト・CI/CD・コンテナ・運用監視** も見直しが要る

### アウトプット
- 実行基盤比較メモ
- Java 21 移行論点リスト
- `javax → jakarta` 置換影響範囲メモ

---

## Week 6: 小さな PoC をやる

### 目的
机上の理解を、移行企画で使える確信に変える。

### PoCのおすすめ対象

#### PoC 1: 代表画面1本の移植
- 入力フォーム + バリデーション + 画面遷移
- CDI bean 化
- Facelets化（必要なら）
- Ajax 1箇所

#### PoC 2: ライブラリ依存の確認
- PrimeFaces等の置換可否
- RichFacesなど旧世代依存なら代替検討

#### PoC 3: ビルド/起動確認
- Java 21
- Jakarta Faces 4
- ターゲットアプリサーバ or Tomcat 構成

### PoCで確認すべき項目
- 起動できるか
- 依存解決できるか
- 画面レンダリングできるか
- バリデーション / Ajax / メッセージ表示が動くか
- セッション / 認可周りで破綻しないか

### アウトプット
- PoC結果メモ
- ブロッカー一覧
- 「段階移行」か「一括移行」かの仮説

---

## Week 7: 企画書に落とす

### 目的
学習結果を、プロジェクト推進に使える文書へ変換する。

### まとめるべき内容
1. 現行システム概要
2. 目標アーキテクチャ
3. 移行対象範囲
4. 非互換ポイント
5. 主要リスク
6. 方式案比較
7. PoC結果
8. 概算WBS
9. 体制・スキル課題
10. 次の2〜4週間でやるべきこと

### 方式案の例
- **案A: 一括移行**  
  短期集中、テスト負荷高い、切替リスク高い

- **案B: 段階移行（画面群単位）**  
  難度は高いが、業務影響を分割できる

- **案C: UI再構築含む再設計寄り移行**  
  既存資産流用は減るが、長期保守性は上がる

### 最終アウトプット
- 経営/上位層向け 1〜2ページ要約
- 開発チーム向け 詳細版
- リスク登録票
- 初期WBS

---

# 4. 毎週の実行テンプレート

各週は以下の型で回すと早い。

## 平日（1.5〜2時間）
- 30分: 一次情報を読む
- 30分: 手を動かして確認
- 30分: メモ化
- 余力: 現行ソース調査

## 週末（4〜6時間）
- 2時間: まとめ直し
- 2時間: 棚卸し or PoC
- 1〜2時間: 翌週計画作成

## 週末時点で必ず残すもの
- 学んだこと3点
- 未解決論点3点
- 来週調べること3点

---

# 5. 最短で効く勉強リソース

以下は **優先度順**。

## A. 一次情報（最優先）

### 1. Jakarta Faces 4.0 release page
- URL: https://jakarta.ee/specifications/faces/4.0/
- 用途: Faces 4 の追加点・削除点を把握する
- 特に見るところ:
  - removals / backwards incompatible changes
  - minimum Java version

### 2. Jakarta Faces 4.0 specification (HTML/PDF)
- URL: https://jakarta.ee/specifications/faces/4.0/jakarta-faces-4.0
- 用途: ライフサイクル、コンポーネントモデル、validation、ajax の正確な理解
- 全部読む必要はない。まずは以下優先:
  - Overview
  - Request Processing Lifecycle
  - Value handling
  - Validation
  - Ajax
  - Navigation / resources / state management

### 3. Jakarta EE Platform 10
- URL: https://jakarta.ee/specifications/platform/10/
- 用途: Faces 4 が Jakarta EE 10 文脈にあることを理解

### 4. Oracle JDK 21 Migration Guide
- URL: https://docs.oracle.com/en/java/javase/21/migrate/getting-started.html
- 用途: Java 8 → 21 の基本論点把握

## B. 実装理解に効く資料

### 5. Eclipse Mojarra project page
- URL: https://eclipse-ee4j.github.io/mojarra/
- 用途: 参照実装観点、必要依存、サーバ構成の理解

### 6. OmniFaces
- URL: https://omnifaces.org/
- URL: https://showcase.omnifaces.org/
- 用途: Facesの実務でよく出る補助ライブラリ・ユーティリティ理解
- コメント: Faces実務の“あるある”を吸収するのに有効

## C. 補助的に使うと良いもの

### 7. BalusC の記事群 / Stack Overflow 回答群
- 公式一次情報ではないが、Facesの実務理解に非常に強い
- 特にライフサイクル、ViewScoped、converter/validator、component tree 周り
- 注意: 古い記事は `javax` 時代なので、Jakarta移行時は読み替えが必要

---

# 6. 7週間で読むべき順番

## 最初の3日
1. Jakarta Faces 4 release page
2. Faces 4 spec の Overview / Lifecycle
3. Mojarra Hello World 相当

## 4日目〜7日目
4. CDI / scope / navigation
5. Facelets 基本文法
6. 現行コードの棚卸し開始

## 2〜3週目
7. 非互換ポイント調査
8. 旧ライブラリ依存確認
9. `javax → jakarta` 影響確認

## 4週目以降
10. Java 21 / server / PoC / WBS化

---

# 7. 学習で絶対に外さない観点

JSF初心者がハマりやすいので、以下は必ず押さえる。

## 1. ライフサイクル中心で理解する
タグを暗記するより、**いつ値が入って、いつ検証されて、いつ action が呼ばれるか** を理解する方が重要。

## 2. scope事故を避ける
`RequestScoped` / `ViewScoped` / `SessionScoped` の使い分けを曖昧にしない。

## 3. 現行が JSP かどうかを最優先確認
ここを外すと企画精度が大きく落ちる。

## 4. UIライブラリ依存を早く洗う
移行難易度の大半はここで決まることが多い。

## 5. Java 21 だけでなく Jakarta 化を別論点として扱う
JDK更新と API namespace 更新は別問題。

---

# 8. 企画に使えるリスク一覧（初版）

1. 現行ViewがJSPベースで、Faceletsへの全面変換が必要
2. `@ManagedBean` / `ManagedProperty` 多用で CDI 置換量が大きい
3. 旧コンポーネントライブラリが Jakarta 非対応
4. カスタムコンポーネントが `MethodBinding` / `ValueBinding` に依存
5. アプリサーバ依存コードが多い
6. 認証/認可周りがコンテナ依存
7. 結合テスト資産が不足
8. 画面回帰テスト自動化がない
9. Java 21 でのビルド/実行差異が周辺ライブラリで顕在化
10. 本番切替時のセッション互換・データ互換に問題

---

# 9. 7週間終了時に持つべき成果物

最低でも以下が揃っていれば、企画フェーズとしてかなり強い。

- JSF/Faces 4 の基礎理解メモ
- 非互換ポイント一覧
- 現行資産棚卸しシート
- 代表画面の難易度評価
- PoC結果
- 方式案比較表
- リスク一覧
- 初期WBS
- 追加調査テーマ一覧

---

# 10. クロウのおすすめ進め方

率直にいうと、この案件は **「JSFを勉強してから企画」では遅い**。  
正しくは、**学習と現行棚卸しを並行** した方がいい。

おすすめは次の進め方。

### すぐやること（今週）
1. JSFライフサイクルを理解
2. 現行コードから JSP / `@ManagedBean` / 旧ライブラリを grep
3. 代表画面を3本選ぶ
4. 移行難所の仮説を出す

### 来週やること
5. 非互換ポイント表を作る
6. Java 21 / Jakarta EE 10 / 実行基盤を整理
7. 小さなPoC対象を決める

つまり、**勉強ロードマップでありつつ、同時に企画のためのデューデリジェンス計画** として回すのが一番強い。

---

# 11. 追加であると精度が一気に上がる情報

もし次に以下が分かれば、かなり具体的な移行計画へ落とせる。

- 現行アプリサーバ（Tomcat / WebLogic / JBoss / WebSphere / 独自）
- View が JSP か XHTML か
- 使っているJSF系ライブラリ（PrimeFaces / RichFaces / OmniFaces / 独自）
- ビルドツール（Maven / Gradle / Ant）
- WAR / EAR 構成
- 画面数、主要業務フロー数
- テスト資産の有無

---

# 12. 出典

1. Jakarta Faces 4.0 Release Page  
   https://jakarta.ee/specifications/faces/4.0/
2. Jakarta Faces 4.0 Specification  
   https://jakarta.ee/specifications/faces/4.0/jakarta-faces-4.0
3. Jakarta EE 10 Platform Release Page  
   https://jakarta.ee/specifications/platform/10/
4. Eclipse Mojarra  
   https://eclipse-ee4j.github.io/mojarra/
5. OmniFaces  
   https://omnifaces.org/
6. OmniFaces Showcase  
   https://showcase.omnifaces.org/
7. Oracle JDK 21 Migration Guide  
   https://docs.oracle.com/en/java/javase/21/migrate/getting-started.html
