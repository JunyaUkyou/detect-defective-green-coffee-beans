# pythonのイメージをダウンロード
FROM python:3.11-bookworm
# pythonの出力表示をDocker用に調整
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# 環境変数にPYTHONPATHを設定
ENV PYTHONPATH="${PYTHONPATH}:/src"

# requirements.txt をコピーして pip で一括インストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードのコピー
COPY . /src

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]