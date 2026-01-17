from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from db.database import Base


class TrainingSession(Base):
    __tablename__ = "training_session"

    id = Column(Integer, primary_key=True, index=True)

    # Relación con el día
    training_day_id = Column(
        Integer,
        ForeignKey("training_day.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Tipo de sesión: FORCE / CARDIO (futuro)
    session_type = Column(String, nullable=False)

    # Orden dentro del día (1, 2, 3…)
    order_index = Column(Integer, nullable=False)

    # Relación
    training_day = relationship(
        "TrainingDay",
        back_populates="sessions",
    )

    performed_exercises = relationship(
        "PerformedExercise",
        back_populates="training_session",
        cascade="all, delete-orphan",
    )
