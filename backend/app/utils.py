from app.database import health_check_database
from app.dramatiq import health_check_redis


async def health_check_app() -> bool:
    redis_healthy = await health_check_redis()
    if not redis_healthy:
        return False

    db_healthy = health_check_database()
    if not db_healthy:
        return False

    return True
