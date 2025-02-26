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


## インストールメモ
※apiのoptionにメンバー名やファンアートタグをまとめたcsvがあり、これを元にDBの更新を行う。
1. docker-composeのインストール
1. [task](https://taskfile.dev/installation/)のインストール
1. CloudFlareでAPIとWEB公開用のトンネルを作成
1. トンネルのトークンの環境変数API_TOKENとUI_TOKENをセット
1. task build or task deployでコンテナ作成
1. 定期的にDBの更新バッチ処理を走らせる


## 環境

開発用
- jupyter lab
- flask(localhost)
- ui(localhost)
- postgresql

本番用
- flask
- postgresql
- nginx
- api tunnel
- nginx tunnel


---

当サイトは以下のガイドラインに従い作成しております。

[ホロライブの二次創作ライセンス規約](https://www.hololive.tv/terms)