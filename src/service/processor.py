import logging
import asyncio
import azure.cosmos.http_constants
import azure.cosmos.exceptions

from src.core.config import CONFIG
from src.core.exception import HTTPException
from src.db.cosmos import get_container


logger = logging.getLogger(__name__)


async def save_item(container_name: str, item: dict) -> str:
    """
    Save an item to the specified container in Cosmos DB.
    If this process fails it raises an HTTPException, which automatically returns HTTP response to the client.
    :param container_name: Name of the container to save the item in.
    :param item: JSON representation of the item to be saved.
    :return: ID of the saved item.
    :raises HTTPException: If the item cannot be saved after the specified number of retries.
    """
    for _ in range(CONFIG.COSMOS_RETRY_COUNT):
        try:
            container = await get_container(container_name)
            item = await container.create_item(body=item, enable_automatic_id_generation=True)

            logger.info(f"saved item: {item['id']}")

            return item["id"]

        except azure.cosmos.exceptions.CosmosHttpResponseError as e:
            if e.status_code not in [
                azure.cosmos.http_constants.StatusCodes.TOO_MANY_REQUESTS,
                azure.cosmos.http_constants.StatusCodes.RETRY_WITH
            ]:
                raise HTTPException(
                    status_code=e.status_code,
                    logger_name=__name__,
                    logger_msg=f"failed to save: item={item}; error={e.http_error_message};",
                )
            else:
                print("retry")
                await asyncio.sleep(
                    e.headers.get(azure.cosmos.http_constants.HttpHeaders.RetryAfterInMilliseconds, 10_000) / 1000
                )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                logger_name=__name__,
                logger_lvl=logging.ERROR,
                logger_msg=f"unexpected error occurred when saving item: {e}",
            )

    raise HTTPException(
        status_code=503,
        detail=f"failed to save item after {CONFIG.COSMOS_RETRY_COUNT} retries | item={item}",
        logger_name=__name__,
    )
