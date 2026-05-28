import pytest
from src.core.exceptions import ValidationError


@pytest.mark.parametrize("invalid", ["", None, "A" * 1001])
def test_validation_errors(service, invalid):
    with pytest.raises(ValidationError):
        service.create_qr(invalid)


def test_scan_logic(service):
    service.create_qr("Scan Me")
    qr_id = service._repo.get_all()[0].id

    qr = service.scan_qr(qr_id, user_role="READER")
    assert qr.content == "Scan Me"

    with pytest.raises(ValidationError):
        service.scan_qr("wrong-uuid")


def test_block_qr_logic(service, logger):
    service.attach(logger)
    service.create_qr("Block Me")
    qr_id = service._repo.get_all()[0].id

    service.block_qr(qr_id, reason="Lost")
    assert logger.logs[-1].action == "BLOCKED"

def test_file_scan_logging(service, logger):
    service.attach(logger)
    service._notify("FILE_SCAN", "DIGITAL", "Content: test_file")
    assert logger.logs[-1].action == "FILE_SCAN"
    assert "test_file" in logger.logs[-1].details

def test_validate_new_types():
    from src.utils.validators import QRDataValidator
    QRDataValidator.validate_type("FILE_SCAN")
    QRDataValidator.validate_type("CAMERA_SCAN")
    QRDataValidator.validate_type("MANUAL")