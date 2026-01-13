from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)

    training_days = relationship(
        "TrainingDay",
        back_populates="user",
        cascade="all, delete-orphan",
    )
