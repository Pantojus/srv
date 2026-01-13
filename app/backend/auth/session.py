from itsdangerous import URLSafeSerializer

SECRET_KEY = "CHANGE_ME_LATER"
SESSION_COOKIE = "session"

serializer = URLSafeSerializer(SECRET_KEY, salt="session")


def create_session(data: dict) -> str:
    return serializer.dumps(data)


def read_session(token: str) -> dict | None:
    try:
        return serializer.loads(token)
    except Exception:
        return None
