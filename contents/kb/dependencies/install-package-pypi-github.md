---
title: How to install a package not on PyPI/Conda but available on GitHub
slug: /knowledge-base/dependencies/install-package-not-pypi-conda-available-github
---

# PyPI/Conda にはないが GitHub で利用可能なパッケージをインストールする方法

## 概要

[Streamlit Community Cloud](/deploy/streamlit-community-cloud) にアプリをデプロイしようとしていて、requirements ファイルに [Python依存関係](/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies#add-python-dependencies) を指定したいが、PyPI や Conda のようなパッケージインデックスにはないパブリックな GitHub リポジトリにしかない場合、どうすればよいかわからない場合は、この方法をお読みください！

例えば、`SomePackage` をG itHub からインストールしたいとします。Git は人気のあるバージョン管理システム（VCS）で、GitHub はそのホスティングサービスです。`SomePackage` が次の URL にあるとします：`https://github.com/SomePackage.git`。

pip（`requirements.txt`経由）では、GitHub からのインストールを [サポート](https://pip.pypa.io/en/stable/topics/vcs-support/) しています。このサポートには、実行可能な Git が必要です。`git+` というURLプレフィックスを使用してインストールします。

## GitHub のウェブ URL を指定

`SomePackage` をインストールするには、`requirements.txt` ファイルに以下を含めます：

```bash
git+https://github.com/SomePackage#egg=SomePackage
```

以下の例のように、ブランチ名、コミットハッシュ、またはタグ名を指定することもできます。

## Gitブランチ名を指定

`SomePackage` をブランチ名（`main`、`master`、`develop` など）を指定してインストールするには、`requirements.txt` に以下を記述します：

```bash
git+https://github.com/SomePackage.git@main#egg=SomePackage
```

## コミットハッシュを指定

`SomePackage` をコミットハッシュを指定してインストールするには、`requirements.txt` に以下を記述します：

```bash
git+https://github.com/SomePackage.git@eb40b4ff6f7c5c1e4366cgfg0671291bge918#egg=SomePackage
```

## タグを指定

`SomePackage` をタグを指定してインストールするには、`requirements.txt` に以下を記述します：

```bash
git+https://github.com/SomePackage.git@v1.1.0#egg=SomePackage
```

## 制限事項

現在、プライベートなGitHubリポジトリからプライベートパッケージをURI形式でインストールすることは **できません**：

```bash
git+https://{token}@github.com/user/project.git@{version}
```

ここで、`version` はタグ、ブランチ、またはコミットで、`token` は読み取り専用の権限を持つ個人アクセストークンです。Streamlit Community Cloud では、パブリックなGitHubリポジトリからのパブリックパッケージのインストールのみがサポートされています。
