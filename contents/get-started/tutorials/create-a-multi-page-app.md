---
title: Create a multipage app
slug: /get-started/tutorials/create-a-multipage-app
---

## マルチページアプリの作成

[さらなる機能](/contents/get-started/fundamentals/additional-features.md)では、マルチページアプリについて説明し、ページの定義方法、アプリの構造と実行、ユーザーインターフェースでのページ間のナビゲーションについて紹介しました。詳しくは、[マルチページアプリのガイド](/contents/develop/concepts/multipage-apps.md)をご覧ください。

このガイドでは、`streamlit hello` アプリをマルチページアプリに変換することで理解を深め、実際に活用してみましょう！

## マルチページにする理由

Streamlit 1.10.0より前は、`streamlit hello` コマンドは大きなシングルページアプリでした。マルチページのサポートがなかったため、サイドバーの `st.selectbox` を使用してアプリの内容を分割し、実行するコンテンツを選択していました。コンテンツは、プロット、マッピング、データフレームの3つのデモで構成されています。

以下は、そのコードとシングルページアプリの例です：

<details>

<summary><b><code>hello.py</code></b> (👈 Toggle to expand)</summary> 

```python
import streamlit as st

def intro():
    import streamlit as st

    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what Streamlit can do!

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

def mapping_demo():
    import streamlit as st
    import pandas as pd
    import pydeck as pdk

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart)
to display geospatial data.
"""
    )

    @st.cache_data
    def from_data_file(filename):
        url = (
            "http://raw.githubusercontent.com/streamlit/"
            "example-data/master/hello/v1/%s" % filename
        )
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            ),
            "Bart Stop Names": pdk.Layer(
                "TextLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_text="name",
                get_color=[0, 0, 0, 200],
                get_size=15,
                get_alignment_baseline="'bottom'",
            ),
            "Outbound Flow": pdk.Layer(
                "ArcLayer",
                data=from_data_file("bart_path_stats.json"),
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[200, 30, 0, 160],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 37.76,
                        "longitude": -122.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

def plotting_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.

(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)
"""
    )

    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

page_names_to_funcs = {
    "—": intro,
    "Plotting Demo": plotting_demo,
    "Mapping Demo": mapping_demo,
    "DataFrame Demo": data_frame_demo
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
```

</details>

このファイルがどれほど大きいかに気づくでしょう！
各アプリの「ページ」は関数として記述され、`selectbox` を使用して表示するページを選択しています。
アプリが大きくなるにつれて、コードの保守には多くの追加作業が必要になります。
また、`st.selectbox` のUIで「ページ」を選択することに制限されており、`st.set_page_config` を使って個別のページタイトルをカスタマイズできず、
URLを使ってページ間をナビゲートすることもできません。

## 既存のアプリをマルチページアプリに変換する

シングルページアプリの制約を確認したところで、次に何をすべきでしょうか？前のセクションで学んだ知識を活かして、既存のアプリをマルチページアプリに変換することができます！大まかに、次のステップを実行します：

1. 「エントリーポイントファイル」（`hello.py`）があるフォルダに新しい `pages` フォルダを作成します。
2. エントリーポイントファイルの名前を `Hello.py` に変更して、サイドバーのタイトルを大文字にします。
3. `pages` フォルダ内に次の3つの新しいファイルを作成します：
   - `pages/1_📈_Plotting_Demo.py`
   - `pages/2_🌍_Mapping_Demo.py`
   - `pages/3_📊_DataFrame_Demo.py`
4. `plotting_demo`、`mapping_demo`、`data_frame_demo` 関数の内容をステップ3で作成した対応する新しいファイルに移動します。
5. `streamlit run Hello.py` を実行して、新しく変換したマルチページアプリを表示します！

では、プロセスの各ステップを確認し、対応するコードの変更を見ていきましょう。

## エントリポイントファイルを作成する

<details open>
<summary><code>Hello.py</code></summary>

```python
import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)
```

</details>

エントリーポイントファイルの名前を `Hello.py` に変更すると、サイドバーのタイトルが大文字になり、イントロページのコードのみが含まれます。さらに、`st.set_page_config` を使用して、ブラウザタブに表示されるページタイトルやファビコンをカスタマイズすることができます。
この設定は、各ページに対しても行うことができます！

ご覧のとおり、サイドバーにはまだページラベルが表示されていません。これは、まだページを作成していないためです。

## 複数ページの作成

ここで覚えておくべきポイント：

1. Pythonファイルの名前の先頭に数字を追加することで、マルチページアプリ(MPA)のページの順序を変更できます。ファイル名の先頭に「1」を追加すると、Streamlitはそのファイルをリストの最初に表示します。
2. 各Streamlitアプリの名前はファイル名によって決まるため、アプリ名を変更する場合はファイル名を変更する必要があります！
3. ファイル名に絵文字を追加することで、アプリに楽しい要素を加えることができます。これらの絵文字はStreamlitアプリ内で表示されます。
4. 各ページにはファイル名で定義された独自のURLが付きます。

以下の方法でこれを実現します！新しいページごとに、`pages` フォルダ内に新しいファイルを作成し、対応するデモコードを追加します。

<details>

<summary><code>pages/1_📈_Plotting_Demo.py</code></summary>

```python
import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
```

</details>


<details>
<summary><code>pages/2_🌍_Mapping_Demo.py</code></summary>

```python
import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write(
    """This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)


@st.cache_data
def from_data_file(filename):
    url = (
        "http://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename
    )
    return pd.read_json(url)


try:
    ALL_LAYERS = {
        "Bike Rentals": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("bike_rental_stats.json"),
            get_position=["lon", "lat"],
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "Bart Stop Exits": pdk.Layer(
            "ScatterplotLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[exits]",
            radius_scale=0.05,
        ),
        "Bart Stop Names": pdk.Layer(
            "TextLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),
        "Outbound Flow": pdk.Layer(
            "ArcLayer",
            data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    }
    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 37.76,
                    "longitude": -122.4,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
```

</details>


<details>
<summary><code>pages/3_📊_DataFrame_Demo.py</code></summary>

```python
import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)


@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


try:
    df = get_UN_data()
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### Gross Agricultural Production ($B)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
```

</details>

追加ページが作成されたので、以下の最終ステップでそれらをすべてまとめましょう。

## マルチページアプリを実行する

新しく変換したマルチページアプリを実行するには、次のコマンドを実行します：

```bash
streamlit run Hello.py
```

これで完了です！`Hello.py` スクリプトがアプリのメインページに対応し、Streamlitが `pages` フォルダ内で見つけた他のスクリプトも、サイドバーに表示される新しいページセレクターに追加されます。

## 次のステップ

おめでとうございます！🎉 ここまで読み進めたあなたは、シングルページアプリとマルチページアプリの両方を作成する方法を学んだはずです。
ここからは、あなたの創造力次第です！アプリにページを追加することがこれまで以上に簡単になったので、どんなアプリを作成するか楽しみにしています。
練習として、今回作成したアプリにさらにページを追加してみてください。
また、フォーラムであなたのマルチページアプリを Streamlit コミュニティに紹介することもできます！🎈

ここから始めるためのいくつかのリソースを紹介します：

- Streamlit の[Community Cloud](/contents/deploy/streamlit-community-cloud.md) で、アプリを無料でデプロイ。
- [コミュニティフォーラム](https://discuss.streamlit.io/c/streamlit-examples/9) で質問を投稿したり、マルチページアプリを共有したり。
- [マルチページアプリ](/contents/develop/concepts/multipage-apps) に関するドキュメントをチェック。
- キャッシング、テーマ設定、アプリに状態を持たせる方法については[コンセプト](/contents/develop/concepts) を読んでみましょう。
- Streamlit のすべてのコマンドの例を確認するために、[APIリファレンス](/contents/develop/api-reference/) を参照。
