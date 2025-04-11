import fastapi

from .probe import router as probe_router
from .entity import router as entity_router


router = fastapi.APIRouter(
    prefix="/api/v1",
)

router.include_router(probe_router)
router.include_router(entity_router)
