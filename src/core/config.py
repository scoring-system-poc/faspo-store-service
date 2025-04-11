import pydantic
import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    """
    Environment configuration for the application.
    """
    # Azure
    AZURE_CLIENT_ID: str
    AZURE_TENANT_ID: str
    AZURE_FEDERATED_TOKEN_FILE: str = "/var/run/secrets/azure/tokens/azure-identity-token"

    # CosmosDB
    COSMOS_URL: str
    COSMOS_DB: str
    COSMOS_RETRY_COUNT: int = 3

    # General
    LOG_LEVEL: pydantic.constr(to_upper=True) = "INFO"


CONFIG = Config()
