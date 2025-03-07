# pythonイメージ
FROM python:3.11

# タイムゾーンを日本時間に設定
ENV TZ=Asia/Tokyo
RUN apt-get update && apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y cron

# uvのインストール
RUN pip install uv

# 作業ディレクトリの設定
WORKDIR /cron

# APIのファイルをコピー
COPY ../api/ /cron

# 仮想環境を作成し、依存関係をインストール
RUN uv sync

# cronの設定
COPY ../cron/cron_jobs /etc/cron_jobs
RUN crontab /etc/cron_jobs
RUN touch /var/log/cron.log

# cron を実行
CMD cron -f