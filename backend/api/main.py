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
from .ssd_predictor import run_ssd_prediction
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
    logger.info("Startup event called")
    # load_model()をここで呼び出すモデルをバックエンド起動時に読み込む
    #load_model()   

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


@app.post('/autoencoder')
async def autoencoder(file: UploadFile = File(...)):
  
  # 画像を開く
  image = Image.open(file.file)
  
  # 現在のディレクトリ取得
  current_dir = os.path.dirname(os.path.abspath(__file__))
  
  # 学習済みモデル、閾値取得
  model_path = os.path.join(current_dir, 'Autoencoder_back.pt')
  threshold_path = os.path.join(current_dir, 'threshold.json')

  # 学習済みモデルロード
  model = torch.jit.load(model_path)  
  
  # 前処理
  transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
  ])
  
  # 推論
  model.eval()
  x = transform(image)
  x = x.unsqueeze(0)
  #print('x', x)
  #print('x shape', x.shape)
  y = model(x)
  #print('y', y)
  
  # 平均二乗誤差
  mse_loss = F.mse_loss(y, x, reduction='none')
  # 損失合計を算出
  total_loss = np.sum(mse_loss.detach().numpy(), axis=(1, 2, 3))
  
    # 欠点豆判定
  with open(threshold_path, 'r') as f:
    config = json.load(f)
    threshold = float(config["autoencoder"])
    print('total_loss', total_loss)
    print('total_loss_0', total_loss[0])
    print('threshold', threshold)
    
    print('判定', threshold < total_loss[0])
    
    # 閾値より損失が大きい場合は欠点豆と判断する
    if (threshold < total_loss[0]):
      result = '欠点豆'
    else:
      result = '良質豆'
  return result