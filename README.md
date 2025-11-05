# Three-Tier Architecture Beginner

OCI（Oracle Cloud Infrastructure）で3層アーキテクチャを構築するためのサンプルアプリケーションです。

## 概要

このリポジトリは、OCIでの3層アーキテクチャ構築を学習するためのサンプルプロジェクトです。
Webブラウザから操作できるTODO管理アプリケーションを題材に、以下を学ぶことができます：

- VCN（Virtual Cloud Network）の構築
- Computeインスタンスの作成と設定
- MySQL HeatWaveの構築
- Flexible Load Balancerの設定
- nginxとGunicornを使ったアプリケーションのデプロイ

## 関連記事

詳細な構築手順は以下のQiita記事を参照してください：

- [Qiita: OCIで3層アーキテクチャを構築する](https://qiita.com/yama6/items/43ad3ea82781646a4144)

## リポジトリ構成

```
.
├── README.md              # このファイル
├── commands.md            # 構築手順で使用するコマンド集
├── config/               # 設定ファイル
│   ├── todoapp.service   # Gunicorn用systemdサービスファイル
│   └── todoapp.conf      # nginx設定ファイル
├── opt/                  # バックエンドアプリケーション
│   └── backend/
│       ├── app.py        # Flaskアプリケーション
│       ├── db.py         # データベース接続
│       ├── requirements.txt  # Python依存パッケージ
│       └── wsgi.py       # WSGIエントリーポイント
└── home/                 # フロントエンドアプリケーション
    └── opc/
        └── frontend/
            └── frontend/
                └── src/
                    └── App.js  # Vue.jsアプリケーション
```

## 技術スタック

- **フロントエンド**: Vue.js
- **バックエンド**: Python / Flask
- **WSGIサーバー**: Gunicorn
- **リバースプロキシ**: nginx
- **インフラ**: OCI (Oracle Cloud Infrastructure)
- **データベース**: MySQL HeatWave

## 前提条件

- OCIアカウント
- 基本的なLinuxコマンド操作の知識
- Python、MySQL、nginxの基本的な知識


詳細な構築手順は以下のファイルを参照してください：

- **コマンド集**: `commands.md` - 構築時に実行するコマンドをまとめたファイル
- **設定ファイル**: `config/` ディレクトリ内のファイルをサーバーにコピーして使用


