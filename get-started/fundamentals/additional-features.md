---
title: Additional Streamlit features
slug: /get-started/fundamentals/additional-features
---

# さらなる機能
Streamlit のさらなる機能について学びます。初めてのアプリでこれらの概念を知る必要はありませんが、何が利用できるのかを確認するためにチェックしてください。

これで、Streamlit の [基本概念](/get-started/fundamentals/main-concepts) をすべて読み、[高度な概念](/get-started/fundamentals/advanced-concepts) でキャッシュとセッション状態を体験しました。一方で、付加機能についてはどうでしょうか? ここでは、アプリを次のレベルに引き上げるための追加機能をいくつか紹介します。

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

If you can't find the right component within the Streamlit library, try out custom components to extend Streamlit's built-in functionality. Explore and browse through popular, community-created components in the [Components gallery](https://streamlit.io/components). If you dabble in frontend development, you can build your own custom component with Streamlit's [components API](/develop/concepts/custom-components/intro).

## 静的ファイルの提供

As you learned in Streamlit fundamentals, Streamlit runs a server that clients connect to. That means viewers of your app don't have direct access to the files which are local to your app. Most of the time, this doesn't matter because Streamlt commands handle that for you. When you use `st.image(<path-to-image>)` your Streamlit server will access the file and handle the necessary hosting so your app viewers can see it. However, if you want a direct URL to an image or file you'll need to host it. This requires setting the correct configuration and placing your hosted files in a directory named `static`. For example, your project could look like:

```bash
your-project/
├── static/
│   └── my_hosted-image.png
└── streamlit_app.py
```

To learn more, read our guide on [Static file serving](/develop/concepts/configuration/serving-static-files).

## アプリのテスト

Good development hygeine includes testing your code. Automated testing allows you to write higher quality code, faster! Streamlit has a built-in testing framework that let's you build tests easily. Use your favorite testing framework to run your tests. We like [`pytest`](https://pypi.org/project/pytest/). When you test a Streamlit app, you simulate running the app, declare user input, and inspect the results. You can use GitHub workflows to automate your tests and get instant alerts about breaking changes. Learn more in our guide to [App testing](/develop/concepts/app-testing).
