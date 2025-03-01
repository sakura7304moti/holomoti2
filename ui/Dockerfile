# ベースイメージ
FROM node:22

# 作業ディレクトリを設定
WORKDIR /ui

# uiフォルダ内の前ファイルをコピー
COPY . .

# パッケージをインストール
RUN npm install
#RUN npm i -g @quasar/cli
#RUN npm i @quasar/app-vite
#RUN npm i quasar 
#RUN npm i @quasar/extras

# 開発サーバーを実行
#CMD ["npm",  "run","dev",  "--hostname", "0.0.0.0"]