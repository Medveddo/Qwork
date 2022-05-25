import datetime

import dramatiq
from loguru import logger
from sqlalchemy.orm.session import Session

from app import crud, schemas
from app.database import SessionLocal
from app.dramatiq import DRAMATIQ_BROKER
from app.nlp.services.controller import controller_service


@dramatiq.actor(broker=DRAMATIQ_BROKER, store_results=True)
def say_something():
    print(f"{datetime.datetime.utcnow()} I'm fine!")
    return f"{datetime.datetime.utcnow()} I'm fine!"


@dramatiq.actor(broker=DRAMATIQ_BROKER)
def process_run(run_id: int) -> None:
    logger.info(f"Start processing Run#{run_id}")

    db: Session = SessionLocal()
    logger.info("Opened session to DB")

    try:
        run = crud.get_run(db, run_id)
        logger.debug(run)
        logger.debug(run)
        logger.debug(run.text)
        logger.debug(run.type)
        result = controller_service.process_text_with_related_clinrecs(schemas.TextInput(text=run.text, type=run.type))

        crud.update_run_result(db, run_id, result)
        logger.success(f"Processed run #{run_id}: {result}")
    finally:
        db.close()
        logger.debug("Closed session to DB.")
