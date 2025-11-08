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

# 仮想環境を有効化
source venv/bin/activate

# 必要なパッケージのインストール
# flask: Webアプリケーションフレームワーク
# gunicorn: 本番環境向けWSGIサーバー
# mysql-connector-python: MySQLデータベース接続ライブラリ
pip install flask gunicorn mysql-connector-python

# インストール確認
pip list | grep -E "flask|gunicorn|mysql"

# 仮想環境を無効化（ファイルコピーなど通常のシェル操作では不要）
deactivate
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
# - Ok to proceed? (y) → y を入力
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
# リポジトリが最新の状態でない場合は、一度削除して再クローンするか、git pullで最新化
# （リポジトリをクローンした後にファイルが追加された場合に必要）
cd /opt/todoapp
rm -rf temp-config
git clone https://github.com/yamadas1213/three-tier-architecture-beginner.git temp-config

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
# 仮想環境とgunicornが正しくインストールされているか確認
cd /opt/todoapp/backend
source venv/bin/activate
which gunicorn
gunicorn --version

# 確認後、仮想環境を無効化
deactivate

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

**重要**: この時点では、MySQL HeatWaveのプライベートIPアドレスとパスワードが確定していないため、
環境変数の編集は後回しにします。MySQL HeatWaveの構築が完了した後、
「MySQL HeatWaveの構築」セクションの後に再度このファイルを編集してください。

### nginxの設定

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・5. nginxの設定`

```bash
# リポジトリからクローンしたnginx設定ファイルをコピー
sudo cp /opt/todoapp/temp-config/config/todoapp.conf /etc/nginx/conf.d/todoapp.conf

# nginx設定ファイルの内容を確認（proxy_passのパスが正しいか確認）
sudo cat /etc/nginx/conf.d/todoapp.conf

# デフォルト設定の無効化
sudo rm -f /etc/nginx/conf.d/default.conf

# todoapp.confにdefault_serverを追加して優先度を上げる
# （これにより、nginx.confのデフォルトserverブロックと競合せずに優先される）
sudo sed -i 's/listen 80;/listen 80 default_server;/' /etc/nginx/conf.d/todoapp.conf

# nginxの設定を確認してから起動
sudo nginx -t

# nginxの起動と自動起動設定
sudo systemctl start nginx
sudo systemctl enable nginx

# サービスが正常に起動しているか確認
sudo systemctl status nginx

```

### ファイアウォール設定（firewalld）

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・6. ファイアウォール設定（firewalld）`

```bash
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-services
```

### SELinuxの無効化

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・7. SELinuxの無効化`

開発・学習環境では、SELinuxを無効化することで権限問題を回避できます。
本番環境では適切に設定することを推奨しますが、ここでは無効化します。

```bash
# SELinuxの現在の状態を確認
getenforce

# SELinuxを無効化（再起動後に反映）
sudo sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config

# 現在のセッションでも一時的に無効化（即座に反映）
sudo setenforce 0

# 無効化されたことを確認
getenforce
```

### アプリケーションの動作確認（ローカル）

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・8. アプリケーションの動作確認（ローカル）`

MySQL HeatWaveがまだ作成されていない段階ですが、アプリケーションサーバーが正しく設定されているか確認します。

```bash
# nginxを再起動して設定を反映
sudo systemctl restart nginx

# アプリケーションサーバー自身から、ローカルホスト経由でアクセス
# ヘルスチェックエンドポイント（データベース接続不要）の確認
curl http://localhost/health

# フロントエンドのHTMLファイルが配信されるか確認
curl -I http://localhost/

# サービス状態の確認
sudo systemctl status todoapp
sudo systemctl status nginx
```

**注意**: この時点では、MySQL HeatWaveがまだ作成されていないため、`/api/todos`エンドポイントはエラーになります。
`/health`エンドポイントはデータベース接続を行わないため、正常にレスポンスが返ります。

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

### Gunicorn設定ファイルの更新

書籍: `=== MySQL HeatWaveの構築 > ==== ■2. データベースとテーブルの作成 > ===== ・3. Gunicorn設定ファイルの更新`

MySQL HeatWaveの作成が完了し、プライベートIPアドレスとパスワードが確定したため、
Gunicornのsystemdサービスファイルを更新します。

```bash
# Gunicornのサービスファイルを編集
sudo vi /etc/systemd/system/todoapp.service

# 以下の環境変数を実際の値に置き換えます：
# Environment="MYSQL_HOST=<mysql-private-ip>"  →  MySQL HeatWaveのプライベートIPアドレス
# Environment="MYSQL_PASSWORD=<mysql-password>" →  MySQL HeatWaveの管理者パスワード

# 設定を更新したら、systemdの設定を再読み込みしてサービスを再起動
sudo systemctl daemon-reload
sudo systemctl restart todoapp

# サービスが正常に起動しているか確認
sudo systemctl status todoapp
```

**注意**: MySQL HeatWaveのプライベートIPアドレスは、OCIコンソールの「データベース」→「MySQL HeatWave」→
作成したDBシステムの「接続」タブから確認できます。パスワードは、MySQL HeatWave作成時に設定した管理者パスワードを使用してください。

### データベース接続後の動作確認

書籍: `=== MySQL HeatWaveの構築 > ==== ■2. データベースとテーブルの作成 > ===== ・4. データベース接続後の動作確認`

Gunicorn設定ファイルを更新し、MySQL HeatWaveへの接続が正しく設定された後、
アプリケーションが正常に動作するか確認します。

```bash
# まず、Gunicornサービスが正常に起動しているか確認
sudo systemctl status todoapp

# GunicornのUnixソケットファイルが作成されているか確認
ls -la /opt/todoapp/backend/todoapp.sock

# nginxの設定が正しく読み込まれているか確認
sudo nginx -t

# nginxの設定ファイルを確認（デフォルト設定が残っていないか確認）
sudo ls -la /etc/nginx/conf.d/

# nginx設定ファイルの内容を確認（proxy_passのパスが正しいか確認）
sudo cat /etc/nginx/conf.d/todoapp.conf

# もし proxy_pass が http://unix:/opt/todoapp/todoapp.sock になっている場合は、
# リポジトリから最新の設定ファイルを再コピーするか、手動で修正する
# sudo cp /opt/todoapp/temp-config/config/todoapp.conf /etc/nginx/conf.d/todoapp.conf
# sudo systemctl reload nginx

# GunicornのUnixソケットのパスと、nginx設定のパスが一致しているか確認
# 設定ファイルの proxy_pass が http://unix:/opt/todoapp/backend/todoapp.sock になっているか確認

# nginxのエラーログを確認（問題がある場合）
sudo tail -20 /var/log/nginx/error.log

# nginxのメイン設定ファイルを確認（conf.dディレクトリが読み込まれているか確認）
sudo grep -A 5 "include.*conf.d" /etc/nginx/nginx.conf

# nginxのアクセスログも確認（リクエストが到達しているか確認）
sudo tail -10 /var/log/nginx/access.log

# nginxが読み込んでいる設定ファイルを確認
sudo nginx -T 2>&1 | grep -A 10 "server_name"

# アプリケーションサーバー自身から、ローカルホスト経由でアクセス
# ヘルスチェックエンドポイントの確認
curl http://localhost/health

# APIエンドポイントの動作確認（データベース接続が必要）
# タスク一覧の取得
curl http://localhost/api/todos

# 新規タスクの追加
curl -X POST http://localhost/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"データベース接続確認用タスク"}'

# 再度タスク一覧を取得して、追加されたことを確認
curl http://localhost/api/todos

# フロントエンドのHTMLファイルが配信されるか確認
curl -I http://localhost/
```

**確認ポイント**:
- `/health`: `{"status": "ok"}` が返る
- `/api/todos`: タスク一覧がJSON形式で返る（初期データがあれば表示される）
- `POST /api/todos`: 新しいタスクが追加され、`{"ok": true}` が返る

データベース接続エラーが発生する場合は、Gunicorn設定ファイルの環境変数（MYSQL_HOST、MYSQL_PASSWORD）が正しく設定されているか確認してください。

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

