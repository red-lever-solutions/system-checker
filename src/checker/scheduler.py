from .mylog import log
from .checkerlog import log_checker_result

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.asyncio import AsyncIOExecutor
import asyncio

_scheduler = AsyncIOScheduler(executors={
    "asyncio": AsyncIOExecutor()
})

def _make_checker_fun(checker):
    def cf():
        log_checker_result(checker[0], checker[2]())
    return cf

def _add_checker(checker):
    log.debug("Adding schedule job for %s", checker[0])
    _scheduler.add_job(
        _make_checker_fun(checker),
        IntervalTrigger(seconds=checker[1]),
        id=checker[0],
        name=checker[0],
        replace_existing=True,
        coalesce=True,
        executor="asyncio")

def set_checkers(checkers):
    log.debug("Removing all schedule jobs")
    _scheduler.remove_all_jobs()
    for checker in checkers:
        _add_checker(checker)

def run():
    log.info("Starting checker scheduler")
    _scheduler.start()
    asyncio.get_event_loop().run_forever()
    log.info("Stopped checker scheduler")
