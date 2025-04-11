import pytest
import unittest.mock

import os
import azure.cosmos.aio
import azure.cosmos.exceptions


@pytest.fixture(autouse=True)
def mock_environ(monkeypatch) -> None:
    with unittest.mock.patch.dict(os.environ, clear=True):
        env = {
            "AZURE_CLIENT_ID": "00000000-0000-0000-0000-000000000000",
            "AZURE_TENANT_ID": "00000000-0000-0000-0000-000000000000",
            "AZURE_SUBSCRIPTION_ID": "00000000-0000-0000-0000-000000000000",
            "COSMOS_URL": "https://test.documents.azure.com:443/",
            "COSMOS_DB": "test",
        }
        for key, value in env.items():
            monkeypatch.setenv(key, value)
        yield


@pytest.fixture(autouse=True, scope="session")
def mock_azure_monitor() -> None:
    with unittest.mock.patch("azure.monitor.opentelemetry.configure_azure_monitor"):
        yield


@pytest.fixture(autouse=True, scope="session")
def mock_cosmos() -> azure.cosmos.aio.DatabaseProxy:
    async def _list_containers():
        yield {"id": "container"}

    with (
        unittest.mock.patch("azure.identity.aio.WorkloadIdentityCredential"),
        unittest.mock.patch("azure.cosmos.aio.CosmosClient") as mock_client,
    ):
        mock_db = unittest.mock.AsyncMock(spec=azure.cosmos.aio.DatabaseProxy)
        mock_container = unittest.mock.AsyncMock(spec=azure.cosmos.aio.ContainerProxy)

        mock_container.id = "container"
        mock_container.create_item.side_effect = lambda body, *args, **kwargs: {**body, "id": body.get("id", "auto-id")}

        mock_db.list_containers = _list_containers
        mock_db.get_container_client.side_effect = lambda name: mock_container if name == "container" else None

        mock_client.return_value = mock_client
        mock_client.get_database_client.return_value = mock_db

        yield mock_db

