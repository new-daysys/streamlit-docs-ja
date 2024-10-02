---
title: Using forms
slug: /develop/concepts/architecture/forms
---

# フォームの使用

ユーザーが入力するたびにスクリプトを再実行したくない場合は、[`st.form`](/develop/api-reference/execution-flow/st.form) が役立ちます！
フォームを使えば、ユーザー入力を一度にまとめて再実行することが簡単になります。
このフォームの使用ガイドでは、具体例を示し、ユーザーがフォームとどのようにやり取りするかを説明しています。

## 例

次の例では、ユーザーが複数のパラメータを設定して地図を更新できます。ユーザーがパラメータを変更しても、スクリプトは再実行されず、地図も更新されません。
ユーザーが「**Update map**」とラベル付けされたボタンでフォームを送信すると、スクリプトが再実行され、地図が更新されます。

ユーザーがいつでもフォームの外にある「**Generate new points**」をクリックすると、スクリプトが再実行されます。
この時、フォーム内で未送信の変更は**送信されません**。
フォームに加えたすべての変更は、フォーム自体が送信されたときにのみ Python のバックエンドに送られます。

```python
import streamlit as st
import pandas as pd
import numpy as np

def get_data():
    df = pd.DataFrame({
        "lat": np.random.randn(200) / 50 + 37.76,
        "lon": np.random.randn(200) / 50 + -122.4,
        "team": ['A','B']*100
    })
    return df

if st.button('Generate new points'):
    st.session_state.df = get_data()
if 'df' not in st.session_state:
    st.session_state.df = get_data()
df = st.session_state.df

with st.form("my_form"):
    header = st.columns([1,2,2])
    header[0].subheader('Color')
    header[1].subheader('Opacity')
    header[2].subheader('Size')

    row1 = st.columns([1,2,2])
    colorA = row1[0].color_picker('Team A', '#0000FF')
    opacityA = row1[1].slider('A opacity', 20, 100, 50, label_visibility='hidden')
    sizeA = row1[2].slider('A size', 50, 200, 100, step=10, label_visibility='hidden')

    row2 = st.columns([1,2,2])
    colorB = row2[0].color_picker('Team B', '#FF0000')
    opacityB = row2[1].slider('B opacity', 20, 100, 50, label_visibility='hidden')
    sizeB = row2[2].slider('B size', 50, 200, 100, step=10, label_visibility='hidden')

    st.form_submit_button('Update map')

alphaA = int(opacityA*255/100)
alphaB = int(opacityB*255/100)

df['color'] = np.where(df.team=='A',colorA+f'{alphaA:02x}',colorB+f'{alphaB:02x}')
df['size'] = np.where(df.team=='A',sizeA, sizeB)

st.map(df, size='size', color='color')
```

## ユーザーインタラクション

ウィジェットがフォーム外にある場合、そのウィジェットの値が変更されるたびにスクリプトが再実行されます。
キー入力を受け付けるウィジェット（`st.number_input`、`st.text_input`、`st.text_area`）では、
ユーザーがウィジェットからクリックやタブで外れたときに新しい値が再実行をトリガーします。
ユーザーがウィジェット内でカーソルをアクティブにしている場合、`Enter`キーを押して変更を送信することも可能です。

一方、ウィジェットがフォーム内にある場合、ユーザーがウィジェットからクリックやタブで外れてもスクリプトは再実行されません。
フォーム内のウィジェットでは、フォームが送信されたときにスクリプトが再実行され、フォーム内のすべてのウィジェットが更新された値を Python のバックエンドに送信します。

ユーザーは、カーソルがキー入力を受け付けるウィジェットにアクティブな状態であれば、キーボードの**Enter**キーを使ってフォームを送信できます。`st.number_input`や`st.text_input`では、**Enter**キーを押すことでフォームが送信されます。`st.text_area`内では、**Ctrl+Enter**（Windows）/**⌘+Enter**（Mac）を押してフォームを送信します。

## ウィジェットの値

フォームが送信される前は、フォーム内のすべてのウィジェットにはデフォルト値があります。
これは、フォーム外のウィジェットにデフォルト値があるのと同じです。

```python
import streamlit as st

with st.form("my_form"):
   st.write("フォーム内")
   my_number = st.slider('数値を選択', 1, 10)
   my_color = st.selectbox('色を選択', ['赤','オレンジ','緑','青','紫'])
   st.form_submit_button('選択を送信')

# これはフォーム外です
st.write(my_number)
st.write(my_color)
```

## フォームはコンテナ

`st.form` が呼び出されると、フロントエンドにコンテナが作成されます。
これは、他の[コンテナ要素](/develop/api-reference/layout)と同様に、そのコンテナに書き込むことができます。
つまり、上記の例のように Python の `with` 文を使用するか、フォームコンテナを変数に割り当てて、その変数上でメソッドを直接呼び出すことができます。
さらに、`st.form_submit_button` はフォームコンテナのどこにでも配置できます。

```python
import streamlit as st

animal = st.form('my_animal')

# これはメインボディに直接書き込まれます。フォームコンテナが
# 上で定義されているので、フォーム内に書かれたすべての下に表示されます。
sound = st.selectbox('Sounds like', ['meow','woof','squeak','tweet'])

# これらのメソッドはフォームコンテナに対して呼び出されるため、フォーム内に表示されます。
submit = animal.form_submit_button(f'{sound}で言う!')
sentence = animal.text_input('あなたの文:', 'Where\'s the tuna?')
say_it = sentence.rstrip('.,!?') + f', {sound}!'
if submit:
    animal.subheader(say_it)
else:
    animal.subheader('&nbsp;')
```

## フォーム送信の処理

フォームの目的は、ユーザーが変更を加えた瞬間にスクリプトを再実行するという Streamlit のデフォルトの動作を上書きすることです。
フォーム外のウィジェットでは、論理フローは次の通りです：

1. ユーザーがフロントエンドでウィジェットの値を変更します。
2. ウィジェットの値が `st.session_state` と Python のバックエンド（サーバー）で更新されます。
3. スクリプトの再実行が開始されます。
4. ウィジェットにコールバックがある場合、それがページの再実行の前に実行されます。
5. 再実行中にウィジェットの関数が実行されると、新しい値が出力されます。

フォーム内のウィジェットでは、ユーザーが行った変更（ステップ1）は、フォームが送信されるまで Python のバックエンド（ステップ2）に渡されません。さらに、フォーム内でコールバック関数を持つことができる唯一のウィジェットは `st.form_submit_button` です。新しく送信された値を使ってプロセスを実行する必要がある場合、主に3つのパターンでそれを実行できます。

### フォームの後にプロセスを実行する

フォーム送信の結果として1回だけ実行するプロセスが必要な場合、そのプロセスを `st.form_submit_button` に依存させて、フォームの後に実行できます。結果をフォームの上に表示する必要がある場合は、コンテナを使ってフォームの表示位置を制御できます。

```python
import streamlit as st

col1, col2 = st.columns([1, 2])
col1.title('Sum:')

with st.form('addition'):
    a = st.number_input('a')
    b = st.number_input('b')
    submit = st.form_submit_button('add')

if submit:
    col2.title(f'{a + b:.2f}')
```

### セッションステートとコールバックを使う

コールバックを使用して、スクリプトの再実行の前にプロセスを実行できます。

> [!Important]
> コールバック内で新しく更新された値を処理する場合、それらの値を直接 `args` または `kwargs` パラメータを介してコールバックに渡さないでください。
> コールバック内で使用するウィジェットの値には、キーを割り当てる必要があります。
> コールバックの中で `st.session_state` からそのウィジェットの値を取得することで、新しく送信された値にアクセスできます。以下の例を参照してください。

```python
import streamlit as st

if 'sum' not in st.session_state:
    st.session_state.sum = ''

def sum():
    result = st.session_state.a + st.session_state.b
    st.session_state.sum = result

col1, col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.sum, float):
    col2.title(f'{st.session_state.sum:.2f}')

with st.form('addition'):
    st.number_input('a', key='a')
    st.number_input('b', key='b')
    st.form_submit_button('add', on_click=sum)
```

### `st.rerun` を使う

プロセスがフォームの上のコンテンツに影響する場合、別の方法として追加の再実行を使用することもできます。ただし、これはリソース効率が悪くなる可能性があり、上記のオプションに比べて望ましくない場合があります。

```python
import streamlit as st

if 'sum' not in st.session_state:
    st.session_state.sum = ''

col1, col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.sum, float):
    col2.title(f'{st.session_state.sum:.2f}')

with st.form('addition'):
    a = st.number_input('a')
    b = st.number_input('b')
    submit = st.form_submit_button('add')

# st.session_state.sum の値はスクリプトの再実行の最後に更新されるため、
# col2の表示された値には新しい合計が表示されません。フォームが送信されたときに
# 再実行をトリガーして、上の値を更新します。
st.session_state.sum = a + b
if submit:
    st.rerun()
```

## 制限事項

- 各フォームには必ず `st.form_submit_button` が含まれていなければなりません。
- `st.button` と `st.download_button` はフォームに追加できません。
- `st.form` は、他の `st.form` の中に埋め込むことはできません。
- コールバック関数は、フォーム内では `st.form_submit_button` にのみ割り当てることができます。他のウィジェットにはコールバックを設定できません。
- フォーム内で相互に依存するウィジェットはあまり有用ではない可能性があります。`widget1` の値を `widget2` に渡す場合、両方ともフォーム内にあると `widget2` はフォームが送信されるまで更新されません。
