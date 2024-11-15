---
title: Managing dependencies when deploying your app
slug: /deploy/concepts/dependencies
---

# アプリデプロイ時の依存関係の管理

アプリ開ブを始める前に、Python や Streamlit をインストールして開発環境を設定したかと思います。アプリをデプロイする際も、同様にデプロイ環境を設定する必要があります。アプリをクラウドサービスにデプロイする場合、アプリの `Python サーバー` はリモートマシン上で動作します。このリモートマシンは、個人のコンピュータにあるすべてのファイルやプログラムにアクセスできません。

すべての Streamlit アプリには少なくとも 2 つの依存関係があります：Python と Streamlit。さらに、Python パッケージやスクリプトの実行に必要なソフトウェアが追加の依存関係になる場合もあります。Streamlit アプリ用に設計された Streamlit Community Cloud のようなサービスを利用する場合、Python と Streamlit のインストールはお任せください！

## Python とその他のソフトウェアのインストール

Streamlit Community Cloud を利用している場合、Python はすでにインストールされています。デプロイ時のダイアログでバージョンを選択するだけです。もし Python を自分でインストールする必要がある場合や、Python 以外のソフトウェアをインストールする必要がある場合は、プラットフォームの指示に従って追加のソフトウェアをインストールしてください。一般的には、パッケージ管理ツールを使用します。例えば、Streamlit Community Cloud では Debian ベースの Linux システム用に Advanced Package Tool（`apt`）を使用します。Streamlit Community Cloud での非 Python 依存関係のインストールについては、[`apt-get` 依存関係](/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies#apt-get-dependencies) をご覧ください。

## Python パッケージのインストール

デプロイ環境に Python をインストールしたら、必要な Python パッケージをすべてインストールする必要があります。これには Streamlit も含まれます。スクリプトでインストール済みパッケージを `import` するたびに、Python の依存関係が追加されます。それらの依存関係をデプロイ環境で Python パッケージマネージャーを使用してインストールしてください。

Streamlit Community Cloud を利用している場合、最新バージョンの Streamlit とそのすべての依存関係がデフォルトでインストールされます。そのため、追加の依存関係が必要でないシンプルなアプリを作成している場合、何もする必要はありません！

### `pip` と `requirements.txt`

Python にはデフォルトで `pip` が含まれているため、Python 環境を構成する最も一般的な方法は `requirements.txt` ファイルを使用することです。`requirements.txt` ファイルの各行には、`pip install` するパッケージを記述します。<a href="https://docs.python.org/3/py-modindex.html" target="_blank">Python 標準ライブラリ</a>（例：`math` や `random`）を `requirements.txt` に含める必要はありません。これらは Python に組み込まれており、別途インストールする必要はありません。

以下のようなスクリプトがある場合、必要なのは Streamlit のインストールだけです。`pandas` や `numpy` は `streamlit` の直接の依存関係としてインストールされ、`math` や `random` は Python に組み込まれています。

```python
import streamlit as st
import pandas as pd
import numpy as np
import math
import random

st.write('Hi!')
```

ただし、使用したパッケージを正確に記録するのがベストプラクティスであるため、推奨される `requirements.txt` ファイルは次のようになります：

```none
streamlit
pandas
numpy
```

特定のバージョンを指定する必要がある場合は、次のように記述することもできます：

```none
streamlit==1.24.1
pandas>2.0
numpy<=1.25.1
```

`requirements.txt` ファイルは通常、リポジトリやファイルディレクトリのルートに保存されます。Streamlit Community Cloud を利用している場合は、[Python 依存関係の追加](/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies#add-python-dependencies) をご覧ください。それ以外の場合は、プラットフォームのドキュメントを確認してください。
