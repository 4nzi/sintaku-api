# sintaku-api

sintaku のバックエンドです。

# 機能仕様

- 新規アカウント作成 ( api/register/ )
- プロフィールの取得、作成、最新  ( api/profile/)
- ログインユーザーのプロフィール取得  (  api/myprofile/)
- 投稿の取得、作成、最新( api/posts/)
- JWTトークン取得 (api/jwt/create/)
- JWTトークン確認 ( api/jwt/verify/)
- ページネーション

# 使用技術

- Django REST Framework
- simple-JWT

# AWS

- S3
- EC2
- Route53
