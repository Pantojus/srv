from fastapi import APIRouter

router = APIRouter(
    prefix="/health/api",
    tags=["health-api"]
)

@router.get("/")
def health_api_root():
    return {"status": "ok", "service": "health"}
