from datetime import date

from db.database import SessionLocal
from models.user import User
from models.training_day import TrainingDay
from models.strength_session import StrengthSession
from models.strength_session_muscle import StrengthSessionMuscle
from models.muscle_group import MuscleGroup
from models.muscle_exercise import MuscleExercise
from models.performed_exercise import PerformedExercise


def run():
    db = SessionLocal()
    today = date.today()

    # 1️⃣ Usuario
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        print("❌ Usuario admin no encontrado")
        return

    # 2️⃣ TrainingDay
    training_day = (
        db.query(TrainingDay)
        .filter(
            TrainingDay.user_id == user.id,
            TrainingDay.date == today,
        )
        .first()
    )

    if not training_day:
        training_day = TrainingDay(
            user_id=user.id,
            date=today,
        )
        db.add(training_day)
        db.commit()
        db.refresh(training_day)

    # 3️⃣ ¿YA EXISTE FUERZA HOY?
    existing_strength = (
        db.query(StrengthSession)
        .filter(StrengthSession.training_day_id == training_day.id)
        .first()
    )

    if existing_strength:
        print("⚠️ Ya existe un entrenamiento de fuerza hoy. No se crea otro.")
        return

    # 4️⃣ Crear StrengthSession
    strength_session = StrengthSession(
        training_day_id=training_day.id,
        order_index=1,
    )
    db.add(strength_session)
    db.commit()
    db.refresh(strength_session)

    # === DEFINICIÓN DEL ENTRENAMIENTO ===
    workout_definition = {
        "Pectoral": [
            "Press banca con mancuerna",
            "Press banca inclinada con mancuerna",
        ],
        "Espalda": [
            "Jalon abierto al pecho",
            "Jalon medio al pecho",
        ],
    }

    # 5️⃣ Crear músculos + ejercicios
    for muscle_order, (muscle_name, exercises) in enumerate(workout_definition.items(), start=1):
        muscle_group = (
            db.query(MuscleGroup)
            .filter(MuscleGroup.name == muscle_name)
            .first()
        )

        if not muscle_group:
            print(f"❌ MuscleGroup '{muscle_name}' no existe")
            continue

        session_muscle = StrengthSessionMuscle(
            strength_session_id=strength_session.id,
            muscle_group_id=muscle_group.id,
            order_index=muscle_order,
        )
        db.add(session_muscle)
        db.commit()
        db.refresh(session_muscle)

        for exercise_order, exercise_name in enumerate(exercises, start=1):
            exercise = (
                db.query(MuscleExercise)
                .filter(MuscleExercise.name == exercise_name)
                .first()
            )

            if not exercise:
                print(f"❌ Ejercicio '{exercise_name}' no existe")
                continue

            performed = PerformedExercise(
                strength_session_muscle_id=session_muscle.id,
                muscle_exercise_id=exercise.id,
                order_index=exercise_order,
            )
            db.add(performed)

        db.commit()

    print("✅ Entrenamiento de fuerza de hoy creado correctamente")


if __name__ == "__main__":
    run()
