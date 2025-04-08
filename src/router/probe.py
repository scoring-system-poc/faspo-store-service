import fastapi


router = fastapi.APIRouter()


@router.get("/alive")
async def alive():
    return "alive"


@router.get("/ready")
async def ready():
    return "ready"
