import cv2
from pyzbar.pyzbar import decode
from src.services.qr_service import QRService
from src.storage.in_memory_repo import InMemoryQRRepository
from src.services.strategies import StandardPNGStrategy


def run_real_camera_scanner(service: QRService):
    cap = cv2.VideoCapture(0)
    print("Камера запущена. Наведіть на QR-код (Натисніть 'q' для виходу)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detected_codes = decode(frame)
        for code in detected_codes:
            qr_data = code.data.decode('utf-8')
            print(f"\n[ЗНАЙДЕНО QR]: {qr_data}")

            service._notify("CAMERA_SCAN", "REAL_TIME", f"Content: {qr_data}")

            (x, y, w, h) = code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "SCANNED", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('QR Scanner Terminal', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    repo = InMemoryQRRepository()
    service = QRService(repo, StandardPNGStrategy())
    run_real_camera_scanner(service)