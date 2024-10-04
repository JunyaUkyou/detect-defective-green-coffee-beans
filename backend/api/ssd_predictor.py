import torch
from torchvision import transforms
from PIL import ImageDraw, ImageFont
import numpy as np
from .net import Net 
import os
import matplotlib.pyplot as plt

# SSDモデルの推論処理
def run_ssd_prediction(image):
  
    # 現在のディレクトリの絶対パスを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    weights_path = os.path.join(current_dir, 'SSD_weights.pth')    
  
    # モデルを読み込み
    model2 = Net()  # NetはSSDの定義済みクラス
    model2.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
    model2.eval()

    # 前処理
    transform2 = transforms.ToTensor()
    x = transform2(image).unsqueeze(0)

    # 推論
    with torch.no_grad():
        y = model2(x)

    # 推論結果を描写
    class_names = {
      1:"良質豆",
      2:"良質豆",
      3:"欠点豆(形)",
      4:"欠点豆(形)",
    }
    return visualize(x[0], y[0], class_names)

def visualize(input_tensor, output, class_names):
    image = transforms.ToPILImage()(input_tensor)
    cmap = plt.cm.get_cmap('hsv', len(class_names) + 1)

    boxes = output['boxes'].cpu().detach().numpy()
    labels = output['labels'].cpu().detach().numpy()

    draw = ImageDraw.Draw(image)
    font_size = 16
    font = ImageFont.truetype('fonts/NotoSansCJKjp-Bold.otf', font_size)

    for box, label in zip(boxes, labels):
        color = cmap(label, bytes=True)
        # バウンディングボックスの描画
        draw.rectangle(box, outline=color)

        # ラベルの描画
        text = class_names[label]
        left, top, right, bottom = font.getbbox(text=text)
        text_height = bottom
        text_width = right - left
        draw.rectangle([box[0], box[1], box[0]+text_width, box[1]+text_height], fill=color)
        draw.text((box[0], box[1]), text, font=font, fill='white')

    return image
