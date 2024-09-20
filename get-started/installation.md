https://docs.streamlit.io/get-started/installation

# インストール

開発環境をセットアップして Streamlit をインストールするには複数の方法があります。  
最も一般的な方法は自分のコンピューターにインストールされた Python を使用してローカルで開発することです。    
Linux や Python に馴染みのある方は次のコマンドですぐにインストールできるでしょう。

    pip install streamlit
    streamlit hello

ここからは、`venv` を使用した環境の作成と `pip` を使用した Streamlit のインストールについて説明します。  
エキスパートの方は読み飛ばしてください。より詳しい情報が必要な方だけ読み進めてください。

`venv` と `pip` は推奨ツールですが、他のツールに精通している場合は、お気に入りのツールを使用することもできます。
Python 環境をの構築に GUI を使用したい場合は、Anaconda を使用してください。
詳しくは https://docs.streamlit.io/get-started/installation/anaconda-distribution を確認してください。

## 事前準備

Streamlit をインストールするには、まずコンピューターが適切にセットアップされていることを確認する必要があります。
より具体的には、次のものが必要になります。

### Python  
バージョン 3.8 ～ 3.12 をサポートします。

### Python 環境マネージャー (推奨)
環境マネージャーは、プロジェクト間で Python パッケージのインストールを分離するための仮想環境を作成します。  
Python パッケージをインストールまたはアップグレードすると、別のパッケージに意図しない影響が生じる可能性があるため、仮想環境を使用することをお勧めします。
Python 環境の詳細については、「[Python 仮想環境: 入門](https://realpython.com/python-virtual-environments-a-primer/)」を参照してください。
このガイドでは、Python に付属する `venv` を使用します。

### Python パッケージマネージャー
パッケージ マネージャーは、Streamlit を含む各 Python パッケージのインストールを処理します。  
このガイドでは、Python に付属の `pip` を使用します。

### コードエディタ
おすすめののエディターは VS Code であり、すべてのチュートリアルでもこれを使用しています。


## venv を使用して環境を作成する

ターミナルを開き、プロジェクト フォルダーに移動します。

    cd myproject

ターミナルで次のように入力します。

    python -m venv .venv

**".venv"** という名前のフォルダーがプロジェクトに表示されます。このディレクトリは、仮想環境とその依存関係がインストールされる場所です。

### 環境をアクティブ化する

ターミナルで、オペレーティング システムに応じて次のコマンドのいずれかを使用して環境をアクティブ化します。

    # Linux
    source .venv/bin/activate
    
    # Windows コマンドプロンプト
    .venv\Scripts\activate.bat

    # Windows PowerShell
    .venv\Scripts\Activate.ps1

アクティブ化すると、次の例のようにプロンプトの前に環境名 **"(.venv)"** が括弧内に表示されます。

   (.venv) yourname@local ~ $
