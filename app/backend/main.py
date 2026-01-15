from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import time

from logging_config import setup_logging

from api.health.router import router as health_api_router
from api.health.views import router as health_ui_router
from api.health.auth import router as health_auth_router
from api.health.activity import router as health_activity_router


# 🔹 Inicializamos logging
logger = setup_logging()

app = FastAPI(title="SRV Backend")

# 🔹 Middleware de logging (NO TOCA LÓGICA)
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            f"🔥 ERROR 500 | {request.method} {request.url.path}"
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

    duration = (time.time() - start_time) * 1000

    logger.info(
        f"{request.method} {request.url.path} "
        f"| {response.status_code} "
        f"| {duration:.2f} ms"
    )

    return response


# 🔹 Static (igual que antes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔹 Routers (idénticos a los tuyos)
app.include_router(health_api_router)
app.include_router(health_ui_router)
app.include_router(health_auth_router)
app.include_router(health_activity_router)

logger.info("🚀 SRV Backend arrancado correctamente")
