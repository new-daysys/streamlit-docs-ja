---
title: Create an app
slug: /get-started/tutorials/create-an-app
---

# アプリの作成

ここまで進んだということは、[Streamlit をインストール](../installation.md)し、[基本的な概念](../fundamentals/main-concepts.md)と[少し高度な概念](../fundamentals/advanced-concepts.md)を学んだ可能性が高いですね。まだの場合は、今が確認する良い機会です。

Streamlit の使い方を学ぶ最も簡単な方法は、自分で試してみることです。このガイドを読み進めながら、各メソッドを実際に試してみましょう。
アプリが実行中であれば、スクリプトに新しい要素を追加して保存するたびに、StreamlitのUIがアプリを再実行して変更を確認するかどうかを尋ねてきます。
これにより、素早いインタラクティブな開発サイクルを回せます。
コードを書いて保存し、出力を確認し、さらにコードを追加していくと、最終的に満足する結果に到達できます。

このガイドの目標は、Streamlit を使ってデータやモデルのためのインタラクティブなアプリを作成し、途中でStreamlitを活用してコードを確認、デバッグ、改善、共有することです。

このガイドでは、Streamlit のコア機能を使って、ニューヨーク市の Uber のピックアップとドロップオフに関する公開データセットを探索するインタラクティブなアプリを作成します。
終了時には、データを取得してキャッシュする方法、チャートを描く方法、地図上に情報をプロットする方法、そしてスライダーのようなインタラクティブなウィジェットを使用して
結果をフィルタリングする方法を習得できます。

> [!Tip]
> すべてを一度に見たい場合は、完全なスクリプトが以下にあります。

## 最初のアプリを作成する

Streamlitは、データアプリを作成するためのツールであるだけでなく、アプリやアイデアを共有し、お互いに助け合うクリエイターのコミュニティでもあります。
ぜひコミュニティフォーラムに参加してください！質問やアイデアをお聞かせいただき、バグ解決のお手伝いもいたします。今日ぜひ立ち寄ってください！

1. 最初のステップは、新しいPythonスクリプトを作成することです。`uber_pickups.py` と名付けましょう。

2. `uber_pickups.py` をお気に入りの IDE またはテキストエディタで開き、次の行を追加します：

   ```python
   import streamlit as st
   import pandas as pd
   import numpy as np
   ```

3. すべての良いアプリにはタイトルが必要ですので、次のコードを追加します：

   ```python
   st.title('Uber pickups in NYC')
   ```

4. 次に、コマンドラインから Streamlit を実行します：

   ```bash
   streamlit run uber_pickups.py
   ```

   Streamlit アプリの実行は、他の Python スクリプトと同じように行われます。アプリを表示する必要がある場合は、いつでもこのコマンドを使用できます。

5. いつものように、アプリは自動的にブラウザの新しいタブで開くはずです。

## データを取得する

アプリができたので、次に行うことは、ニューヨーク市の Uber のピックアップとドロップオフのデータセットを取得することです。

1. まず、データを読み込む関数を作成しましょう。スクリプトに以下のコードを追加してください：

   ```python
   DATE_COLUMN = 'date/time'
   DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

   def load_data(nrows):
       data = pd.read_csv(DATA_URL, nrows=nrows)
       lowercase = lambda x: str(x).lower()
       data.rename(lowercase, axis='columns', inplace=True)
       data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
       return data
   ```
   
   ご覧の通り、`load_data` は単純な関数で、データをダウンロードし、それを Pandas のデータフレームに格納し、日付の列をテキストから日時に変換します。
   この関数は1つのパラメータ (`nrows`) を受け取ります。このパラメータは、データフレームに読み込む行数を指定します。

2. 次に、関数をテストして出力を確認しましょう。関数の下に次の行を追加してください：

   ```python
   # Create a text element and let the reader know the data is loading.
   data_load_state = st.text('Loading data...')
   # Load 10,000 rows of data into the dataframe.
   data = load_data(10000)
   # Notify the reader that the data was successfully loaded.
   data_load_state.text('Loading data...done!')
   ```
   
   これにより、アプリの右上にいくつかのボタンが表示され、アプリを再実行するかどうかを尋ねられます。
   **Always rerun** を選択すると、保存するたびに変更が自動的に反映されます。

うーん、少し物足りないですね...

実際のところ、データをダウンロードして10,000行をデータフレームに読み込むには時間がかかります。
また、日付の列を日時型に変換するのもすぐには終わりません。アプリが更新されるたびにデータを再読み込みしたくないですよね。
幸運なことに、Streamlitではデータをキャッシュすることができます。

## 簡単なキャッシュ

1. `load_data` 関数の宣言の前に `@st.cache_data` を追加してみましょう：

   ```python
   @st.cache_data
   def load_data(nrows):
   ```

2. スクリプトを保存すると、Streamlit が自動的にアプリを再実行します。
   このスクリプトを `@st.cache_data` と一緒に実行するのは初めてなので、最初は特に変化は見られません。
   キャッシングの力を実感できるように、もう少しファイルを調整しましょう。

3. `data_load_state.text('Loading data...done!')` の行を以下のように置き換えます：

   ```python
   data_load_state.text("Done! (using st.cache_data)")
   ```

4. さて、保存してみましょう。追加した行がすぐに表示されるのがわかりますか？
   一歩引いて考えると、これは実際に驚くべきことです。
   背後では何かマジカルなことが起こっており、たった一行のコードでそれが有効になるのです。

翻訳しました。

---

### どう動いてるの？

ここで少し時間を取って、`@st.cache_data` が実際にどのように機能するかを説明しましょう。

Streamlit のキャッシュアノテーションを使って関数にマークを付けると、Streamlit はその関数が呼び出されるたびに以下の2つのことをチェックします：

1. 関数呼び出しで使用した入力パラメータ。
2. 関数内のコード。

これらの要素が、初めて Streamlit に認識されたものである場合（入力パラメータと関数コードが初めての組み合わせである場合）、関数を実行し、その結果をローカルキャッシュに保存します。次回、同じ関数が呼び出される際に、2つの値が変更されていない場合、Streamlit は関数の実行をスキップできると判断します。その代わりに、キャッシュから出力を読み込み、それを呼び出し元に渡します——まるで魔法のようです。

「でも、ちょっと待って、」とあなたは思っているかもしれません。「これはあまりにも良すぎる話だ。何か制約があるんじゃないの？」

はい、いくつか制約があります：

1. Streamlit は現在の作業ディレクトリ内での変更しか確認しません。もし Python ライブラリをアップグレードした場合、そのライブラリが作業ディレクトリ内にインストールされている場合にのみ、Streamlit のキャッシュは変更を検知します。
2. 関数が非決定的（つまり、ランダムな数値に依存する）場合や、外部の時間変動データソース（例: リアルタイムの株式市場ティッカーサービス）からデータを取得する場合、キャッシュされた値は更新されません。
3. 最後に、`st.cache_data` でキャッシュされた関数の出力を変更することは避けるべきです。キャッシュされた値は参照によって保存されるためです。

これらの制約は覚えておくべき重要なポイントですが、実際のところ、それほど問題になることは少ないです。そのため、キャッシュは非常に革新的な機能となります。

> [!Tip]
> コード内に長時間実行される計算がある場合、可能であればそれをリファクタリングし、`@st.cache_data` を使用することを検討してください。
> 詳細は[キャッシング](/develop/concepts/architecture/caching)を参照してください。

Streamlit でのキャッシングの仕組みを理解したところで、Uber のピックアップデータに戻りましょう。

翻訳しました。

---

## 生データの確認

作業を始める前に、扱っている生データを確認することは常に良いアイデアです。アプリにサブヘッダーと生データの出力を追加してみましょう：

```python
st.subheader('Raw data')
st.write(data)
```

[基本概念](/get-started/fundamentals/main-concepts) ガイドで学んだように、[`st.write`](/develop/api-reference/write-magic/st.write) は、
渡されたほぼすべてのデータをレンダリングします。この場合、データフレームを渡しているため、インタラクティブなテーブルとして表示されます。

[`st.write`](/develop/api-reference/write-magic/st.write) は入力のデータ型に基づいて、適切な方法でデータを表示しようとします。
もし期待通りに表示されない場合は、[`st.dataframe`](/develop/api-reference/data/st.dataframe) のような専用のコマンドを使用することもできます。
詳細なリストは [APIリファレンス](/develop/api-reference) を参照してください。

翻訳しました。

---

## ヒストグラムの描画

データセットを確認して何が含まれているかを把握したところで、次のステップに進み、ニューヨーク市における Uber の最も忙しい時間帯を確認するためにヒストグラムを描きましょう。

1. まず、生データセクションのすぐ下にサブヘッダーを追加します：

   ```python
   st.subheader('Number of pickups by hour')
   ```

2. NumPy を使用して、ピックアップ時間を1時間ごとに分けたヒストグラムを生成します：

   ```python
   hist_values = np.histogram(
       data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
   ```

3. 次に、Streamlit の[`st.bar_chart()`](/develop/api-reference/charts/st.bar_chart) メソッドを使って、このヒストグラムを描画します：

   ```python
   st.bar_chart(hist_values)
   ```

4. スクリプトを保存します。このヒストグラムはすぐにアプリに表示されるはずです。確認してみると、最も忙しい時間は17:00（午後5時）のようです。

この図を描画するために、Streamlit のネイティブメソッドである `bar_chart()` を使用しましたが、Streamlitは Altair、Bokeh、Plotly、Matplotlib などのより複雑なチャートライブラリもサポートしています。詳細なリストは、[サポートされているチャートライブラリ](/develop/api-reference/charts) をご覧ください。

翻訳しました。

---

## データを地図上にプロットする

Uber のデータセットを使ったヒストグラムで、ピックアップの最も忙しい時間帯を特定できましたが、ピックアップが市内のどこに集中しているのかを確認したい場合はどうでしょうか。棒グラフを使ってこのデータを表示することもできますが、緯度と経度に精通していない限り、解釈が難しいでしょう。ピックアップの集中を表示するために、Streamlit の[`st.map()`](/develop/api-reference/charts/st.map) 関数を使ってニューヨーク市の地図にデータを重ねて表示しましょう。

1. セクションのサブヘッダーを追加します：

   ```python
   st.subheader('Map of all pickups')
   ```

2. `st.map()` 関数を使用してデータをプロットします：

   ```python
   st.map(data)
   ```

3. スクリプトを保存します。この地図は完全にインタラクティブです。少しパニングやズームを試してみてください。

ヒストグラムを描いた後、Uber のピックアップの最も忙しい時間帯が 17:00 であることが分かりました。次に、17:00 時点でのピックアップの集中を表示するために地図を再描画しましょう。

1. 次のコードスニペットを見つけます：

   ```python
   st.subheader('Map of all pickups')
   st.map(data)
   ```

2. これを次のコードに置き換えます：

   ```python
   hour_to_filter = 17
   filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
   st.subheader(f'Map of all pickups at {hour_to_filter}:00')
   st.map(filtered_data)
   ```

3. データが即座に更新されるのが確認できるはずです。

この地図を描画するために、Streamlit に組み込まれている[`st.map`](/develop/api-reference/charts/st.map) 関数を使用しましたが、より複雑な地図データを視覚化したい場合は、[`st.pydeck_chart`](/develop/api-reference/charts/st.pydeck_chart) もぜひご覧ください。

## Filter results with a slider

In the last section, when you drew the map, the time used to filter results was
hardcoded into the script, but what if we wanted to let a reader dynamically
filter the data in real time? Using Streamlit's widgets you can. Let's add a
slider to the app with the `st.slider()` method.

1. Locate `hour_to_filter` and replace it with this code snippet:

   ```python
   hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
   ```

2. Use the slider and watch the map update in real time.

## Use a button to toggle data

Sliders are just one way to dynamically change the composition of your app.
Let's use the [`st.checkbox`](/develop/api-reference/widgets/st.checkbox) function to add a
checkbox to your app. We'll use this checkbox to show/hide the raw data
table at the top of your app.

1. Locate these lines:

   ```python
   st.subheader('Raw data')
   st.write(data)
   ```

2. Replace these lines with the following code:

   ```python
   if st.checkbox('Show raw data'):
       st.subheader('Raw data')
       st.write(data)
   ```

We're sure you've got your own ideas. When you're done with this tutorial, check out all the widgets that Streamlit exposes in our [API Reference](/develop/api-reference).

## Let's put it all together

That's it, you've made it to the end. Here's the complete script for our interactive app.

<Tip>

If you've skipped ahead, after you've created your script, the command to run
Streamlit is `streamlit run [app name]`.

</Tip>

```python
import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
```

## Share your app

After you’ve built a Streamlit app, it's time to share it! To show it off to the world you can use **Streamlit Community Cloud** to deploy, manage, and share your app for free.

It works in 3 simple steps:

1. Put your app in a public GitHub repo (and make sure it has a requirements.txt!)
2. Sign into [share.streamlit.io](https://share.streamlit.io)
3. Click 'Deploy an app' and then paste in your GitHub URL

That's it! 🎈 You now have a publicly deployed app that you can share with the world. Click to learn more about [how to use Streamlit Community Cloud](/deploy/streamlit-community-cloud).

## Get help

That's it for getting started, now you can go and build your own apps! If you
run into difficulties here are a few things you can do.

- Check out our [community forum](https://discuss.streamlit.io/) and post a question
- Quick help from command line with `streamlit help`
- Go through our [Knowledge Base](/knowledge-base) for tips, step-by-step tutorials, and articles that answer your questions about creating and deploying Streamlit apps.
- Read more documentation! Check out:
  - [Concepts](/develop/concepts) for things like caching, theming, and adding statefulness to apps.
  - [API reference](/develop/api-reference/) for examples of every Streamlit command.
