from loguru import logger
from sqlalchemy.orm import Session

from . import models, schemas


def get_history(db: Session):
    logger.info("Fetching all results from db")
    results: list[models.Run] = db.query(models.Run).all()
    logger.info(f"{results=}")
    return [
        schemas.Run(
            text=result.text,
            is_corresponding=result.is_corresponding,
            temperature=result.temperature,
            systole_pressure=result.systole_pressure,
            diastole_pressure=result.diastole_pressure,
        )
        for result in results
    ]


def create_text_process_result(db: Session, result: schemas.Run) -> models.Run:
    db_result = models.Run(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def create_patient(db: Session, patient: schemas.Patient) -> models.Patient:
    dict_patient = patient.dict()
    dict_patient.pop("id_")
    db_patient = models.Patient(**dict_patient)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient
