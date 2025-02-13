# Python公式イメージ（適宜バージョン変更）
FROM python:3.11

# uvのインストール
RUN pip install uv

# 作業ディレクトリの設定
WORKDIR /app

# apiフォルダ内の全ファイルをコピー
COPY . .

# 仮想環境を作成し、依存関係をインストール
RUN uv sync
