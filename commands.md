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

# インストール確認
python3.11 --version
python3.11 -m pip --version
nginx -v
mysql --version
git --version
```

### GitHubリポジトリのクローン

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・2. アプリケーションのセットアップ > ===== ・2-1. GitHubリポジトリのクローン`

```bash
sudo mkdir -p /opt/todoapp
sudo chown opc:opc /opt/todoapp
cd /opt/todoapp
git clone https://github.com/yamadas1213/three-tier-architecture-beginner.git .
ls -la
```

### Python依存パッケージのインストール

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・3. Python依存パッケージのインストール`

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r ./opt/backend/requirements.txt
```

### Gunicornの設定

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・4. Gunicornの設定`

```bash
sudo cp config/todoapp.service /etc/systemd/system/todoapp.service
sudo systemctl daemon-reload
sudo systemctl start todoapp
sudo systemctl enable todoapp
```

### nginxの設定

書籍: `=== アプリケーション用Computeの構築 > ==== ■2. アプリケーションのデプロイ > ===== ・5. nginxの設定`

```bash
sudo cp config/todoapp.conf /etc/nginx/conf.d/todoapp.conf
sudo rm -f /etc/nginx/conf.d/default.conf
sudo nginx -t
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

