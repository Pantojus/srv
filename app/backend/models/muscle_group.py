from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class MuscleGroup(Base):
    __tablename__ = "muscle_group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    session_muscles = relationship(
        "StrengthSessionMuscle",
        back_populates="muscle_group",
    )

    exercises = relationship(
        "MuscleExercise",
        back_populates="muscle_group",
    )
