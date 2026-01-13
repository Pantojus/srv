from fastapi import Request
from db.database import SessionLocal
from models.user import User
from auth.session import read_session, SESSION_COOKIE


def get_current_user(request: Request) -> User | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None

    data = read_session(token)
    if not data or "user_id" not in data:
        return None

    db = SessionLocal()
    user = db.query(User).filter(User.id == data["user_id"]).first()
    db.close()

    return user
