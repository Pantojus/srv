from sqlalchemy import Column, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from db.database import Base


class TrainingDay(Base):
    __tablename__ = "training_day"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_training_day_user_date"),
    )

    # Relaciones
    user = relationship("User", back_populates="training_days")
    cardio_sessions = relationship(
        "CardioSession",
        back_populates="training_day",
        cascade="all, delete-orphan",
    )
    strength_sessions = relationship(
        "StrengthSession",
        back_populates="training_day",
        cascade="all, delete-orphan",
    )

