from sqlalchemy import Column, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from db.database import Base


class CardioType(enum.Enum):
    ANDAR = "ANDAR"
    CORRER = "CORRER"
    ANDAR_CINTA = "ANDAR_CINTA"
    CORRER_CINTA = "CORRER_CINTA"


class CardioSession(Base):
    __tablename__ = "cardio_session"

    id = Column(Integer, primary_key=True, index=True)
    training_day_id = Column(
        Integer,
        ForeignKey("training_day.id", ondelete="CASCADE"),
        nullable=False,
    )

    cardio_type = Column(Enum(CardioType), nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    distance_km = Column(Float, nullable=True)
    avg_speed_kmh = Column(Float, nullable=True)

    order_index = Column(Integer, nullable=False, default=0)

    training_day = relationship(
        "TrainingDay",
        back_populates="cardio_sessions",
    )
