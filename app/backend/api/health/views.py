from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/health", tags=["health"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "health/login.html",
        {"request": request}
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = request.cookies.get("user")
    if not user:
        return templates.TemplateResponse(
            "health/login.html",
            {"request": request, "error": "Debes iniciar sesión"}
        )

    return templates.TemplateResponse(
        "health/dashboard.html",
        {"request": request, "user": user}
    )
