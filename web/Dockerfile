# 2. Nginxを使って静的ファイルを配信
FROM nginx:latest

WORKDIR /usr/share/nginx/html

# Nginxの設定をコピー
COPY ./default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]