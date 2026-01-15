from sqlalchemy import Column, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from db.database import Base


class SetType(enum.Enum):
    WARMUP = "WARMUP"
    EFFECTIVE = "EFFECTIVE"


class Set(Base):
    __tablename__ = "set"

    id = Column(Integer, primary_key=True, index=True)

    performed_exercise_id = Column(
        Integer,
        ForeignKey("performed_exercise.id", ondelete="CASCADE"),
        nullable=False,
    )

    set_type = Column(Enum(SetType), nullable=False)
    repetitions = Column(Integer, nullable=False)
    weight_kg = Column(Float, nullable=False)
    order_index = Column(Integer, nullable=False, default=0)
    performed_exercise = relationship(
        "PerformedExercise",
        back_populates="sets",
    )
