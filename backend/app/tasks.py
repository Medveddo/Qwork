import datetime

import dramatiq

from app.dramatiq import DRAMATIQ_BROKER


@dramatiq.actor(broker=DRAMATIQ_BROKER)
def say_something():
    print(f" {datetime.datetime.utcnow()} I'm fine!")
