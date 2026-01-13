from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from db.database import SessionLocal
from models.user import User
from security import verify_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/health/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "health/login.html",
            {"request": request, "error": "Usuario o contraseña incorrectos"},
        )

    response = RedirectResponse(url="/health/dashboard", status_code=302)
    response.set_cookie(key="user", value=user.username)
    return response
