---
title: Managing secrets when deploying your app
slug: /deploy/concepts/secrets
---

# アプリデプロイ時のシークレット管理

データソースや外部サービスに接続する場合、資格情報やキーのようなシークレット情報を扱うことが一般的です。シークレット情報は、安全に保存および送信する必要があります。アプリをデプロイする際には、プラットフォームが提供する機能やシークレットを扱うための仕組みを理解し、ベストプラクティスに従うようにしてください。

シークレットを直接コードに保存することは避け、`.gitignore` を更新して、ローカルのシークレットを誤ってリポジトリにコミットしないようにしてください。便利なリマインダーについては、[セキュリティのリマインダー](/develop/concepts/connections/security-reminders) を参照してください。

Streamlit Community Cloud を使用している場合、[シークレット管理](/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) を活用することで、環境変数を保存し、コード外でシークレットを管理することができます。Streamlit 用に設計された他のプラットフォームを使用している場合、それらがシークレットを扱うための組み込み機能を提供しているか確認してください。場合によっては、`st.secrets` をサポートしたり、`secrets.toml` ファイルを安全にアップロードする機能を備えていることもあります。

環境変数を使用して `st.connection` を活用する方法については、[グローバルシークレット、複数のアプリおよびデータストアの管理](/develop/concepts/connections/connecting-to-data#global-secrets-managing-multiple-apps-and-multiple-data-stores) をご覧ください。
