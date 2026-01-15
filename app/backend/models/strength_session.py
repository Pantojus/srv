from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class StrengthSession(Base):
    __tablename__ = "strength_session"

    id = Column(Integer, primary_key=True, index=True)

    training_day_id = Column(
        Integer,
        ForeignKey("training_day.id", ondelete="CASCADE"),
        nullable=False,
    )

    order_index = Column(Integer, nullable=False, default=0)

    training_day = relationship(
        "TrainingDay",
        back_populates="strength_sessions",
    )

    muscles = relationship(
        "StrengthSessionMuscle",
        back_populates="strength_session",
        cascade="all, delete-orphan",
    )
