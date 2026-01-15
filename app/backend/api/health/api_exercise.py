from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from db.database import get_db
from auth.dependencies import get_current_user

from models.user import User
from models.performed_exercise import PerformedExercise
from models.muscle_exercise import MuscleExercise
from models.set import SetType


router = APIRouter(
    prefix="/exercise",
    tags=["Health - Exercise API"],
)


@router.get("/{performed_exercise_id}")
def get_exercise_detail(
    performed_exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve el detalle completo de un ejercicio realizado,
    incluyendo series de calentamiento y series efectivas.
    """

    pe = (
        db.query(PerformedExercise)
        .options(
            joinedload(PerformedExercise.muscle_exercise)
                .joinedload(MuscleExercise.muscle_group),
            joinedload(PerformedExercise.sets),
        )
        .filter(PerformedExercise.id == performed_exercise_id)
        .first()
    )

    if not pe:
        raise HTTPException(status_code=404, detail="Exercise not found")

    warmup_sets = []
    effective_sets = []

    for s in sorted(pe.sets, key=lambda x: x.order_index):
        item = {
            "order": s.order_index,
            "reps": s.repetitions,
            "weight": s.weight_kg,
        }

        if s.set_type == SetType.WARMUP:
            warmup_sets.append(item)
        elif s.set_type == SetType.EFFECTIVE:
            effective_sets.append(item)

    return {
        "id": pe.id,
        "muscle_group": pe.muscle_exercise.muscle_group.name,
        "exercise": pe.muscle_exercise.name,
        "warmup_sets": warmup_sets,
        "effective_sets": effective_sets,
    }
