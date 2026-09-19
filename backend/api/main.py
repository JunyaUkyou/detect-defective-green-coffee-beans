# パッケージインポート
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 別ファイルからインポート
from .events import startup          # イベント
from .routers import ssd, health     # ルーティング
from core.config import FRONTEND_URL  # 設定値


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model
    await startup.load_ssd()
    yield


app = FastAPI(lifespan=lifespan)

# 許可するURL
origins = [
    FRONTEND_URL,  # フロントエンドのURL
]

# CORS 設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルーターの登録
app.include_router(ssd.router)
app.include_router(health.router)
