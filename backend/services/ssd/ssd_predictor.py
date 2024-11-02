# パッケージインポート
import torch
from torchvision import transforms
from PIL import ImageDraw, ImageFont
import os
import matplotlib.pyplot as plt

# 別ファイルからインポート
from .net import Net               # ネットワーク
from .constants import CLASS_NAMES  # 定数

# グローバル変数としてモデルを宣言
g_ssd_model = None


def load_model():
    """
    SSDモデルをロードし、グローバル変数に保存する関数。

    事前学習済みのSSDモデルをロードし、`g_ssd_model`に格納します。
    既にモデルがロードされている場合は再読み込みを行いません。
    モデルの重みは、スクリプトのあるディレクトリの`SSD_weights.pth`ファイルから読み込まれます。

    戻り値:
        torch.nn.Module: SSDモデルを格納したネットワークインスタンス。
    """

    # グローバル変数がNoneの場合モデルロード
    global g_ssd_model
    if (g_ssd_model == None):

        # モデルの重みファイルパス取得
        current_dir = os.path.dirname(os.path.abspath(__file__))    # 現在の絶対パス取得
        weights_path = os.path.join(
            current_dir, 'SSD_weights.pth')  # 絶対パスを元に重みファイルパス取得

        # モデルをグローバル変数に読み込み
        g_ssd_model = Net()
        g_ssd_model.load_state_dict(torch.load(
            weights_path, map_location=torch.device('cpu'), weights_only=True))
        g_ssd_model.eval()
    return g_ssd_model


def run_ssd_prediction(image):
    """
    画像に対してSSDモデルによる推論を実行し、結果を可視化した画像を返す関数。

    入力画像をSSDモデルで推論し、推論結果に基づいてバウンディングボックスとラベルを描画した
    画像を生成して返します。内部で`load_model`を用いてモデルをロードし、画像をTensor形式に
    変換した上で推論を行います。

    パラメータ:
        image (PIL.Image): 入力画像。

    戻り値:
        PIL.Image: 推論結果が描画された画像。
    """

    # モデルロード
    model = load_model()

    # 前処理
    transform = transforms.ToTensor()
    x = transform(image).unsqueeze(0)

    # 推論
    with torch.no_grad():
        y = model(x)

    # 推論結果を可視化した画像を返却
    return visualize(x[0], y[0])


def visualize(input_tensor, output):
    """
    推論結果のバウンディングボックスとラベルを画像に描画する関数。

    SSDモデルの出力に含まれるバウンディングボックスとラベルをPIL画像上に描画し、
    カラーコードはラベルに基づくカラーマップで表示します。
    描画には日本語フォントを使用します。

    パラメータ:
        input_tensor (torch.Tensor): モデルの入力テンソル。
        output (dict): モデルの出力結果で、`boxes`と`labels`が含まれる辞書。

    戻り値:
        PIL.Image: バウンディングボックスとラベルが描画された画像。
    """

    # 画像に推論結果を描画できる状態に変換
    image = transforms.ToPILImage()(input_tensor)  # PIL形式に変換
    draw = ImageDraw.Draw(image)                  # 描画オブジェクトに変換

    # バウンディングボックスとラベルの抽出
    boxes = output['boxes'].cpu().detach().numpy()
    labels = output['labels'].cpu().detach().numpy()

    # 描画に使用するフォント取得
    font_size = 16
    font = ImageFont.truetype('fonts/NotoSansCJKjp-Bold.otf', font_size)

    # 描画に使用するカラーマップ取得
    color_map = plt.cm.get_cmap('hsv', len(CLASS_NAMES) + 1)  # ラベル数分取得

    # バウンディングボックスとラベルの描画
    for box, label in zip(boxes, labels):
        # バウンディングボックスの描画
        color = color_map(label, bytes=True)  # カラーマップからラベルに応じた色を取得
        draw.rectangle(box, outline=color)   # バウンディングボックスの描画

        # 描画するラベル名を取得
        text = CLASS_NAMES[label]

        # ラベルの背景となる短形の描写
        left, top, right, bottom = font.getbbox(
            text=text)  # 描画するラベル名に必要な領域を短形の座標で取得
        text_height = bottom                               # ラベル背景の短形の高さを取得
        text_width = right - left                          # ラベル背景の短形の幅を取得
        draw.rectangle([box[0], box[1], box[0]+text_width,
                       box[1]+text_height], fill=color)

        # ラベルの描画
        draw.text((box[0], box[1]), text, font=font, fill='white')

    return image
