# パッケージ
import pytest
from fastapi.testclient import TestClient

# 他処理
from api.main import app  # main.pyのFastAPIインスタンスをインポート
from services.ssd import ssd_predictor  # モック対象のモジュールをインポート

client = TestClient(app)


@pytest.fixture(autouse=True)
def skip_download(monkeypatch):
    """load_ssdの処理は実行時間がかかるためモックする"""
    monkeypatch.setattr(ssd_predictor, "load_model", lambda: None)


def test_ssd_return_422():
    """必須パラメータが無い場合"""
    # file無しでリクエストする
    response = client.post("/ssd")
    assert response.status_code == 422
