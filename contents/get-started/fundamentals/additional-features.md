---
title: Additional Streamlit features
slug: /get-started/fundamentals/additional-features
---

# さらなる機能

ここまでに Streamlit の [基本概念](/get-started/fundamentals/main-concepts) をすべて読み、[高度な概念](/get-started/fundamentals/advanced-concepts) でキャッシュとセッション状態を体験しました。
さらなる機能についてはどうでしょうか？ここでは、アプリを次のレベルに引き上げるための追加機能をいくつか紹介します。

## テーマ設定

Streamlit は、すぐに使えるライト テーマとダーク テーマをサポートします。
Streamlit はまずユーザーがライトモードまたはダークモードの設定をオペレーティングシステムまたはブラウザで行っているかどうかを確認します。
そうであれば、その設定が使用され、それ以外の場合はデフォルトでライトテーマが適用されます。

アクティブなテーマは、"⋮" → "Settings" から変更することもできます。

自分のアプリに独自のテーマを追加したいですか？
「設定」メニューには「アクティブなテーマを編集」という項目があり、そこからテーマエディタにアクセスできます。
このエディタを使用して、さまざまな色を試し、リアルタイムでアプリの変更を確認してみてください。

作業に満足したら、次の方法でテーマを保存できます。
[構成オプションの設定](/develop/concepts/configuration)
`[テーマ]` 設定セクション内。アプリのテーマを定義すると、
テーマセレクターに「カスタムテーマ」として表示され、次の方法で適用されます。
付属のライトテーマとダークテーマの代わりにデフォルトで使用されます。

テーマの定義時に使用できるオプションの詳細については、こちらをご覧ください。
[テーマ オプションのドキュメント](/develop/concepts/configuration/theming) にあります。

作業に満足したら、テーマは [theme] 設定セクションで設定オプションを設定することで保存できます。
一度アプリにテーマを定義すると、テーマセレクタに「カスタムテーマ」として表示され、デフォルトで適用されます。    
（既存のライトおよびダークテーマの代わりに）

テーマを定義する際に利用できるオプションの詳細は、[テーマ オプションのドキュメント](/develop/concepts/configuration/theming)で確認できます。

> [!Note]
> テーマエディタメニューはローカル開発時にのみ利用可能です。
> アプリを Streamlit Community Cloudでデプロイした場合、「設定」メニューにある「アクティブなテーマを編集」ボタンは表示されなくなります。

> [!Tip]
> 異なるテーマカラーを試すもう一つの方法は、「保存時に実行」オプションをオンにして、`config.toml` ファイルを編集することです。
> これにより、新しいテーマカラーが適用された状態でアプリが再実行される様子を確認できます。

## マルチページ

アプリが大きくなるにつれて、アプリを複数のページに整理すると便利になります。
これにより、開発者としてはアプリの管理が容易になり、ユーザーとしては操作が容易になります。
Streamlit は、複数ページのアプリをスムーズに作成する方法を提供します。

この機能は、複数ページのアプリの構築が単一ページのアプリの構築と同じくらい簡単になるように設計されています。
次のように既存のアプリにページを追加するだけです。

1. メインスクリプトを含むフォルダに、新しい `pages` フォルダーを作成します。メインスクリプトの名前が `main_page.py` であるとします。
2. アプリにページをさらに追加するには、新しい `.py` ファイルを `pages` フォルダに追加します。
3. 通常どおり `streamlit run main_page.py` を実行します。

これでおしまいです！`main_page.py` スクリプトがアプリのメインページに対応するようになります。
そして、サイドバーのページセレクターの `pages` フォルダにある他のスクリプトが表示されます。
ページはファイル名に従ってリストされます。(ファイル拡張子とアンダースコアは無視されます)

例えば：

<details open>
<summary><code>main_page.py</code></summary>

```python
import streamlit as st

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")
```

</details>

<details open>
<summary><code>pages/page_2.py</code></summary>

```python
import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")
```

</details>

<details open>
<summary><code>pages/page_3.py</code></summary>

```python
import streamlit as st

st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")
```

</details>
<br />

今すぐ streamlit run main_page.py を実行して、ピカピカの新しいマルチページアプリを確認してみましょう！

[マルチページ アプリ](/develop/concepts/multipage-apps) に関するドキュメントでは、ページの定義方法、マルチページ アプリの構造と実行方法、ページ間を移動する方法など、アプリにページを追加する方法を説明しています。基本を理解したら、[最初のマルチページ アプリを作成](/get-started/tutorials/create-a-multipage-app)してください。

## カスタムコンポーネント

Streamlit ライブラリ内で適切なコンポーネントが見つからない場合は、カスタム コンポーネントを試して Streamlit の組み込み機能を拡張してください。人気のあるコミュニティ作成のコンポーネントは [コンポーネント ギャラリー](https://streamlit.io/components)で探すことができます。 フロントエンド開発に興味がある場合は、Streamlit の [コンポーネント API](/develop/concepts/custom-components/intro) を使って独自のカスタムコンポーネントを作成することもできます。

## 静的ファイルの提供

Streamlit の基礎で学んだように、Streamlit はクライアントが接続するサーバーを実行します。つまり、アプリの閲覧者は、アプリのローカルにあるファイルに直接アクセスできません。ほとんどの場合、これは、問題にはなりません。なぜなら、Streamlt のコマンドがそれを自動的に処理してくれるからです。`st.image(<path-to-image>)` を使用すると、Streamlit サーバーがファイルにアクセスし、アプリの閲覧者がファイルを見ることができるように必要なホスティングを処理します。ただし、画像またはファイルへの直接 URL が必要な場合は、それをホストする必要があります。これには、正しい構成を設定し、ホストされたファイルを `static` という名前のディレクトリに配置する必要があります。たとえば、プロジェクト構成は次のようになります。

```bash
your-project/
├── static/
│   └── my_hosted-image.png
└── streamlit_app.py
```

詳細については、[静的ファイルの提供](/develop/concepts/configuration/serving-static-files) に関するガイドをお読みください。

## アプリのテスト

良い開発習慣には、コードのテストが含まれます。自動テストにより、より高品質のコードをより速く作成できるようになります。 Streamlit には、テストを簡単に構築できるテスト フレームワークが組み込まれています。お気に入りのテスト フレームワークを使用してテストを実行することができます。私たちのお薦めは [`pytest`](https://pypi.org/project/pytest/) です。 Streamlit アプリをテストするときは、アプリの実行をシミュレートし、ユーザー入力を宣言し、結果を検査します。 GitHub ワークフローを使用してテストを自動化し、重大な変更に関するアラートを即時に受け取ることができます。詳細については、[アプリのテスト](/develop/concepts/app-testing) のガイドをご覧ください。
