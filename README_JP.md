# player_roster

[English README](README.md)

## 概要

本プロジェクトは Django REST Framework（DRF）を用いて開発した、ユーザ認証・権限制御を備えた RESTful Web API である。

ユーザはプレイヤーに対してコメントを投稿・閲覧でき、
ユーザの役割（admin / general）に応じて、実行可能な API や取得できるレスポンスが制御される。

JWT による認証・認可を前提に、
ロールベースの権限制御やリソース指向の API 設計、 およびテストを意識した実装を行っている。

🔗 **Swagger UI (API Documentation)**
https://player-roster.onrender.com/api/schema/swagger-ui/

## 主な機能

-   JWT を用いたユーザ認証
-   ユーザの役割（admin / general）に応じた API アクセス制御
-   ユーザの役割に応じたレスポンス内容の制御
-   ユーザ、チーム、プレイヤー、コメント情報の一覧取得および詳細取得
-   ユーザ、チーム、プレイヤー、コメントの新規作成および閲覧
-   条件付きでのリソース取得（フィルタリング、検索、並び替え）
-   API リクエスト回数制限（Throttling）
-   論理削除（Soft Delete）によるデータの非表示制御

## 設計方針

### ユーザ登録と認証設計

利用者は自由にユーザ登録することが可能である。
ユーザ登録時には username、email、パスワードのみを必須項目とした。

email は個人情報であるため、レスポンスには含めず、
必要最小限の情報のみを公開する設計としている。

ユーザ登録時のロールはすべて一般ユーザ（general）とし、
管理者ユーザ（admin）は API 経由では作成できない。
admin ユーザは、API の管理者がターミナルから直接登録する運用を想定している。

これにより、権限昇格を防ぎ、セキュリティを担保している。

### ロールベースのアクセス制御

チームおよびプレイヤーの新規作成・更新は、
データの整合性を保つため、管理者ユーザ（admin）のみに制限している。

一方で、一覧取得および詳細取得は一般ユーザ（general）にも許可し、
参照系と更新系の責務を明確に分離した。

### レスポンス内容の制御

同一のエンドポイントであっても、
ユーザのロール（general / admin）に応じてレスポンス内容を制御している。

これにより、管理用途に必要な情報と、
一般ユーザに公開すべき情報を明確に分離している。

### 論理削除

データは物理削除せず、deleted_at を用いた論理削除を採用している。
これにより、誤削除時の復旧や履歴管理を可能としている。

一般ユーザからは削除済みデータを非表示とし、
管理者ユーザは必要に応じて参照可能な設計としている。

### API 利用制限

API の安定性を保つため、ユーザの種別に応じた
リクエスト回数制限（Throttling）を導入している。

これにより、過剰なリクエストや不正利用を防止している。

## 技術スタック

### バックエンド

-   Python
-   Django
-   Django REST Framework

### 認証・認可

-   JWT（djangorestframework-simplejwt）

### データベース

-   SQLite（開発環境）
-   PostgreSQL（本番環境を想定）

### API 機能

-   django-filter（Filtering）
-   Ordering / SearchFilter（Django REST Framework）

### テスト

-   pytest
-   pytest-django

### 環境管理

-   django-environ

## テスト

本プロジェクトでは、責務ごとにテスト対象を分離している。

-   Models  
    モデルの属性やメソッドの振る舞いを検証する。

-   Serializers  
    シリアライズ / デシリアライズおよびバリデーションの挙動を検証する。

-   Views  
    実際の HTTP リクエストを通じて、認証・権限・レスポンスの挙動を検証する。

詳細なテストケースについては、[documents/tests](documents/tests/) に記載している。

## 認証

本プロジェクトでは JWT を用いた認証を採用している。

アクセストークンとリフレッシュトークンを用いることで、
セキュリティと利便性の両立を図っている。

## セットアップ

```bash
git clone https://github.com/kikutan-day65/player_roster.git
cd player_roster

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## API デモ利用手順

Swagger UI は以下の URL からアクセス。
https://player-roster.onrender.com/api/docs/

1. ユーザー登録エンドポイント（`POST api/v1/user-accounts/`）を使用してユーザーを作成。
2. `/api/token/` にリクエストを送信し、JWT のアクセストークンを取得。
3. Swagger UI の **Authorize** ボタンをクリックし、取得したアクセストークンを入力。

## 補足

-   本プロジェクトは学習および設計検証を目的としている。
-   フロントエンドは未実装であり、API 単体での動作を想定している。
