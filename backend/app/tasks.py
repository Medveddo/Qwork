import datetime

import dramatiq
from loguru import logger
from sqlalchemy.orm.session import Session

from app import crud, schemas
from app.database import SessionLocal
from app.dramatiq import DRAMATIQ_BROKER


@dramatiq.actor(broker=DRAMATIQ_BROKER, store_results=True)
def say_something():
    print(f"{datetime.datetime.utcnow()} I'm fine!")
    return f"{datetime.datetime.utcnow()} I'm fine!"


@dramatiq.actor(broker=DRAMATIQ_BROKER)
def process_run(run_id: int) -> None:
    logger.info(f"Start processing Run#{run_id}")
    from app.nlp import verify_temp_and_blood_pressure

    db: Session = SessionLocal()
    logger.info("Opened session to DB")

    try:
        run = crud.get_run(db, run_id)

        result = verify_temp_and_blood_pressure(run.text)

        result_ = schemas.Run(
            text=run.text,
            is_corresponding=result.is_correspond,
            temperature=result.temperature,
            systole_pressure=result.systole_pressure,
            diastole_pressure=result.diastole_pressure,
            type=run.type,
            finished=True,
        )
        logger.debug(f"{result_=}")

        crud.update_run(db, run_id, result_)
        logger.success(f"Processed run #{run_id}: {result_}")
    finally:
        db.close()
        logger.debug("Closed session to DB.")
