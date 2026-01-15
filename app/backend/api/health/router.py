from fastapi import APIRouter

from api.health.api_exercise import router as exercise_api_router


router = APIRouter(
    prefix="/health/api",
    tags=["health-api"],
)

@router.get("/")
def health_api_root():
    return {"status": "ok", "service": "health"}

# Subrouters
router.include_router(exercise_api_router)
