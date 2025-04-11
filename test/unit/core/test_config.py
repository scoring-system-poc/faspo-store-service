import pytest


@pytest.mark.asyncio
async def test_config(mock_environ) -> None:
    from src.core.config import CONFIG

    assert CONFIG.AZURE_CLIENT_ID == "00000000-0000-0000-0000-000000000000"
    assert CONFIG.AZURE_TENANT_ID == "00000000-0000-0000-0000-000000000000"
    assert CONFIG.AZURE_FEDERATED_TOKEN_FILE == "/var/run/secrets/azure/tokens/azure-identity-token"
    assert CONFIG.COSMOS_URL == "https://test.documents.azure.com:443/"
    assert CONFIG.COSMOS_DB == "test"
    assert CONFIG.COSMOS_RETRY_COUNT == 3
    assert CONFIG.LOG_LEVEL == "INFO"

