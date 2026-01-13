from fastapi import FastAPI
from api.health.router import router as health_api_router
from api.health.views import router as health_ui_router

app = FastAPI(title="SRV Backend")

app.include_router(health_api_router)
app.include_router(health_ui_router)
