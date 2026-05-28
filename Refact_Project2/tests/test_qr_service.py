import pytest

@pytest.mark.parametrize("i", range(100))
def test_create_qr_bulk_success(service, i):
    content = f"https://example.com/item_{i}"
    result = service.create_qr(content, qr_type="URL")
    assert len(result) > 0
    assert len(service._repo.get_all()) == 1

@pytest.mark.parametrize("i", range(100))
def test_observer_bulk_notifications(service, logger, i):
    service.attach(logger)
    service.create_qr(f"bulk_data_{i}")
    assert len(logger.logs) == 1
    assert logger.logs[0].action == "CREATED"