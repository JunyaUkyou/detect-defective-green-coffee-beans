# detect-defective-green-coffee-beans

# 画面 URL

http://localhost:5173/

# API doc

http://localhost:8000/docs

# 初回起動

This app detects defective green coffee beans.

docker compose build

docker compose run --entrypoint "poetry install --no-root" backend

docker compose run \
 --entrypoint "poetry init \
 --name api \
 --dependency fastapi \
 --dependency uvicorn[standard]" \
 api

# 2 回目以降起動

docker compose up -d
