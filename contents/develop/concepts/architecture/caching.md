---
title: Caching overview
slug: /develop/concepts/architecture/caching
---

> [!Note]
> `@st.cache` デコレーターは廃止されました。
> 関連ドキュメントは [Optimize performance with st.cache](/develop/concepts/architecture/st.cache) にて確認できます。

# キャッシング概要

Streamlit は、ユーザーの操作やコードの変更があるたびに、スクリプトを上から下まで再実行します。この実行モデルにより、開発が非常に簡単になりますが、2つの大きな課題もあります：

1. 長時間実行される関数が何度も再実行されるため、アプリが遅くなる。
2. オブジェクトが何度も再作成されるため、再実行やセッションをまたいでオブジェクトを保持するのが難しくなる。

でも心配しないでください！Streamlitにはこれらの問題に対処するためのキャッシング機能が組み込まれています。キャッシングは、遅い関数呼び出しの結果を保存し、再実行を避けることでアプリを高速化し、再実行時にオブジェクトを持続させます。キャッシュされた値はアプリのすべてのユーザーに利用可能です。セッション内でのみアクセス可能な結果を保存する必要がある場合は、代わりに[セッションステート](/develop/concepts/architecture/session-state) を使用してください。

1. [小さな例](#小さな例)
2. [基本的な使い方](#基本的な使い方)
3. [高度な使い方](#高度な使い方)
4. [st.cacheからの移行](#st.cacheからの移行)

## 小さな例

Streamlit で関数をキャッシュするには、`st.cache_data` または `st.cache_resource` のいずれかのデコレーターで関数を装飾する必要があります：

```python
@st.cache_data
def long_running_function(param1, param2):
    return …
```

この例では、`long_running_function` に `@st.cache_data` を付与することで、Streamlitは関数が呼び出されるたびに以下の2つのことを確認します：

1. 入力パラメータの値（この場合、`param1` と `param2`）。
2. 関数内のコード。

Streamlitがこれらのパラメータ値と関数コードを初めて確認した場合、関数を実行し、その戻り値をキャッシュに保存します。同じパラメータとコードで再度呼び出されると（例：ユーザーがアプリを操作した場合）、Streamlitは関数の実行をスキップし、代わりにキャッシュされた値を返します。開発中は、関数コードが変更されるたびにキャッシュが自動的に更新され、最新の変更がキャッシュに反映されるようになります。

前述のとおり、キャッシングには2つのデコレーターがあります：

- `st.cache_data` は、データを返す計算のキャッシュに推奨されます。例えば、CSVからのデータフレームの読み込み、NumPy配列の変換、APIクエリなど、シリアライズ可能なデータオブジェクト（文字列、整数、浮動小数点数、データフレーム、配列、リストなど）を返す関数に適しています。関数が呼び出されるたびにデータの新しいコピーを作成するため、[ミューテーションや競合状態](#mutation-and-concurrency-issues)に対して安全です。ほとんどの場合、`st.cache_data` を使用するのが適切なので、迷った場合は `st.cache_data` を試してみてください！
- `st.cache_resource` は、機械学習モデルやデータベース接続などのグローバルリソースをキャッシュするために推奨されます。これは、複数回読み込む必要のないシリアライズ不可能なオブジェクトに適しており、アプリの再実行やセッションをまたいでリソースを共有できます。ただし、キャッシュされた戻り値を変更すると、キャッシュ内のオブジェクトも直接変更されることに注意してください（詳細は後述）。

## 基本的な使い方

### st.cache_data

`st.cache_data` は、データフレーム、NumPy配列、文字列、整数、浮動小数点数など、データを返すすべての関数に使用する基本的なコマンドです。ほとんどのユースケースに適しているため、これが主な使用方法です。各ユーザーセッション内では、`@st.cache_data` で装飾された関数はキャッシュされた戻り値の_コピー_を返します（すでにキャッシュされている場合）。

#### 使用例

`st.cache_data` の使用例を見てみましょう。例えば、アプリが[Uberのライドシェアデータセット](https://github.com/plotly/datasets/blob/master/uber-rides-data1.csv)（50 MBのCSVファイル）をインターネットからDataFrameに読み込む場合です：

```python
def load_data(url):
    df = pd.read_csv(url)  # 👈 データをダウンロード
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")
```

`load_data` 関数の実行には、インターネット接続によっては2〜30秒かかります。（ヒント: 回線が遅い場合は[こちらの5 MBデータセット](https://github.com/plotly/datasets/blob/master/26k-consumer-complaints.csv)を使用してください）。キャッシングなしでは、アプリが読み込まれるたび、またはユーザーが操作するたびにデータが再ダウンロードされます。追加したボタンをクリックして試してみてください！あまり良い体験ではありませんよね… 😕

では、`load_data` に `@st.cache_data` デコレーターを追加してみましょう：

```python
@st.cache_data  # 👈 キャッシングデコレーターを追加
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")
```

アプリを再実行すると、最初の実行時のみ遅いダウンロードが発生し、次回以降の再実行はほぼ瞬時に行われます！💨

#### 動作

これがどのように動作するのか、`st.cache_data` の挙動をステップごとに見ていきましょう：

- 最初の実行時、Streamlitは指定されたパラメータ値（この場合はCSVファイルのURL）で `load_data` 関数を呼び出したことがないことを認識します。そこで、関数を実行してデータをダウンロードします。
- ここでキャッシングメカニズムが動作します：返されたDataFrameは[pickle](https://docs.python.org/3/library/pickle.html)を介してシリアライズ（バイトに変換）され、キャッシュに保存されます（`url` パラメータの値と共に）。
- 次回の実行時、Streamlitは特定の `url` に対する `load_data` のキャッシュエントリを確認します。エントリがあるので、キャッシュされたオブジェクトを取得し、シリアライズ解除してDataFrameに変換し、関数を再実行してデータを再ダウンロードする代わりに返します。

このキャッシュされたオブジェクトのシリアライズとシリアライズ解除のプロセスにより、元のDataFrameのコピーが作成されます。このコピー動作は一見不要に思えますが、データオブジェクトをキャッシュする際には有効であり、ミューテーションや競合状態の問題を効果的に防ぎます。詳しくは、以下の「[ミューテーションと競合状態の問題](#mutation-and-concurrency-issues)」のセクションをご覧ください。

> [!Warning]
> `st.cache_data` は暗黙的に `pickle` モジュールを使用しており、これは安全性に問題があることが知られています。キャッシュされた関数が返すものはすべてpickleされて保存され、取り出す際にunpickleされます。キャッシュされた関数が信頼できる値を返すことを確認してください。不正なpickleデータを構築し、unpickle時に任意のコードを実行することが可能です。信頼できないソースから来た可能性があるデータは、安全でないモードで読み込まないでください。**信頼できるデータのみを読み込んでください**。

#### 使用例

**DataFrameの変換**

上記の例では、DataFrameの読み込みをキャッシュする方法を示しました。`df.filter`、`df.apply`、`df.sort_values` などのDataFrame変換もキャッシュすることが有効です。特に大規模なDataFrameでは、これらの操作は遅くなることがあります。

```python
@st.cache_data
def transform(df):
    df = df.filter(items=['one', 'three'])
    df = df.apply(np.sum, axis=0)
	return df
```

**配列の計算**

同様に、NumPy配列の計算をキャッシュすることも意味があります：

```python
@st.cache_data
def add(arr1, arr2):
	return arr1 + arr2
```

**データベースクエリ**

データベースを扱う場合、SQLクエリを使用してデータをアプリに読み込むことが一般的です。これらのクエリを繰り返し実行するのは遅くなり、コストがかかり、データベースのパフォーマンスも低下させる可能性があります。アプリ内のデータベースクエリはキャッシュすることを強く推奨します。詳細な例については、[Streamlitと異なるデータベースを接続するためのガイド](/develop/tutorials/databases)も参照してください。

```python
connection = database.connect()

@st.cache_data
def query():
    return pd.read_sql_query("SELECT * from table", connection)
```

> [!Tip]
> データベースから新しい結果を取得するために `ttl`（有効期限）を設定することをお勧めします。`st.cache_data(ttl=3600)` を設定すると、Streamlitは1時間（3600秒）後にキャッシュされた値を無効化し、再度キャッシュされた関数を実行します。詳細は[キャッシュのサイズと期間の制御](#controlling-cache-size-and-duration)で確認してください。

**API呼び出し**

API呼び出しをキャッシュするのも有効です。これにより、レート制限を回避することもできます。

```python
@st.cache_data
def api_call():
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    return response.json()
```

**MLモデルの実行（推論）**

複雑な機械学習モデルを実行するには、多くの時間とメモリを使用することがあります。同じ計算を何度も再実行するのを避けるために、キャッシングを使用してください。

```python
@st.cache_data
def run_model(inputs):
    return model(inputs)
```

### st.cache_resource

`st.cache_resource` は、すべてのユーザー、セッション、および再実行でグローバルに利用できる「リソース」をキャッシュするためのコマンドです。`st.cache_data` よりも限定的なユースケースを持ち、特にデータベース接続や機械学習モデルのキャッシュに適しています。各ユーザーセッション内で、`@st.cache_resource` で装飾された関数はキャッシュされた返り値のインスタンスを返します（すでにキャッシュされている場合）。したがって、`st.cache_resource` でキャッシュされたオブジェクトはシングルトンのように振る舞い、ミューテーションを引き起こす可能性があります。

#### 使用例

`st.cache_resource` の例として、典型的な機械学習アプリを見てみましょう。まず、機械学習モデルを読み込む必要があります。ここでは、[Hugging Faceのtransformersライブラリ](https://huggingface.co/docs/transformers/index)を使用します：

```python
from transformers import pipeline
model = pipeline("sentiment-analysis")  # 👈 モデルを読み込む
```

このコードをStreamlitアプリに直接書き込むと、アプリは再実行やユーザーの操作のたびにモデルを読み込みます。この繰り返しのモデル読み込みには2つの問題があります：

- モデルの読み込みに時間がかかり、アプリの速度が低下する。
- 各セッションがモデルを最初から読み込むため、膨大なメモリを消費する。

代わりに、モデルを一度だけ読み込み、すべてのユーザーとセッションで同じオブジェクトを使い回す方が合理的です。これこそが `st.cache_resource` の使用例です！アプリに追加して、ユーザーが入力したテキストを処理してみましょう：

```python
from transformers import pipeline

@st.cache_resource  # 👈 キャッシングデコレーターを追加
def load_model():
    return pipeline("sentiment-analysis")

model = load_model()

query = st.text_input("Your query", value="I love Streamlit! 🎈")
if query:
    result = model(query)[0]  # 👈 クエリテキストを分類
    st.write(result)
```

このアプリを実行すると、`load_model` はアプリの起動時に1回だけ呼び出されることが確認できます。以降の再実行では、キャッシュされた同じモデルが再利用され、時間とメモリが節約されます！

#### 動作

`st.cache_resource` の使用は `st.cache_data` に非常によく似ていますが、いくつか重要な違いがあります：

- `st.cache_resource` はキャッシュされた返り値のコピーを作成せず、オブジェクト自体をキャッシュに保存します。そのため、関数の返り値に対するすべての変更は、キャッシュ内のオブジェクトに直接影響します。複数のセッションからの変更が問題を引き起こさないように、返り値がスレッドセーフであることを確認する必要があります。簡単に言えば、返り値はスレッドセーフでなければなりません。

> [!Warning]
> スレッドセーフでないオブジェクトに `st.cache_resource` を使用すると、クラッシュやデータの破損が発生する可能性があります。詳細は[ミューテーションと競合状態の問題](#mutation-and-concurrency-issues)を参照してください。

- コピーが作成されないため、キャッシュされた返り値のグローバルインスタンスが1つだけ存在し、特に大規模な機械学習モデルを使用する場合にメモリが節約されます。コンピュータサイエンスの用語では、[シングルトン](https://en.wikipedia.org/wiki/Singleton_pattern)を作成しています。
- 関数の返り値はシリアライズ可能である必要はありません。この動作は、データベース接続、ファイルハンドル、スレッドなど、もともとシリアライズできない型に対して非常に有効です。これらのオブジェクトは `st.cache_data` でキャッシュすることはできません。

#### 使用例

**データベース接続**

`st.cache_resource` はデータベース接続に非常に便利です。通常、クエリごとに再利用したい接続オブジェクトを作成します。毎回新しい接続オブジェクトを作成するのは非効率で、接続エラーを引き起こす可能性があります。これがまさに `st.cache_resource` の用途です。例えば、Postgresデータベースの場合：

```python
@st.cache_resource
def init_connection():
    host = "hh-pgsql-public.ebi.ac.uk"
    database = "pfmegrnargs"
    user = "reader"
    password = "NWDMCE5xdipIjRrp"
    return psycopg2.connect(host=host, database=database, user=user, password=password)

conn = init_connection()
```

もちろん、他のデータベースでも同様にできます。詳細な例については、[Streamlitとデータベースの接続方法に関するガイド](/develop/tutorials/databases) を参照してください。


**機械学習モデルの読み込み**

アプリは機械学習モデルを常にキャッシュする必要があります。そうしないと、新しいセッションごとにモデルがメモリに再度読み込まれてしまいます。🤗 Hugging Faceモデルを使用する方法の[例](#usage-1)を参照してください。PyTorchやTensorFlowでも同様にできます。以下はPyTorchの例です：

```python
@st.cache_resource
def load_model():
    model = torchvision.models.resnet50(weights=ResNet50_Weights.DEFAULT)
    model.eval()
    return model

model = load_model()
```

### どのキャッシングデコレーターを使用するかの判断

上記のセクションでは、それぞれのキャッシングデコレーターに共通する多くの例を示しましたが、どちらのデコレーターを使用すべきか決定するのが難しいエッジケースも存在します。最終的には、「データ」と「リソース」の違いに帰着します：

- データはシリアライズ可能なオブジェクトです（[pickle](https://docs.python.org/3/library/pickle.html)を介してバイトに変換可能）。ディスクに簡単に保存できるものを指します。通常、データベースやファイルシステムに保存する基本的な型（str、int、floatなど）、または配列、データフレーム、画像など、これらの型を組み合わせたリスト、タプル、辞書などが含まれます。
- リソースはシリアライズ不可能なオブジェクトで、通常はディスクやデータベースに保存しないものです。リソースは、データベース接続、機械学習モデル、ファイルハンドル、スレッドなどのより複雑で一時的なオブジェクトであることが多いです。

上記の型リストから、Pythonのほとんどのオブジェクトが「データ」であることは明らかです。これが `st.cache_data` がほとんどのユースケースで正しいコマンドである理由でもあります。`st.cache_resource` は、特定の状況でのみ使用すべきやや特殊なコマンドです。

あるいは、あまり考えたくない場合は、以下の表を参照して、ユースケースや返り値の型を確認してください😉：

| ユースケース                             |                                                                                                       典型的な返り値の型 |                                                                                                                                            推奨されるデコレーター |
| :----------------------------------- | -------------------------------------------------------------------------------------------------------------------------: | -----------------------------------------------------------------------------------------------------------------------------------------------------------: |
| pd.read_csv でCSVファイルを読み込む  |                                                                                                           pandas.DataFrame |                                                                                                                                                st.cache_data |
| テキストファイルを読み込む            |                                                                                                           str, list of str |                                                                                                                                                st.cache_data |
| pandasデータフレームを変換する         |                                                                                            pandas.DataFrame, pandas.Series |                                                                                                                                                st.cache_data |
| numpy配列を使って計算する             |                                                                                                              numpy.ndarray |                                                                                                                                                st.cache_data |
| 基本的な型を使った単純な計算           |                                                                                                         str, int, float, … |                                                                                                                                                st.cache_data |
| データベースにクエリを送信する         |                                                                                                           pandas.DataFrame |                                                                                                                                                st.cache_data |
| APIにクエリを送信する                  |                                                                                                pandas.DataFrame, str, dict |                                                                                                                                                st.cache_data |
| 機械学習モデル（推論）を実行する      |                                                                                     pandas.DataFrame, str, int, dict, list |                                                                                                                                                st.cache_data |
| 画像を作成または処理する               |                                                                                             PIL.Image.Image, numpy.ndarray |                                                                                                                                                st.cache_data |
| グラフを作成する                       |                                                        matplotlib.figure.Figure, plotly.graph_objects.Figure, altair.Chart | st.cache_data（ただし、ライブラリによっては、グラフオブジェクトがシリアライズ不可能なため、st.cache_resource が必要な場合があります。作成後にグラフを変更しないでください！） |
| 機械学習モデルを読み込む               |                                                             transformers.Pipeline, torch.nn.Module, tensorflow.keras.Model |                                                                                                                                            st.cache_resource |
| データベース接続を初期化する           | pyodbc.Connection, sqlalchemy.engine.base.Engine, psycopg2.connection, mysql.connector.MySQLConnection, sqlite3.Connection |                                                                                                                                            st.cache_resource |
| 永続的なファイルハンドルを開く         |                                                                                                         \_io.TextIOWrapper |                                                                                                                                            st.cache_resource |
| 永続的なスレッドを開く                 |                                                                                                           threading.thread |                                                                                                                                            st.cache_resource |


## 高度な使い方

### キャッシュのサイズと期間の制御

アプリが長時間実行され、関数をキャッシュし続けると、次の2つの問題に直面する可能性があります：

1. キャッシュが大きすぎてメモリ不足になる。
2. キャッシュ内のオブジェクトが古くなる（例：古いデータベースのデータをキャッシュしてしまう）。

これらの問題に対処するために、両方のキャッシングデコレーターで使用できる `ttl` と `max_entries` パラメータがあります。


**`ttl`（time-to-live）パラメータ**

`ttl` はキャッシュされた関数に有効期限を設定します。この期限が切れ、関数が再度呼び出されると、アプリは古いキャッシュ値を破棄し、関数を再実行します。その後、新たに計算された値がキャッシュに保存されます。この動作は、古いデータを防止する（問題2）およびキャッシュが大きくなりすぎるのを防ぐ（問題1）ために役立ちます。特にデータベースやAPIからデータを取得する場合、`ttl` を設定して古いデータを使用しないようにすることが重要です。次の例を見てみましょう：

```python
@st.cache_data(ttl=3600)  # 👈 データを1時間（=3600秒）キャッシュ
def get_api_data():
    data = api.get(...)
    return data
```

> [!Tip]
> `ttl` の値を `timedelta` を使って設定することもできます。例えば `ttl=datetime.timedelta(hours=1)` のようにします。


**`max_entries` パラメータ**

`max_entries` はキャッシュ内のエントリ数の最大値を設定します。キャッシュエントリ数の上限を設定することは、特に大きなオブジェクトをキャッシュする場合にメモリを制限するために役立ちます（問題1）。キャッシュが満杯になると、最も古いエントリが削除され、新しいエントリが追加されます。次の例を見てみましょう：

```python
@st.cache_data(max_entries=1000)  # 👈 キャッシュ内のエントリを最大1000に制限
def get_large_array(seed):
    np.random.seed(seed)
    arr = np.random.rand(100000)
    return arr
```

### スピナーのカスタマイズ

デフォルトでは、キャッシュされた関数が実行中にStreamlitはアプリ内に小さなロードスピナーを表示します。`show_spinner` パラメータを使って、これを簡単にカスタマイズできます。これは、両方のキャッシングデコレーターで使用可能です：

```python
@st.cache_data(show_spinner=False)  # 👈 スピナーを無効にする
def get_api_data():
    data = api.get(...)
    return data

@st.cache_data(show_spinner="APIからデータを取得中...")  # 👈 スピナーにカスタムテキストを設定
def get_api_data():
    data = api.get(...)
    return data
```

### 入力パラメータの除外

キャッシュされた関数では、すべての入力パラメータがハッシュ可能である必要があります。ここでは、その理由と意味を簡単に説明します。関数が呼び出されると、Streamlitはそのパラメータ値を見て、以前にキャッシュされたかどうかを確認します。そのため、パラメータ値を関数呼び出し間で比較する信頼性のある方法が必要です。文字列や整数の場合は簡単ですが、任意のオブジェクトでは複雑です。Streamlitは[ハッシュ化](https://en.wikipedia.org/wiki/Hash_function)を使用してこの問題を解決します。パラメータを安定したキーに変換し、そのキーを保存します。次の関数呼び出しで、パラメータを再度ハッシュ化し、保存されたハッシュキーと比較します。

しかし、すべてのパラメータがハッシュ可能なわけではありません。例えば、ハッシュ不可能なデータベース接続や機械学習モデルをキャッシュされた関数に渡す場合があります。この場合、キャッシュから入力パラメータを除外できます。パラメータ名の前にアンダースコアを付けるだけで（例：`_param1`）、そのパラメータはキャッシュには使用されません。他のすべてのパラメータが一致すれば、そのパラメータが変わっていてもStreamlitはキャッシュされた結果を返します。

以下はその例です：

```python
@st.cache_data
def fetch_data(_db_connection, num_rows):  # 👈 _db_connection をハッシュ化しない
    data = _db_connection.fetch(num_rows)
    return data

connection = init_connection()
fetch_data(connection, 10)
```

しかし、ハッシュ不可能なパラメータを受け取る関数をキャッシュしたい場合はどうすればよいでしょうか？例えば、機械学習モデルを入力として受け取り、そのモデルの層の名前を返す関数をキャッシュしたい場合があります。モデルが唯一の入力パラメータであるため、それをキャッシュから除外することはできません。この場合、`hash_funcs` パラメータを使用して、モデルのカスタムハッシュ関数を指定することができます。

### `hash_funcs` パラメータ

前述のとおり、Streamlitのキャッシングデコレーターは入力パラメータとキャッシュされた関数のシグネチャをハッシュして、関数が以前に実行されて結果が保存されているか（「キャッシュヒット」）、または再実行が必要か（「キャッシュミス」）を判断します。Streamlitのハッシュ処理ができない入力パラメータは、名前の前にアンダースコアを付けて無視することができます。ただし、2つの稀なケースでは、これは望ましくありません。つまり、Streamlitがハッシュできないパラメータをハッシュしたい場合です：

1. Streamlitのハッシュメカニズムがパラメータのハッシュに失敗し、`UnhashableParamError` が発生する場合。
2. 特定のパラメータに対してStreamlitのデフォルトのハッシュメカニズムを上書きしたい場合。

これらのケースをそれぞれ例を使って説明します。


#### 例1: カスタムクラスのハッシュ

Streamlitはカスタムクラスのハッシュ方法を知りません。キャッシュされた関数にカスタムクラスを渡すと、Streamlitは `UnhashableParamError` を発生させます。例えば、初期の整数スコアを受け取るカスタムクラス `MyCustomClass` を定義し、スコアを乗数で掛けるキャッシュされた関数 `multiply_score` を定義します：

```python
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

@st.cache_data
def multiply_score(obj: MyCustomClass, multiplier: int) -> int:
    return obj.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(multiply_score(score, multiplier))
```

このアプリを実行すると、Streamlitが `UnhashableParamError` を発生させるのがわかります。これは、`MyCustomClass` のハッシュ方法をStreamlitが知らないためです：

```python
UnhashableParamError: Cannot hash argument 'obj' (of type __main__.MyCustomClass) in 'multiply_score'.
```

これを修正するには、`hash_funcs` パラメータを使用して `MyCustomClass` のハッシュ方法をStreamlitに伝える必要があります。これには、パラメータ名とハッシュ関数の対応を持つ辞書を `hash_funcs` に渡します。どのハッシュ関数を使用するかは開発者が選択できます。この場合、カスタムクラスを入力として受け取り、そのスコアを返すカスタムハッシュ関数 `hash_func` を定義しましょう。スコアがオブジェクトの一意の識別子として使用できるため、それを使用してオブジェクトを決定論的にハッシュします：

```python
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

def hash_func(obj: MyCustomClass) -> int:
    return obj.my_score  # またはオブジェクトを一意に識別する他の値

@st.cache_data(hash_funcs={MyCustomClass: hash_func})
def multiply_score(obj: MyCustomClass, multiplier: int) -> int:
    return obj.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(multiply_score(score, multiplier))
```

これでアプリを実行すると、Streamlitは `UnhashableParamError` を発生させず、アプリが期待通りに動作します。

次に、`multiply_score` が `MyCustomClass` の属性であり、オブジェクト全体をハッシュしたい場合を考えます：

```python
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))
```

このアプリを実行すると、Streamlitが `UnhashableParamError` を発生させるのがわかります。これは、`multiply_score` 内の `self` がハッシュできないためです。この問題を解決する簡単な方法は、Pythonの `hash()` 関数を使用してオブジェクトをハッシュすることです：

```python
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data(hash_funcs={"__main__.MyCustomClass": lambda x: hash(x.my_score)})
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))
```

上記では、ハッシュ関数を `lambda x: hash(x.my_score)` として定義しています。これにより、`MyCustomClass` インスタンスの `my_score` 属性に基づいたハッシュが作成されます。`my_score` が同じであれば、ハッシュも同じです。そのため、`multiply_score` の結果をキャッシュから再取得することが可能です。

もしPythonの `id()` 関数を使ってオブジェクトをハッシュしたくなるかもしれませんが、以下のように書くことができます：

```python
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data(hash_funcs={"__main__.MyCustomClass": id})
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))
```

このアプリを実行すると、`my_score` が変わっていなくても `multiply_score` が毎回再計算されることがわかります。なぜでしょうか？Pythonでは、`id()` はオブジェクトの一意の識別子を返し、そのオブジェクトの生存期間中に変更されません。つまり、`MyCustomClass` の2つのインスタンス間で `my_score` の値が同じであっても、`id()` は異なる値を返すため、異なるハッシュ値が生成されます。結果として、Streamlitはこれらのインスタンスを別々のキャッシュされた値が必要なものとして扱い、`my_score` が変わっていなくても `multiply_score` を毎回再計算します。

このため、`id()` をハッシュ関数として使用することは推奨されず、決定論的で真のハッシュ値を返す関数を使用することが推奨されます。しかし、もし適切な知識を持っている場合は、`id()` をハッシュ関数として使用することもできます。ただし、その影響については十分に理解しておく必要があります。例えば、`id()` は、`@st.cache_resource` 関数の結果を別のキャッシュ関数への入力パラメータとして渡す場合に適切なハッシュ関数です。これは、ハッシュ不可能なオブジェクトタイプ全体に適用されます。

#### Example 2: Hashing a Pydantic model

Let's consider another example where we want to hash a Pydantic model:

```python
import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_data
def identity(person: Person):
    return person

person = identity(Person(name="Lee"))
st.write(f"The person is {person.name}")
```

Above, we define a custom class `Person` using Pydantic's `BaseModel` with a single attribute name. We also define an `identity` function which accepts an instance of `Person` as an arg and returns it without modification. This function is intended to cache the result, therefore, if called multiple times with the same `Person` instance, it won't recompute but return the cached instance.

If you run the app, however, you'll run into a `UnhashableParamError: Cannot hash argument 'person' (of type __main__.Person) in 'identity'.` error. This is because Streamlit does not know how to hash the `Person` class. To fix this, we can use the `hash_funcs` kwarg to tell Streamlit how to hash `Person`.

In the version below, we define a custom hash function `hash_func` that takes the `Person` instance as input and returns the name attribute. We want the name to be the unique identifier of the object, so we can use it to deterministically hash the object:

```python
import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_data(hash_funcs={Person: lambda p: p.name})
def identity(person: Person):
    return person

person = identity(Person(name="Lee"))
st.write(f"The person is {person.name}")
```

#### Example 3: Hashing a ML model

There may be cases where you want to pass your favorite machine learning model to a cached function. For example, let's say you want to pass a TensorFlow model to a cached function, based on what model the user selects in the app. You might try something like this:

```python
import streamlit as st
import tensorflow as tf

@st.cache_resource
def load_base_model(option):
    if option == 1:
        return tf.keras.applications.ResNet50(include_top=False, weights="imagenet")
    else:
        return tf.keras.applications.MobileNetV2(include_top=False, weights="imagenet")

@st.cache_resource
def load_layers(base_model):
    return [layer.name for layer in base_model.layers]

option = st.radio("Model 1 or 2", [1, 2])

base_model = load_base_model(option)

layers = load_layers(base_model)

st.write(layers)
```

In the above app, the user can select one of two models. Based on the selection, the app loads the corresponding model and passes it to `load_layers`. This function then returns the names of the layers in the model. If you run the app, you'll see that Streamlit raises a `UnhashableParamError` since it cannot hash the argument `'base_model' (of type keras.engine.functional.Functional) in 'load_layers'`.

If you disable hashing for `base_model` by prepending an underscore to its name, you'll observe that regardless of which base model is chosen, the layers displayed are same. This subtle bug is due to the fact that the `load_layers` function is not re-run when the base model changes. This is because Streamlit does not hash the `base_model` argument, so it does not know that the function needs to be re-run when the base model changes.

To fix this, we can use the `hash_funcs` kwarg to tell Streamlit how to hash the `base_model` argument. In the version below, we define a custom hash function `hash_func`: `Functional: lambda x: x.name`. Our choice of hash func is informed by our knowledge that the `name` attribute of a `Functional` object or model uniquely identifies it. As long as the `name` attribute remains the same, the hash remains the same. Thus, the result of `load_layers` can be retrieved from the cache without recomputation.

```python
import streamlit as st
import tensorflow as tf
from keras.engine.functional import Functional

@st.cache_resource
def load_base_model(option):
    if option == 1:
        return tf.keras.applications.ResNet50(include_top=False, weights="imagenet")
    else:
        return tf.keras.applications.MobileNetV2(include_top=False, weights="imagenet")

@st.cache_resource(hash_funcs={Functional: lambda x: x.name})
def load_layers(base_model):
    return [layer.name for layer in base_model.layers]

option = st.radio("Model 1 or 2", [1, 2])

base_model = load_base_model(option)

layers = load_layers(base_model)

st.write(layers)
```

In the above case, we could also have used `hash_funcs={Functional: id}` as the hash function. This is because `id` is often the _correct_ hash func when you're passing the result of an `@st.cache_resource` function as the input param to another cached function.

#### Example 4: Overriding Streamlit's default hashing mechanism

Let's consider another example where we want to override Streamlit's default hashing mechanism for a pytz-localized datetime object:

```python
from datetime import datetime
import pytz
import streamlit as st

tz = pytz.timezone("Europe/Berlin")

@st.cache_data
def load_data(dt):
    return dt

now = datetime.now()
st.text(load_data(dt=now))

now_tz = tz.localize(datetime.now())
st.text(load_data(dt=now_tz))
```

It may be surprising to see that although `now` and `now_tz` are of the same `<class 'datetime.datetime'>` type, Streamlit does not how to hash `now_tz` and raises a `UnhashableParamError`. In this case, we can override Streamlit's default hashing mechanism for `datetime` objects by passing a custom hash function to the `hash_funcs` kwarg:

```python
from datetime import datetime

import pytz
import streamlit as st

tz = pytz.timezone("Europe/Berlin")

@st.cache_data(hash_funcs={datetime: lambda x: x.strftime("%a %d %b %Y, %I:%M%p")})
def load_data(dt):
    return dt

now = datetime.now()
st.text(load_data(dt=now))

now_tz = tz.localize(datetime.now())
st.text(load_data(dt=now_tz))
```

Let's now consider a case where we want to override Streamlit's default hashing mechanism for NumPy arrays. While Streamlit natively hashes Pandas and NumPy objects, there may be cases where you want to override Streamlit's default hashing mechanism for these objects.

For example, let's say we create a cache-decorated `show_data` function that accepts a NumPy array and returns it without modification. In the bellow app, `data = df["str"].unique()` (which is a NumPy array) is passed to the `show_data` function.

```python
import time
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def get_data():
    df = pd.DataFrame({"num": [112, 112, 2, 3], "str": ["be", "a", "be", "c"]})
    return df

@st.cache_data
def show_data(data):
    time.sleep(2)  # This makes the function take 2s to run
    return data

df = get_data()
data = df["str"].unique()

st.dataframe(show_data(data))
st.button("Re-run")
```

Since `data` is always the same, we expect the `show_data` function to return the cached value. However, if you run the app, and click the `Re-run` button, you'll notice that the `show_data` function is re-run each time. We can assume this behavior is a consequence of Streamlit's default hashing mechanism for NumPy arrays.

To work around this, let's define a custom hash function `hash_func` that takes a NumPy array as input and returns a string representation of the array:

```python
import time
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def get_data():
    df = pd.DataFrame({"num": [112, 112, 2, 3], "str": ["be", "a", "be", "c"]})
    return df

@st.cache_data(hash_funcs={np.ndarray: str})
def show_data(data):
    time.sleep(2)  # This makes the function take 2s to run
    return data

df = get_data()
data = df["str"].unique()

st.dataframe(show_data(data))
st.button("Re-run")
```

Now if you run the app, and click the `Re-run` button, you'll notice that the `show_data` function is no longer re-run each time. It's important to note here that our choice of hash function was very naive and not necessarily the best choice. For example, if the NumPy array is large, converting it to a string representation may be expensive. In such cases, it is up to you as the developer to define what a good hash function is for your use case.

#### Static elements

Since version 1.16.0, cached functions can contain Streamlit commands! For example, you can do this:

```python
@st.cache_data
def get_api_data():
    data = api.get(...)
    st.success("Fetched data from API!")  # 👈 Show a success message
    return data
```

As we know, Streamlit only runs this function if it hasn't been cached before. On this first run, the `st.success` message will appear in the app. But what happens on subsequent runs? It still shows up! Streamlit realizes that there is an `st.` command inside the cached function, saves it during the first run, and replays it on subsequent runs. Replaying static elements works for both caching decorators.

You can also use this functionality to cache entire parts of your UI:

```python
@st.cache_data
def show_data():
    st.header("Data analysis")
    data = api.get(...)
    st.success("Fetched data from API!")
    st.write("Here is a plot of the data:")
    st.line_chart(data)
    st.write("And here is the raw data:")
    st.dataframe(data)
```

#### Input widgets

You can also use [interactive input widgets](/develop/api-reference/widgets) like `st.slider` or `st.text_input` in cached functions. Widget replay is an experimental feature at the moment. To enable it, you need to set the `experimental_allow_widgets` parameter:

```python
@st.cache_data(experimental_allow_widgets=True)  # 👈 Set the parameter
def get_data():
    num_rows = st.slider("Number of rows to get")  # 👈 Add a slider
    data = api.get(..., num_rows)
    return data
```

Streamlit treats the slider like an additional input parameter to the cached function. If you change the slider position, Streamlit will see if it has already cached the function for this slider value. If yes, it will return the cached value. If not, it will rerun the function using the new slider value.

Using widgets in cached functions is extremely powerful because it lets you cache entire parts of your app. But it can be dangerous! Since Streamlit treats the widget value as an additional input parameter, it can easily lead to excessive memory usage. Imagine your cached function has five sliders and returns a 100 MB DataFrame. Then we'll add 100 MB to the cache for _every permutation_ of these five slider values – even if the sliders do not influence the returned data! These additions can make your cache explode very quickly. Please be aware of this limitation if you use widgets in cached functions. We recommend using this feature only for isolated parts of your UI where the widgets directly influence the cached return value.

<Warning>

Support for widgets in cached functions is experimental. We may change or remove it anytime without warning. Please use it with care!
</Warning>

<Note>

Two widgets are currently not supported in cached functions: `st.file_uploader` and `st.camera_input`. We may support them in the future. Feel free to [open a GitHub issue](https://github.com/streamlit/streamlit/issues) if you need them!
</Note>

### Dealing with large data

As we explained, you should cache data objects with `st.cache_data`. But this can be slow for extremely large data, e.g., DataFrames or arrays with >100 million rows. That's because of the [copying behavior](#copying-behavior) of `st.cache_data`: on the first run, it serializes the return value to bytes and deserializes it on subsequent runs. Both operations take time.

If you're dealing with extremely large data, it can make sense to use `st.cache_resource` instead. It does not create a copy of the return value via serialization/deserialization and is almost instant. But watch out: any mutation to the function's return value (such as dropping a column from a DataFrame or setting a value in an array) directly manipulates the object in the cache. You must ensure this doesn't corrupt your data or lead to crashes. See the section on [Mutation and concurrency issues](#mutation-and-concurrency-issues) below.

When benchmarking `st.cache_data` on pandas DataFrames with four columns, we found that it becomes slow when going beyond 100 million rows. The table shows runtimes for both caching decorators at different numbers of rows (all with four columns):

|                   |                 | 10M rows | 50M rows | 100M rows | 200M rows |
| ----------------- | --------------- | :------: | :------: | :-------: | :-------: |
| st.cache_data     | First run\*     |  0.4 s   |   3 s    |   14 s    |   28 s    |
|                   | Subsequent runs |  0.2 s   |   1 s    |    2 s    |    7 s    |
| st.cache_resource | First run\*     |  0.01 s  |  0.1 s   |   0.2 s   |    1 s    |
|                   | Subsequent runs |   0 s    |   0 s    |    0 s    |    0 s    |

|                                                                                                                                                              |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _\*For the first run, the table only shows the overhead time of using the caching decorator. It does not include the runtime of the cached function itself._ |

### Mutation and concurrency issues

In the sections above, we talked a lot about issues when mutating return objects of cached functions. This topic is complicated! But it's central to understanding the behavior differences between `st.cache_data` and `st.cache_resource`. So let's dive in a bit deeper.

First, we should clearly define what we mean by mutations and concurrency:

- By **mutations**, we mean any changes made to a cached function's return value _after_ that function has been called. I.e. something like this:

  ```python
  @st.cache_data
  def create_list():
      l = [1, 2, 3]

  l = create_list()  # 👈 Call the function
  l[0] = 2  # 👈 Mutate its return value
  ```

- By **concurrency**, we mean that multiple sessions can cause these mutations at the same time. Streamlit is a web framework that needs to handle many users and sessions connecting to an app. If two people view an app at the same time, they will both cause the Python script to rerun, which may manipulate cached return objects at the same time – concurrently.

Mutating cached return objects can be dangerous. It can lead to exceptions in your app and even corrupt your data (which can be worse than a crashed app!). Below, we'll first explain the copying behavior of `st.cache_data` and show how it can avoid mutation issues. Then, we'll show how concurrent mutations can lead to data corruption and how to prevent it.

#### Copying behavior

`st.cache_data` creates a copy of the cached return value each time the function is called. This avoids most mutations and concurrency issues. To understand it in detail, let's go back to the [Uber ridesharing example](#usage) from the section on `st.cache_data` above. We are making two modifications to it:

1. We are using `st.cache_resource` instead of `st.cache_data`. `st.cache_resource` does **not** create a copy of the cached object, so we can see what happens without the copying behavior.
2. After loading the data, we manipulate the returned DataFrame (in place!) by dropping the column `"Lat"`.

Here's the code:

```python
@st.cache_resource   # 👈 Turn off copying behavior
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv")
st.dataframe(df)

df.drop(columns=['Lat'], inplace=True)  # 👈 Mutate the dataframe inplace

st.button("Rerun")
```

Let's run it and see what happens! The first run should work fine. But in the second run, you see an exception: `KeyError: "['Lat'] not found in axis"`. Why is that happening? Let's go step by step:

- On the first run, Streamlit runs `load_data` and stores the resulting DataFrame in the cache. Since we're using `st.cache_resource`, it does **not** create a copy but stores the original DataFrame.
- Then we drop the column `"Lat"` from the DataFrame. Note that this is dropping the column from the _original_ DataFrame stored in the cache. We are manipulating it!
- On the second run, Streamlit returns that exact same manipulated DataFrame from the cache. It does not have the column `"Lat"` anymore! So our call to `df.drop` results in an exception. Pandas cannot drop a column that doesn't exist.

The copying behavior of `st.cache_data` prevents this kind of mutation error. Mutations can only affect a specific copy and not the underlying object in the cache. The next rerun will get its own, unmutated copy of the DataFrame. You can try it yourself, just replace `st.cache_resource` with `st.cache_data` above, and you'll see that everything works.

Because of this copying behavior, `st.cache_data` is the recommended way to cache data transforms and computations – anything that returns a serializable object.

#### Concurrency issues

Now let's look at what can happen when multiple users concurrently mutate an object in the cache. Let's say you have a function that returns a list. Again, we are using `st.cache_resource` to cache it so that we are not creating a copy:

```python
@st.cache_resource
def create_list():
    l = [1, 2, 3]
    return l

l = create_list()
first_list_value = l[0]
l[0] = first_list_value + 1

st.write("l[0] is:", l[0])
```

Let's say user A runs the app. They will see the following output:

```python
l[0] is: 2
```

Let's say another user, B, visits the app right after. In contrast to user A, they will see the following output:

```python
l[0] is: 3
```

Now, user A reruns the app immediately after user B. They will see the following output:

```python
l[0] is: 4
```

What is happening here? Why are all outputs different?

- When user A visits the app, `create_list()` is called, and the list `[1, 2, 3]` is stored in the cache. This list is then returned to user A. The first value of the list, `1`, is assigned to `first_list_value` , and `l[0]` is changed to `2`.
- When user B visits the app, `create_list()` returns the mutated list from the cache: `[2, 2, 3]`. The first value of the list, `2`, is assigned to `first_list_value` and `l[0]` is changed to `3`.
- When user A reruns the app, `create_list()` returns the mutated list again: `[3, 2, 3]`. The first value of the list, `3`, is assigned to `first_list_value,` and `l[0]` is changed to 4.

If you think about it, this makes sense. Users A and B use the same list object (the one stored in the cache). And since the list object is mutated, user A's change to the list object is also reflected in user B's app.

This is why you must be careful about mutating objects cached with `st.cache_resource`, especially when multiple users access the app concurrently. If we had used `st.cache_data` instead of `st.cache_resource`, the app would have copied the list object for each user, and the above example would have worked as expected – users A and B would have both seen:

```python
l[0] is: 2
```

<Note>

This toy example might seem benign. But data corruption can be extremely dangerous! Imagine we had worked with the financial records of a large bank here. You surely don't want to wake up with less money on your account just because someone used the wrong caching decorator 😉

</Note>

## Migrating from st.cache

We introduced the caching commands described above in Streamlit 1.18.0. Before that, we had one catch-all command `st.cache`. Using it was often confusing, resulted in weird exceptions, and was slow. That's why we replaced `st.cache` with the new commands in 1.18.0 (read more in this [blog post](https://blog.streamlit.io/introducing-two-new-caching-commands-to-replace-st-cache/)). The new commands provide a more intuitive and efficient way to cache your data and resources and are intended to replace `st.cache` in all new development.

If your app is still using `st.cache`, don't despair! Here are a few notes on migrating:

- Streamlit will show a deprecation warning if your app uses `st.cache`.
- We will not remove `st.cache` soon, so you don't need to worry about your 2-year-old app breaking. But we encourage you to try the new commands going forward – they will be way less annoying!
- Switching code to the new commands should be easy in most cases. To decide whether to use `st.cache_data` or `st.cache_resource`, read [Deciding which caching decorator to use](#deciding-which-caching-decorator-to-use). Streamlit will also recognize common use cases and show hints right in the deprecation warnings.
- Most parameters from `st.cache` are also present in the new commands, with a few exceptions:
  - `allow_output_mutation` does not exist anymore. You can safely delete it. Just make sure you use the right caching command for your use case.
  - `suppress_st_warning` does not exist anymore. You can safely delete it. Cached functions can now contain Streamlit commands and will replay them. If you want to use widgets inside cached functions, set `experimental_allow_widgets=True`. See [Input widgets](#input-widgets) for an example.

If you have any questions or issues during the migration process, please contact us on the [forum](https://discuss.streamlit.io/), and we will be happy to assist you. 🎈
