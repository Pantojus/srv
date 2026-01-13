from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class PerformedExercise(Base):
    __tablename__ = "performed_exercise"

    id = Column(Integer, primary_key=True, index=True)

    strength_session_muscle_id = Column(
        Integer,
        ForeignKey("strength_session_muscle.id", ondelete="CASCADE"),
        nullable=False,
    )

    muscle_exercise_id = Column(
        Integer,
        ForeignKey("muscle_exercise.id"),
        nullable=False,
    )

    order_index = Column(Integer, nullable=False, default=0)

    strength_session_muscle = relationship(
        "StrengthSessionMuscle",
        back_populates="performed_exercises",
    )

    muscle_exercise = relationship(
        "MuscleExercise",
        back_populates="performed_exercises",
    )

    sets = relationship(
        "Set",
        back_populates="performed_exercise",
        cascade="all, delete-orphan",
    )
