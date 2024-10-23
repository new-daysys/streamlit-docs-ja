---
title: ImportError libGL.so.1 cannot open shared object file No such file or directory
slug: /knowledge-base/dependencies/libgl
---

# ImportError libGL.so.1 cannot open shared object file No such file or directory

## 問題

[Streamlit Community Cloud](https://streamlit.io/cloud) にデプロイしたアプリでOpenCVを使用すると、`ImportError libGL.so.1 cannot open shared object file No such file or directory` というエラーが発生します。

## 解決策

アプリでOpenCVを使用している場合、Streamlit Community Cloud上のrequirementsファイルに `opencv_contrib_python` や `opencv-python` の代わりに `opencv-python-headless` を含めてください。

もし、`opencv-python` がアプリにとって **必須の依存関係**（オプションではない）である場合、またはアプリ内で使用しているライブラリの依存関係である場合、上記の解決策は適用できません。この場合は、次の方法を使用してください：

リポジトリに `packages.txt` ファイルを作成し、次の行を追加して [apt-get 依存関係](/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies#apt-get-dependencies) `libgl` をインストールします：

```
libgl1
```
