from loguru import logger
from sqlalchemy.orm import Session

from . import models, schemas


def get_history(db: Session):
    logger.info("Fetching all results from db")
    results: list[models.TextProcessResult] = db.query(
        models.TextProcessResult
    ).all()
    logger.info(f"{results=}")
    return [
        schemas.TextProcessResult(
            text=result.text,
            is_corresponding=result.is_corresponding,
            temperature=result.temperature,
            systole_pressure=result.systole_pressure,
            diastole_pressure=result.diastole_pressure,
        )
        for result in results
    ]


def create_text_process_result(db: Session, result: schemas.TextProcessResult):
    db_result = models.TextProcessResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
