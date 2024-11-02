# パッケージインポート
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 別ファイルからインポート
from .events import startup
from .routers import ssd
from core.config import FRONTEND_URL   # 設定値

app = FastAPI()

# 許可するURL
origins = [
  FRONTEND_URL, # フロントエンドのURL
]

# CORS 設定を追加
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# イベントの登録
app.add_event_handler("startup", startup.load_ssd)

# ルーターの登録
app.include_router(ssd.router)