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

## Fetch some data

Now that you have an app, the next thing you'll need to do is fetch the Uber
dataset for pickups and drop-offs in New York City.

1. Let's start by writing a function to load the data. Add this code to your
   script:

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

   You'll notice that `load_data` is a plain old function that downloads some
   data, puts it in a Pandas dataframe, and converts the date column from text
   to datetime. The function accepts a single parameter (`nrows`), which
   specifies the number of rows that you want to load into the dataframe.

2. Now let's test the function and review the output. Below your function, add
   these lines:

   ```python
   # Create a text element and let the reader know the data is loading.
   data_load_state = st.text('Loading data...')
   # Load 10,000 rows of data into the dataframe.
   data = load_data(10000)
   # Notify the reader that the data was successfully loaded.
   data_load_state.text('Loading data...done!')
   ```

   You'll see a few buttons in the upper-right corner of your app asking if
   you'd like to rerun the app. Choose **Always rerun**, and you'll see your
   changes automatically each time you save.

Ok, that's underwhelming...

It turns out that it takes a long time to download data, and load 10,000 lines
into a dataframe. Converting the date column into datetime isn’t a quick job
either. You don’t want to reload the data each time the app is updated –
luckily Streamlit allows you to cache the data.

## Effortless caching

1. Try adding `@st.cache_data` before the `load_data` declaration:

   ```python
   @st.cache_data
   def load_data(nrows):
   ```

2. Then save the script, and Streamlit will automatically rerun your app. Since
   this is the first time you’re running the script with `@st.cache_data`, you won't
   see anything change. Let’s tweak your file a little bit more so that you can
   see the power of caching.

3. Replace the line `data_load_state.text('Loading data...done!')` with this:

   ```python
   data_load_state.text("Done! (using st.cache_data)")
   ```

4. Now save. See how the line you added appeared immediately? If you take a
   step back for a second, this is actually quite amazing. Something magical is
   happening behind the scenes, and it only takes one line of code to activate
   it.

### How's it work?

Let's take a few minutes to discuss how `@st.cache_data` actually works.

When you mark a function with Streamlit’s cache annotation, it tells Streamlit
that whenever the function is called that it should check two things:

1. The input parameters you used for the function call.
2. The code inside the function.

If this is the first time Streamlit has seen both these items, with these exact
values, and in this exact combination, it runs the function and stores the
result in a local cache. The next time the function is called, if the two
values haven't changed, then Streamlit knows it can skip executing the function
altogether. Instead, it reads the output from the local cache and passes it on
to the caller -- like magic.

"But, wait a second," you’re saying to yourself, "this sounds too good to be
true. What are the limitations of all this awesomesauce?"

Well, there are a few:

1. Streamlit will only check for changes within the current working directory.
   If you upgrade a Python library, Streamlit's cache will only notice this if
   that library is installed inside your working directory.
2. If your function is not deterministic (that is, its output depends on random
   numbers), or if it pulls data from an external time-varying source (for
   example, a live stock market ticker service) the cached value will be
   none-the-wiser.
3. Lastly, you should avoid mutating the output of a function cached with `st.cache_data` since cached
   values are stored by reference.

While these limitations are important to keep in mind, they tend not to be an
issue a surprising amount of the time. Those times, this cache is really
transformational.

<Tip>

Whenever you have a long-running computation in your code, consider
refactoring it so you can use `@st.cache_data`, if possible. Please read [Caching](/develop/concepts/architecture/caching) for more details.

</Tip>

Now that you know how caching with Streamlit works, let’s get back to the Uber
pickup data.

## Inspect the raw data

It's always a good idea to take a look at the raw data you're working with
before you start working with it. Let's add a subheader and a printout of the
raw data to the app:

```python
st.subheader('Raw data')
st.write(data)
```

In the [Basic concepts](/get-started/fundamentals/main-concepts) guide you learned that
[`st.write`](/develop/api-reference/write-magic/st.write) will render almost anything you pass
to it. In this case, you're passing in a dataframe and it's rendering as an
interactive table.

[`st.write`](/develop/api-reference/write-magic/st.write) tries to do the right thing based on
the data type of the input. If it isn't doing what you expect you can use a
specialized command like [`st.dataframe`](/develop/api-reference/data/st.dataframe)
instead. For a full list, see [API reference](/develop/api-reference).

## Draw a histogram

Now that you've had a chance to take a look at the dataset and observe what's
available, let's take things a step further and draw a histogram to see what
Uber's busiest hours are in New York City.

1. To start, let's add a subheader just below the raw data section:

   ```python
   st.subheader('Number of pickups by hour')
   ```

2. Use NumPy to generate a histogram that breaks down pickup times binned by
   hour:

   ```python
   hist_values = np.histogram(
       data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
   ```

3. Now, let's use Streamlit's
   [`st.bar_chart()`](/develop/api-reference/charts/st.bar_chart) method to draw this
   histogram.

   ```python
   st.bar_chart(hist_values)
   ```

4. Save your script. This histogram should show up in your app right away.
   After a quick review, it looks like the busiest time is 17:00 (5 P.M.).

To draw this diagram we used Streamlit's native `bar_chart()` method, but it's
important to know that Streamlit supports more complex charting libraries like
Altair, Bokeh, Plotly, Matplotlib and more. For a full list, see
[supported charting libraries](/develop/api-reference/charts).

## Plot data on a map

Using a histogram with Uber's dataset helped us determine what the busiest
times are for pickups, but what if we wanted to figure out where pickups were
concentrated throughout the city. While you could use a bar chart to show this
data, it wouldn't be easy to interpret unless you were intimately familiar with
latitudinal and longitudinal coordinates in the city. To show pickup
concentration, let's use Streamlit [`st.map()`](/develop/api-reference/charts/st.map)
function to overlay the data on a map of New York City.

1. Add a subheader for the section:

   ```python
   st.subheader('Map of all pickups')
   ```

2. Use the `st.map()` function to plot the data:

   ```python
   st.map(data)
   ```

3. Save your script. The map is fully interactive. Give it a try by panning or
   zooming in a bit.

After drawing your histogram, you determined that the busiest hour for Uber
pickups was 17:00. Let's redraw the map to show the concentration of pickups
at 17:00.

1. Locate the following code snippet:

   ```python
   st.subheader('Map of all pickups')
   st.map(data)
   ```

2. Replace it with:

   ```python
   hour_to_filter = 17
   filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
   st.subheader(f'Map of all pickups at {hour_to_filter}:00')
   st.map(filtered_data)
   ```

3. You should see the data update instantly.

To draw this map we used the [`st.map`](/develop/api-reference/charts/st.map) function that's built into Streamlit, but
if you'd like to visualize complex map data, we encourage you to take a look at
the [`st.pydeck_chart`](/develop/api-reference/charts/st.pydeck_chart).

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
