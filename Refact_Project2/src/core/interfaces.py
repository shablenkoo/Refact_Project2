from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.qr_models import QRCodeEntity, LogEntry


class IQRRepository(ABC):
    @abstractmethod
    def save(self, qr: QRCodeEntity) -> None: ...

    @abstractmethod
    def get_by_id(self, qr_id) -> Optional[QRCodeEntity]: ...

    @abstractmethod
    def get_all(self) -> List[QRCodeEntity]: ...


class IQRStrategy(ABC):
    @abstractmethod
    def generate(self, data: str) -> str: ...


class IObserver(ABC):
    @abstractmethod
    def update(self, event_type: str, data: LogEntry) -> None: ...