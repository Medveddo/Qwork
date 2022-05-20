import sys

from apscheduler.schedulers.background import BlockingScheduler

# from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from app.tasks import say_something


def run_scheduler(args):
    scheduler = BlockingScheduler()
    scheduler.add_job(
        say_something.send,
        CronTrigger.from_crontab("*/15 * * * *"),
    )
    # scheduler.add_job(
    #     say_something.send,
    #     IntervalTrigger(seconds=15),
    # )

    try:
        logger.info(f"Starting APScheduler with {len(scheduler.get_jobs())} job")
        scheduler.start()
    except KeyboardInterrupt:
        logger.debug("Keyboard interrupt. Shutting down scheduler ...")
        scheduler.shutdown()

    logger.debug("Scheduler has been shut down")
    return 0


if __name__ == "__main__":
    sys.exit(run_scheduler(sys.argv))
