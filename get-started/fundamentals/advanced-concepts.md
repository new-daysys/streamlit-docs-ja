---
title: Advanced concepts of Streamlit
slug: /get-started/fundamentals/advanced-concepts
---

# 先進的なコンセプト

Streamlit アプリがどのように実行され、データが処理されるかがわかったので、効率について話しましょう。キャッシュを使用すると、関数の出力を保存できるため、再実行時にスキップできます。セッション状態を使用すると、各ユーザーの情報を保存し、再実行の間に保存できます。これにより、不必要な再計算を回避できるだけでなく、動的なページを作成して段階的なプロセスを処理することもできます。

## キャッシュ

キャッシュを使用すると、Web からデータを読み込んだり、大規模なデータセットを操作したり、高価な計算を実行したりする場合でも、アプリのパフォーマンスを維持できます。

キャッシュの基本的な考え方は、負荷の高い関数呼び出しの結果を保存し、同じ入力が再び発生したときにキャッシュされた結果を返すというものです。これにより、同じ入力値を使用した関数の繰り返し実行が回避されます。

Streamlit で関数をキャッシュするには、関数にキャッシュデコレーターを適用する必要があります。選択肢は 2 つあります。

- `st.cache_data` は、データを返す計算をキャッシュするための推奨される方法です。シリアル化可能なデータ オブジェクト (str、int、float、DataFrame、dict、list など) を返す関数を使用する場合は、`st.cache_data` を使用します。 **関数呼び出しごとにデータの新しいコピーが作成されます**。これにより、[突然変異と競合状態](/develop/concepts/architecture/caching#mutation-and-concurrency-issues) に対して安全になります。ほとんどの場合、`st.cache_data` の動作はあなたが望むものです。そのため、よくわからない場合は、`st.cache_data` から始めて、それが機能するかどうかを確認してください。
- `st.cache_resource` は、ML モデルやデータベース接続などのグローバル リソースをキャッシュするための推奨される方法です。関数が複数回ロードしたくないシリアル化できないオブジェクトを返す場合は、「st.cache_resource」を使用します。 **キャッシュされたオブジェクト自体を返します**。これは、コピーや複製を行わずにすべての再実行とセッションで共有されます。 `st.cache_resource` を使用してキャッシュされたオブジェクトを変更すると、その変更はすべての再実行とセッションにわたって存在します。

Example:

```python
@st.cache_data
def long_running_function(param1, param2):
    return …
```

上記の例では、`long_running_function` が `@st.cache_data` で修飾されています。その結果、Streamlit は次のように指摘しています。

- 関数の名前 (`"long_running_function"`)
- 入力の値 (`param1`、`param2`)
- 関数内のコード

「long_running_function」内のコードを実行する前に、Streamlit はキャッシュに以前に保存された結果がないかチェックします。指定された関数と入力値のキャッシュされた結果が見つかった場合、そのキャッシュされた結果が返され、関数のコードは再実行されません。それ以外の場合、Streamlit は関数を実行し、結果をキャッシュに保存し、スクリプトの実行を続行します。開発中、関数コードが変更されるとキャッシュが自動的に更新され、最新の変更がキャッシュに確実に反映されます。

<Image src="/images/caching-high-level-diagram.png" caption="Streamlit の 2 つのキャッシュ デコレータとその使用例。" alt="Streamlit の 2 つのキャッシュ デコレータとその使用例。データベースに保存するものには st.cache_data を使用します。データベースやマシンへの接続など、データベースに保存できないものには st.cache_resource を使用します。学習モデル。」 />

Streamlit キャッシュ デコレーター、その構成パラメーター、およびその制限の詳細については、「[Caching](/develop/concepts/architecture/caching)」を参照してください。

## Session State

Session State provides a dictionary-like interface where you can save information that is preserved between script reruns. Use `st.session_state` with key or attribute notation to store and recall values. For example, `st.session_state["my_key"]` or `st.session_state.my_key`. Remember that widgets handle their statefulness all by themselves, so you won't always need to use Session State!

### What is a session?

A session is a single instance of viewing an app. If you view an app from two different tabs in your browser, each tab will have its own session. So each viewer of an app will have a Session State tied to their specific view. Streamlit maintains this session as the user interacts with the app. If the user refreshes their browser page or reloads the URL to the app, their Session State resets and they begin again with a new session.

### Examples of using Session State

Here's a simple app that counts the number of times the page has been run. Every time you click the button, the script will rerun.

```python
import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")
```

- **First run:** The first time the app runs for each user, Session State is empty. Therefore, a key-value pair is created (`"counter":0`). As the script continues, the counter is immediately incremented (`"counter":1`) and the result is displayed: "This page has run 1 times." When the page has fully rendered, the script has finished and the Streamlit server waits for the user to do something. When that user clicks the button, a rerun begins.

- **Second run:** Since "counter" is already a key in Session State, it is not reinitialized. As the script continues, the counter is incremented (`"counter":2`) and the result is displayed: "This page has run 2 times."

There are a few common scenarios where Session State is helpful. As demonstrated above, Session State is used when you have a progressive process that you want to build upon from one rerun to the next. Session State can also be used to prevent recalculation, similar to caching. However, the differences are important:

- Caching associates stored values to specific functions and inputs. Cached values are accessible to all users across all sessions.
- Session State associates stored values to keys (strings). Values in session state are only available in the single session where it was saved.

If you have random number generation in your app, you'd likely use Session State. Here's an example where data is generated randomly at the beginning of each session. By saving this random information in Session State, each user gets different random data when they open the app but it won't keep changing on them as they interact with it. If you select different colors with the picker you'll see that the data does not get re-randomized with each rerun. (If you open the app in a new tab to start a new session, you'll see different data!)

```python
import streamlit as st
import pandas as pd
import numpy as np

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("Choose a datapoint color")
color = st.color_picker("Color", "#FF0000")
st.divider()
st.scatter_chart(st.session_state.df, x="x", y="y", color=color)
```

If you are pulling the same data for all users, you'd likely cache a function that retrieves that data. On the other hand, if you pull data specific to a user, such as querying their personal information, you may want to save that in Session State. That way, the queried data is only available in that one session.

As mentioned in [Basic concepts](/get-started/fundamentals/main-concepts#widgets), Session State is also related to widgets. Widgets are magical and handle statefulness quietly on their own. As an advanced feature however, you can manipulate the value of widgets within your code by assigning keys to them. Any key assigned to a widget becomes a key in Session State tied to the value of the widget. This can be used to manipulate the widget. After you finish understanding the basics of Streamlit, check out our guide on [Widget behavior](/develop/concepts/architecture/widget-behavior) to dig in the details if you're interested.

## Connections

As hinted above, you can use `@st.cache_resource` to cache connections. This is the most general solution which allows you to use almost any connection from any Python library. However, Streamlit also offers a convenient way to handle some of the most popular connections, like SQL! `st.connection` takes care of the caching for you so you can enjoy fewer lines of code. Getting data from your database can be as easy as:

```python
import streamlit as st

conn = st.connection("my_database")
df = conn.query("select * from my_table")
st.dataframe(df)
```

Of course, you may be wondering where your username and password go. Streamlit has a convenient mechanism for [Secrets management](/develop/concepts/connections/secrets-management). For now, let's just see how `st.connection` works very nicely with secrets. In your local project directory, you can save a `.streamlit/secrets.toml` file. You save your secrets in the toml file and `st.connection` just uses them! For example, if you have an app file `streamlit_app.py` your project directory may look like this:

```bash
your-LOCAL-repository/
├── .streamlit/
│   └── secrets.toml # Make sure to gitignore this!
└── streamlit_app.py
```

For the above SQL example, your `secrets.toml` file might look like the following:

```toml
[connections.my_database]
    type="sql"
    dialect="mysql"
    username="xxx"
    password="xxx"
    host="example.com" # IP or URL
    port=3306 # Port number
    database="mydb" # Database name
```

Since you don't want to commit your `secrets.toml` file to your repository, you'll need to learn how your host handles secrets when you're ready to publish your app. Each host platform may have a different way for you to pass your secrets. If you use Streamlit Community Cloud for example, each deployed app has a settings menu where you can load your secrets. After you've written an app and are ready to deploy, you can read all about how to [Deploy your app](/deploy/streamlit-community-cloud/deploy-your-app) on Community Cloud.
