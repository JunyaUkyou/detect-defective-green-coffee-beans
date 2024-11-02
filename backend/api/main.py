# パッケージインポート
from fastapi import Depends, FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from logging import getLogger

# 別ファイルからインポート
from services.ssd import ssd_predictor # SSD処理関連
from .validate import validate_image   # バリデーション
from core.config import FRONTEND_URL   # 設定値


logger = getLogger("uvicorn.app")
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

@app.on_event("startup")
async def startup_event():
    logger.info("startup event start")
    # アプリ起動時にモデルを読み込む
    # 推論時に事前学習済みモデルの重みファイルがキャッシュに存在しない場合ダウンロード処理が行われる
    # 推論時でダウンロード処理が加わるとAPIレスポンスが遅くなるためアプリ起動時にダウンロードを行う
    ssd_predictor.load_model()
    logger.info("startup event end")

@app.post('/ssd')
async def ssd(file: UploadFile = Depends(validate_image)):
  try:
    # 画像を開く
    image = Image.open(file.file)

    # 推論
    result_img = ssd_predictor.run_ssd_prediction(image)

    # バイナリデータとして画像をメモリ上に保存
    img_io = io.BytesIO()
    result_img.save(img_io, format='JPEG')
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/jpeg")
  except Exception as e:
    logger.error(f"ssd Exception Error: {e}")
    raise HTTPException(status_code=500, detail="Exception Error")
