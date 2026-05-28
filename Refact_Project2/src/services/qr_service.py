from typing import List
from src.core.interfaces import IQRRepository, IQRStrategy, IObserver
from src.models.qr_models import QRCodeEntity, LogEntry
from src.core.exceptions import ValidationError
from src.utils.validators import QRDataValidator


class QRService:

    def __init__(self, repo: IQRRepository, strategy: IQRStrategy):
        self._repo = repo
        self._strategy = strategy
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        self._observers.remove(observer)

    def create_qr(self, content: str, qr_type: str = "URL") -> str:
        QRDataValidator.validate_content(content)
        QRDataValidator.validate_type(qr_type)

        if qr_type == "URL" and not QRDataValidator.is_valid_url(content):
            print(f"--- Warning: Content '{content}' is not a standard URL format ---")

        qr = QRCodeEntity(content=content, qr_type=qr_type)

        self._repo.save(qr)

        image_data = self._strategy.generate(content)

        self._notify("CREATED", qr.id, f"Type: {qr_type}, Content: {content[:20]}...")

        return image_data

    def scan_qr(self, qr_id: str, user_role: str = "READER") -> QRCodeEntity:
        qr = self._repo.get_by_id(qr_id)
        if not qr:
            raise ValidationError(f"QR-код з ID {qr_id} не знайдено в системі.")

        status_update = "SCANNED"
        if user_role == "LIBRARIAN":
            status_update = "VERIFIED_BY_STAFF"

        self._notify("SCAN", qr.id, f"Scanned by {user_role}. New temporary status: {status_update}")

        return qr

    def block_qr(self, qr_id: str, reason: str) -> None:
        qr = self._repo.get_by_id(qr_id)
        if not qr:
            raise ValidationError("Неможливо заблокувати неіснуючий код.")

        self._notify("BLOCKED", qr.id, f"Reason: {reason}")

    def _notify(self, event_type: str, qr_id, details: str) -> None:
        log = LogEntry(action=event_type, qr_id=qr_id, details=details)
        for observer in self._observers:
            observer.update(event_type, log)

    def set_strategy(self, strategy: IQRStrategy) -> None:
        self._strategy = strategy