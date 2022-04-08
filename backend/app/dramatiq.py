import os

from dramatiq.brokers.redis import RedisBroker

DRAMATIQ_REDIS_BROKER = RedisBroker(
    url=os.getenv("DRAMATIQ_BROKER_URL", "redis://localhost:6379")
)

DRAMATIQ_BROKER = DRAMATIQ_REDIS_BROKER
