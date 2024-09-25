from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw
import io
import json
import os




app = FastAPI()

# 許可するURL
origins = [
  "http://localhost:5173", # フロントエンドのURL
]

# CORS 設定を追加
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post('/ssd')
async def ssd(file: UploadFile = File(...)):
  # 画像を開く
  image = Image.open(file.file)

  # ここで推論を実行（物体検出）
  # バウンディングボックスを描画する例（仮の座標）
  draw = ImageDraw.Draw(image)
  draw.rectangle([50, 50, 200, 200], outline="red", width=3)  # 仮のバウンディングボックス

  # メモリ上で画像を保存して、レスポンスとして返す
  img_io = io.BytesIO()
  image.save(img_io, format="JPEG")
  img_io.seek(0)

  return StreamingResponse(img_io, media_type="image/jpeg")


@app.post('/autoencoder')
async def autoencoder():
  current_dir = os.path.dirname(os.path.abspath(__file__))
  json_path = os.path.join(current_dir, 'threshold.json')

  with open(json_path, 'r') as f:
    config = json.load(f)
    threshold = float(config["autoencoder"])
  return threshold