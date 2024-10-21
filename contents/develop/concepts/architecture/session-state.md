---
title: Add statefulness to apps
slug: /develop/concepts/architecture/session-state
---


# アプリにステートフルな機能を追加する

## ステートとは？

Streamlit アプリへのアクセスを1つのブラウザタブでの**セッション**と定義します。Streamlit サーバーに接続する各ブラウザタブごとに新しいセッションが作成されます。Streamlit は、アプリに対する操作があるたびに、スクリプトを上から下まで再実行します。再実行時には、変数が前回の実行から共有されることはなく、すべてが初期状態から始まります。

**セッションステート** は、各ユーザーセッションごとに、再実行間で変数を共有するための方法です。状態を保存し、持続させる機能に加え、Streamlit はコールバックを使用して状態を操作する機能も提供しています。セッションステートは、[マルチページアプリ](/develop/concepts/multipage-apps)のページ間でも持続されます。

このガイドでは、**セッションステート** と **Callbacks** を使用して、状態を保持するカウンターアプリを構築する方法を説明します。

セッションステートおよびCallbacks APIの詳細については、[セッションステート APIリファレンスガイド](/develop/api-reference/caching-and-state/st.session_state)をご参照ください。

また、Streamlit の開発者アドボケートDr. Marisa Smithによるセッションステートの基本チュートリアル動画もご覧ください：

[![](http://img.youtube.com/vi/92jUAXBmZyU/0.jpg)](https://www.youtube.com/watch?v=92jUAXBmZyU)


## カウンターの作成

スクリプトを `counter.py` と呼びます。このスクリプトは `count` 変数を初期化し、`count` 変数に格納された値をインクリメントするボタンを持っています：

```python
import streamlit as st

st.title('Counter Example')
count = 0

increment = st.button('Increment')
if increment:
    count += 1

st.write('Count = ', count)
```

上記のアプリでは、**_Increment_** ボタンを何回押しても、`count` は1のままです。その理由を理解しましょう：

- **_Increment_** ボタンを押すたびに、Streamlit は `counter.py` を上から下まで再実行します。そして、毎回 `count` が `0` に初期化されます。
- **_Increment_** を押すと、0に1が加えられるため、何回押しても `count=1` となります。

この問題は、`count` をセッションステート変数として保存することで解決できます。これにより、アプリの再実行間で `count` の値を維持するようにStreamlitに指示することができます。

では、セッションステートを使用するためのAPIについて学んでいきましょう。


### 初期化

セッションステート APIはフィールドベースのAPIを採用しており、Pythonの辞書に非常に似ています：

```python
import Streamlit  as st

# session_stateに 'key' が存在するか確認
# 存在しない場合は初期化する
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# セッションステートは属性ベースの構文もサポートしています
if 'key' not in st.session_state:
    st.session_state.key = 'value'
```


### 読み取りと更新

セッションステート 内のアイテムの値を読み取るには、アイテムを `st.write` に渡します：

```python
import streamlit as st

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# 読み取り
st.write(st.session_state.key)

# 出力: value
```

セッションステート 内のアイテムを更新するには、値を代入します：

```python
import streamlit as st

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# 更新
st.session_state.key = 'value2'     # 属性ベースのAPI
st.session_state['key'] = 'value2'  # 辞書のようなAPI
```

初期化されていない変数にアクセスすると、Streamlitは例外をスローします：

```python
import streamlit as st

st.write(st.session_state['value'])

# 例外をスロー！
```

![state-uninitialized-exception](/images/state_uninitialized_exception.png)

それでは、セッションステートをカウンターアプリに追加する方法を示すいくつかの例を見ていきましょう。


### 例 1: セッションステート を追加

セッションステート APIに慣れてきたところで、カウンターアプリをセッションステートを使って更新してみましょう：

```python
import streamlit as st

st.title('Counter Example')
if 'count' not in st.session_state:
    st.session_state.count = 0

increment = st.button('Increment')
if increment:
    st.session_state.count += 1

st.write('Count = ', st.session_state.count)
```

上記の例では、**_Increment_** ボタンを押すたびに `count` が更新されることがわかります。


### 例 2: セッションステート と Callbacks

セッションステート を使った基本的なカウンターアプリができたので、少し複雑なものに進みましょう。次の例では、セッションステート と Callbacks を使用します。

**コールバック**：コールバックとは、入力ウィジェットが変更されたときに呼び出されるPython関数です。コールバックは、ウィジェットの `on_change`（または `on_click`）、`args`、`kwargs` パラメーターを使用して設定できます。コールバックAPIの詳細は、[セッションステート API リファレンスガイド](/develop/api-reference/caching-and-state/st.session_state#use-callbacks-to-update-session-state)をご覧ください。

```python
import streamlit as st

st.title('Counter Example using Callbacks')
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter():
    st.session_state.count += 1

st.button('Increment', on_click=increment_counter)

st.write('Count = ', st.session_state.count)
```

この例では、**_Increment_** ボタンを押すと、`increment_counter()` 関数が呼び出され、`count` が毎回更新されます。


### 例 3: Callbacksでargsとkwargsを使用する

Callbacksは、ウィジェット内の `args` パラメータを使用して引数を渡すこともサポートしています：

```python
import streamlit as st

st.title('Counter Example using Callbacks with args')
if 'count' not in st.session_state:
    st.session_state.count = 0

increment_value = st.number_input('Enter a value', value=0, step=1)

def increment_counter(increment_value):
    st.session_state.count += increment_value

increment = st.button('Increment', on_click=increment_counter,
    args=(increment_value, ))

st.write('Count = ', st.session_state.count)
```

さらに、`kwargs` パラメータを使用して名前付き引数をコールバック関数に渡すことも可能です。次の例をご覧ください：

```python
import streamlit as st

st.title('Counter Example using Callbacks with kwargs')
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter(increment_value=0):
    st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
    st.session_state.count -= decrement_value

st.button('Increment', on_click=increment_counter,
	kwargs=dict(increment_value=5))

st.button('Decrement', on_click=decrement_counter,
	kwargs=dict(decrement_value=1))

st.write('Count = ', st.session_state.count)
```


### 例 4: フォームとコールバック

次に、`count` をインクリメントするだけでなく、最後に更新された時刻も保存したいとします。この操作を Callbacks と `st.form` を使って実現する例を示します：

```python
import streamlit as st
import datetime

st.title('Counter Example')
if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.last_updated = datetime.time(0,0)

def update_counter():
    st.session_state.count += st.session_state.increment_value
    st.session_state.last_updated = st.session_state.update_time

with st.form(key='my_form'):
    st.time_input(label='Enter the time', value=datetime.datetime.now().time(), key='update_time')
    st.number_input('Enter a value', value=0, step=1, key='increment_value')
    submit = st.form_submit_button(label='Update', on_click=update_counter)

st.write('Current Count = ', st.session_state.count)
st.write('Last Updated = ', st.session_state.last_updated)
```


## 高度な概念

### セッションステートとウィジェット状態の関連付け

セッションステートは再実行間で変数を保持する機能を提供します。ウィジェットの状態（つまり、ウィジェットの値）もセッション内で保持されます。

簡単にするために、これらの情報を **セッションステート** に統一しています。この便利な機能により、アプリのコードのどこでもウィジェットの状態を簡単に読み書きできるようになっています。セッションステートの変数は、`key` 引数を使用してウィジェットの値と連動します。

次の例でこれを説明します。例えば、摂氏温度を表すスライダーがあるアプリがあるとします。次のように、セッションステート API を使用して温度ウィジェットの値を **設定** し、**取得** できます。

```python
import streamlit as st

if "celsius" not in st.session_state:
    # スライダーウィジェットの初期デフォルト値を設定
    st.session_state.celsius = 50.0

st.slider(
    "Temperature in Celsius",
    min_value=-100.0,
    max_value=100.0,
    key="celsius"
)

# これでスライダーウィジェットの値を取得します
st.write(st.session_state.celsius)
```

ただし、セッションステート API を使用してウィジェットの値を設定する場合には制限があります。

<Important>

Streamlit は `st.button` と `st.file_uploader` のウィジェット値をセッションステート API を介して設定することを **許可していません**。

</Important>

次の例では、セッションステート API を使用して `st.button` の状態を設定しようとすると、`StreamlitAPIException` が発生します。

```python
import streamlit as st

if 'my_button' not in st.session_state:
    st.session_state.my_button = True
    # ボタンの状態を設定しようとすると、Streamlit が例外をスローします

st.button('Submit', key='my_button')
```


### シリアライズ可能なセッションステート

シリアライズとは、オブジェクトやデータ構造を永続化して共有できる形式に変換し、データの元の構造を復元できるようにするプロセスを指します。Pythonの組み込みモジュールである [pickle](https://docs.python.org/3/library/pickle.html) は、Pythonオブジェクトをバイトストリームにシリアライズ（「ピックル化」）し、そのストリームをオブジェクトにデシリアライズ（「アンピックル化」）します。

デフォルトでは、Streamlitの [セッションステート](/develop/concepts/architecture/session-state) は、オブジェクトのピックルシリアライズ性に関係なく、セッションの期間中、任意のPythonオブジェクトを永続化できます。このプロパティにより、整数、浮動小数点数、複素数、ブーリアン、データフレーム、さらには関数が返す [lambdas](https://docs.python.org/3/reference/expressions.html#lambda) などのPythonプリミティブを保存することができます。しかし、いくつかの実行環境では、セッションステート内のすべてのデータをシリアライズする必要があるため、開発中に非互換性を検出するか、将来的に実行環境がその機能をサポートしなくなる場合には、便利です。

そのために、Streamlitは `runner.enforceSerializableSessionState` という [設定オプション](/develop/concepts/configuration) を提供しており、これを `true` に設定すると、セッションステート内ではピックルシリアライズ可能なオブジェクトのみが許可されます。このオプションを有効にするには、次の内容でグローバルまたはプロジェクト設定ファイルを作成するか、コマンドラインフラグとして使用します：

```toml
# .streamlit/config.toml
[runner]
enforceSerializableSessionState = true
```

"_ピックルシリアライズ可能_" とは、`pickle.dumps(obj)` を呼び出したときに [`PicklingError`](https://docs.python.org/3/library/pickle.html#pickle.PicklingError) 例外が発生しないことを意味します。この設定オプションが有効な場合、シリアライズ不可能なデータをセッションステートに追加すると例外が発生します。例：

```python
import streamlit as st

def unserializable_data():
		return lambda x: x

#👇 enforceSerializableSessionState がオンのときに例外を発生させる
st.session_state.unserializable = unserializable_data()
```

> [!Warning]
> `runner.enforceSerializableSessionState` が `true` に設定されている場合、セッションステートは暗黙的に `pickle` モジュールを使用しますが、これはセキュリティ上の問題があることが知られています。セッションステートから保存および取得されたすべてのデータが信頼できるものであることを確認してください。ピックルデータはアンピックル時に任意のコードを実行する悪意のあるデータが構築される可能性があるためです。不正なソースから取得された、または改ざんされた可能性のあるデータをロードしないでください。**信頼できるデータのみをロードしてください**。


### 注意点と制限

セッションステートを使用する際に考慮すべきいくつかの制限事項は次のとおりです：

- セッションステートはタブが開かれていてStreamlitサーバーに接続されている限り存在します。タブを閉じると、セッションステートに保存されたすべての情報は失われます。
- セッションステートは永続化されません。Streamlitサーバーがクラッシュすると、セッションステートに保存されたすべてのデータは消去されます。
- For caveats and limitations with the セッションステート API, please see the [API limitations](/develop/api-reference/caching-and-state/st.session_state#caveats-and-limitations).
