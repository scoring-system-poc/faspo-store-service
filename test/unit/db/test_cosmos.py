import pytest
import unittest.mock
import azure.cosmos.aio

from src.core.exception import HTTPException


@pytest.mark.asyncio
async def test_get_container__cached():
    from src.db.cosmos import get_container, containers

    containers["cached"] = unittest.mock.AsyncMock(spec=azure.cosmos.aio.ContainerProxy)
    containers["cached"].id = "dummy-id"

    container = await get_container("cached")

    assert container is not None
    assert container.id == "dummy-id"


@pytest.mark.asyncio
async def test_get_container__new():
    from src.db.cosmos import get_container, containers

    containers.clear()

    container = await get_container("container")

    assert container is not None
    assert container.id == "container"


@pytest.mark.asyncio
async def test_get_container__missing():
    from src.db.cosmos import get_container, containers

    containers.clear()

    with pytest.raises(HTTPException):
        await get_container("missing")

