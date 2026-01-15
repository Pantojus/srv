from datetime import date
from collections import defaultdict
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from db.database import get_db
from auth.dependencies import get_current_user

from models.user import User
from models.training_day import TrainingDay
from models.strength_session import StrengthSession
from models.strength_session_muscle import StrengthSessionMuscle
from models.performed_exercise import PerformedExercise


logger = logging.getLogger("app")

router = APIRouter(
    prefix="/health/activity",
    tags=["Health - Activity"],
)


@router.get("/today")
def get_today_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    logger.info(
        f"📅 get_today_activity | user_id={current_user.id} | date={today}"
    )

    training_day = (
        db.query(TrainingDay)
        .filter(
            TrainingDay.user_id == current_user.id,
            TrainingDay.date == today,
        )
        .options(
            joinedload(TrainingDay.cardio_sessions),
            joinedload(TrainingDay.strength_sessions)
            .joinedload(StrengthSession.muscles)
            .joinedload(StrengthSessionMuscle.muscle_group),
            joinedload(TrainingDay.strength_sessions)
            .joinedload(StrengthSession.muscles)
            .joinedload(StrengthSessionMuscle.performed_exercises)
            .joinedload(PerformedExercise.muscle_exercise),
        )
        .first()
    )

    if not training_day:
        logger.warning(
            f"⚠️ No TrainingDay found | user_id={current_user.id} | date={today}"
        )
        return {
            "date": today,
            "message": "No training planned for today",
            "cardio": [],
            "strength": [],
        }

    logger.info(
        f"✅ TrainingDay found | "
        f"cardio_sessions={len(training_day.cardio_sessions)} | "
        f"strength_sessions={len(training_day.strength_sessions)}"
    )

    # -------------------
    # Cardio
    # -------------------
    cardio = []
    for s in training_day.cardio_sessions:
        cardio.append(
            {
                "type": s.cardio_type,
                "duration_minutes": s.duration_minutes,
                "distance": s.distance,
                "speed": s.speed,
            }
        )

    logger.info(f"🏃 Cardio sessions processed: {len(cardio)}")

    # -------------------
    # Strength
    # -------------------
    strength_groups = defaultdict(list)
    total_exercises = 0

    for strength_session in training_day.strength_sessions:
        logger.info(
            f"🏋️ StrengthSession id={strength_session.id} "
            f"muscles={len(strength_session.muscles)}"
        )

        for sm in strength_session.muscles:
            logger.info(
                f"💪 MuscleGroup={sm.muscle_group.name} | "
                f"performed_exercises={len(sm.performed_exercises)}"
            )

            for pe in sm.performed_exercises:
                strength_groups[sm.muscle_group.name].append(
                    {
                        "id": pe.id,
                        "name": pe.muscle_exercise.name,
                    }
                )
                total_exercises += 1

    strength = [
        {
            "group": group,
            "exercises": exercises,
        }
        for group, exercises in strength_groups.items()
    ]

    logger.info(
        f"📦 Strength result | groups={len(strength)} | "
        f"total_exercises={total_exercises}"
    )

    return {
        "date": training_day.date,
        "cardio": cardio,
        "strength": strength,
    }
