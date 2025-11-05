# 3層アーキテクチャ構築手順 - コマンド集

本書「03-three-tier-arai.re」で使用するコマンドをまとめたファイルです。
各セクションに対応するコマンドを順番に実行してください。

## 使用方法

1. このファイルを適切なサーバーにコピー
2. 必要な値を置き換える（`<xxx>`の部分）
3. 各セクションごとに実行

---

## セクション: 開発用Computeサーバの作成（オプション）

### 開発サーバへのSSH接続

書籍: `=== 開発用Computeサーバの作成（オプション） > ==== ■2. 必要なツールのインストール`

```bash
ssh -i ~/.ssh/<秘密キー名> opc@<開発用ComputeのパブリックIP>
```

### 必要ツールのインストール

書籍: `=== 開発用Computeサーバの作成（オプション） > ==== ■2. 必要なツールのインストール`

```bash
sudo dnf update -y
sudo dnf install mysql -y
mysql --version
```

---

## セクション: アプリケーション用Computeの構築

### アプリサーバへのSSH接続（開発サーバ経由）

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ`

```bash
# 開発サーバにSSH接続
ssh -i <秘密キー名> opc@<開発用ComputeのパブリックIP>

# アプリサーバへSSH接続（プライベートIP）
ssh -i <秘密キー名> opc@<アプリサーバのプライベートIP>
```

### 必要パッケージのインストール

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・1. 必要パッケージのインストール`

```bash
sudo dnf update -y
sudo dnf install python3.11 python3.11-pip -y
sudo dnf install nginx -y
sudo dnf install mysql -y
sudo dnf install git -y

# Node.jsとnpmのインストール（フロントエンド構築用）
# 利用可能なNode.jsモジュールを確認
sudo dnf module list nodejs

# Node.js 20モジュールを有効化
sudo dnf module enable -y nodejs:20

# Node.jsとnpmをインストール
sudo dnf install -y nodejs npm

# インストール確認
python3.11 --version
python3.11 -m pip --version
nginx -v
mysql --version
git --version
node --version
npm --version
```

### バックエンドの構築

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・2. バックエンドの構築`

#### アプリケーション用ディレクトリの作成とリポジトリのクローン

書籍: `===== ・2-1. アプリケーション用ディレクトリの作成とリポジトリのクローン`

設定ファイル（Gunicornとnginx）を取得するため、GitHubリポジトリをクローンします。

```bash
# アプリケーション用ディレクトリの作成
sudo mkdir -p /opt/todoapp
sudo chown opc:opc /opt/todoapp
cd /opt/todoapp

# GitHubからリポジトリをクローン（設定ファイルを取得するため）
git clone https://github.com/yamadas1213/three-tier-architecture-beginner.git temp-config
```

#### バックエンドディレクトリの作成

書籍: `===== ・2-2. バックエンドディレクトリの作成`

```bash
# バックエンドディレクトリの作成
mkdir -p backend
cd backend
```

#### Python仮想環境と依存パッケージ

書籍: `===== ・2-3. Python仮想環境の作成と依存パッケージのインストール`

```bash
# 仮想環境の作成
python3.11 -m venv venv
source venv/bin/activate

# 必要なパッケージのインストール
pip install flask gunicorn mysql-connector-python
```

#### バックエンドアプリケーションファイルのコピー

書籍: `===== ・2-4. バックエンドアプリケーションファイルのコピー`

```bash
# リポジトリからバックエンドファイルをコピー
cp /opt/todoapp/temp-config/opt/backend/app.py /opt/todoapp/backend/
cp /opt/todoapp/temp-config/opt/backend/db.py /opt/todoapp/backend/
cp /opt/todoapp/temp-config/opt/backend/wsgi.py /opt/todoapp/backend/
```

### フロントエンドの構築

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・3. フロントエンドの構築`

#### Viteプロジェクトの作成

書籍: `===== ・3-1. Viteプロジェクトの作成`

```bash
# /opt/todoappディレクトリに移動
cd /opt/todoapp

# Viteを使ってVue.jsプロジェクトを作成
npm create vite@latest frontend -- --template vue

# プロジェクト作成時に以下の質問が出た場合の回答：
# - 「Use rolldown-vite (Experimental)?」→ 「No」を選択（デフォルトで選択されているためEnterキーでOK）
# - 「Install with npm and start now?」→ 「No」を選択（手動でnpm installを実行するため）

# プロジェクトディレクトリに移動
cd frontend

# 依存パッケージのインストール
npm install
```

#### Vue.jsアプリケーションの実装

書籍: `===== ・3-2. Vue.jsアプリケーションの実装`

```bash
# リポジトリからApp.vueをコピー
cp /opt/todoapp/temp-config/opt/frontend/src/App.vue /opt/todoapp/frontend/src/App.vue
```

#### フロントエンドのビルド

書籍: `===== ・3-3. フロントエンドのビルド`

```bash
# プロダクションビルドの実行
npm run build

# ビルド結果の確認（distディレクトリが作成される）
ls -la dist/
```

### Gunicornの設定

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・4. Gunicornの設定`

```bash
# リポジトリからクローンしたサービスファイルをsystemdディレクトリにコピー
sudo cp /opt/todoapp/temp-config/config/todoapp.service /etc/systemd/system/todoapp.service

# 環境変数を実際のMySQL HeatWaveの設定に合わせて編集
# エディタで直接編集します
sudo vi /etc/systemd/system/todoapp.service
# <mysql-private-ip>を実際のMySQLプライベートIPに置き換える
# <mysql-password>を実際のMySQLパスワードに置き換える

# systemdの設定を再読み込み
sudo systemctl daemon-reload

# サービスの起動と自動起動設定
sudo systemctl start todoapp
sudo systemctl enable todoapp

# サービスが正常に起動しているか確認
sudo systemctl status todoapp
```

**注意**: `todoapp.service`ファイル内の`<mysql-private-ip>`と`<mysql-password>`を実際の値に置き換えてください。

### nginxの設定

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・5. nginxの設定`

```bash
# リポジトリからクローンしたnginx設定ファイルをコピー
sudo cp /opt/todoapp/temp-config/config/todoapp.conf /etc/nginx/conf.d/todoapp.conf

# デフォルト設定の無効化
sudo rm -f /etc/nginx/conf.d/default.conf

# nginxの設定を確認してから起動
sudo nginx -t

# nginxの起動と自動起動設定
sudo systemctl start nginx
sudo systemctl enable nginx
```

### ファイアウォール設定（firewalld）

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・6. ファイアウォール設定（firewalld）`

```bash
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-services
```

### SELinuxの設定

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・7. SELinuxの設定`

```bash
sudo setsebool -P httpd_can_network_connect on
```

---

## セクション: MySQL HeatWaveの構築

### MySQLへの接続

書籍: `=== MySQL HeatWaveの構築 > ==== ■2. データベースとテーブルの作成 > ===== ・1. MySQLへの接続`

```bash
# <mysql-private-ip>: MySQL HeatWaveのプライベートIPアドレス
mysql -h <mysql-private-ip> -u admin -p
# パスワード入力プロンプトで、設定したパスワードを入力
```

### データベースとテーブルの作成

書籍: `=== MySQL HeatWaveの構築 > ==== ■2. データベースとテーブルの作成 > ===== ・2. データベースとテーブルの作成`

```sql
-- データベースの作成
CREATE DATABASE tododb;

-- データベースの選択
USE tododb;

-- テーブルの作成
CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 動作確認用のデータ挿入（オプション）
INSERT INTO todos (title, done) VALUES 
('OCIを学ぶ', 0),
('3層アーキテクチャを構築する', 0),
('TODO管理アプリを完成させる', 0);

-- データの確認
SELECT * FROM todos;

-- MySQLから切断
EXIT;
```

---

## セクション: 動作確認

### ブラウザでのアクセス

書籍: `=== 動作確認 > ==== ■1. Webブラウザからの確認 > ===== ・1. HTMLページへのアクセス`

Webブラウザから以下のURLにアクセス:
```
http://<flb-public-ip>/
```

### MySQLでデータ確認

書籍: `=== 動作確認 > ==== ■2. データベースでの確認`

```bash
mysql -h <mysql-private-ip> -u admin -p
```

```sql
USE tododb;
SELECT * FROM todos;
```

結果例：
```
+----+--------------+------+---------------------+
| id | title        | done | created_at          |
+----+--------------+------+---------------------+
|  1 | 犬の散歩     |    0 | 2025-08-17 10:30:45 |
+----+--------------+------+---------------------+
```

