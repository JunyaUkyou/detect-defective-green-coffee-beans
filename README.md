# detect-defective-green-coffee-beans

This app detects defective green coffee beans.

docker compose build

docker compose run --entrypoint "poetry install --no-root" backend

docker compose run \
 --entrypoint "poetry init \
 --name api \
 --dependency fastapi \
 --dependency uvicorn[standard]" \
 api
