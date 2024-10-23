---
title: ModuleNotFoundError No module named
slug: /knowledge-base/dependencies/module-not-found-error
---

# ModuleNotFoundError: No module named

## 問題

[Streamlit Community Cloud](https://streamlit.io/cloud) でアプリをデプロイすると、`ModuleNotFoundError: No module named` というエラーが発生します。

## 解決策

このエラーは、Streamlit Community Cloud 上でモジュールをインポートする際に、そのモジュールがrequirementsファイルに含まれていない場合に発生します。[Python依存関係](/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies#add-python-dependencies)で標準のPythonインストールに含まれていない外部モジュールは、必ずrequirementsファイルに含める必要があります。

例：`scikit-learn` をrequirementsファイルに含めずにアプリ内で `import sklearn` としている場合、`ModuleNotFoundError: No module named 'sklearn'` というエラーが表示されます。

関連フォーラム投稿:

- https://discuss.streamlit.io/t/getting-error-modulenotfounderror-no-module-named-beautifulsoup/9126
- https://discuss.streamlit.io/t/modulenotfounderror-no-module-named-vega-datasets/16354
