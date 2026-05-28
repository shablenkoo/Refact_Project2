import re
from src.core.exceptions import ValidationError

class QRDataValidator:
    @staticmethod
    def validate_content(content: str):
        if not content:
            raise ValidationError("Контент не може бути порожнім")
        if len(content) > 1000:
            raise ValidationError("Контент занадто довгий")

    @staticmethod
    def is_valid_url(url: str) -> bool:
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    @staticmethod
    def validate_type(qr_type: str):
        # Оновлений список: додали MANUAL та CAMERA_SCAN
        allowed_types = ["URL", "TEXT", "WIFI", "BOOK", "MANUAL", "CAMERA_SCAN"]
        if qr_type not in allowed_types:
            raise ValidationError(f"Тип {qr_type} не підтримується системою")

    @staticmethod
    def validate_type(qr_type: str):
        # Додаємо FILE_SCAN
        allowed_types = ["URL", "TEXT", "WIFI", "BOOK", "MANUAL", "CAMERA_SCAN", "FILE_SCAN"]
        if qr_type not in allowed_types:
            raise ValidationError(f"Тип {qr_type} не підтримується системою")