# scripts/dev/clear_today_training.py

from datetime import date
from db.database import SessionLocal
from models.training_day import TrainingDay

def run():
    db = SessionLocal()
    today = date.today()

    td = db.query(TrainingDay).filter(TrainingDay.date == today).first()

    if not td:
        print("ℹ️ No hay TrainingDay para hoy")
        return

    db.delete(td)
    db.commit()

    print("🧹 TrainingDay de hoy eliminado completamente")

if __name__ == "__main__":
    run()
