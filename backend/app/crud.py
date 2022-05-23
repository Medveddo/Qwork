import json
from typing import List, Tuple

from loguru import logger
from sqlalchemy.orm import Session

from app.hashids import hashids_

from . import models, schemas


def get_history(db: Session, count: int = 10, offset: int = 0) -> List[schemas.Run]:
    logger.debug("Fetching all results from db")
    results: list[models.Run] = db.query(models.Run).order_by(models.Run.id.desc()).offset(offset).limit(count).all()
    logger.info(f"Got {len(results)} history runs")
    return [
        schemas.Run(
            text=result.text,
            is_corresponding=result.is_corresponding,
            temperature=result.temperature,
            systole_pressure=result.systole_pressure,
            diastole_pressure=result.diastole_pressure,
            type=result.type,
            finished=result.finished,
        )
        for result in results
    ]


def create_text_process_result(db: Session, result: schemas.Run) -> models.Run:
    db_result = models.Run(
        text=result.text,
        is_corresponding=result.is_corresponding,
        temperature=result.temperature,
        systole_pressure=result.systole_pressure,
        finished=result.finished,
        type=result.type,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    logger.debug(f"Saved run to DB: <{result}>")
    return db_result


def create_patient(db: Session, patient: schemas.Patient) -> models.Patient:
    dict_patient = patient.dict()
    dict_patient.pop("id_")
    db_patient = models.Patient(**dict_patient)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_runs_stat(db: Session) -> Tuple[int, float]:
    runs = db.query(models.RunNew).all()

    total_runs_count = len(runs)

    runs: List[schemas.RunNew] = [
        schemas.RunNew(text=run.text, result=schemas.FeaturesResult.parse_obj(json.loads(run.result))) for run in runs
    ]

    run_ratios = [
        len(run.result.found_features) / (len(run.result.found_features) + len(run.result.missing_features))
        for run in runs
    ]
    logger.debug(run_ratios)
    if total_runs_count == 0:
        return (0, 0.0)
    return (total_runs_count, sum(run_ratios) / total_runs_count)


def get_run(db: Session, run_id: int) -> schemas.Run:
    db_run = db.query(models.Run).get(run_id)
    logger.debug(db_run.updated_at)
    return schemas.Run(
        text=db_run.text,
        is_corresponding=db_run.is_corresponding,
        temperature=db_run.temperature,
        systole_pressure=db_run.systole_pressure,
        diastole_pressure=db_run.diastole_pressure,
        finished=db_run.finished,
        type=db_run.type,
        run_id=hashids_.to_hash_id(db_run.id),
    )


def create_run(db: Session, input: schemas.TextInput) -> models.Run:
    db_run = models.Run(text=input.text, type=input.type)
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def update_run(db: Session, run_id: int, result: schemas.Run) -> models.Run:
    db_run: models.Run = db.query(models.Run).get(run_id)
    db_run.is_corresponding = result.is_corresponding
    db_run.temperature = result.temperature
    db_run.systole_pressure = result.systole_pressure
    db_run.diastole_pressure = result.diastole_pressure
    db_run.finished = result.finished
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def save_text_and_find_result(db: Session, text: str, result: schemas.FeaturesResult) -> models.RunNew:
    db_run = models.RunNew(text=text, result=result.json())
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def get_new_runs_history(db: Session, count: int = 10, offset: int = 0) -> List[schemas.RunNew]:
    results: list[models.RunNew] = (
        db.query(models.RunNew).order_by(models.RunNew.id.desc()).offset(offset).limit(count).all()
    )
    logger.debug(type(results[0].result))
    logger.debug(results[0].result)
    return [
        schemas.RunNew(
            text=result.text,
            result=schemas.FeaturesResult.parse_obj(json.loads(result.result)),
        )
        for result in results
    ]
