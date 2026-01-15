import models

from db.database import SessionLocal
from models.muscle_group import MuscleGroup


MUSCLE_GROUPS = [
    "Pectoral",
    "Espalda",
    "Hombro",
    "Biceps",
    "Triceps",
    "Gluteo",
    "Cuadriceps",
    "Femoral",
    "Abdomen",
    "Gemelo",
    "Antebrazo",
]


def run():
    db = SessionLocal()

    for name in MUSCLE_GROUPS:
        exists = db.query(MuscleGroup).filter_by(name=name).first()
        if not exists:
            db.add(MuscleGroup(name=name))

    db.commit()
    db.close()
    print("Muscle groups seeded successfully")


if __name__ == "__main__":
    run()
