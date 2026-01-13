from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class StrengthSessionMuscle(Base):
    __tablename__ = "strength_session_muscle"

    id = Column(Integer, primary_key=True, index=True)

    strength_session_id = Column(
        Integer,
        ForeignKey("strength_session.id", ondelete="CASCADE"),
        nullable=False,
    )

    muscle_group_id = Column(
        Integer,
        ForeignKey("muscle_group.id"),
        nullable=False,
    )

    order_index = Column(Integer, nullable=False, default=0)

    strength_session = relationship(
        "StrengthSession",
        back_populates="muscles",
    )

    muscle_group = relationship(
        "MuscleGroup",
        back_populates="session_muscles",
    )

    performed_exercises = relationship(
        "PerformedExercise",
        back_populates="strength_session_muscle",
        cascade="all, delete-orphan",
    )
