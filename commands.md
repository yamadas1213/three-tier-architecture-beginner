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

システム更新:

```bash
sudo dnf update -y
```

MySQLクライアントのインストール:

```bash
sudo dnf install mysql -y
```

バージョン確認:

```bash
mysql --version
```

---

## セクション: アプリケーション用Computeの構築

### アプリサーバへのSSH接続（開発サーバ経由）

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ`

開発サーバにSSH接続:

```bash
ssh -i <秘密キー名> opc@<開発用ComputeのパブリックIP>
```

アプリサーバへSSH接続（プライベートIP）:

```bash
ssh -i <秘密キー名> opc@<アプリサーバのプライベートIP>
```

### 必要パッケージのインストール

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・1. 必要パッケージのインストール`

システム更新:

```bash
sudo dnf update -y
```

Python 3.11とpipのインストール:

```bash
sudo dnf install python3.11 python3.11-pip -y
```

nginxのインストール:

```bash
sudo dnf install nginx -y
```

MySQLクライアントのインストール:

```bash
sudo dnf install mysql -y
```

gitのインストール:

```bash
sudo dnf install git -y
```

利用可能なNode.jsモジュールを確認:

```bash
sudo dnf module list nodejs
```

Node.js 20モジュールを有効化:

```bash
sudo dnf module enable -y nodejs:20
```

Node.jsとnpmをインストール:

```bash
sudo dnf install -y nodejs npm
```

インストール確認:

```bash
python3.11 --version
```

```bash
python3.11 -m pip --version
```

```bash
nginx -v
```

```bash
mysql --version
```

```bash
git --version
```

```bash
node --version
```

```bash
npm --version
```

### バックエンドの構築

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・2. バックエンドの構築`

#### アプリケーション用ディレクトリの作成とリポジトリのクローン

書籍: `===== ・2-1. アプリケーション用ディレクトリの作成とリポジトリのクローン`

設定ファイル（Gunicornとnginx）を取得するため、GitHubリポジトリをクローンします。

アプリケーション用ディレクトリの作成:

```bash
sudo mkdir -p /opt/todoapp
```

```bash
sudo chown opc:opc /opt/todoapp
```

```bash
cd /opt/todoapp
```

GitHubからリポジトリをクローン（設定ファイルを取得するため）:

```bash
git clone https://github.com/yamadas1213/three-tier-architecture-beginner.git temp-config
```

#### バックエンドディレクトリの作成

書籍: `===== ・2-2. バックエンドディレクトリの作成`

バックエンドディレクトリの作成:

```bash
mkdir -p backend
```

```bash
cd backend
```

#### Python仮想環境と依存パッケージ

書籍: `===== ・2-3. Python仮想環境の作成と依存パッケージのインストール`

仮想環境の作成:

```bash
python3.11 -m venv venv
```

仮想環境を有効化:

```bash
source venv/bin/activate
```

必要なパッケージのインストール（flask: Webアプリケーションフレームワーク、gunicorn: 本番環境向けWSGIサーバー、mysql-connector-python: MySQLデータベース接続ライブラリ）:

```bash
pip install flask gunicorn mysql-connector-python
```

インストール確認:

```bash
pip list | grep -E "flask|gunicorn|mysql"
```

仮想環境を無効化（ファイルコピーなど通常のシェル操作では不要）:

```bash
deactivate
```

#### バックエンドアプリケーションファイルのコピー

書籍: `===== ・2-4. バックエンドアプリケーションファイルのコピー`

リポジトリからバックエンドファイルをコピー（全ファイルを一括コピー）:

```bash
cp /opt/todoapp/temp-config/backend/* /opt/todoapp/backend/
```

### フロントエンドの構築

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・3. フロントエンドの構築`

#### Viteプロジェクトの作成

書籍: `===== ・3-1. Viteプロジェクトの作成`

/opt/todoappディレクトリに移動:

```bash
cd /opt/todoapp
```

Viteを使ってVue.jsプロジェクトを作成:

```bash
npm create vite@latest frontend -- --template vue
```

プロジェクト作成時に以下の質問が出た場合の回答：
- Ok to proceed? (y) → y を入力
- 「Use rolldown-vite (Experimental)?」→ 「No」を選択（デフォルトで選択されているためEnterキーでOK）
- 「Install with npm and start now?」→ 「No」を選択（開発サーバーの起動は不要で、プロダクションビルドのみ行うため）

プロジェクトディレクトリに移動:

```bash
cd frontend
```

依存パッケージのインストール:

```bash
npm install
```

#### Vue.jsアプリケーションの実装

書籍: `===== ・3-2. Vue.jsアプリケーションの実装`

リポジトリからApp.vueをコピー:

```bash
cp /opt/todoapp/temp-config/frontend/App.vue /opt/todoapp/frontend/src/App.vue
```

#### フロントエンドのビルド

書籍: `===== ・3-3. フロントエンドのビルド`

プロダクションビルドの実行:

```bash
npm run build
```

ビルド結果の確認（distディレクトリが作成される）:

```bash
ls -la dist/
```

### Gunicornの設定

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・4. Gunicornの設定`

仮想環境とgunicornが正しくインストールされているか確認:

```bash
cd /opt/todoapp/backend
```

```bash
source venv/bin/activate
```

```bash
which gunicorn
```

```bash
gunicorn --version
```

確認後、仮想環境を無効化:

```bash
deactivate
```

リポジトリからクローンしたサービスファイルをsystemdディレクトリにコピー（systemdサービスとして登録することで、OS起動時に自動的にアプリケーションが起動します）:

```bash
sudo cp /opt/todoapp/temp-config/config/todoapp.service /etc/systemd/system/todoapp.service
```

環境変数を実際のMySQL HeatWaveの設定に合わせて編集（`<mysql-private-ip>`を実際のMySQLプライベートIPに、`<mysql-password>`を実際のMySQLパスワードに置き換える）:

```bash
sudo vi /etc/systemd/system/todoapp.service
```

systemdの設定を再読み込み:

```bash
sudo systemctl daemon-reload
```

サービスの起動と自動起動設定:

```bash
sudo systemctl start todoapp
```

```bash
sudo systemctl enable todoapp
```

サービスが正常に起動しているか確認:

```bash
sudo systemctl status todoapp
```

**重要**: この時点では、MySQL HeatWaveのプライベートIPアドレスとパスワードが確定していないため、環境変数の編集は後回しにします。MySQL HeatWaveの構築が完了した後、「MySQL HeatWaveの構築」セクションの後に再度このファイルを編集してください。

### nginxの設定

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・5. nginxの設定`

nginx.confのバックアップを取得:

```bash
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
```

既存のdefault_serverが残ると後から配置するtodoapp.confと競合するため、
デフォルトserverブロックをコメントアウト（パターンマッチで安全に変更）:

```bash
sudo sed -i '/^    server {/,/^    }$/s/^/# /' /etc/nginx/nginx.conf
```

リポジトリからクローンしたnginx設定ファイルをコピー:

```bash
sudo cp /opt/todoapp/temp-config/config/todoapp.conf /etc/nginx/conf.d/todoapp.conf
```

nginxの設定を確認してから起動:

```bash
sudo nginx -t
```

nginxの起動と自動起動設定:

```bash
sudo systemctl start nginx
```

```bash
sudo systemctl enable nginx
```

サービスが正常に起動しているか確認:

```bash
sudo systemctl status nginx
```

### ファイアウォール設定（firewalld）

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・6. ファイアウォール設定（firewalld）`

HTTPサービスを恒久的に許可:

```bash
sudo firewall-cmd --add-service=http --permanent
```

```bash
sudo firewall-cmd --reload
```

許可されたサービスを確認:

```bash
sudo firewall-cmd --list-services
```

### SELinuxの設定調整

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・7. SELinuxの設定調整`

nginxからバックエンドへのネットワーク接続を許可するためのポリシーのみ有効化します。

```bash
sudo setsebool -P httpd_can_network_connect on
```

### アプリケーションの動作確認（ローカル）

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・8. アプリケーションの動作確認（ローカル）`

MySQL HeatWaveがまだ作成されていない段階ですが、アプリケーションサーバーが正しく設定されているか確認します。

nginxを再起動して設定を反映:

```bash
sudo systemctl restart nginx
```

ヘルスチェックエンドポイント（データベース接続不要）の確認:

```bash
curl http://localhost/health
```

フロントエンドのHTMLファイルが配信されるか確認:

```bash
curl -I http://localhost/
```

サービス状態の確認:

```bash
sudo systemctl status todoapp
```

```bash
sudo systemctl status nginx
```

**注意**: この時点では、MySQL HeatWaveがまだ作成されていないため、`/api/todos`エンドポイントはエラーになります。`/health`エンドポイントはデータベース接続を行わないため、正常にレスポンスが返ります。

---

## セクション: MySQL HeatWaveの構築

### MySQLへの接続

書籍: `=== MySQL HeatWaveの構築 > ==== ■2. データベースとテーブルの作成 > ===== ・1. MySQLへの接続`

MySQLへ接続（`<mysql-private-ip>`: MySQL HeatWaveのプライベートIPアドレス、パスワード入力プロンプトで、設定したパスワードを入力）:

```bash
mysql -h <mysql-private-ip> -u admin -p
```

### データベースとテーブルの作成

書籍: `=== MySQL HeatWaveの構築 > ==== ■2. データベースとテーブルの作成 > ===== ・2. データベースとテーブルの作成`

データベースの作成:

```sql
CREATE DATABASE tododb;
```

データベースの選択:

```sql
USE tododb;
```

テーブルの作成:

```sql
CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

動作確認用のデータ挿入（オプション）:

```sql
INSERT INTO todos (title, done) VALUES 
('OCIを学ぶ', 0),
('3層アーキテクチャを構築する', 0),
('TODO管理アプリを完成させる', 0);
```

データの確認:

```sql
SELECT * FROM todos;
```

MySQLから切断:

```sql
EXIT;
```

### Gunicorn設定ファイルの更新

書籍: `=== MySQL HeatWaveの構築 > ==== ■2. データベースとテーブルの作成 > ===== ・3. Gunicorn設定ファイルの更新`

MySQL HeatWaveの作成が完了し、プライベートIPアドレスとパスワードが確定したため、Gunicornのsystemdサービスファイルを更新します。

Gunicornのサービスファイルを編集（以下の環境変数を実際の値に置き換えます：`Environment="MYSQL_HOST=<mysql-private-ip>"` → MySQL HeatWaveのプライベートIPアドレス、`Environment="MYSQL_PASSWORD=<mysql-password>"` → MySQL HeatWaveの管理者パスワード）:

```bash
sudo vi /etc/systemd/system/todoapp.service
```

設定を更新したら、systemdの設定を再読み込みしてサービスを再起動:

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl restart todoapp
```

サービスが正常に起動しているか確認:

```bash
sudo systemctl status todoapp
```

**注意**: MySQL HeatWaveのプライベートIPアドレスは、OCIコンソールの「データベース」→「MySQL HeatWave」→作成したDBシステムの「接続」タブから確認できます。パスワードは、MySQL HeatWave作成時に設定した管理者パスワードを使用してください。

### データベース接続後の動作確認

書籍: `=== MySQL HeatWaveの構築 > ==== ■2. データベースとテーブルの作成 > ===== ・4. データベース接続後の動作確認`

Gunicorn設定ファイルを更新し、MySQL HeatWaveへの接続が正しく設定された後、アプリケーションが正常に動作するか確認します。

ヘルスチェックエンドポイントの確認:

```bash
curl http://localhost/health
```

APIエンドポイントの動作確認（データベース接続が必要）、タスク一覧の取得:

```bash
curl http://localhost/api/todos | jq .
```

新規タスクの追加:

```bash
curl -X POST http://localhost/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"データベース接続確認用タスク"}'
```

再度タスク一覧を取得して、追加されたことを確認:

```bash
curl http://localhost/api/todos | jq .
```

フロントエンドのHTMLファイルが配信されるか確認:

```bash
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

MySQLへ接続:

```bash
mysql -h <mysql-private-ip> -u admin -p
```

データベースを選択:

```sql
USE tododb;
```

データを確認:

```sql
SELECT * FROM todos;
```

結果例:

```
+----+--------------+------+---------------------+
| id | title        | done | created_at          |
+----+--------------+------+---------------------+
|  1 | 犬の散歩     |    0 | 2025-08-17 10:30:45 |
+----+--------------+------+---------------------+
```
