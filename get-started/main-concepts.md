# 基本的な概念

## 基本コンセプト
Streamlit の基本コンセプトを学びます。
Streamlit アプリはどのように構成されているか?    
どのように動作するのか?    
どのようにして魔法のように Web ページ上のデータを取得するのでしょうか?    

Streamlit の操作は簡単です。まず、いくつかの `streamlit` コマンドを通常の Python スクリプトに追加し、次に `streamlit run` で実行します。

    streamlit your_script.py run [-- script args]

上記のようにスクリプトを実行するとすぐに、ローカル Streamlit サーバーが起動し、アプリがデフォルトの Web ブラウザの新しいタブで開きます。
アプリはキャンバスであり、グラフ、テキスト、ウィジェット、表などを描画します。

アプリに何を描くかはあなた次第です。たとえば、`st.text` は生のテキストをアプリに書き込み、`st.line_chart` は、ご想像のとおり、折れ線グラフを描画します。
使用可能なすべてのコマンドについては、API ドキュメントを参照してください。

> [!Note]
> スクリプトにカスタム引数を渡すときは、2 つのダッシュの後に渡す必要があります。それ以外の場合、引数は Streamlit 自体への引数として解釈されます。

Streamlit を実行するもう 1 つの方法は、Python モジュールとして実行することです。
これは、Streamlit で動作するように PyCharm などの IDE を構成するときに役立ちます。

    # 下のコマンドと同じ
    python -m streamlit run your_script.py
    
    # 上のコマンドと同じ
    streamlit run your_script.py

### 開発の流れ
ソースファイが保存されるたびに、アプリを更新します。
Streamlit は変更があったかどうかを検出し、アプリを再実行するかどうかを尋ねます。
画面右上の [常に再実行] を選択すると、ソース コードを変更するたびにアプリが自動的に更新されます。

これにより、高速な対話型ループで作業できるようになります。
コードを入力して保存し、ライブで試してから、満足のいく結果が得られるまで、さらにコードを入力して保存し、試してみることを繰り返します。
コーディングと結果のライブ表示の間のこの緊密なループは、Streamlit が作業を容易にする1つの手段です。

> [!Note]
> Streamlit アプリを開発するときは、コードとアプリを同時に表示できるように、エディターとブラウザーのウィンドウを並べてレイアウトすることをお勧めします。試してみてください!

### データの流れ
Streamlit のアーキテクチャを使用すると、プレーンな Python スクリプトを作成するのと同じ方法でアプリを作成できます。
これを解決するために、Streamlit アプリには独自のデータフローがあります。
画面上で何かを更新する必要があるときは常に、Streamlit が Python スクリプト全体を上から下まで再実行します。

これは次の 2 つの状況で発生する可能性があります。

+ アプリのソースコードを変更するとき。
+ ユーザーがアプリ内のウィジェットを操作するとき。たとえば、スライダーをドラッグするとき、入力ボックスにテキストを入力するとき、またはボタンをクリックするときです。

### データの表示とスタイル設定
Streamlit アプリでデータ (テーブル、配列、データ フレーム) を表示するには、いくつかの方法があります。    
以下では、テキストからテーブルまであらゆるものを書き込むために使用できるマジックコマンドと `st.write()` の２つを紹介します。    
その後、データを視覚化するために特別に設計されたメソッドを見てみましょう。

#### マジックコマンドを使う
はじめに、Streamlit メソッドを呼び出さずに表示を行う方法「マジックコマンド」を説明します。
通常は後述する `st.write()` を使用して画面表示を行いますが、マジックコマンドは `st.write()` をまったく使用する必要がありません。
これを実際に確認するには、次のスニペットを試してください。

````py
import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df
````

Streamlit が独自の行に変数またはリテラル値を見つけるたびに、st.write() を使用してそれをアプリに自動的に書き込みます。
詳細については、マジックコマンドに関するドキュメントを読んでみてください。

#### データフレームを書き込む
魔法のコマンドと同様に、`st.write()` は Streamlit の万能コマンド（Swiss Army knife：スイスのアーミーナイフのように）です。
テキスト、データ、Matplotlib の図、Altair チャートなど、ほとんどすべてのものを `st.write()` に渡すことができます。心配しないでください。Streamlit はそれが何であるかを理解し、正しい方法でレンダリングします。

````py
import streamlit as st
import pandas as pd

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
````

`st.write()` とは別に、データの表示に使用できる `st.dataframe()` や `st.table()` などのデータ固有の関数もあります。
これらの機能をいつ使用するのか、また色やスタイルを追加する方法を理解しましょう。

「なぜ常に st.write() を使用しないのですか?」と自問しているかもしれません。理由はいくつかあります。

+ マジックコマンドと `st.write()` は、渡されたデータのタイプを検査し、アプリ内でそれを最適にレンダリングする方法を決定します。別の方法で描きたい場合もあります。たとえば、データフレームを対話型テーブルとして描画する代わりに、`st.table(df)` を使用して静的テーブルとして描画したい場合があります。
+ 2番目の理由は、他のメソッドが、データを追加するか置き換えることによって使用および変更できるオブジェクトを返すためです。
+ 最後に、より具体的な Streamlit メソッドを使用する場合は、追加の引数を渡してその動作をカスタマイズできます。

たとえば、データ フレームを作成し、Pandas Styler オブジェクトを使用してその書式設定を変更してみましょう。
この例では、Numpy を使用してランダム サンプルを生成し、`st.dataframe()` メソッドを使用して対話型テーブルを描画します。

````py
import streamlit as st
import numpy as np

df = np.random.randn(10, 20)
st.dataframe(df)
````

Pandas Styler オブジェクトを使用して、対話型テーブル内のいくつかの要素を強調表示する最初の例を拡張してみましょう。
列の中で最も大きな数値がハイライトされるのが確認できたでしょう。

````py
import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
````

Streamlit には、静的テーブルを生成するためのメソッド `st.table()` もあります。

````py
import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)
````

#### チャートや地図を描く
Streamlit は、Matplotlib、Altair、deck.gl などのいくつかの一般的なデータグラフ作成ライブラリをサポートしています。
このセクションでは、棒グラフ、折れ線グラフ、地図をアプリに追加します。

`st.line_chart()` を使用すると、アプリに折れ線グラフを簡単に追加できます。
Numpy を使用してランダムなサンプルを生成し、グラフ化します。

```py
import streamlit as st
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)
```

`st.map()` を使用すると、地図上にデータ ポイントを表示できます。
Numpy を使用してサンプル データを生成し、サンフランシスコの地図上にプロットしてみましょう。

```py
import streamlit as st
import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)
```

### ウィジェット

データまたはモデルを調査したい状態にしたら、st.slider()、st.button()、st.selectbox() などのウィジェットを追加できます。
これは非常に簡単です。ウィジェットを変数として扱います。

```py
import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)
```

最初の実行時に、上記のアプリは「0 の 2 乗は 0」というテキストを出力するはずです。
その後、ユーザーがウィジェットを操作するたびに、Streamlit はスクリプトを上から下に再実行し、ウィジェットの現在の状態をプロセス内の変数に割り当てます。

たとえば、ユーザーがスライダーを 10 の位置に移動すると、Streamlit は上記のコードを再実行し、それに応じて x を 10 に設定します。
これで、「10 の 2 乗は 100」というテキストが表示されるはずです。

ウィジェットの一意のキーとして使用する文字列を指定する場合は、キーによってウィジェットにアクセスすることもできます。

```py
import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name
```

キーを持つすべてのウィジェットは、セッション状態に自動的に追加されます。
セッション状態、ウィジェット状態との関連付けの詳細については、[API リファレンスガイド](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)を参照してください。

#### チェックボックスを使用してデータを表示/非表示にします
チェックボックスの使用例の 1 つは、アプリ内の特定のグラフまたはセクションを非表示または表示することです。
`st.checkbox()` は、ウィジェットのラベルを 1 つの引数として受け取ります。
このサンプルでは、​​チェックボックスを使用して条件文を切り替えます。

```py
import streamlit as st
import numpy as np
import pandas as pd

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data
```

#### オプションのセレクトボックスを使用する

シリーズから選択するには `st.selectbox` を使用します。必要なオプションを書き込むことも、配列またはデータ フレーム列を渡すこともできます。   
先ほど作成した df データ フレームを使用してみましょう。

```py
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option
```

### レイアウト
Streamlit を使用すると、`st.sidebar` を使用して左側のパネルのサイドバーでウィジェットを簡単に整理できます。
`st.sidebar` に渡される各要素は左側に固定されるため、ユーザーは UI コントロールにアクセスしながらアプリ内のコンテンツに集中できます。

たとえば、セレクトボックスとスライダーをサイドバーに追加する場合は、`st.slider` と `st.selectbox` の代わりに `st.sidebar.slider` と `st.sidebar.selectbox` を使用します。

```py
import streamlit as st

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
```

サイドバー以外にも、Streamlit はアプリのレイアウトを制御する他の方法をいくつか提供します。
`st.columns` を使用するとウィジェットを並べて配置でき、`st.expander` を使用すると大きなコンテンツを隠してスペースを節約できます。

```py
import streamlit as st

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")
```

#### 進行状況を表示する
長時間実行される計算をアプリに追加する場合、`st.progress()` を使用してステータスをリアルタイムで表示できます。    
`time.sleep()` メソッドを使用して、長時間実行される計算をシミュレートし、進行状況バーを作成します。

```py
import streamlit as st
import time

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'
```



## 先進的なコンセプト
Streamlit の再実行ロジックを理解したら、キャッシュとセッション状態を使用して効率的で動的なアプリを作成する方法を学びます。
データベース接続の処理について説明します。

## 追加機能
Streamlit の追加機能について学びます。初めてのアプリでこれらの概念を知る必要はありませんが、何が利用できるのかを確認するためにチェックしてください。

