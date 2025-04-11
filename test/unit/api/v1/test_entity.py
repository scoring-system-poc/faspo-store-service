import unittest.mock
import pytest
import httpx

from src.core.exception import HTTPException


@pytest.mark.asyncio
async def test_entity_save_item__success(async_client: httpx.AsyncClient) -> None:
    with unittest.mock.patch(
        "src.api.v1.entity.save_item",
        return_value="dummy-id",
    ) as mock_save_item:
        response = await async_client.post("/api/v1/container", json={"key": "value"})

        mock_save_item.assert_awaited_with(container_name="container", item={"key": "value"})
        assert response.status_code == 201
        assert response.json() == {"id": "dummy-id"}


@pytest.mark.asyncio
async def test_entity_save_item__failure(async_client: httpx.AsyncClient) -> None:
    with unittest.mock.patch(
        "src.api.v1.entity.save_item",
        side_effect=HTTPException(503),
    ):
        response = await async_client.post("/api/v1/container", json={"key": "value"})

        assert response.status_code == 503
        assert response.json() == {"detail": "Service Unavailable"}

