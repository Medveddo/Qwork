import os

import aioredis
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends.redis import RedisBackend
from loguru import logger

REDIS_RESULT_BACKEND = RedisBackend(
    url=os.getenv("DRAMATIQ_BROKER_URL", "redis://localhost:6379")
)

DRAMATIQ_REDIS_BROKER = RedisBroker(
    url=os.getenv("DRAMATIQ_BROKER_URL", "redis://localhost:6379")
)
DRAMATIQ_REDIS_BROKER.add_middleware(Results(backend=REDIS_RESULT_BACKEND))

DRAMATIQ_BROKER = DRAMATIQ_REDIS_BROKER

dramatiq.set_broker(DRAMATIQ_BROKER)


async def health_check_redis() -> bool:
    redis = aioredis.Redis.from_url(
        os.getenv("DRAMATIQ_BROKER_URL", "redis://localhost:6379")
    )
    try:
        await redis.ping()
        await redis.close()
        return True
    except Exception as e:
        logger.error(e)
        return False
