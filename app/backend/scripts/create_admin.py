from db.database import SessionLocal
from models.user import User
from security import hash_password


def create_admin():
    db = SessionLocal()

    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        print("Admin user already exists")
        return

    admin = User(
        username="admin",
        hashed_password=hash_password("admin123"),
        role="admin",
        is_active=True,
    )

    db.add(admin)
    db.commit()
    db.close()

    print("Admin user created successfully")


if __name__ == "__main__":
    create_admin()
