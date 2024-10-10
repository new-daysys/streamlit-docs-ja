---
title: Run your Streamlit app
slug: /develop/concepts/architecture/run-your-app
---

# Streamlitアプリを実行する

Streamlitを使うのは簡単です。まず通常のPythonスクリプトにいくつかのStreamlitコマンドを追加し、それを実行します。利用ケースに応じたスクリプトの実行方法をいくつか紹介します。

## `streamlit run` を使用する

スクリプトを作成したら、例えば `your_script.py` という名前のスクリプトを以下のように実行するのが最も簡単です：

```bash
streamlit run your_script.py
```

上記のようにスクリプトを実行すると、ローカルのStreamlitサーバーが起動し、デフォルトのウェブブラウザの新しいタブでアプリが開きます。

### スクリプトに引数を渡す

スクリプトにカスタム引数を渡す場合、2つのダッシュの後に引数を指定する必要があります。それ以外の場合、引数は Streamlit 自体への引数として解釈されます：

```bash
streamlit run your_script.py [-- script args]
```

### `streamlit run` にURLを渡す

`streamlit run` にURLを渡すことも可能です！これは、GitHub Gist などでリモートにホストされたスクリプトを実行する場合に便利です。例えば：

```bash
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
```

## PythonモジュールとしてStreamlitを実行する

もう一つの方法として、Streamlit を Python モジュールとして実行することができます。これは、PyCharm などの IDE で Streamlit を設定する際に便利です：

```bash
# 実行
python -m streamlit run your_script.py
```

```bash
# 上記と同じです：
streamlit run your_script.py
```
