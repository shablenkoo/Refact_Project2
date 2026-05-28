import pytest
from src.storage.in_memory_repo import InMemoryQRRepository
from src.services.strategies import StandardPNGStrategy
from src.services.qr_service import QRService
from src.services.observers import HistoryLogger

@pytest.fixture
def repo():
    return InMemoryQRRepository()

@pytest.fixture
def strategy():
    return StandardPNGStrategy()

@pytest.fixture
def service(repo, strategy):
    return QRService(repo, strategy)

@pytest.fixture
def logger():
    return HistoryLogger()