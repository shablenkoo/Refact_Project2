from typing import List, Dict, Optional
from threading import Lock
from src.core.interfaces import IQRRepository
from src.models.qr_models import QRCodeEntity

class InMemoryQRRepository(IQRRepository):
    def __init__(self):
        self._storage: Dict[str, QRCodeEntity] = {}
        self._lock = Lock()

    def save(self, qr: QRCodeEntity) -> None:
        with self._lock:
            self._storage[str(qr.id)] = qr

    def get_by_id(self, qr_id) -> Optional[QRCodeEntity]:
        return self._storage.get(str(qr_id))

    def get_all(self) -> List[QRCodeEntity]:
        return list(self._storage.values())