from fastapi import Depends, HTTPException, status, Request
from models.user import User
from auth.dependencies import get_current_user


def get_current_user_api(
    request: Request,
) -> User:
    """
    Dependencia estricta para APIs.
    - Devuelve User si está autenticado
    - Lanza 401 si no lo está
    """
    user = get_current_user(request)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return user
