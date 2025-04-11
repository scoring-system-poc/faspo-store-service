import typing
import fastapi

from src.service.processor import save_item


router = fastapi.APIRouter(
    tags=["entity"]
)


@router.post("/{container}")
async def create_item(
    container: str,
    item: dict,
    correlation_id: typing.Annotated[str | None, fastapi.Header()] = None,
) -> fastapi.responses.JSONResponse:
    """
    Create an item in the specified container.
    :param container: The name of the container.
    :param item: The item to create.
    :param correlation_id: Optional correlation ID for tracing.
    :return: str
    """
    item_id = await save_item(container_name=container, item=item)
    return fastapi.responses.JSONResponse(status_code=201, content={"id": item_id})

