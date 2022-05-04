import datetime

import dramatiq
from loguru import logger

from app.dramatiq import DRAMATIQ_BROKER
from app.database import SessionLocal
from sqlalchemy.orm.session import Session


@dramatiq.actor(broker=DRAMATIQ_BROKER)
def say_something():
    print(f" {datetime.datetime.utcnow()} I'm fine!")


@dramatiq.actor(broker=DRAMATIQ_BROKER)
def process_run(run_id: int) -> None:
    db: Session = SessionLocal()

    try:
        logger.critical(run_id)
        logger.success(db.is_active)
    finally:
        db.close()
