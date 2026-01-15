from datetime import date
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from db.database import get_db
from auth.dependencies import get_current_user

from models.user import User
from models.training_day import TrainingDay
from models.strength_session import StrengthSession
from models.strength_session_muscle import StrengthSessionMuscle
from models.performed_exercise import PerformedExercise


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
        return {
            "date": today,
            "message": "No training planned for today",
            "cardio": [],
            "strength": [],
        }

    # -------------------
    # Cardio
    # -------------------
    cardio = [
        {
            "type": s.cardio_type,
            "duration_minutes": s.duration_minutes,
            "distance": s.distance,
            "speed": s.speed,
        }
        for s in training_day.cardio_sessions
    ]

    # -------------------
    # Strength (agrupado por grupo muscular)
    # -------------------
    strength_groups = defaultdict(list)

    for strength_session in training_day.strength_sessions:
        for sm in strength_session.muscles:
            for pe in sm.performed_exercises:
                strength_groups[sm.muscle_group.name].append(
                    pe.muscle_exercise.name
                )

    strength = [
        {
            "group": group,
            "exercises": exercises,
        }
        for group, exercises in strength_groups.items()
    ]

    return {
        "date": training_day.date,
        "cardio": cardio,
        "strength": strength,
    }
