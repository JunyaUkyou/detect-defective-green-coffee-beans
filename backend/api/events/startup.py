# パッケージをインポート
from logging import getLogger

# 別ファイルからインポート
from services.ssd import ssd_predictor  # SSD処理関連
from core.config import FRONTEND_URL   # 設定値

logger = getLogger("uvicorn.app")


async def load_ssd():
    """
    SSDモデルをアプリ起動時に読み込む

    この関数はアプリの起動イベントで呼ばれ、SSDモデルを読み込みます。
    起動イベントでSSDモデルを読み込む理由は、
    事前学習済みモデルの重みファイルがキャッシュに存在しない場合は
    重みファイルのダウンロード処理が行われます。
    このダウンロード処理に1分程度はかかるため、
    アプリ起動時にダウンロード処理を行うことで、
    推論時のAPIリクエストの応答時間を短縮します。
    """
    logger.info("startup event load_ssd start")
    ssd_predictor.load_model()
    logger.info("startup event load_ssd end")
