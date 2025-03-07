# Holomoti

ホロライブのファンアートをまとめた閲覧サイト(開発中)

全てdocker-composeで構築し、できるだけ簡単にデプロイできる環境を目指す。


## 構成

| 役割 | サービス名 |
| ---- | ---- |
| API | flask|
| UI | Quasar Framework |
| DB | PostgreSQL |
| 静的サイト表示 | nginx | 
| 外部公開 | CloudFlare Tunnel |
| タスク処理 | Task |
| 定期実行 | cron |


## インストールメモ
※apiのoptionにメンバー名やファンアートタグをまとめたcsvがあり、これを元にDBの更新を行う。
1. docker-composeのインストール
1. [task](https://taskfile.dev/installation/)のインストール
1. CloudFlareでAPIとWEB公開用のトンネルを作成
1. トンネルのトークンの環境変数API_TOKENとUI_TOKENをセット
1. task build or task deployでコンテナ作成
1. 定期的にDBの更新バッチ処理を走らせる

## トンネル作成

[Cloudflare ZeroTrust公式ドキュメント](https://taskfile.dev/installation/)  
トンネル作成にあたり、以下のサイトを参考に設定した。     
[参考リンク](https://growi.cloud/blog/5787)  
  
作成時、本番用の設定ファイルで  
cloudflaredのコンテナ &rarr; 接続用のコンテナ  
に差し替えばよい。  
nginxとAPI用にそれぞれ作成する。

## docker-composeの構成

docker-compose.yml &larr; 共通
- DB
- API
- cron
- バッチ処理
- UIのビルド

docker-compose.override &larr; 開発用
- jupyter lab
- quasar dev

docker-compose.prob &larr; 本番用
- nginxのwebサーバー
- APIの外部公開用トンネル
- webの外部公開用トンネル

---

当サイトは以下のガイドラインに従い作成しております。

[ホロライブの二次創作ライセンス規約](https://www.hololive.tv/terms)