import pytest
import logging

from src.core.exception import HTTPException


@pytest.mark.asyncio
async def test_http_exception_logging(caplog) -> None:
    with (
        caplog.at_level(logging.DEBUG),
        pytest.raises(HTTPException),
    ):
        raise HTTPException(
            status_code=404,
            detail="Test message",
            logger_name="test_logger",
            logger_lvl=logging.DEBUG,
        )

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "DEBUG"
    assert caplog.records[0].message == "HTTP 404 - Test message"

