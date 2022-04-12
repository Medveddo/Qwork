import app.models as models
from app.database import SessionLocal

db = SessionLocal()

result = db.query(models.Patient).first()

runs = db.query(models.Run).filter(models.Run.patient_id == result.id).all()

run: models.Run
for run in runs:
    print(run.text)


# text_process = models.TextProcessResult(
#     text="Привет, World!",
#     is_corresponding=False,
#     patient_id=1,
# )

# db.add(text_process)
# db.commit()

db.close()
