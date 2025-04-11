import pytest
import httpx


@pytest.fixture
async def async_client(mock_environ, mock_cosmos) -> httpx.AsyncClient:
    from main import app

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
