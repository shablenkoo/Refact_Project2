import cv2
from pyzbar.pyzbar import decode
import os
import sys
import base64

# Додаємо шлях до кореня
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage.in_memory_repo import InMemoryQRRepository
from src.services.strategies import StandardPNGStrategy
from src.services.observers import HistoryLogger, AnalyticsEngine
from src.services.qr_service import QRService


def scan_from_file(service: QRService, file_path: str):
    """Метод для сканування QR-коду прямо з файлу зображення"""
    if not os.path.exists(file_path):
        print(f"[ПОМИЛКА] Файл {file_path} не знайдено!")
        return

    # Читаємо зображення через OpenCV
    img = cv2.imread(file_path)
    if img is None:
        print("[ПОМИЛКА] Не вдалося відкрити зображення.")
        return

    # Декодуємо QR
    detected_codes = decode(img)

    if not detected_codes:
        print("[УВАГА] На зображенні не знайдено QR-кодів.")
        return

    for code in detected_codes:
        qr_data = code.data.decode('utf-8')
        print(f"\n[УСПІХ] З файлу зчитано: {qr_data}")

        # Реєструємо подію в системі
        service._notify("FILE_SCAN", "DIGITAL", f"Content from file: {qr_data}")


def main_menu():
    repo = InMemoryQRRepository()
    service = QRService(repo, StandardPNGStrategy())
    history = HistoryLogger()
    analytics = AnalyticsEngine()

    service.attach(history)
    service.attach(analytics)

    while True:
        print("\n=== QR SERVICE CONTROL PANEL ===")
        print("1. Згенерувати QR (Зберегти у файл)")
        print("2. СКАНУВАТИ З ФАЙЛА (last_generated_qr.png)")
        print("4. Переглянути історію")
        print("5. Вихід")

        choice = input("\nОберіть дію: ")

        if choice == '1':
            content = input("Введіть дані для QR: ")
            image_base64 = service.create_qr(content, qr_type="MANUAL")

            # Збереження
            with open("../last_generated_qr.png", "wb") as fh:
                fh.write(base64.b64decode(image_base64))
            print("[OK] QR збережено в 'last_generated_qr.png'")

        elif choice == '2':
            # Скануємо створений файл
            scan_from_file(service, "../last_generated_qr.png")

        elif choice == '3':
            # Код для камери (залишаємо як опцію)
            from src.main import start_camera_scanner  # якщо винесли в окрему функцію
            start_camera_scanner(service)

        elif choice == '4':
            print("\n--- ІСТОРІЯ ПОДІЙ ---")
            for log in history.logs:
                print(f"[{log.timestamp.strftime('%H:%M:%S')}] {log.action}: {log.details}")

        elif choice == '5':
            break


if __name__ == "__main__":
    main_menu()