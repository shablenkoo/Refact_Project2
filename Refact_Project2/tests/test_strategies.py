import pytest
from src.services.strategies import StandardPNGStrategy, JsonMetadataStrategy
from src.services.qr_service import QRService


def test_strategy_output_formats(repo):
    service_png = QRService(repo, StandardPNGStrategy())
    res_png = service_png.create_qr("test")
    assert isinstance(res_png, str)

    service_json = QRService(repo, JsonMetadataStrategy())
    res_json = service_json.create_qr("test")
    assert '{"data": "test"' in res_json


@pytest.mark.parametrize("data", ["Hello", "https://google.com", "WiFi:123"])
def test_standard_strategy_consistency(strategy, data):
    result = strategy.generate(data)
    assert len(result) > 50