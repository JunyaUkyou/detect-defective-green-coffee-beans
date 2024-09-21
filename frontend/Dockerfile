# ベースイメージを設定
FROM node:16

# 作業ディレクトリを作成
WORKDIR /usr/src/app/app

# package.json と package-lock.json をコピー
COPY ./app/package*.json ./

# 依存パッケージをインストール
RUN npm install

# アプリケーションコードをコピー
COPY ./app .
