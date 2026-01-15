from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.health.router import router as health_api_router
from api.health.views import router as health_ui_router
from api.health.auth import router as health_auth_router
from api.health.activity import router as health_activity_router


app = FastAPI(title="SRV Backend")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(health_api_router)
app.include_router(health_ui_router)
app.include_router(health_auth_router)
app.include_router(health_activity_router)
