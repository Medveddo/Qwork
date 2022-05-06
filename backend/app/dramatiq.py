import os

import aioredis
from dramatiq.brokers.redis import RedisBroker
from loguru import logger

DRAMATIQ_REDIS_BROKER = RedisBroker(
    url=os.getenv("DRAMATIQ_BROKER_URL", "redis://localhost:6379")
)

DRAMATIQ_BROKER = DRAMATIQ_REDIS_BROKER


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
