# ベースイメージを設定
FROM node:20-bookworm-slim AS base

# 作業ディレクトリを作成
WORKDIR /usr/src/app/app

# package.json と package-lock.json をコピー
COPY ./app/package*.json ./

# 依存パッケージをインストール
RUN npm install

# アプリケーションコードをコピー
COPY ./app .

# --- 2. ローカル開発用 (Composeから呼ばれる) ---
FROM base AS dev
EXPOSE 5173
CMD ["npm", "run", "dev"]

# --- 3. 本番用 (ECRへPushするときに使われる) ---
FROM base AS prod
RUN npm run build
EXPOSE 5173
# npm を介さず、Vite を直接起動して SIGTERM を正しく受け取れるようにする
CMD ["./node_modules/.bin/vite", "preview", "--host", "0.0.0.0", "--port", "5173"]