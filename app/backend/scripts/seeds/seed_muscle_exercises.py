# Fuerza carga de modelos
import models.user
import models.training_day
import models.cardio_session
import models.strength_session
import models.strength_session_muscle
import models.muscle_group
import models.muscle_exercise
import models.performed_exercise
import models.set

from db.database import SessionLocal
from models.muscle_group import MuscleGroup
from models.muscle_exercise import MuscleExercise


EXERCISES = {
    "Pectoral": [
        "Press banca con mancuerna",
        "Press banca inclinada con mancuerna",
        "Press banca",
        "Press banca inclinada",
        "Press banca en Smith",
        "Press banca inclinada en Smith",
        "Apertura polea media",
        "Apertura polea alta",
        "Apertura polea baja",
        "Aperturas media maquina",
        "Aperturas alta maquina",
        "Aperturas baja maquina",
    ],
    "Espalda": [
        "Jalon abierto al pecho",
        "Jalon medio al pecho",
        "Jalon cerrado al pecho agarre supino",
        "Jalon cerrado al pecho agarre prono",
        "Remo abierto al pecho",
        "Remo medio al pecho",
        "Remo cerrado al pecho agarre supino",
        "Remo cerrado al pecho agarre prono",
        "Remo en T",
        "Remo alto en maquina",
    ],
    "Hombro": [
        "Press militar en Smith",
        "Press militar con mancuerna",
        "Press militar en maquina",
        "Elevaciones laterales en polea",
        "Elevaciones laterales con mancuerna",
        "Elevaciones laterales en maquina",
        "Elevaciones frontales en polea",
        "Elevaciones frontales con mancuerna",
        "Elevaciones posteriores en polea",
        "Elevaciones posteriores con mancuerna",
        "Elevaciones posteriores en maquina",
    ],
    "Biceps": [
        "Curl de biceps en pronacion en polea",
        "Curl de biceps en supinacion en polea",
        "Curl de biceps en martillo en polea",
        "Curl de biceps Bayesiano",
        "Curl de biceps en pronacion con mancuerna",
        "Curl de biceps en supinacion con mancuerna",
        "Curl de biceps en martillo con mancuerna",
    ],
    "Triceps": [
        "Extension en polea con cuerda",
        "Extension en polea con barra",
        "Extension en polea a una mano",
        "Extension en polea cruzada",
        "Extension en polea tipo katana",
        "Extension en polea frontal",
        "Extension con mancuerna tipo katana",
        "Extension con mancuerna frontal",
        "Press Frances",
    ],
    "Gluteo": [
        "Hip Thrust",
        "Patada a una pierna",
    ],
    "Cuadriceps": [
        "Sentadilla libre",
        "Sentadilla en Smith",
        "Jaca",
        "Prensa",
        "Extensiones en maquina",
    ],
    "Femoral": [
        "Peso muerto libre",
        "Peso muerto en maquina",
        "Curl de femoral en maquina de pie",
        "Curl de femoral en maquina sentado",
        "Curl de femoral en maquina tumbado",
        "Peso muerto rumano con mancuerna",
    ],
    "Abdomen": [
        "Crunches",
        "Plancha",
        "Giro ruso",
    ],
    "Gemelo": [
        "Elevacion de talon sentado",
        "Elevacion de talon en maquina tipo burro",
        "Elevacion de talon en maquina",
        "Elevacion de talon en Smith",
    ],
    "Antebrazo": [
        "Curl de antebrazo",
        "Rodillo de muñeca en pronacion",
        "Rodillo de muñeca en supinacion",
    ],
}


def run():
    db = SessionLocal()

    for group_name, exercises in EXERCISES.items():
        group = db.query(MuscleGroup).filter_by(name=group_name).first()
        if not group:
            print(f"Grupo no encontrado: {group_name}")
            continue

        for exercise_name in exercises:
            exists = (
                db.query(MuscleExercise)
                .filter_by(
                    muscle_group_id=group.id,
                    name=exercise_name,
                )
                .first()
            )
            if not exists:
                db.add(
                    MuscleExercise(
                        muscle_group_id=group.id,
                        name=exercise_name,
                    )
                )

    db.commit()
    db.close()
    print("Muscle exercises seeded successfully")


if __name__ == "__main__":
    run()
