from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw
import io
import json
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
import numpy as np
from logging import getLogger

# 各処理を別ファイルからインポート
from .ssd_predictor import run_ssd_prediction, load_model
logger = getLogger("uvicorn.app")
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

@app.on_event("startup")
async def startup_event():
    logger.info("startup event start")
    # アプリ起動時にモデルを読み込む
    # 推論時に事前学習済みモデルの重みファイルがキャッシュに存在しない場合ダウンロード処理が行われる
    # 推論時でダウンロード処理が加わるとAPIレスポンスが遅くなるためアプリ起動時にダウンロードを行う
    load_model()
    logger.info("startup event end")

@app.post('/ssd')
async def ssd(file: UploadFile = File(...)):
  # 画像を開く
  image = Image.open(file.file)
  
  # 推論
  result_img = run_ssd_prediction(image)

  # バイナリデータとして画像をメモリ上に保存
  img_io = io.BytesIO()
  result_img.save(img_io, format='JPEG')
  img_io.seek(0)

  return StreamingResponse(img_io, media_type="image/jpeg")
