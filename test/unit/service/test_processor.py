import pytest
import unittest.mock
import azure.cosmos.exceptions
import azure.cosmos.http_constants

from src.core.exception import HTTPException


@pytest.fixture
def item() -> dict:
    return {"id": "test_id", "name": "test_name"}


@pytest.mark.asyncio
async def test_save_item__happy_path(item):
    from src.service.processor import save_item

    assert await save_item("container", item) == "test_id"


@pytest.mark.asyncio
async def test_save_item__missing_container(item):
    from src.service.processor import save_item

    with pytest.raises(HTTPException) as e:
        await save_item("missing", item)

    assert e.value.status_code == 404
    assert e.value.detail == "Container 'missing' not found"


@pytest.mark.asyncio
async def test_save_item__generic_error(mock_cosmos):
    mock_container = mock_cosmos.get_container_client("container")
    mock_container.create_item.side_effect = ValueError("generic error")

    from src.service.processor import save_item

    with pytest.raises(HTTPException) as e:
        await save_item("container", {})

    assert e.value.status_code == 500
    assert e.value.detail == "Internal Server Error"


@pytest.mark.asyncio
async def test_save_item__cosmos_error_critical(mock_cosmos):
    mock_container = mock_cosmos.get_container_client("container")
    mock_container.create_item.side_effect = azure.cosmos.exceptions.CosmosHttpResponseError(
        status_code=azure.cosmos.http_constants.StatusCodes.BAD_REQUEST,
        message="Bad Request",
    )

    from src.service.processor import save_item

    with pytest.raises(HTTPException) as e:
        await save_item("container", {})

    assert e.value.status_code == 400
    assert e.value.detail == "Bad Request"


@pytest.mark.asyncio
async def test_save_item__cosmos_error_retriable(mock_cosmos):
    mock_container = mock_cosmos.get_container_client("container")
    mock_container.create_item.side_effect = azure.cosmos.exceptions.CosmosHttpResponseError(
        status_code=azure.cosmos.http_constants.StatusCodes.TOO_MANY_REQUESTS,
        response=unittest.mock.MagicMock(
            headers={azure.cosmos.http_constants.HttpHeaders.RetryAfterInMilliseconds: 1000},
        ),
    )

    from src.service.processor import save_item
    from src.core.config import CONFIG

    with (
        unittest.mock.patch("asyncio.sleep") as mock_sleep,
        pytest.raises(HTTPException) as e,
    ):
        await save_item("container", {})

    assert mock_sleep.call_count == CONFIG.COSMOS_RETRY_COUNT
    assert e.value.status_code == 503
    assert e.value.detail == f"Failed to save item after {CONFIG.COSMOS_RETRY_COUNT} retries"
