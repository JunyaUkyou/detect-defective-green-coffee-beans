# パッケージをインポート
from logging import getLogger

# 別ファイルからインポート
from services.ssd import ssd_predictor # SSD処理関連
from core.config import FRONTEND_URL   # 設定値

logger = getLogger("uvicorn.app")

async def load_ssd():
    logger.info("startup event load_ssd start")
    # アプリ起動時にモデルを読み込む
    # 推論時に事前学習済みモデルの重みファイルがキャッシュに存在しない場合ダウンロード処理が行われる
    # 推論時でダウンロード処理が加わるとAPIレスポンスが遅くなるためアプリ起動時にダウンロードを行う
    ssd_predictor.load_model()
    logger.info("startup event load_ssd end")