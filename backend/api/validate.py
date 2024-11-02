from fastapi import File, HTTPException, UploadFile
from PIL import Image

async def validate_image(file: UploadFile = File(...)):
    # ファイル形式の確認
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="画像ファイルが必要です")

    # ファイルサイズの確認
    if file.size > 1024 * 1024:  # 例: 1MB以下
        raise HTTPException(status_code=400, detail="ファイルサイズが大きすぎます")

    # 画像サイズの確認
    image = Image.open(file.file)
    if image.width != image.height:
      raise HTTPException(status_code=400, detail="画像の幅と高さは一致している必要があります")


    return file