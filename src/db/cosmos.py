import azure.cosmos.aio
import azure.identity.aio

from src.core.config import CONFIG
from src.core.exception import HTTPException


client = azure.cosmos.aio.CosmosClient(
    url=CONFIG.COSMOS_URL,
    credential=azure.identity.aio.WorkloadIdentityCredential(
        tenant_id=CONFIG.AZURE_TENANT_ID,
        client_id=CONFIG.AZURE_CLIENT_ID,
        token_file_path=CONFIG.AZURE_FEDERATED_TOKEN_FILE,
    ),
)

db = client.get_database_client(
    database=CONFIG.COSMOS_DB,
)

containers = {

}


async def get_container(container_name: str) -> azure.cosmos.aio.ContainerProxy:
    """
    Get a container proxy by name.
    If the container is not already cached, it will be retrieved from the database.
    If the container is not found in the database, a fastapi HTTPException will be raised.
    :param container_name: The name of the container to retrieve.
    :return: The container client.
    :raises HTTPException: If the container is not found in the database.
    """
    if container_name not in containers:
        if container_name not in [container["id"] async for container in db.list_containers()]:
            raise HTTPException(
                status_code=404,
                detail=f"Container '{container_name}' not found",
                logger_name=__name__,
            )

        containers[container_name] = db.get_container_client(container_name)

    return containers[container_name]

