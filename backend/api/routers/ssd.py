
# パッケージインポート
from fastapi import Depends, APIRouter,  UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from logging import getLogger

# 別ファイルからインポート
from services.ssd import ssd_predictor  # SSD処理関連
from ..validate import validate_image  # バリデーション

router = APIRouter()


@router.post('/ssd')
async def ssd(file: UploadFile = Depends(validate_image)):
    """
    画像ファイルを受け取り、SSDモデルで物体検出を行い、推論結果を画像として返すエンドポイント。

    このエンドポイントは、アップロードされた画像ファイルをSSDモデルで処理し、
    検出された物体をバウンディングボックスで描画した画像をJPEG形式でストリームとして返します。

    パラメータ:
      file (UploadFile): アップロードされた画像ファイル。`validate_image`依存関数で
      バリデーションチェックを行う。

    戻り値:
      StreamingResponse: 推論結果が描画された画像のストリーミングレスポンスをJPEG形式で返す。

    例外:
      HTTPException: 処理中にエラーが発生した場合、500ステータスコードとエラーメッセージを返す。
    """
    try:
        # 画像を開く
        image = Image.open(file.file)

        # 画像サイズが300より大きい場合はリサイズ
        if (image.width > 300):
            new_size = (300, 300)
            image = image.resize(new_size)

        # 推論
        result_img = ssd_predictor.run_ssd_prediction(image)

        # バイナリデータとして画像をメモリ上に保存
        img_io = io.BytesIO()
        result_img.save(img_io, format='JPEG')
        img_io.seek(0)

        return StreamingResponse(img_io, media_type="image/jpeg")
    except Exception as e:
        logger = getLogger("uvicorn.app")
        logger.error(f"ssd Exception Error: {e}")
        raise HTTPException(status_code=500, detail="Exception Error")
