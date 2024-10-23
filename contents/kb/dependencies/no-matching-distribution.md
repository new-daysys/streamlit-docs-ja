---
title: ERROR No matching distribution found for
slug: /knowledge-base/dependencies/no-matching-distribution
---

# ERROR: No matching distribution found for

## 問題

[Streamlit Community Cloud](https://streamlit.io/cloud) にアプリをデプロイすると、`ERROR: No matching distribution found for` というエラーが発生します。

## 解決策

このエラーは、Streamlit Community Cloud にアプリをデプロイした際、requirementsファイルの [Python依存関係](/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies#add-python-dependencies) に次のいずれかの問題がある場合に発生します：

1. パッケージが [Python標準ライブラリ](https://docs.python.org/3/py-modindex.html) の一部である。例えば、requirementsファイルに [`base64`](https://docs.python.org/3/library/base64.html) を含めると、 **`ERROR: No matching distribution found for base64`** が表示されます。これは `base64` がPython標準ライブラリの一部であるためです。解決策は、requirementsファイルにパッケージを含めないことです。標準のPythonインストールに含まれていないパッケージのみをrequirementsファイルに含めてください。
2. requirementsファイル内のパッケージ名がスペルミスである。パッケージ名をrequirementsファイルに含める前に、綴りが正しいことを確認してください。
3. パッケージが、Streamlitアプリが実行されているオペレーティングシステムをサポートしていない。例えば、`pywin32` を含めた状態で Streamlit Community Cloud にデプロイすると、**`ERROR: No matching distribution found for pywin32`** というエラーが表示されます。`pywin32` モジュールは、Pythonから多くのWindows APIにアクセスするためのものですが、Streamlit Community Cloud上ではLinux環境でアプリが実行されるため、非Windowsシステム上では `pywin32` のインストールに失敗します。解決策は、requirementsファイルから `pywin32` を除外するか、Windowsマシンを提供するクラウドサービスにアプリをデプロイすることです。

関連フォーラム投稿:

- https://discuss.streamlit.io/t/error-no-matching-distribution-found-for-base64/15758
- https://discuss.streamlit.io/t/error-could-not-find-a-version-that-satisfies-the-requirement-pywin32-301-from-versions-none/15343/2
