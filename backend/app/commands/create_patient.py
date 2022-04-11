from datetime import datetime
from app.schemas import Patient

from app.crud import create_patient

from app.database import SessionLocal


# patient = Patient(
#     id_=0,
#     full_name="Иванов Иван Иванович",
#     birthdate=datetime(year=2006, month=1, day=25)
# )

patient = Patient(
    id_=0,
    full_name="Пупонов Джуниор Голангович",
    birthdate=datetime(year=2001, month=1, day=31),
)


db = SessionLocal()

create_patient(db, patient)

db.close()
