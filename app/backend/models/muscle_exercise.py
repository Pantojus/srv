from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class MuscleExercise(Base):
    __tablename__ = "muscle_exercise"

    id = Column(Integer, primary_key=True, index=True)

    muscle_group_id = Column(
        Integer,
        ForeignKey("muscle_group.id"),
        nullable=False,
    )

    name = Column(String, nullable=False)

    muscle_group = relationship(
        "MuscleGroup",
        back_populates="exercises",
    )

    performed_exercises = relationship(
        "PerformedExercise",
        back_populates="muscle_exercise",
    )
